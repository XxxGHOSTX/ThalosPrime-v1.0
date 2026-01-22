"""
Thalos Prime CLI

Command-line interface for managing agent sessions.
"""

import sys
import json
from pathlib import Path
from typing import Optional

import click

from thalos_prime.session import SessionManager, SessionState


@click.group()
@click.version_option(version="1.0.0", prog_name="thalos")
@click.option(
    "--storage-dir",
    type=click.Path(path_type=Path),
    default=".thalos/sessions",
    help="Session storage directory",
)
@click.pass_context
def main(ctx: click.Context, storage_dir: Path) -> None:
    """
    Thalos Prime - Deterministic AI Agent Session Management
    
    Manage agent sessions with explicit control and deterministic behavior.
    """
    ctx.ensure_object(dict)
    ctx.obj["manager"] = SessionManager(storage_dir=storage_dir)
    ctx.obj["storage_dir"] = storage_dir


@main.group()
def session() -> None:
    """Manage agent sessions."""
    pass


@session.command("start")
@click.option("--name", help="Session name")
@click.option("--config", help="Configuration JSON")
@click.pass_context
def session_start(ctx: click.Context, name: Optional[str], config: Optional[str]) -> None:
    """Start a new agent session."""
    manager: SessionManager = ctx.obj["manager"]
    
    # Parse config if provided
    config_dict = None
    if config:
        try:
            config_dict = json.loads(config)
        except json.JSONDecodeError:
            click.echo(f"Error: Invalid JSON config", err=True)
            sys.exit(1)
    
    # Create and start session
    session = manager.create_session(name=name, config=config_dict)
    session.start()
    
    # Save session
    manager.save_session(session.session_id)
    
    click.echo(f"Started session: {session.session_id}")
    click.echo(f"Name: {session.name}")
    click.echo(f"State: {session.state.value}")


@session.command("stop")
@click.argument("session_id")
@click.pass_context
def session_stop(ctx: click.Context, session_id: str) -> None:
    """Stop (terminate) an agent session."""
    manager: SessionManager = ctx.obj["manager"]
    
    # Load session if not in memory
    session = manager.get_session(session_id)
    if not session:
        try:
            session = manager.load_session(session_id)
        except FileNotFoundError:
            click.echo(f"Error: Session {session_id} not found", err=True)
            sys.exit(1)
    
    # Terminate session
    if session.is_terminated:
        click.echo(f"Session {session_id} is already terminated")
    else:
        session.terminate()
        manager.save_session(session_id)
        click.echo(f"Terminated session: {session_id}")


@session.command("pause")
@click.argument("session_id")
@click.pass_context
def session_pause(ctx: click.Context, session_id: str) -> None:
    """Pause a running agent session."""
    manager: SessionManager = ctx.obj["manager"]
    
    # Load session if not in memory
    session = manager.get_session(session_id)
    if not session:
        try:
            session = manager.load_session(session_id)
        except FileNotFoundError:
            click.echo(f"Error: Session {session_id} not found", err=True)
            sys.exit(1)
    
    # Pause session
    try:
        session.pause()
        manager.save_session(session_id)
        click.echo(f"Paused session: {session_id}")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@session.command("resume")
@click.argument("session_id")
@click.pass_context
def session_resume(ctx: click.Context, session_id: str) -> None:
    """Resume a paused agent session."""
    manager: SessionManager = ctx.obj["manager"]
    
    # Load session if not in memory
    session = manager.get_session(session_id)
    if not session:
        try:
            session = manager.load_session(session_id)
        except FileNotFoundError:
            click.echo(f"Error: Session {session_id} not found", err=True)
            sys.exit(1)
    
    # Resume session
    try:
        session.resume()
        manager.save_session(session_id)
        click.echo(f"Resumed session: {session_id}")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@session.command("status")
@click.argument("session_id", required=False)
@click.option("--all", "show_all", is_flag=True, help="Show all sessions")
@click.option("--state", type=click.Choice([s.value for s in SessionState]), help="Filter by state")
@click.pass_context
def session_status(
    ctx: click.Context,
    session_id: Optional[str],
    show_all: bool,
    state: Optional[str],
) -> None:
    """Show status of agent sessions."""
    manager: SessionManager = ctx.obj["manager"]
    
    # Load all sessions from storage
    manager.load_all()
    
    if session_id:
        # Show specific session
        session = manager.get_session(session_id)
        if not session:
            click.echo(f"Error: Session {session_id} not found", err=True)
            sys.exit(1)
        
        click.echo(f"Session ID: {session.session_id}")
        click.echo(f"Name: {session.name}")
        click.echo(f"State: {session.state.value}")
        click.echo(f"Created: {session._created_at.isoformat()}")
        click.echo(f"Updated: {session._updated_at.isoformat()}")
        
    elif show_all or state:
        # List all sessions or filtered
        state_filter = SessionState(state) if state else None
        sessions = manager.list_sessions(state_filter=state_filter)
        
        if not sessions:
            click.echo("No sessions found")
            return
        
        click.echo(f"Found {len(sessions)} session(s):")
        click.echo()
        
        for session in sessions:
            click.echo(f"  {session.session_id}")
            click.echo(f"    Name: {session.name}")
            click.echo(f"    State: {session.state.value}")
            click.echo()
        
        # Show statistics
        stats = manager.get_statistics()
        click.echo("Statistics:")
        for state_name, count in stats.items():
            if state_name != "total":
                click.echo(f"  {state_name}: {count}")
        click.echo(f"  Total: {stats['total']}")
        
    else:
        click.echo("Error: Provide session_id or use --all to list sessions", err=True)
        sys.exit(1)


@session.command("list")
@click.option("--state", type=click.Choice([s.value for s in SessionState]), help="Filter by state")
@click.pass_context
def session_list(ctx: click.Context, state: Optional[str]) -> None:
    """List all agent sessions."""
    manager: SessionManager = ctx.obj["manager"]
    manager.load_all()
    
    state_filter = SessionState(state) if state else None
    sessions = manager.list_sessions(state_filter=state_filter)
    
    if not sessions:
        click.echo("No sessions found")
        return
    
    for session in sessions:
        click.echo(f"{session.session_id}\t{session.name}\t{session.state.value}")


if __name__ == "__main__":
    main()
