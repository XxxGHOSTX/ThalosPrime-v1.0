"""
Basic Usage Example for Thalos Prime Agent Session Management

This example demonstrates core functionality:
- Creating and managing sessions
- State transitions
- Persistence
- Subsystem integration
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "python"))

from thalos_agent_session import (
    AgentSession,
    SessionManager,
    SessionPersistence,
    SessionState
)
from thalos_agent_session.cis_integration import CISIntegration
from thalos_agent_session.memory_subsystem import MemorySubsystem
from thalos_agent_session.code_generation import CodeGenerationModule


def example_basic_session():
    """Example: Basic session lifecycle"""
    print("=" * 60)
    print("Example 1: Basic Session Lifecycle")
    print("=" * 60)
    
    # Create a session
    session = AgentSession(metadata={"user": "alice", "task": "analysis"})
    print(f"Created session: {session.session_id}")
    print(f"Initial state: {session.state.value}")
    
    # Start the session
    session = session.start()
    print(f"Started session, state: {session.state.value}")
    
    # Pause the session
    session = session.pause()
    print(f"Paused session, state: {session.state.value}")
    
    # Resume the session
    session = session.resume()
    print(f"Resumed session, state: {session.state.value}")
    
    # Terminate the session
    session = session.terminate()
    print(f"Terminated session, state: {session.state.value}")
    print(f"Total transitions: {session.transition_count}")
    print()


def example_session_manager():
    """Example: Managing multiple sessions"""
    print("=" * 60)
    print("Example 2: Session Manager")
    print("=" * 60)
    
    # Create manager
    manager = SessionManager()
    
    # Create multiple sessions
    session1 = manager.create_session({"type": "worker"})
    session2 = manager.create_session({"type": "monitor"})
    session3 = manager.create_session({"type": "analyzer"})
    
    print(f"Created {manager.get_session_count()} sessions")
    
    # Start some sessions
    manager.start_session(session1.session_id)
    manager.start_session(session2.session_id)
    
    print(f"Running sessions: {manager.get_session_count(SessionState.RUNNING)}")
    print(f"Initialized sessions: {manager.get_session_count(SessionState.INITIALIZED)}")
    
    # List running sessions
    print("\nRunning sessions:")
    for session in manager.list_sessions(SessionState.RUNNING):
        print(f"  - {session.session_id}: {session.metadata}")
    
    # Terminate and cleanup
    manager.terminate_session(session1.session_id)
    removed = manager.cleanup_terminated_sessions()
    print(f"\nCleaned up {removed} terminated session(s)")
    print(f"Active sessions: {manager.get_session_count()}")
    print()


def example_persistence():
    """Example: Session persistence"""
    print("=" * 60)
    print("Example 3: Session Persistence")
    print("=" * 60)
    
    # Create persistence layer
    persistence = SessionPersistence("./session_data")
    
    # Create and save a session
    session = AgentSession(metadata={"persistent": True})
    session = session.start()
    
    print(f"Saving session: {session.session_id}")
    persistence.save_session(session)
    
    # Load the session
    loaded = persistence.load_session(session.session_id)
    print(f"Loaded session: {loaded.session_id}")
    print(f"State preserved: {loaded.state.value}")
    print(f"Metadata preserved: {loaded.metadata}")
    
    # List all stored sessions
    stored = persistence.list_stored_sessions()
    print(f"\nTotal stored sessions: {len(stored)}")
    print()


def example_cis_integration():
    """Example: CIS integration"""
    print("=" * 60)
    print("Example 4: CIS Integration")
    print("=" * 60)
    
    # Create CIS integration
    cis = CISIntegration()
    
    # Create session
    session = AgentSession(metadata={"cis_enabled": True})
    
    # Register with CIS
    response = cis.register_session_with_cis(session)
    print(f"Registered with CIS: {response}")
    
    # Notify state change
    old_state = session.state
    session = session.start()
    cis.notify_state_change(session, old_state, session.state)
    print(f"Notified CIS of state change: {old_state.value} → {session.state.value}")
    
    # Request decision
    decision = cis.request_decision(session, {"action": "continue"})
    print(f"CIS decision: {decision}")
    
    # Report metrics
    cis.report_metrics(session, {"cpu": 45.2, "memory": 1024})
    print("Reported metrics to CIS")
    print()


def example_memory_subsystem():
    """Example: Memory subsystem"""
    print("=" * 60)
    print("Example 5: Memory Subsystem")
    print("=" * 60)
    
    # Create memory subsystem
    memory = MemorySubsystem()
    
    session_id = "test-session"
    
    # Store working memory
    memory.store_working_memory(session_id, "current_task", "analysis")
    memory.store_working_memory(session_id, "user", "alice")
    print("Stored working memory items")
    
    # Retrieve working memory
    task = memory.retrieve_working_memory(session_id, "current_task")
    print(f"Retrieved task: {task}")
    
    # Store episodic memory
    memory.store_episodic_memory(session_id, {
        "event": "task_completed",
        "duration": 120
    })
    print("Stored episodic memory")
    
    # Store semantic memory
    memory.store_semantic_memory("task_types", {
        "analysis": "Data analysis task",
        "synthesis": "Data synthesis task"
    })
    print("Stored semantic memory")
    
    # Get memory snapshot
    snapshot = memory.get_session_memory_snapshot(session_id)
    print(f"\nMemory snapshot: {len(snapshot['working_memory'])} items")
    print()


def example_code_generation():
    """Example: Code generation"""
    print("=" * 60)
    print("Example 6: Code Generation")
    print("=" * 60)
    
    # Create code generation module
    codegen = CodeGenerationModule()
    
    # Register template
    template = '''def {function_name}({parameters}):
    """
    {docstring}
    """
    {body}
'''
    codegen.register_template("function", template)
    print("Registered function template")
    
    # Generate code
    session_id = "test-session"
    result = codegen.generate_code(
        session_id,
        "function",
        {
            "function_name": "calculate_sum",
            "parameters": "a, b",
            "docstring": "Calculate sum of two numbers",
            "body": "    return a + b"
        }
    )
    
    print("\nGenerated code:")
    print(result["code"])
    print(f"Code hash: {result['hash'][:16]}...")
    
    # Validate code
    validation = codegen.validate_code(result["code"])
    print(f"Code validation: {'✓ Valid' if validation['valid'] else '✗ Invalid'}")
    print()


def example_complete_workflow():
    """Example: Complete workflow"""
    print("=" * 60)
    print("Example 7: Complete Workflow")
    print("=" * 60)
    
    # Initialize all components
    manager = SessionManager()
    persistence = SessionPersistence()
    cis = CISIntegration()
    memory = MemorySubsystem()
    codegen = CodeGenerationModule()
    
    # Create and configure session
    session = manager.create_session({
        "user": "alice",
        "task": "data_processing",
        "priority": "high"
    })
    print(f"Created session: {session.session_id}")
    
    # Register with CIS
    cis.register_session_with_cis(session)
    
    # Start session
    session = manager.start_session(session.session_id)
    print(f"Started session in state: {session.state.value}")
    
    # Store initial context in memory
    memory.store_working_memory(session.session_id, "stage", "initialization")
    memory.store_working_memory(session.session_id, "data_source", "database_1")
    
    # Generate processing code
    codegen.register_template("processor", "def process(): pass")
    code_result = codegen.generate_code(
        session.session_id,
        "processor",
        {}
    )
    print(f"Generated processing code (hash: {code_result['hash'][:8]})")
    
    # Store episode in memory
    memory.store_episodic_memory(session.session_id, {
        "event": "code_generated",
        "template": "processor"
    })
    
    # Report metrics to CIS
    cis.report_metrics(session, {
        "operations": 1,
        "code_generated": 1
    })
    
    # Save session state
    persistence.save_session(session)
    print(f"Persisted session state")
    
    # Get memory snapshot
    snapshot = memory.get_session_memory_snapshot(session.session_id)
    print(f"Memory snapshot: {len(snapshot['working_memory'])} working memory items")
    
    print("\n✓ Complete workflow executed successfully")
    print()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("THALOS PRIME - AGENT SESSION MANAGEMENT")
    print("Usage Examples")
    print("=" * 60 + "\n")
    
    # Run all examples
    example_basic_session()
    example_session_manager()
    example_persistence()
    example_cis_integration()
    example_memory_subsystem()
    example_code_generation()
    example_complete_workflow()
    
    print("=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)
