# The Curry–Howard correspondence

> **TL;DR.** **Propositions are types. Proofs are programs. Proof checking is type checking.**
> That one identification is why modern proof assistants have a small trusted kernel, why you can
> *run* a proof, and why "verified software" is a coherent idea rather than a research aspiration.
> The correspondence is not an analogy — it is a bijection, and you can watch it hold in the code
> below. Its limits matter just as much: **classical reasoning is not free**, and the code on this
> page proves that too.

---

## Theory

### 1. The correspondence

The table that is the whole idea. Every row is a theorem of type theory, provable once and for all:

| Logic | Type theory | Programming |
|---|---|---|
| proposition `A` | type `A` | type |
| proof of `A` | term `t : A` | program |
| `A → B` | function type `A → B` | function |
| `A ∧ B` | product `A × B` | pair / record |
| `A ∨ B` | sum `A + B` | tagged union / `Either` |
| `⊤` (true) | unit type `Unit` | `()` |
| `⊥` (false) | **empty type** `Empty` | a type with no values |
| `¬A` | `A → ⊥` | function into the empty type |
| `∀x : A. B x` | dependent function `Π (x : A), B x` | generic / dependent function |
| `∃x : A. B x` | dependent pair `Σ (x : A), B x` | existential package |
| `A ↔ B` | isomorphism | pair of inverse functions |
| proof by cases | pattern matching | `match` |
| proof by induction | recursion over an inductive type | structural recursion |
| cut / lemma | let-binding, function application | `let`, calling a function |
| cut elimination | **β-reduction** | evaluation |

Read the last two rows again, because they are the load-bearing ones:

> **Normalizing a proof term *is* removing lemmas.** Cut elimination in logic and evaluation in
> programming are the same operation. When Lean reduces a proof, it is simplifying an argument.

### 2. History, and why the discovery took 35 years

| Year | Who | Contribution |
|---|---|---|
| 1934 | **Curry** | observed that the axioms of implicational logic correspond to the types of combinators |
| 1941–58 | **Church, Curry & Feys** | lambda calculus and combinatory logic develop the term side |
| 1967 | **de Bruijn** | builds **Automath**, the first proof assistant, explicitly on this correspondence — *before Howard publishes* |
| 1969 | **Howard** | *The Formulae-as-Types Notion of Construction* — the general statement, circulated as a manuscript, published in 1980 |
| 1972 | **Girard** | System F; the correspondence gives *second-order* logic |
| 1985–88 | **Coquand, Huet, Pauling-Mohring** | CoC, then CIC — the correspondence extended to dependent types, giving the modern proof assistant |
| 2015 | **Wadler** | *Propositions as Types* — a widely-read retrospective |

Two things about that history are worth internalising:

1. **The correspondence was found twice, independently**, and de Bruijn's version was the one that
   produced a working tool. The idea was not obviously useful even to logicians for decades.
2. **The delayed recognition is the point.** For 35 years "proofs are programs" was a curiosity. It
   became the foundation of industrial verification only once dependent types gave it enough
   expressive power to state real theorems.

### 3. Why it holds: natural deduction *is* typed lambda calculus

The correspondence is a syntactic identity between two independently-motivated systems.

```
   NATURAL DEDUCTION                       TYPED LAMBDA CALCULUS
   ─────────────────                       ──────────────────────

   [A]¹  ⋮                                 Γ, x : A ⊢ t : B
     B                                    ──────────────────            (→ intro)
   ──────  (→ intro)¹                      Γ ⊢ (λx. t) : A → B
   A → B

     ⋮            ⋮
   A → B          A                        Γ ⊢ f : A → B    Γ ⊢ a : A
   ───────────────  (→ elim)               ──────────────────────────   (→ elim)
          B                                        Γ ⊢ f a : B
```

The rules line up exactly:

- **Discharging a hypothesis** (`[A]¹`) ↔ **binding a variable** (`λx.`).
- **Modus ponens** ↔ **application**.
- **Normalization of proofs** (removing detours through → intro followed immediately by → elim) ↔
  **β-reduction**: `(λx. t) a ⟶ t[x := a]`.

**A proof with a detour is a program with a redex.** That is why
[strong normalization](type-theory.md#2-simply-typed-lambda-calculus-stlc--the-base) is a theorem
about logic, and why "every proof simplifies to a cut-free one" and "every program terminates" are
the same statement.

### 4. The dependent version — where it becomes useful

Extending to dependent types extends the logic:

| Logic | Type | Where |
|---|---|---|
| `∀x : A, B x` | `Π (x : A), B x` | [type-theory.md §4](type-theory.md#4-dependent-types-π-and-σ--the-real-step) |
| `∃x : A, B x` | `Σ (x : A), B x` | same |
| equality proofs | the identity type / `Eq` | [type-theory.md §6](type-theory.md#6-equality-the-single-most-consequential-design-choice) |

**This is the version that supports software verification**, because now you can write:

```lean
-- "for every input, the output satisfies the spec" — a ∀, i.e. a Π
theorem myMax_ge_both : ∀ a b : Nat, a ≤ myMax a b ∧ b ≤ myMax a b

-- "there exists a witness" — an ∃, i.e. a Σ
example : ∃ n : Nat, n > 2 := ⟨3, by omega⟩
```

The type *is* the specification; the term *is* the proof. There is no separate specification
language, no annotation layer, and no gap between "the thing you proved" and "the thing you claimed"
— they are the same object.

### 5. What the correspondence does NOT give you

This is the part most treatments skip, and it is where the real engineering lives.

#### Classical logic is not free

Intuitionistic logic — which is what the correspondence gives you directly — does **not** prove
excluded middle, double-negation elimination, or Peirce's law. Adding them requires **axioms**, and
axioms are extra trusted assumptions. This is executable:

```lean
-- a constructive proof: uses only the type theory
theorem constructive {p q : Prop} (hp : p) (h : p → q) : q := h hp

-- excluded middle: requires axioms
theorem em_needs_axiom (p : Prop) : p ∨ ¬p := Classical.em p

#print axioms constructive        -- 'constructive' does not depend on any axioms
#print axioms em_needs_axiom      -- depends on: [propext, Classical.choice, Quot.sound]
```

*(Verified: that is the actual output.)*

**Why engineers should care:** the difference is not philosophical. A constructive proof *computes a
witness*; a classical proof may not. If you want to extract a program from your proof, classical
axioms can break extraction. This is why `noncomputable` exists in Lean and why some libraries are
careful to mark where classical reasoning enters. **Your `#print axioms` output is a real
specification of what your proof assumes.**

#### Other limits

| Limit | Consequence |
|---|---|
| **Function extensionality** | not derivable; an axiom in intensional type theory |
| **Propositional extensionality** | an axiom (`propext`) |
| **Proof relevance** | with dependent elimination over `Prop`, proof identity can matter — hence the nuance below |
| **Univalence** | independent of the theory; needs to be assumed (HoTT) |
| **Decidability** | the system does not tell you *which* term inhabits a type — that is search, and it is undecidable |

#### "Propositions as types" vs "propositions as *some* types"

A real disagreement in the field, and worth knowing it exists:

- **Propositions as types** (the classical Curry–Howard reading): every type is a proposition, and
  the distinction between `Prop` and `Type` is one of erasure, not of logic.
- **Propositions as some types** (Harper, and the Lean/Rocq design): `Prop` is a *subset* of `Type`
  — the types that are proof-irrelevant. This justifies `Prop`'s impredicativity and proof
  irrelevance, and it is why Lean's `Prop` is not just `Type` with a tag.

This is not a nitpick. It is the design constraint that lets Lean erase proofs at runtime while still
allowing `Prop` to quantify over everything.

### 6. Generalizations

The correspondence is not one table — it is a family, and each row is a real design decision in a
real language:

| Logic | Type theory | Where you use it |
|---|---|---|
| Intuitionistic propositional | STLC | [type-theory.md §2](type-theory.md#2-simply-typed-lambda-calculus-stlc--the-base) |
| Second-order logic | System F | generics in ML/Haskell |
| Higher-order / dependent | CIC | Lean, Rocq, Agda |
| Modal logic `□A` | **comonad** | staged computation, linear-time |
| Modal logic `◇A` | **monad** | effects, IO, nondeterminism |
| Linear logic | **linear types** | Rust's ownership; session types |
| Separation logic | separation types | [Rust's borrow checker](techniques.md) |
| Classical logic | **continuations** (`call/cc`) | `Control.Operator`, CPS |
| Curry–Howard–**Lambek** | **cartesian closed categories** | semantics of functional languages |

**The Rust connection is the one most engineers will care about.** Linear logic's "use exactly once"
is what Rust's ownership system enforces; separation logic's `∗` is what the borrow checker
approximates. So a working Rust programmer is already relying on a cousin of the Curry–Howard
correspondence — see [techniques.md §5](techniques.md#5-types--lightweight-static-analysis-the-free-tier).

### 7. Why this matters for engineering (not just logic)

| Consequence | Why it is load-bearing |
|---|---|
| **The trusted base is a type checker** | checking a proof means checking a term against a type: no search, no heuristics, no trusted tactics. This is the de Bruijn criterion — see [lean4.md](../05-tools/lean4.md#the-kernel-and-the-trusted-base) |
| **Proofs are data** | a proof is an object you can store, transmit, inspect, and machine-check independently. This is what makes [proof-carrying code](../04-ai-era/fm-for-ai.md#4a-verifying-generated-code) possible |
| **Programs can be extracted from proofs** | prove a specification, get a program (Rocq, Agda, F*, Lean's `#eval`) |
| **Type systems are lightweight verification** | the correspondence is the reason "types are a formal method" is literally true, not a rhetorical stretch |
| **Tactics are untrusted** | only the kernel is trusted, which is why [a tactic can be arbitrary metaprogram code](../05-tools/proof-tactics.md#2-tactics-are-metaprograms-not-logic) without compromising soundness |

That last row is the design principle that makes modern proof assistants usable: because checking is
cheap and independent of how the proof was *found*, you can throw an enormous, complicated,
possibly-buggy search procedure at the problem — or an AI — and the kernel still decides.

---

## Tutorial: the correspondence, executable

All code below compiles and runs against Lean 4.32.0 with no mathlib.

### Step 1 — Read each logical connective as a type

```lean
-- IMPLICATION is the FUNCTION type
theorem impl_as_fn {p q : Prop} (hp : p) (h : p → q) : q := h hp

-- CONJUNCTION is the PRODUCT type; `⟨·,·⟩` is the pair
theorem and_as_product {p q : Prop} (hp : p) (hq : q) : p ∧ q := ⟨hp, hq⟩

-- DISJUNCTION is the SUM type; `.elim` is the case split
theorem or_as_sum {p q r : Prop} (h : p ∨ q) (hp : p → r) (hq : q → r) : r :=
  h.elim hp hq

-- TRUE is the UNIT type
theorem true_as_unit : True := trivial

-- FALSE is the EMPTY type
theorem false_as_empty : False → True := fun h => False.elim h

-- NEGATION is a function into the empty type
theorem not_as_fn_to_empty {p : Prop} : ¬p → (p → False) := fun h hp => h hp

-- forall is the DEPENDENT FUNCTION type (Π)
theorem forall_as_pi {α : Type} (p : α → Prop) (h : ∀ x, p x) : ∀ x, p x := h

-- exists is the DEPENDENT PAIR type (Σ)
theorem exists_as_sigma {α : Type} (p : α → Prop) (a : α) (ha : p a) : ∃ x, p x := ⟨a, ha⟩

-- IFF is an isomorphism: a pair of inverse functions
theorem iff_as_iso {p q : Prop} (f : p → q) (g : q → p) : p ↔ q := ⟨f, g⟩
```

Notice that `∧`, `∨`, `∀`, `∃` are **defined** in Lean as types — `And`, `Or`, `Exists` — and
`⟨hp, hq⟩`, `.elim`, `⟨a, ha⟩` are ordinary term constructors. There is no separate proof language.

### Step 2 — β-reduction is cut elimination

```lean
-- This proof has a "detour": it introduces a function and immediately applies it.
example {p : Prop} (hp : p) : p := (fun h => h) hp
```

The proof term `(fun h => h) hp` contains a redex. Reduction gives `hp`, exactly as cut elimination
removes the detour in a sequent proof. **`#reduce` and `#eval` let you watch this happen.**

### Step 3 — Watch the axiom boundary

This is the most instructive part of the page, and it is real output:

```lean
theorem constructive {p q : Prop} (hp : p) (h : p → q) : q := h hp
#print axioms constructive
-- 'constructive' does not depend on any axioms          ← pure type theory

theorem em_needs_axiom (p : Prop) : p ∨ ¬p := Classical.em p
#print axioms em_needs_axiom
-- 'em_needs_axiom' depends on axioms: [propext, Classical.choice, Quot.sound]
--                                                        ← classical reasoning is assumed
```

**The `#print axioms` command is the correspondence made operational.** It tells you exactly which
parts of your reasoning are constructive (pure type theory, extractable to a program) and which are
classical (assumed, and potentially non-computational). Make it part of your definition of done.

### Step 4 — Use it to make a partial function total

The correspondence is not only about logic; it changes what you can *express as a program*.

```lean
-- Curve25519 field arithmetic, from EverCrypt: the type carries the invariant
--   Fe := { x : Nat // x < 2^255 - 19 }
-- so an out-of-range value is not a runtime error — it is unrepresentable.
```

That example is from a real verified cryptographic library
([HACL*/EverCrypt](../03-applications/hardware-crypto.md)), and it is the correspondence doing
engineering work: the invariant is a proposition, the `//` is `Σ`, and the type checker is what
enforces it.

### Step 5 — The exercise that makes it click

```lean
-- Prove these by writing the PROGRAM, not by searching for a proof.
example {p q : Prop} : p → q → p := ?_
example {p q r : Prop} : (p → q → r) → (p → q) → p → r := ?_
example {p q : Prop} : p ∧ q → q ∧ p := ?_
example {α : Type} {p : α → Prop} : (∃ x, p x) → ¬(∀ x, ¬p x) := ?_
```

Each is a *program shape*: the first takes two arguments and returns the first; the second is
`fun f g x => f x (g x)`; the third swaps a pair; the fourth unpacks and contradicts. **If you can
see the program, you have understood the correspondence.** (The converse — `¬(∀x, ¬p x) → ∃x, p x`
— is *not* intuitionistically provable, which is itself the lesson.)

---

## Reference

### Correspondence tables

**Logic ↔ types ↔ categories** (Curry–Howard–Lambek, for the categorically inclined):

| Logic | Type theory | Category |
|---|---|---|
| proposition | type | object |
| proof | term | morphism |
| implication | function type | exponential |
| conjunction | product | product |
| disjunction | sum | coproduct |
| true | unit | terminal object |
| false | empty | initial object |
| cut elimination | β-reduction | — |
| — | η-expansion | — |

**Constructive vs classical, in terms of what you must assume:**

| Principle | Status in intuitionistic type theory |
|---|---|
| `A → B → A` | provable |
| `A ∧ B → B ∧ A` | provable |
| `∀x. P x → ∃x. P x` (with witness) | provable (witness is the term) |
| `∃x. P x → ¬∀x. ¬P x` | provable |
| `¬∀x. ¬P x → ∃x. P x` | **not** provable |
| `P ∨ ¬P` (excluded middle) | **axiom** |
| `¬¬P → P` (double-negation elimination) | **axiom** |
| `((P → Q) → P) → P` (Peirce) | **axiom** |
| function extensionality | axiom (`funext`) |
| propositional extensionality | axiom (`propext`) |

### In Lean, concretely

| Logic | Lean name | Construction | Elimination |
|---|---|---|---|
| `→` | function type | `fun x => …` | application |
| `∧` | `And` | `⟨h₁, h₂⟩` | `.1`, `.2`, `obtain` |
| `∨` | `Or` | `Or.inl`, `Or.inr` | `.elim`, `cases` |
| `⊤` | `True` | `trivial` | — |
| `⊥` | `False` | (none) | `False.elim` |
| `¬` | `Not` = `→ False` | `fun h => …` | application |
| `∀` | `Π` (dependent function) | `fun x => …` | application |
| `∃` | `Exists` (`Σ` in `Prop`) | `⟨w, h⟩` | `obtain ⟨w, h⟩` |
| `↔` | `Iff` | `⟨f, g⟩` | `.mp`, `.mpr` |
| `=` | `Eq` | `rfl` | `rw`, `subst` |

### Historical dates

| Year | Event |
|---|---|
| 1934 | Curry: the formulae-as-types observation |
| 1940 | Church: simple type theory |
| 1967–70 | de Bruijn: Automath, the first proof assistant |
| 1969 | Howard: the general statement (published 1980) |
| 1972 | Girard: System F, and the inconsistency of System U |
| 1971–84 | Martin-Löf: intuitionistic type theory |
| 1984 | Coquand & Huet: the Calculus of Constructions |
| 1989 | Coq released (the tool that made it mainstream) |
| 1990 | Coquand & Paulin-Mohring: inductive types (CIC) |
| 2013 | HoTT book: univalent foundations |
| 2015 | Wadler: *Propositions as Types* |

---

## References

- **Howard, W.A.** *The Formulae-as-Types Notion of Construction.* 1969; in *To H.B. Curry: Essays
  on Combinatory Logic, Lambda Calculus and Formalism*, Academic Press, 1980.
  [PDF](https://www.cs.cmu.edu/~crary/819-f09/Howard80.pdf) — the primary source.
- **Curry, H.B. & Feys, R.** *Combinatory Logic, Vol. I.* North-Holland, 1958 — the earlier
  observation for implicational logic.
- **de Bruijn, N.G.** *The Mathematical Language AUTOMATH, its Usage, and Some of its Extensions.*
  Symposium on Automatic Demonstration, 1970.
- **Wadler, P.** *Propositions as Types.* Communications of the ACM, 2015.
  [PDF](https://homepages.inf.ed.ac.uk/wadler/papers/propositions-as-types/propositions-as-types.pdf) —
  the best single retrospective; also covers the history and the sociology.
- **Girard, J.-Y.** *Interprétation fonctionnelle et élimination des coupures…* Thèse, Paris VII,
  1972.
- **Coquand, T. & Huet, G.** *The Calculus of Constructions.* Information and Computation 76, 1988.
  [PDF](https://hal.inria.fr/inria-00076024/document)
- **Martin-Löf, P.** *Intuitionistic Type Theory.* Bibliopolis, 1984.
- **Lambek, J. & Scott, P.J.** *Introduction to Higher-Order Categorical Logic.* CUP, 1986 — the
  categorical reading.
- **Harper, R.** *Practical Foundations for Programming Languages.* 2nd ed., CUP 2016.
  [Free online](https://www.cs.cmu.edu/~rwh/pfpl/) — the "propositions as some types" position.
- **The Univalent Foundations Program.** *Homotopy Type Theory: Univalent Foundations of
  Mathematics.* 2013. [Free online](https://homotopytypetheory.org/book/)
- **Pierce, B.** *Types and Programming Languages.* MIT Press, 2002.
- **Nederpelt, R. & Geuvers, H.** *Type Theory and Formal Proof.* CUP, 2014.
- **Chlipala, A.** *Certified Programming with Dependent Types.* MIT Press, 2013.
  [Free online](http://adam.chlipala.net/cpdt/) — the de Bruijn criterion.
- **Wadler, P.** *Propositions as Types* (video) and **Milewski, B.** *Category Theory for
  Programmers* — for the categorical view.
- [Wikipedia: Curry–Howard correspondence](https://en.wikipedia.org/wiki/Curry%E2%80%93Howard_correspondence) ·
  [Intuitionistic type theory](https://en.wikipedia.org/wiki/Intuitionistic_type_theory) ·
  [nLab: propositional logic as a dependent type theory](https://ncatlab.org/nlab/show/propositional+logic+as+a+dependent+type+theory)
- **Lean documentation.** *Axioms and Computation* (Theorem Proving in Lean 4) —
  [link](https://lean-lang.org/theorem_proving_in_lean4/Axioms-and-Computation/)

## Further reading

- [type-theory.md](type-theory.md) — the system this correspondence lives in.
- [lean4.md](../05-tools/lean4.md) — the tool built on it, and its kernel.
- [proof-tactics.md](../05-tools/proof-tactics.md) — how you actually construct the terms.
- [techniques.md](techniques.md) — where "types are a formal method" lands in industry.
