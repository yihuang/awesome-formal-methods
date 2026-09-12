# TextMate grammars for languages Shiki doesn't bundle

VitePress highlights code with [Shiki](https://shiki.style/), which ships ~300 TextMate
grammars. That covers most of what this wiki needs — `lean`, `python`, `rust`, `bash`, `yaml`,
`solidity`, `coq`, and so on.

It does **not** cover two languages this wiki uses, so their grammars are vendored here and
registered in [`../config.mts`](../config.mts) via `markdown.languages`.

| File | Language | Renders fences | Upstream | Commit | Retrieved |
|---|---|---|---|---|---|
| `tlaplus.tmLanguage.json` | TLA+ / PlusCal | ` ```tla ` | [tlaplus/vscode-tlaplus · `languages/tlaplus-grammar.json`](https://github.com/tlaplus/vscode-tlaplus/blob/master/languages/tlaplus-grammar.json) | `2646260c65b2` (2026-04-01) | 2026-09-12 |
| `dafny.tmLanguage.json` | Dafny | ` ```dafny ` | [dafny-lang/ide-vscode · `syntaxes/Dafny.tmLanguage`](https://github.com/dafny-lang/ide-vscode/blob/master/syntaxes/Dafny.tmLanguage) | `58c3528d680a` (2024-11-12) | 2026-09-12 |

## Licensing

Both grammars are **MIT**-licensed and are redistributed here unmodified except as noted below.
The upstream notices:

**`tlaplus.tmLanguage.json`**
```
MIT License

Copyright (c) 2019 Andrew Lygin
Copyright (c) 2020 TLA+ Foundation
```

**`dafny.tmLanguage.json`**
```
MIT License

Copyright (c) 2016 Jonathan Rosca
Copyright (c) 2017 Markus Schaden, Rafael Krucker
Copyright (c) 2018 Institute for Software - University of Applied Science (HSR) Rapperswil
```

Full license texts are in each upstream repository. Neither grammar is covered by this
repository's own [LICENSE](../../../LICENSE) or [LICENSE-docs](../../../LICENSE-docs).

## One modification was required (Dafny)

The upstream Dafny file is a **plist**, and it contains two raw `<` characters inside regular
expressions — `(?<!` and `(?<=` — which makes it **invalid XML**. VS Code's parser is lenient
(the [`fast-plist`](https://github.com/microsoft/vscode-fast-plist) style parsers tolerate it),
but strict parsers reject it:

```
xml.parsers.expat.ExpatError: not well-formed (invalid token): line 136, column 15
```

To vendor it, the plist was converted to JSON, with exactly those two characters escaped to
`&lt;` so the document parses. This is the only change, and it is semantics-preserving — the
parsed regexes are the intended `(?<!` and `(?<=`.

Conversion and repair, for reproducibility:

```bash
curl -sL -o Dafny.tmLanguage \
  https://raw.githubusercontent.com/dafny-lang/ide-vscode/58c3528d680a/syntaxes/Dafny.tmLanguage

python3 - <<'PY'
import plistlib, json, pathlib
raw = pathlib.Path("Dafny.tmLanguage").read_text(encoding="utf-8")
d = plistlib.loads(raw.replace("(?<!", "(?&lt;!").replace("(?<=", "(?&lt;=").encode())
d.pop("uuid", None)
pathlib.Path("dafny.tmLanguage.json").write_text(json.dumps(d, indent=2) + "\n")
PY
```

If upstream fixes the escaping, re-vendor and delete this section.

## Adding another language

1. **Check whether Shiki already has it** — no need to vendor anything if it does:

   ```bash
   npm run grammars:list | grep -x 'yourlang'
   ```

   That script prints every bundled language id. VitePress bundles the lot, so anything listed
   works in a fence immediately.

2. **If it isn't bundled**, fetch the upstream grammar (prefer the official editor extension for
   the language, which is usually the best-maintained), drop the JSON here, and register it in
   [`../config.mts`](../config.mts):

   ```ts
   import { readFileSync } from 'node:fs'
   import { dirname, resolve } from 'node:path'
   import { fileURLToPath } from 'node:url'

   const grammarDir = resolve(dirname(fileURLToPath(import.meta.url)), 'grammars')
   const grammar = (file: string) =>
     JSON.parse(readFileSync(resolve(grammarDir, file), 'utf8'))

   // in the config object:
   markdown: {
     languages: [
       { ...grammar('tlaplus.tmLanguage.json'), name: 'tla', aliases: ['tlaplus'] },
       { ...grammar('dafny.tmLanguage.json'),   name: 'dafny', aliases: ['dfy'] }
     ]
   }
   ```

   `name` must match the fence label you want to write. The grammar's own `scopeName` is
   independent of it.

3. **Verify**: build, and check that the fallback warning for your language is gone and that the
   output contains token classes.

   ```bash
   npm run docs:build 2>&1 | grep "not loaded"   # expect nothing
   ```

4. **Record** the source URL, commit SHA, retrieval date, and license in the table above. If you
   had to modify the file, say so and say why — a silently patched vendored artifact is a
   liability.

## Why vendor rather than hand-write

A hand-written grammar is a permanent maintenance cost and will be worse than the one the
language's own tooling ships. Vendoring a pinned, attributed copy is both more accurate and
easier to update — the trade-off is that attribution and license tracking become *your*
responsibility, which is what this file is for.
