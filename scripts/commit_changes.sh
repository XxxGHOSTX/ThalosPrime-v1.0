#!/bin/bash

###############################################################################
# Thalos Prime - Smart Commit Script
#
# Automatically stages changes and creates AI-generated commit messages
# that describe deterministic behavior and structural updates.
#
# Usage: ./commit_changes.sh [--message "custom message"]
#
# If no message is provided, generates one based on changes.
###############################################################################

set -e

REPO_ROOT="$(git rev-parse --show-toplevel)"
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

cd "$REPO_ROOT"

# Parse arguments
CUSTOM_MESSAGE=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --message|-m)
            CUSTOM_MESSAGE="$2"
            shift 2
            ;;
        *)
            log_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Check for changes
if git diff --quiet && git diff --cached --quiet; then
    log_warn "No changes to commit"
    exit 0
fi

# Stage all changes
log_info "Staging changes..."
git add -A

# Show what will be committed
log_info "Changes to be committed:"
git status --short

# Generate commit message if not provided
if [ -z "$CUSTOM_MESSAGE" ]; then
    log_info "Generating AI-powered commit message..."
    
    # Get changed files
    CHANGED_FILES=$(git diff --cached --name-only)
    
    # Analyze changes
    HAS_TESTS=false
    HAS_DOCS=false
    HAS_SRC=false
    HAS_CONFIG=false
    
    if echo "$CHANGED_FILES" | grep -q "tests/"; then
        HAS_TESTS=true
    fi
    if echo "$CHANGED_FILES" | grep -q -E "docs/|README|\.md$"; then
        HAS_DOCS=true
    fi
    if echo "$CHANGED_FILES" | grep -q "src/"; then
        HAS_SRC=true
    fi
    if echo "$CHANGED_FILES" | grep -q -E "\.toml$|\.yaml$|\.yml$|\.json$"; then
        HAS_CONFIG=true
    fi
    
    # Generate contextual commit message
    COMMIT_TYPE="feat"
    COMMIT_SCOPE=""
    COMMIT_SUBJECT=""
    COMMIT_BODY=""
    
    # Determine scope from directory
    if echo "$CHANGED_FILES" | grep -q "src/thalos_prime/session"; then
        COMMIT_SCOPE="session"
    elif echo "$CHANGED_FILES" | grep -q "src/thalos_prime/cis"; then
        COMMIT_SCOPE="cis"
    elif echo "$CHANGED_FILES" | grep -q "src/thalos_prime/memory"; then
        COMMIT_SCOPE="memory"
    elif echo "$CHANGED_FILES" | grep -q "src/thalos_prime/codegen"; then
        COMMIT_SCOPE="codegen"
    elif echo "$CHANGED_FILES" | grep -q "scripts/"; then
        COMMIT_SCOPE="automation"
        COMMIT_TYPE="build"
    elif echo "$CHANGED_FILES" | grep -q "\.github/"; then
        COMMIT_SCOPE="ci"
        COMMIT_TYPE="ci"
    fi
    
    # Generate subject based on changes
    if [ "$HAS_TESTS" = true ] && [ "$HAS_SRC" = true ]; then
        COMMIT_SUBJECT="implement deterministic behavior with comprehensive tests"
        COMMIT_BODY="- Add explicit control paths with no implicit side effects
- Implement deterministic state transitions
- Add unit and integration tests for reproducibility
- Ensure subsystem isolation"
    elif [ "$HAS_TESTS" = true ]; then
        COMMIT_SUBJECT="add deterministic tests for reproducibility verification"
        COMMIT_BODY="- Add comprehensive test coverage
- Validate deterministic behavior
- Ensure no implicit state changes
- Test explicit control paths"
        COMMIT_TYPE="test"
    elif [ "$HAS_DOCS" = true ]; then
        COMMIT_SUBJECT="update documentation for explicit control paths"
        COMMIT_BODY="- Document deterministic behavior
- Explain explicit control mechanisms
- Add usage examples
- Update API reference"
        COMMIT_TYPE="docs"
    elif [ "$HAS_CONFIG" = true ]; then
        COMMIT_SUBJECT="configure deterministic build and test infrastructure"
        COMMIT_BODY="- Set up deterministic build configuration
- Configure testing framework
- Define explicit dependencies
- Establish reproducible environment"
        COMMIT_TYPE="build"
    elif [ "$HAS_SRC" = true ]; then
        COMMIT_SUBJECT="implement explicit control and deterministic operations"
        COMMIT_BODY="- Add deterministic functionality
- Implement explicit state management
- Ensure no hidden side effects
- Maintain subsystem isolation"
    else
        COMMIT_SUBJECT="update Thalos Prime infrastructure"
        COMMIT_BODY="- Update project infrastructure
- Maintain deterministic behavior
- Ensure explicit control"
        COMMIT_TYPE="chore"
    fi
    
    # Build commit message
    if [ -n "$COMMIT_SCOPE" ]; then
        COMMIT_MESSAGE="${COMMIT_TYPE}(${COMMIT_SCOPE}): ${COMMIT_SUBJECT}"
    else
        COMMIT_MESSAGE="${COMMIT_TYPE}: ${COMMIT_SUBJECT}"
    fi
    
    if [ -n "$COMMIT_BODY" ]; then
        COMMIT_MESSAGE="${COMMIT_MESSAGE}

${COMMIT_BODY}"
    fi
else
    COMMIT_MESSAGE="$CUSTOM_MESSAGE"
fi

# Show commit message
log_info "Commit message:"
echo "---"
echo "$COMMIT_MESSAGE"
echo "---"
echo ""

# Confirm commit
read -p "Proceed with commit? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    log_warn "Commit cancelled"
    git reset HEAD
    exit 0
fi

# Create commit
git commit -m "$COMMIT_MESSAGE"

log_info "Commit created successfully!"
log_info "Use 'git push' to push changes to remote"
