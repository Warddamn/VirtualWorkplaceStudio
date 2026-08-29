import { Stack } from "expo-router/stack";
import { StatusBar } from "expo-status-bar";
import { useCallback, useEffect, useState } from "react";

import { OnboardingOverlay } from "../components/OnboardingOverlay";
import { ensureBootstrapped } from "../lib/device";
import { dismissOnboarding, isOnboardingDismissed } from "../lib/onboarding";
import { colors } from "../lib/theme";

export default function RootLayout() {
  const [showOnboarding, setShowOnboarding] = useState(false);

  useEffect(() => {
    // First-launch bootstrap: load persisted backend URL, create/persist the
    // deviceId, register with POST /devices (push token when available).
    // Fire-and-forget: failures are non-fatal, screens fetch on their own.
    void ensureBootstrapped();
    // First launch only: show the 3-card onboarding overlay.
    void isOnboardingDismissed().then((dismissed) => {
      if (!dismissed) setShowOnboarding(true);
    });
  }, []);

  const handleDismissOnboarding = useCallback(() => {
    setShowOnboarding(false);
    void dismissOnboarding();
  }, []);

  return (
    <>
      <StatusBar style="light" />
      <Stack
        screenOptions={{
          headerStyle: { backgroundColor: colors.surface },
          headerTintColor: colors.text,
          headerTitleStyle: { color: colors.text },
          contentStyle: { backgroundColor: colors.bg },
        }}
      >
        <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
        <Stack.Screen name="cover/[id]" options={{ title: "Player" }} />
        <Stack.Screen
          name="upgrade"
          options={{ title: "Plans", presentation: "modal" }}
        />
      </Stack>
      <OnboardingOverlay visible={showOnboarding} onDismiss={handleDismissOnboarding} />
    </>
  );
}
