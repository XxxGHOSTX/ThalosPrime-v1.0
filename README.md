# Thalos Prime v1.0

**Deterministic AI Agent Session Management System**

Thalos Prime is an advanced AI system using deterministic architecture with explicit control and no implicit side effects. Built for reproducibility, subsystem isolation, and transparent operations.

## 🎯 Core Principles

1. **Deterministic Behavior**: Same inputs always produce same outputs
2. **Explicit Control**: All operations require explicit invocation
3. **No Implicit Side Effects**: State changes are always explicit
4. **Subsystem Isolation**: Modules operate independently
5. **Reproducibility**: Operations are fully reproducible

## 🚀 Features

### Agent Session Management
- Deterministic session lifecycle (initialize → start → pause → resume → terminate)
- Session state persistence with JSON serialization
- Subsystem integration (CIS, Memory, CodeGen)
- Multi-session management with filtering

### CLI Interface
```bash
# Start new session
thalos session start --name "my-session" --config '{"model": "gpt-4"}'

# Pause running session
thalos session pause <session-id>

# Resume paused session
thalos session resume <session-id>

# Check status
thalos session status <session-id>

# List all sessions
thalos session list --state running

# Stop session
thalos session stop <session-id>
```

### DevOps Automation
- Automated feature branch creation
- Module scaffolding with templates
- AI-generated commit messages
- Pull request automation
- CI/CD workflows

## 📦 Installation

```bash
# From PyPI (when published)
pip install thalos-prime

# From source
git clone https://github.com/XxxGHOSTX/ThalosPrime-v1.0.git
cd ThalosPrime-v1.0
pip install -e ".[dev]"
```

## 🏗️ Architecture

```
thalos_prime/
├── session/          # Agent session management
│   ├── lifecycle.py  # State transitions
│   ├── agent_session.py  # Session implementation
│   └── manager.py    # Multi-session manager
├── cis/             # Control & Integration System
├── memory/          # Memory subsystem
├── codegen/         # Code generation
└── api/             # API endpoints
```

## 📚 Quick Start

### Python API

```python
from thalos_prime import SessionManager, SessionState

# Create session manager
manager = SessionManager(storage_dir=".thalos/sessions")

# Create and start session
session = manager.create_session(name="example")
session.start()

# Update subsystem states
session.update_cis_state({"mode": "active"})
session.update_memory_state({"context": "example"})

# Save session
manager.save_session(session.session_id)

# Pause and resume
session.pause()
session.resume()

# Terminate when done
session.terminate()
```

### Development Workflow

```bash
# Create feature branch
./scripts/create_feature_branch.sh my-feature "Add new capability"

# Scaffold new module
./scripts/scaffold_module.sh analytics subsystem

# Make changes and commit
./scripts/commit_changes.sh

# Create pull request
./scripts/create_pr.sh --base main
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run unit tests only
pytest tests/unit/ -v

# Run integration tests
pytest tests/integration/ -v

# Check deterministic behavior (run tests 3 times)
pytest tests/ && pytest tests/ && pytest tests/

# With coverage
pytest tests/ --cov=thalos_prime --cov-report=html
```

## 🔧 Development

### Setup Development Environment

```bash
# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run linters
black src/ tests/
flake8 src/ tests/

# Type checking
mypy src/thalos_prime/
```

### Automation Scripts

| Script | Purpose |
|--------|---------|
| `scripts/create_feature_branch.sh` | Create feature branch with naming conventions |
| `scripts/scaffold_module.sh` | Generate module scaffolds with tests |
| `scripts/commit_changes.sh` | Create commits with AI-generated messages |
| `scripts/create_pr.sh` | Create PRs with detailed descriptions |

## 📖 Documentation

- [Session Management](docs/session.md) - Agent session lifecycle
- [Architecture](docs/architecture.md) - System design principles
- [CLI Reference](docs/cli.md) - Command-line interface
- [DevOps Automation](docs/automation.md) - Workflow automation
- [API Reference](docs/api.md) - Python API documentation

## 🤝 Contributing

1. Create feature branch: `./scripts/create_feature_branch.sh feature-name`
2. Make changes following deterministic principles
3. Add tests for new functionality
4. Commit: `./scripts/commit_changes.sh`
5. Create PR: `./scripts/create_pr.sh`

### Code Standards

- **Determinism**: All functions must be deterministic
- **Explicit Control**: No implicit state changes
- **Type Hints**: All functions must have type annotations
- **Tests**: Minimum 90% code coverage
- **Documentation**: All public APIs must be documented

## 📝 License

MIT License - See [LICENSE](LICENSE) for details

## 🙏 Acknowledgments

Built with deterministic principles and explicit control for reliable AI agent management.

## 📞 Support

- Issues: [GitHub Issues](https://github.com/XxxGHOSTX/ThalosPrime-v1.0/issues)
- Discussions: [GitHub Discussions](https://github.com/XxxGHOSTX/ThalosPrime-v1.0/discussions)

---

**Thalos Prime** - Deterministic AI Agent Sessions with Explicit Control
