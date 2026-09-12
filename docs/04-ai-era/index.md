# AI era — index

Why the AI era is the moment formal methods stop being a niche. Two directions, one engine.

```
                        ┌──────────────────────────────────────┐
                        │   the same asymmetry:                │
                        │   propose = hard   ·   check = cheap │
                        └──────────────────┬───────────────────┘
                                           │
                 ┌─────────────────────────┴─────────────────────────┐
                 ▼                                                   ▼
   ┌──────────────────────────────┐                   ┌──────────────────────────────┐
   │   AI → FM                    │                   │   FM → AI                    │
   │   AI as ACCELERATOR          │                   │   FM as GUARDRAIL            │
   │                              │                   │                              │
   │  • autoformalization         │                   │  • NN robustness certificates │
   │  • neural theorem proving    │                   │  • verifying LLM-written code │
   │  • invariant suggestion      │                   │  • agent policy enforcement   │
   │  • proof repair              │                   │  • runtime monitors/shields   │
   │                              │                   │  • hallucination checks       │
   │  payoff: new theorems with   │                   │  payoff: sound guarantees     │
   │  machine-checked certificates│                   │  where evals can't reach      │
   └──────────────────────────────┘                   └──────────────────────────────┘
                 │                                                   │
                 └─────────────────────────┬─────────────────────────┘
                                           ▼
                        ┌──────────────────────────────────────┐
                        │  THE ECONOMIC DRIVER                 │
                        │  generation got cheap;               │
                        │  verification is the bottleneck      │
                        └──────────────────────────────────────┘
```

---

## Pages

| Page | What it covers | Talk use |
|---|---|---|
| [ai-for-fm.md](ai-for-fm.md) | **AI accelerates FM.** AlphaProof in detail, the 2026 OpenAI results with Lean certificates, autoformalization, the independent-judging layer (Comparator), what doesn't work yet. | The "wow" segment; 5–8 min |
| [fm-for-ai.md](fm-for-ai.md) | **FM guards AI.** Four layers: model robustness, generated code, agent actions, system hyperproperties. AgentSpec, shields, Bedrock automated reasoning, verified-code pipelines. | The "why should I care" segment for AI/ML folks; 5–8 min |
| [verification-bottleneck.md](verification-bottleneck.md) | **The economics.** Why verification is now the constraint, the two asymmetries, the verification gap, what the market is doing, what changes for an individual engineer. | The core economic argument |

---

## The five claims this section makes

1. **AI and formal methods are complements, not rivals — and AI needs FM more than FM needs AI.**
   RL requires a reliable verifier as a reward signal, and formal systems provide the best one we
   have.
2. **The architecture is the same in both directions:** an untrusted proposer and a trusted,
   cheap checker.
3. **Proof search is now a machine-learning problem and it works** — olympiad-level mathematics is
   essentially solved, and in 2026 new research-level results shipped with machine-checked Lean
   certificates.
4. **Machine-checked ≠ accepted.** The 2026 disputes are about attribution and process, not
   correctness — which is itself a striking statement about how far verification has come, and
   requires an independent judging layer (Comparator) to catch statement mismatch and axiom
   smuggling.
5. **Formal methods for AI are narrow, and that's the point.** They give guarantees that hold
   *regardless of whether the model is aligned or correct* — containment, policy compliance,
   robustness within a ball. That's a categorically different kind of assurance than another
   classifier.

---

## The three sentences that summarise this

1. **AI made code cheap and trust expensive.**
2. **Checking is cheap; searching is hard — so AI proposes and kernels dispose.**
3. **The engineer's new core skill is stating precisely what must be true, and picking the cheapest
   sound check for it.**

---

## One-line summary of each direction

> **AI → FM:** *a search amplifier plugged into a sound filter.*
>
> **FM → AI:** *a sound filter plugged into an unreadable, correlated, action-taking system.*
