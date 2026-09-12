# Type theory and dependent types

> **TL;DR.** Type theory is a foundation for mathematics and programming in which **every term has a
> type**, and types are themselves terms. Its distinguishing feature is that **propositions are
> types** ([Curry–Howard](curry-howard.md)), so proof checking *is* type checking, and the trusted
> core of a proof assistant shrinks to a type checker. **Dependent types** let types mention values
> — `Vec α n` is a list of exactly `n` elements — which is what turns a type system from a bug
> filter into a specification language. Everything in this wiki that involves Lean, Rocq, Agda, or
> Isabelle/HOL rests on the material on this page.

---

## Theory

### 1. Judgements: the shape of a type theory

A type theory is presented as a collection of **judgements** and **rules**. The four you meet:

| Judgement | Reads |
|---|---|
| `Γ ⊢ A : Type` | in context `Γ`, `A` is a type |
| `Γ ⊢ t : A` | in context `Γ`, the term `t` has type `A` |
| `Γ ⊢ A ≡ B : Type` | `A` and `B` are **definitionally equal** types |
| `Γ ⊢ t ≡ u : A` | `t` and `u` are definitionally equal terms |

`Γ` is a **context**: a list of variables and their types. Rules have the form

```
   premise₁    premise₂
   ─────────────────────
        conclusion
```

and are read as "if the premises hold, so does the conclusion". **A type checker is an
implementation of these rules**, and that is the whole of the logic — everything else in a proof
assistant (tactics, metaprogramming, editor support) is machinery for *finding* derivations, not for
*checking* them.

**Why the shape matters for trust.** Because the rules are purely syntactic and local, checking a
derivation requires no search and no cleverness. This is the
[cheap-checking half of the fundamental asymmetry](../01-fundamentals/automated-reasoning.md#3-the-deep-asymmetry-checking-is-easy-searching-is-hard),
and it is why [the kernel can be small](../05-tools/lean4.md#the-kernel-and-the-trusted-base).

### 2. Simply typed lambda calculus (STLC) — the base

The smallest interesting type theory. Three constructs: variables, abstraction, application.

```
   x : A ∈ Γ                     Γ, x : A ⊢ t : B                Γ ⊢ f : A → B    Γ ⊢ a : A
   ───────────                   ──────────────────              ──────────────────────────
     Γ ⊢ x : A                     Γ ⊢ (λx. t) : A → B                   Γ ⊢ f a : B
       (var)                          (abs)                                (app)
```

Three syntactic categories, three rules. That is nearly the whole system.

**What STLC gets you:** every well-typed program terminates. The proof is
**strong normalization** — a well-typed term cannot reduce forever, because the types give you a
measure. That is a *non-trivial theorem about a programming language*, proved once at the level of
the type theory rather than per-program.

**What STLC cannot do:** express polymorphism, recursion, or anything where a type depends on a
value. Those gaps are what the rest of the page fills in.

### 3. Polymorphism: System F

Add universal quantification over types (Girard 1972; Reynolds 1974, independently):

```
   Γ, α : Type ⊢ t : A
   ─────────────────────                      Γ ⊢ t : ∀α. A
   Γ ⊢ (Λα. t) : ∀α. A                        ────────────────────
       (type abstraction)                     Γ ⊢ t [B] : A[α := B]
                                                   (type application)
```

This is `id : ∀α. α → α`, and in Lean/Rocq/Agda surface syntax it is simply `def id {α : Type}
(x : α) : α := x` with `α` implicit.

**Note the historical cautionary tale.** System F is strongly normalizing. **System F<sub>ω</sub>**
with type-level recursion is not. And the older **System U** was proved *inconsistent* by Girard in
1972 — which is the same phenomenon as the universe problem in §5. Adding power to a type theory can
destroy its consistency, and the failure mode is not obvious.

### 4. Dependent types: Π and Σ — the real step

Now the move that makes the whole thing worth calling a *specification* language: **let types
mention terms.**

| Form | Name | Reads as | Logic |
|---|---|---|---|
| `Π (x : A), B x` | dependent function | "a function that, for each `x : A`, returns a `B x`" | universal `∀` |
| `Σ (x : A), B x` | dependent pair | "a value `x : A` together with a `B x`" | existential `∃` |
| `A → B` | non-dependent function | `Π (_ : A), B` | implication |
| `A × B` | non-dependent pair | `Σ (_ : A), B` | conjunction |

The typing rules are the STLC rules with the codomain allowed to mention the argument:

```
   Γ, x : A ⊢ b : B x
   ─────────────────────────            Γ ⊢ f : Π (x : A), B x      Γ ⊢ a : A
   Γ ⊢ (λx. b) : Π (x : A), B x         ─────────────────────────────────────────
            (Π-intro)                     Γ ⊢ f a : B a
                                                    (Π-elim)
```

**Why this is different in kind, not degree.** With `Π` and `Σ` you can say things a non-dependent
type system cannot express *at all*:

| Specification | Type |
|---|---|
| "a list of exactly `n` elements" | `Vec α n` |
| "the output list is sorted **and** a permutation of the input" | `Σ (out : List α), Sorted out × Perm out xs` |
| "a division function that cannot be called with a zero divisor" | `Π (a : Int) (b : Int) (h : b ≠ 0), Int` |
| "a compiler that preserves semantics" | `Π (p : Program), Π (s : State), eval (compile p) s = eval p s` |
| "there exists a prime greater than `n`" | `Σ (p : Nat), Prime p × p > n` |

This is the difference between "the type checker stops you doing something silly" and "the type
checker states your theorem". Everything else in this wiki — the
[specification ladder](specifications.md#the-specification-ladder-from-weak-to-strong), refinement,
verified compilers — is downstream of this one idea.

**The `Vec` example is the canonical illustration** because it makes the two benefits visible at
once:

```lean
inductive Vec (α : Type) : Nat → Type where
  | nil  : Vec α 0
  | cons : α → {n : Nat} → Vec α n → Vec α (n + 1)
```

- **`nil` and `cons` carry their length in the type**, so the length is not runtime data — it is
  erased and cannot be wrong.
- **`head` becomes total**, with no `Option` and no runtime check:

```lean
def head : Vec α (n + 1) → α
  | .cons x _ => x
```

  The partial function `List α → α` is unrepresentable at this type. **The type system has absorbed
  an entire precondition.**

### 5. Universes: `Prop`, `Type`, `Sort` — and the paradox that forced them

Types have types, and those have types. If you let that be one level, the theory is inconsistent.

> **Girard's paradox (1972).** System U, which permitted a type of all types, is inconsistent. This
> is the same phenomenon that showed **Martin-Löf's original (1971) type theory, which allowed
> `Type : Type`, to be inconsistent.**

The fix is a **universe hierarchy**: a type lives in a universe, and a universe lives in a bigger
one.

```
   Prop = Sort 0
   Type u = Sort (u + 1)          -- Type u : Type (u+1), and Type u is NOT : Type u
```

| Universe | Contents | Impredicative? |
|---|---|---|
| `Prop` | propositions (types whose terms are all proofs) | **yes** — `∀ (α : Type), α → α` can live in `Prop` |
| `Type u` | computational types | no, predicative, one level up per quantifier |

Two properties of Lean's `Prop`, and both matter in practice:

1. **Impredicativity.** A `Prop`-valued quantification over all types is itself a `Prop`. This is
   what lets logic be written naturally at the top level.
2. **Proof irrelevance.** All proofs of the same proposition are *definitionally equal*. There is
   only ever one proof object to worry about, which is why `Prop` can be erased at runtime.

**The engineering takeaway.** `Prop` is for things you only want to *know*; `Type` is for things you
want to *compute with*. Choosing the right one is a real design decision: proving a fact is cheaper
in `Prop`, but extracting a witness from a proof requires `Type` (or `noncomputable` + choice).

### 6. Equality: the single most consequential design choice

Two different equalities coexist, and confusing them is the most common source of confusion for
newcomers.

| | Definitional (judgemental) | Propositional |
|---|---|---|
| Written | `A ≡ B`, checked by the kernel | `a = b : Prop`, a *type* |
| Meaning | "these are the same by computation" | "there is a proof that these are equal" |
| Decided by | reduction / **conversion checking** | proving a theorem |
| Used for | type checking, `rfl` | rewriting, mathematics |

```lean
-- definitional: closes by computation, no proof needed
example : 2 + 2 = 4 := rfl

-- propositional: the two sides are not definitionally equal, so you must prove it
example (m n : Nat) : m + n = n + m := Nat.add_comm m n
```

**Why this matters enormously in practice:** definitional equality is what makes proofs ergonomic.
When `simp`, `rfl`, or `omega` close a goal, they are exploiting computation rather than reasoning.
Correspondingly, **the ergonomics of a proof assistant are largely determined by how much work its
definitional equality does** — and that is a dial, not a fact:

| | Intensional (Lean, Rocq, Agda, MLTT) | Extensional (Nuprl, some variants) |
|---|---|---|
| Equality reflection (`a = b` ⟹ `a ≡ b`) | ❌ | ✅ |
| Type checking | **decidable** | **undecidable** (needs proof search during checking) |
| Function extensionality | an axiom (Lean: `propext`/`funext`) | derived |
| Typing is unique | yes | no |

**Lean, Rocq, Agda, and Isabelle/HOL are intensional**, trading convenience for decidability. That is
the standard engineering choice: a *decidable* type checker is what makes proof checking cheap, and
cheap proof checking is the entire value proposition ([§1](#1-judgements-the-shape-of-a-type-theory)).

### 7. Inductive types, recursors, and termination

`inductive` declarations introduce a type, its constructors, and — automatically — its
**recursor** (elimination principle). Adding `Nat`:

```lean
inductive Nat where
  | zero : Nat
  | succ : Nat → Nat
```

generates `Nat.rec`, the principle of mathematical induction. **Induction is not an axiom bolted on
— it is derived from the shape of the type.** This is the whole of the "Calculus of Inductive
Constructions": CIC = CoC + inductive definitions, and it is what Lean, Rocq, and Agda use.

Two obligations the kernel enforces so that this remains consistent:

| Obligation | Rule | Why |
|---|---|---|
| **Strict positivity** | an inductive type may not occur in a negative position in its own constructor | prevents `inductive Bad where mk : (Bad → False) → Bad`, which yields `False` |
| **Termination / guard checking** | recursion must be structurally decreasing (or proved well-founded) | prevents `def loop : False := loop`, which proves everything |

`#print axioms` is how you check that a proof didn't sneak around these, and
[the CI gate](https://github.com/yihuang/awesome-formal-methods/blob/main/demos/lean/scripts/check-no-sorry.sh) is how you make that a build failure. See
[limits.md § the trusted base](limits.md#the-trusted-base).

### 8. The landscape of type theories

| System | Adds over the previous | Used by |
|---|---|---|
| **STLC** | functions with types | textbook base |
| **System F** | polymorphism (`∀α`) | ML, Haskell core |
| **System F<sub>ω</sub>** | type operators | Haskell (with caveats), Scala-ish |
| **λ-cube / CoC** | dependent types, type-level quantification | Coq/Rocq's core |
| **CIC** | + inductive types and recursors | **Lean, Rocq, Agda** |
| **MLTT** | Martin-Löf's intensional type theory; identity types | Agda, Cubical Agda |
| **HoTT / Cubical** | identity types as paths; univalence | research; `Univalent Foundations` |
| **Observational / extensional TT** | equality reflection | Nuprl |
| **Isabelle/HOL** | *not* dependent — simple type theory + polymorphism + definitional principles | seL4, most industrial ITP |

**Note the last row.** Isabelle/HOL is not a dependent type theory, and seL4 was verified in it. So
dependent types are a powerful tool, not a precondition for serious verification. The trade-off is
expressiveness versus ergonomics and automation.

### 9. What is decidable

| Question | Answer |
|---|---|
| Given a term and a type, is it well typed? | **decidable** (that is the point) |
| Are two types definitionally equal? | **decidable** in principle; the naive algorithm can loop, so implementations use heuristics |
| Can we *infer* the type of an unannotated term? | **undecidable** in general for dependent types |
| Can we find a proof of a given proposition? | **undecidable** — this is [Rice's theorem](limits.md#rices-theorem-1953--the-one-engineers-should-know) territory, and it is exactly the gap that [tactics](../05-tools/proof-tactics.md) and [AI](../04-ai-era/llm-proof-engineering.md) attack |

That table is the whole architecture of a proof assistant in miniature: **types make checking
decidable, and everything hard happens on the *finding* side.**

---

## Tutorial: dependent types in Lean

All the code below compiles as written (verified against Lean 4.32.0, no mathlib needed).

### Step 1 — A length-indexed vector

```lean
inductive Vec (α : Type) : Nat → Type where
  | nil  : Vec α 0
  | cons : α → {n : Nat} → Vec α n → Vec α (n + 1)
```

Read the type of `cons` carefully: it takes an element, a `Vec α n`, and produces a `Vec α (n + 1)`.
**The length is a parameter of the type, computed by the constructor.**

### Step 2 — A total `head`

```lean
def head : Vec α (n + 1) → α
  | .cons x _ => x
```

There is no case for `nil`, and Lean does not ask for one — `Vec α 0` cannot be unified with
`Vec α (n + 1)`. **The empty case is eliminated by the type.** Compare with `List.head? : List α →
Option α`, which forces every caller to handle a case that the caller may know is impossible.

### Step 3 — Append, and where definitional equality bites

```lean
def append : Vec α m → Vec α n → Vec α (n + m)
  | .nil, ys => ys
  | .cons x xs, ys => .cons x (append xs ys)
```

**Notice the length is `n + m`, not `m + n`.** This is not arbitrary. In the `cons` case the goal is
`Vec α (n + (m + 1))`; the result `cons x (append xs ys)` has type `Vec α ((n + m) + 1)`. These are
**definitionally equal** because `Nat.add` recurses on its *second* argument, so `n + (m + 1)`
reduces to `(n + m) + 1`. Written as `m + n` the equation would not hold definitionally and you
would need an explicit rewrite.

**This is the practical face of §6.** Choosing a formulation where the needed equation holds *by
computation* is worth more than any amount of tactic skill, and it is the main craft skill in
dependent type theory.

### Step 4 — Prove something about it

```lean
def toList : Vec α n → List α
  | .nil => []
  | .cons x xs => x :: toList xs

theorem length_toList (v : Vec α n) : (toList v).length = n := by
  induction v with
  | nil => rfl
  | cons x xs ih => simp [toList, ih]
```

Two things worth seeing:

- **`induction v`** works on `Vec α n` even though `n` is an index, and Lean generalises the index
  automatically. Induction principles come from the type, per §7.
- **The `cons` case needs `simp [toList, ih]`**, not `rfl`: `(x :: toList xs).length` is
  `(toList xs).length + 1`, and reaching `n + 1` uses the induction hypothesis plus arithmetic
  simplification. Definitional equality did not suffice here — propositional reasoning did.

### Step 5 — The same idea as a specification

The reason this matters beyond data structures: the identical mechanism states *theorems*.

```lean
-- "division, but you cannot pass zero" — the precondition is in the type
def safeDiv (a b : Int) (h : b ≠ 0) : Int := a / b

-- "there is a prime greater than n" — the witness and the proof travel together
-- (requires mathlib; shown for shape)
-- theorem infinitely_many_primes : ∀ n : Nat, ∃ p, p > n ∧ Nat.Prime p

-- "the output is sorted AND a permutation" — the frame condition included
-- def sort (xs : List α) : { out : List α // Sorted out ∧ Perm out xs }
```

**The discipline transferable from this page:** every time you write a function, ask *what does the
type not say that I know is true?* Dependent types let you move that knowledge out of a comment, out
of a runtime check, and into the type where the checker enforces it. That is the whole skill.

---

## Reference

### Rule summary

| Rule | Premises | Conclusion |
|---|---|---|
| var | `x : A ∈ Γ` | `Γ ⊢ x : A` |
| abs / Π-intro | `Γ, x : A ⊢ t : B x` | `Γ ⊢ (λx. t) : Π (x : A), B x` |
| app / Π-elim | `Γ ⊢ f : Π (x : A), B x`, `Γ ⊢ a : A` | `Γ ⊢ f a : B a` |
| pair / Σ-intro | `Γ ⊢ a : A`, `Γ ⊢ b : B a` | `Γ ⊢ ⟨a, b⟩ : Σ (x : A), B x` |
| projections / Σ-elim | `Γ ⊢ p : Σ (x : A), B x` | `Γ ⊢ p.1 : A`, `Γ ⊢ p.2 : B p.1` |
| conversion | `Γ ⊢ t : A`, `A ≡ B` | `Γ ⊢ t : B` |

The **conversion rule** is the one that makes definitional equality part of type checking; it is
also what makes the system ergonomic.

### Terminology

| Term | Meaning |
|---|---|
| **Judgement** | an assertion of the form `Γ ⊢ J` |
| **Context** `Γ` | the variables in scope and their types |
| **Π-type** | dependent function type; `A → B` when non-dependent |
| **Σ-type** | dependent pair type; `A × B` when non-dependent |
| **Universe** | a level in the hierarchy preventing `Type : Type` |
| **`Prop`** | the universe of propositions; impredicative; proof-irrelevant |
| **Definitional equality** `≡` | equality by computation, checked by the kernel |
| **Propositional equality** `=` | the identity type; requires a proof |
| **Conversion** | checking definitional equality during type checking |
| **Canonicity** | every closed term of an inductive type reduces to a constructor |
| **Strong normalization** | no well-typed term reduces forever |
| **Impredicative** | a type can quantify over all types including itself |
| **Strict positivity** | the constraint on inductive definitions that keeps the logic consistent |
| **Extraction** | erasing proofs to obtain a runnable program |
| **Univalence** | the axiom that equivalent types are equal (HoTT) |

### Systems at a glance

| | Dependent? | Polymorphic? | Consistent? | Checker decidable? |
|---|---|---|---|---|
| STLC | ❌ | ❌ | ✅ | ✅ |
| System F | ❌ | ✅ | ✅ | ✅ |
| System U | ❌ | ✅ + type-level recursion | ❌ **(Girard)** | — |
| MLTT (1971) | ✅ | ✅ | ❌ **(Type : Type)** | — |
| MLTT (intensional, with universes) | ✅ | ✅ | ✅ | ✅ |
| CoC / CIC | ✅ | ✅ | ✅ | ✅ |
| Isabelle/HOL | ❌ | ✅ | ✅ | ✅ |

### Where to go next in this wiki

| For | See |
|---|---|
| What the correspondence buys you | [curry-howard.md](curry-howard.md) |
| The concrete tool | [lean4.md](../05-tools/lean4.md) |
| The library | [mathlib.md](../05-tools/mathlib.md) |
| How you actually construct proofs | [proof-tactics.md](../05-tools/proof-tactics.md) |
| How language semantics get formalised | [semantics.md](semantics.md) |
| Why `Type : Type` and undecidability bound what's possible | [limits.md](limits.md) |

---

## References

- **Church, A.** *A Formulation of the Simple Theory of Types.* Journal of Symbolic Logic, 1940.
- **Church, A.** *The Calculi of Lambda-Conversion.* Princeton, 1941.
- **Curry, H.B. & Feys, R.** *Combinatory Logic, Vol. I.* 1958 — the "formulae-as-types" observation.
- **Howard, W.A.** *The Formulae-as-Types Notion of Construction.* 1969; published in *To H.B.
  Curry: Essays on Combinatory Logic, Lambda Calculus and Formalism*, 1980.
  [PDF](https://www.cs.cmu.edu/~crary/819-f09/Howard80.pdf)
- **de Bruijn, N.G.** *The Mathematical Language AUTOMATH, its Usage, and Some of its Extensions.*
  1970 — the independent discovery, and the first proof assistant.
- **Girard, J.-Y.** *Interprétation fonctionnelle et élimination des coupures de l'arithmétique
  d'ordre supérieur.* Thèse, 1972 — System F, and the inconsistency of System U.
  [System U](https://en.wikipedia.org/wiki/System_U)
- **Martin-Löf, P.** *An Intuitionistic Theory of Types.* 1971; *Intuitionistic Type Theory.* 1984.
  [nLab](https://ncatlab.org/nlab/show/Martin-L%C3%B6f+dependent+type+theory)
- **Reynolds, J.C.** *Towards a Theory of Type Structure.* 1974 — polymorphism, independently.
- **Coquand, T. & Huet, G.** *The Calculus of Constructions.* Information and Computation, 1988.
  [PDF](https://hal.inria.fr/inria-00076024/document)
- **Coquand, T. & Paulin-Mohring, C.** *Inductively Defined Types.* 1990 — CIC.
- **Aydemir, B., Charguéraud, A., Pierce, B., Pollack, R., Weirich, S.** *Engineering Formal
  Metatheory.* POPL 2008 — the binding problem, and locally nameless representation.
- **Pierce, B.** *Types and Programming Languages.* MIT Press, 2002 — STLC and System F, rigorously.
- **Harper, R.** *Practical Foundations for Programming Languages.* 2nd ed., CUP 2016.
  [Free online](https://www.cs.cmu.edu/~rwh/pfpl/) — the modern type-theoretic account.
- **Nederpelt, R. & Geuvers, H.** *Type Theory and Formal Proof: An Introduction.* CUP, 2014 —
  gentlest route into dependent types.
- **Nordström, B., Petersson, K., Smith, J.** *Programming in Martin-Löf's Type Theory.* 1990.
  [Free online](https://www.cse.chalmers.se/research/group/logic/book/)
- **The Univalent Foundations Program.** *Homotopy Type Theory.* 2013.
  [Free online](https://homotopytypetheory.org/book/)
- **Chlipala, A.** *Certified Programming with Dependent Types.* MIT Press, 2013.
  [Free online](http://adam.chlipala.net/cpdt/) — the source of the de Bruijn criterion quotation.
- **Lean reference manual.** *The Type System* and *Inductive Types*.
  [lean-lang.org](https://lean-lang.org/doc/reference/latest/The-Type-System/Inductive-Types/)
- **Carneiro, M.** *Type Checking in Lean 4* — what a kernel is, and why it is kept small.
  [ammkrn.github.io](https://ammkrn.github.io/type_checking_in_lean4/whats_a_kernel.html)
- [Wikipedia: Intuitionistic type theory](https://en.wikipedia.org/wiki/Intuitionistic_type_theory) ·
  [Dependent type](https://en.wikipedia.org/wiki/Dependent_type) ·
  [System F](https://en.wikipedia.org/wiki/System_F) ·
  [Curry–Howard correspondence](https://en.wikipedia.org/wiki/Curry%E2%80%93Howard_correspondence)

## Further reading

- [curry-howard.md](curry-howard.md) — why propositions *are* types.
- [semantics.md](semantics.md) — the other foundational view: operational semantics.
- [limits.md](limits.md) — decidability, and where type theory does not save you.
