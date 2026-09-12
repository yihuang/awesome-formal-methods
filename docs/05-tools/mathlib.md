# Mathlib

> **TL;DR.** Mathlib is the unified library of mathematics for Lean 4: a single repository holding
> essentially all formalised undergraduate-and-beyond mathematics, organised by strict naming and
> style conventions so that tens of thousands of definitions from hundreds of contributors compose
> without collision. Its value to a newcomer is not the theorems — it is the **discovery
> infrastructure**: `exact?`, `apply?`, `simp?`, Loogle, and `#loogle`, which turn "is this already
> proved?" from a search problem into a command. If you write Lean without learning those tools you
> will re-prove things that were proved a decade ago.

---

## What it is, and how big

| Metric | Figure |
|---|---|
| **Definitions** | ~136,932 |
| **Theorems** | ~288,041 |
| **Contributors** | 772 |
| **Repository** | [github.com/leanprover-community/mathlib4](https://github.com/leanprover-community/mathlib4) |
| **Stats (live)** | [mathlib_stats.html](https://leanprover-community.github.io/mathlib_stats.html) |

*(Figures from the official statistics page, September 2026. The page is updated continuously — quote
it with a date.)*

Three structural facts about mathlib that shape how you use it:

1. **It is one library, not a package ecosystem.** There is no versioning of individual areas and no
   "install just the group theory". You depend on mathlib and get all of it. That is a deliberate
   trade: uniform conventions and no dependency hell, in exchange for a large, slow build.
2. **It tracks recent Lean.** Mathlib moves with Lean, so upgrading Lean breaks proofs and the
   library repairs them continuously. Budget for this if you pin mathlib.
3. **Almost every file is built from source unless you fetch the cache.** `lake exe cache get` is
   therefore the single most important command in the workflow — building mathlib from scratch takes
   hours.

## History

| Period | What happened |
|---|---|
| 2017–2021 | **mathlib3** grows on Lean 3 into the first large-scale formalised mathematics library |
| 2021 | Lean 4 released; the port begins |
| 2021–2023 | **mathlib4** developed alongside Lean 3's mathlib, with automated translation plus heavy manual repair |
| 2023 | mathlib4 becomes the main line; mathlib3 is frozen |
| 2023– | Lean FRO founded; the library and toolchain get dedicated engineering |

The port is worth knowing about because it is the field's biggest natural experiment in **proof
brittleness**: a language change invalidated a very large body of proofs at once. The lesson for
anyone planning a verification effort: proofs are code with no specification of their own, and they
*do* rot ([limits.md](../01-fundamentals/limits.md#proof-cost-and-brittleness)).

---

## Conventions: why they matter more than they look

Mathlib's conventions are not style pedantry. They are what makes a 288,000-theorem library
*navigable*, because the name of a theorem is how you find it.

### Naming

| Rule | Convention | Example |
|---|---|---|
| 1 | **Proofs and theorem names** (terms of `Prop`) | `snake_case` — `add_comm`, `le_of_lt` |
| 2 | **`Prop`s and `Type`s** (inductive types, structures, classes) | `UpperCamelCase` — `MonoidHom`, `IsField` |
| 3 | **Functions** are named after their **return value** | `A → B → C` is named as a term of `C` |
| 4 | Everything else (terms of `Type`s) | `lowerCamelCase` — `toFun`, `map_one'` |
| 5 | An `UpperCamelCase` name inside a `snake_case` name | referenced in `lowerCamelCase` — `MonoidHom.toOneHom_injective` |
| 6 | Acronyms are cased as a group | `LE`, but `NeZero` |
| 7 | The same rules apply to **structure fields and constructors** | `toFun`, `coe_one` |

Files are `UpperCamelCase.lean`. Declaration names use **American** spelling (`factorization`,
`Localization`, `FiberBundle`).

**Prop-valued classes are named `Is…`** when the name is a noun or noun phrase: `IsField`, `IsPrime`.
This is why you write `[IsField R]` in a hypothesis list and it reads like mathematics.

### Symbol → word dictionary

When a theorem statement is translated into a name, this is the mapping:

| Symbol | Name | Symbol | Name |
|---|---|---|---|
| `∨` | `or` | `∈` | `mem` |
| `∧` | `and` | `∉` | `notMem` |
| `→` | `of` / `imp` (conclusion **first**) | `∪` | `union` |
| `↔` | `iff` | `∩` | `inter` |
| `¬` | `not` | `⋃` | `iUnion` / `biUnion` |
| `∃` | `exists` / `bex` | `∑` | `sum` |
| `∀` | `all` / `forall` / `ball` | `∏` | `prod` |
| `=` | `eq` (often omitted) | `≤` | `le` / `ge` |
| `≠` | `ne` | `<` | `lt` / `gt` |
| `∘` | `comp` | `⁻¹` | `inv` |

**The `→` rule is the one that surprises people:** the *conclusion* comes first, and hypotheses are
often omitted. So `le_of_lt` is the theorem "from `a < b`, conclude `a ≤ b`".

**And the `le`/`ge` rule:** mathlib uses `≤` and `<` almost exclusively rather than `≥` and `>`, so
`ge`/`gt` means "the arguments are swapped", not "the reverse relation". `lt_iff_le_not_ge` is
`a < b ↔ a ≤ b ∧ ¬b ≤ a`.

---

## Discovery: the tools that make mathlib usable

This is the part to learn first. Guessing theorem names is not a workflow.

| Tool | What it does |
|---|---|
| **`exact?`** | find a lemma that closes the goal, exactly |
| **`apply?`** | find a lemma that reduces the goal to subgoals |
| **`rw?`** | find a rewrite that makes progress |
| **`simp?`** | run `simp`, then report the *minimal* `simp only [...]` set — the standard way to write robust proofs |
| **`hint`** | suggest next tactics |
| **`#check`** | the type of a term |
| **`#loogle`** / **Loogle** | search by *type shape* — "find a lemma `?a * ?b = ?b * ?a`" — [loogle.lean-lang.org](https://loogle.lean-lang.org/) |
| **Moogle** | natural-language / semantic search over mathlib |
| **`#find`** | search the library by name pattern or type |
| **The docs** | [mathlib4_docs](https://leanprover-community.github.io/mathlib4_docs/) — every declaration, cross-linked |
| **`#lint`** | check your own file against mathlib's conventions |

**The `simp?` trick deserves emphasis.** Writing `by simp` in a mathlib PR is usually considered
brittle, because the simp set changes and your proof may break or, worse, silently start proving
something else. `simp?` reports the lemmas actually used, so you can write
`simp only [Nat.add_comm, List.length_append]` — stable, reviewable, and fast. **This is the single
highest-value habit to adopt from mathlib's culture.**

---

## Workflow

```bash
# add mathlib to a project
lake +leanprover-community/mathlib4:lean-toolchain new myproj mathlib
cd myproj
lake exe cache get     # ← ESSENTIAL: downloads prebuilt .olean files
lake build             # now only your own files compile
```

| Task | Where |
|---|---|
| Ask a question | [Lean Zulip](https://leanprover.zulipchat.com/) — the community lives here |
| Contribute | [contribution guide](https://leanprover-community.github.io/contribute/index.html) |
| See what's needed | the [1000+ theorems](https://leanprover-community.github.io/1000.html) and [undergraduate](https://leanprover-community.github.io/undergrad.html) lists |
| Follow conventions | [naming](https://leanprover-community.github.io/contribute/naming.html) · [style](https://leanprover-community.github.io/contribute/style.html) · [docs](https://leanprover-community.github.io/contribute/doc.html) |
| Review queue | the [queueboard](https://leanprover-community.github.io/queueboard/) |

Contribution reality: PRs are reviewed by humans in a single monolithic repository with CI that
builds the whole library. It is rigorous, and it is slow. Plan accordingly.

---

## What's covered, and what isn't

| Well covered | Thinner / missing |
|---|---|
| Algebra, order theory, group/ring/field theory | Large parts of modern research mathematics |
| Analysis, measure theory, topology | Some combinatorics and parts of number theory |
| Linear algebra, category theory | Numerical analysis, computational mathematics |
| Set theory, logic, basic number theory | Applied/engineering mathematics |
| Algebraic geometry (substantial and growing) | Anything requiring heavy computation |
| Probability, some PDE | Large parts of geometry |

*Treat this as orientation, not a survey — the boundary moves every month, and the authoritative
check is searching the library.*

**The honest framing:** mathlib is a *breadth* library of foundational mathematics. It is not a
library of everything a working engineer needs. For a verification project you will often bring your
own definitions and use mathlib for the algebra, order theory, and tactics.

---

## Mathlib as an AI substrate

Worth noting because it is now one of mathlib's most consequential roles: it is both the **training
corpus** and the **retrieval target** for AI proof search. AlphaProof was fine-tuned on ~300,000
state–tactic pairs extracted from mathlib and used it as the library the search had to navigate;
LeanDojo and ReProver are built around retrieval from it. When OpenAI published ten new results with
Lean certificates in 2026, the proofs were checked against mathlib. See
[llm-proof-engineering.md](../04-ai-era/llm-proof-engineering.md).

**The engineering implication:** if you want AI to be useful on *your* domain, the highest-leverage
investment is a well-named, well-documented library — because naming and documentation are how both
humans and models find things.

---

## Tutorial: use the library instead of re-proving it

*(Illustrative — these snippets require mathlib, which this repo's demos deliberately avoid so that
they build in seconds.)*

### Step 1 — Prove something, then find out it already exists

```lean
import Mathlib

-- You write this:
theorem my_lemma (a b : Nat) : a + b = b + a := Nat.add_comm a b

-- Then discover mathlib has it, and 400 related facts:
#check @Nat.add_comm
#check @add_comm          -- the generic version, for any AddCommMonoid
```

**Lesson:** prefer the *generic* lemma (`add_comm` over `Nat.add_comm`). Using the generic version
makes your proof apply in more settings and survives refactors.

### Step 2 — Ask the library instead of guessing

```lean
example (a b c : Nat) (h : a ≤ b) : a + c ≤ b + c := by
  exact?          -- proposes: Nat.add_le_add_right h c
```

`exact?` is a *search* over the library, and it is nearly always faster than remembering names.

### Step 3 — Make a `simp` proof stable

```lean
example (xs ys : List α) : (xs ++ ys).length = xs.length + ys.length := by
  simp?           -- reports the exact lemmas used
  -- then write it down:
  -- simp only [List.length_append]
```

### Step 4 — Use the coverage map to orient

```lean
import Mathlib

#check @Finset.sum_le_sum        -- order + sums
#check @Continuous.continuousAt  -- topology
#check @MeasureTheory.Measure    -- measure theory
#check @CategoryTheory.Functor   -- category theory

#loogle "List.length (_ ++ _)"
```

### Step 5 — Read a mathlib proof to learn the house style

The most efficient way to learn mathlib's idioms is to open a random theorem near what you're doing
and read it. Look for: generic lemmas over typeclasses, `simp only` over `simp`, `obtain` over
destructuring chains, and a docstring in the mathematical vernacular.

---

## Reference

### Commands and tactics that come with mathlib

| Category | Tactics |
|---|---|
| Simplification | `simp`, `simp?`, `simpa`, `dsimp`, `simp_all` |
| Arithmetic | `ring`, `ring_nf`, `linarith`, `nlinarith`, `omega`, `norm_num`, `positivity`, `field_simp` |
| Order / inequalities | `gcongr`, `mono`, `bound` |
| Casting | `norm_cast`, `push_cast`, `exact_mod_cast` |
| Case analysis / induction | `cases`, `induction`, `rcases`, `obtain`, `interval_cases` |
| Search | `exact?`, `apply?`, `rw?`, `simp?`, `hint` |
| General automation | `aesop`, `grind`, `decide`, `native_decide`, `trivial`, `tauto` |
| Set / finite set | `ext`, `funext`, `Finset` lemmas, `aesop` |
| Analysis | `fun_prop`, `continuity`, `measurability`, `positivity` |
| Metaprogramming | `macro`, `elab`, `syntax` (Lean, not mathlib) |

For the underlying craft — how to use these well — see [proof-tactics.md](proof-tactics.md).

### Finding things, ranked by speed

| Need | Use |
|---|---|
| "What's the type of X?" | `#check X` |
| "What closes this goal?" | `exact?` |
| "What rewrites this?" | `rw?` |
| "Which simp lemmas did that?" | `simp?` |
| "What's proved about this type?" | `#find` / the docs |
| "Is there a lemma of this *shape*?" | `#loogle` / [Loogle](https://loogle.lean-lang.org/) |
| "What's the natural-language answer?" | Moogle, or the docs' search |
| "What's still missing?" | the [1000 theorems](https://leanprover-community.github.io/1000.html) list |

---

## References

- **The mathlib Community.** *The Lean Mathematical Library.* CPP 2020.
  [PDF](https://arxiv.org/abs/1910.09336) — the design and organisation of mathlib.
- **mathlib4 repository** — [github.com/leanprover-community/mathlib4](https://github.com/leanprover-community/mathlib4)
- **Mathlib statistics** — [leanprover-community.github.io/mathlib_stats.html](https://leanprover-community.github.io/mathlib_stats.html)
  *(source of the 136,932 / 288,041 / 772 figures, Sept 2026)*
- **Mathlib naming conventions** —
  [leanprover-community.github.io/contribute/naming.html](https://leanprover-community.github.io/contribute/naming.html)
  *(source of the seven naming rules, the symbol dictionary, and the `Is…` convention)*
- **Mathlib documentation style** — [contribute/doc.html](https://leanprover-community.github.io/contribute/doc.html)
- **Mathlib code style** — [contribute/style.html](https://leanprover-community.github.io/contribute/style.html)
- **API documentation** — [mathlib4_docs](https://leanprover-community.github.io/mathlib4_docs/)
- **Loogle** — [loogle.lean-lang.org](https://loogle.lean-lang.org/) — type-shape search
- **Moogle** — semantic search over mathlib
- **The 1000+ theorems project** — [link](https://leanprover-community.github.io/1000.html) ·
  **Undergraduate maths** — [link](https://leanprover-community.github.io/undergrad.html)
- **Learning resources** — [leanprover-community.github.io/learn.html](https://leanprover-community.github.io/learn.html)
- **Mathematics in Lean** — [link](https://leanprover-community.github.io/mathlib4_docs/Mathlib.html) ·
  **Theorem Proving in Lean 4** — [link](https://lean-lang.org/theorem_proving_in_lean4/)
- **Lean Zulip** — [leanprover.zulipchat.com](https://leanprover.zulipchat.com/) — where mathlib is
  discussed and where questions get answered
- **Yang, K. et al.** *LeanDojo: Theorem Proving with Retrieval-Augmented Language Models.* NeurIPS
  2023. [arXiv:2306.15626](https://arxiv.org/abs/2306.15626) · [leandojo.org](https://leandojo.org/)
- **Hubert, T. et al.** *Olympiad-level formal mathematical reasoning with reinforcement learning.*
  *Nature*, 2025 — mathlib as RL training corpus.
  [Link](https://www.nature.com/articles/s41586-025-09833-y)
- **Alama, J. et al.** *Does GPT-4 pass the Turing test?* — not mathlib, but a useful reminder that
  benchmark claims need scrutiny. For proof benchmarks see [miniF2F](https://github.com/openai/miniF2F),
  [ProofNet](https://github.com/zhangir-azerbayev/proofnet), [PutnamBench](https://trishullab.github.io/PutnamBench/).

## Further reading

- [lean4.md](lean4.md) — the language and kernel mathlib is built on.
- [proof-tactics.md](proof-tactics.md) — the tactics mathlib exposes, and how to use them well.
- [type-theory.md](../01-fundamentals/type-theory.md) — why `instance` resolution is proof search.
- [llm-proof-engineering.md](../04-ai-era/llm-proof-engineering.md) — mathlib as AI substrate.
