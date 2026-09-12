# History — index

| Page | Contents |
|---|---|
| [timeline.md](timeline.md) | Dated table 1666→2026, with "why it matters" for each entry |
| [narrative.md](narrative.md) | The story-shaped version: three acts, one twist, one moral |

## The three-act summary

| Act | Years | Story |
|---|---|---|
| **I** | 1931–1977 | Undecidability is proved three times; Floyd/Hoare/Dijkstra build the ladder anyway; abstract interpretation and model checking are the two principled retreats. |
| **II** | 1977–2019 | FM gets good and ships in silicon, avionics, microkernels, compilers, crypto, and cloud control planes — invisibly. |
| **III** | 2020–2026 | AI makes proof *search* a learning problem and makes code *generation* cheap, so verification becomes the bottleneck and the product. |

## The twist to lead with

**Logic Theorist (1956), the first AI program ever written, was a theorem prover.**
AI and formal methods share an origin; the current convergence is a reunion, not a merger of
strangers.

## Key primary sources for this section

- Clarke & Wing, *Formal Methods: State of the Art and Future Directions*, ACM Computing Surveys
  (1996) — the field's self-assessment at the end of Act II's first phase.
- Woodcock, Larsen, Bicarregui, Fitzgerald, *Formal Methods: Practice and Experience*, ACM
  Computing Surveys (2009) — the industrial case-study survey; strongest source for the
  "it shipped, quietly" claim.
- Newcombe et al., *Use of Formal Methods at Amazon Web Services* (2014/2015) — the practitioner
  voice Act II needs. [PDF](https://lamport.azurewebsites.net/tla/formal-methods-amazon.pdf)
- Klein et al., *seL4: Formal Verification of an OS Kernel*, SOSP (2009).
- Leroy, *Formal Verification of a Realistic Compiler*, CACM (2009).
- Yang et al., *Finding and Understanding Bugs in C Compilers*, PLDI (2011) — the Csmith study.
- Cousot et al., *The ASTRÉE Analyzer*, ESOP (2005).

⚠️ *Items flagged in the timeline still need a source check before you rely on them; see
[RESEARCH-NOTES.md](../research-notes.md).*

## References

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
