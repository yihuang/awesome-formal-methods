# Limits: what formal methods cannot do

> **TL;DR.** Formal methods are subject to hard mathematical limits, not engineering shortfalls.
> Any talk that doesn't state them is marketing. This page is the honesty section — and, used
> correctly, it is the most *credible* part of this wiki.

---

## 1. The mathematical limits

### Gödel's incompleteness theorems (1931)

For any consistent, sufficiently expressive, recursively axiomatised formal system:
1. There are true statements it cannot prove.
2. It cannot prove its own consistency.

**What this means in practice for engineers:** don't over-read it. Gödel does *not* say
"verification is hopeless" — your programs are finite objects and most of what you want to prove
about them is expressible. It says **no single formal system is a universal truth machine**, and
you will always be working relative to a chosen logic and axioms.

Common misconception to pre-empt: *"Gödel proves we can never verify software."* No. Gödel
proves that no logic is complete for *all* arithmetic truth. Software properties usually live in
much weaker fragments where you get decidability or good automation.

### The halting problem and undecidability (Turing 1936)

No algorithm decides whether an arbitrary program halts. Therefore, if you want a *terminating*
verifier, it must be incomplete somewhere.

### Rice's theorem (1953) — the one engineers should know

> **Every non-trivial semantic property of programs is undecidable.**

"Non-trivial" = true of some programs and false of others. So: "does this program ever divide by
zero", "does this function return the max of its inputs", "does this code leak a secret" — all
undecidable in general, for arbitrary programs.

**This is the theorem that explains the entire shape of the tool landscape.** It's why:

| You get | Because |
|---|---|
| Abstract interpretation, not exact analysis | it must over-approximate to terminate |
| `unknown` from SMT solvers | decidability is gone |
| Model checkers requiring finite-state models | decidability is restored by finiteness |
| Proof assistants requiring human/LLM guidance | the search isn't a computable function |
| Type systems being conservative and restrictive | the decidable approximation of correctness |
| Bounded model checking reporting "no bug up to depth k" | only a bound is decidable |

**In one line:** *"Rice's theorem is why every verification tool is either incomplete or
unsound. You don't get to choose otherwise; you only get to choose which side you fail on."*

### The soundness/completeness trade-off in one table

| Tool class | Sound? (never misses a real bug) | Complete? (always answers) | Fails by |
|---|---|---|---|
| Abstract interpretation | ✅ | ❌ | false alarms |
| Program verifiers (Dafny, Verus) | ✅ | ❌ | `unknown`, timeouts, annotation burden |
| Model checkers (unbounded, correct model) | ✅ | ❌ | state explosion; may not finish |
| Bounded model checkers (CBMC, Kani) | ✅ *for the bound* | ✅ | misses bugs deeper than the bound |
| Fuzzers, PBT, most linters | ❌ | ✅* | false negatives — they just don't find it |
| Types | ✅ | ❌ | reject correct programs |

Note the last few rows: **a fuzzer finding nothing is not evidence of absence.** That is the whole
reason formal methods exist. Conversely, a formal tool reporting "unknown" is not evidence of a bug.
Teaching this asymmetry is the highest-value thing on this page.

---

## 2. The engineering limits

### State-space explosion

`n` processes × `k` states = `kⁿ`. Mitigations (symmetry, partial order, symbolic, abstraction,
bounded search) push the wall out but don't remove it. Practical consequence: **model checking
works on protocols, not on applications.**

### Proof cost and brittleness

- **Proof-to-code ratio.** seL4: ~8,700 lines of C, ~200,000 lines of Isabelle proof, ~20
  person-years for the original verification
  ([verifiedsoftware.dev](https://verifiedsoftware.dev/case-studies/)). That's ~23× in lines.
- **Re-verification cost is lower** — the proof infrastructure exists — which is why seL4's
  framing "subsequent changes are cheaper to re-verify" matters and is often omitted.
- **Brittleness.** Refactoring a definition can break hundreds of proofs. Proof scripts are code
  without specs; they rot.

### The annotation bottleneck

The dominant cost in deductive verification is not solver time — it's writing the invariants.
And as §1 says, there is no algorithm for finding them. **This is the single biggest target for
AI assistance** and is why the AI-era chapter is where the field's optimism is concentrated.

### The trusted base

Every claim rests on unverified machinery. Be explicit:

| Claim | Trusted base |
|---|---|
| "Lean accepted this theorem" | the Lean kernel (~thousands of lines) + your axioms |
| "Z3 says unsat" | Z3 + your encoding — unless you use proof logging |
| "TLC found no violation" | TLC + your model + the config (bounds, constants) |
| "seL4 is verified" | Isabelle + the proof + **stated assumptions** (hardware, assembly, boot) |
| "CompCert preserves semantics" | Coq + the semantics *definition* + the C-to-assembly linkage |

And inside every proof assistant there is a way to lie:

```lean
theorem everything_is_easy : 1 = 2 := by sorry   -- compiles, proves nothing
```

Real proof engineering requires CI that rejects `sorry`/`admit`/`axiom` (see
[`demos/lean/`](../demos.md)). Proof assistants *have* had soundness bugs historically —
a famous class of incidents is a faulty termination/guard checker accepting a circular proof.
⚠️ *If you cite a specific incident, verify the version and date — these are usually
fixed quickly and precisely scoped, so precision matters.*

### Cost-benefit reality

| | Verify | Test |
|---|---|---|
| Upfront | high | low |
| Marginal per new feature | medium–high | low |
| Coverage | all inputs (in scope) | sampled |
| Output on failure | counterexample / unprovable obligation | failing example |
| Scales to | small critical cores | whole systems |
| Breaks when | spec changes | never (just goes stale) |

**The pragmatic conclusion:** formal methods are viable when `(cost of failure) × (probability) >
cost of verification`, and the cost of verification drops sharply if you pick a *small, stable,
critical core*. That's the whole industrial playbook — verify the 200-line protocol, not the app.

---

## 3. The scope limits (what FM structurally doesn't cover)

This is the list AWS itself gives. From the AWS experience report, they care about two classes of
problem:

> 1) bugs and operator errors that cause a departure from the logical intent of the system, and
> 2) surprising 'sustained emergent performance degradation' of complex systems that inevitably
> contain feedback loops.

**Formal methods address (1). They do not address (2).** That's an unusually clean statement of
scope from a practitioner, and it's worth emphasising verbatim.

The general pattern: **FM reasons about models of systems, not systems.** What falls outside:

| Outside the model | Why it bites |
|---|---|
| **Performance & emergent behaviour** | feedback loops, queueing collapse, cascading retries — no logical spec captures this |
| **Configuration & deployment** | the code was right; the rollout was wrong |
| **Human operators** | runbooks, on-call decisions, fat-finger errors |
| **Third-party dependencies** | the bug is in the library you call |
| **Requirements correctness** | the spec gap — the deepest limit of all |
| **Security in the full adversarial sense** | side channels, physical access, supply chain |
| **Whether anyone will maintain the proof** | proofs need owners; orphaned proofs are liabilities |

**The spec gap, restated:** tools check `model ⊢ property`. They cannot check that `property` is
what anyone wanted, or that `model` is reality. Verification makes you *precisely wrong* rather
than *vaguely wrong* — which is a genuine improvement, but not omniscience.

---

## 4. The verified-systems-have-failed file

These inoculate against the "so it's magic" reading and they teach the
right lesson: **the bug is almost never in the proof; it's in an assumption.**

| Incident | Year | What the lesson is |
|---|---|---|
| **Pentium FDIV** | 1994 | A lookup-table bug in floating-point division; a ~$475M write-off class event. It accelerated formal verification adoption in hardware, including Intel's own use of HOL Light to verify the floating-point division algorithm (John Harrison's work). Formal methods became standard in silicon *after* a public failure. |
| **Ariane 5 Flight 501** | 1996 | Reused Ariane 4 software; an unhandled arithmetic overflow on a *different* input range destroyed the vehicle. Not a coding bug — an **assumption-reuse** failure. The most quoted example of a specification/assumption error. |
| **Therac-25** | 1985–87 | Race conditions; earlier hardware interlocks removed in software. Testing the "happy path" gave false confidence. Pre-FM folklore that motivates the field. |
| **Knight Capital** | 2012 | Deployed code to the wrong servers; ~$440M lost in 45 minutes. Logic was fine; **deployment** was the model gap. |
| **Any "we verified it" project** | ongoing | Ask: *what were the stated assumptions, and who checks them in production?* |

**The meta-lesson to state explicitly:** formal methods shrink the *logic* risk dramatically and
do nothing for the *assumption, environment, and operations* risks. Mature programs pair
verification with assumption documentation, explicit assumption lists, differential testing, and
canary deployment. seL4's published proof has an explicit **assumptions** section; Cylinder/other
projects do the same. Look for it.

---

## 5. Anti-patterns to recognise at work

| Anti-pattern | Symptom | Fix |
|---|---|---|
| **Proof theatre** | "we have formal methods" but no CI check, specs stale | wire the checker into CI; fail the build |
| **Spec sprawl** | 20,000-line spec nobody reads | verify the 200-line core |
| **`sorry`-driven development** | theorems claimed, not proven | `#print axioms`, grep for `sorry`/`admit` |
| **Model-reality drift** | spec passed, code changed | differential testing (the Cedar pattern) |
| **One-shot verification** | verified once, then abandoned | budget for re-verification; make it a CI gate |
| **Verification as a gate, not a debugger** | team sees tool as blocker | lead with counterexamples — they're a feature |
| **Solving the wrong problem** | proving a property nobody cares about | start from a real incident (AWS's own start) |

---

## 6. The honest one-liner

> **Formal methods cannot tell you what to want. They can tell you, with certainty, whether what
> you asked for is what you'll get — and show you the exact input where it isn't.**

That's the promise. State the scope boundaries in the same breath and the argument will be trusted.

---

Next → [02-history/narrative.md](../02-history/narrative.md): how the field got here, including
the AI entanglement nobody expects.

## References

- **Gödel, K.** *Über formal unentscheidbare Sätze der Principia Mathematica und verwandter
  Systeme I.* 1931. [Stanford Encyclopedia](https://plato.stanford.edu/entries/goedel-incompleteness/)
- **Turing, A.M.** *On Computable Numbers, with an Application to the Entscheidungsproblem.* 1936 —
  the halting problem.
- **Rice, H.G.** *Classes of Recursively Enumerable Sets and Their Decision Problems.* Trans. AMS,
  1953. [PDF](https://www.ams.org/journals/tran/1953-074-02/S0002-9947-1953-0053041-6/S0002-9947-1953-0053041-6.pdf)
- **Wright, A. & Felleisen, M.** *A Syntactic Approach to Type Soundness.* 1994 — progress and
  preservation, the type-system analogue of soundness.
- **Klein, G. et al.** *seL4: Formal Verification of an OS Kernel.* SOSP 2009.
  [PDF](https://sel4.systems/Research/pdfs/sel4-sosp2009.pdf) — the ~8,700 lines of C / ~200,000
  lines of proof / ~20 person-years figures, and the assumptions section.
- **Cousot, P. et al.** *The ASTRÉE Analyzer.* ESOP 2005.
  [PDF](https://pcousot.github.io/publications/CousotEtAl-ESOP05.pdf) — false alarms, and the price
  of soundness.
- **Yang, X., Chen, Y., Eide, E., Regehr, J.** *Finding and Understanding Bugs in C Compilers.*
  PLDI 2011. [PDF](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf) — the Csmith study.
- **Pentium FDIV bug** — [Wikipedia](https://en.wikipedia.org/wiki/Pentium_FDIV_bug)
- **Ariane 5 Flight 501** — [ESA report](https://www.esa.int/Newsroom/Press_Releases/Ariane_5_Flight_501)
- **Knight Capital** — SEC filing and contemporaneous reporting; the deployment-error case study.
- [Gödel's incompleteness theorems](https://en.wikipedia.org/wiki/G%C3%B6del%27s_incompleteness_theorems)
