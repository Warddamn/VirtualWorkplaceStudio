import { Pressable, StyleSheet, Text } from "react-native";

import { colors, radius, spacing } from "../lib/theme";

/**
 * Small pill chip — used for Moments, the takes selector, take switching in
 * the Player, Library filters and the version chain strip.
 */
export function Chip(props: {
  label: string;
  selected?: boolean;
  disabled?: boolean;
  onPress?: () => void;
  onLongPress?: () => void;
}) {
  const { label, selected, disabled, onPress, onLongPress } = props;
  return (
    <Pressable
      onPress={onPress}
      onLongPress={onLongPress}
      disabled={disabled}
      accessibilityRole="button"
      accessibilityState={{ selected: Boolean(selected), disabled: Boolean(disabled) }}
      style={({ pressed }) => [
        styles.chip,
        selected && styles.chipSelected,
        disabled && styles.chipDisabled,
        pressed && !disabled && styles.chipPressed,
      ]}
    >
      <Text style={[styles.label, selected && styles.labelSelected]}>{label}</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  chip: {
    borderRadius: radius.lg,
    borderWidth: 1,
    borderColor: colors.border,
    backgroundColor: colors.surface,
    paddingHorizontal: spacing.sm + 4,
    paddingVertical: spacing.xs + 2,
  },
  chipSelected: {
    borderColor: colors.accent,
    backgroundColor: colors.card,
  },
  chipDisabled: {
    opacity: 0.4,
  },
  chipPressed: {
    opacity: 0.8,
  },
  label: {
    color: colors.textDim,
    fontSize: 13,
    fontWeight: "600",
  },
  labelSelected: {
    color: colors.accent,
  },
});
