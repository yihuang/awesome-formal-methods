# Logics: the languages specs are written in

> **TL;DR.** Formal methods are built on a small number of logical languages. Knowing which one
> you're in tells you what the tool can express and where it will hit a wall. For the talk you
> need five: propositional/FO logic, Hoare logic, temporal logic, separation logic, and type
> theory. Everything else is a variant.

---

## 0. The foundation: propositional and first-order logic

**Propositional logic (PL)**: `p ∧ q → ¬r`. Decidable, and the target of SAT solvers. Cheap.

**First-order logic (FOL)**: adds quantifiers over a domain, functions, and predicates —
`∀x. P(x) → ∃y. Q(x,y)`. Still semi-decidable: valid formulas are enumerable, invalid ones may
never terminate. This is the language of SMT solvers (over specific theories) and Alloy (bounded).

Everything below is an *extension* of FOL with domain-specific machinery. That matters for the
talk: it explains why solvers are the engine, and why the extensions are where the difficulty is.

| Logic | Adds | Comes with |
|---|---|---|
| Propositional | — | SAT (NP-complete) |
| First-order | quantifiers, relations | ATPs, SMT with theories |
| Hoare | program state, `{P}C{Q}` | program verifiers |
| Separation | heap, `∗` | memory-safety verifiers |
| Temporal | time, `G/F/X/U` | model checkers |
| Type theory | proofs-as-terms | proof assistants |
| Fixpoint (μ-calculus) | least/greatest fixpoints | everything temporal reduces here |

---

## 1. Hoare logic — reasoning about code

The original program logic (Hoare 1969, building on Floyd 1967). A **Hoare triple**:

```
{ P }  C  { Q }
```

"if `P` holds before `C`, and `C` terminates, then `Q` holds after."

**Partial vs total correctness**: `{P}C{Q}` alone is *partial* — it says nothing if `C` loops
forever. Total correctness is `[P] C [Q]`, adding termination. Most tools prove partial
correctness and handle termination separately (e.g. Dafny's `decreases` clauses). This
distinction is a real trap: "verified" often means "if it returns, it's right".

### The inference rules (the whole system, essentially)

```
ASSIGNMENT      { Q[x := E] }  x := E  { Q }

SEQUENCE        {P} C1 {R}    {R} C2 {Q}
                ─────────────────────────
                        {P} C1; C2 {Q}

CONDITIONAL     {P ∧ B} C1 {Q}      {P ∧ ¬B} C2 {Q}
                ──────────────────────────────────────
                        {P} if B then C1 else C2 {Q}

WHILE           {I ∧ B} C {I}
                ─────────────────────────────    (I is the loop invariant)
                {I} while B do C {I ∧ ¬B}

CONSEQUENCE     P' → P    {P} C {Q}    Q → Q'
                ────────────────────────────────
                        {P'} C {Q'}
```

Two things to notice, and both are slide-worthy:

1. **Assignment runs backwards.** The precondition is the postcondition with the assigned
   expression substituted. Reasoning about imperative code is *backward* reasoning.
2. **The `while` rule requires an invariant you must supply.** There is no algorithm for finding
   it in general (that's the undecidability showing through). This is why program verification is
   *semi-automatic* in practice, and why "AI proposes the invariant" is such an attractive
   research direction.

### Weakest preconditions

Dijkstra (1975) turned Hoare logic into an algorithm: `wp(C, Q)` = the weakest precondition whose
truth makes `C` establish `Q`. Then verification becomes:

```
wp(C, Q)   ⟸   P          ← discharge this with an SMT solver
```

This is the architecture of essentially every automatic program verifier today: compile the
program into a **verification condition** (VC) and hand it to Z3/cvc5. Learn this pipeline once
and Dafny, Why3, F*, Verus, Creusot, Prusti, Boogie, and Kani all become recognisable.

```
   annotated program
        │  (VC generation: Hoare rules / wp)
        ▼
   first-order verification conditions
        │  (SMT solver: Z3, cvc5, Alt-Ergo)
        ▼
   valid  →  verified        invalid  →  counterexample model (a failing input!)
```

**The counterexample is a feature.** When a VC fails, the SMT solver hands back a model — a
concrete input that breaks your assertion. That's a debugger for specifications.

---

## 2. Separation logic — reasoning about memory

Hoare logic struggles with aliasing: if `x` and `y` might point at the same cell, everything
becomes case analysis. Separation logic (Reynolds, O'Hearn, Yang, 2001) adds the **separating
conjunction** `∗`:

```
P ∗ Q     "P and Q hold for *disjoint* parts of the heap"
```

This makes the frame rule possible:

```
FRAME RULE      {P} C {Q}
                ─────────────────────     (C doesn't touch the footprint of R)
                {P ∗ R} C {Q ∗ R}
```

The frame rule is why separation logic scaled: you can verify one function in isolation and know
it composes, without re-verifying the world. Rust's ownership/borrowing system is the
*compile-time, decidable* descendant of separation-logic ideas — which is why Rust is such a
good target for formal verification ([hardware-crypto.md](../03-applications/hardware-crypto.md),
[05-tools/catalog.md](../05-tools/catalog.md)).

Turing Award 2025 context: Reynolds, O'Hearn, and Yang shared the 2025 ACM A.M. Turing Award for
separation logic. ⚠️ *Verify the exact citation text and year wording before it goes on a slide.*

---

## 3. Temporal logic — reasoning about time

Needed because protocols aren't input→output functions; they're *reactive* systems that run
forever and interact with an environment. Pnueli (1977) introduced temporal logic for programs.

### LTL (Linear Temporal Logic) — one timeline

| Operator | Reads | Meaning |
|---|---|---|
| `X φ` | next | φ holds in the next state |
| `G φ` | globally / always | φ holds in all future states |
| `F φ` | finally / eventually | φ holds at some future state |
| `φ U ψ` | until | φ holds until ψ becomes true (and ψ does) |

Standard formulas every engineer already uses implicitly:

```tla
G(request => F(response))     \* every request is eventually answered  (liveness)
G ¬(cs1 /\ cs2)               \* no two processes in the critical section (safety/mutex)
G(pending => X(served \/ pending))   \* work is never silently dropped
```

### CTL (Computation Tree Logic) — quantifies over branches

CTL pairs path quantifiers `A` (all paths) / `E` (exists a path) with temporal operators:
`AG`, `EF`, `AF`, `EG`, …

| Formula | Meaning | Classic use |
|---|---|---|
| `AG ¬bad` | on **all** paths, **always** not-bad | safety |
| `AG (req → AF ack)` | always, every request has *a* path to ack | liveness under nondeterminism |
| `EF good` | there *exists* a path reaching good | reachability / feasibility |

**LTL vs CTL**: LTL can't express "there exists a path", CTL can't easily express
"all paths satisfy this linear-time property". `CTL*` subsumes both; the **μ-calculus** (fixpoint
logic) subsumes `CTL*` and is the theoretical target that most model checkers reduce to.

### Why this matters to engineers

Temporal logic is where "eventually consistent", "no lost updates", "no starvation", and
"retries don't duplicate" stop being English sentences and become checkable. Every distributed
systems spec you've read that had a real bug — Paxos variants, Raft bugs, Chord, cache coherence —
was, in essence, an LTL/CTL property nobody checked.

---

## 4. Type theory — proofs as programs

The **Curry–Howard correspondence**: *propositions are types, proofs are programs, proof-checking
is type-checking.*

| Logic | Programming |
|---|---|
| proposition `A → B` | function type `A -> B` |
| proof of `A → B` | a function from proofs of `A` to proofs of `B` |
| `A ∧ B` | pair type `A × B` |
| `A ∨ B` | sum type `A + B` |
| `∀x. P(x)` | dependent function type `(x : A) → P x` |
| `∃x. P(x)` | dependent pair / sigma type |
| `⊥` (false) | empty type |
| `¬A` | `A → ⊥` |

This is why proof assistants *are* programming languages (Lean, Rocq, Isabelle/HOL, Agda) and why
you can write verified programs in them. It's also why dependent types matter: with `(n : Nat) →
Vec a n` you can state "this function returns a vector of length n", and the type-checker proves
it — a *specification* enforced with zero runtime cost.

```
   Rung 0 of the specification ladder
   (types and no-crash)
        ↑
   is already a formal method. Rust's borrow checker,
   Haskell's types, and TypeScript's checker are all
   lightweight formal verification you already run.
```

**Key insight for the talk:** the audience is *already doing formal methods* and doesn't call it
that. The talk is about turning up the dial from "types" to "properties", not about switching to
a new religion.

---

## 5. Other logics worth naming (one line each)

| Logic | Where it shows up |
|---|---|
| **Relational / bounded FOL** | Alloy — found real bugs in Chord; bounded scope makes it decidable and fast |
| **Refinement types** | Liquid Haskell, F* — types annotated with predicates, discharged by SMT |
| **Description logic** | Ontologies, Semantic Web — decidable fragments of FOL |
| **Higher-order logic (HOL)** | Isabelle/HOL, HOL4 — the workhorse of seL4 |
| **Calculus of Inductive Constructions** | Rocq/Coq's core |
| **Dependent type theory with universes** | Lean 4's core (CIC + proof irrelevance + quotient) |
| **Epistemic / deontic / hyperproperties** | Multi-agent reasoning; **hyperproperties** = properties of *sets* of traces (non-interference, security) — increasingly relevant for AI systems |
| **Probabilistic logics (PCTL)** | Markov chains, randomized protocols, reliability |

---

## Choosing a logic in one table

| I want to state... | Logic | Tool |
|---|---|---|
| "this function returns the right value" | Hoare logic + VC | Dafny, Why3, Verus |
| "this heap manipulation is memory-safe" | separation logic | Iris, Verus, Creusot |
| "this protocol never deadlocks / eventually converges" | temporal logic | TLA+, SPIN, NuSMV |
| "this theorem of mathematics holds" | dependent type theory | Lean, Rocq, Isabelle |
| "this policy never grants access it shouldn't" | FOL over policy model | Cedar + SMT |
| "this type-level invariant is enforced" | types / refinement types | Rust, Liquid Haskell, F* |
| "this neural net is robust to ε-perturbations" | LP/MILP relaxations, abstract domains | α,β-CROWN, Marabou |

---

Next → [techniques.md](techniques.md): the algorithmic side — how these logics get *checked*.
