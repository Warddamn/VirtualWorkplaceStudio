import { test } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import Database from "better-sqlite3";
import { openStore } from "../src/db.js";

/**
 * A database created by the v0.1 (MVP) schema must open cleanly under v0.2:
 * new columns are ALTERed in with sane defaults and the legacy `credits`
 * column is kept (unused) for migration compat.
 */
test("a v1 database migrates in place to the v2 schema", () => {
  const dataDir = fs.mkdtempSync(path.join(os.tmpdir(), "cover-backend-migrate-"));
  try {
    // Recreate the exact v0.1 tables, with one device and one finished job.
    const db = new Database(path.join(dataDir, "app.db"));
    db.exec(`
      CREATE TABLE jobs (
        id TEXT PRIMARY KEY, device_id TEXT NOT NULL, song_name TEXT NOT NULL,
        style_id TEXT, style_prompt TEXT NOT NULL,
        status TEXT NOT NULL CHECK (status IN ('queued','processing','succeeded','failed')),
        engine TEXT NOT NULL, input_path TEXT NOT NULL, output_path TEXT, error TEXT,
        created_at TEXT NOT NULL, updated_at TEXT NOT NULL
      );
      CREATE INDEX idx_jobs_device ON jobs (device_id, created_at DESC);
      CREATE TABLE devices (
        device_id TEXT PRIMARY KEY, expo_push_token TEXT,
        credits INTEGER NOT NULL DEFAULT 10, created_at TEXT NOT NULL
      );
      INSERT INTO devices VALUES ('old-dev', NULL, 7, '2026-01-01T00:00:00.000Z');
      INSERT INTO jobs VALUES ('old-job', 'old-dev', 'Old Song', NULL, 'warm folk',
        'succeeded', 'mock', '/in.wav', '/out.wav', NULL,
        '2026-01-01T00:00:00.000Z', '2026-01-01T00:00:00.000Z');
    `);
    db.close();

    const store = openStore(dataDir);
    try {
      const device = store.getDevice("old-dev");
      assert.ok(device);
      assert.equal(device.tier, "free"); // migrated default
      assert.equal(device.credits, 7); // legacy column preserved, unused

      const job = store.getJob("old-job");
      assert.ok(job);
      assert.equal(job.takes_requested, 1);
      assert.equal(job.selected_take, 0);
      assert.equal(job.instrumental, 0);
      assert.equal(job.parent_job_id, null);
      assert.equal(job.refine_note, null);
      assert.equal(store.listTakes("old-job").length, 0); // pre-takes job

      // A January job never counts against the current month's quota.
      assert.equal(store.countJobsThisMonth("old-dev"), 0);

      // The v2 tables exist and work.
      store.ensureTakes("old-job", 1);
      assert.equal(store.listTakes("old-job").length, 1);
      assert.equal(store.countCustomStylesByDevice("old-dev"), 0);
    } finally {
      store.close();
    }
  } finally {
    fs.rmSync(dataDir, { recursive: true, force: true });
  }
});
