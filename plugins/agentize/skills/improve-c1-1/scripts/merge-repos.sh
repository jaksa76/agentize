#!/usr/bin/env bash
# merge-repos.sh
#
# Creates a combined git repository containing the content of multiple source
# repositories as subfolders, preserving full commit history and every branch.
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
# How branches are combined:
#   - History of each source repo is rewritten so that its files live under
#     <name>/ in every commit (git filter-repo --to-subdirectory-filter).
#   - Every branch name found in any source repo becomes one branch in the
#     output.  Its tip is a merge commit whose parents are that branch from
#     each source repo, so e.g. the combined `develop` contains the commits
#     of every source `develop`.
#   - A repo that lacks the branch contributes the branch it would have been
#     created from (gitflow): feature/*, bugfix/* and release/* fall back to
#     `develop`, hotfix/* and support/* to `master` (or `main`), and anything
#     else, or a missing fallback, to the repo's default branch.
#   - Source tags are NOT turned into tags.  They are stored as
#     refs/imported-tags/<name>/<tag> (pointing at the rewritten commits) so
#     the caller can decide how to merge them, then delete that namespace.
#   - Uncommitted work, stashes and reflogs of the sources are not carried over.
#
# This is a one-time migration: the output directory must not exist yet.
#
# Requirements:
#   - git >= 2.22
#   - git-filter-repo  (pip install git-filter-repo)

set -euo pipefail

# Gitflow conventions used to pick the fallback branch.
DEVELOP_BRANCH="develop"
DEVELOP_CHILD_PATTERN='^(feature|bugfix|release)/'
PRODUCTION_BRANCHES="master main"
PRODUCTION_CHILD_PATTERN='^(hotfix|support)/'

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
REPO_SPECS=()   # each entry: "name=url"

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
git filter-repo --version >/dev/null 2>&1 \
    || die "git-filter-repo is not installed. Install it with: pip install git-filter-repo"

GIT_VERSION=$(git --version | awk '{print $3}')
log "git version: $GIT_VERSION"

OUTPUT_DIR=$(realpath "$OUTPUT_DIR")
if [[ -e "$OUTPUT_DIR" ]] && [[ -n "$(ls -A "$OUTPUT_DIR")" ]]; then
    die "$OUTPUT_DIR already exists and is not empty. This is a one-time migration; choose a new directory."
fi

WORK_DIR=$(mktemp -d)
trap 'log "Cleaning up work dir..."; rm -rf "$WORK_DIR"' EXIT

log "Output directory : $OUTPUT_DIR"
log "Temporary workdir: $WORK_DIR"

EMPTY_TREE=$(git hash-object -t tree /dev/null)

# ---------------------------------------------------------------------------
# 1. Clone and rewrite each source repo
# ---------------------------------------------------------------------------

# Per-repo data, indexed in parallel (no associative arrays, for bash 3.2).
NAMES=()
DEFAULTS=()
STAT_BRANCHES=()
STAT_COMMITS=()
STAT_TAGS=()
TOTAL_SOURCE_COMMITS=0

for SPEC in "${REPO_SPECS[@]}"; do
    # Parse "name=url"
    NAME="${SPEC%%=*}"
    SOURCE="${SPEC#*=}"

    [[ -n "$NAME" && -n "$SOURCE" && "$SPEC" == *=* ]] || die "Invalid --repo spec '$SPEC'. Expected format: name=url"
    # Validate name: must be a safe directory / ref component
    [[ "$NAME" =~ ^[A-Za-z0-9_][A-Za-z0-9_.-]*$ ]] || die "Repo name '$NAME' must only contain [A-Za-z0-9_.-] and not start with '.' or '-'"
    for EXISTING in ${NAMES[@]+"${NAMES[@]}"}; do
        [[ "$EXISTING" != "$NAME" ]] || die "Repo name '$NAME' is used more than once"
    done

    log "---"
    log "Processing repo: $NAME  (source: $SOURCE)"

    CLONE_DIR="$WORK_DIR/$NAME.git"

    # A bare clone maps every source branch to refs/heads/* directly.
    log "  Cloning..."
    git clone --bare --no-local --quiet "$SOURCE" "$CLONE_DIR"

    # When the source is a local working copy, branches that only exist as
    # remote-tracking refs there (never checked out) must be imported too.
    if [[ -d "$SOURCE" ]] && git -C "$SOURCE" rev-parse --git-dir >/dev/null 2>&1; then
        while IFS= read -r full_ref; do
            branch="${full_ref#refs/remotes/origin/}"
            [[ "$branch" != "HEAD" ]] || continue
            if ! git -C "$CLONE_DIR" show-ref --verify --quiet "refs/heads/$branch"; then
                git -C "$CLONE_DIR" fetch --quiet --no-tags "$SOURCE" "$full_ref:refs/heads/$branch"
            fi
        done < <(git -C "$SOURCE" for-each-ref --format='%(refname)' refs/remotes/origin/)
    fi

    if [[ -z "$(git -C "$CLONE_DIR" for-each-ref --count=1 refs/heads/)" ]]; then
        warn "  Repo '$NAME' has no branches — skipping."
        rm -rf "$CLONE_DIR"
        continue
    fi

    # Detect default branch (fall back to any branch if HEAD is dangling)
    DEFAULT_BRANCH=$(git -C "$CLONE_DIR" symbolic-ref --short HEAD)
    if ! git -C "$CLONE_DIR" show-ref --verify --quiet "refs/heads/$DEFAULT_BRANCH"; then
        DEFAULT_BRANCH=$(git -C "$CLONE_DIR" for-each-ref --count=1 --format='%(refname:short)' refs/heads/)
        warn "  HEAD points to a missing branch; using '$DEFAULT_BRANCH' as default."
    fi
    log "  Default branch: $DEFAULT_BRANCH"

    # Record the original tree of every branch; verification compares the
    # <name>/ folder of each output branch against these.
    git -C "$CLONE_DIR" for-each-ref --format='%(refname:short) %(objectname)' refs/heads/ \
        | while read -r branch commit; do
            echo "$branch $(git -C "$CLONE_DIR" rev-parse "$commit^{tree}")"
        done > "$WORK_DIR/$NAME.trees"

    SRC_BRANCH_COUNT=$(awk 'END{print NR}' "$WORK_DIR/$NAME.trees")
    SRC_COMMIT_COUNT=$(git -C "$CLONE_DIR" rev-list --count --branches)
    SRC_TAG_COUNT=$(git -C "$CLONE_DIR" for-each-ref --format='x' refs/tags/ | awk 'END{print NR}')
    log "  Stats: $SRC_BRANCH_COUNT branches, $SRC_COMMIT_COUNT commits, $SRC_TAG_COUNT tags"

    # Rewrite history so every commit has its files under <name>/.  Commits
    # shared between branches map to the same rewritten commit, so combined
    # branches keep proper merge bases.
    log "  Rewriting history under $NAME/ ..."
    git -C "$CLONE_DIR" filter-repo --force --quiet \
        --to-subdirectory-filter "$NAME" \
        --replace-refs delete-no-add

    NAMES+=("$NAME")
    DEFAULTS+=("$DEFAULT_BRANCH")
    STAT_BRANCHES+=("$SRC_BRANCH_COUNT")
    STAT_COMMITS+=("$SRC_COMMIT_COUNT")
    STAT_TAGS+=("$SRC_TAG_COUNT")
    TOTAL_SOURCE_COMMITS=$(( TOTAL_SOURCE_COMMITS + SRC_COMMIT_COUNT ))
    log "  Done with $NAME."
done

[[ ${#NAMES[@]} -gt 0 ]] || die "No source repository had any branches."

# ---------------------------------------------------------------------------
# 2. Create the output repo and import the rewritten refs
# ---------------------------------------------------------------------------

# The combined default branch is the sources' default if they all agree.
COMBINED_DEFAULT="${DEFAULTS[0]}"
for d in "${DEFAULTS[@]}"; do
    if [[ "$d" != "$COMBINED_DEFAULT" ]]; then
        warn "Source repos have different default branches (${DEFAULTS[*]}); using '$COMBINED_DEFAULT'."
        break
    fi
done

log "---"
mkdir -p "$OUTPUT_DIR"
git -C "$OUTPUT_DIR" init --quiet -b "$COMBINED_DEFAULT"
# Enable long paths so Windows NTFS can check out deep paths after the
# name/ prefix is added.  This is a no-op on Linux/macOS.
git -C "$OUTPUT_DIR" config core.longpaths true
log "Initialised output repo (default branch: $COMBINED_DEFAULT)."

for NAME in "${NAMES[@]}"; do
    log "Importing rewritten refs of $NAME ..."
    git -C "$OUTPUT_DIR" fetch --quiet --no-tags "$WORK_DIR/$NAME.git" \
        "+refs/heads/*:refs/sources/$NAME/*" \
        "+refs/tags/*:refs/imported-tags/$NAME/*"
done

# ---------------------------------------------------------------------------
# 3. Build one combined branch per branch name
# ---------------------------------------------------------------------------

# Prints the branch of repo $1 that the combined branch $2 should contain.
pick_branch() {
    local name="$1" branch="$2" default="$3" candidates candidate
    if [[ "$branch" =~ $DEVELOP_CHILD_PATTERN ]]; then
        candidates="$branch $DEVELOP_BRANCH"
    elif [[ "$branch" =~ $PRODUCTION_CHILD_PATTERN ]]; then
        candidates="$branch $PRODUCTION_BRANCHES"
    else
        candidates="$branch"
    fi
    for candidate in $candidates; do
        if git -C "$OUTPUT_DIR" show-ref --verify --quiet "refs/sources/$name/$candidate"; then
            echo "$candidate"
            return
        fi
    done
    echo "$default"
}

for NAME in "${NAMES[@]}"; do
    awk '{print $1}' "$WORK_DIR/$NAME.trees"
done | sort -u > "$WORK_DIR/all-branches"

ALL_BRANCH_COUNT=$(awk 'END{print NR}' "$WORK_DIR/all-branches")
MERGES_CREATED=0
log "---"
log "Building $ALL_BRANCH_COUNT combined branches..."

# Records "branch name source-branch" for every output branch and repo.
: > "$WORK_DIR/composition"

while IFS= read -r BRANCH; do
    PARENT_ARGS=()
    TREE_INPUT=""
    MESSAGE="Combine branch '$BRANCH' from source repositories"$'\n'
    for i in "${!NAMES[@]}"; do
        NAME="${NAMES[$i]}"
        SRC_BRANCH=$(pick_branch "$NAME" "$BRANCH" "${DEFAULTS[$i]}")
        COMMIT=$(git -C "$OUTPUT_DIR" rev-parse "refs/sources/$NAME/$SRC_BRANCH")
        PARENT_ARGS+=(-p "$COMMIT")
        # A source commit with an empty tree has no <name>/ folder.
        if SUBTREE=$(git -C "$OUTPUT_DIR" rev-parse --verify --quiet "$COMMIT:$NAME"); then
            TREE_INPUT+=$(printf '040000 tree %s\t%s' "$SUBTREE" "$NAME")$'\n'
        fi
        MESSAGE+=$'\n'"- $NAME: $SRC_BRANCH"
        echo "$BRANCH $NAME $SRC_BRANCH" >> "$WORK_DIR/composition"
    done

    if [[ ${#NAMES[@]} -eq 1 ]]; then
        TIP="${PARENT_ARGS[1]}"
    else
        TREE=$(printf '%s' "$TREE_INPUT" | git -C "$OUTPUT_DIR" mktree)
        TIP=$(printf '%s\n' "$MESSAGE" | git -C "$OUTPUT_DIR" commit-tree "$TREE" "${PARENT_ARGS[@]}")
        MERGES_CREATED=$(( MERGES_CREATED + 1 ))
    fi
    git -C "$OUTPUT_DIR" update-ref "refs/heads/$BRANCH" "$TIP"
done < "$WORK_DIR/all-branches"

# The per-repo source refs are no longer needed.
git -C "$OUTPUT_DIR" for-each-ref --format='delete %(refname)' refs/sources/ \
    | git -C "$OUTPUT_DIR" update-ref --stdin

git -C "$OUTPUT_DIR" checkout --quiet -f "$COMBINED_DEFAULT"

# ---------------------------------------------------------------------------
# Verification report
# ---------------------------------------------------------------------------

PASS=0
FAIL=0

# Prints PASS or FAIL for an expected vs actual comparison.
check() {
    local label="$1" expected="$2" actual="$3"
    if [[ "$expected" == "$actual" ]]; then
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
log "  Source repositories processed: ${#NAMES[@]}"
log ""
printf '[merge-repos]   %-28s  %-12s  %8s  %8s  %6s\n' "Repository" "Default" "Branches" "Commits" "Tags"
printf '[merge-repos]   %-28s  %-12s  %8s  %8s  %6s\n' "----------" "-------" "--------" "-------" "----"
for i in "${!NAMES[@]}"; do
    printf '[merge-repos]   %-28s  %-12s  %8s  %8s  %6s\n' \
        "${NAMES[$i]}" "${DEFAULTS[$i]}" "${STAT_BRANCHES[$i]}" "${STAT_COMMITS[$i]}" "${STAT_TAGS[$i]}"
done
log ""

# Every output branch must have, under each <name>/, exactly the tree of the
# source branch it was built from.
MISMATCHES=0
while read -r BRANCH NAME SRC_BRANCH; do
    EXPECTED=$(awk -v b="$SRC_BRANCH" '$1==b{print $2}' "$WORK_DIR/$NAME.trees")
    ACTUAL=$(git -C "$OUTPUT_DIR" rev-parse --verify --quiet "refs/heads/$BRANCH:$NAME" || echo "$EMPTY_TREE")
    if [[ "$EXPECTED" != "$ACTUAL" ]]; then
        warn "  $BRANCH: $NAME/ does not match $NAME's '$SRC_BRANCH'"
        MISMATCHES=$(( MISMATCHES + 1 ))
    fi
done < "$WORK_DIR/composition"

OUT_BRANCH_COUNT=$(git -C "$OUTPUT_DIR" for-each-ref --format='x' refs/heads/ | awk 'END{print NR}')
OUT_BRANCH_COMMIT_COUNT=$(git -C "$OUTPUT_DIR" rev-list --count --branches)
OUT_TAG_COUNT=$(git -C "$OUTPUT_DIR" for-each-ref --format='x' refs/imported-tags/ | awk 'END{print NR}')
SOURCE_TAG_COUNT=0
for t in "${STAT_TAGS[@]}"; do SOURCE_TAG_COUNT=$(( SOURCE_TAG_COUNT + t )); done
# Expected commits on branches: every source commit reachable from a branch
# (rewritten one-to-one) + one combining commit per output branch.
EXPECTED_COMMITS=$(( TOTAL_SOURCE_COMMITS + MERGES_CREATED ))

log "  Checks:"
check "Branches (union of source branch names)" "$ALL_BRANCH_COUNT" "$OUT_BRANCH_COUNT"
check "Commits on branches (source $TOTAL_SOURCE_COMMITS + combining $MERGES_CREATED)" \
    "$EXPECTED_COMMITS" "$OUT_BRANCH_COMMIT_COUNT"
check "Repo folders matching their source branch tree" "0 mismatches" "$MISMATCHES mismatches"
check "Imported tags under refs/imported-tags/" "$SOURCE_TAG_COUNT" "$OUT_TAG_COUNT"
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
log "Branch composition (branch: repo=source-branch ...):"
awk '{a[$1]=a[$1] " " $2 "=" $3} END{for (b in a) print "    " b ":" a[b]}' "$WORK_DIR/composition" | sort
log ""
if [[ $OUT_TAG_COUNT -gt 0 ]]; then
    log "Source tags are stored as refs/imported-tags/<name>/<tag> and are not yet tags."
    log "Merge or recreate them, then delete that namespace."
fi

[[ $FAIL -eq 0 ]]
