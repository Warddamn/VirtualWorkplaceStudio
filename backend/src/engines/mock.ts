import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import type { CoverEngine } from "./types.js";

/**
 * MockEngine — the default, zero-config engine.
 *
 * Waits ~5s (simulating a real generation job), then synthesizes a valid 16-bit PCM
 * WAV of ~8 seconds containing a simple sine-wave melody (a few notes, so it is
 * audibly "a song"), written with no external dependencies. This makes the whole
 * app runnable end-to-end with no API keys.
 */
export class MockEngine implements CoverEngine {
  readonly name = "mock";

  constructor(
    private readonly outputsDir: string,
    private readonly delayMs = 5000,
  ) {}

  async generateCover(req: {
    inputAudioPath: string;
    stylePrompt: string;
  }): Promise<{ outputAudioPath: string }> {
    if (!fs.existsSync(req.inputAudioPath)) {
      throw new Error(`Input audio file not found: ${path.basename(req.inputAudioPath)}`);
    }

    await sleep(this.delayMs);

    const wav = synthesizeMelodyWav();
    const outputAudioPath = path.join(this.outputsDir, `${crypto.randomUUID()}.wav`);
    await fs.promises.mkdir(this.outputsDir, { recursive: true });
    await fs.promises.writeFile(outputAudioPath, wav);
    return { outputAudioPath };
  }
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => {
    // unref() so a pending mock "generation" never holds the process open on shutdown.
    setTimeout(resolve, ms).unref();
  });
}

/**
 * Synthesize ~8 seconds of 16-bit PCM mono WAV at 22.05 kHz: a simple two-phrase
 * sine melody (C major) with a soft attack/release envelope so notes don't click.
 */
export function synthesizeMelodyWav(): Buffer {
  const sampleRate = 22050;
  const noteDuration = 0.5; // seconds per note
  // Frequencies (Hz): C4 D4 E4 G4 etc. — a cheerful little tune, 16 notes = 8s.
  const C4 = 261.63, D4 = 293.66, E4 = 329.63, G4 = 392.0, A4 = 440.0, C5 = 523.25;
  const melody = [C4, E4, G4, C5, A4, G4, E4, D4, C4, E4, G4, A4, G4, E4, D4, C4];

  const samplesPerNote = Math.round(sampleRate * noteDuration);
  const totalSamples = samplesPerNote * melody.length;
  const dataLen = totalSamples * 2; // 16-bit mono

  const buf = Buffer.alloc(44 + dataLen);
  // RIFF header
  buf.write("RIFF", 0, "ascii");
  buf.writeUInt32LE(36 + dataLen, 4);
  buf.write("WAVE", 8, "ascii");
  // fmt chunk
  buf.write("fmt ", 12, "ascii");
  buf.writeUInt32LE(16, 16); // PCM chunk size
  buf.writeUInt16LE(1, 20); // audio format: PCM
  buf.writeUInt16LE(1, 22); // channels: mono
  buf.writeUInt32LE(sampleRate, 24);
  buf.writeUInt32LE(sampleRate * 2, 28); // byte rate
  buf.writeUInt16LE(2, 32); // block align
  buf.writeUInt16LE(16, 34); // bits per sample
  // data chunk
  buf.write("data", 36, "ascii");
  buf.writeUInt32LE(dataLen, 40);

  const amplitude = 0.35 * 0x7fff;
  const envelopeSamples = Math.round(sampleRate * 0.03); // 30ms attack/release
  let offset = 44;
  for (let n = 0; n < melody.length; n++) {
    const freq = melody[n] ?? C4;
    for (let i = 0; i < samplesPerNote; i++) {
      let env = 1;
      if (i < envelopeSamples) env = i / envelopeSamples;
      else if (i > samplesPerNote - envelopeSamples) {
        env = (samplesPerNote - i) / envelopeSamples;
      }
      const t = i / sampleRate;
      const sample = Math.round(amplitude * env * Math.sin(2 * Math.PI * freq * t));
      buf.writeInt16LE(sample, offset);
      offset += 2;
    }
  }
  return buf;
}
