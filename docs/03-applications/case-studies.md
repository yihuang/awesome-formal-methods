# Case studies: where it actually shipped

Seven proof points, ordered so the talk can escalate from "small and irreplaceable" to "runs a
billion times a day". Each entry has **the claim**, **the numbers**, **the pattern to steal**, and
**the honest caveat**.

> Source note: figures below come from project sites, the projects' own papers, and
> [verifiedsoftware.dev/case-studies](https://verifiedsoftware.dev/case-studies/). Vendor-published
> numbers are marked. Verify ⚠️ items before they become a slide.

---

## 1. seL4 — the verified microkernel

**Tool:** Isabelle/HOL · **Technique:** interactive theorem proving + refinement

| | |
|---|---|
| Implementation | ~8,700 lines of C |
| Proof | ~200,000 lines of Isabelle |
| Effort | ~20 person-years for the original verification |
| Guarantees | No buffer overflows, no null-pointer dereferences, no code injection, no memory leaks — for **all** executions, not sampled |
| Later extensions | Integrity & confidentiality (information-flow) proofs; **binary verification** of the compiled artifact |
| Deployed in | DARPA's HACMS autonomous helicopter program, military and aerospace systems |

**The pattern to steal — refinement.** seL4's proof isn't "the C is correct" in one leap. It's a
chain: abstract spec ⊒ (refined by) → design → C implementation. Each step is proved. That's how
you close the model-to-code gap instead of hand-waving it.

**The honest caveat.** The original proof assumed the hardware, assembly glue, and boot code
behaved — which is exactly why the team later added binary verification and an explicit
assumptions section. Also: subsequent changes are much cheaper to re-verify *because* the proof
infrastructure exists. Don't quote the 20 person-years without that second half.

**Talk use:** the "ceiling" example for cost, and the best illustration of refinement.

---

## 2. CompCert — the verified C compiler

**Tool:** Rocq/Coq · **Technique:** interactive theorem proving over a compiler semantics

**The central theorem:** the generated machine code behaves identically to the source C program.
Every optimisation pass comes with a semantic-preservation proof.

**The killer evidence.** In the Csmith study (Yang et al., PLDI 2011), researchers randomly
generated C programs and compiled them with every major compiler. GCC and LLVM each produced
**hundreds of wrong-code bugs**. **CompCert produced zero** — the only compiler for which no
miscompilations were found.

**Why compiler bugs matter more than they look:** they're invisible. Correct source silently
becomes incorrect binaries, and every test you run tests the *binary*, so a miscompile can make
your tests pass *because* it's broken. Also: CompCert is used commercially by **Airbus** for
safety-critical avionics under DO-178C.

**The pattern to steal.** Verify the *tool*, not just the artifact. A verified compiler amortises:
you verify it once, and every program you ever compile inherits the guarantee. Infrastructure
verification has a far better ROI curve than application verification.

**The honest caveat.** CompCert implements a large but not complete subset of C, and its proofs
assume the semantics definition and the C-to-assembly linkage. The Csmith comparison involved
CompCert's more restricted feature set, so "zero bugs" should be read as "zero within its
supported subset" — but that subset is what aircraft fly on.

---

## 3. AWS — TLA+ on the control plane

**Tool:** TLA+/TLC (model checking) · **Technique:** explicit-state model checking of designs

**The story.** From 2011, AWS engineers used TLA+ to specify and model-check designs for **S3,
DynamoDB, EBS** and others. The experience report is the single best practitioner document in the
field.

**The framing that sold it internally** (steal this):

> "Engineers think in terms of debugging rather than 'verification', so we called the presentation
> **'Debugging Designs'**."

> "Software engineers more readily grasp the concept and practical value of TLA+ if we dub it:
> **Exhaustively testable pseudo-code**."

**The two quotes worth the whole slide:**

> "In industry, formal methods have a reputation of requiring a huge amount of training and effort
> to verify a tiny piece of relatively straightforward code, so the return on investment is only
> justified in safety-critical domains such as medical systems and avionics. **Our experience with
> TLA+ has shown that perception to be quite wrong.**"

> "In several cases we have prevented subtle, serious bugs from reaching production. In other cases
> we have been able to make innovative performance optimizations — e.g. removing or narrowing
> locks, or weakening constraints on message ordering — **which we would not have dared to do
> without having model checked those changes.**"

That second quote is the killer. It reframes FM from *insurance* (cost centre) to *enabler*
(lets you ship a faster design). The performance optimisation angle is what gets a
performance-obsessed engineering org interested.

**The permanent lesson:**

> "Formal methods help engineers to get the design right, which is a necessary first step toward
> getting the code right. **If the design is broken then the code is almost certainly broken, as
> mistakes during coding are extremely unlikely to compensate for mistakes in design.** Worse,
> engineers will probably be deceived into believing that the code is 'correct' because it appears
> to correctly implement the (broken) design."

Also surprising and underused: TLA+ turned out to be **excellent for data modelling** — designing
relational/NoSQL schemas. Cheap slide aside for a big-tech audience.

**Source:** [Use of Formal Methods at Amazon Web Services (PDF)](https://lamport.azurewebsites.net/tla/formal-methods-amazon.pdf),
and CACM's *How Amazon Web Services Uses Formal Methods*.

**The honest caveat.** AWS itself is clear that TLA+ is one part of a broader correctness
practice, and that they use model checking on *designs*, not code. It does not find emergent
performance degradation.

---

## 4. Cedar — verified authorization at AWS scale

**Tools:** Dafny (model) + SMT + differential random testing; Lean 4 formalisation ·
**Technique:** deductive verification + refinement-by-testing

**What it is.** An open-source authorization policy language and engine (Apache-2.0) powering
Amazon Verified Permissions and AWS Verified Access.

**Scale.** AWS describes it as ~**1 billion automated-reasoning checks per day** ⚠️ (verify the
current figure).

**The pattern to steal — "verification-guided development"**, in two parts:

1. **Prove properties about a formal model.** Cedar's engine and validator are modelled in Dafny,
   with two proved security properties:
   - **explicit permit** — permission is granted *only* by individual `permit` policies, never by
     error or default;
   - **forbid overrides permit** — any applicable `forbid` always denies.
2. **Differentially random test the production code against the model.** Generate millions of
   diverse inputs; feed them to both the Dafny model and the Rust implementation; require
   identical outputs.

**Why this pattern is the most transferable one in the wiki:** it solves the hardest practical
objection (*"but your production code isn't the thing you proved"*) with engineering rather than
more proof. Proving a model is tractable; proving a Rust codebase is not. **Prove the model,
randomly test the gap.**

Also worth noting: this is a case where the FM work is not a side project — it's the product's
trust story. And authorization is the ideal target: a **pure function** (policy + request →
permit/deny), security-critical, and small.

**Source:** [Amazon Science: How we built Cedar with automated reasoning and differential testing](https://www.amazon.science/blog/how-we-built-cedar-with-automated-reasoning-and-differential-testing)

**The honest caveat.** DRT gives high confidence, not proof, about the model↔code correspondence.
That's a deliberate, well-reasoned trade — and the honest way to describe it.

---

## 5. Microsoft SymCrypt — verified cryptography for Windows and Azure

**Tool:** Lean 4 · **Technique:** deductive/functional verification via translation to Lean

**The claim.** SymCrypt implements the core cryptographic primitives (hashing, encryption, key
exchange) used across Windows and Azure. Microsoft is progressively verifying implementations in
Lean 4, producing machine-checked proofs that the code correctly implements its cryptographic
specification.

**Why crypto is the ideal FM target** (good slide material):

> "Cryptographic code is rarely modified, universally depended upon, and catastrophic when wrong.
> Cryptographic bugs don't crash your program — they silently compromise security. A single
> incorrect bit operation can reduce a 256-bit key to trivially breakable."

Notice the three properties: **stable, shared, catastrophic**. That's the profile of a good
verification investment. Use it as a heuristic.

**Sibling case — HACL*/EverCrypt (F*).** A verified cryptographic library (plus verified assembly,
ValeCrypt) deployed in **Firefox, the Linux kernel, nginx, and WireGuard**
([hacl-star.github.io](https://hacl-star.github.io/HaclValeEverCrypt.html)). Remarkable for being
simultaneously formal and fast — verified code that wins benchmarks, not just audits.

**The pattern to steal.** Combine a **low-level extraction path** (C/Rust/assembly → proof
assistant) with a **high-level spec** (the cryptographic standard). This is the same
refinement-ladder shape as seL4, applied to a library instead of a kernel.

---

## 6. Veil — verified distributed protocols

**Tool:** Lean 4 · **Technique:** framework/DSL for protocol verification with refinement

**What it is.** A framework from NUS for verifying distributed protocols (consensus, replication,
coordination) in Lean 4. Users write protocols in a DSL; Veil generates the refinement proofs.

**The result worth citing.** Veil found bugs in protocols that had previously been "verified" by
**two other tools** ⚠️ ([verifiedsoftware.dev](https://verifiedsoftware.dev/case-studies/)).

**Why that's a *good* story, not an embarrassing one.** It demonstrates the honest reality of the
field: *rigour matters as much as the act of verification*. A bounded check, or a model that
abstracts away the bug's precondition, can produce a "verified" result that is weaker than it
sounds. Which is why the field cares so much about the trusted base and explicit assumptions — and
why "we verified it" should always be followed by "**under these assumptions, with this bound**".

**Talk use:** the credibility slide. Using it shows you're not selling magic.

---

## 7. Neural network verification — α,β-CROWN and VNN-COMP

**Tool:** α,β-CROWN (and Marabou, ERAN, MN-BaB, …) · **Technique:** SMT/LP-relaxation based
verification of trained networks

**The claim.** α,β-CROWN is a state-of-the-art neural-network verifier, winning the **International
Verification of Neural Networks Competition (VNN-COMP)** in 2021, 2022, 2023, 2024, and 2025 with
the highest total score ([vnn-comp.github.io](https://vnn-comp.github.io/)).

**What it proves.** Statements like: *for every input within an ε-ball of this image, the
classification is unchanged* — a **certified robustness** guarantee, not an empirical
observation. And for control systems: reachability/safety properties of a learned controller.

**Why it matters for the AI-era framing.** This is the clearest case where AI created a new class
of verification problem that *classical* formal methods (SMT, LP, abstract domains) had to expand
to handle — and did. The technique is ordinary FM machinery (linear relaxations, branch and bound,
abstract domains) applied to a new kind of artifact: a matrix of weights.

**The honest caveat.** Certifiable robustness is not the same as semantic correctness. A network
can be provably robust to ε-perturbations and still be confidently wrong on a clean input. NN
verification gives you *one specific guarantee* — don't oversell it as "the model is correct."

---

## Cross-case synthesis: the four conditions for a good verification target

Every success above satisfies the same four conditions. This is the most useful slide in the
applications section — it turns case studies into a decision procedure.

| Condition | Why | Best examples |
|---|---|---|
| **Small** | proof/search cost is superlinear in size | seL4's 8.7k lines; Cedar's engine; crypto primitives |
| **Stable** | re-verification is the real cost over time | SymCrypt ("rarely modified"), CompCert |
| **Catastrophic when wrong** | justifies the spend | kernel isolation, crypto, aircraft, authorization |
| **Precisely specifiable** | you can write down what "correct" means | pure authorization functions; consensus safety; semantic preservation |

**And the inverse heuristic — don't verify:** rapidly changing UI code, anything whose
correctness criterion is "the PM is happy", code dominated by third-party dependencies, or
anything where performance/emergence is the actual risk. Users of FM need to be as good at
*declining* targets as choosing them.

## The three reusable industrial patterns

```
   1. MODEL-CHECK THE DESIGN (AWS)          cheapest, finds design bugs before code exists
      TLA+ / Alloy / SPIN

   2. PROVE A MODEL + DIFFERENTIALLY        tractable version of "the code matches the spec"
      TEST THE CODE (Cedar, SymCrypt)
      Dafny/F* + DRT

   3. PROVE THE REAL CODE (seL4, CompCert)  strongest, most expensive, for stable critical cores
      Lean/Isabelle/Rocq + refinement
```

**Ask of the audience:** pick pattern 1 or 2. Nobody in the room is going to do pattern 3 this
quarter, and pretending otherwise loses credibility.
