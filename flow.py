#!/usr/bin/env python3
import os
import sys
import time
import sqlite3
import argparse
from datetime import datetime, date

try:
    from rich.console import Console
    from rich.progress import Progress, TextColumn, BarColumn, TimeRemainingColumn, TaskProgressColumn
    from rich.panel import Panel
    from rich.table import Table
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

DB_PATH = os.path.expanduser('~/.flow_cli.db')

if RICH_AVAILABLE:
    console = Console()
else:
    console = None

def init_db():
    """Initialize the SQLite database for tracking sessions."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_type TEXT NOT NULL,
            duration_minutes INTEGER NOT NULL,
            completed_at DATE DEFAULT CURRENT_DATE
        )
    ''')
    conn.commit()
    return conn

def log_session(conn, session_type, duration_minutes):
    """Log a completed session to the database."""
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO sessions (session_type, duration_minutes, completed_at) VALUES (?, ?, ?)',
        (session_type, duration_minutes, date.today().isoformat())
    )
    conn.commit()

def run_timer(minutes, session_type="Focus"):
    """Run the countdown timer with a beautiful rich progress bar."""
    if not RICH_AVAILABLE:
        print(f"Starting {session_type} for {minutes} minutes...")
        time.sleep(minutes * 60)
        print(f"{session_type} session complete!")
        return True

    total_seconds = minutes * 60
    color = "[green]" if session_type == "Focus" else "[cyan]"
    
    console.print(f"\n{color}▶ Starting {session_type} Session ({minutes} min)[/]\n")
    
    try:
        with Progress(
            TextColumn(f"{color}[progress.description]{{task.description}}"),
            BarColumn(bar_width=40, complete_style="green" if session_type == "Focus" else "cyan"),
            TaskProgressColumn(),
            TimeRemainingColumn(),
            console=console
        ) as progress:
            task = progress.add_task(f"{session_type}...", total=total_seconds)
            
            while not progress.finished:
                time.sleep(1)
                progress.update(task, advance=1)
                
        console.print(f"\n✨ [bold gold1]Great job! {session_type} session complete.[/bold gold1]\n")
        # Terminal bell to notify user
        sys.stdout.write('\a')
        sys.stdout.flush()
        return True
        
    except KeyboardInterrupt:
        console.print("\n[bold red]⏹ Session interrupted. Take a breath![/bold red]\n")
        return False

def show_stats(conn):
    """Show daily and all-time stats."""
    if not RICH_AVAILABLE:
        print("Install 'rich' library to see beautiful stats.")
        return

    cursor = conn.cursor()
    today = date.today().isoformat()
    
    # Get today's focus minutes
    cursor.execute(
        "SELECT SUM(duration_minutes) FROM sessions WHERE session_type='Focus' AND completed_at=?",
        (today,)
    )
    today_focus = cursor.fetchone()[0] or 0
    
    # Get all-time focus minutes
    cursor.execute(
        "SELECT SUM(duration_minutes) FROM sessions WHERE session_type='Focus'"
    )
    all_time_focus = cursor.fetchone()[0] or 0
    
    # Get today's count
    cursor.execute(
        "SELECT COUNT(*) FROM sessions WHERE session_type='Focus' AND completed_at=?",
        (today,)
    )
    today_count = cursor.fetchone()[0] or 0

    table = Table(title=f"📊 Flow Stats for {today}")
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Value", justify="right", style="green")
    
    table.add_row("Today's Focus Time", f"{today_focus} minutes")
    table.add_row("Completed Sessions Today", str(today_count))
    table.add_row("All-Time Focus Time", f"{all_time_focus} minutes")
    
    console.print(table)
    
    # Motivation message
    if today_focus >= 120:
        console.print("[bold green]🔥 You are on fire today! Don't forget to take breaks.[/bold green]")
    elif today_focus > 0:
        console.print("[bold blue]👍 Good start. Keep the momentum going![/bold blue]")
    else:
        console.print("[dim]No focus sessions logged today yet. Time to get started![/dim]")

def main():
    parser = argparse.ArgumentParser(description="flow-cli - A beautiful minimalist Pomodoro & Focus timer.")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Start command
    start_parser = subparsers.add_parser('start', help='Start a focus session')
    start_parser.add_argument('-m', '--minutes', type=int, default=25, help='Duration in minutes (default: 25)')
    
    # Break command
    break_parser = subparsers.add_parser('break', help='Start a break session')
    break_parser.add_argument('-m', '--minutes', type=int, default=5, help='Duration in minutes (default: 5)')
    
    # Stats command
    subparsers.add_parser('stats', help='Show focus statistics')

    args = parser.parse_args()
    
    if not getattr(sys, 'frozen', False) and not RICH_AVAILABLE and args.command != 'help':
        print("Note: 'rich' library not found. Falling back to plain text mode. Run 'pip install rich' for a beautiful UI.\n")

    conn = init_db()
    
    try:
        if args.command == 'start':
            success = run_timer(args.minutes, "Focus")
            if success:
                log_session(conn, "Focus", args.minutes)
        elif args.command == 'break':
            success = run_timer(args.minutes, "Break")
            if success:
                log_session(conn, "Break", args.minutes)
        elif args.command == 'stats':
            show_stats(conn)
        else:
            parser.print_help()
    finally:
        conn.close()

if __name__ == '__main__':
    main()
