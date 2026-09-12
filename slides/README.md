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
| I · The impossible thing | Gödel, Turing, Rice → the asymmetry | the philosophy; earns everything after it |
| II · The ideas that work | Curry–Howard, the spec gap, stuttering invariance, safety vs liveness, the frame rule | the deep fundamentals, one slide each |
| III · It already shipped | seL4, CompCert's zero, AWS's reframing, the adoption gap | credibility, then honesty |
| IV · The AI era | the inversion, AlphaProof, generic models at 92%, **the proof is the review**, blockchain | the reason this talk exists now |
| V · The honest part | what FM can't do, verified systems that failed | say it before the audience does |
| VI · What to do | the ladder, the 5 things, three sentences | the ask |

**The two slides that carry the talk:**

1. **The asymmetry** — searching is expensive, checking is cheap. Everything follows from it.
2. **"I made this mistake four times writing the wiki"** — four bugs, all in the *property*, none in
   the *proof*. Self-incriminating, and the most credible evidence for the whole argument.

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
