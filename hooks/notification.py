#!/usr/bin/env python3
"""
Notification Hook
Sends notifications to agents and orchestrator
"""

import json
import os
from datetime import datetime
from pathlib import Path

NOTIFICATIONS_PATH = "/workspace/shared/logs/notifications.log"

def send_notification(target, message, priority="normal", source="system"):
    """Send a notification to a target (agent_id or 'orchestrator')."""
    
    notification = {
        "timestamp": datetime.utcnow().isoformat(),
        "target": target,
        "source": source,
        "message": message,
        "priority": priority,  # low, normal, high, urgent
        "read": False
    }
    
    # Log notification
    with open(NOTIFICATIONS_PATH, 'a') as f:
        f.write(json.dumps(notification) + "\n")
    
    # Print for visibility
    priority_emoji = {
        "low": "🔵",
        "normal": "⚪",
        "high": "🟡",
        "urgent": "🔴"
    }
    
    emoji = priority_emoji.get(priority, "⚪")
    print(f"[NOTIFY] {emoji} [{priority.upper()}] To {target}: {message}")
    
    return notification

def notify_task_assigned(agent_id, task_id, task_title):
    """Notify agent of new task assignment."""
    
    return send_notification(
        target=agent_id,
        message=f"New task assigned: {task_id} - {task_title}",
        priority="normal",
        source="task_coordination"
    )

def notify_task_completed(agent_id, task_id):
    """Notify orchestrator of task completion."""
    
    return send_notification(
        target="orchestrator",
        message=f"Task {task_id} completed by {agent_id}",
        priority="normal",
        source="task_coordination"
    )

def notify_bug_created(bug_id, assigned_to, priority):
    """Notify assigned agent of new bug."""
    
    return send_notification(
        target=assigned_to,
        message=f"Bug {bug_id} assigned to you (Priority: {priority})",
        priority="high" if priority in ["CRITICAL", "HIGH"] else "normal",
        source="bug_auto_detect"
    )

def notify_bug_fixed(bug_id, fixed_by):
    """Notify QA of bug fix for verification."""
    
    return send_notification(
        target="reviewer-3",  # QA-Tester
        message=f"Bug {bug_id} fixed by {fixed_by} - please verify",
        priority="normal",
        source="bug_auto_detect"
    )

def notify_agent_recovered(agent_id, task_id=None):
    """Notify that agent recovered successfully."""
    
    return send_notification(
        target="orchestrator",
        message=f"Agent {agent_id} recovered successfully" + (f" (task: {task_id})" if task_id else ""),
        priority="normal",
        source="agent_recovery"
    )

def notify_escalation(alert_type, message):
    """Notify orchestrator of escalation."""
    
    return send_notification(
        target="orchestrator",
        message=f"ESCALATION [{alert_type}]: {message}",
        priority="urgent",
        source="escalation"
    )

def list_unread_notifications(target=None):
    """List unread notifications."""
    
    if not os.path.exists(NOTIFICATIONS_PATH):
        return []
    
    notifications = []
    with open(NOTIFICATIONS_PATH) as f:
        for line in f:
            try:
                notif = json.loads(line.strip())
                if not notif.get('read', False):
                    if target is None or notif['target'] == target:
                        notifications.append(notif)
            except:
                continue
    
    return notifications

def mark_as_read(target):
    """Mark all notifications for target as read."""
    
    if not os.path.exists(NOTIFICATIONS_PATH):
        return
    
    lines = []
    with open(NOTIFICATIONS_PATH) as f:
        for line in f:
            try:
                notif = json.loads(line.strip())
                if notif['target'] == target:
                    notif['read'] = True
                lines.append(json.dumps(notif))
            except:
                lines.append(line.strip())
    
    with open(NOTIFICATIONS_PATH, 'w') as f:
        f.write('\n'.join(lines) + '\n')
    
    print(f"[NOTIFY] Marked all notifications for {target} as read")

def main():
    """Main hook execution."""
    
    import sys
    
    if len(sys.argv) < 2:
        # List recent notifications
        notifications = list_unread_notifications()
        if notifications:
            print(f"\n📬 {len(notifications)} unread notifications")
        else:
            print("\n📬 No unread notifications")
        return
    
    command = sys.argv[1]
    
    if command == "send":
        target = sys.argv[2]
        message = sys.argv[3]
        priority = sys.argv[4] if len(sys.argv) > 4 else "normal"
        send_notification(target, message, priority)
    
    elif command == "task":
        agent_id = sys.argv[2]
        task_id = sys.argv[3]
        task_title = sys.argv[4] if len(sys.argv) > 4 else "New Task"
        notify_task_assigned(agent_id, task_id, task_title)
    
    elif command == "bug":
        bug_id = sys.argv[2]
        assigned_to = sys.argv[3]
        priority = sys.argv[4] if len(sys.argv) > 4 else "HIGH"
        notify_bug_created(bug_id, assigned_to, priority)
    
    elif command == "list":
        target = sys.argv[2] if len(sys.argv) > 2 else None
        notifications = list_unread_notifications(target)
        
        if notifications:
            print(f"\n📬 Unread notifications for {target or 'all'}:")
            for n in notifications:
                print(f"  [{n['priority']}] {n['message']}")
        else:
            print(f"\n📬 No unread notifications for {target or 'all'}")
    
    elif command == "read":
        target = sys.argv[2]
        mark_as_read(target)
    
    else:
        print(f"[NOTIFY] Unknown command: {command}")

if __name__ == "__main__":
    main()
