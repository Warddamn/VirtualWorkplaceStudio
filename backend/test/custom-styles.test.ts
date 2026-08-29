import { test } from "node:test";
import assert from "node:assert/strict";
import { createTestApp, destroyTestApp, submitCover, waitForJob } from "./helpers.js";

test("custom styles CRUD and use in a cover", async () => {
  const { app, dataDir } = await createTestApp({ mockDelayMs: 25 });
  try {
    // Create two styles for dev-a (second is newest).
    const first = await app.inject({
      method: "POST",
      url: "/custom-styles",
      payload: {
        deviceId: "dev-a",
        name: "Rainy-day choir",
        emoji: "🌧️",
        stylePrompt: "soft rainy-day choir, gentle piano, melancholic warmth",
      },
    });
    assert.equal(first.statusCode, 201, first.body);
    const firstStyle = (first.json() as { style: Record<string, unknown> }).style;
    assert.equal(firstStyle["deviceId"], "dev-a");
    assert.equal(firstStyle["name"], "Rainy-day choir");
    assert.equal(firstStyle["emoji"], "🌧️");
    assert.ok(firstStyle["id"]);
    assert.ok(firstStyle["createdAt"]);

    const second = await app.inject({
      method: "POST",
      url: "/custom-styles",
      payload: {
        deviceId: "dev-a",
        name: "Grandpa's swing band",
        stylePrompt: "vintage swing band, muted trumpets, brushed drums",
      },
    });
    assert.equal(second.statusCode, 201);
    const secondStyle = (second.json() as { style: Record<string, unknown> }).style;
    assert.equal(secondStyle["emoji"], ""); // emoji is optional

    // List: newest first, scoped to the device.
    const list = await app.inject({ method: "GET", url: "/custom-styles?deviceId=dev-a" });
    assert.equal(list.statusCode, 200);
    const { styles } = list.json() as { styles: { id: string; name: string }[] };
    assert.equal(styles.length, 2);
    assert.equal(styles[0]?.id, secondStyle["id"]);
    assert.equal(styles[1]?.id, firstStyle["id"]);

    const otherDevice = await app.inject({ method: "GET", url: "/custom-styles?deviceId=dev-b" });
    assert.deepEqual(otherDevice.json(), { styles: [] });
    const noDevice = await app.inject({ method: "GET", url: "/custom-styles" });
    assert.equal(noDevice.statusCode, 400);

    // Use the saved style in a cover via customStyleId.
    const cover = await submitCover(app, {
      deviceId: "dev-a",
      songName: "Styled Song",
      customStyleId: firstStyle["id"] as string,
    });
    assert.equal(cover.statusCode, 201, cover.body);
    const job = (cover.json() as { job: Record<string, unknown> }).job;
    assert.equal(job["stylePrompt"], "soft rainy-day choir, gentle piano, melancholic warmth");
    assert.equal(job["styleId"], null);
    await waitForJob(app, job["id"] as string);

    // Another device can't use (or delete) dev-a's style.
    const stolen = await submitCover(app, {
      deviceId: "dev-b",
      songName: "Stolen Style",
      customStyleId: firstStyle["id"] as string,
    });
    assert.equal(stolen.statusCode, 400);
    const wrongDelete = await app.inject({
      method: "DELETE",
      url: `/custom-styles/${firstStyle["id"] as string}?deviceId=dev-b`,
    });
    assert.equal(wrongDelete.statusCode, 404);

    // Delete for real.
    const del = await app.inject({
      method: "DELETE",
      url: `/custom-styles/${firstStyle["id"] as string}?deviceId=dev-a`,
    });
    assert.equal(del.statusCode, 200);
    assert.deepEqual(del.json(), { ok: true });
    const afterDelete = await app.inject({ method: "GET", url: "/custom-styles?deviceId=dev-a" });
    assert.equal((afterDelete.json() as { styles: unknown[] }).styles.length, 1);
  } finally {
    await destroyTestApp(app, dataDir);
  }
});

test("custom style validation and the 50-per-device cap", async () => {
  const { app, dataDir } = await createTestApp();
  try {
    // Artist-voice prompts are refused.
    const artist = await app.inject({
      method: "POST",
      url: "/custom-styles",
      payload: {
        deviceId: "dev-cap",
        name: "Nope",
        stylePrompt: "sounds like Adele singing softly",
      },
    });
    assert.equal(artist.statusCode, 400);
    assert.match((artist.json() as { error: string }).error, /voice/i);

    // Field limits: name <=60, stylePrompt <=300, emoji <=8.
    const longName = await app.inject({
      method: "POST",
      url: "/custom-styles",
      payload: { deviceId: "dev-cap", name: "n".repeat(61), stylePrompt: "warm folk" },
    });
    assert.equal(longName.statusCode, 400);
    const longPrompt = await app.inject({
      method: "POST",
      url: "/custom-styles",
      payload: { deviceId: "dev-cap", name: "Long", stylePrompt: "p".repeat(301) },
    });
    assert.equal(longPrompt.statusCode, 400);
    const longEmoji = await app.inject({
      method: "POST",
      url: "/custom-styles",
      payload: { deviceId: "dev-cap", name: "Emoji", emoji: "🎸🎸🎸🎸🎸", stylePrompt: "warm folk" },
    });
    assert.equal(longEmoji.statusCode, 400);

    // Cap: 50 styles per device, then 400.
    for (let i = 0; i < 50; i++) {
      const res = await app.inject({
        method: "POST",
        url: "/custom-styles",
        payload: { deviceId: "dev-cap", name: `Style ${i}`, stylePrompt: `style prompt ${i}` },
      });
      assert.equal(res.statusCode, 201, res.body);
    }
    const over = await app.inject({
      method: "POST",
      url: "/custom-styles",
      payload: { deviceId: "dev-cap", name: "One too many", stylePrompt: "overflow style" },
    });
    assert.equal(over.statusCode, 400);
    assert.match((over.json() as { error: string }).error, /limit/i);

    // The cap is per device — another device can still save styles.
    const other = await app.inject({
      method: "POST",
      url: "/custom-styles",
      payload: { deviceId: "dev-other", name: "Fresh", stylePrompt: "fresh style" },
    });
    assert.equal(other.statusCode, 201);
  } finally {
    await destroyTestApp(app, dataDir);
  }
});
