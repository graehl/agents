#!/usr/bin/env bash
# Regenerable fetch/extract for surveys/llm-intelligence related work.
#
# Reads papers.yaml and, for each entry with an `arxiv:` or `url:` field,
# builds a durable full-text extract under ./extract/<short>/, keyed by the
# paper's `short` handle (falling back to its citation key when it has none).
# The extract is a "computed" artifact: git-ignored (see .gitignore), durable
# in the author's workdir, regenerated under the user's own access to the
# source, not redistributed. Only papers.yaml + this script are committed.
#
# The committed concepts/<short>.md understanding page is what we reason on;
# the extract is the full text it was read from and is consulted later only for
# a specific the summary omits. Analysis follows a fetch+read: build the extract
# here, read it, then write/refresh concepts/<short>.md from it.
#
# Extraction path, in preference order:
#   1. arXiv HTML view (arxiv.org/html/<id>) — text + figures in one page;
#      saved self-contained (images included) when wget is present.
#   2. PDF -> markdown via marker_single (see ~/agents/AGENTS.user.md
#      "PDF -> Markdown"); marker's extracted images are KEPT beside the .md.
#   3. url: entries (blog / transformer-circuits / Distill) — page saved
#      self-contained (images via wget) or, failing that, as raw HTML.
#
# Usage:
#   ./fetch.sh              # build every extract missing from ./extract
#   ./fetch.sh KEY ...      # only the named papers.yaml keys
#   NO_HTML=1 ./fetch.sh    # skip the arXiv HTML view; go straight to PDF+marker
#   KEYS_ONLY=1 ./fetch.sh  # download raw sources only, skip marker extraction
#
# Idempotent: skips a paper whose extract/<name>/ dir already exists.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p extract

have() { command -v "$1" >/dev/null 2>&1; }

# crude papers.yaml reader: emit "key<TAB>short<TAB>kind<TAB>ident" rows.
# `short` is "" when the entry has no short handle. A block starts at "- key:";
# reset short there so it never leaks from the previous entry.
rows() {
  awk '
    /^[[:space:]]*-[[:space:]]*key:[[:space:]]*/ { key=$0; sub(/.*key:[[:space:]]*/,"",key); gsub(/["\r]/,"",key); short="" }
    /^[[:space:]]*short:[[:space:]]*/            { short=$0; sub(/.*short:[[:space:]]*/,"",short); gsub(/["\r]/,"",short) }
    /^[[:space:]]*arxiv:[[:space:]]*/ { v=$0; sub(/.*arxiv:[[:space:]]*/,"",v); sub(/[[:space:]]+#.*$/,"",v); gsub(/["\r]/,"",v); sub(/[[:space:]]+$/,"",v); print key"\t"short"\tarxiv\t"v }
    /^[[:space:]]*url:[[:space:]]*/   { v=$0; sub(/.*url:[[:space:]]*/,"",v);   sub(/[[:space:]]+#.*$/,"",v); gsub(/["\r]/,"",v); sub(/[[:space:]]+$/,"",v); print key"\t"short"\turl\t"v }
  ' papers.yaml
}

declare -A WANT=(); for a in "$@"; do WANT["$a"]=1; done

# Save a web page into $1, self-contained (html + images) via wget when
# available, else the raw HTML via curl. Images that stay remote are still
# reconstitutable from the source URL recorded in concepts/<short>.md.
save_page() {
  local dir="$1" url="$2" stem="$3"
  mkdir -p "$dir"
  if have wget; then
    # -p page requisites, -k convert links for offline reading, -E adjust
    # extension, -nH drop host dir, robots=off so figures are fetched.
    if wget -q -e robots=off -p -k -E -nH --restrict-file-names=windows \
            -P "$dir" "$url"; then
      return 0
    fi
  fi
  curl -fsSL "$url" -o "$dir/$stem.html"
}

fetch_one() {
  local key="$1" short="$2" kind="$3" ident="$4"
  local name="${short:-$key}"
  [ "${#WANT[@]}" -gt 0 ] && [ -z "${WANT[$key]:-}" ] && return 0
  [ -d "extract/$name" ] && { echo "SKIP $name (extract/$name exists)"; return 0; }
  case "$kind" in
    arxiv)
      if [ -z "${NO_HTML:-}" ]; then
        echo "HTML $name arxiv:$ident (html view)"
        if save_page "extract/$name" "https://arxiv.org/html/$ident" "$name"; then
          echo "  -> extract/$name (arXiv HTML view)"; return 0
        fi
        echo "  arXiv HTML view unavailable; falling back to PDF+marker"
      fi
      mkdir -p "extract/$name"; local pdf="extract/$name/source.pdf"
      echo "GET  $name arxiv:$ident (pdf)"
      curl -fsSL "https://arxiv.org/pdf/$ident" -o "$pdf"
      [ -n "${KEYS_ONLY:-}" ] && return 0
      if have marker_single; then
        echo "MARK $name"
        marker_single "$pdf" --output_dir extract.tmp >/dev/null
        # marker writes extract.tmp/<stem>/ with <stem>.md + extracted images.
        # Copy the WHOLE dir so images are preserved; normalize the .md name.
        local sub; sub=$(find extract.tmp -mindepth 1 -maxdepth 1 -type d -print -quit || true)
        if [ -n "$sub" ]; then
          cp -r "$sub"/. "extract/$name/"
          local md; md=$(find "extract/$name" -maxdepth 1 -name '*.md' -print -quit || true)
          [ -n "$md" ] && [ "$md" != "extract/$name/$name.md" ] && mv "$md" "extract/$name/$name.md"
        fi
        rm -rf extract.tmp
      else
        echo "WARN marker_single not on PATH; kept $pdf unextracted (see AGENTS.user.md)"
      fi ;;
    url)
      echo "GET  $name url:$ident"
      save_page "extract/$name" "$ident" "$name" || { echo "WARN fetch failed $name"; return 0; }
      # best-effort markdown from the raw-HTML fallback filename; the
      # self-contained wget capture is the primary artifact either way.
      have pandoc && [ -e "extract/$name/$name.html" ] && \
        pandoc -f html -t gfm "extract/$name/$name.html" -o "extract/$name/$name.md" 2>/dev/null || true ;;
  esac
}

rows | while IFS=$'\t' read -r key short kind ident; do
  [ -z "$key" ] && continue
  fetch_one "$key" "$short" "$kind" "$ident" || echo "WARN error on $key"
done
echo "done. extracts in ./extract/<short>/ (rg-able); mark papers.yaml grounded/verified as you confirm."
