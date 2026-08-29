/**
 * "Moments" — occasion framing chips on the Create screen (docs/PRODUCT.md
 * pillar 4). Bundled client-side: each moment appends a phrase to whichever
 * style guidance the user picked; the backend just sees the final prompt.
 */
export interface Moment {
  id: string;
  name: string;
  emoji: string;
  /** Appended to the style prompt when this moment is active. */
  phrase: string;
}

export const MOMENTS: Moment[] = [
  {
    id: "birthday",
    name: "Birthday",
    emoji: "🎂",
    phrase: "joyful birthday celebration feel, festive and warm",
  },
  {
    id: "lullaby",
    name: "Lullaby",
    emoji: "🌙",
    phrase: "gentle lullaby feel, slow, soft and soothing for bedtime",
  },
  {
    id: "wedding",
    name: "Wedding",
    emoji: "💍",
    phrase: "romantic first-dance wedding feel, tender and elegant",
  },
  {
    id: "holiday",
    name: "Holiday",
    emoji: "🎄",
    phrase: "festive holiday feel, sleigh bells and cozy seasonal warmth",
  },
  {
    id: "graduation",
    name: "Graduation",
    emoji: "🎓",
    phrase: "triumphant graduation anthem feel, proud and uplifting",
  },
];

export function findMoment(id: string | null): Moment | null {
  if (!id) return null;
  return MOMENTS.find((m) => m.id === id) ?? null;
}

/**
 * Append a moment's phrase to a style prompt, keeping the backend's
 * 300-char style-prompt limit intact.
 */
export function applyMoment(stylePrompt: string, moment: Moment | null): string {
  if (!moment) return stylePrompt;
  return `${stylePrompt}, ${moment.phrase}`.slice(0, 300);
}
