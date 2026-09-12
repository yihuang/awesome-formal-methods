# Runnable demos

Every claim that could be executed, was. This page describes the four demo artifacts in the repo;
the code itself lives in [`demos/`](https://github.com/yihuang/awesome-formal-methods/tree/main/demos)
outside the docs tree, so links below point at GitHub.

| Demo | Runs with no setup? | What it demonstrates |
|---|---|---|
| [Lean 4 project](https://github.com/yihuang/awesome-formal-methods/tree/main/demos/lean) | ✅ `lake build` | Curry–Howard, a real spec + proof, **the specification gap**, `#print axioms`, and a CI gate that catches `sorry` |
| [`dpll_sat.py`](https://github.com/yihuang/awesome-formal-methods/blob/main/demos/python/dpll_sat.py) | ✅ `python3` | A SAT solver in ~90 lines — the engine under all automated verification |
| [`pbt_spec_gap.py`](https://github.com/yihuang/awesome-formal-methods/blob/main/demos/python/pbt_spec_gap.py) | ✅ `python3` | Property-based testing with shrinking, and the weak-spec trap |
| [`temporal_monitor.py`](https://github.com/yihuang/awesome-formal-methods/blob/main/demos/python/temporal_monitor.py) | ✅ `python3` | Runtime verification of an AI agent's action trace — the FM-for-AI pattern |
| [`RetryIdempotency.tla`](https://github.com/yihuang/awesome-formal-methods/blob/main/demos/tla/RetryIdempotency.tla) | ❌ needs TLC | A design bug found by model checking |
| [`Mutex.tla`](https://github.com/yihuang/awesome-formal-methods/blob/main/demos/tla/Mutex.tla) | ❌ needs TLC | The two-minute mutual-exclusion spec |

---

## Run everything that runs

```bash
# Lean 4 — the good stuff
git clone https://github.com/yihuang/awesome-formal-methods
cd awesome-formal-methods/demos/lean
lake build                      # compiles; prints the axiom dependencies of each proof
./scripts/check-no-sorry.sh     # exits 1 — it catches Planted.lean

# Python — zero dependencies, no install
cd ../..
python3 demos/python/dpll_sat.py
python3 demos/python/pbt_spec_gap.py
python3 demos/python/temporal_monitor.py
```

---

## 1. The specification gap, executable

This is the most important demo in the repo. It takes ten seconds and needs no toolchain.

```lean
-- A deliberately useless "sorting" implementation: throw the data away.
def badSort (_ : List Nat) : List Nat := []

-- The weak property: "the output is sorted".
theorem badSort_satisfies_weak_spec (xs : List Nat) : Sorted (badSort xs) := Sorted.nil
```

**The useless implementation passes.** The proof is one line. "The output is sorted" is trivially
true of the empty list. The missing clause is *"the output is a permutation of the input"* — and
the missing clause is where the bugs live.

Three lessons, all of which transfer directly to property-based testing:

1. Writing the property is the hard part; the proof was one line.
2. **A proof is a contract between your model and your property. It tells you nothing about
   either.**
3. Write *two* clauses: what must be **true** of the result, and what must be **preserved**.

The same trap in Python, with shrinking:

```
WEAK SPEC: 'the output is sorted'
  real_sort                  PASS
  bad_sort  (returns [])     PASS      <-- the useless one passes

STRONG SPEC: 'output is sorted AND a permutation of the input'
  real_sort                  PASS
  bad_sort  (returns [])     FAIL
      counterexample (shrunk): [0]
```

That shrinking is the model-checker counterexample-trace idea, at unit-test scale.

See [Specifications § the specification gap](01-fundamentals/specifications.md) and
[Limits](01-fundamentals/limits.md).

---

## 2. How you would lie — and the CI gate that catches it

```lean
theorem everything_is_easy : 1 = 2 := by sorry    -- COMPILES. Proves nothing.
axiom the_axiom_of_belief : 1 = 2                 -- an assumption smuggled in
```

So real proof engineering requires a CI gate. Here it is, and here is it failing:

```shellsession
$ ./scripts/check-no-sorry.sh
Scanning Lean sources under: .../demos/lean

❌ sorry: an unproved proof placeholder
     .../Planted.lean:21:theorem everything_is_easy : 1 = 2 := by sorry

❌ axiom: a smuggled assumption
     .../Planted.lean:24:axiom the_axiom_of_belief : 1 = 2
```

It passes clean on the honest file (comments are stripped first, so prose *about* `sorry` doesn't
trip it).

**Why this matters for AI-generated proofs.** The two ways a machine-checked claim can be
worthless are exactly these two. A third — **statement mismatch**, proving a lookalike theorem — is
what Lean FRO's [Comparator](https://github.com/leanprover/comparator) exists to catch, using an
independently written kernel as a second opinion.

> When the *prover* is untrusted, you must verify the **claim**, not just the proof.

That generalises far beyond mathematics. See [AI → FM § the tooling layer](04-ai-era/ai-for-fm.md).

---

## 3. The trusted base

```shellsession
$ lake build
info: Demo.lean:123:0: 'myMax_ge_both' depends on axioms: [propext, Classical.choice, Quot.sound]
info: Demo.lean:124:0: 'append_nil'    depends on axioms: [propext]
info: Demo.lean:125:0: 'length_append' depends on axioms: [propext, Quot.sound]
```

Even a trivial arithmetic proof rests on something. `#print axioms` makes the trusted base
explicit. **This is the habit worth stealing** from proof engineering: always be able to name what
your claim depends on. See [Limits § the trusted base](01-fundamentals/limits.md#the-trusted-base).

---

## 4. The engine: a SAT solver in 90 lines

`dpll_sat.py` implements DPLL with unit propagation and pure-literal elimination — the skeleton
that modern CDCL solvers still use.

```
[1] A satisfiable scheduling problem (3 jobs, 3 slots, job0 < job2)
    clauses: 18
    SAT    model: x1=T, x2=F, x3=F, x4=F, x5=T, ...
           decoding: slot0->job[0], slot1->job[1], slot2->job[2]

[2] The pigeonhole principle (unsatisfiable, and it gets hard fast)
    3 pigeons / 2 holes :   9 clauses -> UNSAT
    4 pigeons / 3 holes :  22 clauses -> UNSAT
    5 pigeons / 4 holes :  45 clauses -> UNSAT
```

Two things to notice:

- When the formula is SAT, the model **is a counterexample** if you were trying to prove a
  property. That is the killer feature of SAT/SMT-based verification: failure comes with a witness,
  not a shrug.
- `UNSAT` is a *proof* that no satisfying assignment exists. Modern solvers emit machine-checkable
  UNSAT proofs (DRAT/LRAT) so a tiny independent checker can validate them — you needn't trust the
  solver's code either.

See [Automated reasoning](01-fundamentals/automated-reasoning.md).

---

## 5. Runtime verification of an agent trace

`temporal_monitor.py` is the FM-for-AI pattern a normal team can adopt *today*, with no prover:

```python
MUTATING_ACTIONS = {"delete", "transfer", "erase", "drop", "revoke"}

def check_no_unauthorized_action(trace):
    """SAFETY:  G( action ∈ MUTATING_ACTIONS -> authorized )"""
```

Four properties over an agent's action trace — a safety property, an invariant, a response
property, and a no-leakage check:

```
TRACE B — an agent that goes wrong
  ❌ 4 violation(s):
     [no_unauthorized_action] G(action ∈ MUTATING_ACTIONS → authorized)
         witness: step 3: unauthorized 'erase' ('clean up old records')
     [budget_invariant] G(cumulative_spend ≤ 1000.0)
         witness: step 5: spend reached 5900.0 after 'transfer'
     [refund_eventually_audited] G(refund → F≤3(audit))
         witness: step 2: refund of 900.0 not audited within 3 steps

  keyword guardrail matched on 0 step(s) (out of 4 real violations)
```

**The point.** You cannot prove things about the model. You *can* state temporal properties about
its actions and check them soundly, with a witness. And note the contrast at the bottom: a
surface-level keyword guardrail produced a **false alarm** on the benign trace and was **completely
blind** on the real one. Two checks that fail differently are worth more than three that fail the
same way.

**And a bug I kept on purpose.** My first draft of that safety property enumerated
`{"delete", "transfer"}` and **missed the unauthorized `erase`** — a synonym. Guardrails have
specification bugs too: state properties over **categories**, never over word lists. That's the
specification gap, in the guardrail itself.

See [FM → AI](04-ai-era/fm-for-ai.md).

---

## 6. The design bug TLC finds in milliseconds

`RetryIdempotency.tla` models a naive but extremely common retry design, and TLC produces this:

```
step 1  Send(r1)
            inflight = {r1}

step 2  Receive(r1)
            applied  = <<r1>>     <- the effect HAPPENED
            marked   = {r1}       <- remembered, in memory only

step 3  Crash
            marked      = {}      <- the memory of it is LOST
            applied     = <<r1>>  <- but the effect is still real

step 4  Recover

step 5  Receive(r1)               <- the client's retry
            applied = <<r1, r1>>  <- VIOLATION: applied twice
```

This is a **design** bug, not a coding bug — the code faithfully implements a broken design. That
is precisely AWS's point: *"if the design is broken then the code is almost certainly broken."*

**No realistic test suite generates** "crash precisely between the effect and the durable write,
for this specific request id." Model checking does it by construction. And the bug is found
**before any code exists**.

The file includes three candidate fixes to try, each of which makes the counterexample vanish.
See [Distributed systems](03-applications/distributed-systems.md).

---

## If you demo these live

- **Pre-run the demo.** Live demos fail live.
- **Have a recording.** A GIF of `lake build` + the check script is enough.
- **Keep the output pasted somewhere.** If the laptop misbehaves, you lose nothing.
- **The highest-impact demo is the specification gap**, because it takes ten seconds, needs no
  toolchain, and lands viscerally: *the useless function passes.*

| Idea being shown | Demo | What to point out |
|---|---|---|
| "A proof is a program" | Lean §0 | "`1 + 1 = 2` is a *type*. `rfl` is a term inhabiting it." |
| "This is what a spec looks like" | Lean §1 | "One line of spec; `omega` discharges it. Same pipeline as Dafny, just smaller." |
| **"The specification gap"** | Lean §3 or `pbt_spec_gap.py` | "The proof was one line. The property was wrong." |
| "The trusted base" | Lean §4 | "Even this trivial proof rests on `propext`, `Classical.choice`, `Quot.sound`." |
| "How you would lie" | `check-no-sorry.sh` | "This compiles. So real proof engineering needs a gate." |
| "This is the engine" | `dpll_sat.py` | "UNSAT is a proof. SAT is a counterexample." |
| **"Guardrails for agents"** | `temporal_monitor.py` | "Verify the actions, not the model." |
| **"The design bug"** | `RetryIdempotency.tla` | "Five steps. No test suite generates that." |

---

## Environment reality (Sept 2026)

| Tool | Status |
|---|---|
| `lean` / `lake` 4.32.0 + `elan` | ✅ available — the Lean demo is genuinely executed |
| Python 3 | ✅ available — hence the zero-dependency Python demos |
| Node 22 + npm | ✅ available — the site builds locally |
| TLA+ / TLC | ❌ not installed — specs are hand-verified, output is reasoned-through |
| Dafny, Z3, Rocq, Alloy, Kani | ❌ not installed |

Install instructions for the missing tools: [Choosing a tool § getting started](./05-tools/choosing.md).
