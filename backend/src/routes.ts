import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { pipeline } from "node:stream/promises";
import type { FastifyInstance, FastifyReply } from "fastify";
import { z } from "zod";
import {
  toApiCustomStyle,
  toApiDevice,
  toApiJob,
  type CustomStyleRow,
  type DeviceRow,
  type JobRow,
} from "./db.js";
import { STYLE_PRESETS, getStylePreset } from "./styles.js";
import {
  buildStylePrompt,
  extractYouTubeUrl,
  fallbackRefinePrompt,
  fetchYouTubeMetadata,
  mergeRefineNote,
} from "./stylePrompt.js";
import { findArtistVoiceViolation, artistVoiceRefusalMessage } from "./denylist.js";
import { TIER_CONFIG, isTier } from "./tiers.js";
import { computeWavPeaks } from "./peaks.js";

const MAX_STYLE_PROMPT_CHARS = 300;
const MAX_CUSTOM_STYLES_PER_DEVICE = 50;
/** Appended to the style prompt server-side when `instrumental` is requested. */
const INSTRUMENTAL_SUFFIX = ", instrumental only, no vocals";

const stylePromptBodySchema = z.object({
  reference: z.string().trim().min(1, "reference is required").max(2000),
});

const deviceBodySchema = z.object({
  deviceId: z.string().trim().min(1, "deviceId is required").max(200),
  expoPushToken: z.string().trim().min(1).max(500).optional(),
});

const tierBodySchema = z.object({
  tier: z.string().refine(isTier, { message: "tier must be one of free|plus|studio" }),
});

const coverFieldsSchema = z
  .object({
    deviceId: z.string().trim().min(1, "deviceId is required").max(200),
    songName: z.string().trim().min(1, "songName is required").max(300),
    styleId: z.string().trim().min(1).optional(),
    customStylePrompt: z.string().trim().min(1).max(MAX_STYLE_PROMPT_CHARS).optional(),
    customStyleId: z.string().trim().min(1).optional(),
    takes: z
      .string()
      .trim()
      .regex(/^\d+$/, "takes must be a positive integer")
      .optional(),
    instrumental: z.enum(["true", "false"]).optional(),
    // Internal use by POST /covers/:id/refine; unknown ids are rejected.
    parentJobId: z.string().trim().min(1).optional(),
  })
  .refine(
    (v) =>
      [v.styleId, v.customStylePrompt, v.customStyleId].filter(Boolean).length === 1,
    { message: "Provide exactly one of styleId, customStylePrompt or customStyleId" },
  );

const pickBodySchema = z.object({
  take: z.number().int().min(0, "take must be a non-negative integer"),
});

const refineBodySchema = z.object({
  note: z.string().trim().min(1, "note is required").max(300),
});

const customStyleBodySchema = z.object({
  deviceId: z.string().trim().min(1, "deviceId is required").max(200),
  name: z.string().trim().min(1, "name is required").max(60),
  emoji: z.string().trim().max(8).optional(),
  stylePrompt: z.string().trim().min(1, "stylePrompt is required").max(MAX_STYLE_PROMPT_CHARS),
});

const songMetadataBodySchema = z.object({
  url: z.string().trim().min(1, "url is required").max(2000),
});

const ALLOWED_AUDIO_EXTENSIONS = new Set([".mp3", ".m4a", ".wav"]);
const MIME_TO_EXTENSION: Record<string, string> = {
  "audio/mpeg": ".mp3",
  "audio/mp3": ".mp3",
  "audio/mp4": ".m4a",
  "audio/x-m4a": ".m4a",
  "audio/m4a": ".m4a",
  "audio/aac": ".m4a",
  "audio/wav": ".wav",
  "audio/x-wav": ".wav",
  "audio/wave": ".wav",
};

function badRequest(reply: FastifyReply, message: string): FastifyReply {
  return reply.status(400).send({ error: message });
}

/** Computed waveform peaks per `${jobId}:${takeIdx}` — outputs are immutable. */
const peaksCache = new Map<string, number[]>();

function apiDevice(app: FastifyInstance, device: DeviceRow) {
  return toApiDevice(device, app.store.countJobsThisMonth(device.device_id));
}

function apiJob(app: FastifyInstance, row: JobRow) {
  return toApiJob(row, app.store.listTakes(row.id));
}

/**
 * Quota gate for creating a job (docs/ARCHITECTURE-V2.md "Tiers replace raw
 * credits"). `usedThisMonth` counts this month's non-failed jobs, which INCLUDES
 * queued/processing ones — that is the v1 reservation-against-active-jobs
 * semantics carried over to quota: every in-flight job holds a quota slot and
 * only releases it by failing. So the gate is simply `remaining <= 0`.
 */
function quotaError(app: FastifyInstance, device: DeviceRow): string | null {
  const { monthlyQuota } = TIER_CONFIG[device.tier];
  const used = app.store.countJobsThisMonth(device.device_id);
  if (monthlyQuota - used <= 0) {
    return `Monthly cover quota reached (${monthlyQuota}/month on the ${device.tier} tier)`;
  }
  return null;
}

/** Clamp a requested take count to 1..tier max; default = tier max. */
function resolveTakesRequested(raw: string | undefined, maxTakes: number): number {
  if (raw === undefined) return maxTakes;
  return Math.min(Math.max(Number(raw), 1), maxTakes);
}

interface CreateJobParams {
  deviceId: string;
  songName: string;
  styleId: string | null;
  stylePrompt: string;
  inputPath: string;
  takesRequested: number;
  instrumental: boolean;
  parentJobId: string | null;
  refineNote: string | null;
}

/** Insert a job + its pending takes and enqueue it (shared by covers & refine). */
function createJob(app: FastifyInstance, params: CreateJobParams): JobRow {
  const now = new Date().toISOString();
  const row: JobRow = {
    id: crypto.randomUUID(),
    device_id: params.deviceId,
    song_name: params.songName,
    style_id: params.styleId,
    style_prompt: params.stylePrompt,
    status: "queued",
    engine: app.engine.name,
    input_path: params.inputPath,
    output_path: null,
    error: null,
    takes_requested: params.takesRequested,
    selected_take: 0,
    instrumental: params.instrumental ? 1 : 0,
    parent_job_id: params.parentJobId,
    refine_note: params.refineNote,
    created_at: now,
    updated_at: now,
  };
  app.store.insertJob(row);
  app.store.ensureTakes(row.id, params.takesRequested);
  app.queue.enqueue(row.id);
  return row;
}

/**
 * Resolve which take's output file to serve for audio/peaks. Defaults to the
 * job's selected take. Jobs created before the takes table exist fall back to
 * the job-level output path (take 0 only).
 */
function resolveServableTake(
  app: FastifyInstance,
  job: JobRow,
  rawTake: string | undefined,
):
  | { ok: true; idx: number; outputPath: string }
  | { ok: false; status: number; error: string } {
  if (job.status !== "succeeded") {
    return { ok: false, status: 404, error: `No audio available — job is ${job.status}` };
  }
  let idx = job.selected_take;
  if (rawTake !== undefined) {
    if (!/^\d+$/.test(rawTake)) {
      return { ok: false, status: 400, error: "take must be a non-negative integer" };
    }
    idx = Number(rawTake);
  }
  const takes = app.store.listTakes(job.id);
  if (takes.length === 0) {
    // Pre-v0.2 job with no take rows: only the single job-level output exists.
    if (idx !== job.selected_take || !job.output_path) {
      return { ok: false, status: 404, error: `No such take ${idx}` };
    }
    return { ok: true, idx, outputPath: job.output_path };
  }
  const take = takes.find((t) => t.idx === idx);
  if (!take) {
    return { ok: false, status: 404, error: `No such take ${idx}` };
  }
  if (take.status !== "succeeded" || !take.output_path) {
    return { ok: false, status: 404, error: `No audio for take ${idx} — take is ${take.status}` };
  }
  return { ok: true, idx, outputPath: take.output_path };
}

export function registerRoutes(app: FastifyInstance): void {
  // --- Health -------------------------------------------------------------

  app.get("/health", async () => ({ ok: true, engine: app.engine.name }));

  // --- Styles -------------------------------------------------------------

  app.get("/styles", async () => ({ styles: STYLE_PRESETS }));

  // --- Style prompt builder ----------------------------------------------

  app.post("/style-prompts", async (req, reply) => {
    const parsed = stylePromptBodySchema.safeParse(req.body);
    if (!parsed.success) {
      return badRequest(reply, parsed.error.issues[0]?.message ?? "Invalid body");
    }
    const { reference } = parsed.data;

    const violation = findArtistVoiceViolation(reference);
    if (violation) {
      return badRequest(reply, artistVoiceRefusalMessage(violation));
    }

    const result = await buildStylePrompt(reference, app.config.anthropicApiKey, (msg) =>
      app.log.info(msg),
    );

    // Belt-and-braces: never let an artist-voice prompt through, whichever path built it.
    const outViolation = findArtistVoiceViolation(result.stylePrompt);
    if (outViolation) {
      return badRequest(reply, artistVoiceRefusalMessage(outViolation));
    }
    return reply.send(result);
  });

  // --- Song identification from a link (METADATA ONLY) ---------------------

  app.post("/song-metadata", async (req, reply) => {
    const parsed = songMetadataBodySchema.safeParse(req.body);
    if (!parsed.success) {
      return badRequest(reply, parsed.error.issues[0]?.message ?? "Invalid body");
    }
    // Hard rule: a pasted link resolves to YouTube oEmbed METADATA only — the
    // audio is NEVER fetched. This endpoint lets the app prefill the song name
    // and tell the user "now pick your own audio file of this song".
    const youtubeUrl = extractYouTubeUrl(parsed.data.url);
    if (!youtubeUrl) {
      return badRequest(reply, "url must be a YouTube (youtube.com / youtu.be) video link");
    }
    const meta = await fetchYouTubeMetadata(youtubeUrl);
    if (!meta) {
      return reply.status(502).send({ error: "YouTube metadata lookup failed" });
    }
    return reply.send({ title: meta.title, author: meta.author });
  });

  // --- Devices ------------------------------------------------------------

  app.post("/devices", async (req, reply) => {
    const parsed = deviceBodySchema.safeParse(req.body);
    if (!parsed.success) {
      return badRequest(reply, parsed.error.issues[0]?.message ?? "Invalid body");
    }
    const device = app.store.upsertDevice(parsed.data.deviceId, parsed.data.expoPushToken ?? null);
    return reply.send({ device: apiDevice(app, device) });
  });

  app.get<{ Params: { deviceId: string } }>("/devices/:deviceId", async (req, reply) => {
    const device = app.store.getDevice(req.params.deviceId);
    if (!device) {
      return reply.status(404).send({ error: "Device not found" });
    }
    return reply.send({ device: apiDevice(app, device) });
  });

  // DEV STUB: stands in for the future app-store purchase flow — real billing
  // (RevenueCat / StoreKit) replaces this endpoint; do not ship it as-is.
  app.post<{ Params: { deviceId: string } }>("/devices/:deviceId/tier", async (req, reply) => {
    const parsed = tierBodySchema.safeParse(req.body);
    if (!parsed.success) {
      return badRequest(reply, parsed.error.issues[0]?.message ?? "Invalid body");
    }
    const device = app.store.setDeviceTier(req.params.deviceId, parsed.data.tier);
    return reply.send({ device: apiDevice(app, device) });
  });

  // --- Custom styles (saved style library, per device) ----------------------

  app.get<{ Querystring: { deviceId?: string } }>("/custom-styles", async (req, reply) => {
    const deviceId = req.query.deviceId;
    if (!deviceId) {
      return badRequest(reply, "deviceId query parameter is required");
    }
    const styles = app.store.listCustomStylesByDevice(deviceId).map(toApiCustomStyle);
    return reply.send({ styles });
  });

  app.post("/custom-styles", async (req, reply) => {
    const parsed = customStyleBodySchema.safeParse(req.body);
    if (!parsed.success) {
      return badRequest(reply, parsed.error.issues[0]?.message ?? "Invalid body");
    }
    const { deviceId, name, emoji, stylePrompt } = parsed.data;
    const violation = findArtistVoiceViolation(stylePrompt);
    if (violation) {
      return badRequest(reply, artistVoiceRefusalMessage(violation));
    }
    if (app.store.countCustomStylesByDevice(deviceId) >= MAX_CUSTOM_STYLES_PER_DEVICE) {
      return badRequest(
        reply,
        `Saved style limit reached (${MAX_CUSTOM_STYLES_PER_DEVICE} per device) — delete one first`,
      );
    }
    const row: CustomStyleRow = {
      id: crypto.randomUUID(),
      device_id: deviceId,
      name,
      emoji: emoji ?? "",
      style_prompt: stylePrompt,
      created_at: new Date().toISOString(),
    };
    app.store.insertCustomStyle(row);
    return reply.status(201).send({ style: toApiCustomStyle(row) });
  });

  app.delete<{ Params: { id: string }; Querystring: { deviceId?: string } }>(
    "/custom-styles/:id",
    async (req, reply) => {
      const deviceId = req.query.deviceId;
      if (!deviceId) {
        return badRequest(reply, "deviceId query parameter is required");
      }
      const deleted = app.store.deleteCustomStyle(req.params.id, deviceId);
      if (!deleted) {
        return reply.status(404).send({ error: "Custom style not found for this device" });
      }
      return reply.send({ ok: true });
    },
  );

  // --- Covers -------------------------------------------------------------

  app.post("/covers", async (req, reply) => {
    if (!req.isMultipart()) {
      return badRequest(reply, "Expected multipart/form-data");
    }

    const fields: Record<string, string> = {};
    let savedFilePath: string | null = null;
    let originalFilename = "";

    try {
      for await (const part of req.parts()) {
        if (part.type === "file") {
          if (part.fieldname !== "audio") {
            part.file.resume(); // drain and ignore unexpected file fields
            continue;
          }
          originalFilename = part.filename ?? "";
          const ext = resolveAudioExtension(originalFilename, part.mimetype);
          if (!ext) {
            part.file.resume();
            return badRequest(
              reply,
              "Unsupported audio format — upload an mp3, m4a or wav file",
            );
          }
          const uploadsDir = path.join(app.config.dataDir, "uploads");
          savedFilePath = path.join(uploadsDir, `${crypto.randomUUID()}${ext}`);
          await pipeline(part.file, fs.createWriteStream(savedFilePath));
          if (part.file.truncated) {
            throw Object.assign(new Error("Audio file exceeds the 50MB limit"), {
              statusCode: 413,
            });
          }
        } else {
          fields[part.fieldname] = String(part.value);
        }
      }

      const parsed = coverFieldsSchema.safeParse(fields);
      if (!parsed.success) {
        return badRequest(reply, parsed.error.issues[0]?.message ?? "Invalid fields");
      }
      const { deviceId, songName, styleId, customStylePrompt, customStyleId, takes, instrumental, parentJobId } =
        parsed.data;

      if (!savedFilePath) {
        return badRequest(reply, "Missing 'audio' file field");
      }

      let resolvedStyleId: string | null = null;
      let stylePrompt: string;
      if (styleId) {
        const preset = getStylePreset(styleId);
        if (!preset) {
          return badRequest(reply, `Unknown styleId '${styleId}'`);
        }
        resolvedStyleId = preset.id;
        stylePrompt = preset.stylePrompt;
      } else if (customStyleId) {
        const saved = app.store.getCustomStyle(customStyleId);
        if (!saved || saved.device_id !== deviceId) {
          return badRequest(reply, `Unknown customStyleId '${customStyleId}'`);
        }
        stylePrompt = saved.style_prompt;
      } else {
        const violation = findArtistVoiceViolation(customStylePrompt ?? "");
        if (violation) {
          return badRequest(reply, artistVoiceRefusalMessage(violation));
        }
        stylePrompt = customStylePrompt ?? "";
      }

      // Refine's internal linkage field — reject unknown parents outright.
      if (parentJobId) {
        const parent = app.store.getJob(parentJobId);
        // Same-device only: cross-device links would corrupt version chains.
        if (!parent || parent.device_id !== deviceId) {
          return badRequest(reply, `Unknown parentJobId '${parentJobId}'`);
        }
      }

      const wantsInstrumental = instrumental === "true";
      if (wantsInstrumental) {
        stylePrompt = applyInstrumentalSuffix(stylePrompt);
      }

      const device = app.store.ensureDevice(deviceId);
      const quotaMsg = quotaError(app, device);
      if (quotaMsg) {
        return reply.status(402).send({ error: quotaMsg });
      }

      const row = createJob(app, {
        deviceId,
        songName,
        styleId: resolvedStyleId,
        stylePrompt,
        inputPath: savedFilePath,
        takesRequested: resolveTakesRequested(takes, TIER_CONFIG[device.tier].maxTakes),
        instrumental: wantsInstrumental,
        parentJobId: parentJobId ?? null,
        refineNote: null,
      });
      savedFilePath = null; // now owned by the job — don't clean it up below

      return reply.status(201).send({ job: apiJob(app, row) });
    } finally {
      // A refused/failed request must not leave an orphan upload behind.
      if (savedFilePath) {
        await fs.promises.unlink(savedFilePath).catch(() => undefined);
      }
    }
  });

  app.get<{ Querystring: { deviceId?: string } }>("/covers", async (req, reply) => {
    const deviceId = req.query.deviceId;
    if (!deviceId) {
      return badRequest(reply, "deviceId query parameter is required");
    }
    const jobs = app.store.listJobsByDevice(deviceId).map((row) => apiJob(app, row));
    return reply.send({ jobs });
  });

  app.get<{ Params: { id: string } }>("/covers/:id", async (req, reply) => {
    const job = app.store.getJob(req.params.id);
    if (!job) {
      return reply.status(404).send({ error: "Job not found" });
    }
    return reply.send({ job: apiJob(app, job) });
  });

  // --- Pick a take ---------------------------------------------------------

  app.post<{ Params: { id: string } }>("/covers/:id/pick", async (req, reply) => {
    const job = app.store.getJob(req.params.id);
    if (!job) {
      return reply.status(404).send({ error: "Job not found" });
    }
    const parsed = pickBodySchema.safeParse(req.body);
    if (!parsed.success) {
      return badRequest(reply, parsed.error.issues[0]?.message ?? "Invalid body");
    }
    const take = app.store.getTake(job.id, parsed.data.take);
    if (!take || take.status !== "succeeded" || !take.output_path) {
      return badRequest(reply, `take ${parsed.data.take} is not a succeeded take of this job`);
    }
    app.store.setSelectedTake(job.id, take.idx, take.output_path);
    const updated = app.store.getJob(job.id);
    return reply.send({ job: apiJob(app, updated ?? job) });
  });

  // --- Refine (producer-note loop) -----------------------------------------

  app.post<{ Params: { id: string } }>("/covers/:id/refine", async (req, reply) => {
    const source = app.store.getJob(req.params.id);
    if (!source) {
      return reply.status(404).send({ error: "Job not found" });
    }
    const parsed = refineBodySchema.safeParse(req.body);
    if (!parsed.success) {
      return badRequest(reply, parsed.error.issues[0]?.message ?? "Invalid body");
    }
    if (source.status !== "succeeded") {
      return badRequest(reply, `Only succeeded covers can be refined — job is ${source.status}`);
    }
    const { note } = parsed.data;
    const noteViolation = findArtistVoiceViolation(note);
    if (noteViolation) {
      return badRequest(reply, artistVoiceRefusalMessage(noteViolation));
    }

    // Merge the note into the source prompt: LLM when a key is set, else the
    // deterministic fallback. Never let an artist-voice merge through.
    const merged = await mergeRefineNote(
      source.style_prompt,
      note,
      app.config.anthropicApiKey,
      (msg) => app.log.info(msg),
    );
    let stylePrompt = merged.stylePrompt;
    if (findArtistVoiceViolation(stylePrompt)) {
      stylePrompt = fallbackRefinePrompt(source.style_prompt, note);
    }
    const violation = findArtistVoiceViolation(stylePrompt);
    if (violation) {
      return badRequest(reply, artistVoiceRefusalMessage(violation));
    }

    // Refinements are generations: normal quota check applies.
    const device = app.store.ensureDevice(source.device_id);
    const quotaMsg = quotaError(app, device);
    if (quotaMsg) {
      return reply.status(402).send({ error: quotaMsg });
    }

    const row = createJob(app, {
      deviceId: source.device_id,
      songName: source.song_name,
      styleId: null,
      stylePrompt,
      // Same input audio file as the source job (shared upload on disk).
      inputPath: source.input_path,
      takesRequested: TIER_CONFIG[device.tier].maxTakes,
      instrumental: source.instrumental === 1,
      parentJobId: source.id,
      refineNote: note,
    });
    return reply.status(201).send({ job: apiJob(app, row) });
  });

  // --- Audio streaming ------------------------------------------------------

  app.get<{ Params: { id: string }; Querystring: { take?: string } }>(
    "/covers/:id/audio",
    async (req, reply) => {
      const job = app.store.getJob(req.params.id);
      if (!job) {
        return reply.status(404).send({ error: "Job not found" });
      }
      const resolved = resolveServableTake(app, job, req.query.take);
      if (!resolved.ok) {
        return reply.status(resolved.status).send({ error: resolved.error });
      }
      let stat: fs.Stats;
      try {
        stat = await fs.promises.stat(resolved.outputPath);
      } catch {
        return reply.status(404).send({ error: "Output file missing on server" });
      }
      const isWav = resolved.outputPath.toLowerCase().endsWith(".wav");
      const contentType = isWav ? "audio/wav" : "audio/mpeg";
      // Tell clients the real format/filename so share sheets don't have to guess;
      // non-selected takes are called out in the filename ("(take 2)").
      const takeSuffix = resolved.idx !== job.selected_take ? ` (take ${resolved.idx + 1})` : "";
      const baseName = job.song_name.replace(/[^\w\- ]+/g, "").trim() || "cover";
      const downloadName = `${baseName}${takeSuffix}${isWav ? ".wav" : ".mp3"}`;
      void reply.header("Content-Disposition", `inline; filename="${downloadName}"`);

      // Honor single-range requests — iOS AVPlayer needs 206 responses for seeking.
      const range = parseByteRange(req.headers.range, stat.size);
      if (range === "invalid") {
        return reply
          .status(416)
          .header("Content-Range", `bytes */${stat.size}`)
          .send({ error: "Requested range not satisfiable" });
      }
      if (range) {
        return reply
          .status(206)
          .header("Content-Type", contentType)
          .header("Accept-Ranges", "bytes")
          .header("Content-Range", `bytes ${range.start}-${range.end}/${stat.size}`)
          .header("Content-Length", range.end - range.start + 1)
          .send(fs.createReadStream(resolved.outputPath, { start: range.start, end: range.end }));
      }
      return reply
        .header("Content-Type", contentType)
        .header("Accept-Ranges", "bytes")
        .header("Content-Length", stat.size)
        .send(fs.createReadStream(resolved.outputPath));
    },
  );

  // --- Waveform peaks --------------------------------------------------------

  app.get<{ Params: { id: string }; Querystring: { take?: string } }>(
    "/covers/:id/peaks",
    async (req, reply) => {
      const job = app.store.getJob(req.params.id);
      if (!job) {
        return reply.status(404).send({ error: "Job not found" });
      }
      const resolved = resolveServableTake(app, job, req.query.take);
      if (!resolved.ok) {
        return reply.status(resolved.status).send({ error: resolved.error });
      }
      // Non-WAV outputs answer 200 { peaks: [] } — the client falls back to a
      // plain progress bar.
      if (!resolved.outputPath.toLowerCase().endsWith(".wav")) {
        return reply.send({ peaks: [] });
      }
      const cacheKey = `${job.id}:${resolved.idx}`;
      const cached = peaksCache.get(cacheKey);
      if (cached) {
        return reply.send({ peaks: cached });
      }
      let buf: Buffer;
      try {
        buf = await fs.promises.readFile(resolved.outputPath);
      } catch {
        return reply.status(404).send({ error: "Output file missing on server" });
      }
      const peaks = computeWavPeaks(buf) ?? [];
      // Outputs are immutable once a take succeeds, so cache indefinitely
      // (bounded: drop the oldest entry past 500 jobs' worth of peaks).
      peaksCache.set(cacheKey, peaks);
      if (peaksCache.size > 500) {
        const oldest = peaksCache.keys().next().value;
        if (oldest !== undefined) peaksCache.delete(oldest);
      }
      return reply.send({ peaks });
    },
  );
}

/**
 * Append the instrumental suffix, keeping the whole prompt within the 300-char
 * engine limit (the base is trimmed before the suffix is added, never after —
 * the "no vocals" instruction must survive).
 */
function applyInstrumentalSuffix(stylePrompt: string): string {
  const budget = MAX_STYLE_PROMPT_CHARS - INSTRUMENTAL_SUFFIX.length;
  const base = stylePrompt.length > budget ? stylePrompt.slice(0, budget).trimEnd() : stylePrompt;
  return `${base}${INSTRUMENTAL_SUFFIX}`;
}

/** Map an uploaded file's name/mimetype to an allowed audio extension, or null. */
function resolveAudioExtension(filename: string, mimetype: string): string | null {
  const ext = path.extname(filename).toLowerCase();
  if (ALLOWED_AUDIO_EXTENSIONS.has(ext)) return ext;
  return MIME_TO_EXTENSION[mimetype.toLowerCase()] ?? null;
}

/**
 * Parse a `Range: bytes=start-end` header against a file of `size` bytes.
 * Returns the inclusive range, null when absent/multi-range (serve the full file),
 * or "invalid" when the range cannot be satisfied.
 */
function parseByteRange(
  header: string | undefined,
  size: number,
): { start: number; end: number } | null | "invalid" {
  if (!header) return null;
  const match = /^bytes=(\d*)-(\d*)$/.exec(header.trim());
  if (!match) return null; // multi-range or malformed: fall back to the full file
  const [, rawStart, rawEnd] = match;
  if (rawStart === "" && rawEnd === "") return null;
  if (rawStart === "") {
    // Suffix range: last N bytes.
    const suffix = Math.min(Number(rawEnd), size);
    return suffix === 0 ? "invalid" : { start: size - suffix, end: size - 1 };
  }
  const start = Number(rawStart);
  const end = rawEnd === "" ? size - 1 : Math.min(Number(rawEnd), size - 1);
  if (start >= size || start > end) return "invalid";
  return { start, end };
}
