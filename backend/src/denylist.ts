/**
 * Artist-voice denylist (docs/ARCHITECTURE.md hard rule #3).
 *
 * Style prompts must describe genre / instrumentation / vibe — never imitate a named
 * artist's voice. This is a simple pattern check, not NLP: it catches the obvious
 * phrasings ("in the voice of X", "sounds like Drake", "sing it like X", ...).
 */
const ARTIST_VOICE_PATTERNS: { pattern: RegExp; label: string }[] = [
  { pattern: /\bvoice\s+of\b/i, label: '"voice of <name>"' },
  { pattern: /\bin\s+the\s+voice\b/i, label: '"in the voice of <name>"' },
  { pattern: /\bsounds?\s+like\s+[A-Z][a-z]/, label: '"sounds like <Name>"' },
  { pattern: /\bsounds?\s+(?:exactly\s+|just\s+)?like\s+(?:the\s+)?(?:singer|artist|rapper|band)\b/i, label: '"sounds like the artist"' },
  { pattern: /\bsing(?:s|ing)?\s+(?:it\s+)?like\s+[A-Z][a-z]/, label: '"sing like <Name>"' },
  { pattern: /\bimperson\w*/i, label: "impersonation" },
  { pattern: /\bvoice\s*[- ]?\s*clone\w*/i, label: "voice cloning" },
  { pattern: /\bclone\s+(?:the\s+|his\s+|her\s+|their\s+)?voice\b/i, label: "voice cloning" },
  { pattern: /\bas\s+if\s+sung\s+by\s+[A-Z][a-z]/, label: '"as if sung by <Name>"' },
  { pattern: /\bcover\s+by\s+[A-Z][a-z]/, label: '"cover by <Name>" (artist voice)' },
  { pattern: /\bvocals?\s+(?:of|from)\s+[A-Z][a-z]/, label: '"vocals of <Name>"' },
];

/**
 * Returns a human-readable description of the matched artist-voice pattern,
 * or null when the text is clean.
 */
export function findArtistVoiceViolation(text: string): string | null {
  for (const { pattern, label } of ARTIST_VOICE_PATTERNS) {
    if (pattern.test(text)) return label;
  }
  return null;
}

/** Error message used by endpoints when a prompt is refused. */
export function artistVoiceRefusalMessage(label: string): string {
  return (
    `Style prompts can't imitate a named artist's voice (matched ${label}). ` +
    "Describe the genre, instrumentation and mood instead — e.g. \"warm acoustic folk with group harmonies\"."
  );
}
