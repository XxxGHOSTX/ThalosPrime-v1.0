"""
Session Lifecycle Management

Defines deterministic state transitions for agent sessions.
All state changes are explicit and reversible.
"""

from enum import Enum
from typing import Optional, Dict, Any
from datetime import datetime


class SessionState(Enum):
    """
    Deterministic session states with explicit transitions.
    """

    INITIALIZED = "initialized"
    RUNNING = "running"
    PAUSED = "paused"
    RESUMED = "resumed"
    TERMINATED = "terminated"
    ERROR = "error"


class SessionLifecycle:
    """
    Manages deterministic state transitions for agent sessions.

    All transitions are explicit and validated. Invalid transitions
    raise exceptions rather than silently failing.
    """

    # Valid state transitions (explicit control)
    VALID_TRANSITIONS: Dict[SessionState, list[SessionState]] = {
        SessionState.INITIALIZED: [SessionState.RUNNING, SessionState.TERMINATED],
        SessionState.RUNNING: [
            SessionState.PAUSED,
            SessionState.TERMINATED,
            SessionState.ERROR,
        ],
        SessionState.PAUSED: [SessionState.RESUMED, SessionState.TERMINATED],
        SessionState.RESUMED: [SessionState.RUNNING, SessionState.TERMINATED],
        SessionState.TERMINATED: [],  # Terminal state
        SessionState.ERROR: [SessionState.TERMINATED],  # Can only terminate from error
    }

    def __init__(self, initial_state: SessionState = SessionState.INITIALIZED):
        """
        Initialize lifecycle with explicit starting state.

        Args:
            initial_state: Starting state (default: INITIALIZED)
        """
        self._current_state = initial_state
        self._state_history: list[tuple[SessionState, datetime]] = [
            (initial_state, datetime.now())
        ]

    @property
    def current_state(self) -> SessionState:
        """Get current state (read-only)."""
        return self._current_state

    @property
    def state_history(self) -> list[tuple[SessionState, datetime]]:
        """Get state transition history (read-only)."""
        return self._state_history.copy()

    def can_transition_to(self, new_state: SessionState) -> bool:
        """
        Check if transition to new state is valid.

        Args:
            new_state: Target state

        Returns:
            True if transition is valid, False otherwise
        """
        return new_state in self.VALID_TRANSITIONS.get(self._current_state, [])

    def transition_to(self, new_state: SessionState) -> None:
        """
        Perform explicit state transition.

        Args:
            new_state: Target state

        Raises:
            ValueError: If transition is invalid
        """
        if not self.can_transition_to(new_state):
            raise ValueError(
                f"Invalid transition from {self._current_state.value} "
                f"to {new_state.value}"
            )

        self._current_state = new_state
        self._state_history.append((new_state, datetime.now()))

    def start(self) -> None:
        """Start session (INITIALIZED -> RUNNING)."""
        self.transition_to(SessionState.RUNNING)

    def pause(self) -> None:
        """Pause session (RUNNING -> PAUSED)."""
        self.transition_to(SessionState.PAUSED)

    def resume(self) -> None:
        """Resume session (PAUSED -> RESUMED -> RUNNING)."""
        self.transition_to(SessionState.RESUMED)
        self.transition_to(SessionState.RUNNING)

    def terminate(self) -> None:
        """Terminate session (any state -> TERMINATED)."""
        self.transition_to(SessionState.TERMINATED)

    def error(self) -> None:
        """Transition to error state (RUNNING -> ERROR)."""
        self.transition_to(SessionState.ERROR)

    def to_dict(self) -> Dict[str, Any]:
        """
        Export lifecycle state as dictionary.

        Returns:
            Dictionary representation of lifecycle
        """
        return {
            "current_state": self._current_state.value,
            "state_history": [
                {"state": state.value, "timestamp": ts.isoformat()}
                for state, ts in self._state_history
            ],
        }
