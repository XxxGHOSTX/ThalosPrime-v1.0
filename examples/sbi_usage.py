#!/usr/bin/env python3
"""
SBI Interface Usage Examples

Demonstrates how to use the Synthetic Biological Intelligence interface
to interact with Thalos Prime using natural language.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "python"))

from thalos_agent_session import SyntheticBiologicalIntelligence


def print_result(label: str, result: dict):
    """Pretty print a result."""
    print(f"\n{'=' * 70}")
    print(f"📝 {label}")
    print(f"{'=' * 70}")
    print(f"✓ Success: {result.get('success')}")
    print(f"📊 Action: {result.get('action')}")
    print(f"💬 Message: {result.get('message')}")
    
    if 'session_id' in result:
        print(f"🔑 Session ID: {result['session_id']}")
    if 'state' in result:
        print(f"📍 State: {result['state']}")
    if 'response' in result:
        print(f"💡 Response: {result['response']}")
    if 'suggestions' in result and result['suggestions']:
        print(f"💭 Suggestions:")
        for suggestion in result['suggestions'][:3]:
            print(f"   - {suggestion}")


def main():
    """Run SBI interface examples."""
    print("=" * 70)
    print("🧠 THALOS PRIME SBI INTERFACE EXAMPLES")
    print("=" * 70)
    print("\nDemonstrating natural language interaction with ANY input support\n")
    
    # Initialize SBI
    sbi = SyntheticBiologicalIntelligence()
    
    # Example 1: Greeting
    print("\n" + "▶" * 35)
    print("EXAMPLE 1: Greeting")
    print("▶" * 35)
    result = sbi.interpret_and_execute("Hello! How are you?")
    print_result("Greeting", result)
    
    # Example 2: Session Creation
    print("\n" + "▶" * 35)
    print("EXAMPLE 2: Session Creation via Natural Language")
    print("▶" * 35)
    result = sbi.interpret_and_execute("create a new session for testing")
    print_result("Session Creation", result)
    session_id = result.get('session_id')
    
    # Example 3: Information Query
    print("\n" + "▶" * 35)
    print("EXAMPLE 3: Information Query")
    print("▶" * 35)
    result = sbi.interpret_and_execute("What is SBI?")
    print_result("Information Query", result)
    
    # Example 4: Session Control
    if session_id:
        print("\n" + "▶" * 35)
        print("EXAMPLE 4: Session Control")
        print("▶" * 35)
        result = sbi.interpret_and_execute(f"pause session {session_id}")
        print_result("Pause Session", result)
    
    # Example 5: System Status
    print("\n" + "▶" * 35)
    print("EXAMPLE 5: System Status Query")
    print("▶" * 35)
    result = sbi.interpret_and_execute("What is the system status?")
    print_result("System Status", result)
    
    # Example 6: List Sessions
    print("\n" + "▶" * 35)
    print("EXAMPLE 6: List All Sessions")
    print("▶" * 35)
    result = sbi.interpret_and_execute("show me all sessions")
    print_result("List Sessions", result)
    
    # Example 7: Help Request
    print("\n" + "▶" * 35)
    print("EXAMPLE 7: Help Request")
    print("▶" * 35)
    result = sbi.interpret_and_execute("help me understand what you can do")
    print_result("Help Request", result)
    
    # Example 8: General Conversation
    print("\n" + "▶" * 35)
    print("EXAMPLE 8: General Conversation")
    print("▶" * 35)
    result = sbi.interpret_and_execute("That's awesome, thanks!")
    print_result("Acknowledgment", result)
    
    # Example 9: Random Input (demonstrates ANY input handling)
    print("\n" + "▶" * 35)
    print("EXAMPLE 9: Random/General Input")
    print("▶" * 35)
    result = sbi.interpret_and_execute("just some random thoughts today")
    print_result("General Input", result)
    
    # Example 10: How/What/Why Questions
    print("\n" + "▶" * 35)
    print("EXAMPLE 10: How Question")
    print("▶" * 35)
    result = sbi.interpret_and_execute("How does the system work?")
    print_result("How Query", result)
    
    # Show interaction history
    print("\n" + "▶" * 35)
    print("INTERACTION HISTORY")
    print("▶" * 35)
    history = sbi.get_interaction_history(limit=5)
    print(f"\n📚 Last {len(history)} interactions:")
    for i, interaction in enumerate(history, 1):
        print(f"\n{i}. Input: '{interaction['input']}'")
        print(f"   Intent: {interaction.get('intent', 'N/A')}")
        print(f"   Success: {interaction.get('success', 'N/A')}")
    
    # Final summary
    print("\n" + "=" * 70)
    print("✅ SUMMARY")
    print("=" * 70)
    print("""
The SBI interface demonstrates:
✓ Natural language understanding for ANY input
✓ Multiple intent types (greetings, commands, queries, conversations)
✓ Session management through natural language
✓ Information queries with contextual responses
✓ General conversation handling
✓ Helpful responses even for ambiguous inputs
✓ Interaction history tracking
✓ Biological-inspired neural processing

Try it yourself:
  ./src/cli/thalos sbi "your natural language input"
  ./src/cli/thalos sbi -i  (for interactive mode)
    """)
    print("=" * 70)


if __name__ == "__main__":
    main()
