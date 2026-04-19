#!/usr/bin/env python3
"""
Task Coordination Hook
Triggered when: Task state changes, new tasks created
Actions: Updates taskboard, notifies relevant agents, manages dependencies
"""

import json
import os
from datetime import datetime
from pathlib import Path

TASKBOARD_PATH = "/workspace/shared/tasks/TASKBOARD.json"
AGENT_STATUS_PATH = "/workspace/shared/config/agent_status.json"

def update_task_status(task_id, new_status, agent_id=None, comment=None):
    """Update task status and notify relevant parties."""
    
    with open(TASKBOARD_PATH) as f:
        taskboard = json.load(f)
    
    # Find task in any list
    task = None
    task_location = None
    
    for location in ['inbox', 'active', 'review', 'blocked', 'failed']:
        for t in taskboard['tasks'][location]:
            if t['id'] == task_id:
                task = t
                task_location = location
                break
        if task:
            break
    
    if not task:
        print(f"[TASK-HOOK] ERROR: Task {task_id} not found")
        return False
    
    # Update task
    task['status'] = new_status
    task['updated_at'] = datetime.utcnow().isoformat()
    
    if agent_id:
        task['assigned_to'] = agent_id
    
    if comment:
        task['comments'] = task.get('comments', [])
        task['comments'].append({
            'agent': agent_id or 'system',
            'timestamp': datetime.utcnow().isoformat(),
            'text': comment
        })
    
    # Move between lists if status changed significantly
    if new_status in ['Done', 'Completed'] and task_location != 'completed':
        taskboard['tasks'][task_location].remove(task)
        taskboard['tasks']['completed'].append(task)
        print(f"[TASK-HOOK] Task {task_id} moved to completed")
    
    elif new_status in ['Failed', 'Error'] and task_location != 'failed':
        taskboard['tasks'][task_location].remove(task)
        taskboard['tasks']['failed'].append(task)
        print(f"[TASK-HOOK] Task {task_id} moved to failed")
    
    # Save
    with open(TASKBOARD_PATH, 'w') as f:
        json.dump(taskboard, f, indent=2)
    
    print(f"[TASK-HOOK] Task {task_id} status: {new_status}")
    return True

def check_dependencies(task_id):
    """Check if task dependencies are satisfied."""
    
    with open(TASKBOARD_PATH) as f:
        taskboard = json.load(f)
    
    # Find task
    task = None
    for location in ['inbox', 'active', 'review', 'blocked']:
        for t in taskboard['tasks'][location]:
            if t['id'] == task_id:
                task = t
                break
        if task:
            break
    
    if not task or not task.get('dependencies'):
        return True, []
    
    blocked_by = []
    for dep_id in task['dependencies']:
        # Check if dependency is completed
        dep_completed = any(
            t['id'] == dep_id 
            for t in taskboard['tasks']['completed']
        )
        if not dep_completed:
            blocked_by.append(dep_id)
    
    return len(blocked_by) == 0, blocked_by

def assign_next_available_task(agent_id):
    """Assign next available task to agent."""
    
    with open(TASKBOARD_PATH) as f:
        taskboard = json.load(f)
    
    # Find first unassigned inbox task with satisfied dependencies
    for task in taskboard['tasks']['inbox']:
        deps_ok, blocked = check_dependencies(task['id'])
        if deps_ok:
            # Move to active
            taskboard['tasks']['inbox'].remove(task)
            task['assigned_to'] = agent_id
            task['status'] = 'Assigned'
            task['assigned_at'] = datetime.utcnow().isoformat()
            taskboard['tasks']['active'].append(task)
            
            with open(TASKBOARD_PATH, 'w') as f:
                json.dump(taskboard, f, indent=2)
            
            print(f"[TASK-HOOK] Assigned {task['id']} to {agent_id}")
            return task['id']
    
    print(f"[TASK-HOOK] No available tasks for {agent_id}")
    return None

def main():
    """Main hook execution."""
    
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: task_coordination.py <action> [args...]")
        return
    
    action = sys.argv[1]
    
    if action == "update":
        task_id = sys.argv[2]
        new_status = sys.argv[3]
        agent_id = sys.argv[4] if len(sys.argv) > 4 else None
        update_task_status(task_id, new_status, agent_id)
    
    elif action == "assign":
        agent_id = sys.argv[2]
        assign_next_available_task(agent_id)
    
    elif action == "check-deps":
        task_id = sys.argv[2]
        ok, blocked = check_dependencies(task_id)
        print(f"Dependencies for {task_id}: {'OK' if ok else 'BLOCKED by ' + str(blocked)}")
    
    else:
        print(f"[TASK-HOOK] Unknown action: {action}")

if __name__ == "__main__":
    main()
