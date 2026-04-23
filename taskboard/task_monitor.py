#!/usr/bin/env python3
"""
Task Monitor - Background service
Monitors for new tasks in 'todo' status and triggers notifications
"""

import json
import time
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api import load_data, save_data, DATA_FILE
from notifier import notifier, AGENT_BOTS, OWNER_CHAT_ID

# Track already notified tasks
NOTIFIED_TASKS_FILE = os.path.join(os.path.dirname(__file__), '.notified_tasks.json')

def load_notified_tasks():
    """Load list of already notified task IDs"""
    try:
        with open(NOTIFIED_TASKS_FILE, 'r') as f:
            return set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()

def save_notified_tasks(task_ids):
    """Save list of notified task IDs"""
    try:
        with open(NOTIFIED_TASKS_FILE, 'w') as f:
            json.dump(list(task_ids), f)
    except Exception as e:
        print(f"❌ Error saving notified tasks: {e}")

def check_new_tasks():
    """Check for new tasks in 'todo' status and notify agents"""
    try:
        data = load_data()
        notified = load_notified_tasks()
        
        # Find tasks in 'todo' that haven't been notified
        for task in data.get('tasks', []):
            task_id = task.get('id')
            
            if task.get('status') == 'todo' and task_id not in notified:
                agent_key = task.get('agent')
                
                if not agent_key:
                    print(f"⚠️ Task {task_id} has no agent assigned")
                    continue
                
                # Get agent info
                agent_info = data.get('agents', {}).get(agent_key, {})
                task['agent_name'] = agent_info.get('name', agent_key)
                
                # Try to get chat ID from previous interactions or use owner
                chat_id = task.get('agent_chat_id', OWNER_CHAT_ID)
                task['agent_chat_id'] = chat_id
                
                # Send notification
                print(f"🔔 Notifying {agent_key} about task {task_id}")
                result = notifier.send_task_notification(agent_key, task, 'new')
                
                if result:
                    notified.add(task_id)
                    print(f"✅ Notification sent for {task_id}")
                else:
                    print(f"❌ Failed to notify about {task_id}")
        
        # Save notified tasks
        save_notified_tasks(notified)
        
    except Exception as e:
        print(f"❌ Monitor error: {e}")

def start_monitor():
    """Start the background monitor loop"""
    print("🚀 Task Monitor started")
    print("⏱️  Checking for new tasks every 5 seconds...")
    
    while True:
        try:
            check_new_tasks()
            time.sleep(5)  # Check every 5 seconds
        except KeyboardInterrupt:
            print("\n🛑 Monitor stopped")
            break
        except Exception as e:
            print(f"❌ Monitor loop error: {e}")
            time.sleep(5)  # Wait before retry

if __name__ == '__main__':
    start_monitor()
