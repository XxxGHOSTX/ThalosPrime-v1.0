"""
Example: Multi-Session Management

Demonstrates managing multiple concurrent sessions with different states.
"""

from pathlib import Path
from thalos_prime import SessionManager, SessionState


def main():
    """Run multi-session management example."""
    
    print("Multi-Session Management Example")
    print("=" * 50)
    
    # Create session manager
    manager = SessionManager(storage_dir=Path("examples/multi_session_data"))
    
    # Create multiple sessions
    print("\n1. Creating multiple sessions...")
    
    sessions = []
    for i in range(1, 4):
        session = manager.create_session(
            name=f"session-{i}",
            config={"worker_id": i}
        )
        sessions.append(session)
        print(f"   Created: {session.name} ({session.session_id[:8]}...)")
    
    # Start first two sessions
    print("\n2. Starting sessions 1 and 2...")
    sessions[0].start()
    sessions[1].start()
    print(f"   {sessions[0].name}: {sessions[0].state.value}")
    print(f"   {sessions[1].name}: {sessions[1].state.value}")
    print(f"   {sessions[2].name}: {sessions[2].state.value}")
    
    # Pause first session
    print("\n3. Pausing session 1...")
    sessions[0].pause()
    print(f"   {sessions[0].name}: {sessions[0].state.value}")
    
    # List active sessions
    print("\n4. Listing active (running) sessions...")
    active_sessions = manager.list_sessions(state_filter=SessionState.RUNNING)
    print(f"   Active sessions: {len(active_sessions)}")
    for s in active_sessions:
        print(f"      - {s.name} ({s.session_id[:8]}...)")
    
    # List paused sessions
    print("\n5. Listing paused sessions...")
    paused_sessions = manager.list_sessions(state_filter=SessionState.PAUSED)
    print(f"   Paused sessions: {len(paused_sessions)}")
    for s in paused_sessions:
        print(f"      - {s.name} ({s.session_id[:8]}...)")
    
    # Get statistics
    print("\n6. Session statistics:")
    stats = manager.get_statistics()
    for state, count in stats.items():
        print(f"   {state}: {count}")
    
    # Save all sessions
    print("\n7. Saving all sessions...")
    manager.save_all()
    print("   All sessions saved")
    
    # Terminate all sessions
    print("\n8. Terminating all sessions...")
    for session in sessions:
        if not session.is_terminated:
            session.terminate()
            print(f"   Terminated: {session.name}")
    
    # Save final state
    manager.save_all()
    
    # Load sessions in new manager
    print("\n9. Loading sessions in new manager...")
    new_manager = SessionManager(storage_dir=Path("examples/multi_session_data"))
    new_manager.load_all()
    loaded_sessions = new_manager.list_sessions()
    print(f"   Loaded {len(loaded_sessions)} sessions")
    
    for s in loaded_sessions:
        print(f"      - {s.name}: {s.state.value}")
    
    print("\n✅ Multi-session example completed successfully!")


if __name__ == "__main__":
    main()
