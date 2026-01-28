"""
Tests for Session Lifecycle Management

Validates deterministic state transitions and explicit control.
"""

import pytest
from thalos_prime.session.lifecycle import SessionLifecycle, SessionState


class TestSessionLifecycle:
    """Test session lifecycle deterministic behavior."""

    def test_initial_state(self) -> None:
        """Test lifecycle starts in INITIALIZED state."""
        lifecycle = SessionLifecycle()
        assert lifecycle.current_state == SessionState.INITIALIZED

    def test_valid_transition_initialized_to_running(self) -> None:
        """Test valid transition from INITIALIZED to RUNNING."""
        lifecycle = SessionLifecycle()
        lifecycle.start()
        assert lifecycle.current_state == SessionState.RUNNING

    def test_valid_transition_running_to_paused(self) -> None:
        """Test valid transition from RUNNING to PAUSED."""
        lifecycle = SessionLifecycle()
        lifecycle.start()
        lifecycle.pause()
        assert lifecycle.current_state == SessionState.PAUSED

    def test_valid_transition_paused_to_resumed_to_running(self) -> None:
        """Test valid transition from PAUSED to RESUMED to RUNNING."""
        lifecycle = SessionLifecycle()
        lifecycle.start()
        lifecycle.pause()
        lifecycle.resume()
        assert lifecycle.current_state == SessionState.RUNNING

    def test_valid_transition_to_terminated(self) -> None:
        """Test valid transition to TERMINATED from various states."""
        # From INITIALIZED
        lifecycle = SessionLifecycle()
        lifecycle.terminate()
        assert lifecycle.current_state == SessionState.TERMINATED

        # From RUNNING
        lifecycle = SessionLifecycle()
        lifecycle.start()
        lifecycle.terminate()
        assert lifecycle.current_state == SessionState.TERMINATED

        # From PAUSED
        lifecycle = SessionLifecycle()
        lifecycle.start()
        lifecycle.pause()
        lifecycle.terminate()
        assert lifecycle.current_state == SessionState.TERMINATED

    def test_invalid_transition_raises_error(self) -> None:
        """Test invalid transitions raise ValueError."""
        lifecycle = SessionLifecycle()

        # Cannot pause from INITIALIZED
        with pytest.raises(ValueError):
            lifecycle.pause()

        # Cannot resume from RUNNING
        lifecycle.start()
        with pytest.raises(ValueError):
            lifecycle.resume()

    def test_cannot_transition_from_terminated(self) -> None:
        """Test that TERMINATED is a terminal state."""
        lifecycle = SessionLifecycle()
        lifecycle.start()
        lifecycle.terminate()

        # Cannot transition out of TERMINATED
        with pytest.raises(ValueError):
            lifecycle.start()

    def test_state_history_tracking(self) -> None:
        """Test state history is tracked correctly."""
        lifecycle = SessionLifecycle()

        assert len(lifecycle.state_history) == 1
        assert lifecycle.state_history[0][0] == SessionState.INITIALIZED

        lifecycle.start()
        assert len(lifecycle.state_history) == 2
        assert lifecycle.state_history[1][0] == SessionState.RUNNING

        lifecycle.pause()
        assert len(lifecycle.state_history) == 3
        assert lifecycle.state_history[2][0] == SessionState.PAUSED

    def test_can_transition_to(self) -> None:
        """Test can_transition_to method."""
        lifecycle = SessionLifecycle()

        # From INITIALIZED
        assert lifecycle.can_transition_to(SessionState.RUNNING)
        assert lifecycle.can_transition_to(SessionState.TERMINATED)
        assert not lifecycle.can_transition_to(SessionState.PAUSED)

        # From RUNNING
        lifecycle.start()
        assert lifecycle.can_transition_to(SessionState.PAUSED)
        assert lifecycle.can_transition_to(SessionState.TERMINATED)
        assert not lifecycle.can_transition_to(SessionState.RUNNING)

    def test_to_dict_serialization(self) -> None:
        """Test lifecycle serialization to dictionary."""
        lifecycle = SessionLifecycle()
        lifecycle.start()

        data = lifecycle.to_dict()

        assert data["current_state"] == SessionState.RUNNING.value
        assert len(data["state_history"]) == 2
        assert data["state_history"][0]["state"] == SessionState.INITIALIZED.value
        assert data["state_history"][1]["state"] == SessionState.RUNNING.value

    def test_deterministic_behavior(self) -> None:
        """Test that same sequence of operations produces same result."""
        # Run 1
        lifecycle1 = SessionLifecycle()
        lifecycle1.start()
        lifecycle1.pause()
        lifecycle1.resume()

        # Run 2
        lifecycle2 = SessionLifecycle()
        lifecycle2.start()
        lifecycle2.pause()
        lifecycle2.resume()

        # Both should be in RUNNING state
        assert lifecycle1.current_state == lifecycle2.current_state
        assert lifecycle1.current_state == SessionState.RUNNING
