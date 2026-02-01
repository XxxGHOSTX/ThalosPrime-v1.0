"""
Central Intelligence System (CIS) Integration

Provides deterministic integration between agent sessions and the CIS.
All communications are explicit and traceable.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime, UTC
from .session import AgentSession, SessionState


class CISIntegration:
    """
    Integration layer between agent sessions and Central Intelligence System.
    
    Provides explicit communication channels and ensures deterministic
    behavior in all agent-CIS interactions.
    """
    
    def __init__(self, cis_endpoint: str = "localhost:8080"):
        """
        Initialize CIS integration.
        
        Args:
            cis_endpoint: CIS service endpoint
        """
        self.cis_endpoint = cis_endpoint
        self.message_log: List[Dict[str, Any]] = []
    
    def register_session_with_cis(self, session: AgentSession) -> Dict[str, Any]:
        """
        Register an agent session with the CIS.
        
        Args:
            session: AgentSession to register
            
        Returns:
            Registration response from CIS
        """
        message = {
            "type": "session_registration",
            "session_id": session.session_id,
            "state": session.state.value,
            "timestamp": datetime.now(UTC).isoformat(),
            "metadata": session.metadata
        }
        
        self._log_message("register", message)
        
        # In production, this would make actual CIS API call
        return {
            "status": "registered",
            "session_id": session.session_id,
            "cis_tracking_id": f"CIS-{session.session_id[:8]}"
        }
    
    def notify_state_change(
        self,
        session: AgentSession,
        old_state: SessionState,
        new_state: SessionState
    ) -> Dict[str, Any]:
        """
        Notify CIS of session state change.
        
        Args:
            session: AgentSession that changed state
            old_state: Previous state
            new_state: New state
            
        Returns:
            Acknowledgment from CIS
        """
        message = {
            "type": "state_change",
            "session_id": session.session_id,
            "old_state": old_state.value,
            "new_state": new_state.value,
            "timestamp": datetime.now(UTC).isoformat()
        }
        
        self._log_message("state_change", message)
        
        return {
            "status": "acknowledged",
            "session_id": session.session_id
        }
    
    def request_decision(
        self,
        session: AgentSession,
        decision_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Request a decision from CIS for the agent session.
        
        Args:
            session: AgentSession requesting decision
            decision_context: Context for the decision
            
        Returns:
            Decision from CIS
        """
        message = {
            "type": "decision_request",
            "session_id": session.session_id,
            "context": decision_context,
            "timestamp": datetime.now(UTC).isoformat()
        }
        
        self._log_message("decision_request", message)
        
        # In production, this would interact with actual CIS
        return {
            "status": "decision_provided",
            "decision": "continue",
            "confidence": 0.95,
            "reasoning": "Session state is stable"
        }
    
    def report_metrics(
        self,
        session: AgentSession,
        metrics: Dict[str, Any]
    ) -> bool:
        """
        Report session metrics to CIS.
        
        Args:
            session: AgentSession reporting metrics
            metrics: Metrics data
            
        Returns:
            True if metrics were received
        """
        message = {
            "type": "metrics_report",
            "session_id": session.session_id,
            "metrics": metrics,
            "timestamp": datetime.now(UTC).isoformat()
        }
        
        self._log_message("metrics", message)
        
        return True
    
    def _log_message(self, message_type: str, message: Dict[str, Any]) -> None:
        """
        Log CIS communication for audit trail.
        
        Args:
            message_type: Type of message
            message: Message content
        """
        self.message_log.append({
            "message_type": message_type,
            "message": message,
            "logged_at": datetime.now(UTC).isoformat()
        })
    
    def get_message_log(self) -> List[Dict[str, Any]]:
        """
        Retrieve CIS communication log.
        
        Returns:
            List of logged messages
        """
        return self.message_log.copy()
