# Iris (and iris-lean)

> **TL;DR.** Iris is a **framework** for higher-order concurrent separation logic, not a single
> program logic. Its premise is a one-liner: *monoids and invariants are all you need.* You choose a
> **resource algebra** for your notion of ownership, and Iris supplies the machinery — invariants,
> ghost state, the later modality, weakest preconditions — so you can reason about concurrency,
> Rust's type system, program equivalence, and distributed protocols with the same logic. It is
> implemented in **Rocq/Coq**, and a Lean 4 port, **iris-lean**, is in `leanprover-community`.

---

## The idea: monoids and invariants

Iris's POPL 2015 abstract states its thesis directly:

> "Partial commutative monoids enable us to express — and invariants enable us to enforce —
> user-defined protocols on shared state."

Two primitives, deliberately orthogonal:

| Primitive | What it gives you |
|---|---|
| **Monoids** (resource algebras) | a *language* for saying what ownership means: heaps, fractions, tokens, protocols, agreement, monotone maps |
| **Invariants** | a *mechanism* for sharing those resources between threads, without knowing in advance what the resources are |

And the crucial design decision: **these compose without stratification**. Because invariants can
mention invariants, and resources can be built from resources, you get higher-order concurrency
(threads, locks, session types, distributed protocols) without a tower of separate logics.

**Contrast with what came before.** In pre-Iris concurrent separation logic, adding a new feature
(a new kind of sharing, or a new kind of resource) meant extending the logic and re-proving its
soundness. In Iris you *instance* a resource algebra, and the framework's metatheory covers you.

---

## The base logic

Iris's logic (`IProp`) is a **bunched implication logic** (BI) extended with modality, and it is
defined by a **step-indexed** model:

```
   IProp  ≅  UPred  ≡  Nat → (Heap × Monoid) → Prop        -- deeply simplified
```

Every assertion is indexed by a number of *steps*, which is what makes the logic sound for
recursive definitions (including recursive invariants) in a domain with unbounded computation.

| Construct | Notation | Reading |
|---|---|---|
| separating conjunction | `P ∗ Q` | disjoint resources — [separation-logic.md](../01-fundamentals/separation-logic.md) |
| magic wand | `P -∗ Q` | resource-consuming implication |
| **later** | `▷ P` | "`P` holds after one more step" — the guard that makes recursion sound |
| **Löb induction** | `(▷ P → P) → P` | proves `P` even when `P` mentions its own recursion — the reason recursive invariants work |
| **invariant** | `inv N P` | `P` holds always, and is owned by nobody |
| **fancy update** | `\|={E1,E2}=>` | a ghost-state transition between masks, and the primitive for opening invariants |
| **persistence** | `□ P` | duplicable, consumable-none |
| **plainly** | `■ P` | true in the empty-resource world |
| **weakest precondition** | `WP e {Φ}` | a *monadic* program logic inside the logic |

**`▷` and Löb induction are the technical heart of Iris**, and worth understanding as a design idea
even if you never use Iris: they are how the framework avoids *stratifying* the logic (a hierarchy of
"invariants about invariants about …"). The cost is that every recursive fact needs a `▷` guard and
every proof of one needs `iNext` or `iLöb`; the benefit is that you can write the invariants you
actually want.

**The `WP` monad is the other striking design choice:** programs are not embedded as a syntactic
construct in the logic. `WP` is defined once, generically, over any language satisfying a small
interface (`Language`), and `▷` appears in its definition:

```
   WP e {Φ}  ≅  ... ▷ (WP e' {Φ}) ...        -- guarded recursion, uniformly for all languages
```

That is what makes Iris a *framework*: adding a new language (Rust, Wasm, assembly, a distributed
system) means instantiating `Language`, not extending the logic.

### Ghost state: the resource algebras

| Algebra | `∗` composes by | Used for |
|---|---|---|
| `auth(M)` | one authoritative element + fragments | the workhorse: "one owner of the truth, many partial views" |
| `frac` | addition bounded by 1 | read-only sharing |
| `excl(A)` | total only | unique ownership / tokens |
| `agree(M)` | only equal values | threads agreeing on a value |
| `gmap(K, M)` | pointwise | per-location resources |
| `mono_nat`, `mono_list` | monotone growth | counters, append-only logs |

**`auth` is the one to learn first.** The pattern is: you keep an authoritative element describing the
*global* state of some protocol, and hand out fragments describing *local* knowledge. A thread
holding a fragment can only do what the algebra permits, and the invariant ties fragments back to the
authority. Almost every interesting Iris proof uses it.

### Invariants and masks

```
   inv N P      -- an invariant named N, asserting P, owned by nobody
```

To *use* an invariant you must temporarily own it, which requires the thread to be **atomic** — that
is why `WP` carries the atomicity side condition and why fancy updates `\|={E1,E2}=>` carry *masks*
`E1`, `E2` (sets of invariant names you are allowed to open). The bookkeeping is the price of
higher-order concurrency; the payoff is that invariant-opening is a *logical* operation rather than a
side condition on the proof rules.

---

## The proof mode (MoSeL)

Iris's usability breakthrough was **MoSeL** (*A General, Extensible Modal Framework for Interactive
Proofs in Separation Logic*, ICFP 2018): a set of Rocq tactics that let you manipulate separation-logic
judgements with named hypotheses.

*(Illustrative — Iris syntax from the official documentation. See the
[Iris lecture notes](https://gitlab.mpi-sws.org/iris/iris/-/tree/master/docs/lectures) for
authoritative, checkable examples.)*

```coq
Lemma wp_counter_inc (γ : gname) (l : loc) (n : Z) :
  {{{ l ↦ #n ∗ counter γ n }}} incr #l {{{ RET #(); counter γ (n+1) }}}.
Proof.
  iIntros (Φ) "[Hl Hc] HΦ".        (* introduce and destruct the precondition *)
  wp_load.                          (* symbolic execution of the load *)
  iMod (counter_inc γ n with "Hc") as "[Hc Htok]".   (* ghost update *)
  wp_store.
  iModIntro. iApply "HΦ". iFrame.
Qed.
```

| Tactic | Purpose |
|---|---|
| `iIntros` | introduce hypotheses / destruct the precondition |
| `iDestruct` | split a `∗`, decompose an existential, introduce an invariant |
| `iFrame` | discharge parts of the goal automatically ("frame" hypotheses away) |
| `iApply` | apply a lemma to the goal |
| `iMod` | perform a ghost update / use an invariant |
| `iInv` | open an invariant (must be closed again before the atomic step) |
| `iNext` | discharge a `▷`, or push it inward |
| `iLöb` | Löb induction, for recursive invariants |
| `iExists` / `iSplit` / `iSplitL` / `iSplitR` | introduce existentials, split conjunctions choosing which side gets the resources |
| `iAssert` | assert an intermediate assertion with its own resource accounting |
| `iPureIntro` | turn a `⌜φ⌝` into a Coq goal |
| `wp_load`, `wp_store`, `wp_alloc`, `wp_op`, `wp_if`, `wp_pure` | **symbolic execution** of the program |

**`iFrame` is the tactic that sells the tool.** In separation logic you must account for every
resource explicitly, so proofs would drown in bookkeeping; `iFrame` discharges "these hypotheses
exactly cover this part of the goal" automatically. It is the analogue of `simp` for resource
accounting, and it is why Iris proofs are readable.

**And note `wp_*` tactics: Iris does not just prove Hoare triples, it *symbolically executes* the
program.** That is what makes the workflow feel like a debugger rather than a proof.

---

## HeapLang and the ecosystem

Iris ships **HeapLang**, a small ML-like language with a heap, concurrency, and locks, used for
examples and as the target for logical-relations work. iris-lean ships the same, with a library of
verified concurrent data structures (see below).

What has actually been built on Iris, which is the best evidence of what "framework" means here:

| Project | What it did |
|---|---|
| **RustBelt** (POPL 2018) | the first machine-checked *safety* proof for Rust — including `unsafe` libraries |
| **RustBelt meets relaxed memory** (POPL 2020) | Rust under weak memory |
| **RefinedRust** (PLDI 2024) | a type system for high-assurance Rust verification |
| **Perennial** (SOSP 2019) | concurrent, **crash-safe** systems |
| **Aneris** (ESOP 2020) | modular reasoning about **distributed** systems |
| **Actris / Actris 2.0** (POPL 2020, LMCS 2022) | **session types** and asynchronous protocols |
| **Simuliris** (POPL 2022, Distinguished Paper) | verifying **concurrent program optimisations** |
| **Islaris** (PLDI 2022) | machine code against **authoritative ISA semantics** |
| **ReLoC** (LICS 2018) | relational reasoning for fine-grained concurrency |
| **The Future is Ours** (POPL 2020) | prophecy variables in separation logic |
| **Microkernel IPC at Meta** (CPP 2022) | industrial verification of a real microkernel |
| **Folly concurrent queue** (CPP 2022) | a fine-grained queue from Meta's Folly library |
| **Step-indexed logical relations in Iris** (ICFP 2020) | using Iris *as* the logic for logical relations |
| **Quiver** (PLDI 2024) | **inferring** separation logic specs rather than writing them |

Read that list as a catalogue of *what a general separation logic can be used for*: type systems,
compilers, ISA semantics, distributed systems, session types, and program equivalence. That breadth
is Iris's distinguishing claim.

---

## iris-lean

A **Lean 4 port**, in [`leanprover-community/iris-lean`](https://github.com/leanprover-community/iris-lean).

### Status

| Aspect | Detail |
|---|---|
| **Origin** | started as Lars König's master's thesis at KIT (2022), *An Improved Interface for Interactive Proofs in Separation Logic* |
| **Maintained by** | a team in `leanprover-community`, coordinating on the `iris-lean` Zulip channel |
| **Tracking** | a status/tracking site at [leanprover-community.github.io/iris-lean](https://leanprover-community.github.io/iris-lean/) |
| **Lean version** | updated in sync with Lean; releases page carries tags per Lean version |
| **Dependencies** | `batteries` and `Qq` — **no mathlib** for the base `Iris` package (there is an `IrisMath` package for mathlib-based constructions) |

### What's ported

From the project's own README:

- **MoSeL**, the proof interface of Iris
- **`UPred`**, the Iris base logic
- **`IProp`**, the standard model of Iris
- **A selection of Iris resources**, including invariants, later credits, and more

The repository layout shows the port is substantial and follows the Rocq development's structure:

| Directory | Contents |
|---|---|
| `Iris/Algebra/` | `CMRA`, `OFE`, `UPred`, `StepIndex`, `Frac`, `Auth`, `Excl`, `Agree`, `View`, `Monoid`, `Updates`, `LocalUpdates`, `Heap`, `BigOp`, and a `Lib/` of composite algebras |
| `Iris/BI/` | BI, `SIProp`, `MonPred`, `Plainly`, `Updates`, `WeakestPre`, `Telescopes`, `BigOp/`, and `Lib/` (`Atomic`, `Fixpoint`, `Fractional`, `InvHeap`, `Laterable`, `ProphMap`, `Relations`) |
| `Iris/ProgramLogic/` | `Language`, `EctxLanguage`, `WeakestPre`, `TotalWeakestPre`, `Adequacy`, `TotalAdequacy`, `Atomic`, `ThreadPool`, `Lifting`, plus completeness results |
| `Iris/Instances/` | `IProp`, `UPred`, `Classical`, `Data/State`, and `Lib/` (`Invariants`, `CInvariants`, `NaInvariants`, `FUpd`, `GhostMap`, `GhostVar`, `LaterCredits`, `SavedProp`, `Token`, `WSat`, `SetBij`) |
| `Iris/HeapLang/` | `Syntax`, `Semantics`, `ProofMode`, `Tactic`, `Metatheory`, `Completeness`, `PrimitiveLaws`, `ProphErasure`, and a `Lib/` of verified concurrent programs |
| `Iris/Examples/` | `ClosedProofs`, `HeapLang`, `IProp`, `Resources`, `Namesets`, `Fix` |

The `HeapLang/Lib/` directory is a good indicator of maturity — it contains verified **`Counter`,
`Lock`, `SpinLock`, `TicketLock`, `RwLock`, `RwSpinLock`, `Quicksort`**, plus `Array`, `Par`,
`Spawn`, `ClairvoyantCoin`, `LazyCoin`, `LandinsKnot`, and `Diverge`. Locks and a verified quicksort
are the standard smoke tests for a separation logic, and their presence means the port is usable, not
merely type-checking.

### Using it

```toml
# lakefile.toml — no mathlib needed for the base logic
[[require]]
name = "iris"
git.url = "https://github.com/leanprover-community/iris-lean.git"
git.subDir = "Iris"
rev = "master"          # or a release tag, which tracks a Lean version
```

```toml
# for mathlib-based Iris constructions
[[require]]
name = "iris"
git.url = "https://github.com/leanprover-community/iris-lean.git"
git.subDir = "IrisMath"
rev = "master"
```

**Unicode input.** Iris's notation is heavy on `∗`, `-∗`, `▷`, `⌜⌝`. In Lean these are typed via the
extension's replacements (`\ast` → `∗`), and the project suggests adding:

```json
"sep": "∗",
"wand": "-∗",
"pure": "⌜⌝",
"bientails": "⊣⊢"
```

### Honest assessment

| Verdict | Detail |
|---|---|
| ✅ **Usable** | The base logic, proof mode, invariants, ghost state, and HeapLang are ported, and a library of verified concurrent programs (locks, a quicksort) exercises them |
| ✅ **Self-contained** | No mathlib dependency for the core, so it fits in small projects |
| ✅ **Maintained** | Tracks Lean releases, with tagged versions and an active Zulip channel |
| ⚠️ **Less complete than the Rocq original** | Check the [tracking site](https://leanprover-community.github.io/iris-lean/) for what is still missing before committing |
| ⚠️ **The downstream ecosystem is on Rocq** | RustBelt, Perennial, Aneris, Actris and Simuliris are all Rocq developments. iris-lean has the *framework*, not yet the published proofs |
| ⚠️ **Proof effort is high** | Iris proofs are long, and the `▷`/mask bookkeeping is real work |

**The practical recommendation.** If you want to *use* a mature separation logic on real code today,
reach for **Verus** or **Creusot** (Rust, SMT-backed, engineering products — see
[catalog.md](catalog.md)). If you want to *understand or extend* the theory, or you are already in
Lean and your problem is concurrency with tricky ownership, **iris-lean** is the right tool and is
genuinely usable. If you need the full ecosystem of published proofs to build on, use **Rocq + Iris**.

---

## Reference

### Iris syntax you'll meet

| Notation | Meaning |
|---|---|
| `∗` | separating conjunction |
| `-∗` | magic wand |
| `⊢` / `⊣⊢` | entailment / bi-entailment |
| `emp` | empty resource |
| `⌜φ⌝` | pure (no resource) |
| `▷ P` | later |
| `□ P` / `#P` | persistent |
| `■ P` | plainly |
| `inv N P` | invariant named `N` |
| `\|={E1,E2}=>` | fancy update between masks |
| `WP e {Φ}` | weakest precondition |
| <code v-pre>{{{ P }}} e {{{ v, Q }}}</code> | HeapLang triple (Iris 4 notation) |
| `↦` | points-to |

### The proof-mode tactics

`iIntros`, `iDestruct`, `iFrame`, `iApply`, `iMod`, `iModIntro`, `iInv`, `iNext`, `iLöb`, `iExists`,
`iSplit`, `iSplitL`, `iSplitR`, `iAssert`, `iSpecialize`, `iExact`, `iAssumption`, `iRewrite`,
`iPureIntro`, `iPure`, `iStopProof`, `done` — plus the `wp_*` symbolic-execution tactics.

### Iris versus the alternatives

| | Iris / iris-lean | Verus, Creusot, Prusti | Rust's borrow checker |
|---|---|---|---|
| **What it is** | a *framework* for building program logics | verification tools for Rust | a compile-time type system |
| **Automation** | interactive; `iFrame` helps, you write the proof | high (SMT-backed) | total |
| **Expressiveness** | concurrency, higher-order, logical relations, distributed, relaxed memory | sequential-ish Rust; some concurrency | ownership + lifetimes only |
| **Effort** | days–months per proof | hours–days | free |
| **Trust base** | Rocq/Lean kernel + Iris metatheory | SMT solver + encoding | compiler |
| **Use it when** | you need a proof nobody has done before | you need a proof of your Rust code | always |

**The honest summary of the ladder:** the borrow checker gives you the decidable 5% for free; Verus
and Creusot give you most of the rest automatically; Iris is what you reach for when the thing you
need to prove requires *designing a logic*.

---

## References

- **Jung, R., Swasey, D., Sieczkowski, F., Svendsen, K., Turon, A., Birkedal, L., Dreyer, D.**
  *Iris: Monoids and Invariants as an Orthogonal Basis for Concurrent Reasoning.* POPL 2015.
  [PDF](https://iris-project.org/pdfs/2015-popl-iris1-final.pdf) — the original thesis, and the
  source of the "monoids and invariants" quotation.
- **Jung, R., Krebbers, R., Jourdan, J.-H., Bizjak, A., Birkedal, L., Dreyer, D.** *Iris from the
  Ground Up: A Modular Foundation for Higher-Order Concurrent Separation Logic.* JFP 2018.
  [PDF](https://www.mpi-sws.org/~dreyer/papers/iris-ground-up/paper.pdf) — the definitive account of
  the base logic, `▷`, Löb induction, and the `WP` monad.
- **Krebbers, R., Jourdan, J.-H., Jung, R., Tassarotti, J., Kaiser, J.-O., Timany, A.,
  Charguéraud, A., Dreyer, D.** *MoSeL: A General, Extensible Modal Framework for Interactive Proofs
  in Separation Logic.* ICFP 2018. [PDF](https://people.mpi-sws.org/~jung/mosel.pdf) — the proof mode.
- **Jung, R., Krebbers, R., Birkedal, L., Dreyer, D.** *Higher-Order Ghost State.* ICFP 2016 — the
  resource-algebra abstraction.
- **Iris project site** — [iris-project.org](https://iris-project.org/) — publications, lecture
  notes, and the list of projects built on Iris.
- **Iris Rocq development** — [gitlab.mpi-sws.org/iris/iris](https://gitlab.mpi-sws.org/iris/iris/)
- **Iris tutorial / lecture notes** —
  [docs/lectures](https://gitlab.mpi-sws.org/iris/iris/-/tree/master/docs/lectures) — the
  authoritative worked examples; start here if you want to write Iris proofs.
- **Iris-lean** — [github.com/leanprover-community/iris-lean](https://github.com/leanprover-community/iris-lean) ·
  tracking site [leanprover-community.github.io/iris-lean](https://leanprover-community.github.io/iris-lean/) ·
  [Reservoir package](https://reservoir.lean-lang.org/@leanprover-community/iris-lean)
- **König, L.** *An Improved Interface for Interactive Proofs in Separation Logic.* Master's thesis,
  KIT, 2022. [PDF](https://pp.ipd.kit.edu/uploads/publikationen/koenig22masterarbeit.pdf) — the
  origin of iris-lean.
- **RustBelt** — [plv.mpi-sws.org/rustbelt](https://plv.mpi-sws.org/rustbelt/) ·
  **Jung, R., Jourdan, J.-H., Krebbers, R., Dreyer, D.** POPL 2018.
  [PDF](https://plv.mpi-sws.org/rustbelt/popl18/paper.pdf)
- **Jung, R.** *Understanding and Evolving the Rust Programming Language.* PhD thesis, MPI-SWS, 2020.
  [PDF](https://research.ralfj.de/thesis/) — a readable book-length account.
- **Perennial** — **Chajed, T., Tassarotti, J., Kaashoek, M.F., Zeldovich, N.** SOSP 2019.
- **Aneris** — **Krogh-Jespersen, M., Timany, A., Ohlenbusch, M.E., Gregersen, S.O., Birkedal, L.**
  ESOP 2020.
- **Actris** — **Hinrichsen, J.K., Bengtson, J., Krebbers, R.** POPL 2020; *Actris 2.0*, LMCS 2022.
- **Simuliris** — **Gäher, L. et al.** POPL 2022 (Distinguished Paper).
- **Islaris** — **Sammler, M. et al.** PLDI 2022 — machine code against ISA semantics.
- **RefinedRust** — **Gäher, L., Sammler, M., Jung, R., Krebbers, R., Dreyer, D.** PLDI 2024.
- **Quiver** — **Spies, S., Gäher, L., Sammler, M., Dreyer, D.** PLDI 2024 (Distinguished Artifact).
- **Carbonneaux, Q., Zilberstein, N., Klee, C., O'Hearn, P.W., Zappa Nardelli, F.** *Applying Formal
  Verification to Microkernel IPC at Meta.* CPP 2022.
- **O'Hearn, P.** *Resources, Concurrency and Local Reasoning.* CONCUR 2004 — the pre-Iris baseline.
- [Wikipedia: Separation logic](https://en.wikipedia.org/wiki/Separation_logic)

## Further reading

- [separation-logic.md](../01-fundamentals/separation-logic.md) — the theory Iris generalises.
- [techniques.md](../01-fundamentals/techniques.md#5-types--lightweight-static-analysis-the-free-tier) —
  Rust's borrow checker as the decidable fragment.
- [logics.md](../01-fundamentals/logics.md#2-separation-logic--reasoning-about-memory) — the
  connectives in context.
- [lean4.md](lean4.md) — the language iris-lean is written in.
- [type-theory.md](../01-fundamentals/type-theory.md) — step-indexing, guarded recursion, and universes.
