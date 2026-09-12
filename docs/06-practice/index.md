# Practice — index

| Page | Contents |
|---|---|
| [adoption-playbook.md](adoption-playbook.md) | The staged 0→3 ladder with cost/payoff at each rung, metrics, and explicit exit criteria |
| [objections.md](objections.md) | Ten objections with honest answers |

## The two ideas that matter

1. **Start from an incident, not from a tool.** The first artifact you produce must be a *bug
   someone recognises*, not a proof. This is how AWS sold TLA+ internally, and it is the most
   reliable adoption mechanic in the field.

2. **Write down your exit criteria.** Naming when you'll stop is a credibility move — it shows
   you're applying engineering judgement, not advocating a technology.

## The ladder in one table

| Rung | Action | Cost | Payoff |
|---|---|---|---|
| **0** | Teach pre/post-conditions and invariants | 1 hour | better specs and reviews, immediately |
| **1** | Property-based tests on last quarter's incident | 1 day | usually a real bug on the first run |
| **2** | One sound check on the catastrophic-if-wrong core | 1–3 weeks | a counterexample, or a permanently checked invariant in CI |
| **3** | Institutionalise: CI gate, owner, assumptions, second engineer | 5–15% ongoing | the ability to make aggressive risky changes safely |

## The one-page checklist

A version you can hand to a colleague:
[adoption-playbook.md § One-page checklist](adoption-playbook.md#one-page-checklist-to-hand-out).

## The framing to copy verbatim from AWS

- Call it **"Debugging Designs"**, not "formal verification."
- Call the language **"exhaustively testable pseudo-code."**

The framing is not a euphemism — it's the difference between adoption and abandonment.
