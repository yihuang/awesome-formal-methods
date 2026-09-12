# Hardware and cryptography: the domains where FM is already standard

> **TL;DR.** These are the two places where formal verification is not an experiment — it's the
> normal way of working, or close to it. They answer "does anyone actually do this?" — and the
> answer is that your CPU, your TLS connection, and your cloud provider's key management already
> depend on it.

---

## Part 1 — Silicon: you cannot ship a patch

**The structural argument.** Software's escape hatch is "ship a fix." Hardware has no such hatch.
A masking error costs a fab respin worth tens to hundreds of millions and months of schedule. That
asymmetry means hardware teams accepted large upfront verification costs decades before software
teams had any reason to.

**The state of practice.** Formal verification is a standard part of the modern chip design flow,
alongside simulation:

| Technique | What it proves |
|---|---|
| **Equivalence checking** | two RTL models (or RTL vs. gate netlist) have identical sequential behaviour — e.g. after optimising, retiming, or inserting scan chains |
| **Formal property verification (FPV)** | assertions hold for *all* input sequences, up to a bound or unbounded with a proof |
| **Model checking of control logic** | no deadlock, no unreachable states, no illegal states, correct arbitration |
| **Arithmetic formal verification** | IEEE-754 compliance, correct rounding, verified dividers and square-root units |

**Commercial tooling is mature and mainstream:** Cadence's **Jasper** platform (JasperGold,
including a Sequential Equivalence Checking app), Synopsys **VC Formal**, Siemens **Questa Formal**.
These are not research tools; they're line items in every serious chip budget.

### The founding incident: Pentium FDIV (1994)

A flaw in the SRT division lookup table returned incorrect results for certain floating-point
divisions. It was publicly embarrassing and expensive, and it is the standard historical reason
cited for the adoption of formal methods in hardware.

The deeper consequence is worth emphasising:

> After FDIV, Intel didn't just add testing — it started *proving* things. **John Harrison** at
> Intel formalised IEEE-754 binary floating-point arithmetic in **HOL Light** and verified the
> correctness of the floating-point division and square-root algorithms. A machine-checked proof
> that the *algorithm* rounds correctly, for all inputs.

That's the full arc: public catastrophe → practice change → and eventually the *theorem proving*
that the field's more pessimistic observers said would never pay off in industry.

**The lesson:** the adoption driver was a **specific, expensive, public failure** plus the
structural impossibility of patching. Look for that combination in your own organisation; that's
where the appetite will exist.

---

## Part 2 — Cryptography: the best-shaped verification target in existence

Cryptographic code satisfies the four conditions from
[case-studies.md](case-studies.md#cross-case-synthesis-the-four-conditions-for-a-good-verification-target)
almost perfectly:

| Condition | How crypto satisfies it |
|---|---|
| **Small** | a primitive is a few hundred lines; a KEM is a few thousand |
| **Stable** | AES, SHA-2/3, Curve25519, ChaCha20 don't change — they're standards |
| **Catastrophic when wrong** | a single wrong bit can reduce a 256-bit key to trivially breakable; there is no crash, no log line, no alert |
| **Precisely specifiable** | the specification *is* a mathematical document (FIPS/RFC) with exact semantics |

Plus one more property that makes it uniquely attractive: **crypto bugs are silent.** A memory bug
crashes; a crypto bug looks like everything is fine and the attacker reads your traffic. So the
empirical feedback loop that normally catches bugs is absent, which is precisely when you need
proof instead of testing.

### The flagship: HACL* / EverCrypt / Vale (F*)

A verified cryptographic library, plus **ValeCrypt** — a collection of verified **assembly** code
for primitives — combined into a single provider, **EverCrypt**
([hacl-star.github.io](https://hacl-star.github.io/HaclValeEverCrypt.html)).

Three things make this the best story in the wiki:

1. **It's deployed at scale, invisibly:** Firefox, the Linux kernel, nginx, WireGuard.
2. **It's fast.** Verified code that wins benchmarks, not just audits. Vale exists precisely to
   prove you don't have to trade performance for proof.
3. **It spans the whole refinement ladder** — from mathematical spec, down through C and *assembly*,
   with the extraction path itself being part of the trusted engineering story.

### The contemporary: Microsoft SymCrypt in Lean 4

Microsoft is progressively verifying SymCrypt — its core crypto library for Windows and Azure — in
**Lean 4**, producing machine-checked proofs that implementations correctly realise their
specifications. Same shape as HACL*: stable, shared, catastrophic-if-wrong.

### Emerging: verified Rust crypto

A newer pipeline takes production **Rust** cryptographic code and produces machine-checked
correctness proofs in **Lean 4**, using symbolic-extraction tooling (**Charon**, **Aeneas**, or
**Hax**) to lift Rust into a functional model. This is where the Rust + Lean ecosystems are
converging, and it's the most likely path for *your* team if you write Rust and want proofs.

⚠️ *Verify the current maturity of each extraction tool before recommending one — this is a
fast-moving area and the tooling status changes quarterly.*

---

## The side-channel problem (the honest caveat)

Functional correctness is **not** security. A bit-perfect AES implementation with a data-dependent
branch or table lookup leaks the key through timing and cache behaviour. Formal verification of
*functional* correctness says nothing about this.

What exists in this space:

| Concern | Approach |
|---|---|
| **Constant-time / timing side channels** | `ct-verif`, `FaCT`, dedicated constant-time analyzers; also compiler-level tooling (e.g. valgrind-based CT checks, `dudect` statistically) |
| **Speculative execution / microarchitecture** | mostly a hardware + empirical area; formal work exists but is hard |
| **Fault injection** | formal models of glitching; countermeasure verification |
| **Protocol-level security** | symbolic protocol verifiers (ProVerif, Tamarin) and cryptographic proof assistants (CryptoVerif, EasyCrypt) — a *different* FM subfield |

**The nuance that matters:** "formally verified crypto" usually means *functionally correct and, if
you're lucky, constant-time*. It does not mean "secure against an attacker with physical access."
Be precise; security engineers will catch over-claiming immediately.

---

## Related verified-hardware adjacent wins worth one mention each

| Project | What |
|---|---|
| **Verified boot chains** | seL4's *binary* verification closes the gap from proof to the artifact that actually runs — the same gap hardware teams face |
| **Verified RISC-V / processor cores** | formally verified processor implementations exist (e.g. verified RISC-V cores in Coq/Isabelle ⚠️ check current projects); also verified ISA semantics (Sail, ARM's official ASL) |
| **Verified memory consistency models** | formal models of x86/ARM/Power memory models; used to validate litmus tests |
| **Verified floating point** | Harrison's HOL Light library; used in hardware and in verified numerics |
| **zk-SNARK circuit verification** | proving that a circuit correctly implements its intended relation — an active area, since a circuit bug is a soundness break |

---

## What an ordinary software team should take from this section

You are not going to verify silicon or write an F* crypto library. Two transferable lessons:

1. **The adoption pattern is: unavoidable failure + small stable artifact + no escape hatch.**
   Find that pattern in your own system and that's your verification target. Crypto primitives and
   consensus protocols are the ones you're most likely to *consume* — so the action item is
   **use the verified library, don't roll your own**, and know that a verified option may exist
   (HACL*/EverCrypt, SymCrypt, `aws-lc`, verified implementations of the primitives you depend on).

2. **"Verified" needs a scope qualifier.** Functional correctness ≠ constant-time ≠
   side-channel-free ≠ secure. Every claim about verified crypto should carry that qualifier. It's
   the difference between credibility and a security-team objection you can't answer.

---

**Sources:** [hacl-star.github.io](https://hacl-star.github.io/HaclValeEverCrypt.html);
[verifiedsoftware.dev case studies](https://verifiedsoftware.dev/case-studies/);
Cadence JasperGold / Synopsys VC Formal product documentation;
[Pentium FDIV background](https://www.chiplog.io/p/how-intel-makes-sure-the-fdiv-bug);
John Harrison's HOL Light floating-point verification work.

Continue → [safety-critical.md](safety-critical.md): where regulation, not economics, drives
adoption.
