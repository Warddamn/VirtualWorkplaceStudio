/**
 * Waveform peaks (docs/ARCHITECTURE-V2.md "Waveform peaks").
 *
 * Parses a 16-bit PCM WAV (the format the engines/mock produce — same WAV layout
 * the mock engine writes) into ~120 buckets of 0..1 RMS for the player's
 * scrubber. Anything that isn't parseable 16-bit PCM WAV yields null and the
 * route answers `{ peaks: [] }` so the client falls back to a plain progress bar.
 */

export const PEAK_BUCKETS = 120;

interface WavData {
  /** Byte offset of the PCM sample data within the buffer. */
  dataOffset: number;
  /** Byte length of the PCM sample data. */
  dataLength: number;
  channels: number;
}

/** Walk the RIFF chunks of a WAV buffer; null unless it's 16-bit PCM. */
function parseWav(buf: Buffer): WavData | null {
  if (buf.length < 44) return null;
  if (buf.toString("ascii", 0, 4) !== "RIFF" || buf.toString("ascii", 8, 12) !== "WAVE") {
    return null;
  }
  let channels = 0;
  let bitsPerSample = 0;
  let format = 0;
  let sawFmt = false;
  let offset = 12;
  while (offset + 8 <= buf.length) {
    const chunkId = buf.toString("ascii", offset, offset + 4);
    const chunkSize = buf.readUInt32LE(offset + 4);
    const body = offset + 8;
    if (chunkId === "fmt " && body + 16 <= buf.length) {
      format = buf.readUInt16LE(body);
      channels = buf.readUInt16LE(body + 2);
      bitsPerSample = buf.readUInt16LE(body + 14);
      sawFmt = true;
    } else if (chunkId === "data") {
      if (!sawFmt || format !== 1 || bitsPerSample !== 16 || channels < 1) return null;
      const dataLength = Math.min(chunkSize, buf.length - body);
      if (dataLength < 2) return null;
      return { dataOffset: body, dataLength, channels };
    }
    // Chunks are word-aligned: odd sizes carry a pad byte.
    offset = body + chunkSize + (chunkSize % 2);
  }
  return null;
}

/**
 * Compute ~`buckets` RMS values (0..1, relative to 16-bit full scale) from a WAV
 * buffer, averaging across channels. Returns null for non-WAV / non-16-bit-PCM
 * input.
 */
export function computeWavPeaks(buf: Buffer, buckets = PEAK_BUCKETS): number[] | null {
  const wav = parseWav(buf);
  if (!wav) return null;

  const frameBytes = 2 * wav.channels;
  const totalFrames = Math.floor(wav.dataLength / frameBytes);
  if (totalFrames === 0) return null;

  const bucketCount = Math.min(buckets, totalFrames);
  const peaks: number[] = [];
  for (let b = 0; b < bucketCount; b++) {
    const startFrame = Math.floor((b * totalFrames) / bucketCount);
    const endFrame = Math.floor(((b + 1) * totalFrames) / bucketCount);
    let sumSquares = 0;
    let count = 0;
    for (let f = startFrame; f < endFrame; f++) {
      const frameOffset = wav.dataOffset + f * frameBytes;
      for (let c = 0; c < wav.channels; c++) {
        const sample = buf.readInt16LE(frameOffset + c * 2) / 0x8000;
        sumSquares += sample * sample;
        count++;
      }
    }
    peaks.push(count > 0 ? Math.min(1, Math.sqrt(sumSquares / count)) : 0);
  }
  return peaks;
}
