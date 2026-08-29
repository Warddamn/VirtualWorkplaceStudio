import { useFocusEffect } from "expo-router";
import { useCallback, useState } from "react";
import { ScrollView, StyleSheet, Text, TextInput, View } from "react-native";

import { AccentButton } from "../../components/AccentButton";
import { getDevice, getHealth } from "../../lib/api";
import { DEFAULT_API_URL, getApiUrl, normalizeApiUrl, setApiUrl } from "../../lib/config";
import { ensureBootstrapped, reregisterDevice } from "../../lib/device";
import { colors, radius, spacing } from "../../lib/theme";

export default function SettingsScreen() {
  const [deviceId, setDeviceId] = useState<string | null>(null);
  const [credits, setCredits] = useState<number | null>(null);
  const [urlInput, setUrlInput] = useState(getApiUrl());
  const [message, setMessage] = useState<string | null>(null);
  const [messageIsError, setMessageIsError] = useState(false);
  const [busy, setBusy] = useState(false);

  const refresh = useCallback(async () => {
    const { deviceId: idValue } = await ensureBootstrapped();
    setDeviceId(idValue);
    setUrlInput(getApiUrl());
    try {
      const device = await getDevice(idValue);
      setCredits(device.credits);
    } catch {
      setCredits(null);
    }
  }, []);

  useFocusEffect(
    useCallback(() => {
      void refresh();
    }, [refresh]),
  );

  const save = useCallback(async () => {
    setBusy(true);
    setMessage(null);
    try {
      const effective = await setApiUrl(urlInput);
      setUrlInput(effective);
      // Re-register against the (possibly different) backend and pull credits.
      const device = await reregisterDevice();
      if (device) {
        setCredits(device.credits);
        setMessage(`Saved — connected to ${effective}`);
        setMessageIsError(false);
      } else {
        setCredits(null);
        setMessage(`Saved, but ${effective} didn't answer. Check the URL / backend.`);
        setMessageIsError(true);
      }
    } finally {
      setBusy(false);
    }
  }, [urlInput]);

  const testConnection = useCallback(async () => {
    setBusy(true);
    setMessage(null);
    try {
      // Probe what's typed in the field, not the previously-saved URL —
      // otherwise "Test connection" green-lights the old backend.
      const target = normalizeApiUrl(urlInput) || DEFAULT_API_URL;
      const health = await getHealth(target);
      setMessage(`Backend OK at ${target} — engine: ${health.engine}`);
      setMessageIsError(false);
    } catch (e) {
      setMessage(e instanceof Error ? e.message : "Backend unreachable");
      setMessageIsError(true);
    } finally {
      setBusy(false);
    }
  }, [urlInput]);

  return (
    <ScrollView style={styles.screen} contentContainerStyle={styles.content}>
      <Text style={styles.sectionLabel}>Backend URL</Text>
      <TextInput
        style={styles.input}
        value={urlInput}
        onChangeText={setUrlInput}
        autoCapitalize="none"
        autoCorrect={false}
        keyboardType="url"
        placeholder={DEFAULT_API_URL}
        placeholderTextColor={colors.textDim}
      />
      <Text style={styles.hint}>
        On a physical phone, use your computer's LAN IP, e.g. http://192.168.1.23:3000
        — localhost only works on web / simulators. Clear the field to reset to the
        default ({DEFAULT_API_URL}).
      </Text>
      <View style={styles.buttonRow}>
        <View style={styles.buttonFlex}>
          <AccentButton title="Save" onPress={() => void save()} loading={busy} />
        </View>
        <View style={styles.buttonFlex}>
          <AccentButton
            title="Test connection"
            onPress={() => void testConnection()}
            variant="secondary"
            disabled={busy}
          />
        </View>
      </View>
      {message !== null && (
        <Text style={[styles.message, messageIsError && styles.messageError]}>
          {message}
        </Text>
      )}

      <Text style={styles.sectionLabel}>Device</Text>
      <View style={styles.card}>
        <Text style={styles.cardLabel}>Device ID</Text>
        <Text style={styles.cardValue} selectable>
          {deviceId ?? "…"}
        </Text>
        <Text style={styles.cardLabel}>Credits</Text>
        <Text style={styles.cardValue}>
          {credits === null ? "unknown (backend unreachable)" : `${credits} 🎟️`}
        </Text>
      </View>
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
    gap: spacing.sm,
  },
  sectionLabel: {
    color: colors.textDim,
    fontSize: 13,
    fontWeight: "700",
    textTransform: "uppercase",
    letterSpacing: 1,
    marginTop: spacing.md,
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
  hint: {
    color: colors.textDim,
    fontSize: 12,
    lineHeight: 17,
  },
  buttonRow: {
    flexDirection: "row",
    gap: spacing.sm,
  },
  buttonFlex: {
    flex: 1,
  },
  message: {
    color: colors.accent,
    fontSize: 13,
  },
  messageError: {
    color: colors.danger,
  },
  card: {
    backgroundColor: colors.card,
    borderColor: colors.border,
    borderWidth: 1,
    borderRadius: radius.md,
    padding: spacing.md,
    gap: spacing.xs,
  },
  cardLabel: {
    color: colors.textDim,
    fontSize: 12,
    textTransform: "uppercase",
    letterSpacing: 1,
    marginTop: spacing.xs,
  },
  cardValue: {
    color: colors.text,
    fontSize: 14,
  },
});
