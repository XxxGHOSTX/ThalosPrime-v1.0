# DevOps Automation

## Overview

Thalos Prime includes comprehensive DevOps automation scripts for the entire development lifecycle, from feature creation to release.

## Automation Scripts

### 1. Feature Branch Creator

**Purpose**: Create feature branches with standardized naming and initial commits.

**Location**: `scripts/create_feature_branch.sh`

**Usage**:
```bash
./scripts/create_feature_branch.sh <module-name> [description]
```

**Example**:
```bash
./scripts/create_feature_branch.sh session "Add agent session management"
```

**What it does**:
1. Creates branch: `feature/<module-name>`
2. Makes initial empty commit with description
3. Sets up branch for development

**Output**:
```
[INFO] Creating feature branch: feature/session
[INFO] Feature branch created successfully: feature/session
```

### 2. Module Scaffolder

**Purpose**: Generate complete module scaffolds with deterministic templates.

**Location**: `scripts/scaffold_module.sh`

**Usage**:
```bash
./scripts/scaffold_module.sh <module-name> <module-type>
```

**Module Types**:
- `subsystem` - Core subsystem module
- `integration` - Integration module
- `utility` - Utility module

**Example**:
```bash
./scripts/scaffold_module.sh analytics subsystem
```

**What it generates**:
1. Module directory: `src/thalos_prime/analytics/`
2. `__init__.py` with manager class
3. Unit tests: `tests/unit/test_analytics.py`
4. Integration tests: `tests/integration/test_analytics_integration.py`
5. Documentation: `docs/analytics.md`

**Template Structure**:
```python
class AnalyticsManager:
    """Deterministic analytics manager."""
    
    def __init__(self) -> None:
        self._state: Dict[str, Any] = {}
    
    def get_state(self) -> Dict[str, Any]:
        """Get state (read-only)."""
        return self._state.copy()
    
    def update_state(self, state: Dict[str, Any]) -> None:
        """Update state explicitly."""
        self._state.update(state)
```

### 3. Smart Commit

**Purpose**: Create commits with AI-generated, context-aware messages.

**Location**: `scripts/commit_changes.sh`

**Usage**:
```bash
# Auto-generate message
./scripts/commit_changes.sh

# Custom message
./scripts/commit_changes.sh --message "Custom commit message"
```

**Message Generation**:

The script analyzes changed files and generates appropriate commit messages:

| Changes | Type | Example Message |
|---------|------|-----------------|
| `src/` + `tests/` | `feat` | "feat(session): implement deterministic behavior with comprehensive tests" |
| `tests/` only | `test` | "test(session): add deterministic tests for reproducibility verification" |
| `docs/` | `docs` | "docs: update documentation for explicit control paths" |
| `.github/` | `ci` | "ci: add automated testing and release workflows" |
| `scripts/` | `build` | "build(automation): configure deterministic build scripts" |

**Example Output**:
```
[INFO] Staging changes...
[INFO] Generating AI-powered commit message...
[INFO] Commit message:
---
feat(session): implement deterministic behavior with comprehensive tests

- Add explicit control paths with no implicit side effects
- Implement deterministic state transitions
- Add unit and integration tests for reproducibility
- Ensure subsystem isolation
---

Proceed with commit? (y/n)
```

### 4. Pull Request Creator

**Purpose**: Create PRs with comprehensive, AI-generated descriptions.

**Location**: `scripts/create_pr.sh`

**Usage**:
```bash
./scripts/create_pr.sh [--base main] [--title "PR Title"]
```

**Example**:
```bash
./scripts/create_pr.sh --base main
```

**What it does**:
1. Analyzes changed files
2. Generates comprehensive PR description
3. Lists affected subsystems
4. Documents API/CLI changes
5. Includes test coverage info
6. Creates PR via GitHub CLI

**PR Description Template**:
```markdown
## Overview
Deterministic features following Thalos Prime architecture principles.

## Changes

### Subsystems Modified
- **Session Management**: Deterministic agent session lifecycle

### CLI Endpoints Added
- `thalos session start` - Start new session
- `thalos session stop` - Terminate session

### Deterministic Properties
- ✅ Explicit state transitions
- ✅ Reproducible behavior
- ✅ Subsystem isolation

### Test Coverage
- ✅ Unit tests for all components
- ✅ Integration tests
- ✅ Deterministic behavior verification

## Testing
All tests pass with deterministic results
```

### 5. Release Creator

**Purpose**: Automate release process with version tagging and notes.

**Location**: `scripts/create_release.sh`

**Usage**:
```bash
./scripts/create_release.sh <version>
```

**Example**:
```bash
./scripts/create_release.sh 1.0.0
```

**What it does**:
1. Validates version format (X.Y.Z)
2. Updates `pyproject.toml`
3. Runs all tests
4. Generates release notes from commits
5. Creates annotated git tag
6. Pushes tag (triggers release workflow)

**Release Notes Generation**:
- Categorizes commits by type (feat, fix, docs, etc.)
- Lists deterministic properties
- Includes installation instructions
- Links to documentation

## CI/CD Workflows

### Test Workflow

**File**: `.github/workflows/test.yml`

**Triggers**:
- Push to `main`, `develop`, `feature/*`
- Pull requests to `main`, `develop`

**Jobs**:

1. **Test Matrix**
   - Python 3.8, 3.9, 3.10, 3.11
   - Runs linters (black, flake8)
   - Type checking (mypy)
   - Unit tests with coverage
   - Integration tests

2. **Deterministic Verification**
   ```yaml
   - name: Verify deterministic behavior
     run: |
       pytest tests/ -q
       pytest tests/ -q
       pytest tests/ -q
   ```
   Runs tests 3 times to ensure consistent results

3. **CLI Testing**
   ```yaml
   - name: Test CLI commands
     run: |
       thalos --version
       thalos session --help
   ```

4. **Build Package**
   - Builds wheel and sdist
   - Validates with twine
   - Uploads as artifact

### Release Workflow

**File**: `.github/workflows/release.yml`

**Triggers**:
- Push tags matching `v*.*.*`

**Jobs**:

1. **Create Release**
   - Runs all tests
   - Builds package
   - Generates release notes
   - Creates GitHub release
   - Publishes to PyPI (if configured)

**Release Notes**:
```markdown
# Thalos Prime vX.Y.Z

## Features Added
### Agent Session Management
- Deterministic session lifecycle
- Session persistence
- CLI commands

### CLI Endpoints
- `thalos session start`
- `thalos session stop`
...

## Deterministic Properties Verified
- ✅ No implicit state changes
- ✅ Reproducible behavior
...
```

## Development Workflow

### Complete Feature Development

```bash
# 1. Create feature branch
./scripts/create_feature_branch.sh new-feature "Add new capability"

# 2. Scaffold module (if needed)
./scripts/scaffold_module.sh mymodule subsystem

# 3. Develop feature
# ... make changes ...

# 4. Commit changes
./scripts/commit_changes.sh

# 5. Create PR
./scripts/create_pr.sh --base main

# 6. After merge, create release
./scripts/create_release.sh 1.1.0
```

### Quick Changes

```bash
# Make changes
# ... edit files ...

# Commit with auto-generated message
./scripts/commit_changes.sh

# Push
git push
```

## Best Practices

### Branch Naming

Follow conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation
- `refactor/` - Refactoring

### Commit Messages

Use conventional commits:
```
<type>(<scope>): <subject>

<body>
```

Types:
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `test` - Tests
- `refactor` - Refactoring
- `ci` - CI/CD
- `build` - Build system
- `chore` - Maintenance

### Testing Before Release

```bash
# Run all tests
pytest tests/ -v

# Check determinism
pytest tests/ && pytest tests/ && pytest tests/

# Test CLI
thalos --version
thalos session start --name test
thalos session list
```

### Version Management

Follow semantic versioning:
- `MAJOR.MINOR.PATCH`
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

## Troubleshooting

### Script Permissions

If scripts aren't executable:
```bash
chmod +x scripts/*.sh
```

### GitHub CLI Not Found

Install GitHub CLI:
```bash
# macOS
brew install gh

# Linux
sudo apt install gh

# Or download from https://cli.github.com/
```

### Tests Failing

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run specific test
pytest tests/unit/test_session.py -v

# Show full output
pytest tests/ -vv --tb=long
```

## See Also

- [Architecture](architecture.md) - System design
- [Session Management](session.md) - Agent sessions
- [CLI Reference](cli.md) - Command-line interface
