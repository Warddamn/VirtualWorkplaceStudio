import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { pipeline } from "node:stream/promises";
import type { FastifyInstance, FastifyReply } from "fastify";
import { z } from "zod";
import { toApiJob, type JobRow } from "./db.js";
import { STYLE_PRESETS, getStylePreset } from "./styles.js";
import { buildStylePrompt } from "./stylePrompt.js";
import { findArtistVoiceViolation, artistVoiceRefusalMessage } from "./denylist.js";

const MAX_STYLE_PROMPT_CHARS = 300;

const stylePromptBodySchema = z.object({
  reference: z.string().trim().min(1, "reference is required").max(2000),
});

const deviceBodySchema = z.object({
  deviceId: z.string().trim().min(1, "deviceId is required").max(200),
  expoPushToken: z.string().trim().min(1).max(500).optional(),
});

const coverFieldsSchema = z
  .object({
    deviceId: z.string().trim().min(1, "deviceId is required").max(200),
    songName: z.string().trim().min(1, "songName is required").max(300),
    styleId: z.string().trim().min(1).optional(),
    customStylePrompt: z.string().trim().min(1).max(MAX_STYLE_PROMPT_CHARS).optional(),
  })
  .refine((v) => Boolean(v.styleId) !== Boolean(v.customStylePrompt), {
    message: "Provide exactly one of styleId or customStylePrompt",
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

  // --- Devices ------------------------------------------------------------

  app.post("/devices", async (req, reply) => {
    const parsed = deviceBodySchema.safeParse(req.body);
    if (!parsed.success) {
      return badRequest(reply, parsed.error.issues[0]?.message ?? "Invalid body");
    }
    const device = app.store.upsertDevice(parsed.data.deviceId, parsed.data.expoPushToken ?? null);
    return reply.send({ device: { deviceId: device.device_id, credits: device.credits } });
  });

  app.get<{ Params: { deviceId: string } }>("/devices/:deviceId", async (req, reply) => {
    const device = app.store.getDevice(req.params.deviceId);
    if (!device) {
      return reply.status(404).send({ error: "Device not found" });
    }
    return reply.send({ device: { deviceId: device.device_id, credits: device.credits } });
  });

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
      const { deviceId, songName, styleId, customStylePrompt } = parsed.data;

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
      } else {
        const violation = findArtistVoiceViolation(customStylePrompt ?? "");
        if (violation) {
          return badRequest(reply, artistVoiceRefusalMessage(violation));
        }
        stylePrompt = customStylePrompt ?? "";
      }

      // Credits: 402 when the device has none left. Unknown devices get a row
      // with the default 10 credits (mobile normally registers via POST /devices).
      const device = app.store.ensureDevice(deviceId);
      if (device.credits <= 0) {
        return reply.status(402).send({ error: "No credits remaining" });
      }

      const now = new Date().toISOString();
      const row: JobRow = {
        id: crypto.randomUUID(),
        device_id: deviceId,
        song_name: songName,
        style_id: resolvedStyleId,
        style_prompt: stylePrompt,
        status: "queued",
        engine: app.engine.name,
        input_path: savedFilePath,
        output_path: null,
        error: null,
        created_at: now,
        updated_at: now,
      };
      app.store.insertJob(row);
      savedFilePath = null; // now owned by the job — don't clean it up below
      app.queue.enqueue(row.id);

      return reply.status(201).send({ job: toApiJob(row) });
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
    const jobs = app.store.listJobsByDevice(deviceId).map(toApiJob);
    return reply.send({ jobs });
  });

  app.get<{ Params: { id: string } }>("/covers/:id", async (req, reply) => {
    const job = app.store.getJob(req.params.id);
    if (!job) {
      return reply.status(404).send({ error: "Job not found" });
    }
    return reply.send({ job: toApiJob(job) });
  });

  app.get<{ Params: { id: string } }>("/covers/:id/audio", async (req, reply) => {
    const job = app.store.getJob(req.params.id);
    if (!job) {
      return reply.status(404).send({ error: "Job not found" });
    }
    if (job.status !== "succeeded" || !job.output_path) {
      return reply.status(404).send({ error: `No audio available — job is ${job.status}` });
    }
    let stat: fs.Stats;
    try {
      stat = await fs.promises.stat(job.output_path);
    } catch {
      return reply.status(404).send({ error: "Output file missing on server" });
    }
    const contentType = job.output_path.toLowerCase().endsWith(".wav")
      ? "audio/wav"
      : "audio/mpeg";
    return reply
      .header("Content-Type", contentType)
      .header("Content-Length", stat.size)
      .send(fs.createReadStream(job.output_path));
  });
}

/** Map an uploaded file's name/mimetype to an allowed audio extension, or null. */
function resolveAudioExtension(filename: string, mimetype: string): string | null {
  const ext = path.extname(filename).toLowerCase();
  if (ALLOWED_AUDIO_EXTENSIONS.has(ext)) return ext;
  return MIME_TO_EXTENSION[mimetype.toLowerCase()] ?? null;
}
