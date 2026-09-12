/-
# Planted.lean — a file that INTENTIONALLY lies

This file is NOT part of the Lake build (it is not under a declared `lean_lib`
target), so `lake build` will not compile it. It exists so you can watch the CI
check catch it:

    ./scripts/check-no-sorry.sh

It contains two of the classic ways a "machine-checked" claim can be worthless:

  1. `sorry` — a proof placeholder that compiles but proves nothing.
  2. `axiom` — an assumption smuggled in to make a theorem true.

Both are legitimate tools during development and both are catastrophic if they
reach a claim you're relying on. The point is not that they are evil; the point
is that they must be *visible*, and CI is how you make them visible.
-/

/-- A theorem that "proves" something false, by giving up. -/
theorem everything_is_easy : 1 = 2 := by sorry

/-- A theorem that "proves" something false, by assuming it. -/
axiom the_axiom_of_belief : 1 = 2

theorem also_easy : 1 = 2 := the_axiom_of_belief
