#!/bin/bash

###############################################################################
# Thalos Prime - Installation and Verification Script
#
# This script sets up and verifies the Thalos Prime environment for production
# deployment, ensuring all components are functional.
#
# Usage: ./setup_verify.sh [--dev]
#
# Options:
#   --dev    Install development dependencies
###############################################################################

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[!]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

log_section() {
    echo -e "\n${BLUE}==>${NC} $1"
}

# Check if dev mode
DEV_MODE=false
if [[ "$1" == "--dev" ]]; then
    DEV_MODE=true
    log_info "Development mode enabled"
fi

# Print header
cat << 'EOF'
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║              THALOS PRIME v1.0 - SETUP & VERIFICATION               ║
║                                                                      ║
║           Deterministic AI Agent Session Management                 ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
EOF

# Check Python version
log_section "Checking Python version"
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
log_info "Python version: $PYTHON_VERSION"

if python -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    log_info "Python version is compatible (>= 3.8)"
else
    log_error "Python 3.8 or higher required"
    exit 1
fi

# Install package
log_section "Installing Thalos Prime"
if [ "$DEV_MODE" = true ]; then
    log_info "Installing in development mode with dev dependencies..."
    pip install -e ".[dev]" --quiet
else
    log_info "Installing in production mode..."
    pip install -e . --quiet
fi
log_info "Installation complete"

# Verify installation
log_section "Verifying installation"
if python -c "import thalos_prime; print(f'Thalos Prime v{thalos_prime.__version__}')"; then
    log_info "Package import successful"
else
    log_error "Failed to import package"
    exit 1
fi

# Test CLI
log_section "Testing CLI interface"
if thalos --version > /dev/null 2>&1; then
    VERSION=$(thalos --version)
    log_info "CLI available: $VERSION"
else
    log_error "CLI not available"
    exit 1
fi

# Test session commands
log_info "Testing session commands..."
if thalos session --help > /dev/null 2>&1; then
    log_info "Session commands available"
else
    log_error "Session commands not available"
    exit 1
fi

# Run tests if dev mode
if [ "$DEV_MODE" = true ]; then
    log_section "Running test suite"
    if pytest tests/ -q --tb=short; then
        log_info "All tests passed"
    else
        log_error "Some tests failed"
        exit 1
    fi
fi

# Test example script
log_section "Testing example scripts"
if python examples/basic_session.py > /dev/null 2>&1; then
    log_info "Example scripts working"
else
    log_warn "Example scripts had issues (non-critical)"
fi

# Check scripts are executable
log_section "Verifying automation scripts"
SCRIPT_DIR="scripts"
if [ -d "$SCRIPT_DIR" ]; then
    for script in "$SCRIPT_DIR"/*.sh; do
        if [ -x "$script" ]; then
            log_info "$(basename $script) is executable"
        else
            log_warn "$(basename $script) is not executable - fixing..."
            chmod +x "$script"
            log_info "Fixed permissions for $(basename $script)"
        fi
    done
else
    log_warn "Scripts directory not found"
fi

# Create necessary directories
log_section "Creating required directories"
mkdir -p .thalos/sessions
log_info "Created .thalos/sessions directory"

mkdir -p logs
log_info "Created logs directory"

# Verify documentation
log_section "Verifying documentation"
DOCS=("README.md" "CONTRIBUTING.md" "CODE_OF_CONDUCT.md" "SECURITY.md" "CHANGELOG.md")
for doc in "${DOCS[@]}"; do
    if [ -f "$doc" ]; then
        log_info "$doc present"
    else
        log_warn "$doc missing"
    fi
done

# Check workflows
log_section "Verifying CI/CD workflows"
if [ -d ".github/workflows" ]; then
    WORKFLOW_COUNT=$(find .github/workflows -name "*.yml" -o -name "*.yaml" | wc -l)
    log_info "Found $WORKFLOW_COUNT CI/CD workflow(s)"
else
    log_warn "No CI/CD workflows found"
fi

# Final summary
log_section "Setup Summary"
cat << EOF

✅ Thalos Prime v1.0 is fully configured and operational!

Next steps:
  1. Start a session:     thalos session start --name "my-agent"
  2. Check status:        thalos session status --all
  3. Run examples:        python examples/basic_session.py
  4. Read documentation:  cat README.md
  5. Run tests:           make test

For development:
  • Format code:          make format
  • Run linters:          make lint
  • Type checking:        make type-check
  • Full CI checks:       make ci

For automation:
  • Create feature:       ./scripts/create_feature_branch.sh <name>
  • Scaffold module:      ./scripts/scaffold_module.sh <name> <type>
  • Smart commit:         ./scripts/commit_changes.sh
  • Create PR:            ./scripts/create_pr.sh

Documentation:
  • Session Management:   docs/session.md
  • DevOps Automation:    docs/automation.md
  • API Reference:        docs/api.md

EOF

log_info "Setup and verification complete!"
log_info "Thalos Prime is ready for production use"

exit 0
