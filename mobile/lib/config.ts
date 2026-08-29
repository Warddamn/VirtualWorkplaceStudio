/**
 * Backend URL configuration.
 *
 * Priority: Settings-screen override (persisted in AsyncStorage)
 *   > EXPO_PUBLIC_API_URL (inlined at bundle time)
 *   > http://localhost:3000
 *
 * `localhost` only works on web / iOS simulator; a physical phone needs the
 * machine's LAN IP entered in Settings (see README).
 */
import AsyncStorage from "@react-native-async-storage/async-storage";

const API_URL_KEY = "vws.apiUrl";

export const DEFAULT_API_URL: string =
  process.env.EXPO_PUBLIC_API_URL ?? "http://localhost:3000";

let currentApiUrl: string = DEFAULT_API_URL;

/** Synchronous read of the effective backend base URL (no trailing slash). */
export function getApiUrl(): string {
  return currentApiUrl;
}

/** Load a persisted override, if any. Call once early (root layout does). */
export async function loadApiUrl(): Promise<string> {
  try {
    const stored = await AsyncStorage.getItem(API_URL_KEY);
    if (stored) currentApiUrl = stored;
  } catch {
    // Storage unavailable (rare) — keep the default.
  }
  return currentApiUrl;
}

/**
 * Set + persist an override. An empty string clears the override and returns
 * to the default. Returns the now-effective URL.
 */
export async function setApiUrl(url: string): Promise<string> {
  const trimmed = normalizeApiUrl(url);
  try {
    if (trimmed.length === 0) {
      currentApiUrl = DEFAULT_API_URL;
      await AsyncStorage.removeItem(API_URL_KEY);
    } else {
      currentApiUrl = trimmed;
      await AsyncStorage.setItem(API_URL_KEY, trimmed);
    }
  } catch {
    // Persisting failed; the in-memory value still applies for this session.
  }
  return currentApiUrl;
}

/**
 * Trim, drop trailing slashes, and default to http:// when no scheme is given —
 * the README's example is a bare LAN address like 192.168.1.23:3000.
 */
export function normalizeApiUrl(url: string): string {
  const trimmed = url.trim().replace(/\/+$/, "");
  if (trimmed.length === 0 || /^https?:\/\//i.test(trimmed)) return trimmed;
  return `http://${trimmed}`;
}
