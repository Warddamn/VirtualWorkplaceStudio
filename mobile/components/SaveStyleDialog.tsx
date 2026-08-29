import { useEffect, useState } from "react";
import { Modal, StyleSheet, Text, TextInput, View } from "react-native";

import { colors, radius, spacing } from "../lib/theme";
import { AccentButton } from "./AccentButton";

/**
 * Name + emoji dialog for saving a previewed custom style to "My Styles"
 * (POST /custom-styles). The parent owns the actual API call.
 */
export function SaveStyleDialog(props: {
  visible: boolean;
  busy: boolean;
  error: string | null;
  onSubmit: (name: string, emoji: string) => void;
  onClose: () => void;
}) {
  const { visible, busy, error, onSubmit, onClose } = props;
  const [name, setName] = useState("");
  const [emoji, setEmoji] = useState("✨");

  // Fresh fields each time the dialog opens.
  useEffect(() => {
    if (visible) {
      setName("");
      setEmoji("✨");
    }
  }, [visible]);

  return (
    <Modal visible={visible} transparent animationType="fade" onRequestClose={onClose}>
      <View style={styles.backdrop}>
        <View style={styles.card}>
          <Text style={styles.title}>Save to My Styles 💾</Text>
          <Text style={styles.label}>Name</Text>
          <TextInput
            style={styles.input}
            value={name}
            onChangeText={setName}
            placeholder='e.g. "My rainy-day choir"'
            placeholderTextColor={colors.textDim}
            maxLength={60}
          />
          <Text style={styles.label}>Emoji</Text>
          <TextInput
            style={styles.input}
            value={emoji}
            onChangeText={setEmoji}
            placeholder="✨"
            placeholderTextColor={colors.textDim}
            maxLength={8}
          />
          {error !== null && <Text style={styles.error}>{error}</Text>}
          <View style={styles.buttonRow}>
            <View style={styles.buttonFlex}>
              <AccentButton
                title="Cancel"
                onPress={onClose}
                variant="secondary"
                disabled={busy}
              />
            </View>
            <View style={styles.buttonFlex}>
              <AccentButton
                title="Save"
                onPress={() => onSubmit(name.trim(), emoji.trim())}
                disabled={name.trim().length === 0}
                loading={busy}
              />
            </View>
          </View>
        </View>
      </View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  backdrop: {
    flex: 1,
    backgroundColor: "rgba(0,0,0,0.6)",
    alignItems: "center",
    justifyContent: "center",
    padding: spacing.lg,
  },
  card: {
    alignSelf: "stretch",
    backgroundColor: colors.card,
    borderColor: colors.border,
    borderWidth: 1,
    borderRadius: radius.lg,
    padding: spacing.lg,
    gap: spacing.sm,
  },
  title: {
    color: colors.text,
    fontSize: 17,
    fontWeight: "700",
  },
  label: {
    color: colors.textDim,
    fontSize: 12,
    textTransform: "uppercase",
    letterSpacing: 1,
    marginTop: spacing.xs,
  },
  input: {
    backgroundColor: colors.surface,
    borderColor: colors.border,
    borderWidth: 1,
    borderRadius: radius.md,
    color: colors.text,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm + 2,
    fontSize: 15,
  },
  error: {
    color: colors.danger,
    fontSize: 13,
  },
  buttonRow: {
    flexDirection: "row",
    gap: spacing.sm,
    marginTop: spacing.sm,
  },
  buttonFlex: {
    flex: 1,
  },
});
