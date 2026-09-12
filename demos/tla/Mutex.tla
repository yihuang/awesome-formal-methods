---- MODULE Mutex ----
\*
\* The smallest useful TLA+ spec: a two-process mutual-exclusion protocol.
\*
\* This is the "two minutes of writing" example from the talk. It exists to show
\* that a TLA+ spec is roughly the length of the pseudo-code you would have
\* written in your design doc anyway -- except this one is examinable.
\*
\* TLC checks MutualExclusion against EVERY possible interleaving of the two
\* processes. Delete the `owner = 0` guard in Acquire and TLC immediately hands
\* you the exact two-step trace that breaks it.
\*
\* RUNNING IT:
\*   Model: CONSTANT Proc = {"p1", "p2"}, Invariant = MutualExclusion
\*

EXTENDS Naturals

CONSTANT Proc

VARIABLES pc, owner

vars == <<pc, owner>>

TypeOK ==
    /\ pc \in [Proc -> {"idle", "critical"}]
    /\ owner \in Proc \cup {0}          \* 0 means "nobody holds the lock"

Init ==
    /\ pc = [i \in Proc |-> "idle"]
    /\ owner = 0

Acquire(i) ==
    /\ pc[i] = "idle"
    /\ owner = 0                        \* <-- THE GUARD. Remove it and see.
    /\ owner' = i
    /\ pc' = [pc EXCEPT ![i] = "critical"]

Release(i) ==
    /\ pc[i] = "critical"
    /\ owner' = 0
    /\ pc' = [pc EXCEPT ![i] = "idle"]

Next ==
    \/ \E i \in Proc : Acquire(i)
    \/ \E i \in Proc : Release(i)

\* SAFETY: never two processes in the critical section at once.
\* This is the property that makes the protocol correct, stated in one line.
MutualExclusion ==
    \A i, j \in Proc : (pc[i] = "critical" /\ pc[j] = "critical") => i = j

\* LIVENESS (needs fairness): a process that wants in eventually gets in.
\* Note that this is a *different kind* of property, and a harder one.
EventualEntry ==
    \A i \in Proc : (pc[i] = "idle") ~> (pc[i] = "critical")

=============================================================================
\* THE COUNTEREXAMPLE YOU GET WHEN YOU DELETE THE GUARD
\*
\*   1. Acquire(p1)   owner = p1, pc[p1] = "critical"
\*   2. Acquire(p2)   owner = p2, pc[p2] = "critical"   <- VIOLATION at step 2
\*
\* Two states. That is the whole bug.
\*
\* WHY THIS IS THE PITCH
\*   How long would it take you to be *sure* this lock is right by reading it?
\*   TLA+ took two minutes to write and is sure -- for every interleaving, not
\*   just the ones you thought of.
=============================================================================
