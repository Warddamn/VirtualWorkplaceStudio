import { Stack } from "expo-router/stack";
import { StatusBar } from "expo-status-bar";
import { useEffect } from "react";

import { colors } from "../lib/theme";
import { ensureBootstrapped } from "../lib/device";

export default function RootLayout() {
  useEffect(() => {
    // First-launch bootstrap: load persisted backend URL, create/persist the
    // deviceId, register with POST /devices (push token when available).
    // Fire-and-forget: failures are non-fatal, screens fetch on their own.
    void ensureBootstrapped();
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
      </Stack>
    </>
  );
}
