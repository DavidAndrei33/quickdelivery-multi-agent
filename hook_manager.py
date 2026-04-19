#!/usr/bin/env python3
"""
Hook Manager
Central interface for triggering all system hooks
"""

import subprocess
import sys
import json

HOOKS_DIR = "/workspace/shared/hooks"

HOOKS = {
    # Bug tracking
    "bug.detect": "bug_auto_detect.py",
    "bug.create": "bug_auto_detect.py",
    
    # Task management
    "task.update": "task_coordination.py",
    "task.assign": "task_coordination.py",
    "task.check-deps": "task_coordination.py",
    
    # Agent management
    "agent.recover": "agent_recovery.py",
    "agent.check-health": "agent_recovery.py",
    
    # Escalation
    "escalate.bug": "escalation.py",
    "escalate.task": "escalation.py",
    "escalate.agent": "escalation.py",
    "escalate.api": "escalation.py",
    "escalate.margin": "escalation.py",
    "escalate.list": "escalation.py",
    
    # File locking
    "lock.acquire": "file_lock.py",
    "lock.release": "file_lock.py",
    "lock.check": "file_lock.py",
    "lock.list": "file_lock.py",
    
    # Notifications
    "notify.send": "notification.py",
    "notify.task": "notification.py",
    "notify.bug": "notification.py",
    "notify.list": "notification.py",
    "notify.read": "notification.py",
}

def run_hook(hook_name, args=None):
    """Run a hook with arguments."""
    
    if hook_name not in HOOKS:
        print(f"[HOOK-MANAGER] Unknown hook: {hook_name}")
        print(f"[HOOK-MANAGER] Available: {', '.join(HOOKS.keys())}")
        return False
    
    script = HOOKS[hook_name]
    cmd = [sys.executable, f"{HOOKS_DIR}/{script}"]
    
    if args:
        if isinstance(args, list):
            cmd.extend(args)
        else:
            cmd.append(args)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        
        return result.returncode == 0
    
    except subprocess.TimeoutExpired:
        print(f"[HOOK-MANAGER] Hook {hook_name} timed out")
        return False
    except Exception as e:
        print(f"[HOOK-MANAGER] Error running hook: {e}")
        return False

def main():
    """Main entry point."""
    
    if len(sys.argv) < 2:
        print("Hook Manager - Usage:")
        print("")
        print("  hook_manager.py <hook_name> [args...]")
        print("")
        print("Available hooks:")
        for hook in sorted(HOOKS.keys()):
            print(f"  - {hook}")
        print("")
        print("Examples:")
        print("  hook_manager.py bug.detect '{\"error_type\": \"API_ERROR\", \"component\": \"Dashboard\"}'")
        print("  hook_manager.py task.assign builder-1")
        print("  hook_manager.py agent.recover builder-1")
        print("  hook_manager.py lock.acquire /path/to/file.txt builder-1")
        print("  hook_manager.py notify.task builder-1 TASK-001 \"Fix Dashboard\"")
        return
    
    hook_name = sys.argv[1]
    args = sys.argv[2:]
    
    success = run_hook(hook_name, args)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
