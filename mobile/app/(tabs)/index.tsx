import * as DocumentPicker from "expo-document-picker";
import { useFocusEffect, useRouter } from "expo-router";
import { useCallback, useEffect, useState } from "react";
import {
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
} from "react-native";

import { AccentButton } from "../../components/AccentButton";
import { StyleCard } from "../../components/StyleCard";
import {
  createCover,
  fetchStyles,
  getDevice,
  previewStylePrompt,
  type PickedAudio,
  type StylePreset,
  type StylePromptPreview,
} from "../../lib/api";
import { ensureBootstrapped } from "../../lib/device";
import { STYLE_PRESETS } from "../../lib/stylePresets";
import { colors, radius, spacing } from "../../lib/theme";

function stripExtension(name: string): string {
  const dot = name.lastIndexOf(".");
  return dot > 0 ? name.slice(0, dot) : name;
}

export default function CreateScreen() {
  const router = useRouter();

  const [audio, setAudio] = useState<PickedAudio | null>(null);
  const [songName, setSongName] = useState("");
  const [styles_, setStyles] = useState<StylePreset[]>(STYLE_PRESETS);
  const [selectedStyleId, setSelectedStyleId] = useState<string | null>(null);
  const [reference, setReference] = useState("");
  const [preview, setPreview] = useState<StylePromptPreview | null>(null);
  const [previewing, setPreviewing] = useState(false);
  const [credits, setCredits] = useState<number | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Style gallery: backend is authoritative, bundled list is the fallback.
  // Wait for bootstrap first — it loads the Settings URL override, and fetching
  // before that resolves would hit the bundle-time default URL on real devices.
  useEffect(() => {
    let cancelled = false;
    void (async () => {
      try {
        await ensureBootstrapped();
        const list = await fetchStyles();
        if (!cancelled && list.length > 0) setStyles(list);
      } catch {
        // Keep the bundled fallback.
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  // Credits refresh every time the screen gains focus.
  useFocusEffect(
    useCallback(() => {
      let cancelled = false;
      void (async () => {
        const { deviceId } = await ensureBootstrapped();
        try {
          const device = await getDevice(deviceId);
          if (!cancelled) setCredits(device.credits);
        } catch {
          if (!cancelled) setCredits(null);
        }
      })();
      return () => {
        cancelled = true;
      };
    }, []),
  );

  const pickAudio = useCallback(async () => {
    setError(null);
    const result = await DocumentPicker.getDocumentAsync({
      type: ["audio/*"],
      copyToCacheDirectory: true,
      multiple: false,
    });
    if (result.canceled || result.assets.length === 0) return;
    const asset = result.assets[0];
    setAudio({
      uri: asset.uri,
      name: asset.name,
      mimeType: asset.mimeType,
      file: asset.file,
    });
    setSongName((current) => (current.trim() ? current : stripExtension(asset.name)));
  }, []);

  const selectStyle = useCallback((id: string) => {
    setSelectedStyleId((current) => (current === id ? null : id));
    // A card selection replaces any custom described style.
    setPreview(null);
    setError(null);
  }, []);

  const onReferenceChange = useCallback((text: string) => {
    setReference(text);
    // The preview belongs to the text it was generated from — editing invalidates it.
    setPreview(null);
  }, []);

  const runPreview = useCallback(async () => {
    const ref = reference.trim();
    if (!ref) return;
    setPreviewing(true);
    setError(null);
    try {
      const p = await previewStylePrompt(ref);
      setPreview(p);
      setSelectedStyleId(null); // custom prompt replaces card selection
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not preview the style");
    } finally {
      setPreviewing(false);
    }
  }, [reference]);

  const canSubmit =
    audio !== null &&
    songName.trim().length > 0 &&
    (selectedStyleId !== null || preview !== null) &&
    !submitting;

  const submit = useCallback(async () => {
    if (!audio) return;
    setSubmitting(true);
    setError(null);
    try {
      const { deviceId } = await ensureBootstrapped();
      await createCover({
        deviceId,
        songName: songName.trim(),
        ...(selectedStyleId
          ? { styleId: selectedStyleId }
          : { customStylePrompt: preview?.stylePrompt }),
        audio,
      });
      // Reset the form for the next cover and show progress in Library.
      setAudio(null);
      setSongName("");
      setSelectedStyleId(null);
      setReference("");
      setPreview(null);
      router.push("/library");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not start the cover");
    } finally {
      setSubmitting(false);
    }
  }, [audio, songName, selectedStyleId, preview, router]);

  return (
    <ScrollView style={styles.screen} contentContainerStyle={styles.content}>
      <View style={styles.headerRow}>
        <Text style={styles.title}>Make a cover 🎶</Text>
        <View style={styles.creditsBadge}>
          <Text style={styles.creditsText}>
            {credits === null ? "credits: –" : `credits: ${credits}`}
          </Text>
        </View>
      </View>

      <Text style={styles.sectionLabel}>1 · Your song</Text>
      <AccentButton
        title={audio ? `🎵 ${audio.name}` : "Pick an audio file"}
        onPress={() => void pickAudio()}
        variant="secondary"
      />
      <Text style={styles.hint}>
        Use a song you own — an mp3, m4a or wav from your device.
      </Text>
      {audio !== null && (
        <TextInput
          style={styles.input}
          value={songName}
          onChangeText={setSongName}
          placeholder="Song name"
          placeholderTextColor={colors.textDim}
        />
      )}

      <Text style={styles.sectionLabel}>2 · Pick a style</Text>
      <View style={styles.grid}>
        {styles_.map((preset) => (
          <StyleCard
            key={preset.id}
            preset={preset}
            selected={preset.id === selectedStyleId}
            onPress={() => selectStyle(preset.id)}
          />
        ))}
      </View>

      <Text style={styles.orLabel}>…or describe / paste a link</Text>
      <TextInput
        style={styles.input}
        value={reference}
        onChangeText={onReferenceChange}
        placeholder='e.g. "dreamy 60s surf rock" or a YouTube link'
        placeholderTextColor={colors.textDim}
        autoCapitalize="none"
      />
      <AccentButton
        title="Preview style"
        onPress={() => void runPreview()}
        variant="secondary"
        disabled={reference.trim().length === 0}
        loading={previewing}
      />
      {preview !== null && (
        <View style={styles.previewBox}>
          <Text style={styles.previewSource}>
            {preview.source === "llm" ? "✨ generated style" : "🧩 matched style"}
            {preview.metadata ? ` · ${preview.metadata.title}` : ""}
          </Text>
          <Text style={styles.previewText}>{preview.stylePrompt}</Text>
        </View>
      )}

      {error !== null && <Text style={styles.error}>{error}</Text>}

      <AccentButton
        title="Make my cover 🎤"
        onPress={() => void submit()}
        disabled={!canSubmit}
        loading={submitting}
        big
      />
      {credits !== null && credits <= 0 && (
        <Text style={styles.error}>You're out of credits.</Text>
      )}
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
  headerRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },
  title: {
    color: colors.text,
    fontSize: 22,
    fontWeight: "700",
  },
  creditsBadge: {
    borderColor: colors.accent,
    borderWidth: 1,
    borderRadius: radius.lg,
    paddingHorizontal: spacing.sm + 2,
    paddingVertical: spacing.xs,
  },
  creditsText: {
    color: colors.accent,
    fontSize: 13,
    fontWeight: "600",
  },
  sectionLabel: {
    color: colors.textDim,
    fontSize: 13,
    fontWeight: "700",
    textTransform: "uppercase",
    letterSpacing: 1,
    marginTop: spacing.md,
  },
  hint: {
    color: colors.textDim,
    fontSize: 12,
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
  grid: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: spacing.sm,
  },
  orLabel: {
    color: colors.textDim,
    fontSize: 13,
    textAlign: "center",
    marginTop: spacing.xs,
  },
  previewBox: {
    backgroundColor: colors.card,
    borderColor: colors.border,
    borderWidth: 1,
    borderRadius: radius.md,
    padding: spacing.md,
    gap: spacing.xs,
  },
  previewSource: {
    color: colors.accent,
    fontSize: 12,
    fontWeight: "600",
  },
  previewText: {
    color: colors.text,
    fontSize: 13,
    lineHeight: 18,
  },
  error: {
    color: colors.danger,
    fontSize: 13,
    textAlign: "center",
  },
});
