# Semantics: how languages get meaning

> **TL;DR.** You cannot verify a program without a definition of what the program *means*. That
> definition is a **semantics**, and it is the specification a verifier reasons against.
> Everything in this wiki — Hoare logic, model checking, compiler correctness, the EVM — sits on
> top of one. Choosing between small-step, big-step, functional, relational, denotational, and
> axiomatic styles is not pedantry: the choice determines which properties you can even *state*,
> whether your semantics is executable, and whether you can prove anything about it.

---

## Theory

### 1. What a semantics is for

Four jobs, and they pull in different directions:

| Job | Why it matters | Favours |
|---|---|---|
| **Define** what programs mean, unambiguously | removes the ambiguity that prose specs and reference manuals have | operational |
| **Execute** — run the definition on real programs | lets you test a language against its own spec (conformance testing) | big-step / functional |
| **Reason** — support proofs about programs | needed by verifiers, compilers, optimisers | axiomatic, denotational, relational |
| **Mechanize** — be checked by a proof assistant | removes doubt about the theory itself | all, but some styles fight you |

The last row is the modern twist. Writing a semantics in Lean, Rocq, Isabelle, or Coq turns the
language definition itself into a verified artifact — and makes *everything else* verifiable
relative to it.

### 2. The four classical styles

| Style | Meaning is… | Origin | Best at | Weak at |
|---|---|---|---|---|
| **Operational** | a transition relation/function on machine states | Plotkin, Kahn; abstract machines: Landin's SECD (1964) | defining real languages; executability; intuitive | proofs of program properties are indirect |
| **Denotational** | a mathematical object (a function on domains) | Scott & Strachey (1971) | **compositionality**; reasoning about program equivalence | domains are hard; scale poorly to messy languages |
| **Axiomatic** | a set of proof rules about programs | Floyd (1967), Hoare (1969), Dijkstra (1975) | mechanical verification; what you actually use daily | only as good as the assertions; no model of execution |
| **Algebraic / type-theoretic** | behaviour up to an equivalence, or typed terms | Milner; Curry–Howard | concurrency (process calculi); proofs-as-programs | not a from-scratch definition of a real language |

See [logics.md](logics.md) for the axiomatic and type-theoretic styles as *logics*; this page is
about *definition methods*, which is a different axis.

### 3. Small-step vs big-step

The distinction practitioners actually argue about. Take a tiny imperative language, **IMP**:

```
a ::= n | x | a₁ + a₂ | a₁ − a₂
b ::= true | false | a₁ < a₂ | ¬b | b₁ ∧ b₂
c ::= skip | x := a | c₁ ; c₂ | if b then c₁ else c₂ | while b do c
```

State is a partial map `σ : Var ⇀ ℤ`. `⟨c, σ⟩ → ⟨c', σ'⟩` is a small-step transition;
`⟨c, σ⟩ ⇓ σ'` is a big-step relation.

#### Small-step (structural operational semantics, SOS)

**One step at a time.** Rules decompose the syntax, and the *last* step of a computation matters:

```
                     ⟨a, σ⟩ → ⟨a', σ'⟩
  ─────────────      ────────────────────        (sequencing: left first)
  ⟨skip, σ⟩ → σ      ⟨x := a, σ⟩ → ⟨x := a', σ⟩

  ⟨x := n, σ⟩ → σ[x ↦ n]

  ⟨c₁, σ⟩ → ⟨c₁', σ'⟩                   ⟨c₁, σ⟩ → σ'
  ──────────────────────────            ─────────────────      (sequencing: then right)
  ⟨c₁ ; c₂, σ⟩ → ⟨c₁' ; c₂, σ'⟩         ⟨c₁ ; c₂, σ⟩ → ⟨c₂, σ'⟩

                          ⟨b, σ⟩ → true      ⟨c, σ⟩ → ⟨c', σ'⟩
  ────────────────────    ──────────────────────────────────────────   (if-true)
  ⟨while b do c, σ⟩ → σ   ⟨if b then c₁ else c₂, σ⟩ → ⟨c₁', σ'⟩

  ⟨b, σ⟩ → true    ⟨while b do c, σ⟩ → σ''
  ────────────────────────────────────────                            (while)
  ⟨while b do c, σ⟩ → ⟨c ; while b do c, σ⟩
```

**What you get:** a notion of *intermediate state*. Sequencing, concurrency, interleaving,
exceptions, and *"does this program leak a secret on step 7"* are all naturally expressible.
Violations of safety properties are witnessed by finite traces — which is exactly why model
checking and runtime monitoring are built on small-step notions.

**What it costs:** proofs about whole computations require induction over a transitive closure, and
you must handle the whole reduction sequence. It is the least convenient style for "the function
returns `n`" statements.

#### Big-step (natural semantics)

**Whole computation in one judgement.** The relation relates a program and initial state directly
to a final state:

```
  ⟨a, σ⟩ ⇓ n
  ─────────────────

  ⟨skip, σ⟩ ⇓ σ

  ⟨a, σ⟩ ⇓ n                              ⟨c₁, σ⟩ ⇓ σ'    ⟨c₂, σ'⟩ ⇓ σ''
  ────────────────                        ──────────────────────────────────────
  ⟨x := a, σ⟩ ⇓ σ[x ↦ n]                  ⟨c₁ ; c₂, σ⟩ ⇓ σ''
```

**What you get:** *induction over derivations* is the natural proof principle, so big-step is much
friendlier for proving "this program computes this function" and for compiler-correctness diagrams
(compile both sides, apply the induction hypothesis).

**What it costs, and this is the decisive limitation:** big-step **cannot distinguish
non-termination from divergence-by-stuckness**, and it cannot express properties of intermediate
states. Concurrency and interleaving semantics are essentially impossible to state. If your program
might loop forever, big-step simply has no derivation — which sounds fine until you need to prove
something *about* the absence of a derivation.

#### The practical trade, and the modern answer

| | Small-step | Big-step |
|---|---|---|
| Intermediate states | ✅ | ❌ |
| Concurrency / interleaving | ✅ | ❌ (effectively) |
| Proofs about whole runs | awkward | ✅ natural |
| Executable as an interpreter | needs a driving loop | ✅ directly |
| Handles non-termination | as an infinite derivation | no derivation at all |

**The modern answer is to have both, and prove them equivalent.**

### 4. Functional vs relational semantics ← the distinction that matters most in practice

Most textbook treatments present operational semantics as a *relation*. Most *implementations* of
operational semantics are *functions*. This gap causes real problems, and it is the reason
**functional big-step semantics** exists.

#### Relational

`⟨c, σ⟩ ⇓ σ'` is a relation. Nothing forces it to be deterministic or total:

- **Nondeterministic** languages (concurrency, `choose`, `any`, unspecified evaluation order,
  undefined behaviour, hardware races) are naturally relational: two different results can both be
  derivable. You *cannot* express this as a function without an extra mechanism.
- **Non-termination** is "no related `σ'`", which is a statement about the relation, not a value.

Relational semantics is what you want for: nondeterminism, concurrency, compiler correctness under
undefined behaviour, and any language where you want to prove things about *all* permitted
behaviours.

#### Functional

`exec : Stmt → State → State` is a function. The upside is enormous in practice:

- It **executes**. It is an interpreter, so you can run the official conformance test suite against
  the semantics — which is how anyone actually gains confidence in a real language definition
  ([the EVM conformance story](../03-applications/blockchain.md) is exactly this).
- It supports **executable specification** and differential testing against a real implementation.
- Proofs are often easier: no derivation trees, just equational reasoning.

The cost: a function must be **deterministic and total**. Two standard fixes:

1. **Fuel / clock.** `exec : ℕ → Stmt → State → Option State`, where the first argument is a step
   budget. Running out of fuel is `none`. This is how you make a total function out of a partial
   one, and it introduces a proof obligation you must then discharge: *the semantics is
   fuel-invariant* — if `exec n c σ = some σ'` and `m ≥ n`, then `exec m c σ = some σ'`. The
   EVM/Yul model in Lean does exactly this with an explicit `OutOfFuel` state constructor.
2. **Nondeterminism as an input.** `exec : Choice → Stmt → State → State` where `Choice` supplies
   the oracle decisions. Relational nondeterminism becomes *universally quantified over an input* —
   you prove a property for all `Choice`. This is often the cleanest bridge between the two styles.

#### Functional big-step semantics (FBSS)

Named and popularised by Owens, Myreen, Kumar, and Tan (*Functional Big-Step Semantics*, ESOP
2016), this is the style used for **CakeML** and for much of the mechanised-EVM work. The recipe:

```
exec : ℕ → Stmt → State → State        -- fuel, usually called the "clock"
```

with a clock that **decrements on every rule application**, an error state for exhaustion, and
(oracle) inputs to model nondeterministic choices. You then prove:

- **determinism** — trivially, because it is a function;
- **clock monotonicity** — more fuel never changes an answer that already succeeded;
- **equivalence with a relational or small-step specification** — this is the theorem that buys back
  the generality you gave up.

**Why practitioners like it:** you get an *executable* semantics that you can test against real
programs, plus a proof style that scales, plus a total function that Lean/Rocq/Isabelle accept
without termination gymnastics. The price is the clock and the equivalence theorem — and in
practice that is a very good trade.

**Rule of thumb**

> If you need to state something about *all permitted behaviours* of a language with
> nondeterminism or concurrency, start **relational**. If you need to *run* the semantics against a
> conformance suite, start **functional**. Do both, and prove them equivalent — that equivalence
> theorem is one of the most valuable artifacts you can produce about a language.

### 5. Denotational semantics, briefly

Meaning as a mathematical object: `⟦c⟧ : Σ → Σ` for a deterministic IMP, or a domain of partial
functions when recursion is involved. `while` requires a **least fixed point** over a
complete partial order (Kleene's theorem; Scott domains). The payoff is **compositionality**:
`⟦c₁ ; c₂⟧ = ⟦c₂⟧ ∘ ⟦c₁⟧`, so meaning is built from the meaning of parts.

Why it still matters: compositionality is the property that makes a semantics *scale* to reasoning
about program equivalence, and denotational notions underlie how compilers justify their
transformations. Why it is less common than it used to be: real languages (concurrency, undefined
behaviour, C) resist clean denotations, and mechanising domain theory is heavy.

### 6. Mechanising a semantics: what changes

Writing the semantics in a proof assistant changes the engineering:

| Problem you inherit | Where it bites | Standard mitigations |
|---|---|---|
| **Binding and alpha-equivalence** | `let`, functions, capture-avoiding substitution | locally nameless (Aydemir et al., POPL 2008), de Bruijn indices, Ott, Lem |
| **Termination** | recursive interpreter over unbounded syntax | fuel/clock; well-founded recursion; domain measures |
| **Nondeterminism** | relations cannot be "run" | oracle inputs, or a `Set`/`Prop`-valued result |
| **Executability** | `Prop`-valued relations don't compute | `Bool`-valued executable core plus a soundness theorem |
| **Extraction to run tests** | proof assistant code is slow | Lean/Rocq extraction, FFI for hot spots (precompiles, crypto) |

### 7. What a semantics buys you downstream

```
      semantics  ──────────────►  conformance testing (run it against the official suite)
          │
          ├────────────────────►  verifier soundness (your Hoare logic is proved against it)
          ├────────────────────►  compiler correctness (semantic preservation = a theorem about it)
          ├────────────────────►  optimiser justification (transformations proved to preserve it)
          └────────────────────►  client implementation guidance (a reference for what "correct" is)
```

This is not hypothetical. The EVM's Lean semantics is explicitly positioned as the foundation for
all four of those uses — verifying contracts, verifying execution clients, and verifying zkVMs
(see [blockchain.md § Layer 1](../03-applications/blockchain.md)).

---

## Tutorial

### Step 1 — Write the syntax and the state

```lean
inductive Aexp : Type where
  | num  : Int → Aexp
  | var  : String → Aexp
  | plus : Aexp → Aexp → Aexp

inductive Bexp : Type where
  | tt | ff
  | less : Aexp → Aexp → Bexp
  | not  : Bexp → Bexp
  | and  : Bexp → Bexp → Bexp

inductive Stmt : Type where
  | skip   : Stmt
  | assign : String → Aexp → Stmt
  | seq    : Stmt → Stmt → Stmt
  | ite    : Bexp → Stmt → Stmt → Stmt
  | while  : Bexp → Stmt → Stmt

abbrev State := String → Int   -- total map: keeps the rules simple
```

Making the state a *total* function rather than a partial map removes a huge amount of case analysis
from every rule. You can refine to a partial map later; start total.

### Step 2 — Write the small-step relation

```lean
inductive Step : Stmt × State → Stmt × State → Prop where
  | seqStep  : Step (c₁, σ) (c₁', σ') → Step (Stmt.seq c₁ c₂, σ) (Stmt.seq c₁' c₂, σ')
  | seqDone  : Step (Stmt.seq Stmt.skip c₂, σ) (c₂, σ)
  | assign   : Step (Stmt.assign x a, σ) (Stmt.skip, fun y => if y = x then evalA a σ else σ y)
  | ifTrue   : evalB b σ = true  → Step (Stmt.ite b c₁ c₂, σ) (c₁, σ)
  | ifFalse  : evalB b σ = false → Step (Stmt.ite b c₁ c₂, σ) (c₂, σ)
  | whileTrue  : evalB b σ = true  → Step (Stmt.while b c, σ) (Stmt.seq c (Stmt.while b c), σ)
  | whileFalse : evalB b σ = false → Step (Stmt.while b c, σ) (Stmt.skip, σ)
```

Note the shape: the relation is **structural** — each rule decomposes the syntax a little. That is
what "structural" in structural operational semantics means.

### Step 3 — Prove determinism

For small-step semantics, determinism is a real theorem, and proving it is the standard first
exercise:

```lean
theorem step_deterministic (h₁ : Step s t₁) (h₂ : Step s t₂) : t₁ = t₂ := by
  induction h₁ generalizes t₂ with
  | seqStep _ ih => cases h₂ <;> simp_all
  | seqDone     => cases h₂
  | assign      => cases h₂; rfl
  | ifTrue h    => cases h₂ <;> simp_all [h]
  | ifFalse h   => cases h₂ <;> simp_all [h]
  | whileTrue _ => cases h₂ <;> simp_all
  | whileFalse h => cases h₂ <;> simp_all [h]
```

The proof is mechanical but not free — and in a language with concurrency it would be **false**.
That is the point: determinism is a *theorem about your language*, not a given.

### Step 4 — Write the functional big-step version

```lean
def exec : Nat → Stmt → State → Option State
  | 0,     _,  _ => none                 -- out of fuel
  | _+1, Stmt.skip, σ => some σ
  | n+1, Stmt.assign x a, σ => some (fun y => if y = x then evalA a σ else σ y)
  | n+1, Stmt.seq c₁ c₂, σ =>
      match exec n c₁ σ with
      | none   => none
      | some σ' => exec n c₂ σ'
  | n+1, Stmt.ite b c₁ c₂, σ =>
      exec n (if evalB b σ then c₁ else c₂) σ
  | n+1, Stmt.while b c, σ =>
      if evalB b σ then
        match exec n c σ with
        | none => none
        | some σ' => exec n (Stmt.while b c) σ'
      else some σ
```

This is an interpreter. It extracts, it runs, it can be tested against a reference implementation.
It is also total, so Lean accepts it without a termination proof.

### Step 5 — State and prove the property you now owe

Fuel introduced a silent bug class: a program can fail with `none` because it *needs more fuel*, not
because it is undefined. You must prove monotonicity:

```lean
theorem exec_mono (h : exec n c σ = some σ') : ∀ m, n ≤ m → exec m c σ = some σ' := by
  induction n, c, σ using exec.induct generalizes σ' with
  | _ => sorry  -- structurally: more fuel never loses a completed run
```

Two further obligations worth proving, and each is a small research project in its own right:

1. **Agreement with small-step**: `exec n c σ = some σ'` iff `⟨c,σ⟩ →* ⟨skip,σ'⟩` within `n` steps.
2. **Determinism of the language**: `exec` is a function, so this is free — which is a nice
   argument for FBSS when the language *is* deterministic.

### Step 6 — Add nondeterminism and watch the style change

Add `choose : Stmt` that may set a variable to any value. In the functional style you thread an
oracle; in the relational style you simply write two rules:

```
  ─────────────────────────────   (any value)
  ⟨choose x, σ⟩ ⇓ σ[x ↦ any]
```

Now `step_deterministic` is **false**, and the property you actually want is different: not "there is
one result" but "*every* derivable result is safe". This is the moment where relational semantics
stops being academic — a `Bool`-valued interpreter cannot even state the property.

**Exercise.** Take your `exec` and re-state it over `Set State` instead of `Option State`. Compare
the two definitions of "the loop terminates". That comparison is the whole small-step/big-step and
functional/relational debate in miniature.

---

## Reference

### Styles at a glance

| Style | Judgement / object | Nondeterminism | Executable | Good for |
|---|---|---|---|---|
| Small-step (SOS) | `⟨c,σ⟩ → ⟨c',σ'⟩` | natural | needs a driver | concurrency, intermediate states, safety traces |
| Big-step (natural) | `⟨c,σ⟩ ⇓ σ'` | natural | natural | whole-run reasoning, compiler correctness |
| Functional big-step | `exec : ℕ → c → σ → σ` | via oracle input | ✅ directly | executable specs, conformance testing, mechanisation |
| Denotational | `⟦c⟧ : D → D` | needs powerdomains | not usually | compositionality, program equivalence |
| Axiomatic | `{P} c {Q}` | natural | n/a | mechanical verification |
| Reduction / evaluation contexts | `E[c]` + context rules | natural | with a driver | minimal syntax-directed rules |
| Abstract machine | state of a fictitious machine | natural | ✅ | efficient execution, garbage/stack modelling |
| Process calculus / LTS | `P → P'` | inherent | partially | concurrency, bisimulation, equivalence |

### Terminology to keep straight

- **Structural** = the rules are driven by the syntax (SOS). Not to be confused with "small-step";
  there are structural big-step semantics too.
- **Natural semantics** = Kahn's name for big-step.
- **Reduction semantics** = small-step with an explicit notion of *evaluation context*, so that the
  rules only need to mention the redex, not the surrounding program.
- **Fuel / clock** = the step budget that makes a partial interpreter total.
- **Determinism** = every state has at most one successor. A theorem for small-step; a definitional
  fact for functional.
- **Totality** = every state has at least one successor (progress). Part of a type-safety proof.
- **Progress + preservation** = the standard syntactic type-safety formulation: well-typed programs
  don't get stuck and stay well-typed (Wright & Felleisen).
- **Full abstraction** = the denotational equivalence coincides with the operational one.
- **Bisimulation** = the coinductive proof technique for process equivalences.
- **Conformance testing** = running an executable semantics against an official test suite. The
  strongest practical evidence that a mechanised semantics matches reality.

### Tools for writing and mechanising semantics

| Tool | Role |
|---|---|
| **Lean 4 / Rocq / Isabelle / Coq** | full mechanisation; the modern default |
| **PLT Redex** | lightweight reduction-semantics engineering with random testing and debugger |
| **Ott** | generates definitions and proof boilerplate for Lean/Rocq/Isabelle from a concise spec |
| **Lem** | lightweight semantics in a language that extracts to Rocq/Isabelle/HOL/OCaml |
| **K framework** | executable semantics from rewriting rules; KEVM is the flagship |
| **Sail** | ISA semantics; official ARM and RISC-V specifications are written in it |
| **Maude / rewriting logic** | executable rewriting semantics |
| **Coq/Rocq's `Function`/`Equations`, Lean's `termination_by`** | making recursive interpreters total without fuel |

### Further reading

Start with **Winskel** for the classical theory in one book, and **Nielson & Nielson** for a
gentler tour with proofs. **Harper's PFPL** is the reference for the type-theoretic view. For the
practical, mechanisation-first approach, the **functional big-step** paper is the most valuable
single read, and the **EVMYulLean** repository is the best worked example of a real, industrial
language semantics in Lean.

---

## References

- **Plotkin, G.** *A Structural Approach to Operational Semantics.* Aarhus DAIMI FN-19, 1981;
  reprinted in *Journal of Logic and Algebraic Programming* 60–61, 2004.
  [Reprint](https://www.sciencedirect.com/science/article/pii/S1567832604000268) — the origin of SOS.
- **Kahn, G.** *Natural Semantics.* STACS 1987.
  [Springer](https://link.springer.com/chapter/10.1007/BFb0039592) — the origin of big-step semantics.
- **Scott, D. & Strachey, C.** *Toward a Mathematical Semantics for Computer Languages.* 1971 — the
  origin of denotational semantics.
- **Landin, P.** *The Mechanical Evaluation of Expressions.* 1964 — the SECD machine, and the first
  abstract machine semantics.
- **Hoare, C.A.R.** *An Axiomatic Basis for Computer Programming.* CACM 1969. See [logics.md](logics.md).
- **Wright, A. & Felleisen, M.** *A Syntactic Approach to Type Soundness.* Information and
  Computation, 1994 — progress and preservation.
- **Owens, S., Myreen, M., Kumar, R., Tan, Y.K.** *Functional Big-Step Semantics.* ESOP 2016.
  [PDF](https://www.cl.cam.ac.uk/~mom22/papers/functional-big-step.pdf) — **the key reference for the
  functional style**, used for CakeML.
- **Aydemir, B., Charguéraud, A., Pierce, B., Pollack, R., Weirich, S.** *Engineering Formal
  Metatheory.* POPL 2008. [PDF](https://www.cis.upenn.edu/~bcpierce/papers/nominals.pdf) — locally
  nameless representation, the binding problem.
- **Sewell, P., Nardelli, F., Owens, S., et al.** *Ott: Effective Tool Support for the Working
  Semanticist.* ICFP 2007. [Ott](https://www.cl.cam.ac.uk/~pes20/ott/)
- **Roşu, G. & Şerbănuţă, T.** *An Overview of the K Semantic Framework.* JLAP 2010.
  [K framework](https://kframework.org/)
- **Armstrong, A., Bauereiss, T., Campbell, B., Reid, A., Gray, K., Norton-Wright, R., Sewell, P.,
  et al.** *ISA Semantics for ARMv8-A, RISC-V, and CHERI-MIPS.* POPL 2019.
  [Sail](https://github.com/rems-project/sail)
- **Felleisen, M., Findler, R., Flatt, M.** *Semantics Engineering with PLT Redex.* MIT Press, 2009.
  [PLT Redex](https://redex.racket-lang.org/)
- **Winskel, G.** *The Formal Semantics of Programming Languages: An Introduction.* MIT Press, 1993.
- **Nielson, H.R. & Nielson, F.** *Semantics with Applications: A Formal Introduction.*
  [Free online](https://www2.imm.dtu.dk/~hrni/SWA/)
- **Harper, R.** *Practical Foundations for Programming Languages.* 2nd ed., CUP 2016.
  [Online](https://www.cs.cmu.edu/~rwh/pfpl/)
- **Pierce, B.** *Types and Programming Languages.* MIT Press, 2002 — see [bibliography.md](../references/bibliography.md).
- **Nethermind Research.** *How We Formalized Ethereum Execution: A Trustworthy Semantics of the EVM
  and Yul in Lean for Cancun.* [Blog](https://www.nethermind.io/blog/a-trustworthy-formal-model-of-evm-yul-in-lean) ·
  [EVMYulLean](https://github.com/NethermindEth/EVMYulLean) — a fully worked, industrial example of
  everything on this page: functional style, explicit fuel, Yellow Paper alignment, conformance
  testing, and stated limitations.
- [Wikipedia: Operational semantics](https://en.wikipedia.org/wiki/Operational_semantics)
- [Historical notes on operational semantics](https://dvanhorn.github.io/verified-compiler-notes/Basics-of-Operational-Semantics/Historical-Notes/)
  (David Van Horn, verified-compiler notes)

## Further reading

- [techniques.md](techniques.md) — how these semantics get *used* by the five verification families.
- [logics.md](logics.md) — the logics that a semantics makes meaningful.
- [blockchain.md](../03-applications/blockchain.md) — a real language semantics (EVM/Yul) in
  production use.
- [limits.md](limits.md) — why the trusted base matters, including when the semantics itself is
  part of it.
