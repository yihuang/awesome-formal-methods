# Site build configuration

How this wiki is built, and the conventions that affect rendered output. Nothing here is published
as a page — it is maintainer documentation.

```
docs/
├── .vitepress/
│   ├── config.mts              site config: nav, sidebar, theme, markdown options
│   ├── grammars/               TextMate grammars for languages Shiki doesn't bundle
│   └── dist/                   build output (gitignored)
├── public/                     copied verbatim to the site root (robots.txt)
└── *.md                        the wiki itself
```

```bash
npm run docs:dev      # live preview
npm run docs:build    # -> docs/.vitepress/dist
npm run docs:preview  # serve the built output
```

---

## Conventions that affect rendered output

These four things will silently do the wrong thing if you don't know about them. All four have
caused a real bug in this repository.

### 1. Math — `$...$` and `$$...$$`

Math is rendered by **MathJax**, at **build time**, into inline SVG. There is no runtime
JavaScript: a page with math ships rendered SVG, and a page without math ships nothing extra.

**The trap:** VitePress's `markdown.math` option defaults to `true`, but it **silently does
nothing** if the optional dependency `markdown-it-mathjax3` is not installed. `$x^2$` then renders
as literal text with no warning anywhere. That is exactly what happened here, and it is why
`math: true` is now stated explicitly in `config.mts` with a comment — so the dependency is not a
mystery when it goes missing.

**The second trap: `$` is also the dollar sign.** Inline math is delimited by `$...$`, so two
dollar amounts on one line can be parsed as a formula:

| Written | Result |
|---|---|
| `~$475M` on its own line | ✅ fine — an unpaired `$` is left alone |
| `costs ~$475M and saves ~$48M` | ❌ `$475M and saves ~$` becomes a formula |
| `generation $$ → ¢` | ❌ **`$$` opens display math** and swallows the rest of the block |

Rules of thumb:

- Never put two `$` on one line in prose. Specify the currency, or split the sentence.
- Never write a bare `$$` outside a formula. (One table cell in `appendix/presenting.md` did, and
  was rewritten.)
- To write a literal dollar sign next to a formula, escape it: `\$`.

Check before committing:

```bash
# any line with a paired $ outside a code fence?
python3 - <<'PY'
import re, pathlib
for p in pathlib.Path("docs").rglob("*.md"):
    if ".vitepress" in p.parts: continue
    body = re.sub(r"```.*?```", "", p.read_text(encoding="utf-8"), flags=re.S)
    for i, line in enumerate(body.split("\n"), 1):
        if line.count("$") >= 2:
            print(f"{p}:{i}: {line.strip()[:90]}")
PY
```

**Accessibility.** MathJax emits assistive MathML alongside the SVG, so screen readers get a
linearised form of the formula. Even so, **state every formula's content in prose as well** — it
costs one sentence and it survives the next tooling change.

### 2. Heading anchors — GitHub-compatible slugs

VitePress's default slugger prefixes headings that start with a digit with an underscore
(`## 1. Foo` → `_1-foo`), while GitHub produces `1-foo`. Since this wiki is read in both places,
`config.mts` installs a GitHub-compatible `slugify` so one anchor works in both renderers.

**The trap:** without this, every cross-page `#anchor` pointing at a numbered heading is silently
broken *on the site only* — the links look correct in the source and on GitHub. It broke 14 of them
here. See `research-notes.md` §9.

### 3. Code fences — Shiki + vendored grammars

Shiki bundles ~300 languages, including everything this wiki mostly uses (`lean`, `python`, `rust`,
`bash`, `yaml`, `solidity`, `coq`, and `shellsession` for shell transcripts).

```bash
npm run grammars:list            # every bundled language id
npm run grammars:list tla dafny  # check specific ids; exits 1 on a miss
```

For anything not bundled, vendor a grammar — see [`grammars/README.md`](grammars/README.md) for the
attribution requirements and the registration snippet. `tla` and `dafny` are vendored there.

**The trap:** a language Shiki doesn't know falls back to plain text with only a build-log warning.
The page looks *fine* — just unhighlighted — so nobody notices.

### 4. Base path

The site is a GitHub Pages **project** site, so `base = '/awesome-formal-methods/'` in `config.mts`.
Renaming the repository or moving to a user site (`yihuang.github.io`) requires changing it.

**The trap:** relative links from `docs/` that resolve *above* `docs/` exist on disk but are never
published, so they 404 on the site. `tools/check-links.py` has a guard for this; use an absolute
GitHub URL for anything outside the docs tree.

---

## Verification

Four checkers run in CI before the site is deployed. Each catches a class of bug the others cannot:

| Command | Catches |
|---|---|
| `python3 tools/check-links.py` | broken relative Markdown links, bad anchors, links escaping `docs/` |
| `python3 tools/check-refs.py` | a page missing its `## References` section (a ratchet, currently 0) |
| `npm run docs:build` | VitePress dead links — **fails the build** |
| `python3 tools/check-site.py` | broken links in the *built* HTML: base paths, rewritten anchors, hashed assets |

`check-site.py` is the only one that sees what users actually load, and it found bugs the Markdown
checker could not. Run it after any change to `config.mts`.

For rendering changes, assert on the output rather than trusting the build exit code — a silent
fallback still exits 0:

```bash
npm run docs:build 2>&1 | grep "not loaded"        # unhighlighted languages
grep -c 'mjx-container' docs/.vitepress/dist/01-fundamentals/temporal-logic.html   # math rendered
```
