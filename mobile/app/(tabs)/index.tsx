import * as DocumentPicker from "expo-document-picker";
import { useFocusEffect, useRouter } from "expo-router";
import { useCallback, useEffect, useState } from "react";
import {
  Alert,
  Platform,
  ScrollView,
  StyleSheet,
  Switch,
  Text,
  TextInput,
  View,
} from "react-native";

import { AccentButton } from "../../components/AccentButton";
import { Chip } from "../../components/Chip";
import { SaveStyleDialog } from "../../components/SaveStyleDialog";
import { StyleCard } from "../../components/StyleCard";
import {
  ApiError,
  createCover,
  createCustomStyle,
  deleteCustomStyle,
  fetchStyles,
  getDevice,
  identifySong,
  listCustomStyles,
  previewStylePrompt,
  type CustomStyle,
  type DeviceInfo,
  type PickedAudio,
  type SongMetadata,
  type StylePreset,
  type StylePromptPreview,
} from "../../lib/api";
import { ensureBootstrapped } from "../../lib/device";
import { applyMoment, findMoment, MOMENTS } from "../../lib/moments";
import { STYLE_PRESETS } from "../../lib/stylePresets";
import { maxTakesForTier, planForTier } from "../../lib/tiers";
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
  const [device, setDevice] = useState<DeviceInfo | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [quotaExceeded, setQuotaExceeded] = useState(false);

  // v0.2: Moments, identify-from-link, My Styles, takes + instrumental.
  const [momentId, setMomentId] = useState<string | null>(null);
  const [link, setLink] = useState("");
  const [identifying, setIdentifying] = useState(false);
  const [identified, setIdentified] = useState<SongMetadata | null>(null);
  const [identifyError, setIdentifyError] = useState<string | null>(null);
  const [myStyles, setMyStyles] = useState<CustomStyle[]>([]);
  const [selectedCustomStyleId, setSelectedCustomStyleId] = useState<string | null>(null);
  const [saveDialogVisible, setSaveDialogVisible] = useState(false);
  const [savingStyle, setSavingStyle] = useState(false);
  const [saveStyleError, setSaveStyleError] = useState<string | null>(null);
  const [takesChoice, setTakesChoice] = useState<number | null>(null); // null = tier max
  const [instrumental, setInstrumental] = useState(false);

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

  // Tier + quota and My Styles refresh every time the screen gains focus.
  useFocusEffect(
    useCallback(() => {
      let cancelled = false;
      void (async () => {
        const { deviceId } = await ensureBootstrapped();
        try {
          const d = await getDevice(deviceId);
          if (!cancelled) setDevice(d);
        } catch {
          if (!cancelled) setDevice(null);
        }
        try {
          const list = await listCustomStyles(deviceId);
          if (!cancelled) setMyStyles(list);
        } catch {
          // Keep whatever we have (offline / backend without v0.2 yet).
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

  // The three style sources (preset card / My Style / described preview) are
  // mutually exclusive — selecting one clears the others.
  const selectStyle = useCallback((id: string) => {
    setSelectedStyleId((current) => (current === id ? null : id));
    setSelectedCustomStyleId(null);
    setPreview(null);
    setError(null);
  }, []);

  const selectCustomStyle = useCallback((id: string) => {
    setSelectedCustomStyleId((current) => (current === id ? null : id));
    setSelectedStyleId(null);
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
      setSelectedCustomStyleId(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not preview the style");
    } finally {
      setPreviewing(false);
    }
  }, [reference]);

  // "Identify from a link": metadata ONLY (server-side oEmbed) — prefills the
  // song name. The app never downloads audio from YouTube.
  const runIdentify = useCallback(async () => {
    const url = link.trim();
    if (!url) return;
    setIdentifying(true);
    setIdentifyError(null);
    setIdentified(null);
    try {
      const meta = await identifySong(url);
      setIdentified(meta);
      setSongName(meta.title);
    } catch (e) {
      setIdentifyError(e instanceof Error ? e.message : "Could not identify the song");
    } finally {
      setIdentifying(false);
    }
  }, [link]);

  const saveStyle = useCallback(
    async (name: string, emoji: string) => {
      if (!preview) return;
      setSavingStyle(true);
      setSaveStyleError(null);
      try {
        const { deviceId } = await ensureBootstrapped();
        const style = await createCustomStyle({
          deviceId,
          name,
          ...(emoji ? { emoji } : {}),
          stylePrompt: preview.stylePrompt,
        });
        setMyStyles((current) => [style, ...current]);
        setSaveDialogVisible(false);
      } catch (e) {
        setSaveStyleError(e instanceof Error ? e.message : "Could not save the style");
      } finally {
        setSavingStyle(false);
      }
    },
    [preview],
  );

  const removeCustomStyle = useCallback((style: CustomStyle) => {
    const doDelete = () => {
      void (async () => {
        try {
          const { deviceId } = await ensureBootstrapped();
          await deleteCustomStyle(style.id, deviceId);
          setMyStyles((current) => current.filter((s) => s.id !== style.id));
          setSelectedCustomStyleId((current) => (current === style.id ? null : current));
        } catch (e) {
          setError(e instanceof Error ? e.message : "Could not delete the style");
        }
      })();
    };
    if (Platform.OS === "web") {
      // Alert has no buttons on web — use the browser's confirm instead of
      // deleting on a bare long-press.
      if (typeof window !== "undefined" && window.confirm(`Delete "${style.name}" from My Styles?`)) {
        doDelete();
      }
    } else {
      Alert.alert("Delete style?", `Remove "${style.name}" from My Styles.`, [
        { text: "Cancel", style: "cancel" },
        { text: "Delete", style: "destructive", onPress: doDelete },
      ]);
    }
  }, []);

  // Tier unknown (device fetch failed / offline): don't clamp to the free tier —
  // hide the selector, omit `takes`, and let the backend default to tier max.
  const maxTakes = device !== null ? maxTakesForTier(device.tier) : null;
  const effectiveTakes =
    maxTakes !== null ? Math.min(takesChoice ?? maxTakes, maxTakes) : null;
  const plan = planForTier(device?.tier);

  const canSubmit =
    audio !== null &&
    songName.trim().length > 0 &&
    (selectedStyleId !== null || selectedCustomStyleId !== null || preview !== null) &&
    !submitting;

  const submit = useCallback(async () => {
    if (!audio) return;
    setSubmitting(true);
    setError(null);
    setQuotaExceeded(false);
    try {
      const { deviceId } = await ensureBootstrapped();
      // A selected Moment appends its phrase to the chosen style guidance
      // (bundled client-side), so it always ships as a custom prompt.
      const moment = findMoment(momentId);
      const basePrompt = selectedStyleId
        ? styles_.find((s) => s.id === selectedStyleId)?.stylePrompt
        : selectedCustomStyleId
          ? myStyles.find((s) => s.id === selectedCustomStyleId)?.stylePrompt
          : preview?.stylePrompt;
      const styleParams =
        moment && basePrompt
          ? { customStylePrompt: applyMoment(basePrompt, moment) }
          : selectedStyleId
            ? { styleId: selectedStyleId }
            : selectedCustomStyleId
              ? { customStyleId: selectedCustomStyleId }
              : { customStylePrompt: preview?.stylePrompt };
      await createCover({
        deviceId,
        songName: songName.trim(),
        ...styleParams,
        // Tier unknown (offline): omit takes → the backend defaults to tier max.
        ...(effectiveTakes !== null ? { takes: effectiveTakes } : {}),
        ...(instrumental ? { instrumental: true } : {}),
        audio,
      });
      // Reset the form for the next cover and show progress in Library.
      setAudio(null);
      setSongName("");
      setSelectedStyleId(null);
      setSelectedCustomStyleId(null);
      setReference("");
      setPreview(null);
      setMomentId(null);
      setLink("");
      setIdentified(null);
      setTakesChoice(null);
      setInstrumental(false);
      router.push("/library");
    } catch (e) {
      if (e instanceof ApiError && e.status === 402) {
        setQuotaExceeded(true);
        setError(e.message);
      } else {
        setError(e instanceof Error ? e.message : "Could not start the cover");
      }
    } finally {
      setSubmitting(false);
    }
  }, [
    audio,
    songName,
    selectedStyleId,
    selectedCustomStyleId,
    preview,
    momentId,
    styles_,
    myStyles,
    effectiveTakes,
    instrumental,
    router,
  ]);

  return (
    <ScrollView style={styles.screen} contentContainerStyle={styles.content}>
      <View style={styles.headerRow}>
        <Text style={styles.title}>Make a cover 🎶</Text>
        <Chip
          label={
            device === null
              ? "plan: –"
              : `${plan.emoji} ${plan.name} · ${device.remaining}/${device.monthlyQuota}`
          }
          selected
          onPress={() => router.push("/upgrade")}
        />
      </View>

      <Text style={styles.sectionLabel}>Making it for a moment?</Text>
      <View style={styles.chipRow}>
        {MOMENTS.map((moment) => (
          <Chip
            key={moment.id}
            label={`${moment.emoji} ${moment.name}`}
            selected={momentId === moment.id}
            onPress={() =>
              setMomentId((current) => (current === moment.id ? null : moment.id))
            }
          />
        ))}
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
      {(audio !== null || songName.length > 0) && (
        <TextInput
          style={styles.input}
          value={songName}
          onChangeText={setSongName}
          placeholder="Song name"
          placeholderTextColor={colors.textDim}
        />
      )}

      <Text style={styles.orLabel}>…or identify it from a link</Text>
      <TextInput
        style={styles.input}
        value={link}
        onChangeText={(text) => {
          setLink(text);
          setIdentified(null);
          setIdentifyError(null);
        }}
        placeholder="Paste a YouTube link"
        placeholderTextColor={colors.textDim}
        autoCapitalize="none"
        autoCorrect={false}
      />
      <AccentButton
        title="Identify song 🔎"
        onPress={() => void runIdentify()}
        variant="secondary"
        disabled={link.trim().length === 0}
        loading={identifying}
      />
      {identified !== null && (
        <View style={styles.previewBox}>
          <Text style={styles.previewSource}>
            🎯 “{identified.title}” · {identified.author}
          </Text>
          <Text style={styles.previewText}>
            Now pick your own audio file of this song — the app never downloads
            from YouTube.
          </Text>
        </View>
      )}
      {identifyError !== null && <Text style={styles.error}>{identifyError}</Text>}

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

      {myStyles.length > 0 && (
        <>
          <Text style={styles.myStylesLabel}>My styles</Text>
          <ScrollView horizontal showsHorizontalScrollIndicator={false}>
            <View style={styles.chipRow}>
              {myStyles.map((style) => (
                <Chip
                  key={style.id}
                  label={`${style.emoji || "✨"} ${style.name}`}
                  selected={style.id === selectedCustomStyleId}
                  onPress={() => selectCustomStyle(style.id)}
                  onLongPress={() => removeCustomStyle(style)}
                />
              ))}
            </View>
          </ScrollView>
          <Text style={styles.hint}>Long-press a saved style to delete it.</Text>
        </>
      )}

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
          <AccentButton
            title="Save style 💾"
            onPress={() => {
              setSaveStyleError(null);
              setSaveDialogVisible(true);
            }}
            variant="secondary"
          />
        </View>
      )}

      <Text style={styles.sectionLabel}>3 · Options</Text>
      <View style={styles.optionRow}>
        <Text style={styles.optionLabel}>Takes</Text>
        {maxTakes === null ? (
          <Text style={styles.optionLabel}>auto</Text>
        ) : (
          <View style={styles.chipRow}>
            {Array.from({ length: maxTakes }, (_, i) => i + 1).map((n) => (
              <Chip
                key={n}
                label={String(n)}
                selected={n === effectiveTakes}
                onPress={() => setTakesChoice(n)}
              />
            ))}
          </View>
        )}
      </View>
      {maxTakes === 1 && (
        <Text style={styles.upsell} onPress={() => router.push("/upgrade")}>
          More takes per cover on Plus & Studio →
        </Text>
      )}
      <View style={styles.optionRow}>
        <Text style={styles.optionLabel}>Instrumental (no vocals)</Text>
        <Switch
          value={instrumental}
          onValueChange={setInstrumental}
          trackColor={{ false: colors.border, true: colors.accent }}
          thumbColor={colors.text}
        />
      </View>

      {error !== null && <Text style={styles.error}>{error}</Text>}

      <AccentButton
        title="Make my cover 🎤"
        onPress={() => void submit()}
        disabled={!canSubmit}
        loading={submitting}
        big
      />
      {(quotaExceeded || (device !== null && device.remaining <= 0)) && (
        <>
          <Text style={styles.error}>
            You've used this month's covers on the {plan.name} plan.
          </Text>
          <AccentButton
            title="See plans ⭐"
            onPress={() => router.push("/upgrade")}
            variant="secondary"
          />
        </>
      )}

      <SaveStyleDialog
        visible={saveDialogVisible}
        busy={savingStyle}
        error={saveStyleError}
        onSubmit={(name, emoji) => void saveStyle(name, emoji)}
        onClose={() => setSaveDialogVisible(false)}
      />
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
  chipRow: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: spacing.sm,
  },
  myStylesLabel: {
    color: colors.textDim,
    fontSize: 13,
    fontWeight: "700",
    textTransform: "uppercase",
    letterSpacing: 1,
    marginTop: spacing.sm,
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
  optionRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    gap: spacing.md,
  },
  optionLabel: {
    color: colors.text,
    fontSize: 14,
    fontWeight: "600",
  },
  upsell: {
    color: colors.accent,
    fontSize: 12,
  },
  error: {
    color: colors.danger,
    fontSize: 13,
    textAlign: "center",
  },
});
