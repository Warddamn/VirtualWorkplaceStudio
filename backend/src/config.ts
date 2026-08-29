import fs from "node:fs";
import path from "node:path";

export type EngineName = "mock" | "minimax" | "acestep";

export interface AppConfig {
  /** TCP port for the HTTP server. */
  port: number;
  /** Which cover engine to use. */
  engine: EngineName;
  /** Root directory for the SQLite db, uploads and outputs. */
  dataDir: string;
  /** Delay before the mock engine "finishes", in ms (overridable for tests). */
  mockDelayMs: number;
  /** Number of concurrent queue workers. */
  workers: number;
  /** Optional API credentials, read from env. */
  replicateApiToken: string | undefined;
  falKey: string | undefined;
  anthropicApiKey: string | undefined;
}

function parseEngine(raw: string | undefined): EngineName {
  if (raw === "minimax" || raw === "acestep" || raw === "mock") return raw;
  return "mock";
}

/**
 * The backend package root (the directory holding package.json), found by walking
 * up from this module. Anchoring dataDir here keeps storage at backend/data both
 * in dev (running from src/) and in production (running from dist/src/).
 */
function packageRoot(): string {
  let dir = import.meta.dirname;
  for (let i = 0; i < 10; i++) {
    if (fs.existsSync(path.join(dir, "package.json"))) return dir;
    const parent = path.dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  return path.resolve(import.meta.dirname, "..");
}

/** Build the app config from the environment, with per-call overrides (used by tests). */
export function loadConfig(overrides: Partial<AppConfig> = {}): AppConfig {
  const base: AppConfig = {
    port: Number(process.env.PORT ?? 3000),
    engine: parseEngine(process.env.ENGINE),
    dataDir: process.env.DATA_DIR ?? path.join(packageRoot(), "data"),
    mockDelayMs: Number(process.env.MOCK_ENGINE_DELAY_MS ?? 5000),
    workers: 2,
    replicateApiToken: process.env.REPLICATE_API_TOKEN,
    falKey: process.env.FAL_KEY,
    anthropicApiKey: process.env.ANTHROPIC_API_KEY,
  };
  return { ...base, ...overrides };
}
