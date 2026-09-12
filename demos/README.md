# Demos

Runnable artifacts for the talk. Two of the three run **right now** with no dependencies; the
TLA+ ones are readable specs with instructions for running TLC.

| Demo | Runs here? | What it shows |
|---|---|---|
| [`lean/`](lean/) | ✅ `lake build` (Lean 4.32.0 is installed) | Curry–Howard, a real spec + proof, **the specification gap**, `#print axioms`, and a CI gate that catches `sorry` |
| [`python/dpll_sat.py`](python/dpll_sat.py) | ✅ `python3` | A SAT solver in ~90 lines: the engine under all automated verification. Includes the pigeonhole principle. |
| [`python/pbt_spec_gap.py`](python/pbt_spec_gap.py) | ✅ `python3` | Property-based testing with shrinking, and the weak-spec trap (sorted-but-empty) |
| [`python/temporal_monitor.py`](python/temporal_monitor.py) | ✅ `python3` | Runtime verification of an AI agent's action trace — the FM-for-AI pattern, plus a demonstration that structural monitors fail differently from surface guardrails |
| [`tla/RetryIdempotency.tla`](tla/RetryIdempotency.tla) | ❌ needs TLC | A design bug found by model checking: the crash-between-effect-and-durable-mark double-apply |
| [`tla/Mutex.tla`](tla/Mutex.tla) | ❌ needs TLC | The two-minute mutual-exclusion spec, with the counterexample you get by deleting one guard |

---

## Run everything that runs

```bash
# Lean (the good stuff)
cd demos/lean
lake build                 # compiles; prints the axiom dependencies of each proof

# The CI gate that makes proofs honest (exits 1 — it catches Planted.lean)
./scripts/check-no-sorry.sh

# Python (zero dependencies)
python3 demos/python/dpll_sat.py
python3 demos/python/pbt_spec_gap.py
python3 demos/python/temporal_monitor.py
```

---

## How to use these in the talk

| Talk segment | Demo | What to say |
|---|---|---|
| "A proof is a program" | `lean/Demo.lean` §0 | "`1 + 1 = 2` is a *type*. `rfl` is a term inhabiting it. Proving is programming." |
| "This is what a spec looks like" | `lean/Demo.lean` §1 | "One line of spec, `omega` discharges the obligation. This is the same pipeline as Dafny or F* — just smaller." |
| **"The specification gap"** | `lean/Demo.lean` §3 **or** `pbt_spec_gap.py` | "The proof was one line. The property was the hard part. And the property is *wrong*: this useless function passes it." |
| "The trusted base" | `lean/Demo.lean` §4 | "Notice that even a trivial arithmetic proof pulls in `propext`, `Classical.choice`, `Quot.sound`. Always know what your proof rests on." |
| "How you would lie" | `lean/scripts/check-no-sorry.sh` | "This compiles: `theorem t : 1 = 2 := by sorry`. So real proof engineering needs a CI gate. Here it is, and here's it failing." |
| "This is the engine" | `dpll_sat.py` | "SAT solves the pigeonhole problem and comes back with a model — which is a counterexample when you were trying to prove a property." |
| **"Runtime guardrails for agents"** | `temporal_monitor.py` | "You can't verify the model. You *can* verify its actions, soundly, with a witness. And note: a keyword guardrail produced a false alarm on the benign trace and was blind to the real violations." |
| **"The design bug"** | `tla/RetryIdempotency.tla` | "Five steps. A crash between the effect and the durable write. No test suite generates that. TLC finds it in milliseconds, before any code exists." |

---

## Demo hygiene

- **Pre-run the demo.** Live demos fail live.
- **Have a recording.** A GIF of `lake build` and the check script is enough.
- **Have the output pasted in a backup slide.** If the laptop misbehaves, you lose nothing.
- **The highest-impact demo is `pbt_spec_gap.py`**, because it takes 10 seconds, needs no
  toolchain, and lands the specification gap viscerally: *the useless function passes.*

---

## Environment reality (verified Sept 2026)

| Tool | Status |
|---|---|
| `lean` / `lake` 4.32.0 | ✅ installed |
| `elan` toolchain manager | ✅ installed |
| Python 3 | ✅ installed |
| `pip` / network | ❌ unavailable in this environment — hence the zero-dependency Python demos |
| TLA+ / TLC | ❌ not installed |
| Dafny, Z3, Rocq, Alloy, Kani | ❌ not installed |

Install instructions for the missing tools: [`../docs/05-tools/choosing.md`](../docs/05-tools/choosing.md#getting-started-install-reality-check)
