# Thalos Prime API Reference

## Overview

Thalos Prime v1.0 provides both CLI and Python API interfaces for deterministic AI agent session management.

## Python API

### Session Management

#### Creating a Session

```python
from thalos_prime.session import AgentSession, SessionState

# Create a new session
session = AgentSession(
    name="my-agent",
    config={
        "model": "gpt-4",
        "temperature": 0.7,
        "max_tokens": 2000
    }
)

# Access session properties
print(f"Session ID: {session.session_id}")
print(f"Session Name: {session.name}")
print(f"State: {session.state}")
```

#### Session Lifecycle

```python
# Start the session
session.start()
assert session.state == SessionState.RUNNING
assert session.is_active() == True

# Pause the session
session.pause()
assert session.state == SessionState.PAUSED

# Resume the session
session.resume()
assert session.state == SessionState.RUNNING

# Terminate the session
session.terminate()
assert session.state == SessionState.TERMINATED
assert session.is_terminated() == True
```

#### Subsystem State Management

```python
# Update CIS (Control and Integration System) state
session.update_cis_state({
    "mode": "autonomous",
    "priority": "high",
    "timeout": 300
})

# Update Memory subsystem state
session.update_memory_state({
    "context_window": 8192,
    "cache_enabled": True,
    "embedding_model": "text-embedding-ada-002"
})

# Update CodeGen subsystem state
session.update_codegen_state({
    "language": "python",
    "style": "pep8",
    "test_framework": "pytest"
})

# Get subsystem states
cis_state = session.get_cis_state()
memory_state = session.get_memory_state()
codegen_state = session.get_codegen_state()
```

#### Session Persistence

```python
# Serialize to dictionary
session_dict = session.to_dict()

# Serialize to JSON
import json
session_json = session.to_json()

# Create from dictionary
restored_session = AgentSession.from_dict(session_dict)

# Create from JSON
restored_session = AgentSession.from_json(session_json)
```

### SessionManager

#### Creating a Manager

```python
from thalos_prime.session import SessionManager

# Create manager with default storage
manager = SessionManager()

# Create manager with custom storage
manager = SessionManager(storage_dir="/var/lib/thalos/sessions")
```

#### Managing Multiple Sessions

```python
# Create a new session
session = manager.create_session(
    name="agent-1",
    config={"model": "gpt-4"}
)

# Get a session by ID
session = manager.get_session(session_id)

# List all sessions
all_sessions = manager.list_sessions()

# List sessions by state
running_sessions = manager.list_sessions(state=SessionState.RUNNING)
paused_sessions = manager.list_sessions(state=SessionState.PAUSED)

# Get statistics
stats = manager.get_statistics()
print(f"Total sessions: {stats['total']}")
print(f"Running: {stats['running']}")
print(f"Paused: {stats['paused']}")
```

#### Session Persistence with Manager

```python
# Save a session to disk
manager.save_session(session_id)

# Load all sessions from disk
manager.load_all_sessions()

# Delete a session (terminates if active)
manager.delete_session(session_id)
```

### SessionLifecycle

```python
from thalos_prime.session import SessionLifecycle, SessionState

# Create lifecycle manager
lifecycle = SessionLifecycle()

# Check current state
current_state = lifecycle.get_state()

# Transition to new state
lifecycle.transition_to(SessionState.RUNNING)

# Check if transition is valid
can_pause = lifecycle.can_transition_to(SessionState.PAUSED)

# Get state history
history = lifecycle.get_history()
for entry in history:
    print(f"{entry['timestamp']}: {entry['from_state']} -> {entry['to_state']}")
```

## CLI API

### Session Commands

#### Start Session

```bash
# Start with name
thalos session start --name "my-agent"

# Start with configuration
thalos session start --name "my-agent" --config '{"model": "gpt-4"}'

# Start with JSON config file
thalos session start --name "my-agent" --config-file config.json
```

#### Pause Session

```bash
thalos session pause <session-id>
```

#### Resume Session

```bash
thalos session resume <session-id>
```

#### Stop Session

```bash
thalos session stop <session-id>
```

#### List Sessions

```bash
# List all sessions
thalos session list

# List by state
thalos session list --state running
thalos session list --state paused
thalos session list --state terminated
```

#### Session Status

```bash
# Status of specific session
thalos session status <session-id>

# Status of all sessions
thalos session status --all
```

## REST API (Future)

The following REST API endpoints are planned for future releases:

### Authentication

```http
POST /api/v1/auth/login
POST /api/v1/auth/logout
POST /api/v1/auth/refresh
```

### Sessions

```http
GET    /api/v1/sessions              # List sessions
POST   /api/v1/sessions              # Create session
GET    /api/v1/sessions/{id}         # Get session
PUT    /api/v1/sessions/{id}         # Update session
DELETE /api/v1/sessions/{id}         # Delete session
```

### Session Control

```http
POST /api/v1/sessions/{id}/start     # Start session
POST /api/v1/sessions/{id}/pause     # Pause session
POST /api/v1/sessions/{id}/resume    # Resume session
POST /api/v1/sessions/{id}/terminate # Terminate session
```

### Subsystems

```http
GET /api/v1/sessions/{id}/cis        # Get CIS state
PUT /api/v1/sessions/{id}/cis        # Update CIS state

GET /api/v1/sessions/{id}/memory     # Get Memory state
PUT /api/v1/sessions/{id}/memory     # Update Memory state

GET /api/v1/sessions/{id}/codegen    # Get CodeGen state
PUT /api/v1/sessions/{id}/codegen    # Update CodeGen state
```

### Monitoring

```http
GET /api/v1/health                   # Health check
GET /api/v1/metrics                  # Prometheus metrics
GET /api/v1/stats                    # Statistics
```

## Configuration

### Session Configuration

```python
config = {
    # Model configuration
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 2000,
    "top_p": 1.0,
    
    # Session settings
    "name": "my-agent",
    "description": "Example agent session",
    "tags": ["production", "high-priority"],
    
    # Timeouts
    "idle_timeout": 3600,
    "max_duration": 86400,
    
    # Subsystem configuration
    "cis": {
        "mode": "autonomous",
        "priority": "high"
    },
    "memory": {
        "context_window": 8192,
        "cache_enabled": True
    },
    "codegen": {
        "language": "python",
        "style": "pep8"
    }
}
```

### Environment Variables

```bash
# Session storage
export THALOS_SESSION_DIR=/path/to/sessions

# Logging
export THALOS_LOG_DIR=/path/to/logs
export THALOS_LOG_LEVEL=INFO

# API (future)
export THALOS_API_HOST=0.0.0.0
export THALOS_API_PORT=8000
export THALOS_API_AUTH_ENABLED=true
```

## Error Handling

### Python Exceptions

```python
from thalos_prime.session import AgentSession, SessionState

try:
    session = AgentSession(name="test")
    session.start()
    
    # This will raise ValueError - invalid transition
    session.resume()  # Can't resume from RUNNING
    
except ValueError as e:
    print(f"Invalid state transition: {e}")

try:
    # This will raise KeyError - session not found
    manager.get_session("nonexistent-id")
    
except KeyError as e:
    print(f"Session not found: {e}")
```

### CLI Error Codes

- `0` - Success
- `1` - General error
- `2` - Invalid arguments
- `3` - Session not found
- `4` - Invalid state transition
- `5` - I/O error

## Examples

### Complete Session Workflow

```python
from thalos_prime.session import SessionManager, SessionState

# Initialize manager
manager = SessionManager(storage_dir=".thalos/sessions")

# Create and configure session
session = manager.create_session(
    name="production-agent",
    config={
        "model": "gpt-4",
        "temperature": 0.7
    }
)

# Configure subsystems
session.update_cis_state({"mode": "autonomous", "priority": "high"})
session.update_memory_state({"context_window": 8192})
session.update_codegen_state({"language": "python"})

# Start session
session.start()

# Save state
manager.save_session(session.session_id)

# Work with session...

# Pause for interruption
session.pause()
manager.save_session(session.session_id)

# Later: resume
session.resume()

# Complete and terminate
session.terminate()
manager.save_session(session.session_id)

# Clean up
manager.delete_session(session.session_id)
```

### Multi-Session Management

```python
from thalos_prime.session import SessionManager, SessionState

manager = SessionManager()

# Create multiple sessions
sessions = []
for i in range(3):
    session = manager.create_session(
        name=f"agent-{i}",
        config={"model": "gpt-4", "index": i}
    )
    session.start()
    sessions.append(session)
    manager.save_session(session.session_id)

# Get running sessions
running = manager.list_sessions(state=SessionState.RUNNING)
print(f"Running sessions: {len(running)}")

# Get statistics
stats = manager.get_statistics()
print(f"Total: {stats['total']}, Running: {stats['running']}")

# Pause all
for session in sessions:
    session.pause()
    manager.save_session(session.session_id)

# Resume specific one
sessions[0].resume()
manager.save_session(sessions[0].session_id)

# Cleanup
for session in sessions:
    session.terminate()
    manager.delete_session(session.session_id)
```

## Type Annotations

Thalos Prime includes full type annotations for static type checking:

```python
from typing import Dict, List, Optional
from thalos_prime.session import AgentSession, SessionManager, SessionState

def process_sessions(
    manager: SessionManager,
    state: SessionState
) -> List[AgentSession]:
    """Get all sessions in a specific state."""
    return manager.list_sessions(state=state)

def update_config(
    session: AgentSession,
    config: Dict[str, any]
) -> None:
    """Update session configuration."""
    if "cis" in config:
        session.update_cis_state(config["cis"])
    if "memory" in config:
        session.update_memory_state(config["memory"])
    if "codegen" in config:
        session.update_codegen_state(config["codegen"])
```

## Best Practices

### 1. Always Use Context Managers (Future)

```python
# When implemented, use context managers for automatic cleanup
with SessionManager() as manager:
    session = manager.create_session(name="agent")
    session.start()
    # ... work with session ...
    # Automatic termination and cleanup
```

### 2. Save State Regularly

```python
# Save after important state changes
session.update_cis_state(new_state)
manager.save_session(session.session_id)
```

### 3. Handle Errors Gracefully

```python
try:
    session.transition_to(SessionState.PAUSED)
except ValueError as e:
    logger.error(f"Invalid transition: {e}")
    # Handle error appropriately
```

### 4. Use Type Hints

```python
from thalos_prime.session import AgentSession

def create_configured_session(name: str) -> AgentSession:
    session = AgentSession(name=name)
    # Configuration...
    return session
```

### 5. Verify State Before Transitions

```python
if session.lifecycle.can_transition_to(SessionState.PAUSED):
    session.pause()
else:
    print(f"Cannot pause from state: {session.state}")
```

## Performance Considerations

- **Session Creation**: O(1) - Constant time
- **State Transitions**: O(1) - Constant time with validation
- **Session Lookup**: O(1) - Dictionary-based
- **List Sessions**: O(n) - Linear in number of sessions
- **Serialization**: O(1) - Single session, O(n) for all sessions
- **Disk I/O**: Async recommended for production (future enhancement)

## Versioning

API follows Semantic Versioning (SemVer):
- **Major**: Breaking changes
- **Minor**: New features (backward compatible)
- **Patch**: Bug fixes (backward compatible)

Current version: **1.0.0**

## Support

- Documentation: `/docs`
- Issues: GitHub Issues
- Security: See SECURITY.md

---

*For more examples, see the `examples/` directory.*
