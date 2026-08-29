import { test } from "node:test";
import assert from "node:assert/strict";
import { buildMultipart, createTestApp, destroyTestApp, tinyWavBuffer } from "./helpers.js";

test("POST /covers returns 402 when the device has zero credits", async () => {
  const { app, dataDir } = await createTestApp();
  try {
    const reg = await app.inject({
      method: "POST",
      url: "/devices",
      payload: { deviceId: "dev-broke" },
    });
    assert.equal(reg.statusCode, 200);

    // Exhaust the credits directly in the store.
    app.store.db.prepare("UPDATE devices SET credits = 0 WHERE device_id = ?").run("dev-broke");

    const { payload, headers } = buildMultipart(
      { deviceId: "dev-broke", songName: "No Credit Song", styleId: "lofi-chill" },
      { field: "audio", filename: "song.mp3", contentType: "audio/mpeg", data: tinyWavBuffer() },
    );
    const submit = await app.inject({ method: "POST", url: "/covers", payload, headers });
    assert.equal(submit.statusCode, 402, submit.body);
    const body = submit.json() as { error: string };
    assert.match(body.error, /credit/i);

    // No job was created for the refused request.
    const list = await app.inject({ method: "GET", url: "/covers?deviceId=dev-broke" });
    assert.equal(list.statusCode, 200);
    assert.deepEqual(list.json(), { jobs: [] });
  } finally {
    await destroyTestApp(app, dataDir);
  }
});

test("cover submissions are validated", async () => {
  const { app, dataDir } = await createTestApp();
  try {
    // Neither styleId nor customStylePrompt.
    const none = buildMultipart(
      { deviceId: "dev-v", songName: "Song" },
      { field: "audio", filename: "s.wav", contentType: "audio/wav", data: tinyWavBuffer() },
    );
    const noneRes = await app.inject({
      method: "POST",
      url: "/covers",
      payload: none.payload,
      headers: none.headers,
    });
    assert.equal(noneRes.statusCode, 400);

    // Unknown styleId.
    const unknown = buildMultipart(
      { deviceId: "dev-v", songName: "Song", styleId: "polka-doom" },
      { field: "audio", filename: "s.wav", contentType: "audio/wav", data: tinyWavBuffer() },
    );
    const unknownRes = await app.inject({
      method: "POST",
      url: "/covers",
      payload: unknown.payload,
      headers: unknown.headers,
    });
    assert.equal(unknownRes.statusCode, 400);

    // Artist-voice custom prompt is refused.
    const artist = buildMultipart(
      {
        deviceId: "dev-v",
        songName: "Song",
        customStylePrompt: "sung in the voice of Taylor Swift",
      },
      { field: "audio", filename: "s.wav", contentType: "audio/wav", data: tinyWavBuffer() },
    );
    const artistRes = await app.inject({
      method: "POST",
      url: "/covers",
      payload: artist.payload,
      headers: artist.headers,
    });
    assert.equal(artistRes.statusCode, 400);
    assert.match((artistRes.json() as { error: string }).error, /voice/i);

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

    // Nothing above consumed a credit or created a job.
    const list = await app.inject({ method: "GET", url: "/covers?deviceId=dev-v" });
    assert.deepEqual(list.json(), { jobs: [] });
  } finally {
    await destroyTestApp(app, dataDir);
  }
});
