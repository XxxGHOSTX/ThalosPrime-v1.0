"""
Memory Subsystem Integration

Provides deterministic memory management for agent sessions.
All memory operations are explicit and support session persistence.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime, UTC
from collections import OrderedDict


class MemorySubsystem:
    """
    Deterministic memory subsystem for agent sessions.
    
    Provides explicit memory storage, retrieval, and management
    with support for different memory types (working, episodic, semantic).
    """
    
    def __init__(self, max_working_memory: int = 1000):
        """
        Initialize memory subsystem.
        
        Args:
            max_working_memory: Maximum size of working memory
        """
        self.max_working_memory = max_working_memory
        
        # Different memory stores
        self.working_memory: OrderedDict[str, Dict[str, Any]] = OrderedDict()
        self.episodic_memory: List[Dict[str, Any]] = []
        self.semantic_memory: Dict[str, Any] = {}
        
        # Session-specific memory spaces
        self.session_memory: Dict[str, Dict[str, Any]] = {}
    
    def store_working_memory(
        self,
        session_id: str,
        key: str,
        value: Any,
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        Store data in working memory for a session.
        
        Args:
            session_id: Session identifier
            key: Memory key
            value: Memory value
            metadata: Optional metadata
            
        Returns:
            True if stored successfully
        """
        memory_item = {
            "session_id": session_id,
            "key": key,
            "value": value,
            "metadata": metadata or {},
            "stored_at": datetime.now(UTC).isoformat()
        }
        
        # Create session memory space if needed
        if session_id not in self.session_memory:
            self.session_memory[session_id] = {}
        
        # Store in working memory with LRU behavior
        memory_key = f"{session_id}:{key}"
        self.working_memory[memory_key] = memory_item
        self.working_memory.move_to_end(memory_key)
        
        # Enforce max size
        if len(self.working_memory) > self.max_working_memory:
            self.working_memory.popitem(last=False)
        
        # Also store in session-specific memory
        self.session_memory[session_id][key] = memory_item
        
        return True
    
    def retrieve_working_memory(
        self,
        session_id: str,
        key: str
    ) -> Optional[Any]:
        """
        Retrieve data from working memory.
        
        Args:
            session_id: Session identifier
            key: Memory key
            
        Returns:
            Memory value if found, None otherwise
        """
        memory_key = f"{session_id}:{key}"
        memory_item = self.working_memory.get(memory_key)
        
        if memory_item:
            # Update access time
            self.working_memory.move_to_end(memory_key)
            return memory_item["value"]
        
        return None
    
    def store_episodic_memory(
        self,
        session_id: str,
        episode: Dict[str, Any]
    ) -> bool:
        """
        Store an episode in episodic memory.
        
        Args:
            session_id: Session identifier
            episode: Episode data
            
        Returns:
            True if stored successfully
        """
        episode_item = {
            "session_id": session_id,
            "episode": episode,
            "timestamp": datetime.now(UTC).isoformat()
        }
        
        self.episodic_memory.append(episode_item)
        
        return True
    
    def retrieve_episodic_memory(
        self,
        session_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Retrieve recent episodes for a session.
        
        Args:
            session_id: Session identifier
            limit: Maximum number of episodes to return
            
        Returns:
            List of episodes
        """
        session_episodes = [
            e for e in self.episodic_memory
            if e["session_id"] == session_id
        ]
        
        return session_episodes[-limit:]
    
    def store_semantic_memory(
        self,
        key: str,
        concept: Dict[str, Any]
    ) -> bool:
        """
        Store a concept in semantic memory.
        
        Args:
            key: Concept key
            concept: Concept data
            
        Returns:
            True if stored successfully
        """
        self.semantic_memory[key] = {
            "concept": concept,
            "stored_at": datetime.now(UTC).isoformat()
        }
        
        return True
    
    def retrieve_semantic_memory(self, key: str) -> Optional[Any]:
        """
        Retrieve a concept from semantic memory.
        
        Args:
            key: Concept key
            
        Returns:
            Concept data if found, None otherwise
        """
        memory_item = self.semantic_memory.get(key)
        return memory_item["concept"] if memory_item else None
    
    def get_session_memory_snapshot(
        self,
        session_id: str
    ) -> Dict[str, Any]:
        """
        Get a complete memory snapshot for a session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Dictionary containing all memory types for the session
        """
        return {
            "session_id": session_id,
            "working_memory": self.session_memory.get(session_id, {}),
            "episodic_memory": self.retrieve_episodic_memory(session_id),
            "snapshot_time": datetime.now(UTC).isoformat()
        }
    
    def clear_session_memory(self, session_id: str) -> bool:
        """
        Clear all memory for a session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            True if cleared successfully
        """
        # Clear from working memory
        keys_to_remove = [
            k for k in self.working_memory.keys()
            if k.startswith(f"{session_id}:")
        ]
        for key in keys_to_remove:
            del self.working_memory[key]
        
        # Clear session-specific memory
        if session_id in self.session_memory:
            del self.session_memory[session_id]
        
        # Clear episodic memory
        self.episodic_memory = [
            e for e in self.episodic_memory
            if e["session_id"] != session_id
        ]
        
        return True
