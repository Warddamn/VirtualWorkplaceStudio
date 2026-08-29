/**
 * Typed API client — the ONLY module that talks to the backend.
 * Endpoint shapes mirror docs/ARCHITECTURE.md ("Endpoints") exactly, as amended
 * by docs/ARCHITECTURE-V2.md (tiers/quota, takes, refine, custom styles,
 * song metadata, peaks).
 */
import { getApiUrl } from "./config";

// ---------------------------------------------------------------------------
// Shapes (mirroring the backend's API-facing types)
// ---------------------------------------------------------------------------

export type JobStatus = "queued" | "processing" | "succeeded" | "failed";

export type Tier = "free" | "plus" | "studio";

export type TakeStatus = "pending" | "succeeded" | "failed";

/** One generated candidate of a job ("Take A/B/C/D" in the player). */
export interface TakeInfo {
  idx: number;
  status: TakeStatus;
}

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
  // v0.2 additions:
  takes: TakeInfo[];
  selectedTake: number;
  takesRequested: number;
  instrumental: boolean;
  parentJobId: string | null;
  refineNote: string | null;
}

export interface StylePreset {
  id: string;
  name: string;
  emoji: string;
  description: string;
  stylePrompt: string;
}

/** A saved personal style ("My Styles" rail on Create). */
export interface CustomStyle {
  id: string;
  deviceId: string;
  name: string;
  emoji: string;
  stylePrompt: string;
  createdAt: string;
}

/** v0.2 device shape: tier + monthly quota (raw `credits` is gone). */
export interface DeviceInfo {
  deviceId: string;
  tier: Tier;
  monthlyQuota: number;
  usedThisMonth: number;
  remaining: number;
}

export interface StylePromptPreview {
  stylePrompt: string;
  source: "llm" | "fallback";
  metadata?: { title: string; author: string };
}

/** POST /song-metadata result — METADATA ONLY, never audio. */
export interface SongMetadata {
  title: string;
  author: string;
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
 * POST /song-metadata — resolve a YouTube link to `{ title, author }` via
 * oEmbed, server-side. Metadata only: the app NEVER downloads audio from
 * YouTube; the user still picks their own audio file of the song.
 */
export function identifySong(url: string): Promise<SongMetadata> {
  return request<SongMetadata>("/song-metadata", jsonInit("POST", { url }));
}

/**
 * POST /covers — multipart upload starting a cover job.
 * Exactly one of `styleId` / `customStylePrompt` / `customStyleId` should be
 * set. `takes` is clamped server-side to the tier max (default = tier max).
 * Throws ApiError(402) when the device's monthly quota is used up.
 */
export async function createCover(params: {
  deviceId: string;
  songName: string;
  styleId?: string;
  customStylePrompt?: string;
  customStyleId?: string;
  takes?: number;
  instrumental?: boolean;
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
  if (params.customStyleId) form.append("customStyleId", params.customStyleId);
  if (params.takes !== undefined) form.append("takes", String(params.takes));
  if (params.instrumental !== undefined) {
    form.append("instrumental", params.instrumental ? "true" : "false");
  }

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

/**
 * URL of the streamed output audio (GET /covers/:id/audio) for expo-audio.
 * Pass `take` to stream a specific take; omitted → the job's selectedTake.
 */
export function coverAudioUrl(id: string, take?: number): string {
  const base = `${getApiUrl()}/covers/${encodeURIComponent(id)}/audio`;
  return take === undefined ? base : `${base}?take=${take}`;
}

/** POST /covers/:id/pick — set the keeper take (must be a succeeded take). */
export async function pickTake(id: string, take: number): Promise<Job> {
  const { job } = await request<{ job: Job }>(
    `/covers/${encodeURIComponent(id)}/pick`,
    jsonInit("POST", { take }),
  );
  return job;
}

/**
 * POST /covers/:id/refine — "more choir, less piano" → a new child job linked
 * via parentJobId. Consumes quota like any generation (402 when empty).
 */
export async function refineCover(id: string, note: string): Promise<Job> {
  const { job } = await request<{ job: Job }>(
    `/covers/${encodeURIComponent(id)}/refine`,
    jsonInit("POST", { note }),
  );
  return job;
}

/**
 * GET /covers/:id/peaks?take=N — ~120 buckets of 0..1 RMS for the waveform
 * scrubber. Empty array (non-WAV output) → caller falls back to a plain bar.
 */
export async function fetchPeaks(id: string, take?: number): Promise<number[]> {
  const query = take === undefined ? "" : `?take=${take}`;
  const { peaks } = await request<{ peaks: number[] }>(
    `/covers/${encodeURIComponent(id)}/peaks${query}`,
  );
  return peaks;
}

// --- Custom styles ---------------------------------------------------------

/** GET /custom-styles?deviceId= — newest first. */
export async function listCustomStyles(deviceId: string): Promise<CustomStyle[]> {
  const { styles } = await request<{ styles: CustomStyle[] }>(
    `/custom-styles?deviceId=${encodeURIComponent(deviceId)}`,
  );
  return styles;
}

/** POST /custom-styles — save a style to "My Styles" (cap 50 per device). */
export async function createCustomStyle(params: {
  deviceId: string;
  name: string;
  emoji?: string;
  stylePrompt: string;
}): Promise<CustomStyle> {
  const { style } = await request<{ style: CustomStyle }>(
    "/custom-styles",
    jsonInit("POST", params),
  );
  return style;
}

/** DELETE /custom-styles/:id?deviceId= */
export async function deleteCustomStyle(id: string, deviceId: string): Promise<void> {
  await request<{ ok: true }>(
    `/custom-styles/${encodeURIComponent(id)}?deviceId=${encodeURIComponent(deviceId)}`,
    { method: "DELETE" },
  );
}

// --- Devices ---------------------------------------------------------------

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

/** GET /devices/:deviceId — used for the tier + quota display. */
export async function getDevice(deviceId: string): Promise<DeviceInfo> {
  const { device } = await request<{ device: DeviceInfo }>(
    `/devices/${encodeURIComponent(deviceId)}`,
  );
  return device;
}

/**
 * POST /devices/:deviceId/tier — DEV STUB for the future App Store purchase
 * (see the Paywall screen's visible note). Real billing is out of scope.
 */
export async function setDeviceTier(deviceId: string, tier: Tier): Promise<DeviceInfo> {
  const { device } = await request<{ device: DeviceInfo }>(
    `/devices/${encodeURIComponent(deviceId)}/tier`,
    jsonInit("POST", { tier }),
  );
  return device;
}
