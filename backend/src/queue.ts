import type { Store } from "./db.js";
import type { CoverEngine } from "./engines/index.js";
import { getStylePreset } from "./styles.js";
import { sendCoverReadyPush } from "./push.js";

/**
 * In-process FIFO job queue drained by N concurrent workers (no Redis).
 *
 * - Jobs survive restarts: `requeueUnfinished()` re-enqueues `queued` and
 *   interrupted `processing` rows on boot; already-succeeded takes are kept and
 *   only still-pending ones re-run.
 * - A job's takes run SEQUENTIALLY in its one queue slot: the job is `succeeded`
 *   when >=1 take succeeded (failed takes are tolerated and recorded), `failed`
 *   only when all takes fail. Quota consumption is derived from job status
 *   (failed jobs don't count), so nothing is decremented here.
 * - Engine failures mark the take/job `failed` with a human-readable error and
 *   never crash the queue.
 * - On success, an Expo push is sent when the device registered a token.
 */
export class JobQueue {
  private readonly pending: string[] = [];
  private active = 0;
  private readonly inflight = new Set<Promise<void>>();

  constructor(
    private readonly store: Store,
    private readonly engine: CoverEngine,
    private readonly concurrency: number,
    private readonly log: (msg: string) => void = () => undefined,
  ) {}

  /** Re-enqueue unfinished jobs from a previous run. Call once on boot. */
  requeueUnfinished(): number {
    const rows = this.store.jobsToRequeue();
    for (const row of rows) {
      if (row.status === "processing") {
        // Interrupted mid-run by a restart — back to queued before re-running.
        this.store.setJobStatus(row.id, "queued");
      }
      this.pending.push(row.id);
    }
    this.pump();
    return rows.length;
  }

  enqueue(jobId: string): void {
    this.pending.push(jobId);
    this.pump();
  }

  /** Wait for all in-flight work to settle (used by graceful shutdown/tests). */
  async drain(): Promise<void> {
    while (this.inflight.size > 0 || this.pending.length > 0) {
      await Promise.allSettled([...this.inflight]);
      // Loop: settled workers may have pumped new pending jobs.
      if (this.inflight.size === 0 && this.pending.length === 0) break;
    }
  }

  private pump(): void {
    while (this.active < this.concurrency && this.pending.length > 0) {
      const jobId = this.pending.shift();
      if (!jobId) break;
      this.active++;
      const task = this.runJob(jobId)
        .catch((err) => {
          // runJob handles its own errors; this is a last-resort guard.
          this.log(`unexpected queue error for job ${jobId}: ${String(err)}`);
        })
        .finally(() => {
          this.active--;
          this.inflight.delete(task);
          this.pump();
        });
      this.inflight.add(task);
    }
  }

  private async runJob(jobId: string): Promise<void> {
    const job = this.store.getJob(jobId);
    if (!job) {
      this.log(`job ${jobId} vanished before processing`);
      return;
    }
    if (job.status !== "queued") return; // already handled (e.g. double enqueue)

    this.store.setJobStatus(jobId, "processing");
    this.log(`job ${jobId}: processing with engine '${this.engine.name}'`);

    // Pending take rows normally exist from job creation; ensure them anyway so
    // pre-v0.2 rows re-queued after an upgrade still run (as a single take).
    this.store.ensureTakes(jobId, Math.max(1, job.takes_requested));

    // Run the takes sequentially in this one queue slot. Succeeded takes from an
    // interrupted previous run are kept; only pending ones run now.
    const takeErrors: string[] = [];
    for (const take of this.store.listTakes(jobId)) {
      if (take.status !== "pending") {
        if (take.status === "failed" && take.error) takeErrors.push(take.error);
        continue;
      }
      try {
        const { outputAudioPath } = await this.engine.generateCover({
          inputAudioPath: job.input_path,
          stylePrompt: job.style_prompt,
          takeIndex: take.idx,
        });
        this.store.setTakeStatus(jobId, take.idx, "succeeded", {
          outputPath: outputAudioPath,
        });
        this.log(`job ${jobId}: take ${take.idx} succeeded`);
      } catch (err) {
        const message = err instanceof Error ? err.message : String(err);
        this.store.setTakeStatus(jobId, take.idx, "failed", { error: message });
        takeErrors.push(message);
        this.log(`job ${jobId}: take ${take.idx} failed — ${message}`);
      }
    }

    // >=1 succeeded take -> job succeeded; all failed -> job failed.
    const takes = this.store.listTakes(jobId);
    const firstSucceeded = takes.find((t) => t.status === "succeeded");
    if (!firstSucceeded) {
      const message =
        takes.length > 1
          ? `All ${takes.length} takes failed — ${takeErrors[0] ?? "unknown error"}`
          : (takeErrors[0] ?? "unknown error");
      this.store.setJobStatus(jobId, "failed", { error: message });
      this.log(`job ${jobId}: failed — ${message}`);
      return;
    }

    this.store.setJobStatus(jobId, "succeeded", {
      outputPath: firstSucceeded.output_path ?? undefined,
    });
    // Default keeper: the first succeeded take (POST /covers/:id/pick can change it).
    this.store.setSelectedTake(jobId, firstSucceeded.idx, firstSucceeded.output_path);
    this.log(`job ${jobId}: succeeded (${takes.filter((t) => t.status === "succeeded").length}/${takes.length} takes)`);

    const device = this.store.getDevice(job.device_id);
    const styleName = job.style_id
      ? (getStylePreset(job.style_id)?.name ?? job.style_id)
      : "custom style";
    await sendCoverReadyPush({
      expoPushToken: device?.expo_push_token ?? null,
      styleName,
      songName: job.song_name,
      jobId,
      log: this.log,
    });
  }
}
