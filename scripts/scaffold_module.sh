#!/bin/bash

###############################################################################
# Thalos Prime - Module Scaffolder
#
# Automatically scaffolds new deterministic subsystem modules with:
# - Python module files with deterministic templates
# - Test files (unit and integration)
# - CLI integration hooks
# - Documentation stubs
#
# Usage: ./scaffold_module.sh <module-name> <module-type>
#
# Module types: subsystem, integration, utility
#
# Example: ./scaffold_module.sh analytics subsystem
###############################################################################

set -e

# Configuration
REPO_ROOT="$(git rev-parse --show-toplevel)"
SRC_DIR="$REPO_ROOT/src/thalos_prime"
TEST_DIR="$REPO_ROOT/tests"
DOCS_DIR="$REPO_ROOT/docs"

# Colors
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

# Parse arguments
if [ $# -lt 2 ]; then
    log_error "Usage: $0 <module-name> <module-type>"
    log_info "Module types: subsystem, integration, utility"
    log_info "Example: $0 analytics subsystem"
    exit 1
fi

MODULE_NAME="$1"
MODULE_TYPE="$2"

# Validate module type
case "$MODULE_TYPE" in
    subsystem|integration|utility)
        log_info "Creating $MODULE_TYPE module: $MODULE_NAME"
        ;;
    *)
        log_error "Invalid module type: $MODULE_TYPE"
        log_info "Valid types: subsystem, integration, utility"
        exit 1
        ;;
esac

# Create module directories
MODULE_DIR="$SRC_DIR/$MODULE_NAME"
log_info "Creating module directory: $MODULE_DIR"
mkdir -p "$MODULE_DIR"

# Create __init__.py
log_info "Creating module __init__.py"
cat > "$MODULE_DIR/__init__.py" <<EOF
"""
${MODULE_NAME^} Module

Thalos Prime ${MODULE_TYPE} module for ${MODULE_NAME}.

This module follows Thalos Prime's deterministic architecture:
- Explicit control paths
- No implicit state changes
- Deterministic behavior
- Subsystem isolation
"""

from typing import Dict, Any


class ${MODULE_NAME^}Manager:
    """
    Manager for ${MODULE_NAME} ${MODULE_TYPE}.
    
    Provides deterministic operations with explicit control.
    """
    
    def __init__(self) -> None:
        """Initialize ${MODULE_NAME} manager."""
        self._state: Dict[str, Any] = {}
    
    def get_state(self) -> Dict[str, Any]:
        """Get ${MODULE_NAME} state (read-only)."""
        return self._state.copy()
    
    def update_state(self, state: Dict[str, Any]) -> None:
        """Update ${MODULE_NAME} state explicitly."""
        self._state.update(state)


__all__ = ["${MODULE_NAME^}Manager"]
EOF

# Create test files
log_info "Creating unit tests"
mkdir -p "$TEST_DIR/unit"
cat > "$TEST_DIR/unit/test_${MODULE_NAME}.py" <<EOF
"""
Tests for ${MODULE_NAME^} Module

Validates deterministic behavior and explicit control.
"""

import pytest
from thalos_prime.${MODULE_NAME} import ${MODULE_NAME^}Manager


class Test${MODULE_NAME^}Manager:
    """Test ${MODULE_NAME} manager functionality."""
    
    def test_initialization(self) -> None:
        """Test manager initializes correctly."""
        manager = ${MODULE_NAME^}Manager()
        assert manager.get_state() == {}
    
    def test_state_update(self) -> None:
        """Test explicit state updates."""
        manager = ${MODULE_NAME^}Manager()
        manager.update_state({"key": "value"})
        assert manager.get_state() == {"key": "value"}
    
    def test_no_implicit_changes(self) -> None:
        """Test that reading state doesn't modify it."""
        manager = ${MODULE_NAME^}Manager()
        manager.update_state({"test": True})
        
        # Multiple reads
        state1 = manager.get_state()
        state2 = manager.get_state()
        
        # Should be equal
        assert state1 == state2
        assert state1 == {"test": True}
EOF

log_info "Creating integration tests"
mkdir -p "$TEST_DIR/integration"
cat > "$TEST_DIR/integration/test_${MODULE_NAME}_integration.py" <<EOF
"""
Integration Tests for ${MODULE_NAME^} Module

Tests integration with other Thalos Prime subsystems.
"""

import pytest
from thalos_prime.${MODULE_NAME} import ${MODULE_NAME^}Manager


class Test${MODULE_NAME^}Integration:
    """Integration tests for ${MODULE_NAME} module."""
    
    def test_basic_integration(self) -> None:
        """Test basic integration scenario."""
        manager = ${MODULE_NAME^}Manager()
        
        # Basic integration test
        manager.update_state({"integrated": True})
        assert manager.get_state()["integrated"] is True
EOF

# Create documentation
log_info "Creating documentation"
mkdir -p "$DOCS_DIR"
cat > "$DOCS_DIR/${MODULE_NAME}.md" <<EOF
# ${MODULE_NAME^} Module

## Overview

The ${MODULE_NAME} module is a ${MODULE_TYPE} component of Thalos Prime that provides deterministic operations with explicit control.

## Architecture

This module follows Thalos Prime's core principles:
- **Deterministic Behavior**: Same inputs always produce same outputs
- **Explicit Control**: All operations are explicit with no hidden side effects
- **State Isolation**: Module state is isolated from other subsystems
- **Reproducibility**: Operations are fully reproducible

## Usage

\`\`\`python
from thalos_prime.${MODULE_NAME} import ${MODULE_NAME^}Manager

# Initialize manager
manager = ${MODULE_NAME^}Manager()

# Update state explicitly
manager.update_state({"key": "value"})

# Read state (returns copy, no side effects)
state = manager.get_state()
\`\`\`

## API Reference

### ${MODULE_NAME^}Manager

Main manager class for ${MODULE_NAME} operations.

#### Methods

- \`get_state() -> Dict[str, Any]\`: Get current state (read-only copy)
- \`update_state(state: Dict[str, Any]) -> None\`: Update state explicitly

## Testing

Run tests:
\`\`\`bash
pytest tests/unit/test_${MODULE_NAME}.py
pytest tests/integration/test_${MODULE_NAME}_integration.py
\`\`\`

## Integration

This module integrates with:
- Session Management
- CIS (Control and Integration System)
- Memory Subsystem
- Code Generation

## See Also

- [Session Management](session.md)
- [Architecture Overview](architecture.md)
EOF

log_info "Module scaffolding complete!"
log_info ""
log_info "Created:"
log_info "  - Module: $MODULE_DIR"
log_info "  - Tests: $TEST_DIR/unit/test_${MODULE_NAME}.py"
log_info "  - Integration Tests: $TEST_DIR/integration/test_${MODULE_NAME}_integration.py"
log_info "  - Documentation: $DOCS_DIR/${MODULE_NAME}.md"
log_info ""
log_info "Next steps:"
log_info "  1. Implement module functionality in $MODULE_DIR"
log_info "  2. Add comprehensive tests"
log_info "  3. Update documentation"
log_info "  4. Run tests: pytest tests/unit/test_${MODULE_NAME}.py"
