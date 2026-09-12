# AI → FM: AI as an accelerator for formal methods

> **TL;DR.** Formal verification has an architecture that is *uniquely* well-matched to modern AI:
> **finding a proof is hard (search), checking one is cheap (deterministic)**. LLMs are search
> amplifiers; kernels are sound filters. Put them in a loop and you get something that is both
> creative and trustworthy — which neither half is alone. That loop is why a 2020 research demo
> became, by 2026, a system producing new mathematical results with machine-checked certificates.

---

## 1. The architecture (the one diagram to remember)

```
                    ┌─────────────────────────────────────────┐
                    │   PROPOSER (LLM / RL policy)            │
                    │   suggests: tactics, lemmas, invariants │◄──────┐
                    └────────────────┬────────────────────────┘       │
                                     │ candidate proof step           │
                                     ▼                                │
                    ┌─────────────────────────────────────────┐       │
                    │   CHECKER (Lean/Rocq/Isabelle kernel,   │       │
                    │   or SMT solver) — cheap, sound,        │       │
                    │   deterministic, unarguable             │       │
                    └────────────────┬────────────────────────┘       │
                                     │ verified / counterexample      │
                                     ▼                                │
                    ┌─────────────────────────────────────────┐       │
                    │   LEARNING SIGNAL (RL reward / rejection │───────┘
                    │   sampling / search guidance)            │
                    └─────────────────────────────────────────┘
```

Three properties make this loop special, and they're worth stating explicitly on a slide:

1. **The reward signal is perfect.** Unlike RLHF, there is no reward model to hack. Lean says yes
   or no. This is why formal mathematics has become a favoured RL testbed.
2. **Verification is cheap relative to generation.** You can afford to check a million candidates.
   This is the classic generate-and-test asymmetry, upgraded so the "test" is *sound*.
3. **Failure is informative.** A failed proof attempt yields a tactic state — a structured, dense
   learning signal, not a scalar.

**Note the inversion:** AI needs FM. Reinforcement learning requires a reliable environment that
can score attempts. Formal systems are the best such environment anyone has found for reasoning.
So this is not AI helping a legacy field — it's AI discovering it needs the legacy field.

---

## 2. The arc: 1956 → 2026

| Year | Milestone | Significance |
|---|---|---|
| **1956** | Logic Theorist (Newell, Shaw, Simon) | The *first AI program* was a theorem prover. The loop is 70 years old. |
| 2020 | **GPT-f** (Polu & Sutskever) | LLM generates proof steps in Metamath; first credible neural proof search. |
| 2023 | **LeanDojo**, ReProver, COPRA | Retrieval-augmented proving; Lean becomes *infrastructure* rather than a demo target. |
| 2023 | **Lean FRO founded** | Dedicated engineering organisation for Lean — the ecosystem matures. |
| **2024** | **AlphaProof + AlphaGeometry 2, IMO 2024: 4/6 problems, 28/42, silver-medal level** | The breakthrough. RL + formal verification beats previous AI by a wide margin. |
| 2025 | DeepSeek-Prover-V2, **Goedel-Prover** (open-source SOTA), Kimina-Prover | Open weights close the gap; provers become a commodity. |
| 2025 | **Harmonic "Aristotle"**: gold-medal-equivalent on IMO 2025 problems, Lean-verified | Provable reasoning becomes a *product category*. |
| 2025 | **AlphaProof published in *Nature*** (Nov 2025) | Peer-reviewed. The result is real. |
| **2026** | **OpenAI "Ten Advances in Mathematics and Theoretical Computer Science"** | Ten problems, each open ≥10 years, with **Lean 4 certificates published on GitHub**. |
| 2026 | **Comparator** (Lean FRO) + nanoda independent kernel | Infrastructure for *trustworthy judging* of machine-generated proofs. |

---

## 3. AlphaProof in detail (the reference implementation of the idea)

From the *Nature* paper (Nov 2025), the architecture is worth walking through because it *is* the
template:

| Component | Detail |
|---|---|
| **Environment** | Lean 4. State = the tactic state (hypotheses + goals). Action = a tactic, emitted as text. Reward = proof found, with a bonus for shorter proofs. |
| **Proof network** | A **3-billion-parameter** encoder–decoder transformer producing (a) a *policy* over promising tactics and (b) a *value* estimating proof difficulty. |
| **Search** | AlphaZero-style tree search guided by the network; for multi-goal proofs, return is the **minimum** over subgoals (i.e., the hardest branch dominates). |
| **Bootstrapping** | Supervised fine-tuning on **~300,000 state–tactic pairs** extracted from human-written Mathlib proofs. |
| **Curriculum** | A Gemini-based autoformalizer translated **~1 million natural-language problems into ~80 million formal Lean problems** — "vastly exceeding the scale of all other available datasets". Key insight: *even a mis-formalized statement is a valid formal problem to prove or disprove*, so fidelity is not required for training data. |
| **Test-time RL (TTRL)** | For a hard target problem, generate formal *variants*, run focused RL on them, then attack the original. This is what cracked problems that scaling search alone could not. |
| **Result** | P1, P2, P6 by AlphaProof; P4 by AlphaGeometry 2 → 4/6, **28/42**, silver-medal range (one point below the 2024 gold threshold). Combinatorics P3, P5 unsolved. |
| **Cost** | Computation time **far exceeding human contestants** — days, not hours. Honest reporting. |

**Two transferable insights for non-mathematicians:**

1. **Autoformalization is the data engine.** The bottleneck was never proof search data; it was
   *formal* data. Generating 80M formal problems from 1M informal ones is the move that made
   training viable. The analogous move for software is generating formal *specifications and
   invariants* from informal code comments, tickets, and docs.
2. **TTRL is how you attack a specific hard problem.** Do focused self-improvement on variants of
   your actual target. This generalises: for a hard verification obligation, generate variants and
   learn the pattern.

---

## 4. 2026: new mathematics with machine-checked certificates

**The headline.** On 1 August 2026, OpenAI published *Ten Advances in Mathematics and Theoretical
Computer Science* — ten results, each on a problem that had seen no progress on its main result for
at least a decade — together with **Lean 4 formalisations in a public repository**
([github.com/openai/ten-proofs](https://github.com/openai/ten-proofs)). The work was produced by an
internal version of a model called **Astra**, not a publicly released system.

The ten results, as listed in the repository README:

| # | Result | Field |
|---|---|---|
| 1 | Improved asymptotic upper bounds on **high-dimensional sphere packing**, reaching the Cohn–Elkies threshold | discrete geometry |
| 2 | Exponentially stronger upper bounds for **binary and spherical codes** at every minimum distance | coding theory |
| 3 | A construction of a **non-sofic group** | group theory |
| 4 | A **counterexample to Connes's rigidity conjecture** | von Neumann algebras |
| 5 | New **arithmetic circuit lower bounds** for the permanent, including `n⁴/log n` | complexity theory |
| 6 | **Exponential parallel repetition** for arbitrary finite two-player quantum games | quantum information |
| 7 | **Polynomial-factor hardness of approximation for the closest vector problem** (GapCVP) | lattices/crypto |
| 8 | **Ehrhart's volume conjecture** — sharp maximum volume in every dimension | geometry of numbers |
| 9 | **Superexponential lower bound for multicolor triangle Ramsey numbers** (Erdős problem 183) | combinatorics |
| 10 | **Counterexamples to the compactness and degeneracy conjectures** in extremal graph theory (Erdős problems 146, 180) | combinatorics |

**Why this is the perfect closing example for the talk:**

- **The artifacts include Lean 4 certificates.** Verified with Lean 4.32.0 + mathlib. That's the
  whole thesis: AI proposes, a kernel disposes.
- **It's a *new results* claim, not a benchmark score.** Benchmarks were the 2024 story;
  2026 is "new theorems".
- **The cost figure is astonishing** ⚠️: reporting suggests roughly **$2,000** at API rates for all
  ten results combined, according to secondary coverage. *Verify this before using it — it is a
  secondary-source claim and the press has varied.* If it holds up, it's the single most striking
  number in the talk.
- **It's contested on process, not on correctness.** Formalisation moves the dispute from "is the
  proof right?" to "is the *credit and norm* right?" — which is a much better dispute. See below.

**The caveats you must present (this is what makes the slide credible):**

| Caveat | Detail |
|---|---|
| **Not peer-reviewed at announcement** | Announced by blog post + repo, not a journal. Formal certificates address *proof correctness*, not community acceptance. |
| **The model is not public** | Astra was an internal version of a not-yet-released model. Results are not independently reproducible by the community. |
| **The Leiden Declaration (June 2026)** | An international group of mathematicians published a statement warning that AI is challenging core values of mathematics: announcements via press release rather than peer review, use of published research without consent, and threats to attribution and proof integrity. Endorsed by figures including the IMU. |
| **Autoformalization risk** | The failure mode nobody can see: a proof of a *subtly different statement* than intended. Addressed by tooling (§5), not by the proof itself. |

> **Slide-ready nuance:** *"The proofs are machine-checked. That's not the same as the results
> being accepted. Mathematics is now arguing about credit and process — because the correctness
> argument is largely settled by the kernel. That's a remarkable place for a field to be."*

---

## 5. The tooling layer that makes this trustworthy

This is the part most AI-math coverage skips, and it's where the engineering lesson lives.

### The problem: "Lean said yes" is not enough

Three attacks on a machine-checked claim:

1. **Statement mismatch.** The proof establishes a theorem *almost* identical to the claimed one.
   (The AI-math version of "the test asserts the wrong thing".)
2. **Axiom smuggling.** The proof depends on an added `axiom`, or leaves a `sorry`.
3. **Kernel trust.** You're trusting one implementation of the kernel.

### The answer: independent judging

**Comparator** (`leanprover/comparator`) is exactly the "trustworthy judge for Lean proofs":

| Mechanism | Purpose |
|---|---|
| `challenge_module` vs `solution_module` + explicit `theorem_names` | checks the solution proves the **challenge** statement, not a lookalike |
| **Axiom checking** (`Comparator/Axioms.lean`) | detects extra axioms / unsound dependencies |
| Sandboxing via `landrun` | isolates the check |
| `lean4export` + optional **nanoda** kernel (independent Rust implementation) | can re-check the proof with a *second, independently written* kernel |

The repo's test suite is a catalogue of exactly the attacks you'd worry about:
`def_hole`, `theorem_hole_issue`, `simple_axiom_issue`, `def_hole_axiom_issue`,
`type_mismatch`, `kind_mismatch`, `quot_mismatch`, `primitive_issue`, `opaque_value`, `proj_trick`.

**The lesson for engineers, which generalises far beyond mathematics:**

> **When the prover is untrusted, you must verify the *claim*, not just the proof.** Checking a
> proof term tells you "something follows from the axioms you supplied." It does not tell you
> "the thing you wanted follows from the axioms you meant."

That's the same discipline as [the specification gap](../01-fundamentals/specifications.md) —
reappearing in a new costume. **This is the single best AI-era slide in the wiki**, because it
shows the field solving an entirely new problem with an old idea (shrink the trusted base).

### The agentic layer

- **Lean LSP / MCP servers** (`lean-lsp-mcp` and friends) expose Lean's goal state, diagnostics,
  and search to LLM agents via the Language Server Protocol — making Lean a tool an agent can
  actually drive.
- **Autoformalization tooling** is now its own subfield with surveys and benchmarks
  (*Autoformalization in the Era of Large Language Models: A Survey*, arXiv 2505.23486).
- **The library is the knowledge base:** mathlib reached ~**288,041 theorems** and ~**136,932
  definitions** contributed by **772 people** (Sept 2026,
  [mathlib stats](https://leanprover-community.github.io/mathlib_stats.html)) — and reportedly
  around 5 million lines of code. It is both a library and a training corpus.

---

## 6. Benchmarks and the state of play

| Benchmark | What it measures |
|---|---|
| **miniF2F** | olympiad-level problems across multiple systems; the standard small benchmark |
| **ProofNet** | undergraduate-level textbook theorems, Lean/Isabelle |
| **PutnamBench** | Putnam competition problems — a much harder bar |
| **FormalMATH** | large-scale formalised competition mathematics |
| **RLMEval** | evaluation suite for proving *and* statement autoformalization |
| **VeriBench** | benchmark for verifying LLM-generated code |

**State of play, honestly:**

- **Olympiad level: essentially solved** by the best systems (with large compute budgets and, for
  contest problems, expert manual formalisation of statements).
- **Research level: demonstrated, contested on process, not yet reproducible in the open** (the
  2026 OpenAI results).
- **Verification of *software* at research level: early.** Theorem proving in Lean and verifying a
  Rust service are different problems; progress on the first does not automatically transfer.

---

## 7. What does NOT work yet

| Limitation | Why it matters |
|---|---|
| **Autoformalization fidelity** | The dominant failure mode. A model can prove a subtly different statement, and only Comparator-style tooling catches it. |
| **Compute cost** | AlphaProof took *days* per problem where humans took hours. Sample efficiency is still poor. |
| **Long-horizon library knowledge** | Models struggle to find and reuse the right lemma in a 288k-theorem library. Retrieval is a hard subproblem. |
| **Brittle proofs** | Generated proofs break when mathlib definitions change. Nobody wants to own them. |
| **Contamination** | Benchmark leakage; "solved" problems that were in training data. |
| **Specification writing** | AI is decent at formalising *known* statements. Generating a *correct novel specification* — the thing software actually needs — is much harder. |
| **Evaluation of genuine novelty** | Benchmarks measure known-answer performance; the 2026 claims required human refereeing to assess at all. |
| **Governance/attribution** | The Leiden Declaration problem: who is credited, what consent was given, and whether press-release mathematics is acceptable. |

**The honest framing:** *AI has made proof search a learning problem and it works spectacularly on
problems with a crisp formal statement and a verifier. It has not made specification easy, it has
not made verification cheap in general, and it has not changed the fact that a proof is only as
good as the statement it proves.*

---

## 8. What an ordinary engineering team can use *today*

Not IMO silver medals. These:

| Use | Concrete form | Maturity |
|---|---|---|
| **Draft a TLA+ spec** | ask an LLM to turn a design doc into PlusCal/TLA+, then check with TLC | good first-draft quality; expect to fix syntax and semantics |
| **Suggest loop invariants** | for a Dafny/Kani/Verus obligation that times out, ask for candidate invariants | genuinely useful; the classic bottleneck |
| **Explain a counterexample** | paste TLC's trace or an SMT model, ask for the mechanism | high value, low risk |
| **Translate a property into formal syntax** | "every request is eventually acknowledged" → LTL/TLA+ | useful, verify by hand |
| **Repair a broken proof** | after a library upgrade, ask for the fix | saves real time in Lean/Rocq/Isabelle |
| **Turn an incident into a property** | "here's the bug we had, write the property that would have caught it" | **the highest-ROI use in this table** |
| **Property-based test generation** | generate Hypothesis/proptest properties for a module | very accessible; rung 2 of the ladder |

**The rule:** *let the LLM propose; let the machine dispose.* Never accept an AI-produced formal
artifact without running the checker, and never accept a proof without checking *what was proved*.

---

**Sources:** [AlphaProof, *Nature* (2025)](https://www.nature.com/articles/s41586-025-09833-y);
[DeepMind IMO blog](https://deepmind.google/blog/ai-solves-imo-problems-at-silver-medal-level/);
[openai/ten-proofs](https://github.com/openai/ten-proofs);
[Lean FRO Comparator](https://github.com/leanprover/comparator);
[mathlib statistics](https://leanprover-community.github.io/mathlib_stats.html);
[Autoformalization survey, arXiv:2505.23486](https://arxiv.org/abs/2505.23486);
[Leiden Declaration coverage](https://www.universiteitleiden.nl/en/news/2026/06/leiden-declaration-warns-ai-is-challenging-the-core-values-of-mathematics).

Continue → [fm-for-ai.md](fm-for-ai.md): the other direction, where formal methods guard AI.
