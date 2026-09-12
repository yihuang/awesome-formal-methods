# FM → AI: formal methods as guardrails for AI

> **TL;DR.** AI systems fail in ways that testing structurally cannot cover: correlated errors,
> adversarial inputs, unreadable models, and agents that take irreversible actions. Formal methods
> offer the only *sound* guardrails available — narrow, precise, and non-probabilistic. The
> engineering discipline is knowing how narrow, and layering them with everything else.

---

## 1. Four layers of AI risk, four kinds of verification

You cannot verify "the AI". You verify a *specific property of a specific artifact*. This table is
the map.

| Layer | Artifact | Property you might verify | Technique / tool |
|---|---|---|---|
| **Model** | weights, architecture | robustness to all ε-perturbations; reachability of unsafe states | NN verifiers: α,β-CROWN, Marabou, ERAN |
| **Output** | generated code, generated claims | the code satisfies a spec; the claim follows from the sources | deductive verification (Dafny, Kani, Lean); SMT over a policy model |
| **Action** | agent tool calls, API calls | this action is permitted by policy; the plan is safe before execution | runtime enforcement (AgentSpec), shields, proof-carrying actions |
| **System** | multi-agent trace, whole pipeline | non-interference; no information leak; invariant holds over all executions | hyperproperties, temporal-logic monitors, refinement |

**In short:** *"AI safety is not one problem. It's four problems at four layers, and formal
methods have something different to offer at each — always narrow, always precise."*

---

## 2. Why testing is structurally the wrong tool here

This is the argument that makes FM-for-AI more than a curiosity:

| Property of AI systems | Why sampling fails |
|---|---|
| **Correlated failure** | One model serves all requests. A single systematic error appears in every sample, so your test set agrees with your production failures. Ten thousand passing tests can share one blind spot. |
| **Adversarial inputs** | An attacker searches for the failure; your test set doesn't. Sampling the input space uniformly tells you nothing about the worst input. |
| **No readable control flow** | There is no invariant to review in a weight matrix. "It scored 94% on the eval" is not a robustness statement. |
| **Irreversible actions** | An agent that drops a table cannot be tested into safety. You need a *pre-execution* guarantee, not a post-hoc eval. |
| **Non-determinism** | Temperature, sampling, tool ordering, and concurrency make replays unstable; a pass today isn't a pass tomorrow. |
| **Natural-language specs** | "Don't be harmful" is not a testable predicate. It has to be converted into something checkable first — a specification problem. |

**And the guardrail tools people reach for are themselves probabilistic.** A classifier-based
guardrail, or an LLM-as-judge, has the same failure mode as the thing it's guarding: it can be
wrong, and its errors can correlate with the model's. Formal checks are *orthogonal* to that
failure mode. That's the structural argument for including them in a layered defence.

---

## 3. Layer 1 — Model-level: neural network verification

**The problem.** Given a trained network `f`, prove a property like:

> For all `x` with `‖x − x₀‖ ≤ ε`, `argmax f(x) = c`.

That's **certified robustness** — a statement about a continuum of inputs, not a sample.

**The techniques.** These are ordinary formal-methods machinery applied to a new artifact:

| Technique | Idea |
|---|---|
| **Linear relaxation / bound propagation** | compute sound linear bounds through each ReLU layer; the core of α,β-CROWN |
| **Branch and bound** | split the input domain and relax; the `β` in α,β-CROWN are optimised per-neuron bounds |
| **SMT / MILP encodings** | encode the network exactly and solve (Marabou, ERAN); precise but less scalable |
| **Abstract domains** | over-approximate reachable sets (used heavily in control/robotics) |

**The ecosystem is mature enough to have a competition:** **VNN-COMP**, the International
Verification of Neural Networks Competition. **α,β-CROWN** has won it in 2021, 2022, 2023, 2024,
and 2025 with the highest total score ([vnn-comp.github.io](https://vnn-comp.github.io/)).
Sibling tools: **Marabou**, **ERAN**, **MN-BaB**, **nn4sys**, **CROWN-family** variants.

**What this gives you that an eval cannot:**

- **A guarantee, not an estimate.** "94% robust on 10,000 samples" vs "robust for all inputs in
  this ε-ball".
- **A witness when it fails.** Like all FM tools, the counterexample is the product: here's an
  input, inside the ball, that flips the classification.
- **A training signal.** Certified bounds can be used *in* training (certified training), which is
  the same propose/check loop as [ai-for-fm.md](ai-for-fm.md) — verification inside the ML loop.

**Honest limits:**

| Limit | Consequence |
|---|---|
| **Scalability** | verification cost grows fast with network size; VNN-COMP benchmarks are small relative to frontier models |
| **Incompleteness** | verifiers can return `unknown`; sound but incomplete, as always |
| **Narrow guarantees** | ε-ball robustness ≠ semantic correctness. A provably robust net can be confidently wrong on clean inputs. |
| **Specification difficulty** | choosing the right ε, the right property, and the right input region is not automatic |
| **The guarantee is about the network, not the system** | preprocessing, quantization, the deployment stack, and the data distribution are all outside it |

**Also relevant:** verification of **learned controllers** — reachability and safety properties for
RL policies in control systems, where the cost of failure is physical.

---

## 4. Layer 2 — Output-level: verifying LLM-generated code and claims

### 4a. Verifying generated code

**The problem.** LLM-generated code is plausible, often test-passing, and subtly wrong in ways
correlated with the model's blind spots. Tests are written by the same model, or by the same
human, with the same misconceptions.

**The emerging pipeline:** *generate code + generate a specification + machine-check that the code
meets the spec.*

| Component | State of the art |
|---|---|
| **Target language** | Dafny, F*, Lean, Verus (Rust), or a C/Rust codebase + CBMC/Kani |
| **Spec generation** | LLMs write pre/post-conditions and invariants — the *new* bottleneck, and the most active research area |
| **Checking** | SMT solver or proof kernel — the sound half |
| **Evidence** | VeriBench (benchmark for verifying LLM-generated code); "Towards Formal Verification of LLM-Generated Code from Natural Language Prompts" ([arXiv:2507.13290](https://arxiv.org/abs/2507.13290)) |

**The design pattern worth naming: proof-carrying code for AI output.** Instead of trusting the
generator, require the generator to emit *both* the artifact and a machine-checkable certificate.
Then a small, trustworthy checker gates acceptance. This is the 1996 proof-carrying-code idea
(necro) applied to the AI supply chain — and it's the same propose/check architecture as everywhere
else in this wiki.

**Why it's the highest-value FM-for-AI work for engineers:**

- It slots into the workflow teams already have (AI writes code; CI checks it).
- It converts "the model says it's correct" into "the *checker* says it's correct."
- It directly attacks the 2026 bottleneck: [verification, not generation](verification-bottleneck.md).

### 4b. Verifying generated *claims* — the hallucination angle

The most commercially deployed FM-for-AI pattern right now is not about code at all. It's
**checking natural-language assertions against a formal model.**

**AWS Bedrock Guardrails — Automated Reasoning checks.** Instead of scoring an LLM response with a
classifier, this feature uses automated reasoning (SMT) to validate responses against a formal
policy encoding, with the stated goals of detecting hallucinations, surfacing unstated
assumptions, and explaining why correct statements are correct
([AWS docs](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html)).

**Why this is a landmark example:**

1. **It replaces a probabilistic check with a sound one** — a categorical difference, not a
   quality improvement.
2. **It produces explanations**, because SMT gives you a proof or a countermodel — not a score.
3. **It's a shipping product**, not a research paper. That's the "FM reached mainstream" claim in
   concrete form.
4. **It has the classic FM shape:** narrow, formalizable policy; sound check; human writes the
   specification (which is where the work really goes).

**The honest limit:** it only works where the claim can be reduced to a formal policy. Most
natural language cannot be. This is the specification gap again, and it should be stated.

---

## 5. Layer 3 — Action-level: verifying and constraining agents

This is the layer that matters most for 2026-era agentic systems, and where the field is moving
fastest.

### The problem

An agent with tools performs irreversible actions: `DELETE`, `transfer_funds`, `send_email`,
`deploy`, `exec_shell`. An evaluation after the fact is a post-mortem. You need a guarantee
**before execution**.

> "The AI agent is required to generate formal proofs demonstrating the safety of planned actions
> before being authorized to execute them. This approach parallels existing real-world practices
> (e.g. credit card checks before a transaction is authorized)."
> — *Guardians of the Agents*, ACM Queue ([source](https://queue.acm.org/detail.cfm?id=3762990))

That quote stands on its own. Note the analogy: **we already do proof-carrying authorization in
finance.** The novelty is the author, not the mechanism.

### The mechanisms

| Mechanism | How it works | Example |
|---|---|---|
| **Runtime enforcement DSL** | declarative rules with triggers/predicates/enforcement actions; a monitor intercepts the agent's actions and blocks or rewrites them | **AgentSpec** ([arXiv:2503.18666](https://arxiv.org/abs/2503.18666)) |
| **Shields** | a formally synthesised automaton sits between the policy and the environment; it *proves* an action is safe and masks unsafe ones | shielded safe RL; safety shields from temporal-logic specs |
| **Proof-carrying actions** | the agent must emit a machine-checkable certificate that the action satisfies the policy, checked *before* execution | Guardians of the Agents, policy-as-code |
| **Policy-as-code + automated reasoning** | the agent's request is evaluated against a formally modelled policy engine | Cedar-style authorization; Bedrock automated reasoning checks |
| **Constrained decoding** | restrict generation so that only actions satisfying a grammar/policy can be emitted | grammar-constrained decoding, schema enforcement |

### Runtime verification: the pragmatic middle

Full pre-execution proof is expensive. The broadly applicable version is **runtime verification**:
compile temporal-logic properties into monitors, and evaluate them over the agent's execution
trace, blocking or alerting on violation.

This is genuinely the sweet spot for teams today, because:

- It's the same shape as **liveness/readiness probes and circuit breakers** — familiar engineering.
- It **doesn't require proving anything about the model**, only about the trace.
- Temporal logic is the right language for it: `G(refund ⇒ F(audit_log))`,
  `G(spend(x) ⇒ total_spend ≤ budget)`, `G(tool_call) ⇒ authorized(actor, tool))`.

**The framing that lands:** *"You already run assertions on your service. Runtime verification is
assertions on your agent's decisions — with the properties written in a logic rather than in
`if` statements."*

---

## 6. Layer 4 — System-level: traces, hyperproperties, containment

Beyond a single action, the interesting properties are about *sets of executions*:

| Property class | Example | Why it needs hyperproperties |
|---|---|---|
| **Non-interference** | a user's query cannot influence another user's response through the agent | it's a relation between two traces, not a property of one |
| **Information flow** | secrets in the context cannot reach outputs | same |
| **Containment** | even if alignment fails, the agent cannot take catastrophic actions | safety independent of the alignment property |
| **Monotonicity / no-regression** | a policy update never widens permissions | property of a policy *family*, not one policy |
| **Fairness / non-discrimination guarantees** | decisions satisfy a formal fairness predicate | requires a formal model of the decision |

**Why this matters:** it's the most rigorous answer to "what can formal methods do
about AI safety?" The honest answer is: *it can guarantee containment properties that hold
regardless of whether the model is aligned.* That's a qualitatively stronger guarantee than any
behavioural eval, and it's why "defence in depth" for AI is not just more layers of classifiers —
some layers should be formally checked.

Also: **verification gives you the vocabulary to distinguish guarantees from evidence.** When
someone says "our agent is safe", the formal question is: *safe with respect to what property,
over what executions, under what assumptions?* ([limits.md](../01-fundamentals/limits.md))

---

## 7. Safe RL and shielding in one paragraph

In reinforcement learning, a **shield** is a formally verified component that observes the
proposed action and the state, and either permits the action or replaces it with a safe one (or
blocks it). The shield is *synthesised from a temporal-logic specification* and proved correct
against a model of the environment. This gives you:

- **Safe exploration** — the agent can learn without the environment ever reaching a bad state.
- **A guarantee independent of the learned policy** — the policy can be arbitrary; the shield
  constrains the closed loop.
- **A clean separation of concerns** — the ML does the learning; the formal method does the safety.

The catch is the usual one: it requires a model of the environment good enough to prove the shield
correct, and the guarantee only holds inside that model. See
[*Shields for Safe Reinforcement Learning*, CACM](https://cacm.acm.org/research/shields-for-safe-reinforcement-learning/).

---

## 8. What does NOT work yet

Be aggressive about this section — overselling is the fastest way to lose an ML reader.

| Claim you should NOT make | Reality |
|---|---|
| "We can formally verify a frontier LLM." | Nobody can. NN verification scales to small networks and specific properties (robustness, reachability) — not to a 100B-parameter transformer's semantics. |
| "Formal verification solves AI alignment." | It verifies *narrow properties of specified artifacts*. "Aligned" is not yet a formal property. |
| "A verified guardrail makes the agent safe." | It makes one property hold. The rest of the system, the model's other behaviours, the data, and the deployment remain unverified. |
| "Evals are just weak proofs." | No. Evals sample; proofs quantify. They are different categories and you need both. |
| "We can auto-generate the specs." | LLM-generated specs are useful drafts; they *are* the new bottleneck and are not trustworthy as ground truth. |
| "Proofs are cheap now because of AI." | Drafting got cheaper; ownership, maintenance, and comprehension did not. Generated proofs are auditable artifacts and need owners. |
| "We verified the network, so the system is verified." | Quantization, preprocessing, the serving stack, the data distribution, and the surrounding code are all outside the proof. |

**Also underappreciated:** the **specification problem for AI is harder than for software**, because
the requirements are frequently normative ("be helpful"), contested, and context-dependent.
Formal methods force you to write something down — which is valuable even when what you write down
is wrong, because then you can argue about it.

---

## 9. What an AI/ML engineer should actually do

Ordered by return on effort:

1. **Write down the invariants you actually care about.** Budget caps, permission boundaries,
   data-flow rules, rate limits. Plain English first. Half the value is in discovering that nobody
   agreed on them.
2. **Encode the ones with exact structure in a monitor.** Runtime verification over the agent
   trace. Temporal logic or a DSL like AgentSpec. Block on violation; log everything.
3. **Put the irreversible actions behind a formally checked gate.** Proof-carrying action or a
   policy engine (Cedar-style). If you can't prove it, at minimum require an explicit authorization
   decision for it.
4. **For code generation, add a verification rung to CI.** Start with property-based tests (rung 2);
   move one critical function to Kani/Dafny (rung 4). See
   [lightweight-fm.md](../03-applications/lightweight-fm.md).
5. **Where robustness matters, use a verifier, not just an eval.** α,β-CROWN / Marabou for small
   models and specific properties. Report `unknown` honestly.
6. **Never let a probabilistic guardrail be your only guardrail.** Layer it. Classifiers fail in
   correlated ways with the model they guard; formal checks fail differently, which is the point.
7. **Keep the specification next to the code, in the repo, in CI.** A guardrail that isn't
   continuously checked is documentation
   ([anti-patterns](../01-fundamentals/limits.md#5-anti-patterns-to-recognise-at-work)).

---

## 10. The generative-AI irony

```
     The AI era made two things true at once:

     (1)  We now build systems whose behaviour we cannot read
          — weight matrices, agent plans, generated code.

     (2)  We now build systems whose errors are CORRELATED
          — one model, one blind spot, scaled to every request.

     Sampling cannot address either. That is not a
     limitation of our test suites; it is a category error.

     Formal methods are the only technology we have that
     gives a guarantee over ALL inputs, ALL interleavings,
     or ALL adversary perturbations within a budget.

     They are narrow. They are the wrong tool for most things.
     They are the right tool for the things you cannot afford
     to be wrong about.
```

---

**Sources:** [Guardians of the Agents, ACM Queue](https://queue.acm.org/detail.cfm?id=3762990);
[AgentSpec, arXiv:2503.18666](https://arxiv.org/abs/2503.18666);
[AWS Bedrock automated reasoning checks](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html);
[VNN-COMP](https://vnn-comp.github.io/); [α,β-CROWN](https://github.com/Verified-Intelligence/alpha-beta-CROWN);
[Verified LLM-generated code, arXiv:2507.13290](https://arxiv.org/abs/2507.13290);
[Shields for Safe RL, CACM](https://cacm.acm.org/research/shields-for-safe-reinforcement-learning/).

Continue → [verification-bottleneck.md](verification-bottleneck.md): the economic argument that ties
both directions together.
