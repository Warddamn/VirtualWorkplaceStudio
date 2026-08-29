import { useCallback, useMemo, useState } from "react";
import { StyleSheet, View, type GestureResponderEvent } from "react-native";

import { colors, spacing } from "../lib/theme";

const MAX_BARS = 60;
const BAR_AREA_HEIGHT = 48;

/** Downsample the backend's ~120 peaks to a phone-friendly bar count. */
function downsample(peaks: number[]): number[] {
  if (peaks.length <= MAX_BARS) return peaks;
  const out: number[] = [];
  const step = peaks.length / MAX_BARS;
  for (let i = 0; i < MAX_BARS; i++) {
    let max = 0;
    for (let j = Math.floor(i * step); j < Math.min(peaks.length, Math.ceil((i + 1) * step)); j++) {
      if (peaks[j] > max) max = peaks[j];
    }
    out.push(max);
  }
  return out;
}

/**
 * Peaks-based waveform scrubber (SVG-free: a row of Views with heights).
 * With no peaks (non-WAV output / request failed) it falls back to a plain
 * seekable progress bar. Drag or tap to seek; `onSeek` gets a 0..1 fraction.
 */
export function WaveformScrubber(props: {
  peaks: number[];
  /** Playback progress, 0..1. */
  progress: number;
  onSeek: (fraction: number) => void;
  enabled?: boolean;
}) {
  const { peaks, progress, onSeek, enabled = true } = props;
  const [width, setWidth] = useState(0);
  const [dragFraction, setDragFraction] = useState<number | null>(null);

  const bars = useMemo(() => downsample(peaks), [peaks]);
  const shown = dragFraction ?? progress;

  const fractionFromEvent = useCallback(
    (e: GestureResponderEvent) => {
      if (width <= 0) return 0;
      return Math.max(0, Math.min(1, e.nativeEvent.locationX / width));
    },
    [width],
  );

  const responderProps = enabled
    ? {
        onStartShouldSetResponder: () => true,
        onMoveShouldSetResponder: () => true,
        onResponderGrant: (e: GestureResponderEvent) => setDragFraction(fractionFromEvent(e)),
        onResponderMove: (e: GestureResponderEvent) => setDragFraction(fractionFromEvent(e)),
        onResponderRelease: (e: GestureResponderEvent) => {
          onSeek(fractionFromEvent(e));
          setDragFraction(null);
        },
        // Don't let the enclosing ScrollView steal the gesture mid-drag; if it
        // does anyway (native interruption), commit the pending seek rather
        // than discarding the user's drag.
        onResponderTerminationRequest: () => dragFraction === null,
        onResponderTerminate: () => {
          if (dragFraction !== null) onSeek(dragFraction);
          setDragFraction(null);
        },
      }
    : {};

  if (bars.length === 0) {
    // Plain-bar fallback (still seekable).
    return (
      <View
        style={styles.plainTrack}
        onLayout={(e) => setWidth(e.nativeEvent.layout.width)}
        {...responderProps}
      >
        <View style={[styles.plainFill, { width: `${shown * 100}%` }]} />
      </View>
    );
  }

  return (
    <View
      style={styles.waveRow}
      onLayout={(e) => setWidth(e.nativeEvent.layout.width)}
      {...responderProps}
    >
      {bars.map((peak, i) => (
        <View
          key={i}
          pointerEvents="none"
          style={[
            styles.bar,
            {
              height: Math.max(3, Math.round(peak * BAR_AREA_HEIGHT)),
              backgroundColor:
                (i + 0.5) / bars.length <= shown ? colors.accent : colors.border,
            },
          ]}
        />
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  waveRow: {
    flexDirection: "row",
    alignItems: "center",
    height: BAR_AREA_HEIGHT + spacing.sm,
    gap: 2,
    marginTop: spacing.lg,
  },
  bar: {
    flex: 1,
    borderRadius: 1,
  },
  plainTrack: {
    height: 6,
    borderRadius: 3,
    backgroundColor: colors.card,
    overflow: "hidden",
    marginTop: spacing.lg,
  },
  plainFill: {
    height: "100%",
    backgroundColor: colors.accent,
  },
});
