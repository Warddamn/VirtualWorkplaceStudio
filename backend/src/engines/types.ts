/**
 * Engine adapter interface (docs/ARCHITECTURE.md "Engine adapter interface").
 * All engines take a local input audio file + a text style prompt and produce a
 * local output audio file. Failures reject with a human-readable Error; the job
 * queue turns that into a `failed` job — engines must never crash the process.
 */
export interface CoverEngine {
  readonly name: string; // 'mock' | 'minimax' | 'acestep'
  generateCover(req: {
    inputAudioPath: string; // local file path of user's song
    stylePrompt: string; // <=300 chars
  }): Promise<{ outputAudioPath: string }>; // local file path of result
}
