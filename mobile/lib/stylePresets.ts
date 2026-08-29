/**
 * Bundled fallback copy of the shared style-preset list
 * (docs/ARCHITECTURE.md "Shared: style presets").
 *
 * The backend is authoritative via `GET /styles`; this list is only used when
 * that request fails (offline, backend not running yet, wrong URL).
 * Keep in sync with backend/src/styles.ts.
 */
import type { StylePreset } from "./api";

export const STYLE_PRESETS: StylePreset[] = [
  {
    id: "kids-choir",
    name: "Kids Choir",
    emoji: "🎒",
    description: "A joyful school-assembly children's choir with piano.",
    stylePrompt:
      "children's choir, school assembly, piano accompaniment, joyful, live room, group of young voices singing in unison and simple harmony",
  },
  {
    id: "bossa-nova",
    name: "Bossa Nova",
    emoji: "🏖️",
    description: "Laid-back Rio café bossa with nylon guitar.",
    stylePrompt:
      "bossa nova, nylon guitar, soft brushed drums, warm intimate vocals, Rio café feel",
  },
  {
    id: "synthwave-80s",
    name: "80s Synthwave",
    emoji: "🕶️",
    description: "Neon retro-futuristic analog synth drive.",
    stylePrompt:
      "80s synthwave, analog synths, gated reverb drums, neon retro-futuristic mood",
  },
  {
    id: "swing-trio",
    name: "Swing Jazz Trio",
    emoji: "🎩",
    description: "A smoky club swing trio with crooner delivery.",
    stylePrompt:
      "swing jazz trio, upright bass, brushed kit, jazz piano, crooner-style delivery",
  },
  {
    id: "campfire-folk",
    name: "Campfire Folk",
    emoji: "🔥",
    description: "Warm fingerpicked folk with group harmonies.",
    stylePrompt:
      "acoustic folk, fingerpicked guitar, warm group harmonies, intimate campfire feel",
  },
  {
    id: "gospel-choir",
    name: "Gospel Choir",
    emoji: "⛪",
    description: "Powerful massed voices and hammond organ.",
    stylePrompt:
      "gospel choir, hammond organ, claps, powerful massed voices, uplifting church energy",
  },
  {
    id: "heavy-metal",
    name: "Heavy Metal",
    emoji: "🤘",
    description: "Distorted guitars and double-kick aggression.",
    stylePrompt:
      "heavy metal, distorted guitars, double-kick drums, aggressive powerful vocals",
  },
  {
    id: "lofi-chill",
    name: "Lo-fi Chill",
    emoji: "🌙",
    description: "Dusty chillhop beats and hazy vocals.",
    stylePrompt:
      "lo-fi chillhop, dusty drums, mellow keys, relaxed hazy vocals, bedroom-producer feel",
  },
];

export function findPreset(id: string | null | undefined): StylePreset | undefined {
  if (!id) return undefined;
  return STYLE_PRESETS.find((s) => s.id === id);
}
