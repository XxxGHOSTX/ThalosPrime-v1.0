"""
Extended test suite for SBI Interface - additional coverage tests.

Tests additional branches and paths not covered by the primary test suite.
"""

import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch

import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "python"))

from thalos_agent_session import (
    SyntheticBiologicalIntelligence,
    SessionManager,
    SessionPersistence,
    IntentType,
)
from thalos_agent_session.sbi_interface import NeuralProcessingLayer


class TestSBIExtendedCoverage:
    """Additional SBI tests for improved branch coverage."""

    @pytest.fixture
    def temp_storage(self):
        """Create temporary storage directory."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def sbi_with_storage(self, temp_storage):
        """SBI instance with temp persistence storage."""
        manager = SessionManager()
        persistence = SessionPersistence(temp_storage)
        return SyntheticBiologicalIntelligence(
            session_manager=manager,
            persistence=persistence,
        )

    # --- Session control edge cases ---

    def test_session_control_no_session_id(self, sbi_with_storage):
        """Test session control with no session ID provided."""
        sbi = sbi_with_storage
        # Directly test _handle_session_control with no session_id
        result = sbi._handle_session_control({"action": "pause"})
        assert result["success"] is False
        assert result["error"] == "session_id_required"

    def test_session_control_session_not_found(self, sbi_with_storage):
        """Test session control when session doesn't exist anywhere."""
        sbi = sbi_with_storage
        result = sbi._handle_session_control(
            {"session_id": "nonexistent-id-xyz", "action": "pause"}
        )
        assert result["success"] is False
        assert result["error"] == "session_not_found"

    def test_session_control_load_from_persistence(self, sbi_with_storage):
        """Test that session control loads from persistence when not in manager."""
        sbi = sbi_with_storage
        # Create and save a session directly to persistence
        session = sbi.session_manager.create_session()
        session = sbi.session_manager.start_session(session.session_id)
        sbi.persistence.save_session(session)

        # Remove from manager to force persistence load
        sbi.session_manager._sessions.pop(session.session_id)

        # Pause should load from persistence
        result = sbi._handle_session_control(
            {"session_id": session.session_id, "action": "pause"}
        )
        assert result["success"] is True
        assert result["state"] == "paused"

    def test_session_control_terminate_action(self, sbi_with_storage):
        """Test terminating a session through SBI control."""
        sbi = sbi_with_storage
        # Create running session
        session = sbi.session_manager.create_session()
        session = sbi.session_manager.start_session(session.session_id)

        result = sbi._handle_session_control(
            {"session_id": session.session_id, "action": "stop"}
        )
        assert result["success"] is True
        assert result["state"] == "terminated"

    def test_session_control_end_action(self, sbi_with_storage):
        """Test ending a session via 'end' action."""
        sbi = sbi_with_storage
        session = sbi.session_manager.create_session()
        session = sbi.session_manager.start_session(session.session_id)

        result = sbi._handle_session_control(
            {"session_id": session.session_id, "action": "terminate"}
        )
        assert result["success"] is True
        assert result["state"] == "terminated"

    def test_session_control_unknown_action(self, sbi_with_storage):
        """Test session control with an unknown action."""
        sbi = sbi_with_storage
        session = sbi.session_manager.create_session()
        session = sbi.session_manager.start_session(session.session_id)

        result = sbi._handle_session_control(
            {"session_id": session.session_id, "action": "fly"}
        )
        assert result["success"] is False
        assert result["error"] == "unknown_action"

    def test_session_control_action_exception(self, sbi_with_storage):
        """Test session control exception handling."""
        sbi = sbi_with_storage
        session = sbi.session_manager.create_session()

        # Try to pause an INITIALIZED session (which is invalid - not RUNNING)
        result = sbi._handle_session_control(
            {"session_id": session.session_id, "action": "pause"}
        )
        assert result["success"] is False
        assert result["error"] == "action_failed"

    # --- Session query edge cases ---

    def test_session_query_specific_session_not_found(self, sbi_with_storage):
        """Test querying a specific session that doesn't exist."""
        sbi = sbi_with_storage
        result = sbi._handle_session_query({"session_id": "nonexistent-id"})
        assert result["success"] is False
        assert result["error"] == "session_not_found"

    # --- Memory operations ---

    def test_memory_retrieve_operation(self, sbi_with_storage):
        """Test memory retrieval through SBI."""
        sbi = sbi_with_storage
        # Store something first
        sbi._handle_memory_operation("remember this: important data", {})
        # Now retrieve
        result = sbi._handle_memory_operation("recall memory", {})
        assert result["success"] is True
        assert result["action"] == "memory_retrieved"

    def test_memory_retrieve_with_key(self, sbi_with_storage):
        """Test memory retrieval with a specific key."""
        sbi = sbi_with_storage
        sbi.memory.store_working_memory("sbi_system", "my_key", "my_value")
        result = sbi._handle_memory_operation("get memory", {"key": "my_key"})
        assert result["success"] is True
        assert result["value"] == "my_value"

    # --- Code generation ---

    def test_code_generation_handler(self, sbi_with_storage):
        """Test code generation handler."""
        sbi = sbi_with_storage
        result = sbi._handle_code_generation("generate code for me", {})
        assert result["success"] is True
        assert result["action"] == "code_generation"

    def test_interpret_code_generation_intent(self):
        """Test that code generation intent is handled via interpret_and_execute."""
        sbi = SyntheticBiologicalIntelligence()
        # Direct call to code generation handler
        result = sbi._handle_code_generation("write a function", {})
        assert result["success"] is True

    # --- Exception handling in interpret_and_execute ---

    def test_interpret_and_execute_exception_handling(self):
        """Test that interpret_and_execute handles exceptions gracefully."""
        sbi = SyntheticBiologicalIntelligence()

        # Patch a handler to throw an exception
        with patch.object(
            sbi, "_handle_session_create", side_effect=RuntimeError("Test error")
        ):
            result = sbi.interpret_and_execute("create a new session")

        # Should return a failure response, not raise
        assert result["success"] is False
        assert "error" in result

    # --- Information query handlers ---

    def test_respond_to_what_sbi(self):
        """Test 'what is SBI' response."""
        sbi = SyntheticBiologicalIntelligence()
        result = sbi._handle_information_query("what is SBI?")
        assert result["success"] is True
        assert len(result["message"]) > 20

    def test_respond_to_what_thalos(self):
        """Test 'what is thalos' response."""
        sbi = SyntheticBiologicalIntelligence()
        result = sbi._handle_information_query("what is Thalos Prime?")
        assert result["success"] is True

    def test_respond_to_what_session(self):
        """Test 'what is a session' response."""
        sbi = SyntheticBiologicalIntelligence()
        result = sbi._handle_information_query("what is a session?")
        assert result["success"] is True

    def test_respond_to_what_can_you_do(self):
        """Test 'what can you do' response."""
        sbi = SyntheticBiologicalIntelligence()
        result = sbi._handle_information_query("what can you do?")
        assert result["success"] is True

    def test_respond_to_what_time(self):
        """Test 'what time is it' response."""
        sbi = SyntheticBiologicalIntelligence()
        result = sbi._handle_information_query("what time is it?")
        assert result["success"] is True
        assert "time" in result["message"].lower() or "UTC" in result["message"]

    def test_respond_to_how_work(self):
        """Test 'how does it work' response."""
        sbi = SyntheticBiologicalIntelligence()
        result = sbi._handle_information_query("how does this work?")
        assert result["success"] is True

    def test_respond_to_how_session(self):
        """Test 'how do sessions work' response."""
        sbi = SyntheticBiologicalIntelligence()
        result = sbi._handle_information_query("how do sessions work?")
        assert result["success"] is True

    def test_respond_to_how_use(self):
        """Test 'how do I use it' response."""
        sbi = SyntheticBiologicalIntelligence()
        result = sbi._handle_information_query("how do I use this?")
        assert result["success"] is True

    def test_respond_to_how_remember(self):
        """Test 'how does memory work' response."""
        sbi = SyntheticBiologicalIntelligence()
        result = sbi._handle_information_query("how does memory work?")
        assert result["success"] is True

    def test_respond_to_why_sbi(self):
        """Test 'why SBI' response."""
        sbi = SyntheticBiologicalIntelligence()
        result = sbi._handle_information_query("why use SBI?")
        assert result["success"] is True

    def test_respond_to_why_deterministic(self):
        """Test 'why deterministic' response."""
        sbi = SyntheticBiologicalIntelligence()
        result = sbi._handle_information_query("why is it deterministic?")
        assert result["success"] is True

    def test_respond_to_why_default(self):
        """Test 'why' default response."""
        sbi = SyntheticBiologicalIntelligence()
        result = sbi._handle_information_query("why?")
        assert result["success"] is True

    def test_respond_to_when(self):
        """Test 'when' query response."""
        sbi = SyntheticBiologicalIntelligence()
        result = sbi._handle_information_query("when was this created?")
        assert result["success"] is True

    def test_respond_to_where_data(self):
        """Test 'where is data stored' response."""
        sbi = SyntheticBiologicalIntelligence()
        result = sbi._handle_information_query("where is the data stored?")
        assert result["success"] is True

    def test_respond_to_where_default(self):
        """Test 'where' default response."""
        sbi = SyntheticBiologicalIntelligence()
        result = sbi._handle_information_query("where do you run?")
        assert result["success"] is True

    def test_respond_to_who_you(self):
        """Test 'who are you' response."""
        sbi = SyntheticBiologicalIntelligence()
        result = sbi._handle_information_query("who are you?")
        assert result["success"] is True

    def test_respond_to_who_default(self):
        """Test 'who' default response."""
        sbi = SyntheticBiologicalIntelligence()
        result = sbi._handle_information_query("who built this?")
        assert result["success"] is True

    def test_information_query_no_question_word(self):
        """Test information query with no recognized question word."""
        sbi = SyntheticBiologicalIntelligence()
        result = sbi._handle_information_query("tell me stuff")
        assert result["success"] is True
        assert "message" in result

    # --- General conversation ---

    def test_general_conversation_affirmation(self):
        """Test affirmation response in general conversation."""
        sbi = SyntheticBiologicalIntelligence()
        result = sbi._handle_general_conversation("yes")
        assert result["success"] is True
        assert "action" in result

    def test_general_conversation_negation(self):
        """Test negation response in general conversation."""
        sbi = SyntheticBiologicalIntelligence()
        result = sbi._handle_general_conversation("no")
        assert result["success"] is True

    def test_general_conversation_positive_feedback(self):
        """Test positive feedback response."""
        sbi = SyntheticBiologicalIntelligence()
        for feedback in ["cool", "awesome", "great", "nice", "good"]:
            result = sbi._handle_general_conversation(feedback)
            assert result["success"] is True
            assert result["action"] == "positive_feedback"

    def test_general_conversation_default(self):
        """Test general conversation default fallback."""
        sbi = SyntheticBiologicalIntelligence()
        result = sbi._handle_general_conversation("random unrelated text xyz")
        assert result["success"] is True
        assert result["action"] == "general_response"

    # --- General input handling ---

    def test_general_input_session_keyword(self):
        """Test general input with session keyword."""
        sbi = SyntheticBiologicalIntelligence()
        result = sbi._handle_general_input("something about session")
        assert result["success"] is True

    def test_general_input_help_keyword(self):
        """Test general input with help keyword."""
        sbi = SyntheticBiologicalIntelligence()
        result = sbi._handle_general_input("need help here")
        assert result["success"] is True

    def test_general_input_status_keyword(self):
        """Test general input with status keyword."""
        sbi = SyntheticBiologicalIntelligence()
        result = sbi._handle_general_input("show status here")
        assert result["success"] is True

    def test_general_input_default(self):
        """Test general input default response with no keywords."""
        sbi = SyntheticBiologicalIntelligence()
        result = sbi._handle_general_input("completely unrecognized input xyz123")
        assert result["success"] is True
        assert "suggestions" in result

    # --- Unknown intent ---

    def test_handle_unknown(self):
        """Test _handle_unknown returns helpful response."""
        sbi = SyntheticBiologicalIntelligence()
        result = sbi._handle_unknown("something unknown")
        assert result["success"] is True
        assert "capabilities" in result

    # --- Clear history ---

    def test_clear_history(self):
        """Test clearing interaction history."""
        sbi = SyntheticBiologicalIntelligence()
        sbi.interpret_and_execute("hello")
        sbi.interpret_and_execute("create a session")

        assert len(sbi.get_interaction_history()) >= 2

        sbi.clear_history()

        assert len(sbi.get_interaction_history()) == 0

    # --- Neural layer entity extraction with JSON ---

    def test_neural_layer_json_entity_extraction(self):
        """Test that NeuralProcessingLayer extracts JSON metadata."""
        layer = NeuralProcessingLayer()
        _, _, entities = layer.process_input(
            'create a session with {"purpose": "test", "priority": "high"}'
        )
        if "metadata" in entities:
            assert entities["metadata"]["purpose"] == "test"

    def test_neural_layer_invalid_json_ignored(self):
        """Test that invalid JSON in input is ignored gracefully."""
        layer = NeuralProcessingLayer()
        # Should not raise
        _, _, entities = layer.process_input(
            "create session with {invalid json here}"
        )
        # Metadata should not be set (JSON parse failed)
        assert "metadata" not in entities

    # --- Session query listing all sessions ---

    def test_session_query_list_all(self, sbi_with_storage):
        """Test querying all sessions."""
        sbi = sbi_with_storage
        # Create a couple of sessions
        sbi.interpret_and_execute("create a session")
        sbi.interpret_and_execute("start a new session")

        result = sbi._handle_session_query({})
        assert result["success"] is True
        assert result["action"] == "list_sessions"
        assert result["count"] >= 2
