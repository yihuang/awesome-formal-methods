# Quote bank

Sourced and attributed, grouped by theme.

---

## The hook

> "In 1956, the first AI program ever written proved theorems in *Principia Mathematica*. It was
> called Logic Theorist. **The first thing we asked a computer to do with 'intelligence' was formal
> reasoning.**"
> — Newell, Shaw & Simon, *Empirical Explorations with the Logic Theory Machine* (1957)

---

## The cost objection (use these together — they're the strongest pair here)

> "In industry, formal methods have a reputation of requiring a huge amount of training and effort
> to verify a tiny piece of relatively straightforward code, so the return on investment is only
> justified in safety-critical domains such as medical systems and avionics. **Our experience with
> TLA+ has shown that perception to be quite wrong.**"
> — *Use of Formal Methods at Amazon Web Services*

> "**In several cases we have prevented subtle, serious bugs from reaching production. In other
> cases we have been able to make innovative performance optimizations — e.g. removing or narrowing
> locks, or weakening constraints on message ordering — which we would not have dared to do without
> having model checked those changes.**"
> — *Use of Formal Methods at Amazon Web Services*

**Why these two together:** the first kills the cost objection; the second reframes FM from
insurance to *enabler*. The second quote is the one that gets budgets approved, because it's a
speed argument, not a safety argument.

---

## The adoption framing (steal these verbatim)

> "Engineers think in terms of debugging rather than 'verification', so we called the presentation
> **'Debugging Designs'**."
> — *Use of Formal Methods at Amazon Web Services*

> "(Software engineers) more readily grasp the concept and practical value of TLA+ if we dub it:
> **Exhaustively testable pseudo-code**."
> — *Use of Formal Methods at Amazon Web Services*

> "Most recently we discovered that TLA+ is an excellent tool for **data modeling**, e.g. designing
> the schema for a relational or 'No SQL' database."
> — *Use of Formal Methods at Amazon Web Services*

---

## Why designs, not code (the core insight)

> "**If the design is broken then the code is almost certainly broken**, as mistakes during coding
> are extremely unlikely to compensate for mistakes in design. Worse, engineers will probably be
> deceived into believing that the code is 'correct' because it appears to correctly implement the
> (broken) design."
> — *Use of Formal Methods at Amazon Web Services*

> "We have found this rigorous **'what needs to go right?'** approach to be significantly less error
> prone than the ad hoc **'what might go wrong?'** approach."
> — *Use of Formal Methods at Amazon Web Services*

> "Formal methods help engineers to get the design right, which is a necessary first step toward
> getting the code right."
> — *Use of Formal Methods at Amazon Web Services*

---

## Scope honesty

> "(We care about) 1) bugs and operator errors that cause a departure from the logical intent of the
> system, and 2) surprising 'sustained emergent performance degradation' of complex systems that
> inevitably contain feedback loops."
> — *Use of Formal Methods at Amazon Web Services* — **formal methods address (1), not (2)**

> "Formal methods deal with models of systems, not the systems themselves, so the adage applies:
> **'All models are wrong, some are useful.'**"
> — *Use of Formal Methods at Amazon Web Services*

---

## Why AI needs formal methods

> "The soundness of this process is guaranteed by Lean's kernel, which verifies that the generated
> proof term is a valid construction."
> — AlphaProof, *Nature* (2025)

> "**Even a mis-formalized statement, regardless of its fidelity to the original natural-language
> problem, provides a valid formal problem** that AlphaProof can attempt to prove or disprove, thus
> serving as a useful training instance."
> — AlphaProof, *Nature* (2025) — the insight that unlocked 80M training problems

> "**Rigorously verifying the correctness of their reasoning remains (a challenge)**" for
> natural-language models, whereas "the inherent verification capabilities of formal systems
> provide the necessary foundation for building AI agents whose reasoning process and outputs can
> be trusted, **even when exploring beyond the boundaries of existing human proofs and training
> data**."
> — AlphaProof, *Nature* (2025)

> "The two combinatorics problems remained unsolved."
> — AlphaProof, *Nature* (2025) — **use this. The honesty is what makes the rest credible.**

---

## Why AI makes formal methods necessary

> "We are required to generate formal proofs demonstrating the safety of planned actions before
> being authorized to execute them. **This approach parallels existing real-world practices (e.g.
> credit card checks before a transaction is authorized).**"
> — *Guardians of the Agents*, ACM Queue (2025)

> "Cryptographic bugs don't crash your program — they silently compromise security. **A single
> incorrect bit operation can reduce a 256-bit key to trivially breakable.**"
> — on verified cryptography (SymCrypt / HACL\*)

> "(Engineers) report being able to **'fully delegate' only 0–20% of tasks**" while using AI in
> "roughly 60% of their work."
> — Anthropic, *Eight trends defining how software gets built in 2026* ⚠️ *(vendor source; the gap
> is the point, not the precise number)*

---

## The AI-era thesis (in one line each)

> "**AI is a search amplifier. Formal verification is a cheap, sound filter.**"
> — this wiki, [automated-reasoning.md](../01-fundamentals/automated-reasoning.md)

> "**AI made code cheap and trust expensive.**"
> — this wiki, [verification-bottleneck.md](../04-ai-era/verification-bottleneck.md)

> "**Let the LLM propose; let the machine dispose.**"
> — this wiki, [ai-for-fm.md](../04-ai-era/ai-for-fm.md)

> "**The proof is machine-checked. That's not the same as the result being accepted.**"
> — on the 2026 disputes over attribution and process, not correctness

---

## Eyebrow-raising numbers (each needs its source)

| Number | Claim | Source |
|---|---|---|
| **8,700** vs **200,000** | lines of C vs lines of Isabelle proof in seL4 | [verifiedsoftware.dev](https://verifiedsoftware.dev/case-studies/) |
| **~20 person-years** | original seL4 verification effort | same |
| **0** | wrong-code bugs found in CompCert by the Csmith study | Yang et al., PLDI 2011 |
| **hundreds** | wrong-code bugs found in GCC and LLVM by the same study | same |
| **132,000** | lines of C in the Airbus A340 fly-by-wire code proved free of runtime errors by Astrée | Cousot et al., ESOP 2005 |
| **~1 billion/day** | automated-reasoning checks in Cedar ⚠️ | AWS material |
| **28 / 42** | AlphaProof + AlphaGeometry 2 score at IMO 2024 (silver range, 1 point below gold) | DeepMind / *Nature* |
| **~1M → ~80M** | informal problems autoformalized into formal Lean problems for AlphaProof | AlphaProof, *Nature* |
| **~300,000** | human state–tactic pairs used to bootstrap the proof network | same |
| **3 billion** | parameters in AlphaProof's proof network | same |
| **288,041 / 136,932 / 772** | mathlib theorems / definitions / contributors (Sept 2026) | [mathlib stats](https://leanprover-community.github.io/mathlib_stats.html) |
| **10** | new research results announced by OpenAI in Aug 2026, each open ≥10 years, with Lean certificates | [openai/ten-proofs](https://github.com/openai/ten-proofs) |
| **~$2,000** ⚠️ | reported API cost for all ten OpenAI results | secondary reporting — **verify before sliding** |
| **1994** | Pentium FDIV bug; a ~$475M-class event that made FM standard in silicon | [Wikipedia](https://en.wikipedia.org/wiki/Pentium_FDIV_bug) |

---

## Nature's agreement quote

> "The fact that the program can come up with a non-obvious construction like this is very
> impressive, and well beyond what I thought was state of the art."
> — Prof Sir Timothy Gowers, IMO gold medallist and Fields Medallist, on AlphaProof's IMO 2024
> solutions ([DeepMind](https://deepmind.google/blog/ai-solves-imo-problems-at-silver-level/))

A Fields Medallist saying "beyond what I thought was state of the art" is the best
social-proof-per-word in the wiki.

---

## The closing three

Pick one. Don't use all three.

> "**Formal methods cannot tell you what to want. They can tell you, with certainty, whether what
> you asked for is what you'll get — and show you the exact input where it isn't.**"

> "**AI made code free. It didn't make correctness free. That gap is the next decade of
> engineering.**"

> "**The first AI program was a theorem prover. The most valuable AI systems of the next decade may
> well be the ones that verify.**"

---

## The one quotation to avoid

Don't quote Dijkstra's "Program testing can be used to show the presence of bugs, but never to show
their absence" unless you're ready to defend it. It's true, it's famous, and it's been used to
dismiss testing so many times that engineers reflexively discount it. Use this instead:

> "Testing is necessary and stays necessary. The question is what it structurally cannot do:
> quantify over all inputs, all interleavings, and all adversary perturbations."

## References

Every quotation on this page is attributed inline. The underlying documents:

- **Newell, A., Shaw, J.C., Simon, H.** *Empirical Explorations with the Logic Theory Machine.* 1957
  — Logic Theorist.
- **Newcombe, C., Rath, T., Zhang, F., Munteanu, B., Brooker, M., Deardeuff, M.** *Use of Formal
  Methods at Amazon Web Services.* 2014/2015.
  [PDF](https://lamport.azurewebsites.net/tla/formal-methods-amazon.pdf) — the cost objection, the
  "perception is quite wrong" line, the "Debugging Designs" framing, the "exhaustively testable
  pseudo-code" framing, the design-versus-code argument, the "what needs to go right" inversion,
  the two-kinds-of-win quotation, the data-modelling aside, and the "all models are wrong" line.
- **Hubert, T. et al.** *Olympiad-level formal mathematical reasoning with reinforcement learning.*
  *Nature*, 2025. [Link](https://www.nature.com/articles/s41586-025-09833-y) — the kernel-soundness
  quotation, the mis-formalized-statement insight, the "rigorously verifying... remains a challenge"
  quotation, and the honest "combinatorics problems remained unsolved" line.
- **DeepMind.** *AI achieves silver-medal standard solving International Mathematical Olympiad
  problems.* 2024. [Link](https://deepmind.google/blog/ai-solves-imo-problems-at-silver-medal-level/) —
  the Timothy Gowers quotation.
- *Guardians of the Agents.* ACM Queue, 2025.
  [Link](https://queue.acm.org/detail.cfm?id=3762990) — the proof-carrying-actions and
  credit-card-analogy quotation.
- **Anthropic.** *Eight trends defining how software gets built in 2026.*
  [Link](https://claude.com/blog/eight-trends-defining-how-software-gets-built-in-2026) — the
  delegation figure. ⚠️ Vendor-published.
- **Microsoft SymCrypt** — [github.com/microsoft/SymCrypt](https://github.com/microsoft/SymCrypt) —
  the "single incorrect bit operation" line. ⚠️ Vendor material.
- **powdr.** *Formally Verified Autoprecompiles.*
  [Link](https://powdr.org/blog/formally-verified-autoprecompiles); **Alt, L.** *Performant Verified
  Software.* [Link](https://leoalt.de/performant-verified-software) — "the proof is the review".
- **Yang, X., Chen, Y., Eide, E., Regehr, J.** *Finding and Understanding Bugs in C Compilers.*
  PLDI 2011 — the Csmith numbers.
- **Klein, G. et al.** *seL4: Formal Verification of an OS Kernel.* SOSP 2009 — the
  8,700/200,000/~20 person-year figures.
- **Cousot, P. et al.** *The ASTRÉE Analyzer.* ESOP 2005 — the ~132,000 lines of Airbus C.
- [mathlib statistics](https://leanprover-community.github.io/mathlib_stats.html)
- [openai/ten-proofs](https://github.com/openai/ten-proofs)
- [Pentium FDIV bug](https://en.wikipedia.org/wiki/Pentium_FDIV_bug)
- **Dijkstra, E.W.** *Notes on Structured Programming.* 1970 — the testing quotation that this page
  deliberately advises against over-using.
