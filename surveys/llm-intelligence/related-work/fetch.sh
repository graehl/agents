#!/usr/bin/env bash
# Regenerable fetch/extract for surveys/llm-intelligence related work.
#
# Reads papers.yaml, downloads each paper with an `arxiv:` or `url:` field into
# ./pdf or ./html, and extracts PDFs to markdown with marker-pdf (see
# ~/agents/AGENTS.user.md "PDF -> Markdown"). Extracted markdown under ./extract
# is the rg search target for method/limitation/table sections; it and the raw
# downloads are gitignored (see .gitignore). Only papers.yaml + this script are
# committed.
#
# Usage:
#   ./fetch.sh            # fetch+extract every entry missing from ./extract
#   ./fetch.sh KEY ...    # only the named papers.yaml keys
#   KEYS_ONLY=1 ./fetch.sh  # download only, skip marker extraction
#
# Idempotent: skips a paper whose extract/ output already exists.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p pdf html extract

have() { command -v "$1" >/dev/null 2>&1; }
marker() { have marker_single; }   # provided by `uv tool install marker-pdf`

# crude but adequate papers.yaml reader: emit "key<TAB>kind<TAB>ident" rows,
# where kind is arxiv|url. one paper block is delimited by a "- key:" line.
rows() {
  awk '
    /^[[:space:]]*-[[:space:]]*key:[[:space:]]*/ { key=$0; sub(/.*key:[[:space:]]*/,"",key); gsub(/["\r]/,"",key) }
    /^[[:space:]]*arxiv:[[:space:]]*/ { v=$0; sub(/.*arxiv:[[:space:]]*/,"",v); gsub(/["\r]/,"",v); print key"\tarxiv\t"v }
    /^[[:space:]]*url:[[:space:]]*/   { v=$0; sub(/.*url:[[:space:]]*/,"",v);   gsub(/["\r]/,"",v); print key"\turl\t"v }
  ' papers.yaml
}

want_key() { [ "$#" -eq 0 ] && return 0 || return 1; }   # replaced below when args given
declare -A WANT=(); for a in "$@"; do WANT["$a"]=1; done

fetch_one() {
  local key="$1" kind="$2" ident="$3"
  [ "${#WANT[@]}" -gt 0 ] && [ -z "${WANT[$key]:-}" ] && return 0
  [ -e "extract/$key.md" ] && { echo "SKIP $key (extract exists)"; return 0; }
  case "$kind" in
    arxiv)
      local pdf="pdf/$key.pdf"
      [ -e "$pdf" ] || { echo "GET  $key arxiv:$ident"; curl -fsSL "https://arxiv.org/pdf/$ident" -o "$pdf"; }
      if [ -n "${KEYS_ONLY:-}" ]; then return 0; fi
      if marker; then
        echo "MARK $key"; marker_single "$pdf" --output_dir extract.tmp >/dev/null
        # marker writes extract.tmp/<stem>/<stem>.md; flatten to extract/$key.md
        local out; out=$(find extract.tmp -name '*.md' -print -quit || true)
        [ -n "$out" ] && cp "$out" "extract/$key.md"; rm -rf extract.tmp
      else
        echo "WARN marker_single not on PATH; left $pdf unextracted (see AGENTS.user.md)"
      fi ;;
    url)
      echo "GET  $key url:$ident"; curl -fsSL "$ident" -o "html/$key.html" || echo "WARN fetch failed $key"
      # HTML (blog / transformer-circuits / distill): keep raw; extract by hand or pandoc.
      have pandoc && pandoc -f html -t gfm "html/$key.html" -o "extract/$key.md" 2>/dev/null || true ;;
  esac
}

rows | while IFS=$'\t' read -r key kind ident; do
  [ -z "$key" ] && continue
  fetch_one "$key" "$kind" "$ident" || echo "WARN error on $key"
done
echo "done. extracted markdown in ./extract (rg-able); update papers.yaml grounded/verified as you confirm."
