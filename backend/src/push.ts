import { Expo } from "expo-server-sdk";

const expo = new Expo();

/**
 * Send the "your cover is ready" push notification. Best-effort: push failures
 * are logged and swallowed — they must never affect job state.
 */
export async function sendCoverReadyPush(opts: {
  expoPushToken: string | null;
  styleName: string;
  songName: string;
  jobId: string;
  log?: (msg: string) => void;
}): Promise<void> {
  const { expoPushToken, styleName, songName, jobId } = opts;
  const log = opts.log ?? (() => undefined);
  if (!expoPushToken) return;
  if (!Expo.isExpoPushToken(expoPushToken)) {
    log(`skipping push for job ${jobId}: not a valid Expo push token`);
    return;
  }
  try {
    await expo.sendPushNotificationsAsync([
      {
        to: expoPushToken,
        sound: "default",
        title: "Cover ready",
        body: `Your ${styleName} cover of ${songName} is ready 🎶`,
        data: { jobId },
      },
    ]);
  } catch (err) {
    log(`push failed for job ${jobId}: ${err instanceof Error ? err.message : String(err)}`);
  }
}
