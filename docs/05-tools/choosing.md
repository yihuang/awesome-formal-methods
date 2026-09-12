# Choosing a tool

> **TL;DR.** Don't choose by "which is best" — choose by *what you are reasoning about*, then by
> *whether it fits your build system*. A tool that isn't in CI is not adopted.

---

## The decision tree

```
START: what do you want to be true?
│
├─ "The design has no bugs in any interleaving"
│   └─► MODEL CHECKING
│        ├─ distributed protocol / consensus / retries ──► TLA+ (+ TLC, PlusCal)
│        │       too big for TLC? ─────────────────────► Apalache
│        ├─ data model / relational structure, want quick ─► Alloy
│        ├─ concurrent algorithm, message passing ──────► SPIN
│        └─ the system is Rust ─────────────────────────► Stateright
│
├─ "This function is correct for ALL inputs"
│   └─► DEDUCTIVE VERIFICATION
│        ├─ C ──────────► CBMC (bounded) / Frama-C (annotation) / SPARK
│        ├─ Rust ───────► Kani (bounded, push-button, unsafe blocks)
│        │                Verus / Creusot / Prusti (unbounded, annotations)
│        ├─ Java/Scala ─► OpenJML, KeY, Stainless
│        ├─ Python ─────► Nagini (research-ish)
│        └─ new code, want the friendliest ─► Dafny
│
├─ "The whole codebase has no runtime errors / UB"
│   └─► ABSTRACT INTERPRETATION
│        ├─ C/C++ commercial ─► Astrée, Polyspace
│        ├─ C open source ────► Frama-C (Eva)
│        ├─ multi-language CI ► Infer
│        └─ Rust MIR ─────────► MIRAI
│
├─ "This theorem of mathematics is true"
│   └─► PROOF ASSISTANT
│        └─ Lean 4 (mathlib + AI ecosystem) / Rocq / Isabelle
│
├─ "This protocol has no attacks" / "this crypto is correct"
│   └─► ProVerif or Tamarin (symbolic) · EasyCrypt/CryptoVerif (computational)
│       and: use HACL*/EverCrypt rather than writing your own
│
├─ "This authorization policy is right"
│   └─► Cedar + automated reasoning · or SMT over your own policy model
│
├─ "This neural network is robust in this ε-ball"
│   └─► α,β-CROWN (SOTA) · Marabou (exact, small) · ERAN (abstraction)
│
├─ "This agent cannot take forbidden actions"
│   └─► RUNTIME ENFORCEMENT
│        ├─ declarative rules on agent behaviour ─► AgentSpec-style monitors
│        ├─ authorization before action ─────────► Cedar / policy engine
│        ├─ RL policy safety ────────────────────► synthesised shields
│        └─ validate LLM output vs policies ─────► automated reasoning checks
│
└─ "I don't know where to start / no budget"
    └─► LIGHTWEIGHT (rung 0–2, free, today)
         ├─ types + strict compiler flags
         ├─ property-based testing ──► Hypothesis / proptest / fast-check
         └─ fuzzing ─────────────────► language-native / AFL++ / OSS-Fuzz
```

---

## The selection matrix (fit × cost)

| | Cheap to learn | Expensive to learn |
|---|---|---|
| **High assurance, small scope** | Kani 🟢 · Alloy 🟢 · Hypothesis 🟢 | Lean 🟢 · Isabelle 🟢 · Rocq 🟢 |
| **Medium assurance, whole codebase** | Infer 🟡 · Frama-C 🟡 · MIRAI 🔵 | Astrée 🟢 (commercial) · Polyspace 🟢 |
| **Design-level, protocol scope** | TLA+/PlusCal 🟢 · Stateright 🔵 | Apalache 🟡 · mCRL2 🟡 |
| **Specialised** | ProVerif 🟢 · Cedar 🟢 · α,β-CROWN 🟢 | EasyCrypt 🟡 · ct-verif 🔵 |

**Reading the matrix:** the top-left is where adoption happens. Start there and move right/down
only when you have a specific reason.

---

## The 6 selection heuristics

1. **Prefer the tool that lives in your existing build system.** `cargo kani` beats a beautiful
   tool with a custom build. `pytest`-integrated Hypothesis beats a standalone fuzzer.
2. **Prefer bounded/sound to unbounded/expensive, to start.** Bounded model checking finds real
   bugs and never lies about what it proved *for the bound*. Upgrade only when you genuinely need
   unbounded.
3. **Prefer counterexamples to proofs, for your first project.** A tool that produces a concrete
   failing input will be adopted by your team. A tool that says "could not prove" will not. This is
   why model checkers and fuzzers succeed where verifiers stall — **and why you should choose a
   bug-finding entry point even if your end goal is verification.**
4. **Prefer a mature ecosystem with published specs.** TLA+ has Paxos/Raft specs you can read.
   Lean has mathlib. Choosing an empty ecosystem costs you months.
5. **Match the tool to the artifact's lifetime.** Stable artifact → expensive tool is fine.
   Churning artifact → pick something that re-checks cheaply in CI.
6. **Never choose a tool whose trusted base you can't describe.** "It's sound because Z3 says so"
   is fine for a code review; for a safety case you want proof logging or a verified checker.

---

## Anti-patterns in tool selection

| Anti-pattern | Why it fails | Instead |
|---|---|---|
| Picking the most powerful tool first | Lean for a retry-logic bug is 3 months of nothing | match scope to tool |
| Picking a tool with no CI story | verified once, then stale forever | require a CI gate from day one |
| Verifying the whole system | cost explodes superlinearly | verify the small critical core |
| Choosing a tool the team can't read | nobody maintains the spec | readability is a requirement |
| Rolling your own crypto, parser, or consensus | the verified options exist | use HACL*/EverCrypt, Cedar, etc. |
| Ignoring the refactor cost | breaking a definition breaks 200 proofs | isolate verified cores behind stable interfaces |
| Trusting the model to judge itself | correlated failure | independent checking (Comparator-style) |
| Treating "verified" as unqualified | over-claiming destroys credibility | always state scope + assumptions + trusted base |

---

## Getting started: install reality check

Verified in *this* environment (Sept 2026):

| Tool | Status here | Install |
|---|---|---|
| **Lean 4** | ✅ `lean 4.32.0`, `lake` present at `~/.nix-profile/bin` | elan / [lean-lang.org](https://lean-lang.org/) |
| Python 3 | ✅ present | — |
| Node/npx | ✅ present | — |
| TLA+, Dafny, Z3, Coq, Alloy | ❌ not installed | see below |

```bash
# Lean 4 (recommended: elan toolchain manager)
curl -sSf https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh | sh -s -- -y
lake new myproof && cd myproof && lake exe cache get && lake build

# Property-based testing, the free rung
pip install hypothesis
cargo add --dev proptest     # Rust
npm i -D fast-check          # TypeScript

# Rust push-button verification
cargo install --locked kani-verifier && cargo kani setup

# TLA+ : download the TLA+ Toolbox, or use the VS Code extension, from lamport.azurewebsites.net/tla/tla.html

# Dafny
#   download the release binary from github.com/dafny-lang/dafny

# Z3
pip install z3-solver        # or the standalone binary from github.com/Z3Prover/z3
```

⚠️ *Install commands change; verify against the project's own site before relying on them.*

**The one-hour starter for a Java/Go/Python/Rust engineer:** don't install anything. Write three
property-based tests for the function that last broke production. See
[lightweight-fm.md](../03-applications/lightweight-fm.md#the-5-things-to-do-in-your-first-week).

---

## The takeaway

> **"Pick the cheapest tool that can check the property you actually care about, and put it in
> CI. If it can't produce a counterexample, your team will abandon it in a sprint."**

## References

- **Install and getting-started documentation** for the tools named on this page:
  [Lean/elan](https://leanprover-community.github.io/get_started.html) ·
  [TLA+ Toolbox and VS Code extension](https://lamport.azurewebsites.net/tla/tla.html) ·
  [Dafny](https://dafny.org/dafny/Installation) ·
  [Kani](https://model-checking.github.io/kani/install-guide.html) ·
  [CBMC](https://www.cprover.org/cbmc/) · [Z3](https://github.com/Z3Prover/z3) ·
  [Hypothesis](https://hypothesis.readthedocs.io/) ·
  [proptest](https://github.com/proptest-rs/proptest) ·
  [fast-check](https://fast-check.dev/) · [Rocq](https://rocq-prover.org/) ·
  [Isabelle](https://isabelle.in.tum.de/) · [Alloy](https://alloytools.org/)
  ⚠️ Install commands change; always check the project's own site.
- **Newcombe, C. et al.** *Use of Formal Methods at Amazon Web Services.* 2014/2015 — the
  "exhaustively testable pseudo-code" framing, and the argument that a tool must produce
  counterexamples to be adopted.
- **Lamport, L.** *Specifying Systems.* [Free online](https://lamport.azurewebsites.net/tla/book.html)
- **Kani** — [github.com/model-checking/kani](https://github.com/model-checking/kani) ·
  **CBMC** — [cbmc-documentation.readthedocs.io](https://cbmc-documentation.readthedocs.io/)
- **Alt, L.** *Ethereum formal verification overview* —
  [github.com/leonardoalt/ethereum_formal_verification_overview](https://github.com/leonardoalt/ethereum_formal_verification_overview) —
  a good model for how to write a tool *decision guide* rather than a tool list.
