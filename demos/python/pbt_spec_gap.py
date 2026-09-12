#!/usr/bin/env python3
"""
pbt_spec_gap.py — the specification gap, executable, with zero dependencies.

Two lessons in one file:

  1. Property-based testing: state a *universally quantified* property and let
     the machine generate the inputs. This is rung 2 of the adoption ladder and
     the highest-value-per-hour thing in this whole repository.

  2. THE SPECIFICATION GAP: a weak property is satisfied by a useless program.
     "The output is sorted" is satisfied by a function that returns the empty
     list. The missing clause is "the output is a permutation of the input" —
     and the missing clause is where the bugs live.

In real projects, use a mature library instead of the toy harness below:

    Python:  pip install hypothesis
    Rust:    cargo add --dev proptest
    JS/TS:   npm i -D fast-check
    Java:    jqwik
    Go:      native testing.F fuzzing
    Haskell: QuickCheck (the 1999 original)

Those libraries also *shrink* failures to a minimal counterexample, which is the
same value proposition as a model checker's counterexample trace: a minimal
reproducer you can paste into a ticket.

Run:
    python3 pbt_spec_gap.py
"""

from __future__ import annotations

import random
from collections import Counter
from typing import Callable, List, Optional, Tuple


# ---------------------------------------------------------------------------
# A toy property-based testing harness (so this file needs no dependencies)
# ---------------------------------------------------------------------------

def for_all_lists(prop: Callable[[List[int]], Optional[str]],
                  trials: int = 500,
                  max_len: int = 8,
                  seed: int = 0) -> Tuple[bool, Optional[List[int]], Optional[str]]:
    """Generate random lists, check `prop`. On failure, shrink to a minimum.

    `prop` returns None if it holds, or a message describing the violation.
    """
    rng = random.Random(seed)
    for _ in range(trials):
        xs = [rng.randint(-3, 3) for _ in range(rng.randint(0, max_len))]
        msg = prop(xs)
        if msg is not None:
            return False, shrink(xs, prop), msg
    return True, None, None


def shrink(xs: List[int], prop: Callable[[List[int]], Optional[str]]) -> List[int]:
    """Greedily remove elements and simplify values while the failure persists."""
    current = list(xs)
    changed = True
    while changed:
        changed = False
        # try removing one element
        for i in range(len(current)):
            candidate = current[:i] + current[i + 1:]
            if prop(candidate) is not None:
                current, changed = candidate, True
                break
        if changed:
            continue
        # try simplifying a value toward zero
        for i, v in enumerate(current):
            if v == 0:
                continue
            candidate = current[:i] + [v // 2 if v > 0 else -((-v) // 2)] + current[i + 1:]
            if candidate != current and prop(candidate) is not None:
                current, changed = candidate, True
                break
    return current


# ---------------------------------------------------------------------------
# The system under test — including a deliberately broken one
# ---------------------------------------------------------------------------

def real_sort(xs: List[int]) -> List[int]:
    return sorted(xs)


def bad_sort(xs: List[int]) -> List[int]:
    """A 'sorting' function that discards the data. It IS sorted. It is useless."""
    return []


# ---------------------------------------------------------------------------
# The properties
# ---------------------------------------------------------------------------

def p_is_sorted(xs: List[int]) -> Optional[str]:
    out = xs  # placeholder; rebound below
    return None


def make_sorted_property(fn: Callable[[List[int]], List[int]]):
    """WEAK SPEC: 'the output is sorted'. One clause only."""
    def prop(xs: List[int]) -> Optional[str]:
        out = fn(xs)
        for a, b in zip(out, out[1:]):
            if a > b:
                return f"output not sorted: {out}"
        return None
    return prop


def make_strong_property(fn: Callable[[List[int]], List[int]]):
    """STRONG SPEC: sorted AND a permutation of the input. Two clauses."""
    def prop(xs: List[int]) -> Optional[str]:
        out = fn(xs)
        for a, b in zip(out, out[1:]):
            if a > b:
                return f"output not sorted: {out}"
        if Counter(out) != Counter(xs):
            return (f"output is not a permutation of the input: "
                    f"in={xs} out={out}")
        return None
    return prop


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def report(name: str, fn: Callable[[List[int]], List[int]],
           prop_factory) -> None:
    prop = prop_factory(fn)
    ok, counterexample, msg = for_all_lists(prop)
    status = "PASS" if ok else "FAIL"
    print(f"  {name:<26} {status}")
    if not ok:
        print(f"      counterexample (shrunk): {counterexample}")
        print(f"      {msg}")


def main() -> None:
    print("=" * 78)
    print("PROPERTY-BASED TESTING AND THE SPECIFICATION GAP")
    print("=" * 78)

    print("\nWEAK SPEC: 'the output is sorted'")
    print("-" * 78)
    report("real_sort", real_sort, make_sorted_property)
    report("bad_sort  (returns [])", bad_sort, make_sorted_property)

    print("\n  >>> bad_sort PASSES. The weak property is satisfied by a program")
    print("  >>> that throws away every input. This is the specification gap:")
    print("  >>> the proof/test is only as good as the sentence you wrote down.")

    print("\nSTRONG SPEC: 'output is sorted AND a permutation of the input'")
    print("-" * 78)
    report("real_sort", real_sort, make_strong_property)
    report("bad_sort  (returns [])", bad_sort, make_strong_property)

    print("\n  >>> Now bad_sort FAILS, and the harness SHRANK the failure to a")
    print("  >>> minimal reproducer. That shrinking is the model-checker")
    print("  >>> counterexample-trace idea, at unit-test scale.")

    print("\n" + "=" * 78)
    print("THE THREE TAKEAWAYS")
    print("=" * 78)
    print("""
  1. Write TWO properties, not one:
       - what must be TRUE of the result   (sorted)
       - what must be PRESERVED            (permutation, no data loss,
                                            idempotency, ordering, no leak)
     The second clause is the one people forget, and it is where the bugs are.

  2. Property-based testing gets you most of the benefit at a fraction of the
     cost of a proof. It is rung 2 of the ladder. Do this first.

  3. Sampled != proved. A passing property test is not a theorem. That is fine
     -- it is the 80/5 point. Climb higher (Kani, Dafny, TLA+) only for the
     small, stable, catastrophic-if-wrong core.

  The real libraries (Hypothesis, proptest, fast-check) do everything this toy
  harness does, plus better generation, shrinking, and integration with pytest
  / cargo test / jest.
""")


if __name__ == "__main__":
    main()
