# Taxonomy: what actually counts as "formal methods"?

> **TL;DR.** "Formal methods" is not one thing. It is a family of techniques that share exactly
> one property: **they use mathematics to say something about all behaviours of a system, and a
> machine checks the argument.** Everything else — proofs, model checkers, types, solvers — is
> an implementation detail.

The word "formal" is doing real work: it means *syntax with a precise meaning* (semantics), so a
machine can manipulate it and a human can argue about it. If there's no precise semantics, it's
not formal — it's documentation.

---

## The one test that classifies any tool

Ask two questions:

1. **Is the property quantified over all inputs/behaviours, or sampled?**
   - All → formal verification (proof, model checking, abstract interpretation, type checking).
   - Sampled → testing, fuzzing, property-based testing.
2. **Is the check done by a machine-checkable artifact?**
   - Yes, with a small trusted kernel → high assurance.
   - Yes, but with a large trusted tool → medium assurance (bug in the tool = bug in your proof).
   - No, a human reviewed it → not formal.

Property-based testing sits in an interesting middle: the *property* is formal (universally
quantified, checked by a generator), but the *coverage* is sampled. It is the most underrated
on-ramp, and honest talks should say so rather than gatekeeping it out.

---

## The landscape, in one diagram

```
                   ┌──────────────────────────────────────────────────┐
                   │  What do you want to know?                       │
                   └──────────────────────────────────────────────────┘
                                        │
        ┌───────────────────────────────┼───────────────────────────────┐
        ▼                               ▼                               ▼
   "Does it always                "Does this design              "Can I prove a deep
    do X?"                         have a bug?"                   theorem about it?"
        │                               │                               │
        ▼                               ▼                               ▼
  PROGRAM VERIFICATION          MODEL CHECKING                INTERACTIVE THEOREM PROVING
  (Hoare logic + SMT,           (state-space search,           (dependent type theory,
   contracts, refinement)        temporal logic)                tactics, proof scripts)
        │                               │                               │
   Dafny, F*, Why3,              TLA+/TLC, SPIN,                Lean, Rocq(Coq),
   Verus, Kani, CBMC,            NuSMV, Alloy,                  Isabelle/HOL, HOL4,
   Creusot, Prusti               Apalache                       PVS, ACL2
        │                               │                               │
        └───────────────────────────────┴───────────────────────────────┘
                                        │
                     ┌──────────────────┴──────────────────┐
                     ▼                                     ▼
        ABSTRACT INTERPRETATION                TYPE SYSTEMS & LIGHTWEIGHT STATIC ANALYSIS
        (over-approximate, sound,              (check what's decidable cheaply, in the
         always terminates)                     compiler, on every commit)
        Astrée, AstréeA, Polyspace,             Rust borrow checker, refinement types
        Infer, MIRAI                          (Liquid Haskell), TS/Flow, Wuffs
                     │                                     │
                     └──────────────────┬──────────────────┘
                                        ▼
                          AUTOMATED REASONING (the engine under all of it)
                          SAT (CDCL) · SMT (Z3, cvc5) · first-order ATP (Vampire, E)
```

---

## Four orthogonal choices you're really making

Every formal-methods decision reduces to these four dials. Use them as the talk's mental model.

### Dial 1 — What are you reasoning about?

| Object | Typical target | Example tool |
|---|---|---|
| Program *code* | functional correctness, memory safety, absence of runtime errors | Dafny, Kani, Astrée |
| System *design* | protocol correctness, liveness, deadlock-freedom | TLA+, Alloy, SPIN |
| *Mathematical* statement | a theorem | Lean, Rocq, Isabelle |
| *Hardware* circuit | RTL equivalence, no X-propagation | JasperGold, VC Formal |
| *Policy / configuration* | authorization, access control | Cedar + automated reasoning |
| *Learned model* | robustness, reachability | α,β-CROWN, Marabou |

### Dial 2 — Who supplies the ingenuity?

| Mode | You do | Tool does | Cost profile |
|---|---|---|---|
| **Fully automatic** | write the property | search exhaustively / solve | cheap to write, may not scale or may answer "unknown" |
| **Interactive** | write the proof | check every step | expensive, scales to deep mathematics |
| **Semi-automatic** | annotate (invariants, contracts, ghost code) | discharge obligations | the practical middle ground |

The field's centre of gravity has moved steadily toward *automatic*, and AI is accelerating that.

### Dial 3 — Sound vs. complete (you cannot have both)

- **Sound**: "verified" ⇒ actually true. No false alarms missed, but may fail to prove true things.
- **Complete**: will always answer. But any complete checker for a non-trivial property is
  unsound (it must guess occasionally).

Most industrial tools are **sound but incomplete** — they may say "I couldn't prove it", never
"it's proven" when it isn't. Bug-finding tools (fuzzers, some static analyzers) are deliberately
the opposite: **unsound but complete-ish**, optimized to *find* counterexamples.

This is not an implementation wart, it's Gödel/Turing/Rice
([limits.md](../01-fundamentals/limits.md)).

### Dial 4 — What is the trusted base?

Every verified claim rests on *something* you didn't verify. Be explicit about it:

- **Proof assistants**: a small kernel (de Bruijn criterion) — typically a few thousand lines.
- **SMT-based verifiers**: the solver plus the encoding — a bug here silently invalidates proofs.
- **Model checkers**: the model plus the translation from code/spec to model.
- **Compilers/extraction**: the path from proven source to running binary.

The last one is the classic hole: seL4 later added *binary verification* precisely because the
C-to-binary step was outside the original proof.

---

## What formal methods are NOT

| Not this | Why people confuse it | Actually |
|---|---|---|
| Testing, but more of it | both "find bugs" | FM proves absence; testing demonstrates presence |
| Static analysis / linters | both "check code automatically" | many static analyses are *unsound* heuristics; abstract interpretation is the sound version |
| Theorem proving as in "math proofs" only | the name | industrial FM is mostly about protocols and code, not theorems |
| A silver bullet | vendor marketing | see [`limits.md`](../01-fundamentals/limits.md) — the spec gap never closes |
| The opposite of AI | "AI can't do math" | they are now mutually reinforcing ([`04-ai-era/`](../04-ai-era/index.md)) |

---

## Vocabulary the talk should fix early

Fix these six terms in the first five minutes so the audience isn't lost later. Full definitions
in [`references/glossary.md`](../references/glossary.md).

1. **Specification** — the precise statement of what the system must do.
2. **Property** — a specification fragment, usually *safety* ("nothing bad happens") or
   *liveness* ("something good eventually happens").
3. **Invariant** — a property true in every reachable state; the workhorse of verification.
4. **Counterexample** — a concrete trace proving the property false. This is the *feature* that
   sells FM to engineers: it's a debugger for designs.
5. **Soundness** — verified ⇒ true.
6. **Refinement** — the relation "this concrete implementation is a correct instance of that
   abstract spec". This is how you connect a verified model to real code.
