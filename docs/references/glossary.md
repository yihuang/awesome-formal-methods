# Glossary

Every term this wiki uses, defined once, in the order you'd encounter them.

---

## Core concepts

**Formal method** — a technique that uses mathematics with precise semantics to specify or reason
about a system, such that a machine can check the result.

**Specification** — a precise statement of what a system must do. The output of the hard part of
verification.

**Property** — a fragment of a specification, usually classified as safety or liveness.

**Safety property** — "nothing bad ever happens." A violation is witnessed by a finite trace.
Example: no two processes in the critical section simultaneously.

**Liveness property** — "something good eventually happens." A violation requires an infinite
trace. Example: every request is eventually served.

**Invariant** — a property true in every reachable state. The main thing a human (or LLM) must
supply to a verifier.

**Counterexample** — a concrete trace or input demonstrating that a property fails. The most
useful artifact most formal-methods tools produce.

**Model** — an abstract description of a system used for reasoning. Distinct from the system
itself (see *refinement gap*).

**Soundness** — the property "if the tool says verified, it's true." No missed real bugs.

**Completeness** — the property "the tool always returns an answer." A sound, complete checker for
a non-trivial property cannot exist (Rice's theorem).

**Trusted base / trusted computing base (TCB)** — everything you must trust for a verification
claim to hold: the kernel, the solver, the model, the compiler, the assumptions.

---

## Logic and specification

**Hoare triple** — `{P} C {Q}`: if `P` holds before executing `C`, and `C` terminates, then `Q`
holds after.

**Precondition / postcondition** — the `P` (assumed) and `Q` (guaranteed) of a contract.

**Partial correctness** — `{P}C{Q}`: correct *if* it terminates. Says nothing about termination.

**Total correctness** — partial correctness **plus** termination. Written `[P]C[Q]`.

**Weakest precondition (`wp`)** — `wp(C, Q)` is the weakest precondition guaranteeing `C`
establishes `Q`. The basis of automatic verification: prove `P ⟹ wp(C,Q)`.

**Verification condition (VC)** — a first-order formula whose validity implies the program meets
its spec. Generated from annotated code, discharged by an SMT solver.

**Loop invariant** — an assertion preserved by every iteration of a loop; needed to prove anything
about a `while`. Finding it is the classic bottleneck (and undecidable in general).

**Ghost code / ghost state** — specification-only code that doesn't affect execution but lets you
state and prove properties (e.g. a logging variable used only in proofs).

**Separation logic** — an extension of Hoare logic with a separating conjunction `∗`, meaning "and
these hold on disjoint parts of the heap". Enables the **frame rule**: verify a function once and
compose it. Basis for Rust's ownership discipline, and Turing Award 2025.

**Frame rule** — `{P}C{Q} ⟹ {P∗R}C{Q∗R}` provided `C` doesn't touch `R`'s footprint.

**Temporal logic** — logic for reasoning about time/sequences.

**LTL (Linear Temporal Logic)** — one timeline; operators `X` (next), `G` (always/globally),
`F` (eventually), `U` (until).

**CTL (Computation Tree Logic)** — quantifies over paths: `A` (all paths), `E` (exists a path),
combined with temporal operators (`AG`, `EF`, `AF`, `EG`).

**CTL\*** — subsumes LTL and CTL.

**μ-calculus** — fixpoint logic subsuming CTL\*; the theoretical target of most model checkers.

**Hyperproperty** — a property of *sets* of traces rather than a single trace. Needed for
non-interference, information flow, and other security properties.

**Refinement** — the relation "this concrete thing is a correct implementation of that abstract
spec." The mechanism that links a verified model to code.

**Refinement gap / model-reality gap** — the distance between the model you verified and the code
that runs. Closed by refinement proofs, differential testing, or explicit assumption statements.

**Specification gap** — the permanent impossibility of proving that your property is what anyone
wanted. The deepest limitation of the field.

---

## Techniques

**Theorem proving (interactive)** — a human (or AI) writes a proof term; a small kernel checks it.
Lean, Rocq, Isabelle/HOL, HOL4, PVS, ACL2.

**Proof term** — the data structure encoding a complete logical argument from axioms to
conclusion. What a kernel actually checks.

**Tactic** — a proof-construction command that manipulates the proof state. Tactics build proof
terms.

**`sorry` / `admit`** — a proof placeholder that compiles but proves nothing. Grep for these in CI.

**de Bruijn criterion** — the assurance principle that the trusted kernel should be small enough
to be reviewed by a human. Why proof assistants have small kernels.

**Model checking** — exhaustively explore all reachable states of a finite model, checking a
property.

**Explicit-state model checking** — enumerate states directly (TLC, SPIN). Gives traces, hits state
explosion.

**Symbolic model checking** — encode states as formulas/BDDs; reason symbolically (NuSMV, Apalache).

**Bounded model checking (BMC)** — check for violations up to a depth bound `k`. Sound for the
bound; *not* a proof beyond it. CBMC, Kani.

**State-space explosion** — the exponential blowup of the reachable state count; the core
scalability problem of model checking.

**Abstraction** — replacing a system with a simpler one whose behaviours over-approximate the
original, so a proof transfers.

**CEGAR (Counterexample-Guided Abstraction Refinement)** — start with a coarse abstraction, check,
and if the counterexample is spurious, refine the abstraction and repeat.

**Partial-order reduction / symmetry reduction** — techniques to avoid exploring equivalent
interleavings or symmetric states.

**Deductive verification** — generate VCs from annotated code and discharge them with a solver.
Dafny, F*, Why3, Verus, Creusot, Prusti, CBMC, Boogie.

**Abstract interpretation** — interpret a program over an abstract domain that over-approximates
concrete behaviour. Always terminates, sound, may produce false alarms. Cousot & Cousot 1977;
Astrée.

**Abstract domain** — the lattice of properties used (intervals, octagons, polyhedra, congruence,
…). Precision/cost trade-off.

**False alarm (false positive)** — an abstract-interpretation report of a possible error that
can't actually occur. The price of soundness.

**Static analysis** — any automated code analysis. ⚠️ Only *sound* static analysis (e.g. abstract
interpretation) yields proofs; linters and heuristics are typically unsound.

**Type system** — a decidable, conservative approximation of program correctness, enforced by the
compiler. The free tier of formal methods.

**Curry–Howard correspondence** — propositions are types, proofs are programs, proof-checking is
type-checking.

**Dependent type** — a type that depends on a value, e.g. `Vec a n` (a vector of length `n`).
Enables specifications enforced at compile time.

**Refinement type** — a type annotated with a logical predicate, discharged by an SMT solver
(Liquid Haskell, F*).

**Symbolic execution** — execute a program with symbolic inputs, collecting path constraints and
solving them (KLEE, angr, Manticore).

**Runtime verification** — check temporal properties against a running system's execution trace,
via monitors. Blocks/alerts at runtime rather than proving statically.

---

## Solvers

**SAT (satisfiability)** — given a boolean formula in CNF, find a satisfying assignment or prove
none exists. NP-complete; modern solvers handle millions of clauses.

**CNF (conjunctive normal form)** — a conjunction of clauses, each a disjunction of literals. The
standard SAT input format.

**DPLL** — the classic backtracking SAT algorithm with unit propagation (1962).

**CDCL (conflict-driven clause learning)** — the 1996 breakthrough: learn clauses from conflicts and
backjump non-chronologically. Makes SAT industrial.

**Watched literals** — an implementation trick making unit propagation near-constant time (Chaff,
2001).

**DRAT / LRAT** — standard formats for machine-checkable proofs of unsatisfiability, so a small
independent checker can validate a big solver's answer.

**SMT (satisfiability modulo theories)** — SAT extended with decision procedures for theories
(arithmetic, bit-vectors, arrays, strings, …). Z3, cvc5.

**Theory** — a set of axioms with a decision procedure; e.g. EUF, LIA, LRA, BV, arrays, strings.

**Nelson–Oppen** — the method for combining decision procedures for multiple theories.

**`unknown`** — an SMT solver's honest answer when it can't decide. Extremely common with
nonlinear arithmetic and quantifiers; handling it is daily verification work.

**Unsat core** — a subset of constraints that is already unsatisfiable; useful for debugging
failed proofs.

---

## AI-era terms

**Autoformalization** — translating informal (natural-language) mathematics or requirements into a
formal language. The dominant bottleneck in AI-for-math, and the new bottleneck in FM-for-AI.

**Neural theorem proving** — using neural networks / LLMs to guide proof search.

**RL environment / reward signal** — for provers: state = tactic state, action = tactic, reward =
proof found. Formal systems give an *unhackable* reward.

**TTRL (test-time reinforcement learning)** — AlphaProof's approach of generating variants of a hard
target problem and running focused RL on them at inference time.

**Certified robustness** — a *proved* statement that a model's prediction is unchanged for all
inputs within an ε-ball (an Lp norm ball) of a given input. Distinct from empirical robustness.

**Shield** — a formally verified component that constrains an RL agent's actions so that safety
properties hold regardless of the learned policy.

**Proof-carrying code / proof-carrying action** — require the producer (human or AI) to supply a
machine-checkable certificate, checked before acceptance/execution.

**Statement mismatch** — the failure mode where a proof establishes a theorem subtly different
from the claimed one. Caught by tools like Lean FRO's Comparator.

**Axiom smuggling** — strengthening a proof by adding an `axiom` (or leaving a `sorry`) so that the
"theorem" is vacuous. Also caught by Comparator-style tooling.

**VNN-COMP** — the International Verification of Neural Networks Competition; the reference point
for what NN verification can currently do.

**Leiden Declaration on AI and Mathematics (June 2026)** — a statement by an international group of
mathematicians raising concerns about AI in mathematics: press-release announcement rather than
peer review, use of published work without consent, and threats to attribution and proof integrity.

---

## Abbreviations

| Abbrev. | Meaning |
|---|---|
| **FM** | formal methods |
| **VC** | verification condition |
| **TCB** | trusted computing base |
| **BMC** | bounded model checking |
| **PBT** | property-based testing |
| **DRT** | differential random testing |
| **NN** | neural network |
| **LTL / CTL** | linear temporal logic / computation tree logic |
| **SMT** | satisfiability modulo theories |
| **CDCL** | conflict-driven clause learning |
| **IMO** | International Mathematical Olympiad |
| **DO-178C / DO-333** | avionics software standard / its formal-methods supplement |
| **ASIL / SIL** | automotive safety integrity level / safety integrity level |

## References

This glossary defines terms introduced across the wiki; the authoritative sources are on the pages
where each term is used. The primary references for the definitions most often looked up here:

- **Hoare, C.A.R.** CACM 1969 — precondition, postcondition, partial correctness.
- **Dijkstra, E.W.** CACM 1975 — weakest precondition, verification condition.
- **Floyd, R.** 1967 — invariant, as an annotation on a flowchart.
- **Cousot, P. & Cousot, R.** POPL 1977 — abstraction, abstract domain, false alarm.
- **Kahn, G.** STACS 1987; **Plotkin, G.** 1981 — big-step and small-step, and the derivation-based
  proof principles behind them.
- **Clarke & Emerson** 1981; **Pnueli, A.** 1977 — safety, liveness, temporal operators.
- **Emerson & Halpern** 1983 — LTL, CTL, CTL*.
- **Kozen, D.** 1983 — μ-calculus.
- **Reynolds, J.C.** 2002; **O'Hearn, P. et al.** 2001 — separation logic, frame rule, footprint.
- **Rice, H.G.** 1953 — soundness/completeness trade-off.
- **de Bruijn, N.G.** 1980 — trusted base, de Bruijn criterion.
- **Necula, G.** POPL 1997 — proof-carrying code.
- **Clarkson, M. & Schneider, F.** CSF 2008 — hyperproperty, non-interference.
- **Wang, S. et al.** NeurIPS 2021 — certified robustness.
- **Alshiekh, M. et al.** AAAI 2018 — shields.
- **Wang, H. et al.** 2025 ([arXiv:2503.18666](https://arxiv.org/abs/2503.18666)) — runtime
  enforcement for agents.
- **Wright, A. & Felleisen, M.** 1994 — progress and preservation.
- [SAT solver](https://en.wikipedia.org/wiki/SAT_solver) ·
  [SMT](https://en.wikipedia.org/wiki/Satisfiability_modulo_theories) ·
  [Operational semantics](https://en.wikipedia.org/wiki/Operational_semantics) ·
  [Separation logic](https://en.wikipedia.org/wiki/Separation_logic) ·
  [Abstract interpretation](https://en.wikipedia.org/wiki/Abstract_interpretation) —
  for the survey-level definitions.
