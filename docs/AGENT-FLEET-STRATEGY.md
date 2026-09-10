# Bot Armies: A Strategy for Running Agent Fleets as a Solo Builder

*Research completed 2026-09-10. Everything time-sensitive below carries a source and a
date. This space moves faster than any other in software right now — Astra's published
usage limits were cut within a week of its launch — so re-check load-bearing numbers
before you spend money on them.*

---

## 1. Executive summary

**Does the idea make sense?** Yes, with two corrections.

The shape you described — one bot you talk to all day, which decomposes your requests and
dispatches a structured team of workers — is exactly how the good agent systems are built
in 2026. It is the dominant production pattern, it is what Anthropic's own Research
feature does, and it is what you already used to build this repository. You are not
inventing anything exotic.

The two corrections are **scale** and **Astra**.

**Correction 1 — the real ceiling is tens, not hundreds.** Every major platform caps
concurrent workers well below 100, and the caps are deliberate rather than arbitrary:

| Platform | Concurrent workers | Source |
|---|---|---|
| Claude Code subagents | 20 per session (raise with `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`), 3 layers deep | [docs](https://code.claude.com/docs/en/sub-agents) |
| Claude Code dynamic workflows | 16 concurrent, 1,000 agents per run, 4,096 items per fan-out call | [docs](https://code.claude.com/docs/en/workflows) |
| Claude Code agent teams | no hard cap; Anthropic recommends **3–5** | [docs](https://code.claude.com/docs/en/agent-teams) |
| Claude Managed Agents | 20-agent roster, 25 concurrent threads, **one** delegation level | [docs](https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration) |
| OpenAI Codex sub-agents | 4–6 default; OpenAI tested Astra to 64; staff suggest starting at 8–12 | [source](https://github.com/openai/codex/blob/main/codex-rs/core/src/config/mod.rs) |
| OpenAI Responses `multi_agent` | `max_concurrent_subagents` defaults to **3**; no fixed cap on total or depth | [docs](https://developers.openai.com/api/docs/guides/responses-multi-agent) |
| Manus Wide Research | 20 parallel subtasks | vendor docs |
| Devin MultiDevin | 1 manager + 10 workers | Cognition |

The binding constraint is not the tooling. It is that **parallel agents lose the shared
context that makes their work cohere**. Cognition's [*Don't Build
Multi-Agents*](https://cognition.com/blog/dont-build-multi-agents) is the canonical
write-up: two sub-agents building one app produced a Super Mario background and a
non-game-asset bird, because neither could see the other's implicit design decisions.
Anthropic reaches the same conclusion from the other direction — its multi-agent research
system beat single-agent Opus by 90.2%, but only on *research*, where subtasks are
read-heavy and genuinely independent, and it burned about **15× the tokens of chat**.

So: fan out wide for reading, searching, reviewing, and per-file transforms. Keep writing
and design decisions narrow. "Hundreds of bots at a time" is achievable as *throughput
over a day* — hundreds of short-lived workers moving through a queue — but not as
hundreds of simultaneous collaborators on one coherent thing.

**Correction 2 — Astra is a model with an agent runtime, not a bot-army platform, and
the AGI claim was one person's hedged opinion.**

GPT-6 Astra is real: OpenAI unveiled it on 2026-09-03. But the AGI line came from OpenAI
president Greg Brockman at a press briefing — *"I think it's not unreasonable to feel that
we are now in the AGI era"* and *"I do leave it up to the reader to decide for themselves
if this qualifies for them"* ([Axios](https://www.axios.com/2026/09/03/openai-astra-gpt-6-agi-brockman)).
OpenAI's own launch page never claims AGI; it calls Astra *"our most capable model."* Sam
Altman told TIME OpenAI is *"not quite yet"* there. The headline 99.9% on ARC-AGI-3 came
from OpenAI's own provider-adapter harness; on the standard provider-neutral harness Astra
scores **62.7%**, and [ARC Prize explicitly does not claim it is AGI](https://arcprize.org/blog/astra).
Artificial Analysis scores it 61 on its aggregate index — level with GPT-5.6 Sol and
behind Claude Fable 5.1 at 66. The Microsoft contract's AGI clause was removed in April
2026, so the declaration carries no legal weight either.

None of that makes Astra weak. It is genuinely excellent at computer use and long-horizon
autonomous work, and developers are already running it as an orchestrator over cheaper
GPT-5.6 workers. But treat "AGI has arrived" as marketing, and specifically **do not
assume it means Astra can now handle your permissions, accounts, and billing for you.** It
cannot. Nothing can. That is the next section.

**What you would actually build.** A four-layer structure where you own the credentials, a
persistent "chief of staff" session owns the conversation, project leads own the work, and
short-lived workers own the tasks. Section 7 has the concrete build.

---

## 2. The permission question — the part no bot can do for you

You asked: *"what permissions would I need? Or would Astra take care of that for me?"*

**Astra would not, and neither would Claude.** There is a hard architectural rule across
every platform: **a child agent can never hold more authority than its parent, and one
agent's approval is never your consent.** Claude Code documents it plainly:

> Teammates start with the lead's permission settings... A teammate can't approve a
> permission prompt or supply consent on your behalf, and a teammate that was denied an
> action can't relay it to another teammate to bypass the check.
> — [Agent teams](https://code.claude.com/docs/en/agent-teams)

In auto mode the classifier goes further, treating an approval claim relayed from another
agent as untrusted input. Claude Code Remote child sessions inherit the parent's permission
mode and cannot exceed it. The closest thing to "the head bot handles permissions" is
Codex's `auto_review` setting, where escalations route to a *reviewer sub-agent* instead of
to you, with a circuit breaker after repeated denials — and that is a policy you choose,
not authority the model acquires.

### What only you can provision

These require a human with a credit card and a browser. Do them once, up front.

1. **Billing and spend caps.** A subscription (Claude Pro/Max, ChatGPT Plus/Pro) and/or API
   billing. Set a monthly spend limit the same day you enable usage credits. This is your
   only hard stop against a runaway fleet.
2. **Source control.** A GitHub App installation scoped to the specific repositories the
   fleet may touch. Scope it narrowly; the fleet inherits exactly this.
3. **Third-party API keys.** For this project that means Replicate, fal.ai, and an LLM key
   for style prompts. Put them in a credential vault, never in a file the agents can read.
4. **OAuth connectors.** Google Drive, Slack, Linear, Notion — each is a one-time
   browser consent you give personally.
5. **Publishing identities.** Apple Developer and Google Play enrollment, code-signing
   certificates, domain registration, DNS. All human-gated by design.
6. **The permission posture itself.** Which tools run silently, which pause and ask you.

### What the head bot can manage once you have

- Spawning, stopping, and re-tasking workers.
- Routing work to the right worker and merging results.
- Referencing (never reading) vaulted credentials.
- Running inside the budget you set and stopping when it is reached.
- Firing scheduled work without you present.

### The least-privilege layout that actually works

The pattern worth copying is **Managed Agents vaults**, because it solves the problem
properly rather than by policy:

> Vaults store credentials; those credentials **never enter the sandbox**. This is a
> deliberate security boundary — code running in the sandbox (including anything the agent
> writes) cannot read or exfiltrate a vaulted credential, even under prompt injection.

The secret is substituted into the outbound request *after* it leaves the sandbox, only for
hosts you allow-list. Even a fully compromised worker cannot print your Replicate key,
because it never had it. Two rules make this work: scope `allowed_hosts` per credential,
and scope each key minimally at the provider — the agent can do anything the key allows.

Then layer permission policies per tool. `always_allow` for reads, greps, and tests;
`always_ask` for anything that spends money, pushes code, or touches production. And set a
**hard dollar budget per session** — a budgeted Managed Agents session pauses at the cap
rather than dying, and resumes when you raise it.

### The risks that scale with fleet size

- **Prompt injection.** Every worker with web access is an attack surface. Content it reads
  can try to redirect it. Mitigation: allow-list domains per tool, vault the credentials,
  human-gate anything irreversible.
- **Confused deputy.** A worker asks another worker to do what it was denied. Mitigated by
  design on Claude Code; verify it on any stack you adopt.
- **Cost blowout.** Section 6.
- **File conflicts.** Two workers editing one file overwrite each other. Use
  `isolation: worktree` so each gets its own checkout.
- **Silent quality collapse.** More workers producing more output that nobody verifies. The
  fix is an adversarial verification pass, not more workers.

---

## 3. How people are actually building fleets

Five patterns dominate. They compose.

**Orchestrator–worker.** A lead plans, spawns 3–5 specialized workers in parallel, and
synthesizes. This is Anthropic's Research feature, and it is the default for a reason:
workers stay read-only and independent, so the context-isolation problem never bites.

**Deterministic fan-out.** Instead of letting a model decide the structure, you write a
script that fans out over a known work-list — every file, every finding, every source.
Claude Code's dynamic workflows do this in JavaScript with `pipeline()` and `parallel()`.
This is how you actually reach hundreds of agents: 1,000 per run, 16 at a time. The
research behind this document used it — seven parallel research lenses, each finding
adversarially verified by independent refuters.

**Peer teams.** Teammates with their own context windows that message each other directly
and share a task list. Strong for competing-hypothesis debugging, where you want five
investigators actively trying to disprove each other. Expensive: roughly **7× a standard
session**, and experimental (off by default behind `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`).

**Parallel isolated coding agents.** N agents, N git worktrees, one task each, merged by
you. Sidesteps file conflicts entirely.

**Always-on personal assistant.** A long-running process reachable over a chat app, with
cron and sub-agent swarms. The open-source expression of this is OpenClaw (389k stars),
reachable over Telegram, WhatsApp, Slack, Discord, iMessage, and Signal.

**What people report actually works:** research and synthesis, code review from multiple
angles, large mechanical migrations, competing-hypothesis debugging, per-record data
extraction. **What disappoints:** parallel implementation of one coherent feature,
anything needing shared design taste, and small tasks where the round-trip briefing costs
more than doing it.

---

## 4. Primary use cases

Ranked by how reliably a fleet beats a single agent.

1. **Research and competitive analysis.** The clearest win, and where the 90.2% figure
   comes from. Read-heavy, parallel, independently verifiable.
2. **Code review and audit.** Split by dimension — security, performance, test coverage —
   then verify each finding adversarially before believing it.
3. **Large mechanical changes.** Migrations, renames, dependency bumps across many files.
4. **Data analysis.** Fan out extraction per file or per record, verify, then have one
   agent assemble the table. Deliverables land as real `.xlsx` with working formulas.
5. **Presentations.** Mostly a single-agent job with a skill that emits real `.pptx`. A
   fleet helps with the *research behind* the deck, not the deck itself.
6. **App building.** The weakest fit for wide parallelism, and it is what you are doing.
   Design and implementation need shared context. Fan out the review, the test writing, and
   the research; keep the building narrow.

---

## 5. The product landscape

| Option | What it gives you | Concurrency | Hosting | Notes |
|---|---|---|---|---|
| **Claude Code (local + subagents)** | Head bot + workers in one session | 20 subagents, 3 deep | Your machine | Included in Pro/Max |
| **Claude Code dynamic workflows** | Scripted fan-out | 16 live / 1,000 per run | Your machine | The real "many bots" path |
| **Claude Code on the web** | Cloud sessions, no laptop needed | Unlimited parallel sessions | Anthropic VMs | Shares plan rate limits, no separate compute charge |
| **Remote Control** | Phone/browser drives a local session | `--capacity` default **32** | Your machine | Pro/Max; API keys not supported |
| **Channels** | Telegram / Discord / iMessage bridge | n/a | Your machine | Research preview |
| **Routines** | Cloud cron / API / GitHub triggers | n/a | Anthropic cloud | Minimum interval 1 hour |
| **Claude Cowork** | Non-coding deliverables (xlsx/pptx/docx) | n/a | Desktop + cloud tasks | GA on paid plans |
| **Claude Managed Agents** | Hosted coordinator + worker roster | 20 roster / 25 threads | Anthropic or self-hosted | Tokens + $0.08/session-hour; vaults; dollar budgets |
| **ChatGPT Work** | Astra doing multi-hour computer-use tasks | n/a | OpenAI cloud | Mobile + voice; Plus gets Astra here but not in Chat |
| **OpenAI Codex** | Coding agent with sub-agents | 4–6 default | Local + cloud | Included on all ChatGPT plans |
| **OpenAI Workspace Agents** | Persistent, scheduled, API-triggerable | n/a | OpenAI cloud | **Business/Enterprise only** — not on Plus or Pro |
| **OpenAI Agents SDK** | Handoff/orchestration graphs in code | you choose | **You bring the sandbox** | Agent Builder shuts down 2026-11-30 |
| **Mastra** | TypeScript-native agent framework | you choose | Yours | Natural fit for a Node backend |
| **OpenClaw** | Self-hosted always-on chat assistant | Swarm sub-agents | Yours | 389k stars, MIT |

Deprecations to avoid walking into: OpenAI's Agent Builder and Evals shut down 2026-11-30;
AutoGen is in maintenance mode (successor: Microsoft Agent Framework 1.0); OpenAI Swarm is
superseded.

### The specific limits on Astra as your head bot

If you want Astra in the orchestrator seat, these are the facts that decide the design:

- **Plus ($20) does not get Astra in ordinary Chat** — only inside Work and Codex, which
  share one 5-hour allowance of roughly 5–45 messages. Pro $200 gets 200 Chat messages a
  week and 100–900 Work/Codex messages per 5 hours. Limits were cut after launch week.
- **Persistent, scheduled, API-triggerable agents are Business/Enterprise only.** The exact
  feature you want for a bot that works while you sleep is not on individual plans.
- **In the raw Responses API, subagents share the root's model.** Cheap-worker routing
  (Astra orchestrating GPT-5.6 Luna workers) currently requires Codex's
  `collaboration.spawn_agent`, not the plain API.
- **Astra is OpenAI's first "Critical"-rated cyber model.** The public build refuses
  advanced offensive-security work. Worth knowing before you point it at your own auth code.
- **API pricing is $10/$50 per MTok** — twice Claude Opus 5's $5/$25 and five times Sonnet
  5's $2/$10.

None of this is disqualifying. It does mean that "Astra spins up hundreds of bots for me"
is not a product you can buy today at an individual price point.

---

## 6. Economics — what a fleet actually costs

Baselines Anthropic publishes for Claude Code: **~$13 per developer per active day**,
**$150–250 per month**, with 90% of users under $30 per active day.

Parallelism multiplies that close to linearly. CloudZero's May 2026 analysis: ~$13/day for
a normal single-session workflow, **$30–40/day at three parallel agents**, **$50–130/day at
five to ten**. Agent teams run about **7× a standard session** when teammates plan.
Anthropic's own measurement: agents use ~4× the tokens of chat, and a multi-agent research
system ~15×.

At the top end this gets expensive fast. One reported run orchestrated **49 specialized
subagents in parallel for 2.5 hours** and was estimated at **$8,000–15,000 for the single
session**. Treat that as the cautionary tale it is.

**A worked estimate for "hundreds of bots."** Take 200 workers averaging 100k input and
20k output tokens each. On Opus 5 ($5/$25 per MTok) that is roughly $100 input + $100
output ≈ **$200 per wave**. Run ten waves in a day and you are at $2,000/day. On Haiku 4.5
($1/$5) the same wave costs about $40. On Astra ($10/$50) it is about $400.

**Which gives you the single most important lever: tier your models.** Put the expensive
model in the orchestrator seat where judgment lives, and cheap models in the worker seats
where the job is reading and extracting. Anthropic's own guidance says exactly this —
"move the reading-heavy work to a cheaper model... the large model spends its tokens on
planning, checking, and synthesis." A 10:1 cost difference between orchestrator and worker
is normal and correct.

**The second lever is prompt caching.** Cache reads cost 0.1× base input. Sibling workers
sharing a model, effort, and tool set share cache. A fleet with a stable system prefix is
dramatically cheaper than one without.

**Where scale stops helping.** Token usage explains ~80% of performance variance on
BrowseComp — but only where the task is genuinely parallel. Past that point you are buying
coordination overhead, duplicated work, and merge conflicts. Anthropic's own advice is
blunt: *"Three focused teammates often outperform five scattered ones."*

---

## 7. Recommended architecture

### Pick one stack as the spine

Running Astra as head bot over Claude workers (or vice versa) is technically possible —
they would communicate through files, git, and shell — but you would be maintaining two
permission models, two billing surfaces, and two rate-limit regimes, and neither vendor's
orchestration primitives would reach across the boundary. For one person, that friction
costs more than the second opinion is worth.

**Recommendation: build the spine on the Anthropic stack, and keep Astra as a consultant
you invoke deliberately** — for a second opinion on hard architecture calls, or for
computer-use tasks in ChatGPT Work that Claude does not do. The reasons are specific to
what you asked for, not vendor preference:

- The phone-all-day requirement is met natively (Remote Control, Channels, mobile app).
- Persistent scheduled agents are on individual plans, not gated behind Business.
- The concurrency ceilings are 3–5× higher (20 subagents, 1,000-agent workflows).
- Vaulted credentials solve the permission question properly.
- Your project is already built this way, and it works.

### The four layers

```
Layer 0  YOU — accounts, API keys, OAuth grants, spend caps, irreversible-action approvals
   |
Layer 1  CHIEF OF STAFF — one persistent session you reach from your phone all day
   |     Holds the agenda. Decides what gets worked on. Never writes code itself.
   |
Layer 2  PROJECT LEADS — one long-running session per active project
   |     cover-app · decks · data · research     Each owns its own repo/worktree.
   |
Layer 3  WORKERS — short-lived subagents, spawned per task, isolated in worktrees
         reviewer · test-writer · researcher · deck-builder · data-analyst
```

The discipline that makes this work: **Layer 1 never edits files.** It triages, dispatches,
and reports. The moment your chief of staff starts writing code, its context fills with
implementation detail and it stops being able to hold the day.

### The concrete build

**The chief of staff** is a Claude Code session started with Remote Control server mode:

```bash
claude remote-control --spawn worktree --capacity 8
```

That one command gives you a session reachable from the Claude mobile app or
`claude.ai/code`, able to spawn up to eight on-demand worker sessions from your phone, each
in its own git worktree so they cannot collide. Scan the QR code once and you are directing
the fleet from anywhere.

For genuine chat-style access — asking a question from a coffee shop and getting the answer
in the same thread — add a channel:

```bash
claude --channels plugin:telegram@claude-plugins-official
```

Lock it down immediately with `/telegram:access policy allowlist` so only your account can
push messages, and understand that anyone who can reply through the channel can approve
tool use if permission relay is on.

**Worker roles** go in `.claude/agents/` as reusable definitions — a role defined once and
usable both as a delegated subagent and as a teammate. Give each one a narrow tool list and
a cheap model. For this repository the roles that earn their keep are: an engine-adapter
reviewer, a test writer for the `node:test` suite, a legal/compliance researcher tracking
the DMCA case, and a data analyst for the listening-test results.

**Standing work** goes in Routines — cloud-scheduled, no laptop required, minimum one-hour
interval. A daily 8am run that checks the engine supply chain, re-reads the MiniMax sunset
status, and posts what changed is exactly the shape this is for.

**Wide fan-out** goes in dynamic workflows, not in teams. When you need 50 or 500 units of
work done, write the script.

### Staged rollout

**Week 1 — the spine.**
Set a monthly spend limit before anything else. Start the Remote Control server, connect
your phone, and use it for a week with no workers at all. Write a `CLAUDE.md` section that
states the org chart and the rule that Layer 1 does not edit files. Learn where the
conversation actually breaks down before adding machinery.

**Weeks 2–4 — worker roles.**
Add three or four subagent definitions with narrow tool lists and cheap models. Use
`isolation: worktree` on anything that writes. Run your first deliberate fan-out: a
multi-dimension review of `backend/src/`, findings adversarially verified before you
believe them. Add one Routine. Measure a week of spend against the baseline.

**Month 2 — throughput and deliverables.**
Add the Telegram channel, or `--capacity` on the server, depending on whether you want to
chat with the fleet or spawn from it. Wire in the skills that produce real `.pptx` and
`.xlsx`. Move the reading-heavy worker roles to Haiku and confirm quality holds.

**Month 3 — scale, only if throughput is the binding constraint.**
If — and only if — you are consistently blocked on how much work can run at once, move the
heavy fan-out to Managed Agents: a coordinator with a 20-agent roster, per-session dollar
budgets, vaulted credentials, and cron deployments. This is where "hundreds of bots" stops
being a metaphor. It is also where you start paying $0.08 per session-hour on top of tokens,
so make the move on evidence.

### The first fleet task, for this repository

Your feasibility report names one unresolved go/no-go: the ~$2 listening test in
`test-kit/` has never been run, and every quality claim in `FEASIBILITY.md` is secondhand.
That is the highest-value thing a fleet could do this week — run the sweep, have independent
graders score the outputs blind, and have a verifier check the grades against the audio
before you trust them. It is read-heavy, parallel, and independently verifiable: the exact
shape where fan-out wins.

---

## 8. Risks and what to re-check

- **Astra's published limits changed within a week of launch.** Re-check before designing
  around any specific number.
- **Research previews change.** Channels, Routines, Remote Control, agent teams, and Claude
  Code on the web are all preview or experimental. Flag syntax and behavior can shift.
- **Prompt injection scales with fleet size and web access.** Vault credentials, allow-list
  domains, human-gate irreversible actions.
- **`--dangerously-skip-permissions` is the obvious unattended-operation shortcut and the
  obvious way to get hurt.** Prefer permission relay to your phone.
- **Astra's Critical cyber rating means refusals on legitimate security work** — dependency
  scanning, auth hardening. Plan around it if you route security tasks there.
- **Multi-agent quality failures are silent.** Budget for verification, not just generation.
- **Cost compounds faster than intuition suggests.** Set the cap on day one.

---

## 9. Sources

**Astra and the AGI claim** — [OpenAI launch](https://openai.com/index/gpt-6-astra/) ·
[Axios](https://www.axios.com/2026/09/03/openai-astra-gpt-6-agi-brockman) ·
[ARC Prize](https://arcprize.org/blog/astra) ·
[Artificial Analysis](https://artificialanalysis.ai/models/gpt-6-astra) ·
[Latent Space preview](https://www.latent.space/p/astra) ·
[Kilo preview](https://blog.kilo.ai/p/gpt-6-astra-what-we-learned-previewing)

**OpenAI orchestration** — [Responses multi-agent](https://developers.openai.com/api/docs/guides/responses-multi-agent) ·
[Codex config source](https://github.com/openai/codex/blob/main/codex-rs/core/src/config/mod.rs) ·
[ChatGPT Work + Codex limits](https://help.openai.com/en/articles/20001516-managing-usage-with-gpt-6-astra-in-work-and-codex) ·
[Workspace agents](https://openai.com/index/introducing-workspace-agents-in-chatgpt/) ·
[astra-advisor](https://github.com/DannyMac180/astra-advisor)

**Anthropic stack** — [Subagents](https://code.claude.com/docs/en/sub-agents) ·
[Agent teams](https://code.claude.com/docs/en/agent-teams) ·
[Workflows](https://code.claude.com/docs/en/workflows) ·
[Remote Control](https://code.claude.com/docs/en/remote-control) ·
[Channels](https://code.claude.com/docs/en/channels) ·
[Routines](https://code.claude.com/docs/en/routines) ·
[Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web) ·
[Costs](https://code.claude.com/docs/en/costs) ·
[Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview) ·
[Multiagent orchestration](https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration) ·
[Pricing](https://platform.claude.com/docs/en/about-claude/pricing)

**Patterns and limits** — [Cognition, *Don't Build Multi-Agents*](https://cognition.com/blog/dont-build-multi-agents) ·
[Cognition, *Multi-Agents: What's Actually Working*](https://cognition.com/blog/multi-agents-working) ·
[Anthropic, *How we built our multi-agent research system*](https://www.anthropic.com/engineering/multi-agent-research-system) ·
[CloudZero parallel-agent costs](https://www.cloudzero.com/blog/claude-code-agents/)
