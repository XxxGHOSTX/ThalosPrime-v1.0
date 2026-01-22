"""
Example: Session Configuration

Demonstrates various session configuration patterns.
"""

from pathlib import Path
from thalos_prime import SessionManager


# Configuration templates
CONFIGS = {
    "gpt4_default": {
        "model": "gpt-4",
        "temperature": 0.7,
        "max_tokens": 2048,
        "top_p": 1.0,
    },
    "gpt4_deterministic": {
        "model": "gpt-4",
        "temperature": 0.0,
        "max_tokens": 2048,
        "top_p": 1.0,
        "seed": 42,
    },
    "gpt35_fast": {
        "model": "gpt-3.5-turbo",
        "temperature": 0.8,
        "max_tokens": 1024,
    },
    "code_generation": {
        "model": "gpt-4",
        "temperature": 0.2,
        "max_tokens": 4096,
        "stop": ["```"],
        "codegen_mode": True,
    },
}


def main():
    """Run configuration example."""
    
    print("Session Configuration Example")
    print("=" * 50)
    
    manager = SessionManager(storage_dir=Path("examples/config_data"))
    
    # Create sessions with different configs
    print("\n1. Creating sessions with different configurations...")
    
    for config_name, config in CONFIGS.items():
        session = manager.create_session(
            name=f"session-{config_name}",
            config=config
        )
        session.start()
        
        print(f"\n   {session.name}:")
        print(f"      Model: {config.get('model')}")
        print(f"      Temperature: {config.get('temperature')}")
        print(f"      Max Tokens: {config.get('max_tokens')}")
        
        # Set appropriate subsystem states
        if config.get("codegen_mode"):
            session.update_codegen_state({
                "enabled": True,
                "language": "python",
                "style": "pep8",
            })
            print(f"      CodeGen: Enabled")
        
        manager.save_session(session.session_id)
    
    # List all configurations
    print("\n2. All configured sessions:")
    all_sessions = manager.list_sessions()
    
    for session in all_sessions:
        print(f"\n   {session.name}:")
        print(f"      Config: {session.config}")
        print(f"      State: {session.state.value}")
    
    print("\n✅ Configuration example completed!")


if __name__ == "__main__":
    main()
