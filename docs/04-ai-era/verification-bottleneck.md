# The verification bottleneck

> **TL;DR.** For the entire history of software, writing code was expensive and checking it was
> comparatively cheap. AI inverted that. Generation is now abundant; verification is not. The
> scarce resource in the AI-era software lifecycle is *trustworthiness* — and formal methods are
> the only technology that scales a sound check.

This page is the economic argument that makes the talk timely. It's the bridge between
[ai-for-fm.md](ai-for-fm.md) and [fm-for-ai.md](fm-for-ai.md).

---

## 1. The inversion

```
   BEFORE (1969–2022)                      NOW (2023–2026)
   ────────────────────                    ────────────────
   generation:  $$$$                       generation:  ¢
   verification: $$                        verification: $$$$   ← unchanged, now dominant
   → optimise for writing code             → optimise for trusting code
```

The cost of *producing* a plausible implementation has collapsed. The cost of *establishing that
it is correct* has not moved, because it was never a generation problem — it's a checking problem,
and checking arbitrary code is governed by the limits from
[limits.md](../01-fundamentals/limits.md).

**The evidence that this is real, not theoretical:**

- Anthropic's 2026 agentic-coding analysis reports engineers using AI in roughly **60% of their
  work** while reporting they can **"fully delegate" only 0–20% of tasks**
  ([source](https://claude.com/blog/eight-trends-defining-how-software-gets-built-in-2026)).
  That gap between *assisted* and *trusted* **is** the verification bottleneck, in one statistic.
  It's a vendor-published figure — but the direction is corroborated everywhere.
- The same report describes the engineer's role shifting from writing code to "coordinating agents
  that write code", with the human expertise pointed at "architecture, system design, and strategic
  decisions" — i.e., at **deciding what should be true**, which is specification.
- Code volume at fixed headcount rises. Review capacity does not. Every additional line of
  AI-generated code is an additional line nobody has verified.

**Amdahl's-law framing (good slide):** if you speed up one stage of a pipeline by 10× and leave the
next stage unchanged, the next stage becomes the bottleneck and sets the throughput ceiling. AI
sped up authoring. Verification is the unsped-up stage.

---

## 2. The two asymmetries that define the AI-era opportunity

Everything in this wiki reduces to two facts. Put them on consecutive slides.

### Asymmetry A — checking is cheap, searching is hard

```
   FIND a proof     →  intractable (NP-hard / undecidable in general)
   CHECK a proof    →  linear-ish, deterministic, fast
```

**Consequence:** an AI that proposes and a kernel that checks is a *sound* generate-and-test loop.
This is why AI and formal methods are complements, not competitors
([automated-reasoning.md](../01-fundamentals/automated-reasoning.md#3-the-deep-asymmetry-checking-is-easy-searching-is-hard)).

### Asymmetry B — generation is now cheap, verification is not

```
   GENERATE code    →  cheap, parallel, unlimited
   VERIFY code      →  expensive, serial, bounded by human attention or solver time
```

**Consequence:** verification is the constraint. Whoever lowers its cost raises system throughput.

**Together:** AI lowers the cost of the *search* half of verification (Asymmetry A) at exactly the
moment verification became the constraint (Asymmetry B). That coincidence is the whole opportunity.

---

## 3. The verification gap (a metric worth coining)

> **The verification gap** = the volume of behaviour a team has *shipped* minus the volume of
> behaviour it has *soundly established*.

Every organisation's gap grew in 2024–2026. Some consequences:

| Symptom | What's actually happening |
|---|---|
| Review queues grow; reviewers rubber-stamp | generation outran review capacity |
| "It passes CI" becomes the correctness standard | tests became the *only* gate, and they're sampled |
| Incident postmortems increasingly say "the code did something we didn't expect" | the gap |
| Teams add more AI review to review AI's output | correlated failure — same model family, same blind spots |
| Security teams can't keep up with generated code | the gap, with an adversary |

**Crucially: AI-generated review of AI-generated code does not close the gap**, because the errors
correlate. Adding another probabilistic checker to a pipeline of probabilistic checkers improves
the average case and does little for the tail — and the tail is where incidents live.

**This is the sharpest argument for formal methods in the talk**, because it is *not* an argument
that FM is better than testing in general. It's an argument that the *marginal* checker in an
AI-saturated pipeline must be **orthogonal** to the failure modes of the others, and only a sound
checker is.

---

## 4. What the market is already doing about it

The interesting signal is that this is being solved commercially, not just researched.

| Response | Example | What it indicates |
|---|---|---|
| **Formal checks in the LLM product** | AWS Bedrock Guardrails **Automated Reasoning checks** use SMT to validate responses against formal policies | a hyperscaler decided a *sound* check was a product feature |
| **Verified model + differential testing** | Cedar (Dafny model + DRT over Rust) at ~1B checks/day ⚠️ | "verification-guided development" as a named practice |
| **Formal verification as a product category for AI** | Harmonic's Aristotle; agentic provers; Lean LSP/MCP servers | provable reasoning sold as a service |
| **Push-button verifiers in normal build systems** | `cargo kani`, CBMC, Dafny in CI | the barrier to rung 4 dropped to a cargo subcommand |
| **Independent judging infrastructure** | Lean FRO's Comparator + nanoda | the ecosystem is building the *refereeing* layer for machine-generated proofs |
| **Spec-driven development** | agents that write specs/tests before code | the industry rediscovering that the specification is the valuable artifact |
| **Regulatory pull** | DARPA CLARA (formal verification for aerospace control, ~$48M ⚠️) and safety standards | governments treating verified AI-adjacent systems as a capability |

Read together: **verification is becoming a product, a job function, and a procurement
requirement.** That is what a bottleneck looks like when capital notices it.

---

## 5. The counter-arguments (and the honest answers)

| Objection | Answer |
|---|---|
| "Most code doesn't need verification." | Correct. That's why the playbook is *prioritisation by blast radius*, not universal verification. Verify the 1% whose failure is unbounded. |
| "AI will learn to verify." | It will learn to *propose* verifications. A sound check still requires a checker — and the checker is cheap. That division of labour is the point. |
| "This is just more process; we'll slow down." | Verification of a *small critical core* is the enabler that lets you move fast elsewhere. AWS's own report: model checking let them remove locks and weaken ordering constraints they "would not have dared to" change otherwise. Verification buys *speed* on the risky parts. |
| "Our tests are good enough." | Tests are necessary and remain necessary. They are not sufficient for correlated-failure regimes or adversarial inputs. Neither replaces the other. |
| "Nobody will maintain proofs." | True risk, and the reason to keep the verified core *small and stable* and to wire it into CI as a gate with a named owner. Proof sprawl is a genuine failure mode. |
| "The models will get good enough that this doesn't matter." | Better models reduce *reasoning* errors and leave *specification*, *environment*, and *correlation* risks intact. [limits.md](../01-fundamentals/limits.md) is not a statement about model quality. |

---

## 6. What changes for an individual engineer

The talk should end on this, because it's what the audience actually controls.

```
   OLD CORE SKILL                    NEW CORE SKILL
   ─────────────                     ──────────────
   writing code                      deciding what must be true (specification)
   debugging                         constructing counterexamples and invariants
   testing (sampling)                designing sound checks + sampling
   reviewing style and logic         reviewing SPECIFICATIONS and ASSUMPTIONS
```

**The reframing that lands with a big-tech engineering audience:**

> "Your job is becoming less about producing correct code and more about **stating what correct
> means, precisely enough that a machine can check it.** That is a specification skill. It is the
> one part of this field that has never been automated, and it's about to be the highest-leverage
> skill on your team."

Anyone who has spent a week arguing in a design review about whether a retry can duplicate a write
has already done this work. Formal methods just make the argument decidable.

---

## 7. The three-sentence version (for a slide)

1. **AI made code cheap and trust expensive.**
2. **Checking is cheap; searching is hard — so AI proposes and kernels dispose.**
3. **The engineers who can write a precise specification, and choose the cheapest sound check for
   it, will be the ones who keep the system trustworthy as it scales.**

---

Continue → [README.md](README.md) for the bidirectional map, or
[../03-applications/lightweight-fm.md](../03-applications/lightweight-fm.md) for the actionable
ladder.
