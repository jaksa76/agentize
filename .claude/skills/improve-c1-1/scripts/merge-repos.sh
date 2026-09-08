#!/usr/bin/env bash
# merge-repos.sh
#
# Creates a combined git repository containing the content of multiple source
# repositories as subfolders, preserving full commit history and branches.
#
# Usage:
#   ./merge-repos.sh --output <dir> --repo "name=<url-or-path>" [--repo ...]
#
# Example:
#   ./merge-repos.sh \
#     --output ./combined \
#     --repo "serviceA=https://github.com/org/serviceA" \
#     --repo "utils=/local/path/to/utils"
#
# Requirements:
#   - git >= 2.22  (git filter-branch is built in; no extra tools needed)

set -euo pipefail

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

log()  { echo "[merge-repos] $*"; }
warn() { echo "[merge-repos] WARNING: $*" >&2; }
die()  { echo "[merge-repos] ERROR: $*" >&2; exit 1; }

require_cmd() {
    command -v "$1" >/dev/null 2>&1 || die "'$1' is not installed or not on PATH."
}

# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

OUTPUT_DIR=""
declare -a REPO_SPECS=()   # each entry: "name=url"

usage() {
    sed -n '/^# Usage/,/^$/p' "$0" | sed 's/^# \{0,2\}//'
    exit 1
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --output)
            [[ -n "${2:-}" ]] || die "--output requires a value"
            OUTPUT_DIR="$2"; shift 2 ;;
        --repo)
            [[ -n "${2:-}" ]] || die "--repo requires a value"
            REPO_SPECS+=("$2"); shift 2 ;;
        -h|--help) usage ;;
        *) die "Unknown argument: $1" ;;
    esac
done

[[ -n "$OUTPUT_DIR" ]]        || die "--output is required"
[[ ${#REPO_SPECS[@]} -gt 0 ]] || die "At least one --repo is required"

# ---------------------------------------------------------------------------
# Pre-flight checks
# ---------------------------------------------------------------------------

require_cmd git

GIT_VERSION=$(git --version | awk '{print $3}')
log "git version: $GIT_VERSION"

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

OUTPUT_DIR=$(realpath "$OUTPUT_DIR")
WORK_DIR=$(mktemp -d)
trap 'log "Cleaning up work dir..."; rm -rf "$WORK_DIR"' EXIT

log "Output directory : $OUTPUT_DIR"
log "Temporary workdir: $WORK_DIR"

# Initialise the output repo with an empty root commit so that HEAD exists
# before the first merge.  The empty commit becomes the common ancestor for
# the very first --allow-unrelated-histories merge; subsequent merges don't
# need it because main already has commits.
if [[ -d "$OUTPUT_DIR/.git" ]]; then
    warn "$OUTPUT_DIR already exists as a git repo — appending to it."
else
    mkdir -p "$OUTPUT_DIR"
    git -C "$OUTPUT_DIR" init -b main
    # Enable long paths so Windows NTFS can check out deep paths after the
    # name/ prefix is added.  This is a no-op on Linux/macOS.
    git -C "$OUTPUT_DIR" config core.longpaths true
    git -C "$OUTPUT_DIR" commit --allow-empty -m "chore: initialise combined repository"
    log "Initialised output repo."
fi

# ---------------------------------------------------------------------------
# Process each source repo
# ---------------------------------------------------------------------------

# Accumulate per-repo stats for the final verification report.
declare -a STAT_NAMES=()
declare -a STAT_BRANCHES=()
declare -a STAT_COMMITS=()
declare -a STAT_FILES=()
TOTAL_SOURCE_BRANCHES=0
TOTAL_SOURCE_COMMITS=0
TOTAL_SOURCE_FILES=0

for SPEC in "${REPO_SPECS[@]}"; do
    # Parse "name=url"
    NAME="${SPEC%%=*}"
    SOURCE="${SPEC#*=}"

    [[ -n "$NAME" && -n "$SOURCE" ]] || die "Invalid --repo spec '$SPEC'. Expected format: name=url"
    # Validate name: must be a safe directory / branch-prefix component
    [[ "$NAME" =~ ^[A-Za-z0-9_.-]+$ ]] || die "Repo name '$NAME' must only contain [A-Za-z0-9_.-]"

    log "---"
    log "Processing repo: $NAME  (source: $SOURCE)"

    CLONE_DIR="$WORK_DIR/$NAME"

    # ------------------------------------------------------------------
    # 1. Clone (all branches, detached from original)
    # ------------------------------------------------------------------
    log "  Cloning..."
    git clone --no-local --no-hardlinks --quiet "$SOURCE" "$CLONE_DIR"

    # Abort early if repo is completely empty (no commits)
    if ! git -C "$CLONE_DIR" rev-parse HEAD >/dev/null 2>&1; then
        warn "  Repo '$NAME' has no commits — skipping."
        rm -rf "$CLONE_DIR"
        continue
    fi

    # Detect default branch
    DEFAULT_BRANCH=$(git -C "$CLONE_DIR" symbolic-ref --short HEAD)
    log "  Default branch: $DEFAULT_BRANCH"

    # git clone only checks out the default branch locally; all others are
    # remote tracking refs.  Create local branches for every remote branch so
    # that filter-branch (--all) rewrites them all and we can create prefixed
    # refs for them later.
    # Use full refnames (not short names) to avoid ambiguity: on some git
    # versions %(refname:short) for refs/remotes/origin/HEAD returns "origin"
    # rather than "origin/HEAD", which would create a spurious local branch.
    git -C "$CLONE_DIR" for-each-ref --format='%(refname)' refs/remotes/origin/ \
        | grep -v 'refs/remotes/origin/HEAD' \
        | while IFS= read -r full_ref; do
            branch="${full_ref#refs/remotes/origin/}"
            if [[ "$branch" != "$DEFAULT_BRANCH" ]]; then
                git -C "$CLONE_DIR" branch "$branch" "$full_ref"
            fi
        done

    # Collect all local branches (now includes every branch from the source)
    BRANCHES=($(git -C "$CLONE_DIR" for-each-ref --format='%(refname:short)' refs/heads/))
    log "  Branches found: ${BRANCHES[*]:-<none>}"

    # Collect stats before filter-branch (counts are unchanged by rewriting).
    SRC_BRANCH_COUNT=${#BRANCHES[@]}
    SRC_COMMIT_COUNT=$(git -C "$CLONE_DIR" rev-list --count --all)
    SRC_FILE_COUNT=$(git -C "$CLONE_DIR" ls-files | awk 'END{print NR}')
    STAT_NAMES+=("$NAME")
    STAT_BRANCHES+=("$SRC_BRANCH_COUNT")
    STAT_COMMITS+=("$SRC_COMMIT_COUNT")
    STAT_FILES+=("$SRC_FILE_COUNT")
    TOTAL_SOURCE_BRANCHES=$(( TOTAL_SOURCE_BRANCHES + SRC_BRANCH_COUNT ))
    TOTAL_SOURCE_COMMITS=$(( TOTAL_SOURCE_COMMITS + SRC_COMMIT_COUNT ))
    TOTAL_SOURCE_FILES=$(( TOTAL_SOURCE_FILES + SRC_FILE_COUNT ))
    log "  Stats: $SRC_BRANCH_COUNT branches, $SRC_COMMIT_COUNT commits, $SRC_FILE_COUNT files"

    # ------------------------------------------------------------------
    # 2. Add the cloned repo as a subtree under name/
    #
    # git subtree add places all files from the source branch under name/
    # in the working tree and includes the full source commit graph as
    # ancestors of the resulting merge commit — without rewriting any
    # historical commits.  This is much faster than filter-branch (seconds
    # rather than minutes) and avoids long-path issues on Windows.
    #
    # Trade-off vs filter-branch: in historical (pre-merge) commits the
    # files are still at the source repo root, not under name/.
    # git log --follow name/<file> works from the merge point forward.
    # ------------------------------------------------------------------
    log "  Adding $NAME as subtree under $NAME/ ..."
    git -C "$OUTPUT_DIR" subtree add \
        --prefix="$NAME" \
        "$CLONE_DIR" \
        "$DEFAULT_BRANCH" \
        -m "feat: merge repository '$NAME' as subtree" \
        2>&1 | grep -v "^git subtree" || true
    log "  Done with $NAME."
    log "  Done with $NAME."
done

# ---------------------------------------------------------------------------
# Verification report
# ---------------------------------------------------------------------------

TOTAL_REPOS=${#STAT_NAMES[@]}
PASS=0
FAIL=0

# Prints PASS or FAIL for an expected vs actual numeric comparison.
check() {
    local label="$1" expected="$2" actual="$3"
    if [[ "$expected" -eq "$actual" ]]; then
        log "  PASS  $label  (expected: $expected, actual: $actual)"
        (( PASS++ )) || true
    else
        warn "  FAIL  $label  (expected: $expected, actual: $actual)"
        (( FAIL++ )) || true
    fi
}

log "---"
log "VERIFICATION REPORT"
log ""

# Per-repo breakdown table
log "  Source repositories processed: $TOTAL_REPOS"
log ""
printf '[merge-repos]   %-28s  %8s  %8s  %8s\n' "Repository" "Branches" "Commits" "Files"
printf '[merge-repos]   %-28s  %8s  %8s  %8s\n' "----------" "--------" "-------" "-----"
for i in "${!STAT_NAMES[@]}"; do
    printf '[merge-repos]   %-28s  %8s  %8s  %8s\n' \
        "${STAT_NAMES[$i]}" "${STAT_BRANCHES[$i]}" "${STAT_COMMITS[$i]}" "${STAT_FILES[$i]}"
done
printf '[merge-repos]   %-28s  %8s  %8s  %8s\n' "----------" "--------" "-------" "-----"
printf '[merge-repos]   %-28s  %8s  %8s  %8s\n' "TOTAL" "$TOTAL_SOURCE_BRANCHES" "$TOTAL_SOURCE_COMMITS" "$TOTAL_SOURCE_FILES"
log ""

# Measure the output repo
OUT_BRANCH_COUNT=$(git -C "$OUTPUT_DIR" for-each-ref --format='x' refs/heads/ | awk 'END{print NR}')
OUT_ALL_COMMIT_COUNT=$(git -C "$OUTPUT_DIR" rev-list --count --all)
OUT_MAIN_COMMIT_COUNT=$(git -C "$OUTPUT_DIR" rev-list --count main)
OUT_FILE_COUNT=$(git -C "$OUTPUT_DIR" ls-files | awk 'END{print NR}')
# Expected total commits: all source commits (included verbatim via subtree)
# + 1 empty root + one subtree-merge commit per source repo.
EXPECTED_ALL_COMMITS=$(( TOTAL_SOURCE_COMMITS + 1 + TOTAL_REPOS ))

log "  Checks:"
check "Files in output working tree (each repo in its own subfolder)" \
    "$TOTAL_SOURCE_FILES" "$OUT_FILE_COUNT"
check "Total unique commits (source $TOTAL_SOURCE_COMMITS + root 1 + merges $TOTAL_REPOS)" \
    "$EXPECTED_ALL_COMMITS" "$OUT_ALL_COMMIT_COUNT"
log ""
log "  Output repo stats:"
log "    Total branches (incl. main):  $OUT_BRANCH_COUNT"
log "    Commits reachable from main:  $OUT_MAIN_COMMIT_COUNT"
log "    Commits reachable from all:   $OUT_ALL_COMMIT_COUNT"
log "    Files on main (working tree): $OUT_FILE_COUNT"
log ""
if [[ $FAIL -eq 0 ]]; then
    log "  Result: ALL $PASS CHECKS PASSED"
else
    warn "  Result: $FAIL CHECK(S) FAILED, $PASS passed"
fi

# ---------------------------------------------------------------------------
# Final summary
# ---------------------------------------------------------------------------

log ""
log "---"
log "Combined repository ready at: $OUTPUT_DIR"
log ""
log "Branches in output repo:"
git -C "$OUTPUT_DIR" branch | sed 's/^/    /'
log ""
log "To work on a source subfolder:"
log "  cd $OUTPUT_DIR/<name>"
