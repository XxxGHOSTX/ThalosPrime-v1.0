"""
Test suite for Session Persistence

Tests deterministic persistence operations.
"""

import pytest
import sys
import tempfile
import shutil
import time
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "python"))

from thalos_agent_session import AgentSession, SessionPersistence, SessionState


class TestSessionPersistence:
    """Test SessionPersistence functionality."""
    
    @pytest.fixture
    def temp_storage(self):
        """Create temporary storage directory."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    def test_save_session(self, temp_storage):
        """Test saving a session."""
        persistence = SessionPersistence(temp_storage)
        session = AgentSession()
        
        result = persistence.save_session(session)
        assert result is True
        
        # Verify file exists
        session_file = Path(temp_storage) / f"{session.session_id}.json"
        assert session_file.exists()
    
    def test_load_session(self, temp_storage):
        """Test loading a saved session."""
        persistence = SessionPersistence(temp_storage)
        session = AgentSession(metadata={"test": "data"})
        session = session.start()
        
        persistence.save_session(session)
        loaded = persistence.load_session(session.session_id)
        
        assert loaded is not None
        assert loaded.session_id == session.session_id
        assert loaded.state == session.state
        assert loaded.metadata == session.metadata
    
    def test_load_nonexistent_session(self, temp_storage):
        """Test loading a session that doesn't exist."""
        persistence = SessionPersistence(temp_storage)
        loaded = persistence.load_session("nonexistent-id")
        
        assert loaded is None
    
    def test_delete_session(self, temp_storage):
        """Test deleting a session."""
        persistence = SessionPersistence(temp_storage)
        session = AgentSession()
        
        persistence.save_session(session)
        result = persistence.delete_session(session.session_id)
        
        assert result is True
        
        # Verify file is deleted
        session_file = Path(temp_storage) / f"{session.session_id}.json"
        assert not session_file.exists()
    
    def test_delete_nonexistent_session(self, temp_storage):
        """Test deleting a session that doesn't exist."""
        persistence = SessionPersistence(temp_storage)
        result = persistence.delete_session("nonexistent-id")
        
        assert result is False
    
    def test_list_stored_sessions(self, temp_storage):
        """Test listing stored sessions."""
        persistence = SessionPersistence(temp_storage)
        session1 = AgentSession()
        session2 = AgentSession()
        
        persistence.save_session(session1)
        persistence.save_session(session2)
        
        session_ids = persistence.list_stored_sessions()
        assert len(session_ids) == 2
        assert session1.session_id in session_ids
        assert session2.session_id in session_ids
    
    def test_persistence_atomicity(self, temp_storage):
        """Test that save operations are atomic."""
        persistence = SessionPersistence(temp_storage)
        session = AgentSession()
        
        # Save initial version
        persistence.save_session(session)
        
        # Update and save again
        session = session.start()
        persistence.save_session(session)
        
        # Load and verify we have the latest version
        loaded = persistence.load_session(session.session_id)
        assert loaded.state == SessionState.RUNNING
    
    def test_session_state_preservation(self, temp_storage):
        """Test that complex session state is preserved."""
        persistence = SessionPersistence(temp_storage)
        
        # Create session with complex state
        session = AgentSession(metadata={"key": "value"})
        session = session.start()
        session = session.pause()
        session = session.resume()
        
        # Save and load
        persistence.save_session(session)
        loaded = persistence.load_session(session.session_id)
        
        # Verify state history preserved
        assert len(loaded.state_history) == 3
        assert loaded.transition_count == 3
        assert loaded.metadata["key"] == "value"

    def test_save_session_handles_exception(self, temp_storage):
        """Test that save_session handles filesystem errors gracefully."""
        persistence = SessionPersistence(temp_storage)
        session = AgentSession()

        with patch("builtins.open", side_effect=OSError("Permission denied")):
            result = persistence.save_session(session)

        assert result is False

    def test_load_session_handles_corrupt_json(self, temp_storage):
        """Test that load_session handles corrupt JSON gracefully."""
        persistence = SessionPersistence(temp_storage)
        session = AgentSession()

        # Write corrupt JSON
        session_file = Path(temp_storage) / f"{session.session_id}.json"
        session_file.write_text("{ invalid json }")

        loaded = persistence.load_session(session.session_id)
        assert loaded is None

    def test_delete_session_handles_exception(self, temp_storage):
        """Test that delete_session handles filesystem errors gracefully."""
        persistence = SessionPersistence(temp_storage)
        session = AgentSession()

        persistence.save_session(session)

        with patch.object(Path, "unlink", side_effect=OSError("Permission denied")):
            result = persistence.delete_session(session.session_id)

        assert result is False

    def test_list_stored_sessions_handles_exception(self, temp_storage):
        """Test that list_stored_sessions handles errors gracefully."""
        persistence = SessionPersistence(temp_storage)

        with patch.object(Path, "glob", side_effect=OSError("Permission denied")):
            result = persistence.list_stored_sessions()

        assert result == []

    def test_cleanup_old_sessions(self, temp_storage):
        """Test that cleanup_old_sessions removes files older than max_age_days."""
        persistence = SessionPersistence(temp_storage)
        session = AgentSession()

        persistence.save_session(session)

        # Patch time.time to simulate the file is old
        session_file = Path(temp_storage) / f"{session.session_id}.json"
        # The file was just created, so we simulate a max_age_days=0
        removed = persistence.cleanup_old_sessions(max_age_days=0)

        assert removed >= 1
        assert not session_file.exists()

    def test_cleanup_old_sessions_keeps_recent(self, temp_storage):
        """Test that cleanup_old_sessions keeps recent files."""
        persistence = SessionPersistence(temp_storage)
        session = AgentSession()

        persistence.save_session(session)

        # Clean up with a large max_age (30 days) - file should NOT be removed
        removed = persistence.cleanup_old_sessions(max_age_days=30)

        assert removed == 0

    def test_cleanup_old_sessions_handles_exception(self, temp_storage):
        """Test that cleanup_old_sessions handles errors gracefully."""
        persistence = SessionPersistence(temp_storage)

        with patch.object(Path, "glob", side_effect=OSError("Permission denied")):
            count = persistence.cleanup_old_sessions()

        assert count == 0
