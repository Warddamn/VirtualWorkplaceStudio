import Database from "better-sqlite3";
import fs from "node:fs";
import path from "node:path";

export type JobStatus = "queued" | "processing" | "succeeded" | "failed";

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
  created_at: string;
  updated_at: string;
}

/** Raw row shape of the `devices` table. */
export interface DeviceRow {
  device_id: string;
  expo_push_token: string | null;
  credits: number;
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
  createdAt: string;
  updatedAt: string;
}

export function toApiJob(row: JobRow): Job {
  return {
    id: row.id,
    deviceId: row.device_id,
    songName: row.song_name,
    styleId: row.style_id,
    stylePrompt: row.style_prompt,
    status: row.status,
    engine: row.engine,
    error: row.error,
    createdAt: row.created_at,
    updatedAt: row.updated_at,
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
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_jobs_device ON jobs (device_id, created_at DESC);

CREATE TABLE IF NOT EXISTS devices (
  device_id TEXT PRIMARY KEY,
  expo_push_token TEXT,
  credits INTEGER NOT NULL DEFAULT 10,
  created_at TEXT NOT NULL
);
`;

export interface Store {
  db: Database.Database;
  insertJob(row: JobRow): void;
  getJob(id: string): JobRow | undefined;
  listJobsByDevice(deviceId: string): JobRow[];
  setJobStatus(id: string, status: JobStatus, patch?: { outputPath?: string; error?: string }): void;
  /** Rows that should be re-queued after a restart (queued or interrupted mid-processing). */
  jobsToRequeue(): JobRow[];
  upsertDevice(deviceId: string, expoPushToken?: string | null): DeviceRow;
  getDevice(deviceId: string): DeviceRow | undefined;
  /** Ensure a device row exists (10 default credits) and return it. */
  ensureDevice(deviceId: string): DeviceRow;
  /** Jobs currently queued or processing for a device — each will consume a credit on success. */
  countActiveJobsByDevice(deviceId: string): number;
  decrementCredits(deviceId: string): void;
  close(): void;
}

export function openStore(dataDir: string): Store {
  fs.mkdirSync(dataDir, { recursive: true });
  fs.mkdirSync(path.join(dataDir, "uploads"), { recursive: true });
  fs.mkdirSync(path.join(dataDir, "outputs"), { recursive: true });

  const db = new Database(path.join(dataDir, "app.db"));
  db.pragma("journal_mode = WAL");
  db.exec(SCHEMA);

  const insertJobStmt = db.prepare(
    `INSERT INTO jobs (id, device_id, song_name, style_id, style_prompt, status, engine,
                       input_path, output_path, error, created_at, updated_at)
     VALUES (@id, @device_id, @song_name, @style_id, @style_prompt, @status, @engine,
             @input_path, @output_path, @error, @created_at, @updated_at)`,
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
  const requeueSelectStmt = db.prepare(
    "SELECT * FROM jobs WHERE status IN ('queued','processing') ORDER BY created_at ASC, id ASC",
  );
  const getDeviceStmt = db.prepare("SELECT * FROM devices WHERE device_id = ?");
  const insertDeviceStmt = db.prepare(
    `INSERT INTO devices (device_id, expo_push_token, credits, created_at)
     VALUES (@device_id, @expo_push_token, 10, @created_at)
     ON CONFLICT(device_id) DO UPDATE SET
       expo_push_token = COALESCE(excluded.expo_push_token, devices.expo_push_token)`,
  );
  const decrementStmt = db.prepare(
    "UPDATE devices SET credits = credits - 1 WHERE device_id = ? AND credits > 0",
  );
  const countActiveStmt = db.prepare(
    "SELECT COUNT(*) AS n FROM jobs WHERE device_id = ? AND status IN ('queued','processing')",
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
    jobsToRequeue() {
      return requeueSelectStmt.all() as JobRow[];
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
    countActiveJobsByDevice(deviceId) {
      return (countActiveStmt.get(deviceId) as { n: number }).n;
    },
    decrementCredits(deviceId) {
      decrementStmt.run(deviceId);
    },
    close() {
      db.close();
    },
  };
}
