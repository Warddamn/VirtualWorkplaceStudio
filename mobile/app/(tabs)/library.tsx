import { useFocusEffect, useRouter } from "expo-router";
import { useCallback, useMemo, useRef, useState } from "react";
import {
  FlatList,
  Pressable,
  RefreshControl,
  StyleSheet,
  Text,
  TextInput,
  View,
} from "react-native";

import { Chip } from "../../components/Chip";
import { StatusChip } from "../../components/StatusChip";
import { listCovers, type Job } from "../../lib/api";
import { groupIntoChains } from "../../lib/chains";
import { ensureBootstrapped } from "../../lib/device";
import { loadFavorites, toggleFavorite } from "../../lib/favorites";
import { findPreset } from "../../lib/stylePresets";
import { colors, radius, spacing } from "../../lib/theme";

const POLL_MS = 3000;

type Filter = "all" | "ready" | "favorites";

/** One rendered list row: a chain representative or an expanded older version. */
interface Row {
  job: Job;
  version: number;
  chainSize: number;
  rootId: string;
  /** True for the newest version of a chain (the collapsed representative). */
  isRepresentative: boolean;
}

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
  const [favorites, setFavorites] = useState<Set<string>>(new Set());
  const [query, setQuery] = useState("");
  const [filter, setFilter] = useState<Filter>("all");
  const [expanded, setExpanded] = useState<Set<string>>(new Set());
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const hadActiveRef = useRef(false);

  // Poll every 3s while the screen is focused AND any job is still active.
  useFocusEffect(
    useCallback(() => {
      let stopped = false;

      void loadFavorites().then((set) => {
        if (!stopped) setFavorites(set);
      });

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

  const star = useCallback((jobId: string) => {
    void toggleFavorite(jobId).then(setFavorites);
  }, []);

  const toggleExpanded = useCallback((rootId: string) => {
    setExpanded((current) => {
      const next = new Set(current);
      if (next.has(rootId)) {
        next.delete(rootId);
      } else {
        next.add(rootId);
      }
      return next;
    });
  }, []);

  // Group refinement chains under their newest version, then apply the
  // search/filter to each chain's members (a chain stays visible when any
  // version matches; its newest matching version represents it).
  const rows = useMemo<Row[]>(() => {
    if (!jobs) return [];
    const q = query.trim().toLowerCase();
    const matches = (job: Job): boolean => {
      if (filter === "ready" && job.status !== "succeeded") return false;
      if (filter === "favorites" && !favorites.has(job.id)) return false;
      if (q.length > 0) {
        const haystack = `${job.songName} ${styleLabel(job)} ${job.stylePrompt}`.toLowerCase();
        if (!haystack.includes(q)) return false;
      }
      return true;
    };

    const out: Row[] = [];
    for (const chain of groupIntoChains(jobs)) {
      const kept = chain.members.filter((m) => matches(m.job));
      if (kept.length === 0) continue;
      const representative = kept[kept.length - 1]; // newest matching version
      out.push({
        job: representative.job,
        version: representative.version,
        chainSize: kept.length,
        rootId: chain.rootId,
        isRepresentative: true,
      });
      if (expanded.has(chain.rootId)) {
        // Older versions, newest first, under the representative.
        for (let i = kept.length - 2; i >= 0; i--) {
          out.push({
            job: kept[i].job,
            version: kept[i].version,
            chainSize: kept.length,
            rootId: chain.rootId,
            isRepresentative: false,
          });
        }
      }
    }
    return out;
  }, [jobs, query, filter, favorites, expanded]);

  return (
    <View style={styles.screen}>
      {error !== null && <Text style={styles.error}>{error}</Text>}

      <View style={styles.controls}>
        <TextInput
          style={styles.search}
          value={query}
          onChangeText={setQuery}
          placeholder="Search by song or style 🔎"
          placeholderTextColor={colors.textDim}
          autoCapitalize="none"
        />
        <View style={styles.filterRow}>
          <Chip label="All" selected={filter === "all"} onPress={() => setFilter("all")} />
          <Chip
            label="Ready"
            selected={filter === "ready"}
            onPress={() => setFilter("ready")}
          />
          <Chip
            label="⭐ Favorites"
            selected={filter === "favorites"}
            onPress={() => setFilter("favorites")}
          />
        </View>
      </View>

      <FlatList
        data={rows}
        keyExtractor={(row) => row.job.id}
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
                {jobs.length === 0
                  ? "No covers yet — make one on the Create tab."
                  : "Nothing matches this filter."}
              </Text>
            </View>
          )
        }
        renderItem={({ item }) => (
          <Pressable
            onPress={() => openJob(item.job)}
            disabled={item.job.status !== "succeeded"}
            style={({ pressed }) => [
              styles.row,
              !item.isRepresentative && styles.rowNested,
              pressed && styles.rowPressed,
            ]}
            accessibilityRole="button"
          >
            <Text style={styles.rowEmoji}>
              {findPreset(item.job.styleId)?.emoji ?? "🎵"}
            </Text>
            <View style={styles.rowBody}>
              <Text style={styles.rowTitle} numberOfLines={1}>
                {item.job.songName}
                {item.chainSize > 1 ? `  ·  v${item.version}` : ""}
              </Text>
              <Text style={styles.rowSubtitle} numberOfLines={1}>
                {styleLabel(item.job)}
              </Text>
              {item.job.status === "failed" && item.job.error !== null && (
                <Text style={styles.rowError} numberOfLines={2}>
                  {item.job.error}
                </Text>
              )}
              {item.isRepresentative && item.chainSize > 1 && (
                <Pressable
                  onPress={() => toggleExpanded(item.rootId)}
                  accessibilityRole="button"
                  hitSlop={spacing.sm}
                >
                  <Text style={styles.versionsToggle}>
                    {expanded.has(item.rootId)
                      ? "▾ hide versions"
                      : `▸ ${item.chainSize} versions`}
                  </Text>
                </Pressable>
              )}
            </View>
            <Pressable
              onPress={() => star(item.job.id)}
              accessibilityRole="button"
              accessibilityLabel="Toggle favorite"
              hitSlop={spacing.sm}
            >
              <Text
                style={[
                  styles.star,
                  favorites.has(item.job.id) && styles.starActive,
                ]}
              >
                {favorites.has(item.job.id) ? "⭐" : "☆"}
              </Text>
            </Pressable>
            <StatusChip status={item.job.status} />
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
  controls: {
    padding: spacing.md,
    paddingBottom: 0,
    gap: spacing.sm,
  },
  search: {
    backgroundColor: colors.surface,
    borderColor: colors.border,
    borderWidth: 1,
    borderRadius: radius.md,
    color: colors.text,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm + 2,
    fontSize: 15,
  },
  filterRow: {
    flexDirection: "row",
    gap: spacing.sm,
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
  rowNested: {
    marginLeft: spacing.lg,
    backgroundColor: colors.surface,
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
  versionsToggle: {
    color: colors.accent,
    fontSize: 12,
    fontWeight: "600",
    paddingTop: 2,
  },
  star: {
    fontSize: 20,
    color: colors.textDim,
    opacity: 0.6,
  },
  starActive: {
    opacity: 1,
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
