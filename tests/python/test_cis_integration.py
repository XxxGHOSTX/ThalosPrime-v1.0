"""
Test suite for CIS Integration Module

Tests CIS integration operations and message logging.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "python"))

from thalos_agent_session import AgentSession, SessionState
from thalos_agent_session.cis_integration import CISIntegration


class TestCISIntegration:
    """Test CISIntegration functionality."""

    def test_initialization_default_endpoint(self):
        """Test CIS integration initializes with default endpoint."""
        cis = CISIntegration()
        assert cis.cis_endpoint == "localhost:8080"
        assert cis.message_log == []

    def test_initialization_custom_endpoint(self):
        """Test CIS integration initializes with custom endpoint."""
        cis = CISIntegration(cis_endpoint="remote-host:9090")
        assert cis.cis_endpoint == "remote-host:9090"

    def test_register_session_with_cis(self):
        """Test registering a session with CIS."""
        cis = CISIntegration()
        session = AgentSession(metadata={"purpose": "test"})

        result = cis.register_session_with_cis(session)

        assert result["status"] == "registered"
        assert result["session_id"] == session.session_id
        assert "cis_tracking_id" in result
        assert result["cis_tracking_id"].startswith("CIS-")

    def test_register_session_logs_message(self):
        """Test that session registration logs a message."""
        cis = CISIntegration()
        session = AgentSession()

        cis.register_session_with_cis(session)

        log = cis.get_message_log()
        assert len(log) == 1
        assert log[0]["message_type"] == "register"
        assert log[0]["message"]["type"] == "session_registration"
        assert log[0]["message"]["session_id"] == session.session_id

    def test_notify_state_change(self):
        """Test notifying CIS of session state change."""
        cis = CISIntegration()
        session = AgentSession()

        result = cis.notify_state_change(
            session, SessionState.INITIALIZED, SessionState.RUNNING
        )

        assert result["status"] == "acknowledged"
        assert result["session_id"] == session.session_id

    def test_notify_state_change_logs_message(self):
        """Test that state change notification logs a message."""
        cis = CISIntegration()
        session = AgentSession()

        cis.notify_state_change(
            session, SessionState.INITIALIZED, SessionState.RUNNING
        )

        log = cis.get_message_log()
        assert len(log) == 1
        assert log[0]["message_type"] == "state_change"
        assert log[0]["message"]["old_state"] == "initialized"
        assert log[0]["message"]["new_state"] == "running"

    def test_request_decision(self):
        """Test requesting a decision from CIS."""
        cis = CISIntegration()
        session = AgentSession()
        context = {"action": "run_task", "priority": "high"}

        result = cis.request_decision(session, context)

        assert result["status"] == "decision_provided"
        assert result["decision"] == "continue"
        assert "confidence" in result
        assert result["confidence"] == 0.95

    def test_request_decision_logs_message(self):
        """Test that decision request logs a message."""
        cis = CISIntegration()
        session = AgentSession()
        context = {"test": "data"}

        cis.request_decision(session, context)

        log = cis.get_message_log()
        assert len(log) == 1
        assert log[0]["message_type"] == "decision_request"
        assert log[0]["message"]["context"] == context

    def test_report_metrics(self):
        """Test reporting metrics to CIS."""
        cis = CISIntegration()
        session = AgentSession()
        metrics = {"cpu_usage": 0.35, "memory_mb": 256}

        result = cis.report_metrics(session, metrics)

        assert result is True

    def test_report_metrics_logs_message(self):
        """Test that metrics report logs a message."""
        cis = CISIntegration()
        session = AgentSession()
        metrics = {"latency_ms": 100}

        cis.report_metrics(session, metrics)

        log = cis.get_message_log()
        assert len(log) == 1
        assert log[0]["message_type"] == "metrics"
        assert log[0]["message"]["metrics"] == metrics

    def test_get_message_log_returns_copy(self):
        """Test that get_message_log returns a copy of the log."""
        cis = CISIntegration()
        session = AgentSession()
        cis.register_session_with_cis(session)

        log1 = cis.get_message_log()
        log1.append({"fake": "entry"})

        log2 = cis.get_message_log()
        assert len(log2) == 1  # Original unchanged

    def test_multiple_operations_accumulate_log(self):
        """Test that multiple CIS operations accumulate in the log."""
        cis = CISIntegration()
        session = AgentSession()

        cis.register_session_with_cis(session)
        cis.notify_state_change(
            session, SessionState.INITIALIZED, SessionState.RUNNING
        )
        cis.request_decision(session, {})
        cis.report_metrics(session, {})

        log = cis.get_message_log()
        assert len(log) == 4
        assert log[0]["message_type"] == "register"
        assert log[1]["message_type"] == "state_change"
        assert log[2]["message_type"] == "decision_request"
        assert log[3]["message_type"] == "metrics"

    def test_log_entries_have_timestamps(self):
        """Test that log entries include timestamps."""
        cis = CISIntegration()
        session = AgentSession()

        cis.register_session_with_cis(session)

        log = cis.get_message_log()
        assert "logged_at" in log[0]
        assert log[0]["logged_at"] is not None
