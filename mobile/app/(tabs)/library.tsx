import { useFocusEffect, useRouter } from "expo-router";
import { useCallback, useRef, useState } from "react";
import {
  FlatList,
  Pressable,
  RefreshControl,
  StyleSheet,
  Text,
  View,
} from "react-native";

import { StatusChip } from "../../components/StatusChip";
import { listCovers, type Job } from "../../lib/api";
import { ensureBootstrapped } from "../../lib/device";
import { findPreset } from "../../lib/stylePresets";
import { colors, radius, spacing } from "../../lib/theme";

const POLL_MS = 3000;

function isActive(job: Job): boolean {
  return job.status === "queued" || job.status === "processing";
}

function styleLabel(job: Job): string {
  const preset = findPreset(job.styleId);
  if (preset) return `${preset.emoji} ${preset.name}`;
  return `✨ ${job.stylePrompt.slice(0, 48)}${job.stylePrompt.length > 48 ? "…" : ""}`;
}

export default function LibraryScreen() {
  const router = useRouter();
  const [jobs, setJobs] = useState<Job[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [refreshing, setRefreshing] = useState(false);
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const hadActiveRef = useRef(false);

  // Poll every 3s while the screen is focused AND any job is still active.
  useFocusEffect(
    useCallback(() => {
      let stopped = false;

      const tick = async () => {
        try {
          const { deviceId } = await ensureBootstrapped();
          const list = await listCovers(deviceId);
          if (stopped) return;
          setJobs(list);
          setError(null);
          hadActiveRef.current = list.some(isActive);
          if (hadActiveRef.current) {
            timerRef.current = setTimeout(() => void tick(), POLL_MS);
          }
        } catch (e) {
          if (stopped) return;
          setError(e instanceof Error ? e.message : "Could not load your covers");
          // Keep polling through transient failures while jobs are in flight.
          if (hadActiveRef.current) {
            timerRef.current = setTimeout(() => void tick(), POLL_MS);
          }
        }
      };

      void tick();
      return () => {
        stopped = true;
        if (timerRef.current) {
          clearTimeout(timerRef.current);
          timerRef.current = null;
        }
      };
    }, []),
  );

  const refresh = useCallback(async () => {
    setRefreshing(true);
    try {
      const { deviceId } = await ensureBootstrapped();
      const list = await listCovers(deviceId);
      setJobs(list);
      hadActiveRef.current = list.some(isActive);
      setError(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not load your covers");
    } finally {
      setRefreshing(false);
    }
  }, []);

  const openJob = useCallback(
    (job: Job) => {
      if (job.status === "succeeded") {
        router.push(`/cover/${job.id}`);
      }
    },
    [router],
  );

  return (
    <View style={styles.screen}>
      {error !== null && <Text style={styles.error}>{error}</Text>}
      <FlatList
        data={jobs ?? []}
        keyExtractor={(job) => job.id}
        contentContainerStyle={styles.list}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={() => void refresh()}
            tintColor={colors.accent}
          />
        }
        ListEmptyComponent={
          jobs === null ? null : (
            <View style={styles.empty}>
              <Text style={styles.emptyEmoji}>🎧</Text>
              <Text style={styles.emptyText}>
                No covers yet — make one on the Create tab.
              </Text>
            </View>
          )
        }
        renderItem={({ item }) => (
          <Pressable
            onPress={() => openJob(item)}
            disabled={item.status !== "succeeded"}
            style={({ pressed }) => [styles.row, pressed && styles.rowPressed]}
            accessibilityRole="button"
          >
            <Text style={styles.rowEmoji}>{findPreset(item.styleId)?.emoji ?? "🎵"}</Text>
            <View style={styles.rowBody}>
              <Text style={styles.rowTitle} numberOfLines={1}>
                {item.songName}
              </Text>
              <Text style={styles.rowSubtitle} numberOfLines={1}>
                {styleLabel(item)}
              </Text>
              {item.status === "failed" && item.error !== null && (
                <Text style={styles.rowError} numberOfLines={2}>
                  {item.error}
                </Text>
              )}
            </View>
            <StatusChip status={item.status} />
          </Pressable>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: colors.bg,
  },
  list: {
    padding: spacing.md,
    gap: spacing.sm,
    flexGrow: 1,
  },
  row: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: colors.card,
    borderColor: colors.border,
    borderWidth: 1,
    borderRadius: radius.md,
    padding: spacing.md,
    gap: spacing.md,
  },
  rowPressed: {
    opacity: 0.8,
  },
  rowEmoji: {
    fontSize: 28,
  },
  rowBody: {
    flex: 1,
    gap: 2,
  },
  rowTitle: {
    color: colors.text,
    fontSize: 15,
    fontWeight: "600",
  },
  rowSubtitle: {
    color: colors.textDim,
    fontSize: 13,
  },
  rowError: {
    color: colors.danger,
    fontSize: 12,
  },
  error: {
    color: colors.danger,
    fontSize: 13,
    textAlign: "center",
    paddingTop: spacing.sm,
  },
  empty: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    gap: spacing.sm,
  },
  emptyEmoji: {
    fontSize: 40,
  },
  emptyText: {
    color: colors.textDim,
    fontSize: 14,
  },
});
