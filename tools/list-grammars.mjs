#!/usr/bin/env node
/**
 * list-grammars.mjs — print every language id Shiki bundles.
 *
 * VitePress highlights fences with Shiki. If a language appears here, it works in a fence
 * with no configuration. If it does not, vendor a grammar (see
 * docs/.vitepress/grammars/README.md).
 *
 * Usage:
 *   node tools/list-grammars.mjs            # all ids, comma separated
 *   node tools/list-grammars.mjs lean tla   # check specific ids
 */
import { bundledLanguages } from 'shiki'

const ids = Object.keys(bundledLanguages).sort()
const wanted = process.argv.slice(2)

if (wanted.length) {
  let missing = 0
  for (const w of wanted) {
    const ok = ids.includes(w)
    if (!ok) missing++
    console.log(`${ok ? '  yes' : '   NO'}  ${w}`)
  }
  process.exit(missing ? 1 : 0)
}

console.log(`${ids.length} bundled languages:\n`)
console.log(ids.join(', '))
