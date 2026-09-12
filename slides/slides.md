---
theme: default
title: AI Made Code Cheap. Trust Is Still Expensive.
info: |
  Formal methods for engineers, in the AI era.
  Companion wiki: https://yihuang.github.io/awesome-formal-methods/
class: text-center
highlighter: shiki
lineNumbers: false
drawings:
  persist: false
transition: slide-left
mdc: true
colorSchema: dark
aspectRatio: 16/9
fonts:
  webfonts: []
  provider: none
# No `fonts:` block on purpose — declaring webfonts makes Slidev fetch them at
# build time. style.css declares font stacks with system fallbacks instead, so
# the deck renders identically offline and does not depend on a CDN.
---

<div class="kicker">a tech sharing · 45 minutes · no maths required</div>

# AI Made Code Cheap.
# <span class="accent">Trust Is Still Expensive.</span>

<div class="subtitle">
For fifty years, formal methods were the expensive option you only reached for in avionics and
silicon. Then AI inverted the economics.
</div>

<div class="footer-note">
Companion wiki → <span class="mono">yihuang.github.io/awesome-formal-methods</span>
</div>

<!--
Opening. Don't explain formal methods yet. Land the provocation and move on fast.
Pace: 30 seconds.
-->

---
layout: center
---

<div class="huge">1956</div>

<div class="lead">
The first AI program ever written was called <b>Logic Theorist</b>.
It proved 38 of the first 52 theorems in <i>Principia Mathematica</i>.
</div>

<v-click>

<div class="punch">
It was a theorem prover.
</div>

</v-click>

<div class="attrib">Newell, Shaw &amp; Simon, 1957</div>

<!--
THE HOOK. This is the twist nobody expects. Pause after "It was a theorem prover."
Then: the two fields didn't converge recently — they started entangled.
-->

---
layout: center
class: text-center
---

# The thing nobody said out loud

<div class="lead">
Your agent just wrote 400 lines. It compiles. The tests pass.
</div>

<v-click>

<div class="punch big">
<em>How do you know?</em>
</div>

</v-click>

<v-click>

<div class="muted small">
You wrote the tests. So did the model. You share the same blind spot.
</div>

</v-click>

<!--
The provocation. Don't rush the last line — "you share the same blind spot" is the thesis of the
whole second half of the talk.
-->

---
layout: center
---

# What this talk is

<div class="grid2">

<div>
<div class="h3">Not</div>
<ul class="dim">
<li>A tour of 40 tools</li>
<li>A lecture on type theory</li>
<li>"Everyone should learn Lean"</li>
</ul>
</div>

<div>
<div class="h3 accent">But</div>
<ul>
<li><b>The three theorems</b> that make this hard forever</li>
<li><b>The four ideas</b> that make it possible anyway</li>
<li><b>Why AI changed the economics</b> — and didn't change the limits</li>
<li><b>One thing you can do on Monday</b></li>
</ul>
</div>

</div>

---
layout: section
---

<div class="part">Part I</div>
# The impossible thing
<div class="partsub">Three theorems that ended a dream — and defined our entire design space</div>

---
layout: center
---

<div class="quote-block">

> <span class="drop">L</span>et us know; we will know.

<div class="attrib">David Hilbert's programme, paraphrased — <em>wir müssen wissen, wir werden wissen</em></div>

</div>

<v-click>

<div class="lead centered">
Hilbert wanted a <b>mechanical procedure</b> that could decide any mathematical statement.
Not "probably". Not "usually". <span class="accent">Always.</span>
</div>

</v-click>

<!--
Set up the dream properly. Hilbert is the optimist. Everything after is the bill.
-->

---
layout: center
class: text-center
---

<div class="huge red">1931</div>

# Gödel

<div class="lead">
In any consistent formal system strong enough to describe arithmetic,
there are true statements it <b>cannot prove</b> — and it cannot prove its own consistency.
</div>

<div class="subtitle muted">No formal system is a universal truth machine.</div>

---
layout: center
class: text-center
---

<div class="huge red">1936</div>

# Turing

<div class="lead">
No algorithm decides whether an arbitrary program halts.
</div>

<div class="subtitle muted">
Which means: no terminating verifier can be complete.<br>
If it always answers, it sometimes lies.
</div>

---
layout: center
class: text-center
---

<div class="huge red">1953</div>

# Rice

<div class="punch big">
Every non-trivial property of programs is undecidable.
</div>

<div class="lead">
"Does this function ever divide by zero?"<br>
"Does it return the maximum?"<br>
"Does it leak a secret?"
</div>

<div class="subtitle muted">
All undecidable. In general. For arbitrary programs. Forever.
</div>

---
layout: center
---

# Why Rice is the most useful theorem you've never heard of

<div class="subtitle">It explains the entire shape of the tool landscape.</div>

<table class="clean">
<tr><td>Why abstract interpretation over-approximates</td><td class="mono dim">it must terminate</td></tr>
<tr><td>Why SMT solvers answer <code>unknown</code></td><td class="mono dim">decidability is gone</td></tr>
<tr><td>Why model checkers need finite models</td><td class="mono dim">finiteness restores decidability</td></tr>
<tr><td>Why proof assistants need a human or an AI</td><td class="mono dim">proof search isn't computable</td></tr>
<tr><td>Why type systems are conservative</td><td class="mono dim">they're the decidable approximation</td></tr>
</table>

<v-click>

<div class="callout">
<b>The only choice you get:</b> every verification tool is either <b>incomplete</b> or
<b>unsound</b>. You don't get to avoid the choice. You only get to choose which side you fail on.
</div>

</v-click>

---
layout: center
---

# Choose your failure mode

<table class="clean">
<thead><tr><th></th><th>Never misses a bug</th><th>Always answers</th><th>Fails by</th></tr></thead>
<tr><td>Abstract interpretation</td><td class="yes">yes</td><td class="no">no</td><td>false alarms</td></tr>
<tr><td>Program verifiers</td><td class="yes">yes</td><td class="no">no</td><td><code>unknown</code>, timeouts</td></tr>
<tr><td>Model checkers</td><td class="yes">yes</td><td class="no">no</td><td>state explosion</td></tr>
<tr class="hl"><td><b>Fuzzers, tests, most linters</b></td><td class="no">no</td><td class="yes">yes</td><td><b>silence</b></td></tr>
</table>

<v-click>

<div class="punch">
A fuzzer finding nothing is not evidence of absence.
</div>

<div class="muted centered">That single sentence is why this field exists.</div>

</v-click>

---
layout: center
---

# The asymmetry

<div class="lead centered">Everything in this talk follows from one fact:</div>

<div class="asym">
  <div class="asym-card hard">
    <div class="asym-label">find a proof</div>
    <div class="asym-verdict">intractable</div>
    <div class="asym-note">NP-hard. Undecidable in general.</div>
  </div>
  <div class="asym-card easy">
    <div class="asym-label">check a proof</div>
    <div class="asym-verdict">cheap</div>
    <div class="asym-note">Deterministic. Milliseconds. A kernel does it.</div>
  </div>
</div>

<v-click>

<div class="punch">
Search is expensive. Checking is cheap.<br>
<span class="accent">That is the shape of a neural network's strengths and weaknesses.</span>
</div>

</v-click>

<!--
THE central slide of the talk. Everything else is a consequence.
LLMs are brilliant at proposing. Kernels are brilliant at checking. Neither is either.
-->

---
layout: center
class: text-center
---

# So the architecture writes itself

<svg viewBox="0 0 760 250" class="diagram">
  <defs>
    <marker id="arw" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto">
      <path d="M0,0 L7,3 L0,6 z" fill="currentColor"/>
    </marker>
  </defs>
  <rect x="20" y="30" width="200" height="70" rx="10" class="box ai"/>
  <text x="120" y="60" class="t">PROPOSER</text>
  <text x="120" y="82" class="ts">LLM · RL policy</text>

  <rect x="540" y="30" width="200" height="70" rx="10" class="box kernel"/>
  <text x="640" y="60" class="t">CHECKER</text>
  <text x="640" y="82" class="ts">kernel · SMT solver</text>

  <path d="M225,65 L535,65" class="flow" marker-end="url(#arw)"/>
  <text x="380" y="55" class="ts">candidate proof · code · invariant</text>

  <path d="M535,105 C400,175 260,175 225,105" class="flow back" marker-end="url(#arw)"/>
  <text x="380" y="196" class="ts">error · goal state · counterexample</text>
</svg>

<v-click>

<div class="lead">
<b>Generate and test — except the test is sound.</b>
</div>

</v-click>

<div class="muted small">And note the direction of dependence: <b>RL needs a verifier.</b> Formal methods aren't the legacy half of this loop.</div>

---
layout: section
---

<div class="part">Part II</div>
# The ideas that work anyway
<div class="partsub">Four ideas carry the entire field</div>

---
layout: center
---

<div class="idea-num">Idea 1</div>

# Propositions are types. Proofs are programs.

<div class="lead">The Curry–Howard correspondence.</div>

<table class="clean mono small">
<tr><td>implication <code>A → B</code></td><td>a function</td></tr>
<tr><td>conjunction <code>A ∧ B</code></td><td>a pair</td></tr>
<tr><td>disjunction <code>A ∨ B</code></td><td>a tagged union</td></tr>
<tr><td>true</td><td>the unit type</td></tr>
<tr class="hl"><td><b>false</b></td><td><b>the empty type</b></td></tr>
<tr><td>proof by induction</td><td>recursion</td></tr>
<tr class="hl"><td><b>removing a lemma</b></td><td><b>running the program</b></td></tr>
</table>

---
layout: center
---

# Why that one idea matters so much

<div class="lead centered">Because proof checking becomes <b>type checking</b>.</div>

<div class="grid2">
<div>
<div class="h3">Checking a type</div>
<ul>
<li>No search</li>
<li>No heuristics</li>
<li>Local, syntactic, decidable</li>
<li>Governed by a few inference rules</li>
</ul>
</div>
<div>
<div class="h3 accent">Therefore</div>
<ul>
<li>Tactics can be arbitrary programs — even buggy ones</li>
<li>They can be written by an AI</li>
<li>They can be tested, not trusted</li>
<li><b>Soundness never depends on them</b></li>
</ul>
</div>
</div>

<v-click>

<div class="callout">
The kernel is the only thing you must trust. In Lean that's a few thousand lines.
This is the <b>de Bruijn criterion</b>, and it's why an extensible proof assistant is still safe.
</div>

</v-click>

---
layout: center
---

<div class="idea-num">Idea 2</div>

# The specification gap

<div class="lead">A proof is a contract between your <b>model</b> and your <b>property</b>.</div>

<v-click>

<div class="punch">It tells you nothing about either.</div>

</v-click>

---
layout: center
---

# The bug is in the sentence, not the proof

```lean
-- A deliberately useless "sorting" function: throw the data away.
def badSort (_ : List Nat) : List Nat := []

-- The weak property: "the output is sorted".
theorem badSort_satisfies_weak_spec (xs : List Nat) : Sorted (badSort xs) := Sorted.nil
```

<v-click>

<div class="callout">
<b>The useless implementation passes.</b> The proof is one line.
The missing clause is <i>"the output is a permutation of the input"</i> — and the missing clause is
where the bugs live.
</div>

</v-click>

<div class="muted small centered">
Write two clauses: what must be <b>true</b> of the result, and what must be <b>preserved</b>.
</div>

---
layout: center
---

# I made this mistake four times writing the wiki

<table class="clean small">
<thead><tr><th>Bug</th><th>Was the proof wrong?</th><th>Or the property?</th></tr></thead>
<tr><td>My first TLA+ retry spec had a disabled crash action</td><td class="no">no</td><td class="yes">model</td></tr>
<tr><td>My first DPLL encoding was unsatisfiable</td><td class="no">no</td><td class="yes">model</td></tr>
<tr><td>My first agent guardrail missed an unauthorized <code>erase</code></td><td class="no">no</td><td class="yes">property</td></tr>
<tr><td>My first table-row check had an escaping bug</td><td class="no">no</td><td class="yes">property</td></tr>
</table>

<v-click>

<div class="punch">
Four times the <b>sentence</b> was wrong. Zero times the <b>proof</b> was.
</div>

</v-click>

<div class="muted small centered">This is the most honest evidence I have for the whole talk, and I collected it by accident.</div>

<!--
Real, and the best slide in the deck because it's self-incriminating.
Keep the examples concrete — the erase/delete one lands best.
-->

---
layout: center
---

<div class="idea-num">Idea 3</div>

# Stuttering invariance

<div class="lead">The most under-taught idea in the field.<br>It's why refinement proofs exist at all.</div>

---
layout: center
---

# Your implementation has more steps than your spec

<div class="steps">
  <div class="step-row">
    <div class="rowlabel">abstract</div>
    <div class="tokens"><span class="st">A</span><span class="dash">──────</span><span class="st">B</span></div>
  </div>
  <div class="step-row">
    <div class="rowlabel">implementation</div>
    <div class="tokens"><span class="st">A</span><span class="dash">──</span><span class="st small">a₁</span><span class="dash">──</span><span class="st small">a₂</span><span class="dash">──</span><span class="st">B</span></div>
  </div>
</div>

<div class="lead centered">
Three steps implementing one abstract action must not be a refinement <i>violation</i>.
</div>

<v-click>

<div class="callout">
<b>The theorem (Peled–Wilke).</b> A temporal property is stuttering-invariant
<b>if and only if</b> you can write it without the <span class="mono">next</span> operator.
</div>

<div class="punch small">
So: <b>never write <span class="mono">X</span>.</b> And write <span class="mono">[Next]_vars</span>, not
<span class="mono">Next</span> — the bracket is the stuttering step.
</div>

</v-click>

---
layout: center
---

# Two rules, memorised

<div class="rules">
<div class="rule">
<div class="rule-n mono">X φ</div>
<div class="rule-v bad">almost always a bug</div>
<div class="rule-w">"φ in the very next state" is a claim about <b>step granularity</b>. Any implementation with a different granularity breaks it.</div>
</div>
<div class="rule">
<div class="rule-n mono">[Next]_v</div>
<div class="rule-v good">this is the one</div>
<div class="rule-w">"Next happens, <b>or nothing changes</b>." That second disjunct is the stuttering step, and it's what makes a spec refinable.</div>
</div>
</div>

<div class="muted small centered">
Cost of following this rule: zero. Cost of not following it: unprovable refinement, forever.
</div>

---
layout: center
---

<div class="idea-num">Idea 4</div>

# Safety and liveness are topologically different

<div class="lead">Put the Cantor topology on infinite traces.</div>

<v-click>

<div class="topo">
  <div class="topo-card">
    <div class="topo-h">safety</div>
    <div class="topo-sub">"nothing bad ever happens"</div>
    <div class="topo-math mono">= the closed sets</div>
    <div class="topo-body">A violation is witnessed by a <b>finite prefix</b>.</div>
    <div class="topo-cons">→ a model checker can find it. Fuzzers can hit it. You get a reproducible trace.</div>
  </div>
  <div class="topo-card">
    <div class="topo-h">liveness</div>
    <div class="topo-sub">"something good eventually happens"</div>
    <div class="topo-math mono">= the dense sets</div>
    <div class="topo-body">A violation requires an <b>infinite</b> trace.</div>
    <div class="topo-cons">→ you cannot exhibit "never happens" with a finite run. You need a proof, or fairness plus a rank.</div>
  </div>
</div>

</v-click>

<div class="callout">
Every property is a safety property ∩ a liveness property. That's a theorem — and it's why
"find a bug" and "prove it never happens" are different industries.
</div>

---
layout: center
---

# Liveness needs an assumption, not just a proof

<div class="lead">A liveness claim without its fairness assumption is not a claim about any real system.</div>

<div class="grid2">
<div>
<div class="h3 mono">weak fairness</div>
<div class="small">if <span class="mono">A</span> is <b>continuously</b> enabled, it eventually happens</div>
</div>
<div>
<div class="h3 mono">strong fairness</div>
<div class="small">if <span class="mono">A</span> is enabled <b>infinitely often</b>, it happens infinitely often</div>
</div>
</div>

<v-click>

<div class="callout">
The classic trap: a semaphore waiter's action is enabled <i>infinitely often</i> but never
<i>continuously</i>. Weak fairness gives you nothing. You need strong fairness — or you will prove
a theorem about a scheduler you don't have.
</div>

</v-click>

<div class="muted centered small">
First question to ask about any liveness claim: <b>under what fairness?</b>
</div>

---
layout: center
---

# Bonus idea: the frame rule

<div class="lead">Ordinary Hoare logic can't reason about pointers.<br>One connective fixes it.</div>

<div class="compare">
<div class="cmp-col">
<div class="cmp-h">ordinary conjunction</div>
<div class="cmp-code mono">x ↦ 1  ∧  x ↦ 1</div>
<div class="cmp-v good">true</div>
<div class="cmp-w">both facts describe the <b>same</b> cell. Redundant, but fine.</div>
</div>
<div class="cmp-col">
<div class="cmp-h">separating conjunction</div>
<div class="cmp-code mono">x ↦ 1  ∗  x ↦ 1</div>
<div class="cmp-v bad">false</div>
<div class="cmp-w">demands <b>two disjoint</b> cells at the same address. Unsatisfiable — by construction.</div>
</div>
</div>

<v-click>

<div class="punch">
Separation logic makes an aliasing claim <b>unstatable</b> rather than <b>dischargeable</b>.
</div>

<div class="muted centered">And <span class="mono">∗</span> is monoidal composition over a chosen resource algebra — which is why
Rust's borrow checker is a decidable fragment of it, and why Iris is a framework rather than a logic.</div>

</v-click>

---
layout: section
---

<div class="part">Part III</div>
# It already shipped
<div class="partsub">The part where you realise you've been depending on this for years</div>

---
layout: center
---

# Things that run because someone proved something

<div class="parade">
<div class="pcard"><div class="pn">8,700</div><div class="pl">lines of C in seL4</div><div class="pw">+ 200,000 lines of proof</div></div>
<div class="pcard"><div class="pn">0</div><div class="pl">wrong-code bugs in CompCert</div><div class="pw">GCC and LLVM: hundreds</div></div>
<div class="pcard"><div class="pn">1B+</div><div class="pl">Cedar checks per day</div><div class="pw">Dafny model + differential testing</div></div>
<div class="pcard"><div class="pn">3</div><div class="pl">microkernels in your devices</div><div class="pw">seL4, verified end to end</div></div>
</div>

<div class="muted small centered">Plus the TLS in your browser (HACL*/EverCrypt), the silicon in your laptop, and the
authorization decisions behind your cloud account.</div>

---
layout: center
---

# CompCert: the number that should bother you

<div class="lead centered">Csmith (PLDI 2011) generated random C programs and compiled them with every major compiler.</div>

<div class="bignum-row">
<div class="bignum bad">
  <div class="bn">hundreds</div>
  <div class="bl">wrong-code bugs<br><span class="mono">GCC · LLVM</span></div>
</div>
<div class="bignum good">
  <div class="bn">zero</div>
  <div class="bl">wrong-code bugs<br><span class="mono">CompCert</span></div>
</div>
</div>

<div class="callout">
Compiler bugs are <b>invisible</b>: correct source silently becomes incorrect binaries,
and every test you run tests the binary — so a miscompile can make your tests pass <i>because</i>
it's broken.
</div>

<div class="muted small centered">The generalisable lesson: <b>verify the tool, not just the artifact.</b> Verify a compiler once and
every program you ever compile inherits the guarantee.</div>

---
layout: center
---

# The AWS reframing that gets budgets approved

<div class="quote-block">
> In several cases we have prevented subtle, serious bugs from reaching production. In other cases we
> have been able to make innovative performance optimizations — e.g. removing or narrowing locks, or
> weakening constraints on message ordering — <b>which we would not have dared to do without having
> model checked those changes.</b>
<div class="attrib">Use of Formal Methods at Amazon Web Services</div>
</div>

<v-click>

<div class="grid2">
<div>
<div class="h3 dim">Insurance</div>
<div class="small dim">protects against a loss that never appears on a dashboard.<br><b>Gets cut.</b></div>
</div>
<div>
<div class="h3 accent">Enabler</div>
<div class="small">lets you ship a faster design you couldn't otherwise justify.<br><b>Gets funded.</b></div>
</div>
</div>

</v-click>

<div class="muted small centered">
They called the internal talk <b>"Debugging Designs"</b> and described the tool as
<b>"exhaustively testable pseudo-code"</b>. Steal that framing. It isn't a euphemism — it's the
difference between adoption and abandonment.
</div>

---
layout: center
---

# And yet it mostly didn't reach you

<div class="lead centered">That's the honest part, and it has reasons.</div>

<table class="clean small">
<tr><td>The specification gap</td><td class="dim">never closes; product requirements churn weekly</td></tr>
<tr><td>Cost is upfront and lumpy</td><td class="dim">the benefit is a bug that didn't happen</td></tr>
<tr><td>Expertise tax</td><td class="dim">weeks of ramp-up, concentrated in a small community</td></tr>
<tr><td>Tools that aren't in CI</td><td class="dim">are not adopted, regardless of quality</td></tr>
<tr class="hl"><td><b>Selection effects</b></td><td class="dim"><b>we publish successes, never abandoned verification projects</b></td></tr>
</table>

<v-click>

<div class="punch">
It delivered where failure was catastrophic and the artifact was small —<br>
and <span class="accent">nowhere else</span>.
</div>

</v-click>

---
layout: section
---

<div class="part">Part IV</div>
# The AI era
<div class="partsub">Generation got cheap. Verification didn't.</div>

---
layout: center
---

# Amdahl's law, applied to software

<div class="bars">
  <div class="bar-row">
    <div class="bar-label">generating code</div>
    <div class="bar-track"><div class="bar shrink">then: $$$$</div></div>
    <div class="bar-track"><div class="bar tiny">now: ¢</div></div>
  </div>
  <div class="bar-row">
    <div class="bar-label">establishing trust</div>
    <div class="bar-track"><div class="bar flat">then: $$</div></div>
    <div class="bar-track"><div class="bar flat">now: $$ — unchanged</div></div>
  </div>
</div>

<v-click>

<div class="lead centered">
You sped up one stage by 10× and left the next one alone. <b>The next one now sets your throughput ceiling.</b>
</div>

<div class="quote-block">
> (Developers) report being able to <b>"fully delegate" only 0–20% of tasks</b>, while using AI in
> roughly 60% of their work.
<div class="attrib">Anthropic, 2026 agentic coding report ⚠️ vendor-published</div>
</div>

</v-click>

<div class="muted small centered">That gap between <i>assisted</i> and <i>trusted</i> <b>is</b> the verification bottleneck.</div>

---
layout: center
class: text-center
---

# 2024: the year it stopped being hypothetical

<div class="huge">28 <span class="slash">/</span> 42</div>

<div class="lead">
<b>AlphaProof</b> + AlphaGeometry 2 solved 4 of 6 IMO problems — silver-medal range,
one point below gold.
</div>

<div class="muted">
Trained by reinforcement learning with <b>Lean as the environment and the reward</b>.
</div>

<div class="attrib">Published in <i>Nature</i>, November 2025</div>

---
layout: center
---

# What that actually required

<div class="grid3">
<div class="stat"><div class="sn">3B</div><div class="sl">parameter proof network</div></div>
<div class="stat"><div class="sn">~300k</div><div class="sl">human state–tactic pairs</div></div>
<div class="stat"><div class="sn">~80M</div><div class="sl">formal problems, auto-generated</div></div>
</div>

<div class="callout">
<b>The data engine was autoformalization.</b> ~1 million informal problems were translated into
~80 million formal Lean problems. The insight that unlocked it:
<i>even a mis-formalized statement is still a valid formal problem to prove or disprove</i> —
so fidelity isn't required for training data.
</div>

<div class="muted small centered">And the honest part, which is why the rest is credible: <b>"the two combinatorics problems remained unsolved"</b>, and it took days where humans took hours.</div>

---
layout: center
class: text-center
---

# 2026: generic models write Lean now

<div class="lead">This is the thing most formal-methods material hasn't caught up with.</div>

<div class="grid3">
<div class="stat"><div class="sn big">92%</div><div class="sl">Gemini 3.1 Pro<br><span class="mono small">miniF2F, refine@32</span></div></div>
<div class="stat"><div class="sn big">86%</div><div class="sl">Claude Opus 4.7<br><span class="mono small">miniCTX, refine@32</span></div></div>
<div class="stat"><div class="sn big">&lt;$0.01</div><div class="sl">per correct proof<br><span class="mono small">open models</span></div></div>
</div>

<v-click>

<div class="punch">
The winners are <b>general-purpose</b> models — not Lean-specialised provers.
</div>

<div class="muted small">arXiv:2606.05632, June 2026. Note the metric: <span class="mono">refine@k</span> = "given the
compiler's error, fix your attempt" — the actual interactive loop.</div>

</v-click>

---
layout: center
---

# Ten new theorems, with machine-checked certificates

<div class="lead centered">August 2026. Each problem open for at least a decade.</div>

<div class="grid2 small">
<div>
<ul>
<li>First explicit construction of a <b>non-sofic group</b></li>
<li>Counterexample to <b>Connes's rigidity conjecture</b></li>
<li><b>Ehrhart's volume conjecture</b> proved</li>
<li>Improved bounds on <b>high-dimensional sphere packing</b></li>
</ul>
</div>
<div>
<ul>
<li>Three problems from <b>Erdős's catalogue</b></li>
<li>Parallel repetition for <b>quantum games</b></li>
<li>New <b>arithmetic circuit lower bounds</b></li>
<li>Hardness of approximation for <b>Closest Vector</b></li>
</ul>
</div>
</div>

<div class="callout">
Every argument shipped with a <b>Lean 4 certificate</b> in a public repository — and the model was
<i>general-purpose</i>, not a maths system.
</div>

<div class="muted small centered">
Compute cost reported around <b>~$2,000</b> for all ten ⚠️ <i>secondary source — verify before quoting.</i>
</div>

---
layout: center
---

# The pattern that changes how you build software

<div class="lead centered">powdr's zkVM constraint-system optimiser, formally verified in Lean.</div>

<div class="powdr">
<div class="pcol human">
  <div class="pc-h">Human</div>
  <div class="pc-n">~500</div>
  <div class="pc-u">lines of spec</div>
  <div class="pc-w">written, reviewed, <b>frozen</b>. Agents are told not to touch it.</div>
</div>
<div class="pcol ai">
  <div class="pc-h">AI</div>
  <div class="pc-n">10,000</div>
  <div class="pc-u">lines of Lean</div>
  <div class="pc-w">implementation and proofs. <b>No human ever read it.</b></div>
</div>
<div class="pcol ci">
  <div class="pc-h">CI</div>
  <div class="pc-n">2</div>
  <div class="pc-u">things rejected</div>
  <div class="pc-w"><span class="mono">sorry</span> and new <span class="mono">axiom</span> declarations.</div>
</div>
</div>

<v-click>

<div class="punch">
One week. One engineer. Matched the hand-written Rust optimiser.
</div>

</v-click>

---
layout: center
class: text-center
---

<div class="quote-block">
> The mechanism is simple: <b>the proof is the review.</b> Nobody has to sit down and audit every
> aggressive rewrite, so you can point an AI at the code, let it optimize relentlessly, and only
> require that the proof still goes through.
<div class="attrib">Leonardo Alt, <i>Performant Verified Software</i>, Sept 2026</div>
</div>

<v-click>

<div class="lead centered">
You review <b>500 lines of specification</b> instead of <b>10,000 lines of implementation</b>.
</div>

<div class="muted">
That is not less rigour. It's a better use of the only scarce resource you have: human expertise.
</div>

</v-click>

---
layout: center
---

# Blockchain: where this is furthest along

<div class="lead">Money, immutability, and an adversary who reads your code.</div>

<table class="clean small">
<tr><td class="mono">EVMYulLean</td><td>The EVM and Yul semantics in Lean — passes <b>99.99%</b> (22,330/22,332) of the official Cancun tests</td></tr>
<tr><td class="mono">yul-compiler</td><td>A verified Yul→EVM compiler that produces code with <b>better gas performance than <code>solc</code></b></td></tr>
<tr><td class="mono">SP1 Hypercube</td><td>The <b>entire RISC-V zkVM core</b> verified in Lean against the official Sail specification</td></tr>
<tr><td class="mono">zk.golf</td><td>A competition to build the cheapest ZK circuits, <b>proven correct in Lean 4</b></td></tr>
</table>

<v-click>

<div class="callout">
Why is verified code <i>faster</i>? Because the proof is the review.
An unverified optimiser has to be conservative enough for a human to trust it.
A verified one can <b>send it</b> — the kernel will catch anything unsound.
</div>

</v-click>

---
layout: section
---

<div class="part">Part V</div>
# The honest part
<div class="partsub">What this does not do — say it before someone else does</div>

---
layout: center
---

# What formal methods cannot do

<div class="grid2">
<div>
<div class="h3">Outside the model</div>
<ul class="small">
<li>Performance and emergent behaviour — feedback loops, queueing collapse, cascading retries</li>
<li>Configuration and deployment</li>
<li>Human operators and runbooks</li>
<li>Third-party dependencies</li>
<li>Requirements correctness</li>
</ul>
</div>
<div>
<div class="h3">And the big one</div>
<div class="callout small">
A proof is <span class="mono">model ⊢ property</span>.<br><br>
It cannot tell you that <span class="mono">property</span> is what anyone wanted,
or that <span class="mono">model</span> is reality.
</div>
</div>
</div>

<div class="quote-block small">
> We care about 1) bugs and operator errors that cause a departure from the logical intent of the
> system, and 2) surprising 'sustained emergent performance degradation' of complex systems.
<div class="attrib">AWS, being unusually clear about scope. They address (1). Not (2).</div>
</div>

---
layout: center
---

# Verified systems have failed. Here's why.

<table class="clean small">
<thead><tr><th>Incident</th><th>Year</th><th>The lesson</th></tr></thead>
<tr><td>Pentium FDIV</td><td>1994</td><td>A lookup-table bug. Made formal verification standard in silicon — <i>after</i> the public failure.</td></tr>
<tr><td>Ariane 5</td><td>1996</td><td>Reused Ariane 4 software, unhandled overflow on a different input range. <b>An assumption-reuse failure, not a coding bug.</b></td></tr>
<tr><td>Knight Capital</td><td>2012</td><td>Deployed to the wrong servers. Logic was fine; <b>deployment</b> was the model gap.</td></tr>
</table>

<v-click>

<div class="punch">
The bug is almost never in the proof.<br>
<span class="accent">It's in an assumption nobody wrote down.</span>
</div>

</v-click>

<div class="muted small centered">
Hence the highest-value habit you can steal from this field: <b>document your assumptions explicitly</b>.
Every serious verification project has an assumptions section. Ordinary teams almost never write one down.
</div>

---
layout: section
---

<div class="part">Part VI</div>
# What to actually do
<div class="partsub">One property. One function. One day.</div>

---
layout: center
---

# The ladder

<div class="ladder">
  <div class="rung">
    <div class="rnum">0</div><div class="rtitle">Types & memory safety</div>
    <div class="rcost">already paying it</div><div class="rgain">no UB, no data races</div>
  </div>
  <div class="rung">
    <div class="rnum">1</div><div class="rtitle"><b>Assertions & contracts</b></div>
    <div class="rcost">minutes</div><div class="rgain">local invariants hold</div>
  </div>
  <div class="rung hl">
    <div class="rnum">2</div><div class="rtitle"><b>Property-based tests</b></div>
    <div class="rcost">hours</div><div class="rgain">holds for thousands of generated inputs</div>
  </div>
  <div class="rung">
    <div class="rnum">3</div><div class="rtitle">Differential / model-based testing</div>
    <div class="rcost">days</div><div class="rgain">two implementations agree</div>
  </div>
  <div class="rung hl">
    <div class="rnum">4</div><div class="rtitle"><b>SMT-in-CI on one function</b></div>
    <div class="rcost">days</div><div class="rgain">holds for <b>all</b> inputs of that function</div>
  </div>
  <div class="rung">
    <div class="rnum">5</div><div class="rtitle">Model-check a protocol design</div>
    <div class="rcost">weeks</div><div class="rgain">no violation in any interleaving</div>
  </div>
  <div class="rung">
    <div class="rnum">6</div><div class="rtitle">Full functional-correctness proof</div>
    <div class="rcost">person-years</div><div class="rgain">refinement, for all executions</div>
  </div>
</div>

<div class="muted small centered">
<b>My ask: get to rung 2, and try rung 4 on exactly one function.</b> That's it.
</div>

---
layout: center
---

# The 5 things to do in your first week

<div class="numbered">
<div class="num-item"><b>1. Pick the function that broke production last quarter.</b> Not a greenfield module — the one that already hurt. This is exactly how AWS started.</div>
<div class="num-item"><b>2. Write the property in two clauses</b> — one for the happy result, one for what must be <i>preserved</i> (permutation, ordering, idempotency, no leak). Missing the second clause is the most common bug.</div>
<div class="num-item"><b>3. Find a generator, not a test case.</b> <span class="mono">hypothesis</span>, <span class="mono">proptest</span>, <span class="mono">fast-check</span>. Let the machine pick inputs.</div>
<div class="num-item"><b>4. Take one pure function to rung 4.</b> <span class="mono">cargo kani</span>, or Dafny. Feel the difference between "1000 inputs passed" and "proved for all inputs".</div>
<div class="num-item"><b>5. Write one TLA+ spec of a design you're arguing about in review comments.</b> Two hours. Bring the counterexample trace to the design meeting.</div>
</div>

<div class="callout small">
<b>The highest-leverage prompt in this entire talk</b> is not "prove this". It is:
<i>"Here is the bug we shipped. Write the property that would have caught it."</i>
</div>

---
layout: center
class: text-center
---

# The three sentences

<div class="three">
<div class="three-item"><span class="tn">1</span> AI made code cheap and trust expensive.</div>
<div class="three-item"><span class="tn">2</span> Checking is cheap; searching is hard — so AI proposes and kernels dispose.</div>
<div class="three-item"><span class="tn">3</span> The engineer's new core skill is stating precisely what must be true — and picking the cheapest sound check for it.</div>
</div>

<v-click>

<div class="quote-block big">
> Formal methods cannot tell you what to want.<br>
> They can tell you, with certainty, whether what you asked for is what you'll get —<br>
> and show you the exact input where it isn't.
</div>

</v-click>

---
layout: center
class: text-center
---

<div class="huge accent">The first AI program was a theorem prover.</div>

<div class="lead">
The most valuable AI systems of the next decade may well be the ones that <b>verify</b>.
</div>

<div class="footer-note">
Thank you.<br>
<span class="mono">yihuang.github.io/awesome-formal-methods</span>
</div>

---
layout: center
---

# Where to go next

<div class="lead centered">Everything in this talk is one link deep.</div>

<div class="grid2 small">
<div>
<div class="h3">The ideas</div>
<ul>
<li><span class="mono">/01-fundamentals/type-theory</span> — dependent types, universes</li>
<li><span class="mono">/01-fundamentals/curry-howard</span> — why proofs are programs</li>
<li><span class="mono">/01-fundamentals/temporal-logic</span> — safety, liveness, stuttering</li>
<li><span class="mono">/01-fundamentals/separation-logic</span> — the frame rule</li>
<li><span class="mono">/01-fundamentals/limits</span> — Gödel, Rice, the trusted base</li>
</ul>
</div>
<div>
<div class="h3">The practice</div>
<ul>
<li><span class="mono">/03-applications/lightweight-fm</span> — the on-ramp, with code</li>
<li><span class="mono">/03-applications/blockchain</span> — EVM, zk, verified compilers</li>
<li><span class="mono">/reviews/…</span> → <span class="mono">/04-ai-era/llm-proof-engineering</span> — AI writing Lean</li>
<li><span class="mono">/05-tools/choosing</span> — which tool, for which problem</li>
<li><span class="mono">/06-practice/adoption-playbook</span> — the 0→3 rollout</li>
</ul>
</div>
</div>

<div class="callout">
The wiki flags every unverified number with <span class="mono">⚠️</span> and keeps a
<a href="https://yihuang.github.io/awesome-formal-methods/research-notes.html">confidence ledger</a>.
If you catch a wrong claim, that's the most valuable contribution you can make.
</div>

---
layout: center
class: text-center
---

# Backup slides

<div class="muted">The five families · the tool map · the objection answers · the full ladder</div>

---
layout: center
---

# The five families of verification

<div class="grid2 small">
<div>
<div class="h3">Who supplies the ingenuity?</div>
<table class="clean small">
<tr><td>The human</td><td>theorem proving — Lean, Rocq, Isabelle</td></tr>
<tr><td>The machine</td><td>model checking — TLA+, SPIN, Alloy</td></tr>
<tr><td>Both, split</td><td>deductive verification — Dafny, Kani, Verus</td></tr>
<tr><td>Over-approximate</td><td>abstract interpretation — Astrée, Infer</td></tr>
<tr><td>Decidable fragment</td><td>types — Rust, TypeScript, refinement types</td></tr>
</table>
</div>
<div>
<div class="h3">Pick by what you're reasoning about</div>
<table class="clean small">
<tr><td>a protocol design</td><td class="mono">TLA+</td></tr>
<tr><td>one critical function</td><td class="mono">Kani · Dafny</td></tr>
<tr><td>a whole codebase's UB</td><td class="mono">Astrée · Infer</td></tr>
<tr><td>a compiler or kernel</td><td class="mono">Lean · Isabelle</td></tr>
<tr><td>a policy engine</td><td class="mono">Cedar + SMT</td></tr>
<tr><td>an agent's actions</td><td class="mono">runtime monitors</td></tr>
</table>
</div>
</div>

<div class="muted small centered">Full catalog and decision tree: <span class="mono">/05-tools/choosing</span></div>

---
layout: center
---

# The objections, answered briefly

<table class="clean small">
<tr><td>"10 years away for 50 years"</td><td>Ask what <i>did</i> happen: silicon, avionics, crypto, cloud control planes.</td></tr>
<tr><td>"You can't verify the spec"</td><td>Correct, and it's permanent. That's why we say <b>precision, not omniscience</b>.</td></tr>
<tr><td>"AI can just verify things"</td><td>AI <i>proposes</i>; a kernel <i>disposes</i>. And RL needs the verifier.</td></tr>
<tr><td>"Too expensive"</td><td>Rung 1 is one day. Use HACL*, don't write your own crypto.</td></tr>
<tr><td>"Gödel makes it futile"</td><td>Gödel and Rice are <b>why the tools look like this</b>, not why they fail.</td></tr>
<tr><td>"Who maintains the proofs?"</td><td>Real risk. Keep the verified core small, frozen, owned, and in CI.</td></tr>
</table>

<div class="muted small centered">
Longer versions, with sources: <span class="mono">/06-practice/objections</span>
</div>
