# Pitch Dark

Short audio games you play by listening and talking out loud. There's nothing to look
at, so you can close your eyes. An AI host and a cast of voices talk back.

There are four quick daily puzzles, a turn-based adventure and a longer mystery. Each
daily puzzle is the same for everyone that day and gives a result you can share. The
four quick games take a minute or two and have unlimited practice rounds.

## The games

### The Link (daily)
Five words share one hidden connection. They're read out one at a time, hardest first:
*Florida… Map… Piano…* Say what links them ("things with keys"). Say "next" to hear
another word; a wrong guess also reveals the next one. You score better the earlier you
get it.
Share: `🟥🟥🟩⬜⬜`

### Warmer (daily)
There's a secret word. Say any word and you'll hear how close it is in meaning:
freezing, cold, warm, hot, burning. A rising tone tells you the same thing by ear. You
get 20 guesses, with hints after guesses 6, 12 and 16. It works by meaning, not
spelling, because speech-to-text can't tell "cord" from "chord".
Share: `🟦🟨🟧🟥✅  Found in 5`

### Who's Lying? (daily)
Sam, Max and Robin each say one fact about today's topic. One of them is lying. You can
ask each of them one follow-up question, and the liar bluffs. Then name the liar. Every
lie is a common myth, and the true facts are surprising, so you learn something either
way.
Share: `✅ Caught the liar · 1 question`

### The Box (daily)
Something is hidden in a box. Say "shake the box" to hear it: it might rattle, slosh,
jingle, tick or squeak (all synthesized in the page). Then ask up to 10 yes-or-no
questions and guess.
Share: `⬛⬛⬛📦  Opened in 4`

### Quest (adventure)
A text adventure you play out loud, one turn at a time. The narrator sets a short
scene, you say what you do in your own words, and the story answers.
- **One clear goal** per story, at most three characters with simple names, and at most
  four things to carry.
- **Free questions:** "where am I?", "what am I carrying?" and "what's my goal?" are
  answered instantly and don't use a turn.
- **Turns:** you get 6, 9 or 12. A story can be finished in about 6, so more turns means
  more room to explore, and finishing in fewer is a better score. The page sets the pace
  and sends the narrator a short director's note each turn, so the story ends on time.
- **A little luck:** every turn has a hidden dice roll, so risky moves can go well or
  badly. Nothing ever goes worse than a small setback.
- **Daily adventure:** 27 hand-edited stories, such as "The Borrowed Dinosaur Bone" and
  "The Shy Tuba", one per day.
- **Make your own:** say any idea ("a pirate dog looking for treasure") and Claude builds
  an original story around it.
Share: `The Borrowed Dinosaur Bone  ✅ Finished in 8 of 9 turns`

### Lights Out (mystery)
A whodunit in the pitch dark at a snowbound inn. Question the suspects, feel and smell
for clues, and name the killer before dawn.
- **Simple names:** Rose (niece), Hank (handyman), Doctor Bell, Lily (cook) and Tom
  (salesman). Names stay on screen, and you can ask "who's here?" at any time.
- **Difficulty:** choose 3, 4 or 5 suspects. Each extra suspect is an innocent with
  their own secret and red herrings.
- **Question limit:** 8, 12, 20, or no limit.
- **Free actions:** small talk, recaps and "who's who" don't use up questions.
- **New cases:** "Write me a new case" has Claude invent a new mystery with the same
  settings.

## Talking to the game

- **Tap and talk:** tap Space (or the glowing button) once, then talk. It sends when you
  pause.
- **Hold to talk:** or hold Space while you talk, and let go to send.
- **Interrupt:** tap while anyone is speaking.
- **Always available:** say "repeat", "help" or "menu" in any game.
- **From the home screen:** tap Space and say a game's name, or press "Read the games
  aloud".
- **Sounds:** short cues play when listening starts and stops, a clock ticks while the
  AI thinks, and there are sounds for right, wrong and finding a clue.

Without voice (Safari, Firefox, the mobile apps), everything works by typing and
reading the text on screen.

## How it's built

A single HTML page that runs as a claude.ai artifact. It uses the platform's
`dictation` (speech to text), `tts` (Claude voices: one for the narrator and one per
character) and `sample` (Claude) capabilities.

Most answers are checked in the page itself, with no wait for the AI. That covers
names, "next", exact guesses, the facts and the box contents. Claude handles what needs
judgment, on the fastest model:
- **The Link:** loosely worded guesses.
- **Warmer:** how warm each guess is.
- **Who's Lying?:** the follow-up answers.
- **The Box:** the yes-or-no answers.
- **Quest and Lights Out:** the whole story, streamed line by line.

The puzzles and daily adventures are written into the page, not generated, so the daily
one really is the same for everyone.

Every prompt was tested against the fast model before release, including scripted
playthroughs with a careful player and with one trying to break the game.

Daily progress, streaks and any story or mystery in progress are saved in your browser.
