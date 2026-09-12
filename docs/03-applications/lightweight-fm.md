# Lightweight formal methods: the on-ramp

> **TL;DR.** You will not verify your service this quarter. But you can move up one rung of the
> specification ladder, this sprint, for a few hours of work, and get a real guarantee that
> testing cannot give you. This page is the part of the talk the audience can *act on tomorrow*.

This is the most important page in the wiki for a working-engineer audience. Everything else is
context for this.

---

## The ladder (rung 0 is free, rung 6 is seL4)

| Rung | Practice | Marginal cost | Guarantee you gain | Tool examples |
|---|---|---|---|---|
| **0** | **Types & memory safety** | already paying it | no UB, no data races, no null | Rust, TypeScript, mypy, `-Werror` |
| **1** | **Assertions & contracts** | minutes | local invariants hold at runtime/every call | `assert`, Dafny `requires/ensures`, `debug_assert`, Go `//go:build` checks |
| **2** | **Property-based testing** | hours | property holds for *thousands of generated* inputs | Hypothesis, proptest, fast-check, jqwik, Go fuzz |
| **3** | **Differential / model-based testing** | days | two independent implementations agree | Cedar's DRT pattern, `differential` harnesses |
| **4** | **SMT-in-CI on a critical function** | days | property holds for **all** inputs of that function | Kani (Rust), CBMC (C), Dafny, Why3 |
| **5** | **Model-check a protocol design** | weeks | no safety/liveness violation in any interleaving | TLA+/TLC, Alloy, SPIN, Apalache |
| **6** | **Full functional-correctness proof** | person-years | the implementation refines the spec, for all executions | Lean, Rocq, Isabelle |

**The talk's ask: get to rung 2, and try rung 4 on exactly one function.** That's it.

Why rung 2 is the highest-value rung: it converts a *universally quantified* statement ("for all
inputs, sorting is a permutation and is ordered") into an executable artifact, and the generator
explores inputs you would never think to write. It is 80% of the benefit of rung 4 at 5% of the
cost.

---

## Rung 2 in the languages people actually use

### Python — Hypothesis

```python
from hypothesis import given, strategies as st

def my_sort(xs: list[int]) -> list[int]:
    ...

# The two properties that actually define "sorted"
@given(st.lists(st.integers()))
def test_sort_is_sorted(xs):
    out = my_sort(xs)
    assert all(out[i] <= out[i + 1] for i in range(len(out) - 1))

@given(st.lists(st.integers()))
def test_sort_is_a_permutation(xs):
    from collections import Counter
    assert Counter(my_sort(xs)) == Counter(xs)
```

**The pedagogical gold in this example:** a naive "sort" implementation that returns its input
passes `test_sort_is_sorted` and fails `test_sort_is_a_permutation`. **Specifications are
incomplete by default, and the missing clause is where the bugs live.** This is the specification
gap made concrete in 8 lines of Python — the best 3 minutes in the talk.

Hypothesis also *shrinks* failures to a minimal counterexample, which is exactly the
counterexample-as-debugger value proposition of model checking, at the unit-test level.

### Rust — proptest + Kani

```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn encode_decode_roundtrips(bytes in prop::collection::vec(any::<u8>(), 0..1024)) {
        prop_assert_eq!(decode(&encode(&bytes))?, bytes);
    }
}
```

Then, for one critical pure function, step to rung 4 with **Kani** — the same shape, but
`kani::any()` means *all* values rather than random ones:

```rust
#[kani::proof]
fn check_my_property() {
    let input: u8 = kani::any();          // nondeterministic = universally quantified
    let output = function_under_test(input);
    assert!(meets_specification(input, output));
}
```

Kani is a bit-precise model checker for Rust built on CBMC, and it is particularly good at
**verifying `unsafe` blocks** — where the compiler's guarantees stop. Install is
`cargo install --locked kani-verifier && cargo kani setup`; run in CI via the Kani GitHub Action
([github.com/model-checking/kani](https://github.com/model-checking/kani)).

**This is the single most practical FM tool for a Rust team**, because it requires no rewrite:
annotate an existing function, run it in CI.

### TypeScript / JavaScript — fast-check

```ts
import fc from 'fast-check';

test('parse is inverse of format', () => {
  fc.assert(fc.property(fc.date(), (d) => parse(format(d)).getTime() === d.getTime()));
});
```

Sibling: **jqwik** (Java), **Go** native fuzzing (`func FuzzX(f *testing.F)`), **QuickCheck**
(Haskell, the 1999 original from which all of these descend).

---

## Rung 1: contracts, the cheapest real win

The pre/post-condition idea from [specifications.md](../01-fundamentals/specifications.md) shows up
in almost every language now. The *discipline* is what matters, not the tooling:

| Practice | Where |
|---|---|
| `requires` / `ensures` (machine-checked) | Dafny, F*, SPARK/Ada, Verus |
| Assertions on invariants at boundaries | any language |
| Design-by-contract annotations + runtime checks | Eiffel (origin), JML/OpenJML, `@contract` in Python |
| Schema/type validation at every boundary | Pydantic, Zod, protobuf — *this is rung 1* |

**Slide-worthy reframing:** "You already write specifications. `zod` schemas, protobuf
definitions, and Rust type signatures *are* specifications. The question is whether a machine
checks them, and how much they say."

---

## Rung 5: model checking a design (the highest-leverage rung per hour)

This is where the dramatic wins are, and the artifact is written *instead of* prose + diagrams, not
in addition to them.

A TLA+ spec of a lock, in full, is about this long:

```tla
---- MODULE Mutex ----
EXTENDS Naturals

VARIABLES pc, owner      \* pc[i] is the program counter of process i

Init == pc = [i \in {1,2} |-> "idle"] /\ owner = 0

Acquire(i) ==
  /\ pc[i] = "idle"
  /\ owner = 0
  /\ owner' = i
  /\ pc' = [pc EXCEPT ![i] = "critical"]

Release(i) ==
  /\ pc[i] = "critical"
  /\ owner' = 0
  /\ pc' = [pc EXCEPT ![i] = "idle"]

Next == \E i \in {1,2}: Acquire(i) \/ Release(i)

\* SAFETY: never two processes in the critical section. A machine checks this exhaustively.
MutualExclusion == \A i, j \in {1,2}: (pc[i] = "critical" /\ pc[j] = "critical") => i = j
====
```

Two minutes of writing. TLC then checks `MutualExclusion` against **every possible interleaving**
— and if you delete the `owner = 0` guard, it hands you the exact two-step trace that breaks it.

**The pitch:** *"How long would it take you to be sure this lock is right by reading it? TLA+ takes
two minutes and is sure."*

**The other artifact worth producing:** a spec of a retry/idempotency scheme, or a
leader-election protocol, or a cache-coherence rule. Distributed-systems bugs are design bugs and
design bugs are cheap to find *before* the code exists.

**Tooling note:** TLC is explicit-state (great for finding bugs); **Apalache** is a symbolic,
SMT-backed TLA+ checker that handles some specs TLC can't, under the same modelling assumptions
([apalache-mc.org](https://apalache-mc.org/)).

---

## Choosing your entry point (decision table)

| You have | Do this | Tool |
|---|---|---|
| A tricky pure function | PBT now, SMT-in-CI if critical | Hypothesis / proptest → Kani |
| An `unsafe` Rust block | SMT-in-CI | Kani |
| A concurrency/retry/idempotency design | model check the design | TLA+ / PlusCal |
| A data-structure invariant | PBT + SMT | Hypothesis + Kani/Prusti |
| A serialization format | round-trip + differential PBT | fast-check / proptest |
| An authorization policy | model + differential testing | Cedar + DRT pattern |
| A long-lived public API contract | property tests as the contract | Hypothesis / proptest |
| A protocol across 3 services | model check the design | TLA+ + Apalache |
| An evolved C++ codebase | bounded model checking | CBMC |
| A cryptographic primitive | **don't** — use a verified library | HACL*/EverCrypt, SymCrypt |

---

## The 5 things to do in your first week

Copy this into the talk as a closing slide.

1. **Pick the function that broke production last quarter.** Verify or property-test *that*. Not a
   greenfield module — the one that already hurt. (This is exactly how AWS started with TLA+.)
2. **Write the property in two clauses** — one for the happy result, one for what must be
   *preserved* (permutation, ordering, idempotency, no secret leaked). Missing the second clause is
   the most common bug.
3. **Find a generator, not a test case.** Hypothesis / proptest / fast-check. Let the machine pick
   inputs.
4. **Take one pure function to rung 4** (`cargo kani`, or Dafny/Why3 for C/Java). Feel the
   difference between "1000 random inputs passed" and "proved for all inputs".
5. **Write one TLA+ spec of a design you're currently arguing about in review comments.** Two
   hours. Bring the counterexample trace to the design meeting. This is the step that converts
   your team.

## The honest limits of the lightweight path

| You might think | Reality |
|---|---|
| "PBT gives me the same guarantee as verification" | No — it's sampled. It finds more than hand-written tests, but a pass is not a proof. That's fine; it's 80/5. |
| "Kani proves my whole program" | It proves the annotated function, bounded on loops by unwinding depth. Bounded ≠ unbounded. |
| "TLA+ checked my code" | It checked your *design/model* ([refinement gap](../01-fundamentals/specifications.md#refinement)). |
| "One verification pass and we're done" | Verification is a CI gate, not an event ([anti-patterns](../01-fundamentals/limits.md#5-anti-patterns-to-name-so-the-audience-recognises-them-at-work)). |
| "This replaces testing" | No. It complements it. AWS uses both; Cedar uses both; seL4 uses both. |

---

Next → [adoption-gap.md](adoption-gap.md): why, if this is so good, it hasn't already happened
to you.
