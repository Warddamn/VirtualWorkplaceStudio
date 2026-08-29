import { useAudioPlayer, useAudioPlayerStatus, setAudioModeAsync } from "expo-audio";
import { Directory, File, Paths } from "expo-file-system";
import { Stack, useLocalSearchParams } from "expo-router";
import * as Sharing from "expo-sharing";
import { useCallback, useEffect, useState } from "react";
import { Platform, Pressable, StyleSheet, Text, View } from "react-native";

import { AccentButton } from "../../components/AccentButton";
import { coverAudioUrl, getCover, type Job } from "../../lib/api";
import { findPreset } from "../../lib/stylePresets";
import { colors, radius, spacing } from "../../lib/theme";

function formatTime(seconds: number): string {
  if (!Number.isFinite(seconds) || seconds < 0) return "0:00";
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${s.toString().padStart(2, "0")}`;
}

export default function PlayerScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const [job, setJob] = useState<Job | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [sharing, setSharing] = useState(false);
  const [shareError, setShareError] = useState<string | null>(null);

  const audioUrl = coverAudioUrl(id ?? "");
  const player = useAudioPlayer({ uri: audioUrl });
  const status = useAudioPlayerStatus(player);

  useEffect(() => {
    // Play through the phone speaker even with the mute switch on.
    setAudioModeAsync({ playsInSilentMode: true }).catch(() => {});
  }, []);

  useEffect(() => {
    if (!id) return;
    let cancelled = false;
    getCover(id)
      .then((j) => {
        if (!cancelled) setJob(j);
      })
      .catch((e) => {
        if (!cancelled) setError(e instanceof Error ? e.message : "Could not load the cover");
      });
    return () => {
      cancelled = true;
    };
  }, [id]);

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

  return (
    <View style={styles.screen}>
      <Stack.Screen options={{ title: job?.songName ?? "Player" }} />

      <View style={styles.art}>
        <Text style={styles.artEmoji}>{preset?.emoji ?? "🎵"}</Text>
      </View>

      <Text style={styles.songName}>{job?.songName ?? "…"}</Text>
      <Text style={styles.styleName}>
        {preset ? `${preset.name} cover` : (job?.stylePrompt ?? "")}
      </Text>

      {error !== null && <Text style={styles.error}>{error}</Text>}

      <View style={styles.progressTrack}>
        <View style={[styles.progressFill, { width: `${progress * 100}%` }]} />
      </View>
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
        title="Share 📤"
        onPress={() => void share()}
        variant="secondary"
        loading={sharing}
      />
      {shareError !== null && <Text style={styles.error}>{shareError}</Text>}
    </View>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: colors.bg,
    alignItems: "stretch",
    padding: spacing.lg,
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
  progressTrack: {
    height: 6,
    borderRadius: 3,
    backgroundColor: colors.card,
    overflow: "hidden",
    marginTop: spacing.lg,
  },
  progressFill: {
    height: "100%",
    backgroundColor: colors.accent,
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
