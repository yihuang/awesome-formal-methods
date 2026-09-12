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

The deck is deliberately *not* a tool tour. It is built on the wiki's strongest material:

| Part | Content | Why it's there |
|---|---|---|
| I · The impossible thing | Hilbert → Gödel, Turing, Rice → **the asymmetry** | the philosophy; earns everything after it |
| II · The ideas that work | **Hoare logic basics** → Curry–Howard + the kernel → the spec gap → stuttering invariance → **LTL basics** → safety vs liveness → fairness → the frame rule → CompCert's zero | the deep fundamentals; basics come before the ideas that build on them |
| III · The AI era | the inversion → AWS's 2014 precedent → **2024 milestone → 2025 specialists → 2026 state of the art** → the ten results → the proof is the review → blockchain | the reason this talk exists now |
| IV · The honest part | what FM can't do, verified systems that failed, the adoption gap | say it before the audience does |
| V · What to do | the ladder, the 5 things, three sentences | the ask |

**The two slides that carry the talk:**

1. **The asymmetry** — searching is expensive, checking is cheap. Everything follows from it.
2. **"I made this mistake four times writing the wiki"** — four bugs, all in the *property*, none in
   the *proof*. Self-incriminating, and the most credible evidence for the whole argument.

## Revision history

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
