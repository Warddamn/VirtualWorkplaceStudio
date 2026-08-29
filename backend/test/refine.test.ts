import { test } from "node:test";
import assert from "node:assert/strict";
import { createTestApp, destroyTestApp, submitCover, waitForJob } from "./helpers.js";

// No ANTHROPIC_API_KEY in tests -> the deterministic merge path runs.
delete process.env.ANTHROPIC_API_KEY;

test("refine merges the note (fallback path), links the parent and consumes quota", async () => {
  const { app, dataDir } = await createTestApp({ mockDelayMs: 25 });
  try {
    await app.inject({ method: "POST", url: "/devices", payload: { deviceId: "dev-refine" } });

    // v1: the source cover (free tier: 3 covers/month, 1 take).
    const sourceRes = await submitCover(app, {
      deviceId: "dev-refine",
      songName: "Refinable Song",
      customStylePrompt: "warm acoustic folk, fingerpicked guitar",
    });
    assert.equal(sourceRes.statusCode, 201, sourceRes.body);
    const sourceId = (sourceRes.json() as { job: { id: string } }).job.id;
    const source = await waitForJob(app, sourceId);
    assert.equal(source["status"], "succeeded");

    // v2 = refine of v1 (deterministic merge — no ANTHROPIC_API_KEY in tests).
    const refine1 = await app.inject({
      method: "POST",
      url: `/covers/${sourceId}/refine`,
      payload: { note: "more piano" },
    });
    assert.equal(refine1.statusCode, 201, refine1.body);
    const child1 = (refine1.json() as { job: Record<string, unknown> }).job;
    // Deterministic merge: "<source prompt>, <note>".
    assert.equal(child1["stylePrompt"], "warm acoustic folk, fingerpicked guitar, more piano");
    assert.equal(child1["parentJobId"], sourceId);
    assert.equal(child1["refineNote"], "more piano");
    assert.equal(child1["songName"], "Refinable Song");
    assert.equal(child1["styleId"], null);
    assert.equal(child1["takesRequested"], 1); // free tier max
    assert.equal(child1["instrumental"], false);
    const child1Done = await waitForJob(app, child1["id"] as string);
    assert.equal(child1Done["status"], "succeeded");

    // Refinements are generations: quota went 1 -> 2.
    const dev = await app.inject({ method: "GET", url: "/devices/dev-refine" });
    const devBody = (dev.json() as { device: { usedThisMonth: number; remaining: number } }).device;
    assert.equal(devBody.usedThisMonth, 2);
    assert.equal(devBody.remaining, 1);

    // v3 = refine of v2 — the chain keeps linking.
    const refine2 = await app.inject({
      method: "POST",
      url: `/covers/${child1["id"] as string}/refine`,
      payload: { note: "slower and sadder" },
    });
    assert.equal(refine2.statusCode, 201, refine2.body);
    const child2 = (refine2.json() as { job: Record<string, unknown> }).job;
    assert.equal(child2["parentJobId"], child1["id"]);
    assert.equal(
      child2["stylePrompt"],
      "warm acoustic folk, fingerpicked guitar, more piano, slower and sadder",
    );
    await waitForJob(app, child2["id"] as string);

    // Quota exhausted (3/3 on free) — the next refine hits the normal 402.
    const overQuota = await app.inject({
      method: "POST",
      url: `/covers/${sourceId}/refine`,
      payload: { note: "bigger chorus" },
    });
    assert.equal(overQuota.statusCode, 402);
    assert.match((overQuota.json() as { error: string }).error, /quota/i);

    // Validation: unknown job, empty/overlong note, artist-voice note.
    const unknown = await app.inject({
      method: "POST",
      url: "/covers/nope/refine",
      payload: { note: "more piano" },
    });
    assert.equal(unknown.statusCode, 404);
    const empty = await app.inject({
      method: "POST",
      url: `/covers/${sourceId}/refine`,
      payload: { note: "  " },
    });
    assert.equal(empty.statusCode, 400);
    const long = await app.inject({
      method: "POST",
      url: `/covers/${sourceId}/refine`,
      payload: { note: "x".repeat(301) },
    });
    assert.equal(long.statusCode, 400);
    const artist = await app.inject({
      method: "POST",
      url: `/covers/${sourceId}/refine`,
      payload: { note: "in the voice of Adele" },
    });
    assert.equal(artist.statusCode, 400);
    assert.match((artist.json() as { error: string }).error, /voice/i);
  } finally {
    await destroyTestApp(app, dataDir);
  }
});

test("refine keeps the merged prompt within 300 chars and rejects non-succeeded sources", async () => {
  const { app, dataDir } = await createTestApp({ mockDelayMs: 25 });
  try {
    // Long source prompt: the deterministic merge must truncate to <=300.
    const longPrompt = "dreamy synth pads, airy vocals, tape hiss, slow arps, night drive mood, ".repeat(4).slice(0, 290).trim();
    const sourceRes = await submitCover(app, {
      deviceId: "dev-refine-long",
      songName: "Long Prompt Song",
      customStylePrompt: longPrompt,
    });
    assert.equal(sourceRes.statusCode, 201, sourceRes.body);
    const sourceId = (sourceRes.json() as { job: { id: string } }).job.id;
    await waitForJob(app, sourceId);

    const refine = await app.inject({
      method: "POST",
      url: `/covers/${sourceId}/refine`,
      payload: { note: "add sweeping strings and a bigger chorus" },
    });
    assert.equal(refine.statusCode, 201, refine.body);
    const child = (refine.json() as { job: { stylePrompt: string } }).job;
    assert.ok(child.stylePrompt.length <= 300, `merged prompt was ${child.stylePrompt.length} chars`);
    assert.ok(child.stylePrompt.startsWith("dreamy synth pads"));

    // A failed job can't be refined.
    process.env.MOCK_ENGINE_FAIL_TAKES = "0";
    const failRes = await submitCover(app, {
      deviceId: "dev-refine-fail",
      songName: "Failed Song",
      styleId: "kids-choir",
    });
    assert.equal(failRes.statusCode, 201, failRes.body);
    const failedId = (failRes.json() as { job: { id: string } }).job.id;
    const failed = await waitForJob(app, failedId);
    assert.equal(failed["status"], "failed");
    delete process.env.MOCK_ENGINE_FAIL_TAKES;

    const refuseFailed = await app.inject({
      method: "POST",
      url: `/covers/${failedId}/refine`,
      payload: { note: "more piano" },
    });
    assert.equal(refuseFailed.statusCode, 400);
    assert.match((refuseFailed.json() as { error: string }).error, /succeeded/i);
  } finally {
    delete process.env.MOCK_ENGINE_FAIL_TAKES;
    await destroyTestApp(app, dataDir);
  }
});
