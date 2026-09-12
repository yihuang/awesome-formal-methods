# Formal Methods in the AI Era — a talk-prep wiki

A research-backed knowledge base for preparing a **big tech-sharing talk** that introduces
**formal methods to engineers**, framed in the **AI era**.

This repo is deliberately *not* the slides. It is the shared substrate of raw material that the
slides get distilled from: fundamentals, history, applications, tooling, and the AI-era story,
with sources attached so claims survive scrutiny.

> **Status:** early/collection phase. Content is drafted from primary sources and marked with
> confidence where it matters. See [`RESEARCH-NOTES.md`](RESEARCH-NOTES.md) for provenance,
> gaps, and open questions.

---

## The thesis of the talk (working)

> For fifty years formal methods were the expensive, exotic option you reached for only in
> avionics and silicon. **The AI era inverted the economics.** Code is now cheap and abundant;
> *trustworthiness* is the scarce resource. Formal methods are the only technology we have that
> turns "I tested it and it seemed fine" into "this is true for **all** inputs, and a machine
> checked my argument."

Two directions, and the talk should carry both:

| Direction | Meaning | Examples |
|---|---|---|
| **AI → FM** | AI as an *accelerator* for formal methods | Autoformalization, neural theorem proving, Lean/mathlib agents, AI-assisted invariant discovery |
| **FM → AI** | Formal methods as *guardrails* for AI | Verifying LLM-generated code, agent policy enforcement, neural-network robustness certificates, provably-safe RL shielding |

A historical hook worth using: the **first AI program ever written** (Logic Theorist, 1956) *was*
a formal-reasoning program. The two fields did not converge recently — they started entangled.
See [`docs/02-history/narrative.md`](docs/02-history/narrative.md).

---

## Coverage mandate

The talk must cover four axes. This table is the **completeness contract** — no cell may be
empty by the end.

| Axis | Left pole | Right pole | Where it lives |
|---|---|---|---|
| **Depth** | Fundamentals | Applications | [`docs/01-fundamentals/`](docs/01-fundamentals/) ↔ [`docs/03-applications/`](docs/03-applications/) |
| **Time** | History | Recent developments | [`docs/02-history/`](docs/02-history/) ↔ [`docs/04-ai-era/`](docs/04-ai-era/) |
| **Mode** | Theory | Practical | [`docs/01-fundamentals/`](docs/01-fundamentals/) ↔ [`docs/05-tools/`](docs/05-tools/), [`docs/06-practice/`](docs/06-practice/) |
| **Framing** | — | **The AI era** | [`docs/04-ai-era/`](docs/04-ai-era/), woven through everything |

---

## Map of the wiki

```
docs/
  00-orientation/    Why now · taxonomy of the field · reading paths for different audiences
  01-fundamentals/   Specifications · logics · techniques · solvers · hard limits
  02-history/        Timeline (1880s→2026) · the narrative arc
  03-applications/   Case studies · distributed systems · hardware & crypto · safety-critical
                     · lightweight FM (the on-ramp) · the adoption gap (why it stalled)
  04-ai-era/         AI-for-FM · FM-for-AI · the verification bottleneck
  05-tools/          Tool catalog · how to choose
  06-practice/       Adoption playbook for a normal team · objection handling
references/          Glossary · bibliography · quote bank
slides/              Talk outlines by duration (30 / 45 / 60 min) + narrative arc
demos/               Runnable artifacts (Lean is installed in this environment)
```

**Start here:** [`docs/README.md`](docs/README.md) → [`docs/00-orientation/why-now.md`](docs/00-orientation/why-now.md)

---

## Conventions used in this wiki

- **Claims carry sources.** Inline links point to primary sources (papers, official docs,
  project sites) rather than blog summaries where possible. See
  [`references/bibliography.md`](references/bibliography.md).
- **Confidence marking.** Where a number or claim is uncertain, it is marked
  `⚠️ unverified` or `~approx`. Numbers that came from a vendor's own marketing are noted as such.
- **Two audiences per page.** Most pages open with a **TL;DR for engineers** (no math) and then
  go deeper for the technically curious. The talk uses the former; the appendix uses the latter.
- **Talk-ready quotes** get collected in [`references/quote-bank.md`](references/quote-bank.md).

## Environment (verified)

| Tool | Status |
|---|---|
| Lean 4 | ✅ installed (`lean 4.32.0`, `lake`) — demos are runnable here |
| Python 3, Node | ✅ installed — solver / property-based-testing demos possible |
| TLA+, Dafny, Z3, Coq, Alloy | ❌ not installed — specs are readable/writable, not runnable without setup |

## Quality gates (all green)

```bash
python3 tools/check-links.py              # 190 internal links, all resolve
cd demos/lean && lake build               # Lean 4.32.0, builds clean
cd demos/lean && ./scripts/check-no-sorry.sh   # exits 1 by design — catches Planted.lean
python3 demos/python/dpll_sat.py
python3 demos/python/pbt_spec_gap.py
python3 demos/python/temporal_monitor.py
```

See [`RESEARCH-NOTES.md`](RESEARCH-NOTES.md) for the confidence ledger: which facts are 🟢 verified
from primary sources, which are 🟡/🔴 and need checking before they reach a slide, and which of my
own specification bugs got kept as demo material.

## Roadmap

- [x] Repo scaffold, orientation, fundamentals, history
- [x] Applications, case studies, adoption gap
- [x] AI-era (both directions)
- [x] Tool catalog, practice playbook, glossary, bibliography
- [x] Slide outlines by duration (30 / 45 / 60 min)
- [x] Runnable demos: Lean (verified by `lake build`), zero-dependency Python ×3, TLA+ specs
- [x] Internal link checker + honest confidence ledger
- [ ] Diagrams/visuals for the 5 key slides (described in text)
- [ ] Recorded demo fallback (live demos fail live)
- [ ] Rehearsal + measured timing pass
- [ ] Decide the final narrative spine (two candidates in `slides/outline.md`)
- [ ] Resolve the 8 open questions in `RESEARCH-NOTES.md` §7 (audience, length, language, …)
