#!/usr/bin/env bash
# Build .claude/doc-map.md by scanning .md files in canonical directories.
#
# Output: $REPO_ROOT/.claude/doc-map.md
# Trigger: SessionStart hook (matchers: startup, resume, compact). The map is
# always regenerated fresh so it never rots.
#
# Skipped (already auto-loaded by Claude Code or noisy):
#   - CLAUDE.md, MEMORY.md (auto-loaded)
#   - .git/, node_modules/, vendor/, brand/.git/

set -euo pipefail

# Resolve repo root from script location.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd -P)"
cd "$REPO_ROOT"

OUT=".claude/doc-map.md"
mkdir -p "$(dirname "$OUT")"

# Directories to scan (top-level, walked recursively).
DIRS=(brand docs email scripts)

# Repo-root .md files to include (skip auto-loaded ones).
ROOT_FILES=()
for f in *.md; do
  case "$f" in
    CLAUDE.md|MEMORY.md) ;;
    *) [ -f "$f" ] && ROOT_FILES+=("$f") ;;
  esac
done

# Pull purpose: first non-empty paragraph after any YAML frontmatter,
# excluding heading lines. Truncate long lines for the map.
extract_purpose() {
  awk '
    BEGIN { in_fm=0; printed=0 }
    NR==1 && /^---[[:space:]]*$/ { in_fm=1; next }
    in_fm && /^---[[:space:]]*$/ { in_fm=0; next }
    in_fm { next }
    !printed && /^[^#[:space:]]/ {
      line=$0
      if (length(line) > 200) line=substr(line,1,197) "..."
      print line
      printed=1
      exit
    }
  ' "$1"
}

# Pull H2 headings only. H3+ would bloat the map.
extract_headings() {
  grep -E '^## ' "$1" 2>/dev/null | sed 's/^## //' || true
}

# Emit one file's entry to the map.
emit_file() {
  local f="$1"
  printf '### `%s`\n' "$f"
  local purpose
  purpose=$(extract_purpose "$f")
  if [ -n "$purpose" ]; then
    printf '%s\n' "$purpose"
  fi
  local headings
  headings=$(extract_headings "$f")
  if [ -n "$headings" ]; then
    printf '\n'
    while IFS= read -r heading; do
      [ -n "$heading" ] && printf -- '- %s\n' "$heading"
    done <<< "$headings"
  fi
  printf '\n'
}

# Header.
{
  printf '# 40hr Farmer doc map\n\n'
  printf 'Generated %s by `scripts/build-doc-map.sh`. Refreshed by the SessionStart\n' "$(date -I)"
  printf 'hook on every startup, resume, and post-compact. Read this first to find\n'
  printf 'which file to open for a given topic. CLAUDE.md and MEMORY.md are\n'
  printf 'auto-loaded and not listed here.\n\n'
} > "$OUT"

# Repo root .md files first.
if [ ${#ROOT_FILES[@]} -gt 0 ]; then
  printf '## Repo root\n\n' >> "$OUT"
  for f in "${ROOT_FILES[@]}"; do
    emit_file "$f" >> "$OUT"
  done
fi

# Then each scanned directory.
for d in "${DIRS[@]}"; do
  if [ -d "$d" ]; then
    files=$(find "$d" \( -name '.git' -o -name 'node_modules' -o -name 'vendor' \) -prune -o \
            -type f -name '*.md' -print 2>/dev/null | sort)
    if [ -n "$files" ]; then
      printf '## %s/\n\n' "$d" >> "$OUT"
      while IFS= read -r f; do
        [ -n "$f" ] && emit_file "$f" >> "$OUT"
      done <<< "$files"
    fi
  fi
done

# Brief stats to stderr so the hook output stays clean.
lines=$(wc -l < "$OUT")
files_indexed=$(grep -c '^### ' "$OUT" || true)
echo "Doc map refreshed: $files_indexed files, $lines lines at $OUT" >&2
