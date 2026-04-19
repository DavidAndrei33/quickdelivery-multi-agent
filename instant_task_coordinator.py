#!/usr/bin/env python3
"""
Instant Task Coordinator - Triggered immediately when TASKBOARD changes
Usage: python3 /workspace/shared/instant_task_coordinator.py
"""

import json
import os
import sys
from datetime import datetime

TASKBOARD_PATH = "/workspace/shared/tasks/TASKBOARD.json"
LOG_PATH = "/workspace/shared/logs/instant-coordinator.log"

def log_message(msg):
    timestamp = datetime.now().isoformat()
    log_entry = f"[{timestamp}] {msg}"
    print(log_entry)
    with open(LOG_PATH, "a") as f:
        f.write(log_entry + "\n")

def check_and_notify():
    """Check TASKBOARD and return tasks that need immediate attention."""
    
    if not os.path.exists(TASKBOARD_PATH):
        log_message("ERROR: TASKBOARD.json not found")
        return []
    
    try:
        with open(TASKBOARD_PATH) as f:
            taskboard = json.load(f)
        
        urgent_tasks = []
        
        # Check active tasks
        for task in taskboard.get("tasks", {}).get("active", []):
            if task.get("status") == "IN_PROGRESS":
                urgent_tasks.append({
                    "id": task["id"],
                    "title": task["title"],
                    "assigned_to": task.get("assigned_to"),
                    "priority": task.get("priority", "NORMAL")
                })
        
        # Check review tasks
        for task in taskboard.get("tasks", {}).get("review", []):
            if task.get("status") == "IN_REVIEW":
                urgent_tasks.append({
                    "id": task["id"],
                    "title": task["title"],
                    "assigned_to": task.get("reviewer"),
                    "priority": "HIGH"
                })
        
        return urgent_tasks
        
    except Exception as e:
        log_message(f"ERROR: {e}")
        return []

def main():
    tasks = check_and_notify()
    
    if tasks:
        log_message(f"Found {len(tasks)} active tasks requiring attention:")
        for task in tasks:
            log_message(f"  - {task['id']}: {task['title']} -> @{task['assigned_to']} ({task['priority']})")
    else:
        log_message("No urgent tasks found")
    
    return tasks

if __name__ == "__main__":
    urgent = main()
    # Return tasks as JSON for further processing
    print(json.dumps(urgent))
