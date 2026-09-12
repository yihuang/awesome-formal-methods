# Lean 4 demo

A runnable tour of formal verification in Lean 4, built for the talk. Everything here is checked by
the Lean kernel.

## Run it

```bash
cd demos/lean
lake build                      # compiles Demo.lean, prints axiom dependencies
lake env lean Demo.lean         # same, without the build system
./scripts/check-no-sorry.sh     # the CI gate — exits 1, because of Planted.lean
```

Requires Lean 4 (`lean-toolchain` pins `leanprover/lean4:v4.32.0`). Install via
[elan](https://github.com/leanprover/elan):

```bash
curl -sSf https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh | sh -s -- -y
```

This project has **no external dependencies** — no mathlib download, so it builds in seconds.

---

## Files

| File | Purpose | Built by `lake build`? |
|---|---|---|
| `Demo.lean` | The five-part pedagogical demo | ✅ yes |
| `Planted.lean` | A file that *intentionally* contains `sorry` and a smuggled `axiom`, so you can watch the CI gate catch it | ❌ no (not a declared target) |
| `scripts/check-no-sorry.sh` | CI gate: strips comments, then greps for `sorry`, `admit`, and `axiom` | — |
| `lakefile.toml`, `lean-toolchain` | Project config | — |

---

## What `Demo.lean` covers, in order

### §0 — Curry–Howard: a proof is a program

```lean
theorem identity {A : Prop} : A → A := fun h => h
theorem one_plus_one : 1 + 1 = 2 := rfl
```

`A → A` is a proposition *and* a function type. `1 + 1 = 2` is a *type*; `rfl` is a term
inhabiting it. This is why proof assistants are programming languages and why "verified software"
is possible at all.

### §1 — A specification and a proof

```lean
def myMax (a b : Nat) : Nat := if a ≤ b then b else a

theorem myMax_ge_both (a b : Nat) : a ≤ myMax a b ∧ b ≤ myMax a b := by
  unfold myMax
  split <;> omega
```

Two things to notice:

- The specification is the theorem statement. It is **universally quantified over all naturals**,
  not sampled.
- `omega` is a decision procedure doing the arithmetic. This is the same architecture as Dafny,
  Verus, F*, and Why3: generate a verification condition, hand it to a solver.

### §2 — Structural induction

```lean
theorem length_append {α : Type} (xs ys : List α) :
    (xs ++ ys).length = xs.length + ys.length := by
  induction xs with
  | nil => simp
  | cons x xs ih => simp [ih]; omega
```

The induction principle comes free with the datatype. `ih` is the induction hypothesis — the
"assume it holds for the tail" step you would write by hand.

### §3 — THE SPECIFICATION GAP ← the most important demo in the repo

```lean
def badSort (_ : List Nat) : List Nat := []       -- useless: throw the data away

theorem badSort_satisfies_weak_spec (xs : List Nat) : Sorted (badSort xs) := Sorted.nil
```

**The useless implementation passes.** "The output is sorted" is trivially true of the empty list.
The missing clause is *"the output is a permutation of the input"* — and the missing clause is
where the bugs live.

Three lessons, all of which transfer directly to property-based testing:

1. Writing the property is the hard part; the proof was one line.
2. **A proof is a contract between your model and your property. It tells you nothing about
   either.**
3. Write *two* clauses: what must be **true** of the result, and what must be **preserved**.

### §4 — The trusted base

```lean
#print axioms myMax_ge_both
-- 'myMax_ge_both' depends on axioms: [propext, Classical.choice, Quot.sound]
```

Even a trivial arithmetic proof rests on something. `#print axioms` makes the trusted base
explicit. **This is the habit worth stealing** from proof engineering: always be able to name what
your claim depends on.

### §5 — How you would lie

```lean
theorem everything_is_easy : 1 = 2 := by sorry    -- COMPILES. Proves nothing.
```

`sorry` is a placeholder that silences the checker. So is an added `axiom`. Both are legitimate
during development and both are catastrophic if they reach a claim you rely on.

Hence the CI gate:

```bash
$ ./scripts/check-no-sorry.sh
Scanning Lean sources under: /home/ubuntu/formal-methods-sharing/demos/lean

❌ sorry: an unproved proof placeholder
     .../Planted.lean:21:theorem everything_is_easy : 1 = 2 := by sorry

❌ axiom: a smuggled assumption
     .../Planted.lean:24:axiom the_axiom_of_belief : 1 = 2

Fix the above, or explicitly allow them in a documented allowlist
(and say why in the commit message — assumptions are load-bearing).
```

And it passes clean on the honest file:

```bash
$ ./scripts/check-no-sorry.sh /tmp/clean-check   # containing only Demo.lean
✅ No sorry / admit / axiom declarations found.
```

The script strips Lean comments (including nested block comments) first, so prose *about* `sorry`
doesn't trip the gate.

---

## Why this matters for AI-generated proofs

The two ways a machine-checked claim can still be worthless are exactly the two this gate catches:

1. **`sorry` / `admit`** — the "proof" is a placeholder.
2. **Axiom smuggling** — the "theorem" is assumed rather than derived.

There is a third, subtler failure: **statement mismatch** — proving a lookalike theorem instead of
the one that was requested. Catching that requires comparing the proved statement against the
*challenge* statement, which is exactly what Lean FRO's
[Comparator](https://github.com/leanprover/comparator) does (with an independent Rust kernel,
`nanoda`, as a second opinion).

**The generalisable lesson:** when the *prover* is untrusted, you must verify the **claim**, not
just the proof. Checking a proof term tells you "something follows from the axioms you supplied."
It does not tell you "the thing you wanted follows from the axioms you meant."

That is the [specification gap](../../docs/01-fundamentals/specifications.md) in a new costume — and
it's the best AI-era slide in the talk.

---

## Adapting this for a live demo

1. Start with `lake build`. Let them see the axiom output scroll past.
2. Open §3 and say: *"watch — this function throws away all the data, and the proof passes."*
3. Run `./scripts/check-no-sorry.sh` and let it fail. Then say: *"that's the CI gate nobody
   writes, and it's the difference between a proof and a claim."*

Total: about 90 seconds. Have a recording as backup.
