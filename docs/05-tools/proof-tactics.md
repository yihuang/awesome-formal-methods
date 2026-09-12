# Proof tactics

> **TL;DR.** A **tactic** is a program that transforms a proof state — a list of hypotheses and a
> goal — into a simpler state. Tactics are how proofs actually get written in Lean, Rocq, and
> Isabelle, and they are *untrusted*: they build a term, and [the kernel](../05-tools/lean4.md#the-kernel-and-the-trusted-base)
> checks that term. That separation is why a tactic can be arbitrary, buggy, AI-generated
> metaprogram code without endangering soundness. The practical skill is knowing which tier of
> automation to reach for, and knowing when to stop fighting the automation and write the term by
> hand.

---

## Theory

### 1. The proof state

Everything a tactic does is expressed against a **goal state**:

```
   m n : Nat          ← hypotheses (things you may assume)
   h : m = n          ←
   ⊢ m + 1 = n + 1     ← the goal (what you must produce)
```

A tactic is a function from a goal state to zero or more goal states:

```
   tactic : GoalState → List GoalState        -- [] means "proved"
```

`by` switches into tactic mode. The sequence of tactics is *elaborated* into a proof term, and the
kernel checks that term. **The tactic is not part of the proof** — it is a recipe for finding one.

**This is the key structural fact.** Anything may go wrong in the recipe: it may loop, be unsound as
a heuristic, or be written by a language model. The proof is still sound if the term type-checks.
See [Curry–Howard](../01-fundamentals/curry-howard.md#7-why-this-matters-for-engineering-not-just-logic).

### 2. Tactics are metaprograms, not logic

Because tactics are ordinary programs (in Lean, written in Lean), they can do anything: inspect the
goal, search the library, call external solvers, run an SMT engine, or invoke an LLM. Three
consequences:

| Consequence | Detail |
|---|---|
| **Automation can be arbitrarily clever** | `grind` is an SMT-inspired engine, `aesop` is a rule-based search, `omega` is a decision procedure — all just programs |
| **A failure is a program outcome** | "no progress", "timeout", or "synthesis failed", not a logical verdict |
| **Tactics can be tested** | you can unit-test a tactic, unlike a logical rule |

The last row matters for tooling: because tactics are programs, the usual software engineering
applies. And because they're untrusted, the usual *bugs* don't compromise correctness — they just
make proofs fail or run slowly.

### 3. Term mode vs tactic mode

Two ways to write the same proof:

```lean
-- term mode: write the program
theorem and_swap_term {p q : Prop} : p ∧ q → q ∧ p :=
  fun h => ⟨h.2, h.1⟩

-- tactic mode: give instructions
theorem and_swap_tactic {p q : Prop} : p ∧ q → q ∧ p := by
  intro h
  exact ⟨h.2, h.1⟩
```

| | Term mode | Tactic mode |
|---|---|---|
| Looks like | functional programming | imperative script |
| Readability | reveals the proof object | reveals the argument |
| Robustness to definition changes | usually better | often breaks |
| Automation | limited | full access |
| Reviewability in a library | highly valued (mathlib) | accepted, but `simp`-heavy proofs are questioned |

**Both compile to the same thing.** Good Lean style uses tactics for exploration and for goals where
automation shines, and term mode (or the final `exact`/`refine`) for the parts that should be stable.

### 4. Why automation tiers, and what each one actually is

The automation available to you forms a ladder, from "certain and trivial" to "powerful and
incomplete". Knowing the ladder is most of the skill:

| Tier | Tactic | What it really does | Fails when |
|---|---|---|---|
| 0 | `rfl` | definitional equality, by computation | the two sides aren't definitionally equal |
| 1 | `decide`, `native_decide` | evaluates a decidable proposition | the proposition isn't decidable; `native_decide` trusts the compiler |
| 2 | `simp` | oriented rewriting to a normal form | lemma set is wrong; can loop; can prove the wrong thing if over-broad |
| 3 | `norm_num`, `positivity` | numeric normalisation; sign/positivity reasoning | unusual numeric goals |
| 4 | `ring`, `field_simp` | polynomial (semi)ring normalisation | goals with division/side conditions |
| 5 | `linarith`, `nlinarith`, `omega` | linear/nonlinear arithmetic decision procedures | nonlinearity, quantifiers, non-arithmetic atoms |
| 6 | `gcongr`, `mono` | congruence in inequalities | shape mismatch |
| 7 | `aesop` | best-first search over `@[aesop]` rules | search explodes |
| 8 | `grind` | SMT-inspired: congruence closure, E-matching, arithmetic, case splitting | very high-dimensional goals |
| 9 | `exact?`, `apply?` | **library search** — propose a lemma | nothing in the library matches |
| 10 | manual | you | always, eventually |

**Design your proofs to stay low on the ladder.** A proof that uses `omega` will keep working; a
proof that depends on the exact behaviour of a large `simp` set will break on the next library
upgrade. This is a maintenance decision, not an aesthetic one.

### 5. The automation stopped. Now what?

The universal experience of using a proof assistant: automation closes 90% of goals and then refuses.
What to do, in order:

1. **`exact?`** — maybe the lemma already exists in the library. This should always be step one; it
   is astonishing how often the answer is "yes, and it's called something slightly different".
2. **Break the goal down.** `constructor`, `apply`, `cases`, `induction`. A goal that automation
   can't solve is usually a goal that should be several goals.
3. **Expose computation.** `simp?`, `unfold`, `rw` — often the goal is stuck for a definitional
   reason, and unfolding the right definition makes it `rfl`.
4. **Strengthen the induction hypothesis.** The most common *real* failure: the induction hypothesis
   is too weak because you generalised the wrong variable. Fix: `induction` with explicit
   generalisation, or prove an auxiliary lemma.
5. **Prove a helper lemma.** Local lemmas make the main proof trivial and the library better.
6. **Go to term mode.** Sometimes `by` is the wrong tool and `refine` with explicit holes is
   clearer.

**The single most common beginner mistake** is trying to make one giant tactic call work rather than
restructuring the goal. Tactics are not a solver; they are an interface to proof construction.

---

## Tutorial: one lemma, four ways

All code verified against Lean 4.32.0, no mathlib.

### Way 1 — term mode (the proof *is* the program)

```lean
theorem add_zero_term (n : Nat) : n + 0 = n := rfl
```

`rfl` succeeds because `n + 0` is *definitionally* `n`: `Nat.add` recurses on its second argument, so
`n + 0` reduces by computation. No reasoning happened. This is
[definitional equality](../01-fundamentals/type-theory.md#6-equality-the-single-most-consequential-design-choice)
doing the work, and understanding when it applies is the difference between a one-line proof and a
five-line one.

### Way 2 — tactics, minimally

```lean
theorem add_zero_tactic (n : Nat) : n + 0 = n := by simp
```

### Way 3 — automation

```lean
theorem add_comm_automation (m n : Nat) : m + n = n + m := by omega
```

`omega` is a decision procedure for Presburger arithmetic (linear integer arithmetic with
quantifiers over naturals/integers). It is *complete* for that fragment, which is why it is far more
reliable than `simp` for arithmetic goals.

### Way 4 — rewriting and calculation

```lean
example (m n : Nat) (h : m = n) : m + 1 = n + 1 := by
  rw [h]                       -- rewrite with a hypothesis

example (a b c : Nat) (h1 : a = b) (h2 : b = c) : a = c := by
  calc a = b := h1
    _   = c := h2              -- a chain of equalities
```

**Comparing the four:** way 1 is most robust and reveals that no reasoning was needed; way 3 is most
robust when reasoning *is* needed; way 2 is shortest but most fragile; way 4 documents the argument.

### Structuring a real proof

```lean
example {p q : Prop} (h : p ∧ q) : q ∧ p := by
  obtain ⟨hp, hq⟩ := h          -- destruct the hypothesis
  exact ⟨hq, hp⟩                -- anonymous constructor

example {p q : Prop} (h : p ∨ q) : q ∨ p := by
  cases h with                  -- case split, naming the cases
  | inl hp => exact Or.inr hp
  | inr hq => exact Or.inl hq

example (n : Nat) : n + 0 = n ∧ 0 + n = n := by
  constructor <;> simp          -- split into subgoals, solve both

example : ∃ n : Nat, n > 2 := ⟨3, by omega⟩     -- witness first, proof second
```

The four structural moves to internalise: **`obtain`** (destructure), **`cases`** (split on a
sumbool/disjunction), **`constructor`** (split a conjunction/goal into parts), **`⟨·,·⟩`** (provide
a witness or a pair), and **`<;>`** (apply a tactic to all resulting goals).

### Organising a long proof

```lean
example (a b : Nat) (h : a = b) : a * 2 = b * 2 := by
  have h2 : a * 2 = b * 2 := by rw [h]   -- intermediate fact, named
  exact h2

example (a b : Nat) (h : a = b) : a * 2 = b * 2 := by
  suffices a * 2 = b * 2 by exact this    -- prove a stronger/easier statement
  rw [h]
```

| Tactic | Use |
|---|---|
| `have h : T := by …` | introduce a lemma you'll reuse |
| `suffices T by …` | work backwards from a sufficient condition |
| `refine … ?_ …` | give the term, leaving named goals |
| `calc` | a chain of (in)equalities with a justification per step |
| `·` | focus on the next goal |
| `case name => …` | handle a specific case by name |
| `<;>`, `all_goals` | apply a tactic to every resulting goal |

`calc` is the construct that makes proofs readable to mathematicians, and it is worth preferring over
tactic soup when the argument is a chain of rewrites.

### Debugging: when a tactic does something inexplicable

```lean
set_option pp.all true in        -- show fully explicit terms (verbose, but explains elaboration)
example : 1 + 1 = 2 := rfl

example (n : Nat) : n + 0 = n := by
  trace_state                    -- print the goal state here
  rfl
```

| Technique | Purpose |
|---|---|
| `trace_state` | print the goal at this point in the script |
| `set_option pp.all true` | reveal implicit arguments and coercions — why elaboration failed |
| `set_option trace.Meta.synthInstance true` | why did typeclass resolution fail? |
| `guard_target = ...` | assert the goal is exactly what you think (a *test* inside a proof) |
| `sorry` | isolate: replace a subgoal with `sorry` to find which step is broken, then remove it |
| `set_option maxHeartbeats N` | raise the elaboration budget when automation times out |
| `#print axioms` | confirm nothing was smuggled in |

`guard_target` is underused and valuable: it turns "I hope the goal looks like this" into a checked
assertion, so your proof fails loudly at the right place when a definition changes.

---

## Reference

### Core tactics (Lean 4)

| Tactic | Effect |
|---|---|
| `intro h` | move `→`/`∀` in the goal into a hypothesis |
| `intros` | `intro` repeatedly |
| `exact e` | close the goal with the term `e` |
| `apply e` | unify the goal with `e`'s conclusion, leaving its premises as goals |
| `refine e ?_ ?_` | like `apply`, with explicit holes |
| `rw [h]` | rewrite the goal using `h` (left-to-right; `← h` reverses) |
| `simp` | simplify using `@[simp]` lemmas |
| `simpa` | `simp`, then `assumption` |
| `simp only [a, b]` | simplify using *exactly* these lemmas — preferred in libraries |
| `dsimp` | definitional simplification only |
| `cases h` | case split on an inductive hypothesis |
| `induction x` | induction, generating the recursor's cases |
| `constructor` | split a goal into its constructor's premises |
| `use w` | provide a witness for `∃` |
| `have h : T := by …` | introduce an intermediate fact |
| `suffices T by …` | reduce to a sufficient statement |
| `obtain ⟨x, hx⟩ := h` | destructure a hypothesis |
| `rcases h with ⟨x, hx⟩ \| hy` | richer destructuring |
| `subst h` | substitute an equality, eliminating a variable |
| `rfl` | close by definitional equality |
| `trivial` | close trivial goals (`True`, reflexivity, …) |
| `assumption` | close using a hypothesis |
| `contradiction` | close from contradictory hypotheses |
| `exfalso` | change the goal to `False` |
| `by_contra h` | proof by contradiction (classical) |
| `calc` | chain of (in)equalities with justifications |
| `omega` | decision procedure for linear integer/natural arithmetic |
| `decide` | decide a decidable proposition by kernel evaluation |
| `native_decide` | as `decide`, but compiled — **trusts the compiler** |
| `sorry` | placeholder; compiles, proves nothing — **ban it in CI** |

### The `simp` family, and how to use it without regret

`simp` is the most-used and most-misused tactic. Rules that make the difference:

| Do | Don't |
|---|---|
| Use `simp?` to discover the lemmas, then write `simp only [...]` | Leave bare `simp` in library code |
| Keep `simp` sets small and oriented | Add `@[simp]` lemmas that loop or that are not normal forms |
| Use `simp only` in proofs you want to survive upgrades | Rely on `simp`'s recursive set |
| Reach for a decision procedure for arithmetic | Ask `simp` to prove arithmetic |
| Check `simp` didn't over-simplify the *statement* | Assume a passing `simp` means correct |

**Why it matters:** a bare `simp` proof is a proof whose meaning depends on the current simp set. Widen
the library's `@[simp]` set and your proof may still compile but now prove a different (possibly
trivial) statement — or simply break. `simp only` is a *specification* of the rewrite steps you
intended.

### Cross-assistant comparison

| Concept | Lean 4 | Rocq/Coq | Isabelle/HOL |
|---|---|---|---|
| Enter tactic mode | `by` | `Proof.` | `proof - … qed` / `by` |
| Simplification | `simp`, `simp only` | `simpl`, `cbn` | `simp` |
| Arithmetic decision | `omega`, `linarith`, `ring` | `lia`, `lra`, `ring` | `linarith`, `algebra`, `presburger` |
| Search / hammer | `exact?`, `aesop`, `grind` | `auto`, `eauto`, `hint` | `auto`, `blast`, **Sledgehammer** |
| External solvers | via `grind`/`aesop` internals | via plugins | Sledgehammer → ATP/SMT, returns a proof |
| Metaprogramming | Lean (same language) | Ltac / Ltac2 / OCaml plugins | Isar + ML |
| Decide by evaluation | `decide`, `native_decide` | `vm_compute`, `native_compute` | `eval`, `code_simp` |

**Isabelle's Sledgehammer deserves the comparison point:** it exports the goal to external
first-order provers and SMT solvers, and returns a *reconstructed* proof checked by Isabelle — a
hammer with a safety net. Lean's `grind` takes the opposite design decision: an SMT-inspired engine
*inside* the assistant, with no translation round-trip. See the `grind` paper below.

### Best practices, in priority order

1. **Prefer the lowest automation tier that works.** `rfl` over `simp`; `omega` over `simp` for
   arithmetic.
2. **`simp only`, not `simp`**, in anything you expect to last.
3. **`#print axioms`** before you believe a proof.
4. **Ban `sorry`/`admit` in CI.** See
   [the gate](https://github.com/yihuang/awesome-formal-methods/blob/main/demos/lean/scripts/check-no-sorry.sh).
5. **Prove helper lemmas rather than writing long tactic scripts.** They get reused; scripts don't.
6. **Prefer generic lemmas** (over typeclasses) — they survive refactors.
7. **`guard_target` when you depend on the goal's exact shape.**
8. **Watch heartbeats in CI.** A proof that got 10× slower is a regression.
9. **Review proofs for what they *say*, not just that they compile.** A `simp` that closes a
   weakened goal is the [specification gap](../01-fundamentals/specifications.md#the-specification-gap-the-permanent-limitation)
   in miniature.
10. **Use `exact?` more than you think you should.** Search is cheaper than recall.

---

## References

- **Lean documentation.** *Tactics* — the definitive list.
  [Tactic reference](https://leanprover-community.github.io/mathlib4_docs/tactics.html) ·
  [Theorem Proving in Lean 4](https://lean-lang.org/theorem_proving_in_lean4/)
- **Yang, K. & Deng, J. et al.** *Lean by Example* and *Mathematics in Lean* — practice-oriented.
  [Mathematics in Lean](https://leanprover-community.github.io/mathlib4_docs/Mathlib.html) ·
  [Lean by Example](https://leanprover-community.github.io/learn.html)
- **Blaauwbroek, L. et al.** *TacticToe* / **Gauthier, T. et al.** *Tactician* — learning tactic
  sequences.
- **de Moura, L. & Ullrich, S.** *The Lean 4 Theorem Prover and Programming Language.* CADE 2021 —
  the metaprogramming design that makes tactics ordinary Lean programs.
  [PDF](https://leanprover.github.io/papers/lean4.pdf)
- **`grind`**: an SMT-inspired tactic for Lean 4. IJCAR 2026.
  [Springer](https://link.springer.com/content/pdf/10.1007/978-3-032-32589-1_7.pdf) —
  in-assistant automation rather than a translation round-trip.
- **`aesop`**: **Limperg, J. & From, L.** *Aesop: White-Box Best-First Proof Search for Lean.* CPP
  2023. [PDF](https://arxiv.org/abs/2205.03669)
- **`omega`**: **Krämer, M. et al.** — decision procedures for Presburger arithmetic in Lean.
- **`linarith`/`nlinarith`**: **From, L. et al.** *A Linear Arithmetic Procedure for Lean.*
- **Isabelle's Sledgehammer**: **Blanchette, J.C., Böhme, S., Paulson, L.** *Extending Sledgehammer
  with SMT Solvers.* CADE 2011.
- **Rocq tactics** — [rocq-prover.org](https://rocq-prover.org/) · *Software Foundations*
  [link](https://softwarefoundations.cis.upenn.edu/) — the standard introduction to tactic-style
  proving.
- **Wiedijk, F.** *The Seventeen Provers of the World.* Springer, 2006 — the same theorem proved in
  17 systems; the best way to feel the tactical differences.
- **Chlipala, A.** *Certified Programming with Dependent Types.* MIT Press, 2013.
  [Free online](http://adam.chlipala.net/cpdt/) — tactic-heavy proof engineering, and the de Bruijn
  criterion.
- **Lean FRO.** *Validating Proofs.*
  [link](https://lean-lang.org/doc/reference/latest/ValidatingProofs/) — how to check that a proof
  relies on nothing it shouldn't.
- **mathlib naming, style, and doc conventions** —
  [contribute](https://leanprover-community.github.io/contribute/index.html)
- **Zhang, Y. et al.** — *LeanDojo* and retrieval-augmented tactic prediction.
  [leandojo.org](https://leandojo.org/)

## Further reading

- [lean4.md](lean4.md) — the language, and why tactics are untrusted.
- [mathlib.md](mathlib.md) — the tactics and discovery tools the library ships with.
- [curry-howard.md](../01-fundamentals/curry-howard.md) — why proof checking is type checking, and
  therefore why tactics can't break soundness.
- [type-theory.md](../01-fundamentals/type-theory.md) — definitional equality, which is what `rfl`
  exploits.
- [llm-proof-engineering.md](../04-ai-era/llm-proof-engineering.md) — AI writing tactic scripts.
