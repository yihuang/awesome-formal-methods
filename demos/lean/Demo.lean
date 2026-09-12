/-
# Formal Methods Demo — a runnable tour

Companion to the talk-prep wiki in this repo. Everything in this file is checked
by the Lean 4 kernel when you run `lake build`.

The five things it demonstrates, in order:

  0. Curry–Howard: a proof *is* a program, and checking a proof *is* type checking.
  1. A specification plus a proof, with the SMT-style `omega` tactic doing the work.
  2. Structural induction — how you prove things about recursive data.
  3. **The specification gap** — a useless implementation that satisfies a weak spec.
     This is the most important demo in the file.
  4. The trusted base: `#print axioms` shows exactly what a proof rests on.

Run it:
    lake build          # or:  lake env lean Demo.lean
-/

-- ---------------------------------------------------------------------------
-- 0. Curry–Howard: propositions are types, proofs are programs
-- ---------------------------------------------------------------------------
--
-- Read `A → A` as "A implies A" in logic, and as "a function from A to A" in
-- programming. They are the same thing. This is why proof assistants are
-- programming languages, and why "verified software" is even possible.

theorem identity {A : Prop} : A → A := fun h => h

/-- `1 + 1 = 2` is a *type*; `rfl` is a term inhabiting it. -/
theorem one_plus_one : 1 + 1 = 2 := rfl

/-- Conjunction is a pair type: to prove `A ∧ B`, provide both. -/
theorem and_intro {A B : Prop} (ha : A) (hb : B) : A ∧ B := ⟨ha, hb⟩

/-- Implication chains like functions, because they *are* functions. -/
theorem chain {A B C : Prop} (f : A → B) (g : B → C) : A → C := fun a => g (f a)

-- ---------------------------------------------------------------------------
-- 1. A specification and a proof
-- ---------------------------------------------------------------------------
--
-- The specification of `myMax` is the pair of theorems below: whatever else is
-- true, the result is ≥ each argument. That is a *complete* statement of what
-- this function must do. Everything not stated is unconstrained.

def myMax (a b : Nat) : Nat := if a ≤ b then b else a

/-- Spec: `myMax a b` is an upper bound of both inputs.
    This is universally quantified over ALL natural numbers — not sampled. -/
theorem myMax_ge_both (a b : Nat) : a ≤ myMax a b ∧ b ≤ myMax a b := by
  unfold myMax          -- expose the if-then-else
  split <;>             -- case-split on the condition, for both branches
  omega                 -- linear arithmetic; a decision procedure

-- Note what `omega` is doing: this is the same shape as a program verifier
-- (Dafny, Verus, F*) discharging a verification condition with an SMT solver.
-- The proof obligation is arithmetic; the machine does it.

-- ---------------------------------------------------------------------------
-- 2. Structural induction
-- ---------------------------------------------------------------------------
--
-- For recursive data, the induction principle comes free with the datatype.

theorem append_nil {α : Type} (xs : List α) : xs ++ [] = xs := by
  induction xs with
  | nil => rfl
  | cons x xs ih => simp

theorem length_append {α : Type} (xs ys : List α) :
    (xs ++ ys).length = xs.length + ys.length := by
  induction xs with
  | nil => simp
  | cons x xs ih => simp [ih]; omega

-- ---------------------------------------------------------------------------
-- 3. THE SPECIFICATION GAP  ← the important one
-- ---------------------------------------------------------------------------
--
-- A verification tool proves:   model  ⊢  property
--
-- It cannot prove:              property  =  what anyone wanted
--
-- Here is that gap, executable.

inductive Sorted : List Nat → Prop
  | nil : Sorted []
  | single (x : Nat) : Sorted [x]
  | cons {x y : Nat} {ys : List Nat} (h : x ≤ y) (t : Sorted (y :: ys)) :
      Sorted (x :: y :: ys)

/-- A deliberately useless "sorting" implementation: throw the data away. -/
def badSort (_ : List Nat) : List Nat := []

/-- The weak property: "the output is sorted".
    **This is trivially true of the useless implementation.**
    A weak spec is satisfied by a garbage program — and the proof is one line. -/
theorem badSort_satisfies_weak_spec (xs : List Nat) : Sorted (badSort xs) := Sorted.nil

-- The missing clause is the one everybody forgets: *the output is a permutation
-- of the input*. With only `Sorted`, `badSort` is "verified". This is the same
-- failure mode as a test suite that checks the happy path and passes on a
-- program that returns a constant.
--
-- Lessons:
--   * Writing the property is the hard part. The proof was one line.
--   * A proof is a contract between your MODEL and your PROPERTY. It tells you
--     nothing about either.
--   * The same trap exists in property-based testing: two properties, not one.
--     "is sorted" AND "is a permutation of the input".

-- ---------------------------------------------------------------------------
-- 4. The trusted base
-- ---------------------------------------------------------------------------
--
-- A verified claim rests on *something* you did not verify. Lean makes this
-- explicit. Run these and read the output — note that even a simple arithmetic
-- proof pulls in `propext`, `Classical.choice`, and `Quot.sound`.
--
-- This is the habit worth stealing: always be able to name your trusted base.

#print axioms myMax_ge_both
#print axioms append_nil
#print axioms length_append

-- ---------------------------------------------------------------------------
-- 5. How you would lie (and how CI catches it)
-- ---------------------------------------------------------------------------
--
-- Everything above is honest. Here is the dishonest version:
--
--     theorem everything_is_easy : 1 = 2 := by sorry
--
-- That COMPILES. `sorry` is a placeholder that proves nothing, and Lean will
-- happily report success. Real proof engineering therefore requires CI that
-- rejects it.
--
-- See `scripts/check-no-sorry.sh` (which scans for `sorry`, `admit`, and
-- unexpected `axiom` declarations) and `Planted.lean` (a file that
-- intentionally contains one, so you can watch the check fail).
--
-- This is also why independent judging tooling exists for AI-generated proofs:
-- proving a *lookalike* statement, or smuggling in an axiom, are the two ways a
-- machine-checked claim can be wrong. See Lean FRO's Comparator.
