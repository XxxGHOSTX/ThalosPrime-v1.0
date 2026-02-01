"""
Thalos Prime Agent Session Module

This module provides deterministic agent session management with explicit control
and no implicit side effects, following Thalos Prime architectural principles.
"""

__version__ = "1.0.0"
__author__ = "Thalos Prime Team"

from .session import AgentSession, SessionState
from .manager import SessionManager
from .persistence import SessionPersistence
from .sbi_interface import (
    SyntheticBiologicalIntelligence,
    IntentType,
    NeuralProcessingLayer,
)

__all__ = [
    "AgentSession",
    "SessionState",
    "SessionManager",
    "SessionPersistence",
    "SyntheticBiologicalIntelligence",
    "IntentType",
    "NeuralProcessingLayer",
]
