# The adoption gap: why FM is 50 years old and still not mainstream

> **TL;DR.** The technology works. The adoption hasn't happened. Understanding *why* is both the
> most credible part of the talk and the source of the actual blocking issues you'll hit. Never
> give a formal-methods talk without this section — audiences discount everything else if you
> oversell.

---

## The evidence that there is a gap

- Formal methods has been academically active since the 1960s and has produced critical
  infrastructure (SAT/SMT solvers, type systems, model checkers) — yet the majority of commercial
  software development involves no formal specification or proof.
- Empirical software-engineering work documents persistent hesitation driven by "opinions and
  stereotypes" rather than by measured experience
  (see e.g. *Formal methods in industry: a systematic literature review / survey* work and the
  aerospace adoption studies). ⚠️ *Cite the specific study you use; there are several and they
  disagree about magnitudes.*
- The field's own self-assessments — Clarke & Wing's 1996 survey and Woodcock et al.'s 2009
  *Formal Methods: Practice and Experience* — are, in significant part, attempts to explain and
  close this gap. That the gap needed a new survey 13 years later is itself the evidence.

**But note the asymmetry, which is the real story:**

| Domain | FM adoption | Why |
|---|---|---|
| Semiconductor design | **Routine** | can't patch silicon; equivalence checking is standard in the flow |
| Avionics / rail / nuclear | **Standard where required** | certification credit (DO-333, EN 50128, IEC 61508) |
| Verified crypto libraries | **Increasing** | deployed at enormous scale, invisible |
| Cloud control planes | **Established at hyperscalers** | AWS TLA+, Cedar; distributed bugs are design bugs |
| Enterprise application software | **Rare** | *this is the gap* |

So the accurate statement is not "FM doesn't get adopted." It's: **FM gets adopted where failure
is catastrophic, the artifact is small, and there's a regulator or an outage to force it.**
Everything else is the frontier — and that frontier is what the AI era is opening.

---

## The real barriers, ranked (and which ones AI changes)

### 1. The specification gap — *not changed by AI, will never close*

You can prove the model conforms to the property. Nobody can prove the property is what the
product wanted. In fast-moving product development, "what it's supposed to do" changes weekly,
which makes a *stable* spec impossible — and stability is a precondition for the ROI
([case-studies.md](case-studies.md#cross-case-synthesis-the-four-conditions-for-a-good-verification-target)).

**Mitigation:** verify *invariants* (memory safety, no double-spend, no unauthorized access,
idempotency) rather than *features*. Invariants are the part of the spec that doesn't churn.

### 2. The cost structure looks bad on a quarterly budget — *AI changes this*

Verification's cost is upfront and lumpy; its benefit is a bug that didn't happen, which never
appears on a dashboard. Human incentive structures punish prevention.

**Mitigation (and it's a strong one):** two of the AWS quotes reframe this —
"prevented subtle, serious bugs from reaching production" *and* the ability to "make innovative
performance optimizations ... which we would not have dared to do without having model checked
those changes." Reframe FM from insurance to **enabler**. Insurance gets cut; enablers get funded.

### 3. The expertise tax — *AI partially changes this*

TLA+ or Dafny require weeks of ramp-up, plus a shift in mindset (backward reasoning, invariants,
temporal properties). And the skills are concentrated in a small community, so there's no one to
ask.

**Mitigation:** start with the *framing* AWS used — "debugging designs", "exhaustively testable
pseudo-code". Make it feel like an extension of work the team already does. Then let the
lightweight path ([lightweight-fm.md](lightweight-fm.md)) build fluency before attempting proofs.

**AI's contribution:** LLMs lower the ramp for the *syntax and idioms* meaningfully (writing a
first TLA+ spec, suggesting an invariant, explaining a solver error). This is real but should not
be oversold — see [ai-for-fm.md](../04-ai-era/ai-for-fm.md#7-what-does-not-work-yet).

### 4. "We already tried / we already do this" — *partially true, and a trap*

Engineers reasonably say "we have types, we have tests, we have static analysis." All true, and all
formal-ish. The gap is that none of them quantify over *all* inputs, and none of them verify
*protocol logic*.

**Mitigation:** don't argue. Agree, then ask the disarming question: *"when was the last time a
test told you something you couldn't have guessed by reading the code?"* Then: *"here's a tool
that tells you the input you'd never have guessed."* Lead with counterexamples.

### 5. The tooling/ecosystem problem — *partly improved*

Historically: obscure languages, poor IDE support, no CI integration, licence friction, abandoned
projects, no package manager, "install OCaml and 14 dependencies."

**Current state:** genuinely much better. Rust verification covers the full stack (CBMC/Kani,
Verus, Creusot, Prusti). Dafny has real tooling. TLA+ has an IDE and an SMT-backed checker
(Apalache). Lean has mathlib, a package manager (Lake), an LSP, and an active community. Cedar
ships as a normal library.

**Mitigation:** pick tools that live in *your* build system. A tool that isn't in CI is not adopted.

### 6. Distribution and survivorship bias in the literature — *structural*

Published case studies describe successes. Failed verification efforts are rarely published, so
practitioners can't calibrate risk. And the successful ones are atypical by construction (they had
a champion, a critical core, and executive patience).

**Mitigation (intellectual honesty):** when citing seL4 or CompCert, say out loud that they are the
survivors and that the cost profile is not generalisable to a CRUD service.

### 7. The proof-maintenance problem — *a genuine long-term cost*

Proofs need owners. Orphaned specs and proofs are liabilities: they get cited as evidence of
correctness long after the code diverged. A stale spec is worse than no spec.

**Mitigation:** wire the checker into CI *and fail the build*; require a named owner; treat the spec
as production code.

---

## The AI-era inflection, precisely stated

Be surgical here. AI does not dissolve the barriers; it moves **one** of them decisively and
creates a new source of demand.

| Barrier | AI's effect |
|---|---|
| Specification gap | **No change.** Still the deepest limit. |
| Upfront cost | **Improved.** Spec/proof drafting gets cheaper; search gets automated. |
| Expertise tax | **Moderately improved.** LLMs are good at syntax, idioms, first drafts, and explaining errors. Not yet trustworthy as authorities. |
| Tooling/ecosystem | **Slightly improved** (MCP servers, agent-native provers, better docs). |
| Proof maintenance | **Not addressed**, possibly worsened (generated proofs are harder to own). |
| Distribution/survivorship bias | **Not addressed.** |
| **(new) Demand** | **Created.** Cheap generated code + agents that act + unreadable models = a structural need for verification. |

**The honest thesis:**

> AI makes formal methods **cheaper to attempt** and **more necessary to have**. It does not
> make them easy, and it does nothing about the specification gap. What it changes is that for
> the first time the *default engineering answer* to "how do you know this is right?" — testing —
> is visibly insufficient for a large and growing class of systems.

---

## What the talk should do with this page

Use it in this order:

1. **Then:** the case studies (it works).
2. **Now:** this page — the gap, named honestly (it mostly didn't reach you).
3. **Next:** the AI-era chapter (economics changed, demand created).
4. **Ask:** the lightweight ladder (here's your one-step move).

That sequence is "credible → honest → timely → actionable" and it's the strongest structure
available for this talk.

**One more slide-worthy framing:** FM's adoption pattern mirrors *type systems*. In 1995, static
types were widely seen as academic overhead. Today they're the default in new languages and
nobody calls TypeScript "formal methods". **The successful outcome for this field is not that
people adopt "formal methods" — it's that the ideas become invisible infrastructure.** Rust's
borrow checker is already living proof. See
[techniques.md §5](../01-fundamentals/techniques.md#5-types--lightweight-static-analysis-the-free-tier).
