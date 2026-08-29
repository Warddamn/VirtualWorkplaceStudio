import { useAudioPlayer, useAudioPlayerStatus } from "expo-audio";
import { useCallback, useState } from "react";
import { Modal, Pressable, StyleSheet, Text, View } from "react-native";

import { colors, radius, spacing } from "../lib/theme";
import { AccentButton } from "./AccentButton";

// Small bundled demo cover (~5s synthesized melody, 16-bit PCM WAV) so the
// very first sound in the app is instant — no backend needed.
// eslint-disable-next-line @typescript-eslint/no-var-requires
const DEMO_COVER = require("../assets/demo-cover.wav") as number;

const CARDS = [
  {
    emoji: "🎵",
    title: "Pick a song you own",
    body:
      "Start from an mp3, m4a or wav on your device — or a voice memo of you singing. " +
      "A pasted link only identifies the song; the app never downloads audio from YouTube.",
  },
  {
    emoji: "🎨",
    title: "Choose any style",
    body:
      "Preset cards, occasion Moments, or describe your own — then save the keepers " +
      "to My Styles and reuse them on any song.",
  },
  {
    emoji: "🎛️",
    title: "Takes & refine",
    body:
      "Premium covers render multiple takes — flip between Take A/B/C/D, keep the best, " +
      'then refine it like talking to a producer: "more choir, less piano".',
  },
] as const;

/** First-launch onboarding overlay (3 cards + an instantly-playable demo). */
export function OnboardingOverlay(props: { visible: boolean; onDismiss: () => void }) {
  const { visible, onDismiss } = props;
  const [page, setPage] = useState(0);

  const demoPlayer = useAudioPlayer(DEMO_COVER);
  const demoStatus = useAudioPlayerStatus(demoPlayer);

  const toggleDemo = useCallback(() => {
    if (demoStatus.playing) {
      demoPlayer.pause();
    } else {
      if (
        demoStatus.didJustFinish ||
        (demoStatus.duration > 0 && demoStatus.currentTime >= demoStatus.duration)
      ) {
        void demoPlayer.seekTo(0);
      }
      demoPlayer.play();
    }
  }, [demoPlayer, demoStatus]);

  const finish = useCallback(() => {
    demoPlayer.pause();
    setPage(0);
    onDismiss();
  }, [demoPlayer, onDismiss]);

  const last = page === CARDS.length - 1;
  const card = CARDS[page];

  return (
    <Modal visible={visible} transparent animationType="fade" onRequestClose={finish}>
      <View style={styles.backdrop}>
        <View style={styles.card}>
          <Text style={styles.emoji}>{card.emoji}</Text>
          <Text style={styles.title}>{card.title}</Text>
          <Text style={styles.body}>{card.body}</Text>

          {last && (
            <AccentButton
              title={demoStatus.playing ? "Pause the demo ⏸" : "Hear a demo cover ▶️"}
              onPress={toggleDemo}
              variant="secondary"
            />
          )}

          <View style={styles.dots}>
            {CARDS.map((_, i) => (
              <View key={i} style={[styles.dot, i === page && styles.dotActive]} />
            ))}
          </View>

          <AccentButton
            title={last ? "Get started 🎤" : "Next"}
            onPress={() => (last ? finish() : setPage((p) => p + 1))}
            big
          />
          {!last && (
            <Pressable onPress={finish} accessibilityRole="button">
              <Text style={styles.skip}>Skip</Text>
            </Pressable>
          )}
        </View>
      </View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  backdrop: {
    flex: 1,
    backgroundColor: "rgba(0,0,0,0.75)",
    alignItems: "center",
    justifyContent: "center",
    padding: spacing.lg,
  },
  card: {
    alignSelf: "stretch",
    backgroundColor: colors.card,
    borderColor: colors.border,
    borderWidth: 1,
    borderRadius: radius.lg,
    padding: spacing.xl,
    gap: spacing.md,
    alignItems: "stretch",
  },
  emoji: {
    fontSize: 56,
    textAlign: "center",
  },
  title: {
    color: colors.text,
    fontSize: 20,
    fontWeight: "700",
    textAlign: "center",
  },
  body: {
    color: colors.textDim,
    fontSize: 14,
    lineHeight: 20,
    textAlign: "center",
  },
  dots: {
    flexDirection: "row",
    justifyContent: "center",
    gap: spacing.sm,
    marginTop: spacing.xs,
  },
  dot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: colors.border,
  },
  dotActive: {
    backgroundColor: colors.accent,
  },
  skip: {
    color: colors.textDim,
    fontSize: 13,
    textAlign: "center",
    paddingVertical: spacing.xs,
  },
});
