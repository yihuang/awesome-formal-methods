# Safety-critical: where regulation drives adoption

> **TL;DR.** In avionics, rail, automotive, medical, and nuclear, formal methods are adopted
> because *certification credit* is worth money and schedule. Understanding this domain explains
> (a) the origin of most FM tooling, (b) why the culture is conservative, and (c) why "formal
> methods are only for safety-critical systems" is a stereotype you should dismantle, not repeat.

---

## The core concept: certification credit

Safety-critical software isn't verified because engineers like proofs. It's verified because a
**certification authority** requires *evidence* that the software is fit for purpose, and formal
verification can be submitted as that evidence — often **replacing** mandated testing objectives.

That is the key economic mechanism: formal methods can *substitute for* expensive, mandatory
test campaigns. When you can trade 1,000 hours of structural coverage testing for a proof, the
ROI calculation changes completely.

---

## The standards landscape

| Standard | Domain | Relevance to FM |
|---|---|---|
| **DO-178C** *Software Considerations in Airborne Systems and Equipment Certification* | civil avionics | the base software standard; defines objectives and evidence |
| **DO-333** *Formal Methods Supplement to DO-178C* | civil avionics | **the FM-specific supplement** — how formal analysis substitutes for certain verification objectives |
| **DO-331** | avionics | model-based development supplement |
| **DO-332** | avionics | object-oriented technology supplement (and its verification challenges) |
| **DO-330** | cross-domain | **tool qualification** — the standard that answers "who verifies the verifier?" |
| **ISO 26262** | automotive | functional safety, ASIL A–D; increasingly references formal techniques |
| **IEC 61508** | generic functional safety | the parent standard for many domains |
| **EN 50128** | railway | explicitly recommends formal methods at the highest integrity levels (SIL 3–4) |
| **IEC 62304** | medical device software | risk-based; formal methods appear at higher classes |
| **Common Criteria** | security | assurance levels (EAL) can require formal specification and proof |

**Source of truth:** RTCA (avionics), ISO (automotive/generic), CENELEC (rail), IEC (medical).
Do not paraphrase these standards from blog posts — the details of which objectives can be
substituted are precise and legally consequential.

---

## What certification actually looks like

A crucial distinction the talk should make, because engineers conflate them:

```
   VERIFICATION   "I have evidence the system meets a specified property."
                        │
                        ▼
   CERTIFICATION  "An independent authority, following a defined process,
                   accepts that evidence as sufficient for a defined
                   operational context, and takes legal responsibility
                   for saying so."
```

Consequences that surprise engineers:

- **Process matters as much as the artifact.** Documented plans, traceability, configuration
  management, independent review. A proof without the surrounding process evidence may not be
  acceptable.
- **Tool qualification (DO-330).** If a tool's output is used as evidence, the tool itself may need
  qualification — you must argue that a tool bug cannot produce a false pass. This is the same
  "who verifies the verifier" problem as DRAT proof logging, in regulatory form.
- **The authority is in the loop early.** Certification is not a final exam; you engage the
  authority (e.g. FAA/EASA and their designated representatives) throughout.
- **Scope is the operational context.** "Verified" always means "verified for these assumptions in
  this environment." See [limits.md](../01-fundamentals/limits.md#the-trusted-base).

---

## Verified systems in safety-critical contexts

| System | Verification | Standard context |
|---|---|---|
| **Astrée** — Airbus A340/A380 fly-by-wire runtime-error analysis | abstract interpretation; ~132,000 lines of C; proved absence of runtime errors with a low false-alarm rate (Cousot et al., ESOP 2005) | avionics, DO-178B/C |
| **CompCert** | verified compiler, semantic preservation | used by Airbus for safety-critical avionics under DO-178C |
| **Paris Métro Line 14** (opened 1998) | B method for the driverless line's safety-critical software | EN 50128 (rail) |
| **seL4** | functional correctness + integrity + confidentiality + binary verification | DARPA HACMS, military/aerospace |
| **SPARK/Ada** | deductive verification; long pedigree in defence and aerospace | DO-178C, IEC 61508 |
| **Verified arithmetic** | Intel's HOL Light floating-point verification | silicon |

**Note the pattern:** the highest-value industrial FM deployments are *whole-program safety
analysis* (Astrée) and *infrastructure* (CompCert, verified arithmetic). Both amortise: you run
them once and get assurance over everything downstream. This is the same lesson as
CompCert's "verify the tool" insight.

---

## Why this domain is a double-edged sword for the talk

### The good news

1. **It proves FM works at industrial scale** on real, large, safety-critical artifacts.
2. **It has the cleanest ROI story** — regulation turns assurance into a budget line.
3. **The tooling it funded is now general-purpose.** Abstract interpretation, SMT solvers,
   refinement types, verified compilers, verified crypto — all of it came out of or was hardened
   by safety-critical and defence funding.

### The bad news (the stereotype you must dismantle)

Because FM's most visible history is safety-critical, the field inherited a reputation:

> "Formal methods require a huge amount of training and effort to verify a tiny piece of relatively
> straightforward code, so the return on investment is only justified in safety-critical domains
> such as medical systems and avionics."

AWS explicitly calls this perception "quite wrong" for *their* use case. The talk should:

1. **Acknowledge the origin story honestly** (that's how the field actually developed).
2. **Show the cost curve has moved** ([lightweight-fm.md](lightweight-fm.md), solver improvements,
   AI-assisted spec drafting).
3. **Show the non-safety uses** (control planes, authorization, crypto, agents) that have nothing
   to do with certification.

**Slide-ready reframe:** *"Safety-critical gave us the tools and the culture of rigour. It also
gave us a reputation problem. The interesting thing about the AI era is that the demand is now
coming from places with no regulator at all."*

---

## Process ideas worth stealing (even without a regulator)

These safety-critical practices transfer directly to ordinary engineering, and they cost little:

| Practice | Safety-critical form | Ordinary-team form |
|---|---|---|
| **Traceability** | requirement → design → code → test → evidence | issue → ADR → PR → test, linked |
| **Independence** | independent V&V by a different team | someone other than the author writes the verification |
| **Assumption documentation** | explicit assumptions and limitations section | a documented "assumptions" section in the spec — the thing nobody writes |
| **Tool qualification thinking** | argue a tool bug can't cause a false pass | use proof logging; pin solver/toolchain versions; know your trusted base |
| **Evidence, not assertion** | artifacts, not claims | the verification runs in CI and the badge is real |
| **Operational context** | the certification covers a defined envelope | the spec documents what's out of scope |

**The single highest-value transfer: an explicit assumptions section.** Every serious verification
project has one because the authors know a proof is only as good as its assumptions. Ordinary
teams almost never write one down, and that's where the surprises live
([limits.md](../01-fundamentals/limits.md#4-the-verified-systems-have-failed-file)).

---

## What to say (and not say) to a big-tech engineering audience

**Say:**
- This is where the techniques came from, and they work — the Astrée and CompCert results are real.
- The ROI mechanism is *substitution for mandatory testing*, which is why it's well funded there.
- Verified infrastructure amortises: verify the compiler, get assurance over every binary.

**Don't say:**
- "Formal methods are for safety-critical systems." That's the stereotype AWS had to fight. It
  alienates the audience and it's now false.
- "You need DO-333-compliant evidence for your service." Nobody does, and it makes the whole field
  sound like compliance theatre.

**Do say:**
- "The rigorous *habits* of safety-critical engineering — explicit assumptions, independent
  verification, evidence over assertion — are free and they will improve your system this quarter.
  The certification apparatus is the expensive part, and you don't need it."

---

**Sources:** RTCA DO-178C/DO-333 (via [rtca.org](https://www.rtca.org/do-178/));
[Cousot et al., ESOP 2005](https://pcousot.github.io/publications/CousotEtAl-ESOP05.pdf);
[verifiedsoftware.dev](https://verifiedsoftware.dev/case-studies/);
[DO-333 project notes](https://loonwerks.com/projects/do333.html).

Return to [applications index](README.md).
