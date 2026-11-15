# Pitch Dark

A murder mystery you play with only your ears and your voice.

Every case happens with the lights out, so you can't see anything, ever. You hold a
button (or the space bar) and talk to the people in the room. An AI narrator and the
suspects answer out loud, each in their own voice. You find clues by listening,
touching and smelling, catch people in their lies, and name the killer before the
deadline.

## How a game goes

1. **The opening.** The narrator sets the scene, there's a body, and each suspect
   introduces themselves in their own voice.
2. **Fifteen questions.** Each question or action moves the clock 20 minutes
   (1:00 AM to dawn). Asking for help, the time, or a recap of your clues is free.
3. **Anything you can say, you can do.** "Feel the doctor's slippers." "Hollis, what
   did you hear from the boot room?" "Think back. What did I hear by the fire?"
   "Give me a hint." (A hint costs a question.)
4. **Suspects lie.** Each one has a story and holds to it until you confront them
   with the right evidence. Then they crack. Innocent people lie too, about their own
   secrets, which makes them look guilty.
5. **The accusation.** Say "I accuse …" and why. The verdict:
   - **Solved**: the right person, backed by real evidence.
   - **A lucky guess**: the right person, no evidence.
   - **The wrong person**: someone else.
   - **Gone by dawn**: time ran out and the killer walked out with everyone else.

The notebook (press N) lists the suspects, every clue you've found, and the full
transcript, for players who want to glance at it. The game is designed to be played
with your eyes closed.

## Case one: The Kell Inn

A blizzard on Larch Pass. At 12:40 AM the power fails. At 12:52 there's a crash in the
back hall, and the innkeeper, Ambrose Kell, is found dead at the bottom of the cellar
stairs. His flashlight is beside him, switched off.

| Suspect | Voice | Their story | Their secret |
|---|---|---|---|
| Marguerite Vale, niece and heir | airy | "I was in the kitchen looking for candles." | She was upstairs searching her uncle's desk, and found a blackmail letter. |
| Hollis Crane, caretaker | rounded | "I was at the woodshed till I heard the crash." | He was hiding drunk in the boot room, right by the cellar door, and heard everything. |
| Dr. Felix Okafor, retired surgeon | glassy | "I slept in my chair the whole time." | (Play it to find out.) |

The case has 14 clues: eight point to the killer, and the rest are red herrings. Each
clue is something you discover by sound, touch, smell or memory, because there's no
light. The full case file, with the solution, is the `KELL` object in `index.html`.
Spoilers are in there.

## Endless cases

"Write me a brand-new case" asks Claude to invent a whole new mystery: a new setting
in total darkness (a cave, a stalled ship, a mine), three suspects, a killer, a
timeline, clues and red herrings. It uses the same format as the hand-built case.

## How it's built

A single HTML page that runs as a claude.ai artifact and uses four platform
capabilities:

| Need | Capability | Notes |
|---|---|---|
| Hear the player | `dictation` | Push to talk: hold to speak, or tap once to start and tap again to send. |
| Speak the story | `tts` | Narrator plus one voice per suspect. Replies are spoken line by line as they stream in, so the first words come out fast. |
| Run the story | `sample` | Each turn sends the rules, the secret case file, the state and the transcript. Claude replies with one JSON line per spoken line, then a meta line (`found`, `tick`, `end`, `accused`). |
| One permission prompt | `permissions` | Asks for the microphone and Claude together when the case begins. |

The page itself tracks the clock, the clues (only ids from the case file count), the
deadline, the endings and saved progress. The model only has to act and judge.

Sound design is synthesized in the page with Web Audio: wind and fire crackle in the
background, quieter while you talk, a grandfather-clock tick while the narrator
thinks, chimes when listening starts and stops, and a low bell when you find a clue.

Without voice (Safari, Firefox, the mobile apps) it falls back to typing, and to text
on screen when read-aloud isn't available.

Keys: **Space** talk · **R** repeat · **N** notebook · **T** type · **Esc** stop the voice
