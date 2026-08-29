/**
 * Typed API client — the ONLY module that talks to the backend.
 * Endpoint shapes mirror docs/ARCHITECTURE.md ("Endpoints" section) exactly.
 */
import { getApiUrl } from "./config";

// ---------------------------------------------------------------------------
// Shapes (mirroring the backend's API-facing types)
// ---------------------------------------------------------------------------

export type JobStatus = "queued" | "processing" | "succeeded" | "failed";

/** Jobs row, camelCased, without local filesystem paths. */
export interface Job {
  id: string;
  deviceId: string;
  songName: string;
  styleId: string | null;
  stylePrompt: string;
  status: JobStatus;
  engine: string;
  error: string | null;
  createdAt: string;
  updatedAt: string;
}

export interface StylePreset {
  id: string;
  name: string;
  emoji: string;
  description: string;
  stylePrompt: string;
}

export interface DeviceInfo {
  deviceId: string;
  credits: number;
}

export interface StylePromptPreview {
  stylePrompt: string;
  source: "llm" | "fallback";
  metadata?: { title: string; author: string };
}

export interface Health {
  ok: boolean;
  engine: string;
}

/** Audio file selected by the user (from expo-document-picker). */
export interface PickedAudio {
  uri: string;
  name: string;
  mimeType?: string;
  /** Present on web only (parity with the web File API). */
  file?: File;
}

export class ApiError extends Error {
  constructor(
    readonly status: number,
    message: string,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

// ---------------------------------------------------------------------------
// Core request helper
// ---------------------------------------------------------------------------

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${getApiUrl()}${path}`, init);
  let body: unknown = null;
  try {
    body = await res.json();
  } catch {
    // Non-JSON body (proxy error page etc.) — handled below.
  }
  if (!res.ok) {
    const message =
      body !== null &&
      typeof body === "object" &&
      "error" in body &&
      typeof (body as { error: unknown }).error === "string"
        ? (body as { error: string }).error
        : `Request failed (HTTP ${res.status})`;
    throw new ApiError(res.status, message);
  }
  if (body === null) {
    throw new ApiError(res.status, "Backend returned a non-JSON response");
  }
  return body as T;
}

function jsonInit(method: string, payload: unknown): RequestInit {
  return {
    method,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  };
}

// ---------------------------------------------------------------------------
// Endpoints
// ---------------------------------------------------------------------------

/** GET /health — pass baseUrl to probe a URL other than the saved one (Settings "Test connection"). */
export async function getHealth(baseUrl?: string): Promise<Health> {
  if (baseUrl === undefined) return request<Health>("/health");
  const res = await fetch(`${baseUrl}/health`);
  if (!res.ok) throw new Error(`Backend answered HTTP ${res.status}`);
  return (await res.json()) as Health;
}

/** GET /styles — callers fall back to the bundled list on failure. */
export async function fetchStyles(): Promise<StylePreset[]> {
  const { styles } = await request<{ styles: StylePreset[] }>("/styles");
  return styles;
}

/** POST /style-prompts — turn a text/YouTube-link reference into a style prompt. */
export function previewStylePrompt(reference: string): Promise<StylePromptPreview> {
  return request<StylePromptPreview>(
    "/style-prompts",
    jsonInit("POST", { reference }),
  );
}

/**
 * POST /covers — multipart upload starting a cover job.
 * Exactly one of `styleId` / `customStylePrompt` should be set.
 * Throws ApiError(402) when the device is out of credits.
 */
export async function createCover(params: {
  deviceId: string;
  songName: string;
  styleId?: string;
  customStylePrompt?: string;
  audio: PickedAudio;
}): Promise<Job> {
  const form = new FormData();
  if (params.audio.file) {
    // Web: a real File object.
    form.append("audio", params.audio.file, params.audio.name);
  } else {
    // Native: React Native's FormData takes { uri, name, type }.
    form.append("audio", {
      uri: params.audio.uri,
      name: params.audio.name,
      type: params.audio.mimeType ?? "audio/mpeg",
    } as unknown as Blob);
  }
  form.append("deviceId", params.deviceId);
  form.append("songName", params.songName);
  if (params.styleId) form.append("styleId", params.styleId);
  if (params.customStylePrompt) form.append("customStylePrompt", params.customStylePrompt);

  // No Content-Type header: fetch sets the multipart boundary itself.
  const { job } = await request<{ job: Job }>("/covers", {
    method: "POST",
    body: form,
  });
  return job;
}

/** GET /covers/:id */
export async function getCover(id: string): Promise<Job> {
  const { job } = await request<{ job: Job }>(`/covers/${encodeURIComponent(id)}`);
  return job;
}

/** GET /covers?deviceId= — newest first. */
export async function listCovers(deviceId: string): Promise<Job[]> {
  const { jobs } = await request<{ jobs: Job[] }>(
    `/covers?deviceId=${encodeURIComponent(deviceId)}`,
  );
  return jobs;
}

/** URL of the streamed output audio (GET /covers/:id/audio) for expo-audio. */
export function coverAudioUrl(id: string): string {
  return `${getApiUrl()}/covers/${encodeURIComponent(id)}/audio`;
}

/** POST /devices — upsert; registers the push token when provided. */
export async function registerDevice(
  deviceId: string,
  expoPushToken?: string,
): Promise<DeviceInfo> {
  const { device } = await request<{ device: DeviceInfo }>(
    "/devices",
    jsonInit("POST", expoPushToken ? { deviceId, expoPushToken } : { deviceId }),
  );
  return device;
}

/** GET /devices/:deviceId — used for the credits display. */
export async function getDevice(deviceId: string): Promise<DeviceInfo> {
  const { device } = await request<{ device: DeviceInfo }>(
    `/devices/${encodeURIComponent(deviceId)}`,
  );
  return device;
}
