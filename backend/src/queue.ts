import type { Store } from "./db.js";
import type { CoverEngine } from "./engines/index.js";
import { getStylePreset } from "./styles.js";
import { sendCoverReadyPush } from "./push.js";

/**
 * In-process FIFO job queue drained by N concurrent workers (no Redis).
 *
 * - Jobs survive restarts: `requeueUnfinished()` re-enqueues `queued` and
 *   interrupted `processing` rows on boot.
 * - Credits are decremented ONLY on success.
 * - Engine failures mark the job `failed` with a human-readable error and never
 *   crash the queue.
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

    try {
      const { outputAudioPath } = await this.engine.generateCover({
        inputAudioPath: job.input_path,
        stylePrompt: job.style_prompt,
      });
      this.store.setJobStatus(jobId, "succeeded", { outputPath: outputAudioPath });
      // Credits decrement on success only.
      this.store.decrementCredits(job.device_id);
      this.log(`job ${jobId}: succeeded`);

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
    } catch (err) {
      const message = err instanceof Error ? err.message : String(err);
      this.store.setJobStatus(jobId, "failed", { error: message });
      this.log(`job ${jobId}: failed — ${message}`);
    }
  }
}
