---- MODULE RetryIdempotency ----
\*
\* A TLA+ specification of a "just retry it" design, written to demonstrate how
\* model checking finds a design bug that testing would essentially never hit.
\*
\* THE DESIGN (naive, and extremely common in production):
\*
\*   client:  send(req, id);  on timeout, resend(req, id)
\*   server:  on receive(req, id):
\*              if already seen then ack(id)
\*              else { apply(req); remember(id); ack(id) }
\*
\* The intent is at-most-once effects (no double refund, no double charge).
\*
\* THE BUG: "apply the effect" and "durably remember the id" happen at
\* different times. If the server crashes in between, the effect happened but
\* the memory of it did not. The client's retry then applies it a second time.
\*
\* This is a DESIGN bug, not a coding bug: the code faithfully implements a
\* broken design. That is exactly AWS's point -- "if the design is broken then
\* the code is almost certainly broken".
\*
\* RUNNING IT (TLC is not installed in this repo's environment):
\*   1. Install the TLA+ Toolbox, or the VS Code TLA+ extension.
\*   2. Create a new model. Set CONSTANT Id = {"r1"}  (then try {"r1","r2"}).
\*   3. Set INVARIANT to AtMostOnce.
\*   4. Run TLC. It reports a violation and prints the counterexample trace,
\*      whose shape is given at the bottom of this file.
\*
\* Then apply the fix described at the bottom and watch the violation vanish.
\*

EXTENDS Naturals, Sequences

CONSTANT Id

VARIABLES
    serverState,   \* "up" or "down"
    inflight,      \* ids the client has sent and not yet had acked
    applied,       \* SEQUENCE of ids whose effect has actually happened
    seen,          \* ids DURABLY recorded as done
    marked         \* ids applied in this session but NOT yet durable

vars == <<serverState, inflight, applied, seen, marked>>

-----------------------------------------------------------------------------
\* Type invariant -- always worth writing; it catches modelling mistakes.
-----------------------------------------------------------------------------
TypeOK ==
    /\ serverState \in {"up", "down"}
    /\ inflight \subseteq Id
    /\ seen \subseteq Id
    /\ marked \subseteq Id
    /\ applied \in Seq(Id)

-----------------------------------------------------------------------------
\* Initial state
-----------------------------------------------------------------------------
Init ==
    /\ serverState = "up"
    /\ inflight = {}
    /\ applied = <<>>
    /\ seen = {}
    /\ marked = {}

-----------------------------------------------------------------------------
\* Actions
-----------------------------------------------------------------------------

\* The client sends, or retries, a request.
Send(id) ==
    /\ id \in Id
    /\ inflight' = inflight \cup {id}
    /\ UNCHANGED <<serverState, applied, seen, marked>>

\* The server receives a request. If it already knows the id (durably OR in
\* this session's memory), it must not apply the effect again.
Receive(id) ==
    /\ serverState = "up"
    /\ id \in inflight
    /\ id \notin seen
    /\ id \notin marked
    /\ applied' = Append(applied, id)      \* THE EFFECT HAPPENS
    /\ marked' = marked \cup {id}          \* ...remembered, but only in memory
    /\ UNCHANGED <<serverState, inflight, seen>>

\* The server acks. It may already know the id either durably or from memory.
Ack(id) ==
    /\ serverState = "up"
    /\ id \in inflight
    /\ id \in (seen \cup marked)
    /\ inflight' = inflight \ {id}
    /\ UNCHANGED <<serverState, applied, seen, marked>>

\* The in-memory marks are flushed to durable storage.
Flush ==
    /\ serverState = "up"
    /\ seen' = seen \cup marked
    /\ marked' = {}
    /\ UNCHANGED <<serverState, inflight, applied>>

\* *** THE BUG ***
\* A crash loses in-memory state. The effect already happened; the record of it
\* did not survive. `seen` (durable) is preserved, `marked` (memory) is not.
Crash ==
    /\ serverState = "up"
    /\ serverState' = "down"
    /\ marked' = {}
    /\ UNCHANGED <<inflight, applied, seen>>

Recover ==
    /\ serverState = "down"
    /\ serverState' = "up"
    /\ UNCHANGED <<inflight, applied, seen, marked>>

Next ==
    \/ \E id \in Id : Send(id)
    \/ \E id \in Id : Receive(id)
    \/ \E id \in Id : Ack(id)
    \/ Flush
    \/ Crash
    \/ Recover

-----------------------------------------------------------------------------
\* The properties we actually care about
-----------------------------------------------------------------------------

\* SAFETY: no id is ever applied twice. THIS IS THE ONE THAT FAILS.
AtMostOnce ==
    \A i, j \in DOMAIN applied :
        (i # j) => (applied[i] # applied[j])

\* SAFETY: the audit log only contains known ids (a sanity check on the model).
WellFormed ==
    applied \in Seq(Id)

\* LIVENESS (needs TLC's temporal-property checking plus a fairness spec):
\* every request is eventually acked. Note how much harder this is than safety.
EventualAck ==
    \A id \in Id : (id \in inflight) ~> (id \notin inflight)

=============================================================================
\* WHAT TLC WILL SHOW YOU  (with Id = {"r1"}, Invariant = AtMostOnce)
\*
\*   step 1  Send(r1)
\*              inflight = {r1}
\*
\*   step 2  Receive(r1)
\*              applied  = <<r1>>     <- the effect HAPPENED
\*              marked   = {r1}       <- remembered, in memory only
\*
\*   step 3  Crash
\*              serverState = "down"
\*              marked      = {}      <- the memory of it is LOST
\*              applied     = <<r1>>  <- but the effect is still real
\*
\*   step 4  Recover
\*              serverState = "up"
\*
\*   step 5  Receive(r1)            <- the client's retry
\*              r1 \in inflight, r1 \notin seen, r1 \notin marked
\*              applied = <<r1, r1>>  <- VIOLATION: applied twice
\*
\* AtMostOnce is violated at step 5.
\*
\* WHY THIS MATTERS
\*   No realistic test suite generates "crash precisely between the effect and
\*   the durable write, for this specific request id". Model checking does it
\*   by construction, in milliseconds. That is the entire value proposition of
\*   this technique in one spec -- and the bug is found BEFORE any code exists.
\*
\* THE FIX
\*   Constrain the ORDER: either
\*     (a) write the durable mark BEFORE performing the effect, and dedupe on
\*         it -- i.e. Receive requires `id \in seen` to have happened first; or
\*     (b) make the effect and the durable mark a single atomic action
\*         (no Crash step can interleave); or
\*     (c) make the effect itself idempotent and verify that separately.
\*   Re-run TLC after each and watch the counterexample disappear. Trying all
\*   three is a 10-minute exercise that teaches more than a week of reading.
\*
\* EXTENSIONS TO TRY
\*   - Add network duplication and reordering in Send.
\*   - Add a second client id to check for cross-client interference.
\*   - Bound the `seen` set to model dedup-state eviction (unbounded dedup
\*     state is a real operational failure: it is how you OOM).
\*   - Add timeout-and-resend logic and check eventual consistency.
=============================================================================
