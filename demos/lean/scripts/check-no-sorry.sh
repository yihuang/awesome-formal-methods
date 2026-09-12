#!/usr/bin/env bash
# check-no-sorry.sh — the CI gate that makes proof engineering honest.
#
# Greps Lean sources for the three ways a "verified" claim can be hollow:
#   1. `sorry`   — a proof placeholder that compiles but proves nothing
#   2. `admit`   — the Rocq/Coq equivalent
#   3. `axiom`   — an assumption smuggled in to make a theorem true
#
# Block comments (including nested ones) and line comments are stripped first,
# so prose *about* `sorry` doesn't trip the gate.
#
# Exit code 0 = clean, 1 = something suspicious found.
#
# Usage:
#   ./scripts/check-no-sorry.sh            # scan this project
#   ./scripts/check-no-sorry.sh path/...   # scan a specific path

set -uo pipefail

TARGET="${1:-$(cd "$(dirname "$0")/.." && pwd)}"

if [ ! -e "$TARGET" ]; then
  echo "usage: $0 [path]" >&2
  exit 2
fi

echo "Scanning Lean sources under: $TARGET"
echo

# Strip Lean comments (nested block comments + line comments), emitting
# "file:line:code" only for lines that still contain code.
cleaned=$(find "$TARGET" -name '*.lean' -type f -print0 2>/dev/null \
  | xargs -0 -r awk '
      BEGIN { depth = 0 }
      {
        line = $0; out = ""; i = 1; n = length(line)
        while (i <= n) {
          c2 = substr(line, i, 2)
          if (depth > 0) {
            if (c2 == "-/") { depth--; i += 2; continue }
            if (c2 == "/-") { depth++; i += 2; continue }
            i++; continue
          }
          if (c2 == "/-") { depth++; i += 2; continue }
          if (c2 == "--") { break }
          out = out substr(line, i, 1); i++
        }
        if (out ~ /[^ \t\r]/) print FILENAME ":" FNR ":" out
      }')

status=0

report() {
  local pattern="$1" label="$2" hits
  hits=$(printf '%s\n' "$cleaned" | grep -E "$pattern" || true)
  if [ -n "$hits" ]; then
    echo "❌ $label"
    printf '%s\n' "$hits" | sed 's/^/     /'
    echo
    status=1
  fi
}

report '\bsorry\b'          'sorry: an unproved proof placeholder'
report '\badmit\b'          'admit: an unproved proof placeholder'
report '^[^:]*:[0-9]+:[ \t]*axiom\b' 'axiom: a smuggled assumption'

if [ "$status" -eq 0 ]; then
  echo "✅ No sorry / admit / axiom declarations found."
else
  echo "Fix the above, or explicitly allow them in a documented allowlist"
  echo "(and say why in the commit message — assumptions are load-bearing)."
fi

exit "$status"
