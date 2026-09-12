# The slide deck

**Live:** <https://yihuang.github.io/awesome-formal-methods/slides/>

A [Slidev](https://sli.dev/) deck that distils this wiki into ~35 slides for a 45-minute tech
sharing. It is built into the wiki site (`docs/public/slides/`), so it deploys with everything else.

```bash
npm run slides:dev      # live preview with presenter mode (press `p`)
npm run slides:build    # -> docs/public/slides/
npm run build:all       # deck + wiki site
```

---

## The talk

**AI Made Code Cheap. Trust Is Still Expensive.**

Ordered as **motivation → history → methodology → AI era → practice**. That order matters: an
engineer will sit through 2,300 years of philosophy *if* they already know why it is their problem,
and will check out if the deck opens on Aristotle.

| | |
|---|---|
| **I · Motivation** | **why this is your problem**, the inversion, the roadmap. No scene-setting: the deck opens on the engineer's situation |
| **II · History** | Aristotle → Euclid → the fifth postulate → Boole/Frege/Russell → Hilbert → the three schools → what formalism is *for* → where the regress of trust stops; then Gödel, Turing, Rice |
| **III · Methodology** | the asymmetry, the propose/check architecture, Hoare logic, Curry–Howard, the spec gap, **LTL basics → safety/liveness → fairness → stuttering invariance**, the frame rule |
| **IV · The AI era** | AWS's 2014 precedent, 2024 → 2026 state of the art, the ten results, the proof is the review, blockchain |
| **V · Practice** | the honest limits, the adoption gap, the ladder, the five things |

The deck is deliberately *not* a tool tour. It is built on the wiki's strongest material:

**The two slides that carry the talk:**

1. **The asymmetry** — searching is expensive, checking is cheap. Everything follows from it.
2. **"I made this mistake four times writing the wiki"** — four bugs, all in the *property*, none in
   the *proof*. Self-incriminating, and the most credible evidence for the whole argument.

## Why the order is motivation-first

An earlier version opened on Aristotle. The failure mode is obvious in hindsight: an engineer watches
nine slides about the philosophy of mathematics with **no established reason to care**, and the
deck loses them before it has made a single claim about their job.

So Part I now earns the right to the history section. It spends three slides on the engineer's actual
situation — you review more code than you can read, your tests share your model's blind spots,
testing samples and cannot cover the input you didn't imagine, and the failure surfaces in
production. Only then does the deck say: *this question is 2,300 years old, and here is what those
people worked out.* The history part now **pays rent** instead of asking for patience.

## The history section, in detail

It answers the question the rest of the deck depends on: **why would symbols on paper ever be more
trustworthy than a competent person's judgement?**

| Slide | The idea |
|---|---|
| *Why would anyone want this?* | pose the 2,300-year-old question before answering it |
| *Separating form from content* (Aristotle, ~350 BCE) | the syllogism is valid **no matter what A, B and C are** — validity is a property of shape, not content. This is the birth of formality, and what a type checker does to a proof 2,300 years later |
| *The first specification* (Euclid, ~300 BCE) | a claim is accepted because of its **derivation, not its author**. Everything in this talk mechanises that sentence |
| *Then intuition broke* (1733→1832) | Saccheri derived a coherent non-Euclidean geometry and rejected it as *"repugnant to the nature of a straight line."* A century later it was accepted, and models showed it was as consistent as Euclid |
| *The most important philosophical shock* | if two incompatible geometries are both consistent, **axioms are choices, not truths**. Mathematics became about *consequence*, not truth. **Your specification is a choice; the proof is only relative to what you chose** — the spec gap, two centuries early |
| *Logic becomes a language* (1854→1901) | Boole makes reasoning calculable; Frege makes it a precise language with quantifiers; Russell's paradox breaks Frege's system while the book is at the printer |
| *The answer: a game with rules* (1910→1930) | *Principia Mathematica* (2,000 pages to reach `1+1=2`), then Hilbert's programme and the Entscheidungsproblem |
| *Three schools — and what engineering inherited* | logicism, formalism, intuitionism. **Brouwer rejected `p ∨ ¬p` in 1912 — which is why `Classical.em` is an axiom in Lean and Rocq today**, and why constructive proofs compute |
| *What formalism is actually for* | not replacing judgement with machinery — making **disagreement decidable**. Its product is *agreement without authority*, and its cost is that judgement is **relocated** to the specification |
| *Where the regress of trust stops* | every proof needs a checker, the checker is software, the software runs on a chip… You cannot verify the verifier. **Stopping is a choice, and it is philosophical, not mathematical** |

Two of those land repeatedly later: the *axioms are choices* slide is the spec gap in historical form,
and the *1912 philosophy determines today's `#print axioms`* slide is the rebuttal to anyone who
thinks the philosophy is decoration.

## Pacing

62 slides is a lot for 45 minutes — roughly 43 seconds each. That works because the philosophy
slides are statement slides you *say* rather than read, and because three slides at the end are
explicitly backups.

**If you are running long, cut in this order:**

1. the *2025 specialists* slide — the 2024→2026 arc survives without it
2. *What AlphaProof actually required* — keep the milestone, drop the training detail
3. the *two rules, memorised* slide — it repeats the stuttering theorem
4. the *2025 → 2026* pair collapse into one slide
5. *The objections, answered briefly* — it is already a backup

**Never cut:** the asymmetry, the four-mistakes slide, *Why this is your problem*, or the ask.
The history section is safe to trim *only* if Part I stays intact — it is what earns the detour.

**Do not reintroduce a cold open.** Two versions of this deck tried to hook the audience with history
before explaining the stakes, and both times it read as a non-sequitur. If you want an intriguing
opener, earn it — or use the closing slide's reveal, which is where the 1956 fact now lives.

## Revision history

**v5** — two fixes.

- **Removed the 1956 hook and the provocation slide that followed it.** Opening the deck with the
  history of Logic Theorist, before any reason to care, was the same mistake as opening on Aristotle:
  scene-setting ahead of motivation. The deck now goes title → *Why this is your problem* with nothing
  in between. The 1956 fact still lands — as the **closing** slide, where it reads as a reveal rather
  than a warm-up.
- **Stuttering invariance moved after temporal logic.** It was being introduced before the audience had
  seen traces or the `X` operator, so the Peled–Wilke theorem ("stuttering-invariant iff expressible
  without `next`") referenced a symbol nobody had met. The LTL slides now come first, then
  safety/liveness (which the LTL slide explicitly promises as "the next slide"), then fairness, then
  stuttering. The `X` discussion is now the payoff of the operator table rather than a forward
  reference.

**v4** — reordered to motivation → history → methodology → AI era → practice, on the grounds that the
philosophy was unearned. Added a *"Why this is your problem"* slide (four concrete pressures on a
working engineer) and moved the Amdahl-inversion slide out of the AI era and into Motivation, where
it belongs as the "why now". The roadmap slide now states the five parts explicitly, so nobody is
surprised by the history detour. The asymmetry and the propose/check architecture moved from the end
of the history block to the *start* of Methodology — they are the premise of the techniques, not the
conclusion of the history. Practice now absorbs the honest limits, since those are practical
knowledge rather than a separate act.

**v3** — added the philosophical opening. A reviewer pointed out that the deck explained *how*
formalism fails before establishing *why formalism at all*, and asked for the origin of logic and the
philosophy underneath it. Nine new slides covering Aristotle's syllogism (form vs content), Euclid's
axiomatic method (derivation over authority), the non-Euclidean shock (axioms are choices, not truths),
Boole → Frege → Russell's paradox, Hilbert's programme, the three schools of mathematical philosophy
and what engineering inherited from each, what formalism is *for* (agreement without authority), and
where the regress of trust stops. The `#print axioms` slide now has a 1912 origin story.

**v2** — after a review pass:

- **Added Hoare logic basics** (`{P} C {Q}`, the backward assignment axiom, the invariant you must
  supply). It was the missing on-ramp: the audience recognises the triple, and the invariant sets up
  Part III.
- **Added LTL basics** — traces are infinite, `G`/`F`/`U`, and the four patterns people actually
  write. The old deck jumped straight to "safety and liveness are topologically different", which is
  meaningless without the operators.
- **Removed the "It already shipped" part.** It read as an interruption: a case-study section
  dropped between deep theory and the AI era, with no clear job. The evidence was kept and
  redistributed to where it does work — **CompCert** now closes Part II as the payoff of the kernel
  argument, **AWS's 2014 reframing** opens Part III as the precedent for the AI-era economics, and
  **the adoption gap** moved to the honest part where it belongs.
- **Fixed the state-of-the-art framing.** AlphaProof (IMO 2024) was presented as if it were current;
  it is two years old, and by 2026 generic models have taken over. It is now explicitly labelled a
  *milestone, not the state of the art*, with its own limitations on the slide, followed by a
  2024 → 2025 → 2026 progression that ends at the actual state of the art.

---

## Files

| File | Purpose |
|---|---|
| `slides.md` | the deck itself — frontmatter, slides, and speaker notes in HTML comments |
| `style.css` | the visual design: palette, typography, and every custom component class |
| `public/img/` | optional portraits (see its README) |

## Authoring notes

**Fonts are declared as CSS stacks, not webfonts.** Slidev's default theme injects a Google Fonts
`<link>`; `fonts: { webfonts: [], provider: none }` in the frontmatter removes it, and `style.css`
declares `Inter, -apple-system, …` with system fallbacks. The deck therefore renders identically
offline and makes no font CDN request. **Don't add a `fonts:` block back** — it will silently
reintroduce the network dependency.

**No remote images are required.** The deck is self-contained: all visuals are authored SVG, CSS
components, and typography. That was a deliberate choice after discovering that fetching images from
Wikimedia is rate-limited to roughly one request per session in some environments, and that a broken
image in a live talk is worse than no image. `public/img/` is a drop-in slot for portraits if you
want them.

**Speaker notes** live in `<!-- -->` comments under each slide, visible in presenter mode only.

**Colour vocabulary** (used consistently, so the deck reads without explanation):

| Colour | Means |
|---|---|
| cyan | the good stuff / the point |
| rose | impossible, limited, or a failure |
| green | verified, or "this works" |
| amber | the human's role |
| indigo | the machine's role |

## Presenting

Press `p` for presenter mode (notes, next slide, timer). Press `o` for the slide overview.

- **Have a recorded fallback** if you plan to demo anything live.
- **The deck links into the wiki** on the "where to go next" slide — everything is one link deep, and
  the wiki's [confidence ledger](../docs/research-notes.md) flags the numbers that need checking
  (notably the OpenAI "~$2,000" figure and the Anthropic delegation statistic, both of which the
  deck marks `⚠️` on the slide itself).
