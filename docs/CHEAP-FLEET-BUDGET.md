# The Cheap Fleet: Running Agents Well Under $2,000 a Month

*Companion to `AGENT-FLEET-STRATEGY.md`, written after that document's economics section
gave a misleading impression. Researched 2026-09-10. Prices in this space move monthly and
several below changed within the last 30 days, so re-check before committing.*

---

## 1. What my figures were, and what was wrong with them

The table that caused the confusion:

| Fleet composition | Per day | Per month |
|---|---|---|
| All Opus 5 | ~$3,200 | ~$64,000 |
| All Sonnet 5 | ~$1,280 | ~$26,000 |
| All Haiku 4.5 | ~$640 | ~$13,000 |

**That was 100 agents running 8 hours a day, 20 days a month. Sixteen thousand agent-hours.**
It was written to answer the literal question "what would hundreds of bots cost," as a
reality check on that number. Putting it at the top of the economics section made it look
like a plan. It was never the plan, and it is not remotely what you need.

An adversarial audit of that arithmetic found three specific problems:

1. **The multiplication is correct** ($4.00 / $1.60 / $0.80 per agent-hour × 16,000 hours).
   But the three hourly rates were exactly proportional to the models' price ratios, which
   silently assumes identical token consumption across all three. That is wrong.
2. **The Haiku figure is right by accident.** Reverse-engineering $0.80/hour from Haiku's
   $1/$5 per-million pricing implies about 640k input and 32k output tokens per agent-hour.
   That is 3–4× below the raw token flow of a real agent loop. The number only works if
   roughly 90% prompt caching is applied — which Claude Code does automatically, but I never
   said so.
3. **The Opus figure is understated by 1.6–3×.** Two documented reasons: the Opus 5 and
   Sonnet 5 generation uses a newer tokenizer that produces about 30% more tokens for the
   same text than Haiku 4.5, and extended thinking bills as output at $25 per million.
   Corrected, a cached Opus 5 agent-hour is about **$6.54**, or roughly **$13 with heavy
   thinking**. The true Opus-to-Haiku ratio is about 6.5×, not 5×.

And the real omission: **that document never covered open-weight models, cheap inference
providers, or vendor coding subscriptions at all.** It priced the frontier and stopped. That
is the gap this file fills.

---

## 2. What $2,000 a month actually buys

Holding back 20% as headroom leaves about $1,600 of working budget. Split it into an
orchestrator you talk to and a worker pool it dispatches.

| Worker model | Worker agent-hours for ~$1,400 | Concurrent workers, 8h × 22 days |
|---|---|---|
| Claude Haiku 4.5 | ~1,390 | ~8 |
| gpt-oss-120b (DeepInfra) | ~41,000 | ~230 |
| DeepSeek V4-Flash (off-peak) | ~20,000 | ~115 |

**Below the Haiku tier, dollars stop being the binding constraint.** Rate limits, sandbox
capacity, and your own review bandwidth bind long before the budget does. At cheap-model
prices a 20k-in / 1k-out worker turn costs about **$0.0012**, so $2,000 buys on the order of
1.7 million worker turns. The head bot, not the workers, will consume your budget.

That is the direct answer to your question. Your $2,000 ceiling was never in danger from the
architecture I recommended, and at open-model prices you have roughly an order of magnitude
more headroom than you need.

---

## 3. The biggest single lever: vendor coding subscriptions

This is the finding most worth acting on, and it is cheap.

Several open-model vendors sell flat-rate coding plans, **and several speak the Anthropic API
natively — so Claude Code talks to them by swapping one base URL.**

| Plan | Price | What you get |
|---|---|---|
| **GLM Coding Plan (Z.ai)** | ~$18/mo entry, ~$12.60 on annual; Pro ~$72–80 | Points-based quota, off-peak at 50%. *"Any tool that speaks Claude's API — Claude Code, Cline, OpenClaw, Goose, Crush — can talk to GLM out of the box just by swapping the base URL."* |
| **Cerebras Code** | $50/mo Pro, $200/mo Max | Up to 24M tokens/day on Pro, 120M/day on Max (1.5M TPM) |
| **MiniMax** | metered | Anthropic-compatible endpoint at `api.minimax.io/anthropic/v1`; one bug report notes non-standard behavior in at least one client |
| **Claude Max 20x** | $200/mo | Beats Anthropic's own $150–250/developer/month API benchmark, and carries a **1-hour cache TTL instead of the API default of 5 minutes** |

Two caveats. Sources disagree on GLM Pro pricing ($72 versus $80) — check z.ai before
committing. And multiple Claude subscription seats require separate identities, so you get
one seat, not a pool.

**The shape this suggests: one subscription seat for the phone-facing orchestrator, plus
metered cheap-model spend for the fleet.** A serious setup lands around $250–350 a month,
not $2,000.

---

## 4. The cheap token tier, by price

Output dominates agent cost, so rank by output price. The spread from top to bottom is
roughly **80×**.

| Model | Provider | In / Out per MTok | Note |
|---|---|---|---|
| Llama 3.1 8B Instant | Groq | $0.05 / $0.08 | Too small to plan; fine for filtering |
| gpt-oss-20b | cheapest host | $0.03 / $0.13 | Good simplest-of-tasks worker |
| Qwen3.7 Flash | Alibaba | $0.03 / $0.13 | Cheapest listed paid API as of 2026-09-03 |
| **gpt-oss-120b** | **DeepInfra** | **$0.05 / $0.17** | **Best overall worker pick.** SOC 2 / ISO 27001, zero inference retention |
| gpt-oss-120b | Novita | $0.05 / $0.25 | Check which quantization tier you are buying |
| Qwen3 Coder 30B A3B | Novita | $0.07 / $0.27 | Strong cheap coder for TypeScript edits |
| **GLM-5.3-Flash** | **Z.ai** | **$0.15 / $0.50** | 320B total / 18B active, 1M context, MIT weights |
| gpt-oss-120b | Groq / Together | $0.15 / $0.60 | Bought for speed, 3.5× DeepInfra's output price |
| DeepSeek V4-Flash | DeepSeek | $0.22 / $0.66 off-peak | Extreme cache-hit discount; **$0.44 / $1.32 peak** |
| gpt-oss-120b | Cerebras | $0.35 / $0.75 | 4.4× DeepInfra for the identical model |
| Claude Haiku 4.5 | Anthropic | $1.00 / $5.00 | Cache read $0.10 |
| Claude Sonnet 5 | Anthropic | $2.00 / $10.00 | Realistic orchestrator |
| Claude Opus 5 | Anthropic | $5.00 / $25.00 | Reference point only |

**The same model costs 4.4× more on Cerebras than DeepInfra.** At this tier, provider choice
matters more than model choice.

Three things that changed recently and would have burned you:

- **DeepSeek is no longer the automatic winner.** On 2026-08-16 it moved V4-Flash from a flat
  $0.14/$0.28 to peak/off-peak billing, a rise reported at up to 1,100% across the lineup.
- **Gemini 2.5 Flash-Lite ($0.10/$0.40) retires no earlier than 2026-10-16**, and its
  replacements are 3–6× more expensive on output. Do not architect around it.
- **Meta has not released Llama 5.** The repo has not moved since February 2026. Claims of an
  April 2026 release are fabrications. Treat Llama as a dead line for agent work.

Free tiers worth wiring in as overflow: Cerebras 1M tokens/day (but 8,192-token context cap),
Groq 14,400 requests/day per model, Google AI Studio roughly 1,000–1,500 requests/day.

---

## 5. Your instinct is right, and the reason is better than you think

You said you want to break work into the simplest possible tasks. That is correct, and the
mechanism is **horizon, not difficulty.**

The execution literature finds that larger models complete far more turns *even when small
models have 100% single-turn accuracy*, because per-step accuracy decays as a run gets longer:
models self-condition on their own earlier errors. So decomposition does not make a cheap
model smarter. **It caps the number of steps over which its error rate can compound.**

Two measurements make this concrete:

- Task success can drop from 40–50% to **below 10%** purely from embedding the same task in a
  longer history, with roughly a 47-point accuracy decay from the first to the last progress
  decile.
- **Context overflow, not reasoning failure, causes 35.6% of failures** for top models on
  SWE-bench Pro.

And there is a published capability ladder telling you exactly how small a task must be.
AgentFloor tested 16 open-weight models from 0.27B to 32B across 16,542 runs and found small
open models **already sufficient** through: instruction following, a single tool call, a
two-tool chain, and branching on an intermediate result. The gap only opens at long-horizon
planning under persistent constraints.

**So: any leaf task that is "follow this instruction, call one or two tools, branch once" is
safely a cheap-model task.** Anything requiring a plan that survives many steps is not.

---

## 6. The finding that should change your plan

This one contradicts part of what I recommended, so it gets its own section.

**Fan-out is not free. It is measured at 2.6×–5.9× the tokens of doing the same work
sequentially, and it was never faster.**

The mechanism is caching. A subagent starts a fresh context with no share of the parent's
cached prefix, so it pays full price for its system prompt and tools on every turn. One
measured run: the direct sequential version consumed about 121,000 metered input tokens; the
two-subagent fan-out consumed 513,000. Pinning the subagents to Haiku recovered only 37%.

Anthropic's own measured guidance points the same way: an orchestrator only pays off when
there is **genuine bulk to hand off** — many independent pieces, ideally exceeding one context
window. On a single dependent chain that fits in one context, **the coordinator's model alone
at lower effort won in every case they measured.**

Related, and useful for you specifically: for a solo builder with tests, **single-model effort
escalation beats a multi-model cascade** — the same pass rate for half the cost, with no
routing infrastructure to build. And cascade routing's famous savings do not transfer: about
85% on chat but only ~35% on math, and an escalating advisor consulted on nearly every task
becomes a 2.6× cost increase with zero accuracy gain.

**Practical rule: default to one session at lower effort. Fan out only when you have a real
list — many files, many findings, many sources — not because parallel feels faster.**

---

## 7. What can actually drive cheap models

The blocker that decides your architecture:

> Anthropic doesn't endorse, maintain, or audit third-party gateway products, and **doesn't
> support routing Claude Code to non-Claude models through any gateway.**

Gateway model discovery filters out any model ID not containing "claude" or "anthropic". The
gateway protocol accepts only three formats: Anthropic Messages, Bedrock InvokeModel, and
Vertex rawPredict. Against a non-Claude upstream, adaptive thinking, `context_management`,
`output_config` and `cache_control` all return 400.

So the honest split:

**Fully supported — cheap Claude workers.** Pin subagents to Haiku fleet-wide, or per agent
definition. This is first-class and needs one line:

```bash
export CLAUDE_CODE_SUBAGENT_MODEL=haiku
export CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1   # overrides every subagent definition
```

Or per role, in `.claude/agents/*.md` frontmatter: `model: haiku`.

**Works but unsupported — cheap open workers.** Behind a custom base URL, Claude Code passes
any model string through without validating it. That is the opening the community exploits:
`claude-code-router` (~36k stars, MIT, actively maintained) intercepts Anthropic-format
requests and reroutes to OpenAI, Gemini, DeepSeek, OpenRouter, Mistral or Moonshot with
per-request routing rules. It works. You own the breakage.

**The cleaner route for open workers is a harness built for them:**

| Harness | Why |
|---|---|
| **Goose** (Block, Linux Foundation AAIF, 54.1k stars) | The standout. Roadmap explicitly commits to tuning prompts and tool-calling for small and open models, *and* to parallel subagents |
| **OpenHands** (87.2k stars) | Largest model-agnostic coding harness; routes everything through LiteLLM; genuine sub-agent delegation |
| **Mastra** | TypeScript-native, matches your Node and Expo stack directly |
| **mini-swe-agent** | ~100 lines of Python, >74% on SWE-bench Verified, drives any model via LiteLLM |
| **OpenAI Agents SDK** | Three documented first-class paths to non-OpenAI models |

**Dead — do not build on these:** Roo Code was archived 15 May 2026; Continue is read-only
after a final 2.0.0. **Avoid Codex CLI for this:** it removed Chat Completions support in
early February 2026, and `wire_api="responses"` is now the only accepted value, which locks
out most cheap and open endpoints.

**LiteLLM is the budget-enforcement layer.** Per-virtual-key budgets plus budget fallbacks
mean spend crossing a limit reroutes rather than simply failing. Claude Code also tags every
request with per-subagent identifiers, so a gateway can attribute spend per worker.

> **Security, non-negotiable:** LiteLLM shipped **credential-stealing malware on PyPI in March
> 2026**. Pin the version. Never install **1.82.7 or 1.82.8**. Anthropic's own gateway docs
> flag this.

---

## 8. Do not buy hardware

The arithmetic is decisive at this budget.

**$2,000/month of cheap open-weight API buys 10.3 billion tokens** (gpt-oss-120b on Groq) **to
71.4 billion** (gpt-oss-20b on OpenRouter) at an agentic 90/10 input-output blend. A $6,000
RTX 5090 box pinned at 100% duty cycle for 30 straight days produces **11.8 billion**. At a
realistic 10% solo duty cycle it pays back in 29 months against Groq pricing, and never
against the cheapest tier.

The hardware market makes it worse: the DRAM crisis has pushed RTX 5090 street prices to
around **$4,700 against a $1,999 MSRP**, Mac Studio prices rose 25–37.5% this generation, and
relief is not expected until late 2027 or 2028.

Two more reasons specific to agents:

- **Quantization breaks exactly where agents break.** 4-bit builds (NVFP4, AWQ INT4) were
  observed failing to close tool-call JSON envelopes while FP8 and INT8 completed the same
  calls. Structured output degrades below Q4_K_M.
- **Ollama and LM Studio are single-user tools.** Ollama defaults to `OLLAMA_NUM_PARALLEL=1`
  and FIFO-queues the rest. A fleet needs vLLM or SGLang.

Rented GPU is the real middle path, but only if you saturate it: a rented 5090 is $0.040 per
million tokens at 100% utilization and $0.395 at 10%.

**Use local hardware only if you already own it.** Spend the budget on tokens.

---

## 9. The build

**Orchestrator — the one you talk to.** Claude Max 20x at $200/month, or Sonnet 5 metered.
Keep it on a subscription for the 1-hour cache TTL; the API default of 5 minutes means a
bursty fleet that idles between tasks pays roughly 3× more.

**Workers — cheap, narrow, short.** Start with `CLAUDE_CODE_SUBAGENT_MODEL=haiku` because it
is supported and costs nothing to try. Add a GLM Coding Plan (~$18/month) as a second tier
when you want genuinely cheap bulk, pointed at Goose or via base-URL swap.

**Three price points:**

| Tier | Monthly | What it is |
|---|---|---|
| Minimum viable | **~$40** | Claude Pro $20 + GLM Coding Plan entry ~$18 |
| **Recommended** | **~$270** | Claude Max 20x $200 + GLM Pro ~$72, plus overflow free tiers |
| Comfortable | **~$500** | Above, plus ~$230 of metered DeepInfra or Cerebras Code Pro for burst fan-out |

All three sit far under $2,000. Spend the difference on your engine costs, not on tokens.

---

## 10. Cheap-model engineering rules

These are what make the cheap tier actually work. Each is measured.

1. **Rename your tools to match the model's pretraining priors.** Up to **+17% with 80% fewer
   schema-misalignment errors**, training-free, just a name mapping. Small models hallucinate
   plausible tool names absent from your schema because they learned different conventions.
   This is the highest-leverage fix available.
2. **Reason free, constrain late.** Hard schema-constrained decoding raises validity from
   61.5% to 100% but *drops answer accuracy from 19.7% to 11.0%* on small models, and pushes
   wrong-but-valid outputs from 49.5% to 88.9%. Let the model reason in free text, then
   constrain only the final extraction step.
3. **Use structured decoding at the right layer.** Schema-valid JSON is a decoding problem,
   not a model problem: XGrammar and Outlines on vLLM or SGLang make malformed JSON
   structurally impossible.
4. **Have the planner write the whole task tree up front and replan lazily.** Matches
   step-by-step planning on accuracy at 2–3× fewer tokens.
5. **Set `max_tokens` generously.** Silent truncation ended 15–33% of attempts in one study,
   none of them solved. You pay for those tokens and get nothing.
6. **Never go below 4B for judgment.** A reproducible 21-model benchmark found most sub-4B
   models emit valid tool calls but fail to resist keyword triggers or respect negation. They
   look like they are working.
7. **Do not use majority voting with small models.** "More Agents Is All You Need" does not
   transfer — voting actively hurts them on hard problems.
8. **Measure cost per completed task, not per token.** A cheap model that fails still bills,
   and two retries can triple a session.
9. **Watch the coding boundary.** Cheap and local models hold up for surgical single-file
   edits and lint or codemod work, and break around five files or any architectural
   reasoning.

---

## 11. What to re-check before spending

- **GLM Coding Plan pricing.** Sources disagree ($72 versus $80 for Pro). Check z.ai.
- **DeepSeek peak and off-peak hours.** Peak is 01:00–04:00 and 06:00–10:00 UTC, and the
  pricing model changed in August 2026.
- **Gemini 2.5 Flash-Lite retirement**, no earlier than 2026-10-16.
- **Which quantization a provider actually serves.** Hosts differ silently, and 4-bit breaks
  tool calling.
- **LiteLLM version pinning.** Never 1.82.7 or 1.82.8.
- **OpenRouter free endpoints**, where prompts can be the payment.
- **DeepInfra's 200-concurrent-request account cap**, if you plan real fan-out.

---

## Sources

Pricing and providers: DeepInfra, Groq, Together AI, Novita, Cerebras, Baseten, Lambda,
SambaNova, OpenRouter, Z.ai, DeepSeek, Alibaba Model Studio, Mistral, Google AI Studio and
Anthropic public pricing pages, 2026-09-10.

Research: AgentFloor (arXiv 2605.00334) · *The Constraint Tax* (arXiv 2605.26128) · *Don't
Adapt Small Language Models for Tools; Adapt Tool Schemas to the Models* (arXiv 2510.07248,
ACL 2026) · execution-horizon decay (arXiv 2509.09677) · Cursor, *Agent swarms and the new
model economics* · Systima, *The subagent tax* · Anthropic Claude Code docs (costs, model
config, sub-agents, LLM gateway) · Epoch AI open-weights lag measurements.
