/**
 * First-launch onboarding state — the overlay shows until dismissed once,
 * persisted in AsyncStorage like the other device-local flags.
 */
import AsyncStorage from "@react-native-async-storage/async-storage";

const ONBOARDING_KEY = "vws.onboardingDismissed";

/** True when the user has already dismissed the first-launch overlay. */
export async function isOnboardingDismissed(): Promise<boolean> {
  try {
    return (await AsyncStorage.getItem(ONBOARDING_KEY)) === "true";
  } catch {
    // Storage unavailable — don't nag on every launch in that edge case.
    return true;
  }
}

/** Persist the dismissal (best-effort). */
export async function dismissOnboarding(): Promise<void> {
  try {
    await AsyncStorage.setItem(ONBOARDING_KEY, "true");
  } catch {
    // Ignore — worst case the overlay shows again next launch.
  }
}
