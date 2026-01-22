"""
Integration Tests for Session Management

Tests full session lifecycle with persistence.
"""

import pytest
from pathlib import Path
from thalos_prime.session import SessionManager, SessionState


class TestSessionIntegration:
    """Integration tests for session management."""
    
    def test_full_session_lifecycle(self, tmp_path: Path) -> None:
        """Test complete session lifecycle with persistence."""
        manager = SessionManager(storage_dir=tmp_path)
        
        # Create session
        session = manager.create_session(name="Integration Test")
        session_id = session.session_id
        
        # Start session
        session.start()
        assert session.is_active
        manager.save_session(session_id)
        
        # Pause session
        session.pause()
        assert not session.is_active
        manager.save_session(session_id)
        
        # Load in new manager
        new_manager = SessionManager(storage_dir=tmp_path)
        loaded = new_manager.load_session(session_id)
        assert loaded.state == SessionState.PAUSED
        
        # Resume and terminate
        loaded.resume()
        assert loaded.is_active
        loaded.terminate()
        assert loaded.is_terminated
        new_manager.save_session(session_id)
        
        # Verify final state
        final_manager = SessionManager(storage_dir=tmp_path)
        final_session = final_manager.load_session(session_id)
        assert final_session.is_terminated
    
    def test_multiple_sessions_with_subsystems(self, tmp_path: Path) -> None:
        """Test multiple sessions with subsystem integration."""
        manager = SessionManager(storage_dir=tmp_path)
        
        # Session 1: CIS focus
        s1 = manager.create_session(name="CIS Session")
        s1.start()
        s1.update_cis_state({"mode": "autonomous", "priority": 10})
        
        # Session 2: Memory focus
        s2 = manager.create_session(name="Memory Session")
        s2.start()
        s2.update_memory_state({"cache_size": 2048, "enabled": True})
        
        # Session 3: Codegen focus
        s3 = manager.create_session(name="Codegen Session")
        s3.start()
        s3.update_codegen_state({"language": "python", "style": "pep8"})
        
        # Save all
        manager.save_all()
        
        # Load in new manager
        new_manager = SessionManager(storage_dir=tmp_path)
        new_manager.load_all()
        
        # Verify all sessions loaded correctly
        loaded_sessions = new_manager.list_sessions()
        assert len(loaded_sessions) == 3
        
        # Verify subsystem states preserved
        loaded_s1 = new_manager.get_session(s1.session_id)
        assert loaded_s1.get_cis_state()["mode"] == "autonomous"
        
        loaded_s2 = new_manager.get_session(s2.session_id)
        assert loaded_s2.get_memory_state()["cache_size"] == 2048
        
        loaded_s3 = new_manager.get_session(s3.session_id)
        assert loaded_s3.get_codegen_state()["language"] == "python"
    
    def test_session_isolation(self) -> None:
        """Test that sessions are isolated from each other."""
        manager = SessionManager()
        
        s1 = manager.create_session(name="Session 1")
        s2 = manager.create_session(name="Session 2")
        
        # Update s1 state
        s1.start()
        s1.update_cis_state({"session": "1"})
        
        # s2 should not be affected
        assert s2.state == SessionState.INITIALIZED
        assert s2.get_cis_state() == {}
        
        # Update s2 state
        s2.start()
        s2.update_cis_state({"session": "2"})
        
        # Verify isolation
        assert s1.get_cis_state()["session"] == "1"
        assert s2.get_cis_state()["session"] == "2"
