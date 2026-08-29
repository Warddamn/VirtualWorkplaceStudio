# Cover Studio — mobile app

Expo (SDK 57) + expo-router client for the cover-generation backend in `../backend`.
Four screens: **Create** (`/`), **Library** (`/library`), **Player** (`/cover/[id]`),
**Settings** (`/settings`). All backend traffic goes through `lib/api.ts`.

## Run against the local backend

1. Start the backend (from the repo root):

   ```sh
   cd backend && npm install && npm run dev   # http://localhost:3000, mock engine
   ```

2. Start the app:

   ```sh
   cd mobile && npm install && npx expo start
   ```

   - Press **w** for the web build — quickest way to click through the whole flow
     (`localhost:3000` works as-is).
   - Press **i** / **a** for the iOS simulator / Android emulator. iOS simulator can
     reach `localhost`; the Android emulator needs `http://10.0.2.2:3000` in Settings.
   - **On a physical phone (Expo Go):** scan the QR code, then open the app's
     **Settings** tab and set the backend URL to your computer's LAN IP, e.g.
     `http://192.168.1.23:3000` (phone and computer on the same Wi-Fi). Use
     "Test connection" to verify. The URL persists across restarts.

   You can also bake in a default URL at bundle time:

   ```sh
   EXPO_PUBLIC_API_URL=http://192.168.1.23:3000 npx expo start
   ```

   The Settings-screen override wins over `EXPO_PUBLIC_API_URL`; the fallback default
   is `http://localhost:3000`.

3. Typecheck: `npm run typecheck` (`npx tsc --noEmit`).

## Notes

- **Playback uses `expo-audio`**, the successor of `expo-av`. `expo-av` was removed
  from Expo SDK 57 (its last release targets SDK 54 and has no native module in
  current Expo Go), so the Player streams `GET /covers/:id/audio` via
  `useAudioPlayer` instead — same streaming behavior.
- **Push notifications degrade gracefully**: in Expo Go, on simulators, and on web
  no remote push token exists — the app registers the device without a token and
  everything else works. Real push needs a development build with an EAS
  `projectId` configured.
- **Style presets**: the gallery loads from `GET /styles` and silently falls back to
  the bundled copy in `lib/stylePresets.ts` (kept in sync with
  `backend/src/styles.ts`).
- On first launch the app generates a `deviceId` (uuid), persists it in
  AsyncStorage, and registers it via `POST /devices`. New devices get 10 credits
  from the backend; credits show on Create and Settings.
