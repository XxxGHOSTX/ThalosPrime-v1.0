"""
Tests for Session Manager

Validates multi-session management and persistence.
"""

import pytest
from pathlib import Path
from thalos_prime.session import SessionManager, SessionState


class TestSessionManager:
    """Test session manager functionality."""

    def test_create_session(self) -> None:
        """Test creating a new session."""
        manager = SessionManager()
        session = manager.create_session(name="Test Session")

        assert session is not None
        assert session.name == "Test Session"
        assert session.state == SessionState.INITIALIZED

    def test_get_session(self) -> None:
        """Test retrieving a session by ID."""
        manager = SessionManager()
        created = manager.create_session(name="Retrievable")

        retrieved = manager.get_session(created.session_id)

        assert retrieved is not None
        assert retrieved.session_id == created.session_id
        assert retrieved.name == created.name

    def test_get_nonexistent_session(self) -> None:
        """Test retrieving non-existent session returns None."""
        manager = SessionManager()
        session = manager.get_session("nonexistent-id")

        assert session is None

    def test_list_all_sessions(self) -> None:
        """Test listing all sessions."""
        manager = SessionManager()

        session1 = manager.create_session(name="Session 1")
        session2 = manager.create_session(name="Session 2")
        session3 = manager.create_session(name="Session 3")

        all_sessions = manager.list_sessions()

        assert len(all_sessions) == 3
        session_ids = [s.session_id for s in all_sessions]
        assert session1.session_id in session_ids
        assert session2.session_id in session_ids
        assert session3.session_id in session_ids

    def test_list_sessions_by_state(self) -> None:
        """Test filtering sessions by state."""
        manager = SessionManager()

        session1 = manager.create_session(name="Running Session")
        session1.start()

        session2 = manager.create_session(name="Paused Session")
        session2.start()
        session2.pause()

        session3 = manager.create_session(name="Initialized Session")

        # Filter by RUNNING
        running_sessions = manager.list_sessions(state_filter=SessionState.RUNNING)
        assert len(running_sessions) == 1
        assert running_sessions[0].session_id == session1.session_id

        # Filter by PAUSED
        paused_sessions = manager.list_sessions(state_filter=SessionState.PAUSED)
        assert len(paused_sessions) == 1
        assert paused_sessions[0].session_id == session2.session_id

        # Filter by INITIALIZED
        init_sessions = manager.list_sessions(state_filter=SessionState.INITIALIZED)
        assert len(init_sessions) == 1
        assert init_sessions[0].session_id == session3.session_id

    def test_delete_session(self) -> None:
        """Test deleting a session."""
        manager = SessionManager()
        session = manager.create_session(name="To Delete")
        session_id = session.session_id

        # Delete session
        result = manager.delete_session(session_id)

        assert result is True
        assert manager.get_session(session_id) is None

    def test_delete_nonexistent_session(self) -> None:
        """Test deleting non-existent session returns False."""
        manager = SessionManager()
        result = manager.delete_session("nonexistent-id")

        assert result is False

    def test_delete_terminates_active_session(self) -> None:
        """Test deleting an active session terminates it first."""
        manager = SessionManager()
        session = manager.create_session(name="Active Session")
        session.start()
        session_id = session.session_id

        # Delete while running
        manager.delete_session(session_id)

        # Session should have been terminated
        assert session.is_terminated

    def test_save_and_load_session(self, tmp_path: Path) -> None:
        """Test saving and loading a session."""
        manager = SessionManager(storage_dir=tmp_path)

        # Create and save session
        original = manager.create_session(name="Saveable")
        original.start()
        manager.save_session(original.session_id)

        # Create new manager and load session
        new_manager = SessionManager(storage_dir=tmp_path)
        loaded = new_manager.load_session(original.session_id)

        assert loaded.session_id == original.session_id
        assert loaded.name == original.name
        assert loaded.state == original.state

    def test_save_nonexistent_session_raises_error(self) -> None:
        """Test saving non-existent session raises KeyError."""
        manager = SessionManager()

        with pytest.raises(KeyError):
            manager.save_session("nonexistent-id")

    def test_load_all_sessions(self, tmp_path: Path) -> None:
        """Test loading all sessions from storage."""
        manager1 = SessionManager(storage_dir=tmp_path)

        # Create and save multiple sessions
        session1 = manager1.create_session(name="Session 1")
        session2 = manager1.create_session(name="Session 2")
        manager1.save_all()

        # Create new manager and load all
        manager2 = SessionManager(storage_dir=tmp_path)
        manager2.load_all()

        loaded_sessions = manager2.list_sessions()
        assert len(loaded_sessions) == 2

        loaded_ids = [s.session_id for s in loaded_sessions]
        assert session1.session_id in loaded_ids
        assert session2.session_id in loaded_ids

    def test_get_statistics(self) -> None:
        """Test getting session statistics."""
        manager = SessionManager()

        # Create sessions in different states
        s1 = manager.create_session(name="S1")
        s1.start()

        s2 = manager.create_session(name="S2")
        s2.start()
        s2.pause()

        s3 = manager.create_session(name="S3")

        s4 = manager.create_session(name="S4")
        s4.start()
        s4.terminate()

        stats = manager.get_statistics()

        assert stats["total"] == 4
        assert stats["running"] == 1
        assert stats["paused"] == 1
        assert stats["initialized"] == 1
        assert stats["terminated"] == 1

    def test_deterministic_session_management(self) -> None:
        """Test that session management is deterministic."""
        # Manager 1
        manager1 = SessionManager()
        s1 = manager1.create_session(name="Test")
        s1.start()

        # Manager 2
        manager2 = SessionManager()
        s2 = manager2.create_session(name="Test")
        s2.start()

        # Both sessions should be in same state
        assert s1.state == s2.state
        assert s1.name == s2.name
