/**
 * Tier / quota configuration (docs/ARCHITECTURE-V2.md "Tiers replace raw credits").
 *
 * Monthly quota is enforced by counting the device's jobs created in the current
 * calendar month (UTC), excluding `failed` jobs — failed covers don't consume
 * quota, refinements DO (they are generations). The legacy `credits` column is
 * kept for migration compat but unused.
 */

export type Tier = "free" | "plus" | "studio";

export interface TierConfig {
  /** Covers (jobs) allowed per calendar month (UTC). */
  monthlyQuota: number;
  /** Maximum takes per cover. */
  maxTakes: number;
}

export const TIER_CONFIG: Record<Tier, TierConfig> = {
  free: { monthlyQuota: 3, maxTakes: 1 },
  plus: { monthlyQuota: 30, maxTakes: 2 },
  studio: { monthlyQuota: 200, maxTakes: 4 },
};

export const TIERS = Object.keys(TIER_CONFIG) as Tier[];

export function isTier(value: string): value is Tier {
  return value in TIER_CONFIG;
}

/** `YYYY-MM` prefix of the current UTC calendar month, matching ISO created_at. */
export function currentUtcMonthPrefix(now = new Date()): string {
  return now.toISOString().slice(0, 7);
}
