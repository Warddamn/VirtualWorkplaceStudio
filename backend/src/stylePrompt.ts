import Anthropic from "@anthropic-ai/sdk";
import { STYLE_PRESETS } from "./styles.js";

/**
 * Style prompt builder (docs/ARCHITECTURE.md "Style prompt builder").
 *
 * 1. YouTube link -> resolve to METADATA ONLY via the public oEmbed endpoint
 *    (title + author_name). We never touch the audio/stream itself — hard rule.
 * 2. Anthropic (cheapest Haiku-tier model) turns the reference text/metadata into
 *    a <=300-char instrumentation/genre/mood style prompt.
 * 3. If ANTHROPIC_API_KEY is unset or the call fails -> deterministic fallback:
 *    keyword match against the preset table, else a generic template.
 */

/**
 * Cheapest Haiku-tier model id, confirmed via the claude-api skill's current
 * model table ($1/MTok in, $5/MTok out) on 2026-08-29.
 */
const HAIKU_MODEL_ID = "claude-haiku-4-5";

const MAX_PROMPT_CHARS = 300;

const LLM_SYSTEM_PROMPT =
  "You write style prompts for an AI song-cover engine. Given a reference (free text, or the " +
  "title/channel of a YouTube video), reply with ONE style prompt of at most 300 characters " +
  "describing genre, instrumentation, arrangement, vibe and vocal delivery style. " +
  "HARD CONSTRAINTS: never imitate or name a specific artist's voice — no 'in the voice of', " +
  "'sounds like <artist>' or artist names as vocal targets; describe the SOUND instead " +
  "(e.g. 'children's choir, school assembly, piano accompaniment, joyful'). " +
  "Reply with the style prompt only: no quotes, no preamble, no explanation.";

export interface StylePromptResult {
  stylePrompt: string;
  source: "llm" | "fallback";
  metadata?: { title: string; author: string };
}

const YOUTUBE_URL_RE =
  /https?:\/\/(?:www\.|m\.|music\.)?(?:youtube\.com\/(?:watch\?\S*v=|shorts\/|live\/)[\w-]+\S*|youtu\.be\/[\w-]+\S*)/i;

export function extractYouTubeUrl(reference: string): string | null {
  const m = YOUTUBE_URL_RE.exec(reference);
  return m ? (m[0] ?? null) : null;
}

/**
 * Resolve a YouTube link to metadata only (title + channel) via public oEmbed.
 * Also backs POST /song-metadata — the audio itself is NEVER fetched (hard rule).
 */
export async function fetchYouTubeMetadata(
  url: string,
): Promise<{ title: string; author: string } | null> {
  const oembedUrl = `https://www.youtube.com/oembed?url=${encodeURIComponent(url)}&format=json`;
  try {
    const res = await fetch(oembedUrl, { signal: AbortSignal.timeout(5000) });
    if (!res.ok) return null;
    const body = (await res.json()) as { title?: unknown; author_name?: unknown };
    if (typeof body.title !== "string") return null;
    return {
      title: body.title,
      author: typeof body.author_name === "string" ? body.author_name : "",
    };
  } catch {
    return null;
  }
}

/**
 * Deterministic fallback: ordered keyword match against the preset table, else a
 * generic template built from the reference text. Ordered so that specific
 * matches win (e.g. "gospel choir" -> gospel-choir before the bare "choir" ->
 * kids-choir catch-all).
 */
const FALLBACK_KEYWORDS: { pattern: RegExp; presetId: string }[] = [
  { pattern: /gospel|church|hallelujah/i, presetId: "gospel-choir" },
  { pattern: /kids?|child|children|school/i, presetId: "kids-choir" },
  { pattern: /choir|chorus/i, presetId: "kids-choir" },
  { pattern: /bossa|brazil|samba|latin|rio\b/i, presetId: "bossa-nova" },
  { pattern: /synth|retro|neon|outrun|80s|eighties/i, presetId: "synthwave-80s" },
  { pattern: /swing|jazz|crooner|big\s*band/i, presetId: "swing-trio" },
  { pattern: /folk|acoustic|campfire|country/i, presetId: "campfire-folk" },
  { pattern: /metal|rock|punk|shred/i, presetId: "heavy-metal" },
  { pattern: /lo-?fi|chill|study|beats/i, presetId: "lofi-chill" },
];

export function fallbackStylePrompt(referenceText: string): string {
  for (const { pattern, presetId } of FALLBACK_KEYWORDS) {
    if (pattern.test(referenceText)) {
      const preset = STYLE_PRESETS.find((s) => s.id === presetId);
      if (preset) return preset.stylePrompt;
    }
  }
  // Generic template: keep the user's words as a mood cue, describe a safe
  // instrumentation-forward arrangement, and stay under the 300-char cap.
  const cue = referenceText.replace(/\s+/g, " ").trim();
  const budget = MAX_PROMPT_CHARS - 90; // room for the template text below
  const clipped = cue.length > budget ? `${cue.slice(0, budget - 1)}…` : cue;
  return clip(
    `cover arrangement inspired by "${clipped}": expressive lead vocals, full band, faithful melody, warm modern production`,
  );
}

function clip(prompt: string): string {
  const clean = prompt.replace(/\s+/g, " ").trim();
  return clean.length > MAX_PROMPT_CHARS ? clean.slice(0, MAX_PROMPT_CHARS).trim() : clean;
}

/** Turn a free-text reference or YouTube link into a <=300-char style prompt. */
export async function buildStylePrompt(
  reference: string,
  anthropicApiKey: string | undefined,
  log: (msg: string) => void = () => undefined,
): Promise<StylePromptResult> {
  let metadata: { title: string; author: string } | undefined;
  let referenceText = reference.trim();

  const youtubeUrl = extractYouTubeUrl(referenceText);
  if (youtubeUrl) {
    const meta = await fetchYouTubeMetadata(youtubeUrl);
    if (meta) {
      metadata = meta;
      // Metadata only — the link itself never goes further than oEmbed.
      referenceText = `${meta.title}${meta.author ? ` (channel: ${meta.author})` : ""}`;
    } else {
      log("YouTube oEmbed lookup failed; falling back to raw reference text");
    }
  }

  if (anthropicApiKey) {
    try {
      const client = new Anthropic({ apiKey: anthropicApiKey });
      const response = await client.messages.create({
        model: HAIKU_MODEL_ID,
        max_tokens: 256,
        system: LLM_SYSTEM_PROMPT,
        messages: [
          {
            role: "user",
            content: `Reference: ${referenceText}\n\nWrite the style prompt.`,
          },
        ],
      });
      const text = response.content
        .filter((block): block is Anthropic.TextBlock => block.type === "text")
        .map((block) => block.text)
        .join(" ")
        .trim();
      if (text.length > 0) {
        const result: StylePromptResult = { stylePrompt: clip(text), source: "llm" };
        if (metadata) result.metadata = metadata;
        return result;
      }
      log("Anthropic returned no text; using fallback");
    } catch (err) {
      log(
        `Anthropic style-prompt call failed (${err instanceof Error ? err.message : String(err)}); using fallback`,
      );
    }
  }

  const result: StylePromptResult = {
    stylePrompt: fallbackStylePrompt(referenceText),
    source: "fallback",
  };
  if (metadata) result.metadata = metadata;
  return result;
}

const REFINE_SYSTEM_PROMPT =
  "You revise style prompts for an AI song-cover engine. Given the CURRENT style prompt and a " +
  "producer note from the user (e.g. 'more choir, less piano', 'slower and sadder'), reply with " +
  "ONE merged style prompt of at most 300 characters that keeps the current direction and applies " +
  "the note. Describe genre, instrumentation, arrangement, vibe and vocal delivery style. " +
  "HARD CONSTRAINTS: never imitate or name a specific artist's voice — no 'in the voice of', " +
  "'sounds like <artist>' or artist names as vocal targets; describe the SOUND instead. " +
  "Reply with the style prompt only: no quotes, no preamble, no explanation.";

export interface RefinedPromptResult {
  stylePrompt: string;
  source: "llm" | "fallback";
}

/**
 * Deterministic refine merge: `"<source prompt>, <note>"` capped at 300 chars.
 * The note is what the user is paying quota for, so when the combination is too
 * long the SOURCE side is trimmed to make room — never the note.
 */
export function fallbackRefinePrompt(sourcePrompt: string, note: string): string {
  const merged = `${sourcePrompt}, ${note}`;
  if (merged.length <= MAX_PROMPT_CHARS) return merged;
  const room = MAX_PROMPT_CHARS - note.length - 2;
  if (room <= 0) return clip(note);
  return `${sourcePrompt.slice(0, room).replace(/[\s,]+$/, "")}, ${note}`;
}

/**
 * Merge a producer note into a source job's style prompt (POST /covers/:id/refine).
 * Uses Anthropic (same model/constraints as buildStylePrompt) when a key is set,
 * else the deterministic fallback. Result is always <=300 chars; the caller
 * denylist-checks it and drops to the fallback on a violation.
 */
export async function mergeRefineNote(
  sourcePrompt: string,
  note: string,
  anthropicApiKey: string | undefined,
  log: (msg: string) => void = () => undefined,
): Promise<RefinedPromptResult> {
  if (anthropicApiKey) {
    try {
      const client = new Anthropic({ apiKey: anthropicApiKey });
      const response = await client.messages.create({
        model: HAIKU_MODEL_ID,
        max_tokens: 256,
        system: REFINE_SYSTEM_PROMPT,
        messages: [
          {
            role: "user",
            content:
              `Current style prompt: ${sourcePrompt}\n` +
              `Producer note: ${note}\n\n` +
              "Write the merged style prompt.",
          },
        ],
      });
      const text = response.content
        .filter((block): block is Anthropic.TextBlock => block.type === "text")
        .map((block) => block.text)
        .join(" ")
        .trim();
      if (text.length > 0) return { stylePrompt: clip(text), source: "llm" };
      log("Anthropic returned no text for refine; using fallback merge");
    } catch (err) {
      log(
        `Anthropic refine call failed (${err instanceof Error ? err.message : String(err)}); using fallback merge`,
      );
    }
  }
  return { stylePrompt: fallbackRefinePrompt(sourcePrompt, note), source: "fallback" };
}
