import { Pressable, StyleSheet, Text } from "react-native";

import type { StylePreset } from "../lib/api";
import { colors, radius, spacing } from "../lib/theme";

/** Emoji-forward style card for the Create screen's gallery grid. */
export function StyleCard(props: {
  preset: StylePreset;
  selected: boolean;
  onPress: () => void;
}) {
  const { preset, selected, onPress } = props;
  return (
    <Pressable
      onPress={onPress}
      style={({ pressed }) => [
        styles.card,
        selected && styles.cardSelected,
        pressed && styles.cardPressed,
      ]}
      accessibilityRole="button"
      accessibilityState={{ selected }}
      accessibilityLabel={`${preset.name} style`}
    >
      <Text style={styles.emoji}>{preset.emoji}</Text>
      <Text style={styles.name}>{preset.name}</Text>
      <Text style={styles.description} numberOfLines={2}>
        {preset.description}
      </Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  card: {
    flexBasis: "47%",
    flexGrow: 1,
    backgroundColor: colors.card,
    borderColor: colors.border,
    borderWidth: 1,
    borderRadius: radius.md,
    padding: spacing.md,
    alignItems: "center",
    gap: spacing.xs,
  },
  cardSelected: {
    borderColor: colors.accent,
    borderWidth: 2,
    padding: spacing.md - 1,
  },
  cardPressed: {
    opacity: 0.8,
  },
  emoji: {
    fontSize: 34,
  },
  name: {
    color: colors.text,
    fontSize: 15,
    fontWeight: "600",
    textAlign: "center",
  },
  description: {
    color: colors.textDim,
    fontSize: 12,
    textAlign: "center",
  },
});
