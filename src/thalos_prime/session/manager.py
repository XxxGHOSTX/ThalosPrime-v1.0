"""
Session Manager

Manages multiple agent sessions with deterministic operations.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional

from thalos_prime.session.agent_session import AgentSession
from thalos_prime.session.lifecycle import SessionState


class SessionManager:
    """
    Deterministic manager for multiple agent sessions.
    
    Provides:
    - Session creation and deletion
    - Session persistence and loading
    - Session listing and queries
    - No implicit state changes
    """
    
    def __init__(self, storage_dir: Optional[Path] = None):
        """
        Initialize session manager.
        
        Args:
            storage_dir: Directory for session persistence (default: ./.thalos/sessions)
        """
        self.storage_dir = storage_dir or Path(".thalos/sessions")
        self._sessions: Dict[str, AgentSession] = {}
    
    def create_session(
        self,
        name: Optional[str] = None,
        config: Optional[Dict] = None,
    ) -> AgentSession:
        """
        Create new agent session explicitly.
        
        Args:
            name: Session name
            config: Session configuration
            
        Returns:
            New AgentSession instance
        """
        session = AgentSession(name=name, config=config)
        self._sessions[session.session_id] = session
        return session
    
    def get_session(self, session_id: str) -> Optional[AgentSession]:
        """
        Get session by ID.
        
        Args:
            session_id: Session identifier
            
        Returns:
            AgentSession if found, None otherwise
        """
        return self._sessions.get(session_id)
    
    def list_sessions(
        self,
        state_filter: Optional[SessionState] = None,
    ) -> List[AgentSession]:
        """
        List all sessions with optional state filter.
        
        Args:
            state_filter: Filter by session state (None = all sessions)
            
        Returns:
            List of matching sessions
        """
        sessions = list(self._sessions.values())
        
        if state_filter:
            sessions = [s for s in sessions if s.state == state_filter]
        
        return sessions
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete session explicitly.
        
        Args:
            session_id: Session identifier
            
        Returns:
            True if deleted, False if not found
        """
        if session_id in self._sessions:
            session = self._sessions[session_id]
            
            # Terminate if not already terminated
            if not session.is_terminated:
                session.terminate()
            
            del self._sessions[session_id]
            
            # Remove persisted file if exists
            session_file = self.storage_dir / f"{session_id}.json"
            if session_file.exists():
                session_file.unlink()
            
            return True
        
        return False
    
    def save_session(self, session_id: str) -> None:
        """
        Save session to persistent storage.
        
        Args:
            session_id: Session identifier
            
        Raises:
            KeyError: If session not found
        """
        if session_id not in self._sessions:
            raise KeyError(f"Session {session_id} not found")
        
        session = self._sessions[session_id]
        session_file = self.storage_dir / f"{session_id}.json"
        session.save(session_file)
    
    def load_session(self, session_id: str) -> AgentSession:
        """
        Load session from persistent storage.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Loaded AgentSession
            
        Raises:
            FileNotFoundError: If session file not found
        """
        session_file = self.storage_dir / f"{session_id}.json"
        session = AgentSession.load(session_file)
        self._sessions[session.session_id] = session
        return session
    
    def save_all(self) -> None:
        """Save all active sessions to persistent storage."""
        for session_id in self._sessions:
            self.save_session(session_id)
    
    def load_all(self) -> None:
        """Load all sessions from persistent storage."""
        if not self.storage_dir.exists():
            return
        
        for session_file in self.storage_dir.glob("*.json"):
            try:
                session = AgentSession.load(session_file)
                self._sessions[session.session_id] = session
            except Exception:
                # Skip corrupted session files
                pass
    
    def get_statistics(self) -> Dict[str, int]:
        """
        Get session statistics.
        
        Returns:
            Dictionary with session counts by state
        """
        stats: Dict[str, int] = {state.value: 0 for state in SessionState}
        
        for session in self._sessions.values():
            stats[session.state.value] += 1
        
        stats["total"] = len(self._sessions)
        
        return stats
