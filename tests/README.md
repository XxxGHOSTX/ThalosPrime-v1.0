# Thalos Prime Tests

This directory contains the comprehensive test suite for Thalos Prime.

## Test Structure

```
tests/
├── __init__.py                     # Test package marker
├── unit/                           # Unit tests
│   ├── __init__.py
│   ├── test_session_manager.py     # SessionManager tests
│   ├── test_agent_session.py       # AgentSession tests
│   └── test_lifecycle.py           # Lifecycle tests
└── integration/                    # Integration tests
    ├── __init__.py
    └── test_session_integration.py # Full workflow tests
```

## Running Tests

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test File
```bash
pytest tests/unit/test_session_manager.py -v
```

### Run Specific Test
```bash
pytest tests/unit/test_session_manager.py::TestSessionManager::test_create_session -v
```

### Run with Coverage
```bash
pytest tests/ --cov=thalos_prime --cov-report=html --cov-report=term
```

### Run Tests in Parallel
```bash
pytest tests/ -n auto
```

## Test Categories

### Unit Tests (`tests/unit/`)

Test individual components in isolation:

- **test_session_manager.py**: Tests for `SessionManager` class
  - Session creation and retrieval
  - Multi-session management
  - Session filtering and statistics
  - Persistence operations

- **test_agent_session.py**: Tests for `AgentSession` class
  - Session lifecycle operations
  - State management
  - Serialization/deserialization
  - Deterministic behavior

- **test_lifecycle.py**: Tests for `SessionLifecycle` class
  - State transitions
  - Transition validation
  - State history tracking
  - Error handling

### Integration Tests (`tests/integration/`)

Test complete workflows and subsystem interactions:

- **test_session_integration.py**
  - Full session lifecycle
  - Multi-session workflows
  - Subsystem integration
  - Session isolation

## Writing Tests

### Test Structure

Follow the AAA pattern:

```python
def test_feature_name() -> None:
    """Test description."""
    # Arrange - Set up test data
    manager = SessionManager()
    
    # Act - Execute the code under test
    session = manager.create_session(name="Test")
    
    # Assert - Verify the results
    assert session is not None
    assert session.name == "Test"
```

### Test Naming

- File names: `test_<module>.py`
- Test functions: `test_<feature>_<scenario>`
- Be descriptive: `test_session_lifecycle_transitions_are_deterministic`

### Fixtures

Use pytest fixtures for common setup:

```python
import pytest
from thalos_prime.session import SessionManager

@pytest.fixture
def manager():
    """Provide a clean SessionManager instance."""
    return SessionManager()

def test_with_fixture(manager):
    """Test using fixture."""
    session = manager.create_session(name="Test")
    assert session is not None
```

### Type Hints

Always include type hints in tests:

```python
from typing import Dict, Any

def test_session_config() -> None:
    """Test session with configuration."""
    config: Dict[str, Any] = {"model": "gpt-4"}
    session = AgentSession(name="Test", config=config)
    assert session.config == config
```

### Assertions

Use clear, specific assertions:

```python
# Good
assert session.state == SessionState.INITIALIZED
assert len(sessions) == 3
assert "error" in result

# Avoid
assert session
assert sessions
```

## Test Coverage

Current coverage: >90%

### Viewing Coverage

```bash
# Generate HTML coverage report
pytest tests/ --cov=thalos_prime --cov-report=html

# Open in browser
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

### Coverage Goals

- All public APIs: 100%
- Core logic: >95%
- Error handlers: >90%
- Overall: >90%

## Continuous Integration

Tests run automatically on:
- Pull requests
- Pushes to main branch
- Release tags

See `.github/workflows/test.yml` for CI configuration.

## Troubleshooting

### Import Errors

If you get import errors, install the package in editable mode:

```bash
pip install -e .
```

### Test Discovery Issues

Ensure all test directories have `__init__.py` files.

### Slow Tests

Run specific test files or use parallel execution:

```bash
pytest tests/unit/ -n auto
```

## Best Practices

1. **Test one thing**: Each test should verify one specific behavior
2. **Deterministic**: Tests should always produce the same results
3. **Independent**: Tests should not depend on each other
4. **Fast**: Keep unit tests fast (<1s each)
5. **Clear**: Test names and assertions should be self-documenting
6. **Complete**: Test both success and failure cases

## Contributing Tests

When adding features:
1. Write tests first (TDD approach)
2. Ensure all new code is covered
3. Run full test suite before committing
4. Update this README if adding test categories

## Questions?

See [CONTRIBUTING.md](../CONTRIBUTING.md) for more information.
