#!/bin/bash
#
# Thalos Prime Repository Bootstrap Script
#
# This script bootstraps a new Thalos Prime project clone with all
# necessary dependencies, configurations, and validations.
#
# Usage: ./bootstrap.sh
#

set -e  # Exit on error
set -u  # Exit on undefined variable

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Script configuration
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

log_info "Thalos Prime Repository Bootstrap"
log_info "Project root: $PROJECT_ROOT"
echo ""

# Step 1: Validate repository structure
log_info "Step 1: Validating repository structure..."

required_dirs=(
    "src/python/thalos_agent_session"
    "src/nodejs"
    "src/cli"
    "tests/python"
    "tests/nodejs"
    "scripts"
    "docs"
    "examples"
)

for dir in "${required_dirs[@]}"; do
    if [ -d "$PROJECT_ROOT/$dir" ]; then
        log_success "  ✓ $dir exists"
    else
        log_warning "  ✗ $dir missing (will be created)"
        mkdir -p "$PROJECT_ROOT/$dir"
    fi
done

# Step 2: Check for required tools
log_info "Step 2: Checking required tools..."

check_command() {
    if command -v "$1" &> /dev/null; then
        log_success "  ✓ $1 found: $(command -v $1)"
        return 0
    else
        log_error "  ✗ $1 not found"
        return 1
    fi
}

required_tools=("python3" "node" "npm" "git")
missing_tools=()

for tool in "${required_tools[@]}"; do
    if ! check_command "$tool"; then
        missing_tools+=("$tool")
    fi
done

if [ ${#missing_tools[@]} -ne 0 ]; then
    log_error "Missing required tools: ${missing_tools[*]}"
    log_error "Please install missing tools and try again."
    exit 1
fi

# Step 3: Set up Python environment
log_info "Step 3: Setting up Python environment..."

cd "$PROJECT_ROOT"

if [ ! -d "venv" ]; then
    log_info "  Creating virtual environment..."
    python3 -m venv venv
    log_success "  ✓ Virtual environment created"
else
    log_success "  ✓ Virtual environment already exists"
fi

log_info "  Activating virtual environment..."
source venv/bin/activate

log_info "  Installing Python dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
log_success "  ✓ Python dependencies installed"

# Step 4: Set up Node.js environment
log_info "Step 4: Setting up Node.js environment..."

if [ -f "package.json" ]; then
    log_info "  Installing Node.js dependencies..."
    npm install > /dev/null 2>&1
    log_success "  ✓ Node.js dependencies installed"
else
    log_warning "  package.json not found, skipping Node.js setup"
fi

# Step 5: Validate deterministic subsystem structure
log_info "Step 5: Validating deterministic subsystem structure..."

check_python_module() {
    local module=$1
    if [ -f "$PROJECT_ROOT/src/python/thalos_agent_session/$module.py" ]; then
        log_success "  ✓ Module $module exists"
        return 0
    else
        log_error "  ✗ Module $module missing"
        return 1
    fi
}

required_modules=("session" "manager" "persistence" "cis_integration" "memory_subsystem" "code_generation")
missing_modules=()

for module in "${required_modules[@]}"; do
    if ! check_python_module "$module"; then
        missing_modules+=("$module")
    fi
done

if [ ${#missing_modules[@]} -ne 0 ]; then
    log_warning "Some modules are missing: ${missing_modules[*]}"
fi

# Step 6: Make CLI executable
log_info "Step 6: Setting up CLI..."

if [ -f "$PROJECT_ROOT/src/cli/thalos" ]; then
    chmod +x "$PROJECT_ROOT/src/cli/thalos"
    log_success "  ✓ CLI made executable"
    
    # Add to PATH (optional)
    if [[ ":$PATH:" != *":$PROJECT_ROOT/src/cli:"* ]]; then
        log_info "  To use 'thalos' command globally, add to your PATH:"
        echo "    export PATH=\$PATH:$PROJECT_ROOT/src/cli"
    fi
else
    log_warning "  CLI script not found"
fi

# Step 7: Run basic validation tests
log_info "Step 7: Running validation tests..."

if [ -d "$PROJECT_ROOT/tests/python" ]; then
    log_info "  Running Python tests..."
    if python -m pytest tests/python/ -v --tb=short > /tmp/test_output.log 2>&1; then
        log_success "  ✓ Python tests passed"
    else
        log_warning "  ✗ Some Python tests failed (see /tmp/test_output.log)"
    fi
else
    log_warning "  Python tests directory not found"
fi

# Step 8: Create necessary directories
log_info "Step 8: Creating runtime directories..."

runtime_dirs=(
    "session_data"
    "logs"
    ".thalos_cache"
)

for dir in "${runtime_dirs[@]}"; do
    if [ ! -d "$PROJECT_ROOT/$dir" ]; then
        mkdir -p "$PROJECT_ROOT/$dir"
        log_success "  ✓ Created $dir"
    fi
done

# Step 9: Display summary
echo ""
log_success "========================================="
log_success "Bootstrap Complete!"
log_success "========================================="
echo ""
log_info "Next steps:"
echo "  1. Activate Python virtual environment: source venv/bin/activate"
echo "  2. Run tests: pytest tests/python/"
echo "  3. Start using Thalos CLI: src/cli/thalos --help"
echo ""
log_info "Documentation: docs/README.md"
log_info "Examples: examples/"
echo ""

# Return success
exit 0
