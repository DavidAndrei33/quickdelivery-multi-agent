#!/usr/bin/env python3
"""
Creează task-uri BUGFIX pentru bug-urile noi identificate în teste
"""

import json
import os
from datetime import datetime

BUGS_DIR = "/workspace/shared/bugs"
TASKS_DIR = "/workspace/shared/tasks/auto"

# Bug-uri noi identificate în teste
new_bugs = [
    {
        "id": "BUG-102",
        "title": "V32 Robot API endpoint missing",
        "severity": "MEDIUM",
        "component": "API",
        "test": "3.8.2",
        "description": "Endpoint /api/v32/status nu există. Robotul V32 nu poate fi monitorizat din dashboard.",
        "assigned_to": "builder-1",
        "work_dir": "/root/clawd/agents/brainmaker",
        "target_files": ["mt5_core_server.py"],
        "test_files": ["tests/api/test_v32_status.py"]
    },
    {
        "id": "BUG-103",
        "title": "V33 Robot API endpoint missing",
        "severity": "MEDIUM",
        "component": "API",
        "test": "3.8.3",
        "description": "Endpoint /api/v33/status nu există. Robotul V33 nu poate fi monitorizat din dashboard.",
        "assigned_to": "builder-1",
        "work_dir": "/root/clawd/agents/brainmaker",
        "target_files": ["mt5_core_server.py"],
        "test_files": ["tests/api/test_v33_status.py"]
    },
    {
        "id": "BUG-104",
        "title": "Robot switch endpoint not implemented",
        "severity": "MEDIUM",
        "component": "API",
        "test": "3.8.4",
        "description": "Endpoint /api/robot/switch (POST) nu este implementat. Switch între roboți nu funcționează.",
        "assigned_to": "builder-1",
        "work_dir": "/root/clawd/agents/brainmaker",
        "target_files": ["mt5_core_server.py"],
        "test_files": ["tests/api/test_robot_switch.py"]
    },
    {
        "id": "BUG-105",
        "title": "Strategy text update endpoint missing",
        "severity": "MEDIUM",
        "component": "API",
        "test": "3.8.5",
        "description": "Endpoint pentru update strategie robot nu există. Textul strategiei nu se actualizează.",
        "assigned_to": "builder-1",
        "work_dir": "/root/clawd/agents/brainmaker",
        "target_files": ["mt5_core_server.py"],
        "test_files": ["tests/api/test_strategy_update.py"]
    },
    {
        "id": "BUG-108",
        "title": "London session timer API missing",
        "severity": "MEDIUM",
        "component": "API",
        "test": "3.10.1",
        "description": "Endpoint /api/v32/session_time nu există. Timerul sesiunii London nu funcționează.",
        "assigned_to": "builder-1",
        "work_dir": "/root/clawd/agents/brainmaker",
        "target_files": ["mt5_core_server.py"],
        "test_files": ["tests/api/test_v32_timer.py"]
    },
    {
        "id": "BUG-109",
        "title": "NY session timer API missing",
        "severity": "MEDIUM",
        "component": "API",
        "test": "3.10.2",
        "description": "Endpoint /api/v33/session_time nu există. Timerul sesiunii NY nu funcționează.",
        "assigned_to": "builder-1",
        "work_dir": "/root/clawd/agents/brainmaker",
        "target_files": ["mt5_core_server.py"],
        "test_files": ["tests/api/test_v33_timer.py"]
    }
]

def create_bug_file(bug):
    """Creează fișier bug markdown"""
    os.makedirs(BUGS_DIR, exist_ok=True)
    
    bug_path = os.path.join(BUGS_DIR, f"{bug['id']}.md")
    
    content = f"""# {bug['id']}: {bug['title']}

**Status:** OPEN  
**Severitate:** {bug['severity']}  
**Component:** {bug['component']}  
**Test Case:** {bug['test']}  
**Descoperit:** {datetime.now().isoformat()}  
**Asignat:** {bug['assigned_to']}

## Descriere
{bug['description']}

## Pași Reproducere
1. Deschide dashboard
2. Navighează la secțiunea roboți
3. Încearcă să accesezi {bug['id'].replace('BUG-', '/api/').lower().replace('-', '_')}
4. Observă 404 Not Found

## Comportament Așteptat
Endpoint-ul ar trebui să returneze statusul robotului/timerul sesiunii.

## Comportament Actual
Endpoint-ul nu există (404).

## Fișiere de Lucru
- **Work Dir:** `{bug['work_dir']}`
- **Target:** `{', '.join(bug['target_files'])}`

## Checklist
- [ ] Endpoint creat
- [ ] Teste scrise
- [ ] Teste trecute
- [ ] Bug închis
"""
    
    with open(bug_path, 'w') as f:
        f.write(content)
    
    print(f"✅ Bug creat: {bug_path}")
    return bug_path

def create_task_file(bug):
    """Creează fișier task JSON"""
    os.makedirs(TASKS_DIR, exist_ok=True)
    
    task_id = f"BUGFIX-{bug['id']}"
    task_path = os.path.join(TASKS_DIR, f"{task_id}.json")
    
    task = {
        "id": task_id,
        "type": "auto_bugfix",
        "bug_id": bug['id'],
        "title": f"Fix {bug['title']}",
        "description": bug['description'],
        "severity": bug['severity'],
        "component": bug['component'],
        "assigned_to": bug['assigned_to'],
        "work_dir": bug['work_dir'],
        "target_files": bug['target_files'],
        "test_files": bug['test_files'],
        "status": "assigned",
        "created_at": datetime.now().isoformat(),
        "deadline_days": 2,
        "auto_generated": True,
        "priority": "P1",
        "instructions": f"""Lucrează DIRECT în {bug['work_dir']}.

BUG: {bug['title']}
DESCRIERE: {bug['description']}

PAȘI:
1. Implementează endpoint-ul lipsă în {bug['target_files'][0]}
2. Scrie teste în {bug['test_files'][0]}
3. Rulează testele: python3 -m pytest {bug['test_files'][0]} -v
4. Verifică funcționalitatea: curl http://localhost:8001{bug['id'].replace('BUG-', '/api/').lower().replace('_', '/').replace('-', '/')}
5. Marchează task ca done

NU lucra în /workspace/shared/agents/!"""
    }
    
    with open(task_path, 'w') as f:
        json.dump(task, f, indent=2)
    
    print(f"✅ Task creat: {task_path}")
    return task_path

def update_agent_status(agent, bug, task_path):
    """Updatează status.json al agentului"""
    agent_dir = f"/workspace/shared/agents/{agent}"
    status_path = os.path.join(agent_dir, "status.json")
    
    if os.path.exists(status_path):
        with open(status_path, 'r') as f:
            status = json.load(f)
    else:
        status = {
            "agent": agent,
            "status": "idle",
            "pending_tasks": [],
            "completed_tasks": []
        }
    
    # Adaugă task nou
    if "pending_tasks" not in status:
        status["pending_tasks"] = []
    
    status["pending_tasks"].append({
        "bug_id": bug['id'],
        "task_file": task_path,
        "assigned_at": datetime.now().isoformat(),
        "severity": bug['severity'],
        "priority": "P1"
    })
    
    status["status"] = "has_tasks"
    status["last_update"] = datetime.now().isoformat()
    
    with open(status_path, 'w') as f:
        json.dump(status, f, indent=2)
    
    print(f"✅ Status {agent} actualizat")

def main():
    print("🚀 Creare task-uri BUGFIX pentru bug-uri noi...")
    print()
    
    for bug in new_bugs:
        print(f"\n🔧 Procesare {bug['id']}: {bug['title']}")
        
        # Creează fișiere
        bug_path = create_bug_file(bug)
        task_path = create_task_file(bug)
        
        # Update agent
        update_agent_status(bug['assigned_to'], bug, task_path)
    
    print()
    print("=" * 60)
    print(f"✅ {len(new_bugs)} BUG-URI NOI GATA PENTRU FIXARE!")
    print("=" * 60)
    print()
    print("Agenții pot începe lucrul imediat.")
    print("Task-uri în: /workspace/shared/tasks/auto/")

if __name__ == "__main__":
    main()
