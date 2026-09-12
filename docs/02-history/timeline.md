# Timeline: 1666 → 2026

A dated spine for the history of the field. Bold = the ten most consequential dates.

Legend: 🧮 = logic/foundations · 🛠️ = tool/method · 🏭 = industrial deployment · 🤖 = AI overlap

---

## Prehistory: the dream of mechanical reasoning

| Year | Event | Why it's on this list |
|---|---|---|
| 1666 | 🧮 Leibniz's *characteristica universalis* / *calculus ratiocinator*, "Calculemus!" | The founding dream: settle disputes by calculation, not argument. Every FM paper's first paragraph. |
| 1847 | 🧮 Boole, *The Mathematical Analysis of Logic* | Logic becomes algebra — mechanisable at all. |
| 1879 | 🧮 Frege, *Begriffsschrift* | First-order logic with quantifiers. The language of everything downstream. |
| 1910–13 | 🧮 Russell & Whitehead, *Principia Mathematica* | The first serious machine-checkable-mathematics project (by hand). Took ~360 pages to reach `1+1=2`. |
| 1928 | 🧮 Hilbert & Ackermann pose the *Entscheidungsproblem* | "Is there a mechanical procedure to decide validity?" Sets up the 1936 answer. |

## The limits get discovered (the field's foundations are negative results)

| Year | Event | Why it's on this list |
|---|---|---|
| **1931** | 🧮 **Gödel's incompleteness theorems** | No consistent, expressive, effective system proves all truths. The permanent ceiling. |
| **1936** | 🧮 **Turing / Church: undecidability of the Entscheidungsproblem**, the halting problem | Computing is bounded, and verification of arbitrary programs is undecidable. |
| 1953 | 🧮 Rice's theorem | *Every* non-trivial semantic property of programs is undecidable. Explains the entire tool landscape. |

## The birth of program verification (and simultaneously, of AI)

| Year | Event | Why it's on this list |
|---|---|---|
| **1949** | 🛠️ **Turing, "Checking a Large Routine"** | Possibly the first assertion-based correctness argument for a real program (a factorial routine for EDSAC). Formal methods is *older than AI*. |
| **1956** | 🤖 **Logic Theorist (Newell, Shaw, Simon)** | **The first AI program ever written was a theorem prover.** The AI/FM entanglement is 70 years old — the single best narrative hook in the field's history. |
| 1958–62 | 🧮 McCarthy: Lisp, and "Towards a Mathematical Science of Computation" (1962) | Program semantics as a mathematical object; the founding vision of program verification. |
| 1967 | 🛠️ Floyd, "Assigning Meanings to Programs" | Pre/post-conditions as flow-chart annotations. Verified with the *right* formal logic this time. |
| 1967 | 🛠️ Automath (de Bruijn) | The first proof *assistant*: machine-checked mathematics. |
| **1969** | 🛠️ **Hoare, "An Axiomatic Basis for Computer Programming"** | The Hoare triple `{P}C{Q}`. The single most durable idea in the field. |
| 1971–72 | 🛠️ Boyer–Moore prover; LCF (Milner) → the ML language | Theorem proving gets tooling; LCF's "tactic" architecture still shapes Lean/Isabelle/Rocq. |
| 1972 | 🧮 Dijkstra, "The Humble Programmer" | The culture: complexity is the enemy; correctness is a design property, not a test outcome. |
| 1973 | 🛠️ Mizar | First large-scale library of machine-checked mathematics. |
| **1975** | 🛠️ **Dijkstra, weakest preconditions / guarded commands** | Turns Hoare logic into an *algorithm*: `wp(C,Q)`. The architecture of every automatic verifier since. |
| **1977** | 🛠️ **Cousot & Cousot, abstract interpretation** · Pnueli, temporal logic for programs | Two halves of industrial FM: sound whole-program analysis, and specification of reactive systems. |
| 1976–84 | 🛠️ Edinburgh LCF, HOL, Nuprl, Isabelle (1986), Coq (1988–89) | The proof-assistant lineage that leads to today's Lean/Rocq/Isabelle. |
| 1981–82 | 🛠️ Clarke & Emerson, and Queille & Sifakis: **model checking** | Exhaustive state-space search. Turing Award 2007 to Clarke, Emerson, Sifakis; Pnueli got his in 1996. |
| 1986 | 🛠️ BDDs (Bryant) → symbolic model checking (McMillan, 1992) | Pushes the state-explosion wall far out; model checking becomes industrial. |
| 1990s | 🏭 B method on the Paris Métro Line 14 (opened 1998); SPARK in avionics | The first sustained industrial successes. Driverless metro line verified with B. |

## The solver revolution (the quiet part that made everything else possible)

| Year | Event | Why it's on this list |
|---|---|---|
| 1960/62 | 🛠️ Davis–Putnam, then DPLL | The SAT skeleton. |
| **1996** | 🛠️ **CDCL: clause learning (GRASP, RELSAT)** | SAT solvers become industrial tools. Everything downstream depends on this. |
| 1998 | 🛠️ ESC/Java + Simplify | First popular "SMT-backed verifier for a real language". |
| 2001 | 🛠️ Chaff (watched literals, VSIDS) | Orders-of-magnitude speedup. |
| 2003 | 🛠️ MiniSat; SMT-LIB standard begins | A common input format — the interoperability moment for verification. |
| **2008** | 🛠️ **Z3** (Microsoft Research) | The workhorse backend of a huge fraction of all verification. |
| 2001 | 🛠️ Separation logic (Reynolds, O'Hearn, Yang) | Makes heap reasoning scale via the frame rule. Turing Award 2025. |
| 2021– | 🛠️ cvc5, Bitwuzla, proof-logging solvers (DRAT/LRAT) | More assurance about the solvers themselves. |

## Industrial proof points (the case-study era)

| Year | Event | Why it's on this list |
|---|---|---|
| **1994** | 🏭 **Pentium FDIV bug** | A ~$475M-class event that made formal verification standard in silicon. |
| 1996 | 🏭 Ariane 5 Flight 501 | Reused-assumption failure; the canonical "the spec/assumption was wrong" story. |
| 2004–06 | 🏭 **CompCert** begins (Leroy) | A verified C compiler. Csmith (2011): GCC/LLVM found with hundreds of wrong-code bugs; **CompCert found with zero**. |
| 2005 | 🏭 Astrée proves absence of runtime errors in Airbus A340 fly-by-wire code (~132k lines of C) | Abstract interpretation at industrial scale, low false-alarm rate. This is the "whole codebase" story. |
| **2009** | 🏭 **seL4 verified** (Klein et al., SOSP) | ~8,700 lines of C, ~200,000 lines of Isabelle, ~20 person-years. The most rigorous OS kernel. |
| 2013–14 | 🏭 seL4 integrity + confidentiality proofs, then **binary verification** | Closes the C-to-binary gap — a template for how to state assumptions. |
| **2011→** | 🏭 **AWS adopts TLA+** for S3, DynamoDB, EBS… | The mainstream-industry proof point. Experience report 2014/2015. |
| 2015– | 🏭 Project Everest → HACL*/EverCrypt (F*) in Firefox, Linux, nginx, WireGuard | Verified crypto running everywhere without anyone noticing. |
| 2019– | 🏭 Amazon **Cedar** (Dafny model + differential random testing); Microsoft **SymCrypt** in Lean 4 | "Verification-guided development" becomes a named industrial practice. |
| 2024 | 🏭 AWS says Cedar-scale automated reasoning runs **~1 billion checks/day** | ⚠️ verify the exact current figure before sliding; it comes from AWS material. |

## The AI era (two directions at once)

| Year | Event | Why it's on this list |
|---|---|---|
| 2020 | 🤖 GPT-f (OpenAI) — LLM proof search in Metamath | First credible LLM-in-the-loop theorem proving. |
| 2021 | 🤖 Lean 4 released; mathlib4 begins | Proof assistant + language + huge library. The substrate for AI4Math. |
| 2023 | 🤖 **LeanDojo**, ReProver, COPRA; **Lean FRO founded** | Retrieval-augmented proving; the AI/Lean ecosystem becomes real infrastructure. |
| **2024** | 🤖 **AlphaProof + AlphaGeometry 2 solve 4/6 IMO 2024 problems — silver-medal level (28/42)** | The public proof that RL + formal verification works. AlphaProof trained in Lean; the loop is *generate → Lean verifies → reinforce*. |
| 2025 | 🤖 DeepSeek-Prover-V2, Goedel-Prover (open-source SOTA), Kimina-Prover | Open models close the gap; AI theorem proving becomes a commodity. |
| 2025 | 🤖 **Harmonic's Aristotle: gold-medal-equivalent on IMO 2025 problems, with Lean-verified proofs** | "Formal verification as the reward signal" becomes a product category. |
| 2025 | 🤖 **AgentSpec** (Mar 2025) — runtime enforcement DSL for LLM agents | FM-for-AI: temporal-logic-style rules on agent traces. |
| 2025 | 🤖 **Rocq 9.0** (Mar 2025) — Coq renamed | The old guard modernises. |
| 2025 | 🤖 **AlphaProof published in *Nature*** (Nov 2025) | The formal-AI result clears peer review. |
| 2025 | 🤖 **Separation logic wins the ACM A.M. Turing Award** | The theory that makes Rust-style reasoning formal gets the field's highest honour. |
| 2025 | 🤖 α,β-CROWN wins **VNN-COMP 2025** (5th consecutive) | Neural-network verification has a stable, competitive tool ecosystem. |
| 2026 | 🤖 mathlib: ~**288,041 theorems**, ~**136,932 definitions**, **772 contributors** (Sept 2026) | The largest machine-checked mathematics library, and the AI training substrate. |
| 2026 | 🤖 Kani (Rust model checker) published at ASE 2026 | Push-button verification enters mainstream Rust practice. |
| 2026 | 🤖 DARPA CLARA (~$48M) targets formal verification for aerospace control systems | Governments funding FM for AI-adjacent safety. ⚠️ verify program details. |
| 2026 | 🤖 Agentic-coding reports describe engineers shifting to "coordinating agents", with only 0–20% of tasks fully delegable | The verification bottleneck becomes a mainstream engineering concern. |

---

## The three-act narrative this timeline supports

1. **Act I (1930s–1970s): we discovered the limits, then invented the logics.**
   Gödel/Turing/Rice set the ceiling; Floyd/Hoare/Dijkstra built the ladder anyway.
2. **Act II (1980s–2010s): we made it work, and mostly in the shadows.**
   Solvers got fast, model checking got symbolic, and FM quietly shipped in silicon, avionics,
   microkernels, crypto, and cloud control planes — while ordinary app engineers never saw it.
3. **Act III (2020s–): AI changed the economics and created the demand.**
   Proof search becomes a machine-learning problem; code generation becomes cheap; verification
   becomes the bottleneck and, for the first time, a mass-market concern.

**See [narrative.md](narrative.md) for the story-shaped version.**

## References

Primary sources for the entries on this page, in roughly chronological order.

**Logic and foundations**
- **Leibniz, G.W.** *Dissertatio de arte combinatoria.* 1666 — the *calculus ratiocinator*.
- **Boole, G.** *The Mathematical Analysis of Logic.* 1847.
- **Frege, G.** *Begriffsschrift.* 1879.
- **Russell, B. & Whitehead, A.N.** *Principia Mathematica.* 1910–13.
- **Hilbert, D. & Ackermann, W.** *Grundzüge der theoretischen Logik.* 1928 — the Entscheidungsproblem.
- **Gödel, K.** 1931. [Stanford Encyclopedia](https://plato.stanford.edu/entries/goedel-incompleteness/)
- **Turing, A.M.** *On Computable Numbers…* 1936; **Church, A.** 1936.
- **Rice, H.G.** 1953.

**Program verification**
- **Turing, A.M.** *Checking a Large Routine.* 1949.
- **Newell, A., Shaw, J.C., Simon, H.** 1957 — Logic Theorist.
- **McCarthy, J.** *Towards a Mathematical Science of Computation.* IFIP 1962.
- **Floyd, R.** 1967; **Hoare, C.A.R.** 1969; **Dijkstra, E.W.** 1975.
- **de Bruijn, N.G.** Automath, 1967. **Milner, R.** LCF, 1972. **Boyer & Moore**, 1971–.
- **Mizar** — [mizar.org](https://mizar.uwb.edu.pl/) (from 1973).
- **Cousot, P. & Cousot, R.** POPL 1977; **Pnueli, A.** FOCS 1977.
- **Clarke & Emerson** 1981; **Queille & Sifakis** 1982.
- **Bryant, R.** *Graph-Based Algorithms for Boolean Function Manipulation.* IEEE TC 1986 — BDDs.
- **McMillan, K.** *Symbolic Model Checking.* 1993.
- [Paris Métro Line 14 / the B method](https://www.atelier.net/en/trends/articles/b-method-language-used-certify-software) —
  **Abrial, J.-R.** *The B-Book.* CUP, 1996.

**Solvers**
- **Davis, M. & Putnam, H.** 1960; **Davis, Logemann, Loveland** 1962 — DPLL.
- **Marques-Silva & Sakallah** 1996; **Bayardo & Schrag** 1997 — CDCL.
- **Moskewicz, M. et al.** 2001 — Chaff. **Eén & Sörensson** 2003 — MiniSat.
- **de Moura, L. & Bjørner, N.** TACAS 2008 — Z3. [cvc5](https://cvc5.github.io/) 2021–.
- **Reynolds, J.C.** 2002; **O'Hearn, P. et al.** 2001 — separation logic.

**Industry**
- [Pentium FDIV bug](https://en.wikipedia.org/wiki/Pentium_FDIV_bug) 1994.
- [Ariane 5 Flight 501](https://www.esa.int/Newsroom/Press_Releases/Ariane_5_Flight_501) 1996.
- **Leroy, X.** CACM 2009 — CompCert; **Yang, X. et al.** PLDI 2011 — Csmith.
- **Cousot, P. et al.** ESOP 2005 — Astrée.
- **Klein, G. et al.** SOSP 2009 — seL4; the binary-verification follow-up:
  **Sewell, T. et al.** *Translation Validation for a Verified OS Kernel.* PLDI 2013.
- **Newcombe, C. et al.** 2014/2015 — AWS. **Protzenko, J. et al.** IEEE S&P 2020 — EverCrypt.

**AI era**
- **Polu, S. & Sutskever, I.** *Generative Language Modeling for Automated Theorem Proving.* 2020 —
  GPT-f.
- **Yang, K. et al.** *LeanDojo.* NeurIPS 2023. [lean-dojo.org](https://leandojo.org/)
- **Hubert, T. et al.** *Olympiad-level formal mathematical reasoning with reinforcement learning.*
  *Nature*, 2025.
- **Lin, Y. et al.** *Goedel-Prover.* 2025. [arXiv:2502.07640](https://arxiv.org/abs/2502.07640)
- *Autoformalization in the Era of Large Language Models: A Survey.* 2025.
  [arXiv:2505.23486](https://arxiv.org/abs/2505.23486)
- **OpenAI.** *Ten Advances in Mathematics and Theoretical Computer Science.* 2026.
- **Lean FRO.** [Comparator](https://github.com/leanprover/comparator).
- **Klingner, T. et al.** *A comparison of LLMs' effectiveness in producing formal proofs in Lean 4.*
  [arXiv:2606.05632](https://arxiv.org/abs/2606.05632)
- **Rocq 9.0** (the Coq rename), 12 March 2025.
  [Release notes](https://rocq-prover.org/releases/9.0.0)
- [mathlib statistics](https://leanprover-community.github.io/mathlib_stats.html)
- [Leiden Declaration on AI and Mathematics](https://www.universiteitleiden.nl/en/news/2026/06/leiden-declaration-warns-ai-is-challenging-the-core-values-of-mathematics),
  June 2026.
