#!/usr/bin/env python3
"""
Escalation Hook
Triggered when: Critical issues, task blocked > 2h, max retries reached
Actions: Escalates to orchestrator/human, creates high-priority alert
"""

import json
import os
from datetime import datetime
from pathlib import Path

ALERTS_PATH = "/workspace/shared/logs/alerts.log"
TASKBOARD_PATH = "/workspace/shared/tasks/TASKBOARD.json"

def create_alert(alert_type, severity, message, details=None):
    """Create an escalation alert."""
    
    timestamp = datetime.utcnow().isoformat()
    
    alert = {
        "timestamp": timestamp,
        "type": alert_type,
        "severity": severity,  # CRITICAL, HIGH, MEDIUM
        "message": message,
        "details": details or {},
        "status": "OPEN",
        "acknowledged_by": None
    }
    
    # Append to alerts log
    with open(ALERTS_PATH, 'a') as f:
        f.write(json.dumps(alert) + "\n")
    
    print(f"[ESCALATION] {severity}: {message}")
    
    # Format for display
    print("\n" + "=" * 60)
    print("🚨 ESCALATION ALERT 🚨")
    print("=" * 60)
    print(f"Type: {alert_type}")
    print(f"Severity: {severity}")
    print(f"Time: {timestamp}")
    print(f"Message: {message}")
    if details:
        print(f"Details: {json.dumps(details, indent=2)}")
    print("=" * 60 + "\n")
    
    return alert

def escalate_critical_bug(bug_id, component):
    """Escalate critical bug that couldn't be auto-resolved."""
    
    return create_alert(
        alert_type="CRITICAL_BUG",
        severity="CRITICAL",
        message=f"Bug {bug_id} requires immediate attention",
        details={
            "bug_id": bug_id,
            "component": component,
            "auto_resolution": "FAILED",
            "action_required": "Manual intervention needed"
        }
    )

def escalate_blocked_task(task_id, reason, duration_hours):
    """Escalate task blocked for too long."""
    
    return create_alert(
        alert_type="BLOCKED_TASK",
        severity="HIGH",
        message=f"Task {task_id} blocked for {duration_hours}h",
        details={
            "task_id": task_id,
            "blocked_reason": reason,
            "duration_hours": duration_hours,
            "action_required": "Review and unblock or reassign"
        }
    )

def escalate_agent_failure(agent_id, failure_reason):
    """Escalate agent that failed recovery."""
    
    return create_alert(
        alert_type="AGENT_FAILURE",
        severity="HIGH",
        message=f"Agent {agent_id} failed and could not recover",
        details={
            "agent_id": agent_id,
            "failure_reason": failure_reason,
            "action_required": "Investigate agent configuration or spawn replacement"
        }
    )

def escalate_api_outage(endpoint, error_count):
    """Escalate API that is down."""
    
    return create_alert(
        alert_type="API_OUTAGE",
        severity="CRITICAL",
        message=f"API {endpoint} is down ({error_count} errors)",
        details={
            "endpoint": endpoint,
            "error_count": error_count,
            "action_required": "Check MT5 Core Server status"
        }
    )

def escalate_margin_warning(current_margin, threshold=150):
    """Escalate trading margin warning."""
    
    return create_alert(
        alert_type="MARGIN_WARNING",
        severity="CRITICAL",
        message=f"Margin level at {current_margin}% (below {threshold}% threshold)",
        details={
            "current_margin": current_margin,
            "threshold": threshold,
            "action_required": "Close positions or add funds immediately"
        }
    )

def list_open_alerts():
    """List all open alerts."""
    
    if not os.path.exists(ALERTS_PATH):
        print("No alerts found")
        return []
    
    alerts = []
    with open(ALERTS_PATH) as f:
        for line in f:
            try:
                alert = json.loads(line.strip())
                if alert.get('status') == 'OPEN':
                    alerts.append(alert)
            except:
                continue
    
    if not alerts:
        print("No open alerts")
        return []
    
    print("\n📋 OPEN ALERTS:")
    print("-" * 60)
    for alert in alerts:
        print(f"[{alert['severity']}] {alert['type']}: {alert['message']}")
    print("-" * 60 + "\n")
    
    return alerts

def main():
    """Main hook execution."""
    
    import sys
    
    if len(sys.argv) < 2:
        # List open alerts
        list_open_alerts()
        return
    
    command = sys.argv[1]
    
    if command == "bug":
        bug_id = sys.argv[2]
        component = sys.argv[3] if len(sys.argv) > 3 else "Unknown"
        escalate_critical_bug(bug_id, component)
    
    elif command == "task":
        task_id = sys.argv[2]
        reason = sys.argv[3] if len(sys.argv) > 3 else "Unknown"
        duration = int(sys.argv[4]) if len(sys.argv) > 4 else 0
        escalate_blocked_task(task_id, reason, duration)
    
    elif command == "agent":
        agent_id = sys.argv[2]
        reason = sys.argv[3] if len(sys.argv) > 3 else "Unknown"
        escalate_agent_failure(agent_id, reason)
    
    elif command == "api":
        endpoint = sys.argv[2]
        count = int(sys.argv[3]) if len(sys.argv) > 3 else 0
        escalate_api_outage(endpoint, count)
    
    elif command == "margin":
        margin = float(sys.argv[2])
        escalate_margin_warning(margin)
    
    elif command == "list":
        list_open_alerts()
    
    else:
        print(f"[ESCALATION] Unknown command: {command}")

if __name__ == "__main__":
    main()
