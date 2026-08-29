import path from "node:path";
import type { AppConfig } from "../config.js";
import type { CoverEngine } from "./types.js";
import { MockEngine } from "./mock.js";
import { MinimaxReplicateEngine } from "./minimaxReplicate.js";
import { AceStepFalEngine } from "./aceStepFal.js";

export type { CoverEngine } from "./types.js";

/** Instantiate the engine selected by `ENGINE` (default: mock). */
export function createEngine(config: AppConfig): CoverEngine {
  const outputsDir = path.join(config.dataDir, "outputs");
  switch (config.engine) {
    case "minimax":
      return new MinimaxReplicateEngine(outputsDir, config.replicateApiToken ?? "");
    case "acestep":
      return new AceStepFalEngine(outputsDir, config.falKey ?? "");
    case "mock":
      return new MockEngine(outputsDir, config.mockDelayMs);
  }
}
