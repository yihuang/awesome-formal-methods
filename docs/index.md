---
layout: home

hero:
  name: Formal Methods in the AI Era
  text: A wiki for engineers
  tagline: AI made code cheap. Trust is still expensive. Fifty years of verification research finally has an economic reason to reach your team.
  actions:
    - theme: brand
      text: Why now?
      link: /00-orientation/why-now.html
    - theme: alt
      text: The 30-minute tour
      link: /00-orientation/reading-paths.html
    - theme: alt
      text: GitHub
      link: https://github.com/yihuang/awesome-formal-methods

features:
  - title: The core asymmetry
    details: Finding a proof is hard; checking one is cheap. That is why AI proposes and kernels dispose — and why a 1956 idea is suddenly the missing half of AI-assisted engineering.
  - title: It already shipped
    details: seL4, CompCert, AWS's control planes, Cedar at a billion checks a day, your browser's TLS. Formal methods are not a proposal; they are infrastructure you never noticed.
  - title: The honest version
    details: Rice's theorem, the specification gap, the adoption gap, and the verified systems that have failed. The limitations are on the page before the sales pitch.
  - title: Runnable, not just readable
    details: A Lean 4 project that builds, three zero-dependency Python demos, and TLA+ specs. Every claim that could be executed, was.
---

## The thesis

> For fifty years formal methods were the expensive, exotic option you reached for only in avionics
> and silicon. **The AI era inverted the economics.** Code is now cheap and abundant;
> *trustworthiness* is the scarce resource. Formal methods are the only technology we have that
> turns "I tested it and it seemed fine" into "this is true for **all** inputs, and a machine
> checked my argument."

Two directions, and this wiki carries both:

| Direction | Meaning | Examples |
|---|---|---|
| **AI → FM** | AI as an *accelerator* | Autoformalization, neural theorem proving, Lean/mathlib agents, invariant suggestion |
| **FM → AI** | FM as *guardrails* | Verifying LLM-written code, agent policy enforcement, certified robustness, provably-safe RL |

The historical hook: the **first AI program ever written** — Logic Theorist, 1956 — *was* a theorem
prover. The two fields did not converge recently; they started entangled. See
[the narrative arc](./02-history/narrative.md).

---

## Map of the wiki

### Orientation — get the shape of the field first

| Page | What it answers |
|---|---|
| [Why now?](./00-orientation/why-now.md) | Why does this matter *now*, and why should an engineer care? |
| [Taxonomy of the field](./00-orientation/taxonomy.md) | What actually counts as "formal methods"? The four dials. |
| [Reading paths](./00-orientation/reading-paths.md) | Routes through this wiki by role and by talk length. |

### Fundamentals — the durable ideas

| Page | What it answers |
|---|---|
| [Specifications](./01-fundamentals/specifications.md) | What is a specification, and why is writing one the hard part? |
| [Logics](./01-fundamentals/logics.md) | Hoare, separation, temporal, type theory, μ-calculus. |
| [Semantics](./01-fundamentals/semantics.md) | Small-step, big-step, functional vs relational, denotational, axiomatic — and how to mechanise a language definition. |
| [Techniques](./01-fundamentals/techniques.md) | The five families of verification, and how each one fails. |
| [Automated reasoning](./01-fundamentals/automated-reasoning.md) | SAT, SMT, CDCL, DRAT — the engine under everything. |
| [Limits](./01-fundamentals/limits.md) | Gödel, undecidability, Rice's theorem, the specification gap. |

### History — how we got here

| Page | What it answers |
|---|---|
| [Timeline 1666–2026](./02-history/timeline.md) | Dated spine, with "why it matters" for each entry. |
| [The narrative arc](./02-history/narrative.md) | Three acts, one twist, one moral. |

### Applications — where it actually shipped

| Page | What it answers |
|---|---|
| [Case studies](./03-applications/case-studies.md) | seL4, CompCert, AWS TLA+, Cedar, SymCrypt, Veil, VNN-COMP — with numbers and caveats. |
| [Blockchain, EVM & zk](./03-applications/blockchain.md) | The EVM's Lean semantics, verified compilers, zkVM verification, and why verification is a licence to optimise. |
| [Distributed systems](./03-applications/distributed-systems.md) | The best ROI in the field, and why. |
| [Hardware & cryptography](./03-applications/hardware-crypto.md) | Where FM is already standard practice. |
| [Safety-critical](./03-applications/safety-critical.md) | DO-178C/DO-333, certification credit, and the stereotype to dismantle. |
| [Lightweight FM](./03-applications/lightweight-fm.md) | **The on-ramp.** Your one-step move, with code. |
| [The adoption gap](./03-applications/adoption-gap.md) | Why a 50-year-old technology mostly didn't reach you. |

### AI era — the framing that makes this timely

| Page | What it answers |
|---|---|
| [The bidirectional map](./04-ai-era/index.md) | Both directions in one page. |
| [AI → FM](./04-ai-era/ai-for-fm.md) | AlphaProof, autoformalization, the 2026 machine-checked results, and what doesn't work. |
| [AI proof engineering](./04-ai-era/llm-proof-engineering.md) | Generic frontier models now write Lean 4 — benchmarks, the spec-is-the-review workflow, and how it fails. |
| [FM → AI](./04-ai-era/fm-for-ai.md) | Agent guardrails, NN verification, LLM-code verification, runtime monitors. |
| [The verification bottleneck](./04-ai-era/verification-bottleneck.md) | The economics: generation got cheap, verification didn't. |

### Tools & practice — what to actually type

| Page | What it answers |
|---|---|
| [Tool catalog](./05-tools/catalog.md) | ~40 tools in nine families, with "pick this if". |
| [Choosing a tool](./05-tools/choosing.md) | Decision tree, heuristics, install commands. |
| [Adoption playbook](./06-practice/adoption-playbook.md) | The 0→3 ladder, with cost and payoff at each rung. |
| [Objections & answers](./06-practice/objections.md) | Ten objections, answered honestly. |
| [Runnable demos](./demos.md) | Lean, Python, and TLA+ artifacts — two of three run with no dependencies. |
| [Presenting this material](./appendix/presenting.md) | **Optional appendix** — timings and narrative spines if you want to present the wiki's content. |

### Reference

| Page | Contents |
|---|---|
| [Citation conventions](./references/index.md) | How references and confidence marking work in this wiki. |
| [Glossary](./references/glossary.md) | Every term, defined once. |
| [Bibliography](./references/bibliography.md) | Papers, books, courses, tools. |
| [Quote bank](./references/quote-bank.md) | Sourced, quotable lines. |
| [Research notes](./research-notes.md) | **The confidence ledger**: what's verified, what's flagged, and what this repo gets wrong. |

---

## The coverage contract

The wiki is deliberately built along four axes, so that no reader gets only one half of the picture.

| Axis | Left pole | Right pole |
|---|---|---|
| **Depth** | Fundamentals | Applications |
| **Time** | History | Recent developments |
| **Mode** | Theory | Practical |
| **Framing** | — | The AI era, woven through all of it |

---

## Quality gates

This repo is verified, not just asserted. Everything below runs:

```bash
npm run docs:build                 # VitePress site build (fails on dead links)
python3 tools/check-links.py       # internal link checker
python3 tools/check-refs.py        # every page has references; ratcheted at 0 gaps
python3 tools/check-site.py        # links in the BUILT site (base paths, anchors, assets)
cd demos/lean && lake build        # Lean 4.32.0 — builds clean
cd demos/lean && ./scripts/check-no-sorry.sh   # exits 1 by design (catches Planted.lean)
python3 demos/python/dpll_sat.py
python3 demos/python/pbt_spec_gap.py
python3 demos/python/temporal_monitor.py
```

## How to read this

- **I want to use this at work** → [Lightweight FM](./03-applications/lightweight-fm.md) → [Choosing a tool](./05-tools/choosing.md) → [Adoption playbook](./06-practice/adoption-playbook.md)
- **You're an AI/ML engineer** → [The verification bottleneck](./04-ai-era/verification-bottleneck.md) → [FM → AI](./04-ai-era/fm-for-ai.md)
- **You're sceptical** → [The adoption gap](./03-applications/adoption-gap.md) → [Limits](./01-fundamentals/limits.md) → [Objections](./06-practice/objections.md)

## Status and license

A living wiki. Claims carry sources; numbers that need checking are flagged `⚠️` **in the text**,
and aggregated in the [confidence ledger](./research-notes.md). Corrections are welcome — the
ledger exists precisely so that nobody has to guess whether a figure is solid. Known gaps are
listed there too.

**Prose** is licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — quote, remix, and
translate it with attribution. **Code** (the [demos](./demos.md) and tooling) is
[MIT](https://opensource.org/license/mit).

If you reuse a case study's numbers, credit the **primary source** rather than this wiki.

**One closing line:**

> Formal methods cannot tell you what to want. They can tell you, with certainty, whether what you
> asked for is what you'll get — and show you the exact input where it isn't.
