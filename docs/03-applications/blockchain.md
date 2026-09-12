# Blockchain: verification where the money is

> **TL;DR.** Smart contracts are the best-funded formal-verification target in the world, for
> obvious reasons: the code holds money, it is public, it is adversarial, bugs are irreversible, and
> gas makes performance a first-class constraint. That last constraint turned out to be the
> interesting one — **verification is not a brake on optimisation, it is a licence for it.** Once a
> proof is the review, you can let an optimiser (human or AI) do wildly aggressive things and simply
> require that the proof still goes through. That idea is now demonstrated in production: a Lean
> autoprecompiles optimiser matched its hand-written Rust counterpart, and a verified Yul compiler
> beats `solc` on gas.

This page covers the whole Ethereum verification stack: the EVM's own semantics, smart-contract
verifiers, verified compilers, zkVMs, and the performance argument that ties them together.

---

## Why this domain has the money

| Property | Consequence for verification |
|---|---|
| **The code holds funds** | failure cost is directly monetised, so verification budgets are justified |
| **Immutable once deployed** | you cannot ship a patch; you must be right the first time |
| **Fully adversarial** | an attacker reads your code and hunts the edge case; sampling is useless |
| **Public and small** | specs are readable; the relevant code is hundreds, not millions, of lines |
| **Gas is measurable** | performance is a hard, quantifiable objective — which makes "verified code can be *faster*" a testable claim rather than a slogan |
| **The spec is often the product** | an ERC standard or a protocol whitepaper *is* a specification; you rarely have to invent one |

That last row is underrated. Most application domains struggle with the
[specification gap](../01-fundamentals/specifications.md) because nobody wrote the spec. In
blockchain, ERC-20/721, the Yellow Paper, and consensus specs are written down, testable, and
usually unambiguous enough to formalise.

---

## Theory: the verification stack

Verification on Ethereum is not one activity. There are five layers, and they are largely
independent — a contract can be verified while the compiler below it is not, and vice versa.

```
   Layer 5   consensus & clients        (spec refinement; protocol safety/liveness)
   Layer 4   zk circuits & zkVMs        (soundness of the constraint system)
   Layer 3   compilers                  (Yul→EVM; Solidity→EVM; semantic preservation)
   Layer 2   smart contracts & policy   (functional correctness, invariants, access control)
   Layer 1   the EVM/Yul semantics      (what bytecode *means*)
```

**Layer 1 is the foundation for everything above it**, and it is the piece that changed most
recently.

### Layer 1 — the EVM's own semantics

You cannot prove anything about bytecode without defining bytecode. Two decades of work here:

- **KEVM** — a formal EVM semantics in the **K framework**, built for execution and reachability
  logic. It is the ancestor of most industrial EVM tooling (Kontrol is KEVM-based) and was used for
  the end-to-end verification of the Ethereum 2.0 deposit contract.
- **EVMYulLean** — a mechanisation of **EVM and Yul in Lean 4** targeting the **Cancun** hard fork,
  funded by an Ethereum Foundation grant and developed by Nethermind's formal-verification team.

EVMYulLean is the best worked example in existence of the [semantics](../01-fundamentals/semantics.md) ideas in this
wiki, and worth studying even if you never touch Ethereum:

| Aspect | How it was done | The generalisable lesson |
|---|---|---|
| **Fidelity** | Followed the **Ethereum Yellow Paper**, reusing its own function names (`Z`, `X`, `Ξ`, `Λ`, `Υ`) so the formalisation is eyeball-comparable to the paper | name things the same as the spec and you get reviewability for free |
| **Ground truth** | Treated the **official conformance test suite** as the ultimate source of truth, using KEVM to adjudicate where the suite and the Yellow Paper disagreed | when spec and implementation disagree, *decide* which wins and record why |
| **Conformance** | Passes **99.99% (22,330 / 22,332)** of the Cancun execution tests | executability is what makes a semantics credible |
| **Totality** | A `State.OutOfFuel` constructor, so the Yul interpreter is total in Lean | [fuel](../01-fundamentals/semantics.md#functional) is the standard way to make an interpreter total |
| **Control flow** | A `Checkpoint` state constructor to defer reasoning about `break`/`continue`/`leave` | you are allowed to design your semantics for provability, as long as you say so |
| **Impure edges** | Delegated precompiles to efficient Python/C implementations via **FFI** | quote the boundary; an FFI call is a trusted base |
| **Honesty** | A published **Limitations** list — the Yul model does not cover gas, `CREATE`/`CREATE2`, the `EXTCODE*` opcodes, or `SELFDESTRUCT` halting | this is what a trustworthy artifact looks like |

Two of those lines deserve emphasis.

**The disagreement between the Yellow Paper and the test suite is the real story.** The paper and
the tests differ on how gas is charged for memory expansion; the team followed the tests, and
verified their reading by checking how KEVM handled it. Two independent formalisations agreeing is
much stronger evidence than either alone — the same principle as [differential
testing](../03-applications/case-studies.md#the-three-reusable-industrial-patterns).

**The explicitly stated ambitions** for this artifact are the roadmap for the whole field: use it as
a trusted base for proving smart contracts, as the basis for a **verified Yul→EVM compiler**, and
potentially as the **official executable semantics** of the EVM.

### Layer 2 — smart contracts

The commercially mature layer. The tools split into three families:

**Specification languages** — how you say what you want:

| Tool | Approach |
|---|---|
| **Act** | storage updates, pre/post-conditions, contract invariants; backends for Coq, SMT solvers, and hevm |
| **Scribble** | annotations in Solidity source, compiled into concrete runtime assertions |
| **CVL** | Certora's specification language; property rules over a contract's methods |

**Program verifiers** — how it gets checked:

| Tool | Technique | Notes |
|---|---|---|
| **Certora Prover** | static analysis + constraint solving over CVL specs | the commercial standard; widely used on DeFi protocols |
| **Solidity SMTChecker** | SMT + Horn solving, **built into `solc`** | zero-install; the lowest-friction entry point in the entire wiki |
| **solc-verify** | annotated modular verification, SRI-CSL fork of `solc` | research-grade fork |
| **halmos** | symbolic *testing* for Solidity/EVM | tests with symbolic inputs instead of concrete ones |
| **Kontrol** | KEVM-based symbolic execution via Foundry | proofs and symbolic tests from the same test harness |

**Symbolic execution and equivalence** — finding bugs and proving rewrites:

| Tool | Use |
|---|---|
| **hevm** | symbolic execution engine *and equivalence checker* for EVM bytecode |
| **Manticore / Mythril** | symbolic execution for vulnerability detection |
| **Dafny** | general-purpose verifier also applied to contracts |

The **equivalence checker** idea in `hevm` is quietly the most important item in that table: it is
what lets you say "this optimised bytecode is equivalent to that reference bytecode", which is the
mechanism behind Layers 3 and the performance story below.

### Layer 3 — verified compilers

This is where the newest and most striking results are.

- **`yul-compiler`** (powdr-labs) — a verified optimising compiler from **Yul to EVM**. Experiments
  on the **Aave v4 and Uniswap v4** test corpora show it generating code with **better gas
  performance than `solc`**.
- **Verity** (LFG Labs) — a Lean 4 framework for writing smart contracts as a Lean EDSL, compiled
  through an IR to Yul and then to EVM. Every contract is three things: a **specification**, an
  **implementation**, and a **proof** tying them together. From the project's own walkthrough:

```lean
def mint_spec (to : Address) (amount : Uint256) (s s' : ContractState) : Prop :=
  s'.storageMap 1 to = add (s.storageMap 1 to) amount ∧
  s'.storage 2 = add (s.storage 2) amount ∧
  storageMapUnchangedExceptKeyAtSlot 1 to s s' ∧
  sameContext s s'

theorem mint_meets_spec (s : ContractState) (to : Address) (amount : Uint256)
  (h_owner : s.sender = s.storageAddr 0) :
  let s' := ((mint to amount).run s).snd
  mint_spec to amount s s' := by
  simp only [mint, onlyOwner, getMapping, setMapping]
  simp [h_owner]
```

Read that `mint_spec` carefully — it is a *complete* statement of what minting must do, including
the frame condition (`storageMapUnchangedExceptKeyAtSlot`) that says **nothing else changed**. That
fourth conjunct is the clause everyone forgets, and it is exactly the
[specification gap](../01-fundamentals/specifications.md#the-specification-gap-the-permanent-limitation) in practice: without
it, a `mint` that also drains every other balance would satisfy the spec.

Verity is a research project, not production infrastructure. Its importance is that it shows the
whole chain — surface language → spec → proof → Yul → EVM — with proofs checked at compile time.

### Layer 4 — zk: circuits and zkVMs

zk systems add a brutal property: a **soundness bug means the proof system accepts false
statements**, so the failure mode is not "a contract is wrong" but "the cryptography is a lie".

| Result | What happened |
|---|---|
| **SP1 Hypercube core verification** | Nethermind and Succinct Labs verified the correctness of the **entire core of the 64-bit SP1 Hypercube RISC-V zkVM in Lean**, with respect to the **official RISC-V Sail specification**. [sp1-lean](https://github.com/succinctlabs/sp1-lean) |
| **zk.golf** | An ongoing competition to build the **cheapest ZK circuits, proven correct in Lean 4**. Optimisation and proof as a single objective. [zk.golf](https://zk.golf/about) |
| **Arguzz** | The first automated tool for finding **soundness and completeness bugs in zkVMs** (RISC Zero, SP1, Jolt) — the testing counterpart to the proofs. [arXiv](https://arxiv.org/abs/2606.05632) |

Note the composition: SP1's core is verified **against Sail**, the ISA specification language used
for the official ARM and RISC-V specifications ([see semantics.md](../01-fundamentals/semantics.md#tools-for-writing-and-mechanising-semantics)).
Verifying a zkVM against the *official* ISA spec, rather than against a bespoke one, is what makes
the result meaningful.

And note that zk.golf makes *circuit size* the objective function. It is the clearest existing
example of "verified code is allowed to be aggressively optimised".

### Layer 5 — consensus and clients

Execution-layer clients are now written in Rust, Go, and Java, and each has verification efforts of
varying maturity; consensus specs are written down and partially formalised. Two anchors worth
knowing:

- **Runtime Verification's end-to-end verification of the Ethereum 2.0 deposit contract** — one of
  the earliest full-stack results on Ethereum, and still a good template.
- **Zellic's verification of WETH** — the most-used smart contract in DeFi, and a nice illustration
  that *popularity* is a reason to verify specific code.

This layer is the least complete of the five, and the most consequential.

---

## The performance thesis: the proof is the review

This is the most important development in the domain, and it inverts how most engineers think about
verification.

**The conventional view:** verification is a tax. You pay engineering time to get assurance, and you
should verify only where failure is catastrophic.

**The observed view:** *the proof is the review.* If a machine checks that a transformation
preserves the specification, then **no human needs to review the transformation**. That removes the
binding constraint on aggressive optimisation — namely, that someone has to be confident the clever
thing is correct.

Leonardo Alt states the mechanism plainly:

> "The mechanism is simple: the proof is the review. Nobody has to sit down and audit every
> aggressive rewrite, so you can point an AI at the code, let it optimize relentlessly, and only
> require that the proof still goes through."
> — [Performant Verified Software](https://leoalt.de/performant-verified-software), Sept 2026

The AWS precedent for this is a decade old and worth noting: automated reasoning let AWS engineers
remove locks and weaken ordering constraints they "would not have dared to" change otherwise
([AWS blog](https://aws.amazon.com/blogs/security/an-unexpected-discovery-automated-reasoning-often-makes-systems-more-efficient-and-easier-to-maintain/)).

### The flagship case: `apc-optimizer`

powdr's autoprecompiles optimiser turns a constraint system into a smaller equivalent one — the core
of making a zkVM fast. It is now formally verified in Lean, and the process is the story:

| Aspect | Detail |
|---|---|
| **Human-reviewed spec** | ~**500 lines** of Lean, thoroughly reviewed, frozen, and protected from agent edits |
| **AI-written implementation + proofs** | ~**10,000 lines** of Lean that **no human ever read** |
| **Enforcement** | CI type-checks every proof against the frozen spec and **rejects `sorry` and new axioms** |
| **Effort** | **one week of work by a single engineer**, plus a few days of review |
| **Result** | matched the hand-written Rust optimiser |

The measured effectiveness (higher is better, averaged over the 100 hottest RISC-V basic blocks):

| Metric | Rust implementation | Lean implementation |
|---|---|---|
| Variable effectiveness (correlates with proving time) | 4.092× | 4.082× |
| Bus effectiveness | 3.480× | 2.922× |
| Constraint effectiveness | 5.853× | **8.801×** |

So it is on par where it matters, better on one axis, and its runtime is slower — which is
irrelevant because the optimiser runs once at setup time.

The specification itself is a marvel of concision, and shows what "correct optimiser" actually means:

```lean
abbrev Optimizer (p : ℕ) := ConstraintSystem p → ConstraintSystem p × Derivations p

/-- An optimizer is correct if, for every input constraint system, replacing it with the optimized
    system is both sound and complete, and the optimizer respects the degree bound. -/
def Optimizer.isCorrect (optimizer : Optimizer p) (busSemantics : BusSemantics p) : Prop :=
  (∀ originalCS : ConstraintSystem p,
    let (optimizedCS, derivations) := optimizer originalCS
    (optimizedCS.isSoundReplacementOf originalCS busSemantics) ∧
    (optimizedCS.isCompleteReplacementOf originalCS busSemantics derivations))
  ∧ optimizerRespectsDegreeBound busSemantics optimizer
```

**Completeness is the clause that stops the trivial cheat.** Soundness alone permits an "optimiser"
that returns an unsatisfiable circuit — perfectly sound, and useless. Requiring that every input
assignment also has an output assignment is what forces the optimiser to actually work. This is the
same lesson as the `mint_spec` frame condition and the `is_a_permutation` clause in
[the sort example](lightweight-fm.md#rung-2-in-the-languages-people-actually-use): **the second
conjunct is where the bugs live.**

### The integration pattern: replace modules, don't rewrite

The Lean optimiser is not a rewrite of powdr. It is compiled to a static library and called from
Rust via **FFI**, as a drop-in replacement for one function:

```
   Rust pipeline  ──►  autoprecompiles-lean-ffi  ──►  Lean-verified optimiser
                       (FFI boundary — a trusted base you must state)
```

The authors' framing is the most transferable idea in this page: **"we can make existing software
safer module by module, proving equivalent code in Lean and replacing Rust modules/crates via FFI
until the whole system is proved."** You do not need to verify your system. You need to find the
module where correctness matters and performance is being left on the table, verify *that*, and
swap it in.

### Related results

- **`yul-compiler`** — verified Yul→EVM compilation beating `solc` on gas, as above.
- **`lean-zip`** — Kim Morrison's Lean implementation competing with Rust on runtime, showing the
  effect is not specific to compilers
  ([Why Lean is faster than Rust](https://kim-em.github.io/blog/2026-7-24-why-lean-is-faster-than-rust/)).
- **The autoresearch arenas** — [ecdsa.fail](https://ecdsa.fail), [zk.golf](https://zk.golf),
  [snark.fast](https://snark.fast), [better.codes](https://better.codes),
  [precompile.fast](https://precompile.fast). Several are explicitly *scored on machine-checked
  properties*, which turns formal verification into a leaderboard objective.

**The generalisable thesis, stated for any domain:**

> Verification's cost is usually framed as an upfront tax that buys assurance. In an optimisation
> regime, it is better understood as **removing the review bottleneck**: with a proof in place, the
> only requirement on a change is that the proof still holds, which means you can search the space of
> aggressive implementations automatically. Verified performance and verified correctness stop being
> a trade-off.

This is also the strongest argument that AI and formal methods are complements — see
[llm-proof-engineering.md](../04-ai-era/llm-proof-engineering.md).

---

## Tutorial: prove a contract invariant

A worked example, from the property to the proof, at three levels of rigour. The property is the one
everyone gets wrong: **transfers must not change the total supply.**

### Step 0 — State the property in English, and find the missing clause

> "`transfer` moves `amount` from the sender to the recipient."

That is not a specification. A specification is a conjunction:

```
  1. the sender's balance decreases by amount
  2. the recipient's balance increases by amount
  3. totalSupply is unchanged
  4. no other account's balance changes            ← the frame condition
  5. the event is emitted with the right arguments
```

Clauses 3 and 4 are the ones a naive test suite omits, and they are exactly what an attacker
exploits (mint-to-self, or a "transfer" that quietly touches `totalSupply`).

### Step 1 — The lowest-effort check: `SMTChecker`

It ships inside `solc`. Compile with the model checker enabled and it will try to prove your
`assert`s and detect overflow. Zero new tooling, works on an existing codebase. Expect
`unknown` results on anything arithmetic-heavy — that is the
[soundness/completeness trade-off](../01-fundamentals/limits.md#the-soundnesscompleteness-trade-off-in-one-table), not
a bug.

### Step 2 — A property rule (illustrative pseudo-CVL)

Certora-style specs state properties over the *interface*, not the implementation, which is what
makes them survive refactors:

```
// illustrative shape, not exact CVL — see the Certora docs for real syntax
rule transferPreservesTotalSupply() {
    env e; address from; address to; uint256 amount;
    uint256 supplyBefore = totalSupply();
    transfer(e, from, to, amount);
    assert totalSupply() == supplyBefore;
}

rule transferMovesExactlyAmount() {
    env e; address from; address to; uint256 amount;
    uint256 fromBefore = balanceOf(from);
    uint256 toBefore   = balanceOf(to);
    transfer(e, from, to, amount);      // reverts are handled by the prover
    assert balanceOf(from) == fromBefore - amount;
    assert balanceOf(to)   == toBefore + amount;
}
```

Note what these rules *do not* say: nothing about gas, nothing about ordering across accounts. A
verification rule is a precise, narrow claim — and the narrower it is, the more likely the prover
finishes.

### Step 3 — Push it up to Lean (Verity-style)

If you need the guarantee to be a proof rather than a solver result, write the spec in Lean and let
the kernel check it — the `mint_spec` / `mint_meets_spec` pair shown above is the template. The
essential structural move is identical: **write the frame condition explicitly.**

### Step 4 — Wire it into CI, and decide what is *not* covered

```yaml
# illustrative
- run: solc --model-checker-engine all --model-checker-targets all contracts/
- run: certoraRun certora/transfer.spec --verify Token:certora/token.conf
```

Then write down the trusted base. For a verified contract, the honest list is long:

| Trusted | Why |
|---|---|
| the Solidity compiler | it may miscompile your source ([CompCert](case-studies.md#2-compcert--the-verified-c-compiler) exists for C; the Solidity equivalent is Layer 3) |
| the EVM implementation of the client | unless it is itself verified |
| the semantics the verifier assumes | KEVM, EVMYulLean, or the tool's own model — each has stated limitations |
| the SMT solver | unless you use proof logging |
| the precompiles | EVMYulLean delegates them via FFI |
| everything economic | oracles, governance, MEV, bridge operators, upgrade keys |

That last row is the important one: **a fully verified contract can still lose all its money.**
Reentrancy is verifiable; a malicious oracle is not. Say so.

---

## Reference

### The stack, with entry points

| Layer | Verify what | Tools |
|---|---|---|
| 5 · Consensus & clients | protocol safety, liveness, client correctness | spec refinement; RV's deposit-contract verification; client-specific efforts |
| 4 · zk | circuit soundness, zkVM core, constraint systems | **SP1 Hypercube** (Lean), zk.golf, Arguzz |
| 3 · Compilers | Yul→EVM, Solidity→EVM | **`yul-compiler`**, **Verity**, (aspirationally) verified `solc` |
| 2 · Contracts | functional correctness, invariants, access control | **Certora**, **SMTChecker**, **halmos**, **Kontrol**, Act, Scribble, solc-verify, Dafny |
| 1 · Semantics | what bytecode means | **EVMYulLean** (Lean), **KEVM** (K), hevm |
| — · Cross-cutting | bytecode equivalence | **hevm**, differential testing |

### Where to start, by budget

| Effort | Action |
|---|---|
| **an afternoon** | enable `solc`'s SMTChecker on an existing contract; fix what it finds |
| **a day** | write a few `halmos` symbolic tests alongside your existing Foundry tests |
| **a week** | write property rules for your core invariants and run Certora/Kontrol in CI |
| **a month** | prove a critical module against a Lean spec, Verity-style, and keep the spec frozen in CI |
| **a quarter** | adopt the powdr pattern: extract a module to Lean, prove it, call it via FFI, drop the review burden |

### Further reading

- **Leo Alt**, *Performant Verified Software* —
  [leoalt.de/performant-verified-software](https://leoalt.de/performant-verified-software) — the
  performance thesis, and the best short argument for why verification pays for itself.
- **Leo Alt**, *Ethereum formal verification overview* —
  [github.com/leonardoalt/ethereum_formal_verification_overview](https://github.com/leonardoalt/ethereum_formal_verification_overview)
  — the most complete tool survey; supersedes the tool list here.
- **ethereum.org**, *Formal verification of smart contracts* —
  [ethereum.org](https://ethereum.org/developers/docs/smart-contracts/formal-verification) — the
  maintained, community-curated tool index.
- **powdr**, *Formally Verified Autoprecompiles* —
  [powdr.org](https://powdr.org/blog/formally-verified-autoprecompiles) — the AI-writes-the-proofs
  workflow, with numbers.
- **Succinct × Nethermind**, *SP1 Hypercube verification* —
  [blog.succinct.xyz](https://blog.succinct.xyz/nethermind-lean/) ·
  [zkevm.ethereum.foundation](https://zkevm.ethereum.foundation/blog/sp1-fv)

---

## References

- **Nethermind Research.** *How We Formalized Ethereum Execution: A Trustworthy Semantics of the EVM
  and Yul in Lean for Cancun.* 2026.
  [Blog](https://www.nethermind.io/blog/a-trustworthy-formal-model-of-evm-yul-in-lean) ·
  [EVMYulLean](https://github.com/NethermindEth/EVMYulLean) — the 99.99% (22,330/22,332) Cancun
  conformance figure, the Yellow Paper correspondence, the FFI treatment of precompiles, and the
  stated limitations all come from here.
- **Alt, L.** *Performant Verified Software.* leoalt.de, 9 Sept 2026.
  [Link](https://leoalt.de/performant-verified-software) — the "the proof is the review" framing,
  the `apc-optimizer` results, the `yul-compiler` gas comparison, and the autoresearch arenas.
- **powdr.** *Formally Verified Autoprecompiles.* [Link](https://powdr.org/blog/formally-verified-autoprecompiles)
  — the ~500-line reviewed spec vs ~10,000 lines of unreviewed AI-written Lean, the one-week effort,
  the CI enforcement of no-`sorry`/no-new-axioms, and the effectiveness table.
- **LFG Labs.** *Verity: Formally Verified Smart Contract Compiler (Lean 4).* [veritylang.com](https://veritylang.com/)
  — the `mint_spec` / `mint_meets_spec` example and the spec/implementation/proof structure.
- **Morrison, K.** *Why Lean is faster than Rust.* July 2026.
  [Link](https://kim-em.github.io/blog/2026-7-24-why-lean-is-faster-than-rust/) — `lean-zip`.
- **Succinct Labs & Nethermind.** *SP1 Hypercube core verification.*
  [blog.succinct.xyz](https://blog.succinct.xyz/nethermind-lean/) ·
  [zkevm.ethereum.foundation](https://zkevm.ethereum.foundation/blog/sp1-fv) ·
  [sp1-lean](https://github.com/succinctlabs/sp1-lean) — full-core zkVM verification against the
  RISC-V Sail specification.
- **zk.golf.** [About](https://zk.golf/about) — cheapest ZK circuits proven correct in Lean 4.
- **Arguzz.** *Automated detection of zkVM soundness bugs.*
  [arXiv:2606.05632](https://arxiv.org/abs/2606.05632). ⚠️ *This arXiv identifier also resolves to an
  LLM-proving benchmark; confirm the correct Arguzz reference before citing.*
- **Runtime Verification.** *KEVM* — [evm-semantics](https://github.com/runtimeverification/evm-semantics) ·
  *End-to-end verification of the Ethereum 2.0 deposit contract* —
  [blog](https://runtimeverification.com/blog/end-to-end-formal-verification-of-ethereum-2-0-deposit-smart-contract/)
- **Zellic.** *Formally Verifying the World's Most Popular Smart Contract (WETH).*
  [Link](https://www.zellic.io/blog/formal-verification-weth)
- **ethereum.org.** *Formal verification of smart contracts.*
  [Link](https://ethereum.org/developers/docs/smart-contracts/formal-verification) — source for the
  Act, Scribble, CVL, SMTChecker, solc-verify, KEVM, hevm, Manticore, and Mythril descriptions.
- **Solidity documentation.** *SMTChecker and Formal Verification.*
  [Link](https://docs.soliditylang.org/en/latest/smtchecker.html)
- **Ethereum Yellow Paper.** Wood, G. et al. [PDF](https://ethereum.github.io/yellowpaper/paper.pdf)
- **AWS Security Blog.** *An Unexpected Discovery: Automated Reasoning Often Makes Systems More
  Efficient and Easier to Maintain.*
  [Link](https://aws.amazon.com/blogs/security/an-unexpected-discovery-automated-reasoning-often-makes-systems-more-efficient-and-easier-to-maintain/)

## Further reading

- [semantics.md](../01-fundamentals/semantics.md) — the theory behind Layer 1.
- [case-studies.md](case-studies.md) — the same four conditions for a good verification target.
- [llm-proof-engineering.md](../04-ai-era/llm-proof-engineering.md) — the AI-writes-the-proofs
  workflow that makes `apc-optimizer` possible.
- [limits.md § The trusted base](../01-fundamentals/limits.md#the-trusted-base) — why the caveat
  table above is not pedantry.
