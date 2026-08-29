import { test } from "node:test";
import assert from "node:assert/strict";
import {
  buildMultipart,
  createTestApp,
  destroyTestApp,
  sleep,
  tinyWavBuffer,
} from "./helpers.js";

test("full job lifecycle against the mock engine", async () => {
  const { app, dataDir } = await createTestApp();
  try {
    // Health reports the selected engine.
    const health = await app.inject({ method: "GET", url: "/health" });
    assert.equal(health.statusCode, 200);
    assert.deepEqual(health.json(), { ok: true, engine: "mock" });

    // Styles are served (kids-choir first, 8 presets).
    const styles = await app.inject({ method: "GET", url: "/styles" });
    assert.equal(styles.statusCode, 200);
    const styleList = styles.json() as { styles: { id: string; stylePrompt: string }[] };
    assert.equal(styleList.styles.length, 8);
    assert.equal(styleList.styles[0]?.id, "kids-choir");
    for (const s of styleList.styles) assert.ok(s.stylePrompt.length <= 300);

    // Register the device.
    const reg = await app.inject({
      method: "POST",
      url: "/devices",
      payload: { deviceId: "dev-lifecycle" },
    });
    assert.equal(reg.statusCode, 200);
    assert.deepEqual(reg.json(), { device: { deviceId: "dev-lifecycle", credits: 10 } });

    // Submit a multipart cover job.
    const { payload, headers } = buildMultipart(
      { deviceId: "dev-lifecycle", songName: "My Test Song", styleId: "kids-choir" },
      { field: "audio", filename: "song.wav", contentType: "audio/wav", data: tinyWavBuffer() },
    );
    const submit = await app.inject({ method: "POST", url: "/covers", payload, headers });
    assert.equal(submit.statusCode, 201, submit.body);
    const { job } = submit.json() as { job: Record<string, unknown> };
    assert.equal(job["deviceId"], "dev-lifecycle");
    assert.equal(job["songName"], "My Test Song");
    assert.equal(job["styleId"], "kids-choir");
    assert.equal(job["engine"], "mock");
    assert.ok(["queued", "processing"].includes(job["status"] as string));
    // Local filesystem paths must never leak into the API shape.
    assert.ok(!("inputPath" in job) && !("input_path" in job));
    assert.ok(!("outputPath" in job) && !("output_path" in job));
    const jobId = job["id"] as string;

    // Poll until the mock engine finishes.
    let status = "";
    const deadline = Date.now() + 10_000;
    while (Date.now() < deadline) {
      const poll = await app.inject({ method: "GET", url: `/covers/${jobId}` });
      assert.equal(poll.statusCode, 200);
      status = (poll.json() as { job: { status: string } }).job.status;
      if (status === "succeeded" || status === "failed") break;
      await sleep(50);
    }
    assert.equal(status, "succeeded");

    // The output audio streams as a valid ~8s 16-bit PCM WAV.
    const audio = await app.inject({ method: "GET", url: `/covers/${jobId}/audio` });
    assert.equal(audio.statusCode, 200);
    assert.equal(audio.headers["content-type"], "audio/wav");
    const wav = audio.rawPayload;
    assert.equal(wav.subarray(0, 4).toString("ascii"), "RIFF");
    assert.equal(wav.subarray(8, 12).toString("ascii"), "WAVE");
    const sampleRate = wav.readUInt32LE(24);
    const bitsPerSample = wav.readUInt16LE(34);
    const dataLen = wav.readUInt32LE(40);
    assert.equal(bitsPerSample, 16);
    const durationSeconds = dataLen / 2 / sampleRate;
    assert.ok(durationSeconds > 6 && durationSeconds < 10, `duration was ${durationSeconds}s`);

    // Credits decremented on success only — 10 -> 9.
    const dev = await app.inject({ method: "GET", url: "/devices/dev-lifecycle" });
    assert.equal(dev.statusCode, 200);
    assert.deepEqual(dev.json(), { device: { deviceId: "dev-lifecycle", credits: 9 } });

    // Job list for the device, newest first.
    const list = await app.inject({ method: "GET", url: "/covers?deviceId=dev-lifecycle" });
    assert.equal(list.statusCode, 200);
    const { jobs } = list.json() as { jobs: { id: string; status: string }[] };
    assert.equal(jobs.length, 1);
    assert.equal(jobs[0]?.id, jobId);
    assert.equal(jobs[0]?.status, "succeeded");
  } finally {
    await destroyTestApp(app, dataDir);
  }
});

test("audio for an unfinished or unknown job is a 404", async () => {
  const { app, dataDir } = await createTestApp();
  try {
    const missing = await app.inject({ method: "GET", url: "/covers/nope/audio" });
    assert.equal(missing.statusCode, 404);
    assert.ok((missing.json() as { error: string }).error);

    const unknownRoute = await app.inject({ method: "GET", url: "/definitely-not-a-route" });
    assert.equal(unknownRoute.statusCode, 404);
    assert.deepEqual(unknownRoute.json(), { error: "Not found" });
  } finally {
    await destroyTestApp(app, dataDir);
  }
});
