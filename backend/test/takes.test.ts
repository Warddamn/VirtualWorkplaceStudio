import { test } from "node:test";
import assert from "node:assert/strict";
import { createTestApp, destroyTestApp, submitCover, waitForJob } from "./helpers.js";

test("multi-take job tolerates failed takes: >=1 success -> succeeded", async () => {
  const { app, dataDir } = await createTestApp({ mockDelayMs: 25 });
  process.env.MOCK_ENGINE_FAIL_TAKES = "1"; // take idx 1 must fail
  try {
    await app.inject({ method: "POST", url: "/devices", payload: { deviceId: "dev-takes" } });
    const up = await app.inject({
      method: "POST",
      url: "/devices/dev-takes/tier",
      payload: { tier: "studio" },
    });
    assert.equal(up.statusCode, 200);

    const res = await submitCover(app, {
      deviceId: "dev-takes",
      songName: "Take Song",
      styleId: "synthwave-80s",
      takes: "3",
    });
    assert.equal(res.statusCode, 201, res.body);
    const submitted = (res.json() as { job: Record<string, unknown> }).job;
    assert.equal(submitted["takesRequested"], 3);
    const jobId = submitted["id"] as string;

    // Job succeeds despite the failed middle take, which stays recorded.
    const job = await waitForJob(app, jobId);
    assert.equal(job["status"], "succeeded");
    assert.deepEqual(job["takes"], [
      { idx: 0, status: "succeeded" },
      { idx: 1, status: "failed" },
      { idx: 2, status: "succeeded" },
    ]);
    assert.equal(job["selectedTake"], 0); // first succeeded take is the default keeper
    const failedTake = app.store.getTake(jobId, 1);
    assert.match(failedTake?.error ?? "", /take 1/);

    // Audio: default = selected take; explicit takes stream too; failed take 404s.
    const audioDefault = await app.inject({ method: "GET", url: `/covers/${jobId}/audio` });
    assert.equal(audioDefault.statusCode, 200);
    assert.equal(audioDefault.headers["content-type"], "audio/wav");
    assert.doesNotMatch(String(audioDefault.headers["content-disposition"]), /\(take \d+\)/);

    const audioTake2 = await app.inject({ method: "GET", url: `/covers/${jobId}/audio?take=2` });
    assert.equal(audioTake2.statusCode, 200);
    // Non-selected takes are called out in the download filename (1-based).
    assert.match(String(audioTake2.headers["content-disposition"]), /\(take 3\)\.wav/);

    // Range requests keep working with ?take=.
    const ranged = await app.inject({
      method: "GET",
      url: `/covers/${jobId}/audio?take=2`,
      headers: { range: "bytes=0-99" },
    });
    assert.equal(ranged.statusCode, 206);
    assert.equal(ranged.headers["content-length"], "100");

    const audioFailed = await app.inject({ method: "GET", url: `/covers/${jobId}/audio?take=1` });
    assert.equal(audioFailed.statusCode, 404);
    const audioMissing = await app.inject({ method: "GET", url: `/covers/${jobId}/audio?take=9` });
    assert.equal(audioMissing.statusCode, 404);
    const audioBad = await app.inject({ method: "GET", url: `/covers/${jobId}/audio?take=x` });
    assert.equal(audioBad.statusCode, 400);

    // Pick: only succeeded takes can become the keeper.
    const pickFailed = await app.inject({
      method: "POST",
      url: `/covers/${jobId}/pick`,
      payload: { take: 1 },
    });
    assert.equal(pickFailed.statusCode, 400);
    const pickUnknown = await app.inject({
      method: "POST",
      url: `/covers/${jobId}/pick`,
      payload: { take: 7 },
    });
    assert.equal(pickUnknown.statusCode, 400);

    const pick = await app.inject({
      method: "POST",
      url: `/covers/${jobId}/pick`,
      payload: { take: 2 },
    });
    assert.equal(pick.statusCode, 200, pick.body);
    assert.equal((pick.json() as { job: { selectedTake: number } }).job.selectedTake, 2);

    // After picking, the default stream is take 2 and take 0 gets the suffix.
    const afterPickDefault = await app.inject({ method: "GET", url: `/covers/${jobId}/audio` });
    assert.doesNotMatch(String(afterPickDefault.headers["content-disposition"]), /\(take \d+\)/);
    const afterPickTake0 = await app.inject({
      method: "GET",
      url: `/covers/${jobId}/audio?take=0`,
    });
    assert.match(String(afterPickTake0.headers["content-disposition"]), /\(take 1\)\.wav/);
  } finally {
    delete process.env.MOCK_ENGINE_FAIL_TAKES;
    await destroyTestApp(app, dataDir);
  }
});

test("a job fails only when every take fails", async () => {
  const { app, dataDir } = await createTestApp({ mockDelayMs: 25 });
  process.env.MOCK_ENGINE_FAIL_TAKES = "0,1";
  try {
    await app.inject({ method: "POST", url: "/devices", payload: { deviceId: "dev-allfail" } });
    await app.inject({
      method: "POST",
      url: "/devices/dev-allfail/tier",
      payload: { tier: "plus" },
    });

    const res = await submitCover(app, {
      deviceId: "dev-allfail",
      songName: "Cursed Song",
      styleId: "heavy-metal",
    });
    assert.equal(res.statusCode, 201, res.body);
    const submitted = (res.json() as { job: Record<string, unknown> }).job;
    assert.equal(submitted["takesRequested"], 2); // plus tier default = tier max

    const job = await waitForJob(app, submitted["id"] as string);
    assert.equal(job["status"], "failed");
    assert.match(job["error"] as string, /All 2 takes failed/);
    assert.deepEqual(job["takes"], [
      { idx: 0, status: "failed" },
      { idx: 1, status: "failed" },
    ]);

    const audio = await app.inject({
      method: "GET",
      url: `/covers/${submitted["id"] as string}/audio`,
    });
    assert.equal(audio.statusCode, 404);
  } finally {
    delete process.env.MOCK_ENGINE_FAIL_TAKES;
    await destroyTestApp(app, dataDir);
  }
});

test("takes are clamped to the tier maximum and instrumental adjusts the prompt", async () => {
  const { app, dataDir } = await createTestApp({ mockDelayMs: 25 });
  try {
    await app.inject({ method: "POST", url: "/devices", payload: { deviceId: "dev-clamp" } });
    await app.inject({
      method: "POST",
      url: "/devices/dev-clamp/tier",
      payload: { tier: "studio" },
    });

    // 99 clamps down to the studio max of 4; 0 clamps up to 1.
    const high = await submitCover(app, {
      deviceId: "dev-clamp",
      songName: "Clamped High",
      styleId: "bossa-nova",
      takes: "99",
      instrumental: "true",
    });
    assert.equal(high.statusCode, 201, high.body);
    const highJob = (high.json() as { job: Record<string, unknown> }).job;
    assert.equal(highJob["takesRequested"], 4);
    assert.equal(highJob["instrumental"], true);
    // Server-side instrumental variant: suffix appended to the style prompt.
    assert.match(highJob["stylePrompt"] as string, /, instrumental only, no vocals$/);
    assert.ok((highJob["stylePrompt"] as string).length <= 300);

    const low = await submitCover(app, {
      deviceId: "dev-clamp",
      songName: "Clamped Low",
      styleId: "bossa-nova",
      takes: "0",
    });
    assert.equal(low.statusCode, 201, low.body);
    const lowJob = (low.json() as { job: Record<string, unknown> }).job;
    assert.equal(lowJob["takesRequested"], 1);
    assert.equal(lowJob["instrumental"], false);

    await waitForJob(app, highJob["id"] as string);
    await waitForJob(app, lowJob["id"] as string);
  } finally {
    await destroyTestApp(app, dataDir);
  }
});
