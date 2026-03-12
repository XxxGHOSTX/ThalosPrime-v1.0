"""
Agent Session Implementation

Provides deterministic agent session with explicit control and state management.
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

from thalos_prime.session.lifecycle import SessionLifecycle, SessionState


class AgentSession:
    """
    Deterministic agent session with explicit lifecycle management.

    Features:
    - Explicit state transitions
    - Persistent storage
    - Integration with CIS, memory, and codegen subsystems
    - No implicit side effects
    """

    def __init__(
        self,
        session_id: Optional[str] = None,
        name: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize agent session with explicit parameters.

        Args:
            session_id: Unique session identifier (auto-generated if None)
            name: Human-readable session name
            config: Session configuration dictionary
        """
        self.session_id = session_id or str(uuid.uuid4())
        self.name = name or f"session-{self.session_id[:8]}"
        self.config = config or {}

        self._lifecycle = SessionLifecycle()
        self._created_at = datetime.now()
        self._updated_at = datetime.now()

        # Subsystem integration state (explicit)
        self._cis_state: Dict[str, Any] = {}
        self._memory_state: Dict[str, Any] = {}
        self._codegen_state: Dict[str, Any] = {}

    @property
    def state(self) -> SessionState:
        """Get current session state."""
        return self._lifecycle.current_state

    @property
    def is_active(self) -> bool:
        """Check if session is in an active state."""
        return self.state in [SessionState.RUNNING, SessionState.RESUMED]

    @property
    def is_terminated(self) -> bool:
        """Check if session is terminated."""
        return self.state == SessionState.TERMINATED

    @property
    def created_at(self) -> datetime:
        """Get session creation timestamp."""
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        """Get session last update timestamp."""
        return self._updated_at

    def start(self) -> None:
        """
        Start the session explicitly.

        Raises:
            ValueError: If session cannot be started from current state
        """
        self._lifecycle.start()
        self._updated_at = datetime.now()

    def pause(self) -> None:
        """
        Pause the session explicitly.

        Raises:
            ValueError: If session cannot be paused from current state
        """
        self._lifecycle.pause()
        self._updated_at = datetime.now()

    def resume(self) -> None:
        """
        Resume the session explicitly.

        Raises:
            ValueError: If session cannot be resumed from current state
        """
        self._lifecycle.resume()
        self._updated_at = datetime.now()

    def terminate(self) -> None:
        """
        Terminate the session explicitly.

        Raises:
            ValueError: If session cannot be terminated from current state
        """
        self._lifecycle.terminate()
        self._updated_at = datetime.now()

    def update_cis_state(self, state: Dict[str, Any]) -> None:
        """
        Update CIS (Control and Integration System) state explicitly.

        Args:
            state: New CIS state dictionary
        """
        self._cis_state = state.copy()
        self._updated_at = datetime.now()

    def update_memory_state(self, state: Dict[str, Any]) -> None:
        """
        Update memory subsystem state explicitly.

        Args:
            state: New memory state dictionary
        """
        self._memory_state = state.copy()
        self._updated_at = datetime.now()

    def update_codegen_state(self, state: Dict[str, Any]) -> None:
        """
        Update code generation subsystem state explicitly.

        Args:
            state: New codegen state dictionary
        """
        self._codegen_state = state.copy()
        self._updated_at = datetime.now()

    def get_cis_state(self) -> Dict[str, Any]:
        """Get CIS state (read-only copy)."""
        return self._cis_state.copy()

    def get_memory_state(self) -> Dict[str, Any]:
        """Get memory state (read-only copy)."""
        return self._memory_state.copy()

    def get_codegen_state(self) -> Dict[str, Any]:
        """Get codegen state (read-only copy)."""
        return self._codegen_state.copy()

    def to_dict(self) -> Dict[str, Any]:
        """
        Export session to dictionary (deterministic serialization).

        Returns:
            Complete session state as dictionary (deep copy)
        """
        return {
            "session_id": self.session_id,
            "name": self.name,
            "config": self.config.copy() if self.config else {},
            "lifecycle": self._lifecycle.to_dict(),
            "created_at": self._created_at.isoformat(),
            "updated_at": self._updated_at.isoformat(),
            "cis_state": self._cis_state.copy(),
            "memory_state": self._memory_state.copy(),
            "codegen_state": self._codegen_state.copy(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentSession":
        """
        Create session from dictionary (deterministic deserialization).

        Args:
            data: Session data dictionary

        Returns:
            Reconstructed AgentSession instance
        """
        session = cls(
            session_id=data["session_id"],
            name=data["name"],
            config=data.get("config", {}).copy() if data.get("config") else {},
        )

        session._created_at = datetime.fromisoformat(data["created_at"])
        session._updated_at = datetime.fromisoformat(data["updated_at"])
        session._cis_state = data.get("cis_state", {}).copy()
        session._memory_state = data.get("memory_state", {}).copy()
        session._codegen_state = data.get("codegen_state", {}).copy()

        # Restore lifecycle state and history
        lifecycle_data = data.get("lifecycle", {})
        current_state_str = lifecycle_data.get("current_state")
        if current_state_str:
            session._lifecycle._current_state = SessionState(current_state_str)
        
        # Restore state history
        state_history = lifecycle_data.get("state_history", [])
        if state_history:
            session._lifecycle._state_history = [
                (SessionState(entry["state"]), datetime.fromisoformat(entry["timestamp"]))
                for entry in state_history
            ]

        return session

    def save(self, path: Path) -> None:
        """
        Save session to file (deterministic persistence).

        Args:
            path: File path for session storage
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, sort_keys=True, ensure_ascii=False)

    @classmethod
    def load(cls, path: Path) -> "AgentSession":
        """
        Load session from file (deterministic restoration).

        Args:
            path: File path to load from

        Returns:
            Loaded AgentSession instance
        """
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)
