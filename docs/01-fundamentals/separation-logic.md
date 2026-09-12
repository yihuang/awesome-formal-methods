# Separation logic

> **TL;DR.** Ordinary [Hoare logic](logics.md#1-hoare-logic--reasoning-about-code) cannot reason
> about pointers. If `x` and `y` might alias the same cell, every rule needs case analysis over
> aliasing, and the analysis explodes. Separation logic fixes this with one connective: `P ∗ Q`
> means "`P` and `Q` hold of **disjoint** parts of the heap". That single change buys the
> **frame rule** — *verify a function once, and it composes with any disjoint heap* — which is what
> makes local reasoning scale, what makes Rust's borrow checker a decidable fragment of it, and what
> Iris turned into a general framework for concurrency, type systems, and program equivalence.

---

## Theory

### 1. The problem: aliasing destroys compositionality

Here is a correct Hoare triple about a two-cell swap:

```
   { x ↦ 1 ∧ y ↦ 2 }   swap(x, y)   { x ↦ 2 ∧ y ↦ 1 }
```

And here is why it doesn't compose. Suppose you know `{ P } C { Q }`, and you want to conclude
`{ P ∧ R } C { Q ∧ R }` for some unrelated assertion `R` — the **frame** property, which is what
lets you reason about one function while ignoring the rest of the program.

In ordinary Hoare logic that inference is **invalid**, because `R` and `Q` might talk about the same
memory. `C` might have modified the cell `R` mentions. So instead of one rule you need a side
condition: *"`C` does not modify the footprint of `R`"* — which is undecidable, and in practice
becomes a global "modifies" analysis over the whole program.

**That is the whole problem.** Every scalable program logic must answer "what did this code touch?",
and separation logic answers it in the *logic* rather than in a side condition.

### 2. The model: heaps are partial maps, and disjointness is the algebra

```
   Heap  ::=  Loc ⇀ Val                     -- a finite partial map
   h₁ ⊎ h₂                                   -- disjoint union: defined only if dom(h₁) ∩ dom(h₂) = ∅
```

A program state is a heap. Two heaps are **compatible** if their domains are disjoint, and composing
them is partial union. That is the entire semantic idea: **`∗` is the lift of `⊎` to assertions.**

```
   h ⊨ P ∗ Q    iff   ∃ h₁, h₂.  h = h₁ ⊎ h₂  ∧  h₁ ⊨ P  ∧  h₂ ⊨ Q
```

Read it as *"the heap splits into two pieces, one satisfying `P` and one satisfying `Q`"*. Because
the split must be disjoint, `P ∗ Q` **asserts that `P` and `Q` do not share memory** — which is
exactly the fact Hoare logic could not express.

### 3. The connectives

| Connective | Notation | Meaning |
|---|---|---|
| **Points-to** | `x ↦ v` | the heap has exactly one cell, at `x`, holding `v` |
| **Separating conjunction** | `P ∗ Q` | the heap splits into disjoint parts satisfying `P` and `Q` |
| **Magic wand** | `P -∗ Q` | given a disjoint heap satisfying `P`, the result satisfies `Q` — implication *with resource* |
| **Empty heap** | `emp` | the heap is empty |
| **Pure assertion** | `⌜φ⌝` | the mathematical fact `φ` holds (touches no heap) |
| **Ordinary conjunction** | `P ∧ Q` | both hold of the *same* heap |
| **Disjunction / existential** | `P ∨ Q`, `∃ x, P x` | as usual |
| **Later** | `▷ P` | `P` holds after one step of computation — for recursion and concurrency |
| **Persistent** | `□ P` | `P` holds and does not consume resources (can be duplicated) |

**`∧` versus `∗` is the distinction to internalise.** `x ↦ 1 ∧ x ↦ 1` is fine (both conjuncts hold of
the same cell — redundant but true). `x ↦ 1 ∗ x ↦ 1` is **false**, because it demands two disjoint
cells at the same address. Separation logic's power comes from making an aliasing claim
*unstatable* rather than *dischargeable*.

### 4. The frame rule — the point of the whole thing

```
                          { P } C { Q }
   (FRAME)      ─────────────────────────────────        (C does not modify the free variables of R)
                          { P ∗ R } C { Q ∗ R }
```

The side condition is now about *variables*, not memory, and it is discharged by the logic itself:
`C`'s footprint is exactly the part of the heap `P` describes, so the `R` part is untouched **by
construction**. You get the rule for free, and with it:

> **Local reasoning.** To verify a function, look only at the heap it is given. Everything else in
> the program — every other object, every other thread's state — composes by `∗` without any
> global analysis.

This is why separation logic is the answer to the modularity problem, and why it, rather than Hoare
logic, is the foundation of modern heap verification.

### 5. Small axioms and the "footprint" discipline

Separation logic lets you write axioms that mention **only the state the instruction actually
touches**:

```
   { emp }              x := alloc(v)     { x ↦ v }
   { x ↦ v }            y := [x]          { x ↦ v ∧ y = v }
   { x ↦ _ }            [x] := w          { x ↦ w }
   { x ↦ _ }            free(x)           { emp }
```

Compare with the frame-condition-riddled axioms of Hoare logic. These are called **small axioms**,
and the frame rule is what lets you lift a small axiom to any larger heap. Hoare's own later work on
**data refinement** and the "footprint" idea are the same intuition; separation logic made it a
logic.

### 6. What you can now prove

**A linked list** — an inductive spatial predicate:

```
   list(nil, [])      ≡  emp
   list(x, v :: vs)   ≡  x ↦ (v, y) ∗ list(y, vs)
```

Note that `list` is an ordinary inductive definition over an assertion whose second clause **splits
the heap**. Recursion in the *heap* is now expressible, which is what makes it work for
pointer data structures.

**In-place list reversal** then has a three-line spec, and its proof is a handful of frame
applications — with no aliasing case analysis anywhere. That is the empirical payoff: specs shrink
and proofs become mechanical.

**Memory safety for free.** If you can prove `{ emp } C { P }` and every assertion in the derivation
is well-formed, then `C` cannot dereference a freed cell, read unallocated memory, or leak — because
`↦` is the *only* way to talk about a cell, and it must be in the pre-state for a load to be
justified. **Memory safety is a corollary, not a separate analysis.**

### 7. Extensions, in the order they matter

| Extension | Adds | Why you need it |
|---|---|---|
| **Fractional permissions** | `x ↦{π} v` with `π ∈ (0,1]`; `↦{π₁} ∗ ↦{π₂}` only if `π₁+π₂ ≤ 1` | read sharing without giving up the frame rule |
| **Concurrent separation logic (CSL)** | locks as resources: a lock owns an invariant | the first logic where `∗` gives you thread modularity — O'Hearn 2004 |
| **Ghost state** | logical state not present in the program, connected by invariants | encode protocols, history, ownership transfer |
| **RGSep / deny-guarantee** | relies/guarantees for non-disjoint thread interference | data races and fine-grained concurrency |
| **Higher-order / impredicative** | quantify over assertions; invariants mentioning invariants | **Iris** — see [iris.md](../05-tools/iris.md) |
| **Relational** | assertions about *pairs* of programs/states | program equivalence, compiler correctness, type safety proofs |
| **Time / I/O / distribution** | resource algebras for time, protocols, network | Actris, Aneris, Perennial |

**The pattern across all of them:** separation logic is not one logic but a *skeleton* — you choose a
resource algebra, and `∗` becomes "composes according to that algebra". Fractional permissions are
the resource algebra of shares; CSL's locks are an algebra; Iris's contribution was to make that
choice a first-class parameter.

### 8. The resource reading — the idea that generalised the field

The deeper reading of `P ∗ Q`: **it is monoidal composition of resources.**

```
   ∗    is the operation of a partial commutative monoid (PCM) on "resources"
   emp  is its unit
   ↦    is the ownership of one cell
```

Once you see `∗` that way, nothing forces the resources to be heap cells. They can be:

| Resource algebra | `∗` means | Used for |
|---|---|---|
| Heap | disjoint memory | classic separation logic |
| Fractions `(0,1]` | adding shares | read-only sharing |
| `Excl` | "there is exactly one of these" | unique ownership |
| `Auth` | one authoritative owner, many fragments | ghost protocols, invariants |
| `Agree` | all fragments agree | agreement between threads |
| Monotone map `Loc → M` | per-location resources | ownership of many objects |

**This is the abstraction that turned a program logic into a framework.** It is also why
[Rust's ownership discipline](techniques.md#5-types--lightweight-static-analysis-the-free-tier) is a
*decidable fragment* of separation logic: the borrow checker enforces a resource algebra
(ownership plus shared borrows) at compile time, deciding a question that is undecidable in the full
logic.

### 9. What it costs

| Limit | Detail |
|---|---|
| **Undecidable** | entailing `P ⊢ Q` for full separation logic is undecidable; tools must restrict or search |
| **Finding invariants is still the work** | the frame rule removes aliasing case analysis, not the need for a loop invariant that is *strong enough* |
| **Ghost state is a design skill** | choosing the resource algebra and the invariant is where the real effort goes |
| **Annotation burden** | you write `↦`-assertions in every function's contract |
| **Specification gap is unchanged** | a verified heap operation can still be the wrong operation |
| **Tooling maturity varies** | Iris is a research framework; Verus/Creusot are engineering products with narrower scope |

**And the honest historical note:** separation logic is over 20 years old and it is *still* mostly a
research toolchain, with the notable exception of Rust's type system — which is the largest
deployment of its ideas by far, and doesn't use the name. See
[the adoption gap](../03-applications/adoption-gap.md).

---

## Tutorial: the frame rule, by hand

*(This section is deliberately tool-free. For a real proof assistant, see
[iris.md](../05-tools/iris.md) — the Iris proof mode is where separation logic became usable.)*

### Step 1 — State a small axiom

```
   { x ↦ v }   [x] := w   { x ↦ w }
```

Only one cell is mentioned. Nothing is said about the rest of the heap, and nothing *can* be — that
is the discipline.

### Step 2 — Frame it

Suppose `y` is a different address and we also have `y ↦ 0`. The frame rule with `R := y ↦ 0` gives:

```
   { x ↦ v ∗ y ↦ 0 }   [x] := w   { x ↦ w ∗ y ↦ 0 }
```

**Do it yourself:** which side condition did you check? *None* — you checked that `x ↦ v` and
`y ↦ 0` are *separately* satisfied, which is exactly the hypothesis of the frame rule's premise. This
is the operational meaning of local reasoning.

### Step 3 — The aliasing question, answered by arithmetic

Suppose someone asks: "what if `y = x`?" Then `x ↦ v ∗ y ↦ 0` is `x ↦ v ∗ x ↦ 0`, which requires
splitting one cell into two disjoint cells — **unsatisfiable**. The logic returns *false*, not a case
split. So a proof that goes through has already established `x ≠ y`.

**That is the trick:** aliasing questions turn into questions about whether a `∗` decomposition
exists, and the semantics answers them once and for all.

### Step 4 — A two-cell swap, with no aliasing analysis

```
   { x ↦ a ∗ y ↦ b }
       tmp := [x];         -- { x ↦ a ∗ y ↦ b ∗ tmp = a }
       [x] := [y];         -- { x ↦ b ∗ y ↦ b ∗ tmp = a }
       [y] := tmp          -- { x ↦ b ∗ y ↦ a }
   { x ↦ b ∗ y ↦ a }
```

The precondition's `∗` is what licenses reading and writing both cells: each step frames the other
cell, and no step needed to consider `x = y`. **Compare with the Hoare-logic version, which requires
an explicit `x ≠ y` side condition and a modifies-analysis to frame anything.**

### Step 5 — Write an inductive spatial predicate

```
   list(nil, [])      ≡  emp
   list(x, v :: vs)   ≡  x ↦ (v, y) ∗ list(y, vs)
```

Then prove, by induction on the list, that appending is `list`-preserving. You will find the
induction step needs exactly one frame application — and that this frame application is the *entire*
reason the proof is short. That experience is the reason separation logic won.

### Step 6 — Turn it into a locking discipline (the CSL idea)

A lock is a resource, not a boolean. Write `locked(ℓ, P)` for "the lock at `ℓ` protects invariant
`P`". Then:

```
   { locked(ℓ, P) ∗ P }   release(ℓ)   { locked(ℓ, P) }
   { locked(ℓ, P) }       acquire(ℓ)   { locked(ℓ, P) ∗ P }
```

Reading `P` out of a lock and putting it back is now a **logical** accounting of resources, and two
threads can never hold `P` at once because there is only one copy of it. That is concurrent
separation logic, and it is the step that made separation logic the foundation for concurrent
verification — and, eventually, for Iris.

---

## Reference

### Connectives

| Notation | Name | Informal reading |
|---|---|---|
| `emp` | empty heap | touches nothing |
| `x ↦ v` | points-to | one cell, at `x`, value `v` |
| `x ↦{q} v` | fractional points-to | owns share `q` |
| `P ∗ Q` | separating conjunction | disjoint heaps |
| `P -∗ Q` | magic wand | give me a disjoint `P`-heap, get `Q` |
| `⌜φ⌝` | pure | no heap; mathematical fact |
| `P ∧ Q` | conjunction | same heap satisfies both |
| `□ P` / `P` persistent | persistence | duplicable; consumes nothing |
| `▷ P` | later | `P` after one step (guarded recursion, concurrency) |
| `∃ x, P` | existential | usual |
| `P ⊢ Q` | entailment | every heap satisfying `P` satisfies `Q` |

### Core rules

```
   (FRAME)      {P} C {Q}   ⟹   {P ∗ R} C {Q ∗ R}          (R mentions no modified program variable)

   (SEQ)        {P} C₁ {R},  {R} C₂ {Q}   ⟹   {P} C₁; C₂ {Q}

   (CONJ)       {P₁} C {Q₁},  {P₂} C {Q₂}  ⟹  {P₁ ∧ P₂} C {Q₁ ∧ Q₂}

   (DISJ)       {P₁} C {Q},  {P₂} C {Q}    ⟹  {P₁ ∨ P₂} C {Q}

   (EXISTS)     ∀x. {P x} C {Q x}          ⟹  {∃x. P x} C {∃x. Q x}

   (CONS)       P ⊢ P',  {P'} C {Q'},  Q' ⊢ Q   ⟹   {P} C {Q}
```

`FRAME` is the one that matters; the others are ordinary Hoare-logic rules that survive unchanged.

### Small axioms

| Instruction | Axiom |
|---|---|
| allocate | `{ emp } x := alloc(v) { x ↦ v }` |
| load | `{ x ↦ v } y := [x] { x ↦ v ∧ y = v }` |
| store | `{ x ↦ _ } [x] := w { x ↦ w }` |
| free | `{ x ↦ _ } free(x) { emp }` |
| compare-and-swap | `{ x ↦ v } CAS(x, v, w) { (x ↦ w) ∨ (x ↦ v) }` |

### Resource algebras

| Algebra | `∗` composes by | Typical use |
|---|---|---|
| Heap | disjoint union | program heap |
| Fractions | addition, bounded by 1 | read sharing |
| `Excl(A)` | only total | unique ownership |
| `Auth(M)` | one authority + fragments | ghost protocols |
| `Agree(M)` | only equal values | thread agreement |
| `Loc → M` | pointwise | ownership of collections |

### History

| Year | Event |
|---|---|
| 1967–69 | Floyd, Hoare: the aliasing problem is visible and unsolved |
| 1999–2001 | **Reynolds**, **O'Hearn**, **Yang**, **Ishtiaq**: separation logic and the frame rule |
| 2001 | *Local Reasoning about Programs that Alter Data Structures* (CSL 2001) |
| 2004 | **O'Hearn**, *Resources, Concurrency and Local Reasoning* — concurrent separation logic |
| 2005– | **Bornat, Calcagno, O'Hearn, Parkinson**: tooling, permissions, verification of real C |
| 2007 | **Calcagno et al.**, *Local Action and Abstract Separation Logic* — the abstract algebra view |
| 2009 | **Vafeiadis & Parkinson**, RGSep; **Feng**: rely-guarantee meets separation |
| 2015 | **Jung et al.**, Iris — separation logic as a framework ([iris.md](../05-tools/iris.md)) |
| 2018 | **RustBelt** — Rust's safety proved in Iris |
| 2018 | Rust 1.0's borrow checker is the largest deployment of separation-logic ideas, unnamed |
| 2025 | **Turing Award** to Reynolds, O'Hearn and Yang — ⚠️ *verify the exact citation before quoting* |

### Tools

| Tool | Approach |
|---|---|
| **Iris** (Rocq) | the general framework — [iris.md](../05-tools/iris.md) |
| **iris-lean** (Lean 4) | the Lean port — [iris.md](../05-tools/iris.md#iris-lean) |
| **Verus**, **Creusot**, **Prusti** | Rust verification; separation-logic-inspired, SMT-backed |
| **Viper** | intermediate verification language with permissions |
| **VeriFast**, **jStar**, **SpaceInvader** | older separation-logic tools for C/Java |
| **RefinedC**, **RefinedRust** | refinement types + separation logic |
| **Quiver** | abductive *inference* of separation logic specs (PLDI 2024) |
| **Rust's borrow checker** | the decidable fragment, in production |

---

## References

- **Reynolds, J.C.** *Intuitionistic Reasoning about Shared Mutable Data Structure.* Millennial
  Perspectives in Computer Science, 2000 — the origin of separating conjunction.
- **O'Hearn, P., Reynolds, J., Yang, H.** *Local Reasoning about Programs that Alter Data
  Structures.* CSL 2001. [PDF](https://link.springer.com/chapter/10.1007/3-540-44802-0_1) —
  the frame rule and small axioms.
- **Ishtiaq, S. & O'Hearn, P.** *BI as an Assertion Language for Mutable Data Structures.* POPL 2001.
  [PDF](https://dl.acm.org/doi/10.1145/360204.375159) — BI, the logic in which `∗` lives.
- **Reynolds, J.C.** *Separation Logic: A Logic for Shared Mutable Data Structures.* LICS 2002.
  [PDF](https://www.cs.cmu.edu/~jcr/seplogic.pdf) — the canonical reference.
- **O'Hearn, P.** *Resources, Concurrency and Local Reasoning.* CONCUR 2004.
  [PDF](http://www0.cs.ucl.ac.uk/staff/p.ohearn/papers/concur04.pdf) — concurrent separation logic.
- **Bornat, R., Calcagno, C., O'Hearn, P., Parkinson, M.** *Permission Accounting in Separation
  Logic.* POPL 2005 — fractional permissions.
- **Calcagno, C., O'Hearn, P., Yang, H.** *Local Action and Abstract Separation Logic.* LICS 2007 —
  the abstract/algebraic view of `∗`.
- **Vafeiadis, V. & Parkinson, M.** *A Marriage of Rely/Guarantee and Separation Logic.* CONCUR
  2007 — RGSep.
- **Brookes, S.** *A Semantics for Concurrent Separation Logic.* CONCUR 2004, and the tutorial
  [PDF](https://www.cs.cmu.edu/~brookes/concur2004tutorialpaper.pdf).
- **Jung, R., Krebbers, R., Birkedal, L., Dreyer, D.** *Higher-Order Ghost State.* ICFP 2016.
- **Jung, R. et al.** *Iris: Monoids and Invariants as an Orthogonal Basis for Concurrent Reasoning.*
  POPL 2015. [PDF](https://iris-project.org/pdfs/2015-popl-iris1-final.pdf)
- **Jung, R., Krebbers, R., Jourdan, J.-H., Bizjak, A., Birkedal, L., Dreyer, D.** *Iris from the
  Ground Up: A Modular Foundation for Higher-Order Concurrent Separation Logic.* JFP 2018.
  [PDF](https://www.mpi-sws.org/~dreyer/papers/iris-ground-up/paper.pdf)
- **Krebbers, R. et al.** *MoSeL: A General, Extensible Modal Framework for Interactive Proofs in
  Separation Logic.* ICFP 2018. [PDF](https://people.mpi-sws.org/~jung/mosel.pdf) — the proof mode.
- **Jung, R., Jourdan, J.-H., Krebbers, R., Dreyer, D.** *RustBelt: Securing the Foundations of the
  Rust Programming Language.* POPL 2018.
  [PDF](https://plv.mpi-sws.org/rustbelt/popl18/paper.pdf)
- **Jung, R.** *Understanding and Evolving the Rust Programming Language.* PhD thesis, 2020.
  [PDF](https://research.ralfj.de/thesis/) — the best long-form account of separation logic in practice.
- **Sammler, M. et al.** *RefinedRust* (PLDI 2024) and *Islaris* (PLDI 2022) — Rust and machine-code
  verification in Iris.
- **Spies, S. et al.** *Quiver: Guided Abductive Inference of Separation Logic Specifications.*
  PLDI 2024 — Distinguished Artifact Award.
- [Wikipedia: Separation logic](https://en.wikipedia.org/wiki/Separation_logic)
- **Turing Award 2025** ⚠️ — reported for Reynolds, O'Hearn and Yang; verify the citation before
  relying on it.

## Further reading

- [iris.md](../05-tools/iris.md) — the framework that generalised separation logic, and its Lean port.
- [logics.md](logics.md#2-separation-logic--reasoning-about-memory) — the connectives in their
  logical context.
- [techniques.md](techniques.md#5-types--lightweight-static-analysis-the-free-tier) — Rust's borrow
  checker as the decidable fragment.
- [limits.md](limits.md) — the specification gap, which separation logic does not close.
