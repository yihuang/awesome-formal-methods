#!/usr/bin/env python3
"""
dpll_sat.py — a tiny SAT solver in ~90 lines, and why it matters.

This is dependency-free and demonstrates the engine that sits underneath almost
all automated formal verification:

    SAT core  +  theory decision procedures  =  SMT solver
    SMT solver  +  a VC generator            =  Dafny / Verus / F* / Kani

The algorithm here is DPLL (Davis-Putnam-Logemann-Loveland, 1962) with unit
propagation and pure-literal elimination. It is the *skeleton* that modern
CDCL solvers (MiniSat, CaDiCaL, Kissat) still use — they add clause learning,
non-chronological backjumping, and watched literals, which is what made SAT
industrial.

Run:
    python3 dpll_sat.py
"""

from __future__ import annotations

from typing import Dict, List, Optional

Clause = List[int]                 # a disjunction of literals, e.g. [1, -2]
Formula = List[Clause]             # a conjunction of clauses (CNF)
Model = Dict[int, bool]            # variable -> value


# ---------------------------------------------------------------------------
# The solver
# ---------------------------------------------------------------------------

def simplify(formula: Formula, lit: int) -> Optional[Formula]:
    """Assign `lit := True`.

    Returns the simplified formula, or None if a clause became empty
    (i.e. a conflict was found). Note this is *resolution in action*: satisfied
    clauses are dropped, and the negation of the literal is removed.
    """
    out: Formula = []
    for clause in formula:
        if lit in clause:              # clause satisfied -> drop it
            continue
        reduced = [l for l in clause if l != -lit]   # remove falsified literal
        if not reduced:                # empty clause -> unsatisfiable branch
            return None
        out.append(reduced)
    return out


def unit_propagate(formula: Formula, model: Model) -> Optional[Formula]:
    """Repeatedly assign forced literals. This is where most of the speed is."""
    while True:
        units = [c[0] for c in formula if len(c) == 1]
        if not units:
            return formula
        for lit in units:
            model[abs(lit)] = lit > 0
            nxt = simplify(formula, lit)
            if nxt is None:
                return None
            formula = nxt


def pure_literals(formula: Formula, model: Model) -> Optional[Formula]:
    """Assign any variable that appears with only one polarity."""
    while True:
        polarities: Dict[int, set] = {}
        for clause in formula:
            for lit in clause:
                polarities.setdefault(abs(lit), set()).add(lit > 0)
        pure = [v for v, signs in polarities.items() if len(signs) == 1]
        if not pure:
            return formula
        for v in pure:
            positive = polarities[v].pop()
            model[v] = positive
            nxt = simplify(formula, v if positive else -v)
            if nxt is None:
                return None
            formula = nxt


def dpll(formula: Formula, model: Optional[Model] = None) -> Optional[Model]:
    """Return a satisfying assignment, or None if the formula is unsatisfiable."""
    if model is None:
        model = {}

    formula = unit_propagate(formula, model)
    if formula is None:
        return None
    formula = pure_literals(formula, model)
    if formula is None:
        return None
    if not formula:
        return model                          # all clauses satisfied

    # Branch on the smallest-index unassigned variable.
    var = min(abs(l) for clause in formula for l in clause)
    for value in (True, False):
        trial = dict(model)
        trial[var] = value
        nxt = simplify([c[:] for c in formula], var if value else -var)
        if nxt is None:
            continue
        result = dpll(nxt, trial)
        if result is not None:
            return result
    return None                               # both branches failed


# ---------------------------------------------------------------------------
# Demonstrations
# ---------------------------------------------------------------------------

def pigeonhole(holes: int) -> Formula:
    """`holes + 1` pigeons into `holes` holes. Unsatisfiable — a classic hard case.

    Variable numbering: x[p][h] = p * holes + h + 1
    """
    pigeons = holes + 1

    def x(p: int, h: int) -> int:
        return p * holes + h + 1

    clauses: Formula = []
    # Every pigeon is in at least one hole.
    for p in range(pigeons):
        clauses.append([x(p, h) for h in range(holes)])
    # No two pigeons share a hole.
    for h in range(holes):
        for p1 in range(pigeons):
            for p2 in range(p1 + 1, pigeons):
                clauses.append([-x(p1, h), -x(p2, h)])
    return clauses


def scheduling_problem() -> Formula:
    """A satisfiable toy: 3 jobs into 3 time slots, at most one per slot,
    and job 0 must run before job 2.

    Variables: j(i, s) = i * 3 + s + 1  (job i occupies slot s)

    (Note: with only 2 slots this would be unsatisfiable by the pigeonhole
    principle, since at-most-one-per-slot plus 3 jobs cannot fit. That is a
    nice illustration of how a small modelling choice flips SAT to UNSAT --
    and it is exactly the kind of thing TLA+/Alloy are used to catch.)
    """
    def j(i: int, s: int) -> int:
        return i * 3 + s + 1

    clauses: Formula = []
    for i in range(3):                                    # each job scheduled
        clauses.append([j(i, s) for s in range(3)])
    for s in range(3):                                    # at most one job/slot
        for a in range(3):
            for b in range(a + 1, 3):
                clauses.append([-j(a, s), -j(b, s)])
    for s0 in range(3):                                   # job 0 strictly
        for s2 in range(3):                               # before job 2
            if s0 >= s2:
                clauses.append([-j(0, s0), -j(2, s2)])
    return clauses


def render(model: Model, keys: List[int]) -> str:
    return ", ".join(f"x{k}={'T' if model[k] else 'F'}" for k in sorted(keys))


def main() -> None:
    print("=" * 72)
    print("SAT SOLVING — the engine under formal verification")
    print("=" * 72)

    print("\n[1] A satisfiable scheduling problem (3 jobs, 3 slots, job0 < job2)")
    f = scheduling_problem()
    print(f"    clauses: {len(f)}")
    m = dpll(f)
    if m is None:
        print("    UNSAT  (unexpected)")
    else:
        print(f"    SAT    model: {render(m, list(m))}")
        slots = {s: [i for i in range(3) if m.get(i * 3 + s + 1)] for s in range(3)}
        print(f"           decoding: slot0->job{slots[0]}, slot1->job{slots[1]}, "
              f"slot2->job{slots[2]}")
        print("    Note: a model is a *counterexample* when you were trying to")
        print("    prove a property. That is the killer feature of SAT/SMT-based")
        print("    verification: failure comes with a witness, not a shrug.")

    print("\n[2] The pigeonhole principle (unsatisfiable, and it gets hard fast)")
    for holes in (2, 3, 4):
        f = pigeonhole(holes)
        m = dpll(f)
        verdict = "SAT (bug!)" if m is not None else "UNSAT"
        print(f"    {holes + 1} pigeons / {holes} holes : {len(f):3d} clauses -> {verdict}")
    print("    'UNSAT' here is a *proof* that no schedule exists.")
    print("    This is the shape of every 'prove this cannot happen' result.")

    print("\n[3] Why this matters for verification")
    print("    A Hoare triple's verification conditions compile to exactly this.")
    print("    Modern CDCL solvers (MiniSat, CaDiCaL, Kissat) add clause learning +")
    print("    watched literals, handling millions of clauses. Add decision")
    print("    procedures for arithmetic/bit-vectors/arrays and you get SMT (Z3, cvc5),")
    print("    which is the backend of Dafny, Verus, F*, Why3, CBMC and Kani.")
    print("\n    For high assurance, solvers can emit machine-checkable UNSAT proofs")
    print("    (DRAT/LRAT) validated by a tiny independent checker — so you don't")
    print("    have to trust the solver's code either.")
    print()


if __name__ == "__main__":
    main()
