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
