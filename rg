#!/usr/bin/env bash
# Agent-safe ripgrep wrapper.
#
# Purpose:
#   - Make agent-emitted `--type tsx` work.
#   - Make old-grep muscle memory like `rg -rn PATTERN PATH` work as intended.
#   - Ban ambiguous bare `-r`, because in ripgrep it means replacement, not recursion.
#
# Policy:
#   rg -rn ...       => rg -n ...
#   rg -rln ...      => rg -l -n ...
#   rg -ri ...       => rg -i ...
#   rg -R ...        => rg -L ...        # grep -R follows symlinks; rg -L does that
#   rg -r ...        => blocked
#   rg -rFOO ...     => blocked
#   rg --replace ... => allowed
#
# Escape hatch:
#   Use --replace for intentional ripgrep replacement mode.
#   Or bypass this wrapper with RG_REAL=/path/to/real/rg.

set -euo pipefail

find_real_rg() {
	local self cand real d

	self="$(readlink -f "$0" 2>/dev/null || realpath "$0")"

	IFS=':' read -r -a path_dirs <<<"${PATH:-}"
	for d in "${path_dirs[@]}"; do
		[[ -z "$d" ]] && d='.'
		cand="$d/rg"
		[[ -x "$cand" ]] || continue

		real="$(readlink -f "$cand" 2>/dev/null || realpath "$cand")"
		[[ "$real" != "$self" ]] || continue

		printf '%s\n' "$cand"
		return 0
	done

	for cand in /usr/bin/rg /bin/rg /usr/local/bin/rg; do
		[[ -x "$cand" ]] || continue
		real="$(readlink -f "$cand" 2>/dev/null || realpath "$cand")"
		[[ "$real" != "$self" ]] || continue

		printf '%s\n' "$cand"
		return 0
	done

	echo "rg wrapper: could not find the real rg. Set RG_REAL=/path/to/rg." >&2
	return 127
}

REAL_RG="${RG_REAL:-$(find_real_rg)}"

die_bare_r() {
	local opt="${1:-"-r"}"

	cat >&2 <<EOF
rg wrapper: blocked '${opt}'.

In ripgrep, bare -r means --replace, not recursive search.
ripgrep searches recursively by default.

For recursive search, omit -r:
  rg -n 'pattern' path

For intentional replacement mode, reinvoke using --replace:
  rg --replace 'replacement' 'pattern' path
EOF

	exit 2
}

args=()

# Translate short-option bundles that clearly look like GNU grep muscle memory.
#
# Accepted chars here are intentionally conservative: common grep/ripgrep flags
# that agents tend to bundle with -r. Unknown bundles beginning with -r are
# blocked rather than passed through, because passing them through can trigger
# ripgrep replacement mode.
add_grepish_short_bundle() {
	local bundle="$1"
	local i ch

	for ((i = 0; i < ${#bundle}; i++)); do
		ch="${bundle:i:1}"

		case "$ch" in
		r)
			# GNU grep recursion. ripgrep is recursive by default.
			;;

		R)
			# GNU grep recursive + follow symlinks. ripgrep equivalent is -L.
			args+=("-L")
			;;

		E)
			# GNU grep extended regex. ripgrep already uses modern regex syntax.
			;;

		s)
			# GNU grep suppress error messages.
			args+=("--no-messages")
			;;

		I)
			# GNU grep ignore binary files. ripgrep already avoids binary by default.
			;;

		n | l | i | H | h | o | w | F | q | v | c | C | A | B | S | U)
			args+=("-$ch")
			;;

		*)
			return 1
			;;
		esac
	done

	return 0
}

while (($#)); do
	a="$1"
	shift

	case "$a" in
	--)
		args+=("--" "$@")
		break
		;;

	--replace | --replace=*)
		# Long-form replacement is explicit enough. Allow it.
		args+=("$a")
		;;

	-r)
		die_bare_r "$a"
		;;

	-r?*)
		# Examples:
		#   -rn    => -n
		#   -rln   => -l -n
		#   -ri    => -i
		#
		# But:
		#   -rfoo  => blocked; use --replace foo instead
		bundle="${a#-}"
		if add_grepish_short_bundle "$bundle"; then
			:
		else
			die_bare_r "$a"
		fi
		;;

	--recursive)
		# grepism; ripgrep is recursive by default.
		;;

	-R)
		# GNU grep -R follows symlinks.
		args+=("-L")
		;;

	-R?*)
		bundle="${a#-}"
		if add_grepish_short_bundle "$bundle"; then
			:
		else
			args+=("$a")
		fi
		;;

	*)
		args+=("$a")
		;;
	esac
done

exec "$REAL_RG" \
	--type-add 'tsx:*.tsx' \
	--type-add 'ts:*.tsx' \
	"${args[@]}"
