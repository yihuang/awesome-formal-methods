# Why now? The AI-era case for formal methods

> **TL;DR for engineers.** For most of your career, "formal methods" meant a research tool used
> by avionics and CPU teams. The reason it didn't reach you was never that it didn't work — it's
> that *writing the specification and the proof cost more than writing the code*. AI changed that
> ratio. Meanwhile AI made a new problem: we now generate code, policies, and plans faster than we
> can check them. Formal methods are the only mature answer to "how do I trust this at scale?"

---

## The three-part argument

### 1. Verification was always the bottleneck — AI just made it visible

Engineering has a fixed budget for confidence. Historically we spent it like this:

```
spec clarity  <  code  <  tests  <  production incidents
```

AI coding agents compress the middle of that chain dramatically. Anthropic's 2026 agentic-coding
report describes engineers shifting "from writing code to coordinating agents that write code,"
with a Rakuten case of an agent doing 7 hours of autonomous work in a 12.5M-line codebase
([source](https://claude.com/blog/eight-trends-defining-how-software-gets-built-in-2026)).
The same report notes the countervailing finding: developers report being able to **"fully
delegate" only 0–20% of tasks**, despite using AI in ~60% of their work. The gap between
*generated* and *trusted* is the bottleneck.

When generation is cheap and verification is expensive, **verification becomes the constraint on
throughput**. That is exactly the regime where formal methods stop being a luxury.

### 2. The economics of formal methods changed

The classic objection is real and documented:

> "In industry, formal methods have a reputation of requiring a huge amount of training and
> effort to verify a tiny piece of relatively straightforward code, so the return on investment
> is only justified in safety-critical domains such as medical systems and avionics. Our
> experience with TLA+ has shown that perception to be quite wrong."
> — *Use of Formal Methods at Amazon Web Services* ([PDF](https://lamport.azurewebsites.net/tla/formal-methods-amazon.pdf))

Three things have moved since that objection was formed:

1. **Solvers got absurdly good.** Modern SAT/SMT solvers discharge in milliseconds what needed a
   research project in 1990. You now call them from CI.
2. **The tooling moved into normal languages.** Kani runs `cargo kani` on Rust. Dafny is a
   programming language with a verifier. TLA+ checks a spec you'd otherwise write as pseudo-code.
   The "exotic PhD language" barrier is mostly gone.
3. **AI lowered the specification cost.** The expensive part was never the proof search — it was
   *knowing what to prove* and *writing the invariant*. LLMs are surprisingly good at proposing
   invariants, translating informal statements into formal ones (autoformalization), and driving
   proof search. This is the newest and least settled shift, but it is real
   ([see 04-ai-era/ai-for-fm.md](../04-ai-era/ai-for-fm.md)).

### 3. AI created a new class of trust problem that tests cannot cover

Testing samples. It cannot tell you what happens on the input distribution you didn't imagine.
This was always true, but it mattered less when the code was written by a human who could be held
to a mental model. With AI systems, the failure modes are different in kind:

- **LLM-generated code** can be plausible, pass tests, and be subtly wrong in a way that
  correlates across all the tests you thought to write.
- **Agents take actions**, not just produce text. An agent that decides to issue a refund, drop
  a table, or call an external API needs a guarantee *before* execution, not an eval after.
- **Neural networks** are statistical objects with no readable control flow; "it scored well on
  the eval set" is not a robustness statement.

For each of these, formal methods offer something testing structurally cannot: a statement about
**all** inputs, **all** interleavings, or **all** adversary perturbations within a budget. See
[fm-for-ai.md](../04-ai-era/fm-for-ai.md).

---

## The honest counter-arguments

| Objection | Reality |
|---|---|
| "Formal methods have been 10 years away for 50 years." | True. `03-applications/adoption-gap.md` documents the real barriers: training cost, tool churn, and the fact that most bugs are *specification* bugs, not proof bugs. |
| "You still can't verify the spec is what you meant." | Correct, and it is the deepest limitation. The spec gap is permanent. Formal methods buy *precision*, not *omniscience* ([limits.md](../01-fundamentals/limits.md)). |
| "AI can just verify things too." | Partially. LLMs are good at *proposing* proofs; only a checker can *accept* one. The value of a proof comes from the machine-checkable kernel, not the author. |
| "We can't even write good tests." | Then formal methods will be hard too — but they scale differently. A weak property plus a solver still explores every input; a weak test suite explores the ones you wrote. |
| "Our system is too big." | You never verify the whole system. You verify the 200-line consensus state machine or the 40-line unsafe block. Knowing *what to scope* is the skill. |

---

## The short version

```
        THEN                                NOW
  code expensive                    code cheap (AI)
  verification expensive            verification still expensive
  → verify only what must not fail  → verification is the constraint
  → FM = avionics + silicon         → FM = the missing half of AI-assisted engineering
```

**The practical ask:** don't adopt a proof assistant tomorrow. Adopt the *habit* of writing one
precise property that must hold for all inputs, and use the cheapest tool that can check it. That
is the entire on-ramp ([lightweight-fm.md](../03-applications/lightweight-fm.md)).

## References

- **Newcombe, C. et al.** *Use of Formal Methods at Amazon Web Services.* 2014/2015.
  [PDF](https://lamport.azurewebsites.net/tla/formal-methods-amazon.pdf) — the "perception is quite
  wrong" quotation, and formal methods as an enabler rather than insurance.
- **AWS Security Blog.** *An Unexpected Discovery: Automated Reasoning Often Makes Systems More
  Efficient and Easier to Maintain.*
  [Link](https://aws.amazon.com/blogs/security/an-unexpected-discovery-automated-reasoning-often-makes-systems-more-efficient-and-easier-to-maintain/) —
  the same argument from the other direction: verification leading to *faster* systems.
- **Anthropic.** *Eight trends defining how software gets built in 2026.* Jan 2026.
  [Link](https://claude.com/blog/eight-trends-defining-how-software-gets-built-in-2026) — the
  "~60% of work / 0–20% fully delegable" figure. ⚠️ Vendor-published; see the
  [confidence ledger](../research-notes.md#4-confidence-ledger).
- **Alt, L.** *Performant Verified Software.* Sept 2026.
  [Link](https://leoalt.de/performant-verified-software) — the strongest statement of the
  "verification buys performance" thesis, with production numbers.
- **Rice, H.G.** *Classes of Recursively Enumerable Sets and Their Decision Problems.* 1953 → see
  [limits.md](../01-fundamentals/limits.md) for why testing cannot be made sound.
- [Ethereum formal verification overview](https://github.com/leonardoalt/ethereum_formal_verification_overview) —
  an actively maintained list of what is *actually* verified in a domain where failure is
  monetised.
