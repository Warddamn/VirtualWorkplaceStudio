import { test } from "node:test";
import assert from "node:assert/strict";
import { createTestApp, destroyTestApp } from "./helpers.js";

// URL validation only — no network is touched in these tests: non-YouTube links
// are rejected before any oEmbed lookup could happen. (The endpoint NEVER
// fetches audio either way — metadata only, per the hard rule.)
test("POST /song-metadata rejects non-YouTube URLs without any network call", async () => {
  const { app, dataDir } = await createTestApp();
  try {
    for (const url of [
      "https://example.com/watch?v=dQw4w9WgXcQ",
      "https://vimeo.com/12345",
      "https://soundcloud.com/artist/track",
      "not a url at all",
      "youtube.com/watch?v=abc", // no scheme -> not accepted
    ]) {
      const res = await app.inject({ method: "POST", url: "/song-metadata", payload: { url } });
      assert.equal(res.statusCode, 400, `expected 400 for: ${url}`);
      assert.match((res.json() as { error: string }).error, /youtube/i);
    }

    // Missing/empty url field.
    const missing = await app.inject({ method: "POST", url: "/song-metadata", payload: {} });
    assert.equal(missing.statusCode, 400);
    const empty = await app.inject({
      method: "POST",
      url: "/song-metadata",
      payload: { url: "   " },
    });
    assert.equal(empty.statusCode, 400);
  } finally {
    await destroyTestApp(app, dataDir);
  }
});
