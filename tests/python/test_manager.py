"""
Test suite for Session Manager

Tests manager operations and session registry.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "python"))

from thalos_agent_session import SessionManager, SessionState


class TestSessionManager:
    """Test SessionManager functionality."""
    
    def test_create_session(self):
        """Test creating a new session."""
        manager = SessionManager()
        session = manager.create_session()
        
        assert session is not None
        assert session.state == SessionState.INITIALIZED
        assert manager.get_session(session.session_id) == session
    
    def test_create_session_with_metadata(self):
        """Test creating session with metadata."""
        manager = SessionManager()
        metadata = {"user": "test", "type": "worker"}
        session = manager.create_session(metadata)
        
        assert session.metadata == metadata
    
    def test_start_session(self):
        """Test starting a session through manager."""
        manager = SessionManager()
        session = manager.create_session()
        
        started = manager.start_session(session.session_id)
        assert started.state == SessionState.RUNNING
    
    def test_start_nonexistent_session(self):
        """Test starting a session that doesn't exist."""
        manager = SessionManager()
        
        with pytest.raises(KeyError, match="not found"):
            manager.start_session("nonexistent-id")
    
    def test_pause_resume_session(self):
        """Test pause and resume operations."""
        manager = SessionManager()
        session = manager.create_session()
        
        manager.start_session(session.session_id)
        paused = manager.pause_session(session.session_id)
        assert paused.state == SessionState.PAUSED
        
        resumed = manager.resume_session(session.session_id)
        assert resumed.state == SessionState.RUNNING
    
    def test_terminate_session(self):
        """Test terminating a session."""
        manager = SessionManager()
        session = manager.create_session()
        manager.start_session(session.session_id)
        
        terminated = manager.terminate_session(session.session_id)
        assert terminated.state == SessionState.TERMINATED
    
    def test_list_sessions(self):
        """Test listing all sessions."""
        manager = SessionManager()
        session1 = manager.create_session()
        session2 = manager.create_session()
        
        sessions = manager.list_sessions()
        assert len(sessions) == 2
        assert session1 in sessions
        assert session2 in sessions
    
    def test_list_sessions_by_state(self):
        """Test listing sessions filtered by state."""
        manager = SessionManager()
        session1 = manager.create_session()
        session2 = manager.create_session()
        
        manager.start_session(session1.session_id)
        
        running_sessions = manager.list_sessions(SessionState.RUNNING)
        assert len(running_sessions) == 1
        assert running_sessions[0].session_id == session1.session_id
        
        initialized_sessions = manager.list_sessions(SessionState.INITIALIZED)
        assert len(initialized_sessions) == 1
        assert initialized_sessions[0].session_id == session2.session_id
    
    def test_get_session_count(self):
        """Test getting session count."""
        manager = SessionManager()
        manager.create_session()
        manager.create_session()
        
        assert manager.get_session_count() == 2
    
    def test_get_session_count_by_state(self):
        """Test getting session count by state."""
        manager = SessionManager()
        session1 = manager.create_session()
        manager.create_session()
        
        manager.start_session(session1.session_id)
        
        assert manager.get_session_count(SessionState.RUNNING) == 1
        assert manager.get_session_count(SessionState.INITIALIZED) == 1
    
    def test_cleanup_terminated_sessions(self):
        """Test cleaning up terminated sessions."""
        manager = SessionManager()
        session1 = manager.create_session()
        session2 = manager.create_session()
        
        manager.start_session(session1.session_id)
        manager.terminate_session(session1.session_id)
        
        removed = manager.cleanup_terminated_sessions()
        assert removed == 1
        assert manager.get_session_count() == 1
        assert manager.get_session(session1.session_id) is None
        assert manager.get_session(session2.session_id) is not None
    
    def test_operation_log(self):
        """Test operation logging."""
        manager = SessionManager()
        session = manager.create_session()
        manager.start_session(session.session_id)
        
        log = manager.get_operation_log()
        assert len(log) >= 2
        assert log[0]["operation"] == "create"
        assert log[1]["operation"] == "start"
    
    def test_manager_isolation(self):
        """Test that manager instances are isolated."""
        manager1 = SessionManager()
        manager2 = SessionManager()
        
        session1 = manager1.create_session()
        
        assert manager1.get_session_count() == 1
        assert manager2.get_session_count() == 0
        assert manager2.get_session(session1.session_id) is None
