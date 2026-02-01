"""
Agent Session State Management

Provides deterministic session lifecycle management with explicit state transitions.
All state changes are atomic and traceable.
"""

from enum import Enum
from datetime import datetime, UTC
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from uuid import uuid4


class SessionState(Enum):
    """Deterministic session states with explicit transitions."""

    INITIALIZED = "initialized"
    RUNNING = "running"
    PAUSED = "paused"
    TERMINATED = "terminated"
    ERROR = "error"


@dataclass
class AgentSession:
    """
    Deterministic agent session with explicit lifecycle management.

    All operations are explicit and side-effect free. State changes
    are atomic and validated before application.
    """

    session_id: str = field(default_factory=lambda: str(uuid4()))
    state: SessionState = SessionState.INITIALIZED
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None

    # Deterministic state tracking
    state_history: list = field(default_factory=list)
    transition_count: int = 0

    def start(self) -> "AgentSession":
        """
        Explicitly start the session.

        Returns:
            New session instance with updated state (immutable operation).
        """
        if self.state != SessionState.INITIALIZED:
            raise ValueError(
                f"Cannot start session from state {self.state}. "
                f"Must be INITIALIZED. Use resume() for paused sessions."
            )

        return self._transition_to(SessionState.RUNNING)

    def pause(self) -> "AgentSession":
        """
        Explicitly pause the session.

        Returns:
            New session instance with updated state (immutable operation).
        """
        if self.state != SessionState.RUNNING:
            raise ValueError(
                f"Cannot pause session from state {self.state}. " f"Must be RUNNING."
            )

        return self._transition_to(SessionState.PAUSED)

    def resume(self) -> "AgentSession":
        """
        Explicitly resume the session.

        Returns:
            New session instance with updated state (immutable operation).
        """
        if self.state != SessionState.PAUSED:
            raise ValueError(
                f"Cannot resume session from state {self.state}. " f"Must be PAUSED."
            )

        return self._transition_to(SessionState.RUNNING)

    def terminate(self) -> "AgentSession":
        """
        Explicitly terminate the session.

        Returns:
            New session instance with updated state (immutable operation).
        """
        if self.state == SessionState.TERMINATED:
            raise ValueError("Session is already terminated.")

        return self._transition_to(SessionState.TERMINATED)

    def mark_error(self, error_message: str) -> "AgentSession":
        """
        Explicitly mark session as errored.

        Args:
            error_message: Description of the error

        Returns:
            New session instance with error state (immutable operation).
        """
        return self._transition_to(SessionState.ERROR, error_message=error_message)

    def _transition_to(
        self, new_state: SessionState, error_message: Optional[str] = None
    ) -> "AgentSession":
        """
        Internal method for deterministic state transitions.

        Creates a new session instance with updated state, preserving
        immutability and explicit control.
        """
        new_session = AgentSession(
            session_id=self.session_id,
            state=new_state,
            created_at=self.created_at,
            updated_at=datetime.now(UTC),
            metadata=self.metadata.copy(),
            error_message=(
                error_message if error_message is not None else self.error_message
            ),
            state_history=self.state_history
            + [
                {
                    "from": self.state.value,
                    "to": new_state.value,
                    "timestamp": datetime.now(UTC).isoformat(),
                }
            ],
            transition_count=self.transition_count + 1,
        )

        return new_session

    def to_dict(self) -> Dict[str, Any]:
        """
        Export session to deterministic dictionary representation.

        Returns:
            Dictionary with all session data for serialization.
        """
        return {
            "session_id": self.session_id,
            "state": self.state.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "metadata": self.metadata,
            "error_message": self.error_message,
            "state_history": self.state_history,
            "transition_count": self.transition_count,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentSession":
        """
        Create session from deterministic dictionary representation.

        Args:
            data: Dictionary with session data

        Returns:
            AgentSession instance
        """
        return cls(
            session_id=data["session_id"],
            state=SessionState(data["state"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            metadata=data.get("metadata", {}),
            error_message=data.get("error_message"),
            state_history=data.get("state_history", []),
            transition_count=data.get("transition_count", 0),
        )
