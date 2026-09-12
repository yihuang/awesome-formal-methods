# Formal Methods in the AI Era

**📖 Read the wiki: <https://yihuang.github.io/awesome-formal-methods/>**

A research-backed knowledge wiki that introduces **formal methods to engineers**, framed in the
**AI era**. Built to be read, linked, and cited.

> **The thesis.** For fifty years formal methods were the expensive, exotic option you reached for
> only in avionics and silicon. **The AI era inverted the economics.** Code is now cheap and
> abundant; *trustworthiness* is the scarce resource. Formal methods are the only technology we
> have that turns "I tested it and it seemed fine" into "this is true for **all** inputs, and a
> machine checked my argument."

**The hook:** the first AI program ever written — Logic Theorist, 1956 — *was* a theorem prover. AI
and formal methods share an origin. This wiki is about the loop between them.

---

## What's in here

| Section | Contents |
|---|---|
| **[Orientation](docs/00-orientation/)** | Why now · taxonomy of the field · reading paths by role |
| **[Fundamentals](docs/01-fundamentals/)** | Specifications · logics · **semantics (small-step, big-step, functional/relational)** · **temporal logic (safety, liveness, stuttering)** · the five verification techniques · SAT/SMT · hard limits |
| **[History](docs/02-history/)** | Dated timeline 1666→2026 · the three-act narrative |
| **[Applications](docs/03-applications/)** | seL4, CompCert, AWS TLA+, Cedar, SymCrypt, VNN-COMP · **blockchain/EVM/zk** · distributed systems · hardware & crypto · safety-critical · **the lightweight on-ramp** · the adoption gap |
| **[AI era](docs/04-ai-era/)** | **AI → FM** (AlphaProof, autoformalization, the 2026 machine-checked results) · **AI proof engineering** (generic models writing Lean 4) · **FM → AI** (agent guardrails, NN verification, runtime monitors) · the verification bottleneck |
| **[Tools](docs/05-tools/)** | ~40 tools in nine families · how to choose · **model verifiers: TLA+ / Ivy / Veil** |
| **[Practice](docs/06-practice/)** | Adoption playbook (0→3 ladder) · objection handling |
| **[Reference](docs/references/)** | Citation conventions · glossary · bibliography · sourced quote bank |
| **[Demos](docs/demos.md)** | Runnable Lean, Python, and TLA+ artifacts |
| **[Presenting](docs/appendix/presenting.md)** | *Optional appendix* — timings and narrative spines |

Plus **[Research notes](docs/research-notes.md)** — the confidence ledger: what's verified, what's
flagged `⚠️`, and what this repo gets wrong.

---

## Coverage contract

The wiki is deliberately built along four axes, so no reader gets only one half of the picture.

| Axis | Left pole | Right pole |
|---|---|---|
| Depth | Fundamentals | Applications |
| Time | History | Recent developments |
| Mode | Theory | Practical |
| Framing | — | The AI era, woven through all of it |

---

## Run it locally

```bash
# The wiki site (VitePress)
npm ci
npm run docs:dev        # http://localhost:5173/awesome-formal-methods/
npm run docs:build      # static site -> docs/.vitepress/dist
npm run docs:preview

# The demos — Lean 4 is genuinely executed, not just quoted
cd demos/lean && lake build
cd demos/lean && ./scripts/check-no-sorry.sh   # exits 1 by design (catches Planted.lean)

# The demos — zero dependencies, no install
python3 demos/python/dpll_sat.py
python3 demos/python/pbt_spec_gap.py
python3 demos/python/temporal_monitor.py
```

## Quality gates

Everything below runs in CI on every push (see
[`.github/workflows/deploy-pages.yml`](.github/workflows/deploy-pages.yml)):

| Gate | What it catches |
|---|---|
| `python3 tools/check-links.py` | broken relative Markdown links |
| `python3 tools/check-refs.py` | reference coverage — a ratchet: every page must keep a `## References` section |
| `npm run docs:build` | VitePress dead links; **fails the build** |
| `python3 tools/check-site.py` | broken links in the *built* site — base-path, anchor, and asset problems the Markdown checker can't see (2,462 links checked) |
| `lake build` | the Lean proofs actually compile |
| `./scripts/check-no-sorry.sh` | **`sorry` and axiom smuggling** — and CI asserts the gate both *rejects* `Planted.lean` and *accepts* the honest proof |
| Python demos | the SAT solver, property-based testing, and agent monitor run |

Notably, `check-site.py` caught a class of bug that looks fine on GitHub: VitePress slugs numbered
headings as `_1-foo` while GitHub uses `1-foo`, silently breaking every cross-page anchor on the
site. The fix was to force one GitHub-compatible slug convention in
[`docs/.vitepress/config.mts`](docs/.vitepress/config.mts) so the same link works in both renderers.

---

## Two things worth knowing before you cite anything

1. **Numbers flagged `⚠️` in the text are unverified.** The
   [confidence ledger](docs/research-notes.md) has a 🟢/🟡/🔴 breakdown. In particular the OpenAI
   "~$2,000" figure is secondary-source only, and Cedar's "~1 billion checks/day" needs a current
   source.
2. **Three specification bugs I made while writing this are kept as demo material**, because they
   are the most honest available evidence for the wiki's central claim. The best one: my first agent
   guardrail enumerated `{delete, transfer}` and **missed an unauthorized `erase`** — a synonym.
   Guardrails have specification bugs too.

> Formal methods cannot tell you what to want. They can tell you, with certainty, whether what you
> asked for is what you'll get — and show you the exact input where it isn't.

---

## Contributing

Corrections to the confidence ledger are the most valuable contribution — especially for the 🟡 and
🔴 items. If you add a claim, add its source.

---

## License

This repository is **dual-licensed**, because the prose and the code are useful under different
terms:

| Content | License |
|---|---|
| **Prose** — everything under [`docs/`](docs/) and this README | [CC BY 4.0](LICENSE-docs) — read, quote, remix, and translate freely with attribution |
| **Code** — [`demos/`](demos/), [`tools/`](tools/), the workflows, and the site build config | [MIT](LICENSE) — use it however you like |

Attribution for the prose: *"yihuang, Formal Methods in the AI Era"* with a link to
<https://github.com/yihuang/awesome-formal-methods>.

If you reuse a case study's numbers, credit the **primary source** rather than this wiki — every
figure is linked to where it came from, and a few are flagged as unverified in the
[confidence ledger](docs/research-notes.md).
