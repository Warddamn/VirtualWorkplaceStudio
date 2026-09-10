# The Cheap Build — what it costs, and how to run it

*Companion to `CHEAP-FLEET-BUDGET.md`. This file is the how-to. Written 2026-09-10.*

---

## 1. Where the costs actually come in

The thing that trips people up is assuming the cost is in the *setup*. It is not. Setup is
free and permanent. **The meter runs on thinking, and it runs every single turn.**

| What | Costs |
|---|---|
| Writing `.claude/agents/researcher.md` | **$0.** A text file. |
| Having it sit in your repo forever | **$0.** |
| Starting a session | **$0.** |
| An agent reading one file | fractions of a cent |
| That agent's *next* step | **the whole conversation again**, plus the new bit |

That last row is the whole thing. A language model has no memory between steps. To take
step 11, the entire transcript of steps 1 through 10 gets re-sent and re-read. A twenty-turn
task does not cost twenty units. It costs something closer to the sum of 1+2+3...+20,
because context accumulates and every turn pays for all of it again.

**This is why the two levers that matter are caching and horizon.**

- **Caching** means the provider keeps your re-sent prefix warm and charges about a tenth
  for re-reading it. It is the difference between viable and not. Every agent in this build
  sets `cacheTtl: 1h` for exactly this reason.
- **Horizon** means how many turns a task takes before it is done. A task that finishes in
  6 turns costs a fraction of one that takes 30, even at identical per-token prices. Every
  agent in this build sets `maxTurns` to cap it.

So your instinct — break work into the simplest possible tasks — is not just a cost trick.
It is the primary cost mechanism. Short tasks have short transcripts. Short transcripts are
cheap. And they are also *more accurate*, because model error compounds over a long run:
measured task success drops from 40–50% to below 10% purely from embedding the same task in
a longer history.

**What this means for structure versus instructions:** you were right that the structure is
a one-time cost. Where you were off is that instructions do not make the running free. They
make each run *shorter*, which is how they save money. A precise brief that finishes in 8
turns instead of 25 is a roughly 3× saving, permanently, on every future run.

---

## 2. "Can I just tell Astra which APIs to use?"

No, and the reason matters.

A chat assistant cannot hold your API keys, cannot route your traffic, and cannot bill to
your account. Telling a model "use DeepInfra" does nothing — it has no mechanism to act on
that. **Provider choice is configuration you set once, in a file or an environment variable,
not an instruction you give in conversation.**

The good news is that it genuinely is a one-time setup, and it is two lines. Section 4.

---

## 3. "Is a site that runs models cheaply an option?"

**Yes. That is exactly the right move, and it is the single biggest cost lever available
to you.**

Those sites are called inference providers. They host open-weight models and rent them per
token. The prices are not slightly lower than frontier models. They are 30–100× lower on
output, which is what dominates agent cost.

The one worth starting with is **OpenRouter**, because it solves the choice problem too:

- One account, one key, one balance, reaching **427 models from 80+ providers** as of
  2026-09-04, including 18 free ones.
- **No per-token markup.** Prices are identical to the vendors' own pages. It makes its
  money on a 5.5% fee when you buy credits with a card.
- Automatic routing and fallback, so a provider outage does not stop your fleet.

That means you can start on one key, try five models against your real work in an afternoon,
and keep the one that wins — without opening five accounts.

If you later want the cheapest possible rate on one specific model, go direct to the host.
**The same model costs 4.4× more on one provider than another**, so at this tier the host
matters more than the model.

| Model | Provider | In / Out per MTok |
|---|---|---|
| gpt-oss-20b | cheapest host | $0.03 / $0.13 |
| **gpt-oss-120b** | **DeepInfra** | **$0.05 / $0.17** |
| Qwen3 Coder 30B A3B | Novita | $0.07 / $0.27 |
| GLM-5.3-Flash | Z.ai | $0.15 / $0.50 |
| gpt-oss-120b | Cerebras | $0.35 / $0.75 |
| Claude Haiku 4.5 | Anthropic | $1.00 / $5.00 |

**Even cheaper than per-token: flat-rate coding plans.** Several open-model vendors sell
these, and several speak the Anthropic API natively, so Claude Code reaches them by changing
one URL. The GLM Coding Plan starts around $18/month. Cerebras Code is $50/month for up to
24M tokens a day. For steady daily use a flat plan beats metering, because you stop having
to think about it.

---

## 4. How to run this build

### Step 1 — use what is already here, on Claude models

Nothing to install. This repo now has `.claude/settings.json` and five workers in
`.claude/agents/`. The settings file already pins every worker to the cheapest Claude model:

```json
"env": { "CLAUDE_CODE_SUBAGENT_MODEL": "haiku" }
```

Confirm they load before you rely on them:

```bash
claude plugin validate .claude/agents      # -> Validation passed
```

Start a session and ask for work by role:

```
Use the code-reader agent to tell me how quota is enforced in the backend.
Use the engine-reviewer agent on backend/src/engines/minimaxReplicate.ts.
Have the test-writer agent cover the refine loop.
```

You talk to one orchestrator. It dispatches these. **This costs you nothing extra to try** —
it is included in whatever plan you already have, and it is fully supported.

### Step 2 — check what you actually spent

Run `/usage` inside Claude Code. It shows the session's token counts, the cache hit rate,
and a breakdown by subagent. **Do this before optimising anything.** You may find you are
nowhere near your ceiling and the whole question is moot.

The line to watch is cache hit rate. If it is low, something is invalidating your prefix and
you are paying full price on every turn.

### Step 3 — add a cheap provider, when you want bulk

Get an OpenRouter key, then point a router at it. `claude-code-router` (~36k stars, MIT) is
the community tool for this: it listens locally, accepts Claude Code's requests, and forwards
them wherever you configure.

```bash
export ANTHROPIC_BASE_URL="http://127.0.0.1:3456"
export ANTHROPIC_AUTH_TOKEN="<your router token>"
```

Then set the worker model to a cheap one in `.claude/settings.json`.

**Be clear-eyed about this step.** Anthropic's docs state plainly that they *"[don't] support
routing Claude Code to non-Claude models through any gateway."* Model discovery filters out
IDs that do not contain "claude" or "anthropic". It works because Claude Code passes model
strings through unvalidated behind a custom base URL. Against a non-Claude upstream,
adaptive thinking, `context_management`, `output_config` and `cache_control` all return 400.
You own the breakage.

### Step 4 — or use a harness built for open models

Cleaner than fighting the gateway. Run your orchestrator in Claude Code and give the cheap
bulk work to a harness designed for it:

| Harness | Why |
|---|---|
| **Goose** (Block, Linux Foundation) | Roadmap explicitly commits to tuning for small and open models, plus parallel subagents |
| **OpenHands** | Largest model-agnostic coding harness, routes everything through LiteLLM, real sub-agent delegation |
| **Mastra** | TypeScript-native, matches this repo's stack |

Do not build on **Roo Code** (archived 15 May 2026) or **Continue** (read-only). Avoid
**Codex CLI** for this: it dropped Chat Completions in February 2026, which locks out most
cheap endpoints.

> **Security, non-negotiable.** LiteLLM shipped credential-stealing malware on PyPI in March
> 2026. Pin the version and never install **1.82.7 or 1.82.8**.

---

## 5. The workers in this repo

Each is deliberately narrow. Narrow means short transcripts, which means cheap and accurate.

| Agent | Model | Tools | What it is for |
|---|---|---|---|
| `researcher` | haiku | web only | One research question. No filesystem. |
| `code-reader` | haiku | read only | "How does X work", with file:line evidence |
| `extractor` | haiku | read + write | Unstructured input to one structured table |
| `test-writer` | haiku | read + write + bash | Tests for one module. Cannot touch `src/`. |
| `engine-reviewer` | **sonnet** | read only | Reviews one adapter against the contract and the legal rules |

`engine-reviewer` is the one on a better model on purpose: judging whether an adapter
violates the YouTube rule is exactly the kind of judgment call cheap models fail. Everything
else is search, read, extract, and follow a spec, where the measured gap between cheap and
frontier models is small.

**Every one of them caps `maxTurns`.** That is horizon control, and it is the cost lever that
does not depend on which provider you use.

---

## 6. Rules that make cheap models work

Each of these is measured, not folklore.

1. **Do not fan out by default.** Subagent fan-out costs **2.6–5.9× the tokens of doing the
   same work sequentially, and was never faster**, because a subagent starts cold with no
   share of the parent's cache. Use one session at lower effort unless you have a genuine
   list of independent items.
2. **Reason free, constrain late.** Forcing a small model into a rigid output schema raises
   validity from 61.5% to 100% but **drops answer accuracy from 19.7% to 11.0%**. Let it
   think in plain text, then constrain only the final extraction.
3. **Rename tools to match what the model expects.** Up to **+17% with 80% fewer schema
   errors**, training-free. Small models hallucinate plausible tool names they learned in
   pretraining. Cheapest fix available.
4. **Set `max_tokens` generously.** Silent truncation ended 15–33% of attempts in one study,
   none of them solved. You pay for those tokens and get nothing back.
5. **Never go below 4B parameters for judgment.** Sub-4B models emit perfectly valid tool
   calls and still fail to respect negation. They look like they are working.
6. **Do not use majority voting with small models.** It actively hurts them on hard problems.
7. **Measure cost per completed task, not per token.** A cheap model that fails still bills,
   and two retries can triple a session.
8. **Cheap models break around five files.** They hold up well for surgical single-file edits
   and lint or codemod work. Past that, escalate.

---

## 7. What to do this week

1. Use the five agents as they are, on Haiku. Costs nothing extra, nothing to install.
2. Run `/usage` after two real days of work. Get a number instead of an estimate.
3. Only if that number bothers you, get an OpenRouter key and try `gpt-oss-120b` on the
   `code-reader` and `extractor` roles, which are pure read-and-report and the safest place
   to start.
4. Leave `engine-reviewer` on a frontier model regardless. It is guarding the two rules that
   can end the product.

The likely outcome is that step 2 shows you are far under budget and steps 3 and 4 are
optional. Get the measurement before you build the plumbing.
