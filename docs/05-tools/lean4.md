# Lean 4

> **TL;DR.** Lean 4 is a **dependent type theory**, a **programming language**, and a **proof
> assistant** in one system — which means the same language expresses theorems, proofs, programs,
> tactics, and syntax extensions. Its distinguishing bet is that **metaprogramming is done in Lean
> itself**: there is no separate tactic language, so writing a tactic is ordinary programming. A
> small kernel (a type checker) sits under everything and is the only thing you must trust, which is
> why Lean can offer an extensible, programmable surface without giving up soundness.
>
> It is also, as of 2026, the proof assistant the AI-for-mathematics ecosystem standardised on —
> see [llm-proof-engineering.md](../04-ai-era/llm-proof-engineering.md).

---

## The stack

```
   ┌──────────────────────────────────────────────────────────────────────┐
   │  your source:  terms, proofs, tactics, macros, programs               │
   └───────────────────────────────┬──────────────────────────────────────┘
                                   │  parsing
   ┌───────────────────────────────▼──────────────────────────────────────┐
   │  Syntax  — fully user-extensible. `syntax`, `macro`, `elab`.           │
   │            You can add new kinds of *syntax*, not just notation.       │
   └───────────────────────────────┬──────────────────────────────────────┘
                                   │  macro expansion
   ┌───────────────────────────────▼──────────────────────────────────────┐
   │  Elaborator — resolves implicit arguments, inserts coercions,          │
   │               typeclasses, universe levels, metavariables;             │
   │               runs tactics to construct a term                         │
   └───────────────────────────────┬──────────────────────────────────────┘
                                   │  produces an Expr
   ┌───────────────────────────────▼──────────────────────────────────────┐
   │  KERNEL — type checking, definitional equality, inductive checking.    │
   │           Small. The only thing you must trust. NEVER extended                      │
   │           by user code.                                                │
   └───────────────────────────────┬──────────────────────────────────────┘
                                   │  IR → C → native
   ┌───────────────────────────────▼──────────────────────────────────────┐
   │  Compiler — Lean compiles to C, then native. Proofs are erased.        │
   └──────────────────────────────────────────────────────────────────────┘
```

**Everything above the kernel is untrusted, on purpose.** A bug in a tactic, a macro, the
elaborator, or the parser cannot make a false theorem true — the kernel would reject the resulting
term. That is the design that lets Lean be both *extensible* and *sound*.

## The kernel and the trusted base

The de Bruijn criterion, as Adam Chlipala phrases it:

> "Proof assistants satisfy the 'de Bruijn criterion' when they produce proof terms in small kernel
> languages, even when they use complicated and extensible procedures to seek out proofs in the
> first place. … To believe a proof, we can ignore the possibility of bugs during search and just
> rely on a (relatively small) proof-checking kernel that we apply to the result of the search."

Lean's kernel implements, in full:

| Component | What it is |
|---|---|
| Names | the addressing scheme |
| Universe levels | `Prop`, `Type u`, and level arithmetic |
| Expressions | lambdas, applications, constants, `forall`/`let`, literals |
| Declarations | axioms, definitions, theorems, inductive types, recursors |
| Environments | maps from names to declarations |
| Substitution | bound-variable and universe-parameter substitution |
| Type inference, reduction, definitional-equality checking | the core algorithms |
| Inductive checking | recursor generation; constructor/type agreement |
| Optional literal extensions | `Nat` and `String` literals |

Two consequences worth stating plainly:

1. **`#print axioms` is a complete audit.** Every theorem's dependencies are visible. If a proof used
   `Classical.choice` or a smuggled `axiom`, this shows it.
2. **Independent checkers exist.** Because the kernel is small, people re-implement it. Lean's
   **export format** lets an independent checker verify proofs — [Comparator](../04-ai-era/ai-for-fm.md#the-answer-independent-judging)
   uses `lean4export` plus **nanoda**, an independently written Rust kernel, precisely so that a
   claim doesn't rest on one implementation. Carneiro's assessment is fair: *"Writing your own type
   checker is not an afternoon project, but it is well within the realm of what is achievable for
   citizen scientists."*

**What is *not* in the trusted base:** tactics, `simp` lemmas, the elaborator, `decide`/`native_decide`
correctness (the latter trusts the compiler — see §Limits), macros, notation, the LSP, Lake, and
mathlib's proofs. Only the kernel, plus whatever axioms your proof invokes.

---

## Foundations, briefly

Lean's logic is a dependent type theory with inductive types, in the **Calculus of Inductive
Constructions** family. The four facts that matter in daily use:

| Fact | Consequence |
|---|---|
| Universes are stratified: `Prop`, `Type u`, `Sort u` | `Type : Type` is rejected — [Girard's paradox](../01-fundamentals/type-theory.md#5-universes-prop-type-sort--and-the-paradox-that-forced-them) |
| `Prop` is impredicative and proof-irrelevant | proofs are erased at runtime; logic is cheap |
| Definitional equality is intensional and decidable | type checking is decidable — the basis of cheap checking |
| Classical reasoning is an **axiom**, not derivable | `Classical.em`, `propext`, `Quot.sound`, `Classical.choice` show up in `#print axioms` |

That last row is not a technicality. It is the difference between a proof that computes a witness and
one that doesn't — see [curry-howard.md §5](../01-fundamentals/curry-howard.md#classical-logic-is-not-free).

---

## What makes Lean 4 different

Four design choices, each of which you feel within a day of using it.

### 1. Metaprogramming is in Lean

Lean 4's syntax is not fixed. `syntax`, `macro`, and `elab` let you extend the *grammar*, and the
implementation of tactics, notation, and whole domain-specific languages is ordinary Lean code. The
practical payoff: **tactics are programs, so they can be tested, debugged, and abstracted like
programs.** `simp`, `omega`, `ring`, and `grind` are all Lean programs.

### 2. One language for proofs and programs

The same file can contain a theorem and a fast executable function. `#eval` runs Lean code at compile
time; `@[extern]` and `@[implemented_by]` let you swap a proof-friendly definition for a fast
imperative one, keeping the specification while changing the implementation. That is how verified
crypto stays fast.

### 3. It is compiled, not interpreted

Lean compiles to C and then to native code. This is why Lean-written code can compete on
*performance*, not just correctness — the notable 2026 example being `lean-zip` running alongside
Rust implementations, and powdr's verified Lean optimiser being used in production via FFI
([blockchain.md](../03-applications/blockchain.md#the-integration-pattern-replace-modules-dont-rewrite)).

### 4. Lake and the LSP make it a normal development environment

`lake` is the build system and package manager; the language server gives completion, goal display,
error messages, and — now — an interface that AI agents drive over MCP. A tool you can't put in a
build is a tool nobody adopts; Lean is a tool you can put in a build.

---

## Tutorial

Everything below is verified against **Lean 4.32.0**, with **no mathlib dependency**, so it runs in
seconds. See [`demos/lean/`](https://github.com/yihuang/awesome-formal-methods/tree/main/demos/lean)
for the runnable project.

### Install

```bash
curl -sSf https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh | sh -s -- -y
# in a project directory:
lake new myproject && cd myproject && lake build
```

`elan` is the toolchain manager; `lean-toolchain` pins the version per project, so builds are
reproducible.

### The four commands you'll live in

```lean
#check Nat.add_comm          -- what is the type of this?
#eval 2 + 2                  -- run it (42? no: 4)
#print Nat.add_comm          -- its definition
#print axioms my_theorem     -- WHAT DOES THIS PROOF ASSUME?  ← the important one
```

`#print axioms` is the trusted-base audit. Make it part of your definition of done — it is how you
find out that a "constructive" proof is quietly classical, or that a `sorry` slipped in.

### A first proof, and what `rfl` means

```lean
theorem one_plus_one : 1 + 1 = 2 := rfl
```

`rfl` works because both sides are **definitionally equal** — the kernel computes them to the same
term. This is not a trivial point: it is [the definitional/propositional equality
distinction](../01-fundamentals/type-theory.md#6-equality-the-single-most-consequential-design-choice)
in action, and it is why Lean proofs are often shorter than you expect.

### Structures and typeclasses

```lean
structure Point where
  x : Nat
  y : Nat
  deriving Repr

class Describable (α : Type) where
  describe : α → String

instance : Describable Point where
  describe p := s!"({p.x}, {p.y})"

#eval Describable.describe (Point.mk 1 2)     -- "(1, 2)"
```

Note what happened: typeclass **resolution is proof search**. `instance` declarations form a
database that the elaborator searches, and the same machinery resolves both `Describable Point` and
mathematical structures in mathlib. It is also the same machinery that makes goals look insoluble
when two instances conflict.

### Write your own tactic — in Lean

```lean
import Lean

-- a tactic: no separate language, no plugin
macro "trivial_rfl" : tactic => `(tactic| rfl)
example : 1 = 1 := by trivial_rfl

-- a term notation
macro "double " n:term : term => `($n + $n)
#eval double 21                    -- 42

-- a custom *command*, using the elaborator API
open Lean Elab Command in
elab "#greet " name:ident : command =>
  logInfo m!"Hello, {name.getId}!"

#greet world                       -- Hello, world!
```

*(This is real output — verified.)* **A macro or elaborator cannot break soundness**: it produces a
term, and the kernel checks that term. So metaprogramming is a productivity tool, never a
soundness risk. That separation is the whole reason Lean can offer this.

### `do` is monad syntax, not an IO special case

```lean
def pairs : Option (Nat × Nat) := do
  let a ← some 1
  let b ← some 2
  return (a, b)

#eval pairs                        -- some (1, 2)
```

Useful to internalise: `do` desugars through `bind`, so it works for `IO`, `Option`, `Except`, and
any monad. This is [Curry–Howard's monad/logic row](../01-fundamentals/curry-howard.md#6-generalizations)
appearing as syntax.

---

## Reference

### Toolchain

| Tool | Role |
|---|---|
| **`elan`** | toolchain manager; reads `lean-toolchain` |
| **`lake`** | build system and package manager (`lake build`, `lake exe`, `lake test`) |
| **`lakefile.toml` / `.lean`** | project definition: libraries, executables, dependencies |
| **`lake-manifest.json`** | pinned dependency revisions — commit it |
| **`lake exe cache get`** | download prebuilt mathlib binaries (essential; mathlib takes hours to build) |
| **`lean-lsp-mcp`** | Lean over MCP for AI agents: goal states, diagnostics, search |
| **VS Code extension** | the standard editor experience |

### Essential commands

| Command | Purpose |
|---|---|
| `#check t` | the type of a term |
| `#eval e` | evaluate (runs the compiler) |
| `#reduce e` | reduce definitionally |
| `#print d` | print a declaration |
| `#print axioms t` | **the trusted base of a proof** |
| `#print sorryAx` | confirm whether you're relying on an unfinished proof |
| `set_option pp.all true` | show fully explicit terms — for debugging elaboration |
| `set_option maxHeartbeats N` | raise/lower the elaboration budget |
| `#lint` | mathlib linter; catches common proof smells |

### Attributes you'll meet

| Attribute | Effect |
|---|---|
| `@[simp]` | use this lemma in `simp`'s rewrite set |
| `@[ext]` | extensionality lemma |
| `@[norm_cast]` | push coercions in `simp` |
| `@[simp]` / `@[gcongr]` / `@[positivity]` | feed the corresponding automation |
| `@[reducible]`, `@[irreducible]` | control what unfolds definitionally — a **performance and ergonomics** lever |
| `@[inline]`, `@[specialize]`, `@[extern]` | runtime performance |
| `@[deprecated]` | deprecation with a migration hint |

### Version history

| Version | Year | Note |
|---|---|---|
| Lean 1–3 | 2013– | Lean 3 became the base for mathlib and a generation of work |
| **Lean 4** | 2021 | rewrite: extensible syntax, metaprogramming in Lean, compiled, no separate tactic language |
| **Lean FRO** | 2023 | dedicated non-profit engineering organisation; Lean's long-term home |
| Lean 4.32 | 2026 | the version used in this wiki's demos |

### Notable users and projects

| Project | What |
|---|---|
| **mathlib** | the library — see [mathlib.md](mathlib.md) |
| **AlphaProof** (DeepMind) | Lean as RL environment and reward; IMO silver, *Nature* 2025 |
| **Comparator** (Lean FRO) | independent judging: statement matching + second kernel |
| **EVMYulLean** (Nethermind) | the EVM and Yul semantics in Lean — [blockchain.md](../03-applications/blockchain.md) |
| **Verity**, **powdr** | verified smart contracts; verified zkVM optimiser used in production |
| **SymCrypt** (Microsoft) | verified cryptographic primitives for Windows and Azure |
| **SP1 Hypercube** (Succinct × Nethermind) | a full RISC-V zkVM core verified in Lean |
| **lean-zip** | a Lean implementation competitive with Rust on runtime |

### Limits and honest caveats

| Limit | Detail |
|---|---|
| **`native_decide` trusts the compiler** | it evaluates a `Bool` and trusts the result, adding to your trusted base. `decide` (kernel-evaluated) doesn't, but is slower |
| **`sorry` compiles** | so does an added `axiom`. Hence [the CI gate](https://github.com/yihuang/awesome-formal-methods/blob/main/demos/lean/scripts/check-no-sorry.sh) |
| **Termination checking is conservative** | structurally-decreasing recursion is accepted; more general recursion needs `termination_by` and a proof |
| **Universe polymorphism has limits** | some natural constructions need `Type*` gymnastics |
| **mathlib is a heavy dependency** | hours to build from source; always use the cache |
| **Ecosystem churn** | mathlib tracks recent Lean; the API moves, and proofs break on upgrade |
| **"Verified" is relative to the kernel + axioms + `noncomputable`** | state the trusted base, always |

---

## References

- **de Moura, L. & Ullrich, S.** *The Lean 4 Theorem Prover and Programming Language.* CADE 2021.
  [PDF](https://leanprover.github.io/papers/lean4.pdf) — the design rationale.
- **de Moura, L., Kong, S., Avigad, J., van Doorn, F., von Raumer, J.** *The Lean Theorem Prover
  (system description).* CADE 2015 — Lean's origins.
- **Lean documentation.** [lean-lang.org](https://lean-lang.org/) — reference manual, and *Theorem
  Proving in Lean 4* ([link](https://lean-lang.org/theorem_proving_in_lean4/)) and *Functional
  Programming in Lean 4* ([link](https://lean-lang.org/functional_programming_in_lean/)).
- **Lean reference manual.** *The Type System*, *Inductive Types*, *Validating Proofs*.
  [The Type System](https://lean-lang.org/doc/reference/latest/The-Type-System/Inductive-Types/) ·
  [Validating Proofs](https://lean-lang.org/doc/reference/latest/ValidatingProofs/)
- **Carneiro, M.** *Type Checking in Lean 4.*
  [ammkrn.github.io](https://ammkrn.github.io/type_checking_in_lean4/whats_a_kernel.html) — the
  kernel components list, and what a kernel is for.
- **Chlipala, A.** *Certified Programming with Dependent Types.* MIT Press, 2013.
  [Free online](http://adam.chlipala.net/cpdt/) — source of the de Bruijn criterion quotation.
- **Lean FRO.** [lean-fro.org](https://lean-fro.org/) · **Comparator** —
  [github.com/leanprover/comparator](https://github.com/leanprover/comparator)
- **Hubert, T. et al.** *Olympiad-level formal mathematical reasoning with reinforcement learning.*
  *Nature*, 2025. [Link](https://www.nature.com/articles/s41586-025-09833-y)
- **lean-lsp-mcp** — [github.com/oOo0oOo/lean-lsp-mcp](https://github.com/oOo0oOo/lean-lsp-mcp)
- **Bhuwania, N. et al.** *AlphaProof* and the Lean RL environment — see the *Nature* paper above.
- **Morrison, K.** *Why Lean is faster than Rust.* 2026.
  [Link](https://kim-em.github.io/blog/2026-7-24-why-lean-is-faster-than-rust/)
- **Klingner, T. et al.** *A comparison of LLMs' effectiveness in producing formal proofs in Lean 4.*
  [arXiv:2606.05632](https://arxiv.org/abs/2606.05632)
- **This wiki's demos** — [demos/lean](https://github.com/yihuang/awesome-formal-methods/tree/main/demos/lean),
  verified against Lean 4.32.0, no mathlib.

## Further reading

- [type-theory.md](../01-fundamentals/type-theory.md) — the theory underneath the kernel.
- [curry-howard.md](../01-fundamentals/curry-howard.md) — why proof checking is type checking.
- [mathlib.md](mathlib.md) — the library that makes Lean useful for mathematics.
- [proof-tactics.md](proof-tactics.md) — how proofs actually get constructed.
- [llm-proof-engineering.md](../04-ai-era/llm-proof-engineering.md) — AI writing Lean proofs today.
