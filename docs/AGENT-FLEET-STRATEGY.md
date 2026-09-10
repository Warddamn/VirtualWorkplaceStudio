# Bot Armies: A Strategy for Running Agent Fleets as a Solo Builder

*Research completed 2026-09-10 across seven parallel research tracks with adversarial
verification on load-bearing claims. Everything time-sensitive carries a source. This
space moves faster than anything else in software — Astra's published usage limits were
cut within a week of launch — so re-check numbers before you spend money on them.*

---

## 1. The short answer

**Your instinct is right, your scale number is wrong, and Astra will not handle your
permissions.**

The shape you described — one bot you talk to all day that decomposes your requests and
dispatches a structured team of workers — is the dominant production pattern in 2026. It
is what Anthropic's Research feature is. It is what built this repository. You are not
inventing anything exotic, and the utility you're sensing is real.

Three corrections, in order of how much they change your plan.

### Correction 1: read wide, write narrow

This is the single most useful reframe in this document.

"Hundreds of bots at a time" is achievable — but only for **reading**. The moment agents
start **writing**, the number that works collapses to single digits. The Ralph loop
playbook, the most widely copied DIY fleet pattern, states the asymmetry outright:

> Spec/code reading: **Up to 500 parallel Sonnet subagents** for searches and analysis.
> Build/test validation: **Strictly 1 Sonnet subagent** (backpressure control).
> Complex reasoning: Opus subagents when debugging.
> — [Ralph playbook](https://github.com/ClaytonFarr/ralph-playbook)

Cognition reached the same conclusion and published a follow-up that **narrows rather than
retracts** its June 2025 essay *Don't Build Multi-Agents*. Walden Yan is explicit about
which half still stands:

> Our original observations still hold today for parallel-writer swarms: most of the sexy
> ideas in that space still don't see meaningful adoption. But we've found a narrower class
> of patterns that do.

That narrower class is defined by **writes staying single-threaded** while the extra agents
contribute *intelligence* rather than *actions*. (The phrase "single-writer principle" is a
useful shorthand for it, but it is the industry's coinage, not Cognition's own wording.)
Their canonical failure is still the best illustration: two sub-agents building one game
produced a Super Mario background and a bird that didn't look like a game asset, because
each got the explicit objective but not the implicit context.

Google Research quantified it across 180 agent configurations, three model families, and
five architectures, holding prompts and token budgets constant:

| Work shape | Effect of adding agents |
|---|---|
| Parallelizable (research, analysis) | **+80.9%** over a single agent |
| Sequential (dependent reasoning) | **−39% to −70%** — every architecture degraded it |
| Uncoordinated independent agents | **17.2×** error amplification |
| Centralized coordination | **4.4×** error amplification |

Optimal cluster size: **3–4 agents**. Past a single-agent baseline of roughly 45%
accuracy, more agents produce diminishing returns or outright regressions.

So the fleet you want is real, and it is shaped like a funnel: many readers, few writers,
one decider.

### Correction 2: the ceilings are tens, not hundreds

Every platform caps concurrency well below 100, and the caps are deliberate.

| Platform | Concurrent workers | Nesting |
|---|---|---|
| [Claude Code subagents](https://code.claude.com/docs/en/sub-agents) | **20** per session (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`) | 3 layers |
| [Claude Code dynamic workflows](https://code.claude.com/docs/en/workflows) | **16** live, 1,000 per run, 4,096 items per fan-out | n/a |
| [Claude Code agent teams](https://code.claude.com/docs/en/agent-teams) | no cap; **3–5 recommended** | none — teammates can't spawn teammates |
| [Claude Managed Agents](https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration) | **25** threads, 20-agent roster | exactly **one** level |
| [OpenAI Codex](https://github.com/openai/codex/blob/main/codex-rs/core/src/config/mod.rs) | **4–6** default; staff suggest 8–12; OpenAI tested Astra to 64 | depth 1 |
| [OpenAI Responses `multi_agent`](https://developers.openai.com/api/docs/guides/responses-multi-agent) | **3** default (`max_concurrent_subagents`) | no fixed cap |

Note what Managed Agents forbids: **one level of delegation**, enforced with a validation
error. You cannot build a manager-of-managers hierarchy there. The org chart you're
imagining is flatter than you think, on purpose.

And the tightest ceiling of all is not technical. Practitioner reports put the **human
supervision ceiling at two to three simultaneous workstreams** before attention-switching
costs exceed the gains. Teams running parallel coding agents report 4–8 concurrent
worktrees per developer as the reliable band, and that **review, not generation, is the
bottleneck**. Worktrees make it cheap to start ten agents; reading ten diffs is still
expensive. The industry-wide symptom: developers use AI for about 60% of their work but
report being able to fully delegate only 0–20% of tasks.

### Correction 3: Astra is a strong model, not a bot-army platform, and the AGI claim was spoken, not written

GPT-6 Astra is real — OpenAI unveiled it 2026-09-03. The AGI line came from co-founder and
president Greg Brockman, as the closing remark of OpenAI's own launch press briefing, and
OpenAI has not disavowed it. So this is not merely one employee freelancing; it is a company
officer speaking in a company venue, which is why most outlets attributed it to the
institution. But he hedged it in the same breath:

> I think it's not unreasonable to feel that we are now in the AGI era... I do leave it up
> to the reader to decide for themselves if this qualifies for them.

And OpenAI's **written** launch material never makes the claim — it calls Astra *"our most
capable model."* Sam Altman told TIME OpenAI is *"not quite yet"* there. On the benchmark
that generated the headline, ARC Prize is unambiguous:

> When we launched ARC-AGI-3, we made it clear that saturating the benchmark would not
> represent "proof of achieving AGI." Therefore, while we believe Astra represents
> meaningful progress towards generalization, we are not claiming that it is AGI.

The **99.9%** figure and the **62.7%** figure are the same model under two different harness
conditions, not one result and its debunking — the higher number comes from a provider-adapter
harness that preserves reasoning state between requests, the lower from ARC's standard
harness. Quote either, but say which. The Microsoft contract's AGI clause was removed in
April 2026, so the declaration carries no legal weight. Nvidia's Jensen Huang separately
declared "AGI has arrived" three days later — a hardware supplier's claim, not independent
verification.

*(An earlier draft cited Artificial Analysis aggregate index scores here. Adversarial
verification found conflicting figures for Astra across that source's own pages, so the
numbers are withdrawn rather than repeated. The directional read — Astra roughly level with
GPT-5.6 Sol and not clearly ahead of the Claude frontier — appears in secondary coverage but
is not verified.)*

Astra is genuinely excellent at computer use and long-horizon autonomous work, and
developers are already running it as an orchestrator over cheaper GPT-5.6 workers. But
press reporting puts it at roughly **10 parallel sub-agent slots**, not hundreds, and the
parallelism is runtime infrastructure in the Responses API rather than an unbounded model
capability.

Most importantly for your question: **OpenAI's own agent-security guidance tells developers
not to hand agents broad standing credentials and states plainly that the agent cannot
approve OS security prompts.** Astra will not provision permissions for you. Section 3.

---

## 2. What the evidence actually shows about scale

Three real fleets, at three scales, with real numbers.

**16 agents, ~$20,000 — the case that worked.** Anthropic's Nicholas Carlini built a
100,000-line Rust C compiler with 16 parallel Claude agents across nearly 2,000 Claude Code
sessions. It compiles Linux 6.9 on x86, ARM, and RISC-V, plus QEMU, FFmpeg, SQLite,
Postgres, and Redis, at a 99% pass rate on most compiler test suites. Coordination was
**git plus filesystem lock files** — agents claim work by writing to a `current_tasks/`
directory — not chat. The headline lesson is one sentence:

> The task verifier must be nearly perfect, or agents will solve the wrong problem.

A C compiler is the ideal fleet target precisely because a test suite is a perfect
verifier. Your app is not that.

**Hundreds of agents — the case that mostly burned.** Cursor ran hundreds of autonomous
agents to build a browser engine in Rust: over 1 million lines in about a week, and
**more than 70,000 merge conflicts**, with "vast amounts of compute and time wasted on
resolving code conflicts." Their redesigned swarm, reimplementing SQLite from the 835-page
docs alone, cut that to **under 1,000 conflicts and 9,908 lines** for the same task —
better output from a *better-coordinated* fleet, not a bigger one.

**3–5 agents — the case Anthropic ships.** Claude's Research feature is an
orchestrator-worker where the lead spawns **3–5 specialized subagents** in parallel, plus a
separate citation pass. Read that as the typical case rather than a ceiling: the same
write-up scales the count to the question, from *"1 agent with 3-10 tool calls"* for simple
fact-finding to *"more than 10 subagents"* for complex research. It beat single-agent Opus
by **90.2%** on research tasks at roughly **15× the tokens of chat**. Anthropic's own stated
boundary condition:

> Multi-agent systems excel at problems that can be divided into parallel strands of
> research, but are less effective for tightly interdependent tasks such as coding.

And the sobering academic backstop: Cemri et al. (NeurIPS 2025) measured multi-agent LLM
failure rates of **41–86.7%** across seven popular frameworks, with **79% of failures
traceable to specification ambiguity and coordination breakdown** rather than model
capability. The bugs are in your task descriptions, not in the models.

### What works, and what disappoints

**Works — read-heavy and verifiable:** research fan-out, parallel code review split by
dimension, competing-hypothesis debugging (five investigators actively trying to disprove
each other, which defeats the anchoring that makes sequential investigation converge too
early), large mechanical migrations, per-record extraction.

**Disappoints:** tightly coupled feature work, same-file edits, anything needing shared
design taste, and any task where your own review bandwidth is the real constraint.

---

## 3. Permissions — the part no bot does for you

You asked: *"what permissions would I need? Or would Astra take care of that for me?"*

**Neither Astra nor Claude can.** Across every vendor there is one architectural invariant:
**a child agent never holds more authority than its parent, and one agent's approval is
never your consent.** Claude Code documents it plainly:

> Teammates start with the lead's permission settings... A teammate can't approve a
> permission prompt or supply consent on your behalf, and a teammate that was denied an
> action can't relay it to another teammate to bypass the check.

Subagents inherit a *narrowed* tool pool — the mechanism only subtracts. A subagent runs in
`bypassPermissions` only when the parent already does — **though that specific guarantee
requires Claude Code v2.1.267 or later**; on older builds a subagent declaring
`permissionMode: bypassPermissions` under a weaker parent did receive it. Check your version
before relying on it. Cloud child sessions cannot exceed
the calling session's mode, and pre-approved tools the parent lacks are silently dropped.
In auto mode a classifier treats an approval claim relayed from another agent as untrusted
input. **Caveat worth knowing:** this is a designed invariant with at least one open issue
reporting escalation leaks in practice. Treat it as a strong default, not a proof.

### What only you can provision

Human identity and money are the hard boundary. Do these once, up front.

1. **Billing and spend caps.** A subscription and/or API billing, with a monthly spend
   limit set the same day. Note that Remote Control requires a claude.ai subscription login
   and **explicitly does not accept API keys** — that account linkage is a human step.
2. **Source control.** A GitHub App installation scoped to specific repositories. This
   comes in two separately granted layers: clone access does not grant app/webhook access.
   For hand-rolled worker credentials, use fine-grained PATs scoped to selected repos with
   bounded expiry, not classic PATs.
3. **Third-party API keys.** Replicate, fal.ai, and an LLM key for this project. Vault
   them; see below.
4. **OAuth connectors.** Google Drive, Slack, Linear — each a one-time browser consent.
5. **Publishing identities.** Apple requires legal identity verification (potentially
   government ID) and a D-U-N-S number for organizations; Google Play requires paid
   registration and an organization D-U-N-S. Hard human gates by design.
6. **The permission posture itself.** Which tools run silently, which pause and ask.

### The controls that actually hold

Claude Code has six permission modes as of 2026: `default` (Manual), `acceptEdits`, `plan`,
`auto`, `dontAsk`, and `bypassPermissions`. Four things matter for a fleet:

- **`dontAsk` is the documented mode for unattended workers** — it *denies* anything not
  pre-approved. `bypassPermissions` *approves* anything unlisted. These are opposites, and
  the intuitive-sounding one is the dangerous one.
- **Deny rules and `PreToolUse` hooks are the only controls that survive
  `bypassPermissions`.** Allow-lists do not constrain it at all. `PreToolUse` hooks run
  before every other permission step, fire inside subagents with the subagent identified,
  and can deny even under bypass. **This is your single uniform enforcement point across an
  entire fleet.** If you build one piece of safety infrastructure, build this.
- **Some actions are never auto-approved in any mode.** That is the floor a fleet cannot
  dig under.
- **`--max-budget-usd` is the hard local cost stop.** It also kills subagents when it trips.

### Credential brokering — the pattern worth copying

Managed Agents vaults solve the secret problem structurally rather than by policy:

> Vaults store credentials; those credentials **never enter the sandbox**. This is a
> deliberate security boundary — code running in the sandbox (including anything the agent
> writes) cannot read or exfiltrate a vaulted credential, even under prompt injection.

The secret is substituted into the outbound request *after* it leaves the sandbox, only for
allow-listed hosts. A fully compromised worker cannot print your Replicate key because it
never had it. Two rules: scope `allowed_hosts` per credential, and scope each key minimally
at the provider — the agent can do anything the key allows.

Related, and easy to get wrong: **credential-masking config is only honored from settings
files you control** — a repo checked into the project cannot authorize the proxy to inject
real secrets. And **environment variables on a shared cloud environment are readable by
anyone using it**; the docs say so directly. They are the wrong place for worker secrets.

The Bash sandbox **pre-allows zero network domains**. Worker egress is an explicit
allow-list you write, enforced by a proxy outside the sandbox rather than by matching
command text. One documented self-escalation path to avoid: disabling filesystem isolation
while auto-allowing sandboxed commands lets an agent widen its own permissions on the next
run.

### The always-on trap

The surface you most want — **Routines**, the cloud-scheduled head bot that works while you
sleep — is precisely the one with the weakest per-action gating:

> Routines run autonomously as full Claude Code cloud sessions: there is no permission-mode
> picker and no approval prompts.

Connector access is all-or-nothing per routine. So give routines the *narrowest possible*
connector set and the *most reversible possible* tasks. One genuine safeguard is built in:
an inbound API-trigger payload is explicitly framed as untrusted data and cannot act as
instructions — a deliberate prompt-injection boundary.

### Risks that scale with fleet size

- **Agent goal hijack** is the number-one risk in OWASP's Top 10 for Agentic Applications
  (December 2025). Every worker with web access multiplies this surface.
- **MCP supply chain compromise is not hypothetical.** A malicious MCP server shipped clean
  for fifteen versions before adding exfiltration, and a 9.6-CVSS RCE was disclosed in core
  MCP infrastructure. The MCP authorization spec now makes token audience-binding mandatory
  and forbids passthrough — the standard confused-deputy defense.
- **Skills are an untrusted-code surface**, and Anthropic says so explicitly. Think twice
  before installing third-party deck or spreadsheet skills across a fleet.
- **File collisions** on hotspot files — routing tables, config, component registries.
  Use `isolation: worktree`.
- **Silent quality collapse.** More workers producing more output nobody verifies. The fix
  is an adversarial verification pass, not more workers.

---

## 4. Economics

Anthropic's published baseline for Claude Code: **~$13 per developer per active day**,
**$150–250 per month**, 90% of users under $30 per active day — *before any fan-out*.

Bottom-up, one continuously working agent at 2026-09-10 list prices:

| Model | List price (in/out per MTok) | ≈ Cost per agent-hour |
|---|---|---|
| Claude Haiku 4.5 | $1 / $5 | **$0.80** |
| Claude Sonnet 5 | $2 / $10 | **$1.60** |
| Claude Opus 5 | $5 / $25 | **$4.00** |
| Claude Fable 5.1 | $10 / $50 | **$6.64** |
| GPT-6 Astra | $10 / $50 | ≈ $6.64 |

A **100-agent fleet for one 8-hour day**:

| Fleet composition | Per day | Per month (20 days) |
|---|---|---|
| All Opus 5 | ~$3,200 | ~$64,000 |
| All Sonnet 5 | ~$1,280 | ~$26,000 |
| All Haiku 4.5 | ~$640 | ~$13,000 |
| **Mixed: 1 Opus lead + 20 Sonnet + 79 Haiku** | **~$790** | **~$16,000** |

Rate limits are not the wall — Build tier sustains roughly 330 hard-working Opus 5 agents
before output-tokens-per-minute saturates. **The tier spend cap is the wall.** The default
Start tier caps at $500/month, which buys about **1.3 hours** of a 100-agent Opus fleet.

For a solo builder, the realistic middle ground is well documented: about $30–40/day at
three parallel agents, $50–130/day at five to ten. Agent teams run about **7× a standard
session**; Anthropic's research system about **15× chat**.

### The two levers that matter

**Model assignment beats agent count, decisively.** Cursor measured a **7.9× cost spread
($1,339 to $10,565) at externally identical, verified quality on the same task**, produced
*entirely* by which model sat in which seat. Frontier models decompose goals into task
trees; cheap models execute. Their worker fleet cost dropped from $9,373 to $411 on the
SQLite test. Anthropic's own multiagent documentation uses Haiku 4.5 for worker roster
agents throughout, with the rationale stated plainly: delegated work is mostly searching,
reading, and extracting — many input tokens, little hard reasoning.

Haiku's limits are worth knowing before you commit: 200K context (versus 1M for Opus and
Sonnet 5), 64K output cap, no effort parameter. Quality holds for scoped, read-heavy,
short-horizon tasks and degrades on long-horizon multi-file work. That is exactly the
worker profile, so it fits.

**Prompt caching is the difference between viable and not.** Cache reads cost 10% of base
input **and do not count toward input-tokens-per-minute rate limits**, so cache hygiene
raises both the affordable and the *schedulable* agent count. One gotcha: an in-process
teammate's requests fall outside the main conversation's cache TTL bucket and default to
five minutes even on a subscription. Set `subagentPromptCacheTtl` to `1h` or you re-pay for
context on every teammate.

### Where the money stops buying throughput

Coordination overhead grows faster than output. A 3-agent pipeline consumed ~29,000 tokens
against ~10,000 for a single agent (about 3×), and scaling to 32 agents produced only a
**6.21× throughput gain for an 8× agent increase**. Combined with Google's finding that
returns saturate at 3–4 agents, the conclusion is consistent from three independent
directions: **spend on better model assignment and better verifiers, not on more agents.**

*(One widely circulated anecdote — 49 parallel subagents for 2.5 hours estimated at
$8,000–15,000 — does not reconcile with 2026 list prices. Treat it as an upper-bound story,
not a measurement.)*

---

## 5. Recommended architecture

### Pick one stack as the spine

Running Astra as head bot over Claude workers is technically imaginable — they would
communicate through files, git, and shell — but **there is no first-party mechanism for
Astra to orchestrate Claude Code workers**, so you would be hand-building and maintaining
the bridge, two permission models, two billing surfaces, and two rate-limit regimes. For
one person that friction costs more than the second opinion is worth.

**Build the spine on the Anthropic stack; keep Astra as a consultant you invoke
deliberately** — a second opinion on hard architecture calls, or computer-use tasks in
ChatGPT Work. The reasons are specific to what you asked for:

- Phone-all-day is met natively; on the OpenAI side, persistent scheduled agents
  (Workspace Agents) are **Business/Enterprise only**, and on Plus, Astra isn't even in the
  main chat picker — only inside Work and Codex, sharing one 5-hour allowance.
- Concurrency ceilings are 3–5× higher.
- Vaulted credentials solve the permission question structurally.
- Your project is already built this way.

### The four layers

```
Layer 0   YOU — accounts, API keys, OAuth grants, spend caps, irreversible-action approval
   |
Layer 1   CHIEF OF STAFF — one persistent session, reachable from your phone all day
   |      Holds the agenda. Triages. Dispatches. Never edits a file.
   |
Layer 2   PROJECT LEADS — one long-running session per active project
   |      cover-app · decks · data · research      Each owns its own worktree.
   |      THE SINGLE WRITER. One per project, never two.
   |
Layer 3   WORKERS — short-lived, read-mostly, cheap model, spawned per task
          researchers · reviewers · extractors · test-writers
          Fan out to 20+ freely. They read and report; they do not write.
```

The discipline that makes this work is Cognition's rule applied literally, that writes stay
single-threaded:
**Layer 1 never edits files, and each project has exactly one writer at Layer 2.**
Everything at Layer 3 is a reader. The moment your chief of staff starts writing code, its
context fills with implementation detail and it stops being able to hold your day.

### The concrete build

**Chief of staff** — Remote Control server mode:

```bash
claude remote-control --spawn worktree --capacity 8
```

Reachable from the Claude mobile app or `claude.ai/code`, able to spawn on-demand worker
sessions from your phone, each in its own git worktree so they cannot collide. Scan the QR
code once. Note that `--capacity` defaults to 32; start at 8, because your supervision
ceiling is 2–3.

**Phone chat** — a channel, for asking a question from a coffee shop and getting the answer
in the same thread:

```bash
claude --channels plugin:telegram@claude-plugins-official
```

Lock it down immediately with `/telegram:access policy allowlist`. Two caveats: if Claude
hits a permission prompt while you're away the session **pauses until you respond** unless
the channel relays permissions; and anyone who can reply through the channel can approve
tool use when relay is on. There are five documented away-from-desk entry points with
different tradeoffs — Dispatch (phone to a Desktop session), Remote Control (drive a local
session), Channels (chat app into a running session), Slack (`@Claude` spawns a cloud
session), and scheduled tasks. Note that Claude Tag, the persistent org-identity Slack
agent, is Team/Enterprise only; on Pro/Max you get the older per-user Claude Code in Slack,
which works in channels but not DMs.

**Worker roles** go in `.claude/agents/` as reusable definitions — defined once, usable as
both a delegated subagent and a teammate. Narrow tool list, cheap model, read-only where
possible. For this repository the roles that earn their keep: an engine-adapter reviewer, a
`node:test` test writer, a legal/compliance researcher tracking the DMCA case, and a data
analyst for listening-test results.

**Standing work** goes on a schedule. Three tiers with different durability: cloud
**Routines** (no machine needed, 1-hour minimum, no local files), **Desktop scheduled
tasks** (local files, 1-minute minimum, machine must be awake), and session-scoped
**`/loop`** (expires after 7 days). Remember Routines run with no approval prompts — give
them narrow connectors and reversible tasks.

**Wide fan-out** goes in dynamic workflows, not teams. When you need 50 or 500 units of
reading done, write the script. Agent teams are for when workers need to *argue*; workflows
are for when they need to *cover ground*.

**Coordinate through git and the filesystem, not chat.** This is what the C compiler build
did — lock files in a `current_tasks/` directory, claim-pull-push-release. Chat-based
coordination is where the 70,000 merge conflicts came from.

### Staged rollout

**Week 1 — the spine, no workers.**
Set a monthly spend limit before anything else. Start Remote Control, connect your phone,
use it for a week with zero workers. Add a `CLAUDE.md` section stating the org chart and
the rule that Layer 1 does not edit files. Learn where the *conversation* breaks down
before adding machinery.

**Weeks 2–4 — readers first.**
Add three or four subagent definitions: narrow tools, Haiku or Sonnet, read-only. Run your
first deliberate fan-out — a multi-dimension review of `backend/src/` with every finding
adversarially verified before you believe it. Write one `PreToolUse` hook as your uniform
enforcement point. Add one Routine. Measure a week of spend against your baseline.

**Month 2 — writers and deliverables.**
Add the Telegram channel or raise `--capacity`, depending on whether you want to chat with
the fleet or spawn from it. Introduce exactly one writer per project, in its own worktree.
Wire in the skills that emit real `.pptx` and `.xlsx`. Move reading-heavy roles to Haiku
and confirm quality holds. Set `subagentPromptCacheTtl` to `1h`.

**Month 3 — scale, only on evidence.**
If and only if you are consistently blocked on concurrent throughput, move heavy fan-out to
Managed Agents: a coordinator with a 20-agent roster, per-session dollar budgets that pause
rather than kill, vaulted credentials, and cron deployments. Budget the extra $0.08 per
session-hour on top of tokens.

### The first fleet task, for this repository

`FEASIBILITY.md` names one unresolved go/no-go: the ~$2 listening test in `test-kit/` has
never been run, and *every quality claim in that report is secondhand*. That is the
highest-value thing a fleet could do this week — run the sweep, have independent graders
score outputs blind, and have a verifier check the grades against the audio before you
trust them. Read-heavy, parallel, independently verifiable: exactly where fan-out wins. And
it directly de-risks the $19.99 tier the whole product rests on.

---

## 6. Your three use cases, honestly

**Apps.** The weakest fit for wide parallelism, and it is your main activity. Anthropic
states directly that coding is materially less parallelizable than research, because write
actions produce conflicting decisions where read actions do not. Fan out the review, the
test writing, and the research; keep the building single-writer. Note that Lovable, v0,
Bolt, and Replit are all stronger at *producing* software than at *running* it; for an
existing Node/TypeScript repo like yours, Claude Code remains the better fit.

**Presentations.** Mostly a single-agent job. A fleet helps with the *research behind* the
deck, not the deck. Set expectations on output: PPTX export fidelity is the consistent weak
point across every AI slide tool, and reviewers budget **20–30 minutes of cleanup for a
client-ready deck**. Claude's default output is content-strong but visually plain; the
recommended shape is layered — content model, then design layer, then export.

**Data analysis.** The most important fact here is the benchmark-to-reality gap:
text-to-SQL accuracy drops from **over 86% on Spider 1.0 to roughly 6–20% on Spider 2.0's
real enterprise schemas**, with enterprise deployments landing at 50–69%. Treat "simple
analyzations of data" as needing verification, not as a solved problem. The pattern that
works is fan out extraction per file or record, verify each, then have one agent assemble
the table — and produce a real `.xlsx` with working formulas rather than a wall of text.

A note on quota: Claude Code, Claude chat, and Cowork all draw on **one shared usage pool**,
and Cowork burns it faster than chat because each task spawns sub-agents. Running the fleet
will make your chat feel slower. Plan for it.

---

## 7. Risks and what to re-check

- **Astra's published limits changed within a week of launch.** Re-verify before designing
  around any number.
- **Research previews change.** Channels, Routines, Remote Control, agent teams, and Claude
  Code on the web are all preview or experimental. Flags and behavior can shift.
- **`--dangerously-skip-permissions` is the obvious unattended shortcut and the obvious way
  to get hurt.** Use `dontAsk` with a tight allow-list instead, and relay prompts to your
  phone.
- **Agent teams do not work in headless or Agent SDK sessions.** If you ever build a
  Telegram bot on the SDK as your head bot, teams silently become ordinary subagents.
- **OpenClaw is the popular DIY route to a chat-first personal agent and has a serious 2026
  security record.** Do not give it credentials to a production repository.
- **Astra is OpenAI's first "Critical"-rated cyber model.** The public build refuses
  advanced offensive-security work — relevant if you route dependency scanning or auth
  hardening there.
- **Multi-agent quality failures are silent, and 79% of them trace to ambiguous task
  specs.** Budget for verification and for writing better briefs, not for more workers.
- **Cost compounds faster than intuition.** Set the cap on day one.

---

## 8. Sources

**Astra and the AGI claim** — [OpenAI launch](https://openai.com/index/gpt-6-astra/) ·
[Axios](https://www.axios.com/2026/09/03/openai-astra-gpt-6-agi-brockman) ·
[ARC Prize](https://arcprize.org/blog/astra) ·
[Latent Space preview](https://www.latent.space/p/astra) ·
[Kilo preview](https://blog.kilo.ai/p/gpt-6-astra-what-we-learned-previewing) ·
[Microsoft/OpenAI AGI clause](https://simonwillison.net/2026/Apr/27/now-deceased-agi-clause/)

**OpenAI orchestration** — [Responses multi-agent](https://developers.openai.com/api/docs/guides/responses-multi-agent) ·
[Codex config source](https://github.com/openai/codex/blob/main/codex-rs/core/src/config/mod.rs) ·
[Work + Codex limits](https://help.openai.com/en/articles/20001516-managing-usage-with-gpt-6-astra-in-work-and-codex) ·
[Workspace agents](https://openai.com/index/introducing-workspace-agents-in-chatgpt/) ·
[astra-advisor](https://github.com/DannyMac180/astra-advisor)

**Anthropic stack** — [Subagents](https://code.claude.com/docs/en/sub-agents) ·
[Agent teams](https://code.claude.com/docs/en/agent-teams) ·
[Workflows](https://code.claude.com/docs/en/workflows) ·
[Agent view](https://code.claude.com/docs/en/agent-view) ·
[Remote Control](https://code.claude.com/docs/en/remote-control) ·
[Channels](https://code.claude.com/docs/en/channels) ·
[Routines](https://code.claude.com/docs/en/routines) ·
[Permissions](https://code.claude.com/docs/en/permissions) ·
[Hooks](https://code.claude.com/docs/en/hooks) ·
[Costs](https://code.claude.com/docs/en/costs) ·
[Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview) ·
[Multiagent orchestration](https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration) ·
[Pricing](https://platform.claude.com/docs/en/about-claude/pricing)

**Fleet case studies** — [Anthropic: building a C compiler with parallel Claudes](https://www.anthropic.com/engineering/building-c-compiler) ·
[Anthropic: multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) ·
[Cursor: scaling long-running autonomous coding](https://cursor.com/blog/scaling-agents) ·
[Cursor: agent swarms and the new model economics](https://cursor.com/blog/agent-swarm-model-economics) ·
[Ralph playbook](https://github.com/ClaytonFarr/ralph-playbook)

**Research on when fleets help** — [Cognition: Don't Build Multi-Agents](https://cognition.com/blog/dont-build-multi-agents) ·
[Cognition: Multi-Agents, What's Actually Working](https://cognition.com/blog/multi-agents-working) ·
[Google Research: towards a science of scaling agent systems](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/) ·
Cemri et al., *Why Do Multi-Agent LLM Systems Fail?*, NeurIPS 2025 ·
[CloudZero: what parallel agents cost](https://www.cloudzero.com/blog/claude-code-agents/)

**Security** — OWASP Top 10 for Agentic Applications (Dec 2025) ·
[MCP authorization spec](https://modelcontextprotocol.io) ·
[Claude Code security](https://code.claude.com/docs/en/security)
