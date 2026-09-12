# Fundamentals — index

The durable ideas. These pages don't go stale; the AI-era chapter does.

| Page | Core question | Talk use |
|---|---|---|
| [specifications.md](specifications.md) | What does "correct" even mean, and who writes it down? | The skill the audience actually needs |
| [logics.md](logics.md) | What language are specs written in? | Appendix / one-slide "five logics" table |
| [techniques.md](techniques.md) | How is a claim checked? | The big taxonomy slide |
| [automated-reasoning.md](automated-reasoning.md) | What makes automation work? | The "checking is cheap, searching is hard" slide — key AI-era bridge |
| [limits.md](limits.md) | What is impossible? | The credibility slide; use before Q&A |

## The five sentences that summarise this section

1. **A specification is a precise statement of what must hold; the tool proves an implication, so
   a wrong specification yields a very expensive way of being wrong.** ([specifications.md](specifications.md))
2. **There are five families of verification — theorem proving, model checking, deductive
   verification, abstract interpretation, and types — and they differ in who supplies the
   ingenuity and how they fail.** ([techniques.md](techniques.md))
3. **The asymmetry that makes the field work: finding a proof is hard, checking one is cheap.**
   ([automated-reasoning.md](automated-reasoning.md))
4. **Rice's theorem guarantees every tool is either incomplete or unsound; you choose which side
   to fail on.** ([limits.md](limits.md))
5. **Formal methods shrink logic risk and do nothing for requirement, environment, deployment,
   or operational risk.** ([limits.md](limits.md#3-the-scope-limits-what-fm-structurally-doesnt-cover))

## The conceptual ladder (for slide ordering)

```
   why does this matter now?      → docs/00-orientation/why-now.md
            ↓
   what is the territory?         → docs/00-orientation/taxonomy.md
            ↓
   what does correct mean?        → specifications.md
            ↓
   how do you check it?           → techniques.md
            ↓
   what powers the automation?    → automated-reasoning.md
            ↓
   what are the walls?            → limits.md
            ↓
   who actually did it?           → ../03-applications/
            ↓
   what changed in the AI era?    → ../04-ai-era/
```
