"""
Test suite for Agent Session Module

Tests deterministic behavior and state transitions.
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "python"))

from thalos_agent_session import AgentSession, SessionState


class TestAgentSession:
    """Test AgentSession deterministic behavior."""
    
    def test_session_initialization(self):
        """Test session is initialized with correct default state."""
        session = AgentSession()
        assert session.state == SessionState.INITIALIZED
        assert session.session_id is not None
        assert isinstance(session.created_at, datetime)
        assert session.transition_count == 0
    
    def test_session_start_from_initialized(self):
        """Test starting a session from initialized state."""
        session = AgentSession()
        started_session = session.start()
        
        assert started_session.state == SessionState.RUNNING
        assert started_session.session_id == session.session_id
        assert started_session.transition_count == 1
        assert len(started_session.state_history) == 1
    
    def test_session_cannot_start_from_running(self):
        """Test that running session cannot be started again."""
        session = AgentSession()
        running_session = session.start()
        
        with pytest.raises(ValueError, match="Cannot start session"):
            running_session.start()
    
    def test_session_pause_from_running(self):
        """Test pausing a running session."""
        session = AgentSession()
        running_session = session.start()
        paused_session = running_session.pause()
        
        assert paused_session.state == SessionState.PAUSED
        assert paused_session.transition_count == 2
    
    def test_session_cannot_pause_from_initialized(self):
        """Test that initialized session cannot be paused."""
        session = AgentSession()
        
        with pytest.raises(ValueError, match="Cannot pause session"):
            session.pause()
    
    def test_session_resume_from_paused(self):
        """Test resuming a paused session."""
        session = AgentSession()
        running_session = session.start()
        paused_session = running_session.pause()
        resumed_session = paused_session.resume()
        
        assert resumed_session.state == SessionState.RUNNING
        assert resumed_session.transition_count == 3
    
    def test_session_terminate(self):
        """Test terminating a session."""
        session = AgentSession()
        running_session = session.start()
        terminated_session = running_session.terminate()
        
        assert terminated_session.state == SessionState.TERMINATED
    
    def test_session_cannot_terminate_twice(self):
        """Test that terminated session cannot be terminated again."""
        session = AgentSession()
        running_session = session.start()
        terminated_session = running_session.terminate()
        
        with pytest.raises(ValueError, match="already terminated"):
            terminated_session.terminate()
    
    def test_session_mark_error(self):
        """Test marking session as errored."""
        session = AgentSession()
        error_session = session.mark_error("Test error")
        
        assert error_session.state == SessionState.ERROR
        assert error_session.error_message == "Test error"
    
    def test_session_immutability(self):
        """Test that session operations create new instances."""
        session1 = AgentSession()
        session2 = session1.start()
        
        # Original session should be unchanged
        assert session1.state == SessionState.INITIALIZED
        assert session2.state == SessionState.RUNNING
        assert session1.session_id == session2.session_id
    
    def test_session_state_history_tracking(self):
        """Test that state history is properly tracked."""
        session = AgentSession()
        session = session.start()
        session = session.pause()
        session = session.resume()
        
        assert len(session.state_history) == 3
        assert session.state_history[0]["from"] == "initialized"
        assert session.state_history[0]["to"] == "running"
        assert session.state_history[1]["from"] == "running"
        assert session.state_history[1]["to"] == "paused"
    
    def test_session_metadata(self):
        """Test session metadata handling."""
        metadata = {"user": "test", "priority": "high"}
        session = AgentSession(metadata=metadata)
        
        assert session.metadata == metadata
        
        # Verify metadata is copied (not referenced)
        started = session.start()
        started.metadata["new_key"] = "value"
        assert "new_key" not in session.metadata
    
    def test_session_serialization(self):
        """Test session to_dict and from_dict."""
        session = AgentSession(metadata={"test": "data"})
        session = session.start()
        
        # Serialize
        data = session.to_dict()
        assert data["session_id"] == session.session_id
        assert data["state"] == "running"
        assert data["metadata"]["test"] == "data"
        
        # Deserialize
        restored = AgentSession.from_dict(data)
        assert restored.session_id == session.session_id
        assert restored.state == session.state
        assert restored.metadata == session.metadata
