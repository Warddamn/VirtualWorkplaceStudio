/**
 * Library favorites — a device-local set of job ids in AsyncStorage
 * (no accounts/sync in v0.2; see docs/ARCHITECTURE-V2.md "Out of scope").
 */
import AsyncStorage from "@react-native-async-storage/async-storage";

const FAVORITES_KEY = "vws.favorites";

let cached: Set<string> | null = null;

/** Load the favorite job ids (cached after the first read). */
export async function loadFavorites(): Promise<Set<string>> {
  if (cached) return new Set(cached);
  try {
    const raw = await AsyncStorage.getItem(FAVORITES_KEY);
    const parsed: unknown = raw ? JSON.parse(raw) : [];
    cached = new Set(
      Array.isArray(parsed) ? parsed.filter((v): v is string => typeof v === "string") : [],
    );
  } catch {
    cached = new Set();
  }
  return new Set(cached);
}

/** Toggle one job id; returns the new set. Persisting is best-effort. */
export async function toggleFavorite(jobId: string): Promise<Set<string>> {
  const favorites = await loadFavorites();
  if (favorites.has(jobId)) {
    favorites.delete(jobId);
  } else {
    favorites.add(jobId);
  }
  cached = new Set(favorites);
  try {
    await AsyncStorage.setItem(FAVORITES_KEY, JSON.stringify([...favorites]));
  } catch {
    // Storage unavailable — the in-memory set still applies this session.
  }
  return favorites;
}
