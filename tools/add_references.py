#!/usr/bin/env python3
"""
add_references.py — one-off migration that adds curated `## References` sections.

Run from the repository root:  python3 tools/add_references.py

Inserts a References section before an existing `## Further reading` heading if there is
one, otherwise appends it to the end of the page. Idempotent: skips pages that already
have a `## References` heading.
"""

from __future__ import annotations

import re
from pathlib import Path

R: dict[str, str] = {}

R["docs/00-orientation/taxonomy.md"] = """## References

- **Hoare, C.A.R.** *An Axiomatic Basis for Computer Programming.* CACM 12(10), 1969.
  [PDF](https://dl.acm.org/doi/10.1145/363235.363259) — the origin of `{P}C{Q}`.
- **Cousot, P. & Cousot, R.** *Abstract Interpretation: A Unified Lattice Model for Static Analysis
  of Programs by Construction or Approximation of Fixpoints.* POPL 1977.
  [Overview](https://www.di.ens.fr/~cousot/AI/IntroAbsInt.html) — the sound over-approximation family.
- **Clarke, E.M. & Emerson, E.A.** *Design and Synthesis of Synchronization Skeletons Using
  Branching-Time Temporal Logic.* 1981; **Queille, J.P. & Sifakis, J.** 1982 — model checking.
- **Rice, H.G.** *Classes of Recursively Enumerable Sets and Their Decision Problems.* 1953 — why
  every tool is incomplete or unsound.
- **Howard, W.A.** *The Formulae-as-Types Notion of Construction.* 1969 — Curry–Howard, and why
  proof assistants are programming languages.
- **de Bruijn, N.G.** *A Survey of the Project Automath.* 1980 — the de Bruijn criterion, and the
  small-kernel design that proof assistants still follow.
- **Newcombe, C. et al.** *Use of Formal Methods at Amazon Web Services.* 2014/2015.
  [PDF](https://lamport.azurewebsites.net/tla/formal-methods-amazon.pdf) — the practitioner framing
  used throughout this wiki.
- [Wikipedia: Formal methods](https://en.wikipedia.org/wiki/Formal_methods) — for the survey-level
  taxonomy.
"""

R["docs/00-orientation/why-now.md"] = """## References

- **Newcombe, C. et al.** *Use of Formal Methods at Amazon Web Services.* 2014/2015.
  [PDF](https://lamport.azurewebsites.net/tla/formal-methods-amazon.pdf) — the "perception is quite
  wrong" quotation, and formal methods as an enabler rather than insurance.
- **AWS Security Blog.** *An Unexpected Discovery: Automated Reasoning Often Makes Systems More
  Efficient and Easier to Maintain.*
  [Link](https://aws.amazon.com/blogs/security/an-unexpected-discovery-automated-reasoning-often-makes-systems-more-efficient-and-easier-to-maintain/) —
  the same argument from the other direction: verification leading to *faster* systems.
- **Anthropic.** *Eight trends defining how software gets built in 2026.* Jan 2026.
  [Link](https://claude.com/blog/eight-trends-defining-how-software-gets-built-in-2026) — the
  "~60% of work / 0–20% fully delegable" figure. ⚠️ Vendor-published; see the
  [confidence ledger](../research-notes.md#4-confidence-ledger).
- **Alt, L.** *Performant Verified Software.* Sept 2026.
  [Link](https://leoalt.de/performant-verified-software) — the strongest statement of the
  "verification buys performance" thesis, with production numbers.
- **Rice, H.G.** *Classes of Recursively Enumerable Sets and Their Decision Problems.* 1953 → see
  [limits.md](../01-fundamentals/limits.md) for why testing cannot be made sound.
- [Ethereum formal verification overview](https://github.com/leonardoalt/ethereum_formal_verification_overview) —
  an actively maintained list of what is *actually* verified in a domain where failure is
  monetised.
"""

R["docs/01-fundamentals/automated-reasoning.md"] = """## References

- **Davis, M., Logemann, G., Loveland, D.** *A Machine Program for Theorem-Proving.* CACM 1962 —
  the DPLL procedure.
- **Marques-Silva, J. & Sakallah, K.** *GRASP: A Search Algorithm for Propositional Satisfiability.*
  IEEE Trans. Computers, 1999 (conference version 1996) — clause learning.
- **Bayardo, R. & Schrag, R.** *Using CSP Look-Back Techniques to Solve Real-World SAT Instances.*
  AAAI 1997 — RELSAT, non-chronological backjumping.
- **Moskewicz, M. et al.** *Chaff: Engineering an Efficient SAT Solver.* DAC 2001 — watched literals
  and VSIDS.
- **Eén, N. & Sörensson, N.** *An Extensible SAT-solver.* SAT 2003 — MiniSat.
- **de Moura, L. & Bjørner, N.** *Z3: An Efficient SMT Solver.* TACAS 2008.
  [PDF](https://link.springer.com/chapter/10.1007/978-3-540-78800-3_24)
- **Barbosa, H. et al.** *cvc5: A Versatile and Industrial-Strength SMT Solver.* TACAS 2022.
  [PDF](https://arxiv.org/abs/2205.06117)
- **Nelson, G. & Oppen, D.** *Simplification by Cooperating Decision Procedures.* TOPLAS 1979 — the
  Nelson–Oppen combination method.
- **Barrett, C., Sebastiani, R., Seshia, S., Tinelli, C.** *Satisfiability Modulo Theories.* In
  *Handbook of Satisfiability*, 2021. [PDF](https://theory.stanford.edu/~barrett/pubs/BSS+21.pdf)
- **Wetzler, N., Heule, M., Hunt, W.** *DRAT-trim: Efficient Checking and Trimming Using Expressive
  Clausal Proofs.* SAT 2014 — machine-checkable UNSAT proofs.
- **Cook, S.** *The Complexity of Theorem-Proving Procedures.* STOC 1971 — NP-completeness.
- [SAT solver](https://en.wikipedia.org/wiki/SAT_solver) ·
  [Satisfiability modulo theories](https://en.wikipedia.org/wiki/Satisfiability_modulo_theories)
- **Dijkstra, E.W.** *Guarded Commands, Nondeterminacy and Formal Derivation of Programs.* CACM 1975
  — `wp`, and the verification-condition pipeline this page describes.
"""

R["docs/01-fundamentals/limits.md"] = """## References

- **Gödel, K.** *Über formal unentscheidbare Sätze der Principia Mathematica und verwandter
  Systeme I.* 1931. [Stanford Encyclopedia](https://plato.stanford.edu/entries/goedel-incompleteness/)
- **Turing, A.M.** *On Computable Numbers, with an Application to the Entscheidungsproblem.* 1936 —
  the halting problem.
- **Rice, H.G.** *Classes of Recursively Enumerable Sets and Their Decision Problems.* Trans. AMS,
  1953. [PDF](https://www.ams.org/journals/tran/1953-074-02/S0002-9947-1953-0053041-6/S0002-9947-1953-0053041-6.pdf)
- **Wright, A. & Felleisen, M.** *A Syntactic Approach to Type Soundness.* 1994 — progress and
  preservation, the type-system analogue of soundness.
- **Klein, G. et al.** *seL4: Formal Verification of an OS Kernel.* SOSP 2009.
  [PDF](https://sel4.systems/Research/pdfs/sel4-sosp2009.pdf) — the ~8,700 lines of C / ~200,000
  lines of proof / ~20 person-years figures, and the assumptions section.
- **Cousot, P. et al.** *The ASTRÉE Analyzer.* ESOP 2005.
  [PDF](https://pcousot.github.io/publications/CousotEtAl-ESOP05.pdf) — false alarms, and the price
  of soundness.
- **Yang, X., Chen, Y., Eide, E., Regehr, J.** *Finding and Understanding Bugs in C Compilers.*
  PLDI 2011. [PDF](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf) — the Csmith study.
- **Pentium FDIV bug** — [Wikipedia](https://en.wikipedia.org/wiki/Pentium_FDIV_bug)
- **Ariane 5 Flight 501** — [ESA report](https://www.esa.int/Newsroom/Press_Releases/Ariane_5_Flight_501)
- **Knight Capital** — SEC filing and contemporaneous reporting; the deployment-error case study.
- [Gödel's incompleteness theorems](https://en.wikipedia.org/wiki/G%C3%B6del%27s_incompleteness_theorems)
"""

R["docs/01-fundamentals/logics.md"] = """## References

- **Floyd, R.** *Assigning Meanings to Programs.* 1967 — pre/post-conditions.
- **Hoare, C.A.R.** *An Axiomatic Basis for Computer Programming.* CACM 1969 — the Hoare triple and
  the inference rules reproduced on this page.
- **Dijkstra, E.W.** *Guarded Commands, Nondeterminacy and Formal Derivation of Programs.* CACM
  1975 — weakest preconditions.
- **Pnueli, A.** *The Temporal Logic of Programs.* FOCS 1977 — temporal logic for reactive systems
  (Turing Award 1996).
- **Clarke, E.M. & Emerson, E.A.** *Design and Synthesis of Synchronization Skeletons Using
  Branching-Time Temporal Logic.* 1981 — CTL; **Queille & Sifakis** 1982 — the independent origin of
  model checking (Turing Award 2007).
- **Emerson, E.A. & Halpern, J.** *"Sometimes" and "Not Never" Revisited: On Branching versus Linear
  Time.* POPL 1983 — LTL vs CTL, and CTL*.
- **Kozen, D.** *Results on the Propositional μ-Calculus.* 1983.
- **Reynolds, J.C.** *Separation Logic: A Logic for Shared Mutable Data Structures.* LICS 2002;
  **O'Hearn, P., Reynolds, J., Yang, H.** *Local Reasoning about Programs that Alter Data
  Structures.* CSL 2001. [Separation logic](https://en.wikipedia.org/wiki/Separation_logic) — the
  frame rule, and the basis for Rust's ownership discipline.
- **Howard, W.A.** *The Formulae-as-Types Notion of Construction.* 1969 — Curry–Howard.
- **Pierce, B.** *Types and Programming Languages.* MIT Press, 2002.
- **Winskel, G.** *The Formal Semantics of Programming Languages.* MIT Press, 1993.
- [Hoare logic](https://en.wikipedia.org/wiki/Hoare_logic) ·
  [Model checking](https://en.wikipedia.org/wiki/Model_checking)
"""

R["docs/01-fundamentals/specifications.md"] = """## References

- **Floyd, R.** *Assigning Meanings to Programs.* 1967.
- **Hoare, C.A.R.** *An Axiomatic Basis for Computer Programming.* CACM 1969.
  [PDF](https://dl.acm.org/doi/10.1145/363235.363259)
- **Dijkstra, E.W.** *Guarded Commands, Nondeterminacy and Formal Derivation of Programs.* CACM 1975.
- **Lamport, L.** *Specifying Systems: The TLA+ Language and Tools for Hardware and Software
  Engineers.* Addison-Wesley, 2002. [Free online](https://lamport.azurewebsites.net/tla/book.html) —
  the reference for writing specifications at the design level.
- **Newcombe, C. et al.** *Use of Formal Methods at Amazon Web Services.* 2014/2015.
  [PDF](https://lamport.azurewebsites.net/tla/formal-methods-amazon.pdf) — the "what needs to go
  right" inversion, the refinement-gap honesty, and the data-modelling aside.
- **Amazon Science.** *How we built Cedar with automated reasoning and differential testing.*
  [Link](https://www.amazon.com/science/blog/how-we-built-cedar-with-automated-reasoning-and-differential-testing) —
  the ghost/observer spec pattern and the `explicit permit` / `forbid overrides permit` properties.
- **Cutler, J. et al.** *Cedar: A New Language for Expressive, Fast, Safe, and Analyzable
  Authorization.* OOPSLA 2024. [PDF](https://arxiv.org/abs/2403.04651)
- [Refinement](https://en.wikipedia.org/wiki/Refinement_(computing)) — the abstraction relation.
"""

R["docs/01-fundamentals/techniques.md"] = """## References

- **Cousot, P. & Cousot, R.** *Abstract Interpretation: A Unified Lattice Model for Static Analysis
  of Programs.* POPL 1977. [Intro](https://www.di.ens.fr/~cousot/AI/IntroAbsInt.html)
- **Cousot, P. et al.** *The ASTRÉE Analyzer.* ESOP 2005.
  [PDF](https://pcousot.github.io/publications/CousotEtAl-ESOP05.pdf) — industrial abstract
  interpretation on ~132,000 lines of Airbus C.
- **Clarke, E.M. & Emerson, E.A.** 1981; **Queille & Sifakis** 1982 — model checking.
- **Klein, G. et al.** *seL4: Formal Verification of an OS Kernel.* SOSP 2009.
  [PDF](https://sel4.systems/Research/pdfs/sel4-sosp2009.pdf)
- **Leroy, X.** *Formal Verification of a Realistic Compiler.* CACM 2009.
  [PDF](https://xavierleroy.org/publi/compcert-CACM.pdf)
- **Leino, K.R.M.** *Dafny: An Automatic Program Verifier for Functional Correctness.* LPAR 2010.
- **Barnett, M., Chang, B.-Y., DeLine, R., Jacobs, B., Leino, K.R.M.** *Boogie: A Modular Reusable
  Verifier for Object-Oriented Programs.* FMCO 2005 — the VC-generation architecture under many tools.
- **Delmas, R. et al.** *Kani: A Model Checker for Rust.* ASE 2026.
  [Repository](https://github.com/model-checking/kani)
- **Barnett, M. & Rustan, K.** and the **RustBelt** line of work: **Jung, R. et al.** *RustBelt:
  Securing the Foundations of the Rust Programming Language.* POPL 2018 — Rust's ownership as a
  separation-logic discipline.
- [Abstract interpretation](https://en.wikipedia.org/wiki/Abstract_interpretation) ·
  [Model checking](https://en.wikipedia.org/wiki/Model_checking) ·
  [Theorem proving](https://en.wikipedia.org/wiki/Automated_theorem_proving)
"""

R["docs/02-history/index.md"] = """## References

- **Clarke, E.M. & Wing, J.M.** *Formal Methods: State of the Art and Future Directions.* ACM
  Computing Surveys 28(4), 1996.
  [PDF](https://www.cs.cmu.edu/~emc/papers/Books%20and%20Edited%20Volumes/Formal%20Methods%20State%20of%20the%20Art%20and%20Future%20Directions.pdf)
- **Woodcock, J., Larsen, P., Bicarregui, J., Fitzgerald, J.** *Formal Methods: Practice and
  Experience.* ACM Computing Surveys 41(4), 2009.
  [PDF](https://dl.acm.org/doi/10.1145/1592434.1592436) — the industrial case-study survey, and the
  strongest single source for "it shipped, quietly".
- **Klein, G. et al.** *seL4: Formal Verification of an OS Kernel.* SOSP 2009.
- **Leroy, X.** *Formal Verification of a Realistic Compiler.* CACM 2009.
- **Yang, X. et al.** *Finding and Understanding Bugs in C Compilers.* PLDI 2011.
- **Cousot, P. et al.** *The ASTRÉE Analyzer.* ESOP 2005.
- **Newcombe, C. et al.** *Use of Formal Methods at Amazon Web Services.* 2014/2015.
- **Newell, A., Shaw, J.C., Simon, H.** *Empirical Explorations with the Logic Theory Machine.* 1957 —
  the first AI program, and a theorem prover.
- **MacKenzie, D.** *Mechanizing Proof: Computing, Risk, and Trust.* MIT Press, 2001 — the sociology
  of why adoption is hard.
- **Hubert, T. et al.** *Olympiad-level formal mathematical reasoning with reinforcement learning.*
  *Nature*, 2025. [Link](https://www.nature.com/articles/s41586-025-09833-y)
"""

R["docs/02-history/narrative.md"] = """## References

- **Newell, A., Shaw, J.C., Simon, H.** *Empirical Explorations with the Logic Theory Machine: A
  Case Study in Heuristics.* 1957 — Logic Theorist, and the theorems it proved from *Principia
  Mathematica*.
- **Turing, A.M.** *Checking a Large Routine.* 1949 — arguably the first program-correctness
  argument.
- **Gödel, K.** 1931; **Turing, A.M.** 1936; **Rice, H.G.** 1953 — Act I's three ceiling results.
- **Floyd, R.** 1967; **Hoare, C.A.R.** 1969; **Dijkstra, E.W.** 1975 — the ladder.
- **Cousot, P. & Cousot, R.** 1977; **Clarke & Emerson** 1981 — the two escapes from undecidability.
- [Pentium FDIV bug](https://en.wikipedia.org/wiki/Pentium_FDIV_bug) — and John Harrison's HOL Light
  verification of Intel's floating-point division: **Harrison, J.** *Formal Verification of
  Floating-Point Algorithms* (TPHOLs 2000).
- **Cousot, P. et al.** *The ASTRÉE Analyzer.* ESOP 2005 — A340 fly-by-wire.
- **Leroy, X.** *Formal Verification of a Realistic Compiler.* CACM 2009; **Yang, X. et al.** PLDI
  2011 — CompCert and the Csmith comparison.
- **Klein, G. et al.** *seL4: Formal Verification of an OS Kernel.* SOSP 2009.
- **Protzenko, J. et al.** *EverCrypt: A Fast, Verified, Cross-Platform Cryptographic Provider.*
  IEEE S&P 2020. [hacl-star.github.io](https://hacl-star.github.io/HaclValeEverCrypt.html)
- **Newcombe, C. et al.** *Use of Formal Methods at Amazon Web Services.* 2014/2015.
- **Hubert, T. et al.** *Olympiad-level formal mathematical reasoning with reinforcement learning.*
  *Nature*, 2025.
- **OpenAI.** *Ten Advances in Mathematics and Theoretical Computer Science.* 2026.
  [Repository](https://github.com/openai/ten-proofs)
"""

R["docs/02-history/timeline.md"] = """## References

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
"""

R["docs/03-applications/adoption-gap.md"] = """## References

- **Woodcock, J., Larsen, P., Bicarregui, J., Fitzgerald, J.** *Formal Methods: Practice and
  Experience.* ACM Computing Surveys 41(4), 2009.
  [ACM](https://dl.acm.org/doi/10.1145/1592434.1592436) — the industrial case-study survey, and the
  clearest evidence that the technology works *and* did not spread.
- **Clarke, E.M. & Wing, J.M.** *Formal Methods: State of the Art and Future Directions.* ACM
  Computing Surveys 28(4), 1996.
- **Newcombe, C. et al.** *Use of Formal Methods at Amazon Web Services.* 2014/2015.
  [PDF](https://lamport.azurewebsites.net/tla/formal-methods-amazon.pdf) — the "perception is quite
  wrong" quotation, and the "perception problem" framing of the adoption gap.
- **Anthropic.** *Eight trends defining how software gets built in 2026.* Jan 2026.
  [Link](https://claude.com/blog/eight-trends-defining-how-software-gets-built-in-2026) — the
  assisted-versus-delegable gap. ⚠️ Vendor source.
- **Alt, L.** *Performant Verified Software.* 2026.
  [Link](https://leoalt.de/performant-verified-software) — the counter-argument to "verification is
  a brake".
- ⚠️ **Aerospace adoption barriers.** This page refers to empirical work on why aerospace
  contractors, customers, and certification authorities hesitate to adopt formal methods. **No
  specific study is pinned here yet** — candidates include the NASA/RTCA-adjacent surveys and the
  FM 2009 industrial-practice workshop papers. Pin one before relying on the claim; see the
  [confidence ledger](../research-notes.md#4-confidence-ledger).
- **MacKenzie, D.** *Mechanizing Proof: Computing, Risk, and Trust.* MIT Press, 2001 — why adoption
  is a social problem as much as a technical one.
"""

R["docs/03-applications/case-studies.md"] = """## References

- **Klein, G. et al.** *seL4: Formal Verification of an OS Kernel.* SOSP 2009.
  [PDF](https://sel4.systems/Research/pdfs/sel4-sosp2009.pdf) ·
  [sel4.systems](https://sel4.systems/) — the 8,700 / 200,000 / ~20 person-year figures, and the
  assumptions section.
  [verifiedsoftware.dev](https://verifiedsoftware.dev/case-studies/) collects the same numbers
  with the caveats.
- **Leroy, X.** *Formal Verification of a Realistic Compiler.* CACM 2009.
  [PDF](https://xavierleroy.org/publi/compcert-CACM.pdf) · [compcert.org](https://compcert.org/)
- **Yang, X., Chen, Y., Eide, E., Regehr, J.** *Finding and Understanding Bugs in C Compilers.*
  PLDI 2011. [PDF](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf) — the Csmith study
  behind the "zero vs hundreds" comparison.
- **Newcombe, C. et al.** *Use of Formal Methods at Amazon Web Services.* 2014/2015.
  [PDF](https://lamport.azurewebsites.net/tla/formal-methods-amazon.pdf) ·
  *How Amazon Web Services Uses Formal Methods*, CACM 2015.
- **Amazon Science.** *How we built Cedar with automated reasoning and differential testing.*
  [Link](https://www.amazon.science/blog/how-we-built-cedar-with-automated-reasoning-and-differential-testing) ·
  [cedarpolicy.com](https://www.cedarpolicy.com/) — the Dafny model, the two proved properties, and
  the differential random testing of the Rust implementation. ⚠️ The ~1 billion checks/day figure is
  from AWS material; verify the current number.
- **Microsoft SymCrypt** — [github.com/microsoft/SymCrypt](https://github.com/microsoft/SymCrypt)
  ⚠️ Vendor-published; the Lean 4 verification programme is described in Microsoft engineering
  material rather than a peer-reviewed paper.
- **Protzenko, J. et al.** *EverCrypt: A Fast, Verified, Cross-Platform Cryptographic Provider.*
  IEEE S&P 2020. [hacl-star.github.io](https://hacl-star.github.io/HaclValeEverCrypt.html) —
  deployment in Firefox, the Linux kernel, nginx, and WireGuard.
- **Veil** — [github.com/verse-lab/veil](https://github.com/verse-lab/veil); the "found bugs in
  previously verified protocols" claim comes from
  [verifiedsoftware.dev](https://verifiedsoftware.dev/case-studies/). ⚠️ Verify against the Veil
  paper before citing.
- **VNN-COMP** — [vnn-comp.github.io](https://vnn-comp.github.io/) ·
  **α,β-CROWN** — [github.com/Verified-Intelligence/alpha-beta-CROWN](https://github.com/Verified-Intelligence/alpha-beta-CROWN)
- **Kani** — [github.com/model-checking/kani](https://github.com/model-checking/kani)
"""

R["docs/03-applications/distributed-systems.md"] = """## References

- **Newcombe, C. et al.** *Use of Formal Methods at Amazon Web Services.* 2014/2015.
  [PDF](https://lamport.azurewebsites.net/tla/formal-methods-amazon.pdf) — the design-bug argument,
  the "Debugging Designs" framing, and the data-modelling discovery.
- **Lamport, L.** *Specifying Systems.* 2002. [Free online](https://lamport.azurewebsites.net/tla/book.html) ·
  [TLA+ home](https://lamport.azurewebsites.net/tla/tla.html) · [learntla.com](https://learntla.com/)
- **Apalache** — [apalache-mc.org](https://apalache-mc.org/) — symbolic, SMT-backed TLA+ checking.
- **Jackson, D.** *Software Abstractions: Logic, Language, and Analysis.* MIT Press, 2012 — Alloy,
  and the Chord case study.
- **Holzmann, G.** *The SPIN Model Checker.* Addison-Wesley, 2003.
- **Hawblitzel, C. et al.** *IronFleet: Proving Practical Distributed Systems Correct.* SOSP 2015.
  [PDF](https://www.microsoft.com/en-us/research/publication/ironfleet-proving-practical-distributed-systems-correct/)
- **Wilcox, J. et al.** *Verdi: A Framework for Verifying Distributed Systems.* PLDI 2015.
- **Veil** — [github.com/verse-lab/veil](https://github.com/verse-lab/veil) — Lean 4 protocol
  verification.
- **Kingsbury, K.** *Jepsen.* [jepsen.io](https://jepsen.io/) — black-box testing under partitions;
  the complement to model checking, not a substitute.
- **FoundationDB** — *Testing Distributed Systems with Deterministic Simulation.*
  [Apple engineering note](https://apple.github.io/foundationdb/testing.html) ·
  **TigerBeetle** — [Deterministic Simulation Testing](https://docs.tigerbeetle.com/concepts/safety/)
- **Stateright** — [github.com/stateright/stateright](https://github.com/stateright/stateright) —
  model checking in and for Rust.
"""

R["docs/03-applications/hardware-crypto.md"] = """## References

- **Harrison, J.** *Formal Verification of Floating-Point Algorithms* (TPHOLs 2000) and *Floating
  Point Verification in HOL Light: The Exponential Function* — Intel's use of HOL Light for
  floating-point correctness. [Harrison's page](https://www.cl.cam.ac.uk/~jrh13/)
- [Pentium FDIV bug](https://en.wikipedia.org/wiki/Pentium_FDIV_bug) — the 1994 event that made
  formal verification standard in silicon.
- **Cadence Jasper** (incl. Sequential Equivalence Checking) —
  [product page](https://www.cadence.com/en_US/home/tools/system-design-and-verification/formal-and-static-verification/jasper-verification-platform.html) ·
  **Synopsys VC Formal** · **Siemens Questa Formal** — the commercial formal-verification flows.
- **Protzenko, J. et al.** *EverCrypt: A Fast, Verified, Cross-Platform Cryptographic Provider.*
  IEEE S&P 2020. [hacl-star.github.io](https://hacl-star.github.io/HaclValeEverCrypt.html) — and the
  Vale verified-assembly component.
- **Microsoft SymCrypt** — [github.com/microsoft/SymCrypt](https://github.com/microsoft/SymCrypt)
  ⚠️ Verification claims are vendor-published.
- **Rust → Lean extraction tooling**: [Charon](https://github.com/AeneasVerif/charon),
  [Aeneas](https://github.com/AeneasVerif/aeneas), [Hax](https://github.com/hacspec/hax).
  ⚠️ Fast-moving; check maturity before recommending.
- **Constant-time / side channels**: **Almeida, J. et al.** *Verifying Constant-Time
  Implementations.* USENIX Security 2016 (`ct-verif`) ·
  [FaCT](https://github.com/PLSysSec/FaCT) · [dudect](https://github.com/oreparaz/dudect)
- **Protocol verification**: **Blanchet, B.** *ProVerif* —
  [bblanche.gitlabpages.inria.fr/proverif](https://bblanche.gitlabpages.inria.fr/proverif/) ·
  **Tamarin** — [tamarin-prover.github.io](https://tamarin-prover.github.io/) ·
  **EasyCrypt** — [easycrypt.gitlabpages.inria.fr](https://easycrypt.gitlabpages.inria.fr/)
- **Sail** — [github.com/rems-project/sail](https://github.com/rems-project/sail) — official ARM and
  RISC-V ISA semantics, and the specification zkVM verification is checked against.
"""

R["docs/03-applications/lightweight-fm.md"] = """## References

- **Claessen, K. & Hughes, J.** *QuickCheck: A Lightweight Tool for Random Testing of Haskell
  Programs.* ICFP 2000. [PDF](https://www.cs.tufts.edu/~nr/cs257/archive/john-hughes/quick.pdf) —
  the origin of property-based testing.
- **MacIver, D.** *Hypothesis* — [hypothesis.readthedocs.io](https://hypothesis.readthedocs.io/) ·
  **proptest** — [github.com/proptest-rs/proptest](https://github.com/proptest-rs/proptest) ·
  **fast-check** — [fast-check.dev](https://fast-check.dev/) ·
  **jqwik** — [jqwik.net](https://jqwik.net/)
- **Kani** — [github.com/model-checking/kani](https://github.com/model-checking/kani) ·
  [Kani book](https://model-checking.github.io/kani/) — `cargo kani`, `#[kani::proof]`, `kani::any()`
- **CBMC** — [cbmc-documentation.readthedocs.io](https://cbmc-documentation.readthedocs.io/) — the
  bounded model checker Kani is built on.
- **Lamport, L.** *Specifying Systems.* [Free online](https://lamport.azurewebsites.net/tla/book.html) ·
  [TLA+ video course](https://lamport.azurewebsites.net/video/videos.html) ·
  [learntla.com](https://learntla.com/) — the fastest route to a first spec.
- **Wayne, H.** *Practical TLA+.* Apress, 2018 — the engineer-oriented book.
- **Apalache** — [apalache-mc.org](https://apalache-mc.org/)
- **Newcombe, C. et al.** *Use of Formal Methods at Amazon Web Services.* 2014/2015 — the
  "exhaustively testable pseudo-code" framing, and the start-from-an-incident lesson.
- **Amazon Science.** *How we built Cedar with automated reasoning and differential testing.*
  [Link](https://www.amazon.science/blog/how-we-built-cedar-with-automated-reasoning-and-differential-testing) —
  the prove-a-model-then-differentially-test pattern.
"""

R["docs/03-applications/safety-critical.md"] = """## References

- **RTCA DO-178C** — *Software Considerations in Airborne Systems and Equipment Certification.*
  [rtca.org](https://www.rtca.org/do-178/)
- **RTCA DO-333** — *Formal Methods Supplement to DO-178C and DO-278A.*
  [Project notes](https://loonwerks.com/projects/do333.html)
- **RTCA DO-330** — *Software Tool Qualification Considerations* — the "who verifies the verifier"
  problem in regulatory form.
- **RTCA DO-331** (model-based development) and **DO-332** (object-oriented technology).
  [RTCA standards](https://www.rtca.org/standards/)
- **ISO 26262** — *Road vehicles — Functional safety.* [iso.org](https://www.iso.org/standard/68383.html)
- **IEC 61508** — *Functional safety of electrical/electronic/programmable electronic safety-related
  systems.* [iec.ch](https://www.iec.ch/functionalsafety/)
- **EN 50128** — *Railway applications — Software for railway control and protection systems.*
- **IEC 62304** — *Medical device software — Software life cycle processes.*
- **Common Criteria** — [commoncriteriaportal.org](https://www.commoncriteriaportal.org/)
- **Cousot, P. et al.** *The ASTRÉE Analyzer.* ESOP 2005.
  [PDF](https://pcousot.github.io/publications/CousotEtAl-ESOP05.pdf) — the A340 fly-by-wire result.
- **Leroy, X.** *Formal Verification of a Realistic Compiler.* CACM 2009 — CompCert under DO-178C.
- **Newcombe, C. et al.** *Use of Formal Methods at Amazon Web Services.* 2014/2015 — the
  "safety-critical only" stereotype, and why it is out of date.
- **Bloomfield, R. & Craigen, D.** and the wider assurance-case literature for **Goal Structuring
  Notation**: **Kelly, T.** *Arguing Safety.* DPhil thesis, University of York, 1998.
"""

R["docs/04-ai-era/ai-for-fm.md"] = """## References

- **Polu, S. & Sutskever, I.** *Generative Language Modeling for Automated Theorem Proving.* 2020.
  [arXiv:2009.03393](https://arxiv.org/abs/2009.03393) — GPT-f.
- **Yang, K. et al.** *LeanDojo: Theorem Proving with Retrieval-Augmented Language Models.* NeurIPS
  2023. [arXiv:2306.15626](https://arxiv.org/abs/2306.15626) · [lean-dojo.org](https://leandojo.org/)
- **Hubert, T. et al.** *Olympiad-level formal mathematical reasoning with reinforcement learning.*
  *Nature*, 2025. [Link](https://www.nature.com/articles/s41586-025-09833-y) — the AlphaProof
  architecture: 3B-parameter proof network, ~300k state–tactic pairs, ~1M informal → ~80M formal
  problems, TTRL, and the IMO 2024 result. **All architectural figures on this page come from here.**
- **AlphaProof & AlphaGeometry teams.** *AI achieves silver-medal standard solving International
  Mathematical Olympiad problems.* DeepMind, July 2024.
  [Link](https://deepmind.google/blog/ai-solves-imo-problems-at-silver-medal-level/)
- **Chervonyi, Y. et al.** *Gold-medalist performance in solving olympiad geometry with
  AlphaGeometry2.* JMLR 26, 2025.
- **Lin, Y. et al.** *Goedel-Prover: A Frontier Model for Open-Source Automated Formal Theorem
  Proving.* 2025. [arXiv:2502.07640](https://arxiv.org/abs/2502.07640)
- *Autoformalization in the Era of Large Language Models: A Survey.* 2025.
  [arXiv:2505.23486](https://arxiv.org/abs/2505.23486)
- **OpenAI.** *Ten Advances in Mathematics and Theoretical Computer Science.* Aug 2026.
  [openai/ten-proofs](https://github.com/openai/ten-proofs) ·
  [Paper](https://cdn.openai.com/pdf/ten-proofs-oai.pdf) ·
  [Reasoning walkthroughs](https://cdn.openai.com/pdf/reasoning-walkthroughs.pdf) — the ten results,
  and the Lean 4 certificates.
- **Lean FRO.** *Comparator* — [github.com/leanprover/comparator](https://github.com/leanprover/comparator) ·
  **nanoda**, an independent Rust kernel — [github.com/ammkrn/nanoda_lib](https://github.com/ammkrn/nanoda_lib)
- [lean-lsp-mcp](https://github.com/oOo0oOo/lean-lsp-mcp) — Lean as an agent-drivable tool.
- [mathlib statistics](https://leanprover-community.github.io/mathlib_stats.html) — ~288,041
  theorems, ~136,932 definitions, 772 contributors (Sept 2026).
- **Leiden Declaration on Artificial Intelligence and Mathematics**, June 2026.
  [Leiden University](https://www.universiteitleiden.nl/en/news/2026/06/leiden-declaration-warns-ai-is-challenging-the-core-values-of-mathematics) ·
  [PDF](https://zenodo.org/records/20302944) — the governance objection.
- **Benchmarks**: [miniF2F](https://github.com/openai/miniF2F) ·
  [ProofNet](https://github.com/zhangir-azerbayev/proofnet) ·
  [PutnamBench](https://trishullab.github.io/PutnamBench/) ·
  [VeriBench](https://cs.stanford.edu/people/brando9/professional_documents/papers/NeurIPS_2026_VeriBench.pdf)
  ⚠️
- **Harmonic.** *Aristotle* — gold-medal-equivalent IMO 2025 with Lean-verified proofs.
  ⚠️ Vendor claim from the arXiv abstract; verify before citing.
"""

R["docs/04-ai-era/fm-for-ai.md"] = """## References

- *Guardians of the Agents.* ACM Queue / CACM, 2025.
  [ACM Queue](https://queue.acm.org/detail.cfm?id=3762990) ·
  [CACM](https://cacm.acm.org/practice/guardians-of-the-agents/) — proof-carrying actions, and the
  credit-card-authorization analogy.
- **Wang, H. et al.** *AgentSpec: Customizable Runtime Enforcement for Safe and Reliable LLM Agents.*
  2025. [arXiv:2503.18666](https://arxiv.org/abs/2503.18666) ·
  [github.com/haoyuwang99/AgentSpec](https://github.com/haoyuwang99/AgentSpec)
- **AWS.** *Automated Reasoning checks in Amazon Bedrock Guardrails.*
  [Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html) ·
  [Concepts](https://docs.aws.amazon.com/bedrock/latest/userguide/automated-reasoning-checks-concepts.html) ·
  [AWS ML blog](https://aws.amazon.com/blogs/machine-learning/how-automated-reasoning-checks-in-amazon-bedrock-transform-generative-ai-compliance/)
- **VNN-COMP** — [vnn-comp.github.io](https://vnn-comp.github.io/) ·
  **α,β-CROWN** — **Wang, S. et al.** *Beta-CROWN: Efficient Bound Propagation with Per-neuron Split
  Constraints for Complete and Incomplete Neural Network Verification.* NeurIPS 2021.
  [github.com/Verified-Intelligence/alpha-beta-CROWN](https://github.com/Verified-Intelligence/alpha-beta-CROWN)
- **Katz, G. et al.** *The Marabou Framework for Verification and Analysis of Deep Neural Networks.*
  CAV 2019. [PDF](https://arxiv.org/abs/1905.11344)
- *Towards Formal Verification of LLM-Generated Code from Natural Language Prompts.* 2025.
  [arXiv:2507.13290](https://arxiv.org/abs/2507.13290)
- **Alshiekh, M. et al.** *Safe Reinforcement Learning via Shielding.* AAAI 2018;
  *Shields for Safe Reinforcement Learning*, CACM —
  [link](https://cacm.acm.org/research/shields-for-safe-reinforcement-learning/)
- **Necula, G.** *Proof-Carrying Code.* POPL 1997 — the original idea being reapplied to AI output.
  [PDF](https://www.cs.cmu.edu/~necula/Papers/pcc.pdf)
- **Clarkson, M. & Schneider, F.** *Hyperproperties.* CSF 2008 — why non-interference needs a
  different property class. [PDF](https://www.cs.cornell.edu/fbs/publications/Hyperproperties.pdf)
"""

R["docs/04-ai-era/verification-bottleneck.md"] = """## References

- **Anthropic.** *Eight trends defining how software gets built in 2026.* Jan 2026.
  [Link](https://claude.com/blog/eight-trends-defining-how-software-gets-built-in-2026) — the "~60%
  of work / 0–20% fully delegable" figure. ⚠️ **Vendor-published**; the gap is the point, not the
  precise number.
- **Newcombe, C. et al.** *Use of Formal Methods at Amazon Web Services.* 2014/2015.
  [PDF](https://lamport.azurewebsites.net/tla/formal-methods-amazon.pdf) — "optimisations we would
  not have dared to do".
- **AWS Security Blog.** *An Unexpected Discovery: Automated Reasoning Often Makes Systems More
  Efficient and Easier to Maintain.*
  [Link](https://aws.amazon.com/blogs/security/an-unexpected-discovery-automated-reasoning-often-makes-systems-more-efficient-and-easier-to-maintain/)
- **Amazon Science.** *How we built Cedar with automated reasoning and differential testing.*
  [Link](https://www.amazon.science/blog/how-we-built-cedar-with-automated-reasoning-and-differential-testing) —
  verification-guided development in production. ⚠️ The ~1 billion checks/day figure is
  AWS-published.
- **AWS.** *Automated Reasoning checks in Amazon Bedrock Guardrails.*
  [Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html) —
  a sound check shipped as a product feature.
- **powdr.** *Formally Verified Autoprecompiles.*
  [Link](https://powdr.org/blog/formally-verified-autoprecompiles) · **Alt, L.** *Performant
  Verified Software.* [Link](https://leoalt.de/performant-verified-software) — the review-bottleneck
  argument, with production numbers.
- **Lean FRO.** *Comparator* — [github.com/leanprover/comparator](https://github.com/leanprover/comparator) —
  the independent-judging layer for machine-generated proofs.
- **Kani** — [github.com/model-checking/kani](https://github.com/model-checking/kani) — push-button
  verification as a cargo subcommand.
- ⚠️ **DARPA CLARA** (~$48M, formal verification for aerospace control systems, 2026) — secondary
  sources only; verify before citing. See the [confidence ledger](../research-notes.md#4-confidence-ledger).
"""

R["docs/05-tools/catalog.md"] = r"""## References

Entry points for the tools catalogued above. Grouped as in the catalog.

**Proof assistants**
[Lean 4](https://lean-lang.org/) · [mathlib](https://leanprover-community.github.io/) ·
[Rocq (Coq)](https://rocq-prover.org/) · [Isabelle](https://isabelle.in.tum.de/) ·
[HOL4](https://hol-theorem-prover.org/) · [PVS](https://pvs.csl.sri.com/) ·
[ACL2](https://www.cs.utexas.edu/~moore/acl2/) · [Agda](https://wiki.portal.chalmers.se/agda/) ·
[Mizar](https://mizar.uwb.edu.pl/)

**Model checkers**
[TLA+](https://lamport.azurewebsites.net/tla/tla.html) · [Apalache](https://apalache-mc.org/) ·
[Alloy](https://alloytools.org/) · [SPIN](https://spinroot.com/) ·
[NuSMV](https://nusmv.fbk.eu/) · [mCRL2](https://www.mcrl2.org/) ·
[P](https://github.com/p-org/P) · [Stateright](https://github.com/stateright/stateright) ·
[PRISM](https://www.prismmodelchecker.org/) · [UPPAAL](https://uppaal.org/)

**Deductive verifiers**
[Dafny](https://dafny.org/) · [F*](https://fstar-lang.org/) · [Why3](https://why3.lri.fr/) ·
[Verus](https://verus-lang.github.io/verus/guide/) · [Creusot](https://github.com/creusot-rs/creusot) ·
[Prusti](https://github.com/viperproject/prusti-dev) · [Kani](https://github.com/model-checking/kani) ·
[CBMC](https://www.cprover.org/cbmc/) · [SPARK](https://www.adacore.com/sparkpro) ·
[OpenJML](https://www.openjml.org/) · [KeY](https://www.key-project.org/) ·
[Stainless](https://github.com/epfl-lara/stainless) · [Viper](https://viperproject.github.io/) ·
[Boogie](https://github.com/boogie-org/boogie) · [Frama-C](https://frama-c.com/)

**Abstract interpretation and sound static analysis**
[Astrée](https://www.absint.com/astree/) · [Polyspace](https://www.mathworks.com/products/polyspace.html) ·
[Frama-C/Eva](https://frama-c.com/fc-plugins/eva.html) · [CPAchecker](https://cpachecker.sosy-lab.org/) ·
[Infer](https://fbinfer.com/) · [MIRAI](https://github.com/facebookexperimental/MIRAI) ·
[IKOS](https://github.com/NASA-SW-VnV/ikos)

**Solvers**
[Z3](https://github.com/Z3Prover/z3) · [cvc5](https://cvc5.github.io/) ·
[Yices](https://yices.csl.sri.com/) · [MathSAT](https://mathsat.fbk.eu/) ·
[Bitwuzla](https://bitwuzla.github.io/) · [Alt-Ergo](https://alt-ergo.ocamlpro.com/) ·
[Vampire](https://vprover.github.io/) · [E](https://wwwlehre.dhbw-stuttgart.de/~sschulz/E/E.html) ·
[CaDiCaL](https://github.com/arminbiere/cadical) · [Kissat](https://github.com/arminbiere/kissat)

**Neural network verification**
[α,β-CROWN](https://github.com/Verified-Intelligence/alpha-beta-CROWN) ·
[Marabou](https://github.com/NeuralNetworkVerification/Marabou) ·
[ERAN](https://github.com/eth-sri/eran) · [VNN-COMP](https://vnn-comp.github.io/)

**Protocol and cryptographic verification**
[ProVerif](https://bblanche.gitlabpages.inria.fr/proverif/) ·
[Tamarin](https://tamarin-prover.github.io/) ·
[EasyCrypt](https://easycrypt.gitlabpages.inria.fr/) ·
[CryptoVerif](https://bblanche.gitlabpages.inria.fr/cryptoverif/) ·
[ct-verif / FaCT](https://github.com/PLSysSec/FaCT) ·
[HACL\* / EverCrypt](https://hacl-star.github.io/HaclValeEverCrypt.html) ·
[Cedar](https://www.cedarpolicy.com/)

**Agent and runtime enforcement**
[AgentSpec](https://github.com/haoyuwang99/AgentSpec) ·
[AWS Bedrock automated reasoning checks](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html) ·
[Comparator](https://github.com/leanprover/comparator)

**Lightweight and property-based**
[Hypothesis](https://hypothesis.readthedocs.io/) ·
[proptest](https://github.com/proptest-rs/proptest) · [fast-check](https://fast-check.dev/) ·
[jqwik](https://jqwik.net/) · [QuickCheck](https://hackage.haskell.org/package/QuickCheck) ·
[AFL++](https://github.com/AFLplusplus/AFLplusplus) · [OSS-Fuzz](https://github.com/google/oss-fuzz) ·
[KLEE](https://klee-se.org/) · [angr](https://angr.io/) ·
[Echidna](https://github.com/crytic/echidna) · [Foundry](https://book.getfoundry.sh/)

**AI for formal methods**
[lean-lsp-mcp](https://github.com/oOo0oOo/lean-lsp-mcp) · [LeanDojo](https://leandojo.org/) ·
[Goedel-Prover](https://arxiv.org/abs/2502.07640)
"""

R["docs/05-tools/choosing.md"] = """## References

- **Install and getting-started documentation** for the tools named on this page:
  [Lean/elan](https://leanprover-community.github.io/get_started.html) ·
  [TLA+ Toolbox and VS Code extension](https://lamport.azurewebsites.net/tla/tla.html) ·
  [Dafny](https://dafny.org/dafny/Installation) ·
  [Kani](https://model-checking.github.io/kani/install-guide.html) ·
  [CBMC](https://www.cprover.org/cbmc/) · [Z3](https://github.com/Z3Prover/z3) ·
  [Hypothesis](https://hypothesis.readthedocs.io/) ·
  [proptest](https://github.com/proptest-rs/proptest) ·
  [fast-check](https://fast-check.dev/) · [Rocq](https://rocq-prover.org/) ·
  [Isabelle](https://isabelle.in.tum.de/) · [Alloy](https://alloytools.org/)
  ⚠️ Install commands change; always check the project's own site.
- **Newcombe, C. et al.** *Use of Formal Methods at Amazon Web Services.* 2014/2015 — the
  "exhaustively testable pseudo-code" framing, and the argument that a tool must produce
  counterexamples to be adopted.
- **Lamport, L.** *Specifying Systems.* [Free online](https://lamport.azurewebsites.net/tla/book.html)
- **Kani** — [github.com/model-checking/kani](https://github.com/model-checking/kani) ·
  **CBMC** — [cbmc-documentation.readthedocs.io](https://cbmc-documentation.readthedocs.io/)
- **Alt, L.** *Ethereum formal verification overview* —
  [github.com/leonardoalt/ethereum_formal_verification_overview](https://github.com/leonardoalt/ethereum_formal_verification_overview) —
  a good model for how to write a tool *decision guide* rather than a tool list.
"""

R["docs/06-practice/adoption-playbook.md"] = """## References

- **Newcombe, C. et al.** *Use of Formal Methods at Amazon Web Services.* 2014/2015.
  [PDF](https://lamport.azurewebsites.net/tla/formal-methods-amazon.pdf) — every claim on this page
  about how adoption actually happened: "Debugging Designs", "exhaustively testable pseudo-code",
  starting from an incident, and the two kinds of win (bugs prevented, optimisations enabled).
- **Cousot, P. et al.** *The ASTRÉE Analyzer.* ESOP 2005.
  [PDF](https://pcousot.github.io/CousotEtAl-ESOP05.pdf) — the assumptions-and-limitations section as
  an engineering artifact.
- **Woodcock, J. et al.** *Formal Methods: Practice and Experience.* ACM CSUR 41(4), 2009.
  [ACM](https://dl.acm.org/doi/10.1145/1592434.1592436) — what industrial deployments look like in
  practice, including the organisational conditions.
- **Barnett, M. et al.** *Boogie*; **Leino, K.R.M.** *Dafny* — the annotation-burden reality behind
  rung 4, and why loop invariants are the cost centre.
- **Kani** — [github.com/model-checking/kani](https://github.com/model-checking/kani) ·
  [Kani book](https://model-checking.github.io/kani/) — a CI-ready verifier, i.e. one that does not
  require changing languages.
- **Hypothesis** — [hypothesis.readthedocs.io](https://hypothesis.readthedocs.io/) — rung 1–2.
- **Klein, G. et al.** *seL4: Formal Verification of an OS Kernel.* SOSP 2009 — re-verification cost
  after the initial proof.
- **Lean FRO.** [Comparator](https://github.com/leanprover/comparator) — the "verify the claim, not
  just the proof" discipline that rung 3's CI gate should include.
"""

R["docs/06-practice/objections.md"] = """## References

- **Rice, H.G.** *Classes of Recursively Enumerable Sets and Their Decision Problems.* 1953 —
  "Gödel proved we can never verify software" and the decidability objection.
  [PDF](https://www.ams.org/journals/tran/1953-074-02/S0002-9947-1953-0053041-6/S0002-9947-1953-0053041-6.pdf)
- **Gödel, K.** 1931. [Stanford Encyclopedia](https://plato.stanford.edu/entries/goedel-incompleteness/)
- **Newcombe, C. et al.** *Use of Formal Methods at Amazon Web Services.* 2014/2015.
  [PDF](https://lamport.azurewebsites.net/tla/formal-methods-amazon.pdf) — the cost objection, the
  enabler reframe, and the design-versus-code argument.
- **Woodcock, J. et al.** *Formal Methods: Practice and Experience.* ACM CSUR 41(4), 2009 — the
  "academic and unusable" objection, addressed with deployment data.
  [ACM](https://dl.acm.org/doi/10.1145/1592434.1592436)
- **Protzenko, J. et al.** *EverCrypt.* IEEE S&P 2020 —
  [hacl-star.github.io](https://hacl-star.github.io/HaclValeEverCrypt.html) — "don't roll your own
  crypto".
- **Klein, G. et al.** SOSP 2009; **Cousot, P. et al.** ESOP 2005 — maintenance and re-verification.
- **Alt, L.** *Performant Verified Software.* 2026.
  [Link](https://leoalt.de/performant-verified-software) — "isn't this more process?" and the
  verification-as-speed-enabler answer.
- **Klingner, T. et al.** *A comparison of LLMs' effectiveness in producing formal proofs in Lean 4.*
  [arXiv:2606.05632](https://arxiv.org/abs/2606.05632) — the "AI can just verify things" objection.
- **Lean FRO.** [Comparator](https://github.com/leanprover/comparator) — statement mismatch, the
  failure mode behind "you're overselling AI".
- **Amazon Science.** *How we built Cedar with automated reasoning and differential testing.*
  [Link](https://www.amazon.science/blog/how-we-built-cedar-with-automated-reasoning-and-differential-testing)
"""

R["docs/references/glossary.md"] = """## References

This glossary defines terms introduced across the wiki; the authoritative sources are on the pages
where each term is used. The primary references for the definitions most often looked up here:

- **Hoare, C.A.R.** CACM 1969 — precondition, postcondition, partial correctness.
- **Dijkstra, E.W.** CACM 1975 — weakest precondition, verification condition.
- **Floyd, R.** 1967 — invariant, as an annotation on a flowchart.
- **Cousot, P. & Cousot, R.** POPL 1977 — abstraction, abstract domain, false alarm.
- **Kahn, G.** STACS 1987; **Plotkin, G.** 1981 — big-step and small-step, and the derivation-based
  proof principles behind them.
- **Clarke & Emerson** 1981; **Pnueli, A.** 1977 — safety, liveness, temporal operators.
- **Emerson & Halpern** 1983 — LTL, CTL, CTL*.
- **Kozen, D.** 1983 — μ-calculus.
- **Reynolds, J.C.** 2002; **O'Hearn, P. et al.** 2001 — separation logic, frame rule, footprint.
- **Rice, H.G.** 1953 — soundness/completeness trade-off.
- **de Bruijn, N.G.** 1980 — trusted base, de Bruijn criterion.
- **Necula, G.** POPL 1997 — proof-carrying code.
- **Clarkson, M. & Schneider, F.** CSF 2008 — hyperproperty, non-interference.
- **Wang, S. et al.** NeurIPS 2021 — certified robustness.
- **Alshiekh, M. et al.** AAAI 2018 — shields.
- **Wang, H. et al.** 2025 ([arXiv:2503.18666](https://arxiv.org/abs/2503.18666)) — runtime
  enforcement for agents.
- **Wright, A. & Felleisen, M.** 1994 — progress and preservation.
- [SAT solver](https://en.wikipedia.org/wiki/SAT_solver) ·
  [SMT](https://en.wikipedia.org/wiki/Satisfiability_modulo_theories) ·
  [Operational semantics](https://en.wikipedia.org/wiki/Operational_semantics) ·
  [Separation logic](https://en.wikipedia.org/wiki/Separation_logic) ·
  [Abstract interpretation](https://en.wikipedia.org/wiki/Abstract_interpretation) —
  for the survey-level definitions.
"""


def insert(text: str, block: str) -> str:
    """Insert the References block before `## Further reading`, else at the end."""
    m = re.search(r"^##\s+Further reading\s*$", text, re.MULTILINE)
    if m:
        return text[: m.start()] + block.rstrip() + "\n\n" + text[m.start() :]
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def main() -> None:
    changed = skipped = missing = 0
    for path, block in R.items():
        p = Path(path)
        if not p.exists():
            print(f"  !! missing file: {path}")
            missing += 1
            continue
        text = p.read_text(encoding="utf-8")
        if re.search(r"^##\s+References\s*$", text, re.MULTILINE):
            print(f"  -- already has References: {path}")
            skipped += 1
            continue
        p.write_text(insert(text, block), encoding="utf-8")
        print(f"  ++ {path}")
        changed += 1
    print(f"\n{changed} updated, {skipped} skipped, {missing} missing files")


if __name__ == "__main__":
    main()
