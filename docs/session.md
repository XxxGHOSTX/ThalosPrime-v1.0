# Agent Session Management

## Overview

The Agent Session Management module provides deterministic lifecycle control for AI agent sessions in Thalos Prime. All operations are explicit with no hidden side effects.

## Architecture

### Core Components

1. **SessionLifecycle** - Manages state transitions
2. **AgentSession** - Individual session implementation
3. **SessionManager** - Multi-session coordinator

### State Machine

```
INITIALIZED → RUNNING → PAUSED → RESUMED → RUNNING
       ↓         ↓         ↓                    ↓
    TERMINATED ← TERMINATED ← TERMINATED ← TERMINATED
```

Valid transitions:
- `INITIALIZED` → `RUNNING`, `TERMINATED`
- `RUNNING` → `PAUSED`, `TERMINATED`, `ERROR`
- `PAUSED` → `RESUMED`, `TERMINATED`
- `RESUMED` → `RUNNING`, `TERMINATED`
- `ERROR` → `TERMINATED`
- `TERMINATED` → (terminal state)

## Usage

### Creating Sessions

```python
from thalos_prime import SessionManager

manager = SessionManager(storage_dir=".thalos/sessions")

# Create with default config
session = manager.create_session()

# Create with custom config
session = manager.create_session(
    name="my-agent",
    config={
        "model": "gpt-4",
        "temperature": 0.7,
        "max_tokens": 2048
    }
)
```

### Lifecycle Operations

```python
# Start session
session.start()
assert session.state == SessionState.RUNNING
assert session.is_active == True

# Pause session
session.pause()
assert session.state == SessionState.PAUSED
assert session.is_active == False

# Resume session
session.resume()
assert session.state == SessionState.RUNNING

# Terminate session
session.terminate()
assert session.is_terminated == True
```

### Subsystem Integration

```python
# Update CIS state
session.update_cis_state({
    "mode": "autonomous",
    "priority": "high"
})

# Update memory state
session.update_memory_state({
    "cache_size": 2048,
    "enabled": True
})

# Update codegen state
session.update_codegen_state({
    "language": "python",
    "style": "pep8"
})

# Read states (returns copies - no side effects)
cis_state = session.get_cis_state()
memory_state = session.get_memory_state()
codegen_state = session.get_codegen_state()
```

### Persistence

```python
from pathlib import Path

# Save session
session_file = Path(".thalos/sessions/my-session.json")
session.save(session_file)

# Load session
loaded_session = AgentSession.load(session_file)

# With manager
manager.save_session(session.session_id)
manager.save_all()  # Save all sessions

# Load with manager
loaded = manager.load_session(session_id)
manager.load_all()  # Load all from storage
```

### Multi-Session Management

```python
# Create multiple sessions
sessions = [
    manager.create_session(name=f"worker-{i}")
    for i in range(5)
]

# Filter by state
running = manager.list_sessions(state_filter=SessionState.RUNNING)
paused = manager.list_sessions(state_filter=SessionState.PAUSED)

# Get statistics
stats = manager.get_statistics()
print(f"Total: {stats['total']}")
print(f"Running: {stats['running']}")
print(f"Paused: {stats['paused']}")

# Delete session
manager.delete_session(session_id)
```

## CLI Commands

### Start Session

```bash
thalos session start --name "my-session" --config '{"model": "gpt-4"}'
```

Output:
```
Started session: abc123...
Name: my-session
State: running
```

### List Sessions

```bash
# List all
thalos session list

# Filter by state
thalos session list --state running
thalos session list --state paused
```

### Session Status

```bash
# Specific session
thalos session status abc123

# All sessions with stats
thalos session status --all
```

### Pause/Resume

```bash
thalos session pause abc123
thalos session resume abc123
```

### Stop Session

```bash
thalos session stop abc123
```

## Deterministic Properties

### State Transitions

All state transitions are:
- **Explicit**: Must be invoked explicitly
- **Validated**: Invalid transitions raise `ValueError`
- **Tracked**: Full history maintained
- **Reversible**: Can always terminate

### No Implicit Changes

```python
# Reading state never changes it
state1 = session.state
state2 = session.state
assert state1 == state2  # Always true

# Subsystem states are copied
cis_state = session.get_cis_state()
cis_state["modified"] = True
# Original unchanged
assert "modified" not in session.get_cis_state()
```

### Reproducibility

```python
# Same operations = same result
session1 = AgentSession(session_id="test")
session1.start()
session1.pause()

session2 = AgentSession(session_id="test")
session2.start()
session2.pause()

assert session1.state == session2.state
```

## Error Handling

```python
from thalos_prime.session import SessionState

try:
    session.pause()  # Can only pause RUNNING
except ValueError as e:
    print(f"Invalid transition: {e}")

# Check before transitioning
if session.state == SessionState.RUNNING:
    session.pause()
```

## Testing

### Unit Tests

```python
def test_session_lifecycle():
    session = AgentSession()
    session.start()
    assert session.is_active
    
    session.pause()
    assert not session.is_active
    
    session.resume()
    assert session.is_active

def test_determinism():
    # Multiple runs produce same result
    for _ in range(3):
        s = AgentSession(session_id="test")
        s.start()
        assert s.state == SessionState.RUNNING
```

### Integration Tests

```python
def test_persistence(tmp_path):
    manager = SessionManager(storage_dir=tmp_path)
    session = manager.create_session()
    session.start()
    manager.save_session(session.session_id)
    
    # Load in new manager
    new_manager = SessionManager(storage_dir=tmp_path)
    loaded = new_manager.load_session(session.session_id)
    assert loaded.state == SessionState.RUNNING
```

## Best Practices

1. **Always check state before operations**
   ```python
   if not session.is_terminated:
       session.terminate()
   ```

2. **Use context managers for cleanup**
   ```python
   def with_session(manager, name):
       session = manager.create_session(name=name)
       session.start()
       try:
           yield session
       finally:
           session.terminate()
           manager.save_session(session.session_id)
   ```

3. **Persist regularly**
   ```python
   # After important state changes
   session.update_cis_state(new_state)
   manager.save_session(session.session_id)
   ```

4. **Handle errors gracefully**
   ```python
   try:
       session.resume()
   except ValueError:
       # Session not in pausable state
       if session.state == SessionState.TERMINATED:
           session = manager.create_session()
           session.start()
   ```

## See Also

- [API Reference](api.md) - Full API documentation
- [DevOps Automation](automation.md) - Workflow automation
- [Deployment Guide](deployment.md) - Production deployment
