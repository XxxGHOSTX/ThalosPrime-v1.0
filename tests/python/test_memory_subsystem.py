"""
Test suite for Memory Subsystem Module

Tests deterministic memory operations.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "python"))

from thalos_agent_session.memory_subsystem import MemorySubsystem


class TestMemorySubsystem:
    """Test MemorySubsystem functionality."""

    def test_initialization(self):
        """Test memory subsystem initializes correctly."""
        mem = MemorySubsystem()
        assert mem.max_working_memory == 1000
        assert len(mem.working_memory) == 0
        assert len(mem.episodic_memory) == 0
        assert len(mem.semantic_memory) == 0

    def test_initialization_custom_max(self):
        """Test initialization with custom max working memory."""
        mem = MemorySubsystem(max_working_memory=100)
        assert mem.max_working_memory == 100

    def test_store_working_memory(self):
        """Test storing data in working memory."""
        mem = MemorySubsystem()
        result = mem.store_working_memory("session-1", "key1", "value1")

        assert result is True

    def test_retrieve_working_memory(self):
        """Test retrieving data from working memory."""
        mem = MemorySubsystem()
        mem.store_working_memory("session-1", "key1", "test_value")

        retrieved = mem.retrieve_working_memory("session-1", "key1")
        assert retrieved == "test_value"

    def test_retrieve_working_memory_not_found(self):
        """Test retrieving data that doesn't exist returns None."""
        mem = MemorySubsystem()
        result = mem.retrieve_working_memory("session-1", "nonexistent")
        assert result is None

    def test_store_working_memory_with_metadata(self):
        """Test storing data with metadata."""
        mem = MemorySubsystem()
        metadata = {"source": "test", "priority": "high"}
        result = mem.store_working_memory("session-1", "key1", "value", metadata)

        assert result is True

    def test_working_memory_lru_eviction(self):
        """Test that LRU eviction occurs when max capacity reached."""
        mem = MemorySubsystem(max_working_memory=3)

        mem.store_working_memory("s1", "k1", "v1")
        mem.store_working_memory("s1", "k2", "v2")
        mem.store_working_memory("s1", "k3", "v3")
        mem.store_working_memory("s1", "k4", "v4")  # Should evict k1

        assert len(mem.working_memory) == 3
        assert mem.retrieve_working_memory("s1", "k1") is None
        assert mem.retrieve_working_memory("s1", "k4") == "v4"

    def test_store_episodic_memory(self):
        """Test storing an episode in episodic memory."""
        mem = MemorySubsystem()
        episode = {"event": "session_started", "details": "Test run"}
        result = mem.store_episodic_memory("session-1", episode)

        assert result is True
        assert len(mem.episodic_memory) == 1

    def test_retrieve_episodic_memory(self):
        """Test retrieving episodic memory."""
        mem = MemorySubsystem()
        episode1 = {"event": "start"}
        episode2 = {"event": "pause"}
        mem.store_episodic_memory("session-1", episode1)
        mem.store_episodic_memory("session-1", episode2)
        mem.store_episodic_memory("session-2", {"event": "other"})

        episodes = mem.retrieve_episodic_memory("session-1")
        assert len(episodes) == 2
        for ep in episodes:
            assert ep["session_id"] == "session-1"

    def test_retrieve_episodic_memory_with_limit(self):
        """Test retrieving episodic memory with a limit."""
        mem = MemorySubsystem()
        for i in range(5):
            mem.store_episodic_memory("session-1", {"event": f"event_{i}"})

        episodes = mem.retrieve_episodic_memory("session-1", limit=3)
        assert len(episodes) == 3

    def test_retrieve_episodic_memory_empty(self):
        """Test retrieving episodic memory for a session with no episodes."""
        mem = MemorySubsystem()
        episodes = mem.retrieve_episodic_memory("nonexistent-session")
        assert episodes == []

    def test_store_semantic_memory(self):
        """Test storing a concept in semantic memory."""
        mem = MemorySubsystem()
        concept = {"definition": "A session represents an active process"}
        result = mem.store_semantic_memory("session_concept", concept)

        assert result is True
        assert "session_concept" in mem.semantic_memory

    def test_retrieve_semantic_memory(self):
        """Test retrieving semantic memory."""
        mem = MemorySubsystem()
        concept = {"definition": "Test concept"}
        mem.store_semantic_memory("test_key", concept)

        retrieved = mem.retrieve_semantic_memory("test_key")
        assert retrieved == concept

    def test_retrieve_semantic_memory_not_found(self):
        """Test retrieving semantic memory that doesn't exist."""
        mem = MemorySubsystem()
        result = mem.retrieve_semantic_memory("nonexistent")
        assert result is None

    def test_get_session_memory_snapshot(self):
        """Test getting a complete memory snapshot for a session."""
        mem = MemorySubsystem()
        mem.store_working_memory("session-1", "key1", "value1")
        mem.store_episodic_memory("session-1", {"event": "test"})

        snapshot = mem.get_session_memory_snapshot("session-1")

        assert snapshot["session_id"] == "session-1"
        assert "working_memory" in snapshot
        assert "episodic_memory" in snapshot
        assert "snapshot_time" in snapshot

    def test_get_session_memory_snapshot_empty_session(self):
        """Test getting snapshot for session with no memory."""
        mem = MemorySubsystem()
        snapshot = mem.get_session_memory_snapshot("empty-session")

        assert snapshot["session_id"] == "empty-session"
        assert snapshot["working_memory"] == {}
        assert snapshot["episodic_memory"] == []

    def test_clear_session_memory(self):
        """Test clearing all memory for a session."""
        mem = MemorySubsystem()
        mem.store_working_memory("session-1", "key1", "value1")
        mem.store_working_memory("session-1", "key2", "value2")
        mem.store_episodic_memory("session-1", {"event": "test"})
        mem.store_working_memory("session-2", "other", "data")

        result = mem.clear_session_memory("session-1")

        assert result is True
        assert mem.retrieve_working_memory("session-1", "key1") is None
        assert mem.retrieve_working_memory("session-1", "key2") is None
        assert mem.retrieve_episodic_memory("session-1") == []
        # session-2 should be unaffected
        assert mem.retrieve_working_memory("session-2", "other") == "data"

    def test_clear_session_memory_nonexistent(self):
        """Test clearing memory for a session that has no memory."""
        mem = MemorySubsystem()
        result = mem.clear_session_memory("nonexistent-session")
        assert result is True  # Should succeed gracefully

    def test_working_memory_session_isolation(self):
        """Test that working memory is isolated per session."""
        mem = MemorySubsystem()
        mem.store_working_memory("session-1", "key", "value-1")
        mem.store_working_memory("session-2", "key", "value-2")

        assert mem.retrieve_working_memory("session-1", "key") == "value-1"
        assert mem.retrieve_working_memory("session-2", "key") == "value-2"

    def test_retrieve_working_memory_updates_lru(self):
        """Test that retrieving working memory updates LRU order."""
        mem = MemorySubsystem(max_working_memory=3)

        mem.store_working_memory("s1", "k1", "v1")
        mem.store_working_memory("s1", "k2", "v2")
        mem.store_working_memory("s1", "k3", "v3")

        # Access k1 to move it to end (most recently used)
        mem.retrieve_working_memory("s1", "k1")

        # Add k4 which should evict k2 (now oldest)
        mem.store_working_memory("s1", "k4", "v4")

        assert mem.retrieve_working_memory("s1", "k1") == "v1"
        assert mem.retrieve_working_memory("s1", "k2") is None
