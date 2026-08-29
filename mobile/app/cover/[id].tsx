import { useAudioPlayer, useAudioPlayerStatus, setAudioModeAsync } from "expo-audio";
import { Directory, File, Paths } from "expo-file-system";
import { Stack, useLocalSearchParams, useRouter } from "expo-router";
import * as Sharing from "expo-sharing";
import { useCallback, useEffect, useRef, useState } from "react";
import {
  ActivityIndicator,
  Platform,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from "react-native";

import { AccentButton } from "../../components/AccentButton";
import { Chip } from "../../components/Chip";
import { RefineSheet } from "../../components/RefineSheet";
import { WaveformScrubber } from "../../components/WaveformScrubber";
import {
  ApiError,
  coverAudioUrl,
  fetchPeaks,
  getCover,
  listCovers,
  pickTake,
  refineCover,
  type Job,
} from "../../lib/api";
import { chainMembersFor, type ChainMember } from "../../lib/chains";
import { findPreset } from "../../lib/stylePresets";
import { colors, radius, spacing } from "../../lib/theme";

const POLL_MS = 3000;
const TAKE_LETTERS = ["A", "B", "C", "D"];

function formatTime(seconds: number): string {
  if (!Number.isFinite(seconds) || seconds < 0) return "0:00";
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${s.toString().padStart(2, "0")}`;
}

function takeLabel(idx: number): string {
  return `Take ${TAKE_LETTERS[idx] ?? idx + 1}`;
}

export default function PlayerScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const router = useRouter();
  const [job, setJob] = useState<Job | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [sharing, setSharing] = useState(false);
  const [shareError, setShareError] = useState<string | null>(null);

  // v0.2: takes, refine, version chain, waveform peaks.
  const [overrideTake, setOverrideTake] = useState<number | null>(null);
  const [picking, setPicking] = useState(false);
  const [chain, setChain] = useState<ChainMember[]>([]);
  const [peaks, setPeaks] = useState<number[]>([]);
  const [refineVisible, setRefineVisible] = useState(false);
  const [refining, setRefining] = useState(false);
  const [refineError, setRefineError] = useState<string | null>(null);
  const [quotaMessage, setQuotaMessage] = useState<string | null>(null);

  // Omitting ?take= streams the job's selectedTake server-side.
  const audioUrl = coverAudioUrl(id ?? "", overrideTake ?? undefined);
  const player = useAudioPlayer({ uri: coverAudioUrl(id ?? "") });
  const status = useAudioPlayerStatus(player);
  const prevStatusRef = useRef<Job["status"] | null>(null);

  useEffect(() => {
    // Play through the phone speaker even with the mute switch on.
    setAudioModeAsync({ playsInSilentMode: true }).catch(() => {});
  }, []);

  // Load the job — and keep polling while it's still rendering (a freshly
  // refined child job lands here queued; the audio loads once it succeeds).
  useEffect(() => {
    if (!id) return;
    let cancelled = false;
    let timer: ReturnType<typeof setTimeout> | null = null;
    const load = async () => {
      try {
        const j = await getCover(id);
        if (cancelled) return;
        // Reload the audio when the job turns succeeded — including on the very
        // first response (the mount-time source 404s if the job was still
        // rendering when the screen opened).
        const firstLoad = prevStatusRef.current === null;
        const wasActive =
          prevStatusRef.current === "queued" || prevStatusRef.current === "processing";
        prevStatusRef.current = j.status;
        setJob(j);
        setError(null);
        if ((wasActive || firstLoad) && j.status === "succeeded") {
          player.replace({ uri: coverAudioUrl(id) });
        }
        if (j.status === "queued" || j.status === "processing") {
          timer = setTimeout(() => void load(), POLL_MS);
        }
      } catch (e) {
        if (!cancelled) {
          setError(e instanceof Error ? e.message : "Could not load the cover");
        }
      }
    };
    void load();
    return () => {
      cancelled = true;
      if (timer) clearTimeout(timer);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  // Version chain: fetch the device's jobs and pull out this job's family.
  useEffect(() => {
    if (!job) return;
    let cancelled = false;
    void (async () => {
      try {
        const all = await listCovers(job.deviceId);
        if (!cancelled) setChain(chainMembersFor(all, job.id));
      } catch {
        // No strip when the list can't load.
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [job?.id, job?.status]); // eslint-disable-line react-hooks/exhaustive-deps

  // Waveform peaks for the take being played (empty → plain bar fallback).
  useEffect(() => {
    if (!id || job?.status !== "succeeded") return;
    let cancelled = false;
    void (async () => {
      try {
        const p = await fetchPeaks(id, overrideTake ?? undefined);
        if (!cancelled) setPeaks(p);
      } catch {
        if (!cancelled) setPeaks([]);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [id, job?.status, overrideTake]);

  const togglePlayback = useCallback(() => {
    if (status.playing) {
      player.pause();
    } else {
      if (status.didJustFinish || (status.duration > 0 && status.currentTime >= status.duration)) {
        void player.seekTo(0);
      }
      player.play();
    }
  }, [player, status.playing, status.didJustFinish, status.duration, status.currentTime]);

  const seekToFraction = useCallback(
    (fraction: number) => {
      if (status.duration > 0) void player.seekTo(fraction * status.duration);
    },
    [player, status.duration],
  );

  // Switching takes swaps the audio source (?take=N).
  const switchTake = useCallback(
    (idx: number) => {
      if (!id) return;
      setOverrideTake(idx);
      player.replace({ uri: coverAudioUrl(id, idx) });
    },
    [id, player],
  );

  const keepTake = useCallback(async () => {
    if (!id || overrideTake === null) return;
    setPicking(true);
    setError(null);
    try {
      const updated = await pickTake(id, overrideTake);
      setJob(updated);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not keep the take");
    } finally {
      setPicking(false);
    }
  }, [id, overrideTake]);

  const submitRefine = useCallback(
    async (note: string) => {
      if (!id || note.length === 0) return;
      setRefining(true);
      setRefineError(null);
      try {
        const child = await refineCover(id, note);
        setRefineVisible(false);
        player.pause();
        router.push(`/cover/${child.id}`);
      } catch (e) {
        if (e instanceof ApiError && e.status === 402) {
          setRefineVisible(false);
          setQuotaMessage(e.message);
        } else {
          setRefineError(e instanceof Error ? e.message : "Could not refine the cover");
        }
      } finally {
        setRefining(false);
      }
    },
    [id, player, router],
  );

  const share = useCallback(async () => {
    if (!id) return;
    setSharing(true);
    setShareError(null);
    try {
      if (Platform.OS === "web" || !(await Sharing.isAvailableAsync())) {
        setShareError(`Sharing isn't available here — the file streams from ${audioUrl}`);
        return;
      }
      // Mock engine emits WAV; hosted engines emit mp3 (see backend engines).
      const extension = job?.engine === "mock" ? "wav" : "mp3";
      const target = new File(new Directory(Paths.cache), `cover-${id}.${extension}`);
      if (target.exists) target.delete();
      const downloaded = await File.downloadFileAsync(audioUrl, target);
      await Sharing.shareAsync(downloaded.uri, {
        mimeType: extension === "wav" ? "audio/wav" : "audio/mpeg",
        dialogTitle: job ? `${job.songName} cover` : "Your cover",
      });
    } catch (e) {
      setShareError(e instanceof Error ? e.message : "Could not share the file");
    } finally {
      setSharing(false);
    }
  }, [id, audioUrl, job]);

  const preset = findPreset(job?.styleId);
  const progress =
    status.duration > 0 ? Math.min(status.currentTime / status.duration, 1) : 0;

  const ready = job?.status === "succeeded";
  const rendering = job?.status === "queued" || job?.status === "processing";
  const effectiveTake = overrideTake ?? job?.selectedTake ?? 0;
  const takes = job?.takes ?? [];
  const currentTakeInfo = takes.find((t) => t.idx === effectiveTake);
  const showKeep =
    ready &&
    overrideTake !== null &&
    job !== null &&
    overrideTake !== job.selectedTake &&
    currentTakeInfo?.status === "succeeded";

  return (
    <ScrollView style={styles.screen} contentContainerStyle={styles.content}>
      <Stack.Screen options={{ title: job?.songName ?? "Player" }} />

      <View style={styles.art}>
        <Text style={styles.artEmoji}>{preset?.emoji ?? "🎵"}</Text>
      </View>

      <Text style={styles.songName}>{job?.songName ?? "…"}</Text>
      <Text style={styles.styleName}>
        {preset ? `${preset.name} cover` : (job?.stylePrompt ?? "")}
        {job?.instrumental ? " · 🎹 instrumental" : ""}
      </Text>
      {job !== null && job.refineNote !== null && (
        <Text style={styles.refineNote}>🎚️ “{job.refineNote}”</Text>
      )}

      {chain.length > 1 && (
        <ScrollView horizontal showsHorizontalScrollIndicator={false}>
          <View style={styles.chipRow}>
            {chain.map((member, i) => (
              <View key={member.job.id} style={styles.versionItem}>
                {i > 0 && <Text style={styles.versionArrow}>→</Text>}
                <Chip
                  label={`v${member.version}`}
                  selected={member.job.id === job?.id}
                  disabled={member.job.status === "failed"}
                  onPress={() => {
                    if (member.job.id !== job?.id) {
                      player.pause();
                      router.push(`/cover/${member.job.id}`);
                    }
                  }}
                />
              </View>
            ))}
          </View>
        </ScrollView>
      )}

      {error !== null && <Text style={styles.error}>{error}</Text>}

      {rendering && (
        <View style={styles.renderingBox}>
          <ActivityIndicator color={colors.accent} />
          <Text style={styles.renderingText}>
            {job?.status === "queued" ? "Waiting in the queue…" : "Rendering your cover…"}
          </Text>
        </View>
      )}
      {job?.status === "failed" && (
        <Text style={styles.error}>{job.error ?? "This cover failed to render."}</Text>
      )}

      {ready && takes.length > 1 && (
        <View style={styles.chipRowCentered}>
          {takes.map((take) => (
            <Chip
              key={take.idx}
              label={
                takeLabel(take.idx) + (take.idx === job?.selectedTake ? " ★" : "")
              }
              selected={take.idx === effectiveTake}
              disabled={take.status !== "succeeded"}
              onPress={() => switchTake(take.idx)}
            />
          ))}
        </View>
      )}
      {showKeep && (
        <AccentButton
          title="Keep this take ★"
          onPress={() => void keepTake()}
          variant="secondary"
          loading={picking}
        />
      )}

      {ready && (
        <>
          <WaveformScrubber
            peaks={peaks}
            progress={progress}
            onSeek={seekToFraction}
            enabled={status.isLoaded}
          />
          <View style={styles.timeRow}>
            <Text style={styles.time}>{formatTime(status.currentTime)}</Text>
            <Text style={styles.time}>{formatTime(status.duration)}</Text>
          </View>

          <Pressable
            onPress={togglePlayback}
            style={({ pressed }) => [styles.playButton, pressed && styles.playPressed]}
            accessibilityRole="button"
            accessibilityLabel={status.playing ? "Pause" : "Play"}
          >
            <Text style={styles.playIcon}>{status.playing ? "⏸" : "▶️"}</Text>
          </Pressable>
          {!status.isLoaded && <Text style={styles.hint}>Loading audio…</Text>}

          <AccentButton
            title="Refine 🎚️"
            onPress={() => {
              setRefineError(null);
              setRefineVisible(true);
            }}
            variant="secondary"
          />
          <AccentButton
            title="Share 📤"
            onPress={() => void share()}
            variant="secondary"
            loading={sharing}
          />
          {shareError !== null && <Text style={styles.error}>{shareError}</Text>}
        </>
      )}

      {quotaMessage !== null && (
        <>
          <Text style={styles.error}>{quotaMessage}</Text>
          <AccentButton
            title="See plans ⭐"
            onPress={() => router.push("/upgrade")}
            variant="secondary"
          />
        </>
      )}

      <RefineSheet
        visible={refineVisible}
        busy={refining}
        error={refineError}
        onSubmit={(note) => void submitRefine(note)}
        onClose={() => setRefineVisible(false)}
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
    padding: spacing.lg,
    paddingBottom: spacing.xl,
    gap: spacing.sm,
  },
  art: {
    alignSelf: "center",
    width: 160,
    height: 160,
    borderRadius: radius.lg,
    backgroundColor: colors.card,
    borderColor: colors.border,
    borderWidth: 1,
    alignItems: "center",
    justifyContent: "center",
    marginTop: spacing.lg,
    marginBottom: spacing.md,
  },
  artEmoji: {
    fontSize: 72,
  },
  songName: {
    color: colors.text,
    fontSize: 22,
    fontWeight: "700",
    textAlign: "center",
  },
  styleName: {
    color: colors.textDim,
    fontSize: 14,
    textAlign: "center",
  },
  refineNote: {
    color: colors.textDim,
    fontSize: 13,
    fontStyle: "italic",
    textAlign: "center",
  },
  chipRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.sm,
    paddingVertical: spacing.xs,
  },
  chipRowCentered: {
    flexDirection: "row",
    flexWrap: "wrap",
    justifyContent: "center",
    gap: spacing.sm,
    marginTop: spacing.sm,
  },
  versionItem: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.sm,
  },
  versionArrow: {
    color: colors.textDim,
    fontSize: 14,
  },
  renderingBox: {
    alignItems: "center",
    gap: spacing.sm,
    paddingVertical: spacing.xl,
  },
  renderingText: {
    color: colors.textDim,
    fontSize: 14,
  },
  timeRow: {
    flexDirection: "row",
    justifyContent: "space-between",
  },
  time: {
    color: colors.textDim,
    fontSize: 12,
    fontVariant: ["tabular-nums"],
  },
  playButton: {
    alignSelf: "center",
    width: 72,
    height: 72,
    borderRadius: 36,
    backgroundColor: colors.accent,
    alignItems: "center",
    justifyContent: "center",
    marginVertical: spacing.md,
  },
  playPressed: {
    opacity: 0.85,
  },
  playIcon: {
    fontSize: 28,
    color: colors.onAccent,
  },
  hint: {
    color: colors.textDim,
    fontSize: 12,
    textAlign: "center",
  },
  error: {
    color: colors.danger,
    fontSize: 13,
    textAlign: "center",
  },
});
