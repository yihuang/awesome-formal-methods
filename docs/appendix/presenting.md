# Appendix: presenting this material

> **Optional appendix.** Everything else in this wiki is a standalone knowledge base — you can
> read it, link to it, and cite it without ever thinking about a presentation. **This page is
> different.** It is for readers who want to *present* the material: a tech talk, a brown-bag
> session, a reading group, or an internal training slot. Skip it if that isn't you.

The wiki is organised as knowledge, not as a script. This appendix reorganises the same material
into a narrative with timings. Two things to know before you use it:

- **Pick one spine and commit.** Mixing them produces a survey, not a talk.
- **Every claim traces back to a wiki page.** If a slide needs more depth than the outline gives,
  follow the link — that is the point of having the wiki behind the deck.

---

## Title options

| Title | Framing | Best for |
|---|---|---|
| **"AI Made Code Cheap. Trust Is Still Expensive."** | economic | a general engineering audience; strongest hook |
| **"Formal Methods in the AI Era: The Missing Half of AI-Assisted Engineering"** | complementarity | a technically curious audience |
| **"What About All the Inputs You Didn't Try?"** | testing-gap | the most concrete, least jargon-y |
| **"Debugging Designs: 50 Years of Proof Finally Meets Its Moment"** | historical | a mixed/senior audience |

**Suggested:** #1 for the title slide, #3 as the subtitle.

---

## The two candidate narrative spines

Pick one and commit; mixing them produces a survey, not a talk.

### Spine A — "The economics changed" (recommended)

```
  1. Hook: the first AI program was a theorem prover
  2. The inversion: generation cheap, verification expensive
  3. What formal methods actually are (the map + the ladder)
  4. It works: 3 case studies
  5. AI → FM: AlphaProof, and 2026's machine-checked mathematics
  6. FM → AI: the guardrail problem
  7. Honesty: limits, and why it didn't reach you
  8. The ask: one rung, one day
```

**Why it works:** the audience arrives thinking "why now?" and leaves with an action. Every
section answers a question the previous section raised.

### Spine B — "The 70-year reunion"

```
  1. Act I:   we found the ceiling (1931–1975)
  2. Act II:  it worked, and nobody noticed (1977–2019)
  3. Act III: AI flipped the economics (2020–2026)
  4. The ask: one rung, one day
```

**Why it works:** the historical arc is genuinely surprising (Logic Theorist), and it positions FM
as a mature field rather than a fad. **Risk:** less actionable; you must still land the ask.

**Recommendation:** Spine A for a 45–60 min slot; Spine B for 30 min or a senior/mixed audience.

---

## 30 minutes — Spine A, tight

| # | Slide | Min | Content | Key line |
|---|---|---|---|---|
| 1 | Title | 0.5 | "AI Made Code Cheap. Trust Is Still Expensive." | — |
| 2 | **The hook** | 1 | Logic Theorist, 1956: the first AI program was a theorem prover | "AI and formal methods share an origin." |
| 3 | **The inversion** | 2 | generation $$ → ¢; verification unchanged; the 60%/0–20% gap | "Verification is the bottleneck." |
| 4 | **What it is** | 3 | The map: 5 families. The four dials. | "Five ways to establish a guarantee." |
| 5 | **The key asymmetry** | 2 | find = hard, check = cheap | "AI proposes; the kernel disposes." |
| 6 | **Case: AWS TLA+** | 3 | "Debugging Designs", "exhaustively testable pseudo-code", the two quotes | "FM is an enabler, not insurance." |
| 7 | **Case: CompCert** | 1.5 | GCC/LLVM: hundreds of bugs. CompCert: zero. | "Verify the tool, not just the artifact." |
| 8 | **Case: Cedar** | 2.5 | Dafny model + differential random testing; ~1B checks/day ⚠️ | "Prove the model, test the gap." |
| 9 | **AI → FM** | 3 | AlphaProof: IMO silver 28/42, Lean as reward; 2026: ten new results with Lean certificates | "New mathematics, machine-checked." |
| 10 | **FM → AI** | 3 | 4 layers; AgentSpec; Bedrock automated reasoning; "credit card checks" | "Sound guardrails where evals can't reach." |
| 11 | **Honesty** | 2.5 | Spec gap; Rice's theorem; what FM can't do; why it didn't reach you | "Precision, not omniscience." |
| 12 | **The ask** | 2 | The ladder: rung 1 costs a day; the 5 things to do first week | "One property, one function, one day." |
| 13 | Closing | 0.5 | "AI made code free. It didn't make correctness free." | — |

**Cut first if over time:** slide 7 (CompCert detail), then the four-dials part of slide 4.

---

## 45 minutes — Spine A, full

Same as the 30-minute version, with these additions:

| # | Slide | Min | Adds |
|---|---|---|---|
| +4b | **The five families** | 4 | theorem proving / model checking / deductive / abstract interpretation / types — with what each is *good at* and *how it fails* |
| +9b | **Autoformalization & the judging layer** | 3 | the 1M→80M pipeline; **statement mismatch**; Comparator + nanoda (independent kernel) |
| +11b | **Demonstration** | 4 | live: property-based test finding a shrunk counterexample, and/or a Lean proof compiling |
| +12b | **Adoption playbook** | 3 | rungs 0–3, metrics that work, when to stop |
| +12c | **Objection handling** | 3 | pick the top 4 from [objections.md](../06-practice/objections.md) |
| +13b | **Q&A pre-empt** | — | put the limitations slide *before* Q&A, not after |

**Timing warning:** the demo is the riskiest segment. Rehearse it, pre-run it, and have a recorded
backup. See [`demos/`](../demos.md).

---

## 60 minutes — Spine A + playbook depth

Add to the 45-minute version:

| # | Slide | Min | Adds |
|---|---|---|---|
| +3b | **The specification ladder** | 3 | rungs 0–5; the Dafny `Abs` contract example; the "sort" spec-gap illustration |
| +6b | **Distributed systems deep dive** | 4 | the retry/idempotency crash-between-statements bug; quorum intersection; TLC counterexample traces |
| +8b | **Second case: seL4 or SymCrypt** | 3 | the refinement ladder; "stable, shared, catastrophic" as a target heuristic |
| +10b | **Verification bottlenecks & metrics** | 3 | the verification gap; why LLM-reviewing-LLM fails (correlated errors) |
| +12d | **Exit criteria & scope discipline** | 2 | when to stop; scoping as the actual skill |

---

## Slide-by-slide content notes

### Slide 2 — The hook
- **Visual:** Logic Theorist, 1956. Principia Mathematica. "38 of the first 52 theorems."
- **Say:** "The first AI program ever written was a theorem prover. Which means AI and formal
  methods aren't rivals. They were born in the same room. This talk is about the loop between
  them — and why that loop is now the most valuable thing in software engineering."
- **Why this works:** it's genuinely surprising, it's true, and it reframes the whole talk in 30
  seconds.

### Slide 3 — The inversion
- **Visual:** two bars. Generation cost: tall → tiny. Verification cost: unchanged.
- **Numbers:** the 60%-use / 0–20%-delegable gap. Label it as a vendor figure.
- **Say:** "Amdahl's law. You sped up one stage by 10× and left the next one alone. The next one
  now sets your throughput ceiling. That stage is verification."

### Slide 4 — The map
- **Visual:** the five-families diagram from
  [techniques.md](../01-fundamentals/techniques.md), or the simpler decision tree.
- **Say:** "Five ways to establish a guarantee. They differ in who supplies the ingenuity and how
  they fail. You'll never need more than two of them."
- **Do not** enumerate all 40 tools. Name five.

### Slide 5 — The asymmetry (the most important conceptual slide)
- **Visual:** `FIND a proof → expensive` / `CHECK a proof → cheap`.
- **Say:** "This asymmetry is the shape of a neural network's strengths and weaknesses. LLMs
  propose brilliantly and guarantee nothing. Kernels guarantee everything and create nothing. Put
  them in a loop."
- **This is the thesis slide.** Spend time here and refer back to it.

### Slide 6 — AWS TLA+
- **Visual:** the two quotes, large. Name the systems: S3, DynamoDB, EBS.
- **Say:** the cost-objection quote first ("quite wrong"), then the enabler quote ("would not have
  dared to do"). Then: "They called their internal talk 'Debugging Designs'. Steal that."
- **Land the reframe:** insurance gets cut; enablers get funded.

### Slide 9 — AI → FM
- **Visual:** the propose/check loop diagram.
- **Left column (2024–25):** AlphaProof, IMO silver, 28/42, *Nature*, "Lean as the reward."
- **Right column (2026):** Ten new results, each open ≥10 years, **with Lean certificates**.
- **Say:** "This is the loop, running at research level. And note the honest part: the proofs are
  machine-checked, which is not the same as being accepted. The arguments in mathematics are now
  about attribution and process — because the correctness argument is largely settled by the
  kernel. That's a remarkable place for a field to be."
- **Caveats slide or speaker note:** not peer-reviewed at announcement; internal model;
  [Leiden Declaration](../04-ai-era/ai-for-fm.md#4-2026-new-mathematics-with-machine-checked-certificates).

### Slide 10 — FM → AI
- **Visual:** the four-layer table (model / output / action / system).
- **Best single quote:** "The AI agent is required to generate formal proofs demonstrating the
  safety of planned actions before being authorized to execute them… parallels existing
  real-world practices (e.g. credit card checks before a transaction is authorized)."
- **Say:** "You already do proof-carrying authorization in finance. AI just changed the author."
- **The sharpest argument:** classifiers and LLM-judges fail in *correlated* ways with the model
  they guard. Formal checks fail differently. In an AI-saturated pipeline, the marginal checker
  must be orthogonal.

### Slide 11 — Honesty
- **Visual:** a two-column table: "what FM guarantees" / "what it does not."
- **Say:** the specification gap, Rice's theorem (one sentence), the verified-systems-have-failed
  file (FDIV, Ariane 5, Knight Capital), and AWS's own scope statement: FM addresses (1) logic
  bugs, not (2) emergent performance degradation.
- **Then the adoption-gap line:** "This field is 50 years old and it mostly didn't reach you. That's
  the honest part, and here's why: it delivered where failure was catastrophic and the artifact was
  small. The AI era changes the second half of that."
- **This slide buys credibility for everything else.** Put it *before* Q&A.

### Slide 12 — The ask
- **Visual:** the rung ladder, with rung 1 and rung 4 highlighted.
- **Say:** the 5 things, ending with: "Write one TLA+ spec of a design you're currently arguing
  about in review comments. Two hours. Bring the counterexample to the design meeting. That's the
  step that converts your team."
- **Give them the checklist page** ([adoption-playbook.md](../06-practice/adoption-playbook.md)).

---

## Backup / appendix slides (have these ready, don't present them)

| Slide | Use when asked |
|---|---|
| **The five logics** | "what language are the specs in?" |
| **How SAT/SMT solvers work** | a systems-audience follow-up; CDCL, watched literals, DRAT proof logging |
| **The proof-to-code ratio table** | "how expensive is it really?" |
| **The tool catalog** | "what should I install?" |
| **DO-178C/DO-333** | "how does certification work?" |
| **The verified-systems-have-failed file** | "has a verified system ever broken?" |
| **The Leiden Declaration & AI-math governance** | "should we trust AI math results?" |
| **The 6 selection heuristics** | "how do I choose?" |
| **Cost/benefit table** | a manager in the room |

---

## Delivery notes

1. **Lead with counterexamples, not proofs.** Every segment that lands well is one where a
   concrete artifact appears: a failing trace, a shrunk counterexample, a bug someone recognises.
   A proof on a slide is a claim; a counterexample is evidence.
2. **Say "debugging designs" and "exhaustively testable pseudo-code".** The framing from AWS is
   load-bearing for adoption.
3. **Put the limitations slide before Q&A.** Audiences forgive stated limits and punish discovered
   ones.
4. **Concede the objections you can't win:**
   - Yes, the spec gap is permanent.
   - Yes, it's expensive for whole systems.
   - Yes, it mostly didn't reach you.
   - Yes, AI math results are contested on process.
   Each concession makes the following claim more credible.
5. **Use the honest AlphaProof detail** — "the two combinatorics problems remained unsolved." It
   costs nothing and it buys everything.
6. **Name one number you're unsure about as unsure.** Actually say "I've seen this quoted at
   around a billion a day — I haven't verified the current figure." Audiences trust calibrated
   speakers.
7. **Do not quote Dijkstra's testing line.** It's been used to dismiss testing so often that
   audiences discount it reflexively. See
   [quote-bank.md](../references/quote-bank.md#the-one-quotation-to-avoid).

---

## Rehearsal checklist

```
[ ] Demo runs from a clean shell (pre-run it; record a backup GIF)
[ ] All ⚠️-flagged numbers either verified or hedged out loud
[ ] Every quote has a visible attribution on the slide
[ ] The limitations slide appears BEFORE Q&A
[ ] The ask is a single, specific, one-day action
[ ] Timed at target length with 10% slack
[ ] Backup slides loaded for the 5 likeliest questions
[ ] A manager in the audience has a cost/benefit slide available
[ ] The closing line is memorised, not read
```

---

## Related material

- Narrative with hooks and delivery cues: [docs/02-history/narrative.md](../02-history/narrative.md)
- Quote bank: [references/quote-bank.md](../references/quote-bank.md)
- Q&A prep: [docs/06-practice/objections.md](../06-practice/objections.md)
- Demos: [demos/](../demos.md)
