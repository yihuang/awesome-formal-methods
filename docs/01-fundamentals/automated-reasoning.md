# Automated reasoning: SAT, SMT, and the engine under everything

> **TL;DR.** Two solver families do almost all the automated work in formal methods: **SAT**
> (boolean satisfiability) and **SMT** (SAT modulo theories). Their improvement over 30 years is
> one of the great unsung engineering achievements of computer science. When someone says "AI
> makes formal methods practical", a large part of what they mean is "solvers got good".

---

## 1. SAT: the boolean core

**Problem.** Given a boolean formula in conjunctive normal form (CNF), find an assignment making
it true, or prove none exists. NP-complete. Therefore, naively hopeless.

**Reality.** Modern solvers handle instances with *millions* of variables and clauses, routinely,
in milliseconds. The reason is engineering, not theory:

| Year | Milestone | Why it mattered |
|---|---|---|
| 1960 | Davis–Putnam procedure | resolution-based, memory-hungry |
| 1962 | **DPLL** (Davis, Putnam, Logemann, Loveland) | backtracking search with unit propagation — still the skeleton |
| 1996 | **CDCL**: GRASP (Marques-Silva & Sakallah), RELSAT (Bayardo & Schrag) | **conflict-driven clause learning** + non-chronological backjumping — the big jump |
| 2001 | **Chaff** (Moskewicz et al.) | watched literals + VSIDS decision heuristic → orders of magnitude faster |
| 2003 | **MiniSat** | ~600 lines of clean C++; became the template for a whole generation |
| 2010s– | CryptoMiniSat, CaDiCaL, Kissat, Glucose, MapleSAT | proof logging (DRAT), inprocessing, better restarts, parallel SAT |

**The three ideas that made CDCL work** (worth understanding properly if you're technical):

1. **Clause learning.** When a conflict occurs, derive the *reason* and add it as a permanent
   clause. The solver accumulates knowledge and doesn't repeat mistakes.
2. **Non-chronological backjumping.** Jump back to the actual cause of the conflict, not just the
   most recent decision.
3. **Watched literals.** Only watch two literals per clause, so unit propagation is ~O(1) per
   clause. This is the constant-factor miracle.

**Where SAT shows up in engineering practice**
- Bounded model checking (CBMC) and symbolic execution (KLEE, angr, Mythril).
- Test generation and fuzzing seed generation.
- Dependency/version solving (`npm`, Cargo, apt).
- Scheduling, planning, FPGA routing, register allocation, package upgrade rollouts.
- Bounded model checking for neural networks and for circuit equivalence.

---

## 2. SMT: SAT with theories

**Problem.** Boolean logic can't express `x + y < z`, arrays, or bit-vectors. Encoding arithmetic
into CNF naively explodes.

**Solution.** SMT = SAT core + **decision procedures for theories**. The SAT solver searches over
boolean structure; theory solvers check/refine the theory-consistent assignments, communicating
via the **Nelson–Oppen** combination method (1979).

| Theory | Expresses | Used for |
|---|---|---|
| **EUF** (equality + uninterpreted functions) | `f(x) = y` | congruence closure, data structures |
| **LIA / LRA** | linear integer/rational arithmetic | bounds, loop counters, resource limits |
| **NIA / NRA** | nonlinear arithmetic | harder; often incomplete in practice |
| **BV** (bit-vectors) | fixed-width machine ints | **exact** hardware/software semantics, overflow |
| **Arrays** | `select`/`store` | memory models, hash maps |
| **Floating point** | IEEE-754 | numerical code, and famously hard |
| **Strings / regexes** | `contains`, `matches` | sanitizers, injection, parser bugs |
| **Sets / relations** | membership | Alloy-style modelling |

**Tools**
- **Z3** (Microsoft Research, 2008–) — the de facto standard; the backend of an enormous fraction
  of academic and industrial verification.
- **cvc5** — successor to CVC4; strong in strings, quantifiers, and as the SMT-COMP champion class.
- **Yices, MathSAT, Boolector, Bitwuzla, STP** — bit-vector specialists.
- **Alt-Ergo** (OCaml, used by Why3/Frama-C), **Vampire** and **E** (first-order superposition
  provers, used for quantified goals).

**How to think about SMT as an engineer:** it's a *superpowered assertion checker*. You give it
first-order constraints; it either says `unsat` (your property holds), `sat` (here's a
counterexample), or `unknown` (it gave up — genuinely common for nonlinear arithmetic and
quantifiers). **Handling `unknown` is the daily work of program verification.**

```
   ┌───────────────── the verification pipeline ─────────────────┐
   │                                                             │
   │  annotated code ──► VC generator ──► SMT query ──► result   │
   │   (Hoare rules)       (VCs)          (Z3/cvc5)              │
   │                                        │                    │
   │                          ┌─────────────┼─────────────┐      │
   │                          ▼             ▼             ▼      │
   │                       unsat          sat         unknown    │
   │                     (verified)   (counter-     (add hints,  │
   │                                   example)      ghost code, │
   │                                                  or give up)│
   └─────────────────────────────────────────────────────────────┘
```

---

## 3. The deep asymmetry: checking is easy, searching is hard

This is the most important conceptual point in the whole wiki for the AI-era framing.

```
   FIND a proof        ─────────────────────►  EXPENSIVE  (search, NP-hard, undecidable in general)
   CHECK a proof       ─────────────────────►  CHEAP      (polynomial; a kernel does it in ms)
```

- If someone hands you a proof, verifying it is fast and reliable. (This is why `NP ⊆ P` questions
  aside, *proof checking* is tractable: it's deterministic bookkeeping.)
- Finding the proof is the intractable part.

**Now substitute "AI" for "search".** LLMs are astonishingly good at *proposing* candidates — a
proof sketch, an invariant, a formalization, a candidate plan. They are unreliable at *guaranteeing*
correctness. Formal methods provide the cheap, trustworthy *checker*.

> **This is the entire thesis of the AI-era talk in one line:**
> **AI is a search amplifier. Formal verification is a cheap, sound filter. Amplifier + filter is
> a fundamentally better pipeline than either alone — and it's the same architecture as
> generate-and-test, except the "test" is sound.**

The symmetry that makes this work:

| | Propose (search) | Dispose (check) |
|---|---|---|
| Classical FM | human writes proof | kernel checks it |
| AI-era FM | LLM proposes proof/invariant/spec | kernel or SMT solver checks it |
| SWE practice | LLM proposes code | tests check it *(unsound)* |
| **AI-era FM** | LLM proposes code | **SMT/kernel checks it *(sound)*** |

The last row is why formal methods are becoming relevant to ordinary software engineers rather
than staying a niche: it upgrades the *verification* half of the AI coding loop from sampled to
sound.

---

## 4. Proof logging: making solvers trustworthy

A subtle problem: if your verifier's correctness depends on a 500,000-line C++ SMT solver, what
have you actually proven? Two answers:

1. **DRAT/LRAT proof logging** for SAT: the solver emits a machine-checkable proof of
   unsatisfiability, which an independent tiny checker validates. This is now standard in
   competition solvers (CaDiCaL, Kissat) and is increasingly required for industrial use.
2. **Proof-producing SMT / verified checkers**: verified checkers (e.g. in Coq/Lean) for the
   emitted certificates.

**Why it matters:** it shows the field takes its own medicine. When the trusted base
grows, the field's response is to *shrink* it. Any engineer who has debugged a "trust me" third-party
service will appreciate the instinct.

---

## 5. What solvers still can't do

| Limitation | Consequence |
|---|---|
| Nonlinear arithmetic is undecidable over integers; solvers are often incomplete | `unknown` results; you restructure the proof |
| Quantifiers make problems undecidable | you instantiate by hand or use triggers/heuristics |
| Floating point + transcendental functions | hard; often over-approximated |
| Combinatorial blowup persists despite CDCL | the "SAT vs. NP" wall is real, just further away |
| Solvers can be buggy | use proof logging for high assurance |
| Inductive invariants need a human/LLM to propose | the automation boundary |

**Held-out hope for AI:** the bottleneck in most verification is not the solver, it's the
*annotation* — invariants, loop bounds, intermediate assertions, ghost code. That is exactly the
kind of proposal problem LLMs are good at, and it's why `ai-for-fm.md` is the most commercially
interesting page in this wiki.

---

Next → [limits.md](limits.md): what is provably impossible, and the honest boundaries of the field.
