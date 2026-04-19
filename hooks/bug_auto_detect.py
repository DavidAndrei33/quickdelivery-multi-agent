#!/usr/bin/env python3
"""
Bug Auto-Detection Hook
Triggered when: API errors, test failures, agent failures
Actions: Creates bug report, assigns to agent, notifies orchestrator
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

BUG_TRACK_DIR = "/workspace/shared/bugs"
TASKBOARD_PATH = "/workspace/shared/tasks/TASKBOARD.json"
CONFIG_PATH = "/workspace/shared/config/team_orchestration.json"

# Path-uri corecte pentru codul sursă
BACKEND_ROOT = "/root/clawd/agents/brainmaker"
DASHBOARD_ROOT = "/root/clawd/agents/brainmaker/dashboard"
LOGS_DIR = "/var/log"

def create_bug_report(error_type, component, description, evidence=None, priority="HIGH"):
    """Create a new bug report from template."""
    
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    bug_id = f"BUG-{timestamp}"
    
    bug_content = f"""# {bug_id}

**Status:** REPORTED
**Priority:** {priority}
**Component:** {component}
**Error Type:** {error_type}
**Discovered At:** {datetime.utcnow().isoformat()}Z
**Auto-Generated:** Yes

## Description
{description}

## Evidence
```
{evidence or "No additional evidence"}
```

## Assigned To
To be assigned by orchestrator

## Fix Status
- [ ] Bug assigned
- [ ] Fix implemented
- [ ] Fix tested
- [ ] Fix verified
- [ ] Bug closed

## Related
- [Link to failing task]
- [Link to related component]
"""
    
    bug_path = Path(BUG_TRACK_DIR) / f"{bug_id}.md"
    bug_path.write_text(bug_content)
    
    print(f"[BUG-HOOK] Created bug report: {bug_id}")
    return bug_id

def auto_assign_bug(bug_id, component, priority):
    """Auto-assign bug based on component and priority."""
    
    with open(CONFIG_PATH) as f:
        config = json.load(f)
    
    # Assignment rules
    assignment_rules = {
        "API": "builder-1",
        "Dashboard": "builder-4",
        "MT5 Core": "builder-6",
        "Database": "ops-2",
        "Security": "reviewer-2"
    }
    
    # CRITICAL bugs go to lead
    if priority == "CRITICAL":
        assigned_to = "builder-1"  # Core-Developer-Lead
    else:
        assigned_to = assignment_rules.get(component, "builder-1")
    
    # Update bug report
    bug_path = Path(BUG_TRACK_DIR) / f"{bug_id}.md"
    content = bug_path.read_text()
    content = content.replace(
        "To be assigned by orchestrator",
        f"{assigned_to} (auto-assigned)"
    )
    content = content.replace(
        "**Status:** REPORTED",
        "**Status:** ASSIGNED"
    )
    bug_path.write_text(content)
    
    # Update taskboard
    with open(TASKBOARD_PATH) as f:
        taskboard = json.load(f)
    
    taskboard["bugs"]["open"].append({
        "id": bug_id,
        "title": f"Auto-detected: {error_type}",
        "priority": priority,
        "component": component,
        "assigned_to": assigned_to,
        "status": "Assigned",
        "discovered_at": datetime.utcnow().isoformat()
    })
    
    with open(TASKBOARD_PATH, 'w') as f:
        json.dump(taskboard, f, indent=2)
    
    print(f"[BUG-HOOK] Auto-assigned {bug_id} to {assigned_to}")
    
    # Send notification (via sessions_send would happen here)
    print(f"[BUG-HOOK] NOTIFICATION: Bug {bug_id} assigned to {assigned_to}")
    
    return assigned_to

def main():
    """Main hook execution."""
    
    # Read trigger data from stdin or args
    if len(sys.argv) > 1:
        trigger_data = json.loads(sys.argv[1])
    else:
        # Default test data
        trigger_data = {
            "error_type": "API_ERROR",
            "component": "Dashboard",
            "description": "API endpoint returned 500",
            "evidence": "Endpoint: /api/v32/or_data\\nError: Connection timeout",
            "priority": "CRITICAL"
        }
    
    print(f"[BUG-HOOK] Triggered: {trigger_data['error_type']}")
    
    # Create bug report
    bug_id = create_bug_report(
        error_type=trigger_data['error_type'],
        component=trigger_data['component'],
        description=trigger_data['description'],
        evidence=trigger_data.get('evidence'),
        priority=trigger_data.get('priority', 'HIGH')
    )
    
    # Auto-assign
    assigned_to = auto_assign_bug(
        bug_id=bug_id,
        component=trigger_data['component'],
        priority=trigger_data.get('priority', 'HIGH')
    )
    
    print(f"[BUG-HOOK] Complete: {bug_id} → {assigned_to}")

if __name__ == "__main__":
    main()
