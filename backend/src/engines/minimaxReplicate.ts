import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import type { CoverEngine } from "./types.js";

/* ============================================================================
 * Input schema cross-checked 2026-08-30 against search-indexed model docs
 * (replicate.com/minimax/music-cover, runware.ai, aimlapi.com — all agree):
 *   audio_url (required) — publicly accessible MP3/WAV URL of the song, must
 *                          contain vocals
 *   prompt    (required) — target-style description, up to 2,000 chars
 *   optional: sample_rate, bitrate, audio_format (mp3 default)
 * Still eyeball the live model page's API tab before the first paid run —
 * schemas drift, and this environment could not fetch the page directly.
 * ==========================================================================*/
/** Overridable for integration tests against a local Replicate-compatible fake. */
const REPLICATE_API_BASE = (process.env.REPLICATE_BASE_URL ?? "https://api.replicate.com").replace(/\/+$/, "");
const REPLICATE_MINIMAX = {
  /** Model slug on Replicate. */
  model: "minimax/music-cover",
  /** Create a prediction directly against the model (no version pin). */
  predictionsUrl: `${REPLICATE_API_BASE}/v1/models/minimax/music-cover/predictions`,
  /** Replicate Files API (multipart upload -> serving URL). */
  filesUrl: `${REPLICATE_API_BASE}/v1/files`,
  INPUT_FIELDS: {
    /** URL of the user's song to cover (Replicate Files API serving URL). */
    referenceAudio: "audio_url",
    /** Text style prompt (we cap at 300 chars; the model allows 2,000). */
    stylePrompt: "prompt",
  },
} as const;

const POLL_INTERVAL_MS = Number(process.env.REPLICATE_POLL_MS ?? 3000);
const MAX_WAIT_MS = 10 * 60 * 1000; // generation takes minutes; cap at 10.

interface ReplicatePrediction {
  id: string;
  status: "starting" | "processing" | "succeeded" | "failed" | "canceled";
  output?: unknown;
  error?: string | null;
  urls?: { get?: string };
}

/**
 * MinimaxReplicateEngine — calls Replicate's HTTP API for `minimax/music-cover`.
 * Requires `REPLICATE_API_TOKEN`. Flow: upload input audio via the Files API,
 * create a prediction with the style prompt, poll until it settles, download
 * the output audio to the local outputs dir.
 */
export class MinimaxReplicateEngine implements CoverEngine {
  readonly name = "minimax";

  constructor(
    private readonly outputsDir: string,
    private readonly apiToken: string,
  ) {
    if (!apiToken) {
      throw new Error("MinimaxReplicateEngine requires REPLICATE_API_TOKEN");
    }
  }

  async generateCover(req: {
    inputAudioPath: string;
    stylePrompt: string;
  }): Promise<{ outputAudioPath: string }> {
    const audioUrl = await this.uploadInputFile(req.inputAudioPath);

    const createRes = await fetch(REPLICATE_MINIMAX.predictionsUrl, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${this.apiToken}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        input: {
          [REPLICATE_MINIMAX.INPUT_FIELDS.referenceAudio]: audioUrl,
          [REPLICATE_MINIMAX.INPUT_FIELDS.stylePrompt]: req.stylePrompt,
        },
      }),
    });
    if (!createRes.ok) {
      throw new Error(
        `Replicate prediction create failed (HTTP ${createRes.status}): ${truncate(await createRes.text())}`,
      );
    }
    let prediction = (await createRes.json()) as ReplicatePrediction;

    const deadline = Date.now() + MAX_WAIT_MS;
    while (prediction.status === "starting" || prediction.status === "processing") {
      if (Date.now() > deadline) {
        throw new Error("Replicate prediction timed out after 10 minutes");
      }
      await sleep(POLL_INTERVAL_MS);
      const pollUrl =
        prediction.urls?.get ?? `${REPLICATE_API_BASE}/v1/predictions/${prediction.id}`;
      const pollRes = await fetch(pollUrl, {
        headers: { Authorization: `Bearer ${this.apiToken}` },
      });
      if (!pollRes.ok) {
        throw new Error(`Replicate prediction poll failed (HTTP ${pollRes.status})`);
      }
      prediction = (await pollRes.json()) as ReplicatePrediction;
    }

    if (prediction.status !== "succeeded") {
      throw new Error(
        `Replicate prediction ${prediction.status}: ${prediction.error ?? "no error detail"}`,
      );
    }

    const outputUrl = extractOutputUrl(prediction.output);
    if (!outputUrl) {
      throw new Error("Replicate prediction succeeded but returned no output URL");
    }
    return { outputAudioPath: await downloadTo(this.outputsDir, outputUrl) };
  }

  /** Upload the local file via Replicate's Files API and return its serving URL. */
  private async uploadInputFile(inputAudioPath: string): Promise<string> {
    const data = await fs.promises.readFile(inputAudioPath);
    const form = new FormData();
    form.append(
      "content",
      new Blob([new Uint8Array(data)], { type: guessMimeType(inputAudioPath) }),
      path.basename(inputAudioPath),
    );
    const res = await fetch(REPLICATE_MINIMAX.filesUrl, {
      method: "POST",
      headers: { Authorization: `Bearer ${this.apiToken}` },
      body: form,
    });
    if (!res.ok) {
      throw new Error(`Replicate file upload failed (HTTP ${res.status}): ${truncate(await res.text())}`);
    }
    const body = (await res.json()) as { urls?: { get?: string } };
    const url = body.urls?.get;
    if (!url) throw new Error("Replicate file upload returned no serving URL");
    return url;
  }
}

/** Replicate output is either a URL string or an array/object of URLs — handle all. */
function extractOutputUrl(output: unknown): string | null {
  if (typeof output === "string") return output;
  if (Array.isArray(output) && typeof output[0] === "string") return output[0];
  if (output && typeof output === "object") {
    const obj = output as Record<string, unknown>;
    for (const key of ["audio", "audio_url", "url", "output"]) {
      const v = obj[key];
      if (typeof v === "string") return v;
    }
  }
  return null;
}

async function downloadTo(outputsDir: string, url: string): Promise<string> {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Output download failed (HTTP ${res.status})`);
  const ext = extensionFromUrlOrType(url, res.headers.get("content-type"));
  const outPath = path.join(outputsDir, `${crypto.randomUUID()}${ext}`);
  await fs.promises.mkdir(outputsDir, { recursive: true });
  await fs.promises.writeFile(outPath, Buffer.from(await res.arrayBuffer()));
  return outPath;
}

export function extensionFromUrlOrType(url: string, contentType: string | null): string {
  const clean = url.split("?")[0] ?? "";
  const m = /\.(mp3|wav|m4a|flac|ogg)$/i.exec(clean);
  if (m) return `.${m[1]?.toLowerCase()}`;
  if (contentType?.includes("wav")) return ".wav";
  if (contentType?.includes("mp4") || contentType?.includes("m4a")) return ".m4a";
  return ".mp3";
}

export function guessMimeType(filePath: string): string {
  const ext = path.extname(filePath).toLowerCase();
  if (ext === ".wav") return "audio/wav";
  if (ext === ".m4a") return "audio/mp4";
  return "audio/mpeg";
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => {
    setTimeout(resolve, ms).unref();
  });
}

function truncate(s: string, max = 300): string {
  return s.length > max ? `${s.slice(0, max)}…` : s;
}
