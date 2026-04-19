#!/usr/bin/env python3
"""
🎯 AGENT COMPLETION HOOK
Se apelează automat când un agent termină un task
Usage: python3 agent_completed.py <agent_name> <task_id> [status]
"""

import sys
import json
from datetime import datetime
from pathlib import Path

AGENTS_DIR = "/workspace/shared/agents"
TASKS_DIR = "/workspace/shared/tasks/auto"
BUGS_DIR = "/workspace/shared/bugs"

def log(message):
    print(f"[COMPLETION] {message}")

def update_agent_status(agent_name, status, task_id=None):
    """Updatează status agent"""
    try:
        status_file = Path(f"{AGENTS_DIR}/{agent_name}/status.json")
        if not status_file.exists():
            return False
        
        with open(status_file) as f:
            data = json.load(f)
        
        data["status"] = status
        data["last_update"] = datetime.now().isoformat()
        
        if task_id and "pending_tasks" in data:
            for task in data["pending_tasks"]:
                if task.get("task_file") and task_id in str(task.get("task_file")):
                    data["pending_tasks"].remove(task)
                    task["completed_at"] = datetime.now().isoformat()
                    task["status"] = "completed"
                    
                    if "completed_tasks" not in data:
                        data["completed_tasks"] = []
                    data["completed_tasks"].append(task)
                    break
        
        with open(status_file, "w") as f:
            json.dump(data, f, indent=2)
        
        log(f"✅ Agent {agent_name} status updated to: {status}")
        return True
    except Exception as e:
        log(f"❌ Error updating agent status: {e}")
        return False

def mark_task_completed(task_id):
    """Marchează task ca completat"""
    try:
        for task_file in Path(TASKS_DIR).glob("*.json"):
            with open(task_file) as f:
                task = json.load(f)
            
            if task.get("id") == task_id or task.get("bug_id") == task_id:
                task["status"] = "completed"
                task["completed_at"] = datetime.now().isoformat()
                task["auto_completed"] = True
                
                with open(task_file, "w") as f:
                    json.dump(task, f, indent=2)
                
                log(f"✅ Task {task_id} marked as completed")
                return True
        
        return False
    except Exception as e:
        log(f"❌ Error marking task completed: {e}")
        return False

def mark_bug_fixed(bug_id):
    """Marchează bug ca fixat"""
    try:
        bug_file = Path(f"{BUGS_DIR}/{bug_id}.md")
        if not bug_file.exists():
            return False
        
        with open(bug_file) as f:
            content = f.read()
        
        content = content.replace("**Status:** OPEN", "**Status:** FIXED")
        content = content.replace("**Status:** ASSIGNED", "**Status:** FIXED")
        
        if "**Fixed At:**" not in content:
            content = content.replace(
                "**Status:** FIXED",
                f"**Status:** FIXED\n**Fixed At:** {datetime.now().isoformat()}"
            )
        
        with open(bug_file, "w") as f:
            f.write(content)
        
        log(f"✅ Bug {bug_id} marked as fixed")
        return True
    except Exception as e:
        log(f"❌ Error marking bug fixed: {e}")
        return False

def trigger_next_tasks():
    """Trigger task-uri următoare care depind de acesta"""
    log("🔄 Checking for dependent tasks...")
    # Aici se poate adăuga logică de trigger chain
    return True

def notify_orchestrator(agent_name, task_id, status):
    """Notifică orchestratorul că task-ul e gata"""
    log(f"📢 Notifying orchestrator: {agent_name} completed {task_id}")
    # Se poate adăuga aici notificare prin webhook/sessions_send
    return True

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 agent_completed.py <agent_name> <task_id> [status]")
        sys.exit(1)
    
    agent_name = sys.argv[1]
    task_id = sys.argv[2]
    status = sys.argv[3] if len(sys.argv) > 3 else "completed"
    
    log(f"🎯 Agent {agent_name} reports completion of {task_id}")
    
    # 1. Update agent status
    update_agent_status(agent_name, status, task_id)
    
    # 2. Mark task completed
    mark_task_completed(task_id)
    
    # 3. If it's a bugfix, mark bug as fixed
    if task_id.startswith("BUGFIX-"):
        bug_id = task_id.replace("BUGFIX-", "")
        mark_bug_fixed(bug_id)
    
    # 4. Trigger next tasks
    trigger_next_tasks()
    
    # 5. Notify orchestrator
    notify_orchestrator(agent_name, task_id, status)
    
    log("✅ Completion process finished")

if __name__ == "__main__":
    main()
