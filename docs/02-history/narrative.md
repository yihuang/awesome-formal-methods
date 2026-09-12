# The narrative arc

[timeline.md](timeline.md) gives the dates. This page gives the *story* — three acts, one twist,
one moral. Same history, told so that its shape is visible.

---

## The hook (30 seconds)

> "In 1956, a program called Logic Theorist proved 38 of the first 52 theorems in *Principia
> Mathematica*. It is generally considered **the first AI program ever written.**
>
> It was a theorem prover.
>
> Which means: the first thing we ever asked a computer to do with 'intelligence' was **formal
> reasoning**. Seventy years later we're back here — except now the prover is a neural network and
> the checker is a proof kernel. The interesting part is the loop between those two things."

That's the twist most readers don't expect, and it reframes the whole subject: **AI and formal
methods are not rivals.** They were born in the same room.

---

## Act I — We found the ceiling, then built a ladder anyway (1931–1975)

**Beat 1. The ceiling.** In five years the foundational dream got hit three times:

- **1931 Gödel:** no consistent, expressive, effective system proves all truths.
- **1936 Turing/Church:** no algorithm decides whether any program halts.
- **1953 Rice:** *every* non-trivial semantic property of programs is undecidable.

**Key point:** the word "undecidable" appearing three times. Let it sink in.

> "So the mathematically honest position in 1953 was: verification is impossible. And then a bunch
> of people did it anyway."

**Beat 2. The insight that saved the field.** You can't decide properties of *arbitrary* programs.
But real programs aren't arbitrary — they're small, structured, and come with a human who knows
what they're supposed to do. So:

- **1967 Floyd:** annotate the program with assertions.
- **1969 Hoare:** triples `{P}C{Q}` — reasoning as a logic, not an art.
- **1975 Dijkstra:** `wp(C,Q)` — turn the logic into an *algorithm*.

**Key point:** the Hoare triple, large, with the assignment axiom. This 4-line rule set is the
most reused artifact in the field.

> "The ladder they built has one missing rung: the loop invariant. You have to supply it. There is
> no algorithm for finding it — Rice's theorem again. **Hold that thought — it's the rung AI is
> now climbing.**"

Also worth placing here, because it surprises people: **1949, Turing, "Checking a Large
Routine."** Formal verification predates the term "software engineering."

**Beat 3. Two escapes from undecidability.** Rather than give up, the field found two places where
you *can* decide things:

- **Abstract interpretation (1977, Cousot & Cousot):** over-approximate, so you always terminate —
  sound, incomplete, and it scales to millions of lines.
- **Model checking (1981–82, Clarke & Emerson; Queille & Sifakis):** restrict to *finite* models,
  then search exhaustively — you get a counterexample, not a shrug.

*Moral of Act I:* **every practical verification tool is a deliberate, principled retreat from
undecidability.** That's not a compromise; it's the design space.

---

## Act II — It worked, and you didn't notice (1977–2019)

The middle act is a heist movie: formal methods got very good at a few things and shipped them
everywhere, mostly invisibly.

**Beat 4. Silicon first, because you can't patch a chip.**

- **1994: Pentium FDIV.** A division-table bug in floating-point hardware. Public, expensive,
  and it changed industry behaviour: formal equivalence checking became standard practice in chip
  design, and Intel's own floating-point division algorithm was later verified in HOL Light.
- Today formal verification is *routine* in chip design — readers' laptops contain verified
  arithmetic they've never thought about.

**Beat 5. Safety-critical, because certification requires it.**

- **Astrée (2005):** proved the absence of runtime errors in Airbus A340 fly-by-wire code —
  ~132,000 lines of C, fully automatic, with a low false-alarm rate after tuning.
- **DO-178C/DO-333** made formal methods an accepted (not required) means of compliance in
  avionics. The Paris Métro Line 14 was built with the B method and opened in 1998.

**Key point:** "the software flying your last flight was, in places, proved."

**Beat 6. The verified artifacts.** A short parade:

- **CompCert (2006–):** a C compiler whose every optimisation is proved semantics-preserving.
  When Csmith (2011) stress-tested every major compiler with random programs, GCC and LLVM
  produced hundreds of wrong-code bugs. **CompCert produced zero.**
- **seL4 (2009):** ~8,700 lines of C, ~200,000 lines of Isabelle proof, ~20 person-years. No buffer
  overflows, no null derefs, no code injection — for *all* executions.
- **HACL*/EverCrypt (F*):** verified crypto in Firefox, the Linux kernel, nginx, WireGuard —
  deployed at a scale nobody calls "formal methods".

**Beat 7. The cloud learns it, and the framing flips.**

- **AWS, 2011→:** TLA+ on S3, DynamoDB, EBS. The engineers' own pitch to colleagues was
  *"Debugging Designs"* and *"TLA+ is exhaustively testable pseudo-code."*
- The permanent lesson from their write-up: **the design is where the bugs are.** "If the design
  is broken then the code is almost certainly broken, as mistakes during coding are extremely
  unlikely to compensate for mistakes in design." And: they found TLA+ valuable for *data
  modelling* too.
- **Cedar (2019–):** the modern industrial pattern — prove a Dafny model, then *differentially
  random test* the Rust implementation against it, at billions of checks per day.

*Moral of Act II:* **FM solved the problems where failure is catastrophic and the artifact is
small. It never solved the "ordinary app code" problem.** Which is precisely the gap Act III
attacks.

---

## Act III — AI flips the economics and creates the demand (2020–2026)

Two directions, and it's worth being explicit that they are different stories with the same
engine.

**Beat 8. AI → FM: the rung the ladder was missing.**

Recall Act I's missing rung: the invariant. And the meta-lesson of [automated
reasoning](../01-fundamentals/automated-reasoning.md): *finding* a proof is hard; *checking* one
is cheap.

> "That asymmetry is the shape of a neural network's strengths and weaknesses. LLMs are brilliant
> at proposing. Kernels are brilliant at checking. Put them in a loop and you get a system that is
> both creative and sound — which neither component is alone."

Evidence ladder:

- **2020:** GPT-f does LLM-guided proof search.
- **2023:** LeanDojo, ReProver, COPRA — retrieval + LLMs + Lean become infrastructure.
- **2024: AlphaProof** solves 4/6 IMO 2024 problems at silver-medal level (28/42), trained with
  **Lean as the verifier and reward signal**. AlphaGeometry 2 takes the geometry problem.
  Published in *Nature* in Nov 2025.
- **2025:** open SOTA provers (Goedel-Prover, DeepSeek-Prover-V2), and Harmonic's **Aristotle**
  reports gold-medal-equivalent IMO 2025 performance with Lean-verified proofs.
- **2026:** mathlib has ~288k theorems, ~137k definitions, 772 contributors — and it is now
  training data, not just a library.

**Beat 9. FM → AI: the trust problem AI created.**

- LLM-generated code: plausible, test-passing, and correlated in its errors. Tests can't cover it;
  a verifier can. (See the emerging work on verifying LLM-generated code from natural-language
  prompts.)
- **Agents act.** An agent that executes a refund or drops a table needs a guarantee *before*
  action. Hence **AgentSpec**-style runtime enforcement, shields, and policy-as-code.
- **Neural networks are not readable.** Certifying robustness to all ε-perturbations is a formal
  problem; VNN-COMP exists because the tools are real (α,β-CROWN has won it five years running).
- **Enterprise-scale deployment:** AWS Bedrock's Automated Reasoning checks use SMT to validate
  LLM outputs against policies — a production product whose whole value proposition is
  "mathematically verified, not probabilistic".

**Beat 10. The economics, restated.**

> "In 2010, writing the spec cost more than the bug. In 2026, generating the code costs almost
> nothing, so **verification is the only part of the loop with a real price.** That's why this
> fifty-year-old field is suddenly on the critical path."

---

## The moral

```
   Act I    we can't decide everything       → so we built approximations
   Act II   approximations worked,            → but only for small, critical, stable artifacts
            in the shadows
   Act III  AI made proposal cheap            → so verification became the bottleneck
            and made new things to verify    → so verification became the product
```

**Closing line options** (pick one; they're all sourced from this wiki):

1. "Formal methods are not a replacement for testing. They're the only tool that answers the
   question testing can't: *what about all the inputs I didn't try?*"
2. "AI made code free. It didn't make correctness free. That gap is the next decade of
   engineering."
3. "The first AI program was a theorem prover. The most valuable AI systems of the next decade
   may well be the ones that verify."

---

## The shape to remember

If you take one thing from this page, take the shape rather than the dates:

```
   Act I    we can't decide everything       → so we built approximations
   Act II   those approximations worked,      → but only for small, critical, stable artifacts
            in the shadows
   Act III  AI made proposal cheap            → so verification became the bottleneck
            and made new things to verify    → so verification became the product
```

*Presenting this material?* The appendix has
[a presentation outline](../appendix/presenting.md) built on this structure, with timings.

## References

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
