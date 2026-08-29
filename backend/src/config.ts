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

/** Build the app config from the environment, with per-call overrides (used by tests). */
export function loadConfig(overrides: Partial<AppConfig> = {}): AppConfig {
  const base: AppConfig = {
    port: Number(process.env.PORT ?? 3000),
    engine: parseEngine(process.env.ENGINE),
    dataDir: process.env.DATA_DIR ?? path.resolve(import.meta.dirname, "..", "data"),
    mockDelayMs: Number(process.env.MOCK_ENGINE_DELAY_MS ?? 5000),
    workers: 2,
    replicateApiToken: process.env.REPLICATE_API_TOKEN,
    falKey: process.env.FAL_KEY,
    anthropicApiKey: process.env.ANTHROPIC_API_KEY,
  };
  return { ...base, ...overrides };
}
