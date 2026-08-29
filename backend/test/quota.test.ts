import { test } from "node:test";
import assert from "node:assert/strict";
import {
  buildMultipart,
  createTestApp,
  destroyTestApp,
  submitCover,
  waitForJob,
} from "./helpers.js";

test("POST /covers returns 402 at the tier limit and allows again after upgrade", async () => {
  const { app, dataDir } = await createTestApp({ mockDelayMs: 25 });
  try {
    const reg = await app.inject({
      method: "POST",
      url: "/devices",
      payload: { deviceId: "dev-quota" },
    });
    assert.equal(reg.statusCode, 200);

    // Free tier: 3 covers/month. Queued/processing jobs already hold a quota
    // slot (reservation-against-active-jobs), so 3 rapid submissions fill it.
    const jobIds: string[] = [];
    for (let i = 0; i < 3; i++) {
      const res = await submitCover(app, {
        deviceId: "dev-quota",
        songName: `Song ${i + 1}`,
        styleId: "lofi-chill",
      });
      assert.equal(res.statusCode, 201, res.body);
      jobIds.push((res.json() as { job: { id: string } }).job.id);
    }

    // 4th submission is refused while the first three are still in flight.
    const overActive = await submitCover(app, {
      deviceId: "dev-quota",
      songName: "One Too Many",
      styleId: "lofi-chill",
    });
    assert.equal(overActive.statusCode, 402, overActive.body);
    assert.match((overActive.json() as { error: string }).error, /quota/i);

    // Still refused after they finish (3 succeeded jobs this month).
    for (const id of jobIds) {
      const job = await waitForJob(app, id);
      assert.equal(job["status"], "succeeded");
    }
    const dev = await app.inject({ method: "GET", url: "/devices/dev-quota" });
    assert.deepEqual(dev.json(), {
      device: {
        deviceId: "dev-quota",
        tier: "free",
        monthlyQuota: 3,
        usedThisMonth: 3,
        remaining: 0,
      },
    });
    const overDone = await submitCover(app, {
      deviceId: "dev-quota",
      songName: "Still Too Many",
      styleId: "lofi-chill",
    });
    assert.equal(overDone.statusCode, 402);

    // No job rows were created for the refused submissions.
    const list = await app.inject({ method: "GET", url: "/covers?deviceId=dev-quota" });
    assert.equal((list.json() as { jobs: unknown[] }).jobs.length, 3);

    // Tier upgrade (dev stub for the app-store purchase) unlocks more quota.
    const upgrade = await app.inject({
      method: "POST",
      url: "/devices/dev-quota/tier",
      payload: { tier: "plus" },
    });
    assert.equal(upgrade.statusCode, 200, upgrade.body);
    assert.deepEqual(upgrade.json(), {
      device: {
        deviceId: "dev-quota",
        tier: "plus",
        monthlyQuota: 30,
        usedThisMonth: 3,
        remaining: 27,
      },
    });

    const afterUpgrade = await submitCover(app, {
      deviceId: "dev-quota",
      songName: "Plus Song",
      styleId: "lofi-chill",
    });
    assert.equal(afterUpgrade.statusCode, 201, afterUpgrade.body);
    const plusJob = (afterUpgrade.json() as { job: Record<string, unknown> }).job;
    assert.equal(plusJob["takesRequested"], 2); // plus tier default = tier max
    await waitForJob(app, plusJob["id"] as string);

    // Unknown tiers are rejected.
    const badTier = await app.inject({
      method: "POST",
      url: "/devices/dev-quota/tier",
      payload: { tier: "platinum" },
    });
    assert.equal(badTier.statusCode, 400);
  } finally {
    await destroyTestApp(app, dataDir);
  }
});

test("failed jobs do not consume quota", async () => {
  const { app, dataDir } = await createTestApp({ mockDelayMs: 25 });
  process.env.MOCK_ENGINE_FAIL_TAKES = "0";
  try {
    // Free tier, single take that is forced to fail -> job fails -> quota freed.
    const res = await submitCover(app, {
      deviceId: "dev-fail",
      songName: "Doomed Song",
      styleId: "kids-choir",
    });
    assert.equal(res.statusCode, 201, res.body);
    const job = await waitForJob(app, (res.json() as { job: { id: string } }).job.id);
    assert.equal(job["status"], "failed");

    const dev = await app.inject({ method: "GET", url: "/devices/dev-fail" });
    assert.deepEqual(dev.json(), {
      device: {
        deviceId: "dev-fail",
        tier: "free",
        monthlyQuota: 3,
        usedThisMonth: 0,
        remaining: 3,
      },
    });
  } finally {
    delete process.env.MOCK_ENGINE_FAIL_TAKES;
    await destroyTestApp(app, dataDir);
  }
});

test("cover submissions are validated", async () => {
  const { app, dataDir } = await createTestApp();
  try {
    // No style source at all.
    const none = await submitCover(app, { deviceId: "dev-v", songName: "Song" });
    assert.equal(none.statusCode, 400);

    // Two style sources at once.
    const both = await submitCover(app, {
      deviceId: "dev-v",
      songName: "Song",
      styleId: "kids-choir",
      customStylePrompt: "warm folk",
    });
    assert.equal(both.statusCode, 400);

    // Unknown styleId.
    const unknown = await submitCover(app, {
      deviceId: "dev-v",
      songName: "Song",
      styleId: "polka-doom",
    });
    assert.equal(unknown.statusCode, 400);

    // Unknown customStyleId.
    const unknownCustom = await submitCover(app, {
      deviceId: "dev-v",
      songName: "Song",
      customStyleId: "not-a-style",
    });
    assert.equal(unknownCustom.statusCode, 400);
    assert.match((unknownCustom.json() as { error: string }).error, /customStyleId/);

    // Unknown parentJobId (refine's internal field) is rejected.
    const badParent = await submitCover(app, {
      deviceId: "dev-v",
      songName: "Song",
      styleId: "kids-choir",
      parentJobId: "no-such-job",
    });
    assert.equal(badParent.statusCode, 400);
    assert.match((badParent.json() as { error: string }).error, /parentJobId/);

    // Non-numeric takes.
    const badTakes = await submitCover(app, {
      deviceId: "dev-v",
      songName: "Song",
      styleId: "kids-choir",
      takes: "lots",
    });
    assert.equal(badTakes.statusCode, 400);

    // Artist-voice custom prompt is refused.
    const artist = await submitCover(app, {
      deviceId: "dev-v",
      songName: "Song",
      customStylePrompt: "sung in the voice of Taylor Swift",
    });
    assert.equal(artist.statusCode, 400);
    assert.match((artist.json() as { error: string }).error, /voice/i);

    // Unsupported file type.
    const badFile = buildMultipart(
      { deviceId: "dev-v", songName: "Song", styleId: "kids-choir" },
      { field: "audio", filename: "notes.txt", contentType: "text/plain", data: Buffer.from("x") },
    );
    const badFileRes = await app.inject({
      method: "POST",
      url: "/covers",
      payload: badFile.payload,
      headers: badFile.headers,
    });
    assert.equal(badFileRes.statusCode, 400);

    // Nothing above consumed quota or created a job.
    const list = await app.inject({ method: "GET", url: "/covers?deviceId=dev-v" });
    assert.deepEqual(list.json(), { jobs: [] });
  } finally {
    await destroyTestApp(app, dataDir);
  }
});
