#!/usr/bin/env python3
"""
Agent Recovery Hook
Triggered when: Agent heartbeat stalled > 5 minutes
Actions: Attempts recovery, reassigns tasks, notifies orchestrator
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

AGENT_STATUS_PATH = "/workspace/shared/config/agent_status.json"
TASKBOARD_PATH = "/workspace/shared/tasks/TASKBOARD.json"

def check_agent_health(agent_id):
    """Check if agent is healthy based on last heartbeat."""
    
    with open(AGENT_STATUS_PATH) as f:
        status = json.load(f)
    
    agent = status.get('agents', {}).get(agent_id)
    if not agent:
        return False, "Agent not found in registry"
    
    last_heartbeat = datetime.fromisoformat(agent.get('last_heartbeat', '1970-01-01'))
    threshold = datetime.utcnow() - timedelta(minutes=5)
    
    if last_heartbeat < threshold:
        return False, f"Last heartbeat: {last_heartbeat.isoformat()}"
    
    return True, "Healthy"

def recover_agent(agent_id):
    """Attempt to recover a stalled agent."""
    
    print(f"[RECOVERY] Attempting recovery for {agent_id}...")
    
    # Step 1: Check if agent has current task
    with open(TASKBOARD_PATH) as f:
        taskboard = json.load(f)
    
    current_task = None
    for task in taskboard['tasks']['active']:
        if task.get('assigned_to') == agent_id:
            current_task = task
            break
    
    if current_task:
        print(f"[RECOVERY] {agent_id} has task {current_task['id']}")
        
        # Check retry count
        retry_count = current_task.get('retry_count', 0)
        
        if retry_count < 3:
            # Retry the task
            current_task['retry_count'] = retry_count + 1
            current_task['last_retry'] = datetime.utcnow().isoformat()
            
            with open(TASKBOARD_PATH, 'w') as f:
                json.dump(taskboard, f, indent=2)
            
            print(f"[RECOVERY] Task {current_task['id']} retry #{retry_count + 1}")
            
            # Reset agent status
            with open(AGENT_STATUS_PATH) as f:
                status = json.load(f)
            
            status['agents'][agent_id]['status'] = 'recovering'
            status['agents'][agent_id]['recovery_attempts'] = status['agents'][agent_id].get('recovery_attempts', 0) + 1
            
            with open(AGENT_STATUS_PATH, 'w') as f:
                json.dump(status, f, indent=2)
            
            return "retry_task", current_task['id']
        
        else:
            # Max retries reached - reassign
            print(f"[RECOVERY] Max retries reached for {current_task['id']}")
            return "reassign", current_task['id']
    
    else:
        # No task - just mark as available
        print(f"[RECOVERY] {agent_id} has no active task")
        
        with open(AGENT_STATUS_PATH) as f:
            status = json.load(f)
        
        status['agents'][agent_id]['status'] = 'available'
        status['agents'][agent_id]['last_heartbeat'] = datetime.utcnow().isoformat()
        
        with open(AGENT_STATUS_PATH, 'w') as f:
            json.dump(status, f, indent=2)
        
        return "reset_available", None

def reassign_task(task_id, from_agent):
    """Reassign task to different agent."""
    
    with open(TASKBOARD_PATH) as f:
        taskboard = json.load(f)
    
    # Find task
    task = None
    for t in taskboard['tasks']['active']:
        if t['id'] == task_id:
            task = t
            break
    
    if not task:
        print(f"[RECOVERY] Task {task_id} not found")
        return None
    
    # Find available agent with same specialty
    with open(AGENT_STATUS_PATH) as f:
        status = json.load(f)
    
    component = task.get('component', 'General')
    
    # Map component to agent types
    component_agents = {
        'API': ['builder-1', 'builder-2', 'builder-3'],
        'Dashboard': ['builder-4', 'builder-5'],
        'Integration': ['builder-6', 'builder-7'],
        'Database': ['ops-2'],
        'DevOps': ['ops-1']
    }
    
    candidates = component_agents.get(component, ['builder-1', 'builder-2'])
    
    new_agent = None
    for candidate in candidates:
        if candidate != from_agent:
            agent_status = status['agents'].get(candidate, {})
            if agent_status.get('status') == 'available':
                new_agent = candidate
                break
    
    if not new_agent:
        # No available agent - move to blocked
        taskboard['tasks']['active'].remove(task)
        task['status'] = 'Blocked'
        task['blocked_reason'] = f'Agent {from_agent} failed, no replacement available'
        taskboard['tasks']['blocked'].append(task)
        
        with open(TASKBOARD_PATH, 'w') as f:
            json.dump(taskboard, f, indent=2)
        
        print(f"[RECOVERY] Task {task_id} moved to blocked (no available agents)")
        return None
    
    # Reassign
    task['assigned_to'] = new_agent
    task['previous_agent'] = from_agent
    task['reassigned_at'] = datetime.utcnow().isoformat()
    task['retry_count'] = 0
    
    with open(TASKBOARD_PATH, 'w') as f:
        json.dump(taskboard, f, indent=2)
    
    # Update agent status
    status['agents'][from_agent]['status'] = 'failed'
    status['agents'][from_agent]['current_task'] = None
    status['agents'][new_agent]['status'] = 'assigned'
    status['agents'][new_agent]['current_task'] = task_id
    
    with open(AGENT_STATUS_PATH, 'w') as f:
        json.dump(status, f, indent=2)
    
    print(f"[RECOVERY] Task {task_id} reassigned: {from_agent} → {new_agent}")
    
    # Trigger notification
    print(f"[NOTIFICATION] Task {task_id} reassigned to {new_agent}")
    
    return new_agent

def main():
    """Main hook execution."""
    
    import sys
    
    if len(sys.argv) < 2:
        # Check all agents
        with open(AGENT_STATUS_PATH) as f:
            status = json.load(f)
        
        for agent_id in status.get('agents', {}):
            healthy, reason = check_agent_health(agent_id)
            
            if not healthy:
                print(f"[RECOVERY] {agent_id}: UNHEALTHY - {reason}")
                action, task_id = recover_agent(agent_id)
                
                if action == "reassign" and task_id:
                    reassign_task(task_id, agent_id)
            else:
                print(f"[RECOVERY] {agent_id}: Healthy")
    
    else:
        # Check specific agent
        agent_id = sys.argv[1]
        healthy, reason = check_agent_health(agent_id)
        
        if not healthy:
            print(f"[RECOVERY] {agent_id}: UNHEALTHY - {reason}")
            action, task_id = recover_agent(agent_id)
            
            if action == "reassign" and task_id:
                reassign_task(task_id, agent_id)
        else:
            print(f"[RECOVERY] {agent_id}: Healthy")

if __name__ == "__main__":
    main()
