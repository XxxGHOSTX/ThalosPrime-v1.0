# Thalos Prime v1.0

**Deterministic AI Agent Session Management System**

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
- 🔄 **Session Lifecycle Management** - Start, pause, resume, terminate
- 💾 **Persistent Storage** - Atomic session state persistence
- 🧠 **Memory Subsystem** - Working, episodic, and semantic memory
- 🤖 **CIS Integration** - Central Intelligence System integration
- 🔨 **Code Generation** - Template-based deterministic code generation
- 🖥️ **Dual Implementation** - Python and Node.js APIs
- 📦 **Full Automation** - CI/CD, testing, and release automation

## 📖 Documentation

- **[Complete Documentation](docs/README.md)** - Full system documentation
- **[Examples](examples/basic_usage.py)** - Usage examples and tutorials
- **[API Reference](docs/API.md)** - Detailed API documentation

## 🎮 CLI Usage

```bash
# Session management
./src/cli/thalos start                    # Start new session
./src/cli/thalos status <session-id>      # Get session status
./src/cli/thalos pause <session-id>       # Pause session
./src/cli/thalos resume <session-id>      # Resume session
./src/cli/thalos stop <session-id>        # Stop session
./src/cli/thalos list                     # List all sessions
./src/cli/thalos cleanup                  # Cleanup terminated sessions
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
