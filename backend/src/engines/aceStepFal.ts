import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import type { CoverEngine } from "./types.js";
import { extensionFromUrlOrType, guessMimeType } from "./minimaxReplicate.js";

/* ============================================================================
 * !!! VERIFY ME BEFORE FIRST REAL RUN !!!
 *
 * fal.ai was UNREACHABLE from the environment this code was written in, so the
 * endpoint path and input field names below are BEST-EFFORT guesses based on
 * docs/FEASIBILITY.md (endpoint family `fal-ai/ace-step/audio-to-audio`,
 * `audio_cover_strength` ~0.5). They are isolated here so a mismatch is a
 * one-line fix.
 *
 * Before spending money: open https://fal.ai/models/fal-ai/ace-step/audio-to-audio
 * -> API docs -> input schema, and correct `INPUT_FIELDS` / `queueUrl` (and, if
 * needed, the output shape handling in `extractAudioUrl`). See backend/README.md.
 * ==========================================================================*/
const FAL_ACESTEP = {
  /** fal queue endpoint for the ACE-Step audio-to-audio (cover) mode. */
  queueUrl: "https://queue.fal.run/fal-ai/ace-step/audio-to-audio",
  /** BEST-EFFORT input field names — verify against the live model page. */
  INPUT_FIELDS: {
    /** URL (or data URI) of the user's song to cover. */
    referenceAudio: "audio_url",
    /** Text style prompt. */
    stylePrompt: "prompt",
    /** How strongly to restyle vs. copy — FEASIBILITY.md recommends ~0.5. */
    coverStrength: "audio_cover_strength",
  },
  DEFAULT_COVER_STRENGTH: 0.5,
} as const;

const POLL_INTERVAL_MS = 3000;
const MAX_WAIT_MS = 10 * 60 * 1000;

interface FalQueueSubmitResponse {
  request_id?: string;
  status_url?: string;
  response_url?: string;
}

interface FalQueueStatus {
  status?: "IN_QUEUE" | "IN_PROGRESS" | "COMPLETED" | string;
  response_url?: string;
}

/**
 * AceStepFalEngine — ACE-Step 1.5 audio-to-audio ("cover mode") hosted on fal.ai.
 * Requires `FAL_KEY`. Uses fal's queue API: submit (input audio as a data URI —
 * fal accepts data URIs anywhere a URL is expected), poll the status URL, fetch
 * the response, download the output audio locally.
 */
export class AceStepFalEngine implements CoverEngine {
  readonly name = "acestep";

  constructor(
    private readonly outputsDir: string,
    private readonly falKey: string,
  ) {
    if (!falKey) {
      throw new Error("AceStepFalEngine requires FAL_KEY");
    }
  }

  async generateCover(req: {
    inputAudioPath: string;
    stylePrompt: string;
  }): Promise<{ outputAudioPath: string }> {
    const audio = await fs.promises.readFile(req.inputAudioPath);
    const dataUri = `data:${guessMimeType(req.inputAudioPath)};base64,${audio.toString("base64")}`;

    const submitRes = await fetch(FAL_ACESTEP.queueUrl, {
      method: "POST",
      headers: {
        Authorization: `Key ${this.falKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        [FAL_ACESTEP.INPUT_FIELDS.referenceAudio]: dataUri,
        [FAL_ACESTEP.INPUT_FIELDS.stylePrompt]: req.stylePrompt,
        [FAL_ACESTEP.INPUT_FIELDS.coverStrength]: FAL_ACESTEP.DEFAULT_COVER_STRENGTH,
      }),
    });
    if (!submitRes.ok) {
      throw new Error(
        `fal queue submit failed (HTTP ${submitRes.status}): ${truncate(await submitRes.text())}`,
      );
    }
    const submitted = (await submitRes.json()) as FalQueueSubmitResponse;
    if (!submitted.status_url || !submitted.response_url) {
      throw new Error("fal queue submit returned no status/response URLs");
    }

    const deadline = Date.now() + MAX_WAIT_MS;
    for (;;) {
      if (Date.now() > deadline) {
        throw new Error("fal request timed out after 10 minutes");
      }
      const statusRes = await fetch(submitted.status_url, {
        headers: { Authorization: `Key ${this.falKey}` },
      });
      if (!statusRes.ok) {
        throw new Error(`fal status poll failed (HTTP ${statusRes.status})`);
      }
      const status = (await statusRes.json()) as FalQueueStatus;
      if (status.status === "COMPLETED") break;
      if (status.status !== "IN_QUEUE" && status.status !== "IN_PROGRESS") {
        throw new Error(`fal request ended with status ${status.status ?? "unknown"}`);
      }
      await sleep(POLL_INTERVAL_MS);
    }

    const resultRes = await fetch(submitted.response_url, {
      headers: { Authorization: `Key ${this.falKey}` },
    });
    if (!resultRes.ok) {
      throw new Error(`fal result fetch failed (HTTP ${resultRes.status})`);
    }
    const result = (await resultRes.json()) as unknown;
    const outputUrl = extractAudioUrl(result);
    if (!outputUrl) {
      throw new Error("fal request completed but returned no audio URL");
    }

    const dlRes = await fetch(outputUrl);
    if (!dlRes.ok) throw new Error(`Output download failed (HTTP ${dlRes.status})`);
    const ext = extensionFromUrlOrType(outputUrl, dlRes.headers.get("content-type"));
    const outputAudioPath = path.join(this.outputsDir, `${crypto.randomUUID()}${ext}`);
    await fs.promises.mkdir(this.outputsDir, { recursive: true });
    await fs.promises.writeFile(outputAudioPath, Buffer.from(await dlRes.arrayBuffer()));
    return { outputAudioPath };
  }
}

/** fal responses usually nest the file as { audio: { url } } — handle variants. */
function extractAudioUrl(result: unknown): string | null {
  if (!result || typeof result !== "object") return null;
  const obj = result as Record<string, unknown>;
  for (const key of ["audio", "audio_file", "output", "file"]) {
    const v = obj[key];
    if (typeof v === "string") return v;
    if (v && typeof v === "object") {
      const url = (v as Record<string, unknown>)["url"];
      if (typeof url === "string") return url;
    }
  }
  return null;
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => {
    setTimeout(resolve, ms).unref();
  });
}

function truncate(s: string, max = 300): string {
  return s.length > max ? `${s.slice(0, max)}…` : s;
}
