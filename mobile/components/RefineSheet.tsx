import { useEffect, useState } from "react";
import { Modal, StyleSheet, Text, TextInput, View } from "react-native";

import { colors, radius, spacing } from "../lib/theme";
import { AccentButton } from "./AccentButton";

/**
 * Bottom sheet for the Refine loop: a producer's note ("more choir, less
 * piano") sent to POST /covers/:id/refine. The parent owns the API call and
 * navigates to the new child job's player on success.
 */
export function RefineSheet(props: {
  visible: boolean;
  busy: boolean;
  error: string | null;
  onSubmit: (note: string) => void;
  onClose: () => void;
}) {
  const { visible, busy, error, onSubmit, onClose } = props;
  const [note, setNote] = useState("");

  useEffect(() => {
    if (visible) setNote("");
  }, [visible]);

  return (
    <Modal visible={visible} transparent animationType="slide" onRequestClose={onClose}>
      <View style={styles.backdrop}>
        <View style={styles.sheet}>
          <Text style={styles.title}>Refine this cover 🎚️</Text>
          <Text style={styles.hint}>
            Tell the producer what to change — it re-renders as a new linked
            version.
          </Text>
          <TextInput
            style={styles.input}
            value={note}
            onChangeText={setNote}
            placeholder='e.g. "more choir, less piano" or "slower and sadder"'
            placeholderTextColor={colors.textDim}
            maxLength={300}
            multiline
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
                title="Refine ✨"
                onPress={() => onSubmit(note.trim())}
                disabled={note.trim().length === 0}
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
    justifyContent: "flex-end",
  },
  sheet: {
    backgroundColor: colors.card,
    borderColor: colors.border,
    borderWidth: 1,
    borderTopLeftRadius: radius.lg,
    borderTopRightRadius: radius.lg,
    padding: spacing.lg,
    paddingBottom: spacing.xl,
    gap: spacing.sm,
  },
  title: {
    color: colors.text,
    fontSize: 17,
    fontWeight: "700",
  },
  hint: {
    color: colors.textDim,
    fontSize: 13,
    lineHeight: 18,
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
    minHeight: 72,
    textAlignVertical: "top",
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
