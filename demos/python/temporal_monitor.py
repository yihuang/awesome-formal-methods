#!/usr/bin/env python3
"""
temporal_monitor.py — runtime verification of an AI agent's action trace.

This is the FM-for-AI pattern that a normal engineering team can adopt *today*,
with no PhD and no prover. It is also the pattern behind things like AgentSpec
(runtime enforcement for LLM agents) and AWS Bedrock's automated-reasoning
guardrail checks.

The idea, in one sentence:

    You cannot prove things about the model. You CAN state temporal properties
    about the model's ACTIONS, and check them at runtime -- soundly, over every
    trace, with a witness when they fail.

This is exactly what your service's liveness probes, circuit breakers and
assertions already do. The only change is that the properties live for a
*growing trace of decisions* rather than for a single call.

Key point demonstrated at the end: a "probabilistic guardrail" (keyword
matching, classifier, LLM-as-judge) fails in *correlated* ways with the model it
guards. A structural monitor fails differently. In an AI-saturated pipeline, the
marginal checker must be ORTHOGONAL to the others -- which is the whole argument
for having a sound checker somewhere in the stack.

Zero dependencies.

Run:
    python3 temporal_monitor.py
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, List, Optional, Sequence


# ---------------------------------------------------------------------------
# The trace: what an agent actually did
# ---------------------------------------------------------------------------

@dataclass
class Event:
    step: int
    action: str                 # "read" | "refund" | "delete" | "transfer" | ...
    amount: float = 0.0
    authorized: bool = True
    audit: bool = False
    # A free-text field, as an LLM-generated plan step would have.
    detail: str = ""
    secret_in_output: bool = False


# ---------------------------------------------------------------------------
# Monitors: temporal properties compiled into trace checks
# ---------------------------------------------------------------------------
#
# Each property is written first as the temporal-logic formula it encodes,
# then as a function over a trace. In production you would generate these from
# a spec, or use a monitor-synthesis tool. Writing them by hand is fine, and it
# is the same mental motion as writing an assertion.

@dataclass
class Violation:
    property_name: str
    formula: str
    step: int
    witness: str


MUTATING_ACTIONS = {"delete", "transfer", "erase", "drop", "revoke"}


def check_no_unauthorized_action(trace: Sequence[Event]) -> List[Violation]:
    """SAFETY:  G( action ∈ MUTATING_ACTIONS -> authorized )

    "Nothing bad ever happens." A violation is witnessed by a finite prefix.

    SPECIFICATION-GAP NOTE, and this one bit me while writing this file: the
    first draft of this monitor listed only {"delete", "transfer"}, and so it
    missed the agent's unauthorized `erase` -- a synonym. Guardrails have
    specification bugs too, which is why the property has to be stated over a
    *category* (state-mutating actions) rather than an enumeration of words.
    """
    out = []
    for e in trace:
        if e.action in MUTATING_ACTIONS and not e.authorized:
            out.append(Violation(
                "no_unauthorized_action",
                "G(action ∈ MUTATING_ACTIONS → authorized)",
                e.step,
                f"step {e.step}: unauthorized {e.action!r} ({e.detail!r})",
            ))
    return out


def budget_invariant(budget: float) -> Callable[[Sequence[Event]], List[Violation]]:
    """SAFETY:  G( cumulative_spend ≤ budget )

    The classic invariant: a property of every reachable state, checked by
    folding over the trace.
    """
    def check(trace: Sequence[Event]) -> List[Violation]:
        out, spent = [], 0.0
        for e in trace:
            spent += e.amount
            if spent > budget:
                out.append(Violation(
                    "budget_invariant",
                    f"G(cumulative_spend ≤ {budget})",
                    e.step,
                    f"step {e.step}: spend reached {spent} after {e.action!r}",
                ))
                break
        return out
    return check


def refunds_are_audited(trace: Sequence[Event]) -> List[Violation]:
    """RESPONSE / LIVENESS:  G( refund → F(audit within 3 steps) )

    On a finite trace this is 'eventually within the horizon'. In an infinite
    trace you would need a fairness assumption -- which is exactly why liveness
    is harder than safety and why the distinction matters.
    """
    horizon = 3
    out = []
    for i, e in enumerate(trace):
        if e.action != "refund":
            continue
        window = trace[i + 1:i + 1 + horizon]
        if not any(w.audit for w in window):
            out.append(Violation(
                "refund_eventually_audited",
                "G(refund → F≤3(audit))",
                e.step,
                f"step {e.step}: refund of {e.amount} not audited within "
                f"{horizon} steps",
            ))
    return out


def no_secret_leakage(trace: Sequence[Event]) -> List[Violation]:
    """HYPERPROPERTY-ish:  G(¬secret_in_output)

    Strictly, real non-interference is a property of *pairs* of traces. This is
    the single-trace approximation, which is what a runtime monitor can check.
    Information-flow properties are exactly where you need hyperproperties
    rather than trace properties.
    """
    out = []
    for e in trace:
        if e.secret_in_output:
            out.append(Violation(
                "no_secret_leakage",
                "G(¬secret_in_output)",
                e.step,
                f"step {e.step}: response contained secret material",
            ))
    return out


# ---------------------------------------------------------------------------
# A deliberately bad guardrail, for contrast
# ---------------------------------------------------------------------------

def keyword_guardrail(trace: Sequence[Event]) -> List[Violation]:
    """A 'probabilistic-style' guardrail: looks for the literal word 'delete'.

    This is a stand-in for a classifier or an LLM-as-judge: it is tuned on
    surface features and it fails in correlated ways with the thing it guards.
    """
    out = []
    for e in trace:
        if "delete" in e.action.lower() or "delete" in e.detail.lower():
            out.append(Violation(
                "keyword_guardrail",
                "-",
                e.step,
                f"step {e.step}: matched 'delete'",
            ))
    return out


# ---------------------------------------------------------------------------
# The traces
# ---------------------------------------------------------------------------

def good_trace() -> List[Event]:
    return [
        Event(1, "read", detail="list orders"),
        Event(2, "refund", amount=100.0, authorized=True, detail="refund order 7"),
        Event(3, "read", detail="confirmation"),
        Event(4, "audit", audit=True, detail="audit refund"),
        Event(5, "delete", authorized=True, detail="purge cache"),
    ]


def bad_trace() -> List[Event]:
    """A trace with three real violations, two of which a keyword guardrail misses.

    Note the obfuscation in step 3: the action is 'erase', not 'delete'. A
    surface guardrail sees nothing. A structural monitor checks the *decision*,
    not the wording.
    """
    return [
        Event(1, "read", detail="list orders"),
        Event(2, "refund", amount=900.0, authorized=True, detail="refund order 7"),
        Event(3, "erase", authorized=False, detail="clean up old records"),
        Event(4, "read", detail="done"),
        Event(5, "transfer", amount=5000.0, authorized=False, detail="settle"),
    ]


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

MONITORS = [
    ("no_unauthorized_action", check_no_unauthorized_action),
    ("budget_invariant(1000)", budget_invariant(1000.0)),
    ("refund_eventually_audited", refunds_are_audited),
    ("no_secret_leakage", no_secret_leakage),
]


def run(trace: List[Event], label: str) -> None:
    print(f"\n{label}")
    print("-" * 78)
    for e in trace:
        flag = "" if e.authorized else "  <-- UNAUTHORIZED"
        print(f"  step {e.step}: {e.action:<9} amount={e.amount:<7} "
              f"auth={e.authorized!s:<5}{flag} detail={e.detail!r}")

    violations: List[Violation] = []
    for _, monitor in MONITORS:
        violations.extend(monitor(trace))

    print()
    if not violations:
        print("  ✅ all temporal properties hold over this trace")
    else:
        print(f"  ❌ {len(violations)} violation(s):")
        for v in violations:
            print(f"     [{v.property_name}] {v.formula}")
            print(f"         witness: {v.witness}")

    kw = keyword_guardrail(trace)
    print(f"\n  keyword guardrail matched on {len(kw)} step(s) "
          f"(out of {len(violations)} real violations)")


def main() -> None:
    print("=" * 78)
    print("RUNTIME VERIFICATION OF AN AI AGENT'S ACTION TRACE")
    print("=" * 78)
    print("""
  Properties checked (temporal logic, compiled to trace monitors):

    SAFETY       G(action ∈ MUTATING_ACTIONS → authorized)
    INVARIANT    G(cumulative_spend ≤ budget)
    RESPONSE     G(refund → F≤3(audit))
    NO LEAK      G(¬secret_in_output)
""")

    run(good_trace(), "TRACE A — a well-behaved agent")
    run(bad_trace(), "TRACE B — an agent that goes wrong")

    print("\n" + "=" * 78)
    print("WHY THIS IS THE RIGHT PATTERN FOR AI SYSTEMS")
    print("=" * 78)
    print("""
  1. It requires NO guarantee about the model. You do not need the LLM to be
     correct, aligned, or even understood. You state what its ACTIONS must
     satisfy, and you check the actions. The guarantee is about the system's
     behaviour, independent of the policy's internals.

  2. The failure comes with a WITNESS. "Step 3: unauthorized erase" is a
     reproducible artifact you can put in a ticket. "The eval score dropped"
     is not.

  3. The monitor fails in an ORTHOGONAL way to a probabilistic guardrail.
     The keyword guardrail inspects WORDING: in trace A it fires on the
     harmless `delete` at step 5 (a cache purge) -- a FALSE ALARM -- and in
     trace B it is completely blind, because every violating action is
     described in euphemism ('erase', 'settle'). The structural monitor checks
     the DECISION and its authorization, not the vocabulary. Two checks that
     fail differently are worth more than three that fail the same way.

  4. BUT NOTE: my first draft of the safety property enumerated
     {"delete", "transfer"} and MISSED the unauthorized `erase`, because
     'erase' is a synonym. Guardrails have specification bugs too. State
     properties over CATEGORIES (state-mutating actions), never over word
     lists. This is the specification gap, in the guardrail itself, and it is
     why the property needs an owner and a review just like code.

  WHAT IT DOES NOT DO
     - It cannot tell you the action was WISE, only that it satisfied the
       properties you wrote. The specification gap is unchanged.
     - It is a runtime check: it observes and blocks.
     - Liveness on infinite traces needs fairness assumptions.
     - Real non-interference is a hyperproperty (a property of pairs of
       traces), not a trace property. Monitors approximate it.

  In production: put the monitor in the request path for irreversible actions,
  log every decision, and fail closed.
""")


if __name__ == "__main__":
    main()
