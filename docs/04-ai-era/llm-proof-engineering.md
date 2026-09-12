# AI proof engineering: generic models write Lean now

> **TL;DR.** Something changed in 2025–2026 that most formal-methods material has not caught up
> with: **general-purpose frontier models write usable Lean 4**. Not "specialized provers are
> improving" — generic models, the same ones you already use for code, are now among the best
> available tools for machine-checked proof. The best reported result on the standard benchmark is a
> general model at **92%**, and cheap open models produce correct proofs for **under a cent each**.
>
> The consequence is a workflow inversion. The scarce resource is no longer *writing the proof*. It
> is **writing the specification** — and reviewing it. Which means the bottleneck in AI-assisted
> software has moved to exactly the thing formal methods has always been about.

---

## The evidence

### The benchmark comparison

The most directly relevant study is a June 2026 comparison of LLM performance on **Lean 4** proof
generation, evaluated on subsets of **miniF2F** and **miniCTX** using `pass@k` and `refine@k`
metrics ([arXiv:2606.05632](https://arxiv.org/abs/2606.05632)):

| Model | Result |
|---|---|
| **Gemini 3.1 Pro** (general-purpose) | **92%** on miniF2F at `refine@32` |
| **Claude Opus 4.7** (general-purpose) | **86%** on miniCTX at `refine@32` |
| **NVIDIA Nemotron 3 Super**, **GPT-OSS 120B** | most cost-efficient: competitive accuracy at **< $0.01 per correct proof** |

Three things to notice, and all three are the point:

1. **The winners are general-purpose models**, not Lean-specialized provers. The paper contrasts
   "general-purpose frontier models, e.g. Google Gemini 3.1 Pro" against "Lean specialized models,
   e.g. …" — and the general models come out on top.
2. **`refine@k` is the metric that matters operationally.** `pass@k` asks "can the model solve this
   from scratch." `refine@k` asks "given the compiler's error message, can it fix its attempt" —
   which is the actual interactive loop a human does, and the actual loop an agent runs.
3. **Under a cent per correct proof** is a price at which proof search stops being rationed. Even if
   you distrust the number, the order of magnitude changes what is worth attempting.

**Caveat worth stating:** benchmark performance on miniF2F-style problems is not the same as
proving novel research mathematics or verifying a real Rust codebase. miniF2F is olympiad-level and
saturated; passing it does not mean the model can find the invariant in *your* protocol.

### The specialised systems, for contrast

| System | What it is | Result |
|---|---|---|
| **AlphaProof** (DeepMind) | RL agent inside Lean, 3B-parameter proof network, AlphaZero-style search, trained on ~80M autoformalized problems | IMO 2024: silver-medal level (28/42) |
| **Aristotle** (Harmonic) | specialised prover product | gold-medal-equivalent on IMO 2025 problems, Lean-verified |
| **Goedel-Prover / DeepSeek-Prover-V2 / Kimina-Prover** | open-weights specialised provers | closed much of the gap in 2025 |
| **OpenAI "Astra"** (internal) | an internal version of a *general* model | produced ten new results, each open ≥ 10 years, with Lean certificates ([Ten Advances](https://github.com/openai/ten-proofs)) |

The trend line across that table is the story: the specialized systems established that the
architecture works; the general models then absorbed the capability. See
[ai-for-fm.md](ai-for-fm.md) for the AlphaProof architecture in detail.

**And the one that is not a benchmark at all:** OpenAI's ten results were produced by a *general*
model, not a maths-specific one, and shipped with machine-checked certificates. That is the strongest
single data point for "generic models write Lean now".

---

## Why generic models got good at this

Four reasons, and each generalises beyond Lean:

1. **The verifier is a perfect reward signal.** Lean accepts or rejects. No reward model to game, no
   human preference to approximate. This makes proof writing an unusually *learnable* task, and it is
   the same reason RL works well here ([automated-reasoning.md](../01-fundamentals/automated-reasoning.md#3-the-deep-asymmetry-checking-is-easy-searching-is-hard)).
2. **Errors are structured and local.** A failed tactic yields a goal state with hypotheses and
   remaining goals. That is a far better feedback channel than "wrong answer", and it is what makes
   `refine@k` achievable.
3. **Agentic tooling arrived.** LSP/MCP servers expose goal states, diagnostics, and library search
   to the model, so it can *drive* Lean rather than guess at it blind.
4. **The library is a knowledge base.** mathlib's ~288,000 theorems and ~137,000 definitions are
   both a training corpus and a retrieval target. Much of "proving" is finding the right lemma.

Points 3 and 4 are the ones an individual engineer can act on: if you want your *own* domain to
benefit, the highest-leverage investment is making your library and your tooling agent-accessible.

---

## The workflow inversion: the spec is the review

This is the most important practical consequence, and it has a clean worked example.

### The powdr pattern

For the `apc-optimizer` — a zkVM constraint-system optimiser, formally verified in Lean:

| Aspect | Detail |
|---|---|
| **Human role** | write and thoroughly review ~**500 lines** of specification. Freeze it. Instruct agents not to change it. |
| **AI role** | write the entire implementation and every proof: ~**10,000 lines** of Lean |
| **Human review of the implementation** | **none.** It was never read. |
| **What makes that safe** | CI type-checks every proof against the frozen spec and **rejects `sorry` and new axioms** |
| **Effort** | one week, one engineer, plus a few days of spec review |
| **Outcome** | matched the hand-written Rust optimiser; better on one effectiveness metric |

The authors' own summary is the thesis of this page:

> "Write the spec in a formal language, and let AI write both the code and the proofs that show it
> adheres to the spec. … It solves a key bottleneck in AI-driven software development: Reviews."
> — [powdr, *Formally Verified Autoprecompiles*](https://powdr.org/blog/formally-verified-autoprecompiles)

**Read that again, because it reframes the problem.** The widely-felt pain of AI coding is that
generation is cheap and *review* is not — you cannot read code as fast as a model can write it. The
powdr answer is not "review harder". It is **"replace review with a machine-checked proof against a
small frozen spec."** Your review attention is redirected from 10,000 lines of implementation to 500
lines of specification, and the proof does the rest.

That is a *better* use of human expertise, not a reduction in rigour. Reviewing a specification is
the highest-leverage thing a domain expert can do; reading a generated implementation is close to the
lowest.

### The three roles AI can play

| Role | Who reviews the spec | Who reviews the proof | Maturity |
|---|---|---|---|
| **1. Proof assistant** — you write spec and statement, AI fills in the proof | human | the kernel | **mature today**; the benchmark numbers above |
| **2. Co-author** — AI drafts spec and proof, human reviews both | human, carefully | the kernel | maturing; the spec draft is usually the weak part |
| **3. Optimiser** — spec is frozen, AI rewrites implementation and re-proves | human, once | the kernel + CI | **demonstrated** (`apc-optimizer`, `yul-compiler`, zk.golf) |

**Start with role 1.** It is where the evidence is strongest, the failure modes are mildest, and the
existing tooling (any Lean LSP/MCP server plus your model of choice) already works.

### The loop, concretely

```
    human writes / reviews the SPEC        ← the scarce, high-value step
                 │
                 ▼
    AI proposes implementation + proof
                 │
                 ▼
    Lean kernel checks it  ── reject ──►  error + goal state back to the AI
                 │
                accept
                 ▼
    CI checks the CLAIM, not just the proof:
      · does the theorem statement match the frozen challenge?   (Comparator)
      · were `sorry` / new `axiom`s introduced?                  (grep + #print axioms)
      · does the spec still build against the frozen spec module?
                 │
                 ▼
    merge. no human read the implementation.
```

Every box in that diagram is an engineering artifact you can build. None of it requires trusting the
model.

---

## What to watch for: the three ways this goes wrong

Machine-checked ≠ correct. Three failure modes, in decreasing order of how often they bite:

### 1. Statement mismatch — proving the wrong theorem

The model proves something that *looks* like your theorem. Lean agrees. You have a proof of a
different statement.

This is not exotic; it is the natural failure mode of a search process optimising for "kernel
accepts". Catching it requires comparing the proved statement against the *intended* one, which is
exactly what [Comparator](https://github.com/leanprover/comparator) does: it takes a
`challenge_module` and a `solution_module` with explicit `theorem_names`, and checks that the
solution proves the challenge statement — optionally re-checking with an **independently written
kernel** (`nanoda`).

**This is the generalisable lesson of the whole page:** when the *prover* is untrusted, you must
verify the **claim**, not just the proof. A proof term tells you "something follows from the axioms
you supplied". It does not tell you "the thing you wanted follows."

### 2. Axiom smuggling and `sorry`

`theorem t : 1 = 2 := by sorry` compiles. So does adding an `axiom`. Both are legitimate during
development and catastrophic in a claim.

Mitigations, in order of strength:

```lean
-- 1. Make it visible
#print axioms my_theorem      -- names every axiom it depends on

-- 2. Make it fail the build
set_option autoImplicit false
-- and CI: reject sorry/admit/new axiom declarations (see demos/lean/scripts/check-no-sorry.sh)
```

The powdr project's CI does exactly this, and it is the mechanism that makes "no human reviewed the
implementation" defensible rather than reckless.

### 3. Vacuous or mis-scoped specifications

The proof is of the right statement, the statement is what you wrote, and what you wrote is too weak.
Soundness without completeness permits a "correct" optimiser that returns unsatisfiable circuits.
A "sort" spec without the permutation clause permits returning the empty list. A `transfer` spec
without the frame condition permits draining every other account.

There is no tool for this. **It is the [specification gap](../01-fundamentals/specifications.md), and
AI does not close it — it raises the stakes**, because a spec bug now hides behind a machine-checked
proof that everyone trusts. The mitigations are human and procedural:

- write the property in **at least two clauses** (what must be true of the result, and what must be
  preserved),
- write the **frame condition** explicitly,
- state the **negative** case — what must *not* be provable (the completeness clause, the "no
  trivial optimiser" clause),
- have a second person review the **spec**, since that is where your review budget now goes.

---

## Practical guide: run this on your own code today

### For Lean specifically

| Step | Action |
|---|---|
| 1 | **Pick a target with a crisp spec.** A pure function, a data-structure invariant, a small protocol rule. Not a service. |
| 2 | **Write the spec and the theorem statement yourself.** This is the part not to delegate. State the frame condition. |
| 3 | **Freeze it** in a module the agent is told not to edit. |
| 4 | **Give the model a feedback loop**: a Lean LSP/MCP server, or just `lake build` output piped back. `refine@k` is where the value is. |
| 5 | **Gate CI on four things:** `lake build` succeeds; no `sorry`/`admit`; no new `axiom`; the statement matches the frozen challenge. |
| 6 | **Have a second person review the spec**, not the proof. |

A minimal CI gate you can copy lives in [`demos/lean/scripts/check-no-sorry.sh`](https://github.com/yihuang/awesome-formal-methods/blob/main/demos/lean/scripts/check-no-sorry.sh),
and the [demos page](../demos.md) shows it rejecting a planted `sorry` and accepting the honest proof.

### Beyond Lean

The same pattern applies with different tools and the same shape:

| Target | Let the model propose | Let the machine check | What you review |
|---|---|---|---|
| TLA+/PlusCal spec | the spec, actions, invariants | TLC / Apalache | the invariants, and the model's abstraction choices |
| Dafny / Verus / Kani | implementations, loop invariants, intermediate assertions | the SMT solver | the contracts and the frame conditions |
| A Rust `unsafe` block | a safe rewrite | `cargo kani` | the property being checked |
| Property-based tests | the two properties | the generator + runner | **which properties**, and that the preserving clause is there |
| An incident postmortem | "what property would have caught this?" | any of the above | whether the property is the right lesson |

**The highest-leverage prompt in this entire wiki** is not "prove this". It is:

> *"Here is the bug we shipped. Write the property that would have caught it, and the corresponding
> test or proof obligation."*

That converts an incident into a permanent, machine-checkable guardrail, and it plays directly to
what models are good at (pattern-completing from a concrete failure) rather than what they are bad
at (knowing what you meant).

---

## Reference

### Models and results

| Item | Value | Source |
|---|---|---|
| Best reported Lean 4 result (generic model) | Gemini 3.1 Pro — 92% miniF2F, `refine@32` | [arXiv:2606.05632](https://arxiv.org/abs/2606.05632) (June 2026) |
| Best miniCTX result | Claude Opus 4.7 — 86%, `refine@32` | same |
| Cheapest correct proofs | Nemotron 3 Super / GPT-OSS 120B, **< $0.01** per correct proof | same |
| IMO 2024, formal | AlphaProof + AlphaGeometry 2 — 28/42, silver range | [Nature 2025](https://www.nature.com/articles/s41586-025-09833-y) |
| New research results, general model | OpenAI "Astra" — 10 results, each open ≥10 years, Lean certificates | [openai/ten-proofs](https://github.com/openai/ten-proofs) |
| Metric | `refine@k` = fix attempts given compiler feedback; the operational one | [arXiv:2606.05632](https://arxiv.org/abs/2606.05632) |

### Tools

| Tool | Role |
|---|---|
| **Lean LSP / MCP servers** (`lean-lsp-mcp`) | the feedback loop: goal states, diagnostics, library search for agents |
| **Comparator** (Lean FRO) | independent judging: statement match, axiom check, second kernel (`nanoda`) |
| **`#print axioms`** | the built-in trusted-base audit |
| **`check-no-sorry.sh`** | the CI gate ([repo](https://github.com/yihuang/awesome-formal-methods/blob/main/demos/lean/scripts/check-no-sorry.sh)) |
| **LeanDojo / ReProver / COPRA** | research harnesses for retrieval-augmented proving |
| **mathlib** | ~288k theorems / ~137k definitions / 772 contributors (Sept 2026) — the training and retrieval substrate |

### The workflow, in one table

| You write | The model writes | The kernel checks | CI checks |
|---|---|---|---|
| the specification, the theorem statement, the frame condition | the proof (role 1), or spec + proof (role 2), or implementation + proof (role 3) | that the proof term is valid | that no `sorry`/new `axiom` appeared, and that the *statement* matches the frozen challenge |

### Honest limitations

- Benchmarks like miniF2F are **saturated**; 92% does not imply competence on novel mathematics.
- **Statement fidelity remains the weak point** and needs tooling, not optimism.
- **Specification quality is not improved by AI** — it is put under more pressure, because a proof
  now lends authority to whatever was written down.
- **Long-horizon work** (a multi-week proof effort across a large library) is not demonstrated at the
  reliability you would want to bet a project on.
- **Benchmark contamination** is a live concern; assume reported scores are optimistic.
- **Costs are per proof, but proofs are not the whole cost.** Spec writing, review, and maintenance
  are not in the `< $0.01` figure.

---

## References

- **Klingner, T. et al.** *A comparison of LLMs' effectiveness in producing formal proofs in Lean 4.*
  arXiv:2606.05632, June 2026. [Abstract](https://arxiv.org/abs/2606.05632) — Gemini 3.1 Pro at 92%
  (miniF2F, `refine@32`), Claude Opus 4.7 at 86% (miniCTX), and the sub-cent cost-efficiency result.
- **powdr.** *Formally Verified Autoprecompiles.*
  [Link](https://powdr.org/blog/formally-verified-autoprecompiles) — the ~500-line reviewed spec vs
  ~10,000 lines of unreviewed AI-written Lean, one week by one engineer, CI rejecting `sorry` and new
  axioms, and the effectiveness comparison with the Rust implementation.
- **Alt, L.** *Performant Verified Software.* Sept 2026.
  [Link](https://leoalt.de/performant-verified-software) — "the proof is the review", and the
  argument that verified code can be *more* aggressively optimised.
- **Hubert, T. et al.** *Olympiad-level formal mathematical reasoning with reinforcement learning.*
  *Nature*, 2025. [Link](https://www.nature.com/articles/s41586-025-09833-y)
- **OpenAI.** *Ten Advances in Mathematics and Theoretical Computer Science.* Aug 2026.
  [Repository](https://github.com/openai/ten-proofs) · [Paper](https://cdn.openai.com/pdf/ten-proofs-oai.pdf)
- **Lean FRO.** *Comparator.* [github.com/leanprover/comparator](https://github.com/leanprover/comparator) —
  statement matching, axiom checking, and the independent `nanoda` kernel.
- **mathlib community.** *Statistics.*
  [leanprover-community.github.io/mathlib_stats.html](https://leanprover-community.github.io/mathlib_stats.html)
- **Lean FRO.** *Validating Proofs.*
  [Lean reference](https://lean-lang.org/doc/reference/latest/ValidatingProofs/)
- [lean-lsp-mcp](https://github.com/oOo0oOo/lean-lsp-mcp) — Lean as an agent-accessible tool.

## Further reading

- [ai-for-fm.md](ai-for-fm.md) — the AlphaProof architecture, autoformalization, and the tooling layer.
- [verification-bottleneck.md](verification-bottleneck.md) — why *review* rather than *generation* is
  the binding constraint, which is the problem this page's workflow solves.
- [blockchain.md](../03-applications/blockchain.md) — the domain where this workflow is furthest along.
- [specifications.md](../01-fundamentals/specifications.md) — the skill that is now the bottleneck.
- [demos.md](../demos.md) — the runnable Lean demo and the proof gate.
