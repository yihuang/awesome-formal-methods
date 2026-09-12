# Specifications: the actual hard part

> **TL;DR.** Verification is mostly a solved problem for well-scoped things. *Specification* is
> not, and never will be. Every verified system is only as good as the sentence you wrote down
> that said what "correct" means. Engineers who bounce off formal methods usually bounce off
> here, not off the proofs.

---

## The one idea

A verification tool proves an **implication**:

```
     (model of your system)   ∧   (assumed environment)   ⊢   (property)
            ↑                            ↑                        ↑
      you wrote this               you wrote this          you wrote this
```

The tool contributes *rigour*. You contribute *meaning*. If your property is wrong, the proof is
a very expensive way of being confidently wrong. This asymmetry is why every serious FM write-up
spends its first half on specification, not on proofs.

---

## The specification ladder (from weak to strong)

Most engineers think specification means "the strongest possible statement". In practice you
climb:

| Rung | What you state | Cost | Catches |
|---|---|---|---|
| 0 | **Types + no crash** ("this never panics / no UB") | ~free | memory safety, overflow, null, use-after-free |
| 1 | **Assertions / contracts** (`requires`, `ensures`, invariants) | low | local logic errors |
| 2 | **Safety properties** ("nothing bad happens") | medium | protocol violations, invalid states |
| 3 | **Liveness properties** ("something good eventually happens") | higher | starvation, deadlock-freedom, eventual consistency |
| 4 | **Functional correctness** ("output = the mathematically specified answer") | high | everything above + wrong results |
| 5 | **Security / information-flow** ("no secret leaks to low clearance") | highest | side channels, non-interference |

The actionable starting point is **rung 1–2**. seL4 is rung 4–5 and cost ~20 person-years.

---

## The core vocabulary

### Pre/post-conditions and contracts

The oldest and most useful specification device (Floyd 1967, Hoare 1969):

```
{ P }  program  { Q }
```

- `P` = **precondition**: what must be true before (assumed, not proven).
- `Q` = **postcondition**: what is guaranteed after (proven).

In modern notation, as in Dafny:

```dafny
method Abs(x: int) returns (y: int)
  ensures y >= 0
  ensures y == x || y == -x
{
  if x < 0 { y := -x; } else { y := x; }
}
```

The pre/post pair is a *complete* specification of this method — it says nothing about runtime,
memory, or how. **Anything you leave out is unconstrained behaviour.** This is the single most
important sentence in this page.

### Invariants

A property true in *every reachable state*. The workhorse of both model checking and program
verification, because it collapses an infinite set of executions into one state predicate.

```tla
\* The classic: a distributed counter's invariant
Inv == 0 <= sent - acked /\ sent - acked <= Len(buf)
```

Finding the right invariant is where the human insight lives. Strengthen it too much and it
becomes false; too weak and it doesn't imply what you need. **This is precisely the task LLMs are
starting to help with** ([ai-for-fm.md](../04-ai-era/ai-for-fm.md)).

### Safety vs liveness

The most useful dichotomy in the field:

| | Safety | Liveness |
|---|---|---|
| Informal | "Nothing bad ever happens" | "Something good eventually happens" |
| Formally | every finite prefix can be extended to a valid behaviour; a violation is a *finite* trace | a violation requires an *infinite* trace |
| Examples | mutual exclusion, no deadlock, no double-spend, type safety | termination, eventual consistency, no starvation, leader eventually elected |
| Tool behaviour | found by state-space search | needs fairness assumptions; harder for model checkers |
| In a partial-order / temporal logic | `G ¬bad` | `F good` |

Almost every real spec is a conjunction: `safety ∧ liveness`. AWS's framing is exactly this:

> "Safety properties: 'what the system is allowed to do'. Liveness properties: 'what the system
> must eventually do' ... We have found this rigorous 'what needs to go right?' approach to be
> significantly less error prone than the ad hoc 'what might go wrong?' approach."
> — *Use of Formal Methods at AWS* ([PDF](https://lamport.azurewebsites.net/tla/formal-methods-amazon.pdf))

That last sentence is worth emphasising: **formal specification inverts the debugging mindset.** You
don't enumerate failure modes; you state the success condition and let a machine search for
counterexamples.

### Refinement

How a verified abstract model connects to real code:

```
  Abstract spec  ⊒  (is refined by)  Concrete spec  ⊒  Implementation
```

Each step proves the lower level is a *permitted* implementation of the upper. This is the answer
to AWS's most-asked question — *"How do we know the executable code correctly implements the
verified design?"* — and AWS's own honest answer is:

> "We don't [know]. Formal methods help engineers to get the design right, which is a necessary
> first step toward getting the code right. If the design is broken then the code is almost
> certainly broken, as mistakes during coding are extremely unlikely to compensate for mistakes
> in design."

Refinement is the *rigorous* version of that gap-closing, and it's what CompCert, seL4, and
IronFleet actually do. If you don't do refinement, you have verification of a *model*, and you
must say so out loud.

---

## The specification gap (the permanent limitation)

The tool proves `model ⊢ property`. It cannot tell you that `property` is what anyone wanted.

Three flavours of the gap, each with a real failure:

1. **The property is wrong.**
   A verified system can be perfectly correct and useless. Classic illustration: a spec of a
   "sort" that permits returning the input unchanged is trivially satisfied — sorted, yes;
   *a permutation*, not stated.

2. **The model omits reality.**
   seL4's original proof assumed the hardware, the assembly glue, and the boot code behaved. The
   team later added binary verification and explicit assumption lists because
   model-vs-reality gaps are where the remaining risk lives.

3. **The environment assumptions are wrong.**
   Every proof has an `assumed environment` conjunct (see the diagram above). Byzantine-fault
   proofs assume an `n ≥ 3f+1` bound; violate it in production and the theorem is inapplicable,
   not false.

**In one line:** *"A proof is a contract between your model and your property. It tells
you nothing about either."*

---

## How to write a spec an engineer will actually use

Practitioner heuristics, ordered by value:

1. **Start from a bug you had.** Retrofitting a spec onto a system you understand and that
   already failed is the highest-ROI entry point. This is exactly how AWS started.
2. **State "what must go right", not "what might go wrong"** (the AWS inversion).
3. **Model the environment adversarially and explicitly** — list the failure events (network
   partition, disk error, crash, restart, human operator). In TLA+ these become actions.
4. **Write the spec at the level of the design doc**, not the code. If it reads like your design
   doc but is unambiguous, you've got it right. TLA+ is directly marketed as "exhaustively
   testable pseudo-code" for this reason.
5. **Keep the spec small.** A 200-line spec of a protocol is worth more than a 20,000-line spec
   of an app. Verification is a *scoping* discipline.
6. **Version-control the spec next to the code** and re-run the checker in CI. Stale specs are
   worse than none, because they get cited as evidence.
7. **Make the counterexample the deliverable.** Even when the property fails, you got a
   concrete trace — the single most useful artifact FM produces for an engineer.

---

## Two portable spec patterns worth memorising

**Pattern 1 — the ghost/observer spec** (used by Cedar, IronFleet, and every verified
authorization system):

- Write a clear, naive, *obviously correct* implementation of the desired semantics (an oracle).
- Write the optimized/real implementation.
- Prove the real one refines the oracle, or differentially test them.

Cedar's production pipeline is precisely this: a Dafny model with proved properties
(*explicit-permit*, *forbid-overrides-permit*) plus **differential random testing** to show the
Rust production code matches the model
([Amazon Science](https://www.amazon.science/blog/how-we-built-cedar-with-automated-reasoning-and-differential-testing)).

**Pattern 2 — the refinement ladder** (distributed systems):

```
TLA+ spec of the abstract protocol   →  TLC finds a counterexample in 30 seconds
        ↓ (prove refinement)
TLA+ spec of the implementation      →  TLC checks it again
        ↓ (code review / test / refinement proof)
real code
```

The insight: *most distributed-systems bugs live at the abstract level.* Finding them before code
exists is nearly free by comparison.

---

Continue → [logics.md](logics.md): the formal languages these specs are written in.

## References

- **Floyd, R.** *Assigning Meanings to Programs.* 1967.
- **Hoare, C.A.R.** *An Axiomatic Basis for Computer Programming.* CACM 1969.
  [PDF](https://dl.acm.org/doi/10.1145/363235.363259)
- **Dijkstra, E.W.** *Guarded Commands, Nondeterminacy and Formal Derivation of Programs.* CACM 1975.
- **Lamport, L.** *Specifying Systems: The TLA+ Language and Tools for Hardware and Software
  Engineers.* Addison-Wesley, 2002. [Free online](https://lamport.azurewebsites.net/tla/book.html) —
  the reference for writing specifications at the design level.
- **Newcombe, C. et al.** *Use of Formal Methods at Amazon Web Services.* 2014/2015.
  [PDF](https://lamport.azurewebsites.net/tla/formal-methods-amazon.pdf) — the "what needs to go
  right" inversion, the refinement-gap honesty, and the data-modelling aside.
- **Amazon Science.** *How we built Cedar with automated reasoning and differential testing.*
  [Link](https://www.amazon.com/science/blog/how-we-built-cedar-with-automated-reasoning-and-differential-testing) —
  the ghost/observer spec pattern and the `explicit permit` / `forbid overrides permit` properties.
- **Cutler, J. et al.** *Cedar: A New Language for Expressive, Fast, Safe, and Analyzable
  Authorization.* OOPSLA 2024. [PDF](https://arxiv.org/abs/2403.04651)
- [Refinement](https://en.wikipedia.org/wiki/Refinement_(computing)) — the abstraction relation.
