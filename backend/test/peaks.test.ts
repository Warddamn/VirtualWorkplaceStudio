import { test } from "node:test";
import assert from "node:assert/strict";
import { createTestApp, destroyTestApp, submitCover, waitForJob } from "./helpers.js";
import { computeWavPeaks, PEAK_BUCKETS } from "../src/peaks.js";
import { synthesizeMelodyWav } from "../src/engines/mock.js";

test("computeWavPeaks parses 16-bit PCM WAV into 0..1 RMS buckets", () => {
  const peaks = computeWavPeaks(synthesizeMelodyWav());
  assert.ok(peaks, "mock WAV must be parseable");
  assert.equal(peaks.length, PEAK_BUCKETS);
  for (const p of peaks) assert.ok(p >= 0 && p <= 1, `peak out of range: ${p}`);
  // The sine melody plays at ~0.35 amplitude — buckets carry real energy.
  assert.ok(Math.max(...peaks) > 0.1);

  // Non-WAV data is unparseable -> null (the route then answers { peaks: [] }).
  assert.equal(computeWavPeaks(Buffer.from("definitely not a wav file")), null);
  assert.equal(computeWavPeaks(Buffer.alloc(0)), null);
});

test("GET /covers/:id/peaks serves peaks for a mock output", async () => {
  const { app, dataDir } = await createTestApp({ mockDelayMs: 25 });
  try {
    const res = await submitCover(app, {
      deviceId: "dev-peaks",
      songName: "Peaky Song",
      styleId: "lofi-chill",
    });
    assert.equal(res.statusCode, 201, res.body);
    const jobId = (res.json() as { job: { id: string } }).job.id;

    const job = await waitForJob(app, jobId);
    assert.equal(job["status"], "succeeded");

    const peaksRes = await app.inject({ method: "GET", url: `/covers/${jobId}/peaks` });
    assert.equal(peaksRes.statusCode, 200);
    const { peaks } = peaksRes.json() as { peaks: number[] };
    assert.equal(peaks.length, PEAK_BUCKETS);
    for (const p of peaks) assert.ok(p >= 0 && p <= 1);
    assert.ok(Math.max(...peaks) > 0.1);

    // Explicit ?take= works like the audio route.
    const takeRes = await app.inject({ method: "GET", url: `/covers/${jobId}/peaks?take=0` });
    assert.equal(takeRes.statusCode, 200);
    assert.deepEqual(takeRes.json(), { peaks });
    const missingTake = await app.inject({ method: "GET", url: `/covers/${jobId}/peaks?take=5` });
    assert.equal(missingTake.statusCode, 404);

    // Unknown job -> 404.
    const unknown = await app.inject({ method: "GET", url: "/covers/nope/peaks" });
    assert.equal(unknown.statusCode, 404);

    // Non-WAV outputs answer 200 { peaks: [] } so the client can fall back to a
    // plain progress bar. (Simulate an mp3-producing engine by renaming the path.)
    app.store.db
      .prepare("UPDATE takes SET output_path = ? WHERE job_id = ? AND idx = 0")
      .run("/tmp/not-a-real-file.mp3", jobId);
    const nonWav = await app.inject({ method: "GET", url: `/covers/${jobId}/peaks` });
    assert.equal(nonWav.statusCode, 200);
    assert.deepEqual(nonWav.json(), { peaks: [] });
  } finally {
    await destroyTestApp(app, dataDir);
  }
});
