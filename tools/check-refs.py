#!/usr/bin/env python3
"""
check-refs.py — audit reference coverage across the wiki.

The wiki's citation convention lives in docs/references/README.md:

  1. inline link at the point of every checkable claim
  2. a `## References` section at the end of each page, listing the sources used
  3. the master bibliography

This script checks (1) and (2) are actually happening, and reports on density.

It is a RATCHET by design: `--max-missing` defaults to the number of pages currently
lacking a References section. That number may only go down. Fixing a page is progress;
adding a new page without references fails CI.

Usage:
    python3 tools/check-refs.py                  # report + ratchet check
    python3 tools/check-refs.py --strict         # fail if ANY page lacks references
    python3 tools/check-refs.py --max-missing 10 # explicit ratchet
    python3 tools/check-refs.py --md             # emit a Markdown table for pasting into a page

Exit codes: 0 = within budget, 1 = budget exceeded (or --strict failure), 2 = bad usage.
"""

from __future__ import annotations

import os
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

# --- ratchet -----------------------------------------------------------------
# Lower this whenever you add a References section. Never raise it.
MAX_MISSING_DEFAULT = 0
# -----------------------------------------------------------------------------

DOCS = Path("docs")

# Pages that are navigation or conventions, and legitimately do not carry sources.
# Build-configuration docs under .vitepress/ are skipped outright (see audit()).
EXEMPT = {
    # navigation and section indexes (no claims of their own)
    "docs/index.md",
    "docs/README.md",
    "docs/01-fundamentals/index.md",
    "docs/03-applications/index.md",
    "docs/04-ai-era/index.md",
    "docs/05-tools/index.md",
    "docs/06-practice/index.md",
    "docs/00-orientation/reading-paths.md",
    # describes local artifacts rather than external claims
    "docs/demos.md",
    # conventions and the master list itself
    "docs/references/index.md",
    "docs/references/bibliography.md",
    # optional appendix about presenting
    "docs/appendix/presenting.md",
}

LINK_RE = re.compile(r"!?\[[^\]]*\]\((https?://[^)\s]+)\)")
H2_RE = re.compile(r"^##\s+References\s*$", re.IGNORECASE | re.MULTILINE)
H2_ANY_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
WARN_MARK = "⚠️"


def external_links(text: str) -> list[str]:
    return [u.rstrip(".,;") for u in LINK_RE.findall(text)]


def strip_code(text: str) -> str:
    """Remove fenced code blocks so links inside examples aren't counted as citations."""
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def audit() -> tuple[list[dict], Counter]:
    rows = []
    domains: Counter = Counter()
    for path in sorted(DOCS.rglob("*.md")):
        # .vitepress/ is build configuration and docs/public/ is verbatim static
        # assets. Neither is published wiki content, so a markdown file there is
        # an engineering note, not a page that needs a References section.
        if ".vitepress" in path.parts or "public" in path.parts:
            continue
        rel = path.relative_to(Path.cwd()).as_posix() if path.is_absolute() else path.as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        prose = strip_code(text)
        links = external_links(prose)
        for u in links:
            try:
                domains[urlparse(u).netloc] += 1
            except ValueError:
                pass
        headings = [h.strip() for h in H2_ANY_RE.findall(text)]
        rows.append(
            {
                "path": rel,
                "has_refs": bool(H2_RE.search(text)),
                "headings": headings,
                "ext_links": len(links),
                "unique_ext": len(set(links)),
                "warnings": text.count(WARN_MARK),
                "words": len(text.split()),
                "exempt": rel in EXEMPT,
            }
        )
    return rows, domains


def main() -> None:
    args = sys.argv[1:]
    strict = "--strict" in args
    as_md = "--md" in args
    max_missing = MAX_MISSING_DEFAULT
    if "--max-missing" in args:
        i = args.index("--max-missing")
        try:
            max_missing = int(args[i + 1])
        except (IndexError, ValueError):
            print("--max-missing needs an integer", file=sys.stderr)
            sys.exit(2)

    if not DOCS.is_dir():
        print(f"run from the repository root (no {DOCS}/ found)", file=sys.stderr)
        sys.exit(2)

    rows, domains = audit()
    checkable = [r for r in rows if not r["exempt"]]
    missing = [r for r in checkable if not r["has_refs"]]
    scanty = [r for r in checkable if r["has_refs"] and r["unique_ext"] < 3]

    if as_md:
        print("| Page | Ext. links | Unique sources | References section |")
        print("|---|---:|---:|:--:|")
        for r in sorted(checkable, key=lambda r: r["unique_ext"]):
            print(
                f"| `{r['path']}` | {r['ext_links']} | {r['unique_ext']} | "
                f"{'✅' if r['has_refs'] else '❌'} |"
            )
        return

    print(f"Scanned {len(rows)} Markdown files ({len(checkable)} checkable, "
          f"{len(rows) - len(checkable)} exempt).\n")

    print(f"Pages with a `## References` section : {len(checkable) - len(missing)}/{len(checkable)}")
    print(f"Pages missing one                    : {len(missing)}  (budget {max_missing})")
    print(f"Pages with <3 unique sources         : {len(scanty)}")
    total_links = sum(r["ext_links"] for r in checkable)
    total_unique = sum(r["unique_ext"] for r in checkable)
    print(f"External links (excluding code blocks): {total_links} ({total_unique} unique)")
    print(f"Distinct source domains               : {len(domains)}")
    print(f"⚠️ markers across the wiki             : {sum(r['warnings'] for r in checkable)}")

    if missing:
        print("\nMissing a References section:")
        for r in missing:
            print(f"  - {r['path']}  ({r['unique_ext']} unique external sources)")

    if scanty:
        print("\nHas References but fewer than 3 unique external sources (consider deepening):")
        for r in scanty:
            print(f"  - {r['path']}  ({r['unique_ext']})")

    print("\nTop source domains:")
    for dom, n in domains.most_common(12):
        print(f"  {n:>3}  {dom}")

    if "id" in args:  # pragma: no cover
        pass

    limit = 0 if strict else max_missing
    if len(missing) > limit:
        print(
            f"\n❌ {len(missing)} pages lack a References section, over the budget of {limit}.\n"
            f"   Add `## References` to a page (see docs/references/README.md), or add newly\n"
            f"   created pages to the EXEMPT set if they are navigation only.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"\n✅ Within budget ({len(missing)}/{limit} pages missing references).")


if __name__ == "__main__":
    main()
