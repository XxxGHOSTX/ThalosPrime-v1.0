"""
Example: Basic Agent Session Usage

Demonstrates creating, managing, and persisting agent sessions.
"""

from pathlib import Path
from thalos_prime import SessionManager


def main():
    """Run basic session management example."""

    # Create session manager with storage
    print("Creating session manager...")
    manager = SessionManager(storage_dir=Path("examples/session_data"))

    # Create a new session
    print("\n1. Creating new session...")
    session = manager.create_session(
        name="example-session",
        config={
            "model": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 2048,
        },
    )
    print(f"   Session ID: {session.session_id}")
    print(f"   State: {session.state.value}")

    # Start the session
    print("\n2. Starting session...")
    session.start()
    print(f"   State: {session.state.value}")
    print(f"   Is Active: {session.is_active}")

    # Update subsystem states
    print("\n3. Updating subsystem states...")
    session.update_cis_state(
        {
            "mode": "autonomous",
            "priority": "high",
            "timeout": 300,
        }
    )
    session.update_memory_state(
        {
            "context_window": 8192,
            "cache_enabled": True,
        }
    )
    session.update_codegen_state(
        {
            "language": "python",
            "style": "pep8",
        }
    )
    print("   Subsystem states updated")

    # Pause the session
    print("\n4. Pausing session...")
    session.pause()
    print(f"   State: {session.state.value}")
    print(f"   Is Active: {session.is_active}")

    # Save session
    print("\n5. Saving session to disk...")
    manager.save_session(session.session_id)
    print("   Session saved")

    # Resume session
    print("\n6. Resuming session...")
    session.resume()
    print(f"   State: {session.state.value}")
    print(f"   Is Active: {session.is_active}")

    # Show session info
    print("\n7. Session information:")
    session_dict = session.to_dict()
    print(f"   ID: {session_dict['session_id']}")
    print(f"   Name: {session_dict['name']}")
    print(f"   State: {session_dict['lifecycle']['current_state']}")
    print(f"   CIS State: {session_dict['cis_state']}")
    print(f"   Memory State: {session_dict['memory_state']}")
    print(f"   CodeGen State: {session_dict['codegen_state']}")

    # Terminate session
    print("\n8. Terminating session...")
    session.terminate()
    print(f"   State: {session.state.value}")
    print(f"   Is Terminated: {session.is_terminated}")

    # Save final state
    manager.save_session(session.session_id)

    print("\n✅ Example completed successfully!")
    print(f"\nSession data saved to: examples/session_data/{session.session_id}.json")


if __name__ == "__main__":
    main()
