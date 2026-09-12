# Tool catalog

> **TL;DR.** Roughly 40 tools matter. They cluster into nine families. Pick a family by *what you
> are reasoning about*, then pick the tool by *maturity and fit with your build system*.

Maturity key: 🟢 production/mainstream · 🟡 usable, active, some sharp edges · 🔵 research-grade or
narrow but real. Learning curve: 🌱 gentle · 🌿 moderate · 🌳 steep.

---

## 1. Proof assistants (interactive theorem proving)

For deep properties of mathematics, kernels, compilers, and crypto. Strongest guarantees,
highest cost.

| Tool | Logic / language | Used for | Maturity | Curve | Pick if… |
|---|---|---|---|---|---|
| **Lean 4** | dependent type theory (CIC-like) | mathematics (mathlib), AI theorem proving, verified algorithms | 🟢 | 🌳 | you want the largest library + the AI ecosystem; mathlib is the killer asset |
| **Rocq** (formerly Coq; renamed in 9.0, Mar 2025) | Calculus of Inductive Constructions | CompCert, verified software, formalised math | 🟢 | 🌳 | you need maturity, extraction to OCaml/Haskell, and a huge corpus of existing proofs |
| **Isabelle/HOL** | higher-order logic | seL4, verification of hardware/protocols, big automation (Sledgehammer) | 🟢 | 🌿 | you want HOL + the best automation and a mature document/proof-engineering story |
| **HOL4 / HOL Light** | higher-order logic | floating-point verification (Intel), foundational math | 🟡 | 🌳 | you're doing classic LCF-style work or verified numerics |
| **PVS** | higher-order logic + dependent types | aerospace, protocols (SRI pedigree) | 🟡 | 🌳 | legacy aerospace/nasa context |
| **ACL2** | first-order + induction | hardware/software models, AMD/Intel usage | 🟡 | 🌿 | you're in the Lisp-y verified-hardware tradition |
| **Agda / Idris** | dependently typed programming | type theory research, verified programming experiments | 🔵 | 🌳 | you care about the types-first programming experience |
| **Mizar** | set theory (declarative) | the original large math library | 🔵 | 🌿 | historical interest, declarative proof style |
| **Mathlib** (library, not a tool) | Lean 4 | ~288k theorems, ~137k definitions, 772 contributors (Sept 2026) | 🟢 | — | you need existing mathematics to build on |

---

## 2. Model checkers (state-space search)

For protocols, concurrency, design-level bugs. Best bug-finding ROI, gives counterexample traces.

| Tool | Input language | Technique | Maturity | Curve | Pick if… |
|---|---|---|---|---|---|
| **TLA+ / TLC** | TLA+, PlusCal | explicit-state | 🟢 | 🌿 | **the default for distributed protocol design** — Lamport, AWS, huge published spec corpus |
| **Apalache** | TLA+ | symbolic (SMT) | 🟡 | 🌿 | your TLA+ spec is too big for TLC, or you want symbolic checking |
| **Alloy** | relational FOL | bounded SAT | 🟢 | 🌱 | you want fast, bounded, relational modelling — found real bugs in Chord; **gentlest learning curve in the family** |
| **SPIN** | Promela | explicit-state, LTL | 🟢 | 🌿 | classic concurrency/communication protocols; ACM Software System Award |
| **NuSMV / nuXmv** | SMV | BDD/symbolic, CTL/LTL | 🟡 | 🌿 | hardware-ish control logic, CTL properties |
| **mCRL2** | process algebra | explicit + symbolic | 🟡 | 🌳 | process-algebraic modelling, behavioural equivalence |
| **P** (Microsoft) | P language | systematic testing + verification | 🟡 | 🌿 | event-driven systems, Azure-style services |
| **Stateright** | Rust | explicit-state, in-process | 🔵 | 🌱 | your system *is* Rust and you want model checking in the same language |
| **PRISM** | PRISM language | probabilistic (DTMC/MDP) | 🟡 | 🌿 | randomized protocols, reliability, expected values |
| **UPPAAL** | timed automata | timed model checking | 🟡 | 🌿 | real-time systems with deadlines |
| **Java PathFinder** | Java bytecode | explicit-state | 🟡 | 🌿 | verifying actual Java programs |

---

## 3. Deductive program verifiers (VC generation + SMT)

For verifying *real code*: contracts, invariants, functional correctness. Best fit for industry.

| Tool | Target language | Maturity | Curve | Pick if… |
|---|---|---|---|---|
| **Dafny** | Dafny (also compiles to C#/Java/Go/Py) | 🟢 | 🌱 | **the best first program verifier** — designed for teaching, used by AWS for Cedar |
| **F\*** | F* (OCaml-like, dependent types + SMT) | 🟢 | 🌿 | you need dependent types *and* SMT automation; Project Everest / HACL* |
| **Why3** | WhyML (multi-language front ends) | 🟢 | 🌿 | you want a solver-agnostic platform; underlies many tools |
| **Verus** | Rust | 🟡 | 🌿 | you want SMT-based verification of real, concurrent Rust |
| **Creusot** | Rust | 🟡 | 🌿 | Rust → Why3 → SMT; good for functional correctness of Rust |
| **Prusti** | Rust | 🟡 | 🌿 | Rust verification with a strong spec language (Viper-backed) |
| **Kani** | Rust | 🟢 | 🌱 | **push-button bounded verification for Rust, especially `unsafe`** — `cargo kani`, CI-ready |
| **CBMC** | C/C++ | 🟢 | 🌱 | bounded model checking of C; the engine under Kani |
| **SPARK / Ada** | Ada | 🟢 | 🌿 | safety-critical, DO-178C/IEC 61508 pedigree |
| **JML / OpenJML, KeY** | Java | 🟡 | 🌿 | Java verification, KeY does deductive Java verification |
| **Stainless** | Scala | 🟡 | 🌿 | Scala verification |
| **Nagini / Viper** | Python (Nagini), Viper IR | 🔵🟡 | 🌿 | Python verification; Viper is a strong intermediate language |
| **Boogie** | Boogie IVL | 🟡 | 🌳 | you're building a verifier (Dafny/Creusot/Prusti all use it) |
| **Frama-C** | C (ACSL annotations) | 🟢 | 🌿 | C with a plugin ecosystem (value analysis, WP, Eva) — industrial in Europe |
| **Isabelle/Simpl / AutoCorres** | C (via Simpl) | 🔵 | 🌳 | C verification inside Isabelle (seL4's path) |

---

## 4. Abstract interpretation & sound static analysis

Whole-codebase soundness without annotations. Underrated, unglamorous, and deployed.

| Tool | Target | Maturity | Pick if… |
|---|---|---|---|
| **Astrée** | C | 🟢 (commercial) | you need proved absence of runtime errors in large safety-critical C (Airbus pedigree) |
| **Polyspace** | C/C++ | 🟢 (commercial) | same, with a broader toolchain integration |
| **Frama-C / Eva** | C | 🟢 | open-source abstract interpretation for C |
| **CPAchecker** | C | 🟡 | software-verification competition-grade; configurable analyses |
| **Infer** (Meta) | Java/C/C++/ObjC | 🟢 | you want sound-ish analysis in CI at scale (used at Meta) |
| **MIRAI** | Rust MIR | 🔵 | Rust abstract interpretation for panic/UB detection |
| **IKOS** | C/C++ (LLVM) | 🔵 | NASA-funded abstract interpretation |
| **Clang Static Analyzer / Semgrep** | C/C++ / multi | 🟢 | ⚠️ **not sound** — these are heuristics, not abstract interpretation. Useful; don't call them proofs. |

---

## 5. Solvers (the engine)

| Tool | Kind | Maturity | Notes |
|---|---|---|---|
| **Z3** | SMT | 🟢 | the de facto standard backend; enormous ecosystem |
| **cvc5** | SMT | 🟢 | strong on strings, quantifiers; SMT-COMP leader |
| **Yices 2** | SMT | 🟡 | fast for certain fragments |
| **MathSAT** | SMT | 🟡 | good optimisation support (OMT) |
| **Bitwuzla / Boolector / STP** | SMT (bit-vectors) | 🟢 | hardware/bit-precise work |
| **Alt-Ergo** | SMT | 🟡 | OCaml; used by Why3/Frama-C |
| **Vampire / E** | first-order ATP | 🟢 | quantified goals, superposition |
| **CaDiCaL / Kissat / MiniSat** | SAT | 🟢 | CDCL engines; CaDiCaL/Kissat do proof logging |
| **DRAT/LRAT checkers** | proof validation | 🟢 | **use these if your assurance depends on the SAT result** |
| **Gurobi / CPLEX / SCIP** | MILP | 🟢 | NN verification, optimisation problems |

---

## 6. Neural network verification

| Tool | Technique | Maturity | Pick if… |
|---|---|---|---|
| **α,β-CROWN** | linear bound propagation + branch & bound | 🟢 | you want SOTA certified robustness; VNN-COMP winner 2021–2025 |
| **Marabou** | SMT/MILP-style, precise | 🟡 | small networks, exact reasoning, custom properties |
| **ERAN** | abstract interpretation over deep nets | 🟡 | abstraction-based certification |
| **MN-BaB** | branch & bound with multi-neuron relaxation | 🔵 | research baselines |
| **nn4sys / VeriNet** | specialised | 🔵 | systems/control applications |
| **VNN-COMP** (benchmark suite) | — | 🟢 | you want to know what's actually verifiable today |

---

## 7. Protocol & cryptographic verification

| Tool | Kind | Maturity | Pick if… |
|---|---|---|---|
| **ProVerif** | symbolic protocol verifier (Dolev-Yao) | 🟢 | you want to find protocol-level attacks automatically |
| **Tamarin** | symbolic protocol verifier | 🟢 | same, with support for stateful protocols and equational theories |
| **CryptoVerif** | computational soundness | 🟡 | you need cryptographic (not just symbolic) guarantees |
| **EasyCrypt** | proof assistant for crypto | 🟡 | reductionist proofs of cryptographic constructions |
| **ct-verif / FaCT** | constant-time verification | 🔵 | you need to prove absence of timing leakage |
| **Vale** | verified assembly | 🟡 | you need verified, fast low-level crypto |
| **HACL\* / EverCrypt** | verified crypto library (F*) | 🟢 | **you need crypto and shouldn't roll your own** — Firefox/Linux/nginx |
| **Cedar + automated reasoning** | policy verification | 🟢 | authorization policy correctness |

---

## 8. Agent & runtime enforcement (the AI-era category)

| Tool | Kind | Maturity | Pick if… |
|---|---|---|---|
| **AgentSpec** | runtime enforcement DSL for LLM agents (triggers, predicates, enforcement) | 🔵 | you want declarative guardrails on agent behaviour rather than prompt instructions |
| **Shields (synthesised)** | temporal-logic safety automata for RL | 🔵 | safe RL, robotics, control |
| **AWS Bedrock Automated Reasoning checks** | SMT-based validation of LLM output against policies | 🟢 (product) | you want sound hallucination/policy checking in a managed service |
| **Cedar / policy engines (OPA, etc.)** | policy-as-code authorization | 🟢 | you want a formally-grounded authorization decision before an action |
| **Runtime verification frameworks** | temporal-logic monitors over traces | 🟡 | you want assertions on agent decisions |
| **Comparator** (Lean FRO) | independent judging of Lean proofs (statement match + axiom check + second kernel) | 🟡 | **you must not trust a model's claim that it proved your theorem** |

---

## 9. Lightweight / type-level (rung 0–2)

| Tool | Kind | Cost | Pick if… |
|---|---|---|---|
| **Rust** | ownership/borrowing ≈ decidable separation logic | free | you want memory + data-race safety by construction |
| **TypeScript / mypy / pyright** | type checking | free | you want rung 0 for JS/Python |
| **Liquid Haskell / refinement types** | SMT-discharged type refinements | low | you want rung 1–2 in a Haskell codebase |
| **Wuffs** | memory-safe-by-construction language | low | you're writing parsers/decoders |
| **Hypothesis / QuickCheck / proptest / fast-check / jqwik** | property-based testing | low | **you want rung 2 — the highest-value rung** |
| **Go fuzzing / AFL++ / libFuzzer / OSS-Fuzz** | fuzzing | low | you want to find crashes/adversarial inputs |
| **Echidna / Medusa / Foundry invariant tests** | smart-contract fuzzing | low | you're in Solidity; Foundry's invariant testing is effectively PBT for protocols |
| **KLEE / angr / Manticore** | symbolic execution | medium | you want path exploration + concrete inputs |
| **Semgrep / CodeQL** | pattern/dataflow analysis | free | you want broad cheap coverage (unsound) |

---

## 10. AI-for-FM tooling

| Tool | Kind | Notes |
|---|---|---|
| **Lean LSP / MCP servers** (`lean-lsp-mcp`) | agent interface to Lean | lets an LLM drive Lean via the Language Server Protocol: goal states, diagnostics, search |
| **LeanDojo / ReProver** | retrieval-augmented proving infrastructure | the standard research harness |
| **COPRA** | LLM prover in Lean | in-context proof search with environment feedback |
| **DeepSeek-Prover-V2** | open LLM prover | strong open-weights baseline (2025) |
| **Goedel-Prover** | open LLM prover | open-source SOTA claims (2025) |
| **Kimina-Prover** | open LLM prover | Lean-based |
| **Harmonic Aristotle** | agentic prover product | gold-medal-equivalent IMO 2025 with Lean-verified proofs |
| **Comparator** | independent judge | see §8 |

---

## Quick-reference: the five tools to mention in a 30-minute talk

If you only name five:

1. **TLA+** — the distributed-systems design tool (AWS, Lamport). *Best ROI.*
2. **Dafny** — the friendliest program verifier (AWS's Cedar).
3. **Kani** — `cargo kani`, push-button Rust verification in CI. *Most likely to be adopted.*
4. **Lean 4** — the AI-era proof assistant (mathlib, AlphaProof, 2026 results).
5. **Hypothesis / proptest / fast-check** — rung 2, free, today.

Plus one to *not* use: **roll-your-own crypto**. Use HACL*/EverCrypt or SymCrypt.

---

Next → [choosing.md](choosing.md): the decision tree.

## References

Entry points for the tools catalogued above. Grouped as in the catalog.

**Proof assistants**
[Lean 4](https://lean-lang.org/) · [mathlib](https://leanprover-community.github.io/) ·
[Rocq (Coq)](https://rocq-prover.org/) · [Isabelle](https://isabelle.in.tum.de/) ·
[HOL4](https://hol-theorem-prover.org/) · [PVS](https://pvs.csl.sri.com/) ·
[ACL2](https://www.cs.utexas.edu/~moore/acl2/) · [Agda](https://wiki.portal.chalmers.se/agda/) ·
[Mizar](https://mizar.uwb.edu.pl/)

**Model checkers**
[TLA+](https://lamport.azurewebsites.net/tla/tla.html) · [Apalache](https://apalache-mc.org/) ·
[Alloy](https://alloytools.org/) · [SPIN](https://spinroot.com/) ·
[NuSMV](https://nusmv.fbk.eu/) · [mCRL2](https://www.mcrl2.org/) ·
[P](https://github.com/p-org/P) · [Stateright](https://github.com/stateright/stateright) ·
[PRISM](https://www.prismmodelchecker.org/) · [UPPAAL](https://uppaal.org/)

**Deductive verifiers**
[Dafny](https://dafny.org/) · [F*](https://fstar-lang.org/) · [Why3](https://why3.lri.fr/) ·
[Verus](https://verus-lang.github.io/verus/guide/) · [Creusot](https://github.com/creusot-rs/creusot) ·
[Prusti](https://github.com/viperproject/prusti-dev) · [Kani](https://github.com/model-checking/kani) ·
[CBMC](https://www.cprover.org/cbmc/) · [SPARK](https://www.adacore.com/sparkpro) ·
[OpenJML](https://www.openjml.org/) · [KeY](https://www.key-project.org/) ·
[Stainless](https://github.com/epfl-lara/stainless) · [Viper](https://viperproject.github.io/) ·
[Boogie](https://github.com/boogie-org/boogie) · [Frama-C](https://frama-c.com/)

**Abstract interpretation and sound static analysis**
[Astrée](https://www.absint.com/astree/) · [Polyspace](https://www.mathworks.com/products/polyspace.html) ·
[Frama-C/Eva](https://frama-c.com/fc-plugins/eva.html) · [CPAchecker](https://cpachecker.sosy-lab.org/) ·
[Infer](https://fbinfer.com/) · [MIRAI](https://github.com/facebookexperimental/MIRAI) ·
[IKOS](https://github.com/NASA-SW-VnV/ikos)

**Solvers**
[Z3](https://github.com/Z3Prover/z3) · [cvc5](https://cvc5.github.io/) ·
[Yices](https://yices.csl.sri.com/) · [MathSAT](https://mathsat.fbk.eu/) ·
[Bitwuzla](https://bitwuzla.github.io/) · [Alt-Ergo](https://alt-ergo.ocamlpro.com/) ·
[Vampire](https://vprover.github.io/) · [E](https://wwwlehre.dhbw-stuttgart.de/~sschulz/E/E.html) ·
[CaDiCaL](https://github.com/arminbiere/cadical) · [Kissat](https://github.com/arminbiere/kissat)

**Neural network verification**
[α,β-CROWN](https://github.com/Verified-Intelligence/alpha-beta-CROWN) ·
[Marabou](https://github.com/NeuralNetworkVerification/Marabou) ·
[ERAN](https://github.com/eth-sri/eran) · [VNN-COMP](https://vnn-comp.github.io/)

**Protocol and cryptographic verification**
[ProVerif](https://bblanche.gitlabpages.inria.fr/proverif/) ·
[Tamarin](https://tamarin-prover.github.io/) ·
[EasyCrypt](https://easycrypt.gitlabpages.inria.fr/) ·
[CryptoVerif](https://bblanche.gitlabpages.inria.fr/cryptoverif/) ·
[ct-verif / FaCT](https://github.com/PLSysSec/FaCT) ·
[HACL\* / EverCrypt](https://hacl-star.github.io/HaclValeEverCrypt.html) ·
[Cedar](https://www.cedarpolicy.com/)

**Agent and runtime enforcement**
[AgentSpec](https://github.com/haoyuwang99/AgentSpec) ·
[AWS Bedrock automated reasoning checks](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html) ·
[Comparator](https://github.com/leanprover/comparator)

**Lightweight and property-based**
[Hypothesis](https://hypothesis.readthedocs.io/) ·
[proptest](https://github.com/proptest-rs/proptest) · [fast-check](https://fast-check.dev/) ·
[jqwik](https://jqwik.net/) · [QuickCheck](https://hackage.haskell.org/package/QuickCheck) ·
[AFL++](https://github.com/AFLplusplus/AFLplusplus) · [OSS-Fuzz](https://github.com/google/oss-fuzz) ·
[KLEE](https://klee-se.org/) · [angr](https://angr.io/) ·
[Echidna](https://github.com/crytic/echidna) · [Foundry](https://book.getfoundry.sh/)

**AI for formal methods**
[lean-lsp-mcp](https://github.com/oOo0oOo/lean-lsp-mcp) · [LeanDojo](https://leandojo.org/) ·
[Goedel-Prover](https://arxiv.org/abs/2502.07640)
