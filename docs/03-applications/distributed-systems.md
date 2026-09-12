# Distributed systems: the best ROI in the field

> **TL;DR.** If you take one application area away from this wiki, take this one. Distributed
> protocols are small, they fail in ways testing cannot sample, the bugs are design bugs, and the
> failure cost is enormous. This is where formal methods have the best cost/benefit ratio in
> existence — and it's the one an infrastructure team can adopt this quarter.

---

## Why this domain is special

### 1. The bugs are *design* bugs, and design bugs are cheap to fix

AWS's central observation:

> "If the design is broken then the code is almost certainly broken, as mistakes during coding are
> extremely unlikely to compensate for mistakes in design. Worse, engineers will probably be
> deceived into believing that the code is 'correct' because it appears to correctly implement the
> (broken) design."

In a well-factored distributed system, the *hard* part is a protocol of a few hundred lines. The
code around it is plumbing. So the verification target is naturally small, while the risk is
concentrated. That's the ideal shape.

### 2. Testing is structurally the wrong tool

Testing samples executions. The bug lives in a specific interleaving of:

| Failure axis | Combinatorial explosion |
|---|---|
| Messages | reordering, duplication, loss, delay |
| Processes | crash, restart, pause (GC), partition |
| Clocks | skew, drift, non-monotonicity |
| Partitions | arbitrary and dynamic |
| Operators | rolling restarts, config changes, capacity changes |
| Retries | duplicates, amplification, cascade |

The number of relevant interleavings is astronomical, and — critically — **the interesting ones
are not randomly distributed.** Bugs cluster at rare interleavings that random testing will
essentially never hit. This is exactly the shape of problem model checking was invented for.

### 3. Real money is attached

An S3 or DynamoDB consistency bug, a split-brain event, a silent data-loss event, a
double-spend. The cost of a design bug in a control plane is measured in trust and, occasionally,
in regulatory attention. Compare with the cost of a two-week TLA+ exercise.

### 4. The verification is *fun*, which matters for adoption

Engineers enjoy TLA+ because the feedback loop is a counterexample trace that shows a *real*
design flaw that nobody had thought of. It feels like a superpower, not a compliance chore. AWS's
framing — **"Debugging Designs"** — exploited exactly this.

---

## The catalogue of distributed-systems bugs you can actually catch

Every item here is expressible as a safety or liveness property, and every one has shipped in
production somewhere.

| Bug class | Property (informal) | Typical expression |
|---|---|---|
| **Lost update / write skew** | committed writes are all visible to later reads | `G(write(x) ⇒ F(read(x) ≥ v))` |
| **Duplicate delivery** | at-most-once effects | `G(effect applied ⇒ exactly one ack)` |
| **Split brain** | at most one leader per term | `G(leader₁ = leader₂ ≠ none ⇒ same term)` |
| **Stale read after ack** | read-your-writes | `G(ack(w) ⇒ all subsequent reads see w)` |
| **Deadlock** | progress | `G(enabled action ⇒ F(action taken))` |
| **Starvation / livelock** | fairness | `F(request served)` under weak fairness |
| **Non-monotonic reads** | session monotonicity | `G(read v₁ then read v₂ ⇒ v₂ ≥ v₁)` |
| **Unbounded retry amplification** | termination / no infinite retries | liveness + invariant on retry count |
| **Linearizability** | the history is equivalent to some sequential one | refinement to a sequential spec |
| **Reconfiguration safety** | membership changes preserve quorum intersection | invariant over configuration sets |

**The quorum-intersection invariant is the canonical example** — it's the thing that makes Raft and
Paxos correct, it's a one-line invariant, and it's *invisible* to testing.

---

## The three artefacts to produce

### 1. A TLA+ spec of the protocol (rung 5)

Write the protocol abstractly: states, message types, actions, environment failure actions.
Then state the invariants. TLC explores everything.

**Scope discipline:** spec the *consensus/quorum/ordering* logic, not the RPC layer. Abstract the
network to "messages may be lost and reordered" — that's a two-line nondeterministic `Send`.

### 2. A refinement relation to the implementation spec

Two specs: the abstract protocol (what it must do) and the concrete one (how it does it, with real
message types, timeouts, batching). Prove the concrete refines the abstract. This catches the class
of bug where the *optimisation* changed the protocol's guarantees — one of the most common
production failure patterns in systems that were "correct before we made it fast".

### 3. A counterexample trace in the bug tracker

When TLC finds a violation, you get a numbered sequence of states and actions. Paste it into the
design doc. **It's a reproducible bug for a system that doesn't exist yet.** That artifact changes
the culture of a design review more than any amount of advocacy.

---

## Worked example: why "just retry" needs a spec

Consider a trivially plausible design:

```
client:  send(request, id); wait; on timeout, resend(request, id)
server:  on receive(request, id): if seen(id) then ack(id) else { apply(request); mark(id); ack(id) }
```

Properties you would now want to check:

1. **At-most-once effect:** `G(apply(r, id) ⇒ never apply(r, id) again)` — needs `mark(id)` to
   happen *atomically with or before* the effect, and to survive a crash. Spec it, and TLC will
   immediately show you the counterexample where the server crashes after `apply` and before
   `mark`. **That bug is in the design, not the code**, and it's the kind of thing that takes a
   multi-day incident to discover in production.
2. **Eventual ack:** `G(send(id) ⇒ F(ack(id)))` under fairness + eventual network recovery.
3. **Bounded duplicates:** invariant on the size of the `seen` set (a real operational concern —
   unbounded dedup state is how you OOM).

**Two hours of TLA+ finds bug #1.** That is the entire pitch for this domain, and it fits on one
page. It also shows the pattern: the bug is a *crash between two adjacent statements*, found by
enumerating interleavings that no test would generate.

---

## Tools and when to use which

| Tool | Best for | Note |
|---|---|---|
| **TLA+ / TLC** | protocol design, quick counterexamples; the default choice | explicit-state; excellent IDE; huge library of published specs (Paxos, Raft, …) |
| **PlusCal** | engineers who prefer imperative pseudocode | compiles to TLA+; AWS's recommended entry point |
| **Apalache** | symbolic checking of TLA+ specs beyond TLC's reach | SMT-backed; same modelling assumptions as TLC |
| **Alloy** | structural/relational modelling with small scopes; found real bugs in Chord | bounded scope, very fast, great for data-model bugs |
| **SPIN / Promela** | concurrent algorithms, message-passing protocols | classic; strong for finding assertion violations |
| **Ivy / Verdi / IronFleet / Veil** | verified distributed *implementations* in Coq/Lean | research-grade but real; Veil found bugs in previously "verified" protocols |
| **P (Microsoft)** | event-driven systems, systematic testing + verification | used on Azure services |
| **Stateright** (Rust) | model checking Rust systems in Rust | good fit if your service is Rust |

**Complementary (not substitutes) — say this explicitly:**

| Practice | What it does | Relation to FM |
|---|---|---|
| **Jepsen** | black-box testing of a *running* system under partitions | finds real impl bugs FM can't see; FM finds bugs Jepsen's tests may never trigger |
| **Deterministic simulation testing** (FoundationDB, TigerBeetle, Antithesis) | run the whole system with a controlled scheduler and injected failures, reproducibly | empirical but *systematic*; the practical middle ground and a great stepping stone |
| **Property-based testing of the state machine** | same idea as FM but sampled | rung 2; do this if you can't do TLA+ |
| **Fuzzing / chaos engineering** | sample reality | necessary, not sufficient |

> **Honest framing:** TLA+ is "apples" and Jepsen is "oranges"; the right answer is
> both. Model checking catches design bugs before code exists; Jepsen catches implementation bugs
> the model abstracted away.

---

## Adoption advice specific to this domain

1. **Start from an incident.** A real consistency bug your team lost sleep over. AWS's own path.
2. **Spec the thing you're arguing about.** If two engineers disagree in the design doc, that
   disagreement is a spec-shaped hole. Formalize it. Either the model checks out (argument over)
   or it produces a counterexample (also argument over).
3. **Spec data models too.** AWS reported TLA+ being unexpectedly excellent for designing
   relational/NoSQL schemas. Cheap, high-value, underused.
4. **Budget two weeks for the first spec.** One champion, one protocol, one invariant. That's the
   proof of concept; expect it to be uncomfortable and slow.
5. **Make the counterexample the deliverable of the exercise**, even when the property holds —
   because when it doesn't, you've earned the next two quarters of budget.
6. **Re-run specs in CI.** A spec that isn't checked is documentation, and stale documentation is
   a liability.

---

**Sources:** [AWS TLA+ experience report](https://lamport.azurewebsites.net/tla/formal-methods-amazon.pdf);
[Veil / verifiedsoftware.dev](https://verifiedsoftware.dev/case-studies/); Lamport's TLA+ materials;
[apalache-mc.org](https://apalache-mc.org/).

Continue → [hardware-crypto.md](hardware-crypto.md), the domain where FM is *already* standard
practice.
