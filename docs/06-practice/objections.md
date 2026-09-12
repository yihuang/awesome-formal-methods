# Objections and answers

> **TL;DR.** Every one of these will come up. Have the one-paragraph answer ready, agree with the
> part that's true, and don't oversell. The fastest way to lose a technical reader on this topic
> is to sound like a vendor.

Format: **the objection** → **what's true about it** → **the answer**.

---

## "Formal methods have been 10 years away for 50 years."

**True.** The field has a long history of promising more than it delivered, and academia has
published a lot of tools nobody used. The stereotype AWS quoted — "requires a huge amount of
training and effort to verify a tiny piece of relatively straightforward code" — was earned.

**Answer:** Ask what *did* happen, rather than what didn't. Formal verification is routine in
silicon design. It's standard in avionics under DO-178C/DO-333. It's running in your browser via
HACL\*/EverCrypt, in Firefox, the Linux kernel, nginx, and WireGuard. It found design bugs in S3
and DynamoDB. The accurate statement is not "FM never delivered" — it's "**FM delivered exactly
where failure was catastrophic and the artifact was small, and nowhere else.**" The AI era is
changing the second half of that sentence.

---

## "You still can't verify the specification is what you meant."

**True, and it's the deepest limitation.** No tool checks that your property is what anyone wanted.
A verified system can be perfectly correct and useless (the classic: a "sort" spec that permits
returning the input unchanged passes an "is it sorted" check).

**Answer:** Don't defend it — *lead with it*. The specification gap is permanent and this wiki
says so up front, because it reframes what FM is for: **precision, not omniscience.** A proof tells
you "if the model is right and the property is what you meant, then this holds for all
executions." That's a strictly better position than "we tested it and nothing broke," and it's a
strictly worse position than "we know it's correct," which nobody has ever had.

**Killer follow-up:** *"The spec gap is also the reason the AI-era work is interesting. Writing the
spec is the part that was never automated, and it's now the bottleneck — which makes it the most
valuable skill."*

---

## "AI can just verify things too. Why do I need formal methods?"

**Partly true.** LLMs are genuinely useful for proposing proofs, invariants, specifications, and
fixes — and they've gotten remarkably good at it.

**Answer:** Because **proposing is not checking.** An LLM that produces a proof is doing search;
only a checker can accept one. The whole value of a proof comes from the machine-checkable kernel,
not from its author. And the empirical case is now strong: in 2026, AI-produced mathematics shipped
*with Lean certificates* precisely because nobody would accept "the model says it's proven."

**Second half of the answer, which is the more interesting one:** AI *needs* formal methods.
Reinforcement learning requires a reliable verifier as a reward signal, and formal systems provide
the best one known. AlphaProof's design is literally "Lean as the environment and the reward."
So the relationship is symbiotic, not competitive.

**And a third, sharper point:** LLM-based review of LLM-generated code fails in *correlated* ways —
same model family, same blind spots. A sound checker fails differently. In a pipeline saturated
with probabilistic checkers, the marginal checker needs to be **orthogonal**, and only a formal one
is.

---

## "We can't even write good tests. How are we going to write specifications?"

**True and important.** If a team can't state what a function should do in a test, it can't state
it in a property.

**Answer:** You're right that this is the real prerequisite, and it's also why the entry point is
rung 1 (contracts/assertions) and rung 2 (property-based tests) rather than a proof assistant.
Property-based testing is *easier* than a comprehensive test suite, not harder: you write one
universally quantified property instead of thirty examples, and the machine generates the inputs.
Start there. If a team can't do that, they have a specification problem, and formal methods were
never the fix.

---

## "Our system is too big / too complex."

**True.** You cannot verify a large service.

**Answer:** You never verify the whole system. You verify a small, stable, critical core — the
consensus state machine, the authorization function, the ~40-line `unsafe` block, the retry
idempotency rule. seL4 is 8,700 lines of C; Cedar's engine is a pure function. AWS model-checked
*designs*, not S3's codebase.

**The reframe:** this is a **scoping** discipline, and scoping is the skill. "Too big" is usually a
statement that the speaker hasn't identified the 200 lines that carry the risk.

---

## "This is too expensive. We don't have a safety-critical budget."

**True for whole-system proofs.** seL4 was ~20 person-years.

**Answer:** Then don't do whole-system proofs. The cost curve for the useful rungs is:

| Rung | Cost |
|---|---|
| Property-based tests on the incident that paged you | ~1 day |
| `cargo kani` on one unsafe block | ~1 day of setup |
| A TLA+ spec of a protocol you're arguing about | ~1–2 weeks |
| Verified crypto | free — use HACL\*/EverCrypt |
| Whole-kernel proof | person-years (not your problem) |

**And the crucial reframe from AWS:** verification isn't only insurance, it's an *enabler*. Their
report says model checking let them remove or narrow locks and weaken message-ordering constraints
— optimisations "which we would not have dared to do without having model checked those changes."
**Verification buys speed on the risky parts.** That's a budget argument a performance-obsessed org
will actually hear.

---

## "Testing works fine for us. Why change?"

**True** — for most code, most of the time.

**Answer:** Agree, then locate the boundary precisely. Testing is *necessary* and stays necessary.
The question is what testing structurally cannot do:

- quantify over **all** inputs (not samples),
- quantify over **all** interleavings (this is where distributed bugs live),
- quantify over **all** adversary perturbations within a budget,
- tell you that a property **cannot** fail, as opposed to hasn't yet.

**The disarming question:** *"When was the last time a test told you something you
couldn't have guessed by reading the code?"* Then: *"Here's a class of tool that tells you the
input you'd never have guessed."* Lead with counterexamples. Never argue that testing is bad.

---

## "It's academic / the tools are unusable."

**Partially true historically** — obscure languages, no IDE, no CI, no package manager.

**Answer:** The honest state in 2026:

- `cargo kani` — one command, in CI, for Rust.
- Dafny — a real language with real tooling, used by AWS in production.
- `pip install hypothesis` — property-based testing, five minutes.
- Lean 4 + Lake + LSP + mathlib — a package manager, an IDE experience, and ~288k theorems.
- TLA+ has an IDE and an SMT-backed checker (Apalache).
- `pip install z3-solver` — an industrial SMT solver in one line.

**The rule to state:** pick tools that live in *your* build system. A tool that isn't in CI is not
adopted — and if a proposed tool can't be put in CI, that's a legitimate reason to reject it.

---

## "Who maintains the proofs? They'll rot."

**True, and it's a top-three practical risk.** Proofs need owners. Stale specs are worse than no
specs, because they get cited as evidence of correctness after the code has diverged.

**Answer:** Treat the spec as production code:

- it lives in the repo next to the code,
- it has a named owner,
- the checker is a CI gate that **fails the build**,
- the trusted base and assumptions are documented,
- re-verification cost is part of the change estimate.

**And note the honest upside:** re-verification is much cheaper than initial verification. seL4's
own framing is that subsequent changes are significantly cheaper to re-verify precisely because the
proof infrastructure exists. The 20 person-years is an *initial* cost, not a linear one.

---

## "This is the wrong abstraction level for our business problems."

**True.** Most business logic is about product decisions under uncertainty, not invariants.

**Answer:** So don't verify the business rules. Verify the *invariants underneath them* — the
properties that must hold regardless of product direction:

- no unauthorized access,
- no double-spend / no lost update,
- no data corruption,
- no crash / no UB,
- idempotent retries,
- monotonic reads.

**Invariants are the part of your specification that doesn't churn.** Feature specs churn weekly,
which is exactly why they're the wrong target. This is why the ROI condition includes "stable."

---

## "Isn't this just more process? We'll slow down."

**True if you do it wrong** — boil-the-ocean verification absolutely slows you down.

**Answer:** Distinguish the two modes:

- **Verification as a gate**: slows you down, resented, gets abandoned.
- **Verification as a debugger for designs**: speeds you up, gets adopted, produces counterexamples.

That's why AWS called their internal talk **"Debugging Designs"** and described TLA+ as
**"exhaustively testable pseudo-code."** The framing isn't cosmetic — it's the difference between a
compliance chore and a design tool. Copy it.

---

## "Gödel proved we can never fully verify software."

**A real theorem, misapplied.** Gödel (1931) says no consistent, expressive, effective formal
system proves all arithmetic truths. Rice's theorem (1953) says every non-trivial semantic property
of arbitrary programs is undecidable.

**Answer:** Both are true and both are already baked into the design of every practical tool. They
are *why* abstract interpretation over-approximates, why SMT solvers return `unknown`, why model
checkers need finite models, and why proof assistants need human or AI guidance. **Rice's theorem
isn't an objection to formal methods — it's the reason the tool landscape looks the way it does.**
The complete answer is in [limits.md](../01-fundamentals/limits.md#1-the-mathematical-limits).

**And the response to the *spirit* of the objection** — "so it's all futile" — is that you don't
need a decision procedure for all programs. You need one for *your* small, structured, boring
critical core, with a human supplying the invariant. That's been sufficient for a kernel, a
compiler, a cryptographic library, and a billion authorization checks a day.

---

## "You're overselling AI here."

**Fair, and this page should be the first to say it.** Watch for these oversells:

| Oversell | Reality |
|---|---|
| "AI verifies code now" | AI *proposes*; a checker verifies. And the 2026 results were on mathematics, not services. |
| "A verified guardrail makes the agent safe" | It makes one property hold. Everything else is unverified. |
| "Autoformalization solved the spec problem" | It's the *new* bottleneck; statement mismatch is the dominant failure mode. |
| "AI provers are cheap" | AlphaProof took **days** per IMO problem. Sample efficiency is poor. |
| "Formal methods solved AI safety" | They offer narrow, precise guarantees — containment, policy compliance, robustness in a ball. Nothing more. |

**The credibility move:** state the limitations *before* you start answering objections, not after. See
[ai-for-fm.md §7](../04-ai-era/ai-for-fm.md#7-what-does-not-work-yet) and
[fm-for-ai.md §8](../04-ai-era/fm-for-ai.md#8-what-does-not-work-yet).

---

## "Why should *I* care? I write CRUD services."

**Answer, in one line:** because your service's *blast radius* is the thing that matters, not its
category. Every CRUD service contains: an authorization decision, a payment or quota boundary, a
retry path, and a migration. Those are the invariant-shaped parts, and they're where your incidents
come from.

**Then the practical move:** the 1-day rung-1 action — property-based tests on the function that
last broke production. That's the answer to "why should I care" that fits in a sprint.

---

## The meta-answer (if you only remember one)

> **"You're right that formal methods are expensive, narrow, and sometimes impractical. They're
> also the only tool that answers the question testing cannot: *what about all the inputs I didn't
> try?* AI just made that question the bottleneck. Start one rung up — one property, one function,
> one day — and stop wherever it stops paying."**

Agreeing with the objections instead of rebutting them is what makes a formal-methods argument land.

---

Related: [adoption-gap.md](../03-applications/adoption-gap.md) ·
[limits.md](../01-fundamentals/limits.md) ·
[adoption-playbook.md](adoption-playbook.md)

## References

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
