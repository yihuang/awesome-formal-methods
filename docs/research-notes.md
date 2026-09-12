# Research notes: provenance, confidence, and gaps

This file exists so that nobody has to guess whether a number in the wiki is solid. It records
**how** the material was gathered, **what is verified**, **what is uncertain**, and **what is still
missing**.

---

## 1. How this was researched

**Method.** Web search for discovery (topic batches across the four coverage axes), then
`fetch_content` on primary sources — project sites, official docs, papers, repositories — rather
than trusting search summaries. Where a specific number or quotation appears in the wiki, it is
linked to the page it came from.

**Environment constraints hit during research (worth knowing before a re-run):**

| Constraint | Effect |
|---|---|
| Only the **DuckDuckGo** search provider was usable. Brave, Tavily, SearxNG, Parallel, TinyFish, Jina, Firecrawl all lack API keys; the default (`Exa`) hit a **429 rate limit** partway through. | Discovery breadth is narrower than it could be. Re-run with a funded provider to widen coverage. |
| **Wikipedia returns HTTP 403** ("Too Many Reqs") to direct fetches from this environment. | Wikipedia-sourced facts are cited via search results, not read directly. Treat those entries as lower confidence. |
| Paywalled/blocked: CACM, ACM Queue, Springer, RTCA, Nature (partial). | Case-study details come from mirror pages, arXiv preprints, project sites, and the public repositories. |
| **No `pip`, no network for installs.** | The Python demos are deliberately zero-dependency. `z3-solver` and `hypothesis` could not be installed or demoed directly. |
| TLA+, Dafny, Z3, Rocq, Alloy, Kani not installed. | Those demos are readable specs with run instructions, not verified-by-execution artifacts. **Lean 4.32.0 *was* available, so the Lean demo is genuinely executable and was run.** |
| Current date at time of research: **12 Sept 2026**; Lean 4.32.0. | The 2025–2026 material is recent and, in places, still contested. |

---

## 2. Verified by execution (not just by reading)

These ran successfully in this environment:

| Artifact | Verification |
|---|---|
| `demos/lean/Demo.lean` | ✅ `lake build` succeeds; `#print axioms` output captured (see §Trusted base below) |
| `demos/lean/scripts/check-no-sorry.sh` | ✅ Exits 1 on `Planted.lean` (catches `sorry` + `axiom`), exits 0 on the honest file |
| `demos/python/dpll_sat.py` | ✅ SAT on the scheduling encoding; UNSAT on pigeonhole 3/2, 4/3, 5/4 |
| `demos/python/pbt_spec_gap.py` | ✅ `bad_sort` passes the weak spec and fails the strong spec, with a shrunk counterexample |
| `demos/python/temporal_monitor.py` | ✅ Catches 4 violations on the bad trace, 0 on the good trace; keyword guardrail produces a false alarm on the good trace and is blind on the bad one |
| `demos/tla/*.tla` | ⚠️ **Not executed** — TLC is not installed. Syntax and the counterexample traces were reasoned through by hand, including a corrected modelling bug (see §Corrections). |

**Notable captured output — the Lean trusted base:**

```
'myMax_ge_both' depends on axioms: [propext, Classical.choice, Quot.sound]
'append_nil'    depends on axioms: [propext]
'length_append' depends on axioms: [propext, Quot.sound]
```

That is a genuinely useful teaching artifact: even a one-line `omega` proof rests on classical
axioms.

---

## 3. Corrections made during the work (recorded deliberately)

These are worth keeping, because two of them are demos in their own right.

| # | Bug | Lesson |
|---|---|---|
| 1 | **My first TLA+ retry spec was broken.** The crash action required the request to still be in `inflight`, but the `Receive` action cleared it — so the crash was disabled and the spec would never have exhibited the bug it was written to demonstrate. | Modelling bugs are real and easy. A spec that "looks right" can be vacuous. This is why type invariants and sanity invariants (`TypeOK`) belong in every spec. |
| 2 | **My first DPLL scheduling encoding was unsatisfiable** (3 jobs into 2 slots with at-most-one-per-slot is pigeonhole-unsat). | A small modelling choice flips SAT to UNSAT. **Kept as a comment in the demo**, because it's exactly the class of thing TLA+/Alloy are used to catch. |
| 3 | **My first safety monitor enumerated `{delete, transfer}` and missed the unauthorized `erase`** — a synonym. | Kept deliberately in `temporal_monitor.py` as a documented lesson: *guardrails have specification bugs too.* State properties over **categories**, never over word lists. |
| 4 | My first Lean `myMax` proof used the wrong lemma; the demo now uses `split <;> omega`. | Minor; noted for completeness. |

**Pattern across 1–3:** the *property* was wrong three times and the *proof/search* was wrong zero
times. That is the specification gap showing up in the act of writing this repo, which is the most
honest possible evidence for this wiki's central claim.

---

## 4. Confidence ledger

### 🟢 High confidence — primary sources read directly

- AWS TLA+ experience report: all quotations verbatim from the paper/its detailed notes.
- Cedar: the Dafny-model + differential-random-testing pipeline, and the two proved properties
  (`explicit permit`, `forbid overrides permit`), from Amazon Science.
- seL4 numbers (8,700 lines C / 200,000 lines Isabelle / ~20 person-years) from
  verifiedsoftware.dev's case-study page.
- AlphaProof architecture (3B-param proof network, ~300k state–tactic pairs, ~1M informal → ~80M
  formal, TTRL, IMO 2024 result 28/42) from the *Nature* paper text.
- mathlib counts (288,041 theorems / 136,932 definitions / 772 contributors, Sept 2026) from the
  official stats page.
- OpenAI's ten results list from the `openai/ten-proofs` repository README.
- Kani's description and usage from its repository README.
- Comparator's mechanism (challenge vs solution module, axiom checking, `lean4export`, optional
  `nanoda` kernel) from its repository README.
- Rocq 9.0 rename date (12 March 2025) from rocq-prover.org.
- α,β-CROWN's five consecutive VNN-COMP wins from the competition site / project page.

### 🟡 Medium confidence — good source, but paraphrase or single-source risk

- **Adoption-gap claims.** I reference "empirical software-engineering work documenting
  hesitation/stereotypes" and the aerospace adoption surveys, but **did not pin a single specific
  study with a page citation.** ⚠️ *Pick one study and cite it precisely before relying on this.*
  Candidates to check: Woodcock et al. 2009 (ACM CSUR), Bicarregui et al. FM 2009, and the
  aerospace contractor/customer/certification-authority survey.
- **Astrée / Airbus A340** — the ~132,000 lines of C and "absence of runtime errors" are
  well-attested (Cousot et al., ESOP 2005). The precise **false-alarm rate** is hedged in the wiki
  as "low after domain-specific tuning". Don't repeat the number without reading the paper.
- **CompCert "zero bugs"** in the Csmith study — accurate for the version and (restricted C
  subset) tested. The wiki states this caveat explicitly. Keep the caveat if you use the number.
- **Harmonic Aristotle** "gold-medal-equivalent on IMO 2025 problems with Lean-verified proofs" —
  from an arXiv abstract (a vendor claim, self-reported). Hedged in the wiki with the source.
- **Leiden Declaration** — existence and general content confirmed; the claim that it was
  "endorsed by the IMU" comes from secondary reporting. ⚠️ verify.
- **Separation logic → 2025 ACM A.M. Turing Award** — asserted in
  `docs/01-fundamentals/logics.md` with an explicit ⚠️ *verify the exact citation before relying on
  it*. This one is plausible but was **not** confirmed against the ACM announcement.
- **"Verified RISC-V cores in Coq/Isabelle"** — flagged ⚠️ in the wiki as needing a check.

### 🔴 Low confidence — verify before repeating

| Item | Problem |
|---|---|
| Cedar "**~1 billion automated-reasoning checks per day**" | AWS-published scale figure; the wiki carries a ⚠️ and the number may have moved. Verify the current figure or say "billions" without a precise number. |
| OpenAI "**~$2,000** at API rates for all ten results" | **Secondary-source only** (reporting sites, not OpenAI). This is the most striking number in the wiki and therefore the most dangerous. Either verify it or drop it. |
| DARPA **CLARA ~$48M** | Secondary source. Verify or drop. |
| `Harrison verified Intel's division/square-root algorithms in HOL Light` | The *shape* is well known and widely cited; the wiki avoids naming specific papers. Confirm the exact reference before citing. |
| "**0–20% fully delegable**" (Anthropic 2026 report) | Vendor-published, and the exact methodology is unclear. The wiki labels it as vendor data and says "the gap is the point, not the precise number". Keep that framing. |
| mathlib "**~5 million lines**" | Came from a page *title*, not the official stats page (which gives declaration counts). Prefer the declaration counts. |
| Pentium FDIV "**~$475M**" | Widely repeated figure; treat as order-of-magnitude and flag it. |
| Knight Capital "**~$440M**" | Widely reported; verify before citing precisely. |
| Separation-logic Turing Award year | See 🟡 above — listed as needing verification. |

---

## 5. Gaps — what this repo does not yet contain

| Gap | Why it matters | Next step |
|---|---|---|
| **No diagrams/images** | Good diagrams are missing: the five-families map, the propose/check loop, the four AI-risk layers, the specification ladder, the inversion chart. All exist only as ASCII art. | Convert to SVG and check them into `docs/public/`. |
| **No recorded demo** | Live demos fail live. | Record `lake build` + `check-no-sorry.sh` + `pbt_spec_gap.py`. |
| **Only DuckDuckGo search available** | Narrower sourcing than ideal. | Re-run discovery with a funded provider; especially for the adoption-gap studies. |
| **TLA+ specs unexecuted** | Syntax is hand-verified, not machine-verified. | Install the TLA+ Toolbox and run `RetryIdempotency.tla` + `Mutex.tla`; paste the real TLC output into the files. |
| **No verified-code demo in Rust** | Kani is the most likely-to-be-adopted tool for this topic and has no demo. | Add `demos/rust/` with a `cargo kani` example. |
| **No translated version** | The wiki is English-only. | A Chinese translation would widen its reach considerably; see §7. |
| **No quiz/exercise** | A hands-on component would strengthen adoption. | Consider a 20-minute “write one property” exercise. |

---

## 6. Deliberate editorial choices

Recorded so they can be revisited:

1. **The wiki leads with counterexamples and admits limits early.** The `limits.md` and
   `adoption-gap.md` pages are placed before the AI-era payoff. This is intentional: technical
   engineers discount a technology pitch that hasn't stated its failure modes.
2. **AWS's framing is quoted verbatim and repeatedly.** "Debugging Designs" and "exhaustively
   testable pseudo-code" are treated as load-bearing, not as colour.
3. **Three of my own specification bugs were kept, not hidden.** They are the strongest available
   evidence for this wiki's central claim about the specification gap.
4. **Vendor claims are labelled as vendor claims.** Vendor scale figures (Cedar's check volume,
   Anthropic's delegation statistic) carry inline caveats rather than being dropped, because they
   are directionally useful and the direction is corroborated.
5. **Dijkstra's "testing shows the presence, not the absence, of bugs" is explicitly
   *anti*-recommended** in `references/quote-bank.md`, because it has been overused to the point of
   reflexive dismissal.
6. **No tool is recommended without a stated "pick this if".** The catalog avoids ranking tools by
   quality, because the right choice is determined by the artifact, not the tool.

---

## 7. Open questions

Editorial decisions that are **not** answerable from research, and where the wiki is thinnest:

1. **How much mathematics?** The pages assume you can read `{P}C{Q}` and `G(p → F q)`. A
   prose-only track for readers without that background would widen its reach considerably.
2. **Rust coverage.** Kani is the most likely-to-be-adopted tool for working engineers and has no
   demo. `demos/rust/` with a `cargo kani` example is the highest-value addition.
3. **Tool-choice depth.** `05-tools/choosing.md` gives heuristics but no worked examples. A
   "here is a real component and here is which tool I'd pick and why" walkthrough is missing.
4. **Verification economics.** The wiki asserts the cost curve has moved but carries no
   side-by-side cost data (engineer-days per rung, re-verification cost). That is the claim most
   in need of hard numbers.
5. **Failure case studies.** `limits.md` covers failure *modes*; it has few documented cases of
   verification projects that were abandoned or that shipped a bug anyway. Those exist and would
   be valuable.
6. **Translation.** English-only today.

---

## 8. Reproducing / extending this research

### Everything that runs

```bash
# The published wiki site (VitePress -> GitHub Pages)
npm ci                              # uses the repo .npmrc (public registry)
npm run docs:dev                    # local preview at /awesome-formal-methods/
npm run docs:build                  # static site -> docs/.vitepress/dist
python3 tools/check-site.py         # links in the BUILT site (see §9)

# The demos
cd demos/lean && lake build && ./scripts/check-no-sorry.sh
python3 demos/python/dpll_sat.py
python3 demos/python/pbt_spec_gap.py
python3 demos/python/temporal_monitor.py

# Markdown-level link check
python3 tools/check-links.py
```

All of the above run in CI on every push — see
[`.github/workflows/deploy-pages.yml`](https://github.com/yihuang/awesome-formal-methods/blob/main/.github/workflows/deploy-pages.yml) — and CI gates the
Pages deployment on them.

### Infrastructure gotchas worth knowing

1. **Never let a developer-level npm registry mirror reach `package-lock.json`.** This bit us hard.
   The machine that generated the lockfile had `~/.npmrc` pointing at a regional mirror, so all 173
   `resolved` URLs became plain-HTTP mirror URLs. In CI that surfaced as a 71-second hang followed
   by npm's deeply misleading `Exit handler never called!` (npm 10), and later as
   `EALLOWREMOTE: Fetching packages of type "remote" have been disabled` (npm 12). The fix is the
   project-level `.npmrc` pinning `registry=https://registry.npmjs.org/`, plus a CI guard that
   fails fast if the lockfile ever resolves elsewhere. **Regenerate with
   `rm -rf node_modules package-lock.json && npm install`.**
2. **`pip` is unavailable and PyPI is blocked in the authoring environment**, but the npm registry
   is reachable — hence zero-dependency Python demos and a Node-based site generator.
3. **Local and CI VitePress builds produce different asset hashes** (build-time data is included),
   so you cannot verify a deployed chunk by its local filename. Verify against the live URL instead.

### To widen the sourcing

Re-run discovery with a funded search provider, prioritising the 🟡 and 🔴 items in §4 and the
adoption-gap studies in §5.

---

## 9. Why there are two link checkers

They catch different bugs, and the second one was not optional — it found real breakage that
looked fine everywhere else:

| Script | Checks | Found |
|---|---|---|
| `tools/check-links.py` | relative links in Markdown source, GitHub-style heading anchors | 191 links; broke repeatedly during the `docs/` restructure |
| `tools/check-site.py` | links in the **built** HTML: base-path rewriting, VitePress-resolved anchors, hashed assets | **51 broken links that the Markdown checker could not see** |

What the site checker caught:

1. **VitePress slugs numbered headings differently from GitHub.** `## 1. Foo` became `_1-foo` on the
   site but `1-foo` on GitHub, silently breaking 14 cross-page anchors. Fixed by forcing one
   GitHub-compatible slugifier in `docs/.vitepress/config.mts`, so the same anchor works in both
   renderers. **This is the bug worth remembering** — every link looked correct in the source.
2. A footer link missing its `.html` suffix (36 occurrences across pages).
3. Base-path and asset-resolution problems that only exist post-build.

Final state: 2,462 internal links verified clean in the built site, plus a wget mirror of the
**deployed** site re-checked against the same script (2,458 links, clean).
