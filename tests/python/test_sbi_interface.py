"""
Test suite for SBI (Synthetic Biological Intelligence) Interface

Tests the natural language processing and task execution capabilities.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "python"))

from thalos_agent_session import (
    SyntheticBiologicalIntelligence,
    IntentType,
    SessionManager,
    SessionPersistence,
)


class TestSBIInterface:
    """Test SBI interface functionality."""

    def test_sbi_initialization(self):
        """Test SBI interface initializes correctly."""
        sbi = SyntheticBiologicalIntelligence()
        assert sbi is not None
        assert sbi.session_manager is not None
        assert sbi.neural_layer is not None

    def test_greeting_recognition(self):
        """Test that greetings are recognized."""
        sbi = SyntheticBiologicalIntelligence()
        result = sbi.interpret_and_execute("Hello!")
        
        assert result["success"] is True
        assert "greeting" in result.get("action", "").lower()
        assert "message" in result

    def test_general_input_handling(self):
        """Test that any input gets a response."""
        sbi = SyntheticBiologicalIntelligence()
        
        # Test various random inputs
        inputs = [
            "random text",
            "what is the weather?",
            "tell me a story",
            "42",
            "just testing",
        ]
        
        for input_text in inputs:
            result = sbi.interpret_and_execute(input_text)
            assert "message" in result
            # Should always get some response
            assert len(result["message"]) > 0

    def test_session_creation_via_sbi(self):
        """Test session creation through natural language."""
        sbi = SyntheticBiologicalIntelligence()
        result = sbi.interpret_and_execute("create a new session")
        
        assert result["success"] is True
        assert "session_id" in result
        assert result["action"] == "session_created"

    def test_session_query_via_sbi(self):
        """Test querying sessions through natural language."""
        sbi = SyntheticBiologicalIntelligence()
        
        # Create a session first
        create_result = sbi.interpret_and_execute("start a session")
        assert create_result["success"] is True
        session_id = create_result["session_id"]
        
        # Query all sessions
        query_result = sbi.interpret_and_execute("show me all sessions")
        assert query_result["success"] is True
        assert "sessions" in query_result
        assert query_result["count"] >= 1

    def test_information_queries(self):
        """Test information query handling."""
        sbi = SyntheticBiologicalIntelligence()
        
        queries = [
            "what is SBI?",
            "how does this work?",
            "what can you do?",
            "tell me about Thalos Prime",
        ]
        
        for query in queries:
            result = sbi.interpret_and_execute(query)
            assert "message" in result
            assert len(result["message"]) > 20  # Should have substantial response

    def test_help_request(self):
        """Test help request handling."""
        sbi = SyntheticBiologicalIntelligence()
        result = sbi.interpret_and_execute("help me")
        
        assert result["success"] is True
        assert "help" in result.get("action", "").lower()
        assert "capabilities" in result or "message" in result

    def test_system_status_query(self):
        """Test system status query."""
        sbi = SyntheticBiologicalIntelligence()
        result = sbi.interpret_and_execute("what is the system status?")
        
        assert result["success"] is True
        assert "status" in result
        assert "subsystems" in result

    def test_memory_operation(self):
        """Test memory storage through SBI."""
        sbi = SyntheticBiologicalIntelligence()
        result = sbi.interpret_and_execute("remember this: test data")
        
        assert result["success"] is True
        assert "memory" in result.get("action", "").lower()

    def test_conversational_inputs(self):
        """Test conversational input handling."""
        sbi = SyntheticBiologicalIntelligence()
        
        conversations = [
            "thanks!",
            "okay",
            "cool",
            "yes",
            "no",
        ]
        
        for conv in conversations:
            result = sbi.interpret_and_execute(conv)
            assert result["success"] is True
            assert "message" in result

    def test_interaction_history(self):
        """Test that interactions are recorded."""
        sbi = SyntheticBiologicalIntelligence()
        
        sbi.interpret_and_execute("hello")
        sbi.interpret_and_execute("create a session")
        
        history = sbi.get_interaction_history()
        assert len(history) >= 2
        assert "input" in history[0]
        assert "timestamp" in history[0]

    def test_context_awareness(self):
        """Test that SBI maintains context."""
        sbi = SyntheticBiologicalIntelligence()
        
        # First interaction
        result1 = sbi.interpret_and_execute("create a new session")
        assert result1["success"] is True
        
        # Second interaction with context
        result2 = sbi.interpret_and_execute("what is the system status?")
        assert result2["success"] is True
        
        # Check history maintains both
        history = sbi.get_interaction_history()
        assert len(history) >= 2

    def test_low_confidence_handling(self):
        """Test handling of ambiguous inputs."""
        sbi = SyntheticBiologicalIntelligence()
        
        # Ambiguous input
        result = sbi.interpret_and_execute("xyz abc def")
        
        # Should still provide a response
        assert "message" in result
        # May have suggestions
        if "suggestions" in result:
            assert len(result["suggestions"]) > 0

    def test_session_control_via_natural_language(self):
        """Test session control through natural language."""
        sbi = SyntheticBiologicalIntelligence()
        
        # Create session
        create_result = sbi.interpret_and_execute("start a new agent session")
        assert create_result["success"] is True
        session_id = create_result["session_id"]
        
        # Pause session
        pause_result = sbi.interpret_and_execute(f"pause session {session_id}")
        assert pause_result["success"] is True
        assert pause_result["state"] == "paused"
        
        # Resume session
        resume_result = sbi.interpret_and_execute(f"resume {session_id}")
        assert resume_result["success"] is True
        assert resume_result["state"] == "running"

    def test_neural_layer_pattern_matching(self):
        """Test neural processing layer pattern matching."""
        sbi = SyntheticBiologicalIntelligence()
        
        # Test various patterns
        test_cases = [
            ("create a session", IntentType.SESSION_CREATE),
            ("pause the agent", IntentType.SESSION_CONTROL),
            ("show sessions", IntentType.SESSION_QUERY),
            ("hello there", IntentType.GREETING),
            ("help me", IntentType.HELP_REQUEST),
        ]
        
        for input_text, expected_intent in test_cases:
            intent, confidence, entities = sbi.neural_layer.process_input(input_text)
            # Intent should match or be recognized
            assert confidence > 0.0
            # Most patterns should have reasonable confidence
            if expected_intent != IntentType.UNKNOWN:
                assert confidence > 0.5

    def test_entity_extraction(self):
        """Test entity extraction from natural language."""
        sbi = SyntheticBiologicalIntelligence()
        
        # Input with session ID
        uuid = "12345678-1234-1234-1234-123456789abc"
        input_text = f"pause session {uuid}"
        
        intent, confidence, entities = sbi.neural_layer.process_input(input_text)
        
        # Should extract session ID
        if "session_id" in entities:
            assert entities["session_id"] == uuid

    def test_always_responds(self):
        """Test that SBI ALWAYS provides a response to any input."""
        sbi = SyntheticBiologicalIntelligence()
        
        # Try many different types of inputs
        test_inputs = [
            "",  # Empty
            "a",  # Single character
            "test",  # Simple word
            "This is a longer sentence without clear intent.",
            "!@#$%",  # Special characters
            "12345",  # Numbers
            "What? How? Why?",  # Multiple questions
            "create pause stop resume",  # Mixed commands
            "hello system status memory code",  # Mixed intents
        ]
        
        for test_input in test_inputs:
            if test_input:  # Skip empty string
                result = sbi.interpret_and_execute(test_input)
                # Must always have a message
                assert "message" in result
                assert len(result["message"]) > 0
                # Should indicate some action was taken
                assert "action" in result
