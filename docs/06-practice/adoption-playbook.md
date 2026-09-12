# Adoption playbook: 0 → 3 in a normal team

> **TL;DR.** Adoption fails when it starts with a tool. It succeeds when it starts with an
> incident, produces a counterexample, and lands in CI. This page is the staged plan with the cost
> and the payoff at each rung — plus the exit criteria, because abandoning this deliberately is a
> legitimate outcome.

This is the "how" page. Everything else in the wiki is the "why".

---

## Principle 0: the four failure modes of FM adoption

Name these up front so the plan visibly avoids them:

| Failure mode | What it looks like | Antidote |
|---|---|---|
| **Tool-first adoption** | "We're going to learn TLA+ this quarter" → nobody has a problem → abandoned | start from an incident |
| **Boil the ocean** | "Let's verify the service" → 6 months, no result | verify the 200-line core |
| **No CI integration** | proof exists, code drifts, proof becomes a lie | gate the build |
| **The single champion leaves** | one enthusiast, no institutional memory | document specs; train two people |

---

## Rung 0 — Establish the common vocabulary (1 hour, no tools)

**Do:** run an internal session using
[01-fundamentals/specifications.md](../01-fundamentals/specifications.md). Teach *pre/post
conditions*, *invariants*, *safety vs liveness*, and the phrase **"for all inputs"**.

**Cost:** one hour. **Payoff:** the team can now state properties. This is the actual skill.

**Exit criteria:** every engineer can say, for one function they own, what must be true *before*
and *after*.

**Why this is rung 0 and not optional:** the tools are the easy part. If nobody can phrase a
property, all downstream effort fails. Also, this rung costs nothing and immediately improves code
review.

---

## Rung 1 — Property-based tests on the function that broke (1 day)

**Do:** find the function that caused last quarter's incident. Write 2–3 properties:
one for the happy result, one for what must be *preserved* (ordering, permutation, idempotency,
no side effect). Run it.

**Cost:** ~4 hours for an engineer familiar with the language.
**Payoff:** usually finds a bug in the first run. That bug is the business case for everything else.

**Tools:** Hypothesis (Python), proptest (Rust), fast-check (TS), jqwik (Java), Go fuzzing.

**Exit criteria:** PBT runs in CI. A shrunk counterexample has been pasted into a ticket.

**The political note that matters:** *the first artifact you produce must be a bug someone
recognises.* Not a proof. A bug. This is how AWS sold TLA+ internally ("Debugging Designs"), and it
is the single most reliable adoption mechanic in the field.

---

## Rung 2 — One sound check on the critical core (1–3 weeks)

**Do:** pick the smallest, most catastrophic piece of logic. Options:

| Target | Action |
|---|---|
| a protocol/design you keep arguing about | write a TLA+ spec (~200 lines), check with TLC |
| an `unsafe` Rust block | `cargo kani` on it |
| a pure critical function (C/Rust/Java) | CBMC / Kani / Dafny / Why3 |
| an authorization decision | model it in Cedar-style policy-as-code |
| a serialization/parsing boundary | differential PBT against a reference implementation |

**Cost:** 1–3 weeks for one champion, including the learning curve.
**Payoff:** either a counterexample (the good outcome) or a *checked* invariant in CI (the other
good outcome).

**Exit criteria:**
- The spec/annotations live in the repo, next to the code.
- The checker runs in CI and **fails the build**.
- The spec has a named owner.
- An explicit **assumptions** section exists (this is the safety-critical habit worth stealing —
  see [safety-critical.md](../03-applications/safety-critical.md#process-ideas-worth-stealing-even-without-a-regulator)).

**Budget advice:** don't measure this rung by bugs-found-per-hour. Measure it by "how confident are
we in the design decision we were arguing about?" That's the deliverable.

---

## Rung 3 — Institutionalise (ongoing)

**Do:**

1. **Make verification a gate, not an event.** CI fails on: unproven obligations, `sorry`/`admit`
   in proofs, timeout regressions, stale specs.
2. **Add the properties to the review checklist.** "What invariant does this change touch?"
3. **Train a second person.** Bus factor is the top killer of FM programmes.
4. **Track the right metrics** (see below).
5. **Document the trusted base** for every verification: what tool, what version, what
   assumptions, what is *outside* the proof.
6. **Extend by blast radius, not by coverage percentage.** The next target is the next
   catastrophic-if-wrong thing, not "the rest of the codebase".

**Cost:** ongoing, ~5–15% of engineering time for the verified core.
**Payoff:** the thing AWS reported — the ability to make aggressive changes ("removing or narrowing
locks, or weakening constraints on message ordering") *because* you can check them. This is the
payoff that gets budgets renewed: **verification as a speed enabler, not a brake.**

---

## The metrics that actually work (and the ones that don't)

| ✅ Track | ❌ Don't track |
|---|---|
| Critical invariants with a CI gate | "% of code formally verified" |
| Counterexamples found pre-production | lines of proof written |
| Time to re-verify after a change | number of specs |
| Number of **assumptions documented** | number of theorems |
| Incidents in verified components (should be ~0, and that's the point) | "verification coverage" as a vanity metric |
| Engineer-hours per re-verification cycle | solver time (an implementation detail) |

**Why "% verified" is a bad metric:** it incentivises verifying easy, irrelevant code and creates
pressure to overstate scope. Verify the 1% that matters and say so precisely.

---

## Cost/benefit table (use this to make the ask)

| Rung | Cost | Payoff | Payback evidence |
|---|---|---|---|
| 0 — vocabulary | 1 hour | better specs, better reviews | immediate |
| 1 — PBT on the incident | 1 day | a real bug, usually | first run |
| 2 — sound check on critical core | 1–3 weeks | a counterexample or a checked invariant | AWS: "prevented subtle, serious bugs from reaching production" |
| 3 — institutionalise | 5–15% ongoing | aggressive refactors, provable claims | AWS: optimisations they "would not have dared to" make |

**The pitch to a manager, in one line:** *"One day of property tests on the component that paged us
last quarter, then two weeks on the one piece of logic where a bug is unrecoverable. If we find
nothing, we'll have a permanently verified core that lets us move faster on the risky parts."*

---

## When to stop (legitimate exits)

Formal methods are not always worth it. Explicit exit criteria:

- **The artifact churns faster than it can be re-verified.** Stop and go back to PBT.
- **The specification can't be agreed on.** A proof of an undefined property is worthless;
  the disagreement is the real deliverable, and it's fine to stop after resolving it.
- **The property is already guaranteed by construction.** Rust's borrow checker often makes a Kani
  proof redundant. Don't re-prove the compiler.
- **The risk is performance/emergence, not logic.** No formal tool addresses AWS's category (2).
- **The cost of the bug is smaller than the cost of the proof.** Say it out loud and move on.

**Naming your exit criteria up front is a credibility move.** It signals you're applying
engineering judgement, not advocating a technology.

---

## The adoption narrative to rehearse

If someone asks "how did this go at AWS?", the answer is the template:

1. An engineer hit a bug class that testing couldn't catch (design-level, interleaving-dependent).
2. They found a language that could express the design precisely (TLA+).
3. They called the internal presentation **"Debugging Designs"**, not "formal verification".
4. They positioned the tool as **"exhaustively testable pseudo-code"**.
5. The wins were concrete: "(a) prevented subtle, serious bugs from reaching production" and
   "(b) we made optimisations we would not have dared to make otherwise."
6. It spread because the artifacts were useful, not because the technique was impressive.

**Copy steps 3 and 4 verbatim.** The framing is not a euphemism — it's the difference between
adoption and abandonment.

---

## One-page checklist to hand out

```
[ ] 1 hour:  team can state pre/post conditions and invariants
[ ] 1 day:   property-based tests on last quarter's incident, in CI
[ ] name it:  "debugging designs" / "exhaustively testable pseudo-code",
              NOT "formal verification"
[ ] 1-3 wks: one sound check on the catastrophic-if-wrong core
[ ] CI gate: build fails on unproven obligations and on sorry/admit
[ ] owner:   the spec has a named human
[ ] assume:  the spec documents its ASSUMPTIONS explicitly
[ ] scope:   the spec documents what is OUTSIDE the proof
[ ] metrics: invariants gated, not "% verified"
[ ] bus:     a second person can run and change the spec
[ ] exit:    written down, so stopping is a decision not a failure
```

---

Next → [objections.md](objections.md): the answers you'll need in the Q&A.
