# Thalos Prime - Agent Session Management System

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![Node](https://img.shields.io/badge/node-16%2B-green.svg)

## Overview

Thalos Prime is an advanced AI agent session management system built on **deterministic architecture** principles. It provides explicit control over agent lifecycles with no implicit side effects, ensuring reproducible and traceable behavior across all operations.

### Key Features

- 🎯 **Deterministic Architecture**: All operations are reproducible and traceable
- 🔄 **Session Lifecycle Management**: Start, pause, resume, and terminate agent sessions
- 💾 **Persistent Storage**: Atomic session state persistence
- 🧠 **Memory Subsystem**: Working, episodic, and semantic memory management
- 🤖 **CIS Integration**: Seamless integration with Central Intelligence System
- 🔨 **Code Generation**: Template-based deterministic code generation
- 🖥️ **CLI Interface**: Comprehensive command-line tools
- 📚 **Dual Implementation**: Python and Node.js APIs

## Architecture Principles

### Deterministic Design

1. **Explicit Control**: All state changes are explicit and validated
2. **No Implicit Side Effects**: Operations are pure and predictable
3. **Atomic Transitions**: State changes are all-or-nothing
4. **Complete Audit Trail**: Every operation is logged and traceable
5. **Reproducibility**: Same inputs always produce same outputs

### Core Components

```
Thalos Prime
├── Agent Session Module
│   ├── Session (state management)
│   ├── Manager (multi-session control)
│   └── Persistence (storage layer)
├── Subsystem Integration
│   ├── CIS Integration
│   ├── Memory Subsystem
│   └── Code Generation Module
└── CLI Interface
    └── Session management commands
```

## Installation

### Quick Start

```bash
# Clone the repository
git clone https://github.com/XxxGHOSTX/ThalosPrime-v1.0.git
cd ThalosPrime-v1.0

# Bootstrap the environment (installs all dependencies)
./scripts/bootstrap.sh

# Activate Python virtual environment
source venv/bin/activate
```

### Manual Installation

#### Python

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Node.js

```bash
# Install dependencies
npm install
```

## Usage

### CLI Commands

#### Start a Session
```bash
./src/cli/thalos start
./src/cli/thalos start --metadata '{"user": "alice", "priority": "high"}'
```

#### Manage Sessions
```bash
# Get session status
./src/cli/thalos status <session-id>

# Pause a running session
./src/cli/thalos pause <session-id>

# Resume a paused session
./src/cli/thalos resume <session-id>

# Stop (terminate) a session
./src/cli/thalos stop <session-id>

# List all sessions
./src/cli/thalos list
./src/cli/thalos list --state running

# Cleanup terminated sessions
./src/cli/thalos cleanup
```

### Python API

```python
from thalos_agent_session import AgentSession, SessionManager, SessionPersistence

# Create a session manager
manager = SessionManager()

# Create and start a session
session = manager.create_session(metadata={"user": "alice"})
session = manager.start_session(session.session_id)

# Perform operations
session = manager.pause_session(session.session_id)
session = manager.resume_session(session.session_id)

# Persist session state
persistence = SessionPersistence()
persistence.save_session(session)

# Load session later
loaded_session = persistence.load_session(session.session_id)
```

### Node.js API

```javascript
const { AgentSession, SessionManager } = require('./src/nodejs');

// Create a session manager
const manager = new SessionManager();

// Create and start a session
let session = manager.createSession({ user: 'alice' });
session = manager.startSession(session.sessionId);

// Perform operations
session = manager.pauseSession(session.sessionId);
session = manager.resumeSession(session.sessionId);
```

## Development

### Running Tests

#### Python Tests
```bash
# Run all tests
pytest tests/python/ -v

# Run with coverage
pytest tests/python/ --cov=src/python/thalos_agent_session --cov-report=html

# Run specific test file
pytest tests/python/test_session.py -v
```

#### Node.js Tests
```bash
npm test
```

### Code Quality

```bash
# Format code
black src/python/

# Lint code
flake8 src/python/

# Type checking
mypy src/python/thalos_agent_session/
```

### Creating Feature Branches

```bash
# Use the automated script
./scripts/create_feature_branch.sh my-feature "Description of feature"

# This will:
# - Create a new feature branch
# - Stage and commit changes
# - Push to remote
# - Generate PR description
```

## Testing

The project includes comprehensive test suites ensuring:

- ✅ Deterministic state transitions
- ✅ Session lifecycle correctness
- ✅ Persistence atomicity
- ✅ Subsystem integration
- ✅ Error handling
- ✅ Edge cases

### Test Coverage

- Session module: 100%
- Manager module: 95%
- Persistence module: 95%
- Integration tests: 90%

## CI/CD

Automated workflows handle:

- **Continuous Integration**: Automated testing on all PRs
- **Code Quality**: Linting and formatting checks
- **Security Scanning**: Vulnerability detection
- **Release Automation**: Automatic releases with AI-generated notes

## Project Structure

```
ThalosPrime-v1.0/
├── src/
│   ├── python/
│   │   └── thalos_agent_session/
│   │       ├── __init__.py
│   │       ├── session.py              # Core session management
│   │       ├── manager.py              # Multi-session management
│   │       ├── persistence.py          # State persistence
│   │       ├── cis_integration.py      # CIS integration
│   │       ├── memory_subsystem.py     # Memory management
│   │       └── code_generation.py      # Code generation
│   ├── nodejs/
│   │   ├── index.js
│   │   ├── session.js
│   │   └── manager.js
│   └── cli/
│       └── thalos                      # CLI entry point
├── tests/
│   ├── python/
│   │   ├── test_session.py
│   │   ├── test_manager.py
│   │   └── test_persistence.py
│   └── nodejs/
├── scripts/
│   ├── bootstrap.sh                    # Environment setup
│   └── create_feature_branch.sh        # Feature branch automation
├── docs/
│   └── API.md                          # API documentation
├── examples/
│   └── basic_usage.py                  # Usage examples
├── .github/
│   └── workflows/
│       ├── ci.yml                      # CI pipeline
│       └── release.yml                 # Release automation
├── requirements.txt                     # Python dependencies
├── package.json                         # Node.js dependencies
└── README.md                            # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch: `./scripts/create_feature_branch.sh my-feature`
3. Make your changes following deterministic principles
4. Add tests for new functionality
5. Run test suite: `pytest tests/python/ -v`
6. Commit with descriptive messages
7. Push and create a Pull Request

## Architecture Philosophy

Thalos Prime follows strict architectural principles:

### Determinism
- Operations are predictable and reproducible
- No hidden state or side effects
- Complete traceability

### Explicit Control
- All state changes are explicit
- Validation before state transitions
- Clear error messages

### Immutability
- Session operations return new instances
- Original state preserved
- Thread-safe by design

### Subsystem Isolation
- Clear boundaries between subsystems
- Explicit integration points
- Minimal coupling

## License

MIT License - See LICENSE file for details

## Support

- 📧 Email: support@thalosprime.ai
- 🐛 Issues: [GitHub Issues](https://github.com/XxxGHOSTX/ThalosPrime-v1.0/issues)
- 📖 Documentation: [docs/](docs/)
- 💬 Discussions: [GitHub Discussions](https://github.com/XxxGHOSTX/ThalosPrime-v1.0/discussions)

## Roadmap

- [x] Core session management
- [x] Python implementation
- [x] Node.js implementation
- [x] CLI interface
- [x] Subsystem integration
- [x] Test coverage >90%
- [x] CI/CD automation
- [ ] Web UI dashboard
- [ ] REST API server
- [ ] Multi-agent coordination
- [ ] Session analytics
- [ ] Distributed session management

## Acknowledgments

Built on principles of deterministic computing and explicit control, inspired by functional programming paradigms and modern AI agent architectures.

---

**Thalos Prime** - Deterministic AI Agent Session Management
