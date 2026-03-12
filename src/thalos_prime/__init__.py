"""
Thalos Prime - Deterministic AI Agent Session Management System

This package provides deterministic, explicit control over AI agent sessions
with no implicit side effects. It follows strict architectural principles:
- Explicit control paths
- Deterministic behavior
- No implicit state changes
- Subsystem isolation
"""

__version__ = "1.0.0"
__author__ = "Thalos Prime Team"

from thalos_prime.session import AgentSession, SessionManager
from thalos_prime.session.lifecycle import SessionState

__all__ = [
    "AgentSession",
    "SessionManager",
    "SessionState",
]
