"""
Session Manager

Manages multiple agent sessions with deterministic behavior.
Provides centralized session lifecycle control and monitoring.
"""

from typing import Dict, Optional, List
from datetime import datetime
from .session import AgentSession, SessionState


class SessionManager:
    """
    Deterministic session manager for Thalos Prime agents.
    
    Maintains session registry and provides controlled access to
    session lifecycle operations. All operations are explicit and
    have no implicit side effects.
    """
    
    def __init__(self):
        """Initialize empty session registry."""
        self._sessions: Dict[str, AgentSession] = {}
        self._operation_log: List[Dict] = []
    
    def create_session(self, metadata: Optional[Dict] = None) -> AgentSession:
        """
        Create a new agent session.
        
        Args:
            metadata: Optional metadata for the session
            
        Returns:
            Newly created AgentSession instance
        """
        session = AgentSession(metadata=metadata or {})
        self._sessions[session.session_id] = session
        
        self._log_operation("create", session.session_id)
        
        return session
    
    def get_session(self, session_id: str) -> Optional[AgentSession]:
        """
        Retrieve a session by ID.
        
        Args:
            session_id: Unique session identifier
            
        Returns:
            AgentSession if found, None otherwise
        """
        return self._sessions.get(session_id)
    
    def start_session(self, session_id: str) -> AgentSession:
        """
        Start a session explicitly.
        
        Args:
            session_id: ID of session to start
            
        Returns:
            Updated session instance
            
        Raises:
            KeyError: If session not found
            ValueError: If session cannot be started from current state
        """
        session = self._get_session_or_raise(session_id)
        updated_session = session.start()
        self._sessions[session_id] = updated_session
        
        self._log_operation("start", session_id)
        
        return updated_session
    
    def pause_session(self, session_id: str) -> AgentSession:
        """
        Pause a running session.
        
        Args:
            session_id: ID of session to pause
            
        Returns:
            Updated session instance
            
        Raises:
            KeyError: If session not found
            ValueError: If session cannot be paused from current state
        """
        session = self._get_session_or_raise(session_id)
        updated_session = session.pause()
        self._sessions[session_id] = updated_session
        
        self._log_operation("pause", session_id)
        
        return updated_session
    
    def resume_session(self, session_id: str) -> AgentSession:
        """
        Resume a paused session.
        
        Args:
            session_id: ID of session to resume
            
        Returns:
            Updated session instance
            
        Raises:
            KeyError: If session not found
            ValueError: If session cannot be resumed from current state
        """
        session = self._get_session_or_raise(session_id)
        updated_session = session.resume()
        self._sessions[session_id] = updated_session
        
        self._log_operation("resume", session_id)
        
        return updated_session
    
    def terminate_session(self, session_id: str) -> AgentSession:
        """
        Terminate a session explicitly.
        
        Args:
            session_id: ID of session to terminate
            
        Returns:
            Updated session instance
            
        Raises:
            KeyError: If session not found
            ValueError: If session is already terminated
        """
        session = self._get_session_or_raise(session_id)
        updated_session = session.terminate()
        self._sessions[session_id] = updated_session
        
        self._log_operation("terminate", session_id)
        
        return updated_session
    
    def list_sessions(self, state: Optional[SessionState] = None) -> List[AgentSession]:
        """
        List all sessions, optionally filtered by state.
        
        Args:
            state: Optional state filter
            
        Returns:
            List of sessions matching criteria
        """
        sessions = list(self._sessions.values())
        
        if state is not None:
            sessions = [s for s in sessions if s.state == state]
        
        return sessions
    
    def get_session_count(self, state: Optional[SessionState] = None) -> int:
        """
        Get count of sessions, optionally filtered by state.
        
        Args:
            state: Optional state filter
            
        Returns:
            Count of sessions matching criteria
        """
        return len(self.list_sessions(state))
    
    def cleanup_terminated_sessions(self) -> int:
        """
        Remove terminated sessions from registry.
        
        Returns:
            Number of sessions removed
        """
        terminated_ids = [
            sid for sid, session in self._sessions.items()
            if session.state == SessionState.TERMINATED
        ]
        
        for sid in terminated_ids:
            del self._sessions[sid]
        
        self._log_operation("cleanup", f"{len(terminated_ids)} sessions")
        
        return len(terminated_ids)
    
    def _get_session_or_raise(self, session_id: str) -> AgentSession:
        """
        Get session or raise KeyError with descriptive message.
        
        Args:
            session_id: Session ID to retrieve
            
        Returns:
            AgentSession instance
            
        Raises:
            KeyError: If session not found
        """
        session = self._sessions.get(session_id)
        if session is None:
            raise KeyError(f"Session {session_id} not found")
        return session
    
    def _log_operation(self, operation: str, target: str) -> None:
        """
        Log operation for audit trail.
        
        Args:
            operation: Type of operation
            target: Target of operation (session ID or description)
        """
        self._operation_log.append({
            "operation": operation,
            "target": target,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def get_operation_log(self) -> List[Dict]:
        """
        Retrieve operation log for audit purposes.
        
        Returns:
            List of logged operations
        """
        return self._operation_log.copy()
