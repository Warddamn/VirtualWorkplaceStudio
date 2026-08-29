import Database from "better-sqlite3";
import fs from "node:fs";
import path from "node:path";
import { TIER_CONFIG, currentUtcMonthPrefix, type Tier } from "./tiers.js";

export type JobStatus = "queued" | "processing" | "succeeded" | "failed";
export type TakeStatus = "pending" | "succeeded" | "failed";

/** Raw row shape of the `jobs` table. */
export interface JobRow {
  id: string;
  device_id: string;
  song_name: string;
  style_id: string | null;
  style_prompt: string;
  status: JobStatus;
  engine: string;
  input_path: string;
  output_path: string | null;
  error: string | null;
  takes_requested: number;
  selected_take: number;
  instrumental: number; // sqlite boolean (0/1)
  parent_job_id: string | null;
  refine_note: string | null;
  created_at: string;
  updated_at: string;
}

/** Raw row shape of the `takes` table (one per generated candidate). */
export interface TakeRow {
  job_id: string;
  idx: number;
  status: TakeStatus;
  output_path: string | null;
  error: string | null;
}

/** Raw row shape of the `devices` table. `credits` is legacy (unused since v0.2). */
export interface DeviceRow {
  device_id: string;
  expo_push_token: string | null;
  credits: number;
  tier: Tier;
  created_at: string;
}

/** Raw row shape of the `custom_styles` table. */
export interface CustomStyleRow {
  id: string;
  device_id: string;
  name: string;
  emoji: string;
  style_prompt: string;
  created_at: string;
}

/** API-facing Job shape: camelCased jobs row without local filesystem paths. */
export interface Job {
  id: string;
  deviceId: string;
  songName: string;
  styleId: string | null;
  stylePrompt: string;
  status: JobStatus;
  engine: string;
  error: string | null;
  takes: { idx: number; status: TakeStatus }[];
  selectedTake: number;
  takesRequested: number;
  instrumental: boolean;
  parentJobId: string | null;
  refineNote: string | null;
  createdAt: string;
  updatedAt: string;
}

/** API-facing device shape: tier + monthly quota (raw credits are gone since v0.2). */
export interface ApiDevice {
  deviceId: string;
  tier: Tier;
  monthlyQuota: number;
  usedThisMonth: number;
  remaining: number;
}

export function toApiJob(row: JobRow, takes: TakeRow[] = []): Job {
  return {
    id: row.id,
    deviceId: row.device_id,
    songName: row.song_name,
    styleId: row.style_id,
    stylePrompt: row.style_prompt,
    status: row.status,
    engine: row.engine,
    error: row.error,
    takes: takes.map((t) => ({ idx: t.idx, status: t.status })),
    selectedTake: row.selected_take,
    takesRequested: row.takes_requested,
    instrumental: row.instrumental === 1,
    parentJobId: row.parent_job_id,
    refineNote: row.refine_note,
    createdAt: row.created_at,
    updatedAt: row.updated_at,
  };
}

export function toApiDevice(row: DeviceRow, usedThisMonth: number): ApiDevice {
  const { monthlyQuota } = TIER_CONFIG[row.tier];
  return {
    deviceId: row.device_id,
    tier: row.tier,
    monthlyQuota,
    usedThisMonth,
    remaining: Math.max(0, monthlyQuota - usedThisMonth),
  };
}

/** API-facing custom style shape. */
export interface CustomStyle {
  id: string;
  deviceId: string;
  name: string;
  emoji: string;
  stylePrompt: string;
  createdAt: string;
}

export function toApiCustomStyle(row: CustomStyleRow): CustomStyle {
  return {
    id: row.id,
    deviceId: row.device_id,
    name: row.name,
    emoji: row.emoji,
    stylePrompt: row.style_prompt,
    createdAt: row.created_at,
  };
}

const SCHEMA = `
CREATE TABLE IF NOT EXISTS jobs (
  id TEXT PRIMARY KEY,
  device_id TEXT NOT NULL,
  song_name TEXT NOT NULL,
  style_id TEXT,
  style_prompt TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('queued','processing','succeeded','failed')),
  engine TEXT NOT NULL,
  input_path TEXT NOT NULL,
  output_path TEXT,
  error TEXT,
  takes_requested INTEGER NOT NULL DEFAULT 1,
  selected_take INTEGER NOT NULL DEFAULT 0,
  instrumental INTEGER NOT NULL DEFAULT 0,
  parent_job_id TEXT,
  refine_note TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_jobs_device ON jobs (device_id, created_at DESC);

CREATE TABLE IF NOT EXISTS takes (
  job_id TEXT NOT NULL,
  idx INTEGER NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('pending','succeeded','failed')),
  output_path TEXT,
  error TEXT,
  PRIMARY KEY (job_id, idx)
);

CREATE TABLE IF NOT EXISTS devices (
  device_id TEXT PRIMARY KEY,
  expo_push_token TEXT,
  credits INTEGER NOT NULL DEFAULT 10,
  tier TEXT NOT NULL DEFAULT 'free' CHECK (tier IN ('free','plus','studio')),
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS custom_styles (
  id TEXT PRIMARY KEY,
  device_id TEXT NOT NULL,
  name TEXT NOT NULL,
  emoji TEXT NOT NULL DEFAULT '',
  style_prompt TEXT NOT NULL,
  created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_custom_styles_device
  ON custom_styles (device_id, created_at DESC);
`;

/**
 * v0.1 -> v0.2 column migrations for databases created before the v2 schema.
 * (CREATE TABLE IF NOT EXISTS won't add columns to an existing table.)
 */
const COLUMN_MIGRATIONS: { table: string; column: string; ddl: string }[] = [
  { table: "devices", column: "tier", ddl: "ALTER TABLE devices ADD COLUMN tier TEXT NOT NULL DEFAULT 'free'" },
  { table: "jobs", column: "takes_requested", ddl: "ALTER TABLE jobs ADD COLUMN takes_requested INTEGER NOT NULL DEFAULT 1" },
  { table: "jobs", column: "selected_take", ddl: "ALTER TABLE jobs ADD COLUMN selected_take INTEGER NOT NULL DEFAULT 0" },
  { table: "jobs", column: "instrumental", ddl: "ALTER TABLE jobs ADD COLUMN instrumental INTEGER NOT NULL DEFAULT 0" },
  { table: "jobs", column: "parent_job_id", ddl: "ALTER TABLE jobs ADD COLUMN parent_job_id TEXT" },
  { table: "jobs", column: "refine_note", ddl: "ALTER TABLE jobs ADD COLUMN refine_note TEXT" },
];

function migrateColumns(db: Database.Database): void {
  for (const { table, column, ddl } of COLUMN_MIGRATIONS) {
    const cols = db.pragma(`table_info(${table})`) as { name: string }[];
    if (!cols.some((c) => c.name === column)) db.exec(ddl);
  }
}

export interface Store {
  db: Database.Database;
  insertJob(row: JobRow): void;
  getJob(id: string): JobRow | undefined;
  listJobsByDevice(deviceId: string): JobRow[];
  setJobStatus(id: string, status: JobStatus, patch?: { outputPath?: string; error?: string }): void;
  /** Set which take the audio endpoint serves by default (+ keep output_path in sync). */
  setSelectedTake(jobId: string, idx: number, outputPath: string | null): void;
  /** Rows that should be re-queued after a restart (queued or interrupted mid-processing). */
  jobsToRequeue(): JobRow[];
  /** Create pending take rows 0..count-1 for a job (idempotent — restart-safe). */
  ensureTakes(jobId: string, count: number): void;
  listTakes(jobId: string): TakeRow[];
  getTake(jobId: string, idx: number): TakeRow | undefined;
  setTakeStatus(
    jobId: string,
    idx: number,
    status: TakeStatus,
    patch?: { outputPath?: string; error?: string },
  ): void;
  upsertDevice(deviceId: string, expoPushToken?: string | null): DeviceRow;
  getDevice(deviceId: string): DeviceRow | undefined;
  /** Ensure a device row exists (free tier by default) and return it. */
  ensureDevice(deviceId: string): DeviceRow;
  setDeviceTier(deviceId: string, tier: Tier): DeviceRow;
  /**
   * Jobs created by the device in the current UTC calendar month, excluding
   * `failed` ones — this is the quota consumption count. Queued/processing jobs
   * count too (that's the v1 reservation-against-active-jobs semantics: an
   * in-flight job holds a quota slot and releases it only by failing).
   */
  countJobsThisMonth(deviceId: string): number;
  insertCustomStyle(row: CustomStyleRow): void;
  listCustomStylesByDevice(deviceId: string): CustomStyleRow[];
  getCustomStyle(id: string): CustomStyleRow | undefined;
  countCustomStylesByDevice(deviceId: string): number;
  /** Delete a device's custom style; false when the id isn't that device's. */
  deleteCustomStyle(id: string, deviceId: string): boolean;
  close(): void;
}

export function openStore(dataDir: string): Store {
  fs.mkdirSync(dataDir, { recursive: true });
  fs.mkdirSync(path.join(dataDir, "uploads"), { recursive: true });
  fs.mkdirSync(path.join(dataDir, "outputs"), { recursive: true });

  const db = new Database(path.join(dataDir, "app.db"));
  db.pragma("journal_mode = WAL");
  // Fresh databases get the full v2 schema; pre-existing v1 tables pass through
  // CREATE TABLE IF NOT EXISTS untouched and get the new columns ALTERed in.
  db.exec(SCHEMA);
  migrateColumns(db);

  const insertJobStmt = db.prepare(
    `INSERT INTO jobs (id, device_id, song_name, style_id, style_prompt, status, engine,
                       input_path, output_path, error, takes_requested, selected_take,
                       instrumental, parent_job_id, refine_note, created_at, updated_at)
     VALUES (@id, @device_id, @song_name, @style_id, @style_prompt, @status, @engine,
             @input_path, @output_path, @error, @takes_requested, @selected_take,
             @instrumental, @parent_job_id, @refine_note, @created_at, @updated_at)`,
  );
  const getJobStmt = db.prepare("SELECT * FROM jobs WHERE id = ?");
  const listJobsStmt = db.prepare(
    "SELECT * FROM jobs WHERE device_id = ? ORDER BY created_at DESC, id DESC",
  );
  const setStatusStmt = db.prepare(
    `UPDATE jobs SET status = @status,
                     output_path = COALESCE(@output_path, output_path),
                     error = @error,
                     updated_at = @updated_at
     WHERE id = @id`,
  );
  const setSelectedTakeStmt = db.prepare(
    `UPDATE jobs SET selected_take = @selected_take,
                     output_path = COALESCE(@output_path, output_path),
                     updated_at = @updated_at
     WHERE id = @id`,
  );
  const requeueSelectStmt = db.prepare(
    "SELECT * FROM jobs WHERE status IN ('queued','processing') ORDER BY created_at ASC, id ASC",
  );
  const insertTakeStmt = db.prepare(
    `INSERT OR IGNORE INTO takes (job_id, idx, status, output_path, error)
     VALUES (?, ?, 'pending', NULL, NULL)`,
  );
  const listTakesStmt = db.prepare("SELECT * FROM takes WHERE job_id = ? ORDER BY idx ASC");
  const getTakeStmt = db.prepare("SELECT * FROM takes WHERE job_id = ? AND idx = ?");
  const setTakeStatusStmt = db.prepare(
    `UPDATE takes SET status = @status,
                      output_path = COALESCE(@output_path, output_path),
                      error = @error
     WHERE job_id = @job_id AND idx = @idx`,
  );
  const getDeviceStmt = db.prepare("SELECT * FROM devices WHERE device_id = ?");
  const insertDeviceStmt = db.prepare(
    `INSERT INTO devices (device_id, expo_push_token, credits, created_at)
     VALUES (@device_id, @expo_push_token, 10, @created_at)
     ON CONFLICT(device_id) DO UPDATE SET
       expo_push_token = COALESCE(excluded.expo_push_token, devices.expo_push_token)`,
  );
  const setTierStmt = db.prepare("UPDATE devices SET tier = ? WHERE device_id = ?");
  const countMonthStmt = db.prepare(
    `SELECT COUNT(*) AS n FROM jobs
     WHERE device_id = ? AND status != 'failed' AND substr(created_at, 1, 7) = ?`,
  );
  const insertCustomStyleStmt = db.prepare(
    `INSERT INTO custom_styles (id, device_id, name, emoji, style_prompt, created_at)
     VALUES (@id, @device_id, @name, @emoji, @style_prompt, @created_at)`,
  );
  const listCustomStylesStmt = db.prepare(
    // rowid tie-break: same-millisecond inserts still list newest first.
    "SELECT * FROM custom_styles WHERE device_id = ? ORDER BY created_at DESC, rowid DESC",
  );
  const getCustomStyleStmt = db.prepare("SELECT * FROM custom_styles WHERE id = ?");
  const countCustomStylesStmt = db.prepare(
    "SELECT COUNT(*) AS n FROM custom_styles WHERE device_id = ?",
  );
  const deleteCustomStyleStmt = db.prepare(
    "DELETE FROM custom_styles WHERE id = ? AND device_id = ?",
  );

  return {
    db,
    insertJob(row) {
      insertJobStmt.run(row);
    },
    getJob(id) {
      return getJobStmt.get(id) as JobRow | undefined;
    },
    listJobsByDevice(deviceId) {
      return listJobsStmt.all(deviceId) as JobRow[];
    },
    setJobStatus(id, status, patch = {}) {
      setStatusStmt.run({
        id,
        status,
        output_path: patch.outputPath ?? null,
        error: patch.error ?? null,
        updated_at: new Date().toISOString(),
      });
    },
    setSelectedTake(jobId, idx, outputPath) {
      setSelectedTakeStmt.run({
        id: jobId,
        selected_take: idx,
        output_path: outputPath,
        updated_at: new Date().toISOString(),
      });
    },
    jobsToRequeue() {
      return requeueSelectStmt.all() as JobRow[];
    },
    ensureTakes(jobId, count) {
      for (let idx = 0; idx < count; idx++) insertTakeStmt.run(jobId, idx);
    },
    listTakes(jobId) {
      return listTakesStmt.all(jobId) as TakeRow[];
    },
    getTake(jobId, idx) {
      return getTakeStmt.get(jobId, idx) as TakeRow | undefined;
    },
    setTakeStatus(jobId, idx, status, patch = {}) {
      setTakeStatusStmt.run({
        job_id: jobId,
        idx,
        status,
        output_path: patch.outputPath ?? null,
        error: patch.error ?? null,
      });
    },
    upsertDevice(deviceId, expoPushToken) {
      insertDeviceStmt.run({
        device_id: deviceId,
        expo_push_token: expoPushToken ?? null,
        created_at: new Date().toISOString(),
      });
      return getDeviceStmt.get(deviceId) as DeviceRow;
    },
    getDevice(deviceId) {
      return getDeviceStmt.get(deviceId) as DeviceRow | undefined;
    },
    ensureDevice(deviceId) {
      const existing = getDeviceStmt.get(deviceId) as DeviceRow | undefined;
      if (existing) return existing;
      return this.upsertDevice(deviceId, null);
    },
    setDeviceTier(deviceId, tier) {
      this.ensureDevice(deviceId);
      setTierStmt.run(tier, deviceId);
      return getDeviceStmt.get(deviceId) as DeviceRow;
    },
    countJobsThisMonth(deviceId) {
      const month = currentUtcMonthPrefix();
      return (countMonthStmt.get(deviceId, month) as { n: number }).n;
    },
    insertCustomStyle(row) {
      insertCustomStyleStmt.run(row);
    },
    listCustomStylesByDevice(deviceId) {
      return listCustomStylesStmt.all(deviceId) as CustomStyleRow[];
    },
    getCustomStyle(id) {
      return getCustomStyleStmt.get(id) as CustomStyleRow | undefined;
    },
    countCustomStylesByDevice(deviceId) {
      return (countCustomStylesStmt.get(deviceId) as { n: number }).n;
    },
    deleteCustomStyle(id, deviceId) {
      return deleteCustomStyleStmt.run(id, deviceId).changes > 0;
    },
    close() {
      db.close();
    },
  };
}
