import assert from "node:assert/strict";
import fs from "node:fs";
import http from "node:http";
import os from "node:os";
import path from "node:path";
import { after, test } from "node:test";

/**
 * Integration test for MinimaxReplicateEngine against an in-process fake that
 * speaks the Replicate HTTP protocol: Files API upload -> prediction create
 * (model: minimax/music-cover) -> polling (starting/processing/succeeded) ->
 * output download. Proves the adapter's whole dance end-to-end; the one thing
 * it cannot prove is the real model's musical output (needs a paid key).
 */

interface FakeState {
  uploadedBody: Buffer | null;
  predictionInput: Record<string, unknown> | null;
  authHeaders: string[];
  polls: number;
}

function makeWav(samples: number): Buffer {
  const dataLen = samples * 2;
  const buf = Buffer.alloc(44 + dataLen);
  buf.write("RIFF", 0); buf.writeUInt32LE(36 + dataLen, 4); buf.write("WAVE", 8);
  buf.write("fmt ", 12); buf.writeUInt32LE(16, 16); buf.writeUInt16LE(1, 20);
  buf.writeUInt16LE(1, 22); buf.writeUInt32LE(22050, 24); buf.writeUInt32LE(44100, 28);
  buf.writeUInt16LE(2, 32); buf.writeUInt16LE(16, 34);
  buf.write("data", 36); buf.writeUInt32LE(dataLen, 40);
  for (let i = 0; i < samples; i++) buf.writeInt16LE(Math.round(8000 * Math.sin(i / 20)), 44 + i * 2);
  return buf;
}

function startFakeReplicate(state: FakeState): Promise<{ server: http.Server; base: string }> {
  const server = http.createServer((req, res) => {
    const auth = req.headers.authorization ?? "";
    if (auth) state.authHeaders.push(auth);
    const chunks: Buffer[] = [];
    req.on("data", (c) => chunks.push(c));
    req.on("end", () => {
      const body = Buffer.concat(chunks);
      const url = req.url ?? "";
      const base = `http://127.0.0.1:${(server.address() as { port: number }).port}`;
      if (req.method === "POST" && url === "/v1/files") {
        state.uploadedBody = body;
        res.writeHead(201, { "content-type": "application/json" });
        res.end(JSON.stringify({ urls: { get: `${base}/serve/input` } }));
      } else if (req.method === "GET" && url === "/serve/input") {
        res.writeHead(200, { "content-type": "application/octet-stream" });
        res.end(state.uploadedBody ?? Buffer.alloc(0));
      } else if (req.method === "POST" && url === "/v1/models/minimax/music-cover/predictions") {
        const parsed = JSON.parse(body.toString()) as { input: Record<string, unknown> };
        state.predictionInput = parsed.input;
        res.writeHead(201, { "content-type": "application/json" });
        res.end(JSON.stringify({ id: "p1", status: "starting", urls: { get: `${base}/v1/predictions/p1` } }));
      } else if (req.method === "GET" && url === "/v1/predictions/p1") {
        state.polls++;
        const done = state.polls >= 2;
        res.writeHead(200, { "content-type": "application/json" });
        res.end(JSON.stringify(
          done
            ? { id: "p1", status: "succeeded", output: `${base}/out/cover.wav` }
            : { id: "p1", status: "processing" },
        ));
      } else if (req.method === "GET" && url === "/out/cover.wav") {
        res.writeHead(200, { "content-type": "audio/wav" });
        res.end(makeWav(4000));
      } else {
        res.writeHead(404, { "content-type": "application/json" });
        res.end(JSON.stringify({ error: `fake replicate: no route ${req.method} ${url}` }));
      }
    });
  });
  return new Promise((resolve) => {
    server.listen(0, "127.0.0.1", () => {
      resolve({ server, base: `http://127.0.0.1:${(server.address() as { port: number }).port}` });
    });
  });
}

const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "minimax-adapter-"));
after(() => fs.rmSync(tmpDir, { recursive: true, force: true }));

test("MinimaxReplicateEngine runs the full Replicate protocol: upload, predict, poll, download", async () => {
  const state: FakeState = { uploadedBody: null, predictionInput: null, authHeaders: [], polls: 0 };
  const { server, base } = await startFakeReplicate(state);
  try {
    // The engine module reads REPLICATE_BASE_URL/REPLICATE_POLL_MS at load time,
    // so set them before the dynamic import.
    process.env.REPLICATE_BASE_URL = base;
    process.env.REPLICATE_POLL_MS = "30";
    const { MinimaxReplicateEngine } = await import("../src/engines/minimaxReplicate.js");

    const inputPath = path.join(tmpDir, "song.wav");
    const inputBytes = makeWav(2000);
    fs.writeFileSync(inputPath, inputBytes);

    const engine = new MinimaxReplicateEngine(path.join(tmpDir, "outputs"), "test-token");
    const { outputAudioPath } = await engine.generateCover({
      inputAudioPath: inputPath,
      stylePrompt: "children's choir, school assembly, piano accompaniment",
    });

    // Upload really carried the input audio (raw bytes appear inside the multipart body).
    assert.ok(state.uploadedBody, "Files API received an upload");
    assert.notEqual(state.uploadedBody!.indexOf(inputBytes), -1, "uploaded body contains the input audio bytes");

    // Prediction was created with the verified schema: audio_url + prompt.
    assert.ok(state.predictionInput, "prediction create received input");
    assert.equal(state.predictionInput!["audio_url"], `${base}/serve/input`);
    assert.equal(state.predictionInput!["prompt"], "children's choir, school assembly, piano accompaniment");

    // Polling actually happened (starting -> processing -> succeeded).
    assert.ok(state.polls >= 2, `polled at least twice (got ${state.polls})`);

    // Auth flowed on every API call.
    assert.ok(state.authHeaders.every((h) => h === "Bearer test-token"));

    // The output landed on disk as the audio the "model" returned.
    assert.ok(fs.existsSync(outputAudioPath));
    assert.ok(outputAudioPath.endsWith(".wav"));
    const out = fs.readFileSync(outputAudioPath);
    assert.equal(out.subarray(0, 4).toString(), "RIFF", "output is a valid RIFF/WAV file");
    assert.notEqual(out.length, inputBytes.length, "output is not just the input echoed back");
  } finally {
    server.close();
    delete process.env.REPLICATE_BASE_URL;
    delete process.env.REPLICATE_POLL_MS;
  }
});
