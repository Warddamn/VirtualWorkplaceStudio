import { test } from "node:test";
import assert from "node:assert/strict";
import { createTestApp, destroyTestApp } from "./helpers.js";
import { fallbackStylePrompt } from "../src/stylePrompt.js";
import { STYLE_PRESETS } from "../src/styles.js";

// Ensure the endpoint takes the deterministic fallback path even if the shell
// running the tests has a real key exported.
delete process.env.ANTHROPIC_API_KEY;

test("style prompt falls back deterministically when ANTHROPIC_API_KEY is unset", async () => {
  const { app, dataDir } = await createTestApp();
  try {
    // Keyword match against the preset table.
    const choir = await app.inject({
      method: "POST",
      url: "/style-prompts",
      payload: { reference: "a children's choir singing at a school assembly" },
    });
    assert.equal(choir.statusCode, 200, choir.body);
    const choirBody = choir.json() as { stylePrompt: string; source: string };
    assert.equal(choirBody.source, "fallback");
    assert.equal(
      choirBody.stylePrompt,
      STYLE_PRESETS.find((s) => s.id === "kids-choir")?.stylePrompt,
    );

    // Unmatched references get the generic template, capped at 300 chars.
    const generic = await app.inject({
      method: "POST",
      url: "/style-prompts",
      payload: { reference: "underwater accordion polka from the year 3000 ".repeat(12) },
    });
    assert.equal(generic.statusCode, 200);
    const genericBody = generic.json() as { stylePrompt: string; source: string };
    assert.equal(genericBody.source, "fallback");
    assert.ok(genericBody.stylePrompt.length > 0);
    assert.ok(genericBody.stylePrompt.length <= 300);

    // Empty reference is rejected.
    const empty = await app.inject({
      method: "POST",
      url: "/style-prompts",
      payload: { reference: "   " },
    });
    assert.equal(empty.statusCode, 400);
  } finally {
    await destroyTestApp(app, dataDir);
  }
});

test("artist-voice references are refused (denylist)", async () => {
  const { app, dataDir } = await createTestApp();
  try {
    for (const reference of [
      "in the voice of Drake",
      "make it sound like Adele singing",
      "impersonate Freddie Mercury",
    ]) {
      const res = await app.inject({
        method: "POST",
        url: "/style-prompts",
        payload: { reference },
      });
      assert.equal(res.statusCode, 400, `expected refusal for: ${reference}`);
      const body = res.json() as { error: string };
      assert.match(body.error, /voice/i);
    }
  } finally {
    await destroyTestApp(app, dataDir);
  }
});

test("fallbackStylePrompt keyword table matches specific presets first", () => {
  const gospel = STYLE_PRESETS.find((s) => s.id === "gospel-choir")?.stylePrompt;
  const kids = STYLE_PRESETS.find((s) => s.id === "kids-choir")?.stylePrompt;
  const metal = STYLE_PRESETS.find((s) => s.id === "heavy-metal")?.stylePrompt;
  assert.equal(fallbackStylePrompt("a big gospel choir"), gospel);
  assert.equal(fallbackStylePrompt("a choir version"), kids);
  assert.equal(fallbackStylePrompt("crushing metal riffs"), metal);
  const generic = fallbackStylePrompt("something totally uncategorizable");
  assert.ok(generic.length <= 300);
  assert.notEqual(generic, kids);
});
