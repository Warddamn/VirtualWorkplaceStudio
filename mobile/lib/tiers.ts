/**
 * Bundled tier metadata for the Paywall screen and client-side clamps
 * (takes selector). The backend is authoritative — quotas are enforced
 * server-side; this mirrors docs/PRODUCT.md's tier table.
 */
import type { Tier } from "./api";

export interface TierPlan {
  tier: Tier;
  name: string;
  emoji: string;
  price: string;
  monthlyCovers: number;
  maxTakes: number;
  features: string[];
}

export const TIER_PLANS: TierPlan[] = [
  {
    tier: "free",
    name: "Free",
    emoji: "🎵",
    price: "$0",
    monthlyCovers: 3,
    maxTakes: 1,
    features: [
      "3 covers / month",
      "1 take per cover",
      "Style Studio: preview only",
      "Standard queue",
    ],
  },
  {
    tier: "plus",
    name: "Plus",
    emoji: "✨",
    price: "$7.99 / mo",
    monthlyCovers: 30,
    maxTakes: 2,
    features: [
      "30 covers / month",
      "2 takes per cover",
      "Style Studio (link / name → style)",
      "Saved styles",
      "Refine loop",
      "Standard queue",
    ],
  },
  {
    tier: "studio",
    name: "Studio",
    emoji: "🎛️",
    price: "$19.99 / mo",
    monthlyCovers: 200,
    maxTakes: 4,
    features: [
      "200 covers / month (fair use)",
      "4 takes per cover, auto-ranked",
      "Style Studio (link / name → style)",
      "Unlimited saved styles",
      "Unlimited refine loop",
      "Instrumental + stems",
      "Priority queue",
    ],
  },
];

export function planForTier(tier: Tier | null | undefined): TierPlan {
  return TIER_PLANS.find((p) => p.tier === tier) ?? TIER_PLANS[0];
}

/** Max takes per cover for a tier (free when unknown/offline). */
export function maxTakesForTier(tier: Tier | null | undefined): number {
  return planForTier(tier).maxTakes;
}
