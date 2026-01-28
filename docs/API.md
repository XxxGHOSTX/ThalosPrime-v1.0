# Thalos Prime API Reference

## Python API

### AgentSession

Core session class providing deterministic lifecycle management.

#### Constructor

```python
AgentSession(
    session_id: str = None,
    state: SessionState = SessionState.INITIALIZED,
    metadata: Dict[str, Any] = None
)
```

**Parameters:**
- `session_id`: Unique session identifier (auto-generated if not provided)
- `state`: Initial session state (default: INITIALIZED)
- `metadata`: Optional metadata dictionary

#### Methods

##### `start() -> AgentSession`

Start the session. Returns new session instance.

**Raises:** `ValueError` if session cannot be started from current state.

```python
session = AgentSession()
running_session = session.start()
```

##### `pause() -> AgentSession`

Pause a running session. Returns new session instance.

**Raises:** `ValueError` if session is not running.

```python
paused_session = running_session.pause()
```

##### `resume() -> AgentSession`

Resume a paused session. Returns new session instance.

**Raises:** `ValueError` if session is not paused.

```python
resumed_session = paused_session.resume()
```

##### `terminate() -> AgentSession`

Terminate the session. Returns new session instance.

**Raises:** `ValueError` if session is already terminated.

```python
terminated_session = session.terminate()
```

##### `mark_error(error_message: str) -> AgentSession`

Mark session as errored.

**Parameters:**
- `error_message`: Description of the error

```python
error_session = session.mark_error("Connection timeout")
```

##### `to_dict() -> Dict[str, Any]`

Export session to dictionary representation.

```python
session_data = session.to_dict()
```

##### `from_dict(data: Dict[str, Any]) -> AgentSession`

Create session from dictionary representation.

```python
session = AgentSession.from_dict(session_data)
```

### SessionState

Enumeration of possible session states.

```python
class SessionState(Enum):
    INITIALIZED = "initialized"
    RUNNING = "running"
    PAUSED = "paused"
    RESUMING = "resuming"
    TERMINATED = "terminated"
    ERROR = "error"
```

### SessionManager

Manages multiple agent sessions with deterministic behavior.

#### Constructor

```python
SessionManager()
```

#### Methods

##### `create_session(metadata: Dict = None) -> AgentSession`

Create a new session.

```python
manager = SessionManager()
session = manager.create_session({"user": "alice"})
```

##### `get_session(session_id: str) -> Optional[AgentSession]`

Retrieve a session by ID.

```python
session = manager.get_session("session-id-123")
```

##### `start_session(session_id: str) -> AgentSession`

Start a session.

**Raises:** `KeyError` if session not found, `ValueError` if invalid state transition.

```python
started = manager.start_session(session_id)
```

##### `pause_session(session_id: str) -> AgentSession`

Pause a running session.

```python
paused = manager.pause_session(session_id)
```

##### `resume_session(session_id: str) -> AgentSession`

Resume a paused session.

```python
resumed = manager.resume_session(session_id)
```

##### `terminate_session(session_id: str) -> AgentSession`

Terminate a session.

```python
terminated = manager.terminate_session(session_id)
```

##### `list_sessions(state: SessionState = None) -> List[AgentSession]`

List all sessions, optionally filtered by state.

```python
all_sessions = manager.list_sessions()
running_sessions = manager.list_sessions(SessionState.RUNNING)
```

##### `get_session_count(state: SessionState = None) -> int`

Get count of sessions.

```python
total = manager.get_session_count()
running_count = manager.get_session_count(SessionState.RUNNING)
```

##### `cleanup_terminated_sessions() -> int`

Remove terminated sessions from registry. Returns count of removed sessions.

```python
removed = manager.cleanup_terminated_sessions()
```

### SessionPersistence

Provides deterministic session state persistence.

#### Constructor

```python
SessionPersistence(storage_path: str = "./session_data")
```

**Parameters:**
- `storage_path`: Path for storing session data

#### Methods

##### `save_session(session: AgentSession) -> bool`

Save session state to persistent storage.

```python
persistence = SessionPersistence()
success = persistence.save_session(session)
```

##### `load_session(session_id: str) -> Optional[AgentSession]`

Load session from persistent storage.

```python
session = persistence.load_session("session-id-123")
```

##### `delete_session(session_id: str) -> bool`

Delete session from persistent storage.

```python
deleted = persistence.delete_session("session-id-123")
```

##### `list_stored_sessions() -> List[str]`

List all session IDs in storage.

```python
session_ids = persistence.list_stored_sessions()
```

##### `cleanup_old_sessions(max_age_days: int = 30) -> int`

Remove old session data. Returns count of cleaned sessions.

```python
cleaned = persistence.cleanup_old_sessions(max_age_days=7)
```

### CISIntegration

Integration with Central Intelligence System.

#### Constructor

```python
CISIntegration(cis_endpoint: str = "localhost:8080")
```

#### Methods

##### `register_session_with_cis(session: AgentSession) -> Dict`

Register session with CIS.

```python
cis = CISIntegration()
response = cis.register_session_with_cis(session)
```

##### `notify_state_change(session, old_state, new_state) -> Dict`

Notify CIS of state change.

```python
response = cis.notify_state_change(session, old_state, new_state)
```

##### `request_decision(session, decision_context: Dict) -> Dict`

Request decision from CIS.

```python
decision = cis.request_decision(session, {"action": "continue"})
```

##### `report_metrics(session, metrics: Dict) -> bool`

Report metrics to CIS.

```python
cis.report_metrics(session, {"cpu": 45.2, "memory": 1024})
```

### MemorySubsystem

Deterministic memory management for sessions.

#### Constructor

```python
MemorySubsystem(max_working_memory: int = 1000)
```

#### Methods

##### `store_working_memory(session_id, key, value, metadata=None) -> bool`

Store data in working memory.

```python
memory = MemorySubsystem()
memory.store_working_memory(session_id, "task", "analysis")
```

##### `retrieve_working_memory(session_id, key) -> Optional[Any]`

Retrieve data from working memory.

```python
value = memory.retrieve_working_memory(session_id, "task")
```

##### `store_episodic_memory(session_id, episode: Dict) -> bool`

Store an episode in episodic memory.

```python
memory.store_episodic_memory(session_id, {"event": "completed"})
```

##### `retrieve_episodic_memory(session_id, limit=10) -> List[Dict]`

Retrieve recent episodes.

```python
episodes = memory.retrieve_episodic_memory(session_id, limit=5)
```

##### `store_semantic_memory(key, concept: Dict) -> bool`

Store concept in semantic memory.

```python
memory.store_semantic_memory("concept_x", {"definition": "..."})
```

##### `retrieve_semantic_memory(key) -> Optional[Any]`

Retrieve concept from semantic memory.

```python
concept = memory.retrieve_semantic_memory("concept_x")
```

### CodeGenerationModule

Deterministic code generation.

#### Constructor

```python
CodeGenerationModule()
```

#### Methods

##### `register_template(name: str, template: str) -> bool`

Register a code template.

```python
codegen = CodeGenerationModule()
codegen.register_template("function", "def {name}(): pass")
```

##### `generate_code(session_id, template_name, parameters, language="python") -> Dict`

Generate code using template.

```python
result = codegen.generate_code(
    session_id,
    "function",
    {"name": "process"}
)
```

##### `validate_code(code: str, language="python") -> Dict`

Validate generated code.

```python
validation = codegen.validate_code(code)
```

## Node.js API

### AgentSession

```javascript
const { AgentSession, SessionState } = require('./src/nodejs');

// Create session
const session = new AgentSession({ metadata: { user: 'alice' } });

// Lifecycle operations
let running = session.start();
let paused = running.pause();
let resumed = paused.resume();
let terminated = resumed.terminate();

// Serialization
const data = session.toObject();
const restored = AgentSession.fromObject(data);
```

### SessionManager

```javascript
const SessionManager = require('./src/nodejs/manager');

const manager = new SessionManager();

// Create and manage sessions
const session = manager.createSession({ user: 'alice' });
manager.startSession(session.sessionId);
manager.pauseSession(session.sessionId);
manager.resumeSession(session.sessionId);
manager.terminateSession(session.sessionId);

// List sessions
const allSessions = manager.listSessions();
const runningSessions = manager.listSessions(SessionState.RUNNING);

// Cleanup
const removed = manager.cleanupTerminatedSessions();
```

## CLI Commands

### Session Management

```bash
# Start new session
thalos start
thalos start --metadata '{"user": "alice"}'

# Get status
thalos status <session-id>

# Lifecycle operations
thalos pause <session-id>
thalos resume <session-id>
thalos stop <session-id>

# List sessions
thalos list
thalos list --state running

# Cleanup
thalos cleanup
```

## Examples

See [examples/basic_usage.py](../examples/basic_usage.py) for complete working examples.
