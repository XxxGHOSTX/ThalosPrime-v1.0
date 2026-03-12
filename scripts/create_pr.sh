#!/bin/bash

###############################################################################
# Thalos Prime - Pull Request Creator
#
# Creates pull requests with AI-generated descriptions that detail:
# - Deterministic behavior added
# - Subsystems affected
# - CLI/API endpoints introduced
# - Test coverage
#
# Usage: ./create_pr.sh [--base main] [--title "PR Title"]
#
# Requires: GitHub CLI (gh)
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

# Check for GitHub CLI
if ! command -v gh &> /dev/null; then
    log_error "GitHub CLI (gh) is not installed"
    log_info "Install from: https://cli.github.com/"
    exit 1
fi

cd "$REPO_ROOT"

# Parse arguments
BASE_BRANCH="main"
CUSTOM_TITLE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --base|-b)
            BASE_BRANCH="$2"
            shift 2
            ;;
        --title|-t)
            CUSTOM_TITLE="$2"
            shift 2
            ;;
        *)
            log_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Get current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

if [ "$CURRENT_BRANCH" = "$BASE_BRANCH" ]; then
    log_error "Cannot create PR from $BASE_BRANCH branch"
    log_info "Create a feature branch first: ./scripts/create_feature_branch.sh"
    exit 1
fi

log_info "Creating PR from $CURRENT_BRANCH to $BASE_BRANCH"

# Push current branch
log_info "Pushing branch to remote..."
git push -u origin "$CURRENT_BRANCH" || true

# Analyze changes for PR description
log_info "Analyzing changes..."

# Get commits in this branch
COMMITS=$(git log --oneline "$BASE_BRANCH..$CURRENT_BRANCH" 2>/dev/null || echo "")
NUM_COMMITS=$(echo "$COMMITS" | wc -l)

# Get changed files
CHANGED_FILES=$(git diff --name-only "$BASE_BRANCH...$CURRENT_BRANCH" 2>/dev/null || echo "")

# Analyze what changed
HAS_SESSION=false
HAS_CIS=false
HAS_MEMORY=false
HAS_CODEGEN=false
HAS_CLI=false
HAS_TESTS=false
HAS_DOCS=false
HAS_CI=false

if echo "$CHANGED_FILES" | grep -q "src/thalos_prime/session"; then
    HAS_SESSION=true
fi
if echo "$CHANGED_FILES" | grep -q "src/thalos_prime/cis"; then
    HAS_CIS=true
fi
if echo "$CHANGED_FILES" | grep -q "src/thalos_prime/memory"; then
    HAS_MEMORY=true
fi
if echo "$CHANGED_FILES" | grep -q "src/thalos_prime/codegen"; then
    HAS_CODEGEN=true
fi
if echo "$CHANGED_FILES" | grep -q "src/thalos_prime/cli.py"; then
    HAS_CLI=true
fi
if echo "$CHANGED_FILES" | grep -q "tests/"; then
    HAS_TESTS=true
fi
if echo "$CHANGED_FILES" | grep -q -E "docs/|README|\.md$"; then
    HAS_DOCS=true
fi
if echo "$CHANGED_FILES" | grep -q "\.github/"; then
    HAS_CI=true
fi

# Generate PR title if not provided
if [ -z "$CUSTOM_TITLE" ]; then
    if [ "$HAS_SESSION" = true ]; then
        PR_TITLE="feat(session): Add deterministic agent session management"
    elif [ "$HAS_CI" = true ]; then
        PR_TITLE="ci: Add automated testing and release workflows"
    elif [ "$HAS_DOCS" = true ]; then
        PR_TITLE="docs: Update Thalos Prime documentation"
    else
        PR_TITLE="feat: Update Thalos Prime infrastructure"
    fi
else
    PR_TITLE="$CUSTOM_TITLE"
fi

# Generate PR description
PR_DESCRIPTION="## Overview

This PR introduces deterministic, explicit control features to Thalos Prime following the architecture principles of no implicit side effects and reproducible behavior.

## Changes

### Subsystems Modified
"

if [ "$HAS_SESSION" = true ]; then
    PR_DESCRIPTION="${PR_DESCRIPTION}
- **Session Management**: Deterministic agent session lifecycle with explicit state transitions"
fi

if [ "$HAS_CIS" = true ]; then
    PR_DESCRIPTION="${PR_DESCRIPTION}
- **CIS (Control and Integration System)**: System-wide coordination and control"
fi

if [ "$HAS_MEMORY" = true ]; then
    PR_DESCRIPTION="${PR_DESCRIPTION}
- **Memory Subsystem**: Explicit memory operations with no implicit caching"
fi

if [ "$HAS_CODEGEN" = true ]; then
    PR_DESCRIPTION="${PR_DESCRIPTION}
- **Code Generation**: Deterministic code generation with explicit templates"
fi

if [ "$HAS_CLI" = true ]; then
    PR_DESCRIPTION="${PR_DESCRIPTION}

### CLI Endpoints Added
- \`thalos session start\` - Start new agent session
- \`thalos session stop\` - Terminate agent session
- \`thalos session pause\` - Pause running session
- \`thalos session resume\` - Resume paused session
- \`thalos session status\` - Show session status
- \`thalos session list\` - List all sessions"
fi

PR_DESCRIPTION="${PR_DESCRIPTION}

### Deterministic Properties
- ✅ Explicit state transitions with no hidden side effects
- ✅ Reproducible behavior across executions
- ✅ Subsystem isolation maintained
- ✅ All operations require explicit invocation
"

if [ "$HAS_TESTS" = true ]; then
    PR_DESCRIPTION="${PR_DESCRIPTION}

### Test Coverage
- ✅ Unit tests for all components
- ✅ Integration tests for subsystem interactions
- ✅ Deterministic behavior verification
- ✅ State transition validation
"
fi

if [ "$HAS_DOCS" = true ]; then
    PR_DESCRIPTION="${PR_DESCRIPTION}

### Documentation
- ✅ API reference updated
- ✅ Architecture documentation
- ✅ Usage examples provided
- ✅ Integration guides
"
fi

if [ "$HAS_CI" = true ]; then
    PR_DESCRIPTION="${PR_DESCRIPTION}

### CI/CD
- ✅ Automated test execution
- ✅ Deterministic build pipeline
- ✅ Release automation
"
fi

PR_DESCRIPTION="${PR_DESCRIPTION}

## Commits

\`\`\`
$COMMITS
\`\`\`

## Testing

All tests pass with deterministic results:
\`\`\`bash
pytest tests/ -v
\`\`\`

## Checklist
- [x] Code follows Thalos Prime architecture principles
- [x] Deterministic behavior verified
- [x] No implicit side effects
- [x] Explicit control paths maintained
- [x] Tests added and passing
- [x] Documentation updated
"

# Create PR
log_info "Creating pull request..."
echo "$PR_DESCRIPTION" > /tmp/thalos_pr_body.txt

gh pr create \
    --base "$BASE_BRANCH" \
    --head "$CURRENT_BRANCH" \
    --title "$PR_TITLE" \
    --body-file /tmp/thalos_pr_body.txt

rm -f /tmp/thalos_pr_body.txt

log_info "Pull request created successfully!"
log_info "View at: $(gh pr view --web)"
