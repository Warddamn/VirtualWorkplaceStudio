import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import type { FastifyInstance } from "fastify";
import { createApp } from "../src/app.js";

process.env.NODE_ENV = "test";

/** Build an app against a throwaway data dir with a fast mock engine. */
export async function createTestApp(): Promise<{ app: FastifyInstance; dataDir: string }> {
  const dataDir = fs.mkdtempSync(path.join(os.tmpdir(), "cover-backend-test-"));
  const app = await createApp({
    dataDir,
    engine: "mock",
    mockDelayMs: 100,
    anthropicApiKey: undefined, // tests never call the live API
  });
  return { app, dataDir };
}

export async function destroyTestApp(app: FastifyInstance, dataDir: string): Promise<void> {
  await app.close();
  fs.rmSync(dataDir, { recursive: true, force: true });
}

export interface MultipartFilePart {
  field: string;
  filename: string;
  contentType: string;
  data: Buffer;
}

/** Hand-rolled multipart/form-data encoder for fastify.inject. */
export function buildMultipart(
  fields: Record<string, string>,
  file?: MultipartFilePart,
): { payload: Buffer; headers: Record<string, string> } {
  const boundary = `----test${crypto.randomBytes(12).toString("hex")}`;
  const chunks: Buffer[] = [];
  for (const [name, value] of Object.entries(fields)) {
    chunks.push(
      Buffer.from(
        `--${boundary}\r\nContent-Disposition: form-data; name="${name}"\r\n\r\n${value}\r\n`,
      ),
    );
  }
  if (file) {
    chunks.push(
      Buffer.from(
        `--${boundary}\r\nContent-Disposition: form-data; name="${file.field}"; ` +
          `filename="${file.filename}"\r\nContent-Type: ${file.contentType}\r\n\r\n`,
      ),
    );
    chunks.push(file.data);
    chunks.push(Buffer.from("\r\n"));
  }
  chunks.push(Buffer.from(`--${boundary}--\r\n`));
  return {
    payload: Buffer.concat(chunks),
    headers: { "content-type": `multipart/form-data; boundary=${boundary}` },
  };
}

/** A tiny (fake but well-formed-enough) WAV payload for upload tests. */
export function tinyWavBuffer(): Buffer {
  const dataLen = 2 * 100;
  const buf = Buffer.alloc(44 + dataLen);
  buf.write("RIFF", 0, "ascii");
  buf.writeUInt32LE(36 + dataLen, 4);
  buf.write("WAVE", 8, "ascii");
  buf.write("fmt ", 12, "ascii");
  buf.writeUInt32LE(16, 16);
  buf.writeUInt16LE(1, 20);
  buf.writeUInt16LE(1, 22);
  buf.writeUInt32LE(8000, 24);
  buf.writeUInt32LE(16000, 28);
  buf.writeUInt16LE(2, 32);
  buf.writeUInt16LE(16, 34);
  buf.write("data", 36, "ascii");
  buf.writeUInt32LE(dataLen, 40);
  return buf;
}

export function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
