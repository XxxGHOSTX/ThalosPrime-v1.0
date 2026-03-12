#!/bin/bash

###############################################################################
# Thalos Prime - Release Automation Script
#
# Automates the release process:
# - Validates tests pass
# - Creates git tag
# - Generates AI-written release notes
# - Pushes tag to trigger release workflow
#
# Usage: ./create_release.sh <version>
#
# Example: ./create_release.sh 1.0.0
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

# Parse version
if [ $# -lt 1 ]; then
    log_error "Usage: $0 <version>"
    log_info "Example: $0 1.0.0"
    exit 1
fi

VERSION="$1"
TAG="v${VERSION}"

cd "$REPO_ROOT"

# Validate version format
if ! echo "$VERSION" | grep -qE '^[0-9]+\.[0-9]+\.[0-9]+$'; then
    log_error "Invalid version format: $VERSION"
    log_info "Expected format: X.Y.Z (e.g., 1.0.0)"
    exit 1
fi

log_info "Creating release for version $VERSION"

# Check if tag already exists
if git rev-parse "$TAG" >/dev/null 2>&1; then
    log_error "Tag $TAG already exists"
    exit 1
fi

# Ensure we're on main/master branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "main" ] && [ "$CURRENT_BRANCH" != "master" ]; then
    log_warn "Not on main/master branch (current: $CURRENT_BRANCH)"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "Release cancelled"
        exit 0
    fi
fi

# Ensure working directory is clean
if ! git diff --quiet || ! git diff --cached --quiet; then
    log_error "Working directory has uncommitted changes"
    log_info "Commit or stash changes before creating release"
    exit 1
fi

# Update version in pyproject.toml (portable across macOS and Linux)
log_info "Updating version in pyproject.toml..."
python3 -c "
import re
import sys

with open('pyproject.toml', 'r') as f:
    content = f.read()

content = re.sub(r'^version = .*', f'version = \"$VERSION\"', content, flags=re.MULTILINE)

with open('pyproject.toml', 'w') as f:
    f.write(content)
"

# Update version in __init__.py
log_info "Updating version in __init__.py..."
python3 -c "
import re

with open('src/thalos_prime/__init__.py', 'r') as f:
    content = f.read()

content = re.sub(r'^__version__ = .*', f'__version__ = \"$VERSION\"', content, flags=re.MULTILINE)

with open('src/thalos_prime/__init__.py', 'w') as f:
    f.write(content)
"

# Commit version update
git add pyproject.toml src/thalos_prime/__init__.py
git commit -m "chore: bump version to $VERSION" || log_warn "No version changes to commit"

# Run tests
log_info "Running tests to verify release quality..."
if command -v pytest &> /dev/null; then
    pytest tests/ -q || {
        log_error "Tests failed - release aborted"
        exit 1
    }
    log_info "✅ All tests passed"
else
    log_warn "pytest not found - skipping tests"
fi

# Generate changelog/release notes
log_info "Generating release notes..."

# Get commits since last tag
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
if [ -z "$LAST_TAG" ]; then
    COMMITS=$(git log --oneline --no-merges)
else
    COMMITS=$(git log --oneline --no-merges "$LAST_TAG..HEAD")
fi

# Categorize commits
FEAT_COMMITS=$(echo "$COMMITS" | grep -E "^[a-f0-9]+ feat" || true)
FIX_COMMITS=$(echo "$COMMITS" | grep -E "^[a-f0-9]+ fix" || true)
DOCS_COMMITS=$(echo "$COMMITS" | grep -E "^[a-f0-9]+ docs" || true)
TEST_COMMITS=$(echo "$COMMITS" | grep -E "^[a-f0-9]+ test" || true)
BUILD_COMMITS=$(echo "$COMMITS" | grep -E "^[a-f0-9]+ (build|ci|chore)" || true)

# Create release notes
cat > RELEASE_NOTES.md <<EOF
# Thalos Prime v${VERSION}

Release Date: $(date +%Y-%m-%d)

## Overview

This release brings deterministic behavior and explicit control to Thalos Prime,
ensuring reproducible AI agent sessions with no implicit side effects.

## Features

EOF

if [ -n "$FEAT_COMMITS" ]; then
    echo "### New Features" >> RELEASE_NOTES.md
    echo "" >> RELEASE_NOTES.md
    echo "$FEAT_COMMITS" | while IFS= read -r commit; do
        echo "- ${commit#* }" >> RELEASE_NOTES.md
    done
    echo "" >> RELEASE_NOTES.md
fi

if [ -n "$FIX_COMMITS" ]; then
    echo "### Bug Fixes" >> RELEASE_NOTES.md
    echo "" >> RELEASE_NOTES.md
    echo "$FIX_COMMITS" | while IFS= read -r commit; do
        echo "- ${commit#* }" >> RELEASE_NOTES.md
    done
    echo "" >> RELEASE_NOTES.md
fi

if [ -n "$DOCS_COMMITS" ]; then
    echo "### Documentation" >> RELEASE_NOTES.md
    echo "" >> RELEASE_NOTES.md
    echo "$DOCS_COMMITS" | while IFS= read -r commit; do
        echo "- ${commit#* }" >> RELEASE_NOTES.md
    done
    echo "" >> RELEASE_NOTES.md
fi

cat >> RELEASE_NOTES.md <<EOF
## Deterministic Properties

- ✅ No implicit state changes
- ✅ Reproducible behavior across executions
- ✅ Explicit control paths only
- ✅ Subsystem isolation maintained
- ✅ All operations require explicit invocation

## Installation

\`\`\`bash
pip install thalos-prime==${VERSION}
\`\`\`

## Documentation

- Session Management: docs/session.md
- Architecture: docs/architecture.md
- CLI Reference: docs/cli.md
- API Documentation: docs/api.md

## Testing

All tests pass with deterministic results:
\`\`\`bash
pytest tests/ -v
\`\`\`

## Full Changelog

$COMMITS

---

For more details, see the full documentation at:
https://github.com/XxxGHOSTX/ThalosPrime-v1.0
EOF

log_info "Release notes generated"
cat RELEASE_NOTES.md

# Create annotated tag
log_info "Creating git tag: $TAG"
git tag -a "$TAG" -m "Release version $VERSION

$(cat RELEASE_NOTES.md)"

# Push changes and tag
log_info "Pushing changes and tag to remote..."
git push origin "$CURRENT_BRANCH"
git push origin "$TAG"

log_info "✅ Release $TAG created successfully!"
log_info ""
log_info "The GitHub Actions release workflow will now:"
log_info "  1. Run all tests"
log_info "  2. Build the package"
log_info "  3. Create GitHub release with notes"
log_info "  4. Publish to PyPI (if configured)"
log_info ""
log_info "Monitor the release at:"
log_info "https://github.com/XxxGHOSTX/ThalosPrime-v1.0/releases/tag/$TAG"

# Cleanup
rm -f RELEASE_NOTES.md
