# Temporal logic: safety, liveness, and stuttering

> **TL;DR.** Reactive systems don't have a "final answer" — they run forever and talk to an
> environment. So you specify them with **temporal logic**, whose formulas are true or false of
> *infinite sequences of states*. Three ideas do most of the work: the **safety/liveness**
> distinction (what kind of thing can go wrong determines what technique can find it), **fairness**
> (what the environment is allowed to do), and **stuttering invariance** (why refinement proofs
> work at all). Get these three right and TLA+, Ivy, Veil, SPIN, and NuSMV all become readable.

This page is the theory. [model-verifiers.md](../05-tools/model-verifiers.md) is the tools, with
worked specs in TLA+, Ivy, and Veil.

---

## Theory

### 1. Traces are the objects of study

A **state** is an assignment of values to variables. A **trace** (behaviour) is an infinite
sequence of states:

```
   σ = s₀ s₁ s₂ s₃ …
```

A **property** is a set of traces. A specification is satisfied by a system when every trace the
system can produce is in that set. That's the whole setup:

| Concept | Formal object |
|---|---|
| State | assignment to variables |
| Trace / behaviour | `σ ∈ S^ω` (an ω-word) |
| Property | a set of traces, `P ⊆ S^ω` |
| System satisfies `P` | every execution trace of the system is in `P` |
| Specification | a property (or a conjunction of them) |

**Why infinite?** Because a reactive system is never "done". A trace that stops is a crashed system,
not a correct one. This is the single conceptual difference from the input/output view in
[specifications.md](specifications.md): there, a program transforms an input to an output. Here, a
system runs forever alongside an environment.

Two consequences that surprise people:

1. **Termination is not the goal** — for a server, termination *is* the bug. What you want is
   *liveness*: that the system keeps doing useful things.
2. **"Nothing bad happened yet" is not a proof.** A test observes a finite prefix; a property is
   about an infinite sequence. That gap is [why testing cannot be made sound](limits.md).

### 2. LTL: linear temporal logic

**LTL** (Pnueli, 1977) adds temporal operators to ordinary logic. Formulas are evaluated at a
position in a trace:

| Operator | Read | `σ, i ⊨ φ` iff |
|---|---|---|
| `X φ` | **next** | `σ, i+1 ⊨ φ` |
| `G φ` / `□φ` | **always / globally** | `σ, j ⊨ φ` for all `j ≥ i` |
| `F φ` / `◇φ` | **eventually / finally** | `σ, j ⊨ φ` for some `j ≥ i` |
| `φ U ψ` | **until** | some `j ≥ i` with `σ, j ⊨ ψ`, and `σ, k ⊨ φ` for all `i ≤ k < j` |
| `φ W ψ` | **weak until** | `φ U ψ` or `G φ` |

`X` and `G` are enough to define the rest: `F φ ≡ true U φ`, `φ U ψ ≡ ψ ∨ (φ ∧ X(φ U ψ))`.

Derived and useful: `G F φ` ("infinitely often"), `F G φ` ("eventually always"), and the
**leads-to** operator `φ ↝ ψ ≡ G(φ ⇒ F ψ)`, also written `φ ~> ψ`.

#### The patterns you actually write

| English | LTL |
|---|---|
| Nothing bad ever happens | `G ¬bad` |
| Something good eventually happens | `F good` |
| Every request is eventually answered | `G (req → F ack)` |
| A request is answered *while* the system stays healthy | `G (req → (healthy U ack))` |
| The system is never permanently stuck | `G (enabled → F taken)` |
| Behavior repeats forever | `G F progress` |
| Eventually stabilizes | `F G stable` |
| A `forbid` policy always overrides | `G (forbid ∧ permit → ¬allow)` |

**A warning about `X`.** The next-time operator looks natural and is almost always a mistake in a
specification you intend to use for *refinement* or *composition*. Section 5 explains why. Short
version: don't use it.

#### LTL vs CTL vs TLA

| Logic | Quantifies over | Notes |
|---|---|---|
| **LTL** | one timeline at a time; properties of a single trace | linear time |
| **CTL** | pairs path-quantifiers with temporal operators (`AG`, `EF`, …) | branching time; not comparable to LTL in expressive power |
| **CTL\*** | both | subsumes LTL and CTL |
| **μ-calculus** | least/greatest fixpoints | subsumes CTL\*; what model checkers reduce to |
| **TLA** | LTL + action formulas + quantification over state functions | strictly more expressive than LTL |

The LTL/CTL incomparability catches people out: `AG(EF p)` ("from everywhere, `p` is still
reachable") is expressible in CTL and *not* in LTL. Conversely `FG p` is LTL-expressible and not
CTL-expressible. See [logics.md](logics.md) for the logical languages themselves.

### 3. Safety and liveness — the distinction that determines your tooling

Intuition:

- **Safety** = "nothing bad ever happens". Violation is witnessed by a **finite** prefix.
- **Liveness** = "something good eventually happens". Violation requires an **infinite** trace.

Now make it precise, because the precision is what tells you which tool can help.

#### The definitions (Alpern & Schneider, 1985)

> A property `P` is a **safety** property iff: for every trace `σ ∉ P`, there is a **finite prefix**
> `σ[0..n]` such that **no extension** of that prefix is in `P`.
>
> A property `P` is a **liveness** property iff: **every finite prefix can be extended** to a trace
> in `P`.

Put geometrically: put the **Cantor topology** on traces, where a basic open set is "all traces
with this finite prefix". Then:

> **Safety properties are exactly the closed sets.**
> **Liveness properties are exactly the dense sets.**

That is not an analogy — it is a theorem, and it makes two things immediate:

**Theorem (decomposition).** *Every property is the intersection of a safety property and a liveness
property.*

$$\text{every } P = \underbrace{\text{closure}(P)}_{\text{safety}} \cap \underbrace{L}_{\text{liveness}}$$

**Consequences you can use as a working engineer:**

1. **A safety violation is always finitely witnessed.** So a model checker can find it, a fuzzer can
   hit it, and a counterexample trace is a finite, displayable, reproducible object. This is why
   safety is tractable and liveness is not.
2. **A liveness violation is never finitely witnessed.** You cannot exhibit "it never happens" with
   a finite run. So liveness needs either an argument about *all* runs (a proof) or a model checker
   with a fairness assumption and a finite state space.
3. **Safety and liveness are not disjoint and not exhaustive.** "Always x > 0" is safety; "eventually
   x = 0" is liveness; and a property can be both (e.g. "always x > 0 *and* eventually x = 0", whose
   safety part is `G(x>0)` and liveness part is `F(x=0)`).

#### The Manna–Pnueli hierarchy

The two-way split is the coarse version. Manna and Pnueli refined it into a hierarchy classified by
the structure of the ω-automaton recognising the property
([PODC'90](https://dl.acm.org/doi/10.1145/93385.93394); also implemented in
[Spot](https://spot.lrde.epita.fr/hierarchy.html)):

| Class | Shape | Example | Recognising automaton |
|---|---|---|---|
| **Safety** | `G p` | `G ¬(cs₁ ∧ cs₂)` — mutual exclusion | all states accepting |
| **Guarantee** (reachability) | `F p` | `F (all nodes agree)` | some state accepting |
| **Obligation** | boolean combination of safety and guarantee | `G p → F q` | — |
| **Response** (recurrence) | `G F p` | `G F (every request served)` | accepting states visited infinitely often |
| **Persistence** | `F G p` | `F G (leader stable)` | eventually always accepting |
| **Reactivity** | boolean combination of response and persistence | `G F req → G F ack` | general |

Each class strictly contains the previous ones. **Why you should care:** the class of your property
determines what will prove it. Safety needs an invariant; guarantee needs a reachability argument;
response needs fairness plus a well-founded measure (or a ranking argument); reactivity needs the
full machinery, and is where automated tools most often give up.

**`G F p` deserves special attention** — "infinitely often" is the class most production liveness
properties live in (`G F (progress)`, `G F (heartbeat)`, `G (req → F ack)` = `G F ack` under
`G req`), and it is exactly the class that weak/strong fairness makes provable.

### 4. Fairness: constraining the environment

A specification says what the system may do. It also has to say what the **environment** will
eventually do — otherwise you can't prove anything liveness-shaped, because the environment is
allowed to never schedule your process.

| Notion | TLA notation | Meaning |
|---|---|---|
| **Weak fairness** | `WF_v(A)` | if `A` is **continuously enabled**, `A` eventually happens |
| **Strong fairness** | `SF_v(A)` | if `A` is **enabled infinitely often**, `A` happens infinitely often |

Formally, with `⟨A⟩_v` meaning "`A` happens and `v` changes" and `[A]_v` meaning "`A` happens or
nothing changes":

```
   WF_v(A) ≡ ◇□(¬Enabled ⟨A⟩_v) ∨ □◇⟨A⟩_v
   SF_v(A) ≡ □◇(¬Enabled ⟨A⟩_v) ∨ □◇⟨A⟩_v
```

Simplified further:

```
   WF_v(A)  ≡  "if A stays enabled forever, A eventually occurs"
   SF_v(A)  ≡  "if A keeps becoming enabled, A eventually occurs"
```

`SF` is strictly stronger than `WF`. The classic case where you need `SF` and not `WF`: a critical
section guarded by a semaphore that is repeatedly grabbed and released. The waiter's action is
enabled *infinitely often* but never *continuously*, so `WF` gives you nothing and `SF` gives you
progress. This distinction is the source of a large fraction of real liveness bugs.

**The trap:** adding fairness is a *modelling assumption*, not a proof step. If you assume `WF` on a
scheduler that doesn't provide it, you have proved a theorem about a system that doesn't exist.

### 5. Stuttering invariance — why refinement works

This is the most under-appreciated idea in the page, and it is what makes TLA work.

**Definition.** Two traces are **stuttering-equivalent** if one can be obtained from the other by
duplicating or deleting *finite* repetitions of states:

```
   s₀ s₁ s₂ s₃ …        and        s₀ s₀ s₁ s₁ s₁ s₂ s₃ …
   └──────────┬────────┘           └──────────┬───────────┘
        stuttering-equivalent (same "interesting" states, different durations)
```

A property `P` is **stuttering-invariant** (stuttering-insensitive) if it is closed under
stuttering-equivalence: `σ ∈ P` iff every stuttering-equivalent `σ' ` is in `P`.

**Why you want this.** An implementation has *more steps* than its specification. A three-step
implementation of an atomic abstract action must not be a refinement violation merely because it
took three steps. Stuttering invariance is what licenses the implementation to "pad" the abstract
behaviour with extra steps.

```
   abstract:        A ──────────────► B
   implementation:  A ──► a₁ ──► a₂ ──► B
                              └────────┘ these steps must be allowed to be "invisible"
                                          to the abstract-level specification
```

**The theorem.** Lamport introduced stuttering invariance deliberately when designing TLA
(*What Good is Temporal Logic?*, 1983), and Peled and Wilke proved the sharp characterisation:

> **Peled–Wilke.** An LTL property is stuttering-invariant **iff** it can be expressed in LTL
> **without the next-time operator `X`**.

**The practical rules that follow — memorize these two:**

1. **Never use `X` in a specification you will refine, compose, or implement.** `X φ` says "φ holds
   in the very next state", which is a statement about step granularity. Any implementation with a
   different step granularity breaks it. This is why TLA omits `X` entirely from its standard
   repertoire.
2. **Write `[Next]_v`, not `Next`.** In TLA, `[A]_v ≡ A ∨ UNCHANGED v` — "either the action happens
   or the variables in `v` don't change". That disjunct *is* the stuttering step, and it is what
   makes a spec stuttering-invariant. `⟨A⟩_v ≡ A ∧ ¬UNCHANGED v` is the non-stuttering version, and
   it is what you use inside fairness assumptions.

**A two-line demonstration of the failure.** Let `x` be a counter.

```
   Spec₁ ≡ x = 0 ∧ □[x' = x + 1]_x            ← stuttering-invariant; increments ✓
   Spec₂ ≡ x = 0 ∧ □[x' = x + 1]_x ∧ □(X(x > 0))   ← "x > 0 in the next state"
```

`Spec₂` is satisfied by a one-step increment. Now consider an implementation `Impl` that first
updates a temporary variable and *then* increments `x` — every `x`-visible behaviour is the same.
`Impl` refines `Spec₁` but **not** `Spec₂`, because at the intermediate state `X(x > 0)` is false.
Nothing about `x` changed; only the step count did. **That is the entire argument for stuttering
invariance**, and it costs you nothing to respect it: just don't write `X`.

### 6. Refinement: connecting levels

**Refinement** is the relation "this concrete thing is an acceptable implementation of that abstract
spec". Written `Impl ⇒ Spec`, meaning *every trace of `Impl` is* (after stuttering) *a trace of
`Spec`*.

In TLA, the proof obligations for `Impl ⇒ Spec` are:

```
   1.  Init_Impl        ⇒  Init_Spec                    (initial states agree)
   2.  [Next_Impl]_v    ⇒  [Next_Spec]_w                (every step is a Spec step or stutters)
   3.  fairness of Impl ⇒  fairness of Spec             (liveness transfers)
   4.  v and w related by a REFINEMENT MAPPING          (the abstract state is a function of the concrete state)
```

Obligation 2 is where stuttering does its work: whenever a concrete step doesn't correspond to any
abstract step, it must be a *stuttering* step at the abstract level — which is exactly what
`[·]_w` permits.

**When a refinement mapping doesn't exist.** Sometimes the abstract state isn't a function of the
concrete state, and you need to add machinery:

| Technique | What you add | Reference |
|---|---|---|
| **History variables** | extra state recording what happened | — |
| **Prophesy (prophecy) variables** | extra state predicting what *will* happen | Abadi & Lamport, 1991 |
| **Auxiliary variables** | both, for completeness | Abadi & Lamport, *The Existence of Refinement Mappings* |

**Abadi–Lamport completeness theorem:** with stuttering, history variables, and prophecy variables,
*every* refinement has a refinement mapping. That is the theoretical reason the technique is not a
hack.

**Practical upshot:** refinement lets you verify a small abstract protocol once, then prove each
implementation level refines it — which is how [seL4](../03-applications/case-studies.md#1-sel4--the-verified-microkernel)
gets from an abstract spec down to C, and how Veil and Ivy structure distributed-protocol proofs.

### 7. How to prove: safety, liveness, refinement

#### Proving safety — inductive invariants

The rule, in TLA:

```
                        Init ⇒ I        I ∧ [Next]_v ⇒ I'
   (INV1)               ─────────────────────────────────────
                        Init ∧ □[Next]_v  ⇒  □ I
```

To prove a safety property `P`, find an invariant `I` with `I ⇒ P`. **`I` must be *inductive*: it
must be preserved by every step.** The hard part is that the obvious invariant usually isn't
inductive, and you must **strengthen** it.

```
   Goal:  prove □P
   Try:   I₀ = P                 — not inductive
   Fix:   I₁ = P ∧ J₁            — still not inductive
   Fix:   I₂ = P ∧ J₁ ∧ J₂      — inductive ✓
```

**How do you find `J`?** That's the whole game, and every tool in this space is a different answer:

| Technique | How it finds the strengthening |
|---|---|
| Human insight | read the protocol, think about *why* it's correct |
| **CTI (counterexample to induction)** | the tool exhibits a state satisfying `I` whose successor violates `I`; you add a clause excluding it |
| **Interactive generalization** (Ivy) | same loop, but obligations are checked in a **decidable** logic so the CTI is always explainable |
| **Automatic invariant inference** | Houdini, IC3/PDR, interpolation, abstract interpretation |
| **Abstraction / CEGAR** | check on a coarse model, refine the abstraction when a spurious counterexample appears |
| **Bounded model checking + `k`-induction** | check depth `k`, then prove the induction step |

**This is the bottleneck of the entire field.** The invariant is the undecidable part (see
[limits.md](limits.md)), which is why the tools differ mainly in how well they help you find it.

#### Proving liveness — leads-to calculus

Liveness proofs are built from **leads-to** (`↝`, `~>`) properties, using a small calculus. These
rules are standard (Manna–Pnueli; Chandy–Misra; Lamport's TLA book chapter 8):

```
(Reflexivity)     p ↝ p

(Transitivity)    p ↝ q,   q ↝ r
                  ─────────────────
                        p ↝ r

(Disjunction)     p ↝ r,   q ↝ r
                  ─────────────────
                      p ∨ q ↝ r

(Conjunction)     p ↝ q,   p ↝ r
                  ─────────────────
                      p ↝ q ∧ r

(Implication)     p ⇒ q   ⟹   p ↝ q            (any safety property gives liveness "for free")

(Weakening)       p ↝ q,   q ⇒ r   ⟹   p ↝ r

(Well-founded)    ∀n :  p ∧ (rank = n) ↝ ( q ∨ (p ∧ rank < n) )
                  ────────────────────────────────────────────
                                  p ↝ q
```

The **well-founded rule** is how you prove that a loop terminates or a request is eventually
served: find a `rank` into a well-founded set that strictly decreases on every step that doesn't
reach the goal. `Nat` with `<` is the usual choice; lexicographic products and multisets are the
usual upgrades.

**Fairness rules.** The well-founded rule gives you "the rank cannot decrease forever", but it does
not make anything *happen*. You need fairness to turn "enabled" into "eventually taken". Lamport's
TLA book provides four rules for this:

| Rule | Assumption used | Shape of what you prove |
|---|---|---|
| **WF1** | weak fairness of one action | `p` stays true until the action fires, and the action is enabled while `p` holds |
| **WF2** | weak fairness, with a decreasing rank | combines `WF1` with a well-founded measure |
| **SF1** | strong fairness of one action | `p` eventually stays true until the action fires |
| **SF2** | strong fairness with a rank | as above, for `SF` |

The intuition behind all four: **`WF`/`SF` is the only bridge from "can happen" to "does happen".**
Without a fairness assumption, no liveness property is provable for a system with an adversarial
environment.

**A worked liveness proof sketch.** For `G(req → F ack)` in a two-step protocol (process, then
ack), with `WF` on both actions:

```
   1.  req ∧ ¬ack            ⇒  Enabled⟨Process⟩        (it can run)
   2.  WF(Process)           gives   req ∧ ¬ack ↝ processing
   3.  processing            ⇒  Enabled⟨Ack⟩
   4.  WF(Ack)               gives   processing ↝ ack
   5.  transitivity of ↝     gives   req ∧ ¬ack ↝ ack
   6.  implication           gives   G(req → F ack)
```

Every step is mechanical. The *insight* was in steps 1 and 3 — establishing enabledness — which is
exactly why liveness proofs feel different from safety proofs: they are about *opportunity*, not
about *state*.

#### Proving refinement

Obligations 1–4 from §6. In practice:

1. Prove the abstract spec's safety by induction (§7.1).
2. Prove the implementation's safety by induction.
3. Prove the refinement mapping commutes with each concrete step (§6.2).
4. Transfer liveness using the same fairness structure.

Tools help at different points: TLC/Apalache check finite instances; TLAPS discharges the proof
obligations; Ivy makes the obligations decidable; Veil generates both the model check *and* the
inductive proof in Lean.

### 8. What is decidable, and why it matters for tool choice

The expressiveness–decidability–automation trade-off is the axis along which the tools differ:

| Setting | Logic | Decidable? | Consequence |
|---|---|---|---|
| **Finite-state** model checking | LTL/CTL over a finite Kripke structure | ✅ (PSPACE-complete for LTL) | fully automatic; state explosion is the limit |
| **Parameterised** safety (Ivy's target) | EPR / FAU fragments | ✅ | invariant checking is automatic; finding the invariant is interactive |
| **Infinite-state** safety with arithmetic | first-order + theories | ❌ in general | SMT gives `unknown`; human or AI must supply invariants |
| **Full temporal logic with nesting** | LTL / TLA over infinite state | ❌ | proofs, not search |
| **Any non-trivial semantic property** | — | ❌ (Rice) | see [limits.md](limits.md) |

**The engineering reading:** *decidability determines whether a failed proof is explainable.* This
is Ken McMillan's argument for Ivy's design — a heuristic prover "fails in ways that are
unpredictable and often not understandable by a human user", whereas a decidable logic guarantees
that a proof failure yields a concrete, displayable scenario. That is why Ivy insists on reducing
every obligation to a decidable fragment, even at the cost of expressiveness.

---

## Tutorial: five worked examples

### Example 1 — Safety, and why the obvious invariant fails

A two-process mutual-exclusion protocol. `pc[i]` is the program counter, `owner` is the lock holder
(`0` = nobody).

```tla
---- MODULE Mutex ----
EXTENDS Naturals
CONSTANT Proc
VARIABLES pc, owner
vars == <<pc, owner>>

Init == pc = [i \in Proc |-> "idle"] /\ owner = 0

Acquire(i) ==
    /\ pc[i] = "idle"
    /\ owner = 0                      \* ← remove this line and safety fails
    /\ owner' = i
    /\ pc' = [pc EXCEPT ![i] = "critical"]

Release(i) ==
    /\ pc[i] = "critical"
    /\ owner' = 0
    /\ pc' = [pc EXCEPT ![i] = "idle"]

Next == \/ \E i \in Proc : Acquire(i)
        \/ \E i \in Proc : Release(i)

\* THE SAFETY PROPERTY
MutualExclusion == \A i, j \in Proc :
    (pc[i] = "critical" /\ pc[j] = "critical") => i = j
====
```

TLC finds the violation in **two steps** when the guard is removed:

```
   1. Acquire(p1)   owner = p1, pc[p1] = "critical"
   2. Acquire(p2)   owner = p2, pc[p2] = "critical"   ← VIOLATION
```

Now **prove** it rather than search it. The invariant is not `MutualExclusion` itself — invariants
about `pc` alone are not preserved, because `Acquire` doesn't inspect the *other* process's `pc`.
The inductive invariant must mention the lock:

```tla
\* The invariant that IS inductive:
Inv == /\ owner \in Proc \cup {0}
       /\ \A i \in Proc : pc[i] = "critical" => owner = i    \* ← the missing piece
       /\ \A i \in Proc : pc[i] \in {"idle", "critical"}

THEOREM Safety == Init /\ [][Next]_vars => []MutualExclusion
  <1>1. Init => Inv                     BY DEF Init, Inv
  <1>2. Inv /\ [Next]_vars => Inv'      BY DEF Next, Acquire, Release, Inv
  <1>3. Inv => MutualExclusion          BY DEF Inv, MutualExclusion
  <1>q. QED                             BY <1>1, <1>2, <1>3
```

*(Sketch. A checkable TLAPS proof requires exact step naming and `DEF` annotations; what
matters here is the obligation structure — `INV1`'s two premises plus `Inv ⇒ P`.)*

**The lesson, and it is the lesson of the whole field:** the property you want (`MutualExclusion`)
is not inductive. What *is* inductive is the stronger statement tying the program counters to the
lock. **Finding that strengthening is the work** — and `owner = i` is exactly the kind of clause a
CTI-driven tool would suggest, because the CTI for `MutualExclusion` alone is "two processes in the
critical section with `owner` pointing at one of them".

### Example 2 — Liveness with a ranking function

Termination-style liveness reduces to a decreasing measure. The smallest example that shows the
whole shape:

```tla
---- MODULE Countdown ----
EXTENDS Naturals
CONSTANT N
ASSUME N \in Nat
VARIABLE n

Init == n = N
Next == n > 0 /\ n' = n - 1
Fairness == WF_n(Next)

Spec == Init /\ [][Next]_n /\ Fairness

\* LIVENESS: the counter reaches zero.
Terminates == (n > 0) ~> (n = 0)
====
```

The proof uses the **well-founded rule** with `rank = n`, measuring into `⟨Nat, <⟩`:

```
   Goal:   n > 0  ↝  n = 0

   1.  (n > 0) ∧ (n = k)  ⇒  Enabled⟨Next⟩_n         -- Next is enabled whenever n > 0
   2.  WF_n(Next)         ⇒  (n > 0) ∧ (n = k) ↝ (n = 0) ∨ (n = k-1)
                                                      -- fairness + the effect of Next
   3.  (n = k-1) means rank decreased                  -- the measure strictly decreased
   4.  well-founded rule on ⟨Nat, <⟩  ⇒  n > 0 ↝ n = 0
```

**Why the ranking function is the right mental model:** it converts a liveness question ("will it
ever happen?") into a safety-shaped one ("can the measure decrease forever?") — and the answer to
the latter is *no*, by well-foundedness. Notice the shape: `rank` must be a function of the state,
and every state change that doesn't satisfy the goal must decrease it.

For nontrivial protocols, `rank` is a tuple — e.g. `(phase, messages outstanding, distance to
leader)` lexicographically ordered. Most real liveness bugs are "the measure can get stuck", which
is precisely a missing fairness assumption or a livelock.

### Example 3 — Stuttering and refinement

An abstract counter that increments once per step, and an implementation that does the same work in
two steps using a temporary variable.

```tla
---- MODULE Refinement ----
EXTENDS Naturals

\* ---------- ABSTRACT ----------
VARIABLE x
AbsInit == x = 0
AbsNext == x' = x + 1
AbsSpec == AbsInit /\ [][AbsNext]_x

\* ---------- CONCRETE ----------
VARIABLES x, tmp
ConInit == x = 0 /\ tmp = 0
ConNext == \/ tmp' = 1 /\ UNCHANGED x         \* a step invisible at the abstract level
           \/ tmp = 1 /\ x' = x + 1 /\ tmp' = 0
ConSpec == ConInit /\ [][ConNext]_<<x, tmp>>

\* ---------- REFINEMENT ----------
\* The refinement mapping: the abstract variable IS the concrete variable.
\* Obligation: every concrete step is either an AbsNext step, or stutters on x.
THEOREM Refines == ConSpec => AbsSpec
  \* <1>1. ConInit => AbsInit
  \* <1>2. [ConNext]_<<x,tmp>> => [AbsNext]_x
  \*         The first disjunct leaves x unchanged — a stuttering step, permitted
  \*         by [AbsNext]_x. This is exactly why the spec uses [ ]_x and not AbsNext.
====
```

Now watch it break if the abstraction quantifies over step counts:

```
   AbsSpecBad == AbsInit /\ [][AbsNext]_x /\ [](X(x > 0))
```

The first concrete step leaves `x = 0`, so at that intermediate state `X(x > 0)` is false and
refinement **fails** — even though no observable abstract behaviour differs. This is the
Peled–Wilke theorem as a practical failure: `X` is not stuttering-invariant, so any refinement
involving an implementation with different step granularity is unprovable. **The fix is to delete
the `X`**, and there is essentially never a reason not to.

### Example 4 — Telling safety and liveness apart

Useful exercise for building intuition. Classify each; the answer is in the reference table below.

| Property | Safety, liveness, both, or neither? |
|---|---|
| `G(x > 0)` | ? |
| `F(x = 0)` | ? |
| `G(x > 0) ∧ F(x = 0)` | ? |
| `G F (x > 0)` | ? |
| `F G (x > 0)` | ? |
| `G(x > 0) → F(x = 0)` | ? |
| `X(x > 0)` | ? |

<details>
<summary>Answers</summary>

| Property | Class | Why |
|---|---|---|
| `G(x > 0)` | **safety** | violation has a finite witness: the first state with `x ≤ 0` |
| `F(x = 0)` | **liveness** | every finite prefix can be extended to one that reaches `x = 0` |
| `G(x > 0) ∧ F(x = 0)` | **both** | the intersection of a safety and a liveness property |
| `G F (x > 0)` | **liveness** | no finite prefix can witness a violation |
| `F G (x > 0)` | **liveness** | same |
| `G(x > 0) → F(x = 0)` | **liveness** | no finite witness; this is the *response* class |
| `X(x > 0)` | **safety** | but **not stuttering-invariant** — the interesting case |

The last row is the one worth remembering: `X(x>0)` *is* a safety property (a one-step violation is
finitely witnessed), yet it is the property you must never write. **Safety ≠ useful.**

</details>

### Example 5 — Why fairness is not optional

```tla
\* Two processes, each willing to enter. Does p1 get in?
SpecNoFairness == Init /\ [][Next]_vars

\* Counterexample: the scheduler simply never runs p1's Acquire.
\* TLC finds it trivially, and the violation is a legitimate behaviour of this spec.
\* The spec is not wrong; it just does not say the scheduler is fair.

SpecWithFairness == Init /\ [][Next]_vars /\ WF_vars(Acquire(p1))
\* Now p1 enters. But note: you have ASSUMED something about the scheduler.
```

The lesson: **a liveness property is only ever proved relative to a fairness assumption.** When you
read a liveness claim in a paper or a spec, the first question is *"under what fairness?"* If the
answer is missing, the claim is not yet a statement about any real system.

---

## Reference

### LTL operator summary

| Syntax | Name | Intuition | Stuttering-invariant |
|---|---|---|---|
| `X φ` | next | φ in the immediately following state | ❌ **avoid** |
| `G φ` / `□φ` | always | φ in all future states | ✅ |
| `F φ` / `◇φ` | eventually | φ in some future state | ✅ |
| `φ U ψ` | until | φ until ψ, and ψ happens | ✅ |
| `φ W ψ` | weak until | `φ U ψ` or `G φ` | ✅ |
| `G F φ` | infinitely often | φ recurs forever | ✅ |
| `F G φ` | eventually always | φ holds from some point on | ✅ |
| `φ ↝ ψ` | leads to | `G(φ ⇒ F ψ)` | ✅ |

### Property classification quick table

| Property | Class | Needs an invariant? | Needs fairness? |
|---|---|---|---|
| `G p` | safety | ✅ | ❌ |
| `F p` | guarantee | ❌ (reachability) | ✅ |
| `G p → F q` | response | ✅ (for `p`) | ✅ |
| `G F p` | response | ❌ | ✅ |
| `F G p` | persistence | ✅ | sometimes |
| arbitrary boolean combination | reactivity | ✅ | ✅ |
| `X p` | safety | — | — (but don't write it) |

### TLA+ notation you need for this page

| Notation | Meaning |
|---|---|
| `[A]_v` | `A ∨ UNCHANGED v` — action **or stutter**. Makes a spec stuttering-invariant. |
| `⟨A⟩_v` | `A ∧ ¬UNCHANGED v` — action that **changes** `v`. Used inside fairness. |
| `□[Next]_v` | "every step is a `Next` step or leaves `v` unchanged" |
| `WF_v(A)` | weak fairness: if `A` stays enabled, it eventually happens |
| `SF_v(A)` | strong fairness: if `A` is enabled infinitely often, it happens infinitely often |
| `p ↝ q` (`p ~> q`) | leads-to: `G(p ⇒ F q)` |
| `ENABLED A` | the action `A` can be taken in the current state |
| `[][Next]_vars` | the always-boxed next-step relation, the backbone of every TLA+ spec |

### Proof rules summary

| Goal | Rule | Shape |
|---|---|---|
| `□I` (safety) | **INV1** | `Init ⇒ I`, `I ∧ [Next]_v ⇒ I'` |
| `□P` where `P` not inductive | **strengthening** | find `J` with `I = P ∧ J` inductive |
| `p ↝ q` across a step | **transitivity** | decompose into intermediate states |
| `p ↝ q` for a loop | **well-founded** | `rank` decreasing into a well-founded order |
| `p ↝ q` using fairness | **WF1/WF2/SF1/SF2** | prove enabledness, then invoke fairness |
| `Impl ⇒ Spec` | **refinement** | init, step (`[Next]`), fairness, refinement mapping |
| `Impl ⇒ Spec` with hidden state | **auxiliary variables** | history and/or prophecy variables (Abadi–Lamport) |

### Tool roles, mapped to the theory

| Task | Automatic? | Tools |
|---|---|---|
| Find a safety violation in a finite instance | ✅ | TLC, SPIN, NuSMV, Veil's `#model_check`, Alloy |
| Find a safety violation symbolically | ✅ | Apalache, CBMC, Ivy's `bmc` |
| Prove safety in an *unbounded/parameterised* system | interactive invariant + decidable check | **Ivy**, **Veil** |
| Prove safety by machine-checked proof | interactive | TLAPS, Veil/Lean, Rocq, Isabelle |
| Check liveness in a finite instance | ✅ (given fairness) | TLC, SPIN, NuSMV |
| Prove liveness in general | interactive, via leads-to + fairness + ranking | TLAPS, Veil/Lean, Isabelle |
| Prove refinement | interactive | TLAPS, Veil, Ivy's modular refinement |

---

## References

- **Pnueli, A.** *The Temporal Logic of Programs.* FOCS 1977 — the origin of LTL for programs
  (Turing Award 1996).
- **Lamport, L.** *Proving the Correctness of Multiprocess Programs.* IEEE TSE, 1977 — introduced
  the safety/liveness vocabulary.
- **Lamport, L.** *What Good is Temporal Logic?* IFIP 1983 — introduced **stuttering invariance**
  and the TLA viewpoint.
- **Lamport, L.** *The Temporal Logic of Actions.* ACM TOPLAS 16(3), 1994.
  [PDF](https://lamport.azurewebsites.net/pubs/lamport-actions.pdf)
- **Lamport, L.** *Specifying Systems: The TLA+ Language and Tools for Hardware and Software
  Engineers.* Addison-Wesley, 2002. [Free online](https://lamport.azurewebsites.net/tla/book.html) —
  chapters 5–8 cover invariants, liveness, and the WF1/WF2/SF1/SF2 rules.
- **Alpern, B. & Schneider, F.B.** *Defining Liveness.* Information Processing Letters 21(4), 1985.
  [PDF](https://cs.nyu.edu/~apanda/classes/sp25/papers/alpern85defining.pdf) — the topological
  characterisation (safety = closed, liveness = dense) and the decomposition theorem. Dijkstra Prize
  2018.
- **Manna, Z. & Pnueli, A.** *A Hierarchy of Temporal Properties.* PODC 1990.
  [ACM](https://dl.acm.org/doi/10.1145/93385.93394) — safety/guarantee/obligation/response/
  persistence/reactivity. Also their book *The Temporal Logic of Reactive and Concurrent Systems*
  (Springer, 1992).
- **Peled, D. & Wilke, T.** *Stutter-Invariant Temporal Properties are Expressible Without the
  Next-Time Operator.* Information Processing Letters, 1997 — the precise theorem behind §5.
- **Browne, M., Clarke, E., Grümberg, O.** *Characterizing Finite Kripke Structures in Propositional
  Temporal Logic.* TCS 1988 — stuttering bisimulation.
- **Lehmann, D., Pnueli, A., Stavi, J.** *Impartiality, Justice and Fairness.* ICALP 1981 — the
  fairness notions.
- **Abadi, M. & Lamport, L.** *The Existence of Refinement Mappings.* TCS 82(2), 1991.
  [PDF](https://lamport.azurewebsites.net/pubs/refinement.pdf) — history and prophecy variables, and
  completeness of refinement mappings.
- **Chandy, K.M. & Misra, J.** *Parallel Program Design: A Foundation.* Addison-Wesley, 1988 — the
  leads-to calculus.
- **Clarke, E.M. & Emerson, E.A.** 1981; **Queille & Sifakis** 1982 — CTL and model checking. See
  [logics.md](logics.md).
- **Emerson, E.A. & Halpern, J.** *"Sometimes" and "Not Never" Revisited.* POPC 1983 — LTL vs CTL,
  CTL\*.
- **Kozen, D.** *Results on the Propositional μ-Calculus.* 1983.
- **TLAPS** — the TLA+ Proof System. [github.com/tlaplus/tlapm](https://github.com/tlaplus/tlapm) ·
  [tlapl.us](https://tlapl.us/)
- **Spot** — LTL/ω-automata library with the Manna–Pnueli hierarchy implemented.
  [spot.lrde.epita.fr/hierarchy.html](https://spot.lrde.epita.fr/hierarchy.html)
- [Wikipedia: Linear temporal logic](https://en.wikipedia.org/wiki/Linear_temporal_logic) ·
  [Safety property](https://en.wikipedia.org/wiki/Safety_property) ·
  [Liveness](https://en.wikipedia.org/wiki/Liveness) ·
  [Fairness](https://en.wikipedia.org/wiki/Fairness_(computer_science))

## Further reading

- [model-verifiers.md](../05-tools/model-verifiers.md) — TLA+, Ivy, and Veil in depth, with specs.
- [logics.md](logics.md) — the logical languages these temporal logics sit among.
- [semantics.md](semantics.md) — what a trace *is*, formally, for a given language.
- [distributed-systems.md](../03-applications/distributed-systems.md) — where these techniques earn
  their keep.
- [limits.md](limits.md) — decidability, and why invariant-finding is the bottleneck.
