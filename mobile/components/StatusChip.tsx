import { ActivityIndicator, StyleSheet, Text, View } from "react-native";

import type { JobStatus } from "../lib/api";
import { colors, radius, spacing } from "../lib/theme";

const LABELS: Record<JobStatus, string> = {
  queued: "queued",
  processing: "processing",
  succeeded: "ready",
  failed: "failed",
};

/** Small status chip for Library rows; spins while processing. */
export function StatusChip({ status }: { status: JobStatus }) {
  const accented = status === "processing" || status === "succeeded";
  const failed = status === "failed";
  return (
    <View
      style={[
        styles.chip,
        accented && styles.chipAccent,
        failed && styles.chipFailed,
      ]}
    >
      {status === "processing" && (
        <ActivityIndicator size="small" color={colors.accent} style={styles.spinner} />
      )}
      <Text
        style={[
          styles.label,
          accented && styles.labelAccent,
          failed && styles.labelFailed,
        ]}
      >
        {LABELS[status]}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  chip: {
    flexDirection: "row",
    alignItems: "center",
    borderRadius: radius.lg,
    borderWidth: 1,
    borderColor: colors.border,
    paddingHorizontal: spacing.sm + 2,
    paddingVertical: spacing.xs,
    backgroundColor: colors.surface,
  },
  chipAccent: {
    borderColor: colors.accent,
  },
  chipFailed: {
    borderColor: colors.danger,
  },
  spinner: {
    marginRight: spacing.xs,
    transform: [{ scale: 0.7 }],
  },
  label: {
    color: colors.textDim,
    fontSize: 12,
    fontWeight: "600",
  },
  labelAccent: {
    color: colors.accent,
  },
  labelFailed: {
    color: colors.danger,
  },
});
