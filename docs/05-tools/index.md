# Tools — index

| Page | Contents |
|---|---|
| [catalog.md](catalog.md) | ~40 tools in nine families, with maturity, learning curve, and "pick this if" |
| [choosing.md](choosing.md) | Decision tree, selection heuristics, install commands, selection anti-patterns |
| [model-verifiers.md](model-verifiers.md) | TLA+, Ivy, Veil in depth: specs, toolchains, CTI-driven invariant discovery |
| [lean4.md](lean4.md) | The Lean 4 kernel, elaborator, metaprogramming, and a runnable tour |
| [mathlib.md](mathlib.md) | The library: conventions, discovery tools, workflow, coverage |
| [iris.md](iris.md) | The Iris framework: monoids, invariants, ghost state, proof mode, and the Lean port |
| [proof-tactics.md](proof-tactics.md) | The goal state, the automation ladder, debugging, best practices |

## The short version

> **Pick the cheapest tool that can check the property you actually care about, and put it in CI.**
> **If it can't produce a counterexample, your team will abandon it within a sprint.**

## The five tools to name in a 30-minute talk

1. **TLA+** — protocol/design model checking. The best ROI, and the AWS story. 🟢🌿
2. **Dafny** — the friendliest program verifier; behind Cedar. 🟢🌱
3. **Kani** — `cargo kani`, push-button Rust verification, especially `unsafe`. 🟢🌱
4. **Lean 4** — the AI-era proof assistant (mathlib, AlphaProof, the 2026 results). 🟢🌳
5. **Hypothesis / proptest / fast-check** — rung 2, free, works today. 🟢🌱

**And the anti-recommendation:** don't roll your own crypto. Use HACL\*/EverCrypt or SymCrypt.

## The nine families at a glance

| Family | What it's for | Entry point |
|---|---|---|
| Proof assistants | deep properties; kernels, compilers, crypto, math | Lean 4 |
| Model checkers | protocol/design bugs, exhaustive interleavings | TLA+/TLC, Alloy |
| Deductive verifiers | real code, contracts, functional correctness | Dafny, Kani |
| Abstract interpretation | whole-codebase absence of runtime errors | Frama-C, Polyspace, Astrée |
| Solvers | the engine under everything | Z3, cvc5 |
| NN verification | certified robustness, reachability | α,β-CROWN, Marabou |
| Protocol/crypto verification | attacks, cryptographic correctness | ProVerif, Tamarin, HACL\* |
| Agent/runtime enforcement | guardrails, policy, shields, proof-carrying actions | AgentSpec, Cedar, Comparator |
| Lightweight / types | rung 0–2, free, in CI today | Rust, Hypothesis, proptest |

## Environment note

In this repo's environment (Sept 2026): **Lean 4.32.0 + `lake` are installed and the demos in
[`demos/lean/`](../demos.md) are runnable.** TLA+, Dafny, Z3, Rocq, and Alloy are *not*
installed; TLA+ and Python demos are provided as readable artifacts with install instructions.
