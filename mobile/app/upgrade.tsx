import { useFocusEffect } from "expo-router";
import { useCallback, useState } from "react";
import { ScrollView, StyleSheet, Text, View } from "react-native";

import { AccentButton } from "../components/AccentButton";
import { getDevice, setDeviceTier, type DeviceInfo, type Tier } from "../lib/api";
import { ensureBootstrapped } from "../lib/device";
import { TIER_PLANS } from "../lib/tiers";
import { colors, radius, spacing } from "../lib/theme";

/**
 * Paywall — tier comparison from docs/PRODUCT.md. Purchasing is a DEV STUB:
 * the "Switch (dev)" buttons hit POST /devices/:id/tier, the stand-in for the
 * future App Store purchase (real billing is explicitly out of scope in v0.2).
 */
export default function UpgradeScreen() {
  const [device, setDevice] = useState<DeviceInfo | null>(null);
  const [busyTier, setBusyTier] = useState<Tier | null>(null);
  const [error, setError] = useState<string | null>(null);

  useFocusEffect(
    useCallback(() => {
      let cancelled = false;
      void (async () => {
        const { deviceId } = await ensureBootstrapped();
        try {
          const d = await getDevice(deviceId);
          if (!cancelled) setDevice(d);
        } catch (e) {
          if (!cancelled) {
            setError(e instanceof Error ? e.message : "Backend unreachable");
          }
        }
      })();
      return () => {
        cancelled = true;
      };
    }, []),
  );

  const switchTier = useCallback(async (tier: Tier) => {
    setBusyTier(tier);
    setError(null);
    try {
      const { deviceId } = await ensureBootstrapped();
      const updated = await setDeviceTier(deviceId, tier);
      setDevice(updated);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not switch the tier");
    } finally {
      setBusyTier(null);
    }
  }, []);

  return (
    <ScrollView style={styles.screen} contentContainerStyle={styles.content}>
      <Text style={styles.title}>Reliability of the magic ✨</Text>
      <Text style={styles.subtitle}>
        More covers, more takes, and the refine loop — pick the plan that fits.
      </Text>

      <View style={styles.devNote}>
        <Text style={styles.devNoteText}>
          🛠️ Developer stub — switching plans here calls a dev endpoint. Real
          purchases come with App Store billing.
        </Text>
      </View>

      {device !== null && (
        <Text style={styles.usage}>
          This month: {device.usedThisMonth} of {device.monthlyQuota} covers used ·{" "}
          {device.remaining} left
        </Text>
      )}
      {error !== null && <Text style={styles.error}>{error}</Text>}

      {TIER_PLANS.map((plan) => {
        const current = device?.tier === plan.tier;
        return (
          <View key={plan.tier} style={[styles.card, current && styles.cardCurrent]}>
            <View style={styles.cardHeader}>
              <Text style={styles.planName}>
                {plan.emoji} {plan.name}
              </Text>
              <Text style={styles.planPrice}>{plan.price}</Text>
            </View>
            {plan.features.map((feature) => (
              <Text key={feature} style={styles.feature}>
                · {feature}
              </Text>
            ))}
            {current ? (
              <View style={styles.currentBadge}>
                <Text style={styles.currentBadgeText}>Current plan</Text>
              </View>
            ) : (
              <AccentButton
                title={`Switch to ${plan.name} (dev)`}
                onPress={() => void switchTier(plan.tier)}
                variant="secondary"
                loading={busyTier === plan.tier}
                disabled={busyTier !== null}
              />
            )}
          </View>
        );
      })}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: colors.bg,
  },
  content: {
    padding: spacing.md,
    paddingBottom: spacing.xl,
    gap: spacing.sm,
  },
  title: {
    color: colors.text,
    fontSize: 22,
    fontWeight: "700",
  },
  subtitle: {
    color: colors.textDim,
    fontSize: 14,
    lineHeight: 20,
  },
  devNote: {
    backgroundColor: colors.surface,
    borderColor: colors.accent,
    borderWidth: 1,
    borderRadius: radius.md,
    padding: spacing.md,
  },
  devNoteText: {
    color: colors.textDim,
    fontSize: 13,
    lineHeight: 18,
  },
  usage: {
    color: colors.accent,
    fontSize: 13,
    fontWeight: "600",
  },
  error: {
    color: colors.danger,
    fontSize: 13,
  },
  card: {
    backgroundColor: colors.card,
    borderColor: colors.border,
    borderWidth: 1,
    borderRadius: radius.lg,
    padding: spacing.md,
    gap: spacing.xs,
  },
  cardCurrent: {
    borderColor: colors.accent,
    borderWidth: 2,
    padding: spacing.md - 1,
  },
  cardHeader: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    marginBottom: spacing.xs,
  },
  planName: {
    color: colors.text,
    fontSize: 17,
    fontWeight: "700",
  },
  planPrice: {
    color: colors.accent,
    fontSize: 15,
    fontWeight: "700",
  },
  feature: {
    color: colors.textDim,
    fontSize: 13,
    lineHeight: 19,
  },
  currentBadge: {
    alignSelf: "flex-start",
    borderColor: colors.accent,
    borderWidth: 1,
    borderRadius: radius.lg,
    paddingHorizontal: spacing.sm + 2,
    paddingVertical: spacing.xs,
    marginTop: spacing.xs,
  },
  currentBadgeText: {
    color: colors.accent,
    fontSize: 12,
    fontWeight: "700",
  },
});
