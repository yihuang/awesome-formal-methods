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
# No `fonts:` webfonts on purpose — Slidev's CLI injects a Google Fonts <link>
# whenever `webfonts` is non-empty, and `fonts: false` does NOT suppress it.
# style.css declares font stacks with system fallbacks instead, so the deck
# renders identically offline and makes no font CDN request. Don't undo this.
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
layout: section
---

<div class="part">Part I</div>
# Motivation
<div class="partsub">Why this is your problem now — before we go anywhere near mathematics</div>

---
layout: center
---

# Why this is your problem

<div class="lead">Three things changed. None of them are about mathematics.</div>

<div class="grid2">
<div>
<div class="h3">You review more code than you can read</div>
<div class="small">Not because you got slower — because generation outran review capacity.
<b>The bottleneck moved, and it moved onto you.</b></div>
</div>
<div>
<div class="h3 accent">Your tests share your blind spots</div>
<div class="small">They were written by the same model, from the same assumptions, against the same
imagined inputs. Correlated errors don't cancel. <b>They compound.</b></div>
</div>
</div>

<div class="callout">
And the failure surfaces in the one place you can't afford it: <b>production</b>. Testing samples. It
cannot tell you about the input you didn't imagine — and that input is exactly what an adversary, an
unusual customer, or next quarter's data will find.
</div>

<div class="muted small centered">
So the question this talk is about is not "should I learn Lean". It is:<br>
<b>what do you do when you can no longer personally vouch for the code you ship?</b>
</div>

<!--
The slide that answers "what has this got to do with me". Do not skip or rush it — it is the reason
the history section that follows is allowed to exist.
-->

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
---

# What this talk is

<div class="lead">Five parts, in this order — the first one is why you're here.</div>

<table class="clean small">
<tr><td class="mono">I&nbsp;&nbsp;&nbsp;&nbsp;Motivation</td><td>why trusting code is now the bottleneck, and why that lands on you</td></tr>
<tr><td class="mono">II&nbsp;&nbsp;&nbsp;History</td><td>where formalism came from, and the three theorems that cap it forever</td></tr>
<tr><td class="mono">III&nbsp;&nbsp;Methodology</td><td>the five ideas that make verification possible anyway</td></tr>
<tr><td class="mono">IV&nbsp;&nbsp;The AI era</td><td>what actually changed in 2024–2026, with numbers</td></tr>
<tr><td class="mono">V&nbsp;&nbsp;&nbsp;Practice</td><td>the honest limits, and one thing to do on Monday</td></tr>
</table>

<div class="grid2">
<div>
<div class="h3">Not</div>
<ul class="dim small">
<li>A tour of 40 tools</li>
<li>"Everyone should learn Lean"</li>
</ul>
</div>
<div>
<div class="h3 accent">But</div>
<ul class="small">
<li><b>Why anyone invented this at all</b> — a 2,300-year-old answer</li>
<li>Why it can never be complete, and why that's survivable</li>
<li>What AI changed — and what it didn't</li>
</ul>
</div>
</div>

<!--
Set expectations honestly, including that history gets real time. Engineers sit through a section they
know is coming; they check out of one that surprises them with Aristotle.
-->

---
layout: section
---

<div class="part">Part II</div>
# History: the origin of formalism
<div class="partsub">Why anyone would want symbols to be more trustworthy than judgement</div>

---
layout: center
---

# Why would anyone want this?

<div class="lead centered">Not "how do I verify code". The prior question:</div>

<v-click>

<div class="punch big">
Why would <em>symbols on paper</em> ever be more trustworthy<br>than a competent person's judgement?
</div>

</v-click>

<v-click>

<div class="muted centered small">
This is a 2,300-year-old question. The answer is not obvious, and engineers reinvent it badly every
time they write "the tests pass, ship it".
</div>

</v-click>

<!--
Open with the actual question. Don't answer it yet — the next six slides are the answer, and they're
also the origin story of the discipline the audience is about to be sold on.
-->

---
layout: center
---

<div class="era">~350 BCE</div>

# Separating form from content

<div class="lead">
Aristotle's <i>Prior Analytics</i> contains the first formal system in history:
the <b>syllogism</b>.
</div>

<div class="syllogism">
<div class="syl">
<div class="syl-line mono">All A are B.</div>
<div class="syl-line mono">All B are C.</div>
<div class="syl-rule"></div>
<div class="syl-line mono accent">Therefore all A are C.</div>
</div>
</div>

<v-click>

<div class="callout">
<b>The discovery is not the argument. It's that the argument is valid no matter what A, B and C
are.</b> You can check it without knowing anything about the subject matter.
</div>

<div class="lead centered">
Validity became a property of the <b>shape</b>, not of the content.
</div>

</v-click>

<!--
This is the birth of everything. Formality = you can evaluate an argument without understanding it.
Pause on "no matter what A, B and C are" — that's the whole idea, and it's what a type checker does
to a proof 2,300 years later.
-->

---
layout: center
---

<div class="era">~300 BCE</div>

# The first specification

<div class="lead">
Euclid's <i>Elements</i> does something Aristotle didn't: it starts from
<b>five postulates</b> and derives <b>465 propositions</b> from them, and from nothing else.
</div>

<div class="grid2">
<div>
<div class="h3">What it established</div>
<ul class="small">
<li>A small set of assumptions is stated <b>up front</b></li>
<li>Every claim traces back to them</li>
<li>A claim is accepted because of its <b>derivation</b>, not its author</li>
<li>Anyone can check it independently</li>
</ul>
</div>
<div>
<div class="h3 accent">Why it lasted 2,000 years</div>
<div class="small">
It was the paradigm of <b>certain knowledge</b> — the model for how you would prove anything at all.
Descartes, Spinoza, Newton all wrote in Euclid's format.
</div>
</div>
</div>

<div class="callout">
That second bullet is the thing to notice. <b>A claim is accepted because of its derivation, not its
author.</b> Everything in this talk is a mechanisation of that one sentence.
</div>

<!--
Euclid is the origin of "spec is the source of truth", and of the idea that authority is replaceable
by checkability. Both are still the pitch.
-->

---
layout: center
---

<div class="era">1733 → 1832</div>

# Then intuition broke

<div class="lead">
For two millennia, mathematicians tried to <b>prove</b> Euclid's fifth postulate (the parallel
postulate) from the other four. Everyone failed. In 1733, Saccheri tried a reductio — assume it's
false, derive a contradiction.
</div>

<v-click>

<div class="punch">
He derived no contradiction.<br>
<span class="accent">He derived a coherent geometry — and rejected it as "repugnant to the nature of a
straight line".</span>
</div>

</v-click>

<v-click>

<div class="lead">
A century later Lobachevsky, Bolyai and Gauss accepted the result instead of rejecting it. Riemann
generalised it. Beltrami, Klein and Poincaré built <b>models</b> — showing that non-Euclidean
geometry is exactly as consistent as Euclidean.
</div>

</v-click>

<div class="attrib">Saccheri, <i>Euclid Freed of Every Flaw</i>, 1733</div>

<!--
THE philosophical pivot of the whole talk, and it's a great story — Saccheri got the right answer and
threw it away because it was aesthetically unacceptable.

The payoff on the next beat: if two incompatible geometries are both consistent, then geometry does
not describe the world. It describes what FOLLOWS from assumptions.
-->

---
layout: center
---

# The most important philosophical shock for engineers

<div class="grid2">
<div>
<div class="h3 dim">What everyone believed</div>
<div class="small dim">
Axioms are <b>self-evident truths</b> about reality. Geometry describes the world.
Deriving from axioms therefore gives you <b>true</b> statements.
</div>
</div>
<div>
<div class="h3 accent">What turned out to be true</div>
<div class="small">
Axioms are <b>choices</b>. Different consistent systems exist. A derivation proves only:
<i>if you accept these, you must accept that.</i>
</div>
</div>
</div>

<v-click>

<div class="callout">
<b>Mathematics stopped being about truth and became about consequence.</b> Two incompatible geometries
are both fine; you pick one and go <i>test</i> which fits the world.
</div>

</v-click>

<v-click>

<div class="punch">
Your specification is a <b>choice</b>, not a fact.<br>
The proof is only ever <span class="accent">relative to what you chose</span>.
</div>

</v-click>

<!--
This is the deepest slide in the deck, and it is where the spec gap comes from — two centuries early.
Engineers find "the spec is a choice, the proof is relative" unsettling. Mathematicians had to absorb
exactly this, and it was harder for them.

Call back to this slide at the spec-gap slide in Part II. It's the same point, made twice, once as
history and once as an engineering bug I actually shipped.
-->

---
layout: center
---

<div class="era">1854 → 1901</div>

# Logic becomes a language

<div class="grid3">
<div class="stat">
<div class="sn">1854</div>
<div class="sl"><b>Boole</b><br><i>Laws of Thought</i><br><span class="dim">reasoning becomes algebra</span></div>
</div>
<div class="stat">
<div class="sn">1879</div>
<div class="sl"><b>Frege</b><br><i>Begriffsschrift</i><br><span class="dim">quantifiers, scope, binding</span></div>
</div>
<div class="stat">
<div class="sn red">1901</div>
<div class="sl"><b>Russell</b><br><span class="dim">writes to Frege. The system is inconsistent.</span></div>
</div>
</div>

<v-click>

<div class="callout">
Frege's <i>Grundgesetze</i> volume 2 was <b>already at the printer</b> when the letter arrived. His reply
is one of the most honest passages in the history of ideas: <i>"Hardly anything more unfortunate can
befall a scientific writer than to have one of the foundations of his edifice shaken after the work is
finished."</i>
</div>

</v-click>

<div class="muted small centered">
Boole made reasoning <b>calculable</b>. Frege made it a <b>precise language</b> — the first one with
quantifiers. And within twenty years, the most precise language anyone had ever built
<b>proved a contradiction</b>. That is the crisis formalism was invented to answer.
</div>

<!--
Boole → Frege → Russell is the arc from "logic is algebra" to "logic is a language" to "our best
language is broken".

Russell's paradox is one line: the set of all sets that do not contain themselves. Frege's honesty is
worth reading aloud if you have the room.
-->

---
layout: center
---

<div class="era">1910 → 1930</div>

# The answer: make it a game with rules

<div class="lead">
Russell and Whitehead spent a decade writing <i>Principia Mathematica</i> to repair Frege's
foundations: 3 volumes, ~2,000 pages — and <span class="mono">1 + 1 = 2</span> finally appears at
proposition <span class="mono">*54.43</span>.
</div>

<v-click>

<div class="lead">
Hilbert proposed something bolder. Stop arguing about what mathematics <em>means</em>. Treat it as
<b>symbols and rules</b> — then the question "is mathematics consistent?" becomes an ordinary
mathematical question you can <em>answer</em>.
</div>

</v-click>

<v-click>

<div class="quote-block">
> <span class="drop">W</span>ir müssen wissen. Wir werden wissen.
<div class="attrib">Hilbert, Königsberg, 1930 — "We must know. We will know."</div>
</div>

</v-click>

<div class="muted small centered">
His programme: formalise all of mathematics, then prove it consistent using only <b>finitary</b>
methods — reasoning so concrete that even an intuitionist would accept it. And in 1928, Hilbert and
Ackermann asked whether there is a procedure to decide <em>any</em> statement. They called it the
<span class="mono">Entscheidungsproblem</span>.
</div>

<!--
Hilbert is the optimist, and his programme is the direct ancestor of formal verification: take the
spec (axioms), take the derivation (proof), and check it mechanically. THAT is why this talk exists.

Also: Principia Mathematica is the book Logic Theorist attacked in 1956. The hook loops back here.
-->

---
layout: center
---

# Three schools — and what engineering inherited

<div class="schools">
<div class="school">
<div class="sch-name">Logicism</div>
<div class="sch-who mono">Frege · Russell · Whitehead</div>
<div class="sch-claim">Mathematics reduces to logic plus definitions.</div>
<div class="sch-inherit"><b>Inherited:</b> the ambition to write a precise language that can express
anything — and the habit of tracing every claim to stated foundations.</div>
</div>
<div class="school">
<div class="sch-name">Formalism</div>
<div class="sch-who mono">Hilbert</div>
<div class="sch-claim">Mathematics is symbol manipulation. Study the system, not the meaning.</div>
<div class="sch-inherit"><b>Inherited:</b> <b>everything</b>. Proof checking, kernels, type checking,
and the idea that a derivation is mechanical object you can audit.</div>
</div>
<div class="school">
<div class="sch-name">Intuitionism</div>
<div class="sch-who mono">Brouwer · Heyting · Kolmogorov</div>
<div class="sch-claim">Mathematics is construction. Truth = a construction you can carry out.
<b>Excluded middle is not valid</b> for infinite objects.</div>
<div class="sch-inherit"><b>Inherited:</b> constructive logic → the Curry–Howard correspondence →
<b>programs you can extract from proofs</b>.</div>
</div>
</div>

<v-click>

<div class="callout">
<b>This is not ancient history.</b> Brouwer rejected <span class="mono">p ∨ ¬p</span> in 1912. That is
why <span class="mono">Classical.em</span> is an <b>axiom</b> in Lean and Rocq, why
<span class="mono">#print axioms</span> on a constructive proof says "does not depend on any axioms",
and why a constructive proof can be <b>executed</b> while a classical one may not.
</div>

</v-click>

<!--
The payoff slide of the philosophical section: a 1912 argument about the philosophy of mathematics
determines what shows up in `#print axioms` today, and why constructive proofs compute.

If anyone thinks the philosophy is decoration, this slide is the rebuttal. Also a nice callback: the
`#print axioms` slide later in the deck.
-->

---
layout: center
---

# What formalism is actually *for*

<div class="quote-block">
> <span class="drop">C</span>alculemus. — let us calculate.
<div class="attrib">Leibniz's programme, 1666</div>
</div>

<div class="grid2">
<div>
<div class="h3 dim">The misunderstanding</div>
<div class="small dim">
That formal methods replace judgement with machinery. That they are for mathematicians who don't trust
each other, or for people who want to avoid thinking.
</div>
</div>
<div>
<div class="h3 accent">What it actually does</div>
<div class="small">
It makes <b>disagreement decidable</b>. Two parties who trust neither each other nor their tools can
still converge, because a derivation can be checked independently.
</div>
</div>
</div>

<v-click>

<div class="punch">
Formalism is a <b>social technology</b>.<br>
Its product is agreement without authority.
</div>

</v-click>

<v-click>

<div class="callout">
<b>And this is the honest cost.</b> Formalism does not remove judgement — it <b>relocates</b> it. It
moves the undecidable argument ("is this reasoning correct?") into a decidable one ("does this
derivation check?"), and leaves you holding the harder question: <b>is this specification what we
actually wanted?</b>
</div>

</v-click>

<!--
The thesis of the philosophical section. Formalism's product is agreement without authority — which is
exactly what a protocol between mutually distrusting parties needs, and exactly why blockchains care.

And the cost is the setup for the spec gap. Judgement isn't removed; it's relocated to the spec.
-->

---
layout: center
---

# Where the regress of trust stops

<div class="lead centered">Every proof needs a checker. The checker is software. The software runs on a chip…</div>

<svg viewBox="0 0 720 260" class="diagram regress">
  <defs>
    <marker id="arw2" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto">
      <path d="M0,0 L7,3 L0,6 z" fill="currentColor"/>
    </marker>
  </defs>
  <rect x="10"   y="10"  width="700" height="240" rx="12" class="box lop"/>
  <rect x="60"   y="42"  width="600" height="180" rx="10" class="box lop"/>
  <rect x="110"  y="74"  width="500" height="120" rx="9"  class="box lop"/>
  <rect x="160"  y="104" width="400" height="64"  rx="8"  class="box stop"/>

  <text x="30"  y="34"  class="ts left">physics</text>
  <text x="80"  y="66"  class="ts left">the CPU</text>
  <text x="130" y="98"  class="ts left">the compiler</text>
  <text x="180" y="128" class="ts left">the kernel</text>

  <text x="360" y="145" class="t stop-t">your proof</text>
  <path d="M200,178 L200,240" class="flow" marker-end="url(#arw2)"/>
  <text x="212" y="216" class="ts left">you must choose where to stop</text>
</svg>

<v-click>

<div class="punch">
You cannot verify the verifier. The regress is infinite, so <b>stopping is a choice</b> — and that
choice is philosophical, not mathematical.
</div>

</v-click>

<div class="muted small centered">
Lean's answer is the <b>de Bruijn criterion</b>: make the kernel small enough that a human can review it,
and accept everything below. Note that this is a claim about <i>engineering judgement</i>, dressed as a
mathematical one.
</div>

<!--
The philosophical core, and it is also the practical one: the trusted base is where you CHOOSE to stop
justifying. Every verification report should state it. Every engineer who says "just trust the
compiler" has made this choice without noticing.

This closes the philosophy section and hands off to Gödel: Hilbert wanted the regress to have an end
in finitary proof. Gödel showed it can't.
-->

---
layout: section
---

<div class="part">Part II · continued</div>
# And then the dream collapsed
<div class="partsub">Three theorems that closed Hilbert's programme — and defined our entire design space</div>

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
layout: section
---

<div class="part">Part III</div>
# Methodology &amp; techniques
<div class="partsub">How any of this is possible at all — five ideas, in order</div>

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
layout: center
---

<div class="idea-num">The oldest idea, still the useful one</div>

# Hoare logic: `{P} C {Q}`

<div class="lead">
"If <b>P</b> holds before <b>C</b> runs, and C terminates, then <b>Q</b> holds afterwards."
</div>

<table class="clean small">
<tr><td class="mono">P</td><td>the <b>precondition</b> — what you may assume. <span class="dim">(assumed, not proven)</span></td></tr>
<tr><td class="mono">C</td><td>the program</td></tr>
<tr><td class="mono">Q</td><td>the <b>postcondition</b> — what you must deliver. <span class="dim">(proven)</span></td></tr>
</table>

```text
{ x = 3 }      x := x + 1        { x = 4 }
{ n ≥ 0 }      factorial(n)      { result = n! }
```

<v-click>

<div class="callout">
<b>Two things that surprise everyone.</b><br>
<b>1.</b> The assignment axiom runs <b>backwards</b> — the precondition is the postcondition with the
assignment substituted in. Reasoning about imperative code is backward reasoning.<br>
<b>2.</b> The <code>while</code> rule needs an <b>invariant that you must supply</b>. There is no
algorithm for finding it. That's Rice's theorem, showing up in the most practical place possible.
</div>

</v-click>

<div class="muted small centered">
Hold that second point. <b>Everything in the AI-era section is about who supplies the invariant.</b>
</div>

<!--
This is the on-ramp for the audience: most engineers have seen {P}C{Q} in a course.
Set up the invariant as the bottleneck — it pays off twice later (AI proposing invariants,
and the spec gap).
-->

---
layout: center
---

<div class="idea-num">Idea 1 · why you can trust the tools</div>

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
The <b>kernel</b> is the only thing you must trust. In Lean that's a few thousand lines.
This is the <b>de Bruijn criterion</b>, and it's why an extensible proof assistant is still safe.
<span class="dim">Check it yourself: <code>#print axioms my_theorem</code>.</span>
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

<div class="idea-num">Idea 4 · the basics</div>

# How do you specify something that never finishes?

<div class="lead">
A server has no "final answer". It runs forever, next to an environment.
</div>

<div class="grid2">
<div>
<div class="h3">A program is</div>
<div class="small">an input → an output.<br>That's what <span class="mono">{P} C {Q}</span> describes.</div>
</div>
<div>
<div class="h3 accent">A reactive system is</div>
<div class="small">an infinite sequence of states:<br><span class="mono">σ = s₀ s₁ s₂ s₃ …</span></div>
</div>
</div>

<div class="callout">
<b>That is the whole conceptual shift.</b> A specification stops being about a result and becomes a
predicate on <b>infinite sequences</b>. Give up "output" and you get the ability to say things like
"every request is eventually answered" — which no input/output spec can express.
</div>

---
layout: center
---

# LTL in one slide

<div class="lead">Linear temporal logic: operators evaluated at a position in a trace.</div>

<table class="clean small">
<thead><tr><th>Operator</th><th>Reads</th><th>Meaning</th></tr></thead>
<tr><td class="mono">X φ</td><td>next</td><td>φ holds in the immediately following state <span class="dim">— we'll see why you never write this</span></td></tr>
<tr><td class="mono">G φ</td><td>always</td><td>φ holds in <b>all</b> future states</td></tr>
<tr><td class="mono">F φ</td><td>eventually</td><td>φ holds in <b>some</b> future state</td></tr>
<tr><td class="mono">φ U ψ</td><td>until</td><td>φ holds until ψ does — and ψ does happen</td></tr>
</table>

<div class="h3 accent" style="margin-top:1.1rem">The patterns you'll actually write</div>

<table class="clean small mono">
<tr><td>G ¬bad</td><td class="dim">nothing bad ever happens</td></tr>
<tr><td>F good</td><td class="dim">something good eventually happens</td></tr>
<tr><td>G (req → F ack)</td><td class="dim">every request is eventually answered</td></tr>
<tr><td>G F progress</td><td class="dim">progress keeps happening, forever</td></tr>
</table>

<div class="muted small centered">
<code>G</code> is <b>safety</b>-shaped. <code>F</code> is <b>liveness</b>-shaped. That distinction is the
next slide — and it determines which tool can help you.
</div>

<!--
The basics the audience needs before safety/liveness makes sense.
Land: traces are infinite, G and F are the two shapes, and everything else is built from them.
-->

---
layout: center
---

<div class="idea-num">Idea 4 · continued</div>

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

<div class="idea-num">Idea 5</div>

# The frame rule

<div class="lead">Ordinary Hoare logic can't reason about pointers — because of aliasing.<br>One connective fixes it.</div>

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
layout: center
---

# Where that gets you

<div class="lead centered">Back to the mechanism from Idea 1 — applied to a real artifact.</div>

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
Csmith (PLDI 2011) generated random C programs and compiled them with every major compiler.
CompCert — a C compiler whose <b>every optimisation is proved semantics-preserving</b> — had none.
</div>

<div class="muted small centered">
Compiler bugs are <b>invisible</b>: correct source silently becomes incorrect binaries, and every test
you run tests the binary — so a miscompile can make your tests pass <i>because</i> it's broken.<br>
<b>The lesson: verify the tool, not just the artifact.</b> Verify a compiler once and every program you
ever compile inherits the guarantee.
</div>

---
layout: section
---

<div class="part">Part IV</div>
# The AI era
<div class="partsub">Generation got cheap. Verification didn't.</div>

---
layout: center
---

# We already had this argument once — in 2014

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
Keep this framing — it is the same claim the AI era makes, ten years earlier and with humans doing the
proofs. <b>Verification is a speed enabler, not a brake.</b>
</div>

---
layout: center
class: text-center
---

# 2024 — the milestone

<div class="huge">28 <span class="slash">/</span> 42</div>

<div class="lead">
<b>AlphaProof</b> + AlphaGeometry 2 solved 4 of 6 IMO problems — silver-medal range.
</div>

<div class="muted">
Trained by reinforcement learning with <b>Lean as the environment and the reward</b>.
Published in <i>Nature</i>, 2025.
</div>

<v-click>

<div class="callout">
<b>This is a milestone, not the state of the art.</b> It took days per problem where humans took
hours, and <b>the two combinatorics problems remained unsolved</b>. What it proved was the
<i>architecture</i>: search proposes, a kernel disposes. Everything since has been about making that
architecture cheap and general.
</div>

</v-click>

<!--
Important framing. AlphaProof is where the field's own material tends to stop, and it's now two years
old. Use it as the proof of the architecture and move on quickly — the next two slides are the
actual state of the art.
-->

---
layout: center
---

# What AlphaProof actually required

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

<div class="muted small centered">Remember this trick. It is why the field stopped needing hand-formalised problems, and it generalises to
generating <i>specifications</i> from tickets, comments, and docs.</div>

---
layout: center
---

# 2025 — the specialists

<div class="lead centered">Leapfrogging the 2024 result, mostly with the same architecture.</div>

<table class="clean small">
<tr><td class="mono">Aristotle</td><td><b>gold-medal-equivalent</b> on the IMO 2025 problems, with Lean-verified proofs ⚠️ vendor claim</td></tr>
<tr><td class="mono">Goedel-Prover</td><td>open-weights SOTA for formal proof generation</td></tr>
<tr><td class="mono">DeepSeek-Prover-V2</td><td>open models close most of the gap</td></tr>
<tr><td class="mono">Kimina-Prover</td><td>Lean-based, open</td></tr>
</table>

<div class="callout">
<b>2025 was the year specialised provers stopped being a research curiosity and became a product
category</b> — and the year open weights made them reproducible.
</div>

<div class="muted small centered">
But note the shape of every one of these: <b>a model trained specifically for Lean</b>.
That's the part that stopped being true in 2026.
</div>

---
layout: center
class: text-center
---

# 2026 — the state of the art

<div class="lead">Generic models took over. This is the part most formal-methods material hasn't caught up with.</div>

<div class="grid3">
<div class="stat"><div class="sn big">92%</div><div class="sl">Gemini 3.1 Pro<br><span class="mono small">miniF2F, refine@32</span></div></div>
<div class="stat"><div class="sn big">86%</div><div class="sl">Claude Opus 4.7<br><span class="mono small">miniCTX, refine@32</span></div></div>
<div class="stat"><div class="sn big">&lt;$0.01</div><div class="sl">per correct proof<br><span class="mono small">open models</span></div></div>
</div>

<v-click>

<div class="punch">
The leaders are <b>general-purpose</b> models — not Lean-specialised provers.
</div>

<div class="muted small">
arXiv:2606.05632, June 2026. Note the metric: <span class="mono">refine@k</span> = "given the
compiler's error, fix your attempt" — the actual interactive loop, not a one-shot benchmark.<br>
And note the price: sub-cent proofs make search something you stop rationing.
</div>

</v-click>

---
layout: center
---

# 2026 — ten new theorems, machine-checked

<div class="lead centered">August 2026. Each problem open for at least a decade. Produced by a <b>general-purpose</b> model.</div>

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
Every argument shipped with a <b>Lean 4 certificate</b> in a public repository.
No Lean-specialised prover involved.
</div>

<div class="muted small centered">
Compute cost reported around <b>~$2,000</b> for all ten ⚠️ <i>secondary source — verify before quoting.</i><br>
<b>And the honest part:</b> machine-checked ≠ accepted. Mathematics is now arguing about attribution and
process, because the correctness argument is largely settled by the kernel.
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
# Under the hood
<div class="partsub">What these tools actually do when you press the button</div>

---
layout: center
---

# What the five families actually are

<div class="lead">Every verification tool is one of five things. This is the map.</div>

<table class="clean small">
<thead><tr><th>Family</th><th>Who supplies the ingenuity</th><th>It gives you</th><th>It fails by</th></tr></thead>
<tr><td><b>Theorem proving</b></td><td>the human (or the AI)</td><td>a proof, checked by a small kernel</td><td>effort — the proof-to-code ratio</td></tr>
<tr><td><b>Model checking</b></td><td>the machine</td><td>a counterexample trace</td><td>state explosion</td></tr>
<tr><td><b>Deductive verification</b></td><td>both, split</td><td>real code, verified against a spec</td><td><code>unknown</code>, annotations</td></tr>
<tr><td><b>Abstract interpretation</b></td><td>the machine</td><td>whole-codebase soundness</td><td>false alarms</td></tr>
<tr><td><b>Types</b></td><td>nobody — it's automatic</td><td>a decidable fragment, free</td><td>rejecting correct programs</td></tr>
</table>

<div class="grid2">
<div>
<div class="h3">Pick by the artifact</div>
<table class="clean small mono">
<tr><td>a protocol design</td><td>TLA+</td></tr>
<tr><td>one critical function</td><td>Kani · Dafny</td></tr>
<tr><td>a whole codebase's UB</td><td>Astrée · Infer</td></tr>
<tr><td>a kernel or compiler</td><td>Lean · Isabelle</td></tr>
</table>
</div>
<div>
<div class="h3 accent">And note the shape of the trade</div>
<div class="small">
Automation and expressiveness pull against each other, and <b>decidability is what you're spending</b>
to buy automation. Types are fully automatic because they say almost nothing. Theorem proving says
anything, and does nothing for you.
</div>
</div>
</div>

---
layout: center
---

# Why sampling cannot work — the arithmetic

<div class="lead">Not an opinion. A division.</div>

<div class="grid2">
<div>
<div class="h3">A single 64-bit input</div>
<div class="small">
The space is <span class="mono">2⁶⁴ ≈ 1.8 × 10¹⁹</span> inputs.
</div>
</div>
<div>
<div class="h3 accent">A very good fuzzer</div>
<div class="small">
<span class="mono">10⁶</span> executions per second, sustained.
</div>
</div>
</div>

<table class="clean small">
<tr><td>Executions in a <b>year</b></td><td class="mono">3.2 × 10¹³</td></tr>
<tr class="hl"><td><b>Fraction of the input space covered</b></td><td class="mono"><b>0.00017%</b></td></tr>
<tr><td>Years to exhaust it</td><td class="mono">584,000</td></tr>
<tr><td>…if you make the fuzzer <b>twice</b> as fast</td><td class="mono">292,000</td></tr>
<tr class="hl"><td><b>Add a second 64-bit argument</b></td><td class="mono"><b>10⁻²⁶</b></td></tr>
</table>

<div class="callout">
This is the argument for the whole field, and it does not depend on how good your tests are.
<b>Doubling your fuzzing throughput buys you a 2× improvement on a number with 19 digits.</b> The
exponent is the problem, and hardware does not touch exponents.
</div>

<div class="muted small centered">
And this is the <i>optimistic</i> case: it assumes bugs are spread uniformly across the input space.
They are not. They cluster in the corners nobody samples.
</div>

<!--
The single most persuasive quantitative slide in the deck. Everything else is philosophy; this is a
division. Pause on 0.00017%.
-->

---
layout: center
---

# How a SAT solver decides

<div class="lead">The engine under every SMT solver, verifier, and bounded model checker. Four clauses:</div>

<div class="grid2">
<div>
<div class="mono small">
C1: (x₁ ∨ x₂)<br>
C2: (¬x₁ ∨ x₃)<br>
C3: (¬x₃ ∨ ¬x₂)<br>
C4: (¬x₁ ∨ ¬x₃)
</div>
<div class="muted small" style="margin-top:1rem">
No unit clauses, so nothing is forced yet. There is exactly one satisfying assignment.
</div>
</div>
<div>
<div class="h3">The trace</div>
<div class="mono small trace">
<span class="tr-d">decide</span>     x₁ := true<br>
<span class="tr-p">propagate</span>  C2 → x₃ := true<br>
<span class="tr-p">propagate</span>  C4 → x₃ := false<br>
<span class="tr-c">CONFLICT</span>   on x₃<br>
<span class="tr-l">learn</span>      (¬x₁)<br>
<span class="tr-b">backjump</span>   x₁ := false<br>
<span class="tr-p">propagate</span>  C1 → x₂ := true<br>
<span class="tr-p">propagate</span>  C3 → x₃ := false<br>
<span class="tr-ok">SAT</span>        x₁=F, x₂=T, x₃=F
</div>
</div>
</div>

<v-click>

<div class="callout">
<b>The learning step is the whole idea.</b> The conflict depended only on the decision <span class="mono">x₁</span>,
so the solver writes down <span class="mono">(¬x₁)</span> permanently and <b>never tries that branch again</b>.
That is why modern solvers handle millions of clauses: they accumulate knowledge about their own
mistakes, and they only appear to be doing exhaustive search.
</div>

</v-click>

<div class="muted small centered">
Three engineering tricks turn this into an industrial tool: <b>watched literals</b> (unit propagation in
~constant time), <b>VSIDS</b> (branch on the variables that recently caused conflicts), and
<b>restarts</b>. None of them change the logic. All of them are why it is fast.
</div>

<!--
Verified by brute force before going on the slide: the unique satisfying assignment is
x1=F, x2=T, x3=F, and the trace reaches it.
-->

---
layout: center
---

# How a program verifier decides

<div class="lead">Annotated code → verification conditions → SMT query. Three outcomes, no magic.</div>

```lean
def myMax (a b : Int) : Int := if a ≤ b then b else a

theorem spec : ∀ a b, a ≤ myMax a b ∧ b ≤ myMax a b
```

<div class="grid2">
<div>
<div class="h3">The tool generates this</div>
<div class="mono small vc">
∀ a b : Int,<br>
&nbsp;&nbsp;(a ≤ b &nbsp;→&nbsp; a ≤ b ∧ b ≤ b)<br>
&nbsp;&nbsp;∧<br>
&nbsp;&nbsp;(¬(a ≤ b) → a ≤ a ∧ b ≤ a)
</div>
<div class="muted small" style="margin-top:0.6rem">
One branch per path through the <span class="mono">if</span>. This is <b>weakest-precondition</b>
generation, and it is mechanical.
</div>
</div>
<div>
<div class="h3 accent">Then it asks the solver</div>
<div class="small">
"Sit the <b>negation</b> of this. Is it unsatisfiable?"
</div>
<table class="clean small">
<tr><td class="mono yes">unsat</td><td>no counterexample exists → <b>verified</b></td></tr>
<tr><td class="mono no">sat</td><td>here is a model → <b>counterexample</b></td></tr>
<tr><td class="mono">unknown</td><td>it gave up → <b>your problem</b></td></tr>
</table>
</div>
</div>

<v-click>

<div class="callout">
<b>Change the spec to something false and watch what the tool gives you.</b>
Ask for <span class="mono">a &lt; myMax a b</span> and the solver returns <span class="mono">sat</span> with the
model <span class="mono">a = b = 5</span>. That is not an error message — <b>it is the failing input</b>.
Counterexamples are the product, not the consolation prize.
</div>

</v-click>

<!--
The myMax obligation is the same one in demos/lean/Demo.lean, where omega discharges it — same
pipeline, smaller package. The point of the slide: verification is VC generation plus a solver, and
the solver is a black box you can reason about.
-->

---
layout: center
---

# When the solver says `unknown`

<div class="lead">The part nobody puts in a product page. It happens constantly, and it is not a bug.</div>

<div class="grid2">
<div>
<div class="h3">Why it happens</div>
<ul class="small">
<li><b>Nonlinear arithmetic</b> — <span class="mono">x·y &lt; z</span> is undecidable over the integers</li>
<li><b>Quantifiers</b> — needs instantiation heuristics; the wrong trigger and it flounders</li>
<li><b>Floating point and transcendentals</b></li>
<li><b>Strings and regexes</b> beyond the supported fragment</li>
<li><b>Sheer size</b> — the timeout, not the logic</li>
</ul>
</div>
<div>
<div class="h3 accent">What you actually do</div>
<ul class="small">
<li>Add an <b>intermediate assertion</b> so the solver can take two small steps instead of one leap</li>
<li>Supply a <b>lemma</b> that captures the fact it can't derive</li>
<li><b>Restructure the encoding</b> — bit-vectors instead of integers, or the reverse</li>
<li><b>Weaken the property</b> and prove the rest by hand</li>
<li>Give it a <b>different solver</b> — this works surprisingly often</li>
</ul>
</div>
</div>

<div class="callout">
<b>This is the annotation burden, and it is the real cost of deductive verification.</b> Not the
solver's speed — the human hours spent turning one unprovable goal into five provable ones.
It is also exactly the work AI is now good at, which is why
<span class="mono">llm-proof-engineering</span> is the page to read next.
</div>

<div class="muted small centered">
And the honest framing: <span class="mono">unknown</span> is <b>Rice's theorem arriving at the tool
boundary</b>. Somebody has to supply the insight the machine cannot compute. The tool's job is to make
sure that whatever they supply gets <i>checked</i>.
</div>

---
layout: center
---

# How an invariant is actually found

<div class="lead">The skill nobody demonstrates. Start with the property you want:</div>

<div class="syllogism" style="margin:0.8rem 0">
<div class="syl">
<div class="syl-line mono">MutualExclusion &nbsp;≡&nbsp; ¬(pc₁ = crit ∧ pc₂ = crit)</div>
</div>
</div>

<div class="lead">
Ask the tool to prove it by induction. <b>It fails</b> — and it hands you a
<b>counterexample to induction</b>: not a bug, a state that satisfies your property whose successor
violates it.
</div>

<div class="grid2">
<div>
<div class="h3">The CTI it gives you</div>
<div class="mono small vc">
pc = [p₁ ↦ <b>idle</b>, p₂ ↦ <b>crit</b>]<br>
owner = <b>0</b>
</div>
<div class="muted small" style="margin-top:0.5rem">
This satisfies <span class="mono">MutualExclusion</span> — only p₂ is critical.<br>
But <span class="mono">Acquire(p₁)</span> is <b>enabled</b> (owner = 0), and it produces
<span class="mono">pc₁ = crit ∧ pc₂ = crit</span>.
</div>
</div>
<div>
<div class="h3 accent">Read the CTI, generalise it</div>
<div class="muted small">
The state is legitimate — nothing in my invariant says <span class="mono">owner</span> has to agree with
the program counters. That's the missing fact, and the CTI points straight at it:
</div>
<div class="mono small vc" style="margin-top:0.6rem">
<b>∀ i.&nbsp; pcᵢ = crit &nbsp;→&nbsp; owner = i</b>
</div>
</div>
</div>

<v-click>

<div class="callout">
One clause. Now the three obligations close: <span class="mono">Init ⇒ I</span> ✓,
<span class="mono">I ∧ Next ⇒ I′</span> ✓, <span class="mono">I ⇒ Mutex</span> ✓ — and the middle one is
true because a process can only enter the critical section while <span class="mono">owner = 0</span>,
which the invariant says is impossible if anyone else is in there.
</div>

</v-click>

<div class="muted small centered">
<b>This loop — CTI, read it, strengthen by one clause — is the entire craft.</b> Ivy makes it decidable so
the CTI is always explainable. Veil generates the CTI for you. Neither finds the clause for you.
</div>

<!--
Verified exhaustively over a finite model before putting it on the slide: the naive invariant has
exactly this counterexample to induction, and the strengthened one satisfies all three obligations.
-->

---
layout: center
---

# State explosion, with numbers

<div class="lead">Why model checking needs a protocol-sized target, not your application.</div>

<table class="clean small">
<thead><tr><th></th><th>Global states (4 local states each)</th><th>Explicit-state checking</th></tr></thead>
<tr><td>5 processes</td><td class="mono">4⁵ = 1.0 × 10³</td><td class="yes">instant</td></tr>
<tr><td>10 processes</td><td class="mono">4¹⁰ = 1.0 × 10⁶</td><td class="yes">seconds</td></tr>
<tr><td>15 processes</td><td class="mono">4¹⁵ = 1.1 × 10⁹</td><td>minutes to hours</td></tr>
<tr class="hl"><td><b>20 processes</b></td><td class="mono"><b>4²⁰ = 1.1 × 10¹²</b></td><td class="no">out of reach</td></tr>
<tr><td>25 processes</td><td class="mono">4²⁵ = 1.1 × 10¹⁵</td><td class="no">no</td></tr>
</table>

<div class="grid2">
<div>
<div class="h3">And that's the <i>generous</i> model</div>
<div class="small">
It counts only process state. Add <b>message channels</b> — a queue of capacity <span class="mono">c</span>
between every pair — and each channel multiplies the space by <span class="mono">c+1</span>. With
<span class="mono">n²</span> channels, the exponent <b>itself</b> becomes quadratic in your process count.
</div>
</div>
<div>
<div class="h3 accent">What the mitigations actually cost</div>
<table class="clean small">
<tr><td>Symmetry reduction</td><td class="dim">need symmetric processes</td></tr>
<tr><td>Partial-order reduction</td><td class="dim">need independence</td></tr>
<tr><td>Symbolic (BDD/SMT)</td><td class="dim">changes the failure mode</td></tr>
<tr><td>Bounded checking</td><td class="dim">not a proof past depth k</td></tr>
<tr><td>Abstraction (CEGAR)</td><td class="dim">needs refinement effort</td></tr>
</table>
</div>
</div>

<div class="callout">
<b>The practical rule that follows:</b> model-check the <i>protocol</i> — a few hundred lines of design with
a small number of participants — and never the application. The exponent is why scoping is not a
weakness of the method. It is the method.
</div>

---
layout: center
---

# How the kernel decides

<div class="lead">The trusted part of Lean is a <b>reduction machine plus a type checker</b>. Nothing else.</div>

```lean
-- closes by computation: both sides reduce to the same term
example : 2 + 2 = 4 := rfl

-- does NOT close by computation: the two sides are different normal forms
example (m n : Nat) : m + n = n + m := Nat.add_comm m n
```

<div class="grid3">
<div class="stat">
<div class="sn">1</div>
<div class="sl"><b>Reduce</b><br><span class="dim">normalise both sides</span></div>
</div>
<div class="stat">
<div class="sn">2</div>
<div class="sl"><b>Compare</b><br><span class="dim">definitional equality</span></div>
</div>
<div class="stat">
<div class="sn">3</div>
<div class="sl"><b>Assign</b><br><span class="dim">the term gets the type</span></div>
</div>
</div>

<v-click>

<div class="callout">
That is the whole kernel, and <b>definitional equality is decidable</b> — which is what makes checking
cheap, which is what makes the asymmetry in Part III true. When <span class="mono">rfl</span>,
<span class="mono">simp</span> or <span class="mono">omega</span> close a goal, they are exploiting
<i>computation</i>, not reasoning.
</div>

</v-click>

<div class="callout">
<b>And the audit is one command.</b> <span class="mono">#print axioms my_theorem</span> lists exactly what
a proof depends on. A constructive proof says <i>"does not depend on any axioms"</i>. Use a classical
argument and it says <span class="mono">[propext, Classical.choice, Quot.sound]</span> — the 1912
philosophy argument from Part II, surfacing in your build output.
</div>

<div class="muted small centered">
Every tactic, macro, elaborator and AI agent above the kernel is <b>untrusted by design</b>. They propose
terms; the kernel checks them. A thousand lines of buggy tactic code cannot make a false theorem true.
</div>

---
layout: center
---

# The trusted base, itemised

<div class="lead centered">Every verified claim rests on something nobody verified. Say what it is.</div>

<table class="clean small">
<thead><tr><th>Claim</th><th>What you are actually trusting</th><th>Rough size</th></tr></thead>
<tr><td>"Lean accepted this theorem"</td><td>the Lean kernel + the axioms <span class="mono">#print axioms</span> reports</td><td class="mono">~10³ lines</td></tr>
<tr><td>"Z3 says unsat"</td><td>the solver <b>and</b> your encoding of the problem into it</td><td class="mono">~10⁵ lines</td></tr>
<tr><td>"TLC found no violation"</td><td>the checker + your model + the config bounds</td><td class="mono">—</td></tr>
<tr><td>"the C is correct"</td><td>also the compiler, unless you re-verified the binary</td><td class="mono">—</td></tr>
<tr><td>"it runs correctly"</td><td>the CPU, the OS, the network, the operator</td><td class="mono">—</td></tr>
</table>

<div class="grid2">
<div>
<div class="h3">What this means in practice</div>
<div class="small">
A <b>100× difference</b> in trusted-base size between a kernel-checked proof and an SMT-backed one.
Both are legitimate. They are not the same claim, and a verification report that doesn't say which
one it is hasn't told you anything you can use.
</div>
</div>
<div>
<div class="h3 accent">The highest-value habit in this field</div>
<div class="small">
<b>Every serious verification project publishes an assumptions section.</b> Ordinary engineering
projects almost never write one down. That is free to adopt tomorrow, and it is where
<a href="https://yihuang.github.io/awesome-formal-methods/01-fundamentals/limits.html">most real
failures live</a> — not in the proof.
</div>
</div>
</div>

<div class="muted small centered">
Sizes are order-of-magnitude. The exact figures belong in the
<a href="https://yihuang.github.io/awesome-formal-methods/01-fundamentals/limits.html#the-trusted-base">wiki</a>,
with sources.
</div>

---
layout: center
---

# The bill

<div class="lead">What it costs, measured rather than promised.</div>

<div class="grid3">
<div class="stat">
<div class="sn">23×</div>
<div class="sl">proof lines per line of code<br><span class="dim">seL4: 200,000 Isabelle vs 8,700 C</span></div>
</div>
<div class="stat">
<div class="sn">~20</div>
<div class="sl">person-years<br><span class="dim">the original seL4 effort</span></div>
</div>
<div class="stat">
<div class="sn">↓</div>
<div class="sl">re-verification cost<br><span class="dim">the proof infrastructure already exists</span></div>
</div>
</div>

<div class="grid2">
<div>
<div class="h3">Why the third number is the one that matters</div>
<div class="small">
The 23× and the 20 person-years are <b>initial</b> costs, and quoting them without the third number is
how this field gets dismissed. Once the proof exists, changing the code costs a re-check, not a
re-proof. That is the difference between an expense and an asset — and it is why the verified core has
to be <b>small and stable</b>.
</div>
</div>
<div>
<div class="h3 accent">And the failure mode to plan for</div>
<div class="small">
Proofs are code with no specification of their own, so they rot. When mathlib moved from Lean 3 to
Lean 4, a language change invalidated a very large body of proofs at once, and repairing it took
years of community effort. Budget for re-verification, and keep the verified surface small enough to
re-do.
</div>
</div>
</div>

<div class="callout">
<b>The scoping rule, stated as economics:</b> verification is worth it when
<span class="mono">(cost of failure) × (probability)</span> exceeds
<span class="mono">(cost of the proof) + (cost of re-proving it every time the code changes)</span>.
The second term is what people forget, and it is the reason <i>small and stable</i> is the whole game.
</div>

---
layout: section
---

<div class="part">Part VI</div>
# Practice: the limits, and one thing to do
<div class="partsub">The honest boundaries — then the smallest useful step</div>

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
<li><span class="mono">/01-fundamentals/logics</span> — Hoare logic, in full</li>
<li><span class="mono">/01-fundamentals/temporal-logic</span> — LTL, safety, liveness, stuttering</li>
<li><span class="mono">/01-fundamentals/curry-howard</span> — why proofs are programs</li>
<li><span class="mono">/01-fundamentals/separation-logic</span> — the frame rule</li>
<li><span class="mono">/01-fundamentals/limits</span> — Gödel, Rice, the trusted base</li>
</ul>
</div>
<div>
<div class="h3">The practice</div>
<ul>
<li><span class="mono">/03-applications/lightweight-fm</span> — the on-ramp, with code</li>
<li><span class="mono">/03-applications/blockchain</span> — EVM, zk, verified compilers</li>
<li><span class="mono">/04-ai-era/llm-proof-engineering</span> — AI writing Lean</li>
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
