# Kettlekin — Build Brief for Claude Code

*Friendly gym clothes starring a tiny crew of nervous, cheering gym equipment. Print-on-demand. Written 2026-11-10.*

## Contents

| § | Section | What's in it |
|---|---|---|
| 0 | Read me first (for the founder) | Start, what you'll see, costs, your dates |
| 1 | Mission & definition of done | Deliverables D1–D7 and where they live |
| 2 | Founder decisions & defaults | Every open decision, its default, overrides |
| 3 | Ground rules for the build session | Mandatory rules, most backed by tests |
| 4 | Brand bible | Name, positioning, personas, voice, tokens, logo, cast, community, don'ts |
| 5 | Product catalog | SKUs, listings, launch set, drops, pricing, copy, data |
| 6 | Artwork & print-file pipeline | Toolchain, print specs, designs D01–D30, export, validators, mockups |
| 7 | Website prototype (D5) | Stack, pages, components, commerce adapter, state, tests |
| 8 | Going live: POD setup, operations & legal | Store setup, sync script, samples, operations, legal |
| 9 | Launch & growth plan | Pre-launch, launch week, content, email, KPIs, 90 days |
| 10 | Build plan & milestones | Repo tree, npm scripts, milestones M0–M9, final report |
| A | Appendix A. Reference code (tested snippets) | A.3 favicon · A.5 crew-kit (cast, wordmark, icon, text-to-path) · A.6 banned-word check · A.7–A.13 print-pipeline code |
| B | Appendix B. Verification ledger | Every [U] item, who confirms it, how |
| C | Appendix C. Key sources | Load-bearing URLs |

Navigate with `grep -nE '^#{1,4} ' BUILD-BRIEF.md` (a line-numbered section map).

---

## 0. Read me first (for the founder)

**What this is.** One file that tells a fresh Claude Code session how to build the whole Kettlekin starter kit: brand assets, print-ready art, catalog, mockups, a working storefront prototype and a go-live kit. The build needs no accounts, keys or money; going live does. Facts are tagged:

| Tag | Meaning | What you do |
|---|---|---|
| **[V]** | Official source (partner help centre, npm registry, standards body) | Trust it; re-check prices on the day you pay |
| **[T]** | Third-party source (blogs, aggregators, community SDKs) | Likely right; confirm before spending |
| **[S]** | Search-engine summary of an official page we couldn't open (ftc.gov, shopify.com, uspto.gov) | Treat like [T]: confirm on the official page before paying or filing |
| **[L]** | Tested locally by us (code ran, render inspected) | Reproducible |
| **[U]** | Unverified | The session confirms live; **you** confirm before spending |

A compound tag [X/Y] means the value is X and its remainder or rule is Y (e.g. [L/U]: measured locally, partner rule unconfirmed).

**How to start**
1. Mac or Linux; on Windows use WSL2 (Ubuntu) for every step.
2. Node.js 24 LTS (24.22.2 is the §7.1 pin; any later 24.x works and the session logs the difference; not 26), Git and Claude Code (claude.com/claude-code; needs a Claude plan or API key).
3. An empty folder (e.g. `kettlekin-build`): save this file there as **`BUILD-BRIEF.md`**, open a terminal there and run `claude`; the session runs `git init` itself.
4. Approve the npm, npx, node and git prompts for this folder; allow ~3 GB of disk.
5. Paste:
   ```text
   BUILD-BRIEF.md is large (~450 KB): never read it in one go. Run grep -nE '^#{1,4} ' BUILD-BRIEF.md to get a
   section map with line numbers. Read §0–§3 and §10 in full now, using Read with offset/limit from the map.
   Then execute §10 milestone by milestone, in order. Before each milestone, read every section on its
   "Read first:" line, and re-read any section a task cites before doing that task. Follow §3 at all times and
   re-read §3 after any context compaction. After each milestone run its verification commands, commit, update
   docs/progress.md and give me a 5-line status. Only ask me what §3 rule 20 allows; otherwise use the defaults
   and log them. Never place real orders or use real payment keys. Finish with the §10 final report (D7).
   ```
6. If a session ends mid-way, open a new one and paste: `Continue BUILD-BRIEF.md: run grep -nE '^#{1,4} ' BUILD-BRIEF.md for the section map, re-read §0–§3 and §10, check git log and docs/progress.md, then read the "Read first:" sections of the first unfinished milestone and continue.`

**What you get** (details in §1): brand kit and character library (D1), validated print files (D2), catalog with margins, a Shopify import CSV and a Printful set-up plan (D3), offline mockups (D4), a static storefront you can click through (D5), a go-live kit (D6) and an honest final report listing what still needs you (D7).

**What you'll see.** The clickable shop exists from milestone M6 (≈ 27 Nov, §10.3); before that, look at the review sheets in `art/review/` and the checklist in `docs/progress.md`. To open the shop, ask the session to "start the preview", or open a second terminal in the same folder, run `npm run build && npm run preview` (on a fresh copy of the repo, once M8 is done: `npm ci && npm run build:full && npm run preview`) and open http://localhost:4173; press Ctrl+C there to stop it (stop it before the session runs its tests, which use the same port). Print files are in `print-files/<design>/`, mockups in `public/mockups/`, the brand guide at http://localhost:4173/brand/. Until your Printful account exists, size charts, delivery times and some costs show "TBC" and the export scripts end with "exit 1" and a blocker list: both expected. The build takes several long sessions over multiple days; compare progress with the §10.3 dates. `REPORT.md` is the final summary.

**When the build is done** (M9, ≈ 11 Dec). Open `REPORT.md`: R1 says what works and what doesn't, R9 lists every open check (Appendix B) with who confirms it, R13 is your dated to-do list. Then work through `golive/README.md`, the §8.2 go-live checklist as tick boxes: **[F]** steps are yours (accounts, payments, lawyer, launch switch); for **[C→F]** steps, start a new Claude Code session in this folder and ask it to prepare that step. Live Printful commands need your API token: put it in a `.env.local` file in this folder yourself (git-ignored; never in the chat) and run `--apply` only in your own terminal after reading the diff (§8.3). Nothing goes live or charges a card until you do it.

**What costs money**

| Item | When | Rough cost | Tag |
|---|---|---|---|
| Building D1–D7 | Now | $0: no accounts, keys or hosting | — |
| Domain | By 17 Nov | ≈ $10–25/yr | [U] |
| Trademark | Knock-out by 17 Nov; file before paid ads | USPTO ≈ $350 per class [S]; attorney opinion ≈ $500–1,500 [U] | [S]/[U] |
| LLC, EIN, bank | Start by 17 Nov | ≈ $50–500 state fee | [U] |
| Printful | Account by 17 Nov | Free plan $0; Growth $24.99/mo optional (§5.1) | [V] |
| Samples | Round 1 Mon 23 Nov (latest 28 Nov) | ≈ $300–450 for 14 pieces + stickers; rounds 2–3 ≈ $400–600 more (§8.4). Printful: 20% off samples, 1 discounted order/month, ≤ 3 items | [U]; discount [V] |
| Shopify Basic | Live by Fri 27 Nov (waitlist from Tue 1 Dec) | $39/mo monthly or $29/mo yearly | [S] |
| Creator gifts | Dec–Jan | ≈ $500–875 | [U] |
| Email, free stickers | At launch | $0 free tiers; ≈ $2 base per free sticker | [U]/[T] |
| **Total to day 90 (10 Nov – 4 Apr)** | | **≈ $3,800 expected (range $2,300–6,000) + 10% contingency; detail §9.9** | |

**What only you can do, and when**

| By | You do |
|---|---|
| Tue 10 Nov | Start the build with the prompt above. Read §2 and reply with any overrides before M1 ends. |
| Tue 17 Nov | Trademark knock-out search + attorney quote; TESS/Etsy check on the launch lines (§4.1). Buy the domain; claim handles. Create a free Printful account (card on file) and a static-host account (Cloudflare Pages, §7.15). Start the LLC, EIN, business bank account and `hello@{domain}` inbox (§8.2 step 1). |
| 18–20 Nov | With the session: download Printful templates for every round-1 placement and run the §6.3.4 paste procedure; review `golive/sample-plan.md`. |
| Mon 23 Nov (latest Sat 28 Nov) | Order sample round 1: 14 pieces + stickers, ≈ $300–450 (§8.4). |
| Fri 27 Nov | Shopify Basic, Shopify Payments and the Printful app (§8.2 steps 3–6); run the step-8 `tierMode` test; register for sales tax in your home state. |
| Tue 1 Dec | DNS live: `{domain}` password page = waitlist; `club.{domain}` = the club-mode waitlist build (§8.1). |
| 1–8 Dec | Sample QA, laid-flat photos, 10 Comeback-Dev chats (§2 decision 17); order round 2 by ~Tue 8 Dec. |
| Mid Dec | Lawyer review of the policy drafts and creator agreement; sign off prices; products saved as drafts. |
| Mon 4 – Tue 5 Jan 2027 | Launch switch (§8.2 step 22, §9.3). |

**Starting later than 10 Nov 2026?** Every date here, in §5.6, §9 and in §10.3 assumes a 10 Nov start. Add one line to the starter prompt, e.g. "Start date: 2 Feb 2027; launch: Tue 6 Apr 2027". The session then re-dates the timeline in `docs/decisions.md` before M0, keeping drops on Tuesdays and the same gaps between steps (samples need ≈ 6 weeks before launch). It never edits this file.

Never paste payment keys or passwords into the chat.

---

## 1. Mission & definition of done

**Mission.** In one repository, with zero accounts, keys or live orders, build everything needed to launch **Kettlekin** (friendly print-on-demand gym clothes for casual and gym-anxious people, starring nervous, cheering gym equipment), up to a go-live kit that turns it into a Shopify + Printful store, drafts only. Nothing is reported as working unless a command proved it.

All must be true (paths per §10.1):

| ID | Deliverable | Done means |
|---|---|---|
| **D1** | Brand kit | The name is one value in `brand.config.json`. `npm run brand` regenerates tokens (JSON, CSS variables, Tailwind `@theme`), wordmark, icon, favicons (SVG + PNG) and the cast library (7 characters × 10 expressions × allowed poses × 4 LODs: full / XS / icon / embroidery); contact sheets show every expression and pose. The rename test passes (§4.1); `/brand` renders from the same data. |
| **D2** | Artwork | Every design D01–D30 (§6.4.7–6.4.8) is a code module rendering a print-ready PNG per placement × colourway × tier. `npm run validate:print` passes for 100%; `print-files/manifest.json` lists each file's spec, hash and result. Sheets were looked at (§3 rule 15); `art/REVIEW.md` has a row per design and cast sheet. |
| **D3** | Catalog | `catalog/catalog.json` validates against its schema. Every variant (colour × size) has a base cost (source + tag), price and margin; the invariants (same price every size, margin floor, real size ranges) are unit-tested. `exports/shopify-products.csv`, `exports/catalog-margins.csv` and `exports/printful-sync-plan.json` (+ checklist) are generated with their blocker lists; the exporters exit 1 while Appendix B blockers remain (§10.2). |
| **D4** | Mockups | Offline, code-drawn flat-lay mockups (`public/mockups/`) for every listing × colourway (no photos, no bodies), plus 1200×630 OG images (`public/og/`). |
| **D5** | Storefront prototype | `npm run build` makes a static `out/` with **zero env vars**; every §7 page exists; the cart works, checkout is a labelled mock, community is local-only; e2e, axe (0 violations) and Lighthouse budgets pass. |
| **D6** | Go-live kit (`golive/`, `exports/`) | The Printful sync script is dry-run by default and can only create **draft** products and orders. Plus Shopify CSV, theme kit, policy and legal drafts, sample plan (`golive/sample-rounds.json`), QA and launch checklists. |
| **D7** | Final report (`REPORT.md`) | What was built, how to run it, every verification command with its real output, every open [U] item with who confirms it. |

---

## 2. Founder decisions & defaults

The build **never blocks** on these: it uses the default, logs it in `docs/decisions.md` and moves on. Override in one line (e.g. "Decision 11: free shipping at $60"); "config" means `brand.config.json` or `catalog/`.

| # | Decision | Default | Why | Override |
|---|---|---|---|---|
| 1 | Brand name | **Kettlekin**; then **Gymlings** (only with a clean US 25/16/21/35 opinion and no plush/toys in Australia), then **Huddlebell** | Zero exact-match hits in two search rounds [T]. | `name` in `brand.config.json`, `npm run brand` |
| 2 | POD partner | **Printful** for every year-one product. **No Printify account and no Printify exporter in year one.** The 24 oz protein shaker (Printify, ≈ $13.98 [T]) is deferred: separate parcel, and it leans toward protein/diet culture (§5.1). Revisit only if the founder approves it. | Deepest Shopify sync; 4.8★ on the Shopify App Store [V]. | Founder approves the shaker |
| 3 | Platform | **Shopify Basic + Printful app** at go-live; prototype: **static Next.js** + `MockCommerceAdapter` | Zero accounts to build; headless later. | Swap the `CommerceAdapter` (§7) |
| 4 | Market | **US only** | Trademark scope, shipping, one tax regime. | config `markets`, after clearance |
| 5 | Currency | **USD**, integer cents, tax-exclusive | US launch. | config `currency` |
| 6 | Launch date | Public launch **Tue 5 Jan 2027**; **"Rest, don't quit"** mid-January (Mallow Hours). December: waitlist, quiz, free Send a Bel e-card; **no orders** | Samples need 2–3 weeks [U]; January is the gym-join peak [U]. | Gifting soft launch in early Dec only if samples pass by 1 Dec |
| 7 | Sizing, navigation | **Unisex** core; activewear labelled by fit ("fitted / supportive"), never gender; shop **by vibe** and **by product type** (§4.8) | Gender-inclusive cute is white space [T]. | Not recommended |
| 8 | Visibility tiers | Every hero design ships **Quiet / Loud / Private** (Private on tees only); the PDP **defaults to Quiet** | #1 anxiety trigger is being watched (53%) [T]. | config `tiers.default` |
| 9 | Launch set | §5.5: 16 listings, D01–D13 | Small evergreen core plus monthly drops. | `launch` flags in `catalog/` |
| 10 | Pricing | Headline: hero tee **$34** · everyday tee **$28** · Private −$6 (tees only) · **Buddy Pack $60** (−$8 on an A + B pair) · **same price in every size**. Full ladder and unit economics: §5.7. | Between Etsy POD and Gymshark [T]; base costs pulled live [U]. | Edit `catalog/src/listings.json`; margin tests re-run |
| 11 | Free shipping | **$75** | About two tees plus stickers; unproven [U]. | config `shipping.freeThresholdCents` |
| 12 | Printful plan | **Free**; **Growth** ($24.99/mo [V]) once "up to 33% off" beats the fee | No fixed costs before revenue. | Any time (base costs carry `plan`) |
| 13 | Prototype community | **Local-only**, no accounts or backend (§4.8); cheer wall and crews are demos | Proves the experience at zero ops cost. | config `features.*` |
| 14 | Cheer wall, crews at launch | **No: v1.1** | Both need moderation and personalisation ops. | Flags, plus a moderation plan (§8) |
| 15 | Personalisation (D27, D28) | **Off at launch**; prototype demos generation, validation and draft-order review; **$0 surcharge** when it ships (§5.7) | Per-order files, review step, offensive-text risk. | config `features.personalisation` |
| 16 | Email | `EmailAdapter` no-op; forms say "demo: nothing was sent" | No accounts in the prototype; provider later [U]. | Implement the adapter (§8) |
| 17 | Wearability check (Comeback Dev) | Launch neutral-led (≥ 50% neutral garment colours per drop, §4.5). You run 10 short interviews **1–8 Dec** on the round-1 samples, **D04 Loud on Bay and D09 Loud on Navy, plus D01 Quiet (Sand hoodie) vs D01 Loud (Ivory tee)**, before launch and before any paid ads. Use the held lines (§4.4) as A/B stimuli. | Top risk: "cute stuff is for 19-year-old girls." | Results may change the colourway mix |
| 18 | Launch cast | **Bel, Mallow, Gus, Pip & Pop** lead launch products; Sip = D07 bottle (launch), Tuck = D03 Off Camera, On Purpose tee (launch), Ollie = D20 tee (2 Mar), one design each (§4.7 Tiers). | Supporting silhouettes are fixed in v3 [L]. | `characters.json` `tier` |
| 19 | Blush | **An emotion:** shy, proud, hyped and nervous faces only | Avoids generic kawaii grammar; saves a thread. | `blushRule: "always"` (not recommended) |
| 20 | Embroidery colours | **No unlimited-colour thread**; Bel 2–3 standard threads; Mallow and Gus one-colour line art (Purple 1832 / Grey 1718) or DTG only | Unlimited colour ≈ +$3.50–3.95/item [U]. | `embroidery.unlimitedColor: true` |
| 21 | Dark mode | **Not in v1**; dark *sections* only | Scope. | — |
| 22 | Analytics, cookies | **None in the prototype**; the club build allows one cookie-free counter (§7.13); KPIs: §9 | Privacy-first; nothing to consent to. | Later, with a consent design (§8) |
| 23 | Minimum age | **13+**; Slogan Lab 18+ (§4.8) | US children's-privacy rules [U]. | — |
| 24 | Tote | **$30** with a `pending` margin exception; codes exclude it | −$1.29 at its $25.75 high base under 15% off. | $34, or a cheaper blank |
| 25 | B+C Private 2XL+ | If a +$3 upcharge is confirmed, B+C Private only up to XL | Keeps every contribution ≥ $0 under codes. | A margin exception |
| 26 | Art deviations | D17 LIGHT ink-outline board; D09/D27 seal ×0.95 | Knock-out text fails; the full-size halo clips. | Approve at the M5 review |
| 27 | Gift sets | First Visit Kit and Rest on Purpose Set from drop 11 | Gifting season; small launch set. | Kit at launch |
| 28 | Returns | §8.5: misprint → free remake or refund; one size swap at the standard first-item shipping rate; no change-of-mind returns | Every piece is made to order. | Edit §8.5 |
| 29 | Go-live shipping | A = Printful rates + free ≥ $75; fallback B = flat $5.95 below $75 (§8.2 step 13) | Carrier-calculated rates on Basic are [U]. | Approve B |
| 30 | Launch architecture | §8.1 (Shopify password page + club-mode `club.{domain}`); `tierMode` "option" unless §8.2 step 8 fails | December waitlist, no orders. | One line |
| 31 | Bottle | D07-W788 launches only if its wrap template and print method are verified before round 1; otherwise drop 1 (launch = 15 listings) | Wrap size and method are [U]. | Move it now |

---

## 3. Ground rules for the build session

Every rule is mandatory; every named test runs in CI (`npm run ci`).

1. **Read in stages, then build.** Read §0–§3 and §10 in full before writing code. Before each milestone, read every section on its **Read first:** line (use the `grep -nE '^#{1,4} '` map and Read with offset/limit), and re-read §3 after any context compaction. Execute §10 milestones in order; don't start a milestone until the previous one's acceptance checks pass. Keep `docs/progress.md` (milestone checklist with dates) current.
2. **Verify versions live:** `npm view <pkg> version time dist-tags` before installing; pin **exact** versions (no `^`/`~`), ≥ 14 days old unless a newer one fixes a security issue. The brief's versions are a 2026-11-10 snapshot; record what you installed in D7.
3. **Read Next.js's bundled docs** (`node_modules/next/dist/docs/`) before writing routes or config; commit the `AGENTS.md` block `next dev` writes; follow §7's static-export constraints.
4. **Never invent facts.** Prices, base costs, size ranges, garment colours, print areas, DPI and lead times live **only** in data (`catalog/`, `print-specs.json`) as `{ value, source, tag: "V"|"T"|"L"|"S"|"U", checkedAt }`; components never hard-code them. Unknown: `null` + tag `U`, a visible "TBC", a D7 entry.
5. **The name lives in one place:** `brand.config.json` → `name`; CI fails on the literal (any case) outside §4.1's allowlist; copy uses `{brand}` / `{castNoun}`.
6. **No money, no live orders.** No real payment keys, tokens or passwords in the repo (`.env.example` holds empty values). Checkout is a mock labelled "Demo checkout: no payment is taken". Partner scripts are **dry-run by default**; a real call needs `--live` **and** an env token and creates **drafts only**: never confirm, submit or pay for an order.
7. **Blocked network ≠ fake data.** If a host is unreachable (printful.com, api.printful.com, printify.com, shopify.com, USPTO, registrars), never fabricate a response: use the brief's fallback, keep its [U] tag, log host, command and error in D7.
8. **No borrowed IP.** Don't copy, trace or imitate other brands' characters, logos, slogans, fonts, patterns or photos; no real people; check new characters and poses against §4.7's resemblance list. Shipped assets (font packages, `lucide-react`, files copied into `public/` or `print-files/`) are OFL-1.1, MIT, ISC or Apache-2.0; every direct dependency has an OSI licence (`@resvg/resvg-js` is MPL-2.0, a devDependency). Node packages: the §10 M0 licence test. Licences go in `licenses/` (fonts: `licenses/fonts.json`).
9. **Copy is tested.** The §4.4 banned list and copy-lint run in CI over every customer-facing string (`content/`, `catalog/`, slogan strings in `art/designs/`, visible text of `out/**/*.html`); any hit fails the build.
10. **Only cleared lines go on product.** Product art may use only the exact lines in the Text columns of §6.4.7–6.4.8 (the reviewed D01–D30 lineup, including whispers and format labels); `content/print-lines.json` is the machine list. §4.4's ten core slogans are among them. Every new line needs founder approval, must pass the banned list, and is tagged [U] until its trademark/Etsy check (Appendix B U6).
11. **WCAG 2.2 AA.** Only §4.5's text/background pairs (unit-tested); axe 0 violations on every page; a full keyboard path through cart and checkout; visible focus (§4.5); `prefers-reduced-motion` honoured; touch targets ≥ 44×44 px; alt text on every character image (§4.7).
12. **Print files must pass the validator** before they count as done: `npm run validate:print` (§6.6; values in §6.2) checks exact template pixels, sRGB 8-bit RGBA PNG, alpha 0 or 255 only, text outlined (no `<text>`, no NaN), and every primary element ≥ 3:1 against the garment.
13. **Garment rules.** Light garments: `oat`/`white` export **transparent** (no white without an underbase). Dark garments: the oat sticker border (§4.7). **No text on leggings, sports bras or any stretch panel.** AOP uses the year-one seamless patterns (D16, D21, D23) at a fixed 6 in tile scale (§6.3.3); no tossed heads, no text. No Caprasimo under §4.5's minimums.
14. **Fonts for rasterising are the two TTFs** (§6.1 pitfalls 1–3); only Caprasimo and Atkinson Hyperlegible Next.
15. **Look before you declare art done:** Read the rendered PNGs and contact sheets, check them against §4.7 (silhouettes, misreads, sticker borders, text fit), fix, re-render, look again; D7 lists the sheets inspected.
16. **Deterministic output:** same inputs, same bytes (no timestamps, seeded RNGs); manifest SHA-256 hashes make a re-run diff show only real changes.
17. **Privacy by default:** no analytics, trackers, third-party scripts or cookies in the prototype; `localStorage` holds only cart and community data (a visible "Clear my data" wipes it); no email is sent.
18. **No bodies in imagery:** characters and code-drawn flat-lays only; no stock or AI people, no before/after.
19. **Commit per milestone** as `M<n>: <what changed>` once it passes. Never commit secrets, `.env` or files over 10 MB; print files are git-ignored and listed in the manifest.
20. **Ask only what this rule allows.** Ask the founder only about §2 decisions, a decision a section explicitly hands to the founder, or a new line (rule 10). List open ones in each milestone status. Otherwise take the default, log it in `docs/decisions.md` and continue.
21. **Honest reporting.** Never claim something works unless a command proved it in this session. D7 pastes each verification command with its real result, marks untested items **untested**, lists every open [U] item.
22. **Brand rules are tests, not taste.** Every checkable §4 rule (contrast, banned words, ≤ 3 characters on a Loud garment, no recoloured characters, stamp totals never decreasing) gets a test; the rest join the rule 15 checklist.

---

## 4. Brand bible

**The system in one line:** gym-equipment characters (the IP moat) in grown-up, garment-dyed colourways and a vintage athletic serif, on a community engine where progress never goes down.

### 4.1 Name & config

| Field | Value |
|---|---|
| Name | **Kettlekin**, pronounced KET-ul-kin: *kettle(bell)* + *kin* (your people) |
| Two jobs | The brand **and** the cast's collective noun ("Bel is a Kettlekin", "Which Kettlekin are you?"). |
| Tagline, descriptor | **Wear a friend to the gym.** · **friendly gym clothes** (with the Bel tittle, it fixes the "tea kettle" misread) |
| Alternate #1 | **Gymlings.** IP Australia GYMLINGS No. 2616722, class 28, shown as registered [U]; beginner slang [T]; no US mark found [U]. |
| Alternate #2 | **Huddlebell.** Zero exact hits [T]; class 25 HUDDLE-formative marks are crowded (HUDDLE HAT live; HUDLE pending) [T]: medium risk. No i/j: icon lockup. |
| Closest prior right | **KETTLE AND DESIGN, US Reg. 6244834** (chicken head in a kettle; shirts, sweatshirts, hats) [T]: low–medium risk; an attorney confirms KETTLEKIN is distinguishable. |

**`brand.config.json`** (repo root): the **only** place the name is written; the other keys hold §2 defaults.

```json
{
  "name": "Kettlekin",
  "overrides": { "wordmarkText": null, "castMemberNoun": null, "handle": null, "domain": null },
  "tagline": "Wear a friend to the gym.",
  "descriptor": "friendly gym clothes",
  "bellGlyph": "auto",
  "markets": ["US"],
  "currency": "USD",
  "tiers": { "default": "quiet" },
  "shipping": { "freeThresholdCents": 7500 },
  "features": {
    "stampCard": "on", "firsts": "on", "quiz": "on", "sendABel": "on", "tierToggle": "on",
    "cheerWall": "demo", "crews": "demo", "personalisation": "demo", "waitlist": "demo"
  },
  "minimumAge": 13
}
```

`features`: `"on"` = live at launch; `"demo"` = prototype only, with a "demo" badge; `"off"` = hidden. `waitlist`: `on` = buy buttons become "Join the waitlist" (the December club build); `demo` = prototype default with a preview switch (`?preview=waitlist`); `off` = after launch (§7.4).

**Derivation rules** (`lib/brand.ts`; nothing else reads the raw name): `wordmarkText = overrides.wordmarkText ?? name.toLowerCase()` · `castMemberNoun = overrides.castMemberNoun ?? name` (copy: "Which {castNoun} are you?") · `handle = overrides.handle ?? "@" + wordmarkText` · `domain = overrides.domain ?? wordmarkText + ".com"` (placeholder until bought) · `bellGlyph: "auto"` swaps the tittle of the **last** `i` or `j` for the mini-Bel; with no `i`/`j`, the horizontal icon lockup (§4.6).

**Tests (CI):**
1. **Name grep:** `/kettlekin/i` appears in no tracked file except `brand.config.json`, `BUILD-BRIEF.md`, `REPORT.md`, `docs/**`, `licenses/**`, `art/REVIEW.md`, `catalog/live/**` and generated output (`out/`, `.next/`, `public/brand/`, `public/mockups/`, `public/og/`, `print-files/`, `exports/`). The npm package is `storefront`. Copy uses `{brand}`, `{castNoun}`, `{handle}`, `{domain}`; `golive/**` uses `{brand}` placeholders like `content/`. Tests never contain the literal: they build the regex from `brand.config.json` `name` (wordmark expectations keyed by it).
2. **Rename** (temp-copy procedure: §10.2 `test:integration`): with `name` = `"Gymlings"`, `npm run brand && npm run build` puts "gymlings" in `out/index.html` and the wordmark, and the old name is nowhere in `out/` or `public/brand/`; `"Huddlebell"` uses the horizontal lockup.

**Founder clearance checklist** (not legal advice; ledger: Appendix B):
- [ ] USPTO (https://tmsearch.uspto.gov): KETTLEKIN, KETTLE KIN, KETTLEKINS and KETTLE-formative marks in classes 25, 16, 18, 21, 9, 35, 41 and 28 (apparel, paper/stickers, bags, bottles, digital stickers, retail, fitness content, future plush); TSDR for Reg. 6244834. Also DAY ONE in classes 9 and 42 (software): keep "day one" a lowercase descriptive label, never an app, feature, tracker or line name. Printed apparel text that only quotes it (D05 "day one: the sequel.") is fine.
- [ ] Other markets (EUIPO/TMview, UKIPO, IP Australia, CIPO) before selling there.
- [ ] Domain, in order: `kettlekin.com` → `kettlekin.co` → `getkettlekin.com` → `shopkettlekin.com` → `kettlekin.club` (not checked [U]).
- [ ] Handles `@kettlekin` on Instagram, TikTok, Pinterest, YouTube, Threads, Bluesky; fallbacks, identical everywhere: `@kettlekin.club` → `@kettlekincrew` → `@meetkettlekin` [U].
- [ ] Marketplace sweep (Etsy, Amazon, Redbubble, TikTok Shop): "kettlekin", "kettlebell with face", "kettlebell character sneakers", "gym equipment characters".
- [ ] TESS and Etsy check on the 10 core slogans (§4.4) plus "department of showing up", "moving at the speed of okay", "i count visits" and "New year, no pressure. No resolutions needed." before round 1 (~23 Nov); every other line in `content/print-lines.json` before its drop (Appendix B U6). No exact hits so far, which is not clearance [U].
- [ ] Never register character names as marks ("Mallow" is also a Pokémon character); register copyright in each final model sheet.
- [ ] Attorney clearance opinion **before paid ads or bulk samples**.

### 4.2 Positioning, promise, pillars, enemy, manifesto

**One-line pitch:** {brand} makes friendly gym clothes starring a tiny crew of gym equipment who are just as nervous as you are, and who cheer for you anyway.

| Positioning | |
|---|---|
| For | Casual and nervous gymgoers put off by mainstream fitness brands: first-timers, returners, "for my brain" movers, gym-buddy pairs |
| It is | Character-led gym apparel that turns the scary stuff on the gym floor into friends who cheer for **showing up** |
| Unlike | Physique-first brands (skulls, wolves, "earn it"), it counts **visits, not bodies**, treats **rest as part of the plan** and lets you **choose your volume** (a sticker-sized friend on your chest, a big print on your back, a secret on the inside label) |
| Proof the gap is real | About half of adults report gym anxiety: 56% in the UK, 67% of women vs 49% of men (PureGym 2022/23) [V]. "The way other users look at me" is the #1 US factor at 53% [T]. 19% of Gen Z have walked away over fear of being filmed [T]. No brand found owns "cute, friendly gym apparel for beginners" [T, not exhaustive]. |

**Brand promise: "Wear a friend to the gym."** Quiet, Loud and Private versions; grown-up garment-dyed blanks; **one price in every size**; no body or food comments, no guilt-trips.

**The enemy: The Glare:** being watched, filmed, judged and ranked on the gym floor, and the culture that monetises it (physique-as-credential, pain-as-virtue, "no excuses", filming strangers). **Never drawn** (no villain, no eye motifs): we fight it by existing, not with fear, and reject the *culture*, never people who train hard.

**Pillars:** (1) **Friends, not idols:** no human bodies on product, ever; characters with *feelings* replace physiques to compare yourself to (the cast, §4.7). (2) **Showing up counts. So does rest.** Progress is visits, rest days and comebacks, never outcomes; nothing logged goes down (stamp card, Mallow Hours, "both halves", §4.4, §4.8). (3) **Your volume, your call:** you choose how visible you are, consent-first; from a few steps back it reads as a good vintage tee, and the joke rewards a closer look (Quiet/Loud/Private, The Small Print, neutrals, no filming, fits laid flat).

**Manifesto** (About page; a future swing tag if pack-ins are ever added; use verbatim):

> The hard part was the door.
> Not the weights. Not the machine with the little sticker on it. The door, and getting past everyone who seems to have been here forever.
> So we made you some company. A kettlebell who's nervous too. A foam roller who thinks rest is training. A gym bag that spent three years in a closet and isn't sorry. Two ends of one dumbbell who'd rather go together.
> We count visits, not bodies. Rest days go on the card. Coming back counts as much as starting. We don't film strangers, we don't rank anyone, and nobody has to be loud unless they want to be.
> Wear a friend. Go in. Do one thing, or nothing yet.
> Whenever you're ready, the crew's already there.

### 4.3 Personas

Personas span genders on purpose (about half of men report gym anxiety too [V]); statistics: §4.2, Appendix C.

**First-Timer Frankie, 21–27** (any gender; she/her in the research). New to a $10–15/month gym after months of "getting ready"; off-peak, headphones on, cardio corner. Fears being watched and filmed. Buys a mascot that's "literally me", opaque pocketed leggings, anything under $35. **Bel**, plus **Tuck**. *Lands:* "You don't have to know what you're doing yet." *Repels:* "transformation", "no excuses". **Needs:** Quiet by default; the First Visit Plan; "Is it see-through?" answered on the PDP; under-$35 prices easy to find; pop-ups that close on first click.

**Comeback Dev, 32–45** (any gender; he/him in the research). Lost 2–10 years to kids, injury or burnout; often XL–4XL now; feels "behind". Objections: "cute stuff is for 19-year-old girls", "cheap POD shirts shrink". Buys deadpan humour on heavyweight garment-dyed neutral tees (to 4XL, one price), a cap, joggers; it must read as vintage merch from a few steps back. **Gus**. *Lands:* "Welcome back. No catching up required." *Repels:* pink-only palettes, bro intensity, "girlboss". **Needs:** neutrals first; size range and "same price in every size" on the PDP; inches and cm; honest care and shrink notes; a flat-lay of the quiet print at a distance.

**Brain-First Priya, 25–38** (she/they). Manages anxiety, ADHD or depression; moves "for my brain, not my body"; inconsistent in bad weeks; **rest days are non-negotiable**; unfollows over diet talk and guilt-trip streaks. Buys rest-positive lines, a character with feelings, soft crews, stickers, a journal. **Mallow**. *Lands:* "Rest days count. You're still on the card." *Repels:* "earn your rest", "burn it off". **Needs:** rest counts fully and nothing decreases; opt-in reminders only; reduced motion; no streaks, countdowns or red "missed" states.

**Gym Buddy Duo, Sam & Alex, 18–26** (any gender mix). Go together because going alone feels scary; under $30 an item; content only *with consent*. Buy two-for bundles, complementary (not matching) designs, referral rewards for both, a shared stamp card. **Pip & Pop**. *Lands:* "Bring your gym person. You both get stickers." *Repels:* elitist aesthetics, expensive single items, unexplained slow shipping. **Needs:** Buddy Pack and split tees side by side; share links; honest lead times; a crew demo.

**Cross-persona rules:** opaque fabrics, pockets, relaxed fits by default · a Quiet variant for every hero design (catalog test) · size range and "same price in every size" on every PDP (e2e) · navigation **never by gender** (e2e: no "men"/"women" labels) · any web imagery spans genders, sizes, ages and abilities (the prototype has none) · no body-outcome language (banned list).

### 4.4 Voice & tone

**Who's talking:** a supportive friend who is *also a little nervous*: warm, specific, gently funny; texts "you went!!" and means it, and admits they sat in the car for a minute first.

**Principles** (how each is tested):
1. **Text like a friend:** second person, short sentences, contractions, about grade 6 (Flesch-Kincaid ≤ 7 on `content/` long-form; warn only).
2. **Specific beats generic:** the real tiny thing (sitting in the car for a sec, the little sticker on the machine, wiping the bench); "good vibes only" is lazy (review).
3. **The joke is on the character, never the reader** (review).
4. **Permission, not pressure:** "it counts", "no rush", "whenever you're ready", "you're allowed", "no pressure"; no fake urgency, guilt or FOMO (banned list).
5. **Honest about hard:** name nerves, bad weeks, breaks; celebrate comebacks, never "restarts" (review).
6. **Sincere first, funny second:** at most **one joke**, **one `!`** and **one ALL-CAPS word** per message; caps only in Sip's or Pop's voice (copy-lint).
7. **Both halves:** every rest or comfort line sits near a gentle show-up line on the same surface; cosy, not anti-effort (review per page).
8. **Honest about how it's made:** POD = *made just for you*, with real windows from data (`{production_window}`, `{transit_window}`) (e2e).
9. **Case:** brand copy sentence case; character speech and slogans lowercase (plus the character's quirk); format labels (receipt "total", crest "est.") stored lowercase, may be set in caps by the layout (copy-lint).
10. **Accessible by default:** no ableist intensifiers or ability-dependent idioms; emoji rare, never in errors, sizing, money or anything about bodies; alt text per §4.7 (banned list; e2e).

**Signature vocabulary:** showed up, counts, the crew, buddy, your pace, day one, stamp, rest on purpose, comeback, whenever you're ready, made just for you, quiet / loud.

**Banned words and themes.** Save this verbatim as `brand/banned-words.json` [L, 2026-11-10: 0 hits on 217 cleared lines (§4.4, §6.4.7–6.4.8; scope `product`), 0 misses on 98 known-bad lines, 0 `names` hits on 74 listing and collection names]. `tests/unit/banned-words.test.ts` (A.6) and a post-build scan of the visible text of `out/**/*.html` apply it as `notes` says; any hit fails the build. Exemptions: the scope rules below.

```json
{
  "version": 1,
  "notes": "Case-insensitive JS RegExps. Normalise (NFKC, straight quotes), delete 'allow' matches, test in-scope 'banned'. all = every customer-facing string; product = + catalog copy, print slogans; names = collection, drop, bundle, design, listing names.",
  "allow": [
    "\\bno resolutions needed\\b",
    "\\b(high|low|print|screen)[- ]resolution\\b"
  ],
  "banned": [
    {"id": "weight-loss", "cat": "body", "scope": "all", "re": "\\bweight[- ]?loss\\b|\\b(lose|losing|lost|drop|dropping|gain|gaining|cut|cutting)\\s+(the\\s+|some\\s+|a\\s+few\\s+)?(weight|pounds|lbs?|kilos|kgs?)\\b"},
    {"id": "weigh-in", "cat": "body", "scope": "all", "re": "\\bweigh(ing)?[- ]?ins?\\b|\\bweigh\\s+(yourself|myself|themselves|ourselves|himself|herself)\\b"},
    {"id": "lb-kg", "cat": "body", "scope": "all", "re": "\\b\\d+\\s?(lbs?|kgs?|pounds|kilos)\\b"},
    {"id": "calories", "cat": "body", "scope": "all", "re": "\\bcalori(e|es)\\b"},
    {"id": "burn", "cat": "body", "scope": "all", "re": "\\bburn(s|ed|ing|t)?\\b"},
    {"id": "shred", "cat": "body", "scope": "all", "re": "\\bshred(s|ded|ding)?\\b"},
    {"id": "cut-bulk", "cat": "body", "scope": "all", "re": "\\b(get|getting|got)\\s+cut\\b|\\bcut(ting)?\\s+(season|phase)\\b|\\bbulk(ing)?\\b"},
    {"id": "tone", "cat": "body", "scope": "all", "re": "\\btoned\\b|\\btoning\\b|\\btone\\s+(up|your|those)\\b"},
    {"id": "size-words", "cat": "body", "scope": "all", "re": "\\bskinny\\b|\\bfat\\b|\\bslim(s|mer|ming)?\\b|\\bflatter(s|ing)?\\b|\\bproblem\\s+areas?\\b"},
    {"id": "body-season", "cat": "body", "scope": "all", "re": "\\b(bikini|summer|beach)[- ]body\\b"},
    {"id": "transformation", "cat": "body", "scope": "all", "re": "\\btransformations?\\b|\\bbefore\\s*(and|&|/|-)\\s*after\\b|\\bprogress\\s+(pics?|photos?|pictures?)\\b"},
    {"id": "food-morality", "cat": "body", "scope": "all", "re": "\\bguilt[- ]?free\\b|\\bcheat\\s+(meals?|days?)\\b|\\bclean\\s+eating\\b|\\btreat\\s+(yo)?(urself|yourselves|myself|ourselves)\\b|\\bthen\\s+snack\\b|\\bfeed\\s+me\\b"},
    {"id": "earn-deserve", "cat": "body", "scope": "all", "re": "\\bearn(s|ed|ing)?\\b|\\bdeserve(s|d)?\\b"},
    {"id": "body-slang", "cat": "body", "scope": "all", "re": "\\bflat\\s+(days?|but\\s+fine|tummy|stomach|belly|abs|chest)\\b|\\bbuns\\b|\\bmuffin\\s+tops?\\b|\\bdoughy\\b|\\bloaf\\b|\\b(belly|back)\\s+rolls?\\b|\\blove\\s+handles\\b"},
    {"id": "body-parts", "cat": "body", "scope": "all", "re": "\\b(booty|butt|glutes?|six[- ]?pack|thigh[- ]gap|thicc)\\b|\\babs\\b"},
    {"id": "body-compliment", "cat": "body", "scope": "all", "re": "\\byou\\s+look\\s+(amazing|great|good|hot|thin|fit|incredible)\\b"},
    {"id": "diet-words", "cat": "body", "scope": "all", "re": "\\bdiet(s|ing)?\\b|\\bdetox\\b|\\bcleanse\\b|\\bfit(spo|spiration)\\b|\\bthinspo\\b"},
    {"id": "proof-claims", "cat": "claims", "scope": "all", "re": "\\bsquat[- ]proof\\b|\\bwon'?t\\s+fade\\b|\\bno[- ]shrink\\b|\\bmade\\s+in\\s+(the\\s+)?usa\\b"},
    {"id": "grind", "cat": "grind", "scope": "all", "re": "\\bno\\s+excuses?\\b|\\bno\\s+pain,?\\s+no\\s+gain\\b|\\bno\\s+days\\s+off\\b|\\bbeast(\\s*mode)?\\b|\\bsavage\\b|\\bgrind(s|set|ing)?\\b|\\bhustle\\b|\\bgo\\s+hard\\s+or\\s+go\\s+home\\b"},
    {"id": "violence", "cat": "grind", "scope": "all", "re": "\\bcrush(es|ed|ing)?\\b|\\bdestroy(s|ed|ing)?\\b|\\bkill(s|ed|er|ing)?\\b"},
    {"id": "shame", "cat": "grind", "scope": "all", "re": "\\bquitters?('s)?\\b|\\blazy\\b"},
    {"id": "address", "cat": "grind", "scope": "all", "re": "\\brookies?\\b|\\bbros?\\b"},
    {"id": "hierarchy", "cat": "hierarchy", "scope": "all", "re": "\\bathletes?\\b|\\bwarriors?\\b|\\belite\\b|\\balpha\\b|\\bsigma\\b|\\breal\\s+lifters?\\b|\\bleg[- ]day\\b"},
    {"id": "ableist", "cat": "ableist", "scope": "all", "re": "\\binsane(ly)?\\b|\\bcrazy\\b|\\bpsycho\\b|\\blame\\b|\\bcrippling\\b|\\bso\\s+ocd\\b"},
    {"id": "ableist-2", "cat": "ableist", "scope": "all", "re": "\\b(dumb|stupid|spaz|retard(ed)?|psychotic|schizo)\\b"},
    {"id": "urgency", "cat": "urgency", "scope": "all", "re": "\\blast\\s+chance\\b|\\bselling\\s+fast\\b|\\bdon'?t\\s+miss\\s+out\\b|\\bhurry\\b|\\bcountdown\\b|\\bonly\\s+\\d+\\s+left\\b"},
    {"id": "watched", "cat": "watched", "scope": "all", "re": "\\bwe\\s+noticed\\b|\\bwe'?re\\s+watching\\b|\\bnobody(\\s+here)?(\\s+is|'s)\\s+(looking|watching)\\b|\\ball\\s+eyes\\s+on\\s+you\\b|\\bshow(ing)?\\s+off\\b"},
    {"id": "infantilising", "cat": "infantilising", "scope": "all", "re": "\\bgold\\s+stars?\\b|\\bgood\\s+job,?\\s+buddy\\b|\\bhono(u)?rable\\s+mention\\b"},
    {"id": "whole-thing", "cat": "infantilising", "scope": "product", "re": "\\byou\\s+did\\s+a\\s+whole\\s+thing\\b"},
    {"id": "diet-cycle", "cat": "diet-cycle", "scope": "all", "re": "\\b(start|starting|come\\s+back)\\s+(on\\s+)?monday\\b|\\bnew\\s+year,?\\s+new\\s+you\\b|\\bresolutions?\\b"},
    {"id": "innuendo", "cat": "innuendo", "scope": "all", "re": "\\b(you|we)\\s+came\\b"},
    {"id": "ip-phrases", "cat": "ip", "scope": "all", "re": "\\bjudge?ment[- ]free\\s+zone\\b|\\bhot\\s+girl\\s+walk\\b|\\bcozy\\s+cardio\\b|\\bpilates\\s+princess\\b|\\blifting\\s+club\\b|\\bcatch\\s+(them|'em)(\\s+all)?\\b|\\bcollect\\s+them\\s+all\\b"},
    {"id": "trend-phrases", "cat": "ip", "scope": "all", "re": "\\bshy\\s*girl\\b|\\bgym\\s+besties?\\b|\\bgirl\\s?boss\\b|\\bgalentine'?s?\\b"},
    {"id": "rest-day-line-name", "cat": "ip", "scope": "names", "re": "\\brest\\s+day\\b"},
    {"id": "brain-day-line-name", "cat": "ip", "scope": "names", "re": "(?<!\\bevery\\s+day\\s+is\\s+)\\bbrain\\s+day\\b"}
  ]
}
```

In plain words: no body or food talk, grind or hierarchy words, ableist intensifiers, fake urgency, being-watched lines, infantilising praise, diet-cycle framing, innuendo, unverifiable product claims or IP-loaded and gendered trend phrases. "Quitter's Day" is a planning term only.

**Copy-lint** (`tests/unit/copy-lint.test.ts`). UI strings live in `content/*.json` as `{ "text": "...", "surface": "...", "speaker": null | "<characterId>" }`; `speaker` is set only for speech bubbles (copy *hosted* by a character stays `null`).

| Rule | Check |
|---|---|
| Exclamation marks | `count("!") ≤ 1` per string. Ollie's leading "oh!" does not count. |
| Caps | Count words matching `\b[A-Z]{2,}\b` after removing placeholders `\{[a-z_]+\}`, ignoring the acronym allowlist (XS S M L XL 2XL–6XL US USD UK EU FAQ SKU DTG DTF AOP OG PDF CSV TBC UPF GRS OEKO TEX). At most 1, and only when `speaker` is `sip` or `pippop` (Pop's half). Write "Zip code", never "ZIP". |
| Character voice (when `speaker` is set) | Lowercase. Mallow starts with `mm.` · Ollie starts with `oh!` · Tuck matches `^\(.*\)$` · Gus has no `!` · Sip (`sip`) and Pop (speaker `pippop`) may use the one CAPS word. |

**Scope rules** (banned words and copy-lint):
1. `/brand` content inside `data-copy-exempt` skips banned words **and** copy-lint; the attribute on any other route fails the test.
2. Policy pages (`/privacy/`, `/terms/`, `/shipping/`, `/returns/`) render the drafts inside `data-copy-surface="legal"`: the caps rule is skipped there; banned words still apply.
3. Text inside `<code>` is skipped by copy-lint; `scan:html` fails any `<code>` whose text doesn't match `/^[A-Z0-9-]{3,16}$|^[a-z0-9-]{3,24}$|^#[0-9A-Fa-f]{6}$/` (discount codes and hex values only).

**Example lines by surface** (cleared; use verbatim; `{…}` are data placeholders)

| # | Surface | Line |
|---|---|---|
| 1 | Hero headline | **Wear a friend to the gym.** |
| 2 | Hero subhead | Soft, heavyweight gym clothes starring a tiny crew of nervous, cheering gym equipment. Quiet or loud, your call. [Meet the crew] [Shop the Small Print] |
| 3 | PDP description (The Door tee) | Bel's first day was scary too. Now Bel rides along on your chest, about the size of a sticker, quietly rooting for you. Heavyweight garment-dyed cotton with a soft, lived-in feel. Same price in every size, {size_range}. Made just for you, so give it a few days. |
| 4 | Size-guide intro | Every body's welcome here, and every size costs the same. Lay a tee you already love flat, measure straight across the chest, and match it below. Between sizes? Size up for slouchy, down for snug. Still not sure? Ask us. A real person answers. |
| 5 | Add-to-cart toast | In the bag. Gus is thrilled (you can tell because he isn't). [View bag] |
| 6 | Empty cart | Nothing packed yet. No rush. Gus spent three years in a closet; he can wait. [Browse the Small Print] |
| 7 | Checkout success | Order's in. Pip & Pop are high-fiving about it. Each piece is made just for you, so it usually ships in {production_window}. We'll email the minute it's on its way. |
| 8 | 404 (hosted by Ollie) | Oh! This page isn't here. That's okay. I didn't know where anything was on my first day either. [Back to the shop] |
| 9 | Email signup (hosted by Bel) | **Want a First Visit Plan?** A free, step-by-step "what to actually do" guide for your first few gym visits, plus 10% off. One email a week, tops. [Send me the plan] · *maybe later* (closes on the first click) |
| 10 | Made-to-order note | **Made just for you.** We print each piece after you order, so there's no warehouse of leftovers. It usually ships in {production_window} and arrives about {transit_window} after that. Ordering a few things? They may come from different studios in separate boxes. |
| 11 | Payment error | Hmm, that card didn't go through, and nothing was charged. Try again, or use another card. Your bag's still packed. |
| 12 | Form-field error | That email looks like it's missing a bit. Check for the @? |
| 13 | Free-shipping bar | You're {amount} from free shipping. No pressure, it's just there if you want it. |
| 14 | Unavailable variant | This colour's taking a breather. Want a nudge when it's back? |
| 15 | Rest stamped (Mallow speaks) | mm. rest day stamped. it counts here. |
| 16 | After a gap (hosted by Gus) | Welcome back. Every stamp's still here; nothing was lost. Add today whenever you're ready. |
| 17 | Review request | How's it wearing? Tell us about the fit. A photo of it folded on a chair is perfect. No selfies needed. |
| 18 | Unsubscribed | You're unsubscribed. We'll still be cheering, just quietly. |
| 19 | Shipping delay | Heads up: your hoodie's taking a little longer than we said. New estimate: {date}. Sorry about that. We'll keep you posted. |
| 20 | Quiz intro | Which {castNoun} are you? Six questions, no wrong answers, and nobody's grading. |
| 21 | UGC prompt | show us your fit, your tote, your bottle. no strangers in frame, no bodies required. |
| 22 | Campaign lines | **New year, no pressure. No resolutions needed.** (launch line, Tue 5 Jan 2027; use exactly: it passes only through the `no resolutions needed` allow rule; [U] until the TESS/Etsy check) · "Rest, don't quit" (mid-January, Mallow Hours) · "Rest counts. Come back whenever." · "no resolutions needed". All are cleared for §5, §7 and §9. |

`{size_range}` is filled per selected colour from `BlankColor.sizes`; a copy test fails any `listing.copy` text matching `/\b(XS|S|M|[2-6]?XL)\s*[–-]\s*[2-6]?XL\b/` (no literal size ranges).

**Ten core slogans** (lowercase; [U] until the TESS/Etsy check; owner · design per §6.4.7–6.4.8):
1. the hard part was the door. (Bel · D01)
2. currently reading the little sticker on the machine. (Bel · D02)
3. off camera, on purpose. (Tuck · D03)
4. long time no gym. (Gus · D04)
5. day one: the sequel. (Gus · D05)
6. rest day. still on the team. (Mallow · D06)
7. proud of you. also, water. (Sip · D07)
8. i brought my buddy. / i'm the buddy. (Pip & Pop split pair · D08)
9. est. whenever you're ready (crest format · D09)
10. today: / sat in the car for a sec / went in anyway (Bel · D19, ships 2 Mar; checkboxes are drawn, never ☑ glyphs)

**Other lines**
- **Reserve** (benched; not on product in year one; the founder may promote one if a month needs a third design): "proof i showed up" · "special skills: re-racking / wiping the bench / quietly cheering for you" · "starting again counts as starting." · "slow days count too." · "you went. that's the whole thing." · "you're doing fine." Only "starting again counts as starting." and "slow days count too." may also appear in UI and social copy.
- **Held until the 10 Comeback-Dev interviews** (§2 decision 17); not on product, UI or social: "the nod club (we re-rack. we wipe. we nod.)" · "lightest on the rack. loudest cheer."
- **Still cleared** (product use only as printed in §6.4.7–6.4.8): "you went." and "okay. we're in." (the only lines tested to fit a hold-sign board [L]) · "gym towel (not for dishes)" · "i count visits. (that's it. that's the metric.)" · "you go, / i'll go too." · "moving at the speed of okay." · "showing up since {year} (with a few breaks)" (year picker only) · the menu and receipt lines as printed in §6.4.8.

**Replaced lines** (the banned list catches each old version): "we noticed" → "that counts" · "you came / WE came" → "you made it. / WE made it!" · "polite lifting club" is cut; no replacement ships · "Come back Monday" → "Come back whenever" · "flat days count too." → "slow days count too." · "re-rack, then snack." and "feed me (a snack, a rep…)" are cut · "oh! you did a whole thing!" is Ollie's UI only; the garment line is "oh! / you're here." (one "!", D20).

**Character voices** (canonical catchphrases; `voice.lines[]` also takes the character's lines above)

| Character | Voice rule | Lines (cleared) |
|---|---|---|
| **Bel** | Pep-talks itself in short sentences ("okay okay"); models courage, never panics *at* the reader | "okay. okay. we're in." |
| **Mallow** | All lowercase, slow, starts with "mm."; gives permission to rest | "mm. rest counts." · "mm. how about a rest day? it counts." (opt-in nudge only) |
| **Gus** | Deadpan, no `!`, closet jokes, never body-deprecating. The closet is a storage closet: no "coming out" or "out of the closet" puns in any Gus copy, skit or caption. | "long time no gym." · "starting again counts as starting." |
| **Pip & Pop** | One speaker id, `pippop`; alternate lines; Pip earnest, Pop goofy with one CAPS word at most | "pip: you made it. / pop: WE made it!" |
| **Sip** | One CAPS word, then a lowercase water reminder | "PROUD of you. also, water." |
| **Ollie** | Every line starts with "oh!"; easily impressed; the voice of the cheer wall | "oh! you're here!" (UI) · "oh! you did a whole thing!" (UI only) |
| **Tuck** | Whispers, always in parentheses; the consent-first ambassador | "(psst. you showed up. that counts.)" · "(psst. that counts.)" (short label fallback) |

### 4.5 Design tokens

**Feel:** 1970s campus-athletic merch meets a friendly sticker crew: chunky ink outlines, flat fills, a Cooper-style display serif, a hyper-legible sans, grown-up garments, bright little characters. **No gradients, no photoreal art, no black** (`ink` replaces it).

**Single source of truth:** `brand/tokens.json`. `npm run brand` generates CSS custom properties, the Tailwind 4 `@theme` block (§7.7) and `art/palette.ts`. A grep test fails on 6-digit hex literals outside `brand/tokens.json`, `print-specs.json`, `catalog/**`, `tests/**`, `BUILD-BRIEF.md`, `REPORT.md`, `docs/**`, `art/REVIEW.md` and generated files (`styles/tokens.css`, `art/palette.ts`, `golive/theme/assets/brand-tokens.css`, `print-files/manifest.json`, `out/`, `public/`). `app/manifest.ts` reads `theme_color`/`background_color` from `art/palette.ts`, and ported Appendix A code imports colours from it.

**Palette** (every cast member owns a colour, so the palette carries the cast even without a character)

| Token | Name | Hex | Role | Owner |
|---|---|---|---|---|
| `ink` | Night Ink | `#22263A` | Outlines, body text, primary buttons; blue-slate, softer than black | — |
| `oat` | Oat Milk | `#FFF7EC` | Page ground, sneakers, dark-garment sticker border, reversed text | Tuck's towel |
| `canvas` | Locker Canvas | `#F4EBDD` | Cards, alternate sections, input fills | — |
| `white` | White | `#FFFFFF` | Eye highlights; product-image tiles only | — |
| `coral` | Bel Coral | `#FF8A65` | Lead colour; secondary buttons, badges, favicon | **Bel** |
| `lilac` | Nap Lilac | `#CDB9F2` | Rest / Mallow Hours | **Mallow** |
| `bubblegum` | Bubblegum | `#FFB3C9` | Blush on emotional faces; buddy chips | **Pip** |
| `butter` | Butter | `#FFD86E` | Sparkles, toasts, stamps, highlights | **Pop** |
| `sage` | Locker Sage | `#A9BCA2` | Calm neutral; Dev colourways; quiet-tier UI | **Gus** |
| `pool` | Pool Day | `#8BD7E6` | Info states, sneaker stripes | **Sip** |
| `pistachio` | Pistachio | `#B9E3A3` | Success states | **Ollie** |
| `ink-soft` | — | `#4A4E66` | *Text only:* secondary text, captions, meta, card borders | — |
| `coral-deep` | — | `#B5432A` | *Text only:* links, error text; destructive button fill | — |
| `lilac-deep` | — | `#6A4FB0` | *Text only:* rest accents | — |
| `sage-deep` | — | `#4D6146` | *Text only:* success text | — |
| `pool-deep` | — | `#1D6A7A` | *Text only:* info text | — |
| `lilac-shade` | — | `#B8A0EA` | *Illustration only:* Mallow's end face; never UI | Mallow |

**Usage:** ≈ 70% `oat`/`canvas`, 20% `ink`, 10% cast colours (*inside characters, chips, stamps*, never big fills); purple + yellow never dominates (Planet Fitness). **No dark mode in v1**; dark *sections* (footer, Mallow Hours band) use `ink` grounds and the on-dark pairs below.

**Allowed text/background pairs** (WCAG 2.2 relative luminance, sRGB threshold 0.04045 [L, re-run 2026-11-10]; AA ≥ 4.5, AAA ≥ 7): the **only** permitted text pairings; `tests/unit/contrast.test.ts` recomputes every row from `tokens.json`.

| Text on background | Ratio | Use |
|---|---|---|
| `ink` on `oat` / `canvas` / `white` | 14.06 / 12.64 / 14.93 | Body text and headings / cards / product tiles |
| `ink-soft` on `oat` / `canvas` / `white` | 7.68 / 6.91 / 8.16 | Secondary text, captions |
| `coral-deep` on `oat` / `canvas` / `white` | 5.20 / 4.68 / 5.52 | Links, error text (never on `butter` or pastels) |
| `lilac-deep` on `oat` / `canvas` | 5.89 / 5.29 | Rest accents |
| `sage-deep` on `oat` | 6.35 | Success text |
| `pool-deep` on `oat` | 5.82 | Info text |
| `ink` on `coral` | 6.45 | Secondary button label, badges |
| `ink` on `butter` / `lilac` / `bubblegum` / `sage` / `pool` / `pistachio` | 10.88 / 8.40 / 8.92 / 7.40 / 9.22 / 10.37 | Toasts, stamps / rest, buddy, quiet-tier chips / info, success banners |
| `oat` on `ink` | 14.06 | Primary button label, footer, dark sections |
| `butter` on `ink` | 10.88 | Headings on dark sections |
| `coral` on `ink` | 6.45 | Accent text on dark |
| `lilac` / `pool` / `pistachio` / `bubblegum` / `sage` on `ink` | 8.40 / 9.22 / 10.37 / 8.92 / 7.40 | Accents and links on dark sections |
| `oat` on `coral-deep` | 5.20 | Destructive button label |
| *Must FAIL (test asserts):* `coral` / `sage` / `butter` on `oat` | 2.18 / 1.90 / 1.29 | **Pastels and coral are never text on light grounds** |

**Non-text contrast** (WCAG 1.4.11, 3:1): every cast fill is **below 3:1 on `oat`** (1.29–2.18), so **the `ink` outline is mandatory** on every character, icon, chip and stamp (ink vs each fill 6.45–10.88). Cards (`canvas` vs `oat` 1.11) get a 1.5px `ink-soft` border (7.68) or a 2px `ink` border. Focus ring: 3px `ink` (14.06), 2px `oat` offset; on dark sections 3px `butter` (10.88).

**UI component map:** primary button `ink` fill, `oat` label, pill, sticker shadow · secondary `coral` fill, `ink` label, 2px `ink` border · tertiary `oat` fill, `ink` label, 2px `ink` border · error `coral-deep` text **plus an icon** on `oat` (never colour alone) · success `pistachio` banner, `ink` text + icon · info `pool` banner, `ink` text · toast `butter` fill, `ink` text, 2px `ink` border · disabled `canvas` fill, `ink-soft` text, `aria-disabled`, plus a line saying why.

**Garment × ink pairing.** Garment hexes and light/dark flags: §5.2; the validator computes every contrast (live `color_code` first) and fails any primary element below 3:1 against its garment. It also enforces:
1. **Light colourway** (`ink` ≥ 4.5:1): ink outlines and text, cast fills inside; `oat`/`white` **export transparent** (sneakers show the garment colour; accepted).
2. **Dark colourway** (flag D: `ink` < 3:1, plus Blue Jean): the oat **sticker border** (§4.7); text `oat` or `butter`; `coral` text only at display size on Navy or Espresso.
3. **Same-hue:** a character whose body fill is below 1.2:1 on the garment isn't the hero there (pick another, or tonal ink line art).
4. **Range:** at least **half of each drop's garment colours are neutrals** (flag N); pastels accent, never the rack.
5. **Persona colourways:** Dev: Bay, Sage, Ivory, Espresso, Pepper, Blue Jean · Frankie, Priya: Ivory, Blossom, Chalky Mint, Orchid, Butter · Duo: Butter + Chalky Mint, Blossom + Bay.

**Embroidery.** Thread map: §6.3.2; unlimited colour is off (§2 decision 20).
- No pastel threads exist.
- The standard Bel face (hat, chest icon) is **2 threads** on light garments (Navy line + Orange body; Navy on khaki 6.0:1) and **3** on dark (White sticker outline + Orange body + Navy features; Navy on Orange 3.21, White vs Orange 3.62) [L].
- The **wordmark is never embroidered under 5.3 in wide** (Caprasimo's smallest counter at 4 in ≈ 0.036 in, under the 0.05 in gap minimum [L]); hats, left chest, sleeves, beanies get the **Bel icon**.

**Typography.** Two families only (not Fredoka: kids'-app feel; Gluten: closes counters; Caveat: too thin), self-hosted, no runtime CDN (§3 rule 17). Pins: print TTFs §6.1, web WOFF2 §7.1; both OFL-1.1 [V]. Text-to-path: §6.1 pitfalls 1–3.
- **Display: Caprasimo 400** (Cooper-style soft serif): wordmark, web H1–H3 (**≥ 28px only**), slogans, quiz result titles, hero prices.
- **Body / UI: Atkinson Hyperlegible Next** (400, 400 italic, 700, 800; variable 200–800): body, UI, buttons, labels, size charts, inside labels, receipt/menu formats.

**Web type scale** (base 16px; body 18px; measure 60–70ch; sentence case except `eyebrow`)

| Token | Family / weight | Size | Line-height | Tracking |
|---|---|---|---|---|
| `display` | Caprasimo 400 | `clamp(2.75rem, 6vw, 4.5rem)` | 1.05 | −0.01em |
| `h1` | Caprasimo 400 | `clamp(2.25rem, 4.5vw, 3.25rem)` | 1.1 | −0.01em |
| `h2` | Caprasimo 400 | `clamp(1.75rem, 3vw, 2.25rem)` | 1.15 | 0 |
| `h3` | Caprasimo 400 | 1.75rem (28px: the Caprasimo floor) | 1.2 | 0 |
| `h4` | Atkinson 800 | 1.25rem | 1.3 | 0 |
| `eyebrow` | Atkinson 800, uppercase via CSS | 0.875rem | 1.3 | +0.08em |
| `body-lg` | Atkinson 400 | 1.25rem | 1.5 | 0 |
| `body` | Atkinson 400 | **1.125rem (18px)** | 1.55 | 0 |
| `small` | Atkinson 400 | 1rem (16px: the floor for running text) | 1.5 | 0 |
| `meta` | Atkinson 700 | 0.875rem (14px; labels and legal only) | 1.4 | +0.02em |
| `button` | Atkinson 700 | 1.125rem | 1 | 0 |
| `price` | Atkinson 800, `tabular-nums` | 1.25rem | 1 | 0 |

**Print type minimums**, measured from glyph outlines at x-height 200 px [L] against §6.2's minimums [U until sampled]; the validator recomputes them from the real paths.

| Font | Smallest counter | Thinnest stroke | Min x-height, DTG/DTF | Min x-height, embroidery (gap ≥ 15 px) |
|---|---|---|---|---|
| Caprasimo 400 | 0.09 × x-height | 0.12 × x-height | **200 px (0.67 in)** | 167 px (0.56 in); large front only |
| Atkinson Hyperlegible Next 800 | 0.17 × x-height | 0.14 × x-height | **110 px (0.37 in)** | 90 px (0.30 in) |

- Caprasimo slogans are **Loud only** (front or back, ≥ 8 in wide), broken onto 2–3 lines. Garment and embroidery minimums: §6.2; wordmark minimums: §4.6.
- **Inside neck labels:** Atkinson 800 only, never Caprasimo. Layout and sizes per §6.3.1 (icon box 375 px at Icon LOD, whisper x-height 30 px ≈ 0.14 in cap, y 640–900 left empty for Printful's auto-filled size, fibre and origin). **No size letter in our art.** If a sample's counters fill in, use "(psst. that counts.)".
- **Auto-fit rule** (every slogan generator): measure the advance width with opentype.js, scale to ≤ 86% of the frame's inner width (capped at the design's max size), and **fail the build** below the minimum x-height. Sign-board test [L]: "you went." and "okay. we're in." fit; "long time no gym." and "the hard part was the door." **fail, as designed**; long lines go in a text block.

**Radius, shadow, spacing, layout:** `radius-pill` 999px (buttons, chips, toggles) · `radius-card` 20px (cards, modals) · `radius-tile` 24px (product tiles) · `radius-input` 14px · `radius-icon` 23% of width (rx 56 on 240) · `shadow-sticker` `0 3px 0 0 var(--color-ink)` on buttons and interactive cards with a 2px `ink` border (`:active`: none plus `translateY(3px)`; never blurred; none on static content) · `space-*` 4, 8, 12, 16, 24, 32, 48, 64, 96, 128 px · max width 1200px; section padding 64–96px (48px mobile); product grid 2 / 3 / 4 columns (mobile / tablet / desktop), 24–32px gaps; touch targets ≥ 44×44px. No sharp corners except 4-point sparkles.

**Iconography:** Lucide (ISC), pinned in §7.1: stroke 2.25 on a 24 grid, round caps and joins, `ink`, optional single cast-colour fill; 24px (20px inline). **Custom icons:** stamp; tiny kettlebell (from the solid bell); sneaker; rest-moon with a "z"; buddy pair (two overlapping circles); quiet / loud (speaker with 0 / 3 arcs); private (a tag); off camera (camera with a heart lens). **Banned:** eyes or "watching" glyphs, recording dots, crossed-out eyes, crosshairs, skulls, flames, lightning bolts, scales, tape measures, trophy-plus-pill "achievement" toasts. Icon-only buttons need an `aria-label`.

**Illustration rules ("Chunky Ink")**
1. One `ink` outline: 6 units on the 240 grid (face strokes 5), round joins and caps; LOD swaps §4.7; print minimums §3 rule 12.
2. **Flat fills only** (§3 rule 12); the only "depth" is misregistration (an ink duplicate offset +6/+6 behind type).
3. Per character: body, one accent, `ink`, `oat`, a `white` eye highlight, plus blush only when the expression calls for it.
4. **Recognisable gym objects** from circles, rounded rects and one or two cubic paths; no noses, ears, tails, wings or belly symbols; rubber-hose tube arms, round hand nubs (no fingers or gloves).
5. Everyone wears **the same chunky `oat` sneakers** with a coloured sole stripe; **expressive eyebrows**; **blush is an emotion**, not makeup.
6. Props: 4-point `butter` sparkles, motion ticks, path-drawn "z"s, `pool` sweat drops (nerves or effort, **never pain**), sign boards, stamps, doorways, lockers.
7. Never-draw list: §4.7 usage rules.
8. One ground line; group overlaps ≤ 15% of a body width; **≤ 3 characters on a Loud design** (all 7 only on posters and sticker sheets).
9. Formats are character-led, never food: crest, menu board, receipt, tea-towel layout (D09, D17, D24, D25).

**Motion:** UI 120–200ms `cubic-bezier(.2,.8,.2,1)`; character reactions 240–320ms; no parallax, scroll-jacking, auto-advancing carousels or sound. Celebrations are **earned by an action**, never ambient (a stamp landing: 1.1× scale-in plus a butter sparkle; the Pip & Pop high-five on order success); max 2 bounce cycles; nothing flashes more than 3 times a second (WCAG 2.3.1) or loops past 5 s without a pause control (WCAG 2.2.2). `prefers-reduced-motion: reduce`: instant pose swaps, ≤ 1ms opacity transitions, static sparkles, via a global CSS block **and** a `useReducedMotion()` guard in `<CastMember>`; e2e runs once with reduced motion emulated. Loading: Sip bouncing (600ms cycle); reduced motion: a static Bel "reading the little sticker" plus "Loading…".

### 4.6 Logo system

All rendered and checked [L]; regenerated from code (A.5), never by hand.

**Wordmark:** `wordmarkText` in **Caprasimo 400**, outlined per glyph (`charToGlyph`), tracking −0.01 em plus kerning, `ink`. **Measured** [L]: advance 4.743 em, x-height 0.500 em, cap height 0.700 em (UPM 2048, sxHeight 1024, sCapHeight 1434).
- **Tittle swap:** the last `i` becomes the dotless ı (U+0131); the **mini-Bel** (≈ 0.30 em tall with its handle, 0.07 em above the stem) takes its dot (A.5 `wordmark()`). Unit test for "kettlekin": stem centre 3.885 em from the left edge, bell centre 0.730 em above the baseline (±0.005 em). **No i/j** (e.g. Huddlebell): no swap; use the horizontal lockup.
- **Clear space:** 0.35 em (0.5 × cap height) on all sides, from the bell top and glyph extremes.
- **Minimum widths:** 240 px on screen with the bell face; 120 px with a faceless bell [L]; **6.3 in** on DTG garments (counter rule, §4.5); 1.5 in on paper and stickers; **5.3 in** for embroidery, large front only. Below these, use the icon.

**Mini-Bel** (A.5 `miniBel()`, fixtures): `color` on light grounds (coral, `ink` outline) · `reverse` on dark (outlines `oat`, eyes `ink`) · `solid` for one colour, foil, emboss or one-ink DTG: **no outline**, a **wide, low handle** keeps the window open (a narrow, tall shackle read as a padlock [L]), never a face.

**Icon mark** (avatar, app icon, inside labels, embroidery source; ≥ 64 px or ≥ 1.25 in; A.5 `iconMark()`, fixtures): Bel's handle and body with the *happy* face (no blush, arms or feet) in a rounded square: rx 56 on the 240 grid, `oat` fill, 6-unit `ink` border.

**Favicon** ("Bel peek" crop, 16–48 px; A.3): the bell fills the square, cropped flat at the bottom (no padlock or ghost); legible at 32 and 48 px, passable at 16 [L]; no smile below 32 px. Ship `favicon.svg`, `favicon-32.png`, `apple-touch-icon.png` (180 px, full icon), `icon-maskable-512.png` (full icon on `oat`, 20% safe padding).

**Lockups:** wordmark only (site header) · **horizontal:** icon at height H, gap 0.5 H, wordmark at S = 0.64 H optically centred, with a **plain "i"** [L] · **stacked:** icon above the wordmark, gap 0.25 H (paper, stickers, future packaging). **Colours** [L]: primary `ink` + `color` bell · reversed `oat` + `reverse` bell · one-colour `ink` or `oat` + `solid` bell · embroidery: Bel icon only.

**Never:** recolour the bell (always `coral`), add a face to the solid bell, use a pastel ground (only `oat`, `canvas`, `white`, `ink`), or outline, shadow, stretch, rotate, re-set it or place it on a character. **Visual review** (§3 rule 15): the solid bell at 120 px and the 24 px kettlebell icon read as kettlebells, not padlocks (else widen the handle); the 16 px favicon is not a ghost.

### 4.7 The cast (character system)

**The equipment is the cast:** what beginners fear on the gym floor becomes small, nervous friends who cheer for you, **each defusing one researched anxiety trigger**. Collective noun: `castMemberNoun` ("Collect the crew", never "catch them").

**Tiers:** **Lead** Bel (logo, favicon, hero tee, onboarding) · **Core** (launch products) Bel, Mallow, Gus, Pip & Pop · **Supporting:** Sip, Ollie and Tuck appear in UI states, the sticker sheet and one product design each: Sip = D07 bottle (launch), Tuck = D03 Off Camera, On Purpose tee (launch), Ollie = D20 tee (2 Mar). Tuck also voices the inside-label whisper; the D25 towel uses his voice without drawing him · **Future, by vote only** (≤ 1 a year): **Cora** the cable machine ("everyone's scared of her; she's actually really nice") vs **Skip** the jump rope; spec only.

| Character | Object | Colour tokens | Personality | Trigger (internal) |
|---|---|---|---|---|
| **Bel** | Kettlebell | `coral` body and handle; `pool` sole stripes | Nervous-but-brave first-timer who pep-talks itself | Being new; not knowing what to do |
| **Mallow** | Foam roller, lying down | `lilac` body, `lilac-shade` end face; `butter` stripes | Sleepy, cosy recovery expert | Rest guilt, burnout |
| **Gus** | Barrel gym duffel | `sage` body, `coral` handle, `butter` grip wrap and zip pull; `coral` stripes | Deadpan returner; three years in a storage closet | Feeling "behind" after a break |
| **Pip & Pop** | **One** hex dumbbell, a face on each plate | Pip `bubblegum` + `coral` sweatband; Pop `butter` + `pool` sweatband; `oat` bar | Inseparable; Pip sincere, Pop goofy | Nobody to go with |
| **Sip** | Straw-lid water bottle | `pool` body, `butter` cap and loop; `coral` stripes | Hype friend with a water reminder | Feeling unseen |
| **Ollie** | Bumper plate on edge; the hole is its mouth (always amazed) | `pistachio`; `coral` stripes; `butter` sparkles | Easily impressed; voice of the cheer wall | Needing validation |
| **Tuck** | Hand towel over a locker rail | `oat` towel, `coral` + `pool` hem stripes, `sage` rail; `pool` stripes | Shy, whispers; **the consent-first ambassador** | Being watched or filmed |

`persona`: §4.3 (Sip: gift buyers; Ollie: all).

**Silhouette rules and misread fixes** (each fix rendered and checked [L]; hard rules)

| Character | Must-have silhouette features | Misread → fix |
|---|---|---|
| Bel | Arched handle tube over a body with a **flat base**; tube arms; sneakers | Ball / Kirby / padlock → handle, flat base, coral (never pink or red-footed) |
| Mallow | Long body, **5 grip nubs** on top, two grooves, **visible end face (ellipse) with a hollow `oat` core** on the right, flat ends; lying down; no arms by default | Pill capsule → nubs, end face, hollow core, flat ends |
| Gus | **One** carry-handle arch with a `butter` grip wrap; dashed zipper; zip pull; curved end seams; slightly tapered barrel | Bunny ears (two handles) → one handle, grip wrap |
| Pip & Pop | Two **rounded hexagon plates, flat side down** ("we don't roll away"); short knurled `oat` bar; sweatbands across the plates; outer arms only | Tall rounded rectangles → hex plates |
| Sip | Straw loop on top, wide `butter` cap, tall rounded body, 3 measurement ticks on the right edge | — |
| Ollie | Big circle plate with an **inner rim ring**; the hole *is* the mouth, never changes | Donut → rim ring |
| Tuck | Towel on a long `sage` rail; front-flap edge with a `pool` stripe; `coral` + `pool` hem stripes; terry-fringe ticks; dangling sneakers; **no visible hands** | Paper cup, soap dispenser, goggles → towel-on-rail v3 |

**Geometry: Appendix A.5 (port it; don't redraw by eye):** 240 grid (ground y 216, centre x 120), tubes, sneaker, face kit, anchors and poses, pinned by the fixtures.

**Expressions (10)**, verified on Bel [L]: happy (default), nervous, proud, sleepy, hyped, surprised, determined, shy, chill, trying. Only nervous, proud, hyped and shy blush (`bubblegum`; `coral` on Pip & Pop); nervous and trying add a `pool` sweat drop (never pain).

**Poses:** idle, wave, cheer and hold-sign are in A.5 [L] (hold-sign hands never cover text). Spec only (build, render and inspect per §3 rule 15 before use): **peek** (top 55% visible, both hands gripping the print or screen edge; sleeve and back-neck prints, chat bubble) · **high-five** (inner arms of two characters meet overhead, `butter` sparkle at contact; order success) · **nap** (Mallow native; others rotated 90° onto a `lilac` mat rect) · **sit** (sneakers forward, toes up, body lowered 10) · **walk** (body −4°, rear sneaker +15° and lifted 6; hero banner) · **carry** (a mini Gus at scale 0.35 by the handle; tote) · **stamp** (one arm pressing a `butter` stamp, an `ink`-outlined rect plus knob; stamp-card UI) · **hide** (Tuck behind its flap, others crouched behind Gus; Quiet tier).

**Level of detail.** One grid unit = canvas width ÷ 240; print minimums per §6.2 [T/U]; the validator enforces the LOD per file.

| LOD | Canvas width | Changes | Check |
|---|---|---|---|
| **Full** | ≥ 3.0 in (≥ 900 px; 3.75 px/unit) | Everything | Outline 22.5 px, face 18.8 px, highlight 19.5 px ✓ |
| **XS** | 1.5–3.0 in | Outline 9, face strokes 7, sole stripes 5. **No highlights, no lace ticks.** | 1.5 in: outline 16.9, face 13.1 px ✓ |
| **Icon** | 1.25–1.5 in (inside labels) | Body and handle only. Outline 10; eyes only, rx 11 ry 14. | 1.25 in: outline 15.6 px ✓; **never smaller** |
| **Embroidery** | ≥ 2.0 in | Icon geometry; outline 10; face strokes 7; eyes rx 9 ry 12; no highlights. Blush (Flamingo) only if the expression needs it. ≤ 3 threads. | 2 in: outline 25, face 17.5 px ✓ |
| **AOP motif** | 6 in tile | XS rules; year-one seamless patterns (D16, D21, D23) at a fixed 6 in tile scale; no tossed heads, no text | §6.3.3 |

**Sticker border** (dark garments, [L] on Espresso; A.5 `halo()`): under the art, an all-`oat` copy with strokes +16 units (unstroked shapes get a 16-unit stroke); normal art on top. On every garment flagged D in §5.2; also the **sticker cut line** (Printful adds its own white border [T]). `oat` prints over the white underbase (light garments: §4.5 rule 1).

**Data model and component** (one source for site and print):
- `art/characters/characters.json`: `{ id, name, object, tier, colors: { body, accent, stripe, blush }, anchors, defaultExpression, defaultPose, allowedPoses, voice: { rule, lines[] }, trigger, nervousBit, persona, altObject }` per character.
- `nervousBit` (customer-facing `CopyString`): Bel "not knowing what to do yet." · Mallow "feeling bad about taking a rest day." · Gus "feeling behind after a break." · Pip & Pop "having nobody to go with." · Sip "wondering if anyone's in your corner." · Ollie "wondering if small wins count." · Tuck "worrying about being filmed." The character page renders "The nervous bit: {nervousBit}"; `trigger` stays internal and is shown on no page (About included).
- `<CastMember id expression pose lod garment size title />` in `components/cast/CastMember.tsx` (never named after the brand: §4.1 name grep) renders inline SVG; the same generators feed resvg + sharp in print.
- Alt text: "{name} the {altObject}, {expression}, {pose}" ("Bel the kettlebell, nervous, waving").

**Usage rules**
- **Do:** consistent voices (§4.4); one character per social reply; let them be scared, sleepy, wrong or unbothered; every interaction opt-in.
- **Don't:** a character who shames, nags, guilts, diets, weighs itself, compares bodies, gets injured or cries from pain; filming or being filmed without consent; numbers on Bel, plates or any weight; romance or sexual jokes; human bodies, noses, ears, tails, belly symbols; scales, tape measures, food as reward or punishment, skulls, wolves, flames, real people or logos.
- **Never recolour a character** (seasonal colourways recolour garments): every fill in a character's output is in its own tokens ∪ {`ink`, `oat`, `white`, blush} (test). **≤ 3 characters on a Loud garment** (test). The founder, as "mascot guardian", signs off every new pose and line.

**Resemblance-avoidance list.** Before any new character or pose ships, ask: could a stranger mistake it for one of these? An IP lawyer reviews the final model sheets.
- **Kirby:** Bel is coral with a handle, flat base, tube arms, white sneakers; never a pink ball with red feet.
- **Mr. Men / Little Miss:** real gym objects; outlined colour tubes, not black stick limbs; no noses.
- **Duolingo's Duo:** no birds, no green lead, no white-sclera eyes.
- **Sanrio, Pusheen, Molang, Cinnamoroll; Etsy gym animals (frogs, capybaras, skeletons):** no animals or skeletons; expressive eyebrows; no bows; no "w" mouths; blush only for emotions.
- **Sumikko Gurashi:** chunky 6-unit ink outline, object silhouettes, sneakers (not thin-line pastel blobs).
- **Care Bears:** no symbols on bodies.
- **Pokémon object creatures; "Mallow" the trial captain:** no powers or evolutions, no "catch" vocabulary, never register "Mallow".
- **Shopkins:** gym domain only, adult voice, rubber-hose plus sneaker construction.
- **Moshi Monsters' Moshlings:** no "-lings" cast naming, no "collect them all".
- **Gymshark:** no sharks or fins, no "G" shields, no "Lifting Club".
- **Nike swoosh:** no slash or score marks on the bell or any chest logo.
- **Xbox achievement toast:** stamps and sign boards, never circle-plus-pill trophy toasts.

### 4.8 Community mechanics (rules; implemented in §7)

Brand rules; §7 implements them (prototype: local-only `localStorage` + JSON seeds; moderation, email and orders stubbed).

| # | Mechanic | Rules (each "never" is a test) |
|---|---|---|
| 1 | **Bel's Stamp Card** (rest counts) | Stamp a **visit** (Bel) or a **rest day** (Mallow); both count fully. Show **showed-up weeks** (≥ 1 stamp) and **total stamps**; **neither ever decreases**: no streak or broken-streak state; a gap shows only the welcome-back line (§4.4 #16). The **day-one line** marks where you started; the meter never falls below it. **Weeks, not days.** Only the user's "Clear my card" (tap plus confirm) lowers them. |
| 2 | **Milestones and Firsts** | Milestones at **1, 5, 10, 25, 50, 100** stamps unlock digital stickers. Six self-reported **Firsts**: First Visit (Bel) · Asked for Help (Ollie) · First Class (Pip & Pop) · Tried the Weights Area (Gus) · Rested on Purpose (Mallow) · Came Back (Gus); each gives a code for that **physical sticker, $0 with any order** (prototype: a mock code). **No gold stars, ever.** |
| 3 | **Mallow's rest nudge** | **Opt-in, off by default.** After ≥ 6 visit stamps in 7 days with no rest stamp: "mm. how about a rest day? it counts." Nothing else comments on frequency. |
| 4 | **Privacy and reminders** | Local-first, deletable in one tap; reminders opt-in, ≤ 1 a week, never guilt or missed-day counts (prototype: a toggle; nothing sent). |
| 5 | **"Which {castNoun} are you?" quiz** | Six questions → **Bel, Mallow, Gus, Pip & Pop** (buddies), **Sip** or **Tuck**; the result card shows products, the **First Visit Plan** and 10% off. **Result before any email ask; email optional.** Target ≥ 5% capture [T]. |
| 6 | **Quiet / Loud / Private** | A PDP toggle, default Quiet. **Quiet:** chest hit or back-neck print. **Loud:** big front or back. **Private:** inside label only (tees only). **The Small Print** is the Quiet collection and the Bel and Tuck quiz landing page. |
| 7 | **Buddy System** | **Split tees:** Pip on tee A, bar running off the right edge; Pop on tee B, bar entering from the left; together, one dumbbell. **Buddy Pack:** an A + B pair, −$8 ($60, §5.7). **Bring a Buddy:** a share link; *both* get the Collect the Crew sheet (or 15% off). |
| 8 | **Start a Crew** (demo) | 2–8 people, a crew name, a crew page with a **combined stamp total**; one shared checkout link, own sizes; optional **personalised crew-back hoodie**. Names and hoodie text: `A–Z 0–9 space . ' -`, ≤ 16 characters, past the profanity/brand-name blocklist and banned list; personalised orders go to **draft-order review**. |
| 9 | **Cheer wall** (demo) | Prompts "Today I…", "First time I…", "Came back after…"; ≤ 140 characters; banned list. **No free-text comments**: one-tap "proud of you", "same!", "you've got this", Ollie's "oh!". Photos: **objects and outfits laid flat only**. Report, moderation queue, blocklist (stubbed). |
| 10 | **Consent-first filming** | A Tuck-hosted policy page, linked from the footer, the wall and every UGC form. **We never film strangers.** UGC: fits and gear laid flat, or self-filmed alone in frame; never bystanders, body or progress photos. 13+. Prompt: §4.4 #21. |
| 11 | **Send a Bel** (e-card) | Free e-card for someone starting the gym: "Wear a friend to the gym." plus a custom first line (auto-fit, banned list, ≤ 60 characters by default); upsells to a gift order whose note covers the made-to-order wait. Prototype: local render, copyable link, nothing sent. |
| 12 | **First Visit Plan, "Meet the Machine"** | A free printable plan narrated by Bel: what to bring, three machines you'll recognise, what to do if it's busy. **Meet the Machine** is narrated *by the equipment*, diagrams only, never bodies. No unsolicited advice. |
| 13 | **Made just for you** | Partner-data production and transit windows on PDP, cart, checkout and emails; a split-shipment note; delays announced proactively (§4.4 #19). |
| 14 | **Side Quests and votes** | Monthly drops of 1–3 designs (17 in year one; calendar §5.6). Members vote on the **next seasonal colourway** and yearly **next crew member** (prototype: local). **Slogan Lab:** an IP-licence checkbox and the banned list; Slogan Lab is 18+ ("I'm 18 or older" checkbox); credit by handle only, opt-in. |
| 15 | **Seasonal colourways** | Named *garment* colourways (characters never recoloured): **Mallow Hours** (Jan–Feb, Orchid + Ivory; "Rest, don't quit") · **Pool Day** (Apr–May, Chalky Mint + Chambray) · **Golden Hour** (Jul–Aug, Butter + Bay) · **Sweater Weather** (Oct–Nov, Espresso + Pepper + Sage, sticker borders). Dates: §5.6. |
| 16 | **"showing up since {year} (with a few breaks)"** | Personalised tee; **year picker only**; off at launch (§2 decision 15). |

**Navigation:** by **vibe** (The Small Print · Meet the Crew · Buddy System · Mallow Hours · Side Quests) and **product type**; **never by gender**.

### 4.9 Brand don'ts

Review items; (T) = also an automated test.
1. **Don't** show human bodies on product, or before/after, progress photos, physique imagery or "fitspo". (T: no people images in `public/`)
2. **Don't** frame food as reward or punishment: no bakery or food master metaphor, no bread words for bodies. (T)
3. **Don't** build streak breaks, red "you missed a day" states, guilt notifications or countdown timers. (T: stamp invariants; no countdown component)
4. **Don't** tell customers to watch, rate, correct or film strangers, say "we noticed" or promise "nobody's looking"; no stranger-directed rituals. (T)
5. **Don't** give unsolicited form, frequency or body advice. Help only when asked.
6. **Don't** use skulls, wolves, sharks, flames, lightning, blackout palettes, camo, or "athlete / warrior / elite" language. (T for the words)
7. **Don't** autoplay sound, loop motion past 5 s, ignore `prefers-reduced-motion`, or make any celebration flash. (T for reduced motion)

Also enforced by tests: banned list and copy-lint (§4.4), contrast pairs (§4.5), print rules (§3 rules 12–13, §6.6), cast rules (§4.7 usage), never by gender (§4.3, §2 decision 7), the name literal (§4.1), resolution framing (§4.4 banned list).

---

## 5. Product catalog

**What we sell, how each item is identified, what it costs and what it earns.** `npm run catalog` compiles this into `catalog/catalog.json` (D3). Every number is a tagged **snapshot**; the build swaps in live partner data when it can and keeps the tag honest when it can't (§3 rules 4 and 7). The 30 designs (D01–D30, art in §6) are fixed; this section maps them onto products, collections and drops. Paths: §10.1.

### 5.1 Sourcing strategy

| Partner | Year one | Why | Tag |
|---|---|---|---|
| **Printful** | Everything, inside labels included | Owned US/EU facilities, the most consistent quality, the deepest Shopify sync (4.8★); catalog, pricing, size-guide and mockup APIs. **Draft orders are not charged** (only confirmed ones). | [V] rating, plans; [T] draft billing |
| **Printify** | **Nothing.** No Printify account and no Printify exporter in year one; add one only if the founder approves the shaker. | The 24 oz protein shaker (M.i.A Merchandise, provider #80, ≈ $13.98) is **deferred**: it ships as a separate parcel and leans toward protein/diet culture. | [T] |
| Gelato, Gooten, Spreadconnect, Apliiq, Prodigi | Not used | No activewear (Gelato), weak reputation (Gooten, 2.7–2.8 Trustpilot), inconsistent quality (Spreadconnect); Apliiq: maybe a v2 woven-label capsule. | [T] |

**Rules**
1. `Blank.partner` is `"printful"` for every blank (catalog test).
2. **Split shipments:** items from different Printful facilities (AOP, drinkware, embroidery) may arrive separately [U], so the PDP and cart always show the made-to-order note (§4.4 line 10) with its "separate boxes" sentence; §8 reads real splits from shipment data.
3. **Production time:** "most products in 2–5 business days" [V]; partner-made AOP synthetics 3–7 days [V]. `Blank.productionDays` feeds `{production_window}`; never hard-coded.
4. **Printful Growth** ($24.99/mo, 14-day trial, free for a year once yearly sales pass $12K; 25% off samples; 9% off branding; "up to 33% off custom premium products") [V]; which blanks get the 33% is **[U]**. Start on **Free** (§2 decision 12); switch when `Σ(base spend × blank discount) + 0.09 × label spend > $24.99`, measured in the trial (§5.7).
5. **Inside labels:** ≈ **$0.99 each** [T] (one source: $0.99–1.25 [T]); tear-away-label garments only, **never fleece** [T]; Printful auto-fills size, fibre and origin [T]; **priced separately even as the only placement** [T: Printful v2 pricing notes]. So:
   - Every eligible tee (`cc1717`, `bc3001`) carries the D13 default whisper and `labelCost = $0.99` on every variant (default; cheaper option: labels on Private only; log the choice in `docs/decisions.md`).
   - **Private** = no outside print + that design's whisper on the label. **Tees only.** Base = garment + label. Whether Printful accepts a label-only product, and whether both tees are label-eligible, is **[U]**: confirm both live; if either fails, drop Private from that blank and log it.
6. **No black garments, no 3D puff, no unlimited-colour thread, no outside labels, no pack-ins** in year one (§5.3, Not in year one).

**Pull LIVE vs seed.** Endpoints: Printful v2 OpenAPI via the community SDK `printful-sdk-js-v2@2.2.0-beta` [T]; whether catalog GETs need a token is [U]. Per §3 rule 6, `npm run catalog:pull` without `--live` and `PRINTFUL_TOKEN` only reads the committed snapshots in `catalog/live/printful/` (each with `checkedAt`); the founder runs the live pull once accounts exist (§8).

| Data | Live source (`…` = `GET /v2/catalog-products/{id}`) | Seed | If unreachable |
|---|---|---|---|
| Product id, name, techniques, placements | `…` (= product-page id? [U]) | §5.3 | keep id, tag [U]; an `export:*` blocker |
| Variant ids, exact colour names, `color_code`, sizes per colour | `…/catalog-variants` | §5.2 | approx hex [U]; validator warns |
| Price per variant × technique; extra placements | `…/prices` (+ `/v2/catalog-variants/{id}/prices`) | §5.3 | `marginBasis: "planning"` |
| **Size chart** | `…/sizes` | **none: never invent one** | "TBC"; can't be `active` |
| Print areas, templates | `…/mockup-templates` + File guidelines tab | §6 canvases | `verified: false` |
| Stock · shipping rates | `…/availability` · `POST /v2/shipping-rates` (store token [U]) | — · §5.3 | `"unknown"` · estimates stay [U] |

Designs, listings, tiers, chosen colours, prices, bundles, collections, drops and copy are ours, seeded here.

### 5.2 IDs & SKU scheme

IDs never contain the brand name (rename-safe, §4.1). Regexes: `lib/catalog/ids.ts`; `tests/unit/catalog-ids.test.ts` checks every compiled ID.

| Thing | Format | Regex | Example |
|---|---|---|---|
| Design (+ buddy half `A`/`B`, e.g. `D08B`) | `D01`–`D30` (lineup numbers; D31+ reserved) | `^D(0[1-9]\|[12]\d\|3[0-9])$` | `D08` |
| Product key (blank) | lowercase; = `designs.json` `products[].blank` | `^[a-z0-9]+$` | `cc1717` |
| SKU code | 2–5 chars, one per blank × technique | `^[A-Z0-9]{2,5}$` | `CC17`, `G180E` |
| Listing ID | `<design><half?>-<skuCode>` (multi-design: `MIX-<skuCode>`) | `^(D\d{2}[AB]?\|MIX)-[A-Z0-9]{2,5}$` | `D08B-CC17` |
| Listing handle | `slug(title)`: title lowercased, apostrophes removed, every other run of non-alphanumerics → `-`, trimmed; unique; never changes after launch | `^[a-z0-9]+(-[a-z0-9]+)*$` | `the-door-tee` |
| Option code | 3-char colour code (table below) · `STD` (single colour) · `B1`–`B6` (Firsts badge) | `^([A-Z0-9]{3}\|STD\|B[1-6])$` | `IVR` |
| **SKU** | `<design><half?>-<tier>-<skuCode>-<option>-<size>`; tier `Q` quiet · `L` loud · `P` private · `N` none; size `XS`–`6XL` or `OS` | `^D\d{2}[AB]?-[QLPN]-[A-Z0-9]{2,5}-([A-Z0-9]{3}\|STD\|B[1-6])-(XS\|S\|M\|L\|XL\|[2-6]XL\|OS)$` | `D01-Q-CC17-IVR-M` |
| Bundle | `BND-<NAME>` | `^BND-[A-Z-]+$` | `BND-BUDDY-TEE` |
| Print file | `<design><half?>.<tier>.<productKey>.<placement>.<recipe>.<option\|ANY>[.<size>]` (size only for per-size AOP templates) | — | `D01.loud.cc1717.back.DARK.PEP` |

**SKU codes:** `CC17` cc1717 · `BC30` bc3001 · `G180` g18000 DTG · `G180E` g18000 embroidery · `CC15` cc1566 · `G185` g18500 · `M758` m7580 · `L559` aop559 · `L334` aop334 · `B477` aop477 · `S507` aop507 · `K882` socks882 · `Y624` y6245cm · `Y150` y1501kc · `EC80` ec8000 · `W788` bottle788 · `STK3` sticker3 · `SH505` sheet505 · `T883` towel883 · `N474` notebook474 · `PT3` patch3.

**More SKUs:** `D08B-Q-CC17-CMT-L` (Buddy Tee B, quiet) · `D10-N-G180E-NVY-2XL` · `D21-N-L559-LSG-XS` · `D12-N-STK3-B4-OS` (Firsts "tried the weights area") · `D02-N-STK3-STD-OS` (D02's sticker in `MIX-STK3`) · `D07-N-W788-STD-OS`.

**Rules**
- **The SKU is the one join key:** Shopify `Variant SKU` = Printful sync-variant `external_id` = `Variant.sku`. Never reused; a retired colour keeps its SKUs, archived. Personalised values (D27 crew name, D28 year) are **order line properties**, and the default inside label is a cost and a print file on the variant: neither is a SKU segment.
- **Handles:** `catalog-ids` asserts `handle === slug(title)` (or an entry in `handleOverrides`, empty at launch) and uniqueness, e.g. `buddy-tee-a-i-brought-my-buddy`, `day-one-the-sequel-crew`, `still-on-the-team-crew-garment-dyed`, `sneaker-toss-leggings-with-pockets`, `bel-mark-cap`.

**Colour codes.** This table seeds `catalog/src/colors.json` (`GarmentColor`) and is the **only home of garment hexes**. Names are **targets** until the live pull confirms them. N = neutral (≥ 50% rule) · D = dark (DARK recipe) · hex = `approxHex`, [U] unless marked; † = our estimate (`source: "brief §6.3 estimate"`) for mockup tint and provisional checks. The live `color_code` wins; checks on [U] hexes warn only (§6.3.1).

| Blank family | Code · name · flags · approx hex |
|---|---|
| Comfort Colors (1717, 1566) | `IVR` Ivory N `#EDE4CF` · `BAY` Bay N `#94A596` [T] · `SGE` Sage N `#B7BFA4` · `CHB` Chambray N `#A9B9CE` · `PEP` Pepper N D `#4F4D4C` · `ESP` Espresso N D `#4B3A31` · `BJN` Blue Jean N D `#6B7F99` (sticker border) · `CMT` Chalky Mint `#B8E2D0` · `BLS` Blossom `#F2C9CF` · `BTR` Butter `#F3E3A8` · `ORC` Orchid `#C9B4D6` |
| Bella+Canvas 3001 | `VWH` Vintage White N `#F2EDE3`† · `NAT` Natural N `#EFE6D3`† (also the EC8000 tote) · `WHT` White N `#FFFFFF` · `HDU` Heather Dust N `#E6D9CA`† · `NVY` Navy N D `#2B3150` · `HPM` Heather Prism Mint `#C6E5D6`† · `HPC` Heather Peach `#F2CBB8`† · `YLW` closest butter-yellow (name TBC [U]) `#F2DF8C` |
| Gildan 18000/18500 | `SND` Sand N `#D9CFB9`† · `SGY` Sport Grey N `#9C9FA3`† · `NVY` Navy N D · `DKH` Dark Heather N D `#464A50`† · `LBL` Light Blue `#A4C2DB`† |
| Yupoong hats, beanie, M7580 | `STN` Stone N `#D8D0BE`† · `NVY` Navy N D · `SPR` Spruce N D (offered? [U]) `#2F4A41`† · `HGY` Heather Grey N `#B4B4B2`† · `CHR` Charcoal N D `#45464A`† · `BPK` Soft Pink `#F2C6D2`† (`partnerColorName` "Baby Pink") |
| Pattern grounds (AOP, socks, towel): token hex [L] | `LCV` Locker Canvas N (`canvas`) · `LSG` Locker Sage N (`sage`) · `OAT` Oat N (`oat`) · `INT` Ink Night N D (`ink`) · `LNT` Lilac Night (`lilac`) · `POL` Pool (`pool`) · `GLD` Golden Hour (`butter`) |
| No colour choice / badges: `oat` hex [L] | `STD` · `B1` First Visit · `B2` Asked for Help · `B3` First Class · `B4` Tried the Weights Area · `B5` Rested on Purpose · `B6` Came Back |

### 5.3 Master product table

**Margin formula** (per unit, integer cents, `scripts/catalog/margins.ts`; every figure below is this formula, run by us [L]):

```
contribution = retail − baseCost − round(0.029 × retail) − 30 − labelCost
margin %     = contribution ÷ retail
```

- **Payment fees:** 2.9% + $0.30 (Shopify Payments, US online card rate) **[S]**; `pricing-rules.json` `paymentFee`: tag `"S"`, source "shopify.com/pricing (search summary, 2026-11-10)". The full $0.30 hits each unit (conservative). `labelCost` = $0.99 [T] on every eligible tee, Private included.
- **Shipping** is outside per-unit margin (the customer pays below the free-shipping threshold; above it, §5.7).
- **Base cost** = smallest size, first placement, Free plan. For a range the margin uses the **high** end (low end in brackets). "Planning" values are our derivations [U]: `planningBaseCost`, never displayed, replaced by the live price.
- **Per-size seeding:** sizes up to XL (XS–XL on B+C) take the blank's seeded base cost and tag. 2XL+ get `baseCost` null [U], `contribution` null and `marginBasis: "unknown"` until the live per-size price arrives.
- **US shipping, first / each additional** (snapshot): tees $4.75 / $2.20 [T]; fleece $8.79 / $2.50 [U] (joggers' $8.79 [T]); stickers and sheet $4.29 [T] / TBC; patch $4.29 / TBC [U]; bottle, notebook TBC [U]; the rest $4.75 / $2.20 [U]. Free lines ride with an order.
- Placements: F front · B back · LC/RC left/right chest · BN back neck · IL inside label. Colours and first drops: §5.2, §5.4.

| Key | Product · blank | Printful id | Method: placements | Sizes | Base cost | Retail | Contribution · % |
|---|---|---|---|---|---|---|---|
| `cc1717` | Hero heavyweight tee · Comfort Colors 1717 | 586 [T] | DTG: F, B, LC, RC, BN, IL | S–4XL [T] (varies by colour) | $15.60 [T] | $34 | $16.12 · 47.4% |
| `cc1717` Private | label only | — | DTG: IL | S–4XL | $15.60 + label | $28 | $10.30 · 36.8% |
| `bc3001` | Everyday tee · Bella+Canvas 3001 | 71 [U] | DTG: F, B, LC, IL | XS–5XL brand range [T]; Printful range [U] | $11.69–12.95 [T] | $28 | $12.95 · 46.3% ($14.21) |
| `bc3001` Private | label only | — | DTG: IL | same | $12.95 + label | $22 | $7.12 · 32.4% ($8.38) |
| `g18000` | Crewneck (value) · Gildan 18000 | 145 [U] | DTG: F, B, LC | S–5XL [T] | $19.72 [T] | $52 | $30.47 · 58.6% |
| `g18000` emb | Embroidered crew · Gildan 18000 | same | Embroidery: emb chest | S–5XL | $24.00 planning [U] (no source) + digitisation $6.50 once [T] | $56 | $30.08 · 53.7% |
| `cc1566` | Premium garment-dyed crew · Comfort Colors 1566 | 839 [T] | DTG: F, B, LC | S–3XL [U] | $31.29 planning [U] (Printify SwiftPOD price [T]) | $62 | $28.61 · 46.1% |
| `g18500` | Hoodie · Gildan 18500 | 146 [T] | DTG: F (art ≤ 3600 × 3000, clears pouch), B, LC | S–5XL [T] | $24.95 [T] | $58 | $31.07 · 53.6% |
| `g18500` 2-place | Crew-back hoodie (D27) | same | DTG: B + LC | S–5XL | $24.95 + extra placement ≈ $5.95 [U] | $64 | $30.94 · 48.3% |
| `m7580` | Joggers · Cotton Heritage M7580 | TBC [U] | DTG: left hip (fallback left leg) [U] | XS–2XL [U] | $29.98 [T] | $58 | $26.04 · 44.9% |
| `aop559` | AOP Recycled Leggings with Pockets | 559 [T] | Sublimation, cut-sew: all panels | XS–XL [U] | $32.00 planning [U] (€38.25 incl. NL VAT [T]) | $54 | $20.13 · 37.3% |
| `aop334` | AOP Plus Size Leggings | 334 [T] | same | 2XL–6XL [U] | $35.24 [T] | **$54 (same)** | $16.89 · 31.3% |
| `aop477` | AOP Recycled Longline Sports Bra | 477 [T] | same | "7 sizes" [T]; range [U] | $29.08 planning [U] (padded bra #387 price [T]) | $42 | $11.40 · 27.1% |
| `aop507` | AOP Biker Shorts | 507 [T] | same | XS–2XL [U] | $30.00 planning [U] (€27.77 incl. VAT [T]) | $46 | $14.37 · 31.2% |
| `socks882` | Sublimation Socks | 882 [T] | Sublimation: all panels | S / M / L [T] | $7.14 [T] | $16 | $8.10 · 50.6% |
| `y6245cm` | Low-profile cap · Yupoong 6245CM | 206 [T] | Flat embroidery: hat front | one size | $16.05 planning [U] (€16.05 incl. VAT [T]; DTFlex $14.02 [T]) + digitisation once | $32 | $14.72 · 46.0% |
| `y1501kc` | Cuffed beanie · Yupoong 1501KC | 266 [T] | Embroidery: beanie cuff | one size | $13.05 [T] | $28 | $13.84 · 49.4% |
| `ec8000` | Tote · Econscious EC8000 | TBC [U] | DTG: tote front (area [U]) | one size | $14.95–25.75 [T] | $30 | **$3.08 · 10.3%** ($13.88) |
| `bottle788` | Stainless Steel Water Bottle with Straw Lid, 32 oz | 788 [T] | per listing [U]: wrap (one body colour [U]) | 32 oz | $21.80 [T] | $40 | $16.74 · 41.9% |
| `sticker3` | Kiss-Cut Stickers, 3 in | 358 [U] | Digital: 3 in | 3 in | $1.95 [T] | $5 | $2.60 · 52.0% |
| `sticker3` Firsts | Firsts sticker | same | same | 3 in | $1.95 [T] | $0 | −$1.95 (promo) |
| `sheet505` | Kiss-Cut Sticker Sheet | 505 [T] | Digital: 5.83 × 8.27 in sheet | — | $5.15 [T] | $12 | $6.20 · 51.7% |
| `sheet505` gift | Free sheet (sign-up, Bring a Buddy, Black Friday) | same | same | — | $5.15 [T] | $0 | −$5.15 (promo) |
| `towel883` | Hand Towel, 16 × 28 in | 883 [T] | Sublimation: towel face | one size | $9.85 [T] | $24 | $13.15 · 54.8% |
| `notebook474` | Spiral Notebook | 474 [T] | Print [U]: cover | one size | $12.43–16.03 [T] | $24 | $6.97 · 29.0% ($10.57) |
| `patch3` | Printful embroidered patch, 3 in | TBC [U] | Embroidery: patch face | 3 in [U] | from $8.25 [T] + $6.50 digitisation per design once [T] | $14 | $5.04 · 36.0% |
| (component) | Inside label | placement `label_inside` | DTG: IL | 900 × 900 px (some 600/750) | $0.99 [T]; $0.90 on Growth | — | cost on every eligible tee |

**Margin floors** (`catalog/src/pricing-rules.json`; founder default, logged in `docs/decisions.md`). `tests/unit/catalog-margins.test.ts` checks every non-null contribution at **its own size's base cost**, maps every null to Appendix B U36 and warns with the §5.7 +$1.50 / +$3.00 sensitivity. A breach fails the build unless `catalog/src/margin-exceptions.json` lists the listing with a reason and `approvedBy` `"founder"`, or `"pending"` (only on `launch: false`; listed in D7). `D24-EC80` and `D26-EC80` are seeded `pending` (§2 decision 24); the Zod schema mirrors this.

| Class | Applies to | Floor |
|---|---|---|
| `core` | Quiet/Loud tees, all fleece, joggers | ≥ 35% **and** ≥ $9.00 |
| `entry` | Private tier, AOP activewear, socks, hats, accessories, paper, stickers, patches | ≥ 20% **and** ≥ $3.00 |
| `promo` | $0 lines (Firsts stickers, free sheet) | exempt; in the §5.7 order tests |

`Blank.marginClass` sets the class; a **Private-tier variant is always `entry`**.

**Watch list** (reported in D7):
- **Tote:** fails `entry` at the $25.75 high base (20% line: $22.83). Default $30, `pending` exception, no codes (§5.7 rule 4); options $34 or a cheaper blank (§2 decision 24).
- **Sports bra** (27.1%), **notebook** (29.0%): pass `entry` only at planning prices.
- **Plus-size leggings** keep $54 on purpose (values signal, §2), earning $3.24 less than the pocket pair.
- **B+C Private 2XL+:** a +$3.00 upcharge [U] leaves $4.12 (18.7%), below the floor; if confirmed, B+C Private stops at XL (§2 decision 25; option: an exception).
- **Patches:** six designs × $6.50 digitisation = $39 one-time [T].

**Not in year one** (not seeded; listed to save re-research; bare numbers = Printful ids): `shaker-py` (Printify M.i.A Merchandise #80, $13.98; $10.32 Premium [T]) — deferred (above) · `bottle17` ($20.25 [T]) — one bottle is enough · `m2580` (Cotton Heritage, $25.45 before the Feb-2026 rise [T]) — G18500 covers hoodies · `mat675` (675, $43.18 [T]) — prints differ from screen [T]; margin [U] · `gymbag-aop` ($52.01 [T]) and `duffle465` (465, $66.29 [T]) — price and margin · `case601` (601, $14.23 [T]) and `mug11` ([U]) — off-category · `sttu169` (Stanley/Stella, 456, $13.95 [T]) — a third tee blank (later eco capsule?) · `bc6400` (≈ $14.54 [T]) — unisex sizing only (§2 decision 7) · `bc6482` crop tee ([U]), `tank` (B+C 6008/8800 [U]; Printify NL 1533, $12.11 [T]) and `bc7502` cropped hoodie (317, €42.35 incl. VAT [T]) — narrow ranges · `ind20srt` fleece shorts (482, $26.47 [T]) — low priority · `aop242` (242, ≈ $30.12 [T]) — `aop559` has pockets · `aop282` (282, $24.92; padded #387 $29.08 [T]) — longline 477 chosen · `beach-towel` ($29.40 [T]) — the hand towel covers it · `poster` ([U]) — not apparel-led · `headband` (none at Printful or Printify [U]) — needs a third partner · `puff` 3D-puff hat (hats only [T], ≈ +$2–3 [U]) — Bel is too wide for 0.2–0.5 in puff columns · `label-out` outside label ($2.49 [T]) — inside label chosen · `packin` pack-in card ($0.50/order + $25/mo storage [U]) — a monthly fee before revenue · `emb-unlimited` (≈ $3.50–3.95 [U]) — §2 decision 20.

### 5.4 Listings: the year-one design × product matrix

A **listing** = one design (or buddy half) on one blank with one technique: one PDP, one Shopify product. **58 listings** over 12 months: 16 at launch, then 7 / 5 / 10 / 5 / 2 / 3 / 2 / 1 / 3 / 4 in drops 1–10. Drops 11–12 add no listings.

**Options** (Shopify allows **3 per product** [U]; its variant cap is reportedly raised from 100 to 2,048 [U]): tiered apparel `Style` (Quiet / Loud / Private) · `Color` · `Size`; untiered apparel and AOP `Color` (garment or ground) · `Size`; hats, beanie, towel `Color`; `MIX-STK3` `Design`; Firsts `Badge`; bottle, sheet, tote, notebook: Shopify's default title. Personalisation (D27, D28) is a line-item property, never an option.
- **Hard rule: ≤ 100 variants per listing**, safe under either cap (test): at most **4 colours** on a three-tier CC 1717 listing (3 × 4 × 7 = 84), **3** on a three-tier B+C 3001 listing (3 × 3 × 9 = 81). A seasonal colour **replaces** one on a full listing ("X for Y @drop").
- **`tierMode`:** default `"option"` (one product, Style option). Whether the Printful ↔ Shopify sync takes different print files per variant of one product is **[U]**; if not, `"sibling"`: one Shopify product per tier, linked by a `custom.tier_group` metafield, PDP toggle as links. §8 decides after a one-product test; the prototype always uses `"option"`.
- **Blank** = the SKU code's product key (§5.2; `G180E` = `g18000` embroidered) · **Sizes** = the blank's range (§5.3) · **Price** = the §5.7 ladder.
- **Variants** per listing = tiers × colours × sizes, an upper bound: the live pull disables combinations Printful doesn't make, so real counts can only fall.

| Listing ID | Title | Tiers | Colours (changes @drop) | Drop |
|---|---|---|---|---|
| `D01-CC17` | The Door tee | QLP | IVR BAY CMT PEP (BTR for CMT @7) | 0 |
| `D01-G185` | The Door hoodie | QL | SND NVY | 0 |
| `D02-BC30` | The Little Sticker tee | QLP | VWH HPM NVY | 0 |
| `D03-CC17` | Off Camera, On Purpose tee | QLP | PEP ESP IVR | 0 |
| `D04-CC17` | Long Time No Gym tee | QLP | BAY IVR PEP (+CHB @4) | 0 |
| `D05-G180` | Day One: The Sequel crew | L | SND NVY | 0 |
| `D06-G180` | Still on the Team crew | QL | SND LBL NVY | 0 |
| `D07-W788` | Proud of You. Also, Water. bottle | N | STD | 0 |
| `D08A-CC17` | Buddy Tee A: i brought my buddy. | QLP | BTR BAY PEP (+CHB @4) | 0 |
| `D08B-CC17` | Buddy Tee B: i'm the buddy. | QLP | CMT BLS BJN | 0 |
| `D09-G185` | Department of Showing Up hoodie | QL | SGY NVY | 0 |
| `D10-Y624` | Bel Mark cap | N | STN NVY (+SPR @10) | 0 |
| `D10-G180E` | Bel Mark crew (embroidered) | N | SND NVY | 0 |
| `D11-SH505` | Collect the Crew sticker sheet | N | STD | 0 |
| `D12-STK3` | Firsts stickers | N | B1 B2 B3 B4 B5 B6 | 0 |
| `MIX-STK3` | Single stickers | N | D01 D02 D03 D06 (+D19 @3, +D20 @3, +D26 @7) | 0 |
| `D06-CC15` | Still on the Team crew (garment-dyed) | QL | ORC IVR PEP | 1 |
| `D06-CC17` | Still on the Team tee | QLP | IVR ORC PEP | 1 |
| `D14-CC15` | Speed of Okay crew | QL | ORC IVR PEP | 1 |
| `D14-CC17` | Speed of Okay tee | QLP | IVR ORC PEP | 1 |
| `D15-Y150` | Rest on Purpose beanie | N | HGY BPK (+NVY @10, +CHR @10) | 1 |
| `D15-M758` | Rest on Purpose joggers | Q | HGY NVY | 1 |
| `D16-K882` | Lights Out socks | N | LNT INT | 1 |
| `D17-CC17` | Today's Specials tee | QLP | IVR BAY PEP | 2 |
| `D18A-CC17` | You Go tee (A) | QLP | BAY CMT PEP | 2 |
| `D18B-CC17` | I'll Go Too tee (B) | QLP | IVR BLS ESP | 2 |
| `D18A-G180` | You Go crew (A) | QL | SND NVY | 2 |
| `D18B-G180` | I'll Go Too crew (B) | QL | LBL DKH | 2 |
| `D19-BC30` | Today's List tee | QLP | NAT HDU NVY | 3 |
| `D20-BC30` | Oh! You're Here. tee | QLP | WHT HPC NVY (YLW for HPC @7) | 3 |
| `D21-L559` | Sneaker Toss leggings with pockets | N | LCV LSG | 3 |
| `D21-L334` | Sneaker Toss plus-size leggings | N | LCV LSG | 3 |
| `D21-B477` | Sneaker Toss longline sports bra | N | LCV LSG | 3 |
| `D21-S507` | Sneaker Toss biker shorts | N | LCV LSG | 3 |
| `D21-K882` | Sneaker Toss socks | N | LCV LSG | 3 |
| `D16-L559` | Lights Out leggings with pockets | N | LNT | 3 |
| `D16-L334` | Lights Out plus-size leggings | N | LNT | 3 |
| `D12-PT3` | Firsts patches | N | B1 B2 B3 B4 B5 B6 | 3 |
| `D23-S507` | Plate Party biker shorts | N | POL (+GLD @7) | 4 |
| `D23-B477` | Plate Party longline sports bra | N | POL (+GLD @7) | 4 |
| `D23-L559` | Plate Party leggings with pockets | N | POL (+GLD @7) | 4 |
| `D23-L334` | Plate Party plus-size leggings | N | POL (+GLD @7) | 4 |
| `D23-K882` | Plate Party socks | N | POL (+GLD @7) | 4 |
| `D22-CC17` | Every Day Is Brain Day tee | QLP | IVR CHB BLS PEP | 5 |
| `D22-CC15` | Every Day Is Brain Day crew | QL | IVR PEP | 5 |
| `D24-CC17` | The Receipt tee | QLP | IVR CMT BJN PEP | 6 |
| `D24-EC80` | The Receipt tote | N | NAT | 6 |
| `D25-T883` | Gym Towel (Not for Dishes) | N | OAT LSG | 6 |
| `D26-EC80` | Packed tote | N | NAT | 7 |
| `D09-CC17` | Department of Showing Up tee | QL | BTR BAY | 7 |
| `D27-G185` | The Crew Back hoodie (personalised) | L | SGY NVY | 8 |
| `D28-CC17` | Showing Up Since tee (personalised) | QLP | IVR BAY PEP BLS | 9 |
| `D28-G180` | Showing Up Since crew (personalised) | QL | SND NVY | 9 |
| `D30-N474` | Showed-Up Log notebook | N | STD | 9 |
| `D29-CC15` | I Count Visits crew | QL | ESP PEP SGE | 10 |
| `D29-CC17` | I Count Visits tee | QLP | BAY SGE ESP PEP | 10 |
| `D04-CC15` | Long Time No Gym crew | QL | ESP PEP | 10 |
| `D09-CC15` | Department of Showing Up crew | QL | ESP PEP | 10 |

**Totals [L]:** 58 listings · **575 SKUs at launch** · **1,901 SKUs by year end** (upper bounds) · largest listing 84 variants · 17 three-tier listings.

**Matrix rules (catalog tests):**
- Every hero design (D01, D04, D06, D08) has Quiet and Loud on every apparel listing, plus Private on every tee listing (sticker, MIX and accessory listings are exempt).
- A Loud design shows ≤ 3 characters; no design sits on a blank its `designs.json` `products[]` doesn't list; leggings and stretch panels carry no text; no black garment codes.
- In each drop ≥ half of the newly enabled **distinct garment colour codes** (`kind = "garment"`; no grounds, `STD`, badges) are neutral (N, §5.2). Golden Hour (drop 7) passes 2 : 2 (Bay, Natural : Butter, yellow).
- Side Quests carry `availability.until`: D05 28 Feb and D19 30 Apr (both back each January) · D24 and D25 31 Aug (back 2 Nov) · D28 moves to Meet the Crew after 4 Oct (default).
- **Leggings** (`D16-`, `D21-`, `D23-` × `L559`/`L334`) carry `gate.kind = "squat_test"` and stay `draft` until it passes. If only Locker Sage passes, ship only it and say so on the PDP; if nothing passes, no leggings. Bra, shorts and socks carry `"sample_qa"` and ship once their own sample passes.
- `D27-G185` stays `draft` while `features.crews` is not `"on"`.

### 5.5 The launch set (Tue 5 Jan 2027)

**Launch set** = the 16 drop-0 rows of §5.4 (`D01-CC17` `D01-G185` `D02-BC30` `D03-CC17` `D04-CC17` `D05-G180` `D06-G180` `D07-W788` `D08A-CC17` `D08B-CC17` `D09-G185` `D10-Y624` `D10-G180E` `D11-SH505` `D12-STK3` `MIX-STK3`), plus D13's default label on every eligible tee: 13 designs (D01–D13) on 8 blanks. No AOP (March, after the squat test), no black garments, no 3D puff.
- **Placements:** D01/D09 hoodies Quiet = front chest, Loud = back · D03 Quiet = back neck · D04 Bay = GARMENT-FILL · D08B Quiet = right chest · D09 Sport Grey (Sand if it fails contrast).
- **Bottle (§2 decision 31):** `D07-W788` launches only if its wrap template and print method are verified before round 1; otherwise it moves to drop 1 (launch = 15 listings).
- `tests/unit/launch-set.test.ts` reads the `launch: true` IDs from `catalog/src/listings.json` and fails if they differ from this list, unless a decision logged in `docs/decisions.md` trims it. Sample pieces, dates and costs: §8.4.

**Launch SKUs [L]: 575** (upper bound; 561 tee and fleece). To trim, cut `D01-G185` and `D05-G180` first: 14 listings, **527 SKUs**.

**Coverage check (test):** every persona has a Quiet option and an item under $35 (Frankie D01/D02/D03/D10; Dev D04/D05/D09/D10 cap; Priya D06/D07/D11; Duo D08 + Buddy Pack). Launch garment colours are 8 neutral : 5 pastel (Ivory, Bay, Pepper, Espresso, Blue Jean, Sand, Navy, Sport Grey : Chalky Mint, Butter, Blossom, Light Blue, Heather Prism Mint); Vintage White and Stone also count as neutral.

### 5.6 Collections & 12-month drop calendar

**Collections are queries** (`catalog/src/collections.json`, typed `Collection`); the build computes each listing's `collections[]`. Vibe collections open the PDP on **Quiet**; type collections (`tees` · `sweatshirts` · `activewear` · `hats` · `accessories` · `stickers-and-patches`, by `Blank.type`) use the brand default. Side Quest windows are stated calmly ("Here until 28 February. It might come back."): no countdowns, no "last chance", no scarcity (print-on-demand never runs out).

| Vibe handle | Rule | Primary designs | Blurb *(new)* |
|---|---|---|---|
| `meet-the-crew` | primary + alsoIn; D28 after its window | D01 D02 D04 D07 D09 D11 D12 D20 D21 D26 D29 D30 | The whole crew, every day. Pick a friend to take with you. |
| `the-small-print` | primary + **every listing with a quiet or private tier** + D15 | D03 D10 D13 | Quiet versions of everything: a small friend on the chest, or a secret on the label. |
| `buddy-system` | primary + Buddy Pack bundles + D11 (referral gift) | D08 D18 D23 D27 | Bring your gym person. You both get stickers. |
| `mallow-hours` | primary + D30 | D06 D14 D15 D16 D17 D22 | Rest counts. You're still on the card. Come back whenever. |
| `side-quests` | primary, **only inside the window** + live seasonal recolours | D05 D19 D24 D25 D28 | Small runs with plain end dates. They might come back. |

**Calendar** (`catalog/src/drops.json`, typed `Drop`; all Tuesdays [L]; campaign copy §9, art §6). `newListingIds` = the §5.4 rows with that drop number; `colorChanges` = its "@n" entries. `tests/unit/drops.test.ts` asserts Tuesdays, in order.

| # | Date | Drop | New designs | Listings; changes |
|---|---|---|---|---|
| — | 10 Nov–4 Jan | Pre-launch | — | Waitlist, quiz, free "Send a Bel" e-card, First Visit Plan; **no physical orders** |
| 0 | **Tue 5 Jan 2027** | **Launch: "New year, no pressure. No resolutions needed."** | D01–D13 | 16 (§5.5); stamp card, quiz, Firsts, Bring a Buddy |
| 1 | Tue 19 Jan | **Mallow Hours** + "Rest, don't quit" (campaign 8–22 Jan) | D14 D15 D16 | 7 |
| 2 | Tue 2 Feb | Buddy System: "Bring your gym person." | D17 D18 | 5; Buddy Packs for D18 |
| 3 | Tue 2 Mar | Side Quest "First Things" + activewear | D19 D20 D21 | 10 (incl. `D16-L559/L334`, `D12-PT3`); stickers +D19 +D20; leggings gated |
| 4 | Tue 6 Apr | Pool Day (Chalky Mint + Chambray) | D23 | 5; +Chambray on D04 and D08A |
| 5 | Tue 4 May | "For your brain" (not called "Brain Day") | D22 | 2 |
| 6 | Tue 1 Jun | Side Quest "Summer Receipt" (to 31 Aug) | D24 D25 | 3 |
| 7 | Tue 6 Jul | Golden Hour (Butter + Bay) | D26 | 2 (incl. `D09-CC17`); D01 Butter for Chalky Mint; D20 yellow for Heather Peach; D23 Golden Hour ground; sticker +D26 |
| 8 | Tue 3 Aug | Buddy System 2: "Start a crew." | D27 (if crews ship) | 1, behind `features.crews` |
| 9 | Tue 7 Sep | Comeback Season: "Welcome back. No catching up required." | D28 D30 | 3 (personalisation on) |
| 10 | Tue 5 Oct | Sweater Weather (Espresso, Pepper, Sage) | D29 | 4 (incl. `D04-CC15`, `D09-CC15`); hat +Spruce; beanie +Navy +Charcoal; crew-member vote opens |
| 11 | Tue 2 Nov | Gifting: "Send a Bel." | — | Gift bundles on (§5.7); D24 tote and D25 towel return; calm Black Friday (26 Nov) |
| 12 | Tue 7 Dec | "Your year in stamps" + new crew member reveal | — | New member ships as a sticker (id assigned then) |

`D09-CC17` (Butter, Bay; Quiet/Loud) is a founder default for the "D09 on Butter" recolour; it could be a hoodie colour instead.

### 5.7 Pricing rules & unit economics

**Price ladder** (§2 decision 10; `catalog/src/listings.json` is the only place prices live): hero tee $34 · everyday tee $28 · **Private tier $6 less** (CC 1717 $28, B+C 3001 $22) · crew $52 · embroidered crew $56 · premium crew $62 · hoodie $58 · crew-back hoodie $64 · joggers $58 · pocket leggings **and plus-size leggings $54** · sports bra $42 · biker shorts $46 · socks $16 · cap $32 · beanie $28 · tote $30 · bottle $40 · towel $24 · notebook $24 · patch $14 · sticker $5 · sheet $12 · Firsts $0 · free shipping at **$75** (`brand.config.json` `shipping.freeThresholdCents = 7500`).

**Rules (each a test in `tests/unit/pricing.test.ts`)**
1. **Same price in every size:** all variants of a listing × tier share one `price`; **no plus-size upcharge** (`aop334` = its `aop559` sibling).
2. **Whole dollars only** (`amount % 100 === 0`): no .99 endings, no compare-at or strike-through prices (`Variant Compare At Price` stays empty).
3. Private price = Quiet/Loud price − 600, tees only.
4. **Allowed discounts:** bundles; one first-order code of 10% (quiz/email, §4.4 line 9); Bring a Buddy (free sheet or 15%). Codes never stack and never apply to bundles or $0 lines (`excludes`: `bundles`, `promo`, `margin_exception`). With the largest code applied, every variant still has contribution ≥ $0. Codes exclude listings with a margin exception (the tote: −$1.29 at its $25.75 high base under 15% off). Otherwise the worst case is B+C Private 2XL+ with a +$3 upcharge [U] at 15% off: $0.92. The mock `priceCart()` (§7.9) and the Shopify codes (§8.2 step 12) apply the same exclusions.
5. **No sales, no countdowns.** Black Friday (Fri 26 Nov 2027) to 29 Nov: no discount, just a free Collect the Crew sheet with any order and plain copy.
6. Personalisation is +$0; D27's $64 is the two-placement price, not a fee.
7. **Re-price only by founder decision:** `npm run catalog` reports any live base cost that moved > $1.00 and any floor breach, and never edits a price.

**Bundles** (`catalog/src/bundles.json`, typed `Bundle`; a fixed discount in cents, so the price follows the tiers chosen)

| Bundle ID | What | Discount | Price | Contribution [L] | Live from |
|---|---|---|---|---|---|
| `BND-BUDDY-TEE` | Buddy Pack: one A + one B of the same design (D08 or D18 tees), sizes picked separately | −$8 | **$60** (Private pair $48) | $24.78 · 41.3% (Private pair $13.13 · 27.4%) | drop 0 (D08), 2 (D18) |
| `BND-BUDDY-CREW` | D18 crew A + B | −$8 | $96 | $53.48 · 55.7% | drop 2 |
| `BND-FIRST-VISIT` | First Visit Kit: D01 tee + D07 bottle + D11 sheet | −$14 | $72 | $26.07 · 36.2% | drop 11 (or launch, founder) |
| `BND-REST-SET` | Rest on Purpose Set: D06 crew (CC 1566) + D15 joggers; generated `sizeNote` "Crew S–3XL, joggers XS–2XL for now. For more room, try the Still on the Team crew (to 5XL)." | −$15 | $105 | $40.38 · 38.5% | drop 11 |

**Worked examples** (size M, Free plan, label $0.99 [T], fees [S]): contribution now → on Growth (9% branding [V] + an illustrative blank discount d = 0 / 5% / 10%, measured in the trial):
- `D01-CC17` Loud $16.12 (47.4%) → $16.21 / $16.99 / $17.77 · Private $10.30 (36.8%) → $10.39 / $11.17 / $11.95
- `D02-BC30` Loud $12.95 (46.3%, high base [T]) → $13.04 / $13.69 / $14.33 · `D06-G180` Loud $30.47 (58.6%) → $30.47 / $31.46 / $32.44
- `D09-G185` Loud $31.07 (53.6%) → $31.07 / $32.32 / $33.56 · `D10-Y624` Stone $14.72 (46.0%, base [U]) → $14.72 / $15.52 / $16.32 · `D07-W788` $16.74 (41.9%) → $16.74 / $17.83 / $18.92

**Size upcharge sensitivity** (2XL+ costs more [T]; amounts [U]), margin at +$1.50 / +$3.00: CC 1717 Loud 43.0% / 38.6% · CC 1717 Private 31.4% / 26.1% · B+C 3001 Loud 40.9% / 35.5% · B+C 3001 Private 25.5% / **18.7%** (fails `entry`, §5.3 watch list) · Gildan 18500 51.0% / 48.4%.

**Growth break-even:** d × base spend + 0.09 × label spend beats $24.99 once base spend passes **$500/month at d = 5%** or **$250 at d = 10%**; labels alone need **$278/month** (≈ 280 tees).

**Free shipping at $75** (merchandise subtotal after discounts, $0 lines excluded, integer cents). Below it the customer pays Printful's live rates via the Shopify app at go-live [U], or the prototype mock $4.75 + $2.20 each additional (the tee rate [T]). At ≥ $75 we absorb it:

| Qualifying order | Subtotal | Base + labels | Fees | Shipping absorbed (est.) | Contribution [L] |
|---|---|---|---|---|---|
| 2 hero tees + sticker sheet | $80 | $38.33 | $2.62 | $7.45 [T/U] | $31.60 · 39.5% |
| 3 everyday tees | $84 | $41.82 | $2.74 | $9.15 [T/U] | $30.29 · 36.1% |
| Hoodie + cap | $90 | $41.00 | $2.91 | $11.29 [U] | $34.80 · 38.7% |
| Plus-size leggings + longline bra (worst case) | $96 | $64.32 | $3.08 | $6.95 [U] | $21.65 · 22.6% |

Two hero tees ($68) or a Buddy Pack ($60) fall short, so the free-shipping bar (§4.4 line 13) shows the gap honestly, without pressure copy. `tests/unit/shipping.test.ts`: $74.99 → charged; $75.00 → free; a 10% code taking $80 to $72 → charged.

**Break-even** (no ads, returns or tax): fixed costs Shopify Basic ≈ $29–39/mo [S] + domain ≈ $2/mo [U] = **≈ 3 hero-tee orders a month** at $16.12 (≈ 5 with Growth) · every $100 of samples (§8.4) ≈ 6 hero tees · misprints and damage are reprinted free within 30 days [V]; wrong-size exchanges cost a new base plus shipping (§8.5).

### 5.8 Size, fit, fabric & care

**Size charts are never invented:** `GET /v2/catalog-products/{id}/sizes` [T], or the partner's product-page table copied by the founder with its URL (tag [T]), into `catalog/size-guides/<productKey>.json` (`SizeGuide`). With no chart the PDP says "The size chart comes from our print studio. It isn't loaded yet, so this one is TBC." and the listing can't be `active` (test). Show inches + cm (× 2.54, to the nearest 0.5) from the partner's flat measurements; never interpolate a size.

| Blank | Fit (our note) · size advice | Fabric (pull live; snapshot) | Range, honestly shown |
|---|---|---|---|
| `cc1717` | Boxy and relaxed; heavyweight. Garment-dyed, so each tee is a touch different. · True to size; size up for slouchy | 100% ring-spun cotton, garment-dyed [U] | S–4XL [T]; some colours stop earlier: show the per-colour range |
| `bc3001` | Classic retail fit; lighter and softer · true to size | Combed ring-spun cotton; heathers are blends [U] | XS–5XL brand range [T]; Printful per colour [U] |
| `g18000` / `g18500` | Classic, roomy fleece; the hoodie has a front pouch · true to size | Cotton/poly fleece [U] | S–5XL [T] |
| `cc1566` | Garment-dyed, relaxed · true to size | [U] | S–3XL [U]: size note points to the Gildan crew (to 5XL) |
| `m7580` | Fleece joggers; **run small** [T] · **size up** | [U] | XS–2XL [U]: "This style stops at 2XL for now." |
| `aop559` / `aop334` | Fitted and supportive; high waist; pockets / plus-size cut, same pattern scale · true to size | 75% recycled polyester, 25% elastane (US/MX) [T]; UPF 50+ claim [T] / [U] | XS–XL [U] / 2XL–6XL [U], same price; each PDP links the other cut |
| `aop477` | Longline, removable padding [T] · partner chart | Recycled polyester blend [T] | "7 sizes" [T]; plus sizes not confirmed: an honest size note, never "every size" |
| `aop507` | Biker shorts · partner chart | 75/25 recycled poly/elastane [T] | XS–2XL [U]; QA the waistband (reviews say it rolls [T]) |
| `socks882` | Stretch knit; pattern only · partner shoe-size map | 95% polyester / 5% spandex [T] | S / M / L [T] |
| `y6245cm` / `y1501kc` | Low-profile adjustable cap / cuffed knit beanie · one size | [U] | one size |
| other accessories, paper | Dimensions from the partner | Tote is organic cotton [T]; bottle lid called "a little cheap" in reviews [T]: sample it | — |

**Rules**
1. **Show the real range** on the PDP and every card; **no sitewide range**. "Same price in every size" is the only sitewide size claim.
2. **Narrow ranges get a `sizeNote`:** "Sizes {size_range}. This style stops at {max} for now. For more room, try {alternative}." The build fills `{max}` and `{alternative}`; `{size_range}` stays a placeholder filled per colour (no literal size range in listing copy, §4.4).
3. **Plus sizes:** same price, AOP pattern scale (fixed physical tile, §6) and laid-flat mockups, shown **next to** the standard cut (cross-linked PDPs, one size filter for both). Never a separate "plus" collection.
4. **Claims.** UPF, recycled, organic and certification claims need a [V] source (the partner's own product page or the certificate) stored in `Sourced.source`. With only [T], omit the claim (every [T] claim above, for now). Never "Made in USA": the facility varies and Printful prints the origin on the label.
5. **Care:** the partner's care strings; until pulled, "Wash cold, inside out. Hang to dry if you can." [U]. No performance claims ("won't fade", "no shrink").
6. **Copy-lint** per §4.4.

### 5.9 Product copy

Every PDP string is a `CopyString` in `listing.copy`, so banned words (scope `product`; titles `names`) and copy-lint cover it. The build writes `PdpCopy` for every listing from this template, lists each new string in `docs/decisions.md` as *(new)* for one founder batch review, and never waits for it. Slogans and whispers come only from `designs.json`.

| Field | Source | Rule |
|---|---|---|
| `title` | listing | "<Design name> <product noun>". Never "Rest Day" in any title, collection, drop or bundle name (a Gymshark line). "Brain Day" only inside the full slogan title "Every Day Is Brain Day …", never alone (drop 5 is "For your brain") |
| `tagline` | the design's slogan, else one line | lowercase if it is the slogan |
| `description` | template | 3–5 sentences: who the character is → what it feels like → the fabric → "Same price in every size, {size_range}." → "Made just for you, so give it a few days." Max one joke, one "!" |
| `tierBlurbs.quiet/loud/private` | per listing | what you'll see, where, how big. Private names the label and ends with `{whisper}` (from `designs.json`; D13 default shown verbatim in parentheses) |
| fit, fabric, care, size range · `sizeNote` | `Blank` (live) · §5.8 template | never typed in copy · only for narrow ranges or split cuts |
| `seeThroughNote` | squat-test listings | rendered only when `gate.status = "passed"`: "Is it see-through? Before it went on sale, we tested each colour in a bright room, in a deep squat, in a standard size and a plus size. Only the colours that passed are here." |
| `windowNote` · bundle callout | Side Quests · `bundleIds` | "Here until {date}. It might come back." · "Buddy Pack: one A and one B, sizes picked separately. Save $8 on the pair." |
| made-to-order block · image alt | §4.4 line 10 · `Mockup.alt` | `{production_window}`/`{transit_window}` from data · garment colour + "{Name} the {object}, {expression}, {pose}" + placement |
| `seo.title` / `.description` | per listing | ≤ 60 / ≤ 155 chars |

Example A in §5.10 holds a full `copy` block (`D01-CC17`); Example B shows the AOP differences (`D21-L559`: no tier blurbs, a `sizeNote`). Plus:

**Example: `D04-CC17` Long Time No Gym tee**
- **Tagline:** long time no gym.
- **Description:** Gus spent three years in a closet. He's back now, and he isn't making a big thing of it. Heavyweight garment-dyed cotton in grown-up colours. Same price in every size, {size_range}. Made just for you, so give it a few days.
- **Quiet:** Gus and one small dust puff on the left chest. No words. · **Loud:** Gus stepping out of his locker, with the line across the top. · **Private:** plain outside. Inside the label: (psst. welcome back. no catching up.)
- **Colour note (Bay):** On Bay, Gus is printed in the shirt's own colour, so he reads tonal and calm.

All copy in §5.6–5.10 and every title and name here pass the §4.4 banned list and copy-lint, with no literal size range in listing copy [L]; "Rest Day Set" and "Brain Day crew" fail `names`, "you came back" fails `innuendo` (write "you're back").

### 5.10 Catalog data model

**Flow.** Paths: §10.1. `npm run catalog` compiles `catalog/src/*` + `art/designs/designs.json` + `catalog/live/` into `catalog/catalog.json`; `catalog:pull -- --live` writes snapshots; `export:shopify` writes both CSVs; `export:printful` writes the sync plan. `catalog/live/printful/` starts empty (`.gitkeep`); §5.3 values live in `catalog/src/blanks.json` (the 20 year-one `ProductKey`s only); `catalog:pull` with no files prints '0 snapshots, nothing to validate' and exits 0. `Catalog.snapshotDate` = the latest `checkedAt` across the seeds (2026-11-10), never the wall clock. `lib/catalog/ids.ts` exports `SKU_RE`, `LISTING_ID_RE`, `DESIGN_ID_RE`, `TIER_CODE` and `skuFor(listing, tier, option, size)`.

**`lib/catalog/types.ts`**, type-checked by us with tsc 5.9.3 and 6.0.2 (`--strict --noUncheckedIndexedAccess --exactOptionalPropertyTypes`), with Example A and the full form of Example B as `satisfies Listing` [L]:

```ts
// lib/catalog/types.ts: CANONICAL. §6 and §7 import these; nothing redefines them. Money = integer US cents;
// partner facts are Sourced<T> with a verification tag; no wall-clock timestamps.

// --- primitives
export type CurrencyCode = 'USD';
export interface Money { readonly amount: number; readonly currency: CurrencyCode } // 3400 = $34.00
export type IsoDate = `${number}-${number}-${number}`; // YYYY-MM-DD
export type VerificationTag = 'V' | 'T' | 'L' | 'S' | 'U';
export interface Sourced<T> {
  readonly value: T;
  readonly source: string; // URL | 'printful:/v2/catalog-products/586/prices' | 'brief §5.3'
  readonly tag: VerificationTag;
  readonly checkedAt: IsoDate;
  readonly note?: string;
}
// same shape as content/*.json entries, so copy-lint and banned-words run on catalog copy
export interface CopyString { readonly text: string; readonly surface: string; readonly speaker: CharacterId | null }

// --- ids and closed vocabularies
type Digit = '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9';
export type DesignId = `D${'0' | '1' | '2' | '3'}${Digit}`; // D01…D30; D31+ reserved
export type DesignPart = 'A' | 'B'; // buddy halves
export type Tier = 'quiet' | 'loud' | 'private';
export type TierOrNone = Tier | 'none';
export type TierCode = 'Q' | 'L' | 'P' | 'N';
export type SizeId = 'XS' | 'S' | 'M' | 'L' | 'XL' | '2XL' | '3XL' | '4XL' | '5XL' | '6XL' | 'OS';
export type ProductKey = 'cc1717' | 'bc3001' | 'g18000' | 'cc1566' | 'g18500' | 'm7580' | 'aop559' | 'aop334' | 'aop477' | 'aop507'
  | 'socks882' | 'y6245cm' | 'y1501kc' | 'ec8000' | 'bottle788' | 'sticker3' | 'sheet505' | 'towel883' | 'notebook474' | 'patch3';
export type SkuCode = 'CC17' | 'BC30' | 'G180' | 'G180E' | 'CC15' | 'G185' | 'M758' | 'L559' | 'L334' | 'B477' | 'S507' | 'K882'
  | 'Y624' | 'Y150' | 'EC80' | 'W788' | 'STK3' | 'SH505' | 'T883' | 'N474' | 'PT3';
export type ListingId = `${DesignId}${'' | DesignPart}-${SkuCode}` | `MIX-${SkuCode}`;
export type ColorCode = string;
export type BadgeCode = 'B1' | 'B2' | 'B3' | 'B4' | 'B5' | 'B6';
export type OptionCode = ColorCode | 'STD' | BadgeCode;
export type BundleId = 'BND-BUDDY-TEE' | 'BND-BUDDY-CREW' | 'BND-FIRST-VISIT' | 'BND-REST-SET';
export type CharacterId = 'bel' | 'mallow' | 'gus' | 'pippop' | 'sip' | 'ollie' | 'tuck';
export type Expression = 'happy' | 'nervous' | 'proud' | 'sleepy' | 'hyped' | 'surprised' | 'determined' | 'shy' | 'chill' | 'trying';
export type ExpressionPreset = Expression | 'reading'; // D02: determined brows + shifted pupils
export type PersonaId = 'frankie' | 'dev' | 'priya' | 'duo';
export type CollectionHandle = 'meet-the-crew' | 'the-small-print' | 'buddy-system' | 'mallow-hours' | 'side-quests';
export type TypeCollectionHandle = 'tees' | 'sweatshirts' | 'activewear' | 'hats' | 'accessories' | 'stickers-and-patches';
export type TokenName = 'ink' | 'oat' | 'canvas' | 'white' | 'coral' | 'lilac' | 'bubblegum' | 'butter' | 'sage' | 'pool' | 'pistachio'
  | 'ink-soft' | 'coral-deep' | 'lilac-deep' | 'sage-deep' | 'pool-deep' | 'lilac-shade'; // all 17; text-only tokens reach art only as thread sources (§6.3.2)
export type PodPartner = 'printful'; // year one: Printful only (§5.1 rule 1)
export type Technique = 'dtg' | 'dtfilm' | 'embroidery' | 'sublimation' | 'cut-sew' | 'digital' | 'uv'; // = Printful v2 technique keys [T]
export type PlacementId = 'front' | 'back' | 'left_chest' | 'right_chest' | 'back_neck' | 'sleeve_left' | 'label_inside' | 'emb_chest'
  | 'hat_front' | 'beanie_cuff' | 'left_hip' | 'sticker_3in' | 'sticker_sheet' | 'aop_panels' | 'wrap' | 'tote_front' | 'towel_face'
  | 'notebook_cover' | 'patch_face';
export type ColourRecipe = 'LIGHT' | 'DARK' | 'GARMENT-FILL' | 'TONAL-INK' | 'TONAL-OAT' | 'FULL-BLEED';
export type ProductType = 'tee' | 'crewneck' | 'hoodie' | 'joggers' | 'leggings' | 'sports_bra' | 'shorts' | 'socks' | 'dad_hat' | 'beanie'
  | 'tote' | 'water_bottle' | 'sticker' | 'sticker_sheet' | 'towel' | 'notebook' | 'patch';
export type MarginClass = 'core' | 'entry' | 'promo';

// --- placements (print-specs.json by §6, key `${productKey}.${placement}`)
export interface PrintAreaSpec {
  readonly key: string; readonly productKey: ProductKey; readonly placement: PlacementId; readonly technique: Technique;
  readonly canvasPx: readonly [number, number];
  readonly artBoxPx?: { readonly x: number; readonly y: number; readonly w: number; readonly h: number }; // e.g. left_chest in front
  readonly dpi: number; readonly background: 'transparent' | 'full_bleed';
  readonly partnerPlacement: Sourced<string | null>; // Printful placement id [U until pulled]
  readonly maxThreads?: number;
  readonly verified: Sourced<boolean>; // true only once checked against the partner template
}

// --- colours and blanks
export interface GarmentColor {
  readonly code: ColorCode; readonly name: string; readonly kind: 'garment' | 'aop_ground' | 'single';
  readonly isDark: boolean; readonly neutral: boolean; readonly approxHex: Sourced<`#${string}`>; // §5.2; name = display name
}
export interface BlankColor {
  readonly code: ColorCode;
  readonly partnerColorName: Sourced<string>; // exact Printful `color`
  readonly colorCode: Sourced<`#${string}` | null>; // Printful `color_code`: validator input
  readonly sizes?: readonly SizeId[];
}
export interface BlankOffer {
  readonly technique: Technique; readonly skuCode: SkuCode; readonly placements: readonly PlacementId[];
  readonly baseCost: Sourced<Money | null>; // smallest size, first placement, Free plan, US
  readonly planningBaseCost?: { readonly value: Money; readonly derivation: string }; // [U]; margins only
  readonly baseCostBySize?: Readonly<Partial<Record<SizeId, Sourced<Money>>>>;
  readonly extraPlacementCost?: Sourced<Money | null>;
  readonly oneTimeFees?: readonly { readonly label: string; readonly cost: Sourced<Money | null> }[];
}
export interface FitInfo {
  readonly cut: 'unisex_boxy' | 'unisex_classic' | 'unisex_relaxed' | 'fitted_supportive' | 'one_size';
  readonly sizeAdvice: 'true_to_size' | 'size_up' | 'size_down_for_closer_fit';
  readonly note: CopyString;
}
export interface Gate { readonly kind: 'squat_test' | 'sample_qa' | 'feature_flag'; readonly status: 'pending' | 'passed' | 'failed'; readonly note: string; readonly decidedAt?: IsoDate }
export interface Blank {
  readonly key: ProductKey; readonly type: ProductType;
  readonly title: string; readonly brand: string; readonly model: string; // 'Comfort Colors', '1717'
  readonly partner: PodPartner;
  readonly partnerProductId: Sourced<number | null>; // Printful catalog product id
  readonly offers: readonly BlankOffer[];
  readonly insideLabel: { readonly eligible: Sourced<boolean>; readonly cost: Sourced<Money | null> } | null;
  readonly colors: readonly BlankColor[];
  readonly sizes: Sourced<readonly SizeId[]>;
  readonly shippingUS: { readonly first: Sourced<Money | null>; readonly additional: Sourced<Money | null> };
  readonly productionDays: Sourced<{ readonly min: number; readonly max: number } | null>;
  readonly fit: FitInfo; readonly fabric: Sourced<string | null>; readonly certifications?: Sourced<readonly string[]>;
  readonly care: Sourced<readonly string[] | null>; readonly sizeGuideId: string | null;
  readonly marginClass: MarginClass; readonly gate?: Gate;
}

// --- designs (art/designs/designs.json, owned by §6; copied into catalog.json)
export interface DesignText {
  readonly role: 'slogan' | 'sub' | 'sign' | 'ring_top' | 'ring_bottom' | 'caption' | 'menu' | 'receipt';
  readonly font: 'caprasimo' | 'atkinson';
  readonly lines: readonly string[]; // exact; placeholders {brand} {crew_name} {month} {year} stay lowercase; the layout upper-cases them
  readonly xHeightPx?: number;
}
export interface DesignVariant { readonly placement: PlacementId; readonly canvas: readonly [number, number]; readonly layout: string } // layout id → art/designs/index.ts registry (§6.4.1)
export type DesignVariants = Readonly<Partial<Record<TierOrNone, DesignVariant>>>;
export interface DesignProduct { readonly blank: ProductKey; readonly method: Technique; readonly variants: readonly TierOrNone[]; readonly overrides?: DesignVariants }
export interface DesignPartSpec { readonly text: readonly DesignText[]; readonly whisper: readonly string[] | null; readonly variants: DesignVariants }
export interface Design {
  readonly id: DesignId; readonly name: string;
  readonly kind: 'mascot' | 'typographic' | 'buddy_pair' | 'mark' | 'pattern' | 'sticker' | 'accessory' | 'format' | 'personalised' | 'label';
  readonly collection: CollectionHandle; readonly alsoIn: readonly CollectionHandle[];
  readonly personas: readonly PersonaId[];
  readonly hero: boolean; // hero ⇒ quiet + loud on apparel (+ private on tees): catalog test
  readonly drop: IsoDate;
  readonly window?: { readonly from: IsoDate; readonly until: IsoDate | null; readonly returns?: string };
  readonly characters: readonly { readonly id: CharacterId; readonly expression: ExpressionPreset; readonly pose: string; readonly part?: DesignPart }[];
  readonly text: readonly DesignText[];
  readonly whisper: readonly string[] | null; // Private label text; null ⇒ D13 default
  readonly variants: DesignVariants;
  readonly parts?: Readonly<Record<DesignPart, DesignPartSpec>>; // buddy pairs (top-level text/variants empty)
  readonly colourways: {
    readonly light: readonly string[]; readonly dark: readonly string[]; readonly garmentFill?: readonly string[];
    readonly accentSwaps?: readonly { readonly on: string; readonly from: TokenName; readonly to: TokenName }[];
  };
  readonly products: readonly DesignProduct[];
  readonly clearance: Sourced<'brand_cleared' | 'tess_etsy_checked'>; // [U] until the TESS/Etsy check
}

// --- print files and mockups
export interface PrintFile { // one entry of print-files/manifest.json (§6)
  readonly id: string; // `${designId}${part}.${tier}.${productKey}.${placement}.${recipe}.${option|ANY}[.${size}]`
  readonly designId: DesignId; readonly part?: DesignPart; readonly tier: TierOrNone;
  readonly productKey: ProductKey; readonly placement: PlacementId; readonly technique: Technique;
  readonly recipe: ColourRecipe; readonly garmentColor: ColorCode | null; // null = colour-independent
  readonly size?: SizeId; // per-size AOP templates only
  readonly path: string; // 'print-files/D01/D01.loud.cc1717.back.DARK.PEP.png'
  readonly widthPx: number; readonly heightPx: number; readonly dpi: number; readonly sha256: string;
  readonly specKey: string;
  readonly validator: { readonly status: 'pass' | 'warn' | 'fail'; readonly failures: readonly string[]; readonly warnings: readonly string[] };
  readonly perOrderTemplate?: boolean; // D27/D28 preview; real file per order
  readonly hostedUrl?: string;
}
export interface Mockup {
  readonly listingId: ListingId; readonly option: OptionCode; readonly tier: TierOrNone;
  readonly view: 'flat_front' | 'flat_back' | 'detail' | 'label' | 'pair' | 'og';
  readonly src: string; // '/mockups/<handle>/<option>-<tier>-<view>.webp' · OG: '/og/<handle>.png'
  readonly widths: readonly number[]; readonly width: number; readonly height: number;
  readonly alt: string;
  readonly origin: 'generated-svg' | 'printful-mockup-api';
}

// --- listings and variants
export interface ListingColor { readonly code: OptionCode; readonly recipe: ColourRecipe; readonly addedInDrop: number; readonly retiredInDrop?: number }
export interface Personalisation {
  readonly kind: 'year' | 'crew_name';
  readonly rule: string; // 'year picker 1980..AS_OF year' | "A-Z 0-9 space . ' -; ≤ 16; blocklists; draft-order review"
  readonly surcharge: Money; // 0
  readonly flag: 'features.personalisation' | 'features.crews';
}
export interface PdpCopy {
  readonly tagline: CopyString; readonly description: CopyString;
  readonly tierBlurbs: Readonly<Partial<Record<Tier, CopyString>>>;
  readonly sizeNote?: CopyString; readonly windowNote?: CopyString;
  readonly seeThroughNote?: CopyString; // squat_test listings; shown only once passed
  readonly seo: { readonly title: string; readonly description: string };
}
export interface PartnerVariantRef {
  readonly printful?: { readonly catalogVariantId: Sourced<number | null>; readonly syncVariantId?: number; readonly externalId: string };
  readonly shopify?: { readonly variantGid?: string };
}
export interface Variant {
  readonly sku: string; // SKU_RE; stable forever, never reused
  readonly listingId: ListingId; readonly designId: DesignId; readonly part?: DesignPart;
  readonly tier: TierOrNone; readonly option: OptionCode; readonly size: SizeId;
  readonly price: Money;
  readonly baseCost: Sourced<Money | null>; // this size + every placement printed
  readonly labelCost: Money | null;
  readonly contribution: Money | null; // computed (§5.3)
  readonly marginBasis: 'live' | 'snapshot' | 'planning' | 'unknown';
  readonly availability: 'available' | 'partner_out_of_stock' | 'discontinued' | 'unknown';
  readonly printFileIds: readonly string[]; // label included
  readonly partner: PartnerVariantRef;
  readonly shopifyOptions: readonly string[];
}
export interface Listing {
  readonly id: ListingId;
  readonly handle: string; // slug(title), §5.2: unique, never changes after launch
  readonly title: string;
  readonly designIds: readonly DesignId[];
  readonly part?: DesignPart;
  readonly productKey: ProductKey; readonly technique: Technique; readonly skuCode: SkuCode;
  readonly tiers: readonly TierOrNone[]; readonly defaultTier: TierOrNone; // brand.config tiers.default if offered
  readonly optionAxis: 'color' | 'design' | 'badge' | 'none';
  readonly colors: readonly ListingColor[];
  readonly sizes: readonly SizeId[];
  readonly price: Readonly<Partial<Record<TierOrNone, Money>>>;
  readonly collections: readonly CollectionHandle[]; // computed
  readonly typeCollection: TypeCollectionHandle;
  readonly drop: number;
  readonly availability: { readonly from: IsoDate; readonly until: IsoDate | null; readonly returns?: string };
  readonly status: 'draft' | 'active' | 'archived';
  readonly visibility: 'public' | 'unlock_only'; // Firsts: unlock_only
  readonly launch: boolean;
  readonly gate?: Gate; readonly personalisation?: Personalisation;
  readonly copy: PdpCopy;
  readonly tags: readonly string[]; readonly bundleIds: readonly BundleId[]; readonly crossSell: readonly ListingId[];
  readonly mockups: readonly Mockup[]; readonly variants: readonly Variant[];
  readonly shopify: { readonly tierMode: 'option' | 'sibling'; readonly productType: string };
}

// --- merchandising and money rules
export interface CollectionRule {
  readonly primaryDesigns?: boolean; readonly alsoInDesigns?: boolean;
  readonly tiersAny?: readonly Tier[]; // the-small-print: ['quiet', 'private']
  readonly includeDesigns?: readonly DesignId[]; readonly productTypes?: readonly ProductType[];
  readonly onlyInsideWindow?: boolean;
}
export interface Collection {
  readonly handle: CollectionHandle | TypeCollectionHandle; readonly kind: 'vibe' | 'type';
  readonly title: string; readonly blurb: CopyString; readonly rule: CollectionRule;
  readonly pinned?: readonly ListingId[]; readonly openTier?: Tier;
}
export interface Drop {
  readonly number: number; readonly date: IsoDate; readonly name: string;
  readonly campaignLine?: CopyString;
  readonly newDesignIds: readonly DesignId[]; readonly newListingIds: readonly ListingId[];
  readonly colorChanges: readonly { readonly listingId: ListingId; readonly add?: OptionCode; readonly retire?: OptionCode }[];
  readonly bundlesOn?: readonly BundleId[]; readonly gated?: readonly ListingId[]; readonly flags?: readonly string[];
}
export interface Bundle {
  readonly id: BundleId; readonly title: string;
  readonly slots: readonly { readonly label: string; readonly listingIds: readonly ListingId[]; readonly tiers?: readonly TierOrNone[] }[];
  readonly pairing?: 'same_design_A_then_B';
  readonly discount: { readonly kind: 'fixed'; readonly value: Money };
  readonly headlinePrice: Money;
  readonly availableFrom: IsoDate; readonly availableUntil: IsoDate | null;
  readonly sizeNote?: CopyString; // generated when slot ranges differ (§5.7)
}
export interface MarginException { // catalog/src/margin-exceptions.json
  readonly listingId: ListingId; readonly reason: string;
  readonly approvedBy: 'founder' | 'pending'; // pending: launch: false only; listed in D7
}
export interface SizeGuide {
  readonly id: string; readonly productKey: ProductKey; readonly unit: 'in';
  readonly measurementKeys: readonly string[];
  readonly rows: readonly { readonly size: SizeId; readonly values: Readonly<Record<string, number | readonly [number, number]>> }[];
  readonly source: Sourced<string>; // V or T required for an active listing
}
export interface PricingRules {
  readonly paymentFee: Sourced<{ readonly pct: number; readonly fixed: Money }>;
  readonly mockShipping: { readonly first: Money; readonly additional: Money }; // prototype; threshold: brand.config
  readonly marginFloors: Readonly<Record<'core' | 'entry', { readonly minPct: number; readonly minAmount: Money }>>;
  readonly privateTierDelta: Money; readonly rounding: 'whole_dollar'; readonly sizeUpcharge: 'never';
  readonly discountCodes: readonly { readonly id: string; readonly percent: number; readonly stacks: false; readonly excludes: readonly ('bundles' | 'promo' | 'margin_exception')[] }[];
  readonly growth: { readonly fee: Sourced<Money>; readonly brandingDiscountPct: Sourced<number>; readonly blankDiscountPct: Sourced<number | null> };
}
export interface Catalog {
  readonly version: 1; readonly currency: CurrencyCode;
  readonly snapshotDate: IsoDate; // latest seed checkedAt (2026-11-10), never the wall clock
  readonly pricing: PricingRules; readonly colors: readonly GarmentColor[]; readonly blanks: readonly Blank[];
  readonly designs: readonly Design[]; readonly listings: readonly Listing[]; readonly bundles: readonly Bundle[];
  readonly collections: readonly Collection[]; readonly drops: readonly Drop[]; readonly sizeGuides: readonly SizeGuide[];
  readonly marginExceptions: readonly MarginException[];
}
```

**Zod (`lib/catalog/schema.ts`).** Pin `zod` 4.x live (§3 rule 2). One schema per type (`MoneySchema` … `CatalogSchema`); `tests/types/schema-matches.test-d.ts` checks each `z.infer<typeof XSchema>` is assignable to `X`. `Money` = `z.object({ amount: z.number().int().nonnegative(), currency: z.literal('USD') })`; `Sourced<T>` = a generic `sourced(schema)` helper whose `checkedAt` matches `/^\d{4}-\d{2}-\d{2}$/` and is a real date; IDs use the `ids.ts` regexes. No `.readonly()` on the output; if inferred optionals add `| undefined` under `exactOptionalPropertyTypes`, strip `undefined` keys before validating. **`CatalogSchema.superRefine`** enforces: unique SKUs, each `=== skuFor(...)` of its own fields, with tier, option and size on its listing · pricing rules 1–3 (§5.7); ≤ 100 variants · hero tiers (Quiet and Loud on every apparel listing, Private on every tee listing; sticker, MIX and accessory listings exempt) and ≤ 3 characters on a Loud · the `launch: true` IDs read from `catalog/src/listings.json` equal the §5.5 list unless a logged decision trims it · each `active` listing has a V/T size guide, only `validator.status = "pass"` print files and a mockup per option · §5.3 floors or an exception (`pending` only on `launch: false`) · Tuesday drops; resolvable bundle slots. **Exports:** both exporters always write their files, list every blocker (null partner ids, planning margins, unverified or provisional specs) and exit 1 while any remain; they are not ci gates (§10.2).

**Example A: a tiered CC 1717 tee** (1 of 84 variants shown; the build generates the rest: e.g. `D01-P-CC17-PEP-4XL` prints only `D01.private.cc1717.label_inside.DARK.ANY`, options `["Private","Pepper","4XL"]`, and as 2XL+ has `baseCost.value` null [U], `contribution` null, `marginBasis: "unknown"`)

```json
{
  "id": "D01-CC17",
  "handle": "the-door-tee",
  "title": "The Door tee",
  "designIds": ["D01"],
  "productKey": "cc1717",
  "technique": "dtg",
  "skuCode": "CC17",
  "tiers": ["quiet","loud","private"],
  "defaultTier": "quiet",
  "optionAxis": "color",
  "colors": [
    {"code":"IVR","recipe":"LIGHT","addedInDrop":0},
    {"code":"BAY","recipe":"LIGHT","addedInDrop":0},
    {"code":"CMT","recipe":"LIGHT","addedInDrop":0,"retiredInDrop":7},
    {"code":"PEP","recipe":"DARK","addedInDrop":0},
    {"code":"BTR","recipe":"LIGHT","addedInDrop":7}
  ],
  "sizes": ["S","M","L","XL","2XL","3XL","4XL"],
  "price": {"quiet":{"amount":3400,"currency":"USD"},"loud":{"amount":3400,"currency":"USD"},"private":{"amount":2800,"currency":"USD"}},
  "collections": ["meet-the-crew","the-small-print"],
  "typeCollection": "tees",
  "drop": 0,
  "availability": {"from":"2027-01-05","until":null},
  "status": "draft",
  "visibility": "public",
  "launch": true,
  "copy": {
    "tagline": {"text":"the hard part was the door.","surface":"pdp.tagline","speaker":null},
    "description": {"text":"Bel's first day was scary too. Now Bel rides along on your chest, about the size of a sticker, quietly rooting for you. Heavyweight garment-dyed cotton with a soft, lived-in feel. Same price in every size, {size_range}. Made just for you, so give it a few days.","surface":"pdp.description","speaker":null},
    "tierBlurbs": {"quiet":{"text":"Quiet: a small Bel in a doorway on the left chest. No words.","surface":"pdp.tier","speaker":null},"loud":{"text":"Loud: the whole doorway and the line, big on the back.","surface":"pdp.tier","speaker":null},"private":{"text":"Private: nothing on the outside. The line is printed on the inside label, just for you: {whisper}","surface":"pdp.tier","speaker":null}},
    "seo": {"title":"The Door tee: heavyweight garment-dyed gym tee","description":"A friendly gym tee starring Bel the kettlebell. Quiet chest print, loud back print, or a secret inside label. Same price in every size."}
  },
  "tags": ["bel","hero","frankie","first-visit"],
  "bundleIds": [],
  "crossSell": ["MIX-STK3","D07-W788"],
  "mockups": [
    {"listingId":"D01-CC17","option":"IVR","tier":"quiet","view":"flat_front","src":"/mockups/the-door-tee/IVR-quiet-flat_front.webp","widths":[480,960,1440],"width":1440,"height":1800,"alt":"Ivory tee laid flat with Bel the kettlebell, proud, standing in a small doorway on the left chest","origin":"generated-svg"}
  ],
  "variants": [
    {"sku":"D01-Q-CC17-IVR-M","listingId":"D01-CC17","designId":"D01","tier":"quiet","option":"IVR","size":"M","price":{"amount":3400,"currency":"USD"},"baseCost":{"value":{"amount":1560,"currency":"USD"},"source":"https://www.printful.com/custom/product/586","tag":"T","checkedAt":"2026-11-09","note":"snapshot; replace with /v2/catalog-variants/{id}/prices"},"labelCost":{"amount":99,"currency":"USD"},"contribution":{"amount":1612,"currency":"USD"},"marginBasis":"snapshot","availability":"unknown","printFileIds":["D01.quiet.cc1717.left_chest.LIGHT.ANY","D13.none.cc1717.label_inside.LIGHT.ANY"],"partner":{"printful":{"catalogVariantId":{"value":null,"source":"printful:/v2/catalog-products/586/catalog-variants","tag":"U","checkedAt":"2026-11-10"},"externalId":"D01-Q-CC17-IVR-M"}},"shopifyOptions":["Quiet","Ivory","M"]}
  ],
  "shopify": {"tierMode":"option","productType":"T-Shirt"}
}
```

**Example B: AOP leggings** (gated; planning margin until the live price). Only fields that differ from A; mockups under `/mockups/sneaker-toss-leggings-with-pockets/`.

```json
{
  "id": "D21-L559",
  "handle": "sneaker-toss-leggings-with-pockets",
  "title": "Sneaker Toss leggings with pockets",
  "technique": "cut-sew",
  "tiers": ["none"],
  "defaultTier": "none",
  "colors": [{"code":"LCV","recipe":"FULL-BLEED","addedInDrop":3}, {"code":"LSG","recipe":"FULL-BLEED","addedInDrop":3}],
  "price": {"none":{"amount":5400,"currency":"USD"}},
  "launch": false,
  "gate": {"kind":"squat_test","status":"pending","note":"Ship only grounds that pass the daylight squat test on a size M and one plus size (§8.4)."},
  "copy": {"tierBlurbs": {}, "sizeNote": {"text":"Sizes {size_range}. This cut stops at XL. For more room, try the Sneaker Toss plus-size leggings: same pattern, same price.","surface":"pdp.sizeNote","speaker":null}},
  "variants": [
    {"sku":"D21-N-L559-LSG-M","listingId":"D21-L559","designId":"D21","tier":"none","option":"LSG","size":"M","price":{"amount":5400,"currency":"USD"},"baseCost":{"value":null,"source":"https://www.printful.com/custom/product/559","tag":"U","checkedAt":"2026-11-10","note":"EUR 38.25 incl. NL VAT seen; USD not found"},"labelCost":null,"contribution":{"amount":2013,"currency":"USD"},"marginBasis":"planning","availability":"unknown","printFileIds":["D21.none.aop559.aop_panels.FULL-BLEED.LSG.M"],"partner":{"printful":{"catalogVariantId":{"value":null,"source":"printful:/v2/catalog-products/559/catalog-variants","tag":"U","checkedAt":"2026-11-10"},"externalId":"D21-N-L559-LSG-M"}},"shopifyOptions":["Locker Sage","M"]}
  ]
}
```

**Shopify product CSV** (`exports/shopify-products.csv`): headers follow Shopify's import template as we know it [U]; diff them against the current one before import. One row per variant; product-level columns on each `Handle`'s first row. `Handle` = `listing.handle` (sibling mode `<handle>-quiet`/`-loud`/`-private`) · `Body (HTML)` = description + tier blurbs + made-to-order block, HTML-escaped, after the copy tests · `Vendor` = the brand name from `lib/brand.ts` at export time, never a literal · `Product Category` = Shopify taxonomy [U] · `Type` = `shopify.productType` · `Tags` = `tags` + `collections` + `drop-<n>` + `tier-group-<listing id>` · `Published` `FALSE`, `Status` `draft` (§3 rule 6) · `Option1/2/3 Name`/`Value` per §5.4 · `Variant Price` = cents ÷ 100, 2 dp · `Variant Compare At Price` empty · `Cost per item` = `baseCost.value` (empty if null) · `Variant Grams` = partner weight [U], `Variant Weight Unit` `g` · `Variant Inventory Tracker` empty, `Variant Inventory Policy` `continue` · `Variant Fulfillment Service` `manual` until the Printful app links it [U] · `Variant Requires Shipping`, `Variant Taxable` `TRUE` (tax at checkout, §8) · `Image Src` = hosted mockup URL (empty in the prototype), `Image Position`, `Image Alt Text` = `Mockup.alt`, `Variant Image` = per-colour mockup · `SEO Title`/`SEO Description` = `copy.seo` · `Metafield: custom.tier_group [single_line_text_field]` = `listing.id` (sibling mode; header syntax [U]). Title and `Variant SKU` (the join key) map directly.

**Margins CSV** (`exports/catalog-margins.csv`, written by `export:shopify` only): one row per SKU, sorted by `sku`; columns `sku,listing_id,tier,size,price_cents,base_cents,base_tag,label_cents,fees_cents,contribution_cents,margin_pct,margin_class,floor_ok,margin_basis,exception`.

**Printful mapping** (`exports/printful-sync-plan.json`, written by `export:printful`, §8.3). Sync products are a v1 concept (`sync_product` / `sync_variants`); the v2 SDK has catalog, files, mockups and orders but no sync-product endpoints [T]. Whether the API may create sync products for a Shopify-linked store is **[U]**, so the plan doubles as a click-through checklist for the dashboard.

| Ours | Printful | Note |
|---|---|---|
| `Listing` | sync product: `name` = title, `external_id` = `listing.id`, thumbnail = first mockup | one per listing (option mode) or tier (sibling) |
| `Variant.sku` | sync variant `external_id` (and `sku`) | join key (Shopify) |
| `partner.printful.catalogVariantId` · `Variant.price` | `variant_id` (v1) / `catalog_variant_id` (v2 order items) · `retail_price` (decimal string) | from `/v2/catalog-products/{id}/catalog-variants` |
| `PrintFile` per placement | v1 `files[{ type, url }]`; v2 `placements[{ placement, technique, layers[{ type: "file", url }] }]` | `left_chest`/`right_chest` → `front` and `back_neck` → `back`, uploaded as full 3600 × 4800 canvases with the art already inside the art box; **no API offset** (§6.3.1) · `label_inside` → `label_inside` · names [U] until pulled |
| Embroidery threads · inside label | product options `thread_colors` / `stitch_color` · `inside_label_type` [T] | thread map §6.3.2 |
| Personalised D27/D28 | a per-order file on a **draft** order item | §8 review |

**Catalog tests** (in `npm run ci`): `tests/unit/catalog-schema.test.ts` (Zod + invariants) · `catalog-ids` (IDs, SKUs, handles) · `catalog-margins` · `pricing` · `shipping` · `drops` · `collections` (= §5.6 primaries) · `launch-set` (IDs from `listings.json`, 575 upper-bound SKUs before live pruning, persona coverage) · `banned-words` and `copy-lint` over `catalog/src/*.json`.

---

## 6. Artwork & print-file pipeline

Builds **D2** (design modules, validated print files, manifest) and **D4** (offline mockups, OG images). No print file is hand-placed: each comes from data (`art/designs/designs.json`, `print-specs.json`, `brand/tokens.json`), a design module, the character kit (§4.7, A.5) and the tested helpers in A.7–A.13. Scripts: §10.2.

```text
tokens.json + characters.json + designs.json + print-specs.json (canvases, method rules, threads)
 ─> art/designs/Dxx.ts (layout functions) ─> SVG, px at 300 px/in (art/out/svg/<id>.svg)
 ─> resvg crispEdges ─> key-out + heal (A.8) ─> sharp sRGB ICC, 300 DPI ─> print-files/<D>/<id>.png
 ─> npm run validate:print (A.9, A.10) ─> print-files/manifest.json ─> npm run mockups (A.13) ─> public/mockups/, public/og/
```

### 6.1 Toolchain

Pin exact versions after `npm view` (§3 rule 2). [L] runs used Node 22.23.4; the build uses the §7.1 Node pin.

| Package | Version | Role | Notes |
|---|---|---|---|
| `@resvg/resvg-js` | 2.6.2 [L] | **The only SVG rasteriser** (print, mockups) | MPL-2.0 dev tooling (§3 rule 8); no alphas (`next` = 2.7.0-alpha.2) |
| `sharp` | 0.35.5 [L] | PNG encode (ICC, pHYs), resize, WebP/AVIF, raw decode | Node ≥ 20.9.0. **Never renders SVG.** |
| `opentype.js` | 2.0.0 [L] | Text → outlined paths | `parse()` only; `loadSync` is deprecated |
| `@expo-google-fonts/caprasimo` | 0.4.0 [L] | Print TTF `400Regular/Caprasimo_400Regular.ttf` | OFL-1.1 |
| `@expo-google-fonts/atkinson-hyperlegible-next` | 0.4.1 [L] | Print TTF `800ExtraBold/AtkinsonHyperlegibleNext_800ExtraBold.ttf` (also `700Bold`, `400Regular`) | OFL-1.1 (wrapper MIT) |
| Web WOFF2 packages | §7.1 | **Web only** | Never loaded by `art/` |
| `zod` | 4.x, §5 pin | `print-specs.json` schema | — |
| Not used | — | `svgo` on print SVGs (rewrites paths), `text-to-svg` (stale since 2022), Inkscape, Cairo, librsvg | System deps or silent font substitution |

**Known pitfalls** (every fix is mandatory and guarded):

| # | Pitfall [L unless noted] → symptom | Fix | Guard |
|---|---|---|---|
| 1 | resvg ignores WOFF/WOFF2 → 0 ink pixels, no error | TTF only; art has no `<text>` | SVG lint; "empty file" |
| 2 | opentype.js 2.0.0 `toPathData()` emits literal `NaN` (828 of 1,082 fractional offsets tested); resvg stops at the first bad token → half a glyph | Serialise `path.commands` yourself (A.5 `ser`); throw on `NaN` | SVG lint `NaN` |
| 3 | Caprasimo's GSUB `ccmp`: `getPath(string)`/`stringToGlyphs()` throw "substFormat: 2 is not yet supported" | Per-glyph `charToGlyph` + `getKerningValue` (A.5 `textPath`) | Test outlines every `designs.json` slogan |
| 4 | WOFF2 needs a decompressor; `loadSync` is deprecated | `opentype.parse()` on the TTF's exact bytes (A.5 `loadFont`) | — |
| 5 | Missing glyph (e.g. "×" U+00D7 in D24) → `.notdef` box or a silent "x" | Throw on `glyph.index === 0` (as A.11 does; add to A.5 `textPath`/`fitText`) | Test with D24's lines |
| 6 | `sharp`/librsvg draws `<text>` in any system font (Inter for Fredoka) → a plausible wrong font | Always outline text; SVG goes only to resvg | SVG lint `<text>` |
| 7 | `width="12in"` renders at 96 DPI → 1152 × 1536 | Author in **px**, `viewBox` at 300 px/in; `fitTo: { mode: 'width', value: spec px }`; assert the size (A.8 throws) | Size check |
| 8 | resvg writes no pHYs → files read as 72 DPI | `sharp(...).withMetadata({ density: 300 })` (pHYs 11811 px/m) | Warn if density ≠ spec |
| 9 | Anti-aliasing leaves semi-transparent edges (0.24% of ink at 3600 × 4800; Bel at 900 px: 3,100 semi pixels) → underbase halos on dark shirts | Print renders use `shapeRendering: 1` (crispEdges) → 0 semi pixels; mockups keep anti-aliasing | Alpha ∈ {0, 255} |
| 10 | `extractChannel(3).threshold().joinChannel()` → a fully opaque rectangle | Key out in a raw RGBA buffer (A.8) | Transparency counts |
| 11 | Keying out `oat` leaves 8 px slivers (sole stripe vs sneaker outline, box 1950) and 1 px pinholes (tubes meet bodies) → garment-colour hairlines | `healKnockouts()` fills enclosed knock-outs under the method minimum with a neighbouring colour and logs each (A.8, A.9) | Manifest warnings; §6.7 |
| 12 | Each silent failure above still yields a valid PNG | Validate every file (§6.6) | `npm run ci` |
| 13 | DPI metadata is cosmetic: both partners judge **pixel dimensions at the placed size**; no source says either reads pHYs [U] | Pixel size is the contract; write 300 DPI for humans | — |
| 14 | Printify SVG limits: no `<text>`, ≤ 20,000 paths, ≤ 20 MB [V] | **PNG only** (no Printify item in year one) | — |

**Fonts and licences.** `art/fonts.ts` resolves the two print TTFs from `node_modules`, refusing any other font. `licenses/fonts.json` (written once by hand in M1 with a fixed `checkedAt`; `npm run brand` only verifies its hashes) has one entry per family and use: `{ family, weights, use: ["web"|"print"], package, version, file, sha256, license: "OFL-1.1", licenseFile, source, checkedAt }`; each `OFL.txt` goes to `licenses/OFL-<Family>.txt`. **The OFL allows printed merchandise and outlined glyphs** [V] (OFL FAQ); only selling the font file is restricted. `tests/unit/fonts.test.ts` fails on an unlisted font in `art/`, a `sha256` mismatch, or a WOFF/WOFF2 path under `art/`.

### 6.2 `print-specs.json`

One root file holds **every** canvas, art box, DPI, method rule and thread colour; generators, validators, mockups and the Printful exporter read print geometry **only** from it (they get a `spec`, no size constants). `tests/unit/print-specs.test.ts` fails on a seeded canvas literal (`/\b(3600|4800|1890|1749|2481|7200)\b/`) in code under `art/print/`, `art/mockups/`, `art/lib/` or `scripts/` (comments ignored); design modules use them only as their `designSpace` (§6.4.3). **Geometry changes are data edits, never code:** a different template (say a 3600 × 4500 back) = a `print-specs.json` edit + `npm run art`, which refits (§6.5) and re-checks every design.

**Types** (`art/print/spec-types.ts`; imports `PrintAreaSpec` and the rest from `lib/catalog/types.ts`, redeclares nothing):

```ts
import type { PrintAreaSpec, Sourced, SizeId, VerificationTag } from '../../lib/catalog/types';
export type RuleSet = 'garment' | 'label' | 'embroidery' | 'hardgoods' | 'stretch';
export interface MethodRules {  // physical units: px = in × spec.dpi (A.10 takes px)
  readonly minStrokeIn: Sourced<number>;  // positive ink element
  readonly minKnockoutIn: Sourced<number>;  // enclosed gap / reversed line (after heal)
  readonly minXHeightIn: Readonly<Record<'caprasimo' | 'atkinson', Sourced<number | null>>>; // null = font not allowed
  readonly minCapHeightIn?: Sourced<number>;
  readonly safeMarginIn: Sourced<number>;
  readonly minEdgeContrast: Sourced<number>;  // WCAG ratio, edge colours vs the garment
  readonly primaryEdgeShare: number;  // 0.10: edge share above which a colour is "primary"
  readonly mergeDeltaE: Sourced<number>;  // ΔE00 below this = merge (fail)
  readonly cautionDeltaE: Sourced<number>;  // below this = "sample first" (warn)
  readonly maxColours?: Sourced<number>;  // embroidery threads
  readonly textAllowed: boolean;
}
export interface AreaExtras {  // fields PrintAreaSpec lacks, keyed by PrintAreaSpec.key
  readonly ruleSet: RuleSet;
  readonly artMaxPx?: readonly [number, number];  // e.g. hoodie front ≤ 3600 × 3000 (pouch)
  readonly reservedPx?: readonly { x: number; y: number; w: number; h: number; why: string }[];
  readonly perSizeTemplates?: Readonly<Partial<Record<SizeId, { canvasPx: readonly [number, number]; source: Sourced<string> }>>>;
  readonly tileIn?: number;  // AOP: physical tile size
  readonly provisional?: true;  // placeholder (no partner number): warn + block export
  readonly note?: string;
}
export interface PrintSpecsFile {
  readonly version: 1;
  readonly limits: { readonly maxBytes: Sourced<number>; readonly maxSidePx: Sourced<number> };
  readonly rules: Readonly<Record<RuleSet, MethodRules>>;
  readonly threads: readonly { readonly name: string; readonly number: string; readonly hex: `#${string}`; readonly tag: VerificationTag }[];
  readonly areas: readonly PrintAreaSpec[];  // key = `${productKey}.${placement}`
  readonly extras: Readonly<Record<string, AreaExtras>>;
}
```

**`verified` and sources.** Each area's `verified` is a `Sourced<boolean>`: `source`/`tag` give the origin of the canvas and art-box numbers; `value` turns `true` only after a check against the partner's downloaded template or `GET /v2/catalog-products/{id}/mockup-templates`, URL or file recorded. `partnerPlacement` and every rule value are `Sourced` too. Zod (`PrintSpecsSchema`): every key matches `^[a-z0-9]+\.[a-z_0-9]+$` and joins to a `ProductKey` and `PlacementId`; every area has extras; `artBoxPx` fits `canvasPx`; `maxSidePx` holds. `validate:print` **warns** per unverified spec used; `export:printful` **fails** on any file using an unverified or `provisional` spec (expected in the prototype: D7 lists them).

**Limits:** `maxBytes` 100,000,000 (Printify's PNG cap; Printful says 200 MB in one article, 100 MB in another: use the lower) [V]; `maxSidePx` 20,000 [V].

**Rule sets** (seeds; px at 300 DPI unless noted; transparent background except `hardgoods` per area, `stretch` full bleed; [U] = our conservative heuristic, not a partner rule, until a sample confirms it, §8 QA)

| Rule | `garment` (DTG/DTF) | `label` (inside neck) | `embroidery` | `hardgoods` (stickers, sheet, bottle, towel, notebook) | `stretch` (leggings, bra, shorts, socks) |
|---|---|---|---|---|---|
| Min positive stroke | 0.04 in = 12 px [U] | 0.04 in [U] | 0.05 in = 15 px [V] | 0.04 in [U] | 0.04 in = 6 px @150 [U] |
| Min knock-out / gap | 0.06 in = 18 px [U] | 0.06 in [U] | 0.05 in = 15 px [V] | 0.06 in [U] | 0.04 in [U] |
| Caprasimo x-height | ≥ 0.667 in = 200 px [L/U] | not allowed | ≥ 0.556 in = 167 px, large front only [L/U] | ≥ 0.2 in = 60 px [U] | no text |
| Atkinson 800 x-height | ≥ 0.367 in = 110 px [L/U] | cap height ≥ 0.1 in = 30 px [U] | ≥ 0.30 in = 90 px [V/L] (partner: text ≥ 0.25 in lowercase, 0.3 in caps [V]) | cap height ≥ 0.1 in (x-height ≥ 22 px) [U] | no text |
| Safe margin | 0.25 in = 75 px [U] | 0.25 in [U] | 0.1 in [U] | 0.125 in [U] (stickers: the halo is the die line) | n/a (full bleed) |
| Edge contrast vs garment | ≥ 3:1 [U] | ≥ 3:1 [U] | ≥ 3:1 [U] | n/a | n/a |
| ΔE00 merge / caution | < 12 fail / < 18 warn [L rule] | — | < 12 / < 18 | — | — |
| Max colours | — | — | 6 threads [V]; the Bel face ≤ 3 | — | — |

**Seeded areas** (`areas[]` + `extras`; `verified.value` `false` for **every** row until the live check; 300 DPI, transparent, unless noted):

| Key | Tech. | Canvas px | Art box `{x,y,w,h}` / extras | Partner placement | Rule set | Source of numbers |
|---|---|---|---|---|---|---|
| `cc1717` · `bc3001` `.front` | dtg | 3600 × 4800 | — | `front` | garment | 12 × 16 in [V] Printful file guide |
| `cc1717` · `bc3001` `.back` | dtg | 3600 × 4800 | — | `back` | garment | assumed = front [U] |
| `cc1717` · `bc3001` · `g18000` · `cc1566` · `g18500` `.left_chest` | dtg | 3600 × 4800 | `{2325,150,1050,1050}` | `front` | garment | box [U] (§6.3.1) |
| `cc1717.right_chest` | dtg | 3600 × 4800 | `{225,150,1050,1050}` | `front` | garment | [U]; D08 B Quiet only |
| `cc1717.back_neck` | dtg | 3600 × 4800 | `{1350,150,900,600}` | `back` | garment | [U] |
| `cc1717` · `bc3001` `.label_inside` | dtg | 900 × 900 | reserved `{0,640,900,260}` (Printful's auto text) | `label_inside` | label | 3 × 3 in [V]; some blanks 600/750 [V]; reserved zone [T/U] |
| `cc1717.sleeve_left` | dtg | 1200 × 1050 | unused in year one | `sleeve_left` | garment | 4 × 3.5 in [V] |
| `g18000.front` · `.back` · `cc1566.front` · `.back` · `g18500.back` | dtg | 3600 × 4800 | — | `front` / `back` | garment | assumed tee-like [U] |
| `g18500.front` | dtg | 3600 × 4800 | `artMaxPx [3600,3000]` (clears the pouch) | `front` | garment | [U] |
| `g18000.emb_chest` | embroidery | 1200 × 1200 | — | `embroidery_chest_left` [U name] | embroidery | 4 × 4 in [V] |
| `y6245cm.hat_front` | embroidery | 1890 × 768 | `{270,84,1350,600}` | `embroidery_front` [U name] | embroidery | 6.3 × 2.56 in [V]; art box [T] |
| `y1501kc.beanie_cuff` | embroidery | 1500 × 525 | — | [U] | embroidery | 5 × 1.75 in [V/T] |
| `patch3.patch_face` | embroidery | 900 × 900 | `provisional` | [U] | embroidery | 3 in patch [U] |
| `m7580.left_hip` | dtg | 1200 × 1200 | `provisional`; falls back to the left-leg placement | [U] | garment | **placeholder** [U] |
| `ec8000.tote_front` | dtg | 3000 × 3300 | `provisional` | `front` [U] | garment | **placeholder** = D26's assumed 10 × 11 in [U] |
| `sticker3.sticker_3in` | digital | 900 × 900 | die line = the art's halo | [U] | hardgoods | 3 in [V]; px [T] |
| `sheet505.sticker_sheet` | digital | 1749 × 2481 | transparent **[U]** (`full_bleed` if the template says so) | [U] | hardgoods | 5.83 × 8.27 in [T] |
| `bottle788.wrap` | [U] | 3000 × 1500 | `provisional`; full bleed | [U] | hardgoods | **placeholder** (no spec found) [U] |
| `towel883.towel_face` | sublimation | 4800 × 8400 | `provisional`; full bleed | [U] | hardgoods | 16 × 28 in product [T]; template [U] |
| `notebook474.notebook_cover` | [U] | 1650 × 2550 | `provisional`; full bleed | [U] | hardgoods | **placeholder** [U] |
| `aop559` · `aop334` `.aop_panels` | cut-sew | 7200 × 6225 @150 | `perSizeTemplates` (empty until pulled), `tileIn 6`, `provisional`, full bleed | [U] | stretch | ≈ 48 × 41.5 in [U] |
| `aop477.aop_panels` | cut-sew | 3750 × 3300 @150 | as above | [U] | stretch | ≈ 25 × 22 in [U] |
| `aop507.aop_panels` | cut-sew | 7050 × 2700 @150 | as above | [U] | stretch | ≈ 47 × 18 in [U] |
| `socks882.aop_panels` | sublimation | 2400 × 3000 @150 | as above | [U] | stretch | **placeholder** (no spec found) [U] |

**Placeholder** = no number found: it only lets the pipeline run end to end; never quote it as a spec.

### 6.3 Spec tables by method

#### 6.3.1 DTG / DTF (tees, crews, hoodies, joggers, tote) and inside labels

**Where art sits** (canvas px at 300 DPI, top-left origin):

| Placement | Rule |
|---|---|
| `front`, `back` | Design space 3600 × 4800, top-aligned with a 150 px top margin; art ≤ 4200 px tall (ends above the hem); 75 px safe margin; one file for every size. The 15 × 18 in `front_large` area (select products and sizes, e.g. B+C 3001 L–5XL [V]) is **not used in v1**. |
| `front` on hoodies | Art ≤ 3600 × 3000, top-aligned, to clear the kangaroo pouch [U]. D09's ring text fails at that size, so the crest is a **back** print. |
| `left_chest` | **Wearer's left = the RIGHT side of the canvas.** Box 1050 × 1050 (3.5 in) centred at (2850, 675), top-left (2325, 150), inside the full front canvas (works with any upload path); a box-only file plus an API offset is [U] and not used. |
| `right_chest` | Mirror, centred at x 750. Only D08 B's Quiet, so the two halves face each other. |
| `back_neck` | Box `{1350,150,900,600}` (900 × 600, top-centred, top at y 150) on the `back` placement: one placement, like any Quiet. |
| `label_inside` | 900 × 900 (some blanks 600 or 750: scale everything with the label). Atkinson 800 **only**. Bel at Icon LOD (§4.7), box 375, centre x 450, top y 40. Whisper on 2 lines at x-height 30 px (cap ≈ 0.14 in), centred x 450, baselines 470 and 550. **y 640–900 stays empty** for Printful's auto-filled size, fibre and origin [T]; **no size letter in our art**. Light garments `ink`; dark garments `oat` text plus a reversed icon (`oat` line, `coral` body). Tees only, never fleece [T]. |

**Ink rules** (values: §6.2 `garment` rule set; recipes §6.4.4):
- **Light garments:** white does not print without an underbase [T], so `oat`, `canvas` and `white` are exported transparent (LIGHT recipe).
- **Dark garments:** ink and near-garment colours vanish [T], so DARK uses the `oat` halo (§6.4.4).
- DTF (`dtfilm`, Printful "DTFlex" [T]) takes the same files. Prefer DTG for large solid panels (D17's menu board).

Hex priority: live `color_code`, then `GarmentColor.approxHex` (§5.2); checks on [U] hexes warn only.

#### 6.3.2 Embroidery (dad hat, embroidered crew, beanie, patches)

```text
EMBROIDERY RULES (Printful [V]; Printify publishes the same palette and limits)
- Off-palette colours get auto-mapped, so we export the exact thread hexes ourselves. Details under the
  §6.2 minimums are enlarged, turned into run stitch or REMOVED by the digitiser.
- No unlimited-colour thread in v1 (§2 decision 20). No 3D puff in v1: hats only, needs 0.2–0.5 in
  columns and can't mix with flat in one area [T]; Bel's body is ≈ 1.6 in wide.
- Max areas: chest 4 × 4 in; large front 10 × 6 in (extra fee); sleeve 2 × 3; hat front file 6.3 × 2.56
  (dad-hat art ≈ 4.5 × 2 in); beanie 5 × 1.75; hat side/back ≈ 2.5 × 1 [U].
- Digitisation $2.95–6.50 one-time per design and placement; re-digitised if resized or moved [V/T].
```

**Thread palette** [V] (seeds `print-specs.json` `threads[]`):
White 1801 `#FFFFFF` · Black 1800 `#000000` · Grey 1718 `#96A1A8` · Navy 1966 `#333366` · Aqua/Teal 1695 `#3399FF` ·
Purple 1832 `#6B5294` · Maroon 1784 `#660000` · Red 1839 `#CC3333` · Flamingo 1910 `#CC3366` · Orange 1987 `#E25C27` ·
Gold 1951 `#FFCC00` · Old Gold 1672 `#A67843` · Kiwi Green 1848 `#7BA35A` · Kelly Green 1751 `#01784E` · Royal 1842 `#005397`

**Token → thread map** (canonical, used by the exporter; nearest ΔE00 [L], reproduced by A.7 `nearest()`; no pastel threads exist). Any other token in an embroidery file fails the build.

| Token | Thread (ΔE00) | Use |
|---|---|---|
| `ink` | Navy 1966 (10.8); runner-up Black 1800 (14.7): sample both | Outlines, features |
| `oat` | White 1801 (5.7) | Halo on dark garments |
| `coral` | Orange 1987 (12.6) | Bel's body; reads stronger than screen coral (accepted) |
| `butter` | Gold 1951 (7.3) | Pop, sparkles, Gus's grip wrap |
| `coral-deep` | Red 1839 (6.6) | Small accents |
| `lilac-deep`, Mallow line art | Purple 1832 (5.9) | One-colour line art |
| `sage`, Gus line art | Grey 1718 (17.0; Kiwi Green 1848 is 15.0: neither close) | One-colour line art (§2 decision 20) |
| `bubblegum` (used only as blush, when the expression needs it) | Flamingo 1910 (nearest is White, 25.1) | Blush |
| `lilac` · `pool` · `pistachio` | none close (Grey 19.4 · Grey 18.9 · Kiwi Green 17.4) | Mallow's body would need unlimited colour (§2 decision 20): Purple line art; `pool`/`pistachio`: avoid |

- **Recipes:** LIGHT (Ivory, Stone, Sand, Khaki, Sage, Heather Grey) = Navy + Orange; DARK (Navy, Pepper, Charcoal, Dark Heather) = White halo +16 u, Orange body, Navy features; TONAL-INK = one-thread line art.
- The manifest records `meta.threads` per file. §8's sync uses it to fill Printful's `thread_colors` option [T].

#### 6.3.3 All-over print (sublimation / cut-and-sew)

- **Templates are per product and usually per size** [V]: one file per size (`…FULL-BLEED.<ground>.<size>`); until `perSizeTemplates` is filled, render the one provisional canvas, flagged.
- **150 DPI** for cut-and-sew [V Printful]. Patterns: **6 × 6 in seamless tiles at 300 px/in (1800 px)** at a **fixed physical scale** (same motif size on XS and 6XL), anchored on the panel's centre line (A.12 `fillPanel`).
- **100% coverage through the bleed; zero transparent pixels** [V]. Front-to-back alignment is not guaranteed [V]: keep key motifs off seams and waistbands.
- **No text on stretch panels** (leggings, bra, shorts, socks), no precise geometry (checks, stripes); multi-directional tossed motifs so back panels read upside down. **No dark grounds on leggings** (undyed white shows at stretched seams [T]); `INT` Ink Night is socks-only.
- Tiles: toroidal Poisson-disc spacing per design, seeded RNG (§3 rule 16); overlap and seam checks per §6.6 #18 (A.12).
- Leggings stay `draft` until the squat test passes (§5.4); the art still renders.

#### 6.3.4 Accessories and paper: status and the paste procedure

| Product (key) | What we know (canvas: §6.2) | Rules |
|---|---|---|
| 3 in kiss-cut sticker (`sticker3`) | 300 DPI; Printful adds the white border; transparent areas print white [V]; 900 × 900 px [T] | One opaque island per sticker; die line = the `oat` halo (+16 u). No enclosed holes: export heals with `minKoPx = Infinity` (also filling the handle window the halo nearly closes). No thin protrusions. |
| Sticker sheet (`sheet505`) | §5.3 | D11 3 × 3 grid; transparent vs full-bleed ground [U]: D11 supports both via `spec.background` |
| 32 oz bottle wrap (`bottle788`) | Print method and wrap size not found [U] | D07 is wrap-relative (§6.4.7), so it survives any real size |
| Socks (`socks882`) | ≥ 150 DPI full bleed, key art in the safe area [V] | Stretch rules; pattern only |
| Hand towel (`towel883`) | §6.2 | Hard-goods minimums; sublimation mutes colours slightly [T] |
| Tote (`ec8000`) | Print area not found [U] | Garment rules (DTG); D24 uses the short receipt if the area is < 11 in wide |
| Notebook (`notebook474`) | Cover template [U]; interior is Printful stock | 300 DPI full-bleed cover; spine and back per template |

**Paste procedure** (founder or build session, once a Printful account exists; for every row with `verified.value` `false`):
1. Download Printful's **File guidelines / template** per placement (AOP: **per size**) from the product creator, or run `npm run catalog:pull -- --live` (saves `GET /v2/catalog-products/{id}/mockup-templates` to `catalog/live/printful/<id>.mockup-templates.json`).
2. Save templates as `art/templates/<productKey>/<placement>[.<size>].<ext>` (git-ignored if > 10 MB; SHA-256 in `art/templates/index.json`).
3. Copy the **print-file pixel size** (not the inches) into `canvasPx`, the safe area into `artBoxPx` (AOP: `perSizeTemplates[size]`) and the exact placement id into `partnerPlacement.value`.
4. Set `verified: { value: true, source: "<template URL or file>", tag: "V", checkedAt: "<today>" }`; delete `provisional`.
5. Run `npm run art && npm run validate:print`: every design is refitted (§6.5) and any that now breaks a minimum fails by name.
6. Commit as `specs: verify <key> from template`; note it in `docs/decisions.md`.

### 6.4 Design-as-code

#### 6.4.1 Layout of `art/`

Paths: §10.1 `art/` subtree. Layout ids resolve through `art/designs/index.ts`.

#### 6.4.2 `designs.json` rules

- One `Design` (§5.10) per D-number, from §6.4.7–6.4.8 and §5.4 (products, listings, colours).
- `variants[tier].layout` is `"<D>.<tier>"`, `"<D><part>.<tier>"` or `"label.whisper"`. `canvas` is the layout's **design space**; the real canvas always comes from `print-specs.json`.
- **Text is stored exactly as cleared, in lowercase**, format labels included (crest rings, receipt "total", menu footer, Firsts labels): the layout sets caps, so copy-lint's ALL-CAPS rule (§4.4 #9) sees lowercase.
- Placeholders are stored lowercase and upper-cased by the layout: `{brand}` (`brand.config.json` `name`); per order `{crew_name}`, `{month}`, `{year}`. Previews: crew name "your crew", the year of `AS_OF` (`lib/site.ts`, default 2027), month "jan". The `copy-placeholders` test registers the four as print-only providers.
- `whisper: null` = the D13 default whisper.
- Every printed line and whisper is also in `content/print-lines.json` (`{ text, surface: "print", speaker }`) for banned-words and copy-lint. `tests/unit/designs.test.ts` fails on a `designs.json` line missing there (§3 rule 10) and on a `Design.name` failing the banned-words `names` scope.

#### 6.4.3 Module interface

```ts
// art/designs/types.ts (canonical ids from lib/catalog/types.ts)
import type { DesignId, DesignPart, TierOrNone, PlacementId, ProductKey, ColourRecipe, ColorCode, SizeId, CharacterId, ExpressionPreset, TokenName, PrintAreaSpec } from '../../lib/catalog/types';
import type { AreaExtras } from '../print/spec-types';
export interface RenderInput {
  readonly designId: DesignId; readonly part?: DesignPart; readonly tier: TierOrNone; readonly placement: PlacementId; readonly productKey: ProductKey;
  readonly recipe: ColourRecipe; readonly garment: { readonly code: ColorCode; readonly hex: string; readonly isDark: boolean } | null; // null = paper/AOP
  readonly spec: PrintAreaSpec; readonly extras: AreaExtras; readonly size?: SizeId;
  readonly personal?: { readonly year?: number; readonly crewName?: string };
  readonly swaps: readonly { readonly from: TokenName; readonly to: TokenName }[]; // accent swaps resolved for this garment
}
export interface Layer { readonly cls: 'character' | 'smallProp' | 'largeProp' | 'text' | 'ground'; readonly svg: string; readonly unitPx: number } // unitPx = px per 240-grid unit (halo width)
export interface RenderOutput {
  readonly designSpace: readonly [number, number];  // nominal size the coordinates in §6.4.7 assume
  readonly layers: readonly Layer[];  // composed by lib/recipes.ts (halo, key-out, swaps)
  readonly meta: {
    readonly texts: readonly { text: string; font: 'caprasimo' | 'atkinson'; xHeightPx: number; capHeightPx: number }[]; // design-space px
    readonly characters: readonly { id: CharacterId; expression: ExpressionPreset; pose: string; lod: 'full' | 'xs' | 'icon' | 'emb' }[];
    readonly minStrokePx: number;  // thinnest authored stroke × scale (pre-check before pixels)
    readonly edgeBleed?: boolean;  // D08 bars only
    readonly maxThreads?: number; readonly threads?: readonly string[];
    readonly alt: string;  // "{Name} the {object}, {expression}, {pose}"
  };
}
export type Layout = (input: RenderInput) => RenderOutput;
```

- Every layout is **pure and deterministic** (no `Date` or `Math.random`; patterns take an explicit seed). `fitText`/`fitArc` **throw** below the surface minimum (A.5, A.11): a build failure, by design.
- `tests/unit/designs.test.ts` renders every variant × recipe on a fixture garment: no throw; ≤ 3 characters on a Loud; character fills ⊆ own tokens ∪ {`ink`, `oat`, `white`, blush}; no SVG `<text>`, `NaN`, `opacity`, gradient, `<filter>` or `<image>`.

#### 6.4.4 Colourway engine (`art/lib/recipes.ts`)

| Recipe | Garments | Key-out (exported transparent) | Layers |
|---|---|---|---|
| `LIGHT` | `ink` ≥ 4.5:1 against the garment | `oat`, `canvas`, `white` (eye highlights drop: accepted) | as drawn; `ink` text |
| `DARK` | `isDark` (D in §5.2: Pepper, Espresso, Blue Jean, Navy, Dark Heather, Charcoal) | none | `character` + `smallProp` layers get `halo()` underneath (+16 u at their own `unitPx`); the layout draws `largeProp` layers as `oat` line art (`props.lineArt()`); text `oat` (one accent word or line may be `butter`; `coral` only at display size on Navy or Espresso) |
| `GARMENT-FILL` | a body fill is ΔE00 < 12 from the garment | LIGHT set **plus** the merging fill (and its shade, e.g. `lilac-shade`) | accents keep their colour |
| `TONAL-INK` / `TONAL-OAT` | one-colour budget prints; embroidery line art | every fill | strokes and ink features stay `ink` (or `oat`) |
| `FULL-BLEED` | AOP, paper, stickers' own grounds | none | the ground prints |

- `ListingColor.recipe` (§5.4) is re-checked against the garment hex; the build fails when a LIGHT garment has `ink` < 4.5:1, a dark garment isn't DARK, or a character body fill is ΔE00 < 12 from the garment without GARMENT-FILL (or an accent swap). ΔE00 12–18 logs "sample first".
- **Garment bans** (test): Mallow (`lilac`) never on Butter; Pop's `butter` never on lilac garments; Pip never on Blossom (D08 A); Pop never on Butter (D08 B); never Watermelon with Bel; no black garments.
- `swaps` (`designs.json` `colourways.accentSwaps`, e.g. sparkles, D04 grip wrap and zip pull, D22 headphones) apply to every layer and never target a character's **body** colour: characters are never recoloured (§4.7). The cast test allows exactly the declared swaps.

#### 6.4.5 Shared primitives (`art/lib/`, building on A.5)

- `place(svg, cx, groundY, boxPx)` puts a 240-grid character's x 120 on `cx` and its ground line (y 216) on `groundY`.
- `art/characters/lod.ts` `lodFor(boxIn, technique)` → `'full' | 'xs' | 'icon' | 'emb'` per the §4.7 LOD table; cast builders: A.5 exports. `halo()`/`onDark()` live in `kit.ts`; `art/lib/halo.ts` re-exports them plus the per-layer `unitPx` wrapper used by `recipes.ts`.
- New builders, each spec'd in §6.4.7–6.4.8: expression preset `reading`; Gus `hold-sign`; Bel headphones; embroidery-LOD Bel (D10) and Mallow (D15); the pattern sneaker with a second lace tick; `pippopHalf('A'|'B')`.
- Text: `textPath`/`fitText` (A.5) fit ≤ 86% of the frame, capped at the design size, **throwing below the minimum**; add a glyph-index-0 check and `capHeightPx` (`os2.sCapHeight`). `arcText`/`fitArc` (A.11); `centredLine(font, str, xh, cx, baseline, fill)` (Caprasimo tracking −0.01 em).
- Props (`props.ts`; outlines 6 u unless given): `sparkle(cx, cy, r)` (4-point Q-curve star, `butter`), `heart(x, y, scale)` (D03's unit heart), `doorway`, `locker`, `dustPuff(x, y, k)`, `motionTicks`, `floor(x0, x1, y, w)`, `stamp`, `dashedRing`, `checkbox(x, y, s, ticked)`, `receipt`, `menuBoard`, `notepad`, `gauge`, `lineArt(svg, colour)` (fills → `none`, strokes → `colour`).

#### 6.4.6 One character source for print and web

- `art/characters/kit.ts` exports pure functions returning SVG strings, coloured from `art/palette.ts`. The site's `<CastMember id expression pose lod garment size title />` (`components/cast/CastMember.tsx`, §4.7, built in §7) calls **the same functions** inside `<svg role="img" aria-labelledby>` with the generated alt; on the web `garment` only picks halo (dark section) or plain.
- Tests: `<CastMember id="bel" expression="happy" pose="idle" />` matches the geometry of the A.5 fixture `tests/fixtures/bel-happy-idle.svg` (snapshot); print imports `kit.ts`, never `components/`; a grep test fails if `art/` imports React or touches `document`.

#### 6.4.7 Launch designs D01–D13: layout parameters

**Conventions.** Design-space px at 300 px/in (3600 × 4800 front/back; 1050 × 1050 chest boxes). "Box N" = a character's 240 grid at N px (u = N/240) via `place(…, cx, groundY, N)`. Strokes `ink`, text centred on x 1800, unless stated. Cap = Caprasimo; Atk = Atkinson Hyperlegible Next 800; xh = x-height px. **DARK = the §6.4.4 default unless the row says otherwise**; rows list only deviations. [L] rows were rendered and inspected; others are specified only (render, then §6.7). Slogans and whispers are exact.

| ID · name | Text (exact) | Loud | Quiet / other placements | Colourways (garment targets per §5.4) |
|---|---|---|---|---|
| **D01** The Door · Bel *proud cheer* | Cap xh 225: "the hard part" / "was the door." · whisper "(psst. the hard part" / "was the door.)" | Back [L]. Doorway `M975 2400 L975 1125 A825 825 0 0 1 2625 1125 L2625 2400 Z` `oat`, 45. Leaf `M1020 1180 L1290 1300 L1290 2330 L1020 2400 Z` `canvas`, 30. Knob (1245, 1850) r 30 `butter`, 16. Floor `M600 2400 H3000`, 45, round caps. Bel box 1950, cx 1880, ground 2400. Sparkles (760, 640) r 120, (2880, 980) r 90, 24. Baselines 2960, 3510. | Left chest: doorway `M150 1000 L150 525 A375 375 0 0 1 900 525 L900 1000 Z`, 20; floor `M60 1000 H990`, 20; Bel *proud idle* XS box 760, cx 525, ground 1000; sparkle (960, 180) r 55; no text. Hoodie: same Loud (back) and Quiet. | LIGHT; Butter → sparkles `coral`. DARK. |
| **D02** The Little Sticker · Bel *reading idle* (`reading` = determined brows, pupils +4 x / −2 y) | Atk xh 150 "currently reading" · Cap xh 300 "the little" / "sticker" · Atk xh 150 "on the machine." · whisper "(psst. you're allowed" / "to be new.)" | Front. Machine x 2250–2950, y 300–2050, rx 80, `canvas`, 40. Knob (2600, 450) r 60 `butter`, 24. Sticker x 2330–2870, y 950–1300, rx 30, `oat`, 24; bars (22) at y 1040 / 1120 / 1200 from x 2400 to 2800 / 2740 / 2640. Bel box 1700, cx 1250, ground 2050. Floor `M300 2050 H3300`, 40. Baselines 2500 (Atk), 3050, 3650 (Cap), 4000 (Atk). | Bel *reading* XS box 700, cx 400, ground 1000; mini sticker x 760–1000, y 480–660, `oat`, 18, 2 bars. | LIGHT (B+C). DARK Navy: the sticker keeps its `oat` fill and bars. |
| **D03** Off Camera, On Purpose · Tuck *shy* | Cap xh 240: "off camera," / "on purpose." · whisper "(psst. off camera," / "on purpose.)" | Back. Tuck box 2000, cx 1350, ground 2300. Camera x 2250–3150, y 1500–2100, rx 90, `oat`, 45; bump x 2420–2700, y 1400–1520, rx 30. Heart: unit heart `M0 0.3 C0 -0.1 0.5 -0.1 0.5 0.3 C0.5 -0.1 1 -0.1 1 0.3 C1 0.6 0.5 0.85 0.5 1 C0.5 0.85 0 0.6 0 0.3 Z` ×300 at (2550, 1650), `coral`, 36. Shelf `M2150 2100 H3250`, 45. Baselines 2900, 3450. No lens rings, no recording dot. | **Back-neck** (900 × 600): Tuck XS box 900, top 55% only, cut by a straight `ink` line (9 u) at the bottom edge ("peek"); no text. Sticker: Quiet art + Atk "off camera," / "on purpose." xh 40. | **DARK is the hero colourway** (Tuck's `oat` towel prints); the camera is haloed, not line art. LIGHT: the towel becomes garment colour (accepted). |
| **D04** Long Time No Gym · Gus *chill wave* | Cap xh 300: "long time" / "no gym." · whisper "(psst. welcome back." / "no catching up.)" | Front [L]. Baselines 650, 1300. Locker x 1000–2600, y 1500–3700, rx 40, `canvas`, 45. Door `M2600 1500 L3150 1650 L3150 3550 L2600 3700 Z` `oat`, 45. Vents `M2760 1800 L3000 1860`, repeated +100 and +200 in y, 30. Handle (3050, 2550) 40 × 200, rx 20, `butter`, 16. Floor `M700 3700 H3250`, 45. Gus box 2200, cx 1800, ground 3700. Dust puff(x, y, k) = circles (x−90k, y) r 80k · (x, y−54k) r 100k · (x+90k, y) r 76k, `oat`, 28, at (900, 3590) k 1 and (2700, 3610) k 0.85. Ticks `M2860 2520 l90 -40 M2890 2640 l100 -10`, 30. | Gus *chill* XS box 820, cx 525, ground 1000; puff (900, 960) k 0.45; floor `M60 1000 H990`, 20. | **GARMENT-FILL on Bay** [L] and Sage (`sage` keyed). LIGHT Ivory, Chambray; Butter → grip wrap and zip pull `pool`. DARK [L]: halo on Gus only (puffs are line art too). |
| **D05** Day One: The Sequel · Gus *hold-sign* | Cap xh 300: "day one:" (baseline 650) · "the sequel." (baseline 3750) · board Atk "part 2" at 14 u xh (≈ 117 px) | Front. Gus box 2000, cx 1800, ground 3150. Hold-sign: face (120, 140); zipper dash at y 112 (x 60–180); zip pull at y 105; board rect (30, 172) 180 × 34, rx 10, `oat`, 6; arms `M44 150 C30 156 24 168 28 186` + mirror from (196, 150); hands (31, 189), (209, 189) on the board's edges. Floor `M600 3150 H3000`, 50. | Loud only (no Quiet; fleece has no Private). | LIGHT Sand, Light Blue (check `sage` vs Sand, ΔE00). DARK Navy. |
| **D06** Still on the Team · Mallow *sleepy* | Cap xh 280: "rest day." / "still on" / "the team." · whisper "(psst. rest days" / "count here.)" | Front [L]. Mat (Mallow's grid, under the sneakers) (14, 214) 212 × 12, rx 6, `canvas`, 5. Mallow box 2000, cx 1650, ground 2000. Stamp group `rotate(-8 3050 1450)`: rect (2800, 1200) 500 × 500, rx 60, `oat`, 40; dashed circle (3050, 1450) r 175, 22, dasharray 40 30; crescent `M3110 1330 A130 130 0 1 0 3110 1570 A100 100 0 1 1 3110 1330 Z` `lilac`, 22. Baselines 2650, 3250, 3850. | Mallow *sleepy* XS with "z z", box 900, cx 525, ground 980. | LIGHT Sand, Light Blue, Ivory. GARMENT-FILL on Orchid (`lilac` + `lilac-shade` keyed; the moon swaps to `coral`). DARK Navy, Pepper (mat and stamp haloed). |
| **D07** Proud of You. Also, Water. · Sip *hyped cheer* | Cap: "proud of you." / "also, water." (hard-goods minimum xh ≥ 60) | Wrap, relative to the spec canvas: `oat` ground; 5% of the width clear at both seams. Panel A at 25% of the width: Sip box = 62% of the height, ground at 88%. Panel B at 75%: both lines fitted to 40% of the width. Swap panels if the template puts the front opposite the spout. | — | FULL-BLEED, `oat` ground; transparent if the listing can't print a ground. |
| **D08** Two Ends of One Dumbbell · Pip *happy* (A) / Pop *hyped* (B), outer arm raised | Cap xh 280. A "i brought" / "my buddy." (cx 1500) · B "i'm the" / "buddy." (cx 2100); baselines 700, 1300 · whispers A "(psst. you brought" / "your buddy.)", B "(psst. you're" / "the buddy.)" | Front [L]. Local grid at scale 11; plate `roundedHex(R 48)`, cy = 204 − 48·sin 60° = 162.4; `translate(tx, 392)`. **A:** tx 762; Pip plate (58, cy); bar rect local x 96–296, y cy ± 10, `oat`, 6, cut by the canvas at x 3600; knurl ticks `v14` (2.5) at local x 110 / 120 / 130 / 220 / 230 / 240; sweatband `M24 cy−22 H92` `coral` 7; left arm up. **B:** tx 198; bar local x −60 to 144; ticks at 0 / 10 / 20 / 110 / 120 / 130; sweatband `pool`; right arm up. `meta.edgeBleed = true`: only the bar enters the safe margin, touching the edge with no end outline. | A: `left_chest`, Pip plate + sweatband + face only (u 5), plate centre (450, 560), bar to the box's right edge. B: **`right_chest`** mirror, bar from the box's left edge. | Pairs: A Butter + B Chalky Mint [L] · A Bay + B Blossom · A Pepper + B Blue Jean (DARK). |
| **D09** Department of Showing Up · Bel *proud cheer* in a seal | Atk caps xh 120, tracking +0.04 em: top arc "department of showing up" · bottom arc "est. whenever you're ready" (stored lowercase) | Back [L]. Seal centre (1800, 1875). Outer circle r 1725, 45 (band: none on LIGHT, `oat` on DARK). Inner disc r 1290, `butter`, 30. Text baselines on r 1400 (A.11 `top`) and r 1600 (`bottom`). Sparkles (293, 1875) and (3307, 1875) r 110. Floor `M1250 2575 H2350`, 45. Bel box 1900, cx 1800, ground 2575. **Then scale the whole seal group by 0.95 about (1800, 1875)**: at r 1725 the DARK halo passes the canvas edge (1725 + 22.5 + 60 > 1800). Ring text becomes xh 114 (≥ 110). | `left_chest` mini seal: ring r 500, 20; disc r 380 `butter`, 16; Bel at XS LOD, box 560, centred; sparkles at 3 and 9 o'clock r 40; no text. | LIGHT Sport Grey (Sand if it fails contrast); butter-family garments → disc `pool`. DARK Navy: `oat` band, `ink` ring text, halo round the whole seal. |
| **D10** Bel Mark · Embroidery LOD | none (no wordmark under 5.3 in) | — | 240 grid [L]: handle `M82 110 C74 20 166 20 158 110`, core 14 `coral`, `ink` at core + 20; Bel body `coral`, `ink` 10; eyes (98, 150) and (142, 150) rx 9 ry 12; brows `M91 127 H105 M135 127 H149`, 7; mouth `M113 166 Q120 173 127 166`, 7. No highlights, arms or feet. **Hat:** art 600 px tall, centred in 1890 × 768; **crew `emb_chest`:** 750 px tall in 1200 × 1200. At 2.0 in: brow gap 0.079 in, handle window 0.18 in, outline 0.105 in, face strokes 0.074 in (all ≥ 0.05). | Light (Stone, Sand): Navy 1966 + Orange 1987. Dark (Navy): + White 1801 halo (+16 u) = 3 threads. |
| **D11** Collect the Crew · all 7 | Captions Atk lowercase xh 34: "bel", "bel", "mallow", "gus", "pip & pop", "sip", "ollie", "tuck" · title Cap xh 70: "collect" / "the crew" | — | Sheet 1749 × 2481: 3 × 3 grid, 20 px gutters, 37 px margin, so **cells are 545 × 780**. Per cell: character XS box 500, centred, ground at cell top + 600; caption baseline + 700 on an `oat` rounded rect; die line = halo (+16 u) ∪ caption rect. Stickers: Bel *nervous wave*, Bel *proud cheer*, Mallow *sleepy*, Gus *chill wave*, Pip & Pop *happy/hyped*, Sip *hyped cheer*, Ollie *cheer*, Tuck *shy*, and a title sticker (`oat` rect, two Cap lines, mini-Bel). | Full colour; ground per `spec.background`. |
| **D12** Firsts · 6 badges | Atk caps xh 40, stored lowercase: B1 "first visit" · B2 "asked for / help" · B3 "first class" · B4 "tried the / weights area" · B5 "rested on / purpose" · B6 "came back" (before "/" = top arc, after = bottom arc) | — | 900 × 900: disc r 430 `oat`, 14; band r 300–430 in the owner colour (B1 `coral`, B2 `pistachio`, B3 `butter`, B4 `sage`, B5 `lilac`, B6 `sage`); inner disc r 300 `canvas`; top baseline r 335 (tops out), bottom r 400 (tops in); character box 470, centred, ground y 640; one `butter` sparkle at the inner disc's upper right. B1 Bel *proud* in a mini doorway · B2 Ollie *cheer* + speech bubble with an outlined Atk "?" · B3 Pip & Pop · B4 Gus *trying* · B5 Mallow *sleepy* · B6 Gus *happy wave* + locker door edge. Patches (drop 3): Embroidery LOD, ≤ 6 threads, label xh ≥ 90 (band ≥ 0.45 in); drop the label ring if the sample fills in. | Full colour on paper. |
| **D13** The Whisper | default "(psst. you showed up." / "that counts.)" plus each design's whisper | — | `label.whisper` layout (§6.3.1); file ids §6.5 | §6.3.1 |

Single stickers (`MIX-STK3`, 3 in): the Quiet art of D01, D02, D03 (with its text) and D06 + halo die line; later D19, D20, D26.

#### 6.4.8 Later designs D14–D30 (build now; they ship per §5.6)

Conventions: §6.4.7. Unless stated, Quiet = the character at XS in the 1050 left-chest box; Private = the whisper label (tees only).

| ID · name | Text (exact) | Composition (key parameters) | Colour notes |
|---|---|---|---|
| D14 Speed of Okay · Mallow *chill walk* | Cap xh 220 "moving at the" / "speed of okay." · Atk xh 120 "okay" · whisper "(psst. okay is" / "a speed.)" | Gauge centre (1800, 1300): annulus r 760–950, sectors 180°→120° `canvas`, **120°→60° `pistachio`**, 60°→0° `canvas`, 40 on band and dividers. Needle θ 100°, length 820, 60, round caps. Hub r 80 `oat`, 40. "okay" centred at (1800, 445). Mallow box 1500, cx 1800, ground 2750; walk = body −4°, rear sneaker +15° and lifted 6. Ticks `M780 2200 h-220 M760 2380 h-260 M780 2560 h-220`, 40. Floor `M500 2750 H3100`. Baselines 3300, 3850. No numbers. | Mallow rules (D06). On Chalky Mint the okay zone → `coral`. |
| D15 Mallow Mark · Mallow *sleepy* (no outside text; product named "Rest on Purpose") | whisper "(psst. rest on" / "purpose.)" | Embroidery Mallow: body with 5 grip nubs (14 u wide); no grooves; end face = one ellipse (190, 161) rx 20 ry 43, no hollow core; "U" eyes, "o" mouth and z's at 7; Gold sole stripes. Beanie: 780 × 390 centred in 1500 × 525. Joggers `left_hip` (DTG): Mallow XS full colour, box 900. | Threads: Purple 1832 (light knits) / White 1801 (dark) + Gold 1951. |
| D16 Lights Out · pattern | none | Tile 1800, ground `lilac`: 6 z's `M0 0 h12 l-12 13 h12`, 0.6–0.8 in tall, `ink` stroke 15 px, ± 25°; 4 crescent moons 0.9–1.1 in, `oat`, 16; 8 four-point sparkles 0.3–0.45 in, `oat`, 14; spacing ≥ 1.3 × the larger motif's diameter. | "Lilac night" (`LNT`, default). "Ink night" (`INT`: `ink` ground, `lilac` z's, `oat` moons) on **socks only**. Moons are never `butter` (purple + yellow ban). |
| D17 Today's Specials · Mallow *sleepy* | Cap xh 230 "today's" / "specials" (left, x 420, baselines 1350, 1850) · Atk xh 115 items / values: "warm-up" / "gently" · "a few sets" / "yes" · "stretch" / "if you like" · "big nap" / "market price" (baselines 2350 / 2750 / 3150 / 3550; values right-aligned to x 3180) · Atk caps xh 110 "served all day" (baseline 3820) · whisper "(psst. big nap," / "market price.)" | Back. Board x 225–3375, y 800–3950, rx 80, `ink`; inner frame inset 70, rx 50, `butter` stroke 24. Mallow box 950, cx 2600, ground 860 (on the board). Leader dots: 20 px circles every 48 px, 40 px clear at each end; drawn, never "…" glyphs. | DARK: board = `oat` 45 outline, no fill; dots `oat`; frame `butter`. **LIGHT: knock-out text fails** (Atkinson's thinnest stroke 0.14 × xh = 16 px < 18, §4.5), so LIGHT uses the DARK geometry in `ink` (outline board, `ink` text and dots). DTG only. |
| D18 You Go, I'll Go Too · sneakers only | A Cap xh 340 "you go," · B Cap xh 300 "i'll go too." (baseline 900) · whisper "(psst. you're not" / "going alone.)" | Sneaker at u 55: centre x 1800, toe right, ground y 2700; outline fixed 45 px; sole stripe 4 u (A `coral`, B `pool`); lace ticks 30. Quiet: the same sneaker 3 in long (u 22.5, outline 20), toe right, **left chest on both tees**. | LIGHT: the `oat` upper is keyed (ink outline + stripe). DARK: the upper prints. Pairs Bay + Ivory, Chalky Mint (A) + Blossom, Pepper + Espresso. |
| D19 Today's List · Bel *nervous* | Cap xh 300 "today:" (x 520, baseline 1250) · Atk xh 130 "sat in the car" / "for a sec" (x 880, baselines 1830, 2160) · "went in anyway" (baseline 2680) · whisper "(psst. you went in" / "anyway.)" | Notepad x 250–3350, y 500–3700, rx 70, `oat`, 45. 5 rings r 70, 34, no fill, at x 750 / 1250 / 1800 / 2350 / 2850, y 500. Checkboxes x 520–780, y 1600–1860 and 2450–2710, rx 50, `oat`, 36; tick `M570 1730 L640 1800 L740 1650`, 44. Bel box 1000, cx 2850, ground 3700. Quiet: checkbox x 80–440, y 560–920 + tick, and Bel XS box 600, cx 760, ground 1000. | LIGHT: the notepad becomes an outline. DARK: solid `oat` pad with `ink` text. |
| D20 Oh! You're Here. · Ollie *cheer* | Cap "oh!" xh 420 / "you're here." xh 240 (**one** "!") · whisper "(psst. oh!" / "you're here.)" | Ollie box 2200, cx 1800, ground 2100; baselines 2800, 3350. | Not on mint or sage garments (`pistachio` caution). Butter → sparkles `coral`. DARK Navy. |
| D21 Sneaker Toss · pattern | none | A.12 with 6 sneakers (A.5 sneaker + tick `M118 198.5 l4 2.5`, 9.5 px/u ≈ 1.27 in; stripes cycle `coral`, `pool`, `butter`, `bubblegum`, `lilac`, `pistachio`; upright 0° ± 30° or flipped 180° ± 30°, random mirror; r 240, spacing 620) and 8 `butter` sparkles (r 50–85, 20; r 95, spacing 330). | Grounds `LCV` (default) and `LSG`; no dark grounds. |
| D22 Every Day Is Brain Day · Bel *chill idle* + headphones | Cap "every day is" xh 260 / "brain day." xh 300 (baselines 3100, 3700) · whisper "(psst. it counts" / "for your brain too.)" | Headphone band: tube `M52 150 C40 -6 200 -6 188 150`, core 10 `pool`, drawn after the handle, before the body. Cups x 34–62 and 178–206, y 126–174, rx 12, `pool`, 6, after the body. Bel box 2000, cx 1800, ground 2500. Sparkles (900, 900) r 100, (2750, 800) r 80, (2900, 1500) r 60. | Chambray and Chalky Mint → headphones `lilac`. No medical claims anywhere. |
| D23 Plate Party · pattern | none | Ground `pool`. 4 faceless `roundedHex` plates R 150 (alternating `bubblegum` / `butter`, 18; hole r 24 `oat`, 12). 4 bumper rings (disc r 165 `pistachio`; ring r 115, 12; hole r 30 `ink`). 3 bar segments (330 × 60 `oat`, 14, 3 knurl ticks). 8 `oat` sparkles. Free rotation; spacing ≥ 1.3 × the larger diameter. No faces, no numbers. | Golden Hour (`GLD`): `butter` ground, `coral` / `pistachio` plates; yellow plates → `bubblegum`. |
| D24 The Receipt · stamp | Atk, left-aligned, tabular: "{brand}" xh 150 · "receipt #0001 · today" 110 · "1 × walked in" / "1 × water" / "1 × towel" / "0 × pressure" 120 · "total: you showed up" 120 (caps "TOTAL" by layout) · "(thanks for coming in.)" 110 · whisper "(psst. total:" / "you showed up.)" | Back. Receipt x 150–3450, y 300–3900, `oat`, 36; zig-zag bottom (teeth 150 wide, 90 deep). Text x 300–3300. Baselines 650, 900, 1300, 1600, 1900, 2200; dashed rule y 2450 (60 × 14 dashes, 40 gaps); then 2800 and 3100. Stamp (2950, 650) r 260, −8°, `butter`, 30; dashed ring r 200; solid Bel 260 tall, `ink`. Quiet = stamp, 3 in. "×" must exist in the font (pitfall 5). | LIGHT: outline receipt; stamp → `coral` on Butter. DARK: solid `oat` receipt. Tote: if the area is < 11 in wide, use lines 1 and 3–7 only. |
| D25 Gym Towel (Not for Dishes) | Cap xh 300 "gym towel" · Atk xh 120 "(not for dishes)" · Atk caps xh 45 "{brand} · towel dept." | 16 × 28 in portrait, `oat` ground. Stripes 1.5 in from both short ends: `coral` 0.6 in, 0.25 in gap, `pool` 0.4 in. Title at 45% height; sub-line 0.5 in below; three 0.5 in `butter` sparkles 1 in above. | Alternative `LSG`: `sage` ground, `oat` stripes, `ink` text. |
| D26 Packed · Gus *happy* (unzipped) | Cap xh 200 "packed:" (baseline 520) · Atk xh 120 "water" / "towel" / "courage" (baselines 1500 / 2000 / 2500 at x 2200) | Design space 3000 × 3300 (tote). Slot `M70 112 Q120 128 170 112 Q120 100 70 112 Z` `ink`. In the slot: faceless bottle x 82–104, y 60–116, `pool`, 6, `butter` cap y 50–64; a towel corner `M118 112 L132 70 L156 80 L148 112 Z` `oat` with `coral` + `pool` stripes; a heart ×22 at (139, 74), `coral`. Gus box 1700, cx 950, ground 2900. Checkboxes 180 px at x 1950 (30; tick 36). | Natural tote = LIGHT; check `sage` vs the tote hex. |
| D27 The Crew Back · Pip & Pop *happy/hyped* | top arc "{crew_name}" (A–Z 0–9 space . ' -, ≤ 16; `fitArc`, xh 110–150) · bottom arc "crew · est. {month} {year}" | D09 seal geometry (incl. the 0.95 scale); Pip & Pop box 2400, cx 1800, ground 2575. Per-order file; the preview uses "your crew", "jan" and the `AS_OF` year. Quiet = D09 mini seal (always included). | As D09. `features.crews` gate. |
| D28 Showing Up Since · stamp | Cap xh 260 "showing up" / "since {year}" (baselines 2450, 3000) · optional Atk xh 140 "(with a few breaks)" (3400) · whisper "(psst. showing up" / "since {year}.)" | Stamp centre (1800, 1150), rotated −6°: disc r 750 `butter`, 45; dashed ring r 640, 26, dasharray 60 40; solid Bel 700 px tall at (1800, 1180), `ink`. Year picker 1980 to the `AS_OF` year. Quiet = stamp, no text. | Butter garments → stamp `coral`. DARK: stamp `butter`. |
| D29 I Count Visits · Gus *chill* | Cap xh 230 "i count visits." (baseline 600) · Atk xh 130 "(that's it." / "that's the metric.)" (2500, 2850) · whisper "(psst. that's it." / "that's the metric.)" | Tally of outlined tubes (`ink` 150 wide, fill 60). `oat` uprights 900 tall (y 1100–2000): group 1 at x 450 / 670 / 890 / 1110, group 2 at x 1350–2010, loose at 2250 and 2470. `coral` diagonals run bottom-left → top-right per group. Gus box 1300, cx 3000, ground 2000. Floor `M300 2050 H3300`, 45. | Gus rules (D04). Check the "ladder / fence" misread (§6.7). |
| D30 Showed-Up Log · notebook cover | Cap "showed-up log" fitted to 0.8 W (xh ≥ 60) · Atk "day one" · Atk xh ≥ 30 "weeks, not days. nothing here goes down." | Relative to cover width W: `canvas` ground; top margin 0.1 W; 13 × 4 dashed `ink` circles (diameter 0.85 W / 13 × 0.8). Row 1 pre-stamped: 3 `coral` with a solid mini-Bel, 1 `lilac` with Mallow's crescent. A dashed day-one line under the "day one" label. Back cover (if any): Bel icon + `{brand}`. | FULL-BLEED. |

### 6.5 Export

**Which files exist.** `art/print/plan.ts` exports the pure `printFileIdsFor(variant)`, which `npm run catalog` uses for `Variant.printFileIds`; `npm run art:print` renders the **unique** ids in `catalog/catalog.json` (ci order: §10.2).

| Segment | Rule |
|---|---|
| id | §5.2 format |
| `ANY` vs option | `ANY` when the bytes don't depend on the garment (LIGHT, DARK or TONAL without an accent swap for it); else the colour code (GARMENT-FILL, an active swap, an AOP/paper ground `LCV`…, a Firsts badge `B1`–`B6`) |
| size | AOP only, once `perSizeTemplates` exist; until then one provisional file without a size |
| labels | Default `D13.none.<pk>.label_inside.<LIGHT\|DARK>.ANY` on every eligible tee variant. Private: `<D>.private.<pk>.label_inside.<LIGHT\|DARK>.ANY` |
| examples | `D04.loud.cc1717.front.GARMENT-FILL.BAY` · `D08B.quiet.cc1717.right_chest.LIGHT.ANY` · `D10.none.y6245cm.hat_front.DARK.ANY` · `D12.none.sticker3.sticker_3in.FULL-BLEED.B4` (more in §5.10) |

**Steps per file** (`scripts/art/render-print.ts`):
1. Resolve spec, extras, recipe (§6.4.4) and swaps; call the layout; compose layers (halo, swaps); embroidery: tokens → thread hexes.
2. **Refit design space → spec:** box = `artBoxPx`, else `artMaxPx` top-left, else the canvas; `s = min(box.w / ds.w, box.h / ds.h)`; wrap in `translate(box.x + (box.w − ds.w·s)/2, box.y) scale(s)` (top-aligned, centred). If `s ≠ 1`, scale every `meta.texts` height and `minStrokePx` by `s` and re-check: a smaller real label (600/750) can fail; its fallback whisper is "(psst. that counts.)".
3. SVG lint (no `<text>`, `NaN`, opacity, gradient, filter or `<image>`; < 20,000 path elements); write the SVG.
4. `exportPrint(svg, { w, h, keyOut, minKoPx, dpi })` (A.8): crisp render, key-out, heal below the rule set's minimum, sRGB ICC + pHYs, SHA-256.
5. Write the PNG and a manifest entry with `validator: { status: "fail", failures: ["not validated"] }` until `validate:print` fills it.

**Manifest** (`print-files/manifest.json`, committed; types in `art/print/manifest.ts`, extending `PrintFile` from §5.10):

```ts
import type { PrintFile, ListingId, ColorCode } from '../../lib/catalog/types';
import type { RenderOutput } from '../designs/types';
export interface ManifestEntry extends PrintFile {  // PrintFile: id, designId, part, tier, productKey, placement, technique,
  readonly listings: readonly ListingId[];  //   recipe, garmentColor, size, path, widthPx, heightPx, dpi, sha256,
  readonly usedOn: readonly ColorCode[];  //   specKey, validator { status, failures, warnings }, perOrderTemplate
  readonly bytes: number; readonly specVerified: boolean; readonly provisional: boolean;
  readonly svgPath: string; readonly scale: number; readonly healed: number;
  readonly meta: RenderOutput['meta'];  // texts with px sizes, characters + LOD, threads, alt text
}
export interface PrintManifest {
  readonly version: 1;
  readonly scope: 'launch' | 'all';  // which run wrote it; files = exactly that scope's ids
  readonly specsSha256: string;  // sha256 of print-specs.json
  readonly fonts: readonly { file: string; sha256: string }[];
  readonly tools: Readonly<Record<'node' | 'resvg' | 'sharp' | 'opentype', string>>;
  readonly files: readonly ManifestEntry[];  // sorted by id; NO timestamps (§3 rule 16)
}
```

- PNGs are git-ignored; the manifest is committed. **Determinism:** stage it, re-run, then `git diff --exit-code print-files/manifest.json` (§10 M5); `tests/integration/print-determinism.test.ts` renders 5 fixed ids twice and compares SHA-256.
- **Scope:** `--scope launch|all` (default `all`); the manifest holds exactly that scope's ids, sorted, and records it in `scope`. A `--scope launch` run against an `all` manifest exits 1 (from M8 on only `all` runs); `validate:print` and `mockups` refuse a `--scope` that differs from the manifest's.
- **Speed:** render + validate ≈ 2–2.5 s per 3600 × 4800 file [L]: use a worker pool (`os.availableParallelism()`) and a cache keyed by `sha256(svg + spec + recipe + tools)` in `art/out/cache.json`.
- **Personalised** (D27, D28): one `perOrderTemplate: true` preview per variant; §8's draft-order step calls the same layout with `personal` and the same validators.

### 6.6 Validators (`npm run validate:print`)

`scripts/art/validate-print.ts` runs A.10 per manifest entry and `usedOn` colour (rules in px at `spec.dpi`) plus the checks below, writing `validator` to the manifest and `print-files/validation-report.md` (per design: pass/warn/fail, every message). **Exit 1 on any `fail`;** warnings never block the prototype (`export:printful` also refuses unverified or provisional specs).

| # | Check (applies to; default all) | Fail when |
|---|---|---|
| 1 | 8-bit RGBA PNG, sRGB (ICC embedded) | other format, depth, channels or space |
| 2 | Exact canvas | `width × height ≠ spec.canvasPx` (or the per-size template) |
| 3 | Limits | over `maxSidePx` or `maxBytes` |
| 4 | Density | **warn** if ≠ `spec.dpi` (partners judge pixels) |
| 5 | Spec status | **warn** if `verified.value` is false or `provisional` |
| 6 | Binary alpha | any 0 < alpha < 255; no anti-alias allowance (crisp rendering gets 0). Printful: "avoid semi-transparent edges or fades for DTG/DTF" [V]: no fades, gradients, opacity, filters, blurred shadows, glows or halftones in v1 |
| 7 | Coverage (full-bleed specs) | any transparent pixel |
| 8 | Not empty | 0 opaque pixels (catches silent font, NaN and clip failures) |
| 9 | Safe area (transparent specs) | ink bbox outside `artBoxPx`, or (no art box) outside canvas minus the safe margin; waived only for `meta.edgeBleed` (D08 bars) |
| 10 | Reserved zones (labels) | any opaque pixel in `reservedPx` (label y 640–900) |
| 11 | Palette | a colour outside the allowed exact hexes (tokens; threads for embroidery) |
| 12 | Element width | an element under the minimum stroke, or an enclosed knock-out under the minimum gap (after healing; A.9 reads ±1 px straight, +2.3 px diagonal) |
| 13 | Text sizes | a `meta.texts` x-/cap height under the rule set after refit; Caprasimo on a label; **any** text on `stretch` |
| 14 | Edge contrast (garment × colour) | a colour ≥ `primaryEdgeShare` (10%) of edge pixels is < `minEdgeContrast` vs the garment hex |
| 15 | Merge (garment × colour) | a non-`ink` colour ≥ 2% of ink is below `mergeDeltaE` from the garment (below `cautionDeltaE` = warn) |
| 16 | White ink (light garments) | any `#FFFFFF` pixel |
| 17 | Embroidery | > `maxThreads` (`meta.maxThreads` for the Bel face); a non-thread hex; elements, gaps or Atkinson xh under the rule set |
| 18 | Pattern (stretch / AOP) | tile overlaps > 0 (incl. across the wrap); seam check > 0.01%; text; tile not at the spec's `tileIn` |
| 19 | Stickers (`sticker_3in`, `sticker_sheet`) | > 1 opaque island per sticker (a transparent-ground sheet has exactly 9); any enclosed hole |
| 20 | Copy | a `meta.texts` string or whisper hits `brand/banned-words.json` (scope `product`) |
| 21 | Cast | > 3 characters on a Loud; a character fill outside its own tokens (SVG layers) |
| 22 | Determinism (ci) | re-render SHA-256 ≠ manifest |

`tests/unit/print-validate.test.ts`: tiny in-memory PNGs, one failing per rule (50%-alpha pixel; off-palette pixel; 11 px stroke; 10 px enclosed gap; LIGHT art on Pepper; `sage` art on Bay; white pixel on Ivory; 7 thread colours; opaque pixel in the label reserve; text on a leggings file) plus one pass; A.10's results are the expected outputs.

### 6.7 Visual review loop

Validators can't tell whether Bel reads as a padlock: **you must look** (§3 rule 15).
1. `npm run art:sheets` writes `art/review/<D>.png` (`-- --cast`: cast sheets, M2): 400 px cells of every print file on each `usedOn` garment hex, plus a checkerboard; a **1:1 crop** (400 × 400 at 100%) of the smallest text and of a face; patterns as 2 × 2 tiles; buddy pairs A-left / B-right; labels in outlined Atkinson (file id + garment).
2. **Open every sheet with the Read tool** after each art milestone or art change; check it against the list below.
3. Fix the module, re-render, look again; after 3 failed rounds on one design, log an open founder item in D7.
4. Log every inspection in `art/REVIEW.md`: `date | sheet | files | items checked | problems | fix | manifest sha after | status`. D7 lists the sheets inspected.

**Checklist:** silhouette reads as its object at 25% zoom · text fits, no collisions, open counters in the 1:1 crop · LIGHT knock-outs look intentional (sneakers garment-coloured), no stray hairlines · DARK halos are soft edges, not one `oat` blob; large props are line art · GARMENT-FILL characters don't read as holes · labels: reserved zone empty, whisper legible · embroidery: handle window open, brow/eye gaps visible · patterns: no clumps, no visible seam, no motif reading as a letter or number · §4.9 don'ts: no numbers on weights, no recording dot or eye motif, ≤ 3 characters on a Loud.

**Misread list.** Characters: §4.7 table; at print sizes also Bel as a ghost (small) or a bun with a lid (embroidery: taller D10 handle; favicon crop), Gus as a lunch box (never two handles), Pip & Pop as sunglasses (keep knurl ticks); Mallow keeps its hollow core outside embroidery. Other elements (seen or predicted):

| Element | Must not read as | Look at | Fix lever |
|---|---|---|---|
| 4-point sparkle | "+" / first-aid cross (small, A.12) | concave Q-curve sides | Raise r, or fewer, larger sparkles |
| D16 "z" | lightning bolt (banned icon) | the z's horizontal bars | Rotation within ± 25°, bars level-ish |
| D29 tally | ladder, fence, prison bars | `coral` diagonals | Keep the diagonals and Gus beside it |
| D03 camera | a recording device | heart lens | No red dot, no lens rings, ever |
| D21 sneakers | clutter, footprints | spacing | Sparse single shoes; overlap validator |
| D09 seal | a government or police badge | Bel + the `butter` disc | Keep Bel large in the disc; no stars, shields or eagles |

### 6.8 Offline mockups (D4)

`npm run mockups` (`scripts/art/render-mockups.ts`) needs **no credentials**: for every listing × option × tier × view it composites the **validated print PNG** onto a code-drawn garment template (A.13), so a mockup shows exactly what will print.

**Templates** (`art/mockups/templates/<type>.ts`): silhouette and seam paths, print-area origins in **garment inches** at 50 px/in on 1440 × 1800 (4:5); art resized (`lanczos3`) to `canvasPx / dpi × 50` px.

| Type | Silhouette | Print-area origin | Views (all but stickers add `detail`) |
|---|---|---|---|
| tee (cc1717, bc3001) | 22 in body, short sleeves (A.13) | front top 3.0 in below the collar, back 2.4 in; chest/back-neck boxes come from the file | flat_front, flat_back, label, pair |
| crewneck · hoodie | Rib cuffs and hem band · hood + kangaroo pouch | Same as the tee; hoodie art clears the pouch | flat_front, flat_back |
| joggers | Two legs, waistband, cuffs | left hip, 3 in below the waistband | flat_front |
| leggings · bra · shorts · socks | Panel silhouettes | The **tile** at the same 6 in scale (A.12 `fillPanel`, clipped) | flat_front |
| dad hat · beanie · patch | ¾ front cap · folded cuff · round patch with a satin edge | Art box centred | flat_front |
| bottle · tote · towel · notebook | Cylinder (front half of the wrap) · square bag with handles · folded towel showing the title · spiral cover | Per spec; relative layouts | flat_front |
| sticker · sticker sheet | Die-cut sticker with Printful's white border · sheet with kiss-cut lines | Whole file | flat_front |

**Rules:**
- **Colour:** live `color_code`, then `approxHex` (§5.2); for a U-tagged hex §7 shows "Colour is approximate until we've seen the real thing." under the image.
- **Shading:** 14% `ink` side gradients, 18% seams, 35% outline; no photos, bodies or props implying people (§3 rule 18); optional fabric noise (`feTurbulence`, ≤ 6% alpha) off by default.
- **Output:** `public/mockups/<handle>/<option>-<tier>-<view>.webp` (1440 w) + `-960.webp`, `-480.webp`, `.avif` siblings; srcset = `<src>` 1440w, `<src minus .webp>-960.webp` 960w, `-480.webp` 480w. `Mockup`: `widths [480, 960, 1440]`, `width 1440`, `height 1800`, `origin "generated-svg"`. PNG copies only in `exports/images/` (for Shopify later). Budgets: target ≤ 60 KB per 1440 WebP (measured 22 KB [L]); limits hero ≤ 120 KB at 1440w, card ≤ 45 KB at 480w.
- **Views:** `detail` = print area at 2×; `label` = the neck with the label file at 3 in true size (tee listings); `pair` = A + B side by side (D08, D18) on each half's listing as `/mockups/<handle>/<option>-<tier>-pair.webp`, with the partner half's first colour (§5.4); `/bundles/buddy-tee/` reuses D08A-CC17's pair image.
- **OG:** `public/og/<handle>.png`, 1200 × 630, ≤ 300 KB: `oat` ground; default-tier first-colour mockup 600 px tall at left; title in Caprasimo (`fitText`, ≤ 520 px wide, xh ≥ 28 px; passes the `names` scope); A.5 wordmark bottom right; no price.
- **Alt text:** `Mockup.alt` per §5.10 ("{Colour} {product} laid flat with {Name} the {object}, …").

**Upgrade path:** local SVG (now) → Printful v2 `GET /v2/catalog-products/{id}/mockup-templates` (positions for compositing on real product photos [T]) → `POST /v2/mockup-tasks`, poll or webhook (≈ 2–10 per minute reported [U]; back off on 429; v2 is open beta [V]) → photos of physical samples laid flat (§8).

**Partner mockups:** only `npm run golive:printful -- --live --mockups <listingId>` calls the API, writing raw results to `catalog/live/printful/mockups/`; `MOCKUP_PROVIDER=printful npm run mockups` reads that cache offline (no token, no network) and writes `public/mockups/` with origin "printful-mockup-api". Never in ci.

### 6.9 Optional human-designer handoff

`npm run art:handoff -- D01` writes `handoff/D01/` (git-ignored):
- **Pack:** generated `README.md` (exact text, cast, expressions, poses, placements with canvas px, recipes, target garments + hexes, every minimum, misread risks; construction fixed; composition, scale, prop styling negotiable); flat outlined `svg/<id>.svg` with groups `ground`, `largeProp`, `character`, `smallProp`, `text`; `png/` (print files + contact sheet); `spec.json` (relevant areas, rules, threads); the validation excerpt; the OFL texts (fonts from Google Fonts).
- **Return path:** SVGs at design-space size, exact token hexes, flat fills, no `<text>` or effects, saved as `art/designs/overrides/<id>.svg` with the variant's `layout` = `"override:<file>"`.
- The exporter applies the same refit, key-out, heal and validators; the manifest's `svgPath` points at the override.
- Get a signed IP assignment before using any outside art (template [U]: the lawyer review in §8). Never accept traced or AI-imitated work of other brands (§3 rule 8).

---

## 7. Website prototype (D5)

**Goal.** A static Next.js storefront that proves the whole customer experience with **zero accounts, zero keys and zero env vars**: browse, Quiet/Loud/Private, cart, a labelled mock checkout, and the local-only community features of §4.8. Every number on screen comes from `catalog/catalog.json`, `brand.config.json` or `content/*.json`; nothing is hard-coded (§3 rule 4). Catalog types come from `lib/catalog/types.ts` (§5.10), never redeclared; this section defines only the commerce surface (§7.9) and the community logic (§7.8).

### 7.1 Stack (pinned versions)

Run `npm view <pkg> version time dist-tags` for every row and pin **exact** versions (§3 rule 2); record them in `docs/decisions.md` and D7. After `npm i`, per §3 rule 3, read `node_modules/next/dist/docs/` (static exports, metadata, JSON-LD, CSS, `useSearchParams`), run `next dev` once and commit its `AGENTS.md` block; `CLAUDE.md` is one line: `@AGENTS.md`. A pin is the newest release **≥ 14 days old on 2026-11-10** (npm publish dates, checked that day [V]); keep them for the whole build and upgrade only for a security advisory (log it).

| Package | Pin | Notes |
|---|---|---|
| Node.js (`.nvmrc`; `engines: ">=24.22.0"`) | **24.22.2** LTS (2026-10-27) | 24.22.1 was a security release [V nodejs.org/dist/index.json]. Not 26. |
| `next` + `eslint-config-next` | **16.4.3** (2026-10-23) | Read the 16.4.4–16.4.6 notes; take one only for a security fix |
| `react`, `react-dom` / `@types/react`, `@types/react-dom` | **19.3.1** / **19.3.0** | |
| `typescript` / `@types/node` | **5.9.3** / **24.19.2** | **Not TS 7**: `eslint-config-next` and typescript-eslint need the TS 6 API [V Next.js docs]. §7's snippets compile under 5.9.3 and 6.0.2 [L]. |
| `tailwindcss`, `@tailwindcss/postcss` | **4.3.3** (2026-07-16) | PostCSS plugin, not `@tailwindcss/turbopack` (new in 4.3.4) [V] |
| `zustand` · `zod` | **5.0.16** (2026-10-22) · **4.6.7** | §7.8 · `lib/catalog/schema.ts` (§5.10) |
| `server-only` | exact; verify live (0.0.1 expected [U]) | Only `lib/catalog/load.ts` imports it; Vitest aliases it (§7.14) |
| `lucide-react` | **1.62.0** (2026-10-27) | ISC; icon rules in §4.5 |
| `@fontsource/caprasimo`, `@fontsource-variable/atkinson-hyperlegible-next` | **5.3.0**, **5.3.0** | OFL-1.1 web WOFF2 (§7.7) |
| `marked` | **18.1.2** | Build-time Markdown for policy drafts; zero client JS |
| `eslint` | **9.39.5** | Plugins inside `eslint-config-next` still peer on ESLint ≤ 9 [V]. Flat config. |
| `vitest` + `vite` | **5.0.5** + **8.3.5** | Vite is a required peer of Vitest 5 [V] |
| `@playwright/test` · `@axe-core/playwright` | **1.64.1** · **4.14.0** | `npx playwright install --with-deps chromium firefox webkit` |
| `@lhci/cli` · `linkinator` · `serve` · `tsx` | **0.15.1** · **8.1.0** · **14.2.6** · **4.23.15** | linkinator needs Node ≥ 22 |
| `prettier` + `prettier-plugin-tailwindcss` | **3.9.10** + **0.8.1** | Optional format gate |
| `sharp`, `@resvg/resvg-js` | §6.1 | Print toolchain only; the site never imports them |

**Not used:** `next/font/google` (downloads at build time) · CSS-in-JS · UI kits · analytics SDKs · Stripe · React Compiler · `@shopify/hydrogen` (Phase-2 adapter only, §7.9).

**Breaking changes** (upgrade guide and changelogs, checked 2026-11-10 [V]):
- **Next 16:** `params`/`searchParams` are Promises (`const { handle } = await props.params`, typed with the generated `PageProps<'/products/[handle]'>`) · Turbopack is the default; a custom `webpack` config fails (none here) · `next lint` is gone (`eslint .`) · `middleware` is now `proxy`; Cache Components and parallel slots (`default.js`) don't export: `cacheComponents` off, no parallel or intercepting routes · the default image loader is unsupported (§7.2).
- **Tailwind 4:** CSS-first `@import "tailwindcss"` + `@theme`; no `tailwind.config.js` (§7.7).
- **Playwright 1.64+:** actions wait for non-`inert` elements (close dialogs first); `test.skip()` takes only a description. **Vitest 5:** `clearMocks` defaults to true; unawaited assertions fail; output in `.vitest/` (git-ignored); no parent-folder config (root `vitest.config.ts`). **Zustand 5:** named imports only; object selectors loop, so `useShallow` for multi-field selectors [U: prior knowledge].

### 7.2 Static-export constraints and how to comply

```ts
// next.config.ts (complete for the prototype)
import type { NextConfig } from 'next';
const config: NextConfig = {
  output: 'export', // → out/
  trailingSlash: true, // out/shop/index.html works on every static host
  images: { unoptimized: true },
  reactStrictMode: true,
  poweredByHeader: false,
};
export default config;
```

Unsupported with `output: 'export'` [V Next.js static-exports guide] → how we comply (test):
- Dynamic routes without `generateStaticParams`, or with `dynamicParams: true` → every `[param]` route exports `generateStaticParams()` from data **and** `export const dynamicParams = false` (route manifest, §7.14).
- `searchParams` in a page → `useSearchParams()` in a client island inside `<Suspense>` for `?tier/color/size` and filters; the fallback is the **same component with default props** (no CLS); a missing boundary fails the build.
- Route Handlers reading `Request`; `cookies()`, `headers()`, redirects, rewrites → no server code; data routes are force-static GETs (`export const dynamic = 'force-static'`): `sitemap.ts`, `robots.ts`, `manifest.ts`, `app/catalog-index.json/route.ts` (ESLint bans `next/headers`).
- Server Actions, ISR, Draft Mode, `proxy`, intercepting routes → not used; forms call adapter methods client-side (ESLint bans `'use server'`).
- Default image optimisation → pre-rendered widths from §6, `ResponsiveImage` (no `/_next/image` in `out/`).
- Per-visitor pages (order, e-card, crew invite, buddy link) → one static route each; ids in `?id=`, payloads in the **URL fragment** (`#…`, never in host logs) (e2e flows 1, 10, 11).
- Response headers → `out/_headers`, written by `scripts/site/write-headers.ts` after `next build` (Cloudflare Pages and Netlify honour it [U: confirm on the chosen host]; §7.15).

**Hydration.** Persisted stores use `skipHydration: true`; `<StoreHydrator />` in the root layout calls each `persist.rehydrate()` after mount. Until `useHydrated()` is true, components show a placeholder (the bag count is hidden, not "0"). Static HTML never holds per-visitor data.

**Build-time date.** `AS_OF` (`lib/site.ts`) defaults to `"2027-01-05"` (launch day), so the prototype shows the launch set; `NEXT_PUBLIC_AS_OF=2027-03-02` previews a later drop. `isVisible(listing)` (`lib/catalog/visible.ts`, unit-tested) needs all of: `visibility === 'public'` and `status !== 'archived'` (drafts **are** shown: `status` describes Shopify publication) · `availability.from ≤ AS_OF ≤ (until ?? ∞)` · `gate` absent or `passed` · for a `personalisation` listing, its flag ≠ `off`; for `D27-G185`, `features.crews === 'on'` (§5).

### 7.3 Repo layout, env and club mode

**Paths: §10.1** (the Next.js app lives at the repo root); it reads what §4–§6 produce and writes nothing back. **tsconfig.json:** `strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `noImplicitOverride`, `verbatimModuleSyntax`, `paths: {"@/*": ["./*"]}`. **Catalog reads:** `lib/catalog/read.ts` = plain `fs` + `CatalogSchema` (no `server-only`), for scripts and tests; `lib/catalog/load.ts` = `import 'server-only'` + `read.ts`, for the app, so catalog loading never reaches a client bundle.

**Data files §7 adds:** `catalog/src/transit.json` = `{ "US": Sourced<{ min: number; max: number } | null> }` (business days; `null` [U] until §8 reads real delivery estimates; typed in `lib/delivery/types.ts` with §5's `Sourced`) · `brand/blocklist.json` = profanity and other brands' names (our own name only as `{brand}`, never the literal: §4.1 name grep) · the `content/*.json` files named in §7.5; seeds (cheer posts, demo crew members) are `CopyString`s too, so copy tests cover them.

**Env vars** are all optional; the full list is §10.1's `.env.example`. Defaults (names without `NEXT_PUBLIC_`): COMMERCE_PROVIDER `mock` · SITE_ENV `preview` (only `production` allows indexing) · AS_OF `2027-01-05` · SITE_MODE unset (`club` only via `build:club`) · ANALYTICS_HOST unset (club only, never in tests). CI proves zero env with `env -i PATH="$PATH" HOME="$HOME" npm run build`.

**Club mode (built in M7, §8.1).** `npm run build:club` (`NEXT_PUBLIC_SITE_MODE=club NEXT_PUBLIC_SITE_ENV=production npm run build`) is the public `club.{domain}` site: December with `features.waitlist` `"on"`, from Tue 5 Jan 2027 the same build with `"off"`. No DemoBar, no Bag, no `/cart/` or `/checkout/*`; buy buttons link to `https://{domain}/products/<handle>`; email forms post to `https://{domain}/contact#contact_form` (`form_type=customer`, `contact[email]`, `contact[tags]`), with no "nothing was sent" note; the live codes (`BUDDYSHEET`, `BUDDY15`, `FIRSTB1`–`FIRSTB6`, §9.5) replace the mock ones, in `<code>` (§4.4); the cookie-free counter runs (§7.13); indexable, with no `X-Robots-Tag` (§7.15). `test:club` (§10.2) checks all of this with waitlist `"on"` and `"off"`, plus "Join the waitlist" on every buy surface when on.

### 7.4 Sitemap, IA and navigation

Shop **by vibe**, **by product type** and **by character**. **Never by gender**: no men's/women's split in nav, filters, size guides or copy (§2 decision 7). Help sits in the same place on every page (header right and footer; WCAG 3.2.6).

| Group | Route (page) | Indexed | Flag |
|---|---|---|---|
| Shop | `/` · `/shop/` | yes | — |
| | `/collections/[handle]/`: vibes `meet-the-crew` `the-small-print` `buddy-system` `mallow-hours` `side-quests`; types `tees` `sweatshirts` `activewear` `hats` `accessories` `stickers-and-patches` | yes | — |
| | `/products/[handle]/` (every visible listing except `unlock_only`) | yes | — |
| | `/bundles/[slug]/` (slug = id lower-cased without `bnd-`: `buddy-tee` `buddy-crew` `first-visit` `rest-set`; generated once `availableFrom ≤ AS_OF`) | yes | — |
| | `/crew/` · `/crew/[id]/` (`bel mallow gus pippop sip ollie tuck`) | yes | — |
| Bag | `/cart/` · `/checkout/{contact,shipping,review}/` · `/order/?id=` | no | — |
| Community | `/quiz/` · `/stamp-card/` · `/firsts/` | yes | `quiz` `stampCard` `firsts` |
| | `/cheer-wall/` · `/start-a-crew/` (+ `join/#…`) | no | `cheerWall` `crews` (demo) |
| | `/send-a-bel/` (+ `card/#…`, no) · `/bring-a-buddy/` · `/first-visit-plan/` | yes | `sendABel` |
| Help | `/size-guide/` `/shipping/` `/returns/` `/faq/` `/contact/` | yes | — |
| About/legal | `/about/` `/club-rules/` · `/brand/` · `/privacy/` `/terms/` · `/your-data/` | yes · no · yes · no | — |
| Mode | `/waitlist/` (December pre-launch) · `404.html` | yes · no | `waitlist` |

**Flags** are read at build time (`lib/flags.ts`): `off` hides the links and renders a calm "Not open yet" panel (routes are never deleted); `demo` adds `<DemoBadge />` and keeps the route out of the sitemap. **`features.waitlist`** (values: §4.1): `"on"` also puts the waitlist panel on cart and checkout; under `"demo"`, the DemoBar's "Preview the waitlist" (or `?preview=waitlist` on any URL) sets `sessionStorage sf.preview`.

**Header** (sticky, 64px; `scroll-padding-top: 80px` so it never hides focus): wordmark (generated SVG, §4.6) · **Shop** (disclosure menu: *By vibe* 5 · *By type* 6 · *By character* 7 · "Under $35" → `/shop/?under=3500`) · **Meet the crew** · **Stamp card** · **Quiz** · **Help** · **Bag** (count after hydration; opens the drawer). Mobile: wordmark, Bag, Menu (a full-height `<dialog>` sheet with the same groups, items ≥ 44×44 px). **Above it:** the **DemoBar** (non-club builds; not sticky; `canvas` ground, `ink` text) "Demo store: nothing is for sale yet and no payment is taken." with the waitlist preview switch, then the **AnnouncementBar** "Free shipping at {freeShipping}. Same price in every size." (amount from config).

**Footer** (dark: `ink` ground, `oat` text, `butter` headings, 3px `butter` focus ring): **Shop** (vibes, types) · **Community** (stamp card, Firsts, quiz, Send a Bel, Bring a Buddy, the demo cheer wall and crews) · **Help** (size guide, shipping and made-to-order, returns, FAQ, contact) · **About** (about, Club Rules, brand guide) · **Legal** (privacy, terms, your data). Below: `{handle}` as text (never a link to an unverified profile), "{brand} is for people {minimumAge} and up.", and Tuck's "(off camera, on purpose.)" (speaker: tuck) linking to Club Rules.

### 7.5 Page-by-page spec

**Conventions.** Every page: DemoBar, Header, skip link, `<main id="main">`, one `h1`, Footer; breadcrumbs below the top level. Copy: `content/<page>.json` via `t(key, vars)` (`lib/copy.ts`; also fills `{brand} {castNoun} {handle} {domain}`). "#n" = §4.4 example line n, verbatim · "Speaker: x" = a speech bubble with `speaker = x` · "Hosted by x" = brand copy (`speaker: null`), x drawn beside it · "Rules: §4.8 #n" = the page implements that rule. *(new)* = new copy, each line past the §4.4 banned list and copy-lint [L, as Appendix A.6]; founder-editable (tests re-run).
- Loading: §4.5 Motion (client islands). **Error boundary:** "Something went sideways on our end. Your bag's still packed. Try again?" *(new)* [Try again]. **Storage blocked:** `StorageNotice` "Your browser isn't saving anything for this site, so your bag and stamps reset when you close the tab." *(new)*

#### Home: `/`
1. Hero: `h1` = config `tagline` (#1); subhead #2; [Meet the crew] → `/crew/`, [Shop the Small Print] → `/collections/the-small-print/`. Bel `happy`/`wave` beside the `D01-CC17` Ivory Quiet `flat_front` mockup, the LCP image (`fetchpriority="high"`).
2. "Your volume, your call": D01 Quiet (`flat_front`), Loud (`flat_back`), Private (`label`), each with its `tierBlurbs`, linking to `/products/the-door-tee/?tier=<tier>`.
3. Shop by vibe: 5 tiles (title, blurb, host), hidden when empty · 4. Start here: `meet-the-crew.pinned` (≤ 8), else §5.5 order · 5. Meet the crew: 7 CastMembers with catchphrases (speaker: each).
6. Mallow Hours band (dark): Mallow `sleepy`, "mm. rest counts." (speaker: mallow) + "Showing up counts. So does rest."; [Open your stamp card] [Shop Mallow Hours].
7. Quiz CTA: #20 · 8. Made just for you: #10, windows from the `cc1717` blank.
9. Email signup (hosted by Bel): #9, **inline**; "maybe later" collapses it (`sf.prefs`). **No pop-ups anywhere.** Success: "You're on the list. Demo: nothing was sent." *(new)* (club mode drops the second sentence); invalid: #12.
- Accept: `h1` = config tagline (rename test) · hero has `width`/`height` · both halves in the Mallow band · flow 16.

#### Shop all: `/shop/`
- `h1` "Shop everything" *(new)*. Filters: desktop sidebar; mobile [Filter and sort] → `Sheet` with [Show {n} items]. Polite live count; ProductCard grid (§4.5 columns) of every visible listing, no pagination.
- Filters (URL params; AND across groups, OR within): `vibe` · `type` · `character` (`Design.characters`) · `size` (any colour has it) · `colour` (`neutral`/`pastel` from `GarmentColor.neutral`, or a code) · `tier` ("Has a Quiet version" / "Has a Private version") · `under=3500` (lowest tier price). Sort: `featured` (drop, then §5.5 order) · `new` · `price-asc` · `price-desc`.
- ProductCard (summary array serialised at build): default-tier mockup, first neutral colour · title · default-tier price ("$34", + "Private $28" if offered) · "+{n} colours" · the real size range ("S–4XL"; never sitewide, §5.8). No results: "Nothing matches all of that. Try removing a filter." *(new)* [Clear filters]. Suspense fallback = the unfiltered grid (= static HTML). Accept: flow 2.

#### Collection: `/collections/[handle]/` (all 11)
Title, `Collection.blurb`, host (`the-small-print` Tuck `shy` · `meet-the-crew` Bel `happy` · `buddy-system` Pip & Pop `hyped` · `mallow-hours` Mallow `sleepy`, dark band · `side-quests` Ollie `surprised` · type collections: none). Shop's filter island minus the fixed group; cards link with `?tier=<openTier>`; `side-quests` cards show `windowNote`, no timers; `buddy-system` leads with a Buddy Pack tile; `mallow-hours` pairs a rest line with a show-up line; last, an "Other vibes" row. Empty: "Nothing in here yet. The crew's working on it." *(new)* Accept: membership = `listing.collections` (§5 `collections` test) · Small Print cards open on Quiet.

#### Cast index and character page: `/crew/`, `/crew/[id]/`
- Index: 7 cards grouped Lead / Core / Supporting, plus a text-only teaser of the yearly vote (Cora vs Skip; no art).
- Character page: CastMember (default expression and pose), `h1` = name, "the {altObject}", catchphrase (speaker: the character) · "The nervous bit: {nervousBit}" (`characters.json`) and personality; `trigger` is internal, shown on no page · all 10 expressions (Ollie's mouth never changes; hover bounce `motion-safe`) · cleared voice lines (§4.4) · "Wear {name}": visible listings with the character, then the quiz CTA. No products: "{name}'s own piece arrives later. For now, {name} is on the Collect the Crew sticker sheet." *(new)* + the `D11-SH505` card.
- Accept: 7 pages; alt per §7.11.

#### PDP: `/products/[handle]/`
**URL state** `?tier=&color=<code, lower-case>&size=`. Tier defaults to `listing.defaultTier` (or the collection's `openTier`); colour to the first `neutral: true` (neutrals first for Dev). **Size is never preselected.**
1. Gallery: `Mockup[]` for option × tier (`flat_front`, `flat_back`, `detail`, `label` for Private, `pair` for buddy halves); 4:5 tiles, "1 / 4" counter, [Previous]/[Next] (swipe never the only way, WCAG 2.5.7), desktop thumbnails, first image only preloaded. "See it at a glance" *(new)*, helper "From a few steps back it reads as a good vintage tee." *(new)*: the front at 25% on a `canvas` tile.
2. Title block: `h1` (Caprasimo), tagline (the lowercase slogan), the tier's price (Atkinson 800, `tabular-nums`), "Same price in every size, {size_range}." (selected colour's `BlankColor.sizes`).
3. TierPicker ("How loud?"): radiogroup of `listing.tiers` with `tierBlurbs` (`{whisper}` from `designs.json`); Private adds "Inside label only. Tees only." *(new)* and a "More quiet things" *(new)* link to the Small Print. Changing it swaps gallery, price, URL; `tiers: ['none']`: no picker.
4. SwatchPicker: radiogroup, visible "Colour: Ivory" label, ring + check, 1.5px `ink-soft` border, fill `GarmentColor.approxHex`, note "Colours on screens are close, not exact." *(new)*
5. SizePicker: chips; sizes not in this colour (`BlankColor.sizes`) disabled with "4XL: not in this colour" *(new)*; then [Size guide], `fit.note`, `copy.sizeNote`.
6. Add to bag: sticky on mobile once scrolled past (`scroll-padding-bottom`). No size: "Pick a size first." *(new)* inline, focus to the sizes, no emoji. Success: toast #5 (hosted by Gus), [View bag] opens the drawer. Waitlist mode: `WaitlistForm`.
7. Made just for you: `MadeToOrderNote` (#10), windows from `Blank.productionDays` and `transit.json`, + `DeliveryEstimate` ("Arrives about {date range}"). **Any `null` shows a visible TBC** (§3 rule 4).
8. Bundle callout (`bundleIds` set): the §5.9 line → `/bundles/buddy-tee/`.
9. Accordion: Description · Fit and sizing · Fabric and care (`Blank.fabric`/`care`, else the §5.8 fallback [U]) · Print details (technique; inches = `artBoxPx` or `canvasPx` ÷ `dpi` from `print-specs.json`, only when the area's `verified.value === true`, else "Print size: TBC") · Shipping and returns.
10. "Is it see-through?" (§5.9) only when `gate.kind === 'squat_test'` and `status === 'passed'` · 11. Who's on this (→ `/crew/[id]/`), Pairs well with (visible `crossSell`, 2–4).
12. Reviews: empty state only, "Reviews open after launch. We'll only ever show real ones." *(new)* **No stars, no sample reviews, no `aggregateRating`.**
- Data: the server component reads `getListing()` + its `Blank`, `Design`, `SizeGuide`, mockups, spec sizes; client islands: Gallery, pickers, AddToBag. No size chart: §5.8 TBC (can't be `active`) · `partner_out_of_stock`: #14, size disabled. Accept: no literals in the lead-time block (grep) · flows 7, 16, 17 · `listing-ready`.

#### Bundle builder: `/bundles/[slug]/`
Buddy Pack: design (D08; D18 from drop 2) → **one tier for the pair** ($60; Private pair $48) → colour and size for Tee A, then Tee B → [Add both to bag]: two lines sharing a `bundleGroup`. `/bundles/buddy-tee/` shows `D08A-CC17`'s pair mockup. −$8 only while both halves are present at equal quantity, else "The Buddy Pack price needs both tees." *(new)* "Send this pair to your gym person" *(new)* copies `/bundles/buddy-tee/?design=D08`. Later bundles reuse this template.

#### Cart drawer and cart page: `CartDrawer`, `/cart/`
- Drawer: `ui/Dialog` (§7.6); `/cart/` renders the same `CartContents`. Lines: thumbnail, title, "Quiet · Ivory · M", unit price, stepper (1–10), [Remove]; buddy halves grouped with their −$8 line; $0 lines read "Free with your order".
- FreeShippingBar (polite live region): #13, `{amount}` = `remainingForFree`; then "Free shipping is on." *(new)*, ≤ 1 sparkle (none under reduced motion).
- Codes: one discount code + any number of Firsts sticker codes. Errors: "That code didn't work. Check the spelling?" · "One code per order, so we kept the first one." · "Add anything else and your sticker rides along free." *(all new)*
- Then: gift note (≤ 200 characters, banned-list checked; "Add a gift note" *(new)*) · totals: shipping $4.75 + $2.20 per extra item or Free, "Tax: calculated at checkout (demo: $0.00)" *(new)* · #10 · ≤ 2 add-ons under $15 (`MIX-STK3`, `D11-SH505`) below the threshold · [Check out].
- Prices from `/catalog-index.json` (SKU → listing, price, option name, size, thumbnail, margin-exception flag), **never storage**. Unknown SKU: dropped, "One item left the shop, so we took it out of your bag." *(new)* Empty: #6 (hosted by Gus) · skeletons until hydrated and the index loads · waitlist mode: the waitlist panel.

#### Checkout (mock): `/checkout/{contact,shipping,review}/`
- Every step: `pool` banner **"Demo checkout: no payment is taken."** (§3 rule 6, exact) · "Step 1 of 3: Contact" (`aria-current="step"`) · order summary (collapsible on mobile). **Never** payment fields, card iframes or "Pay" wording. Draft: `sessionStorage` `sf.checkout`; one route per step (back works); an incomplete draft redirects to the first incomplete step.
- Contact: email (`autocomplete="email"`), first name (`given-name`), **unchecked** "Send me the First Visit Plan"; no account. Shipping: name · address lines 1–2 · city · state (US `<select>`) · "Zip code" (5 or 5 + 4 digits; never "ZIP", §4.4) · country fixed to United States (`markets`); one method, "Standard", price or Free plus the delivery window. Review: lines, address, email, each with [Edit] (values carry over, never re-asked: WCAG 3.3.7) · totals · [Place demo order] + "No card needed. This is a prototype." *(new)*
- Placing: `adapter.checkout.begin()` returns `{ kind: 'mock-order', orderNumber }` (`1001`, `1002`, … per browser, `-`, 4 random digits; no letters); saved to `sf.orders`; cart and draft cleared; → `/order/?id=`. Errors: focused summary linking to fields; per field `aria-invalid` + `aria-describedby` + inline text (#12 for email; "Check the zip code: 5 digits, or 5 + 4." *(new)*). #11 stays in `content/checkout.json` for go-live.
- Accept: no `input` name or autocomplete matches `/card|cc-|cvc|iban/i` · banner on all 3 steps · flows 1, 13.

#### Order confirmation: `/order/`
Pip & Pop `high-five` (a spec pose: build, render, inspect it first, §4.7) with #7 (hosted by Pip & Pop) · `{production_window}` = the widest across the lines · number, lines, totals · timeline Ordered → Printing ({production_window}) → On its way ({transit_window} or TBC) → Arrives · "Demo: no email is sent." *(new)* · **Send a Bel** (primary): "Know someone starting the gym? Send them a Bel. It's free." *(new)* · "Put today on your stamp card" *(new)*. Unknown id: "We can't find that order on this device. Demo orders live only in this browser." *(new)* Accept: survives a refresh · Clear my data removes it.

#### Quiz: `/quiz/` ("Which {castNoun} are you?")
Rules: §4.8 #5. Intro #20 → six questions, one per screen (radiogroup, [Next]/[Back], "Question 2 of 6", no timer) → **the result, before any email ask**. Each answer is +1 for its character; highest wins; ties go to the Q6 answer if tied, else the first in bel › tuck › gus › mallow › pippop › sip. New copy (`content/quiz.json`):

| # | Question | Answers → character |
|---|---|---|
| 1 | It's your first time at a new gym. What's the plan? | Sit in the car for a sec, then go in → bel · Find the quietest corner → tuck · Bring a friend so I'm not alone → pippop · Walk in like I've been away a while, because I have → gus |
| 2 | Pick one thing for your gym bag. | A big water bottle → sip · Headphones → tuck · A cosy layer for after → mallow · My gym person → pippop |
| 3 | A friend says they went to the gym today. You say… | Proud of you. Did you drink water? → sip · Nice. You don't have to tell me more → tuck · Want to go together next time? → pippop · Good. Now rest → mallow |
| 4 | Your pace this week: | Slow and steady, rest days included → mallow · Back after a break, no big fuss → gus · One new thing, then home → bel · Whatever my buddy's doing → pippop |
| 5 | How loud should your shirt be? | Quiet: a tiny friend on the chest → bel · Loud: a big friend on my back → sip · Private: a secret on the inside label → tuck · Somewhere in the middle → gus |
| 6 | Best part of the gym? | Getting in the door. I did it → bel · The stretch area → mallow · The water fountain → sip · Heading home, done for the day → gus |

Result card: CastMember (`proud`; `hyped` for Sip and Pip & Pop) · "You're {name}." *(new)* · the catchphrase (speaker: the character) · three launch products · the landing collection: bel `D01-CC17` `D02-BC30` `D10-Y624` → `the-small-print` · tuck `D03-CC17` `D10-G180E` `MIX-STK3` → `the-small-print` · gus `D04-CC17` `D05-G180` `D09-G185` → `meet-the-crew` · mallow `D06-G180` `D11-SH505` `D07-W788` → `mallow-hours` · pippop `D08A-CC17` `D08B-CC17` + Buddy Pack → `buddy-system` · sip `D07-W788` `D11-SH505` `MIX-STK3` → `meet-the-crew`.

Below it, no email needed: the First Visit Plan link and "Your code: `firstvisit10` (10% off your first order)" *(new)* (codes lower-case in `<code>`, accepted in any case); then an optional "Want the plan by email too?" *(new)* (`EmailAdapter`) and [Retake the quiz]. Accept: every result shows ≥ 2 visible products at `AS_OF` 2027-01-05 · email never blocks the result · the result survives reload (`sf.quiz`) · every character can win (unit test).

#### Stamp card and day-one line: `/stamp-card/`
Rules: §4.8 #1, #3–4. Logic `lib/community/stamps.ts` (§7.8); data `sf.stamps`.
1. Header: "Bel's Stamp Card" *(new)*; **Showed-up weeks** and **Total stamps** big; the **day-one** ribbon ("day one: {date}") where the card starts. "day one" stays a lowercase label, never a feature name (§4.1).
2. Stamping: [Stamp a visit] (Bel's stamp) replies "okay. okay. we're in." (speaker: bel); [Stamp a rest day] (Mallow's) replies #15 (speaker: mallow). "Change today to a rest day" / "…to a visit" switches the kind; totals unchanged.
3. Grid: weeks as rows, Monday first; butter stamps, ink outline; empty days blank. "Forgot a day?" backfills 6 days, never future ones. A gap ≥ 7 days shows #16 (hosted by Gus), never the gap length.
4. Milestone stickers (§4.8 #2; landing per §4.5 Motion), default *(new; log it in decisions.md)* 1 Bel `proud` · 5 Tuck `shy` · 10 Gus `chill` · 25 Mallow `sleepy` · 50 Pip & Pop `hyped` · 100 Ollie `surprised` (SVG).
5. Settings (off by default): "Mallow's rest nudge" (when `shouldNudgeRest()`: "mm. how about a rest day? it counts.", speaker: mallow) · "Weekly reminder (demo: nothing is sent)" *(new)*.
6. [Download my card] · [Clear my card], confirm "Clear every stamp on this device? This can't be undone." *(new)*
- Accept: no DOM text matches `/streak|missed|broke/i` (plus the `stamps` test and flow 8).

#### Firsts: `/firsts/`
Rules: §4.8 #2 (also no ranks or percentages); its six badges, in order, are B1–B6 (`content/firsts.json`, §5.2). [I did this] asks "No proof needed. We believe you." *(new)*; the badge shows its character, the date and a code `first-b<n>-<4 chars>` (lower-case base32, `crypto.getRandomValues`). In the cart the code adds `D12-N-STK3-B<n>-OS` at $0; it needs ≥ 1 paid line, once per badge per order.

#### Cheer wall (demo): `/cheer-wall/`
Rules: §4.8 #9. `DemoBadge`, "Sample posts (demo). Your posts stay on this device." *(new)*, hosted by Ollie. Composer: the three prompts; ≤ 140 characters, live count; `lib/community/moderation.ts` checks the banned list and `brand/blocklist.json` and rejects URLs and `@`: "Let's keep the wall about showing up. Try different words?" *(new)* **No photo upload in the prototype.** Seeds: ≥ 8 in `content/cheer-wall.json` (`sample: true`, labelled "Sample post"), e.g. "First time I asked where the mats were." Replies: the four presets ("oh!" is speaker ollie), one each per post. [Report] hides a post into a demo moderation queue (`sf.cheers`). Links to Club Rules.

#### Start a Crew (demo): `/start-a-crew/`, `/start-a-crew/join/#<payload>`
Rules: §4.8 #8. Create: a name matching `^[A-Za-z0-9 .'-]{1,16}$`, past the banned list and blocklist, shown as typed (the hoodie preview uses capitals in SVG paths only), plus a display name ≤ 24. Crew page: you + 2–5 "Demo member"s from `content/crews.json` (max 8) and the **combined stamp total** (your `totals().total` + the demo totals). Invite: `/start-a-crew/join/#` + base64url JSON `{ v: 1, name, code }`; the join page re-validates, then "{crew} invited you." *(new)* [Join this crew]; bad payload: "That invite link doesn't look right. Ask your crew to send it again." *(new)* Hoodie and group checkout: teaser "Crew hoodies come later." *(new)* until `features.crews` is `on` and D27 is visible.

#### Send a Bel: `/send-a-bel/`, `/send-a-bel/card/#<payload>`
Rules: §4.8 #11. Fields: "To" and "From" (optional, ≤ 24 each) · the **custom first line** (≤ 60, + blocklist) · Bel's expression (`proud`/`hyped`/`happy`); fixed line = config tagline. Preview: 1200×630 (inline Bel SVG + text), auto-fit via `measureText` after `document.fonts.load()`. **[Download the card as an image]:** SVG into a `<canvas>`, text via `fillText`, `toBlob('image/png')` (web fonts reach canvas text but not an `<img>`-loaded SVG [U: confirm in the e2e screenshot]). **[Copy link]:** `/send-a-bel/card/#` + base64url JSON `{ v: 1, to, line, from, expr }`. Card page: re-validates (failures render the default card), then "Make it a real gift" *(new)* → `meet-the-crew` and a gift-note hint; `noindex`, OG `/og/send-a-bel.png`; nothing is sent, no email field.

#### Bring a Buddy and First Visit Plan: `/bring-a-buddy/`, `/first-visit-plan/`
- Buddy link: [Make my buddy link] → `/bring-a-buddy/#{ v: 1, code }`. The opener reads "Your gym person sent you this. You both get the Collect the Crew sticker sheet, or 15% off." *(new)* and picks `buddy-sheet-<4>` (adds `D11-SH505` at $0) or `buddy15-<4>`; the sender gets the same choice locally (demo). Neither stacks with `firstvisit10` (§5.7). Club mode shows the live codes (§7.3).
- First Visit Plan (Rules: §4.8 #12; `content/first-visit-plan.json`): printable (`@media print` drops the chrome; ink on white); machines described by **what they are and where the little sticker is** (never form, frequency or body advice; equipment-only diagrams); ends "you can leave whenever you want".
- Accept: print emulation hides the chrome · banned-list scan passes.

#### Club Rules (consent-first filming): `/club-rules/`
Rules: §4.8 #10. Hosted by Tuck `shy`, "(off camera, on purpose.)" (speaker: tuck). Copy (`content/club-rules.json`, all *(new)*): 1. We never film strangers. 2. Share your fit and your gear laid flat, or film yourself with nobody else in frame. 3. We never repost anything with people in the background. 4. We never feature body photos. 5. This site and its community are for people {minimumAge} and up. 6. We only help when someone asks. Then the UGC prompt (#21). Linked from the footer, the cheer wall and every UGC form (link test).

#### Size guide: `/size-guide/` (+ `SizeGuideDialog`)
Intro #4; one table per `catalog/size-guides/<productKey>.json`, columns = the partner's `measurementKeys` exactly; in/cm `<button aria-pressed>` (cm = in × 2.54, rounded to 0.5; `sf.prefs`); source line "From our print studio's size chart, checked {checkedAt}"; a laid-flat how-to-measure drawing (**no body**). Missing guide: the §5.8 TBC text, never interpolated. Dialog title "Size guide: {blank title}". Accept: each visible listing's sizes are covered, or TBC.

#### Shipping and returns: `/shipping/`, `/returns/`
`golive/policies/{shipping,returns}.md` (§8) via `marked`, inside `data-copy-surface="legal"` (§4.4), under "Draft for legal review. Not legal advice." *(new)*; until §8 writes them, data blocks only. Shipping: #10 · production window per product type (`Blank.productionDays` + tag), transit (`transit.json`, TBC) · "$4.75 for the first item, $2.20 for each extra, free at $75" (from data) · US only · split-shipment note · #19 as the delay example. Returns: misprints and damage replaced (Printful reprints within 30 days [V]; customer window per §8) · size exchanges per §8. Accept: no hard-coded day counts (grep).

#### FAQ: `/faq/`
`content/faq.json` as `<details>` with anchors, numbers from placeholders. At minimum: Quiet, Loud and Private (`#tiers`) · Do bigger sizes cost more? (No) · Is it see-through? · Why does it take a few days? · Where do you ship? (US) · Returns and exchanges · The stamp card · Where my data is kept · Who the crew are · Is this store real yet?

#### About: `/about/`
The manifesto **verbatim** (§4.2; test: matches `content/about.json`), hosted by Bel going from `nervous` to `proud` · the three pillars · "The Glare" (never drawn, no eye motifs) · each character's "The nervous bit" line (`nervousBit`, never `trigger`).

#### Brand guide: `/brand/` (D1, `app/brand/`)
`noindex`; from source: token swatches · contrast table recomputed from `tokens.json` · type scale · lockups and favicons (`public/brand/`) · the cast in 10 expressions · voice rules and cleared lines · the banned list inside `data-copy-exempt` (§4.4 scope rule 1: this route only) · misuse rules.

#### Contact: `/contact/`
Static stub, no form: "Questions about fit, an order, or anything else? A real person answers." *(new)* · `mailto:hello@{domain}` with "Demo: this inbox isn't set up yet." *(new)* · response time and postal address: TBC [U, founder].

#### Privacy, Terms, Your data: `/privacy/`, `/terms/`, `/your-data/`
Privacy and Terms: `golive/policies/{privacy,terms}.md` (§8) inside `data-copy-surface="legal"`, under the draft banner; the privacy draft states: no cookies, analytics or third-party scripts; nothing is sent; the storage keys (`lib/storage-registry.ts`); 13+. **`/your-data/`:** the disclosure (§7.8, with its club-mode line), the registry table (key, what it holds, when cleared), [Download my data] (one JSON of every `sf.*` key), [Clear my data] (confirm → remove every `sf.*` key from both storages → reset the stores → reload).

#### Waitlist mode: `/waitlist/` (+ every buy surface)
When `features.waitlist` is `on` or previewed: `AddToBag` → `WaitlistForm` (email + optional "Which piece?"; `EmailAdapter` list `waitlist`) · no bag icon · `/cart/` and `/checkout/*` show the waitlist panel · Home CTAs → [Join the waitlist] [Send a Bel]. Page: the §4.4 launch line "New year, no pressure. No resolutions needed." (exact: it passes only via the `no resolutions needed` allow rule) · "We open on Tuesday 5 January. One email when we do, then nothing unless you ask." *(new)* · links to the quiz, Send a Bel, the First Visit Plan.

#### 404: `app/not-found.tsx` → `out/404.html`
Ollie `surprised`/`wave` with #8 (hosted by Ollie), [Back to the shop], links to vibes, crew, help. Accept: `/nope/` serves it under `serve` [U: confirm serve 14's 404 handling] · one `h1` · axe clean.

### 7.6 Component inventory

Server components by default; (c) = `'use client'`. Interactive elements are ≥ 44×44 px and follow §4.5's component map. The client fetches only `/catalog-index.json` and images (same-origin).
- `layout/`: DemoBar (c) · Header · MobileMenu (c) · Footer · AnnouncementBar · SkipLink · Breadcrumbs, from `lib/brand.ts` and `lib/flags.ts`; no gender labels; Help in a fixed place.
- `cast/CastMember` (animated variant: c): `id expression pose lod garment size title` → inline SVG from §6's generators (`art/characters/`). §4.7's component (never named after the brand: §4.1 name grep); `role="img"` + `<title>` with the generated alt; `useReducedMotion()` guard; never-recoloured fill test; `cast-component` test (§7.14). `cast/SpeechBubble` (`speaker: CharacterId | null`, `copyKey`) emits `data-speaker`, so the post-build copy-lint applies voice rules.
- `ui/`: Button · IconButton (needs `aria-label`) · Chip · DemoBadge · Toast (c) · Banner · DarkSection (sets `data-surface="ink"`), variants and disabled state per §4.5 · Dialog, Sheet (c; native `<dialog>` + `showModal()`; focus to the heading, Esc closes, focus returns, background `inert`) · RadioCards, RadioChips, Accordion, Field, ErrorSummary, Stepper (form ones c; visible labels, errors via `aria-describedby`, arrow keys in radiogroups) · Loading (c), StorageNotice (c), NotOpenYet (reduced motion: static Bel).
- `ui/ResponsiveImage` (`Mockup`): `srcset` = `<src>` 1440w, `<src minus .webp>-960.webp` 960w, `-480.webp` 480w (§6.8); explicit `width`/`height`. Pair mockups `/mockups/<handle>/<option>-<tier>-pair.webp` sit on each half's listing.
- `product/`: ProductCard · ProductGrid · FilterBar, FilterSheet, SortSelect (c; URL state, live count) · Gallery, TierPicker, SwatchPicker, SizePicker, SizeGuideDialog, AddToBag, WaitlistForm (c; ARIA radio pattern; `Listing`, `Blank`, `SizeGuide`, `print-specs.json`) · FitNote · PrintDetails · CrossSell · ReviewsEmpty · MadeToOrderNote, DeliveryEstimate (c) from `Blank.productionDays`, `transit.json`, `lib/delivery/window.ts`: `null` → TBC; business days skip Sat/Sun; holidays not modelled [U].
- `cart/` (c; `useCart()` → adapter; live regions: CartDrawer, CartContents, FreeShippingBar, CodeField, …) · `checkout/` (c; `sf.checkout`; no payment inputs, tested: StepIndicator, the three step forms, OrderSummary, DemoCheckoutBanner) · `community/` (c; stores §7.8; one per §7.5 block, e.g. StampCard, FirstsGrid, QuizRunner, CheerComposer, CrewInvite, ECardMaker, BuddyLink; a grep test fails on any `Streak`, `Missed` or `Rank` component name) · `brand/` (`/brand` only, from `brand/*.json`).
- `StoreHydrator` (c, root layout) rehydrates every persisted store after mount and exposes `useHydrated()`.

### 7.7 Tokens → Tailwind v4 and self-hosted fonts

`npm run brand` writes `styles/tokens.css` from `brand/tokens.json`, headed `/* GENERATED — do not edit */` (exempt from the §4.5 hex grep):

```css
@theme {
  --color-*: initial;   /* drop Tailwind's default palette [U: confirm the v4 reset syntax, then grep the built CSS for non-token colours] */
  /* one --color-<token> per brand/tokens.json colour except lilac-shade (generated) */
  --font-display: var(--font-caprasimo), Georgia, serif;
  --font-sans: var(--font-atkinson), system-ui, sans-serif;
  --text-display: clamp(2.75rem, 6vw, 4.5rem); --text-display--line-height: 1.05; --text-display--letter-spacing: -0.01em;
  /* …h1 h2 h3 h4 eyebrow body-lg body small meta button price, exactly as the §4.5 type scale… */
  --radius-pill: 999px; --radius-card: 20px; --radius-tile: 24px; --radius-input: 14px;
  --shadow-sticker: 0 3px 0 0 var(--color-ink);
}
```

**`app/globals.css`:** `@import "tailwindcss"; @import "../styles/tokens.css";` · `body { background: var(--color-oat); color: var(--color-ink); font-size: 1.125rem }` · `:focus-visible { outline: 3px solid var(--color-ink); outline-offset: 2px }`, `[data-surface="ink"] :focus-visible { outline-color: var(--color-butter) }` · the §4.5 reduced-motion block (animation and transition durations `1ms`) · spacing on Tailwind's 0.25rem base, only the §4.5 steps 1 2 3 4 6 8 12 16 24 32.

**Rules** (`tests/unit/tokens-usage.test.ts` + ESLint): no arbitrary colours (`bg-[#…]`) · `text-coral|butter|lilac|bubblegum|sage|pool|pistachio` only inside `DarkSection` · **class-pair test:** a `className` with both a `text-*` and a `bg-*` token matches a §4.5 allowed pair · `font-display` never below `h3` (Caprasimo ≥ 28px).

**Fonts** (self-hosted, no runtime CDN): `npm run brand` copies WOFF2 from `@fontsource/caprasimo` (latin) and `@fontsource-variable/atkinson-hyperlegible-next` (latin + latin-ext, upright and italic) into `public/fonts/` (exact names: each package's `files/` folder [U]; licences in `licenses/fonts.json`). `next/font/local` in `app/layout.tsx` loads them (`variable: '--font-caprasimo'` / `'--font-atkinson'`, `weight: '200 800'` for the variable file), giving `font-display: swap` and fallback metrics. Preload exactly two: Caprasimo latin and Atkinson latin upright. Print TTFs (`@expo-google-fonts/*`) are §6's; the site never loads them.

### 7.8 Client state, storage and the disclosure

**Storage registry.** Every key is registered once in `lib/storage-registry.ts`, which the `/your-data/` table, Download and Clear read; a test asserts every `persist({ name })` in `stores/` is registered. Keys start `sf.` (never the brand name). All access goes through `lib/storage.ts` (try/catch; in-memory fallback triggers `StorageNotice`).

| Store | Key | Storage | Holds | Also cleared by (Clear my data clears every key) |
|---|---|---|---|---|
| cart | `sf.cart` | local | `{ sku, quantity, bundleGroup?, unlockCode? }[]`, code, gift note: **never prices** | order placed |
| checkout | `sf.checkout` | **session** | email, first name, address, plan opt-in | order placed · tab closed |
| orders | `sf.orders` | local | last 5 demo orders: number, date, lines, totals, first name, masked email (`f•••@example.com`) | — |
| stamps | `sf.stamps` | local | `StampState` (below) | Clear my card |
| firsts · quiz · codes | `sf.firsts` · `sf.quiz` · `sf.codes` | local | badges (date, code, redeemed) · answers and result · issued codes | quiz: Retake |
| cheers · crews | `sf.cheers` · `sf.crews` | local | own posts, replies, reported ids · crews created or joined | — |
| prefs | `sf.prefs` | local | in/cm, dismissed blocks, list flags (**no email addresses**) | — |
| preview | `sf.preview` | session | waitlist demo preview | tab closed |

**Persist rules:** every store has `version: 1`, `partialize`, `skipHydration: true`, `storage: createJSONStorage(() => safeStorage)` and a `migrate()`, one fixture per version (`tests/unit/migrations.test.ts`); an unknown shape resets to empty, never throws. The cart persists `{ lines, code, giftNote }`; `migrateCart`: v0 `{items:[{sku,qty}]}` → v1 lines; unknown shape → empty bag. The wrapper was type-checked with Zustand 5.0.16 under TS 5.9.3 and 6.0.2 strict [L]:

```ts
// lib/storage.ts
import type { StateStorage } from 'zustand/middleware';
const memory = new Map<string, string>();
export let storageWorks = true; // false → <StorageNotice />
export const safeStorage: StateStorage = {
  getItem: (k) => { try { return window.localStorage.getItem(k); } catch { storageWorks = false; return memory.get(k) ?? null; } },
  setItem: (k, v) => { try { window.localStorage.setItem(k, v); } catch { storageWorks = false; memory.set(k, v); } },
  removeItem: (k) => { try { window.localStorage.removeItem(k); } catch { memory.delete(k); } },
};
```

**Stamp card logic** (`lib/community/stamps.ts`) [L]: in 200 seeded runs × 300 operations (add, backfill, change kind, rehydrate, jumps up to 19 days), totals never decreased and no future stamp was stored; ISO weeks correct for 2025-12-29 → `2026-W01`, 2027-01-03 → `2026-W53`, 2027-01-04 → `2027-W01`; the nudge fired at 6 visits in 7 days with no rest, only when opted in.

```ts
export type LocalDate = `${number}-${number}-${number}`; // the visitor's local date
export type StampKind = 'visit' | 'rest'; // both count fully
export interface Stamp { readonly date: LocalDate; readonly kind: StampKind }
export interface StampState {
  readonly dayOne: LocalDate | null; // set by the first stamp; never moves later
  readonly stamps: readonly Stamp[]; // append-only, at most one per date
  readonly high: { readonly total: number; readonly weeks: number }; // high-water marks
  readonly restNudge: boolean; // opt-in, default false (§4.8 #3)
}
export const EMPTY_CARD: StampState = { dayOne: null, stamps: [], high: { total: 0, weeks: 0 }, restNudge: false };
export const BACKFILL_DAYS = 6;
const toUtc = (d: LocalDate) => { const [y, m, day] = d.split('-').map(Number) as [number, number, number]; return Date.UTC(y, m - 1, day); };
export const daysBetween = (a: LocalDate, b: LocalDate) => Math.round((toUtc(b) - toUtc(a)) / 86_400_000);
export function isoWeekKey(d: LocalDate): string { // ISO 8601 week, Monday start
  const t = new Date(toUtc(d));
  t.setUTCDate(t.getUTCDate() - ((t.getUTCDay() + 6) % 7) + 3); // Thursday of the same week
  const year = t.getUTCFullYear();
  return `${year}-W${String(1 + Math.floor((t.getTime() - Date.UTC(year, 0, 1)) / (7 * 86_400_000))).padStart(2, '0')}`;
}
export function totals(s: StampState): { total: number; weeks: number } {
  const weeks = new Set(s.stamps.map((x) => isoWeekKey(x.date))).size;
  return { total: Math.max(s.stamps.length, s.high.total), weeks: Math.max(weeks, s.high.weeks) };
}
export function addStamp(s: StampState, date: LocalDate, kind: StampKind, today: LocalDate): StampState {
  const age = daysBetween(date, today);
  if (age < 0 || age > BACKFILL_DAYS || s.stamps.some((x) => x.date === date)) return s; // no future, no duplicates
  const stamps = [...s.stamps, { date, kind }].sort((a, b) => a.date.localeCompare(b.date));
  const next = { ...s, stamps, dayOne: s.dayOne === null || date < s.dayOne ? date : s.dayOne };
  return { ...next, high: totals(next) };
}
/** Switch a day between visit and rest. Totals stay the same: there is no "unstamp". */
export function changeKind(s: StampState, date: LocalDate, kind: StampKind): StampState {
  return { ...s, stamps: s.stamps.map((x) => (x.date === date ? { date, kind } : x)) };
}
export function shouldNudgeRest(s: StampState, today: LocalDate): boolean {
  if (!s.restNudge) return false;
  const week = s.stamps.filter((x) => { const a = daysBetween(x.date, today); return a >= 0 && a < 7; });
  return week.filter((x) => x.kind === 'visit').length >= 6 && !week.some((x) => x.kind === 'rest');
}
/** The only way the numbers go down: the visitor's own "Clear my card" (tap plus confirm). */
export const clearCard = (): StampState => EMPTY_CARD;
```

**"Today"** = `new Intl.DateTimeFormat('en-CA').format(new Date())` (local `YYYY-MM-DD`); injected in unit tests, `page.clock` in e2e.

**The disclosure** (`/your-data/`, privacy draft) says plainly what each key holds, that nothing leaves this browser, that there are no cookies, and that Clear removes everything; no consent banner is needed for this functional storage alone [U: legal view, §8]. **Club mode** says instead: "Your stamps, Firsts and quiz answers never leave this browser. We count page visits and a few anonymous totals with a cookie-free counter; it never sees what you logged or answered." *(new)*

### 7.9 CommerceAdapter: mock now, Shopify later

**Import rule.** UI imports **only** `@/lib/commerce`; ESLint `no-restricted-imports` bans `lib/commerce/{mock,shopify}/*` outside `lib/commerce/index.ts`, which picks the adapter from `process.env.NEXT_PUBLIC_COMMERCE_PROVIDER ?? 'mock'` and **throws at build time** if a non-mock provider lacks its env. Type-checked against §5's `types.ts` under TS 5.9.3 and 6.0.2 strict [L]:

```ts
// lib/commerce/types.ts
import type { Bundle, BundleId, Collection, Listing, ListingId, Money } from '@/lib/catalog/types';
export type ProviderId = 'mock' | 'shopify';
export interface CartLineInput {
  readonly sku: string; // SKU_RE (lib/catalog/ids.ts): the one join key
  readonly quantity: number; // integer 1..10
  readonly bundleGroup?: string; // same value on both halves of a Buddy Pack
  readonly unlockCode?: string; // Firsts sticker or free-sheet code: a $0 line
}
export interface CartLine extends CartLineInput {
  readonly id: string; readonly listingId: ListingId;
  readonly unitPrice: Money; // from the catalog index at render time, never from storage
  readonly lineTotal: Money;
  readonly promo: boolean; // $0 line: no codes, not counted for shipping or the threshold
}
export interface CartDiscount { readonly kind: 'bundle' | 'code'; readonly label: string; readonly amount: Money }
export interface Cart {
  readonly lines: readonly CartLine[]; readonly merchandiseSubtotal: Money; readonly discounts: readonly CartDiscount[];
  readonly qualifyingSubtotal: Money; // after discounts, $0 lines excluded: the free-shipping base
  readonly shipping: { readonly amount: Money; readonly free: boolean; readonly remainingForFree: Money };
  readonly tax: null; // mock never computes tax: "calculated at checkout"
  readonly total: Money; readonly code: string | null; readonly giftNote: string | null;
  readonly notices: readonly string[]; // content keys, e.g. 'cart.notice.itemRemoved'
}
export interface Address {
  readonly name: string; readonly line1: string; readonly line2?: string; readonly city: string;
  readonly region: string; readonly postalCode: string; readonly countryCode: 'US'; // brand.config markets
}
export interface CheckoutInput { readonly email: string; readonly firstName: string; readonly shipTo: Address; readonly planOptIn: boolean }
export type CheckoutResult =
  | { readonly kind: 'redirect'; readonly url: string } // Shopify cart.checkoutUrl (go-live)
  | { readonly kind: 'mock-order'; readonly orderNumber: string }; // prototype: '1001-4821'
export type ApplyCodeResult =
  | { readonly ok: true; readonly cart: Cart }
  | { readonly ok: false; readonly reason: 'unknown' | 'one-code-only' | 'needs-paid-item' | 'already-in-bag' };
export interface CatalogReader { // build time only (server components)
  listListings(filter?: { readonly collection?: Collection['handle'] }): Promise<readonly Listing[]>;
  getListing(handle: string): Promise<Listing | null>;
  listCollections(): Promise<readonly Collection[]>;
  getCollection(handle: Collection['handle']): Promise<Collection | null>;
  getBundle(id: BundleId): Promise<Bundle | null>;
}
export interface CartService { // browser only
  get(): Promise<Cart>; addLines(lines: readonly CartLineInput[]): Promise<Cart>;
  setQuantity(lineId: string, quantity: number): Promise<Cart>; removeLine(lineId: string): Promise<Cart>;
  applyCode(code: string): Promise<ApplyCodeResult>; removeCode(): Promise<Cart>;
  setGiftNote(note: string | null): Promise<Cart>; clear(): Promise<void>;
}
export interface CheckoutService { begin(cart: Cart, input: CheckoutInput): Promise<CheckoutResult> }
export interface EmailAdapter { // §2 decision 16; mock = local no-op
  subscribe(input: { readonly email: string; readonly list: 'waitlist' | 'first-visit-plan' | 'quiz' }): Promise<{ readonly ok: boolean; readonly delivered: boolean }>;
}
export interface CommerceAdapter {
  readonly id: ProviderId;
  readonly capabilities: { readonly realPayments: boolean; readonly tax: 'none' | 'exact'; readonly codes: 'local' | 'platform' };
  readonly catalog: CatalogReader; readonly cart: CartService; readonly checkout: CheckoutService;
}
```

**Cart maths** (`lib/commerce/pricing.ts`, integer cents, shared by the mock adapter and tests). Codes never touch bundle lines, $0 lines or margin-exception listings (§5.7 rule 4). Cases run [L]: $74.99 → $4.75 shipping, $0.01 to go · $75.00 → free · 2 × $34 + $12 at 10% off → $72.00 qualifying, $9.15 shipping · Buddy Pack + code → code untouched, $60 qualifying, $6.95 shipping · $30 tote (margin exception) at 15% → no discount, $4.75 shipping · tote + $34 tee at 15% → $5.10 off the tee only · a $0 sticker alone → $0.00.

```ts
import type { PricingRules } from '@/lib/catalog/types';
export interface PricedLine { readonly quantity: number; readonly unitCents: number; readonly bundleGroup?: string; readonly promo: boolean; readonly marginException: boolean }
export type CodeRule = Pick<PricingRules['discountCodes'][number], 'percent' | 'excludes'>;
export function priceCart(lines: readonly PricedLine[], opts: {
  readonly bundleDiscountCents: ReadonlyMap<string, number>; // complete bundle groups only
  readonly code: CodeRule | null; readonly freeThresholdCents: number; readonly ship: PricingRules['mockShipping'];
}) {
  const sum = (ls: readonly PricedLine[]) => ls.reduce((a, l) => a + l.quantity * l.unitCents, 0);
  const paid = lines.filter((l) => !l.promo && l.unitCents > 0);
  const groups = new Set(paid.flatMap((l) => (l.bundleGroup ? [l.bundleGroup] : [])));
  const bundleDiscount = [...groups].reduce((a, g) => a + (opts.bundleDiscountCents.get(g) ?? 0), 0);
  const ex = opts.code?.excludes ?? [];
  const eligible = paid.filter((l) => !(l.bundleGroup && ex.includes('bundles')) && !(l.marginException && ex.includes('margin_exception')));
  const codeDiscount = opts.code ? Math.round((sum(eligible) * opts.code.percent) / 100) : 0;
  const qualifying = sum(paid) - bundleDiscount - codeDiscount;
  const units = paid.reduce((a, l) => a + l.quantity, 0);
  const free = units > 0 && qualifying >= opts.freeThresholdCents;
  const shipping = units === 0 || free ? 0 : opts.ship.first.amount + (units - 1) * opts.ship.additional.amount;
  return { merchandise: sum(lines), bundleDiscount, codeDiscount, qualifying, shipping, free,
           remainingForFree: free ? 0 : Math.max(0, opts.freeThresholdCents - qualifying), total: qualifying + shipping };
}
```

**`MockCommerceAdapter`** (`lib/commerce/mock/`, default): `capabilities = { realPayments: false, tax: 'none', codes: 'local' }` · `catalog` reads `catalog/catalog.json` through `lib/catalog/load.ts` (Zod-parsed once: an invalid catalog fails the build, as does a missing `catalog.json` or referenced mockup file) and filters with `isVisible()` · `cart` wraps `stores/cart.ts`, priced by `priceCart()` over `/catalog-index.json` · `checkout.begin()` writes `sf.orders` and returns `mock-order` · `EmailAdapter` stores only `{ list, date }` in `sf.prefs` and returns `{ ok: true, delivered: false }` ("Demo: nothing was sent.").

**Codes** (`lib/commerce/codes.ts`): `firstvisit10` = the 10% entry in `PricingRules.discountCodes` · `buddy15-*` = 15% · `buddy-sheet-*` adds `D11-SH505` as a $0 promo line (free-item codes live here, not in `PricingRules`) · `first-b<n>-*` adds that Firsts sticker. At most one discount code plus any number of sticker codes; the `codes` test asserts every `discountCodes` entry excludes `bundles`, `promo` and `margin_exception`.

**`ShopifyCommerceAdapter`** (`lib/commerce/shopify/`, stub): every method throws `Error('shopify adapter: not built in the prototype')`; its README fixes the Phase-2 contract: Storefront API **2026-10** via `@shopify/hydrogen` **2026.10.x** [V npm]; catalog read at build with the **public** token; cart via `cartCreate`/`cartLinesAdd`, `sf.cart` keeps only the cart id; `checkout.begin()` returns `{ kind: 'redirect', url: cart.checkoutUrl }`; **prices, totals, discounts and tax only from Shopify**. `tests/unit/commerce.contract.test.ts` runs one suite per adapter: mock always; Shopify against `https://mock.shop/api` only with `RUN_NETWORK_TESTS=1`, cart only (mock.shop has no checkout [V Hydrogen package docs]).

**Go-live** (§8.1; decision 3): a Shopify theme (`golive/theme/`) ports these tokens, copy, IA and components; the adapter isn't involved. Optional Phase 2 sets `NEXT_PUBLIC_COMMERCE_PROVIDER=shopify`, `NEXT_PUBLIC_SHOPIFY_STORE_DOMAIN`, `NEXT_PUBLIC_SHOPIFY_STOREFRONT_TOKEN` (public token only) and changes no UI files (`git diff --stat app/ components/` empty). Community stores stay local until a backend and a moderation plan exist (§2 decision 14).

### 7.10 SEO

| Item | Rule |
|---|---|
| Indexing | `robots.ts` (force-static): with `NEXT_PUBLIC_SITE_ENV=production`, allow all but `/cart/ /checkout/ /order/ /your-data/ /brand/`, else `Disallow: /`. Root `metadata.robots` adds `noindex, nofollow` outside production and on §7.4's "no" routes. The zero-env build is never indexable. |
| Metadata | `metadataBase = https://{domain}` (placeholder until bought). Titles `%s · {brand}`; home `{brand}: {descriptor}`. Descriptions from `copy.seo` (≤ 155 chars) or content. One trailing-slash canonical per page; the PDP's drops `?tier/color/size`. |
| OG | Static files from §6/D4: `/og/<handle>.png` (1200×630), `/og/site.png`, `/og/collection-<handle>.png`, `/og/crew-<id>.png`, `/og/send-a-bel.png`; no `opengraph-image.tsx`; `twitter:card = summary_large_image`. |
| JSON-LD | `lib/seo/jsonld.ts` → `<script type="application/ld+json">` with `JSON.stringify(x).replace(/</g, '\\u003c')` [V Next.js JSON-LD guide]. Home `Organization` + `WebSite`; PLP/PDP `BreadcrumbList`. PDP `ProductGroup`: `productGroupID` = listing id; `variesBy` color and size (+ `pattern` for the tier [U]); `hasVariant` = one `Product` per variant (`sku`, `name` "{title}, {Style}, {Colour}, {Size}", `color`, `size`, absolute `image`) with an `Offer` (`price` "34.00", `priceCurrency` USD, `availability` `https://schema.org/MadeToOrder` [U: confirm Google accepts it, else `InStock`], `itemCondition` New, `url`). `shippingDetails`, `hasMerchantReturnPolicy` only once §8's policies are final [U]. **Never `aggregateRating` or `review`.** |
| Sitemap | `sitemap.ts` (force-static) from the route registry: indexable routes only; no `unlock_only` listings, demo pages or per-visitor routes. |
| Tests | Inside `scan:html` (§7.14) over `out/products/*/index.html`: one `ProductGroup`; variant count = visible variants; prices = the catalog's. Every page: one `<title>` (≤ 60 chars), one canonical, one `h1`; outside production, `noindex`. |

### 7.11 Accessibility (WCAG 2.2 AA, §3 rule 11)

Implementation per §3 rule 11 and §4.5. Besides axe on every route and flow 13 (§7.14): `contrast.test.ts` (§4.5) and the class-pair test (§7.7) (1.4.3, 1.4.11) · e2e tabs through PDP and checkout: each focused rect in view and clear of the sticky header (`scroll-padding` for header and add-to-bag; no sticky banners) (2.4.7, 2.4.11) · e2e measures `button, a, input, [role=radio]` ≥ 44×44 px, incl. steppers, swatches, chips, on 6 routes at 390px (2.5.8 needs only 24×24) · keyboard: purchase, quiz, stamp, cheer and e-card flows; arrow keys in radiogroups; dialogs trap focus, Esc closes · no autoplay, loops past 5 s or flashing; the reduced-motion project asserts `document.getAnimations().filter(a => a.effect.getTiming().duration > 1).length === 0` after each flow (2.2.2, 2.3.1, 2.3.3) · not colour alone: swatch ring + check, errors as text + icon, stamps labelled "visit"/"rest" (1.4.1) · CastMember alt "{Name} the {object}, {expression}, {pose}", `Mockup.alt`, sparkles `aria-hidden`; every `svg[role=img]` has a `<title>`, every `img` an `alt` · forms: visible labels, `autocomplete`, error summary + inline errors, no CAPTCHA, re-entry or accounts (3.3.1–3.3.3, 3.3.7, 3.3.8) · `lang="en-US"`, skip link, landmarks, ordered headings, live regions, `aria-current`, Help in one place (3.2.6).

### 7.12 Performance budgets (project targets, mobile Lighthouse)

| Budget | Value | Measured by |
|---|---|---|
| Performance / Accessibility / Best Practices / SEO | ≥ 0.90 / **1.00** / ≥ 0.95 / ≥ 0.90 | `npm run lhci` |
| LCP / CLS / TBT | ≤ 2.5 s / ≤ 0.05 / ≤ 200 ms | LHCI |
| First-load JS per route (gzip) | ≤ 170 KB (`/send-a-bel/` ≤ 200 KB) | `scripts/site/check-bundle.ts` gzip-sums the `/_next/static/**/*.js` each `out/**/index.html` references (not `next build` output) |
| HTML per page (gzip) | ≤ 60 KB (worst case: a PDP with 84 variants of JSON-LD) | same script |
| Images (WebP) | hero ≤ 120 KB at 1440w (§6.8 target ≤ 60 KB); card ≤ 45 KB at 480w | same script, reading the `srcset` files |
| Fonts / third parties | 2 families, ≤ 2 preloads, ≤ 150 KB WOFF2 total / **0** third-party requests | same script; e2e request log |

**`lighthouserc.json`:** `collect.staticDistDir: "./out"`; URLs `/`, `/shop/`, `/collections/the-small-print/`, `/products/the-door-tee/`, `/quiz/`, `/stamp-card/`, `/crew/bel/`, `/cart/`, `/checkout/contact/` (URL form per the LHCI docs [U]). `assertMatrix`: SEO ≥ 0.90 only on the 7 indexable URLs; `/cart/` and `/checkout/contact/` assert only Performance ≥ 0.90, Accessibility = 1, Best Practices ≥ 0.95, LCP ≤ 2.5 s, CLS ≤ 0.05, TBT ≤ 200 ms. `lhci` builds with `NEXT_PUBLIC_SITE_ENV=production` (`is-crawlable` passes); `ci` ends with a zero-env rebuild (§10.2).

### 7.13 Analytics stub (no-op, no cookies)

`lib/analytics.ts` exports `track(event, props?)`, **a no-op in every build** (`console.debug` only with `NEXT_PUBLIC_ANALYTICS_DEBUG=1`). Events `'view_listing' | 'select_tier' | 'add_to_bag' | 'begin_checkout' | 'place_demo_order' | 'quiz_complete' | 'stamp_added' | 'first_claimed' | 'ecard_created' | 'waitlist_join' | 'email_signup'` map to §9's KPIs; props are ids, tiers and step numbers only, never emails, names, free text or dates.
- **Club mode only:** one cookie-free counter at `NEXT_PUBLIC_ANALYTICS_HOST` counts page views plus bare counts (no props) of `quiz_complete`, `ecard_created`, `waitlist_join`, `email_signup`. `stamp_added`, `first_claimed` and quiz answers are never sent. §9's KPI is "Weekly visits to `/stamp-card/` (cookie-free page count)".
- **Tests** (`analytics.test.ts`): no `fetch`, `sendBeacon`, `XMLHttpRequest`, `document.cookie` or `<script` in the module · the HTML scan fails on any external host (`ANALYTICS_HOST` unset in tests) · e2e: `context.cookies()` empty after flow 1. **Go-live:** any other provider only behind a consent design (§8; §2 decision 22).

### 7.14 Testing

**Prerequisite.** `build` needs the outputs of `npm run brand`, `npm run catalog` and `npm run mockups`; §10 orders `ci` so they run first. Scripts: §10.2.

**`vitest.config.ts`:** `resolve.alias { '@': <repo root>, 'server-only': './tests/fixtures/empty.ts' }` · `include ['tests/{unit,integration}/**/*.test.ts']` · `typecheck.include ['tests/types/**/*.test-d.ts']` · `passWithNoTests: true`. `test:unit` (`vitest run --typecheck` [U: confirm in Vitest 5.0.5]) collects only `tests/unit` + `tests/types`, `test:integration` only `tests/integration`; M0 proves both by listing the collected files.

**Vitest** (`tests/unit/`, besides §4's and §5's):

| File | Checks |
|---|---|
| `listing-ready` | each visible listing has, per colour × tier, a mockup on disk with non-empty alt; whole-dollar prices; Private = Quiet − $6 on tees; a guide or TBC; inches only for `verified.value === true` areas, else "Print size: TBC" |
| `pricing`, `shipping` (§5) | plus the §7.9 `priceCart` cases |
| `stamps` | seeded property test (only `clearCard` lowers either number), ISO weeks, backfill limit, nudge |
| `migrations` · `codes` | each store's v0 fixture → current · no stacking; bundle, `promo`, margin-exception exclusion; sticker codes need a paid line |
| `visible` · `delivery` · `quiz` | `isVisible()` across `AS_OF`, gates, flags · business days, `null` → TBC · every result reachable, deterministic ties |
| `moderation` | crew-name regex; 8-member cap; 140/60/24 limits; banned list and blocklist |
| `tokens-usage` · `storage-registry` | §7.7 rules · every persisted key registered |
| `copy-placeholders` | every `{var}` in content has a provider; `{brand}` `{crew_name}` `{month}` `{year}` are print-only providers, `{size_range}` a PDP one |
| `banned-words`, `copy-lint` | per §4.4 (including the `/brand`, legal-surface and `<code>` rules), over `content/*.json` and `catalog/src/*.json` |
| `analytics` · `no-countdown` | §7.13 · no countdown or timer component, no countdown or scarcity text in `content/` (§4.9 #3) |
| `cast-component` | `<CastMember id="bel" expression="happy" pose="idle" />` equals the A.5 fixture `tests/fixtures/bel-happy-idle.svg` |

**ESLint:** `no-restricted-imports` for `next/headers` (`cookies()`, `headers()`) and `lib/commerce/{mock,shopify}`; no `'use server'`; §7.7's token rules.

**Post-build scan** (`scan-built-html.ts`, `out/**/*.html`): banned words on visible text · copy-lint per text node per §4.4, voice from the nearest `data-speaker` · `data-copy-exempt` only in `out/brand/index.html` · every `<code>` matches the §4.4 pattern · no external hosts, `/_next/image`, payment-like inputs, or countdown or scarcity words · the §7.10 checks · `route-manifest.ts`: every §7.4 route, with all static params, exists as `out/<path>/index.html`.

**Playwright flows** (`tests/e2e/`; projects and `webServer`: §10.2; axe in each final state):

1. **Browse to order:** home → shop → *the-door-tee* (Quiet) → Bay → L → add → toast → drawer → 3 checkout steps → `/order/?id=` shows #7 and the Send a Bel CTA
2. **Filters:** `type=tees&size=4XL&under=3500` shows only tees with 4XL; URL round-trip; back restores filters; mobile [Show {n} items] = cards rendered; no `unlock_only` listing
3. **Free shipping:** 2 hero tees: $7.00 to go, $6.95 shipping; + `D11-SH505` → free
4. **Buddy Pack:** builder → 2 lines → −$8 → remove a half → discount and notice change
5. **Codes:** `firstvisit10` works; a second code refused; bundle lines untouched
6. **Firsts:** claim First Visit → code → $0 sticker line; a bag of only $0 lines can't check out
7. **Size and tier:** add without a size → error and focus; Private → `label` mockup, $28; tier, colour, size round-trip via the URL and survive reload
8. **Stamp card:** visit + rest (#15) → reload → `page.clock` +21 days → #16, totals unchanged → Clear needs a confirm
9. **Cheer wall:** "Sample post" labels; banned word refused; preset reply; Report hides the post
10. **Crews:** invalid name refused; invite in a new context → join → combined total
11. **Send a Bel:** create → copy link → a new context renders the same text → PNG non-empty, 1200×630
12. **Waitlist:** `?preview=waitlist` → no add-to-bag on any PDP; `/cart/` shows the waitlist panel
13. **Keyboard only:** flow 1 without a mouse
14. **Storage blocked:** `localStorage` throws (init script) → pages render, cart works in memory, StorageNotice
15. **Your data:** Download has every registry key present; Clear leaves no `sf.*` key
16. **Persona checks:** no nav label matches `/\b(men|women)('?s)?\b/i`; every PDP shows its size range and "Same price in every size"; Quiet default where offered
17. **No-JS:** Home and PDP with `javaScriptEnabled: false` show title, price, description, nav (PDP: fit and the size table in `<details>`)
18. **404:** `/nope/` renders Ollie and #8

**Axe sweep** (`tests/a11y/all-routes.spec.ts`): `AxeBuilder.withTags(['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa'])` on **every manifest route** plus: drawer, size guide, mobile menu and filter sheet open, a checkout step with errors, the quiz result. **Gate: 0 violations.**

**Screenshot review** (§3 rule 15): `npm run screens` (`artifacts/screens/<route>@<w>.png` at 390, 768, 1440); **open the PNGs** and check spacing, type scale (Caprasimo ≥ 28px), colour pairs, the ground line, clipped text, the mobile sticky bar, empty states, the DemoBar; log fixes in `docs/progress.md`. `toHaveScreenshot()` is optional (chromium only).

### 7.15 Deploy options and caveats

D5 is done without hosting: `out/` plus green tests. Preview hosts, terms unverified (Appendix B U27 [U]): **Cloudflare Pages** (recommended: build `npm run build`, output `out`, reads `out/_headers`; Access can lock previews) · **Netlify** (same) · **Vercel** (Hobby is non-commercial; a store needs Pro ≈ $20/user/mo) · **GitHub Pages** (design previews only; a project page needs `basePath`; no `_headers`).

**Headers.** `npm run build` = `next build && tsx scripts/site/write-headers.ts`, which writes `out/_headers` (`/*`) from `lib/site.ts`; there is no `public/_headers`:
- `X-Robots-Tag: noindex, nofollow`, only when `NEXT_PUBLIC_SITE_ENV !== "production"`
- `Referrer-Policy: strict-origin-when-cross-origin` · `Permissions-Policy: camera=(), microphone=(), geolocation=()`
- `Content-Security-Policy: default-src 'self'; img-src 'self' data: blob:; font-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; connect-src 'self'; frame-ancestors 'none'`, with `NEXT_PUBLIC_ANALYTICS_HOST` added to `connect-src` only in club mode with the host set. Next's inline bootstrap scripts need `'unsafe-inline'` (or per-build hashes) on a static host [U: confirm via CSP violations in Playwright].

Prototype previews (non-club builds) keep the DemoBar and noindex and never sit on `{domain}`. The public `club.{domain}` site is always the club-mode production build (§8.1).

---

## 8. Going live: POD setup, operations & legal

This section turns D1–D5 into a real store and builds D6, the go-live kit. **Not legal or tax advice.** The build session prepares files, scripts and drafts offline; the founder opens accounts, pays, signs and publishes. §3 rule 6 throughout: dry-run by default, drafts only, code never confirms an order.

D6 paths: §10.1 (`golive/`, `exports/`, `content/{cs-macros,emails,social}.json`). Tags: **[C]** build session (offline, no accounts) · **[F]** founder (accounts, money, identity, legal sign-off) · **[C→F]** C prepares, F executes.

### 8.1 Recommended path

**Default: Shopify (Basic) + the official Printful app, with a Shopify theme as the storefront** (§2 decision 3): Shopify owns checkout, PCI, tax, fraud screening, order emails and abandoned-checkout recovery; Printful imports paid orders, prints, ships and returns tracking. Least operations for one founder.

| Cost line | Amount | Tag |
|---|---|---|
| Shopify Basic · Payments (US cards) · third-party gateway | $39/mo monthly or $29/mo yearly · 2.9% + $0.30 · +2% on Basic (only without Payments) | [S] |
| Shopify Tax | Free for the first $100,000 of US sales per calendar year, then 0.35% per order (max $0.99); stores created after 13 May 2026 may get the $100,000 once (lifetime) | [S]; lifetime [U] |
| Printful Free · Growth (optional, §5.1 rule 4) | $0 · $24.99/mo, 14-day trial, free for a year past $12K yearly sales | [V] |
| Printful US holiday surcharge | $0.40 per US order, 15 Oct 2026 – 17 Jan 2027 (launch week; absorbed) | [S] |
| Domain · Shopify Email (§8.2 step 18) | ≈ $10–25/yr · free allowance, then per send | [U] |

**Printful** for every year-one product. **No Printify account and no Printify exporter in year one.** The 24 oz protein shaker (Printify, ≈ $13.98 [T]) is deferred: separate parcel, and it leans toward protein/diet culture (§5.1). Revisit only if the founder approves it.

Not a custom Stripe + Printful build: you'd own tax, fraud holds, an order database, webhooks, emails and returns (3–6+ weeks). The adapter stays a stub.

**Launch architecture** (default; override in one line):

| Surface | December 2026 (waitlist, no orders) | From Tue 5 Jan 2027 |
|---|---|---|
| `{domain}` + `www` | Shopify **password page = waitlist** (themed; native signup [U on the chosen theme]) | Shopify theme: shop, cart, checkout, policies |
| `club.{domain}` | `npm run build:club` with `features.waitlist = "on"` (club mode, §7.3): quiz, Send a Bel, First Visit Plan, stamp card, Club Rules; buy surfaces say "Join the waitlist" | Same build, `waitlist` `"off"`: buy buttons → `https://{domain}/products/<handle>`; live codes in `<code>`; community data in `localStorage` (§2 decision 13) |
| Club email capture | Form post to `https://{domain}/contact#contact_form` (`form_type=customer`, `contact[email]`, `contact[tags]` e.g. `waitlist,quiz-bel`): a navigation, not a fetch, so no third-party script loads first; captcha possible [U]. **Fallback:** the ESP's public subscribe endpoint behind an explicit consent checkbox | Same |

Non-club previews keep the DemoBar and noindex, never on `{domain}` (§7.15).

**Later, optional: headless** via `ShopifyCommerceAdapter` (§7.9, contract tests), only after day 90 and if a theme limit blocks a measured §9.8 KPI; theme apps (reviews, popups) then don't render, so consent and analytics need manual wiring. Products, orders and sync stay in Shopify.

### 8.2 Step-by-step setup checklist

In order. Dates per the §0 timeline (Printful account by 17 Nov for the round-1 order; Shopify by 27 Nov; DNS by Tue 1 Dec). `golive/README.md` is this table as checkboxes.

| # | Step | Who | Done when |
|---|---|---|---|
| 1 | **Basics** (§8.6 rows 2–3): entity, EIN, business bank, `hello@{domain}`, password manager | [F] | Bank open; 2FA on Shopify, Printful, registrar, email, social |
| 2 | **Domain** (§4.1 order); `overrides.domain` in `brand.config.json` if not `{wordmark}.com`; `npm run brand && npm run build` | [F] · [C] | `metadataBase` and policies show it |
| 3 | **Shopify**: Basic; name from `brand.config.json`; **USD**; **US only** (§2 decision 4); tax-exclusive; password page **on**. **DNS by Tue 1 Dec:** apex + `www` → Shopify; `club` → the club-mode waitlist build (static host, §7.15) | [F] | US, USD, password on; `club.{domain}` serves it over HTTPS |
| 4 | **Shopify Payments** on; Shop Pay on; descriptor = brand name (limit [U]); one test-mode order | [F] | No live charge |
| 5 | **Printful app**: connect; billing on file; **resale certificate** (§8.6 row 3); **manual approval** for 14 days (setting [U]) | [F] | A test import holds |
| 6 | **Printful branding.** D13 default labels (`D13.none.<productKey>.label_inside.<LIGHT\|DARK>.ANY`) on `cc1717`, `bc3001` via `inside_label_type` [T]; none on fleece [T]. **No pack-ins** (§5.1 rule 6). Slip: logo (`public/brand/`) + "(psst. you showed up. that counts.)" [U]. **Return address:** Printful's, a PO box or virtual mailbox, **never home** (it prints on labels) [U] | [C→F] | §8.4 label check; slip shows logo and message |
| 7 | **Print files**: `npm run art:print && npm run validate:print && npm run export:printful` (only `pass` + `specVerified` + not `provisional`, §6.6); upload via §8.3 or the file library | [C] · [F] | 0 blocked files for the 16 launch listings |
| 8 | **`tierMode` test.** `D01-CC17` with **Style** (Quiet/Loud/Private) as Option1, pushed to Shopify. If one product carries per-Style files and placements, keep `"option"`; else all 17 three-tier listings go `"sibling"` (§5.4); re-run `export:printful` + `export:shopify`; log in `docs/decisions.md` | [F] · [C] | Each Style shows the right print in Printful mockups |
| 9 | **Other 15 launch products** per `exports/printful-sync-checklist.md` (blank, variants, file per placement, technique, threads, copy, tags); the dashboard push creates them in Shopify [U API scope], **unpublished** | [F] · [C] | All Shopify drafts |
| 10 | **SKUs**: Shopify variant SKU = our SKU (`D01-Q-CC17-IVR-M`); `npm run golive:printful -- --live`, fix each `sku-mismatch`. If Printful's `external_id` proves Shopify-owned [U]: our SKU in Shopify `Variant SKU` + Printful `sku`, `external_id` in `golive/state/printful-map.json`, logged | [C→F] | 0 `sku-mismatch`, 0 `missing-variant` |
| 11 | **Prices** = `catalog.json` (whole dollars, same in every size, Private −$6 on tees); no compare-at; cost per item = live base + label | [C→F] | 0 `price-mismatch`; no floor breach in `exports/catalog-margins.csv` without an approved exception |
| 12 | **Discounts** (§5.7 rule 4): none stack; never on bundles, $0 lines or margin-exception listings; once per customer. `FIRSTVISIT10` (10%) · `BUDDY15` (15%) · `BUDDYSHEET` (free `D11-SH505` with any order) · `FIRSTB1`–`FIRSTB6` (that Firsts sticker free with any order; honour system) · Buddy Pack = **automatic** $8 off tees A + B of one design [U: native, else the free Shopify Bundles app]. Case-insensitive [U] | [C→F] | No combining; `FIRSTVISIT10` skips Buddy Packs and margin-exception listings |
| 13 | **Shipping. Default A:** Printful's calculated rates (carrier-calculated on Basic [U]) + free at ≥ $75.00 merchandise subtotal after discounts. **Fallback B (founder approves):** flat $5.95 below $75, free at $75; model it in `exports/catalog-margins.csv` first. `catalog/src/pricing-rules.json` gets the live rule; the prototype's $4.75 + $2.20 stays the test fixture | [F] | $68 (two hero tees) charged; $80 − 10% = $72 charged; $76 free |
| 14 | **Shopify Tax**: home-state registration (§8.6 row 3) added in Shopify; categories (apparel vs accessories; states differ [U]) | [F] | Home-state checkout shows tax |
| 15 | **Policies**: `npm run golive:policies` → paste `exports/policies/*.md` into Settings → Policies (refund, privacy, terms, shipping, contact) after lawyer review (§0) | [C] · [F] | Footer links work; "Not legal advice" banner off only after review |
| 16 | **Theme**: free OS 2.0 (Horizon or Dawn [U]) + the `golive/theme/` kit per its `README.md` (Edit code steps; §7.5 PDP blocks → sections): `assets/brand-tokens.css` (`:root` vars from `npm run brand`, committed), `assets/brand-fonts.css` (`@font-face`, the two WOFF2 files from `public/fonts/`), `snippets/{made-to-order,free-shipping-bar,size-range,tier-blurbs}.liquid` (copy from `content/*.json`; `{brand}` → `{{ shop.name }}`; no brand literal). §4.5 contrast pairs. Style = Option1, **Quiet** first (§2 decision 8). PDP: tier blurbs, size guide, made-to-order note (§4.4 #10), size range, "Same price in every size"; cart free-shipping bar (§4.4 #13); launch-line announcement; nav by vibe and type, never gender, + "The club". **No countdown, scarcity, fake-review or spin-to-win apps**; ≤ 3 apps, Lighthouse after each. M9: `shopify theme check` offline if `@shopify/cli` installs, else untested in D7 | [C→F] | Kit installed; tier blurbs, size range, made-to-order note on the D01 PDP; axe 0 on home, PDP, cart, checkout; mobile LCP/INP per §7.12 |
| 17 | **Order notifications** from `content/emails.json` (§9.6): confirmation, shipping, delivery, delay | [C→F] | Read against §4.4 |
| 18 | **Email**: Shopify Email + automations [U: names, allowance]; §9.6 flows only, **no browse-triggered automation**; footer postal address (PO box or virtual mailbox) + one-click unsubscribe | [F] | Welcome arrives; unsubscribe works |
| 19 | **Consent, analytics**: Shopify's privacy banner **on**; honour GPC. Shopify analytics plus, on `club.{domain}` only, one cookie-free counter at `NEXT_PUBLIC_ANALYTICS_HOST` [U provider]: page views and bare counts (no props) of `quiz_complete`, `ecard_created`, `waitlist_join`, `email_signup` (§7.13); never `stamp_added`, `first_claimed` or quiz answers; `track()` stays a no-op. Ad pixels only for the §9.9 paid test, behind consent | [F] | No third-party cookies pre-consent |
| 20 | **Test orders**: 2–3 real ones (paid → Printful draft → approve → tracking → delivered), refunded; check tax, billing, label, slip | [F] | Each passes §8.4 checks 3 and 9 |
| 21 | **Search**: Search Console, sitemap, Rich Results Test on a PDP; theme JSON-LD; never fake ratings | [F] | Sitemap accepted |
| 22 | **Launch switch** (§9.3): Mon 4 Jan evening, redeploy the club-mode build with `waitlist` `"off"`, launch products active behind the password; Tue 5 Jan 08:30 ET, password off. DNS unchanged | [F] | §9.3 checks pass |

### 8.3 Printful sync script spec (D6)

**Purpose.** Reconcile Printful (and so Shopify) with `catalog/catalog.json` and `print-files/manifest.json`: dry-run default, idempotent, prints a diff, never deletes, **never confirms an order**.

**Invocation** (scripts: §10.2):

| Command | Network | Writes · use |
|---|---|---|
| `npm run export:printful` (`--plan`) | none | `exports/printful-sync-plan.json` + `exports/printful-sync-checklist.md` (dashboard click-through); exit 1 if a needed file isn't `pass` + `specVerified` + not `provisional` |
| `npm run golive:printful` | none | Nothing; diff against `golive/state/printful-map.json` (last applied) |
| `… -- --live` | **GET only** (`PRINTFUL_TOKEN`) | `catalog/live/printful/*.json` snapshots (`checkedAt`); diff against the **live** store (every check) |
| `… -- --live --apply` | GET + POST/PUT | Files, sync products, the map. Founder only, own terminal, after reading the diff; typed `apply <n> changes to store <id>` |
| `… --live --apply --draft-order <SKU,…> --to founder` | + `POST /v2/orders` | One **draft** order (real sample costs); founder confirms or deletes it |
| `… --live --mockups <listingId>` | + mockup tasks | Raw results in `catalog/live/printful/mockups/`; `MOCKUP_PROVIDER=printful npm run mockups` then writes `public/mockups/` offline (origin `printful-mockup-api`) |
| `… --live --rates` | `POST /v2/shipping-rates` | `catalog/live/printful/shipping-rates.json`; fills `catalog/src/transit.json` (tag V, `checkedAt`) for `{transit_window}` |

**The build session never runs `--apply`** or sets a real token; it tests against a fake server.

**Inputs → desired state.** Every listing with `launch = true` or a released drop, mapped per §5.10 "Printful mapping": one sync product (`name` = title, external id = listing id; per tier in sibling mode); enabled variants (`catalogVariantId` from the live pull, `sku` = our SKU); `retail_price` = catalog price; files per variant from the manifest (`printFileIds`); techniques (`dtg`, `dtfilm`, `embroidery`, …); options `thread_colors` (`meta.threads`), `inside_label_type` [T].

**Endpoints** (verify each against the live OpenAPI at developers.printful.com before the first `--live` run; record the doc date in `golive/README.md`): auth `Authorization: Bearer $PRINTFUL_TOKEN` (+ `X-PF-Store-Id: $PRINTFUL_STORE_ID` for account-level tokens) [T] · catalog: §5.1 live sources [T] · `POST /v2/files` with `{ url }`, poll `GET /v2/files/{id}` (v1 fallback `POST /files`) [U] · sync products **v1 only**: `GET`/`POST /store/products`, `GET`/`PUT /store/products/{id}`, `PUT /store/variants/{id}` [T]; on a Shopify store (API creation may be Manual/API-store only) products come from the dashboard push and the script **matches on `sku` and updates** files, options, `retail_price` [U] · `POST /v2/mockup-tasks`, poll `GET /v2/mockup-tasks?id=…` [T] · `POST /v2/orders` (a draft; not billed) [T] · `POST /v2/shipping-rates` [T; token need U].

**File hosting.** PNGs are local, git-ignored. If files upload only by URL [U], `--file-base-url <https://…>` points at a temporary host (files named by SHA-256, deleted after the sync); otherwise the founder uploads in the dashboard and pastes the ids into the map.

**Safety rules** (each a unit test in `tests/unit/golive-printful-*.test.ts`, run in `npm run ci` against an in-memory fake Printful; no network in CI):
1. Without `--live`, zero `fetch` calls (the test injects a throwing `fetch`).
2. `--live` without `--apply`: GET only, plus `POST /v2/shipping-rates` with `--rates`.
3. **Order denylist** (`golive/lib/printful.ts`) refuses `/orders/\d+/confirm`, `/orders/{id}/confirmation`, any `confirm=` query or `"confirm": true|1` body, any `PATCH` changing order status; each throws before sending.
4. **Never deletes.** Live items missing from the catalog are reported as `orphan` (archive by hand).
5. **Idempotent.** Each write records `contentHash = sha256(canonical JSON of the desired object + file shas)` in the map (committed; ids and hashes only, no secrets or timestamps; only `--apply` writes it). A second `--apply` with no input change makes **0 writes**.
6. **Secrets.** Token only from `process.env` (or a git-ignored `.env.local`); `.env.example` has empty `PRINTFUL_TOKEN=` and `PRINTFUL_STORE_ID=`; logs redact `Authorization`. `npm run ci` fails on any per-line hit, over `git ls-files` excluding `*.md`, of `` /^\s*(export\s+)?PRINTFUL_TOKEN=[^\s'"`#]+/m `` or `/Bearer [A-Za-z0-9_-]{20,}/`; test tokens are under 20 characters or built at runtime. Real token: narrowest scopes, an expiry [U: scope names].
7. **Rate limits:** token bucket at 120 requests/min [T], tuned by `X-Ratelimit-*` [T]; on 429 honour `Retry-After`. Mockup tasks ≤ 2/min (estimates 2–10/min [T]). Serial writes. Retries: backoff with jitter (max 5, cap 60 s), only on GETs and writes with an idempotency key or pre-checked hash.

**Diff output** (stdout, stable order; `--json` for machines). Exit 0 when nothing blocks; 2 while `sku-mismatch`, `price-mismatch` or `blocked-file` remain.

```text
printful-sync  store=<id>  mode=live/read-only  catalog=<sha8>  manifest=<sha8>
+ create   product  D02-BC30  "The Little Sticker tee"  81 variants
~ update   variant  D01-Q-CC17-IVR-M   retail_price 32.00 -> 34.00
~ update   file     D01.loud.cc1717.back.DARK.PEP   sha 3f2a91c0 -> 9c1d44e7
! mismatch variant  D04-L-CC17-BAY-XL  sku "6385F4A1B_1717" (expected D04-L-CC17-BAY-XL)
- orphan   variant  D01-L-CC17-WTM-S   not in catalog; archive by hand (never deleted)
= 412 unchanged · 3 to write · 1 blocking · 1 orphan
```

### 8.4 Samples & QA

**Rule:** no listing goes live without a physical sample that passed the checklist (§5.5). Printful sample orders [V]: 20% off on Free (25% on Growth), **one discounted order a month, ≤ 3 items**, ≤ 3 addresses, no other discounts: the 3 priciest pieces go there, the rest in a normal order to the founder (or a founder-confirmed `--draft-order`).

**`golive/sample-rounds.json`**: `{ "rounds": [{ "round": 1, "orderBy": "2026-11-23", "pieces": [{ "sku": "D01-L-CC17-IVR-M", "why": "…" }] }] }`; garments in size M, one-size items `OS`, Firsts `D12-N-STK3-B1-OS` … `B6-OS`. `npm run golive:samples` (M5) joins it with `catalog.json` for costs → `golive/sample-plan.md` + `exports/sample-plan.csv`.

**Round 1: order Mon 23 Nov 2026 (latest Sat 28 Nov); 14 pieces + stickers:**

| Blank | Pieces | Proves |
|---|---|---|
| CC 1717 ×6 | D01 Loud Ivory · D01 **Private** Ivory · D04 Loud Bay (GARMENT-FILL) · D03 Loud Pepper (DARK) · D08A Loud Butter · D08B **Quiet right chest** Chalky Mint | LIGHT, GARMENT-FILL, DARK; label; buddy pair; right chest |
| B+C 3001 ×1 | D02 Loud Vintage White (default label) | Mixed fonts at minimum size; label on blank 2 |
| Gildan 18000 ×2 | D06 Loud Sand · D10 embroidered Navy (3 threads) | DTG on fleece; embroidery gaps |
| Gildan 18500 ×2 | D09 Loud Navy (crest) · D01 Quiet Sand | 114 px arc text; hoodie chest |
| Yupoong 6245CM ×2 | D10 Stone (2 threads) · D10 Navy (3 threads) | Hat embroidery both ways |
| Bottle #788 ×1 | D07 | Wrap seam, method, lid ("a little cheap" [T]) |
| Stickers | D11 sheet · 6 × D12 Firsts · 4 singles | Cut lines; paper text minimums |

**Round-1 budget** [U; recompute live]: snapshot base ≈ $285 (products + labels), ≈ $40–60 shipping (stickers may ship separately), $2.95–6.50 embroidery digitisation per design and placement [V/T]: **≈ $300–450** incl. shipping.

**Round 2 (by ~Tue 8 Dec; holiday cutoffs may slow it [S]):** round-1 fixes · drop 1 (`D06-CC15` Orchid GARMENT-FILL, `D14-CC17`, `D15-Y150` beanie, `D15-M758` joggers, `D16-K882` socks) · drop 2 (`D17-CC17`, D18 A + B tee and crew) · AOP gate: D21 leggings in Locker Canvas and Locker Sage, size M + one plus size (#334). ≈ $300–400 [U].
**Round 3 (by ~Mon 25 Jan 2027, for 2 Mar):** D19, D20, D21 bra, shorts and socks, D12 patch. ≈ $100–200 [U]. Rule: each drop's samples ≥ 4 weeks ahead.

**QA checklist** (`golive/qa-checklist.md`, one row per sample; pass or fix, and a fix means re-sample):
1. **Three-metre test:** each Loud reads as vintage merch, not a sticker shop. Show Dev-type testers D04 on Bay and D09 on Navy (§2 decision 17).
2. **Smallest type:** open counters on the smallest Caprasimo line (D01, 225 px) and the smallest Atkinson lines (D02 150 px; D09 ring 114 px after the 0.95 seal scale).
3. **Label:** whisper readable; clear of Printful's auto-filled size, fibre, origin text [T]; no ghosting.
4. **Embroidery:** brows and eyes separate, handle window open, no crown puckering.
5. **GARMENT-FILL on Bay:** Gus reads as Gus, not a hole.
6. **DARK underbase:** halo and oat areas soft, not plasticky; no white edges.
7. **Wash test:** 3 cold washes inside out; no cracking, fading or shrink (chest width before/after).
8. **Buddy photo:** A left, B right, laid flat; the bars line up as one dumbbell.
9. **Colour truth:** check against the mockup hex; log the real `color_code` for the validator.
10. **Sticker cuts:** die lines follow the halo; no torn thin protrusions.
11. **Squat test (leggings, gate `squat_test`):** a consenting adult volunteer (the founder or a friend) signs `golive/legal/photo-release.md` with a "QA only, never published" clause and may take the photos. Daylight, deep squat, photos from 1 m behind and the side, each colour, both cuts. Pass = no skin or underwear visible, no white underside at stretch. Photos stay in a local git-ignored folder, deleted once logged; only pass/fail and the date go into `catalog/src/listings.json` `gate.status`. Locker Canvas fails → Locker Sage only; both fail → no leggings.

**Photo shot list** (founder; never people; home or a booked empty space; `photos/<handle>/<option>-<tier>-<view>.jpg`, git-ignored; generated mockups stay as fallbacks). `Mockup` views: `flat_front`, `flat_back` per listing × launch colour (laid flat on the oat/canvas backdrop, daylight, 4:5, ≥ 2400 × 3000 px, no filters) · `detail` (print close-up, ruler) · `label` (neck open) · `pair` (D08 A left, B right, bars aligned) · object scenes (tee folded on a bench, bottle and sticker sheet in a gym bag, hat on a locker hook) · one grey-card frame per garment colour.

### 8.5 Operations

**Lead times.** Production "most products in 2–5 business days" [V]; AOP synthetics 3–7 days at partner facilities [V]; transit from `--rates` (§8.3), else TBC. Surfaces render `{production_window}` and `{transit_window}` from data (§4.4 #8); split parcels are possible [U], so the "separate boxes" sentence always shows.

**FTC Mail, Internet, or Telephone Order Merchandise Rule** (16 CFR 435) [S]: a reasonable basis to ship within the stated time (30 days if none is stated); else an **option notice** before the deadline (accept the delay or cancel for a prompt refund). SOP: not shipped by `production max + 2 business days` → M3 that day.

**Returns and exchanges** (default `golive/policies/returns.md`; founder may change it):

| Case | Customer gets | Window | Who pays | Printful side |
|---|---|---|---|---|
| Misprint, defect, damage | Free remake or full refund; **nothing sent back** | 30 days from delivery, with a photo | Us; recovered from Printful | Claim **the same day** with the photo (Printful's window: 30 days from delivery [V]) |
| Wrong size (garments) | **One swap per order:** the new size; keep or pass on the first | 30 days from delivery | Customer pays the standard first-item shipping rate (`{swap_fee}`, from `catalog/src/pricing-rules.json`: Printful's live rate under default A, $5.95 under fallback B; $4.75 only in the prototype); we pay the new base | Not covered [S]; a new order. Revisit if swaps pass 5% of garment units |
| Change of mind | No return (made to order); said on PDP, cart and policy | — | — | Not covered [S] |
| Bad address | One reship once fixed | — | Customer pays reship shipping | Printful charges shipping [V]; unclaimed returns donated after 30 days [V] |
| Lost in transit | Remake after a carrier trace | 30 days | Us, unless Printful accepts the claim [U] | Claim process [U] |
| Cancel | Full refund before production; then as change of mind | Before production | — | Editable until production [U] |

**Customer-service macros** (`content/cs-macros.json`, `surface: "cs-macro"`, `speaker: null`; brand voice; banned-words and copy-lint; signed with a first name):

| # | Use | Text |
|---|---|---|
| M1 | In production | Hi {name}. Your order {order} is being made right now, just for you. Most pieces ship in {production_window}, and we'll email tracking the minute it leaves. Thanks for waiting with us. |
| M2 | Shipped | Good news: {order} is on its way. Track it here: {tracking_url}. If anything arrives looking wrong, send us a photo and we'll fix it. |
| M3 | Delay (FTC option notice) | Heads up: your {item} is taking a little longer than we said. New estimate: {date}. Sorry about that. If you'd rather not wait, reply "cancel" and we'll refund you in full, no questions. |
| M4 | Misprint or damage | That's not how it should look, and we're sorry. Could you send a photo of the print (and the label, if you can)? Then we'll make you a new one for free. No need to send anything back. |
| M5 | Remake confirmed | Your new {item} is being made now and usually ships in {production_window}. Keep or pass on the first one, whatever's easiest. |
| M6 | Size swap | Sizing is tricky, and that's not on you. We can send {item} in {size} for {swap_fee} shipping. Keep the first one or pass it to a friend. Want us to set that up? |
| M7 | Change of mind | Thanks for telling us. Each piece is made just for you, so we can't take back items that arrived okay in the right size. If it's a fit problem, we can swap the size: {returns_url} |
| M8 | Split shipment | Your order is coming in {n} boxes, because different pieces are made in different studios. Nothing's missing. Tracking for each box: {tracking_urls} |
| M9 | Address change | Thanks. If it hasn't started printing yet, we can update the address. We'll confirm within one business day. |
| M10 | Unsubscribe, data request | Done. You're unsubscribed. We'll still be cheering, just quietly. (Data requests: we'll confirm within {days} days.) |

**Order-issue SOP** (founder, 10 min a day; support replies within 1 business day; same day unless noted): new order in the first 14 days → Shopify fraud analysis; high risk → cancel and refund before approving in Printful · Printful "on hold"/"failed" → fix file, address (M9) or payment · not shipped by production max + 2 business days → M3, logged · misprint photo → M4 → Printful claim → M5 once approved · ≥ 2 misprints from one file → pause the variant, re-sample, fix the file (§6) within 48 h · "not received" → carrier trace; remake after 5 business days · Mondays → Printful "issues" list, `golive/dashboard/weekly.csv`.

**Holiday cutoffs.** No physical orders in December 2026 (Printful's 2025 US apparel cutoffs: 11 Dec standard, 16 Dec express [S]). By 15 Oct 2027, copy Printful's 2027 table into `catalog/src/cutoffs.json` (each date `Sourced`); the site renders "Order by {date} for delivery by 24 December (standard)" and drops it after the date. Black Friday 2027: a free Collect the Crew sheet only (§5.7 rule 5).

### 8.6 Legal & compliance checklist (not legal advice)

The founder signs off each row; the build session drafts copy and adds the named tests. `golive/policies/` drafts use `{brand}` `{domain}` `{production_window}`. **Before launch** rows block the launch switch (§8.2 step 22).

| # | Area | Do this | Owner · When | Tag |
|---|---|---|---|---|
| 1 | **Trademark** | Knock-out + attorney clearance for KETTLEKIN (§4.1) **before paid ads or bulk samples**. File **class 25** first, then 16, 21, 35; 18, 9, 41, 28 later. USPTO since 18 Jan 2025: **$350 per class**, +$200/class for free-form goods text, +$100 for insufficient information (use ID Manual entries); intent-to-use needs a statement of use (fee [U]). No slogan filings in v1; never character names as standalone marks | F · search by 17 Nov; file before launch | [S] fees |
| 2 | **Entity** | Single-member LLC (or sole proprietorship) in the home state; EIN; business bank; separate money | F · start by 17 Nov (§0) | [U] fees |
| 3 | **Sales tax** | Home-state registration before the first sale; Shopify Tax watches other states' nexus thresholds (vary [U]); file on schedule. Resale certificate to Printful (untaxed base costs [U]) | F · before launch | [U] |
| 4 | **FTC Mail/Internet Order Rule** | §8.5: windows from data, option notice M3, prompt refunds | F+C · before launch | [S] |
| 5 | **FTC Endorsement Guides** (16 CFR 255, rev. June 2023) | Gifted or paid creators disclose **in each post**, up front ("#ad" or "gifted by {brand}", not buried); a code isn't a disclosure. The brand can be liable: written instructions (`golive/legal/creator-agreement.md`), post checks | F · from the first gift | [S] |
| 6 | **FTC Consumer Reviews and Testimonials Rule** (16 CFR 465, from 21 Oct 2024) | No fake, bought, sentiment-conditioned, undisclosed-insider or suppressed reviews; no bought followers; penalties up to $51,744 per violation (2024). Reviews only via the post-delivery request (§4.4 #17); no demo reviews on the live store | F · always | [S] |
| 7 | **CAN-SPAM + consent** | No pre-checked boxes; honest subjects; postal address in marketing emails; one-click unsubscribe, honoured promptly (limit 10 business days [U]); no promotions in transactional emails; double opt-in outside the US. **No SMS in v1** (TCPA) | F · before the first email | [U] |
| 8 | **Privacy** | `golive/policies/privacy.md` names what Shopify, Printful, the ESP and the counter receive, and why. Honour GPC; "Do not sell or share" **if** any ad pixel runs. CCPA probably doesn't apply yet [U]; write as if it did. `club.{domain}` keeps community data in the browser and says so (§7 `/your-data/`) | C draft · F review · before launch | [U] |
| 9 | **Minimum age 13** | 13+ (`minimumAge`); no birthdates; age in the terms and Club Rules; delete data you learn belongs to a child under 13 (COPPA) | C+F · before launch | [U] |
| 10 | **GDPR / UK GDPR, EU GPSR** | US only at launch. **Before** EU/UK sales: cookie opt-in, GDPR notices, EU VAT OSS / UK VAT, **GPSR** (since 13 Dec 2024: manufacturer details, EU Responsible Person, safety info, `compliance.euResponsiblePerson`) [U partner support] | F · if expanding | [U] |
| 11 | **CPSIA** | "Children's product" = designed or intended primarily for children **12 or younger** (sizing, marketing are key) [S]. Ours are general-use, 13+: **no youth or toddler sizes or blanks**, no kid-directed marketing, the cast never called toys; no plush (class 28). `tests/unit/catalog-audience.test.ts` fails if a size matches `^(Y\|[2-5]T)` or a title, tag or collection handle matches `/\b(kids?\|toddler\|youth\|baby)\b/i` (so BPK displays "Soft Pink") | C test · always | [S] definition |
| 12 | **Accessibility** | Live theme meets WCAG 2.2 AA (axe 0 on key pages, keyboard checkout, alt text); footer statement with a contact route | C→F · before launch | — |
| 13 | **Licences and IP** | §3 rule 8 (OFL fonts, `licenses/fonts.json`; no stock photos; original art); IP assignment from any outside designer (§6.9); copyright in the final character model sheets (fee [U]); Slogan Lab IP-licence checkbox (§4.8 #14) | F | [U] fees |
| 14 | **Claims** | **No medical or mental-health outcome claims** (never "reduces anxiety", treats or improves anything); "For your brain" is about reasons, not outcomes. UPF, recycled, organic and certification claims (GRS, OEKO-TEX) need a [V] source (partner product page or certificate) in `Sourced.source`; with only [T], omit the claim (§5.8 rule 4). **Never "Made in USA"**; no green claims beyond Printful's documentation. Crisis or self-harm mentions: a human replies (never a character) with local emergency help (US: call or text 988) | C review · always | [U] 988 |
| 15 | **Consent-first photos, UGC** | The §9.2 rule; signed `golive/legal/photo-release.md` for anyone photographed for the brand; written permission to repost UGC (`golive/legal/ugc-release.md`; screenshot in git-ignored `docs/ugc-permissions/`) | F · always | — |
| 16 | **Promotions and votes** | The Send a Bel e-card has no cash value (not a gift card). Votes carry no prizes (a prize = a sweepstakes needing official rules [U]). Black Friday: a gift with purchase, not a contest | F | [U] |
| 17 | **Terms** | `golive/policies/terms.md`: made-to-order sales, the §8.5 returns table, community conduct (preset replies only, no strangers filmed, 13+), the licence for user content and Slogan Lab | C draft · F review | — |

---

## 9. Launch & growth plan

The founder runs this. The build session writes `content/{emails,social,cs-macros}.json` (social: `surface: "social"`; all under banned-words and copy-lint), `golive/README.md` and the dashboard template. *(new)* lines pass §4.4 but need founder approval (like §3 rule 10).

### 9.1 Positioning recap & launch narrative

Positioning: §4.2 (The Glare is never drawn or named in ads). Persona messages: §4.3.

**Launch line:** **"New year, no pressure. No resolutions needed."** Use it exactly: it passes the banned list only through the `no resolutions needed` allow rule (§4.4). Never "new year, new you", resolution framing, "fresh start, new body" or any January guilt.

| Act | Dates | Message | On the site |
|---|---|---|---|
| 1. The crew gets ready | 1 Dec – 4 Jan | "We open on Tuesday 5 January. One email when we do, then nothing unless you ask." (§7) | Waitlist, quiz, Send a Bel, First Visit Plan, Meet the Machine |
| 2. The door | Tue 5 Jan | **New year, no pressure. No resolutions needed.** + "the hard part was the door." | D01 hero, Quiet by default, "Same price in every size", stamp card |
| 3. Rest, don't quit | 8–22 Jan (Mallow Hours drops 19 Jan) | "Rest counts. Come back whenever." · "mm. rest counts." | Rest stamps count fully; nothing goes down |
| 4. Bring your gym person | Tue 2 Feb | "Bring your gym person. You both get stickers." | Buddy Pack, Bring a Buddy |

### 9.2 Pre-launch (Nov–Dec 2026)

Founder dates: §0. Build milestones: §10.3.

| When | Founder [F] | Build session [C] |
|---|---|---|
| 10–20 Nov | §0 tasks to 17 Nov; §6.3.4 template paste; creator long-list of 60 | M0–M5 by Fri 20 Nov (incl. `golive/sample-rounds.json`) |
| Mon 23 Nov (latest 28 Nov) | Order sample round 1 (§8.4) | — |
| Fri 27 Nov | Shopify, Payments, Printful app (§8.2 steps 3–6); step-8 `tierMode` test; home-state sales tax | M6–M7: club-mode build (`npm run build:club`) |
| **Tue 1 Dec** | DNS live (§8.2 step 3). First post: "We open on Tuesday 5 January." | — |
| 1–8 Dec | QA round 1; laid-flat photos; 10 Comeback-Dev interviews (§2 decision 17); shortlist 35 creators; round 2 by ~Tue 8 Dec | M8 by Fri 4 Dec (D14–D18, D21 first); QA file fixes |
| Tue + Thu in Dec | **Meet the Machine** (§4.8 #12): what it is, its sticker, wiping it, what if it's taken; **never form, frequency or body advice**. Treadmill, cable machine, rowing machine, dumbbell rack (Pip & Pop), stretch corner (Mallow), locker room (Gus), water fountain (Sip) | Stills, flat cards |
| ~9–10 Dec | **Gifting wave 1** (20), only QA-passed pieces; ship by Printful's standard cutoff (2025: 11 Dec [S]; 2026 [U]) | M9 by Fri 11 Dec |
| Week of 14 Dec | Send a Bel push ("for someone starting the gym in January"); the e-card covers the wait: no gift orders | — |
| Mid-Dec | Lawyer review; prices signed off; products as drafts | `npm run golive:policies` |
| 28 Dec – 4 Jan | Schedule launch posts and emails; §8.2 steps 20–22 | Final `npm run ci`; `golive:printful -- --live` diff clean |

**`content/social.json`**: one entry per Meet the Machine episode (7) and crew skit (6, §9.4): `{id, pillar: 'meet-the-machine'|'crew-skit', title, beats: CopyString[] (3–6), caption: CopyString, speaker}`.

**Creator seeding** (**20 in wave 1 + 15 in wave 2**, the second shipped ~5 Jan with Mallow Hours and Buddy pieces):

| Criterion | Rule |
|---|---|
| Size | 1k–50k followers [T] |
| Niches (≥ 1) | Beginner strength, first-gym-visit stories · gym anxiety (find creators via tags like #gymanxiety; never use gendered trend tags such as #shygirlworkout in our captions, products or line names) · **plus- and mid-size fitness** · **mental-health movement** ("I move for my brain") · returners (parents, post-injury, burnout) · adaptive and disabled fitness · queer and trans fitness |
| Mix | ≥ 30% plus-size; ≥ 30% men or non-binary (Dev); never only women-coded studio content |
| Red flags (last 20 posts; any = no) | Before/after or progress photos · weight, calorie or diet talk · supplement or diet sponsors · filming strangers or reacting to others' gym clips · grind language ("no excuses") · mocking gym-goers · mirror body-checks as the main format |
| Gift · obligation | One launch piece (Quiet or Loud) + the D11 sheet, a personal Send a Bel e-card as the note (no pack-ins). **No obligation to post**; posts need FTC disclosure (§8.6 row 5), the consent rule below, no health or outcome claims |
| Affiliate (optional) | `<NAME>10` (10% off; the one discount) + 15% commission on net sales, monthly (norm 10–20% [T]); Shopify Collabs or manual [U] |

**Consent-first filming rule: ALL content** (brand, founder, creators, reposts); in `golive/legal/creator-agreement.md`.
1. **Never film strangers.** Nobody identifiable in frame unless they agreed (signed release for brand shoots).
2. Shoot at home, outdoors with nobody in frame, or in a gym with its permission, in an empty area or booked time.
3. If anyone else is in frame, even blurred or far in the background, don't post it. Reshoot.
4. No stitches, duets or reactions to anyone filmed without consent.
5. No body or progress photos. Fits are laid flat, or self-filmed and framed on the garment.
6. Reposts need written permission (§8.6 row 15). Never feature minors.

### 9.3 Launch week, day by day

US Eastern. The waitlist was promised **one** email (W0, §9.6).

| Day | Email and social | Site and ops |
|---|---|---|
| **Mon 4 Jan** | Schedule W0 and Tue posts | Test orders refunded. Evening: step 22 (club build, waitlist off; 16 listings active, password **on**). axe + Lighthouse on the theme; every launch PDP on iOS Safari and Android Chrome |
| **Tue 5 Jan: LAUNCH** | 09:00 W0 to every subscriber: "New year, no pressure. No resolutions needed." (W1 emails due this week slip a week: cap). 08:45 "Bel at the door" video (TikTok, Reels) · "Meet the crew" carousel · launch pins; tell creators (no obligation) | 08:30 password **off**. Approve orders by hand, hourly to 18:00 (§8.5). Reply to every comment (§9.4) |
| Wed 6 Jan | "Your volume, your call": Quiet / Loud / Private flat-lay + label reveal | Support inbox twice a day; Printful queue |
| Thu 7 Jan | Pip & Pop: Buddy Pack + Bring a Buddy · First Visit Plan Reel · 10 pins | `BUDDY15`/`BUDDYSHEET` redemption counts work |
| **Fri 8 Jan** | **"Rest, don't quit" opens** (8–22 Jan; 2nd-Friday Quitter's Day [S]): Mallow "mm. rest counts." + "rest days go on the card" *(new)* | No discount, no countdown |
| Sat 9 Jan | Scheduled: one UGC repost, written permission only | Founder rest day |
| Sun 10 Jan | Meet the Machine episode | Prepare the week-1 dashboard |
| **Mon 11 Jan** | — | **Week-1 review** (§9.8). First shipping emails about now (production 2–5 business days [V]) |
| Tue 12 Jan | Weekly email cap applies; Gus: "starting again counts as starting." (2nd-Tuesday Quitter's Day [S]) | Manual approval until 18 Jan |

### 9.4 Content pillars & cadence

| # | Pillar | Format | Example | Share |
|---|---|---|---|---|
| 1 | **Meet the Machine** | Equipment narrates; diagrams | "The cable machine. Yes, it has a little sticker. Here's where." | 30% |
| 2 | **Crew skits** | 15–30 s animation or puppet stills | The premises below | 25% |
| 3 | **"First time I…"** | Consenting creator and UGC stories | "First time in the weights area" | 15% |
| 4 | **Laid-flat fits** | "What I wear when I'm nervous", three-metre test, label reveal | Quiet vs Loud vs Private on one table | 15% |
| 5 | **Mallow Hours** | Rest on purpose, slow days | "slow days count too." | 10% |
| 6 | **Small kind things** | Club Rules, Tuck's consent tips | "(off camera, on purpose.)" | 5% |

**Crew-skit premises** *(new)*: (1) Bel's parking-lot pep talk, "okay. okay.", then the door · (2) Gus walks back in after three years away; nobody asks where he's been · (3) Pip & Pop go for a high-five and remember they're one dumbbell · (4) Mallow takes the stretch corner on a slow day: "mm. rest counts." · (5) Ollie's first visit: amazed by lockers, mats, the water fountain · (6) Tuck checks a photo's background is empty before anyone posts.

**Channels** (≈ 6–8 founder hours a week, batched Mondays): **TikTok** 4 posts/week (Tue, Thu, Fri, Sun) + 2 in-character video replies; stitches **only** of consenting creators; no TikTok Shop in v1 (fees, POD shipping [U]) · **Instagram** 3 feed posts (Reel, carousel, flat-lay) + 3–5 stories a week; story polls for Side Quest colourway votes (no prizes) · **Pinterest** 10 scheduled pins a week; evergreen boards (beginner gym outfits, gym bag essentials, first gym visit checklist → First Visit Plan, flat-lays) linking to PDPs; search-driven [T] · **Email** ≤ 1 marketing email a week (§9.6).

**In-character reply rules**
1. **One character per reply**: nerves or a first visit → Bel · rest or a bad week → Mallow · coming back → Gus · buddies, tagged friends → Pip & Pop · water, hype → Sip · other firsts → Ollie · filming, privacy → Tuck. §4.4 voice rules exactly.
2. **Out of character** ("a real person", no jokes) for orders, sizing, money, complaints, accessibility, bodies, health, injury or crisis (§8.6 row 14).
3. Never comment on a body, even kindly ("love that fit", not "you look amazing"). No form, frequency or diet advice: "a trainer at your gym can help with that."
4. Hide body-shaming, doxxing, filmed strangers; block repeat offenders.
5. The founder ("mascot guardian") signs off new poses and copy (§4.7).

| Comment | Character | Reply |
|---|---|---|
| "first time tomorrow, terrified" | Bel | okay. okay. tomorrow we're in. the hard part is the door. *(new)* |
| "skipped all week, feel bad" | Mallow | mm. rest counts. you're still on the card. |
| "first time back in 5 years" | Gus | welcome back. no catching up required. |
| "did my first class" | Pip & Pop | pip: you made it. / pop: WE made it! |
| tags a friend | Pip & Pop | you go, / i'll go too. |
| "asked someone for help today" | Ollie | oh! that counts. *(new)* |
| "remember to hydrate" | Sip | PROUD of you. also, water. |
| "can I film at my gym?" | Tuck | (psst. ask your gym first, and keep everyone else out of frame.) *(new)* |

**Banned behaviours (every channel):** stitching or reacting to non-consenting people's clips · dunking on "gym bros" or anyone who trains hard (we reject the culture, not the people) · guilt-trip mascot humour ("Bel is disappointed you skipped"; no "unhinged" mascots) · bought followers, engagement pods, fake reviews (§8.6 row 6) · trending sounds with body or diet lyrics · and everything in §4.4/§4.9 and the §9.2 consent rule.

### 9.5 Community & referral roll-out

| Date | Feature (where) | Gate |
|---|---|---|
| Tue 1 Dec | Quiz, Send a Bel, First Visit Plan, stamp card with day-one line (`club.{domain}`, local-only) | `features.*` on |
| Tue 5 Jan | Firsts (`FIRSTB1`–`FIRSTB6`), **Bring a Buddy**, Buddy Pack (D08), Q/L/P Style option (Shopify + club) | §8.2 step 12 codes tested |
| Tue 19 Jan | Mallow's rest nudge, opt-in, off by default (club, local-only) | — |
| Tue 2 Feb | Bring a Buddy push; D18 Buddy Packs, tee $60, crew $96 (Shopify + club) | — |
| Tue 2 Mar | Cheer wall v1.1 (Ollie); D12 patches (club) | **Only with a moderation plan:** backend, preset replies only, ≤ 140 characters, banned list, report button, daily queue (24 h SLA), 13+; else `demo` |
| Tue 3 Aug | Start a Crew + D27 crew backs (club + Shopify) | `features.crews` on only if the cheer wall ran cleanly since March |
| Tue 7 Sep | D28 "showing up since {year}", year picker (Shopify) | `features.personalisation` on; draft-order review (§8.3) |
| Tue 5 Oct | Crew-member vote: Cora vs Skip (club + IG stories) | No prizes (§8.6 row 16) |
| Tue 7 Dec | "Your year in stamps" recap (club, local data) | Never a ranking |

**Bring a Buddy at launch.** Club mode shows the live codes (`BUDDYSHEET`, `BUDDY15` on `/bring-a-buddy/`; `FIRSTB1`–`FIRSTB6` on `/firsts/`) in `<code>` instead of the mock ones (§7.3) [C]. Rules: §8.2 step 12. Track redemptions weekly; unique per-referrer codes (a referral app [U]) only past 50 a month. Physical Firsts and referral stickers (≈ $2 base each [T]) go out only "with any order", sharing shipping (Printful may still split them [U]).

### 9.6 Email flows

| Flow | Trigger | Emails and timing | Subject lines |
|---|---|---|---|
| **W0 Launch** | Every subscriber (waitlist, quiz, plan) | 1 email, Tue 5 Jan 09:00, with an opt-in button for the plan emails; waitlist-only contacts get nothing more unless they opt in | New year, no pressure. No resolutions needed. |
| **W1 Welcome / quiz result** | Quiz or First Visit Plan signup (tag `quiz-<character>`) | E1 now · E2 day 7 · E3 day 14 · E4 day 21 · E5 day 28. E1: 6 quiz-result variants + `FIRSTVISIT10` (December signups get E1 at once; the code works from 5 Jan) | E1 Here's your First Visit Plan. Bel made it. *(new)* · E2 The hard part was the door (here's a plan for the rest) · E3 We don't film strangers. Here's what we do instead. *(new)* · E4 Quiet, loud, or a secret on the inside *(new)* · E5 Bring your gym person. You both get stickers. |
| **O Order updates** (transactional; Shopify) | Order events | Confirmation · in production (only past 3 business days) · shipped · split shipment · delay (M3, FTC option) · review request 3 days after delivery (one; no sentiment-tied incentive) | Order's in. It's being made just for you. *(new)* · It's on its way: {order} *(new)* · Your order is coming in {n} boxes *(new)* · Heads up: your order's taking a little longer *(new)* · How's it wearing? |
| **R Cart reminder** | Abandoned checkout; only contacts who ticked marketing consent | **One** email at 24 h; no discount, no second reminder, no countdown | Your bag's still packed. No rush. *(new)* |
| **WB Win-back** | 90 days after a first order with no second · 150 days without an open | One each; no reply in 14 days → suppress | Welcome back. No catching up required. · Want to keep hearing from us? *(new)* |
| **D Drops** | Each drop Tuesday, 09:00 | One email (that week's marketing email) | §9.7 |

**Rules for every email:** No email is ever triggered by browsing or page views. ≤ 1 marketing email per person per week (transactional exempt); banned-words and copy-lint pass; no discount in any reminder; `FIRSTVISIT10` only in W1 E1; plain-text part; alt text; ink-on-oat images that survive dark mode; footer postal address and one-click unsubscribe (page: "You're unsubscribed. We'll still be cheering, just quietly."); from `hello@{domain}` with SPF, DKIM, DMARC [U: bulk-sender rules].

**`content/emails.json`**: `{flow, step, subject, preheader, body: CopyString[]}` (`subject`/`preheader` surface `"email-subject"`, body `"email-body"`); ≤ 120 words per body; bodies are *(new)*, for one founder batch review.

### 9.7 Drop cadence

Dates, names, designs and calm Side Quest windows: §5.6 (Tuesdays, 09:00 ET). No countdowns; ≥ half of each drop's garment colours neutral; no gendered holiday hooks.

| # | Social hero | Email subject |
|---|---|---|
| 0 | Bel at the door | New year, no pressure. No resolutions needed. |
| 1 | Mallow's rest stamp | Rest day? It goes on your card too. *(new)* |
| 2 | Split-tee reveal (Valentine's week: bring your gym person) | Bring your gym person. You both get stickers. |
| 3 | Laid-flat leggings and a squat-test diagram (no bodies, no test photos) | First Things: here until 30 April (it might come back) *(new)* |
| 4 | Colourway reveal | Pool Day: mint and chambray are here *(new)* |
| 5 | Bel with headphones | Every day is brain day. Bel brought headphones. *(new)* |
| 6 | Receipt skit | Total: you showed up |
| 7 | Butter + Bay flat-lays | Golden Hour: butter and bay *(new)* |
| 8 | Crew page | Start a crew. Pick the name together. *(new)* |
| 9 | Gus returns | Welcome back. No catching up required. |
| 10 | Vote post | A new crew member is coming. You get a vote. *(new)* |
| 11 | Gift sets | Send a Bel to someone starting the gym *(new)* |
| 12 | Year recap | Your year in stamps *(new)* |

### 9.8 KPIs, targets & weekly dashboard

Day-90 targets are **internal placeholders** unless tagged; re-set after 30 days of data.

| KPI | Definition | Target | Source |
|---|---|---|---|
| **Email capture** | New subscribers ÷ unique visitors (store + club) | **≥ 5%** (forms average ≈ 3% [T]) | ESP + analytics |
| Quiz completion | `quiz_complete` ÷ `/quiz/` page views | ≥ 60% [U] | Cookie-free counter (§7.13) |
| **Conversion** | Orders ÷ store sessions | ≥ 1.5% [U] | Shopify |
| **AOV vs $75** | Revenue after discounts ÷ orders; share ≥ $75 and within $10 below | AOV ≥ $55; 25–40% ≥ $75 [U] | Shopify |
| Contribution per order | §5.7 model on real orders | ≥ 35% blended; §5 floors | `exports/catalog-margins.csv` + Printful |
| **Misprint / damage** | Printful claims ÷ units shipped | ≤ 2%; > 5% on one design → pause it [U] | Printful |
| Size swaps / fit complaints | ÷ garment units | ≤ 5% [U] | Support log |
| **Repeat rate** | Customers with ≥ 2 orders ÷ all, rolling 90 days | ≥ 10% [U] | Shopify |
| **Weekly visits to `/stamp-card/` (cookie-free page count)** | Page views per week; no user ids, no stamp events | ≥ 150 by week 12 [U] | Cookie-free counter |
| Creator posts · code redemption | Posted ÷ gifted · code orders ÷ reach | ≥ 30% · ≥ 3% [T placeholders] | Manual |
| Email health | Unsubscribes per send · spam complaints | ≤ 0.5% · < 0.1% [U] | ESP |
| UGC per 100 orders | Permissioned product posts | ≥ 5 [U] | Manual |

**Weekly dashboard** (`golive/dashboard/weekly.csv`, a row every Monday, 30 minutes; `quiz_starts` = `/quiz/` page views; `firsts_claimed` = `FIRSTB1`–`FIRSTB6` redemptions in Shopify):

```text
week_start,sessions_store,visitors_club,email_signups,capture_rate,quiz_starts,quiz_completes,orders,conversion,revenue_usd,aov_usd,orders_ge_75_pct,units,printful_claims,misprint_rate,size_swaps,repeat_customers_90d,stamp_card_weekly_visits,ecards_created,firsts_claimed,buddy_redemptions,creators_gifted,creator_posts,creator_code_orders,ad_spend_usd,contribution_usd,one_change_this_week,notes
2027-01-04,,,,,,,,,,,,,,,,,,,,,,,,,,,
```

Monday: fill the row, note anything off-target, pick **one** change (`one_change_this_week`). Two weeks off-target on misprints or fit → pause that listing before any marketing spend.

### 9.9 First 90 days plan & budget

| Days (dates): focus | Must happen | Gate to continue |
|---|---|---|
| Pre (10 Nov – 4 Jan): build, samples, waitlist | D1–D6; sample rounds 1–2; 10 Comeback-Dev interviews 1–8 Dec on round-1 samples (§2 decision 17); 20 creator gifts; §8.6 "before launch" rows | Every launch listing passed QA, or is dropped (§5.5) |
| 1–14 (5–18 Jan): launch, first deliveries | Manual approvals, daily support, week-1 review | Misprints ≤ 2% of the first 50 units; else pause creators and paid, fix files |
| 15–30 (19 Jan – 3 Feb): Mallow Hours | Round 3 by ~25 Jan; Growth trial? (worth it at base spend ≥ $500/mo at 5% off, or labels ≥ $278/mo, §5.7); auto-approval if no fraud | Capture ≥ 3% and rising |
| 31–60 (4 Feb – 5 Mar): Buddy System, activewear, paid test | Squat-test result by 16 Feb for 2 Mar; **paid test:** $300 over 14 days boosting the 2 best organic posts, pixels only behind consent (§8.2 step 19) | Keep paying only if cost per first order ≤ $20 [U] (≈ one first order's contribution) |
| 61–90 (6 Mar – 4 Apr): Side Quest, wave 2, review | Pool Day samples by 9 Mar; `docs/90-day-review.md`: KPIs vs targets, keep or kill per listing (kill: < 3 sales in 60 days, not a hero), cheer wall and headless go/no-go (§8.1) | — |

**Budget, 10 Nov 2026 – 4 Apr 2027** (USD; excludes per-order costs paid from revenue: Printful base, labels, payment fees, absorbed shipping, the $0.40 surcharge, Shopify Tax):

| Item | Low | Expected | High | Tag |
|---|---|---|---|---|
| Samples round 1 (14 pieces + stickers) | 300 | 375 | 450 | [U] |
| Samples round 2 (fixes, drops 1–2, AOP gate) | 300 | 350 | 400 | [U] |
| Samples round 3 (drop 3) | 100 | 150 | 200 | [U] |
| Domain, 1 year | 10 | 20 | 25 | [U] |
| Shopify Basic Dec–Mar (4 × $39 monthly; yearly is $29/mo upfront) | 156 | 156 | 156 | [S] |
| Printful Growth (Feb–Mar if the trial pays) | 0 | 50 | 75 | [V] |
| Shopify Email beyond the free allowance | 0 | 0 | 20 | [U] |
| Cookie-free analytics on `club.{domain}` | 0 | 27 | 27 | [U] |
| Creator gifting (20 / 30 / 35 × ≈ $25 incl. shipping) | 500 | 750 | 875 | [U] |
| Firsts + referral stickers (≈ $2 base each) | 50 | 100 | 150 | [T] base |
| Small paid test | 0 | 300 | 500 | founder choice |
| Photo props (backdrop, grey card, ruler) | 0 | 50 | 100 | [U] |
| **Subtotal: launch operations** | **1,416** | **2,328** | **2,978** | |
| USPTO filing: class 25 (high: + 16 + 21) | 350 | 350 | 1,050 | [S] $350/class |
| Attorney clearance opinion (quote) | 500 | 1,000 | 1,500 | [U] |
| LLC state filing fee | 50 | 150 | 500 | [U] |
| **Subtotal: legal & admin** | **900** | **1,500** | **3,050** | |
| **Grand total** | **2,316** | **3,828** | **6,028** | + 10% contingency (≈ $383 on expected) |

Expected operations ($2,328) ≈ the contribution of 144 hero tees at $16.12 [L arithmetic on §5.7]. Shopify intro offers may lower its line [U]. Recheck every [S]/[U] price the day you pay; log it in `docs/decisions.md`.

---

## 10. Build plan & milestones

Execute M0 → M9 in order (§3 rule 1). Before each milestone, read its **Read first:** sections in full. A milestone is done only when its acceptance checks and `npm run ci` (`-- --art-scope launch` in M5–M7) pass **in this session**; then commit as `M<n>: <its §10.3 name>` (§3 rule 19), tick it in `docs/progress.md` and give the founder a 5-line status (§0). **The launch set (D01–D13, 16 listings) is finished end to end in M1–M7, before any of D14–D30 is drawn (M8).** Where two sections disagree, **paths and script names follow §10**; numbers and specs follow the owning section. Log each case in `docs/decisions.md`.

### 10.1 Final repo tree

The single source for paths; it wins over any other section (§1).

```text
.                          # npm package "storefront"; brand literal only where §4.1 allows
├─ BUILD-BRIEF.md REPORT.md (D7) README.md (how to run; no brand literal: use "the store")
├─ brand.config.json       # §4.1 block (verbatim)
├─ print-specs.json        # §6.2; schema: art/print/spec-types.ts
├─ package.json package-lock.json .nvmrc (24.22.2) .gitignore .env.example (names only, empty values)
├─ next.config.ts tsconfig.json postcss.config.mjs eslint.config.mjs vitest.config.ts playwright.config.ts
├─ lighthouserc.json linkinator.config.json AGENTS.md (block written by `next dev`) CLAUDE.md (`@AGENTS.md`)
├─ brand/         tokens.json banned-words.json blocklist.json
├─ art/
│  ├─ characters/ characters.json kit.ts (A.5 port, incl. halo, onDark) lod.ts
│  ├─ palette.ts (generated by `npm run brand`) fonts.ts
│  ├─ lib/        text.ts arc-text.ts tile.ts place.ts props.ts recipes.ts halo.ts (re-export + unitPx wrapper)
│  ├─ designs/    designs.json types.ts index.ts D01.ts … D30.ts shared/label.ts overrides/ (optional, §6.9)
│  ├─ print/      spec-types.ts color.ts export.ts inspect.ts validate.ts plan.ts manifest.ts
│  ├─ mockups/    templates/<type>.ts flatlay.ts og.ts
│  ├─ templates/  index.json (+ downloaded partner templates, §6.3.4)
│  ├─ REVIEW.md   # visual-review log (§6.7)
│  └─ out/svg/ out/cache.json review/            # git-ignored
├─ print-files/   manifest.json validation-report.md <D>/<id>.png (PNGs git-ignored)
├─ catalog/
│  ├─ src/        colors blanks listings bundles collections drops pricing-rules margin-exceptions transit cutoffs (.json)
│  │              (cutoffs.json: [] until filled by 15 Oct 2027, §8.5)
│  ├─ live/printful/ .gitkeep, then <id>.{product,variants,prices,sizes,mockup-templates}.json shipping-rates.json mockups/
│  ├─ size-guides/    <productKey>.json   # live pull or founder copy with URL only; never invented
│  └─ catalog.json    # compiled by `npm run catalog`; committed
├─ content/       <page>.json (one per §7.5 page) print-lines.json cs-macros.json emails.json social.json
├─ app/           layout.tsx globals.css page.tsx not-found.tsx sitemap.ts robots.ts manifest.ts catalog-index.json/route.ts
│                 + one folder per §7.4 route (shop/ … your-data/; M6 and M7 list them)
├─ components/    layout/ cast/ (CastMember.tsx, SpeechBubble.tsx) ui/ product/ cart/ checkout/ community/ brand/
├─ lib/           brand.ts copy.ts flags.ts site.ts storage.ts storage-registry.ts analytics.ts
│                 catalog/{types,schema,ids,read,load,visible}.ts   commerce/{types,index,pricing,codes}.ts + mock/ + shopify/
│                 community/{stamps,firsts,quiz,crews,cheers,ecard,moderation}.ts   delivery/{types,window}.ts   seo/{metadata,jsonld}.ts
├─ stores/        cart checkout orders stamps firsts quiz codes cheers crews prefs (.ts)
├─ styles/tokens.css   # generated by `npm run brand`; committed
├─ public/        brand/ fonts/ mockups/ og/   # generated and git-ignored (headers: the build writes out/_headers)
├─ scripts/
│  ├─ ci.ts       # STEPS table (§10.2) → artifacts/ci-summary.md (D7)
│  ├─ brand/build.ts
│  ├─ catalog/    build.ts pull.ts margins.ts export-shopify.ts
│  ├─ art/        render-print.ts validate-print.ts contact-sheets.ts render-mockups.ts handoff.ts
│  ├─ site/       check-bundle.ts scan-built-html.ts route-manifest.ts screens.ts check-club.ts write-headers.ts
│  └─ golive/     render-policies.ts sample-plan.ts
├─ golive/        README.md printful-sync.ts lib/{printful,plan,diff,limiter}.ts state/printful-map.json sample-rounds.json
│                 theme/{assets/{brand-tokens,brand-fonts}.css, snippets/*.liquid, README.md}   (§8.2 step 16)
│                 policies/{shipping,returns,privacy,terms}.md legal/{creator-agreement,ugc-release,photo-release}.md
│                 sample-plan.md qa-checklist.md dashboard/weekly.csv
├─ exports/       shopify-products.csv catalog-margins.csv printful-sync-plan.json printful-sync-checklist.md
│                 sample-plan.csv policies/ images/ (images/ git-ignored)
├─ tests/         unit/ types/schema-matches.test-d.ts integration/{print-determinism,rename}.test.ts
│                 e2e/ (18 flows, §7.14) a11y/all-routes.spec.ts
│                 fixtures/ empty.ts {bel-happy-idle,icon,minibel-color,minibel-reverse,minibel-solid}.svg (A.5)
│                           store v0 shapes, PNG builders, fake Printful
├─ docs/          progress.md decisions.md 90-day-review.md (template) ugc-permissions/ (git-ignored)
├─ licenses/      fonts.json (by hand, M1) OFL-Caprasimo.txt OFL-AtkinsonHyperlegibleNext.txt README.md (licences + exceptions)
└─ (git-ignored)  node_modules/ .next/ out/ .vitest/ artifacts/ handoff/ photos/ test-results/ playwright-report/
                  .lighthouseci/ .env .env.* (but keep !.env.example)
```

- **Commit** sources plus small, deterministic generated text: `catalog/catalog.json`, `print-files/manifest.json`, `styles/tokens.css`, `art/palette.ts`, `golive/theme/assets/brand-tokens.css`, the text files in `exports/` (§3 rule 16). **Don't commit** regenerated binaries (PNG, WebP, AVIF, WOFF2) or files over 10 MB (§3 rule 19).
- `.env.example` lists, with empty values: `NEXT_PUBLIC_COMMERCE_PROVIDER` `NEXT_PUBLIC_SITE_ENV` `NEXT_PUBLIC_AS_OF` `NEXT_PUBLIC_ANALYTICS_DEBUG` `NEXT_PUBLIC_SITE_MODE` `NEXT_PUBLIC_ANALYTICS_HOST` `NEXT_PUBLIC_SHOPIFY_STORE_DOMAIN` `NEXT_PUBLIC_SHOPIFY_STOREFRONT_TOKEN` `PRINTFUL_TOKEN` `PRINTFUL_STORE_ID` `MOCKUP_PROVIDER` `RUN_NETWORK_TESTS`.

### 10.2 npm scripts

Exact names; apart from `test`, no aliases. Env-prefixed commands assume a POSIX shell (macOS, Linux, WSL). When: `ci n · M<k>` = step n of `npm run ci`, due from M<k>.

| Script | Command | Does | When |
|---|---|---|---|
| `dev` | `next dev` | Local dev server | M0+ |
| `preview` | `serve out -l 4173` | Serves the static build | M6+ |
| `brand` | `tsx scripts/brand/build.ts` | `brand/tokens.json` → `styles/tokens.css`, `art/palette.ts` (+ the theme's `brand-tokens.css` from M9); WOFF2 → `public/fonts/`; logos, icon, favicons → `public/brand/`; verifies `licenses/fonts.json` hashes | ci 1 · M1 |
| `catalog` | `tsx scripts/catalog/build.ts` | `catalog/src/*` + `designs.json` + `catalog/live/` → `catalog.json`: Zod + `superRefine` invariants, `printFileIds` (`plan.ts`), deterministic `Mockup[]`; reports base costs moved > $1.00 and floor breaches; never edits a price | ci 2 · M4 |
| `catalog:pull` | `tsx scripts/catalog/pull.ts` | Default: validates committed snapshots offline (§5.10). `-- --live` + `PRINTFUL_TOKEN`: GETs the §5.1 endpoints into `catalog/live/printful/` with `checkedAt` | once a token exists |
| `export:shopify` | `tsx scripts/catalog/export-shopify.ts` | `exports/shopify-products.csv` (drafts) + `exports/catalog-margins.csv` (§5.10) for listings with `launch: true` or a drop date ≤ `AS_OF` | M4, M9 |
| `export:printful` | `tsx golive/printful-sync.ts --plan` | Offline: `exports/printful-sync-plan.json` + `exports/printful-sync-checklist.md`; blocks any needed file that isn't `pass` + `specVerified` + not `provisional` | M9 |
| `art:print` | `tsx scripts/art/render-print.ts` | Renders the catalog's unique print-file ids → `print-files/**` + manifest (worker pool, cache). `-- --scope launch\|all` (default `all`): the manifest records `scope` and holds exactly that scope's ids, sorted; a `--scope launch` run against an `all` manifest exits 1 (from M8 on only `all` runs) | ci 3 · M5 |
| `validate:print` | `tsx scripts/art/validate-print.ts` | §6.6 on every manifest entry → results + `validation-report.md`; **exit 1 on any fail** | ci 4 · M5 (core M3) |
| `mockups` | `tsx scripts/art/render-mockups.ts` | D4 (§6.8): `public/mockups/**`, `public/og/**`, PNG copies in `exports/images/`; never calls an API | ci 5 · M5 |
| `art:sheets` | `tsx scripts/art/contact-sheets.ts` | `-- --cast`: `art/review/cast-{expressions,poses,lod,dark}.png` (M2); per design: `art/review/<D>.png` (M5) | M2+ (not ci) |
| `art` | `npm run art:print && npm run validate:print && npm run art:sheets && npm run mockups` | Whole art loop | any time |
| `art:handoff` | `tsx scripts/art/handoff.ts` | `-- <D-id>` → `handoff/<D>/` (§6.9) | optional |
| `typecheck` · `lint` | `tsc --noEmit` · `eslint . --max-warnings 0` | Types; lint (§7.14 ESLint rules) | ci 6–7 · M0 |
| `test` | `npm run test:unit` | Entry point | — |
| `test:unit` | `vitest run --typecheck --reporter=dot tests/unit tests/types` | Only `tests/unit` + `tests/types` (§7.14 config) | ci 8 · M0 |
| `build` | `next build && tsx scripts/site/write-headers.ts` | Static export → `out/`, then `out/_headers` (§7.15: noindex only when `NEXT_PUBLIC_SITE_ENV !== "production"`; `NEXT_PUBLIC_ANALYTICS_HOST` in CSP `connect-src` only in club mode). ci runs `env -i PATH="$PATH" HOME="$HOME" npm run build`. Needs `brand`, `catalog`, `mockups` outputs | ci 9 · M0 |
| `scan:html` | `tsx scripts/site/scan-built-html.ts` | §7.14 post-build scan (incl. `route-manifest.ts`, §7.10 SEO/JSON-LD) | ci 10 · M6 |
| `check:bundle` | `tsx scripts/site/check-bundle.ts` | §7.12 JS/HTML/image/font budgets from `out/` | ci 11 · M6 |
| `links` | `linkinator ./out --recurse --skip "^(?!http://localhost)"` | Internal links only | ci 12 · M6 |
| `test:e2e` | `playwright test tests/e2e` | 18 flows (§7.14). `webServer`: `npx serve out -l 4173`. 6 projects: chromium, firefox, webkit at 1440; Pixel 7; iPhone 15; chromium with `reducedMotion: 'reduce'`. Reporter `failures` (if available, else `line`) plus HTML `open: 'never'` | ci 13 · M6 |
| `test:a11y` | `playwright test tests/a11y` | axe on every route + listed states; gate 0 violations | ci 14 · M6 |
| `test:integration` | `vitest run tests/integration` | Print determinism (5 fixed launch ids twice, same SHA-256). **Rename test** (§4.1): copy the working tree with Node `fs.cpSync`, filtering out `node_modules`, `.next`, `out` and `.git` (keeping `public/mockups`, `public/og`, `catalog.json`); symlink `node_modules`; set `name`; `npm run brand && npm run build`; assert per §4.1 for Gymlings and Huddlebell; 10-minute timeout; runs only here | ci 15 · M5 |
| `lhci` | `NEXT_PUBLIC_SITE_ENV=production npm run build && lhci autorun` | Lighthouse per `lighthouserc.json` (§7.12) | ci 16 · M6 |
| `test:club` | `tsx scripts/site/check-club.ts` | In a temp copy (rename-test procedure), builds club mode with `features.waitlist` `"on"` and `"off"`; asserts no DemoBar text; no `/cart/` or `/checkout/` in `out/`; robots allows indexing, no `X-Robots-Tag` in `out/_headers`; every email form posts to `https://{domain}/contact`; no "nothing was sent"; with waitlist on, every buy surface says "Join the waitlist" | ci 17 · M7 |
| `build:club` | `NEXT_PUBLIC_SITE_MODE=club NEXT_PUBLIC_SITE_ENV=production npm run build` | The public `club.{domain}` build (§7.3, §8.1) | M7; founder deploys |
| `build:full` | `npm run brand && npm run catalog && npm run art:print && npm run validate:print && npm run mockups && npm run build` | Everything the build needs (fresh clone, static host) | hosts (complete from M8) |
| `screens` | `tsx scripts/site/screens.ts` | `artifacts/screens/<route>@<w>.png` at 390/768/1440 | M6+ (not ci) |
| `golive:printful` | `tsx golive/printful-sync.ts` | Dry-run diff vs `golive/state/printful-map.json`; `-- --live` = GET-only; `--apply` founder only; other flags §8.3 | M9 (offline); founder (live) |
| `golive:policies` | `tsx scripts/golive/render-policies.ts` | `golive/policies/*.md` with real values → `exports/policies/` | M9 |
| `golive:samples` | `tsx scripts/golive/sample-plan.ts` | Joins `golive/sample-rounds.json` with `catalog.json` for costs → `golive/sample-plan.md` + `exports/sample-plan.csv` | M5 |
| `ci` | `tsx scripts/ci.ts` | Runs ci 1–17, then a final zero-env `build` (so `out/` is zero-env). Stops at the first failure; writes `artifacts/ci-summary.md` (step, command, exit code, duration, last 20 lines). `-- --art-scope launch` passes `--scope launch` to steps 3–5 (M5–M7 only) | every milestone (steps before their `since` are skipped) |

**Exporters** (`export:shopify`, `export:printful`) always write their files, list every blocker (null partner ids, planning margins, unverified or provisional specs) and **exit 1 while any remain**. They are not ci gates; exit 1 is expected in the prototype.

**ci gating.** `scripts/ci.ts` holds a fixed STEPS table: ci 1–17 (§6.5's order, then `typecheck`, `lint`, `test:unit`, `build` and the post-build checks), each with the `since` milestone of the When column. The current milestone is the first unticked box in `docs/progress.md`, or `--milestone M<n>`; a step not yet due is written to `artifacts/ci-summary.md` as "skipped (not built until M<n>)". **From M9 any skip is a failure.** Vitest runs with `passWithNoTests: true`.

### 10.3 Milestones M0–M9

| M | Milestone | Needed by |
|---|---|---|
| M0 | Scaffold, pins, Next docs | Fri 20 Nov 2026 |
| M1 | Brand kit (D1) | Fri 20 Nov |
| M2 | Cast library (D1) | Fri 20 Nov |
| M3 | Print specs, validators (D2) | Fri 20 Nov |
| M4 | Catalog (D3) | Fri 20 Nov |
| M5 | Launch art, mockups, sample plan (D2, D4) | Fri 20 Nov (round 1 ordered Mon 23 Nov) |
| M6 | Storefront core (D5; closes D1) | Fri 27 Nov |
| M7 | Community, waitlist, club mode (D5) | Fri 27 Nov (club site live Tue 1 Dec) |
| M8 | Designs D14–D30 (D2, D4 complete) | Fri 4 Dec (round 2 ordered by ~Tue 8 Dec) |
| M9 | Go-live kit, theme kit, report (D6, D7) | Fri 11 Dec (lawyer review mid-Dec) |

**Dates are targets, not gates:** never skip an acceptance check to make a date. If a date will slip, say so in that milestone's 5-line status.

#### M0 · Scaffold, verified pins, Next docs
**Read first:** §3 rules 2, 3, 8, 19 · §4.1 "Tests (CI)" · §4.5 hex-literal rule · §6.1 · §7.1–§7.3 · §7.14 · §8.3 rule 6 · §10.1–§10.2
**Tasks**
- `git init`. Create `.nvmrc` (`24.22.2`) and `package.json` (`"name": "storefront"`, `"private": true`, `"type": "module"`, `"engines": {"node": ">=24.22.0"}`, every §10.2 script).
- For every package in §7.1 and §6.1, run `npm view <pkg> version time dist-tags`, then `npm i -E`. `sharp`, `@resvg/resvg-js`, `opentype.js`, `@expo-google-fonts/*`, `tsx` and all test tools are devDependencies. Log a table in `docs/decisions.md`: package · brief pin · installed · publish date · ≥ 14 days old? · licence.
- `npx playwright install --with-deps chromium firefox webkit`.
- Read the `node_modules/next/dist/docs/` guides for static export, metadata, JSON-LD, CSS and `useSearchParams`; list them in `docs/progress.md`.
- Write the §7.2, §7.3 and §7.14 configs (incl. `vitest.config.ts` + `tests/fixtures/empty.ts`), `.gitignore`, `.env.example` (§10.1) and `brand.config.json` (the §4.1 block verbatim; the name grep reads it). Add placeholder `app/layout.tsx` and `app/page.tsx`, `scripts/site/write-headers.ts` and the env part of `lib/site.ts` (`build` calls them; §7.15).
- Run `next dev` once, commit the `AGENTS.md` block, and make `CLAUDE.md` the single line `@AGENTS.md`. If `next dev` writes no block or `node_modules/next/dist/docs/` is absent, write `AGENTS.md` by hand ("Read node_modules/next/dist/docs/ if present; otherwise follow §7.1–§7.2"), log it in `docs/decisions.md` and continue.
- Write `scripts/ci.ts` (STEPS table, §10.2), `docs/progress.md` (M0–M9 checklist with the §10.3 dates), `docs/decisions.md` (every §2 decision, "default in use") and `licenses/README.md`.
- Tests: `pins` (no `^`/`~` in `package.json`; `.nvmrc` satisfies `engines`) · `name-grep` (§4.1 test 1; regex from `brand.config.json` `name`) · `hex-literals` (§4.5 allowlist) · `secrets-grep` (§8.3 rule 6 patterns and fake-token rule) · `licenses`: "shipped" = the font packages, `lucide-react` and every file copied into `public/` or `print-files/`, each OFL-1.1, MIT, ISC or Apache-2.0; every direct dependency OSI; transitive data and native binaries (`caniuse-lite` CC-BY-4.0, `@img/sharp-libvips` LGPL-3.0) are logged exceptions in `licenses/README.md`.
- Ask the founder once to read §2 and send overrides before M1 ends (§0).

**Acceptance**
- [ ] `node -v` prints `v24.22.x`, or the deviation is logged.
- [ ] `npm ls --depth=0` reports no missing or invalid packages; the pins test passes.
- [ ] `vitest list` with each script's filters shows `test:unit` collecting only `tests/unit` + `tests/types` and `test:integration` only `tests/integration`.
- [ ] `typecheck`, `lint` and `test:unit` pass. The zero-env build writes `out/index.html` and an `out/_headers` with `X-Robots-Tag: noindex, nofollow`.
- [ ] `npm run ci` passes, every step not yet due reported as skipped. `docs/decisions.md` has a row for every installed package and every §2 decision.

```bash
node -v && npm ls --depth=0
npx vitest list --typecheck tests/unit tests/types && npx vitest list tests/integration
npm run typecheck && npm run lint && npm run test:unit
env -i PATH="$PATH" HOME="$HOME" npm run build && test -f out/index.html && grep -q noindex out/_headers
npm run ci
```

#### M1 · Brand kit: config, tokens, copy rules, logo system (D1, part 1)
**Read first:** §4.1 · §4.4 · §4.5 · §4.6 · §6.1 (fonts and licences) · §7.7 · A.3 · A.5 · A.6
**Tasks**
- `brand.config.json` = the §4.1 block verbatim (written in M0). `brand/tokens.json`: the 17 colour tokens with roles (§4.5), type scale, radii, shadow, spacing. `brand/banned-words.json` is the §4.4 JSON verbatim. `brand/blocklist.json` per §7.3 (+ the §4.7 resemblance list).
- `lib/brand.ts` (the §4.1 derivations) and `lib/copy.ts` (`t(key, vars)` fills `{brand} {castNoun} {handle} {domain}`).
- `art/fonts.ts` (the two print TTFs only) and `art/lib/text.ts` (A.5 `textPath`/`fitText`, plus a glyph-index-0 throw and `capHeightPx`). Port A.3 and A.5's `wordmark()`, `miniBel()` and `iconMark()` into `art/characters/kit.ts`. Generate and commit the A.5 fixtures (`node crew-kit.mjs` once, A.5 intro); the port must match them byte for byte.
- `scripts/brand/build.ts` writes `styles/tokens.css` and `public/fonts/` (§7.7), `art/palette.ts` and `public/brand/`: wordmark (primary, reversed, one-colour), horizontal and stacked lockups, `favicon.svg`, `favicon-32.png`, `apple-touch-icon.png` (180), `icon-maskable-512.png`.
- Write `licenses/fonts.json` **once by hand** (§6.1 fields, fixed `checkedAt`) and the two OFL texts; `npm run brand` only verifies the hashes.
- Tests: `contrast` (every §4.5 row, including the 3 must-fail pairs) · `banned-words` (A.6: every cleared line in §4.4 → 0 hits at scope `product`; every replaced line and banned example → ≥ 1) · `copy-lint` (per §4.4) · `wordmark` (stem cx 3.885 em and bell 0.730 em above the baseline, ±0.005, keyed by the configured name; "huddlebell" → `stem: null` → horizontal lockup; "gymlings" finds a stem) · `fonts`.
- Read the favicon at 16/32/48 px, the solid bell at 120 px and the 24 px tiny kettlebell (§4.6); log them in `art/REVIEW.md`.

**Acceptance**
- [ ] The staged re-run below leaves no diff.
- [ ] Contrast values match §4.5 to ±0.01, and the 3 must-fail pairs fail. Favicon PNGs are exactly 32, 180 and 512 px square. `miniBel()` and `iconMark()` match their fixtures byte for byte.
- [ ] `art/REVIEW.md` shows: favicon not a ghost at 16 px; solid bell not a padlock at 120 px. The §2 overrides (or "none") are logged.

```bash
npm run brand && git add -A styles art/palette.ts brand && npm run brand && git diff --exit-code styles art/palette.ts brand licenses
npx vitest run tests/unit/{contrast,banned-words,copy-lint,wordmark,fonts,name-grep,hex-literals}.test.ts
```

#### M2 · Cast library + review sheets (D1, part 2)
**Read first:** §4.7 · §6.4.5–§6.4.6 · §6.4.7 rows D02 D05 D08 D10 · §6.4.8 rows D15 D18 D21 D22 · §6.7 · A.5
**Tasks**
- `art/characters/characters.json` (7 entries, §4.7 fields; voice lines verbatim from §4.4).
- Finish the A.5 port in `kit.ts`: 7 builders, the face kit, 10 expressions (Ollie's mouth never changes), tubes, sneakers, `halo()` and `onDark()` (they live in `kit.ts`; `art/lib/halo.ts` only re-exports them plus the per-layer `unitPx` wrapper). Add `lod.ts` (§4.7 LOD table; Icon never below 1.25 in).
- Keep the 4 [L] poses (A.5); build the 8 `spec` poses (§4.7) and §6.4.5's new builders.
- Write `scripts/art/contact-sheets.ts` with `--cast` mode (per-design mode added in M5). Run `npm run art:sheets -- --cast` and Read every sheet against §4.7's silhouette and misread table, the resemblance list and the Espresso/Navy halo. ≤ 3 fix rounds per item, then a founder item.
- `tests/unit/cast.test.ts`: `bel`/`happy`/`idle` matches the A.5 fixture `bel-happy-idle.svg`; every combination renders; the §6.4.3 fill and SVG checks; alt "{Name} the {object}, {expression}, {pose}"; nothing under `art/` imports React or touches `document`.

**Acceptance**
- [ ] The sheets show every character in all 10 expressions, every allowed pose at least once, all 4 LODs and the dark-garment halo (§1 D1).
- [ ] `cast.test.ts` passes. `art/REVIEW.md` has one row per sheet, each "pass" or "founder item". The high-five, stamp and hold-sign poses were inspected.

```bash
npm run art:sheets -- --cast && ls art/review/cast-{expressions,poses,lod,dark}.png
npx vitest run tests/unit/cast.test.ts
```

#### M3 · `print-specs.json`, colour maths, export core, validators (D2 foundation)
**Read first:** §5.10 (types.ts block) · §6.2–§6.3 · §6.4.3–§6.4.4 · §6.5–§6.6 · A.7–A.12
**Tasks**
- `lib/catalog/types.ts`, verbatim from §5.10 (§6 imports it).
- `print-specs.json` from §6.2: limits, the 5 rule sets, the 15 threads, and every seeded area plus its extras. `verified.value` is `false` everywhere, and `provisional: true` wherever §6.2 says so.
- `art/print/spec-types.ts` (+ `PrintSpecsSchema`) and `manifest.ts` (incl. `scope`, §6.5). Port A.7 `color.ts`, A.8 `export.ts`, A.9 `inspect.ts`, A.10 `validate.ts`, A.11 `arc-text.ts` and A.12 `tile.ts`, plus `art/lib/{place,props,recipes,halo}.ts`. Write the core of `scripts/art/validate-print.ts`.
- Tests: `print-specs` (schema; keys join to `ProductKey`/`PlacementId`; art box inside canvas; §6.2's canvas-literal grep) · `print-validate` (the 10 §6.6 fixtures each fail with their rule, plus one passing file; A.10's expected outputs) · `color` (A.7 `nearest()` reproduces the §6.3.2 thread map).

**Acceptance**
- [ ] `PrintSpecsSchema` parses the file; every area has extras; the literal grep finds 0 hits.
- [ ] Each fixture fails with exactly its own rule id. A crispEdges render of the fixture art has 0 pixels with 0 < alpha < 255.

```bash
npx vitest run tests/unit/{print-specs,print-validate,color,fonts}.test.ts && npm run typecheck
```

#### M4 · Catalog: seeds, compile, margins, Shopify CSV (D3)
**Read first:** §5.1–§5.10 · §6.4.1–§6.4.2 · §6.4.7–§6.4.8 (Text columns) · §6.5 (print-file ids) · §6.8 (Output, Views, Alt text) · §7.2 (`isVisible`) · §7.3 (data files §7 adds) · §8.6 row 11 · Appendix B.3–B.4
**Tasks**
- `lib/catalog/{schema,ids,read,load,visible}.ts`: Zod 4.6.7 with §5.10's `superRefine` list; `read.ts` (scripts, tests) and `load.ts` (`server-only`, the app) per §7.3; `visible.ts` per §7.2.
- `catalog/src/*.json` from §5.2–5.7: colours from the §5.2 table (approx hex + tag); blanks = the 20 year-one ProductKeys (`partner: "printful"`; 2XL+ base `null` [U], §5.3); all 58 listings with their §5.9 copy, 4 bundles, 11 collections, drops 0–12; `pricing-rules.json` (payment fee 2.9% + 30¢ [S] per §5.3, mock shipping 475/220, floors, Private −600, codes excluding `margin_exception`); `transit.json` (`"US": null`, tag U); `cutoffs.json` (`[]`). `catalog/live/printful/` starts empty (`.gitkeep`); `snapshotDate` = the latest seed `checkedAt` (2026-11-10), never the wall clock.
- `art/designs/designs.json` (30 entries: text exact from §6.4.7–6.4.8, products from §5.4, clearance tag U) and `content/print-lines.json`.
- `art/print/plan.ts` `printFileIdsFor(variant)`; deterministic `Mockup[]` paths (§6.8); `scripts/catalog/{build,pull,margins,export-shopify}.ts`.
- **Tote default** (its $25.75 high base fails `entry`): keep $30; add `D24-EC80` and `D26-EC80` to `margin-exceptions.json` with `"approvedBy": "pending"`; ask the founder in the M4 status (§2 decision 24). `pending` passes only on `launch: false` listings; D7 lists every pending exception; codes never apply to a margin-exception listing.
- Tests: `catalog-schema`, `catalog-ids`, `catalog-margins` (§5.3: nulls → U36, sensitivity warnings), `pricing`, `shipping`, `drops`, `collections`, `launch-set` (incl. persona coverage), `catalog-audience`, `designs` (print-lines coverage, the `names` scope and the §6.4.4 garment bans) and `tests/types/schema-matches.test-d.ts`. Extend `banned-words` and `copy-lint` over `catalog/src/*.json` and every `content/*.json`.

**Acceptance** (each number is asserted by a test)
- [ ] 58 listings; `launch: true` on exactly the 16 §5.5 IDs; 575 launch SKUs (561 tee/fleece); 1,901 by year end; max 84 variants, none > 100; 17 three-tier listings.
- [ ] Every SKU matches `SKU_RE` and equals `skuFor()`. Contribution: `D01-Q-CC17-IVR-M` 1612, `D01-P-CC17-IVR-M` 1030, `D02-L-BC30-VWH-M` 1295.
- [ ] Shipping: 7499 → charged, 7500 → free, 8000 at −10% (7200) → charged. Every drop date is a Tuesday; no black garment codes; ≥ 50% neutral new garment colours per drop.
- [ ] The staged re-run leaves `catalog.json` unchanged. The CSV has 575 rows, `Status` = `draft`, `Published` = `FALSE`, empty compare-at; the margins CSV has one row per SKU. `export:shopify` exits 1, and every blocker it lists maps to an Appendix B row.

```bash
npm run catalog && git add catalog/catalog.json && npm run catalog && git diff --exit-code catalog/catalog.json
npm run test:unit && npm run catalog:pull
npm run export:shopify; echo "exit $?"   # 1 expected in the prototype: read the blocker list
```

#### M5 · Launch art D01–D13: print files, mockups, OG, sample plan (D2 + D4 for the launch set)
**Read first:** §5.5 · §6.3–§6.8 · A.8 · A.11 · A.13 · §7.10 (OG row) · §8.4 (round 1, `golive/sample-rounds.json`)
**Tasks**
- `art/designs/{types,index}.ts`, `shared/label.ts` (`label.whisper`) and `D01.ts`–`D13.ts` per §6.4.7. Build in this order, which proves every recipe early: D13 → D01 → D04 (GARMENT-FILL on Bay) → D03 (DARK) → D08 A/B (right chest, edge bleed) → D02 → D06 → D05 → D09 (seal ×0.95) → D10 (embroidery) → D11 → D12 → D07.
- `scripts/art/render-print.ts` (§6.5). Add the per-design mode to `contact-sheets.ts`; run `npm run art:sheets` and Read every sheet and 1:1 crop per §6.7 (one `art/REVIEW.md` row per design; ≤ 3 fix rounds, then a founder item).
- Mockups: `art/mockups/templates/{tee,crewneck,hoodie,dad_hat,sticker,sticker_sheet,water_bottle}.ts`, `flatlay.ts` (A.13), `og.ts`, `scripts/art/render-mockups.ts`; views per §6.8. OG images per §7.10: each launch handle, `site`, 11 collections, 7 crew, `send-a-bel`.
- Samples: `golive/sample-rounds.json` (§8.4 shape; round 1 = the 14 pieces + stickers, garments in M, one-size `OS`) and `scripts/golive/sample-plan.ts`; run `npm run golive:samples` for the founder's 18–20 Nov review.
- Once the founder's Printful account exists (§0, by Tue 17 Nov), run the §6.3.4 paste procedure for every round-1 placement (the bottle wrap decides §2 decision 31). If it can't be done before round 1, list those specs in the M5 status as "sampled on an unverified placement".
- Tests: `designs.test.ts` render part (§6.4.3 checks on every design registered in `art/designs/index.ts`; each unregistered D14–D30 entry is an `it.todo` until M8) · `listing-ready`'s `public/` audit (every image under `public/` is a generated mockup, OG or brand file) · `tests/integration/print-determinism.test.ts` (5 fixed launch ids).

**Acceptance**
- [ ] `validate:print -- --scope launch` exits 0: 0 `fail`. A `warn` is allowed only for an unverified or provisional spec, or a [U] garment hex.
- [ ] Every `printFileIds` entry of every launch variant is in the manifest, including the D13 default labels and a Private label for every tee design. The §8.4 round-1 pieces all pass.
- [ ] The staged re-run leaves `print-files/manifest.json` unchanged, and the determinism test passes.
- [ ] Every launch `Mockup.src` exists with its 960/480/AVIF siblings; each 1440 WebP ≤ 120 KB (target ≤ 60 KB), each 480 ≤ 45 KB; each OG image is 1200 × 630 and ≤ 300 KB. `art/REVIEW.md` has rows D01–D13.
- [ ] `exports/sample-plan.csv` round 1 holds exactly the 14 pieces + stickers of §8.4, costed from `catalog.json` (≈ $285 base for products and labels).

```bash
npm run art:print -- --scope launch && git add print-files/manifest.json && npm run art:print -- --scope launch && git diff --exit-code print-files/manifest.json
npm run validate:print -- --scope launch && npm run art:sheets && npm run mockups -- --scope launch
npx vitest run tests/integration/print-determinism.test.ts tests/unit/listing-ready.test.ts
npm run golive:samples && cat exports/sample-plan.csv
```

#### M6 · Storefront core (D5, part 1; closes D1)
**Read first:** §4.4 (example lines) · §4.5 (UI map, type scale, motion) · §4.8 #6–#7 · §5.6–§5.9 · §7.2–§7.7 · §7.9–§7.12 · §7.14–§7.15 · the §7.5 pages built in M6
**Tasks**
- Shell (§7.4, §7.6: DemoBar … `StoreHydrator`), `lib/{flags,site,storage,storage-registry,analytics}.ts`, Tailwind tokens (§7.7), fonts via `next/font/local`.
- Commerce (§7.9): `lib/commerce/types.ts` and `pricing.ts` verbatim, `codes.ts`, the `MockCommerceAdapter` (`priceCart()` never discounts a margin-exception listing), the throwing `shopify/` stub plus its README, and stores `cart`, `checkout`, `orders`, `codes` and `prefs`, each with `migrate()`.
- Routes: `/`, `/shop/`, `/collections/[handle]/` (11), `/products/[handle]/`, `/bundles/[slug]/`, `/crew/` + 7 × `/crew/[id]/`, `/cart/` + drawer, `/checkout/{contact,shipping,review}/`, `/order/`, `/size-guide/`, `/shipping/` and `/returns/` (data blocks until M9), `/faq/`, `/about/` (manifesto verbatim), `/contact/`, `/brand/` (D1 guide), 404, `sitemap.ts`, `robots.ts`, `manifest.ts` and `catalog-index.json`. SEO and JSON-LD per §7.10; a11y per §7.11; `lighthouserc.json` per §7.12.
- `scripts/site/{scan-built-html,route-manifest,check-bundle,screens}.ts`. Stub every M7 route with the `NotOpenYet` panel (§7.4), so links and the route manifest resolve.
- Tests: unit `listing-ready`, `visible`, `delivery`, `codes`, `migrations`, `tokens-usage`, `storage-registry`, `copy-placeholders`, `commerce.contract`, `analytics` (no network), `cast-component` (`<CastMember>` vs the A.5 fixture), `no-countdown`; the ESLint rule against `cookies()`/`headers()`; e2e flows 1–5, 7, 13, 16, 17, 18; a11y on every M6 route + the §7.14 states; `tests/integration/rename.test.ts` (§10.2).
- `npm run screens`; Read the PNGs (§7.14 screenshot review).

**Acceptance**
- [ ] `npm run ci -- --art-scope launch` passes steps 1–16 (`test:club` is skipped until M7).
- [ ] Listed flows pass on all 6 projects; axe finds 0 violations; requests are same-origin only; `context.cookies()` is empty.
- [ ] Budgets: first-load JS ≤ 170 KB and HTML ≤ 60 KB gzip; hero ≤ 120 KB. LHCI on the 9 §7.12 URLs: Performance ≥ 0.90, Accessibility = 1, Best Practices ≥ 0.95, LCP ≤ 2.5 s, CLS ≤ 0.05, TBT ≤ 200 ms; SEO ≥ 0.90 only on the 7 indexable ones.
- [ ] Rename test passes for Gymlings and Huddlebell. "Demo checkout: no payment is taken." shows on all 3 steps, and there are no payment-like inputs.

```bash
npm run ci -- --art-scope launch && cat artifacts/ci-summary.md
npm run screens && ls artifacts/screens | wc -l
```

#### M7 · Community, content pages, waitlist and club mode (D5, part 2)
**Read first:** §4.8 · §7.5 (Quiz → Waitlist, 404) · §7.8 · §7.13 · §7.14 flows 6, 8–12, 14, 15 · §7.15 · §8.1 (launch architecture, club mode) · §8.2 steps 3 and 22 · §9.5
**Tasks**
- `lib/community/stamps.ts` verbatim (§7.8), plus `firsts`, `quiz`, `crews`, `cheers`, `ecard` and `moderation`. Stores `stamps`, `firsts`, `quiz`, `cheers` and `crews`, each with `migrate()`.
- Routes: `/quiz/`, `/stamp-card/`, `/firsts/`, `/cheer-wall/` (demo), `/start-a-crew/` + `join/`, `/send-a-bel/` + `card/`, `/bring-a-buddy/`, `/first-visit-plan/`, `/club-rules/`, `/waitlist/`, `/privacy/` and `/terms/` (data blocks plus the draft banner until M9), and `/your-data/`.
- Content: the quiz (§7.5 table), ≥ 8 cheer-wall seeds (`sample: true`), demo crew members, club rules, the First Visit Plan and FAQ. Log the milestone-sticker mapping (§7.5) in `docs/decisions.md`. Wire `features.waitlist` `"demo"`, `?preview=waitlist` and `sf.preview`.
- **Club mode** exactly as §7.3 specifies (`build:club`; §8.1, §9.5): no DemoBar or cart/checkout; buy links and form posts to `https://{domain}`; live codes in `<code>` (copy-lint per §4.4); the cookie-free counter at `NEXT_PUBLIC_ANALYTICS_HOST` (§7.13; unset in tests), added to CSP by `write-headers.ts` only in club mode. Write `scripts/site/check-club.ts` (`test:club`, §10.2).
- Tests: unit `stamps` (200 seeded runs × 300 ops), `quiz`, `moderation`, `migrations` (every store), `readability` (Flesch-Kincaid ≤ 7 on `content/` long-form, warn only; §4.4), and the cheer-wall-off test (renders the route with `flags={cheerWall:'off'}` via `lib/flags.ts`'s test seam); e2e flows 6, 8–12, 14, 15; a11y on every route plus the quiz-result state.

**Acceptance**
- [ ] All 18 e2e flows pass on 6 projects, and axe finds 0 violations on every manifest route and state.
- [ ] No DOM text matches `/streak|missed|broke/i`, and no component is named `Streak`, `Missed` or `Rank`. Under reduced motion, 0 animations last > 1 ms.
- [ ] Every quiz result shows ≥ 2 visible products at `AS_OF` 2027-01-05. `/send-a-bel/` JS is ≤ 200 KB, and the card PNG is 1200 × 630. With `cheerWall: "off"`, the page shows "Not open yet".
- [ ] `test:club` passes with waitlist `"on"` and `"off"`; `scan:html` accepts every `<code>`.

```bash
npm run ci -- --art-scope launch && npm run screens
```

#### M8 · Year-one designs D14–D30 (D2 + D4 complete)
**Read first:** §5.4 (D14–D30 rows) · §5.6 · §6.3.3–§6.3.4 · §6.4.8 · §6.7–§6.8 · A.12 · §8.4 (rounds 2–3)
**Tasks**
- `D14.ts`–`D30.ts` per §6.4.8, **round-2 designs first** (D14–D18 and D21; round 2 is ordered by ~Tue 8 Dec), then the rest:
  - AOP tiles (D16, D21, D23) with the A.12 overlap and seam validators at the fixed 6 in scale, on the single provisional canvas until per-size templates exist.
  - D15 as embroidery Mallow.
  - D27 and D28 as `perOrderTemplate` previews: crew name "your crew", the year of `AS_OF`, month "jan".
  - D24's "×" glyph check, and D17 LIGHT drawn with the DARK geometry in `ink`.
- The remaining §6.8 mockup templates (joggers, leggings, sports bra, shorts, socks, beanie, patch, tote, towel, notebook).
- `npm run art` (scope `all` from now on). Read every new sheet against §6.7 (D16, D21, D23, D29 misreads). Build preview sites at later `NEXT_PUBLIC_AS_OF` dates.

**Acceptance**
- [ ] From here on, `npm run ci` with no flags passes. All 30 designs are registered (no `it.todo` left in `designs.test.ts`); the manifest holds every id the catalog needs, with 0 `fail`; the staged re-run leaves it unchanged.
- [ ] Every stretch file has no text and 100% coverage. `INT` appears only on socks; no D16 moon is `butter`; D21 has no dark ground.
- [ ] Gated listings (leggings `squat_test`, `D27-G185` while crews ≠ on) are hidden in every build, but their files and mockups exist. The 2027-12-07 preview build has no missing image.

```bash
npm run art:print && git add print-files/manifest.json && npm run art:print && git diff --exit-code print-files/manifest.json
npm run art && npm run ci
NEXT_PUBLIC_AS_OF=2027-12-07 npm run build && npm run scan:html && npm run check:bundle
env -i PATH="$PATH" HOME="$HOME" npm run build
```

#### M9 · Go-live kit, theme kit, final report (D6 + D7)
**Read first:** §8 · §9 · §5.10 (Printful mapping) · §6.3.2 (thread map) · §10.4–§10.6 · Appendix B
**Tasks**
- Printful sync per §8.3: `golive/printful-sync.ts`, `golive/lib/{printful,plan,diff,limiter}.ts`; `golive/state/printful-map.json` starts as `{ "version": 1, "products": {} }`. Placements per §5.10 "Printful mapping": chest and back-neck files are full canvases, **no API offset**.
- Tests: `tests/unit/golive-printful-{plan,diff,safety,idempotent}.test.ts` against the in-memory fake Printful (`tests/fixtures/`).
- Drafts: `golive/policies/*.md` (§8.5 returns; shipping A + fallback B; privacy lists the `lib/storage-registry.ts` keys, no cookies, 13+) · `golive/legal/*.md` · `golive/README.md` (§8.2 steps 1–22 + §9.3 as [C]/[F]/[C→F] checkboxes) · `golive/qa-checklist.md` (§8.4: 11 checks × round-1 pieces + shot list) · `golive/dashboard/weekly.csv` (exact §9.8 header + one example row) · `docs/90-day-review.md` (template).
- **Theme kit** `golive/theme/` exactly as §8.2 step 16 lists it: `npm run brand` now also writes `assets/brand-tokens.css` (committed); add `assets/brand-fonts.css`, the four `snippets/*.liquid` (`{brand}` → `{{ shop.name }}`) and `README.md` (Edit code steps; Style = Option1, Quiet first).
- Copy: `content/cs-macros.json` (M1–M10), `content/emails.json` (§9.6), `content/social.json` (7 Meet the Machine + 6 crew skits, §9.2). Run `npm run golive:policies`. `/shipping/`, `/returns/`, `/privacy/`, `/terms/` now render the drafts in `data-copy-surface="legal"` (§4.4) under "Draft for legal review. Not legal advice."
- Write `REPORT.md` from §10.6.

**Acceptance**
- [ ] Safety tests prove §8.3 rules 1–5: no `fetch` without `--live`; `--live` is GET-only (+ shipping rates); denylisted order calls throw before sending; orphans are never deleted; a second `--apply` makes 0 writes.
- [ ] `golive:printful` (offline) prints the §8.3 diff format. In the prototype it exits 2 (blocked files) and `export:printful` exits 1, after writing both files. Every blocker is an unverified or provisional spec listed in Appendix B.
- [ ] Theme kit: every file exists; no brand literal; its copy passes banned-words and copy-lint; `brand-tokens.css` survives the staged re-run of `npm run brand`. `shopify theme check` runs offline if `@shopify/cli` (pin ≥ 14 days old) installs; otherwise it is listed as untested in D7.
- [ ] `exports/policies/` has no unfilled `{…}` except TBC [U] values. Banned-words and copy-lint cover the three new content files.
- [ ] `npm run ci` passes with **no skipped step**. Every box in `docs/progress.md` is ticked, and REPORT.md is complete.

```bash
npx vitest run tests/unit/golive-printful-*.test.ts
npm run export:printful; echo "exit $?"; npm run golive:printful; echo "exit $?"
npm run brand && git add -A golive/theme && npm run brand && git diff --exit-code golive/theme
npm run golive:policies && npm run ci && cat artifacts/ci-summary.md
```

### 10.4 Whole-project definition of done

Tick each box only with evidence produced in this session (§3 rule 21).
- [ ] **Fresh clone:** `git clean -xdf && npm ci && npm run ci` passes with no skipped step, and `artifacts/ci-summary.md` is pasted into REPORT.md.
- [ ] **D1–D7:** every §1 "Done means" criterion, each with evidence from this session.
- [ ] **Determinism:** the staged re-runs of `brand`, `catalog` and `art:print` (M1, M4, M8) leave `git diff` empty.
- [ ] **Safety:** the secrets grep is clean, `.env.example` holds names only, no real key or token was used, and no order was confirmed or paid.
- [ ] **Hygiene:** the name grep, hex grep and pins test pass; `licenses/fonts.json` hashes match; shipped licences are allowed.
- [ ] **Honesty:** REPORT.md lists every Appendix B row with a status (open / confirmed / changed), every untested item as **untested**, and every blocked host. `docs/decisions.md` lists every default, deviation and section conflict.

### 10.5 Blocker protocol

Never stop the whole build for one blocker: do the "Do" column, log it in `docs/decisions.md`, carry on. D7 records each case with its evidence (host + command + error; pin vs installed; skipped projects as **untested**; founder items with sheet paths; before/after numbers).

| Situation | Do | Never |
|---|---|---|
| A host blocked or failing (§3 rule 7; also a CDN) | Retry once, then use the brief's fallback and keep its tag (`null` + [U] if none) | Fabricate a response; change a tag to V/T without a source |
| npm pin missing, yanked or not installable | Nearest older release ≥ 14 days old; re-run M0's checks | `latest`, alpha/beta/rc, `^`/`~` |
| A dependency's API differs from the brief | Read its changelog or `node_modules` docs; adapt, keeping the brief's behaviour and tests | Delete or weaken a test |
| Playwright browsers or LHCI's Chrome won't install | Run the projects that work; LHCI: `CHROME_PATH` = Playwright's Chromium | Report a skipped project as passed |
| A spec is [U] (canvas, art box, placement, hex, size range, chart) | Keep the seed, `verified: false` / tag U (and its Appendix B row); `validate:print` warns; exporters block it | Flip `verified` without a template or live response |
| Art misreads (§4.7, §6.7) or fails a minimum | §6.7 fix levers; long text → the brief's fallback (whisper "(psst. that counts.)", D24's short receipt); after 3 rounds, drop that placement (founder item) | Lower a minimum; ship a doubtful silhouette |
| An a11y contrast or axe failure | Switch to an allowed §4.5 pair (`ink` on `oat` is always safe); fix the markup | Edit `tokens.json`, the contrast table or the axe tags |
| A cleared line fails banned-words or copy-lint | Stop using it and ask the founder (§3 rule 10); rewrite your own new copy | Edit `banned-words.json` or the allowlist yourself |
| A §7.12 budget is missed | Server components, split islands, re-encode images, trim per-variant JSON-LD | Remove required content; raise a budget |
| Determinism breaks (re-run diff) | Find the timestamp, unseeded RNG, unsorted map or tool drift | Commit the noisy diff |
| Session ends or the container restarts | Resume from `git log` and `docs/progress.md` at the first unticked task | Redo committed milestones |

### 10.6 Final report template (`REPORT.md`, D7)

REPORT.md has exactly these sections, in order, each a `##` heading (shown as `R1`–`R13` so they can't be confused with this brief's headings); it may use the brand name (§4.1). Start it with: `Final report · built <dates> · Node <version> · commit <sha> · brief dated 2026-11-10`.

| # | REPORT.md section | Content |
|---|---|---|
| R1 | Summary | 5 lines: what works, what doesn't, what the founder does next |
| R2 | Deliverables | Per D1–D7: done / partial / not done · evidence (command + result) · where |
| R3 | How to run | `npm ci` · `npm run build:full` · `npm run preview` → http://localhost:4173 · `npm run ci` |
| R4 | Versions installed | package · brief pin · installed · why different |
| R5 | Verification results | `artifacts/ci-summary.md` plus the real output of every verify block; no paraphrase |
| R6 | Visual reviews | `art/REVIEW.md` summary (sheets, problems fixed, open founder items) and the screens reviewed |
| R7 | Numbers | listings 58 · launch SKUs `<n>`/575 · print files pass / warn / 0 fail · mockups · budgets (measured vs limit) |
| R8 | Founder decisions used | §2 # · default or override · where it lives; every `pending` margin exception |
| R9 | Open verification items | Every Appendix B row: status · who · next step · what it blocks |
| R10 | Blocked hosts and failures | host · command · error · fallback used |
| R11 | Untested | each item and why |
| R12 | Deviations and section conflicts | from `docs/decisions.md` |
| R13 | Founder next steps, dated | §0 + `golive/README.md`: trademark, domain, accounts, samples ~23 Nov, QA, lawyer, launch Tue 5 Jan 2027 |

### 10.7 What NOT to do

All §3 rules apply; in addition:
- Don't start D14–D30 before M7 passes. Don't use `--art-scope launch` from M8 on.
- Don't add a dependency outside §7.1 and §6.1 without a log line (licence, age ≥ 14 days, why). No UI kits, CSS-in-JS, `next/font/google` or Stripe.
- Don't put black garments, 3D puff, unlimited-colour thread, Printify items or leggings without a passed squat test into any launch export.
- Don't loosen a test, budget, minimum or banned-word rule to get green. Fix the cause, or log a blocker (§10.5).

---

## Appendix A. Reference code (tested snippets)

A.3, A.5 and A.6 back §4; A.7–A.13 back §6 (the gaps in the numbering are intentional: the mini-Bel, icon and static Bel snippets were retired because A.5's `miniBel()`, `iconMark()` and `bel()` generate them). All were run on 2026-11-10 [L]. `crew-kit.mjs` (A.5; `opentype.js@2.0.0`, `@resvg/resvg-js@2.6.2`, Node 22) reproduces our reference renders **byte for byte** (cast, 10 expressions, poses, dark-garment sheet, primary wordmark, 240 icon). Port it to TypeScript under `art/`, colours from `art/palette.ts`.

**A.7–A.13 (print-pipeline code).** Run with Node 22.23.4, `sharp@0.35.5`, `@resvg/resvg-js@2.6.2`, `opentype.js@2.0.0` and A.5 [L]. Port each to the path in its heading, changing only types and imports (`./color.mjs`, `./inspect.mjs`, `./crew-kit.mjs` → the ported modules). **No hex literals** (§4.5 grep rule): callers pass colours from `art/palette.ts` and `print-specs.json`; hexes in the notes are test fixtures.

### A.3 Favicon ("Bel peek", 48 grid)

Legible at 32 and 48 px, passable at 16 px [L]. Below 32 px, drop the final smile path.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">
  <rect width="48" height="48" rx="11" fill="#FFF7EC"/>
  <path d="M14 26 C12 7 36 7 34 26" fill="none" stroke="#22263A" stroke-width="9" stroke-linecap="round"/>
  <path d="M14 26 C12 7 36 7 34 26" fill="none" stroke="#FF8A65" stroke-width="3.5" stroke-linecap="round"/>
  <path d="M24 18 C40 18 47 30 47 42 L47 48 L1 48 L1 42 C1 30 8 18 24 18 Z" fill="#FF8A65" stroke="#22263A" stroke-width="3" stroke-linejoin="round"/>
  <ellipse cx="17" cy="33" rx="3.3" ry="4.3" fill="#22263A"/><ellipse cx="31" cy="33" rx="3.3" ry="4.3" fill="#22263A"/>
  <path d="M20.5 39.5 Q24 42.5 27.5 39.5" fill="none" stroke="#22263A" stroke-width="2.4" stroke-linecap="round"/>
</svg>
```

### A.5 `crew-kit.mjs`: characters, face kit, poses, text-to-path, auto-fit, sticker border, wordmark, icon

**Fixtures:** run `node crew-kit.mjs` once (a few lines that write `svgDoc()` of `bel()`, `iconMark()` and each `miniBel()` mode) and commit `tests/fixtures/{bel-happy-idle,icon,minibel-color,minibel-reverse,minibel-solid}.svg`; the TS port must match them byte for byte.

**Verified [L]:** wordmark "kettlekin" at S = 200 measures `widthEm 4.743`, `stemCxEm 3.885`, `bellAboveBaselineEm 0.730`; `fitText('cap', s, 164, 28, 9)` passes "you went." (x-height 14.0) and "okay. we're in." (9.6) and throws, as designed, for "long time no gym." (7.8) and "the hard part was the door." (5.1); `wordmark('huddlebell', …)` returns `stem: null` (use the horizontal lockup), `wordmark('gymlings', …)` finds the stem.

```js
// crew-kit.mjs (reference). The TS port imports colours from art/palette.ts instead of the C literal below.
// All geometry is on the 240-unit grid: viewBox 0 0 240 240, ground line y=216, centre x=120.
import fs from 'node:fs';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const opentype = require('opentype.js');

export const C = { // mirror of brand/tokens.json (illustration subset)
  ink: '#22263A', oat: '#FFF7EC', white: '#FFFFFF', coral: '#FF8A65', lilac: '#CDB9F2', lilacShade: '#B8A0EA',
  bubblegum: '#FFB3C9', butter: '#FFD86E', sage: '#A9BCA2', pool: '#8BD7E6', pistachio: '#B9E3A3',
};
export const SW = 6;  // master outline
export const FSW = 5;  // face strokes
export const O = (ln = C.ink) => `stroke="${ln}" stroke-width="${SW}" stroke-linejoin="round" stroke-linecap="round"`;

// Outlined tube (arms, handles, rails): ink at core+12 underneath, fill colour at core on top.
export const tube = (d, fill, core = 8, ln = C.ink) =>
  `<path d="${d}" fill="none" stroke="${ln}" stroke-width="${core + 2 * SW}" stroke-linecap="round" stroke-linejoin="round"/>` +
  `<path d="${d}" fill="none" stroke="${fill}" stroke-width="${core}" stroke-linecap="round" stroke-linejoin="round"/>`;
export const hand = (x, y, fill, ln = C.ink) =>
  `<circle cx="${x}" cy="${y}" r="8" fill="${fill}" stroke="${ln}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>`;

// Sneaker: identical on every character, drawn last. flip=false -> toe points left (s=-1).
export const sneaker = (cx, accent, ln = C.ink, flip = false) => {
  const s = flip ? 1 : -1, heel = cx - 18 * s, toe = cx + 22 * s;
  return `<path d="M${heel} 216 L${heel} 205 C${heel} 198 ${heel + 5 * s} 194 ${heel + 13 * s} 194 C${cx + 4 * s} 194 ${cx + 8 * s} 199 ${cx + 13 * s} 202 C${toe - 2 * s} 204 ${toe} 207 ${toe} 211 L${toe} 216 Z" fill="${C.oat}" stroke="${ln}" stroke-width="5" stroke-linejoin="round"/>` +
    `<line x1="${heel + 2 * s}" y1="210.5" x2="${toe - 2 * s}" y2="210.5" stroke="${accent}" stroke-width="4"/>` +
    `<line x1="${cx - 2 * s}" y1="198" x2="${cx + 3 * s}" y2="201" stroke="${ln}" stroke-width="3" stroke-linecap="round"/>`;
};
export const feet = (l, r, accent) => sneaker(l, accent) + sneaker(r, accent, C.ink, true);

// ---------- face kit: 10 expressions; blush is an emotion, not makeup ----------
export const EXPRESSIONS = ['happy', 'nervous', 'proud', 'sleepy', 'hyped', 'surprised', 'determined', 'shy', 'chill', 'trying'];
const BLUSH_EXPR = new Set(['shy', 'proud', 'hyped', 'nervous']);
export function face({ fx, fy, gap = 22, expr = 'happy', blush = C.bubblegum, ln = C.ink }) {
  const L = fx - gap, R = fx + gap, by = fy - 19;
  const st = (w = FSW) => `stroke="${ln}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round" fill="none"`;
  const ovalEye = (x, y, lookX = 0) => `<ellipse cx="${x + lookX}" cy="${y}" rx="7" ry="9.5" fill="${ln}"/><circle cx="${x + lookX - 2.5}" cy="${y - 3.5}" r="2.6" fill="${C.white}"/>`;
  const brow = (x, y, tilt, side) => { // + tilt = inner end down (determined), - = inner end up (worried)
    const inner = side === 'L' ? x + 7 : x - 7, outer = side === 'L' ? x - 7 : x + 7;
    return `<line x1="${outer}" y1="${y - tilt}" x2="${inner}" y2="${y + tilt}" ${st()}/>`;
  };
  const sweat = (x) => `<path d="M${x} ${fy - 22} q-6 9 0 12 q6 -3 0 -12 z" fill="${C.pool}" stroke="${ln}" stroke-width="3.5" stroke-linejoin="round"/>`;
  const cheeks = BLUSH_EXPR.has(expr) ? `<ellipse cx="${L - 12}" cy="${fy + 13}" rx="8" ry="5" fill="${blush}"/><ellipse cx="${R + 12}" cy="${fy + 13}" rx="8" ry="5" fill="${blush}"/>` : '';
  const E = {
    happy: () => ovalEye(L, fy) + ovalEye(R, fy) + brow(L, by, 0, 'L') + brow(R, by, 0, 'R') + `<path d="M${fx - 9} ${fy + 12} Q${fx} ${fy + 21} ${fx + 9} ${fy + 12}" ${st()}/>`,
    nervous: () => ovalEye(L, fy) + ovalEye(R, fy) + brow(L, by, -3.5, 'L') + brow(R, by, -3.5, 'R') + `<path d="M${fx - 10} ${fy + 16} q3.3 -4 6.6 0 t6.6 0 t6.6 0" ${st()}/>` + sweat(R + 26),
    proud: () => `<path d="M${L - 8} ${fy + 2} Q${L} ${fy - 9} ${L + 8} ${fy + 2}" ${st()}/><path d="M${R - 8} ${fy + 2} Q${R} ${fy - 9} ${R + 8} ${fy + 2}" ${st()}/>` + brow(L, by, 2, 'L') + brow(R, by, 2, 'R') +
      `<path d="M${fx - 10} ${fy + 12} Q${fx} ${fy + 22} ${fx + 10} ${fy + 12} Z" fill="${ln}" stroke="${ln}" stroke-width="3" stroke-linejoin="round"/>`,
    sleepy: () => `<path d="M${L - 8} ${fy} Q${L} ${fy + 7} ${L + 8} ${fy}" ${st()}/><path d="M${R - 8} ${fy} Q${R} ${fy + 7} ${R + 8} ${fy}" ${st()}/>` + `<ellipse cx="${fx}" cy="${fy + 15}" rx="4" ry="5" fill="${ln}"/>`,
    hyped: () => `<path d="M${L - 8} ${fy + 3} L${L} ${fy - 6} L${L + 8} ${fy + 3}" ${st()}/><path d="M${R - 8} ${fy + 3} L${R} ${fy - 6} L${R + 8} ${fy + 3}" ${st()}/>` + brow(L, by - 4, -2, 'L') + brow(R, by - 4, -2, 'R') +
      `<path d="M${fx - 12} ${fy + 9} L${fx + 12} ${fy + 9} Q${fx + 12} ${fy + 24} ${fx} ${fy + 24} Q${fx - 12} ${fy + 24} ${fx - 12} ${fy + 9} Z" fill="${ln}" stroke="${ln}" stroke-width="3" stroke-linejoin="round"/><path d="M${fx - 6} ${fy + 20} Q${fx} ${fy + 16} ${fx + 6} ${fy + 20}" fill="none" stroke="${C.coral}" stroke-width="3" stroke-linecap="round"/>`,
    surprised: () => ovalEye(L, fy) + ovalEye(R, fy) + brow(L, by - 6, -1.5, 'L') + brow(R, by - 6, -1.5, 'R') + `<ellipse cx="${fx}" cy="${fy + 16}" rx="5.5" ry="7" fill="${ln}"/>`,
    determined: () => ovalEye(L, fy) + ovalEye(R, fy) + brow(L, by + 1, 3.5, 'L') + brow(R, by + 1, 3.5, 'R') + `<path d="M${fx - 9} ${fy + 14} Q${fx + 1} ${fy + 20} ${fx + 10} ${fy + 11}" ${st()}/>`,
    shy: () => ovalEye(L, fy, 4) + ovalEye(R, fy, 4) + brow(L, by, -2.5, 'L') + brow(R, by, -2.5, 'R') + `<path d="M${fx - 4} ${fy + 15} Q${fx + 1} ${fy + 18} ${fx + 6} ${fy + 15}" ${st()}/>`,
    chill: () => `<path d="M${L - 8} ${fy - 2} L${L + 8} ${fy - 2} A8 8 0 0 1 ${L - 8} ${fy - 2} Z" fill="${ln}" stroke="${ln}" stroke-width="4" stroke-linejoin="round"/><path d="M${R - 8} ${fy - 2} L${R + 8} ${fy - 2} A8 8 0 0 1 ${R - 8} ${fy - 2} Z" fill="${ln}" stroke="${ln}" stroke-width="4" stroke-linejoin="round"/>` +
      brow(L, by + 2, 0, 'L') + brow(R, by + 2, 0, 'R') + `<path d="M${fx - 8} ${fy + 15} Q${fx + 3} ${fy + 20} ${fx + 11} ${fy + 12}" ${st()}/>`,
    trying: () => ovalEye(L, fy) + ovalEye(R, fy) + brow(L, by, -2.5, 'L') + brow(R, by, -2.5, 'R') + `<ellipse cx="${fx}" cy="${fy + 16}" rx="7" ry="5" fill="${ln}"/>` + sweat(L - 26),
  };
  if (!E[expr]) throw new Error(`unknown expression ${expr}`);
  return cheeks + E[expr]();
}

// ---------- arm poses (shoulder-relative; right side mirrored) ----------
const idleL = ([x, y]) => `M${x} ${y} C${x - 14} ${y + 2} ${x - 22} ${y + 8} ${x - 26} ${y + 22} S${x - 26} ${y + 34} ${x - 20} ${y + 38}`;
const idleR = ([x, y]) => `M${x} ${y} C${x + 14} ${y + 2} ${x + 22} ${y + 8} ${x + 26} ${y + 22} S${x + 26} ${y + 34} ${x + 20} ${y + 38}`;
const upL = ([x, y]) => `M${x} ${y} C${x - 18} ${y - 6} ${x - 26} ${y - 24} ${x - 22} ${y - 46}`;
const upR = ([x, y]) => `M${x} ${y} C${x + 18} ${y - 6} ${x + 26} ${y - 24} ${x + 22} ${y - 46}`;
export const armsIdle = (f, l = [62, 150], r = [178, 150]) => tube(idleL(l), f) + hand(l[0] - 18, l[1] + 40, f) + tube(idleR(r), f) + hand(r[0] + 18, r[1] + 40, f);
export const armsWave = (f, l = [62, 150], r = [178, 146]) => tube(idleL(l), f) + hand(l[0] - 18, l[1] + 40, f) + tube(upR(r), f) + hand(r[0] + 22, r[1] - 50, f) +
  `<path d="M${r[0] + 40} ${r[1] - 66} q6 -4 10 2 M${r[0] + 44} ${r[1] - 52} q7 -1 9 6" fill="none" stroke="${C.ink}" stroke-width="4" stroke-linecap="round"/>`;
export const armsCheer = (f, l = [62, 146], r = [178, 146]) => tube(upL(l), f) + hand(l[0] - 22, l[1] - 50, f) + tube(upR(r), f) + hand(r[0] + 22, r[1] - 50, f);
const sparkle4 = `<path d="M30 70 l4 10 l10 4 l-10 4 l-4 10 l-4 -10 l-10 -4 l10 -4 z M206 62 l3 7 l7 3 l-7 3 l-3 7 l-3 -7 l-7 -3 l7 -3 z" fill="${C.butter}" stroke="${C.ink}" stroke-width="3.5" stroke-linejoin="round"/>`;

// ---------- characters ----------
export const BEL_BODY = 'M120 82 C168 82 192 118 190 156 C189 180 178 198 160 204 L80 204 C62 198 51 180 50 156 C48 118 72 82 120 82 Z';
export const bel = ({ expr = 'happy', pose = 'idle', fy = 150 } = {}) => {
  const f = C.coral;
  const arms = pose === 'wave' ? armsWave(f) : pose === 'cheer' ? armsCheer(f) : pose === 'none' ? '' : armsIdle(f);
  return arms + tube('M86 112 C80 44 160 44 154 112', f, 16) + `<path d="${BEL_BODY}" fill="${f}" ${O()}/>` +
    face({ fx: 120, fy, expr }) + (pose === 'none' ? '' : feet(98, 142, C.pool));
};
export const mallow = ({ expr = 'sleepy', zz = true } = {}) => {
  let top = 'M46 118';
  for (let x = 58; x <= 166; x += 27) top += ` L${x} 118 a7 7 0 0 1 14 0`;  // 5 grip nubs
  return `<path d="${top} L190 118 L190 204 L46 204 Q34 204 34 192 L34 130 Q34 118 46 118 Z" fill="${C.lilac}" ${O()}/>` +
    `<ellipse cx="190" cy="161" rx="20" ry="43" fill="${C.lilacShade}" ${O()}/>` +  // end face
    `<ellipse cx="190" cy="161" rx="7" ry="16" fill="${C.oat}" stroke="${C.ink}" stroke-width="4"/>` +  // hollow core
    `<path d="M60 128 V194 M150 128 V194" stroke="${C.ink}" stroke-width="4" stroke-linecap="round"/>` + // grooves
    face({ fx: 105, fy: 158, gap: 21, expr }) + feet(80, 136, C.butter) +
    (zz ? `<path d="M176 76 h12 l-12 13 h12 M196 58 h9 l-9 10 h9" fill="none" stroke="${C.ink}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>` : '');
};
export const gus = ({ expr = 'chill', pose = 'idle' } = {}) => {
  const f = C.sage;
  return (pose === 'wave' ? armsWave(f, [44, 156], [196, 152]) : armsIdle(f, [44, 156], [196, 156])) +
    tube('M80 104 C80 52 160 52 160 104', C.coral, 9) +  // ONE handle
    `<rect x="104" y="50" width="32" height="18" rx="7" fill="${C.butter}" stroke="${C.ink}" stroke-width="5" stroke-linejoin="round"/>` + // grip wrap
    `<path d="M112 53 v12 M120 53 v12 M128 53 v12" stroke="${C.ink}" stroke-width="2.5" stroke-linecap="round"/>` +
    `<path d="M52 110 Q52 100 64 100 L176 100 Q188 100 188 110 L196 190 Q197 204 182 204 L58 204 Q43 204 44 190 Z" fill="${f}" ${O()}/>` +
    `<path d="M60 120 H180" stroke="${C.ink}" stroke-width="4" stroke-linecap="round" stroke-dasharray="1 8"/>` + // zipper
    `<rect x="168" y="113" width="10" height="16" rx="3" fill="${C.butter}" stroke="${C.ink}" stroke-width="3.5"/>` + // zip pull
    `<path d="M56 136 Q48 160 58 196 M184 136 Q192 160 182 196" fill="none" stroke="${C.ink}" stroke-width="4" stroke-linecap="round"/>` +
    face({ fx: 120, fy: 160, gap: 21, expr }) + feet(92, 148, C.coral);
};
export const roundedHex = (cx, cy, R, r = 9) => { // flat side down; corners rounded by Q through each vertex
  const V = [0, 60, 120, 180, 240, 300].map(a => [cx + R * Math.cos(a * Math.PI / 180), cy + R * Math.sin(a * Math.PI / 180)]);
  const t = r / R; let d = '';
  V.forEach((v, i) => {
    const p = V[(i + 5) % 6], n = V[(i + 1) % 6];
    const a = [v[0] + (p[0] - v[0]) * t, v[1] + (p[1] - v[1]) * t], b = [v[0] + (n[0] - v[0]) * t, v[1] + (n[1] - v[1]) * t];
    d += (i === 0 ? `M${a[0].toFixed(1)} ${a[1].toFixed(1)}` : ` L${a[0].toFixed(1)} ${a[1].toFixed(1)}`) + ` Q${v[0].toFixed(1)} ${v[1].toFixed(1)} ${b[0].toFixed(1)} ${b[1].toFixed(1)}`;
  });
  return d + ' Z';
};
export const pippop = ({ pipExpr = 'happy', popExpr = 'hyped' } = {}) => {
  const P = C.bubblegum, Q = C.butter, R = 48, cy = +(204 - R * Math.sin(Math.PI / 3)).toFixed(1); // 162.4
  const pip = `<path d="${roundedHex(58, cy, R)}" fill="${P}" ${O()}/>` + `<path d="M24 ${cy - 22} H92" stroke="${C.coral}" stroke-width="7"/>` + face({ fx: 58, fy: cy + 6, gap: 13, expr: pipExpr, blush: C.coral });
  const pop = `<path d="${roundedHex(182, cy, R)}" fill="${Q}" ${O()}/>` + `<path d="M148 ${cy - 22} H216" stroke="${C.pool}" stroke-width="7"/>` + face({ fx: 182, fy: cy + 6, gap: 13, expr: popExpr, blush: C.coral });
  const bar = `<rect x="96" y="${cy - 10}" width="48" height="20" rx="4" fill="${C.oat}" ${O()}/><path d="M110 ${cy - 7} v14 M120 ${cy - 7} v14 M130 ${cy - 7} v14" stroke="${C.ink}" stroke-width="2.5"/>`;
  const arms = tube(`M14 ${cy + 4} C2 ${cy - 8} 0 ${cy - 30} 8 ${cy - 46}`, P) + hand(9, cy - 50, P) + tube(`M226 ${cy + 4} C238 ${cy - 8} 240 ${cy - 30} 232 ${cy - 46}`, Q) + hand(231, cy - 50, Q);
  return arms + bar + pip + pop + sneaker(58, C.coral) + sneaker(182, C.pool, C.ink, true);
};
export const sip = ({ expr = 'hyped' } = {}) => armsCheer(C.pool, [88, 146], [152, 146]) + tube('M107 66 C105 38 135 38 133 66', C.butter, 8) +
  `<rect x="94" y="60" width="52" height="28" rx="9" fill="${C.butter}" ${O()}/>` +
  `<rect x="82" y="84" width="76" height="122" rx="28" fill="${C.pool}" ${O()}/>` +
  `<path d="M146 108 h8 M146 122 h8 M146 136 h8" stroke="${C.ink}" stroke-width="4" stroke-linecap="round"/>` +
  face({ fx: 116, fy: 150, gap: 16, expr }) + feet(100, 140, C.coral);
export const ollie = () => armsCheer(C.pistachio, [56, 144], [184, 144]) + // mouth = the plate hole; never changes
  `<circle cx="120" cy="138" r="70" fill="${C.pistachio}" ${O()}/>` +
  `<circle cx="120" cy="138" r="50" fill="none" stroke="${C.ink}" stroke-width="4"/>` +  // rim ring: plate, not donut
  `<ellipse cx="102" cy="114" rx="7" ry="9.5" fill="${C.ink}"/><circle cx="99.5" cy="110.5" r="2.6" fill="${C.white}"/>` +
  `<ellipse cx="138" cy="114" rx="7" ry="9.5" fill="${C.ink}"/><circle cx="135.5" cy="110.5" r="2.6" fill="${C.white}"/>` +
  `<line x1="94" y1="95" x2="108" y2="92" stroke="${C.ink}" stroke-width="5" stroke-linecap="round"/><line x1="132" y1="92" x2="146" y2="95" stroke="${C.ink}" stroke-width="5" stroke-linecap="round"/>` +
  `<circle cx="120" cy="140" r="13" fill="${C.ink}"/>` + feet(100, 140, C.coral) + sparkle4;
export const tuck = ({ expr = 'shy' } = {}) => tube('M40 70 H200', C.sage, 10) +  // rail
  `<path d="M80 80 Q80 62 98 62 L142 62 Q160 62 160 80 L162 186 Q162 196 152 196 L88 196 Q78 196 78 186 Z" fill="${C.oat}" ${O()}/>` +
  `<path d="M80 96 Q120 106 160 96" fill="none" stroke="${C.ink}" stroke-width="5" stroke-linecap="round"/>` +  // front-flap edge
  `<path d="M82 86 Q120 95 158 86" fill="none" stroke="${C.pool}" stroke-width="5" stroke-linecap="round"/>` +
  `<path d="M80 164 H160" stroke="${C.coral}" stroke-width="6"/><path d="M80 175 H160" stroke="${C.pool}" stroke-width="6"/>` +
  [86, 98, 110, 130, 142, 154].map(x => `<path d="M${x} 199 v8" stroke="${C.ink}" stroke-width="4" stroke-linecap="round"/>`).join('') + // terry fringe
  face({ fx: 120, fy: 128, gap: 15, expr }) +
  `<g transform="translate(0 8)">${sneaker(104, C.pool)}${sneaker(136, C.pool, C.ink, true)}</g>`;  // dangling, no hands

// ---------- text -> outlined paths (no <text>, no NaN; Caprasimo via charToGlyph) ----------
const loadFont = p => { const b = fs.readFileSync(p); return opentype.parse(b.buffer.slice(b.byteOffset, b.byteOffset + b.byteLength)); };
export const FONTS = {};
export function loadFonts({ caprasimoTtf, atkinson800Ttf }) { FONTS.cap = loadFont(caprasimoTtf); FONTS.atk = loadFont(atkinson800Ttf); }
const ser = cmds => cmds.map(c => c.type === 'M' || c.type === 'L' ? `${c.type}${c.x.toFixed(2)} ${c.y.toFixed(2)}`
  : c.type === 'Q' ? `Q${c.x1.toFixed(2)} ${c.y1.toFixed(2)} ${c.x.toFixed(2)} ${c.y.toFixed(2)}`
  : c.type === 'C' ? `C${c.x1.toFixed(2)} ${c.y1.toFixed(2)} ${c.x2.toFixed(2)} ${c.y2.toFixed(2)} ${c.x.toFixed(2)} ${c.y.toFixed(2)}` : 'Z').join('');
export function textPath(fontKey, str, size, x0, base, track = 0) {
  const f = FONTS[fontKey], gl = [...str].map(ch => f.charToGlyph(ch)); let x = x0, d = '';
  gl.forEach((g, i) => {
    d += ser(g.getPath(x, base, size).commands);
    x += g.advanceWidth * size / f.unitsPerEm + (i < gl.length - 1 ? f.getKerningValue(g, gl[i + 1]) * size / f.unitsPerEm + track * size : 0);
  });
  if (d.includes('NaN')) throw new Error('NaN in path for ' + str);
  return { d, width: x - x0 };
}
// AUTO-FIT: scale to <= 86% of the frame's inner width, cap at maxSize, FAIL if x-height < minXh (canvas units).
export function fitText(fontKey, str, frameW, maxSize, minXh) {
  const f = FONTS[fontKey], w1 = textPath(fontKey, str, 100, 0, 0).width;
  const size = Math.min(maxSize, 0.86 * frameW / (w1 / 100));
  const xh = f.tables.os2.sxHeight / f.unitsPerEm * size;
  if (xh < minXh) throw new Error(`FIT FAIL "${str}": x-height ${xh.toFixed(1)} < ${minXh}`);
  return { size, width: w1 * size / 100, xh };
}
// hold-sign pose: Bel, face raised, board in front; hands on the board's side edges, never over text.
export const belSign = (line, { expr = 'proud' } = {}) => {
  const f = C.coral, bx = 30, bw = 180, by = 168, bh = 36;
  const fit = fitText('cap', line, bw - 16, 28, 9);
  const t = textPath('cap', line, fit.size, 120 - fit.width / 2, by + bh / 2 + fit.xh / 2);
  return tube('M86 112 C80 44 160 44 154 112', f, 16) + `<path d="${BEL_BODY}" fill="${f}" ${O()}/>` + face({ fx: 120, fy: 136, expr }) +
    feet(98, 142, C.pool) + tube('M62 146 C44 150 30 164 32 180', f) + tube('M178 146 C196 150 210 164 208 180', f) +
    `<rect x="${bx}" y="${by}" width="${bw}" height="${bh}" rx="10" fill="${C.oat}" ${O()}/>` +
    `<path d="${t.d}" fill="${C.ink}"/>` + hand(31, 186, f) + hand(209, 186, f);
};

// ---------- dark-garment sticker border: oat copy, every stroke +16, unstroked shapes get a 16 stroke ----------
export const halo = (svg, add = 16) => svg.replace(/stroke-width="([\d.]+)"/g, (_, w) => `stroke-width="${+w + add}"`)
  .replace(/(fill|stroke)="#[0-9A-Fa-f]{3,6}"/g, (m, k) => `${k}="${C.oat}"`).replace(/stroke="none"/g, `stroke="${C.oat}"`)
  .replace(/<(rect|path|circle|ellipse)(?![^>]*stroke=)/g, `<$1 stroke="${C.oat}" stroke-width="${add}" stroke-linejoin="round"`);
export const onDark = (art) => halo(art) + art;

// ---------- mini-Bel (tittle) and wordmark ----------
export function miniBel(x, y, s, fill = C.coral, ln = C.ink, faceOn = true, mode = 'color') {
  const H = 'M-13 -6 C-14 -30 14 -30 13 -6', B = 'M0 -14 C19 -14 27 0 26 13 C25 23 18 27 12 28 L-12 28 C-18 27 -25 23 -26 13 C-27 0 -19 -14 0 -14 Z';
  const t = `<g transform="translate(${x.toFixed(1)} ${y.toFixed(1)}) scale(${s.toFixed(3)})">`;
  if (mode === 'solid') return t + `<path d="M-20 -2 C-22 -38 22 -38 20 -2" fill="none" stroke="${fill}" stroke-width="10" stroke-linecap="round"/><path d="${B}" fill="${fill}"/></g>`;
  const line = mode === 'reverse' ? C.oat : ln;
  return t + `<path d="${H}" fill="none" stroke="${line}" stroke-width="17" stroke-linecap="round"/><path d="${H}" fill="none" stroke="${fill}" stroke-width="7" stroke-linecap="round"/>` +
    `<path d="${B}" fill="${fill}" stroke="${line}" stroke-width="5" stroke-linejoin="round"/>` +
    (faceOn ? `<ellipse cx="-8" cy="9" rx="3" ry="4" fill="${C.ink}"/><ellipse cx="8" cy="9" rx="3" ry="4" fill="${C.ink}"/>` : '') + `</g>`;
}
// text = brand.wordmarkText. The LAST i/j becomes dotless (U+0131 / U+0237) and gets the mini-Bel tittle.
export function wordmark(text, S, x0, base, { ink = C.ink, bellFill = C.coral, bellFace = true, mode = 'color', plainI = false } = {}) {
  const f = FONTS.cap, idx = plainI ? -1 : Math.max(text.lastIndexOf('i'), text.lastIndexOf('j'));
  const chars = [...text].map((ch, i) => (i === idx ? (ch === 'i' ? 'ı' : 'ȷ') : ch));
  const gl = chars.map(ch => f.charToGlyph(ch)); let x = x0, d = '', stem = null;
  gl.forEach((g, i) => { if (g.index === 0) throw new Error(`glyph missing for "${chars[i]}": use the horizontal lockup`); });
  gl.forEach((g, i) => {
    const p = g.getPath(x, base, S); d += ser(p.commands);
    if (i === idx) {
      const xh = f.tables.os2.sxHeight * S / f.unitsPerEm, top = p.commands.filter(c => 'x' in c && c.y < base - 0.7 * xh);
      const xs = top.map(c => c.x); stem = { cx: (Math.min(...xs) + Math.max(...xs)) / 2, top: Math.min(...top.map(c => c.y)) };
    }
    x += g.advanceWidth * S / f.unitsPerEm + (i < gl.length - 1 ? f.getKerningValue(g, gl[i + 1]) * S / f.unitsPerEm - 0.01 * S : 0);
  });
  if (d.includes('NaN')) throw new Error('NaN in wordmark');
  const s = (0.30 * S) / 58, cy = stem ? stem.top - 0.07 * S - 28 * s : 0;
  return { svg: `<path d="${d}" fill="${ink}"/>` + (stem ? miniBel(stem.cx, cy, s, bellFill, C.ink, bellFace, mode) : ''), width: x - x0, stem, bell: stem ? { cx: stem.cx, cy, s } : null };
}
// icon mark: Bel head (handle + body + happy face; no blush, arms or feet) in a rounded square on the 240 grid
export const iconMark = (bg = C.oat, f = C.coral, ln = C.ink) =>
  `<rect x="3" y="3" width="234" height="234" rx="56" fill="${bg}" stroke="${ln}" stroke-width="6"/>` +
  `<g transform="translate(0 -4)">` + tube('M86 112 C80 44 160 44 154 112', f, 16, ln) +
  `<path d="${BEL_BODY}" fill="${f}" stroke="${ln}" stroke-width="6" stroke-linejoin="round"/>` + face({ fx: 120, fy: 150, expr: 'happy', ln }) + `</g>`;

export const svgDoc = (inner, w = 240, h = 240, bg = null) =>
  `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">${bg ? `<rect width="${w}" height="${h}" fill="${bg}"/>` : ''}${inner}</svg>`;
```

**Usage:** `loadFonts()` with the two §6.1 TTFs (under `node_modules/`); `svgDoc(onDark(art))` for dark garments, `svgDoc(art)` for light (oat/white keyed out at export, §6.4.4); rasterise only via A.8.

### A.6 Banned-word check (the procedure used to verify §4.4's list [L])

```js
// tests/unit/banned-words.test.ts core (port to TS + Vitest)
import fs from 'node:fs';
const B = JSON.parse(fs.readFileSync('brand/banned-words.json', 'utf8'));
const norm = s => s.normalize('NFKC').replace(/[‘’]/g, "'").replace(/[“”]/g, '"');
export function bannedHits(text, scope = 'all') {  // scope: 'all' | 'product' | 'names'
  let t = norm(text);
  for (const a of B.allow) t = t.replace(new RegExp(a, 'gi'), ' ');
  return B.banned.filter(b => b.scope === 'all' || b.scope === scope)
                 .filter(b => new RegExp(b.re, 'i').test(t)).map(b => b.id);
}
```

### A.7 Colour maths: CIEDE2000, WCAG contrast, nearest thread (`art/print/color.ts`)

Verified [L]: six published CIEDE2000 test pairs (Sharma, Wu & Dalal 2005) to 4 decimals (2.0425, 2.3669, 27.1492, 1.2644, 7.1792, 4.3065); the brief's own numbers (`sage` vs Bay 7.4, `lilac` vs Orchid 6.6, `coral` vs Bay 35.0, `ink` on `oat` 14.06:1); and the §6.3.2 nearest-thread ΔE00 for `ink`, `oat`, `coral`, `butter`, `lilac-deep`, `sage`.

```js
const lin = v => (v /= 255) <= 0.04045 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4;
export const rgb = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16));
export const luminance = h => { const [r, g, b] = rgb(h).map(lin); return 0.2126 * r + 0.7152 * g + 0.0722 * b; };
export const contrast = (a, b) => { const [x, y] = [luminance(a), luminance(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };
export function lab(h) {
  const [r, g, b] = rgb(h).map(lin);
  const f = t => (t > 216 / 24389 ? Math.cbrt(t) : (24389 / 27 * t + 16) / 116);
  const X = f((0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047), Y = f(0.2126 * r + 0.7152 * g + 0.0722 * b), Z = f((0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883);
  return [116 * Y - 16, 500 * (X - Y), 200 * (Y - Z)];
}
const D = Math.PI / 180;
export function de2000([L1, a1, b1], [L2, a2, b2]) {
  const C7 = c => c ** 7 / (c ** 7 + 25 ** 7), Cm = (Math.hypot(a1, b1) + Math.hypot(a2, b2)) / 2, G = 0.5 * (1 - Math.sqrt(C7(Cm)));
  const A1 = (1 + G) * a1, A2 = (1 + G) * a2, C1 = Math.hypot(A1, b1), C2 = Math.hypot(A2, b2);
  const hue = (b, a) => (b === 0 && a === 0 ? 0 : (Math.atan2(b, a) / D + 360) % 360), h1 = hue(b1, A1), h2 = hue(b2, A2);
  let dh = C1 * C2 === 0 ? 0 : h2 - h1; if (dh > 180) dh -= 360; else if (dh < -180) dh += 360;
  const dL = L2 - L1, dC = C2 - C1, dH = 2 * Math.sqrt(C1 * C2) * Math.sin(dh * D / 2), Lm = (L1 + L2) / 2, Cp = (C1 + C2) / 2;
  let hm = h1 + h2; if (C1 * C2 !== 0) hm = Math.abs(h1 - h2) <= 180 ? hm / 2 : hm < 360 ? (hm + 360) / 2 : (hm - 360) / 2;
  const T = 1 - 0.17 * Math.cos((hm - 30) * D) + 0.24 * Math.cos(2 * hm * D) + 0.32 * Math.cos((3 * hm + 6) * D) - 0.2 * Math.cos((4 * hm - 63) * D);
  const SL = 1 + 0.015 * (Lm - 50) ** 2 / Math.sqrt(20 + (Lm - 50) ** 2), SC = 1 + 0.045 * Cp, SH = 1 + 0.015 * Cp * T;
  const RT = -2 * Math.sqrt(C7(Cp)) * Math.sin(60 * Math.exp(-(((hm - 275) / 25) ** 2)) * D);
  return Math.sqrt((dL / SL) ** 2 + (dC / SC) ** 2 + (dH / SH) ** 2 + RT * (dC / SC) * (dH / SH));
}
export const deltaE = (h1, h2) => de2000(lab(h1), lab(h2));
export const nearest = (hex, palette) => Object.entries(palette).map(([name, h]) => ({ name, hex: h, dE: deltaE(hex, h) })).sort((a, b) => a.dE - b.dE)[0];
```

### A.8 Print export: crisp render, key-out, sliver heal, sRGB + 300 DPI (`art/print/export.ts`)

Verified [L] on a 3600 × 4800 LIGHT file (Bel *proud cheer* box 1950 + a Caprasimo line): 0 semi-transparent pixels; exactly 4 colours left (`ink`, `coral`, `bubblegum`, `pool`; oat sneakers and white highlights keyed out); `sharp` metadata 3600 × 4800, 4 channels, `density` 300, srgb, ICC embedded, 102 KB; two runs, same SHA-256. Heal filled six enclosed knock-outs (four 1 px pinholes where tubes meet bodies, two 8 px sole-stripe slivers: §6.1 pitfall 11). resvg's `img.pixels` is RGBA; crisp alpha is 0 or 255, so premultiplication doesn't matter.

```js
import crypto from 'node:crypto'; import { Resvg } from '@resvg/resvg-js'; import sharp from 'sharp';
import { rgb } from './color.mjs'; import { healKnockouts } from './inspect.mjs';
export async function exportPrint(svg, { w, h, keyOut = [], minKoPx = 0, dpi = 300 }) {
  if (/<text[\s>]/.test(svg) || svg.includes('NaN')) throw new Error('svg lint: <text> or NaN');
  const img = new Resvg(svg, { fitTo: { mode: 'width', value: w }, font: { loadSystemFonts: false }, shapeRendering: 1 }).render();
  if (img.width !== w || img.height !== h) throw new Error(`canvas ${img.width}x${img.height}, spec ${w}x${h}`);
  const px = Buffer.from(img.pixels), keys = keyOut.map(rgb); // RGBA; crispEdges => alpha is only 0 or 255
  for (let i = 0; i < px.length; i += 4)
    if (px[i + 3] && keys.some(([r, g, b]) => px[i] === r && px[i + 1] === g && px[i + 2] === b)) px[i + 3] = 0;
  const warnings = minKoPx ? healKnockouts(px, w, h, minKoPx) : [];
  for (let i = 0; i < px.length; i += 4) if (px[i + 3] === 0) px[i] = px[i + 1] = px[i + 2] = 0; // canonical clear pixels
  const png = await sharp(px, { raw: { width: w, height: h, channels: 4 } })
    .withIccProfile('srgb').withMetadata({ density: dpi }).png({ compressionLevel: 9, adaptiveFiltering: false }).toBuffer();
  return { png, bytes: png.length, sha256: crypto.createHash('sha256').update(png).digest('hex'), warnings };
}
```

### A.9 Pixel inspector: colours, bbox, element widths, knock-outs (`art/print/inspect.ts`)

Verified [L] on a calibration sheet (strokes 8/11/12/13/18/24 px at 0°, 30°, 45°; gaps 10/17/18/24 px): horizontal strokes read 8, 12, 12, 14, 18, 24 (odd widths +1); diagonals up to +2.3 px; gaps 10, 18, 18, 24; ≈ 2 s per 3600 × 4800 file. **Rule:** the §6.6 width checks carry no extra tolerance; a design within 2 px of a minimum gets a visual check (§6.7).

```js
// Per-colour 4-connected components + chamfer distance transform: element width ~= 2 x (max distance to another label).
export function analyse(px, w, h) {
  const N = w * h, lab = new Uint8Array(N), ids = new Map(), colours = new Map();
  let clear = 0, semi = 0, x0 = w, y0 = h, x1 = -1, y1 = -1;
  for (let p = 0; p < N; p++) {
    const a = px[4 * p + 3]; if (a === 0) { clear++; continue; } if (a < 255) semi++;
    const hex = '#' + (px[4 * p] * 65536 + px[4 * p + 1] * 256 + px[4 * p + 2]).toString(16).padStart(6, '0').toUpperCase();
    if (!ids.has(hex)) { if (ids.size === 254) throw new Error('more than 254 colours: not flat vector art'); ids.set(hex, ids.size + 1); }
    lab[p] = ids.get(hex); colours.set(hex, (colours.get(hex) ?? 0) + 1);
    const x = p % w, y = (p / w) | 0; if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y;
  }
  const d = new Float32Array(N).fill(1e9), r2 = Math.SQRT2; // the canvas border is not a boundary
  for (let p = 0; p < N; p++) { const x = p % w, l = lab[p];
    if ((x > 0 && lab[p - 1] !== l) || (x < w - 1 && lab[p + 1] !== l) || (p >= w && lab[p - w] !== l) || (p < N - w && lab[p + w] !== l)) d[p] = 1; }
  for (let p = 0; p < N; p++) { const x = p % w; let v = d[p];
    if (x > 0) v = Math.min(v, d[p - 1] + 1); if (p >= w) { v = Math.min(v, d[p - w] + 1); if (x > 0) v = Math.min(v, d[p - w - 1] + r2); if (x < w - 1) v = Math.min(v, d[p - w + 1] + r2); } d[p] = v; }
  for (let p = N - 1; p >= 0; p--) { const x = p % w; let v = d[p];
    if (x < w - 1) v = Math.min(v, d[p + 1] + 1); if (p < N - w) { v = Math.min(v, d[p + w] + 1); if (x < w - 1) v = Math.min(v, d[p + w + 1] + r2); if (x > 0) v = Math.min(v, d[p + w - 1] + r2); } d[p] = v; }
  const comp = new Int32Array(N).fill(-1), stack = new Int32Array(N), names = ['transparent', ...ids.keys()], elements = [];
  for (let s = 0; s < N; s++) {
    if (comp[s] >= 0) continue; const l = lab[s], id = elements.length; let top = 0, maxD = 0, size = 0, edge = false, nb = -1;
    stack[top++] = s; comp[s] = id;
    while (top) { const p = stack[--top], x = p % w; size++; if (d[p] > maxD) maxD = d[p];
      if (x === 0 || x === w - 1 || p < w || p >= N - w) edge = true;
      for (const q of [x > 0 ? p - 1 : -1, x < w - 1 ? p + 1 : -1, p - w, p + w]) { if (q < 0 || q >= N) continue;
        if (lab[q] !== l) { if (nb < 0) nb = q; } else if (comp[q] < 0) { comp[q] = id; stack[top++] = q; } } }
    elements.push({ id, colour: names[l], knockout: l === 0 && !edge, background: l === 0 && edge, widthPx: 2 * maxD, size, at: [s % w, (s / w) | 0], nb });
  }
  return { w, h, clear, semi, opaque: N - clear - semi, bbox: x1 < 0 ? null : { x: x0, y: y0, w: x1 - x0 + 1, h: y1 - y0 + 1 }, colours, elements, comp };
}
// Fill enclosed transparent slivers and pinholes narrower than minKoPx with a neighbouring colour (logged as warnings).
export function healKnockouts(px, w, h, minKoPx) {
  const { elements, comp } = analyse(px, w, h), thin = elements.filter(e => e.knockout && e.widthPx < minKoPx), fill = new Map(thin.map(e => [e.id, e.nb]));
  if (thin.length) for (let p = 0; p < w * h; p++) { const q = fill.get(comp[p]); if (q !== undefined) px.copy(px, 4 * p, 4 * q, 4 * q + 4); }
  return thin.map(e => `healed ${e.size}px knock-out (${e.widthPx.toFixed(0)}px wide) at ${e.at}`);
}
```

### A.10 File validator core (`art/print/validate.ts`)

Called once per manifest entry with every garment colour in `usedOn`. `rules` = the `print-specs.json` method rules in px at `spec.dpi` (§6.2); `allowed` = the recipe's exact hexes (tokens, or thread hexes for embroidery); `rules.inkHex`/`whiteHex` from `art/palette.ts`.

Verified [L] on the A.8 file: **Bay** passes (only the "spec not verified" warning); **Pepper** fails `#22263A edge on PEP 1.78:1 < 3` (LIGHT art on a dark garment, as designed); **Watermelon** warns `#FF8A65 vs WTM dE00 16.8: sample first`; the 2.8% `pool` sole-stripe edge pixels are not primary (`primaryEdgeShare` 0.10); art-box placements get no extra margin inside the box (a bar 60 px inside the left-chest box passes, 40 px outside fails).

```js
import sharp from 'sharp'; import { analyse } from './inspect.mjs'; import { contrast, deltaE } from './color.mjs';
export async function validateFile(png, { spec, rules, garments = [], allowed, meta = {} }) {
  const F = [], W = [], m = await sharp(png).metadata(), [cw, ch] = spec.canvasPx;
  if (m.format !== 'png' || m.channels !== 4 || m.depth !== 'uchar') F.push('not an 8-bit RGBA PNG');
  if (m.width !== cw || m.height !== ch) F.push(`canvas ${m.width}x${m.height}, spec ${cw}x${ch}`);
  if (Math.max(m.width, m.height) > 20000 || png.length > rules.maxBytes) F.push(`too large: ${png.length} bytes`);
  if (m.space !== 'srgb') F.push(`colour space ${m.space}`);
  if (m.density !== spec.dpi) W.push(`density ${m.density}, spec ${spec.dpi}`);
  if (!spec.verified.value) W.push(`spec ${spec.key} not verified against the partner template [${spec.verified.tag}]`);
  const { data } = await sharp(png).raw().toBuffer({ resolveWithObject: true }), a = analyse(data, m.width, m.height);
  if (!a.opaque) F.push('empty file (0 ink pixels)');
  if (a.semi) F.push(`${a.semi} semi-transparent pixels (alpha must be 0 or 255)`);
  if (spec.background === 'full_bleed' && a.clear) F.push(`${a.clear} transparent pixels in a full-bleed file`);
  const box = spec.artBoxPx ?? { x: 0, y: 0, w: cw, h: ch }, g = meta.edgeBleed || spec.artBoxPx ? 0 : rules.safeMarginPx, b = a.bbox;
  if (b && spec.background === 'transparent' && (b.x < box.x + g || b.y < box.y + g || b.x + b.w > box.x + box.w - g || b.y + b.h > box.y + box.h - g))
    F.push(`art ${JSON.stringify(b)} outside the safe area of ${JSON.stringify(box)} (margin ${g})`);
  for (const hex of a.colours.keys()) if (!allowed.includes(hex)) F.push(`off-palette colour ${hex}`);
  if (spec.maxThreads && a.colours.size > (meta.maxThreads ?? spec.maxThreads)) F.push(`${a.colours.size} thread colours > ${meta.maxThreads ?? spec.maxThreads}`);
  for (const e of a.elements) {
    if (e.background || (e.touchesEdge && meta.edgeBleed)) continue;
    const min = e.knockout ? rules.minKnockoutPx : rules.minStrokePx;
    if (e.widthPx < min) F.push(`${e.knockout ? 'knock-out' : e.colour} element ${e.widthPx.toFixed(1)}px wide < ${min} at ${e.at}`);
  }
  for (const t of meta.texts ?? []) if (t.xHeightPx < rules.minXHeightPx[t.font]) F.push(`text "${t.text}" x-height ${t.xHeightPx} < ${rules.minXHeightPx[t.font]}`);
  const edge = new Map(); let edgeN = 0; // colours that touch the garment (transparent neighbours)
  for (let p = 0; p < m.width * m.height; p++) { if (data[4 * p + 3] === 0) continue; const x = p % m.width;
    if ((x > 0 && !data[4 * p - 1]) || (x < m.width - 1 && !data[4 * p + 7]) || (p >= m.width && !data[4 * (p - m.width) + 3]) || (data[4 * (p + m.width) + 3] === 0)) {
      const hex = '#' + data.readUIntBE(4 * p, 3).toString(16).padStart(6, '0').toUpperCase(); edge.set(hex, (edge.get(hex) ?? 0) + 1); edgeN++; } }
  for (const gm of garments) {
    for (const [hex, n] of edge) if (n / edgeN >= rules.primaryEdgeShare && contrast(hex, gm.hex) < rules.minEdgeContrast) F.push(`${hex} edge on ${gm.code} ${contrast(hex, gm.hex).toFixed(2)}:1 < ${rules.minEdgeContrast}`);
    for (const [hex, n] of a.colours) { if (hex === rules.inkHex || n / a.opaque < 0.02) continue; const dE = deltaE(hex, gm.hex);
      if (dE < rules.mergeDeltaE) F.push(`${hex} merges with ${gm.code} (dE00 ${dE.toFixed(1)}): use GARMENT-FILL or an accent swap`);
      else if (dE < rules.cautionDeltaE) W.push(`${hex} vs ${gm.code} dE00 ${dE.toFixed(1)}: sample first`); }
    if (!gm.isDark && a.colours.has(rules.whiteHex)) F.push(`white ink on light garment ${gm.code} will not print`);
    if (gm.hexTag === 'U') W.push(`${gm.code} hex is an estimate [U]: recheck with the live color_code`);
  }
  return { status: F.length ? 'fail' : W.length ? 'warn' : 'pass', failures: F, warnings: W, stats: { opaque: a.opaque, bbox: b, colours: a.colours.size } };
}
```

### A.11 Arc text and arc auto-fit (`art/lib/arc-text.ts`)

Verified [L]: D09's rings measure **3923 px of 4154** (top, r 1400) and **3988 of 4747** (bottom, r 1600) at x-height 120, matching the reference render; the D27 worst case `MMMMMMMMMMMMMMMM` (16 characters, r 1400) fits at x-height **140.3**; 22 characters throws `ARC FIT FAIL … x-height 102.0 < 110`, as designed; rendered, the top ring reads clockwise and the bottom upright.

```js
// top: reads clockwise, glyph tops outward, centred on 12 o'clock. bottom: upright, tops toward the centre, centred on 6 o'clock.
import { FONTS, textPath } from './crew-kit.mjs';
const unit = (fontKey) => { const f = FONTS[fontKey]; return { f, xhEm: f.tables.os2.sxHeight / f.unitsPerEm }; };
function advances(fontKey, str, size, track) {
  const { f } = unit(fontKey), u = size / f.unitsPerEm, gl = [...str].map(ch => f.charToGlyph(ch));
  if (gl.some(g => g.index === 0)) throw new Error(`missing glyph in "${str}"`); // e.g. U+00D7 in D24: fail, never substitute
  return { gl, u, adv: gl.map((g, i) => g.advanceWidth * u + (i < gl.length - 1 ? f.getKerningValue(g, gl[i + 1]) * u : 0) + track * size) };
}
// Largest x-height (<= maxXh) whose arc length fits maxDeg of the circle; throws below minXh (the build fails, as designed).
export function fitArc(fontKey, str, { r, maxXh, minXh, maxDeg = 170, track = 0.04 }) {
  const { xhEm } = unit(fontKey), at100 = advances(fontKey, str, 100, track).adv.reduce((s, v) => s + v, 0) / 100;
  const xh = Math.min(maxXh, (r * maxDeg * Math.PI / 180) / at100 * xhEm);
  if (xh < minXh) throw new Error(`ARC FIT FAIL "${str}": x-height ${xh.toFixed(1)} < ${minXh} on r ${r}`);
  return xh;
}
export function arcText(fontKey, str, { xh, cx, cy, r, where, fill, track = 0.04, maxDeg = 170 }) {
  const size = xh / unit(fontKey).xhEm, { gl, u, adv } = advances(fontKey, str, size, track);
  const total = adv.reduce((s, v) => s + v, 0), budget = r * maxDeg * Math.PI / 180;
  if (total > budget) throw new Error(`ARC FIT FAIL "${str}": ${total.toFixed(0)}px > ${budget.toFixed(0)}px`);
  let pos = -total / 2, svg = '';
  gl.forEach((g, i) => {
    const a = (pos + adv[i] / 2) / r, top = where === 'top', p = textPath(fontKey, [...str][i], size, -g.advanceWidth * u / 2, 0);
    const x = cx + r * Math.sin(a), y = top ? cy - r * Math.cos(a) : cy + r * Math.cos(a);
    svg += `<path d="${p.d}" fill="${fill}" transform="translate(${x.toFixed(1)} ${y.toFixed(1)}) rotate(${((top ? a : -a) * 180 / Math.PI).toFixed(2)})"/>`;
    pos += adv[i];
  });
  return { svg, arcPx: total, budgetPx: budget };
}
```

### A.12 Seamless pattern tile, overlap check, seam check, panel fill (`art/lib/tile.ts`)

Verified [L] with the D21 kinds (sneaker r 240, same-kind spacing 620; sparkle r 95, spacing 330; 40 px clearance): 14 motifs, 0 overlaps; seam check 80 stray pixels (0.0025%, rasteriser noise) vs 107,735 for a deliberately unwrapped tile, hence ≤ 0.01%; `fillPanel` filled a 7200 × 6225 @150 placeholder leggings panel with 6 in tiles (900 px): 474 KB, fully opaque. Small 4-point sparkles at this scale can read as "+" (§6.7 misread list).

```js
import { Resvg } from '@resvg/resvg-js';
export function makeTile({ T = 1800, ground, seed = 7, clear = 40, kinds }) { // kinds: [{ id, count, r (bounding radius px), space (same-kind centre gap), draw(rnd) }]
  let s = seed; const rnd = () => (s = (s * 16807) % 2147483647) / 2147483647;
  const tor = (p, q) => { const dx = Math.abs(p.x - q.x), dy = Math.abs(p.y - q.y); return Math.hypot(Math.min(dx, T - dx), Math.min(dy, T - dy)); };
  const placed = [];
  for (const k of kinds) for (let n = 0, tries = 0; n < k.count; ) {
    if (++tries > 50000) throw new Error(`tile: could not place ${k.id} #${n + 1}`);
    const p = { x: Math.round(rnd() * T), y: Math.round(rnd() * T), r: k.r, k };
    if (placed.every(q => tor(p, q) >= Math.max(p.r + q.r + clear, q.k === k ? k.space : 0))) { placed.push(p); n++; }
  }
  const overlaps = []; // validator: bounding circles may not touch, including across the wrap
  placed.forEach((p, i) => placed.slice(i + 1).forEach(q => { if (tor(p, q) < p.r + q.r) overlaps.push([p.k.id, q.k.id, Math.round(tor(p, q))]); }));
  const body = dx => placed.map(p => { const m = p.k.draw(rnd), X = (p.x + dx) % T, Y = (p.y + dx) % T; let g = '';
    for (const ox of [-T, 0, T]) for (const oy of [-T, 0, T]) g += `<g transform="translate(${X + ox} ${Y + oy})">${m}</g>`; return g; }).join('');
  const svg = (dx = 0) => { s = seed + 1; return `<svg xmlns="http://www.w3.org/2000/svg" width="${T}" height="${T}" viewBox="0 0 ${T} ${T}"><rect width="${T}" height="${T}" fill="${ground}"/>${body(dx)}</svg>`; };
  return { svg: svg(0), shifted: svg(T / 2), overlaps, count: placed.length };
}
// Seam check: the centre crop of a 2x2 mosaic must match the tile re-generated with every motif shifted by T/2.
export function seamCheck({ svg, shifted }, T) {
  const px = s => new Resvg(s, { shapeRendering: 1, font: { loadSystemFonts: false } }).render().pixels;
  const a = px(svg), b = px(shifted); let diff = 0;
  for (let y = 0; y < T; y++) for (let x = 0; x < T; x++) {
    const sx = (x + T / 2) % T, sy = (y + T / 2) % T, i = 4 * (sy * T + sx), j = 4 * (y * T + x);
    if (a[i] !== b[j] || a[i + 1] !== b[j + 1] || a[i + 2] !== b[j + 2] || a[i + 3] !== b[j + 3]) diff++;
  }
  return { diff, ok: diff <= T * T * 1e-4 };
}
// Fill a whole template canvas at a FIXED physical scale (same motif size on every garment size), anchored on the centre line.
export function fillPanel(tileSvg, { w, h, dpi, tileIn = 6, anchorX = w / 2 }) {
  const s = tileIn * dpi, inner = tileSvg.replace(/^<svg[^>]*>|<\/svg>$/g, ''), T = +tileSvg.match(/width="(\d+)"/)[1];
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}"><defs><pattern id="t" patternUnits="userSpaceOnUse" x="${anchorX - s / 2}" y="0" width="${s}" height="${s}"><g transform="scale(${s / T})">${inner}</g></pattern></defs><rect width="${w}" height="${h}" fill="url(#t)"/></svg>`;
}
```

Usage (D21): `makeTile({ T: 1800, ground: tokens.canvas, seed: 7, kinds: [{ id: 'sneaker', count: 6, r: 240, space: 620, draw: shoe }, { id: 'sparkle', count: 8, r: 95, space: 330, draw: sparkle }] })`. `draw(rnd)` takes all randomness from `rnd`, so `svg` and `shifted` draw identical motifs.

### A.13 Offline flat-lay mockup at true print scale (`art/mockups/flatlay.ts`)

Verified [L]: the A.8 back print on a Bay tee rendered 1440 × 1800 in 5.8 s; WebP 5.7 / 13.4 / 21.9 KB and AVIF 3.4 / 6.0 / 9.1 KB at 480 / 960 / 1440 px; the 12 × 16 in area lands as 600 × 800 px on a 22 in body (50 px/in); inspected: a believable laid-flat tee.

```js
// Art lands at TRUE print scale (PPI mockup px per garment inch). Mockups may use opacity and gradients (print files never);
// tee shown, other templates per §6.8.
import { Resvg } from '@resvg/resvg-js'; import sharp from 'sharp';
const PPI = 50, W = 1440, H = 1800; // 28.8 x 36 in "table"; tee body 22 in wide
const TEE = { outline: 'M560 110 Q720 190 880 110 L1230 215 L1425 520 L1290 610 L1270 560 L1270 1600 L170 1600 L170 560 L150 610 L15 520 L210 215 Z',
  seams: 'M560 110 Q720 205 880 110 M1270 560 L1230 215 M170 560 L210 215 M170 1560 H1270', area: { front: { x: 4.2, y: 3.0 }, back: { x: 4.2, y: 2.4 } } };
export async function flatLay({ printPng, spec, garmentHex, view = 'front', ink, bg }) { // ink, bg from art/palette.ts
  const [cw, ch] = spec.canvasPx, aw = Math.round(cw / spec.dpi * PPI), ah = Math.round(ch / spec.dpi * PPI); // 12x16 in -> 600x800
  const art = await sharp(printPng).resize(aw, ah, { kernel: 'lanczos3' }).png().toBuffer(), o = TEE.area[view];
  const ax = Math.round((W - aw) / 2), ay = Math.round(110 + o.y * PPI); // centred; top N in below the collar
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
<defs><clipPath id="g"><path d="${TEE.outline}"/></clipPath><linearGradient id="s" x1="0" x2="1"><stop offset="0" stop-color="${ink}" stop-opacity=".14"/>
<stop offset=".22" stop-color="${ink}" stop-opacity="0"/><stop offset=".78" stop-color="${ink}" stop-opacity="0"/><stop offset="1" stop-color="${ink}" stop-opacity=".14"/></linearGradient></defs>
<rect width="${W}" height="${H}" fill="${bg}"/><g clip-path="url(#g)"><rect width="${W}" height="${H}" fill="${garmentHex}"/>
<image x="${ax}" y="${ay}" width="${aw}" height="${ah}" xlink:href="data:image/png;base64,${art.toString('base64')}"/>
<rect width="${W}" height="${H}" fill="url(#s)"/></g>
<path d="${TEE.seams}" fill="none" stroke="${ink}" stroke-opacity=".18" stroke-width="5"/><path d="${TEE.outline}" fill="none" stroke="${ink}" stroke-opacity=".35" stroke-width="4"/></svg>`;
  const png = new Resvg(svg, { font: { loadSystemFonts: false } }).render().asPng(); // anti-aliased: fine for mockups
  const out = {};
  for (const w of [480, 960, 1440]) { const img = sharp(png).resize(w); out[w] = { webp: await img.clone().webp({ quality: 82 }).toBuffer(), avif: await img.clone().avif({ quality: 50 }).toBuffer() }; }
  return { svg, png, out };
}
```

---

## Appendix B. Verification ledger

Every [U] (and [S]) item in this brief, de-duplicated; why each matters is in its owning section. REPORT.md (R9) gives each row a status: **open**, **confirmed** (source and date; tag changed to V or T in the data) or **changed** (new value; every test re-run).

**Who:** **C** = the build session checks it live or with a test (host blocked: keep [U], §10.5) · **F** = the founder (account, money, lawyer or physical sample) · **C/F** = C prepares, F completes.
**Blocks:** **P** = the prototype (milestone in brackets) · **L** = launch, Tue 5 Jan 2027 · **L-Dec** = the 1 Dec waitlist · **R1** = the round-1 sample order (~23 Nov) · **Dn** = drop n (§5.6) · **Later** = after launch, or only if a decision changes.

### B.1 Name, IP & legal

| ID | Item | Who | How | Blocks |
|---|---|---|---|---|
| U1 | KETTLEKIN clearance in US classes 25, 16, 18, 21, 9, 35, 41, 28, incl. distinguishability from **KETTLE AND DESIGN, Reg. 6244834** | F (attorney) | §4.1 checklist | L (before paid ads or bulk samples) |
| U2 | The same search in EUIPO/TMview, UKIPO, IP Australia, CIPO | F | §4.1 checklist | Later |
| U3 | Alternates: GYMLINGS (IP Australia No. 2616722, class 28: status, owner; no US mark found); Huddlebell's crowded HUDDLE field | F | §4.1 checklist | Later (only on a rename) |
| U4 | Domain availability, in the §4.1 order | F | §4.1 checklist | L-Dec |
| U5 | Handles `@kettlekin` (or the §4.1 fallbacks) on IG, TikTok, Pinterest, YouTube, Threads, Bluesky | F | §4.1 checklist | L-Dec |
| U6 | TESS + Etsy check: the 10 core slogans plus "department of showing up", "moving at the speed of okay", "i count visits" and the launch line before round 1; every other `content/print-lines.json` line before its drop (`Design.clearance` stays U) | F | §4.1 checklist | R1 (those lines) · Dn (each later line) |
| U7 | Marketplace sweep: Etsy, Amazon, Redbubble, TikTok Shop (§4.1 terms) | F | §4.1 checklist | L |
| U8 | USPTO fees: $350 per class [S], + $200 free-form goods text, + $100 insufficient information; statement-of-use fee | F | Fee schedule on the filing day | L (filing) |
| U9 | Attorney clearance cost ($500–1,500 estimate) | F | Quote | L |
| U10 | Entity type and state fees (LLC $50–500 estimate) | F | State filing site | L |
| U11 | Sales tax: home-state registration, nexus, clothing vs accessory categories, Printful resale certificate | F | State revenue site; Shopify Tax | L |
| U12 | Shopify Tax: $100k free per calendar year, or once per lifetime for stores created after 13 May 2026 | F | Shopify help/admin | Later |
| U13 | CAN-SPAM opt-out window (10 business days); bulk-sender rules (SPF, DKIM, DMARC) | F | FTC CAN-SPAM guide; ESP docs | L (W0 on 5 Jan) |
| U14 | CCPA/state-privacy thresholds; functional `localStorage` needs no consent banner | F (lawyer) | Review of `golive/policies/privacy.md` | L |
| U15 | COPPA approach for a 13+ community | F (lawyer) | Review of terms + Club Rules | L |
| U16 | Community votes with prizes count as sweepstakes | F | Lawyer, only if a prize is added | Later (D10) |
| U17 | Copyright registration fees for the model sheets | F | copyright.gov | Later |
| U18 | IP-assignment template for outside designers (§6.9) | F (lawyer) | Lawyer | Later |
| U19 | Crisis-line wording (US 988) for human replies | F | Official 988 site | L |
| U20 | GPSR (EU Responsible Person), EU VAT OSS, UK VAT | F | Partner support + advisor | Later (non-US) |
| U21 | Lawyer review of `golive/policies/*` and `golive/legal/*`; the "Draft for legal review" banner stays until then | F | Mid-December review | L |

### B.2 Platform plans, fees and budget

| ID | Item | Who | How | Blocks |
|---|---|---|---|---|
| U22 | Shopify Basic: $39/mo monthly or $29/mo yearly [S]; any introductory offer | F | shopify.com/pricing on the day you pay | L |
| U23 | Shopify Payments 2.9% + 30¢ [S]; 2% third-party gateway fee | F | Admin after activation; update `pricing-rules.json`, re-run `npm run catalog` | L |
| U24 | Printful Growth: which blanks get "up to 33% off" (§5.1 rule 4) | F | 14-day trial; measure discount d | Later |
| U25 | Email provider (default Shopify Email + automations): names, free allowance | F | Shopify admin | L |
| U26 | Cookie-free analytics provider, cost (≈ $27 estimate), host name | F | Choose one; set `NEXT_PUBLIC_ANALYTICS_HOST` at deploy | L |
| U27 | Static-host terms: Cloudflare Pages (limits, commercial use, Access), Netlify, Vercel (Hobby non-commercial; Pro ≈ $20/user), GitHub Pages business use | F | Current terms | L-Dec |
| U28 | Sample costs: R1 $300–450 (14 pieces + stickers), R2 $300–400, R3 $100–200 [U] | F | A `--draft-order` (§8.3) shows real costs before confirming | R1 |
| U29 | Other budget lines: creator gifts ≈ $25 each, photo props, domain $10–25 | F | Real receipts in `docs/decisions.md` | L |
| U30 | Paid-test target: cost per first order ≤ $20 | F | The 14-day $300 test (§9.9) | Later |
| U31 | Unlimited-colour embroidery ≈ +$3.50–3.95 per item (not used) | F | Printful pricing, only if §2 decision 20 changes | Later |

### B.3 Printful catalog, costs and print specs

Once a token exists, `npm run catalog:pull -- --live` (GET only) and §6.3.4's paste procedure close most rows; until then the snapshots and seeds stand, tagged U.

| ID | Item | Who | How | Blocks |
|---|---|---|---|---|
| U32 | Catalog product ids: `bc3001` 71, `g18000` 145, `m7580` TBC, `ec8000` TBC, `sticker3` 358, `patch3` TBC; whether product-page id = API id | C | `GET /v2/catalog-products/{id}` | L (exports refuse `null`) |
| U33 | Whether catalog GETs need a token | C | One GET without one | P (M4; fallback: snapshots) |
| U34 | Variant ids, colour names, colour × size availability per blank (incl. `YLW`, `SPR`, joggers, beanie, bottle body); counts can only fall below 575/1,901 | C | `/catalog-variants` | L |
| U35 | Garment `color_code` for every code (§5.2 approx hexes: Bay [T], the rest [U], incl. Navy `#2B3150`) | C (live) + F (QA #9, grey card) | `/catalog-variants`; sample photos | L (P: validator warns) |
| U36 | Base costs by size (2XL+ upcharges) and every `planningBaseCost` in §5.3 | C | `/prices`, `/catalog-variants/{id}/prices` | L (founder signs off prices) |
| U37 | Size ranges per blank and colour: `bc3001` on Printful, `cc1566` S–3XL, `m7580` XS–2XL, `aop559` XS–XL, `aop334` 2XL–6XL, `aop477` "7 sizes", `aop507` XS–2XL | C | `/catalog-variants`, `/sizes` | L |
| U38 | Size charts for every blank (none = TBC; the listing can't be `active`) | C (or F copies with URL) | `/sizes` → `catalog/size-guides/` | L |
| U39 | Fabric, care and certification strings (ring-spun, garment-dyed; fleece blends; UPF 50+, recycled %) | C | Product endpoint or page | L (P: fallback care line) |
| U40 | Inside label: $0.99 [T], both tees eligible, label-only Private accepted, the reserved y 640–900 zone matches the auto-fill, 600/750 px label sizes | F (one-product test) + R1 sample | §8.2 step 8; §8.4 check 3 | L |
| U41 | Every `print-specs.json` area (`verified: false`): back = front, chest and back-neck art boxes, hoodie pouch limit (3600 × 3000), sleeve, label, embroidery names and boxes | C or F | §6.3.4 paste procedure | R1 (round-1 placements) · L (exports) |
| U42 | Placeholder canvases (§6.2): `m7580.left_hip`, `ec8000.tote_front`, `bottle788.wrap` (+ print method), `towel883`, `notebook474`, `socks882`, `patch3`, AOP per-size templates | C or F | Download the templates | **R1 for the bottle** (§2 decision 31) · D1, D3, D6, D7, D9 for the rest |
| U43 | Sticker 3 in pixel size; sticker-sheet ground transparent vs full-bleed | C or F | Template | L |
| U44 | Partner placement ids (`front`, `back`, `label_inside`, `embroidery_chest_left`, `embroidery_front`, …) | C | `/mockup-templates` / live product data | L |
| U45 | The §6.2 print heuristics (stroke ≥ 12 px, knock-out ≥ 18 px, label text ≥ 0.1 in, other minimums, safe margins, 3:1 edge contrast, x-height floors) | F | R1 QA checks 2–3 (§8.4); tighten or keep, log it | L |
| U46 | Embroidery: Navy 1966 vs Black 1800 for `ink`; the Bel face at 2 in; digitisation $2.95–6.50 per design and placement | F | R1 samples (§8.4 check 4) | L |
| U47 | US shipping per blank (fleece $8.79 / +$2.50, AOP, hats, bottle, notebook, stickers +1) and transit days (`transit.json` is `null`) | C or F | `golive:printful -- --live --rates` | L (P shows TBC) |
| U48 | Split parcels (AOP, drinkware, embroidery); holidays not modelled in business-day windows | F | Test orders (§8.2 step 20) | L (copy says "separate boxes") |
| U49 | Activewear: leggings opacity (squat test), white show-through at stretch, shorts waistband roll; bottle lid quality | F | R2 samples, §8.4 check 11 | D3 (bottle: L) |
| U50 | Printful holiday cutoffs: 2026 standard date (gifting wave 1 ~9 Dec); the 2027 table → `catalog/src/cutoffs.json` | F | Printful holiday guide | L-Dec · D11 |
| U51 | Printful lost-parcel claims; orders editable until production starts | F | Printful help centre | L |
| U52 | Mockup-task rate limit (≈ 2–10/min) | C | `X-Ratelimit-*` live | Later |

### B.4 Shopify ↔ Printful integration

| ID | Item | Who | How | Blocks |
|---|---|---|---|---|
| U53 | `tierMode`: one Shopify product with different print files per Style (`option` vs `sibling`, 17 listings) | F | §8.2 step 8 one-product test, then re-export | L |
| U54 | Sync-product creation via API for a Shopify-linked store (v1 endpoints) | C (live read) | `GET /store/products` on the founder's token | L |
| U55 | Whether sync-variant `external_id` is platform-owned on Shopify stores (§5.2 join key) | C | `golive:printful -- --live` diff | L |
| U56 | Whether the files endpoint accepts only a URL (`POST /v2/files`) | C | Live API docs + one dry call | L |
| U57 | Token scope names; when `X-PF-Store-Id` is required | F | Printful developer portal | L |
| U58 | Printful dashboard names: manual order approval, packing-slip options, return-address options | F | Printful settings (§8.2 steps 5–6) | L |
| U59 | Carrier-calculated shipping on Shopify Basic (else fallback B: flat $5.95 below $75) | F | Shopify admin | L |
| U60 | Buddy Pack as an automatic −$8 discount without an app; codes case-insensitive | F | Test carts (§8.2 step 12) | L |
| U61 | Password-page signup on the chosen theme; the customer-form post from `club.{domain}` (captcha?) | C/F | Live test on 1 Dec | L-Dec |
| U62 | Shopify CSV: template headers, Product Category taxonomy, metafield syntax, variant grams, 3-option limit, 100 vs 2,048 variant cap | C | Diff `exports/shopify-products.csv` against a fresh template | L |
| U63 | Statement-descriptor length; theme family (Horizon vs Dawn) | F | Shopify admin | L |
| U64 | Growth tools: Shopify Collabs or manual affiliates, a referral app, TikTok Shop fees and POD shipping times | F | Once redemptions pass 50/month (§9.5) | Later |

### B.5 Web stack (closed during the prototype)

| ID | Item | Who | How | Blocks |
|---|---|---|---|---|
| U65 | Every package pin in §6.1/§7.1 (a 2026-11-10 snapshot) | C | `npm view` (§3 rule 2); R4 table | P (M0) |
| U66 | Vitest 5.0.5 `--typecheck` flag | C | Run it | P (M0) |
| U67 | Tailwind 4 `--color-*: initial` reset syntax | C | Build, grep the CSS for non-token colours | P (M1, M6) |
| U68 | Fontsource WOFF2 file names under `files/` | C | List the folder | P (M1) |
| U69 | Zustand 5 `useShallow` for multi-field selectors | C | Zustand docs in `node_modules` | P (M6) |
| U70 | LHCI `staticDistDir` URL configuration | C | LHCI configuration docs | P (M6) |
| U71 | `serve` 14 serves `out/404.html` | C | e2e flow 18 | P (M6) |
| U72 | Canvas `fillText` with web fonts for the e-card PNG | C | e2e flow 11 screenshot | P (M7) |
| U73 | CSP needs `'unsafe-inline'`; the chosen host honours the generated `out/_headers` | C (CSP violations in Playwright) · F (host) | Playwright console; host docs | P (M6) · L-Dec |
| U74 | JSON-LD: Google accepts `MadeToOrder`; `pattern` in `variesBy`; `shippingDetails`/`hasMerchantReturnPolicy` once policies are final | F | Rich Results Test (§8.2 step 21) | L |
| U75 | Contact response time and postal address (PO box / virtual mailbox) | F | Decide and fill in | L |

### B.6 Market claims and KPI targets

| ID | Item | Who | How | Blocks |
|---|---|---|---|---|
| U76 | Market figures: 53% "how others look at me" (attribution [S/U]), 62% "get in shape before joining" (date [U]), 1 in 3 have nobody to train with [S], the January gym-join peak, "samples need 2–3 weeks". **Never in copy or ads until verified** | F | Appendix C sources; record date + publisher | Later (before any ad uses one) |
| U77 | $75 free-shipping threshold is optimal | F | 30 days of data (§9.8 AOV vs $75) | Later |
| U78 | Every [U] KPI target in §9.8 | F | Re-set after 30 days of real data | Later |

---

## Appendix C. Key sources

Load-bearing URLs with the brief's tags. Re-open a page before spending money on its figure.

**Audience and market**
1. PureGym UK Fitness Report 2022/23 (56% gym anxiety; 67% of women vs 49% of men) [V]: https://www.puregym.com/blog/uk-fitness-report-gym-statistics-2022-2023/
2. US gymtimidation poll ("the way other users look at me" 53%; attribution [U]) [S]: https://musclebooster.welltech.com/gymtimidation-us
3. Vice: Gen Z fear of being recorded at the gym (19%) [T]: https://www.vice.com/en/article/gen-z-are-quitting-the-gym-for-fear-of-being-recorded/
4. Planet Fitness / Kelton via BioSpace (62% get in shape before joining) [V]: https://www.biospace.com/planet-fitness-study-finds-fear-of-judgement-prompts-majority-of-americans-nearly-two-thirds-to-try-to-get-in-shape-before-ever-stepping-foot-into-a-gym
5. Adidas x Bumble (1 in 3 have nobody to train with) [S]: https://athletechnews.com/adidas-bumble-partner-to-connect-gym-goers/

**Name and IP**
6. USPTO trademark search [V]: https://tmsearch.uspto.gov
7. KETTLE AND DESIGN, US Reg. 6244834 (serial 90006819) [S]: https://trademarks.justia.com/900/06/kettle-and-90006819.html
8. IP Australia, GYMLINGS No. 2616722 [S]: https://search.ipaustralia.gov.au/trademarks/search/view/2616722/details

**Fonts and licences**
9. Caprasimo metadata (OFL-1.1) [V]: https://raw.githubusercontent.com/google/fonts/main/ofl/caprasimo/METADATA.pb
10. Atkinson Hyperlegible Next metadata (OFL-1.1) [V]: https://raw.githubusercontent.com/google/fonts/main/ofl/atkinsonhyperlegiblenext/METADATA.pb
11. SIL OFL FAQ (merchandise and outlined glyphs allowed) [V]: https://tug.ctan.org/fonts/gentium/OFL-FAQ.txt

**Printful: plans and products**
12. Pricing and plans [V]: https://www.printful.com/pricing
13. Growth plan ($24.99/mo, trial, discounts) [V]: https://help.printful.com/hc/en-us/articles/10720462952988
14. Sample orders (20% / 25% off, 1 per month, ≤ 3 items) [V]: https://help.printful.com/hc/en-us/articles/360014067959
15. Fulfilment time (2–5 business days; AOP longer) [V]: https://help.printful.com/hc/en-us/articles/360014007980-how-long-does-fulfillment-take-
16. Returns (misprints within 30 days; wrong size not covered) [V]: https://help.printful.com/hc/en-us/articles/360014006840-What-is-Printful-s-return-and-refund-policy
17. Holiday shipping deadlines [S]: https://www.printful.com/blog/your-holiday-shipping-and-order-deadline-guide
18. Comfort Colors 1717, product 586 (base $15.60) [T]: https://www.printful.com/custom/product/586
19. AOP leggings with pockets, product 559 [T]: https://www.printful.com/custom/product/559
20. Printful on the Shopify App Store [V]: https://apps.shopify.com/printful

**Printful: print-file specs**
21. Preparing print files (no semi-transparent edges or fades) [V]: https://help.printful.com/hc/en-us/articles/28491464259740-How-should-I-prepare-my-print-file-for-the-best-results
22. Maximum print-file size [V]: https://help.printful.com/hc/en-us/articles/360014066319-What-is-the-maximum-file-size-of-a-print-file
23. Inside and outside labels (3 × 3 in, 900 × 900 px; auto-filled size, fibre, origin) [V]: https://www.printful.com/blog/printful-inside-outside-labels
24. Customising inside labels [V]: https://help.printful.com/hc/en-us/articles/5582030932764-How-do-I-customize-inside-labels
25. Embroidery threads (15 threads, ≤ 6 per design) [V]: https://support.printful.com/hc/en-us/articles/41396531482001
26. Embroidered hats (1890 × 768 file; dad-hat art box) [V]: https://www.printful.com/blog/custom-embroidered-hats-guide-to-creating-a-design-and-embroidery-file
27. All-over-print files (per-product, per-size templates) [V]: https://www.printful.com/ca/creating-aop-file
28. Graphics and embroidery guide (150 DPI for cut-and-sew) [V]: https://www.printful.com/graphics-and-embroidery-guide

**APIs**
29. Printful API v2 (beta) [V]: https://developers.printful.com/docs/v2-beta/
30. What to know about Printful API v2 [V]: https://help.printful.com/hc/en-us/articles/10293184543260-What-should-I-know-about-Printful-s-API-v2
31. Shopify Storefront API [V]: https://shopify.dev/docs/api/storefront

**Web stack, SEO, accessibility**
32. Next.js static exports [V]: https://github.com/vercel/next.js/blob/canary/docs/01-app/02-guides/static-exports.mdx
33. Next.js 16 upgrade guide [V]: https://nextjs.org/docs/app/guides/upgrading/version-16
34. Next.js JSON-LD guide [V]: https://github.com/vercel/next.js/blob/canary/docs/01-app/02-guides/json-ld.mdx
35. Node.js release index [V]: https://nodejs.org/dist/index.json
36. WCAG 2.2 [V]: https://www.w3.org/TR/WCAG22/
37. Google Product structured data [V]: https://developers.google.com/search/docs/appearance/structured-data/product

**Commerce and US law** (official pages; figures from them stay [S] until re-read)
38. Shopify plans and pricing (Basic $39/mo monthly, $29/mo yearly) [S]: https://www.shopify.com/pricing
39. FTC Mail, Internet, or Telephone Order Merchandise Rule: https://www.ftc.gov/business-guidance/resources/business-guide-ftcs-mail-internet-or-telephone-order-merchandise-rule
40. FTC Rule on Consumer Reviews and Testimonials: https://www.ftc.gov/legal-library/browse/rules/rule-use-consumer-reviews-testimonials
