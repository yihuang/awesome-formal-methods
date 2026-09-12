# Bibliography

Organised for usefulness, not completeness. ⭐ = the highest-value items.

---

## The five things to read if you read nothing else

1. ⭐ **Newcombe, Rath, Zhang, Munteanu, Brooker, Deardeuff — *Use of Formal Methods at Amazon Web
   Services*** (2014; CACM version 2015). The single best practitioner document in the field, and
   the source of half the quotes in this wiki.
   [PDF](https://lamport.azurewebsites.net/tla/formal-methods-amazon.pdf) ·
   [CACM](https://cacm.acm.org/research/how-amazon-web-services-uses-formal-methods/)
2. ⭐ **Amazon Science — *How we built Cedar with automated reasoning and differential testing*.**
   The most transferable industrial pattern: prove a model, differentially test the code.
   [link](https://www.amazon.science/blog/how-we-built-cedar-with-automated-reasoning-and-differential-testing)
3. ⭐ **AlphaProof, *Nature* (Nov 2025)** — *Olympiad-level formal mathematical reasoning with
   reinforcement learning*. The reference architecture for AI + formal verification.
   [link](https://www.nature.com/articles/s41586-025-09833-y)
4. ⭐ **verifiedsoftware.dev — Case Studies.** Concise, numbers-first summaries of seL4, CompCert,
   Cedar, SymCrypt, Veil. [link](https://verifiedsoftware.dev/case-studies/)
5. **Clarke & Wing — *Formal Methods: State of the Art and Future Directions*, ACM Computing
   Surveys (1996)** + **Woodcock, Larsen, Bicarregui, Fitzgerald — *Formal Methods: Practice and
   Experience*, ACM Computing Surveys (2009)**. The field's own adoption self-assessment.

---

## Foundations — logic and verification

- Hoare, C.A.R. — *An Axiomatic Basis for Computer Programming* (CACM, 1969). The Hoare triple.
- Floyd, R. — *Assigning Meanings to Programs* (1967). Pre/post-conditions.
- Dijkstra, E.W. — *Guarded Commands, Nondeterminacy and Formal Derivation of Programs* (CACM,
  1975). Weakest preconditions.
- Dijkstra, E.W. — *A Discipline of Programming* (1976). The book-length version.
- Turing, A.M. — *Checking a Large Routine* (1949). Possibly the first program-correctness proof.
- Gödel, K. — *Über formal unentscheidbare Sätze…* (1931).
- Turing, A.M. — *On Computable Numbers…* (1936).
- Rice, H.G. — *Classes of Recursively Enumerable Sets and Their Decision Problems* (1953).
- Cousot, P. & Cousot, R. — *Abstract Interpretation: A Unified Lattice Model for Static Analysis
  of Programs…* (POPL 1977). [Intro overview](https://www.di.ens.fr/~cousot/AI/IntroAbsInt.html)
- Pnueli, A. — *The Temporal Logic of Programs* (1977).
- Clarke, E.M. & Emerson, E.A. — *Design and Synthesis of Synchronization Skeletons Using
  Branching-Time Temporal Logic* (1981); Queille & Sifakis (1982). Model checking.
- Reynolds, J.C. — *Separation Logic: A Logic for Shared Mutable Data Structures* (2002);
  O'Hearn, Reynolds, Yang — *Local Reasoning about Programs that Alter Data Structures* (2001).
- Lamport, L. — *Specifying Systems* (the TLA+ book, free online).
- Pierce, B. — *Software Foundations* (Coq/Rocq) and *Types and Programming Languages*.
- Nipkow, Klein — *Concrete Semantics* (Isabelle).
- Harrison, J. — *Handbook of Practical Logic and Automated Reasoning*.

---

## Solvers and automated reasoning

- Marques-Silva & Sakallah — *GRASP: A Search Algorithm for Propositional Satisfiability* (1996).
- Bayardo & Schrag — *Using CSP Look-Back Techniques to Solve Real-World SAT Instances* (1997).
- Moskewicz et al. — *Chaff: Engineering an Efficient SAT Solver* (DAC 2001).
- Eén & Sörensson — *An Extensible SAT-solver* (MiniSat, 2003).
- de Moura & Bjørner — *Z3: An Efficient SMT Solver* (TACAS 2008).
- Barbosa et al. — *cvc5: A Versatile and Industrial-Strength SMT Solver* (TACAS 2022).
- Barrett, Sebastiani, Seshia, Tinelli — *Satisfiability Modulo Theories* (Handbook of
  Satisfiability, 2021).
- Wetzler, Heule, Hunt — *DRAT-trim: Efficient Checking and Trimming Using Expressive Clausal
  Proofs* (2014). Proof logging.

---

## Industrial case studies

- Klein et al. — *seL4: Formal Verification of an OS Kernel* (SOSP 2009).
- Leroy, X. — *Formal Verification of a Realistic Compiler* (CACM 2009).
- Yang, Chen, Eide, Regehr — *Finding and Understanding Bugs in C Compilers* (PLDI 2011). The
  Csmith study.
- Cousot et al. — *The ASTRÉE Analyzer* (ESOP 2005).
- Newcombe et al. — *How Amazon Web Services Uses Formal Methods* (CACM 2015).
- CACM — *Systems Correctness Practices at Amazon Web Services* (2025).
  [link](https://cacm.acm.org/practice/systems-correctness-practices-at-amazon-web-services/)
- Hawblitzel et al. — *IronFleet: Proving Practical Distributed Systems Correct* (SOSP 2015).
- Wilcox et al. — *Verdi: A Framework for Verifying Distributed Systems* (PLDI 2015).
- Protzenko et al. — *EverCrypt: A Fast, Verified, Cross-Platform Cryptographic Provider*
  (S&P 2020). [hacl-star.github.io](https://hacl-star.github.io/HaclValeEverCrypt.html)
- Delmas et al. — *Kani: A Model Checker for Rust* (ASE 2026).
  [github.com/model-checking/kani](https://github.com/model-checking/kani)
- Cutler et al. — *Cedar: A New Language for Expressive, Fast, Safe, and Analyzable Authorization*
  (OOPSLA 2024).

---

## Safety-critical and standards

- RTCA DO-178C — *Software Considerations in Airborne Systems and Equipment Certification*.
  [rtca.org](https://www.rtca.org/do-178/)
- RTCA DO-333 — *Formal Methods Supplement to DO-178C and DO-278A*.
- RTCA DO-330 — *Software Tool Qualification Considerations*.
- ISO 26262 — automotive functional safety.
- IEC 61508 — generic functional safety.
- EN 50128 — railway applications software.
- Bicarregui, Fitzgerald, Larsen, Woodcock — *Industrial Practice in Formal Methods* (FM 2009).

---

## AI era — AI for formal methods

- Polu & Sutskever — *Generative Language Modeling for Automated Theorem Proving* (GPT-f, 2020).
- Yang et al. — *LeanDojo: Theorem Proving with Retrieval-Augmented Language Models* (NeurIPS
  2023). [lean-dojo.github.io](https://leandojo.org/)
- AlphaProof & AlphaGeometry teams — *AI achieves silver-medal standard solving International
  Mathematical Olympiad problems* (DeepMind, July 2024).
  [link](https://deepmind.google/blog/ai-solves-imo-problems-at-silver-medal-level/)
- Hubert et al. — *Olympiad-level formal mathematical reasoning with reinforcement learning*,
  *Nature* (2025). [link](https://www.nature.com/articles/s41586-025-09833-y)
- Ren et al. — *DeepSeek-Prover-V2* (2025).
- Lin et al. — *Goedel-Prover: A Frontier Model for Open-Source Automated Formal Theorem Proving*
  (2025). [arXiv:2502.07640](https://arxiv.org/abs/2502.07640)
- *Autoformalization in the Era of Large Language Models: A Survey* (2025).
  [arXiv:2505.23486](https://arxiv.org/abs/2505.23486)
- *Towards a Common Framework for Autoformalization* (2026).
- **OpenAI — *Ten Advances in Mathematics and Theoretical Computer Science*** (Aug 2026), with Lean
  4 formalisations. [github.com/openai/ten-proofs](https://github.com/openai/ten-proofs) ·
  [paper PDF](https://cdn.openai.com/pdf/ten-proofs-oai.pdf) ·
  [reasoning walkthroughs](https://cdn.openai.com/pdf/reasoning-walkthroughs.pdf)
- **Lean FRO — Comparator**: a trustworthy judge for Lean proofs.
  [github.com/leanprover/comparator](https://github.com/leanprover/comparator) ·
  [nanoda](https://github.com/ammkrn/nanoda_lib) (independent Rust kernel)
- mathlib statistics. [link](https://leanprover-community.github.io/mathlib_stats.html)

## AI era — formal methods for AI

- *Guardians of the Agents* — ACM Queue / CACM (2025). Proof-carrying actions for AI agents.
  [ACM Queue](https://queue.acm.org/detail.cfm?id=3762990) ·
  [CACM](https://cacm.acm.org/practice/guardians-of-the-agents/)
- Wang et al. — *AgentSpec: Customizable Runtime Enforcement for Safe and Reliable LLM Agents*
  (2025). [arXiv:2503.18666](https://arxiv.org/abs/2503.18666)
- *Towards Formal Verification of LLM-Generated Code from Natural Language Prompts* (2025).
  [arXiv:2507.13290](https://arxiv.org/abs/2507.13290)
- *VeriBench* (NeurIPS 2026).
- AWS — *Automated Reasoning checks in Amazon Bedrock Guardrails*.
  [docs](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html)
- *Shields for Safe Reinforcement Learning*, CACM.
  [link](https://cacm.acm.org/research/shields-for-safe-reinforcement-learning/)
- Wang et al. — *α,β-CROWN: Efficient Bound Propagation with Per-neuron Split Constraints for
  Complete Neural Network Verification* (NeurIPS 2021).
  [VNN-COMP](https://vnn-comp.github.io/) ·
  [github](https://github.com/Verified-Intelligence/alpha-beta-CROWN)
- Katz et al. — *The Marabou Framework for Verification and Analysis of Deep Neural Networks*
  (CAV 2019).
- **Leiden Declaration on Artificial Intelligence and Mathematics** (June 2026).
  [Leiden University](https://www.universiteitleiden.nl/en/news/2026/06/leiden-declaration-warns-ai-is-challenging-the-core-values-of-mathematics) ·
  [PDF](https://zenodo.org/records/20302944)
- Anthropic — *Eight trends defining how software gets built in 2026*.
  [link](https://claude.com/blog/eight-trends-defining-how-software-gets-built-in-2026)
  (⚠️ vendor source; the "60% use / 0–20% fully delegate" figure)

---

## History and context

- MacKenzie, D. — *Mechanizing Proof: Computing, Risk, and Trust* (2001). The sociology of the
  field; unusually honest about why adoption is hard.
- Davis, M. — *The Universal Computer* (2000). The logic lineage.
- Newell, Shaw, Simon — *Empirical Explorations with the Logic Theory Machine* (1957). The first AI
  program.
- Wikipedia: [Formal methods](https://en.wikipedia.org/wiki/Formal_methods) ·
  [Model checking](https://en.wikipedia.org/wiki/Model_checking) ·
  [Hoare logic](https://en.wikipedia.org/wiki/Hoare_logic) ·
  [Separation logic](https://en.wikipedia.org/wiki/Separation_logic) ·
  [Satisfiability modulo theories](https://en.wikipedia.org/wiki/Satisfiability_modulo_theories) ·
  [Pentium FDIV bug](https://en.wikipedia.org/wiki/Pentium_FDIV_bug) ·
  [Gödel's incompleteness theorems](https://en.wikipedia.org/wiki/G%C3%B6del%27s_incompleteness_theorems) ·
  [Leiden Declaration](https://en.wikipedia.org/wiki/Leiden_Declaration_on_Artificial_Intelligence_and_Mathematics)

---

## Courses and learning resources

| Resource | Notes |
|---|---|
| **Lamport's TLA+ video course** | [lamport.azurewebsites.net/video/videos.html](https://lamport.azurewebsites.net/video/videos.html) — the fastest way to learn TLA+ |
| **Hillel Wayne's *Learn TLA+*** | [learntla.com](https://learntla.com/) — engineer-friendly, practical |
| **Software Foundations** (Pierce et al.) | Rocq/Coq from scratch; the standard proof-assistant course |
| **Theorem Proving in Lean 4** | [leanprover.github.io/theorem_proving_in_lean4](https://leanprover.github.io/theorem_proving_in_lean4/) |
| **Mathematics in Lean** | mathlib-oriented, practical |
| **Dafny tutorial + `dafny verify`** | the gentlest industrial entry point |
| **Kani tutorial** | [model-checking.github.io/kani](https://model-checking.github.io/kani/) |
| **Cousot's abstract interpretation intro** | [di.ens.fr/~cousot/AI/IntroAbsInt.html](https://www.di.ens.fr/~cousot/AI/IntroAbsInt.html) |
| **TLA+ specs in the wild** | Paxos, Raft, and many cloud protocols are published; reading them is the fastest way to learn specification style |
