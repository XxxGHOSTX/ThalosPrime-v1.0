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
- [API Reference](docs/api.md) - Python API documentation
- [DevOps Automation](docs/automation.md) - Workflow automation
- [Deployment Guide](docs/deployment.md) - Production deployment

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
![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![Node](https://img.shields.io/badge/node-16%2B-green.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

> Thalos Prime: An advanced interactive AI system using Synthetic Biological Intelligence principles, featuring deterministic agent session management with explicit control and no implicit side effects.

## 🚀 Quick Start

```bash
# Clone and setup
git clone https://github.com/XxxGHOSTX/ThalosPrime-v1.0.git
cd ThalosPrime-v1.0
./scripts/bootstrap.sh

# Start using
source venv/bin/activate
./src/cli/thalos --help
```

## ✨ Key Features

- 🎯 **Deterministic Architecture** - Reproducible and traceable operations
- 🧠 **SBI Interface** - Natural language interaction with ANY input support
- 🔄 **Session Lifecycle Management** - Start, pause, resume, terminate
- 💾 **Persistent Storage** - Atomic session state persistence
- 🧠 **Memory Subsystem** - Working, episodic, and semantic memory
- 🤖 **CIS Integration** - Central Intelligence System integration
- 🔨 **Code Generation** - Template-based deterministic code generation
- 🖥️ **Dual Implementation** - Python and Node.js APIs
- 📦 **Full Automation** - CI/CD, testing, and release automation

## 🧠 SBI (Synthetic Biological Intelligence) Interface

Interact with Thalos Prime using natural language! The SBI interface responds to ANY input:

```bash
# Natural language commands
./src/cli/thalos sbi "create a new session"
./src/cli/thalos sbi "what can you do?"
./src/cli/thalos sbi "hello, how are you?"

# Interactive mode
./src/cli/thalos sbi -i
```

**The SBI interface understands:**
- Commands: "create a session", "pause agent", "show status"
- Questions: "what is SBI?", "how does this work?"
- Greetings: "hello", "thanks", "help me"
- ANY general input - always gets a relevant response!

See [SBI Documentation](docs/SBI_INTERFACE.md) for details.

## 📖 Documentation

- **[Complete Documentation](docs/README.md)** - Full system documentation
- **[Examples](examples/basic_usage.py)** - Usage examples and tutorials
- **[API Reference](docs/API.md)** - Detailed API documentation

## 🎮 CLI Usage

```bash
# SBI Natural Language Interface (NEW!)
./src/cli/thalos sbi "create a session"     # Natural language command
./src/cli/thalos sbi "what can you do?"     # Ask questions
./src/cli/thalos sbi -i                     # Interactive mode

# Traditional Session management
./src/cli/thalos start                      # Start new session
./src/cli/thalos status <session-id>        # Get session status
./src/cli/thalos pause <session-id>         # Pause session
./src/cli/thalos resume <session-id>        # Resume session
./src/cli/thalos stop <session-id>          # Stop session
./src/cli/thalos list                       # List all sessions
./src/cli/thalos cleanup                    # Cleanup terminated sessions
```

## 🔬 Architecture

Thalos Prime follows strict deterministic principles:

- **Explicit Control**: All state changes are explicit and validated
- **No Side Effects**: Operations are pure and predictable
- **Atomic Transitions**: State changes are all-or-nothing
- **Complete Audit Trail**: Every operation is logged
- **Reproducibility**: Same inputs → same outputs

## 🧪 Testing

```bash
# Python tests
pytest tests/python/ -v --cov

# Integration tests
./scripts/bootstrap.sh
./src/cli/thalos start
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `./scripts/create_feature_branch.sh my-feature`
3. Add tests and ensure they pass
4. Submit Pull Request

## 📋 Project Structure

```
ThalosPrime-v1.0/
├── src/
│   ├── python/thalos_agent_session/    # Python implementation
│   ├── nodejs/                         # Node.js implementation
│   └── cli/                            # CLI interface
├── tests/                              # Test suites
├── scripts/                            # Automation scripts
├── docs/                               # Documentation
└── examples/                           # Usage examples
```

## 📜 License

MIT License - See LICENSE file for details

## 🔗 Links

- [GitHub Repository](https://github.com/XxxGHOSTX/ThalosPrime-v1.0)
- [Issue Tracker](https://github.com/XxxGHOSTX/ThalosPrime-v1.0/issues)
- [Documentation](docs/README.md)

---

Built with ❤️ using deterministic architecture principles
