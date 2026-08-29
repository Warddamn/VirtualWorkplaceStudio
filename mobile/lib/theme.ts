/**
 * The app's design tokens: clean dark theme, ONE accent color, emoji-forward.
 * Every screen/component pulls colors from here — no inline hex elsewhere.
 */
export const colors = {
  bg: "#0B0C10",
  surface: "#15171E",
  card: "#1B1E27",
  border: "#262A35",
  text: "#F4F5F8",
  textDim: "#8E94A3",
  accent: "#8B5CF6",
  onAccent: "#FFFFFF",
  danger: "#E5484D",
} as const;

export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
} as const;

export const radius = {
  sm: 8,
  md: 12,
  lg: 16,
} as const;
