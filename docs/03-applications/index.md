# Applications — index

| Page | What it gives you |
|---|---|
| [case-studies.md](case-studies.md) | **The proof it works.** seL4, CompCert, AWS TLA+, Cedar, SymCrypt, Veil, VNN-COMP — with numbers and caveats. |
| [distributed-systems.md](distributed-systems.md) | **The best ROI.** Why protocol verification is the highest-value target for an infra team. |
| [hardware-crypto.md](hardware-crypto.md) | **Where FM is already standard.** Silicon equivalence checking, FDIV, HACL*/EverCrypt, constant-time caveats. |
| [safety-critical.md](safety-critical.md) | **Where regulation drives it.** DO-178C/DO-333, certification credit, and the stereotype to dismantle. |
| [lightweight-fm.md](lightweight-fm.md) | **The on-ramp.** The rungs from types to TLA+, with code, that an ordinary team can climb. |
| [adoption-gap.md](adoption-gap.md) | **The honesty.** Why this 50-year-old technology mostly didn't reach most engineers — and what AI changes. |

---

## Suggested reading order

```
   1. It works          → case-studies.md        (credibility)
   2. Here's the best   → distributed-systems.md (the highest-ROI target)
      target
   3. It's already      → hardware-crypto.md     (you depend on it today)
      around you
   4. But it didn't      → adoption-gap.md        (honesty; disarms scepticism)
      reach you
   5. AI changed the    → ../04-ai-era/           (timeliness)
      economics
   6. Here's your       → lightweight-fm.md       (action)
      one-step move
```

## The decision table to end the section with

| Your situation | Best-fit technique | Page |
|---|---|---|
| Distributed protocol / consensus / retries | Model checking (TLA+) | [distributed-systems.md](distributed-systems.md) |
| Whole codebase, want no UB ever | Abstract interpretation | [techniques.md §4](../01-fundamentals/techniques.md#4-abstract-interpretation-sound-over-approximation) |
| One critical function, all inputs | SMT-based deductive verification (Kani/Dafny) | [lightweight-fm.md](lightweight-fm.md) |
| Authorization / policy engine | Proved model + differential testing | [case-studies.md §4](case-studies.md#4-cedar--verified-authorization-at-aws-scale) |
| Cryptography | Use a verified library | [hardware-crypto.md](hardware-crypto.md) |
| Regulated safety | Standard-mapped evidence | [safety-critical.md](safety-critical.md) |
| Just getting started | Types + property-based testing | [lightweight-fm.md](lightweight-fm.md#rung-2-in-the-languages-people-actually-use) |
