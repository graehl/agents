#!/usr/bin/env bash
# Regenerable fetch/extract for surveys/llm-intelligence related work.
#
# Reads papers.yaml and, for each entry with an `arxiv:` or `url:` field,
# builds a durable full-text extract under ./extract/<key>/, keyed by the
# citation key. Deliberately NOT the `short` handle: a short is added when a
# paper earns a concept page, which is usually after its extract exists, and
# keying on it would move the directory out from under the completion sentinel
# -- silently re-downloading every already-fetched paper and orphaning the
# extract path each concepts/<short>.md records. The key never changes; the
# short names the concept page, not the extract.
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
#   ./fetch.sh              # build every extract not yet completed
#   ./fetch.sh KEY ...      # only the named papers.yaml keys
#   ./fetch.sh --audit      # reconcile papers.yaml state against ./extract;
#                           # exits 1 on drift, so it also works as a check
#   NO_HTML=1 ./fetch.sh    # skip the arXiv HTML view; go straight to PDF+marker
#   KEYS_ONLY=1 ./fetch.sh  # download raw sources only, skip marker extraction
#   REFETCH=1 ./fetch.sh K  # re-fetch even a completed target (rebuild)
#
# Idempotent by completion sentinel: a target counts as done only once its
# extract SUCCEEDS, recorded as extract/<name>/.fetched. Re-running skips
# completed targets — so you can add papers to papers.yaml and fetch only the
# new ones — but RETRIES a partial/failed one: a PDF whose marker run crashed
# leaves source.pdf and no .fetched, so the next run tries again (reusing the
# already-downloaded PDF). Guarding on the sentinel, not on the dir's mere
# existence, is what keeps a cached failure from masquerading as done.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p extract

have() { command -v "$1" >/dev/null 2>&1; }

# Completion sentinel: written ONLY when an extract actually succeeded, so a
# partial/crashed run is retried rather than cached as done. Line: method + src.
mark_fetched() { printf '%s\t%s\n' "$2" "$3" > "extract/$1/.fetched"; }
# true when the extract dir holds extracted content (markdown or a saved page).
has_content() { [ -n "$(find "extract/$1" \( -name '*.md' -o -name '*.html' \) -print -quit 2>/dev/null)" ]; }

# crude papers.yaml reader: emit "key<US>kind<US>ident" rows, where <US> is the
# 0x1f unit separator. A non-whitespace separator is deliberate: `read` with a
# tab IFS collapses an empty field and shifts every column left, which once
# silently mis-parsed every entry but one. Keep 0x1f even now that no field is
# optional, since `ident` is arbitrary URL text.
rows() {
  awk '
    /^[[:space:]]*-[[:space:]]*key:[[:space:]]*/ { key=$0; sub(/.*key:[[:space:]]*/,"",key); gsub(/["\r]/,"",key) }
    /^[[:space:]]*arxiv:[[:space:]]*/ { v=$0; sub(/.*arxiv:[[:space:]]*/,"",v); sub(/[[:space:]]+#.*$/,"",v); gsub(/["\r]/,"",v); sub(/[[:space:]]+$/,"",v); printf "%s\037arxiv\037%s\n", key, v }
    /^[[:space:]]*url:[[:space:]]*/   { v=$0; sub(/.*url:[[:space:]]*/,"",v);   sub(/[[:space:]]+#.*$/,"",v); gsub(/["\r]/,"",v); sub(/[[:space:]]+$/,"",v); printf "%s\037url\037%s\n",   key, v }
  ' papers.yaml
}

# Same crude reader, for the state fields the audit reconciles. `has` is 1 when
# the entry carries an arxiv:/url: (i.e. rows() can regenerate it) and `src` is
# its `source:` provenance when it has one.
audit_rows() {
  awk '
    function val(line, name,   v) {
      v = line; sub(".*" name ":[[:space:]]*", "", v)
      sub(/[[:space:]]*#.*$/, "", v); gsub(/["\r]/, "", v)
      sub(/[[:space:]]+$/, "", v); return v
    }
    function flush() {
      if (key != "") printf "%s\037%s\037%s\037%s\037%s\037%s\n", key, g, v, f, has, src
    }
    /^[[:space:]]*-[[:space:]]*key:[[:space:]]*/ {
      flush(); key=val($0,"key"); g=""; v=""; f=""; has=0; src=""
    }
    /^[[:space:]]*grounded:[[:space:]]*/ { g=val($0,"grounded") }
    /^[[:space:]]*verified:[[:space:]]*/  { v=val($0,"verified") }
    /^[[:space:]]*fetched:[[:space:]]*/   { f=val($0,"fetched") }
    /^[[:space:]]*source:[[:space:]]*/    { src=val($0,"source") }
    /^[[:space:]]*(arxiv|url):[[:space:]]*/ { has=1 }
    END { flush() }
  ' papers.yaml
}

# Reconcile the manifest's declared state against the extract tree, so that
# staying honest is a command rather than a standing manual chore. Four rules,
# each a claim the manifest header makes that disk can confirm or refute:
#
#   grounded    <-> the completion sentinel exists. Drifts both ways in
#                   practice: a paper fetched but never marked, and a paper
#                   marked but never actually extracted.
#   fetched     -> a date whenever the sentinel exists.
#   verified    -> for a grounded paper, fetching its own source settles its
#                   own citation, so grounded-but-unverified is a contradiction.
#                   Verified WITHOUT grounded is fine and common: a citation
#                   checked against the anchor's fetched bibliography needs no
#                   extract of its own — but it must then say so in `source:`,
#                   which is what separates it from pretrained recall.
#   regenerable -> an extract on disk whose entry has no arxiv:/url: cannot be
#                   rebuilt from this repo, which is the one promise the
#                   git-ignored extract tree makes.
audit() {
  local drift=0
  local key grounded verified fetched has_ident source sentinel
  while IFS=$'\x1f' read -r -u 3 key grounded verified fetched has_ident source; do
    [ -z "$key" ] && continue
    sentinel="extract/$key/.fetched"
    if [ -e "$sentinel" ]; then
      if [ "$grounded" != true ]; then
        echo "DRIFT $key: extract fetched, but grounded: ${grounded:-<unset>}"; drift=1
      fi
      if [ -z "$fetched" ] || [ "$fetched" = null ]; then
        echo "DRIFT $key: extract fetched, but fetched: ${fetched:-<unset>}"; drift=1
      fi
      if [ "$verified" != true ]; then
        echo "DRIFT $key: own source fetched, but verified: ${verified:-<unset>}"; drift=1
      fi
    elif [ "$grounded" = true ]; then
      echo "DRIFT $key: grounded: true, but no $sentinel"; drift=1
    fi
    if [ -d "extract/$key" ] && [ "$has_ident" != 1 ]; then
      echo "DRIFT $key: extract on disk, but no arxiv:/url: to regenerate it"; drift=1
    fi
    if [ "$verified" = true ] && [ "$grounded" != true ] && [ -z "$source" ]; then
      echo "DRIFT $key: verified without its own extract needs source:"; drift=1
    fi
  done 3< <(audit_rows)
  if [ "$drift" = 0 ]; then
    echo "audit: papers.yaml agrees with ./extract"
    return 0
  fi
  echo "audit: reconcile papers.yaml with disk (or re-run ./fetch.sh)" >&2
  return 1
}

if [ "${1:-}" = --audit ]; then
  audit || exit 1
  exit 0
fi

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
  local key="$1" kind="$2" ident="$3"
  local name="$key"
  [ "${#WANT[@]}" -gt 0 ] && [ -z "${WANT[$key]:-}" ] && return 0
  [ -z "${REFETCH:-}" ] && [ -e "extract/$name/.fetched" ] && { echo "SKIP $name (already fetched)"; return 0; }
  case "$kind" in
    arxiv)
      if [ -z "${NO_HTML:-}" ]; then
        echo "HTML $name arxiv:$ident (html view)"
        if save_page "extract/$name" "https://arxiv.org/html/$ident" "$name"; then
          mark_fetched "$name" arxiv-html "$ident"
          echo "  -> extract/$name (arXiv HTML view)"; return 0
        fi
        echo "  arXiv HTML view unavailable; falling back to PDF+marker"
      fi
      mkdir -p "extract/$name"; local pdf="extract/$name/source.pdf"
      # keep the PDF across retries so a re-run after a marker crash re-uses it
      [ -e "$pdf" ] || { echo "GET  $name arxiv:$ident (pdf)"; curl -fsSL "https://arxiv.org/pdf/$ident" -o "$pdf"; }
      [ -n "${KEYS_ONLY:-}" ] && return 0   # raw download only; no sentinel -> a later run extracts
      if have marker_single; then
        echo "MARK $name"
        marker_single "$pdf" --output_dir extract.tmp >/dev/null || true   # tolerate a marker crash (e.g. CUDA OOM)
        # marker writes extract.tmp/<stem>/ with <stem>.md + extracted images.
        # Copy the WHOLE dir so images are preserved; normalize the .md name.
        local sub; sub=$(find extract.tmp -mindepth 1 -maxdepth 1 -type d -print -quit 2>/dev/null || true)
        if [ -n "$sub" ]; then
          cp -r "$sub"/. "extract/$name/"
          local md; md=$(find "extract/$name" -maxdepth 1 -name '*.md' -print -quit || true)
          [ -n "$md" ] && [ "$md" != "extract/$name/$name.md" ] && mv "$md" "extract/$name/$name.md"
        fi
        rm -rf extract.tmp
        if has_content "$name"; then mark_fetched "$name" pdf-marker "$ident"
        else echo "WARN $name: marker produced no markdown (kept source.pdf; will retry next run)"; fi
      else
        echo "WARN marker_single not on PATH; kept $pdf unextracted (see AGENTS.user.md)"
      fi ;;
    url)
      echo "GET  $name url:$ident"
      save_page "extract/$name" "$ident" "$name" || { echo "WARN fetch failed $name (no sentinel; will retry)"; return 0; }
      # best-effort markdown from the raw-HTML fallback filename; the
      # self-contained wget capture is the primary artifact either way.
      have pandoc && [ -e "extract/$name/$name.html" ] && \
        pandoc -f html -t gfm "extract/$name/$name.html" -o "extract/$name/$name.md" 2>/dev/null || true
      mark_fetched "$name" url-html "$ident" ;;
  esac
}

# Read rows on FD 3 (not a pipe into the loop) so the loop runs in the main
# shell; fetch_one's stdin is /dev/null so a child (wget/curl/marker) can't
# read from the terminal. IFS is the 0x1f unit separator emitted by rows().
while IFS=$'\x1f' read -r -u 3 key kind ident; do
  [ -z "$key" ] && continue
  fetch_one "$key" "$kind" "$ident" </dev/null || echo "WARN error on $key"
done 3< <(rows)
echo "done. extracts in ./extract/<key>/ (rg-able); mark papers.yaml grounded/verified"
echo "as you confirm, then ./fetch.sh --audit to check the manifest against disk."
