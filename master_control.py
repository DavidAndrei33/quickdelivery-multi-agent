#!/usr/bin/env python3
"""
Master Control Script for Multi-Agent System
Orchestrates all components: hooks, cron jobs, task board, bug tracking
"""

import json
import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

# Paths
BASE_DIR = "/workspace/shared"
CONFIG_DIR = f"{BASE_DIR}/config"
TASKS_DIR = f"{BASE_DIR}/tasks"
BUGS_DIR = f"{BASE_DIR}/bugs"
HOOKS_DIR = f"{BASE_DIR}/hooks"
CRON_DIR = f"{BASE_DIR}/cron"

def log(message):
    """Log with timestamp."""
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def check_system_health():
    """Check if all components are in place."""
    log("Checking system health...")
    
    components = {
        "Team Config": f"{CONFIG_DIR}/team_orchestration.json",
        "Task Board": f"{TASKS_DIR}/TASKBOARD.json",
        "Standing Orders": f"{BASE_DIR}/docs/STANDING_ORDERS.md",
        "Bug Tracking": f"{BASE_DIR}/docs/BUG_TRACKING_SYSTEM.md",
        "Communication Rules": f"{BASE_DIR}/docs/AGENT_COMMUNICATION_RULES.md",
        "Heartbeat Config": f"{CONFIG_DIR}/HEARTBEAT.md",
        "Bug Auto-Detect Hook": f"{HOOKS_DIR}/bug_auto_detect.py",
        "Task Coordination Hook": f"{HOOKS_DIR}/task_coordination.py",
    }
    
    all_ok = True
    for name, path in components.items():
        if os.path.exists(path):
            log(f"  ✅ {name}")
        else:
            log(f"  ❌ {name} - MISSING")
            all_ok = False
    
    return all_ok

def initialize_system():
    """Initialize the multi-agent system."""
    log("=" * 60)
    log("INITIALIZING MULTI-AGENT SYSTEM")
    log("=" * 60)
    
    # Check health
    if not check_system_health():
        log("ERROR: System components missing!")
        return False
    
    # Create necessary directories
    dirs = [
        f"{BASE_DIR}/logs",
        f"{BASE_DIR}/memory/agents",
        f"{TASKS_DIR}/inbox",
        f"{TASKS_DIR}/active",
        f"{TASKS_DIR}/completed",
        f"{BUGS_DIR}/open",
        f"{BUGS_DIR}/closed",
        f"{BASE_DIR}/artifacts/v31",
        f"{BASE_DIR}/artifacts/v32",
        f"{BASE_DIR}/artifacts/v33",
    ]
    
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    
    log("✅ All directories created")
    
    # Verify task board
    try:
        with open(f"{TASKS_DIR}/TASKBOARD.json") as f:
            taskboard = json.load(f)
        log(f"✅ Task board loaded: {len(taskboard['tasks']['active'])} active tasks")
    except Exception as e:
        log(f"❌ Task board error: {e}")
        return False
    
    # Verify agent config
    try:
        with open(f"{CONFIG_DIR}/team_orchestration.json") as f:
            config = json.load(f)
        agents = len(config['agents']['builders']) + len(config['agents']['reviewers']) + len(config['agents']['ops'])
        log(f"✅ Team config loaded: {agents} agents configured")
    except Exception as e:
        log(f"❌ Team config error: {e}")
        return False
    
    log("=" * 60)
    log("SYSTEM INITIALIZED SUCCESSFULLY")
    log("=" * 60)
    
    return True

def run_heartbeat():
    """Run a single heartbeat cycle."""
    log("Running heartbeat cycle...")
    
    # Run individual cron jobs
    cron_jobs = [
        ("Agent Heartbeat", f"{CRON_DIR}/agent_heartbeat.py"),
        ("Task Board Sync", f"{CRON_DIR}/task_board_sync.py"),
        ("Bug Triage", f"{CRON_DIR}/bug_triage.py"),
        ("Dashboard Health", f"{CRON_DIR}/dashboard_health.py"),
    ]
    
    for name, script in cron_jobs:
        if os.path.exists(script):
            try:
                result = subprocess.run(
                    [sys.executable, script],
                    capture_output=True,
                    timeout=30
                )
                if result.returncode == 0:
                    log(f"  ✅ {name}")
                else:
                    log(f"  ⚠️  {name} - check logs")
            except Exception as e:
                log(f"  ❌ {name} - {e}")
        else:
            log(f"  ⚠️  {name} - script not found")
    
    log("Heartbeat cycle complete")

def show_status():
    """Show current system status."""
    log("=" * 60)
    log("SYSTEM STATUS")
    log("=" * 60)
    
    # Task board summary
    try:
        with open(f"{TASKS_DIR}/TASKBOARD.json") as f:
            tb = json.load(f)
        
        log(f"📋 TASKS:")
        log(f"  Inbox: {len(tb['tasks']['inbox'])}")
        log(f"  Active: {len(tb['tasks']['active'])}")
        log(f"  Review: {len(tb['tasks']['review'])}")
        log(f"  Completed: {len(tb['tasks']['completed'])}")
        
        log(f"🐛 BUGS:")
        log(f"  Open: {len(tb['bugs']['open'])}")
        log(f"  Closed: {len(tb['bugs']['closed'])}")
        
        log(f"🤖 AGENTS:")
        for agent_id, info in tb['agent_status'].items():
            status = info.get('status', 'unknown')
            task = info.get('current_task', 'idle')
            log(f"  {agent_id}: {status} ({task})")
            
    except Exception as e:
        log(f"❌ Error reading status: {e}")
    
    log("=" * 60)

def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: master_control.py <command>")
        print("")
        print("Commands:")
        print("  init      - Initialize the system")
        print("  heartbeat - Run heartbeat cycle")
        print("  status    - Show system status")
        print("  help      - Show this help")
        return
    
    command = sys.argv[1]
    
    if command == "init":
        success = initialize_system()
        sys.exit(0 if success else 1)
    
    elif command == "heartbeat":
        run_heartbeat()
    
    elif command == "status":
        show_status()
    
    elif command == "help":
        print("Multi-Agent System Master Control")
        print("")
        print("Commands:")
        print("  init      - Initialize the system")
        print("  heartbeat - Run heartbeat cycle")
        print("  status    - Show system status")
    
    else:
        log(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
