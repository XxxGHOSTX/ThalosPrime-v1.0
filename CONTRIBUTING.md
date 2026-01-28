# Contributing to Thalos Prime

Thank you for your interest in contributing to Thalos Prime! This document provides guidelines for contributing to the project.

## 🎯 Core Principles

Before contributing, please understand Thalos Prime's core architectural principles:

1. **Deterministic Behavior**: Same inputs must always produce same outputs
2. **Explicit Control**: All operations require explicit invocation
3. **No Implicit Side Effects**: State changes must always be explicit
4. **Subsystem Isolation**: Modules should operate independently
5. **Reproducibility**: All operations must be fully reproducible

## 🚀 Getting Started

### Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/XxxGHOSTX/ThalosPrime-v1.0.git
   cd ThalosPrime-v1.0
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Verify installation**
   ```bash
   pytest tests/
   black --check .
   flake8 src/ tests/
   mypy src/
   ```

## 📝 Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

- Follow the existing code style (enforced by Black)
- Write comprehensive docstrings for all public APIs
- Add type hints to all function signatures
- Ensure no implicit state changes or side effects

### 3. Write Tests

- Add unit tests for all new functionality
- Maintain or improve test coverage
- Tests should be deterministic and reproducible
- Place tests in appropriate directory:
  - `tests/unit/` for unit tests
  - `tests/integration/` for integration tests

### 4. Run Quality Checks

```bash
# Format code
black .

# Run linter
flake8 src/ tests/

# Type checking
mypy src/

# Run tests
pytest tests/ -v --cov=thalos_prime
```

### 5. Commit Your Changes

Use clear, descriptive commit messages:

```bash
git commit -m "Add: New feature description"
git commit -m "Fix: Bug description"
git commit -m "Docs: Documentation update"
git commit -m "Test: New test cases"
```

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub with:
- Clear description of changes
- Reference to any related issues
- Screenshots for UI changes
- Test results

## 🧪 Testing Guidelines

### Writing Tests

- Test file names: `test_*.py`
- Test function names: `test_*`
- Use descriptive test names that explain what is being tested
- Follow AAA pattern: Arrange, Act, Assert

```python
def test_session_lifecycle_operations() -> None:
    """Test that session lifecycle follows deterministic state transitions."""
    # Arrange
    session = AgentSession(name="Test Session")
    
    # Act
    session.start()
    session.pause()
    
    # Assert
    assert session.state == SessionState.PAUSED
```

### Test Coverage

- Aim for >90% code coverage
- All public APIs must be tested
- Edge cases should be covered
- Error handling should be tested

## 📚 Documentation

### Code Documentation

- All modules should have module-level docstrings
- All classes should have class-level docstrings
- All public methods should have docstrings with:
  - Description of functionality
  - Args: Parameter descriptions with types
  - Returns: Return value description with type
  - Raises: Exception descriptions

Example:
```python
def create_session(self, name: str, config: Optional[Dict[str, Any]] = None) -> AgentSession:
    """
    Create a new agent session with explicit configuration.
    
    Args:
        name: Human-readable session name
        config: Optional session configuration dictionary
        
    Returns:
        AgentSession: Newly created session instance
        
    Raises:
        ValueError: If name is empty or invalid
    """
```

### Documentation Files

- Update README.md for user-facing changes
- Update CHANGELOG.md for all releases
- Add examples to `examples/` directory for new features

## 🔍 Code Review Process

All contributions go through code review:

1. **Automated Checks**: CI/CD runs tests, linting, and formatting
2. **Maintainer Review**: Core team reviews code quality and architecture
3. **Feedback**: Address any requested changes
4. **Approval**: Once approved, changes will be merged

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Description**: Clear description of the issue
2. **Steps to Reproduce**: Minimal steps to reproduce the bug
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Environment**: Python version, OS, package version
6. **Code Sample**: Minimal reproducible example

## 💡 Feature Requests

For feature requests, please provide:

1. **Use Case**: Why is this feature needed?
2. **Proposed Solution**: How should it work?
3. **Alternatives**: What alternatives have you considered?
4. **Alignment**: How does it align with core principles?

## 📜 Code Style

### Python Style

- Follow PEP 8
- Use Black for formatting (line length: 88)
- Use type hints for all function signatures
- Import order: stdlib → third-party → local

### Naming Conventions

- Classes: `PascalCase`
- Functions/methods: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Private members: `_leading_underscore`

### Best Practices

- Keep functions small and focused
- Avoid mutable default arguments
- Use explicit type annotations
- No implicit state changes
- Document all public APIs

## 🤝 Community

- Be respectful and inclusive
- Help others learn and grow
- Share knowledge and best practices
- Provide constructive feedback

## 📄 License

By contributing to Thalos Prime, you agree that your contributions will be licensed under the MIT License.

## ❓ Questions?

If you have questions about contributing, please:
- Open a GitHub issue with the "question" label
- Check existing documentation and issues first
- Be clear and specific in your questions

Thank you for contributing to Thalos Prime! 🚀
