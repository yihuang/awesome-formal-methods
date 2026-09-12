#!/usr/bin/env python3
"""
check-links.py — verify that every relative Markdown link in this repo resolves.

Zero dependencies. Skips external URLs, mailto, and pure-anchor links.

Usage:
    python3 tools/check-links.py            # check the repo root
    python3 tools/check-links.py path/to/dir

Exit code 0 = all internal links resolve, 1 = at least one is broken.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote

# [text](target)  and  ![alt](target)
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")

SKIP_SCHEMES = ("http://", "https://", "mailto:", "tel:", "ftp://")


def slugify(heading: str) -> str:
    """Approximate GitHub's heading -> anchor slug."""
    s = heading.strip().lower()
    s = re.sub(r"`([^`]*)`", r"\1", s)          # strip inline code
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)  # strip links
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE)  # drop punctuation
    s = s.replace(" ", "-")
    return s.strip("-")


def anchors_of(path: Path) -> set:
    """Collect heading anchors from a Markdown file, with GitHub-style dedup."""
    anchors: set = set()
    seen: dict = {}
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return anchors
    in_fence = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if not m:
            continue
        slug = slugify(m.group(2))
        seen[slug] = seen.get(slug, 0) + 1
        anchors.add(slug if seen[slug] == 1 else f"{slug}-{seen[slug] - 1}")
    return anchors


def find_markdown(root: Path) -> list:
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in {".git", "node_modules", ".lake"}]
        for fn in filenames:
            if fn.endswith(".md"):
                out.append(Path(dirpath) / fn)
    return sorted(out)


def check(root: Path) -> int:
    files = find_markdown(root)
    if not files:
        print(f"No Markdown files found under {root}")
        return 0

    anchor_cache: dict = {}
    broken: list = []
    checked = 0

    for md in files:
        text = md.read_text(encoding="utf-8", errors="replace")
        for lineno, line in enumerate(text.splitlines(), start=1):
            for target in LINK_RE.findall(line):
                if target.startswith(SKIP_SCHEMES) or target.startswith("#"):
                    if target.startswith("#"):
                        checked += 1
                        frag = unquote(target[1:])
                        if md not in anchor_cache:
                            anchor_cache[md] = anchors_of(md)
                        if frag and frag not in anchor_cache[md]:
                            broken.append((md, lineno, target, "anchor not found in file"))
                    continue
                if "://" in target:
                    continue
                checked += 1

                path_part, _, frag = target.partition("#")
                path_part = unquote(path_part)
                resolved = (md.parent / path_part).resolve() if path_part else md

                if not resolved.exists():
                    broken.append((md, lineno, target, "path does not exist"))
                    continue

                if frag and resolved.suffix == ".md":
                    if resolved not in anchor_cache:
                        anchor_cache[resolved] = anchors_of(resolved)
                    if frag not in anchor_cache[resolved]:
                        broken.append((md, lineno, target, "anchor not found in target"))

    rel_root = root
    for md, lineno, target, why in broken:
        try:
            shown = md.relative_to(rel_root)
        except ValueError:
            shown = md
        print(f"❌ {shown}:{lineno}: {target}  --  {why}")

    print()
    print(f"Scanned {len(files)} Markdown files, checked {checked} internal links.")
    if broken:
        print(f"❌ {len(broken)} broken link(s).")
        return 1
    print("✅ All internal links resolve.")
    return 0


def main() -> None:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    if not root.is_dir():
        print(f"Not a directory: {root}", file=sys.stderr)
        sys.exit(2)
    print(f"Checking internal links under: {root}\n")
    sys.exit(check(root))


if __name__ == "__main__":
    main()
