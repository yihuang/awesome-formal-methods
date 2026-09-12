# Model verifiers: TLA+, Ivy, and Veil

> **TL;DR.** A "model verifier" doesn't check your code — it checks a *model* of your design, by
> asking whether any reachable state violates a property. The three tools on this page take three
> genuinely different positions on the central trade-off. **TLA+** is maximally expressive
> (infinite state, liveness, refinement) and gives the work back to you. **Ivy** deliberately
> restricts expressiveness so that every proof obligation lands in a *decidable* logic — sacrificing
> reach for the guarantee that a failed proof is always explainable. **Veil** embeds protocol
> modelling in Lean 4 and runs three verification modes over the same model: concrete model
> checking, symbolic model checking, and machine-checked proof.
>
> The theory behind all three (LTL, safety/liveness, fairness, stuttering, refinement) is in
> [temporal-logic.md](../01-fundamentals/temporal-logic.md).

---

## What the three tools actually are

| | TLA+ | Ivy | Veil |
|---|---|---|---|
| **What it is** | a specification language + model checker + proof system | a language designed so obligations are decidable | a Lean 4 DSL + verification framework |
| **Logic** | TLA (LTL + actions + set theory) | EPR and other decidable fragments | Lean 4 (dependent type theory) |
| **Decidable?** | ❌ in general | ✅ by design | ❌ in general, but model checking is |
| **Proves** | safety, liveness, refinement | safety (liveness via temporal prophecy) | safety (primarily) |
| **Infinite / parameterised state** | yes, via proofs | yes, via decidable fragments | yes, via Lean proofs |
| **Origin** | Lamport, 1990s → | McMillan, Padon et al., PLDI 2016 | Verse lab (NUS), built on Lean 4 |
| **Sweet spot** | distributed protocol design; liveness; refinement | parameterised protocol safety; composable specs; testing | distributed protocols where you want model checking *and* proof over one model |

**They are not competitors.** TLA+ is where you *design*; Ivy is what you reach for when you need a
parameterised safety proof you can actually explain; Veil is what you use when you want the
counterexample search and the proof to live in the same Lean artifact.

---

## The design space in one picture

Every model verifier is a point in a triangle, and you cannot maximise all three corners:

```
                        expressiveness
                        (what you can say)
                              ▲
                             ╱ ╲
                            ╱   ╲
                           ╱     ╲
                          ╱       ╲
                         ╱         ╲
              TLA+ ●────╱───────────╲────● Ivy
                    ╱                 ╲
                   ╱                   ╲
                  ╱      ● Veil         ╲
                 ╱                       ╲
                ▼─────────────────────────▼
        automation                   decidability / explainability
        (push-button)                (a failed proof is always understood)
```

The engineering consequence, and the reason Ivy exists:

> A heuristic prover fails in ways that are "unpredictable and often not understandable by a human
> user" (McMillan). A decidable logic guarantees that a failed proof produces a concrete, finite,
> displayable scenario. **You trade expressiveness for the guarantee that you will always
> understand your own proof failures.**

---

## TLA+

### The idea

TLA (**T**emporal **L**ogic of **A**ctions) is a logic in which the *system* and its *properties* are
written in the same language, and the logic is **stuttering-invariant** by construction — which is
what makes refinement provable ([§5 of the theory page](../01-fundamentals/temporal-logic.md#5-stuttering-invariance--why-refinement-works)).

A specification has exactly one shape:

```
   Spec  ≡  Init  ∧  □[Next]_vars  ∧  Fairness
            ─┬─     ──────┬──────     ────┬───
             │            │                │
      initial states      │         WF/SF for progress
                 every step is Next, or nothing changes
                 (the "[ ]_vars" is the stuttering step)
```

Three things make this distinctive and worth learning even if you never use TLA+:

1. **`□[Next]_vars` allows stuttering**, so a spec describes *behaviour*, not *step counts* — exactly
   what refinement needs.
2. **It is untyped and mathematical** (sets, functions, records) rather than a programming language,
   so you describe *what* must hold at a level above implementation.
3. **Properties live in the same language as the spec**, so a theorem like
   `Spec ⇒ □Inv` or `Spec ⇒ (req ↝ ack)` is a formula, not a separate DSL.

### The toolchain

| Tool | Role | When |
|---|---|---|
| **TLC** | explicit-state model checker | default; finds counterexamples fast; needs a finite model |
| **Apalache** | symbolic, SMT-backed | when TLC's state space explodes; supports `k`-induction |
| **TLAPS** | proof system (`tlapm`) with SMT/Isabelle/Zenon backends | when you need a proof, not just a check |
| **PlusCal** | imperative-looking frontend that compiles to TLA+ | engineers who prefer pseudocode |
| **VS Code extension / Toolbox** | editing, running TLC, viewing traces | always |
| **TLA+ Community Modules** | reusable operators (sequences, functions, …) | as soon as you write real specs |

**The workflow that actually gets used:** write a spec → run TLC on a small model → *get a
counterexample* → fix the design → repeat. Most of the value is in that loop, and the counterexample
is the product. Formal proof with TLAPS is the exception, not the rule.

### Worked example: a resource allocator with a safety *and* a liveness property

Small enough to read, rich enough to show both property classes and a fairness assumption.

```tla
---- MODULE Allocator ----
EXTENDS Naturals, FiniteSets

CONSTANTS Client, Resource

VARIABLES
    owner,      \* Resource -> Client \cup {None}: who holds each resource
    waiting     \* Client -> SUBSET Resource : what each client has asked for

None == CHOOSE c : c \notin Client

vars == <<owner, waiting>>

TypeOK ==
    /\ owner \in [Resource -> Client \cup {None}]
    /\ waiting \in [Client -> SUBSET Resource]

Init ==
    /\ owner = [r \in Resource |-> None]
    /\ waiting = [c \in Client |-> {}]

\* A client requests a set of resources. It may already hold some.
Request(c) ==
    /\ waiting[c] = {}                       \* one outstanding request at a time
    /\ \E req \in SUBSET Resource :
          req # {} /\ waiting' = [waiting EXCEPT ![c] = req]
    /\ UNCHANGED owner

\* A client takes one resource it asked for, if nobody holds it.
Acquire(c) ==
    /\ \E r \in Resource :
          /\ owner[r] = None
          /\ r \in waiting[c]
          /\ owner'   = [owner EXCEPT ![r] = c]
          /\ waiting' = [waiting EXCEPT ![c] = waiting[c] \ {r}]

\* A client releases everything it holds. (A no-op if it holds nothing.)
Release(c) ==
    /\ owner' = [r \in Resource |-> IF owner[r] = c THEN None ELSE owner[r]]
    /\ UNCHANGED waiting

Next == \/ \E c \in Client : Request(c)
        \/ \E c \in Client : Acquire(c)
        \/ \E c \in Client : Release(c)

\* ---------------- SAFETY ----------------
\* A resource is held by at most one client at a time.
\* (True by construction here, because owner is a function — which is the point:
\*  choose a representation that makes your safety property structural.)
MutualExclusion == \A r \in Resource : owner[r] = None \/ owner[r] \in Client

\* ---------------- LIVENESS ----------------
\* Fair scheduling: every client's Acquire eventually fires when enabled.
Fairness == \A c \in Client : WF_vars(Acquire(c))

Spec == Init /\ [][Next]_vars /\ Fairness

\* ---------------- THE NAIVE LIVENESS ATTEMPT ----------------
\* "Every waiting client is eventually served."
\* This does NOT hold for Spec as written, and TLC finds the counterexample:
\* a client acquires a resource and simply never releases it, so the waiter
\* starves forever. The spec is not wrong -- it just never said the environment
\* is fair. Stating liveness REQUIRES stating assumptions on the environment.
ProgressNaive == \A c \in Client : (waiting[c] # {}) ~> (waiting[c] = {})

\* ---------------- THE HONEST FORMULATION ----------------
Holds(c) == \E r \in Resource : owner[r] = c

\* Assumption 1: every holder eventually releases (needs WF on Release).
HolderReleases == \A c \in Client : Holds(c) ~> ~Holds(c)

\* Assumption 2: releases are weakly fair.
FairRelease == \A c \in Client : WF_vars(Release(c))

SpecFair == Init /\ [][Next]_vars /\ Fairness /\ FairRelease

\* Now the progress property is a theorem, not a hope -- and the two assumptions
\* above are exactly what it rests on. A liveness claim without its fairness
\* assumptions is not a claim about any real system.
Progress == \A c \in Client : (waiting[c] # {}) ~> (waiting[c] = {})
====
```

The last property is deliberately written to make a point: **you cannot state useful liveness without
stating what the environment does.** The full version needs "every holder eventually releases", which
is itself a liveness property requiring its own fairness assumption on `Release`. This is why
liveness proofs are usually done as a chain of leads-to properties rather than one big formula:

```tla
\* The realistic formulation, decomposed:
HolderReleases == \A c \in Client : (owner[c] # None) ~> (owner[c] = None)   \* needs WF(Release(c))
RequestServed  == \A c \in Client : (waiting[c] # {}) ~> (waiting[c] = {})   \* follows from the above + WF(Acquire)
```

**What TLC does with this:** with `Client` and `Resource` finite, TLC checks `MutualExclusion`
immediately and checks the liveness properties once you add `Spec` as the specification and the
properties as `PROPERTY` — TLC's liveness checking is more expensive than invariant checking, which
is the practical face of the safety/liveness distinction.

**What TLAPS does:** turns the safety claim into an obligation `Init ∧ □[Next]_vars ⇒ □Inv` and
discharges `INV1`'s two premises (see
[the theory page](../01-fundamentals/temporal-logic.md#proving-safety--inductive-invariants)). For
liveness, you use the WF1/WF2 rules to establish each `↝` step, then combine with transitivity.

### Strengths and honest limits

| ✅ | ❌ |
|---|---|
| Expressive enough for real distributed protocols (S3, DynamoDB) | No push-button path to a proof; TLAPS requires real effort |
| Liveness and refinement are first-class | TLC state explosion on anything with big value domains |
| Stuttering-invariant by design, so refinement proofs are clean | Unfamiliar mathematics; a genuine learning curve |
| Published spec corpus (Paxos, Raft, …) to learn from | The *model* is verified, not the code |
| The counterexample trace is immediately actionable | Typo-level errors can be silent; you must run TLC to catch them |

---

## Ivy

### The idea

Ivy's design goal is not maximal power. It is **transparency**: that a proof failure is always
explainable, and that the artifacts are useful to engineers who can't do the proof themselves.

Two mechanisms achieve this:

**(a) Decidable logics.** Ivy's language is engineered so that proof obligations reduce to
fragments with a decision procedure — chiefly **EPR** (Effectively Propositional Logic, the `∃*∀*`
fragment) and related decidable theories. In a decidable fragment, "the invariant is not inductive"
is not a heuristic timeout; it is a **model you can print**. That is the whole point.

```
   Heuristic prover (SMT, unbounded arithmetic):
        "unknown"  →  user has no idea why, or what to change

   Decidable fragment (EPR):
        "not inductive"  →  here is a concrete finite state satisfying I
                            whose successor violates I   ← generalize this into a lemma
```

**(b) Interactive generalization.** This is the PLDI 2016 contribution. The loop is:

```
   1.  User writes a safety property P.
   2.  Ivy checks whether the current invariant is inductive.
   3.  If not, Ivy produces a CTI — a counterexample to induction — and VISUALIZES it.
   4.  The user reads the scenario and GENERALIZES it into a new lemma (or strengthens a
       quantifier, or identifies a missing hypothesis about the environment).
   5.  Repeat until inductive.
```

The tool does not find the invariant for you. It makes the *reason* the invariant is insufficient
obvious, in a logic where "obvious" is guaranteed rather than hoped for.

### Modularity and design artifacts

Ivy's other distinguishing feature is that proofs are **modular**, so verification decomposes into
local, decidable problems:

| Mechanism | What it does |
|---|---|
| **`isolate`** | verify a component assuming its specification, discharging the assumption separately |
| **Abstract types** | verify the protocol assuming a total order, then implement the order with integers/bitvectors — the same *refinement* idea from [the theory page](../01-fundamentals/temporal-logic.md#6-refinement-connecting-levels) |
| **Composable temporal specs** | if each component locally satisfies its spec, the composition satisfies the composition of specs |
| **Test generation** | Ivy generates **test benches and test oracles from the specification**, so a component can be tested rigorously against its own spec — catching bugs that integration tests miss |

That last row is the underrated one. Ivy's specs are not just proof artifacts; they are
**executable specifications that generate tests**, which is why the approach travels to teams that
will never write a proof. The QUIC work (McMillan & Zuck, SIGCOMM 2019) is the flagship: a formal
specification of the QUIC protocol used for testing real implementations.

### What an Ivy proof looks like (schematic)

Ivy's surface syntax is close to the Veil example below — `action` blocks, `require` guards,
`relation` declarations, and named invariants. The *shape* of the work is:

```
   # schematic — see the Ivy repository/docs for exact syntax

   type node
   relation pending(N: node, M: node)          # "N has a message queued for M"
   relation leader(N: node)

   action send(n: node, next: node) = {
       require is_next(n, next);
       pending(n, next) := true
   }

   action recv(sender: node, n: node, next: node) = {
       require is_next(n, next);
       require pending(sender, n);
       pending(sender, n) := false;
       if sender = n { leader(n) := true }
       else { if le(n, sender) { pending(sender, next) := true } }
   }

   # the safety property
   invariant [single_leader] leader(N) & leader(M) -> N = M

   # LEMMAS you add during interactive generalization:
   invariant [leader_greatest] leader(L) -> le(N, L)
   invariant [self_msg_greatest] pending(L, L) -> le(N, L)
```

Those two extra invariants are not decoration — they are the *output of the CTI loop*. The first
`invariant` you write will not be inductive, and the CTIs tell you which of these you need. Compare
this directly with Veil's `Ring` example below: it is the same protocol, the same two auxiliary
invariants, reached by the same mechanism.

### Strengths and honest limits

| ✅ | ❌ |
|---|---|
| Proof failures are always explainable (decidable fragments) | Restricted expressiveness on purpose; not every protocol fits the fragment |
| Parameterised / unbounded systems, not just finite instances | Finding invariants is still interactive — Ivy assists, it does not infer |
| Modular refinement makes large proofs tractable | ~~Liveness~~ — historically safety-focused; liveness needs temporal prophecy (Padon et al., FMCAD 2018) |
| Composable specs generate **tests**, so the artifact is useful beyond proofs | Syntax and tooling are less beginner-friendly than TLA+ |
| Real deployments: QUIC, cache-coherence interfaces | Smaller community than TLA+ |

---

## Veil

### The idea

Veil is a **multi-modal** framework for distributed protocols, built **inside Lean 4**. Its premise:
the same protocol model should support *bug finding* and *proof*, in one artifact, in one language.

Four capabilities, from the project's own framing:

| Capability | Mechanism |
|---|---|
| **Specify** | a DSL that guides you toward specs admitting automated proofs; Lean's full power when you need it |
| **Find bugs** | concrete **and symbolic** model checking, with counterexample traces rendered in Lean's InfoView |
| **Discover properties** | an interactive **CTI generator** — the same generalization loop as Ivy, for inductive invariants |
| **Verify** | push-button automation, escalating to Lean's tactic language when automation isn't enough |

So Veil sits between the other two: it has TLA+-style model checking *and* Ivy-style CTI-driven
invariant discovery *and* machine-checked proofs — all in one Lean development, which means the
proof and the model checker can never drift apart.

### Worked example: leader election on a ring

This is the project's own example, reproduced because it fits the page's purpose exactly — it is
the same protocol as the Ivy sketch above, and the same two auxiliary invariants appear.

```lean
import Veil

veil module Ring

type node
instantiate tot : TotalOrder node
instantiate btwn : Between node

open Between TotalOrder

relation leader : node → Bool
relation pending : node → node → Bool

#gen_state

after_init {
  leader N := false
  pending M N := false
}

ghost relation isNext (n : node) (next : node) :=
  ∀ Z, n ≠ next ∧ ((Z ≠ n ∧ Z ≠ next) → btw n next Z)

action send (n next : node) {
  require isNext n next
  pending n next := true
}

action recv (sender n next : node) {
  require isNext n next
  require pending sender n
  pending sender n := false
  if (sender = n) then
    leader n := true
  else
    if (le n sender) then
      pending sender next := true
}

safety [single_leader] leader N ∧ leader M → N = M
invariant [leader_greatest] leader L → le N L
invariant [self_msg_greatest] pending L L → le N L

#gen_spec

#model_check { node := Fin 7 }

sat trace {
  any 3 actions
  assert (∃ l, leader l)
}

unsat trace {
  any 5 actions
  assert (∃ n₁ n₂, n₁ ≠ n₂ ∧ leader n₁ ∧ leader n₂)
}

#check_invariants

end Ring
```

*(Example from [veil.dev](https://veil.dev/), reproduced for exposition.)*

What to notice, because each line is a design decision:

| Construct | What it does |
|---|---|
| `veil module Ring` | a protocol module with its own namespace, inside a Lean file |
| `instantiate tot : TotalOrder node` | **abstract types**: the protocol assumes a total order; you *implement and verify it separately* — this is Ivy's modularity idea, and it is [refinement](../01-fundamentals/temporal-logic.md#6-refinement-connecting-levels) |
| `ghost relation isNext …` | a **ghost** definition: specification-only, no runtime cost, but available to invariants |
| `after_init { … }` | initial-state predicate, written imperatively |
| `action send … { require … }` | a transition with a guard; `require` is the enabledness condition |
| `safety [single_leader] …` | the property to prove; named for the proof output |
| `invariant [leader_greatest] …` | **an auxiliary inductive invariant** — the output of the CTI loop |
| `#gen_spec` | generates the `Init ∧ □[Next]_vars` specification, in TLA+ shape |
| `#model_check { node := Fin 7 }` | **concrete** model checking: search for violations up to 7 nodes |
| `sat trace { any 3 actions; assert … }` | *find a trace* satisfying the assertion — bug hunting / sanity checking the spec is not vacuous |
| `unsat trace { any 5 actions; assert … }` | *prove no such trace exists within the bound* — bounded safety checking |
| `#check_invariants` | attempt the **deductive** proof with automation |

**The `unsat trace`/`sat trace` pair is worth dwelling on.** `unsat trace` is bounded model
checking, which gives a *bounded* guarantee. `#check_invariants` is the unbounded proof. Having both
in one file means you get the fast counterexample search *and* the general proof without switching
tools or re-modelling — and the two can never disagree, because they share one definition.

**And `sat trace` addresses a failure mode nothing else on this page addresses:** it lets you check
that your *model is not vacuous*. If the actions can never fire, every safety property is trivially
true and every proof succeeds. `sat trace { any 3 actions; assert (∃ l, leader l) }` states "a leader
*can* be elected" — an existence claim that catches a dead specification. This is the
[specification gap](../01-fundamentals/specifications.md#the-specification-gap-the-permanent-limitation) being tested
directly, and it is a genuinely good idea.

### Strengths and honest limits

| ✅ | ❌ |
|---|---|
| One model, three verification modes: concrete MC, symbolic MC, Lean proof | Primarily **safety**; liveness is not its focus |
| CTI-driven invariant discovery, like Ivy | Requires knowing some Lean for the hard cases |
| Counterexamples render in the Lean InfoView — an actual debugging experience | Newer and smaller ecosystem than TLA+ |
| `sat trace` catches vacuous specifications | Syntax is a DSL to learn, on top of Lean |
| Proofs and model checks share one definition, so they cannot drift | Fewer published case studies than TLA+ |

---

## Comparison: choosing between them

| If you need… | Use | Why |
|---|---|---|
| To design a protocol and get counterexamples fast | **TLA+ / TLC** | the fastest path from idea to a broken design |
| **Liveness** (`G(req → F ack)`, no starvation) | **TLA+** (+ TLAPS) | liveness is first-class; Veil and Ivy are safety-first |
| **Parameterised / unbounded** safety (N processes, any N) | **Ivy** or **Veil** | finite model checking cannot reach N = ∞ |
| To *understand why* your invariant isn't inductive | **Ivy** | decidable obligations ⇒ the failure is always explainable |
| Model checking **and** proof, in one artifact | **Veil** | multi-modal by design, in Lean |
| Composable specs that also generate **tests** | **Ivy** | test benches and oracles from specifications |
| Refinement from abstract spec down toward code | **TLA+ / TLAPS**, **Veil** | both support refinement; TLAPS most mature |
| To check a model isn't vacuous | **Veil** (`sat trace`) | explicit existence checks |
| Structural/data-model bugs, bounded scope | **Alloy** | see [catalog.md](../05-tools/catalog.md) |
| Concurrent algorithms with message passing | **SPIN** | mature LTL model checking |
| Hardware-ish control logic with CTL properties | **NuSMV / nuXmv** | BDD/symbolic, CTL |

### The three-step path that usually works

```
   1.  TLA+          design the protocol, run TLC, iterate on counterexamples
        │             ← cheap, fast, catches design bugs before code
        │             ← add liveness once the design is stable
        ▼
   2.  Ivy or Veil   once the design is fixed, prove it for unbounded N
        │             ← Ivy if explainability of proof failures is the priority
        │             ← Veil if you want model checking + proof in one Lean artifact
        ▼
   3.  TLAPS / Lean  mechanise the proof you care about permanently
                      ← the artifact that survives staff turnover
```

You rarely need step 3. Steps 1 and 2 are where the bugs are.

---

## Reference

### TLA+ quick reference

```tla
---- MODULE Name ----          \* module header
EXTENDS Naturals, Sequences    \* imports
CONSTANT C                     \* parameters of the model
VARIABLE v                     \* state variables
vars == <<v>>                  \* tuple, for [Next]_vars

Init == …                      \* initial predicate
Next == …                      \* next-state relation
Spec == Init /\ [][Next]_vars /\ Fairness

\* properties
Inv         == …                \* a state predicate
Safety      == □Inv             \* or just "Inv", since TLC checks it as an invariant
Liveness    == req ~> ack       \* leads-to
MutualExcl  == \A i, j : …
====
```

| Concept | Syntax |
|---|---|
| Stuttering-permitting step | `[Next]_vars` |
| Non-stuttering step | `⟨Next⟩_vars` |
| Weak fairness | `WF_vars(Action)` |
| Strong fairness | `SF_vars(Action)` |
| Leads-to | `p ~> q` or `p ↝ q` |
| Enabled | `ENABLED Action` |
| Temporary variable | `\E x \in S : …` in `Next`; declared in `VARIABLES` |
| Model config | a separate `.cfg` file: `INIT`, `NEXT`, `INVARIANT`, `PROPERTY`, `CONSTANT` |

### Ivy quick reference

| Concept | Meaning |
|---|---|
| **EPR** | Effectively Propositional Logic: the `∃*∀*` fragment, decidable |
| **Decidable fragment** | the design constraint that makes proof failures explainable |
| **CTI** | counterexample to induction — a state satisfying `I` whose successor violates `I` |
| **Interactive generalization** | the user's response to a CTI: strengthen the invariant or hypothesis |
| **`isolate`** | verify a component against its spec, discharging the assumption elsewhere |
| **Abstract type** | assume a total order; implement and verify it separately (modular refinement) |
| **Composable spec** | if components satisfy their specs, the composition satisfies the composition |
| **Test oracle generation** | tests derived from specifications, for use against real implementations |

- Repository: [github.com/microsoft/ivy](https://github.com/microsoft/ivy) ·
  docs: [microsoft.github.io/ivy](https://microsoft.github.io/ivy/) ·
  McMillan's page: [mcmil.net](http://mcmil.net/wordpress/2019/12/09/ivy/)

### Veil quick reference

| Construct | Meaning |
|---|---|
| `veil module X … end X` | a protocol module inside a Lean file |
| `type node` | declare an abstract type (uninterpreted) |
| `instantiate t : TotalOrder node` | assume a theory; verify its implementation separately |
| `relation r : node → Bool` | mutable state |
| `ghost relation g …` | specification-only definition (no runtime cost) |
| `after_init { … }` | initial-state predicate |
| `action a (x : T) { require …; … }` | a guarded transition |
| `safety [name] …` | the property to prove |
| `invariant [name] …` | an auxiliary inductive invariant (CTI output) |
| `#gen_state`, `#gen_spec` | generate the state type and the `Init ∧ □[Next]_vars` spec |
| `#model_check { node := Fin 7 }` | concrete model checking |
| `sat trace { … }` / `unsat trace { … }` | existence / bounded-nonexistence of a trace |
| `#check_invariants` | attempt the deductive proof |

- Site: [veil.dev](https://veil.dev/) · docs: [veil.dev/docs](https://veil.dev/docs/) ·
  playground: [try.veil.dev](https://try.veil.dev) ·
  Lean use case: [lean-lang.org/use-cases/veil](https://lean-lang.org/use-cases/veil/)

### Where to start, concretely

| You have | Do this |
|---|---|
| 2 hours | [Lamport's TLA+ video course](https://lamport.azurewebsites.net/video/videos.html), then [learntla.com](https://learntla.com/) |
| a protocol you keep arguing about | write the TLA+ spec, run TLC, bring the counterexample to the design review |
| a design that's stable and needs a real proof | try **Veil**'s `#model_check` + `#check_invariants` loop first — it's the gentlest entry to deductive verification of protocols |
| a parameterised safety property you need to explain | **Ivy**, and expect to iterate on invariants via CTIs |
| liveness, not just safety | **TLA+** with `WF`/`SF` and the leads-to rules |

---

## References

- **Lamport, L.** *Specifying Systems: The TLA+ Language and Tools for Hardware and Software
  Engineers.* Addison-Wesley, 2002. [Free online](https://lamport.azurewebsites.net/tla/book.html)
- **Lamport, L.** *The Temporal Logic of Actions.* ACM TOPLAS 16(3), 1994.
  [PDF](https://lamport.azurewebsites.net/pubs/lamport-actions.pdf)
- **Lamport, L.** *What Good is Temporal Logic?* IFIP 1983 — stuttering invariance.
- **Yu, Y., Manolios, P., Lamport, L.** *Model Checking TLA+ Specifications.* CHARME 1999 — TLC.
  [PDF](https://lamport.azurewebsites.net/pubs/tlc.pdf)
- **Konnov, I., Kukovec, J., Tran, T.-H.** *TLA+ Model Checking Made Symbolic.* OOPSLA 2019 — Apalache.
- **Cousineau, D., Doligez, D., Lamport, L., Merz, S., Ricketts, D., Vanzetto, H.** *TLA+ Proofs.*
  FM 2012. [PDF](https://lamport.azurewebsites.net/pubs/tla-proofs.pdf) — TLAPS.
- **TLAPS** — [github.com/tlaplus/tlapm](https://github.com/tlaplus/tlapm) · [tlapl.us](https://tlapl.us/)
- **Padon, O., McMillan, K.L., Panda, A., Sagiv, M., Shoham, S.** *Ivy: Safety Verification by
  Interactive Generalization.* PLDI 2016.
  [PDF](https://cs.nyu.edu/~apanda/assets/papers/pldi16.pdf) ·
  [ACM](https://dl.acm.org/doi/10.1145/2908080.2908118) — **the primary source for Ivy's approach**.
- **McMillan, K.L. & Padon, O.** *Deductive Verification in Decidable Fragments with Ivy.* SAS 2018.
  [PDF](http://mcmil.net/pubs/SAS18.pdf)
- **Taube, M., Losa, G., McMillan, K.L., Padon, O., Sagiv, M., Shoham, S., Wilcox, J.R., Woos, D.**
  *Modularity for Decidability of Deductive Verification with Applications to Distributed Systems.*
  PLDI 2018. [DOI](https://doi.org/10.1145/3192366.3192414) — `isolate` and modular proofs.
- **Padon, O., Hoenicke, J., McMillan, K.L., Podelski, A., Sagiv, M., Shoham, S.** *Temporal
  Prophecy for Proving Temporal Properties of Infinite-State Systems.* FMCAD 2018.
  [PDF](http://mcmil.net/pubs/FMCAD18.pdf) — how Ivy handles liveness.
- **McMillan, K.L. & Zuck, L.D.** *Formal Specification and Testing of QUIC.* SIGCOMM 2019.
  [PDF](http://mcmil.net/pubs/SIGCOMM19.pdf) — specs as test oracles.
- **McMillan, K.L.** *Modular Specification and Verification of a Cache-Coherent Interface.*
  FMCAD 2016.
- **McMillan, K.L.** *Ivy project page.* [mcmil.net](http://mcmil.net/wordpress/2019/12/09/ivy/) —
  the transparency and design-artifacts framing quoted on this page.
- **Veil.** *Multi-Modal Verification of Distributed Protocols.*
  [veil.dev](https://veil.dev/) · [docs](https://veil.dev/docs/) —
  the `Ring` example and the four-capability framing.
- **Veil** — [Lean use case page](https://lean-lang.org/use-cases/veil/)
- **verse-lab/veil** — [github.com/verse-lab/veil](https://github.com/verse-lab/veil)
- **Lamport, L.** *Computation and State Machines.* 2008 —
  [PDF](https://lamport.azurewebsites.net/pubs/state-machine.pdf) — the behavioural-reasoning
  framework underneath TLA+.
- [Apalache](https://apalache-mc.org/) · [TLA+ home](https://lamport.azurewebsites.net/tla/tla.html) ·
  [learntla.com](https://learntla.com/) · [SPIN](https://spinroot.com/) ·
  [NuSMV](https://nusmv.fbk.eu/) · [Alloy](https://alloytools.org/)

## Further reading

- [temporal-logic.md](../01-fundamentals/temporal-logic.md) — LTL, safety/liveness, fairness,
  stuttering invariance, refinement, and the proof rules these tools implement.
- [distributed-systems.md](../03-applications/distributed-systems.md) — why this is the highest-ROI
  application area.
- [blockchain.md](../03-applications/blockchain.md) — protocols under adversarial economics, where
  these techniques are applied to real money.
- [lightweight-fm.md](../03-applications/lightweight-fm.md) — the on-ramp if you're starting from
  property-based tests rather than specifications.
