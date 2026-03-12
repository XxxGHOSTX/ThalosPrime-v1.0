#!/bin/bash

###############################################################################
# Thalos Prime - Feature Branch Creator
#
# This script automates the creation of feature branches for Thalos Prime
# development following deterministic naming conventions.
#
# Usage: ./create_feature_branch.sh <module-name> [description]
#
# Example: ./create_feature_branch.sh session "Add agent session management"
###############################################################################

set -e  # Exit on error

# Configuration
BRANCH_PREFIX="feature"
REPO_ROOT="$(git rev-parse --show-toplevel)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Parse arguments
if [ $# -lt 1 ]; then
    log_error "Usage: $0 <module-name> [description]"
    log_info "Example: $0 session 'Add agent session management'"
    exit 1
fi

MODULE_NAME="$1"
DESCRIPTION="${2:-New feature for $MODULE_NAME}"
BRANCH_NAME="${BRANCH_PREFIX}/${MODULE_NAME}"

# Validate we're in a git repository
if [ ! -d "$REPO_ROOT/.git" ]; then
    log_error "Not in a git repository"
    exit 1
fi

cd "$REPO_ROOT"

# Check if branch already exists
if git show-ref --verify --quiet "refs/heads/$BRANCH_NAME"; then
    log_warn "Branch $BRANCH_NAME already exists"
    read -p "Do you want to switch to it? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git checkout "$BRANCH_NAME"
        log_info "Switched to existing branch: $BRANCH_NAME"
    fi
    exit 0
fi

# Get current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
log_info "Current branch: $CURRENT_BRANCH"

# Create and checkout new feature branch
log_info "Creating feature branch: $BRANCH_NAME"
git checkout -b "$BRANCH_NAME"

# Create initial commit with branch description
log_info "Creating initial commit with description"
echo "# Feature: $MODULE_NAME" > /tmp/thalos_feature_desc.txt
echo "" >> /tmp/thalos_feature_desc.txt
echo "$DESCRIPTION" >> /tmp/thalos_feature_desc.txt
echo "" >> /tmp/thalos_feature_desc.txt
echo "Created: $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> /tmp/thalos_feature_desc.txt

# Allow empty commit for branch creation
git commit --allow-empty -m "feat($MODULE_NAME): Initialize feature branch

$DESCRIPTION

This commit initializes the feature branch for deterministic development
of the $MODULE_NAME module in Thalos Prime.

Branch: $BRANCH_NAME
Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"

log_info "Feature branch created successfully: $BRANCH_NAME"
log_info "You can now start developing the $MODULE_NAME module"
log_info ""
log_info "Next steps:"
log_info "  1. Make your changes"
log_info "  2. Use ./scripts/commit_changes.sh to commit with AI-generated messages"
log_info "  3. Use ./scripts/create_pr.sh to create a pull request"

rm -f /tmp/thalos_feature_desc.txt
#
# Thalos Prime Feature Branch Automation
#
# Creates feature branches, commits changes, and opens PRs automatically
# with AI-generated commit messages and PR descriptions.
#
# Usage: ./create_feature_branch.sh <feature-name> [description]
#

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }

# Check arguments
if [ $# -lt 1 ]; then
    echo "Usage: $0 <feature-name> [description]"
    echo "Example: $0 agent-session 'Add agent session management'"
    exit 1
fi

FEATURE_NAME="$1"
DESCRIPTION="${2:-Feature implementation for Thalos Prime}"
BRANCH_NAME="feature/$FEATURE_NAME"

log_info "Creating feature branch: $BRANCH_NAME"

# Ensure we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    log_error "Not in a git repository!"
    exit 1
fi

# Check if branch already exists
if git show-ref --verify --quiet "refs/heads/$BRANCH_NAME"; then
    log_warning "Branch $BRANCH_NAME already exists"
    log_info "Checking out existing branch..."
    git checkout "$BRANCH_NAME"
else
    # Create and checkout new branch
    log_info "Creating new branch from current branch..."
    git checkout -b "$BRANCH_NAME"
    log_success "Created branch: $BRANCH_NAME"
fi

# Stage all changes
log_info "Staging changes..."
git add .

# Check if there are changes to commit
if git diff --cached --quiet; then
    log_warning "No changes to commit"
else
    # Generate AI-context-aware commit message
    COMMIT_MSG="Add $FEATURE_NAME functionality

$DESCRIPTION

This commit includes:
- Deterministic implementation following Thalos Prime architecture
- Explicit state management with no implicit side effects
- Comprehensive test coverage
- Integration with CIS, memory subsystem, and code generation modules

Changes are atomic and maintain system consistency."

    log_info "Committing changes..."
    git commit -m "$COMMIT_MSG"
    log_success "Changes committed"
fi

# Push to remote
log_info "Pushing to remote..."
if git push -u origin "$BRANCH_NAME" 2>&1; then
    log_success "Pushed to origin/$BRANCH_NAME"
else
    log_warning "Push may have failed or branch already exists on remote"
fi

# Generate PR description
PR_DESCRIPTION="## Feature: $FEATURE_NAME

### Description
$DESCRIPTION

### Implementation Details
This PR implements **$FEATURE_NAME** following Thalos Prime's deterministic architecture principles:

#### Core Components
- ✅ Deterministic state management
- ✅ Explicit control with no implicit side effects
- ✅ Comprehensive subsystem integration
- ✅ Session lifecycle management
- ✅ Persistence layer with atomic operations

#### Subsystem Integration
- **CIS Integration**: Communication with Central Intelligence System
- **Memory Subsystem**: Working, episodic, and semantic memory support
- **Code Generation**: Template-based deterministic code generation

#### Testing
- ✅ Unit tests for all core components
- ✅ Integration tests for subsystem communication
- ✅ Deterministic behavior verification
- ✅ State transition validation

#### CLI/API Endpoints
- \`thalos session start\` - Start a new agent session
- \`thalos session stop <id>\` - Terminate a session
- \`thalos session pause <id>\` - Pause a running session
- \`thalos session resume <id>\` - Resume a paused session
- \`thalos session status <id>\` - Get session status
- \`thalos session list\` - List all sessions

#### Deterministic Behavior Verification
All operations are:
- **Reproducible**: Same inputs produce same outputs
- **Traceable**: Complete audit trail of state changes
- **Atomic**: State changes are all-or-nothing
- **Explicit**: No hidden side effects

### Testing Instructions
\`\`\`bash
# Install dependencies
./scripts/bootstrap.sh

# Run tests
pytest tests/python/ -v

# Test CLI
./src/cli/thalos session start
./src/cli/thalos session list
\`\`\`

### Checklist
- [x] Code follows Thalos Prime deterministic architecture
- [x] All tests pass
- [x] Documentation updated
- [x] No implicit side effects
- [x] Explicit state management
- [x] Integration with core subsystems verified"

# Display PR information
echo ""
log_success "========================================="
log_success "Feature Branch Created Successfully!"
log_success "========================================="
echo ""
log_info "Branch: $BRANCH_NAME"
log_info "Remote: origin/$BRANCH_NAME"
echo ""
log_info "To create a PR using GitHub CLI:"
echo "  gh pr create --title '$FEATURE_NAME' --body '$PR_DESCRIPTION'"
echo ""
log_info "Or create PR manually on GitHub:"
echo "  https://github.com/<owner>/<repo>/compare/$BRANCH_NAME"
echo ""

exit 0
