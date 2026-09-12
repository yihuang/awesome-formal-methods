#!/usr/bin/env python3
"""
check-site.py — verify the BUILT VitePress site has no broken internal links.

This is stronger than check-links.py: it inspects the generated HTML, so it
catches problems that only exist after base-path rewriting, link normalisation,
and asset hashing.

It checks:
  - every internal href resolves to a file that exists in dist/
  - every internal src (css/js/images) exists
  - every in-page anchor (#foo) exists on the target page
  - reports external links (informational, not verified)

Usage:
    npm run docs:build
    python3 tools/check-site.py [dist-dir] [--base /awesome-formal-methods/]

Exit code 0 = no broken internal links, 1 = at least one broken.
"""

from __future__ import annotations

import html
import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse

ATTR_RE = re.compile(r'(?:href|src)\s*=\s*"([^"]+)"', re.IGNORECASE)
ID_RE = re.compile(r'\sid\s*=\s*"([^"]+)"', re.IGNORECASE)
SKIP_PREFIXES = ("mailto:", "tel:", "javascript:", "data:", "ftp:")


TABLE_RE = re.compile(r"<table\b.*?</table>", re.DOTALL | re.IGNORECASE)
ROW_RE = re.compile(r"<tr\b.*?</tr>", re.DOTALL | re.IGNORECASE)
TD_RE = re.compile(r"<td\b", re.IGNORECASE)


def check_tables(page: Path, rel_page: str) -> list:
    """Report tables that markdown did not parse as intended.

    Two failure modes, both of which build cleanly and produce well-formed HTML:

    1. **Ragged rows** — rows disagree on cell count. Markdown tables always
       produce uniform rows, so a mismatch means the source is broken.

    2. **A backtick leaking into rendered text.** This is the signature of an
       unescaped `|` inside inline code in a cell: the `|` splits the cell, the
       backticks end up as literal text, and because the row is then truncated
       to the header's column count the cell *count* still matches — so (1)
       does not catch it. Any literal backtick in rendered output is a bug,
       since inline code becomes `<code>`.
    """
    problems = []
    text = page.read_text(encoding="utf-8", errors="replace")
    for t_i, table in enumerate(TABLE_RE.findall(text), start=1):
        counts = []
        for row in ROW_RE.findall(table):
            n = len(TD_RE.findall(row))
            if n:
                counts.append(n)
        if len(counts) > 1 and len(set(counts)) > 1:
            problems.append(
                (rel_page, f"table #{t_i} has ragged rows: cell counts {sorted(set(counts))}")
            )
        for cell in re.findall(r"<t[dh]\b[^>]*>(.*?)</t[dh]>", table, re.DOTALL | re.IGNORECASE):
            plain = html.unescape(re.sub(r"<[^>]+>", "", cell))
            if "`" in plain:
                snippet = " ".join(plain.split())[:70]
                problems.append(
                    (rel_page, f'table #{t_i}: stray backtick in rendered cell: "{snippet}"')
                )
    return problems


def page_ids(path: Path, cache: dict) -> set:
    if path in cache:
        return cache[path]
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        cache[path] = set()
        return cache[path]
    ids = {html.unescape(m) for m in ID_RE.findall(text)}
    cache[path] = ids
    return ids


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    base = "/awesome-formal-methods/"
    for a in sys.argv[1:]:
        if a.startswith("--base="):
            base = a.split("=", 1)[1]
        elif a.startswith("--base"):
            base = "/" + base.strip("/") + "/"

    dist = Path(args[0] if args else "docs/.vitepress/dist").resolve()
    if not dist.is_dir():
        print(f"dist directory not found: {dist}", file=sys.stderr)
        print("Run `npm run docs:build` first.", file=sys.stderr)
        sys.exit(2)

    base = "/" + base.strip("/") + "/"
    pages = sorted(dist.rglob("*.html"))
    if not pages:
        print(f"No HTML files found under {dist}", file=sys.stderr)
        sys.exit(2)

    id_cache: dict = {}
    broken: list = []
    table_problems: list = []
    external: set = set()
    checked = 0

    for page in pages:
        rel_page = page.relative_to(dist).as_posix()
        table_problems.extend(check_tables(page, rel_page))
        text = page.read_text(encoding="utf-8", errors="replace")
        for raw in ATTR_RE.findall(text):
            url = html.unescape(raw).strip()
            if not url or url.startswith("#"):
                continue
            if url.startswith(SKIP_PREFIXES):
                continue
            parsed = urlparse(url)
            if parsed.scheme in ("http", "https"):
                external.add(f"{parsed.scheme}://{parsed.netloc}")
                continue
            if parsed.scheme:
                continue

            checked += 1
            path_part = unquote(parsed.path)
            frag = unquote(parsed.fragment)

            if path_part.startswith("/"):
                if path_part.startswith(base):
                    target_rel = path_part[len(base):]
                else:
                    target_rel = path_part.lstrip("/")
                target = dist / target_rel
            else:
                # relative to the current page's directory
                target = (page.parent / path_part).resolve()

            if path_part.endswith("/") or target.is_dir():
                target = target / "index.html"

            if not target.exists():
                broken.append((rel_page, url, "target file does not exist"))
                continue

            if frag and target.suffix == ".html":
                if frag not in page_ids(target, id_cache):
                    broken.append((rel_page, url, f"anchor #{frag} not found in target"))

    print(f"Site root : {dist}")
    print(f"Base path : {base}")
    print(f"Pages     : {len(pages)}")
    print(f"Checked   : {checked} internal href/src")
    print(f"Tables    : {sum(1 for p in pages for _ in TABLE_RE.findall(p.read_text(encoding="utf-8", errors="replace")))} across {len(pages)} pages, structure verified")
    print(f"External  : {len(external)} distinct host(s) (not verified)")
    print()

    for page, why in table_problems:
        print(f"⚠️  {page}: {why}")

    if broken or table_problems:
        for page, url, why in broken:
            print(f"❌ {page}: {url}  --  {why}")
        print()
        if broken:
            print(f"❌ {len(broken)} broken internal link(s).")
        if table_problems:
            print(f"❌ {len(table_problems)} malformed table(s).")
        sys.exit(1)

    print("✅ No broken internal links in the built site.")
    sys.exit(0)


if __name__ == "__main__":
    main()
