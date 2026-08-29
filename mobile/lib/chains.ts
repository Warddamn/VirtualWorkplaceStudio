/**
 * Refinement version chains — jobs linked by `parentJobId` (v0.2 Refine).
 * Pure helpers shared by Library (grouped rows) and Player (version strip).
 */
import type { Job } from "./api";

export interface ChainMember {
  job: Job;
  /** 1-based version number within the chain (v1 = the original). */
  version: number;
}

export interface Chain {
  rootId: string;
  /** Ascending by version (oldest first). */
  members: ChainMember[];
}

/** Walk `parentJobId` links (cycle-safe) to the chain's root id. */
function rootIdOf(job: Job, byId: Map<string, Job>): string {
  let current = job;
  const seen = new Set<string>([current.id]);
  while (current.parentJobId) {
    const parent = byId.get(current.parentJobId);
    if (!parent || seen.has(parent.id)) break;
    seen.add(parent.id);
    current = parent;
  }
  return current.id;
}

function byCreatedAtAsc(a: Job, b: Job): number {
  if (a.createdAt !== b.createdAt) return a.createdAt < b.createdAt ? -1 : 1;
  return a.id < b.id ? -1 : 1;
}

/**
 * Group a device's jobs (any order) into refinement chains. Chains are
 * ordered newest-first by their newest member — matching the Library's
 * newest-first list — and standalone jobs are single-member chains.
 */
export function groupIntoChains(all: Job[]): Chain[] {
  const byId = new Map(all.map((j) => [j.id, j]));
  const membersByRoot = new Map<string, Job[]>();
  for (const job of all) {
    const rootId = rootIdOf(job, byId);
    const members = membersByRoot.get(rootId);
    if (members) {
      members.push(job);
    } else {
      membersByRoot.set(rootId, [job]);
    }
  }
  const chains: Chain[] = [...membersByRoot.entries()].map(([rootId, jobs]) => {
    jobs.sort(byCreatedAtAsc);
    return { rootId, members: jobs.map((job, i) => ({ job, version: i + 1 })) };
  });
  // Newest chain first = the one whose newest member is newest.
  chains.sort((a, b) =>
    byCreatedAtAsc(a.members[a.members.length - 1].job, b.members[b.members.length - 1].job) * -1,
  );
  return chains;
}

/** The full chain (ascending v1..vN) containing `jobId`, or [] when absent. */
export function chainMembersFor(all: Job[], jobId: string): ChainMember[] {
  for (const chain of groupIntoChains(all)) {
    if (chain.members.some((m) => m.job.id === jobId)) return chain.members;
  }
  return [];
}
