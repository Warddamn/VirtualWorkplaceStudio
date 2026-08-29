import Fastify, { type FastifyInstance } from "fastify";
import cors from "@fastify/cors";
import multipart from "@fastify/multipart";
import { loadConfig, type AppConfig } from "./config.js";
import { openStore, type Store } from "./db.js";
import { createEngine, type CoverEngine } from "./engines/index.js";
import { JobQueue } from "./queue.js";
import { registerRoutes } from "./routes.js";

declare module "fastify" {
  interface FastifyInstance {
    config: AppConfig;
    store: Store;
    engine: CoverEngine;
    queue: JobQueue;
  }
}

export const MAX_UPLOAD_BYTES = 50 * 1024 * 1024; // 50MB per contract

/**
 * Build the whole app: config -> sqlite store -> engine -> queue -> routes.
 * `overrides` lets tests point at a temp data dir / fast mock engine.
 */
export async function createApp(overrides: Partial<AppConfig> = {}): Promise<FastifyInstance> {
  const config = loadConfig(overrides);
  const app = Fastify({ logger: process.env.NODE_ENV !== "test" });

  const store = openStore(config.dataDir);
  const engine = createEngine(config);
  const queue = new JobQueue(store, engine, config.workers, (msg) => app.log.info(msg));

  app.decorate("config", config);
  app.decorate("store", store);
  app.decorate("engine", engine);
  app.decorate("queue", queue);

  await app.register(cors, { origin: true });
  await app.register(multipart, {
    limits: { fileSize: MAX_UPLOAD_BYTES, files: 1 },
  });

  // All error responses are `{ error: string }` JSON.
  app.setErrorHandler((err, _req, reply) => {
    const statusCode =
      typeof err.statusCode === "number" && err.statusCode >= 400 ? err.statusCode : 500;
    if (statusCode >= 500) app.log.error(err);
    void reply.status(statusCode).send({ error: err.message || "Internal server error" });
  });
  app.setNotFoundHandler((_req, reply) => {
    void reply.status(404).send({ error: "Not found" });
  });

  registerRoutes(app);

  // Jobs survive restarts: re-enqueue queued/processing rows on boot.
  const requeued = queue.requeueUnfinished();
  if (requeued > 0) app.log.info(`re-queued ${requeued} unfinished job(s) from previous run`);

  app.addHook("onClose", async () => {
    store.close();
  });

  return app;
}
