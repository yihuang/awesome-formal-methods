# Techniques: the five families of verification

> **TL;DR.** There are only five ways to establish a formal guarantee. They differ in what they
> can prove, how much of the work is automated, and how they fail. Every tool in the catalog is a
> point in this space.

```
                        who supplies the ingenuity?
                   human ─────────────────────────── machine
                     │                                  │
   exact,      ┌─────┴──────────┐          ┌────────────┴───────────┐
   all states  │  THEOREM       │          │  MODEL CHECKING        │
               │  PROVING       │          │  (exhaustive search)   │
               │  Lean, Rocq,   │          │  TLA+/TLC, SPIN,       │
               │  Isabelle,     │          │  NuSMV, Alloy          │
               │  HOL4, PVS     │          │                        │
               └────────────────┘          └────────────────────────┘
                     │                                  │
   over-approx,  ┌────┴───────────┐          ┌─────────┴──────────────┐
   all states    │  ABSTRACT      │          │  DEDUCTIVE VERIFICATION│
                 │  INTERPRETATION│          │  (VC generation + SMT) │
                 │  Astrée,       │          │  Dafny, F*, Why3,      │
                 │  Polyspace     │          │  Verus, Kani, CBMC     │
                 └────────────────┘          └────────────────────────┘
                     │                                  │
   every state?  ┌───┴────────────────────────────────┴───┐
   no — sampled   │  TYPES / LIGHTWEIGHT STATIC ANALYSIS  │
                  │  Rust, TS, Liquid Haskell, linters     │
                  └───────────────────────────────────────┘
```

Below: what each family is, what it's good at, how it fails, and the one-paragraph version for a
slide.

---

## 1. Theorem proving (interactive)

**Idea.** Encode the system and its specification in a logic with a small trusted kernel. A human
(or now an LLM) writes a *proof term*; the kernel checks it. Based on Curry–Howard
([logics.md](logics.md)): proving is programming.

**Tools.** Lean 4, Rocq (formerly Coq, renamed with Rocq 9.0 in March 2025 —
[source](https://rocq-prover.org/releases/9.0.0)), Isabelle/HOL, HOL4, PVS, ACL2, Agda.

**What it's uniquely good at**
- Deep mathematics and *any* statement you can write in the logic (no bounded scope).
- Functional correctness, full functional correctness of compilers (CompCert), microkernels (seL4).
- The strongest guarantees on offer: a small kernel checks everything (the **de Bruijn
  criterion**). Trust base is thousands of lines, not tens of thousands.

**How it fails**
- Proof engineering is hard and labour-intensive. The **proof-to-code ratio is the killer
  metric**: seL4 is ~8,700 lines of C backed by ~200,000 lines of Isabelle proof, ~20 person-years.
- Proofs are brittle: change the definition, redo the proof.
- Tactic scripts are code with no specs — a "proof" can be an accidental `sorry`/`admit` away
  from being a lie. **Always grep for `sorry` in CI.** (`demos/lean/` does this.)

**Slide version.** *"Theorem proving is the strongest guarantee and the most expensive. It is
justified when the artifact is small, stable, and catastrophic when wrong — a kernel, a compiler,
a crypto primitive."*

---

## 2. Model checking (exhaustive state-space search)

**Idea.** Build a finite-state model. Explore *all* reachable states. If a property is violated,
you get a concrete **counterexample trace**.

**Tools.** TLA+/TLC, PlusCal, Apalache (symbolic, SMT-backed TLA+), SPIN/Promela, NuSMV/nuXmv,
Alloy (bounded, relational), mCRL2, PRISM (probabilistic), UPPAAL (timed).

**What it's uniquely good at**
- **It gives you the bug, not a "failed to prove".** The counterexample trace is the product.
- Fully automatic once you have the model: no invariants needed for *finding* violations (though
  you need them for proving correctness in symbolic variants).
- Perfect for *concurrent* and *distributed* systems, where the state space is the enemy that
  testing cannot sample: interleavings, partial failure, message reordering.

**How it fails**
- **State-space explosion.** `n` concurrent processes with `k` local states is `kⁿ` — exponential.
  Mitigations: symmetry reduction, partial-order reduction, symbolic (BDD/SMT) checking,
  abstraction, bounded checking.
- A successful check proves the *model*, not the code (the refinement gap).
- Tuning the model (which failures to inject, what to abstract) is a real skill.

**The two most important subtypes**
- **Explicit-state** (TLC, SPIN): enumerate states. Simple, gives traces, hits explosion.
- **Symbolic/bounded** (Apalache, CBMC, Alloy, NuSMV with BDDs): encode as formulas, let a solver
  reason. Scales differently, "bounded" means *up to depth k* — a bound is not a proof.

**Slide version.** *"Model checking is a bug-finder for designs. You write the design in
unambiguous pseudo-code — TLA+ calls itself 'exhaustively testable pseudo-code' — and it hands
you the interleaving that breaks it."*

---

## 3. Deductive verification (VC generation + SMT)

**Idea.** Annotate the program (contracts, invariants). A tool generates first-order
**verification conditions** and discharges them with an SMT solver
([logics.md](logics.md#weakest-preconditions)).

**Tools.** Dafny, F* (+ its tactic layer), Why3, Verus (Rust), Creusot (Rust), Prusti (Rust),
Kani (Rust → CBMC), CBMC (C), Boogie (IR), SPARK/Ada, JML/OpenJML, KeY (Java), Stainless (Scala).

**What it's uniquely good at**
- **Verifies the actual code**, not a model. This is the big advantage over model checking.
- Highly automated *given* the annotations; the SMT solver does the tedious case analysis.
- Widely deployable because the language is nearly a normal language.

**How it fails**
- **Annotation burden is the barrier.** Invariants must be strong enough, and finding them is
  the undecidable part. Solver "unknown"/timeout is common and requires manual ghost code,
  intermediate assertions, or hints.
- SMT solvers are the trusted base: a solver bug can produce a bogus "verified".
- Works best on single-threaded functional code; concurrency needs extra theory.

**Slide version.** *"This is the sweet spot for industry. You write Dafny or annotate Rust, and a
solver checks it. It's the technology behind Cedar, and it's where an ordinary team has a real
chance."*

---

## 4. Abstract interpretation (sound over-approximation)

**Idea.** Define an abstract domain (intervals, octagons, polyhedra) and interpret the program
over it. Because the abstraction *over-approximates* every concrete behaviour, a proof on the
abstraction is a proof on the program. Always terminates, never misses a real error (sound), but
may produce **false alarms** (incomplete).

**Tools.** Astrée/AstréeA, Polyspace, AbsInt, Facebook/Meta Infer, MIRAI, CPAchecker, Frama-C
(value analysis), IKOS.

**What it's uniquely good at**
- **Scales to millions of lines** — the only family that does. Astrée proved the absence of
  runtime errors in the fly-by-wire software of the Airbus A340 (~132,000 lines of C) with a
  remarkably low false-alarm rate after domain-specific tuning
  ([Cousot et al., ESOP 2005](https://pcousot.github.io/publications/CousotEtAl-ESOP05.pdf),
  [overview](https://www.di.ens.fr/~cousot/AI/IntroAbsInt.html)).
- Fully automatic, no annotations required in principle.
- Ideal for "no runtime errors ever" (division by zero, overflow, out-of-bounds, uninitialised
  read) across a whole codebase.

**How it fails**
- **False alarms**, and tuning them out is domain expertise.
- Precision is bought with cost: intervals are cheap and imprecise; polyhedra are precise and
  expensive.
- Proving *functional correctness* with abstract interpretation is possible but much harder than
  proving *absence of runtime errors*.

**Slide version.** *"Abstract interpretation is how you get 'this entire codebase has no undefined
behaviour' without annotating anything. It's the quiet industrial workhorse — you've probably run
it as a linter without knowing."*

---

## 5. Types & lightweight static analysis (the free tier)

**Idea.** A decidable, cheap approximation of correctness, enforced by the compiler on every
commit.

**Tools.** Rust's borrow checker + type system, Liquid Haskell (refinement types), F*'s effect
system, TypeScript/Flow, Wuffs (memory-safe by construction), clippy/linters, CBMC's
`--bounds-check`.

**What it's uniquely good at**
- **Cost is effectively zero at the margin** — it's already in the build.
- Catches the highest-frequency real-world bug classes: memory safety, null, data races.
- Rust's ownership is a decidable fragment of separation logic shipped to millions of developers.
  Empirically, this is the largest-scale deployment of formal-methods *ideas* in history.

**How it fails**
- Only expresses what's decidable and cheap, so it says nothing about your protocol being right.
- Can be fought tooth and nail (lifetime gymnastics), which is a UX cost, not a soundness cost.
- "It type-checks" is rung 0 of 5 ([specifications.md](specifications.md#the-specification-ladder-from-weak-to-strong)).

**Slide version.** *"You are all already running formal methods on every commit. The question is
whether you want the dial at 'types' or at 'properties'."*

---

## How to choose (and what to combine)

| Situation | Best first move | Why |
|---|---|---|
| Concurrent/distributed protocol design | **Model checking** (TLA+) | finds interleaving bugs tests can't reach |
| A single tricky algorithm, verified code | **Deductive verification** (Dafny/Kani/Verus) | verifies real code with solver automation |
| Whole codebase, undefined behaviour | **Abstract interpretation** | scales, no annotations |
| Deep mathematics / compiler / kernel | **Theorem proving** | only option strong enough |
| Authorization / policy | **SMT over a model + differential testing** | the Cedar pattern |
| You have no budget and no buy-in | **Types + property-based tests** | rung 0–1, free-ish |

**The combinations that actually work in industry**

1. **Model checking + testing** (AWS): TLA+ on the design, then conventional tests on the code.
   Catches design bugs early; tests catch coding bugs.
2. **Deductive verification + differential random testing** (Cedar, Microsoft SymCrypt): prove a
   model, then show by massive random testing that production code matches the model.
3. **Abstract interpretation + deductive verification** (safety-critical): whole-program soundness
   first, then targeted functional proofs on critical functions.
4. **Types + everything else** (Rust): get memory safety for free, then add Kani/Creusot proofs
   where the value is.

> **Pedagogical point for the talk:** these are not competing religions. AWS's experience report
> is explicit that they use TLA+ *and* testing *and* code review, and that TLA+ answers a question
> none of the others can.

---

Next → [automated-reasoning.md](automated-reasoning.md): the solvers that power families 3 and 5.
