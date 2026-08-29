/**
 * Device identity + registration.
 *
 * First launch: generate a uuid deviceId, persist it, POST /devices — with an
 * Expo push token when notification permission is granted. Push registration
 * degrades gracefully: in Expo Go (no remote push since SDK 53), on
 * simulators, and on web we simply register without a token.
 */
import AsyncStorage from "@react-native-async-storage/async-storage";
import Constants from "expo-constants";
import * as Crypto from "expo-crypto";
import * as Device from "expo-device";
import * as Notifications from "expo-notifications";
import { Platform } from "react-native";

import { registerDevice, type DeviceInfo } from "./api";
import { loadApiUrl } from "./config";

const DEVICE_ID_KEY = "vws.deviceId";

let cachedDeviceId: string | null = null;

/** Stable per-install uuid, generated on first launch. */
export async function getOrCreateDeviceId(): Promise<string> {
  if (cachedDeviceId) return cachedDeviceId;
  try {
    const stored = await AsyncStorage.getItem(DEVICE_ID_KEY);
    if (stored) {
      cachedDeviceId = stored;
      return stored;
    }
  } catch {
    // fall through to generating a fresh id
  }
  const id = Crypto.randomUUID();
  cachedDeviceId = id;
  try {
    await AsyncStorage.setItem(DEVICE_ID_KEY, id);
  } catch {
    // Couldn't persist — the id lives for this session only.
  }
  return id;
}

/**
 * Best-effort Expo push token. Returns null wherever remote push can't work
 * (web, simulator, Expo Go, permission denied) instead of throwing.
 */
export async function getPushTokenSafe(): Promise<string | null> {
  try {
    if (Platform.OS === "web") return null;
    if (!Device.isDevice) return null; // simulator/emulator

    const existing = await Notifications.getPermissionsAsync();
    let status = existing.status;
    if (status !== "granted") {
      status = (await Notifications.requestPermissionsAsync()).status;
    }
    if (status !== "granted") return null;

    const projectId: string | undefined =
      Constants.expoConfig?.extra?.eas?.projectId ?? Constants.easConfig?.projectId;
    const token = await Notifications.getExpoPushTokenAsync(
      projectId ? { projectId } : {},
    );
    return token.data;
  } catch {
    // Expo Go / missing project id / anything else: no push, app still works.
    return null;
  }
}

let bootstrapPromise: Promise<{ deviceId: string; device: DeviceInfo | null }> | null =
  null;

/**
 * Idempotent app bootstrap: load the persisted backend URL, ensure a deviceId,
 * and POST /devices (with a push token when available). A failed registration
 * (backend down / wrong URL) is not fatal — screens retry via their own calls.
 */
export function ensureBootstrapped(): Promise<{
  deviceId: string;
  device: DeviceInfo | null;
}> {
  if (!bootstrapPromise) {
    bootstrapPromise = (async () => {
      await loadApiUrl();
      const deviceId = await getOrCreateDeviceId();
      const pushToken = await getPushTokenSafe();
      try {
        const device = await registerDevice(deviceId, pushToken ?? undefined);
        return { deviceId, device };
      } catch {
        return { deviceId, device: null };
      }
    })();
  }
  return bootstrapPromise;
}

/** Re-register against the (possibly new) backend URL, e.g. after Settings save. */
export async function reregisterDevice(): Promise<DeviceInfo | null> {
  const deviceId = await getOrCreateDeviceId();
  const pushToken = await getPushTokenSafe();
  try {
    return await registerDevice(deviceId, pushToken ?? undefined);
  } catch {
    return null;
  }
}
