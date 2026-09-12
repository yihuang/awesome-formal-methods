# Reading paths

Different readers need different routes. Pick the one that matches why you're here.

---

## Path A — "I'm giving the talk" (≈2 hours of reading)

1. [why-now.md](why-now.md) — get the argument.
2. [taxonomy.md](taxonomy.md) — get the map, especially the four dials.
3. [02-history/narrative.md](../02-history/narrative.md) — get the story arc.
4. [03-applications/case-studies.md](../03-applications/case-studies.md) — get the concrete proof it works.
5. [03-applications/lightweight-fm.md](../03-applications/lightweight-fm.md) — get the actionable ask.
6. [04-ai-era/ai-for-fm.md](../04-ai-era/ai-for-fm.md) + [fm-for-ai.md](../04-ai-era/fm-for-ai.md) — get the timeliness.
7. [03-applications/adoption-gap.md](../03-applications/adoption-gap.md) — get the honesty.
8. [slides/outline.md](../../slides/outline.md) — assemble.

Skip on first pass: logics.md, automated-reasoning.md, hardware-crypto.md, safety-critical.md.

## Path B — "I'm an engineer who wants to use this" (≈1 hour)

1. [03-applications/lightweight-fm.md](../03-applications/lightweight-fm.md) — the ladder, start at rung 0.
2. [01-fundamentals/specifications.md](../01-fundamentals/specifications.md) — the actual skill.
3. [05-tools/choosing.md](../05-tools/choosing.md) — pick one tool.
4. [06-practice/adoption-playbook.md](../06-practice/adoption-playbook.md) — the rollout plan.
5. [demos/lean/](../../demos/lean/) — read a real proof that compiles here.
6. [06-practice/objections.md](../06-practice/objections.md) — so you can answer your tech lead.

## Path C — "I'm an AI/ML engineer" (≈1 hour)

1. [04-ai-era/verification-bottleneck.md](../04-ai-era/verification-bottleneck.md) — your new constraint.
2. [04-ai-era/fm-for-ai.md](../04-ai-era/fm-for-ai.md) — agent guardrails, NN certificates, LLM code.
3. [04-ai-era/ai-for-fm.md](../04-ai-era/ai-for-fm.md) — what provers can do now.
4. [03-applications/case-studies.md](../03-applications/case-studies.md#4-cedar--verified-authorization-at-aws-scale) — the Cedar pattern (model + differential testing).
5. [01-fundamentals/limits.md](../01-fundamentals/limits.md) — what guarantees are *not* on offer.

## Path D — "I want to understand the theory properly" (weekend)

1. [01-fundamentals/logics.md](../01-fundamentals/logics.md)
2. [01-fundamentals/techniques.md](../01-fundamentals/techniques.md)
3. [01-fundamentals/automated-reasoning.md](../01-fundamentals/automated-reasoning.md)
4. [01-fundamentals/limits.md](../01-fundamentals/limits.md)
5. [references/bibliography.md](../../references/bibliography.md) — then the real textbooks.

## Path E — "I'm sceptical and want the strongest counter-arguments"

1. [03-applications/adoption-gap.md](../03-applications/adoption-gap.md)
2. [01-fundamentals/limits.md](../01-fundamentals/limits.md)
3. [06-practice/objections.md](../06-practice/objections.md)
4. [04-ai-era/fm-for-ai.md](../04-ai-era/fm-for-ai.md#8-what-does-not-work-yet) — the honest failures.

---

## Talk-length → content mapping

| Length | Spine | Cut |
|---|---|---|
| **15 min** (lightning) | Why now → one story (AWS TLA+) → the ladder → ask | Everything else |
| **30 min** | Hook (AI era) → taxonomy map → 3 case studies → AI bidirectional → lightweight ladder → ask | History depth, solvers, limits detail |
| **45 min** | Above + history arc + limits section + a live demo | Safety-critical detail, tool catalog depth |
| **60 min** | Everything, plus the adoption playbook and objection handling | Nothing, but move reference material to appendix slides |

See [`slides/outline.md`](../../slides/outline.md) for minute-by-minute scripts.
