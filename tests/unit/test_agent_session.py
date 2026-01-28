"""
Tests for Agent Session Management

Validates session creation, lifecycle, and persistence.
"""

import json
import pytest
from pathlib import Path
from thalos_prime.session import AgentSession, SessionState


class TestAgentSession:
    """Test agent session functionality."""

    def test_create_session_with_defaults(self) -> None:
        """Test creating session with default parameters."""
        session = AgentSession()

        assert session.session_id is not None
        assert session.name.startswith("session-")
        assert session.state == SessionState.INITIALIZED
        assert session.config == {}

    def test_create_session_with_parameters(self) -> None:
        """Test creating session with explicit parameters."""
        config = {"model": "gpt-4", "temperature": 0.7}
        session = AgentSession(
            session_id="test-123",
            name="Test Session",
            config=config,
        )

        assert session.session_id == "test-123"
        assert session.name == "Test Session"
        assert session.config == config

    def test_session_lifecycle_operations(self) -> None:
        """Test session lifecycle operations."""
        session = AgentSession()

        # Start
        session.start()
        assert session.state == SessionState.RUNNING
        assert session.is_active

        # Pause
        session.pause()
        assert session.state == SessionState.PAUSED
        assert not session.is_active

        # Resume
        session.resume()
        assert session.state == SessionState.RUNNING
        assert session.is_active

        # Terminate
        session.terminate()
        assert session.state == SessionState.TERMINATED
        assert session.is_terminated
        assert not session.is_active

    def test_subsystem_state_management(self) -> None:
        """Test subsystem state updates."""
        session = AgentSession()

        # Update CIS state
        cis_state = {"mode": "active", "priority": "high"}
        session.update_cis_state(cis_state)
        assert session.get_cis_state() == cis_state

        # Update memory state
        memory_state = {"context": "test", "size": 1024}
        session.update_memory_state(memory_state)
        assert session.get_memory_state() == memory_state

        # Update codegen state
        codegen_state = {"language": "python", "version": "3.11"}
        session.update_codegen_state(codegen_state)
        assert session.get_codegen_state() == codegen_state

    def test_subsystem_state_isolation(self) -> None:
        """Test that subsystem states are isolated (no side effects)."""
        session = AgentSession()

        original_state = {"key": "value"}
        session.update_cis_state(original_state)

        # Modify returned state
        retrieved_state = session.get_cis_state()
        retrieved_state["key"] = "modified"

        # Original state should not be affected
        assert session.get_cis_state() == {"key": "value"}

    def test_session_serialization(self) -> None:
        """Test session serialization to dictionary."""
        session = AgentSession(
            session_id="test-456",
            name="Serialization Test",
            config={"test": True},
        )
        session.start()
        session.update_cis_state({"cis": "data"})

        data = session.to_dict()

        assert data["session_id"] == "test-456"
        assert data["name"] == "Serialization Test"
        assert data["config"]["test"] is True
        assert data["lifecycle"]["current_state"] == SessionState.RUNNING.value
        assert data["cis_state"] == {"cis": "data"}

    def test_session_deserialization(self) -> None:
        """Test session deserialization from dictionary."""
        original = AgentSession(session_id="test-789", name="Original")
        original.start()
        original.update_memory_state({"memory": "test"})

        # Serialize
        data = original.to_dict()

        # Deserialize
        restored = AgentSession.from_dict(data)

        assert restored.session_id == original.session_id
        assert restored.name == original.name
        assert restored.state == original.state
        assert restored.get_memory_state() == original.get_memory_state()

    def test_session_persistence(self, tmp_path: Path) -> None:
        """Test session save and load."""
        session_file = tmp_path / "session.json"

        # Create and save session
        original = AgentSession(session_id="persist-test")
        original.start()
        original.update_codegen_state({"gen": "code"})
        original.save(session_file)

        # Load session
        loaded = AgentSession.load(session_file)

        assert loaded.session_id == original.session_id
        assert loaded.state == original.state
        assert loaded.get_codegen_state() == original.get_codegen_state()

    def test_deterministic_session_creation(self) -> None:
        """Test that sessions with same ID are deterministic."""
        session1 = AgentSession(session_id="deterministic-id", config={"test": 1})
        session2 = AgentSession(session_id="deterministic-id", config={"test": 1})

        # Perform same operations
        session1.start()
        session2.start()

        assert session1.session_id == session2.session_id
        assert session1.state == session2.state
        assert session1.config == session2.config

    def test_no_implicit_state_changes(self) -> None:
        """Test that reading state doesn't change it."""
        session = AgentSession()
        session.start()

        initial_state = session.state

        # Multiple reads should not change state
        _ = session.state
        _ = session.is_active
        _ = session.get_cis_state()
        _ = session.to_dict()

        assert session.state == initial_state
