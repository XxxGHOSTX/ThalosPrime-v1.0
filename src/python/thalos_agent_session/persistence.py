"""
Session Persistence

Provides deterministic session state persistence with multiple backend support.
All persistence operations are explicit and atomic.
"""

import json
import os
import logging
from typing import Optional, Dict, Any
from pathlib import Path
from .session import AgentSession

logger = logging.getLogger(__name__)


class SessionPersistence:
    """
    Deterministic session persistence layer.

    Provides explicit save/load operations for session state with
    configurable backends (filesystem, Redis, etc.).
    """

    def __init__(self, storage_path: str = "./session_data"):
        """
        Initialize persistence layer.

        Args:
            storage_path: Path for storing session data
        """
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def save_session(self, session: AgentSession) -> bool:
        """
        Explicitly save session state to persistent storage.

        Args:
            session: AgentSession instance to save

        Returns:
            True if save was successful
        """
        try:
            session_file = self.storage_path / f"{session.session_id}.json"
            session_data = session.to_dict()

            # Atomic write using temp file
            temp_file = session_file.with_suffix(".tmp")
            with open(temp_file, "w") as f:
                json.dump(session_data, f, indent=2)

            # Atomic rename
            temp_file.rename(session_file)

            return True
        except Exception as e:
            logger.error(f"Error saving session {session.session_id}: {e}")
            return False

    def load_session(self, session_id: str) -> Optional[AgentSession]:
        """
        Explicitly load session state from persistent storage.

        Args:
            session_id: Unique session identifier

        Returns:
            AgentSession instance if found, None otherwise
        """
        try:
            session_file = self.storage_path / f"{session_id}.json"

            if not session_file.exists():
                return None

            with open(session_file, "r") as f:
                session_data = json.load(f)

            return AgentSession.from_dict(session_data)
        except Exception as e:
            logger.error(f"Error loading session {session_id}: {e}")
            return None

    def delete_session(self, session_id: str) -> bool:
        """
        Explicitly delete session from persistent storage.

        Args:
            session_id: Unique session identifier

        Returns:
            True if deletion was successful
        """
        try:
            session_file = self.storage_path / f"{session_id}.json"

            if session_file.exists():
                session_file.unlink()
                return True

            return False
        except Exception as e:
            logger.error(f"Error deleting session {session_id}: {e}")
            return False

    def list_stored_sessions(self) -> list:
        """
        List all session IDs in persistent storage.

        Returns:
            List of session IDs
        """
        try:
            session_files = self.storage_path.glob("*.json")
            return [f.stem for f in session_files]
        except Exception as e:
            logger.error(f"Error listing sessions: {e}")
            return []

    def cleanup_old_sessions(self, max_age_days: int = 30) -> int:
        """
        Remove old session data from storage.

        Args:
            max_age_days: Maximum age of sessions to keep

        Returns:
            Number of sessions cleaned up
        """
        import time

        count = 0
        current_time = time.time()
        max_age_seconds = max_age_days * 24 * 60 * 60

        try:
            for session_file in self.storage_path.glob("*.json"):
                file_age = current_time - session_file.stat().st_mtime

                if file_age > max_age_seconds:
                    session_file.unlink()
                    count += 1
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

        return count
