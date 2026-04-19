#!/usr/bin/env python3
"""
BUG ROUTER - Sistem automat de atribuire bug-uri la agenți
Rulează ca hook sau cron job
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path

# Configurare - Cine fixează ce
AGENT_ASSIGNMENTS = {
    'backend': {
        'patterns': ['api', 'endpoint', 'server', 'cors', '404', '500', 'database', 'sql', 'postgresql'],
        'agent': 'builder-1',
        'skills': 'Python, Flask, API',
        'work_dir': '/root/clawd/agents/brainmaker',
        'main_files': ['mt5_core_server.py'],
        'test_files': ['tests/api/test_api_endpoints.py', 'tests/integration/test_server.py']
    },
    'robots': {
        'patterns': ['robot', 'v31', 'v32', 'v33', 'trading', 'strategy', 'tpl', 'breakout'],
        'agent': 'builder-1',
        'skills': 'Python, Trading Logic',
        'work_dir': '/root/clawd/agents/brainmaker',
        'main_files': ['v31_marius_tpl_robot.py', 'v32_london_breakout_robot.py', 'v33_ny_breakout_robot.py'],
        'test_files': ['tests/unit/test_v31.py', 'tests/unit/test_v32.py', 'tests/unit/test_v33.py']
    },
    'frontend-js': {
        'patterns': ['javascript', 'js', 'innerhtml', 'xss', 'function', 'event', 'async'],
        'agent': 'dashboard-frontend',
        'skills': 'JavaScript, DOM',
        'work_dir': '/root/clawd/agents/brainmaker/dashboard',
        'main_files': ['dashboard_functional.js', 'auth.js'],
        'test_files': ['tests/unit/test_dashboard.js', 'tests/e2e/test_dashboard_flow.js']
    },
    'frontend-ui': {
        'patterns': ['css', 'html', 'layout', 'responsive', 'design', 'style'],
        'agent': 'builder-3',
        'skills': 'HTML, CSS',
        'work_dir': '/root/clawd/agents/brainmaker/dashboard',
        'main_files': ['index.html', 'login.html'],
        'test_files': []
    },
    'security': {
        'patterns': ['xss', 'security', 'vulnerability', 'injection', 'auth', 'authentication'],
        'agent': 'security-auditor',
        'skills': 'Security, Auth',
        'work_dir': '/root/clawd/agents/brainmaker',
        'main_files': ['mt5_core_server.py', 'dashboard/auth.js'],
        'test_files': ['tests/security/test_xss.py', 'tests/security/test_auth.py']
    },
    'integration': {
        'patterns': ['integration', 'mismatch', 'api-ui', 'sync'],
        'agent': 'integration-engineer',
        'skills': 'Full-stack',
        'work_dir': '/root/clawd/agents/brainmaker',
        'main_files': ['mt5_core_server.py', 'dashboard/dashboard_functional.js'],
        'test_files': ['tests/integration/test_api_ui.py', 'tests/e2e/test_full_flow.py']
    },
    'testing': {
        'patterns': ['test', 'testing', 'unittest', 'pytest', 'assert', 'mock'],
        'agent': 'qa-tester',
        'skills': 'Testing, QA',
        'work_dir': '/root/clawd/agents/brainmaker/tests',
        'main_files': [],
        'test_files': []
    }
}

BUGS_DIR = '/workspace/shared/bugs'
TASKS_DIR = '/workspace/shared/tasks/auto'
AGENTS_DIR = '/workspace/shared/agents'

def parse_bug_file(bug_path):
    """Extrage informații din fișierul bug"""
    with open(bug_path, 'r') as f:
        content = f.read()
    
    bug_info = {
        'id': '',
        'title': '',
        'severity': '',
        'priority': '',
        'component': '',
        'file': '',
        'description': ''
    }
    
    # Extrage ID din nume fișier
    bug_info['id'] = Path(bug_path).stem
    
    # Extrage titlu
    title_match = re.search(r'^# (?:BUG-\d+: )?(.+)$', content, re.MULTILINE)
    if title_match:
        bug_info['title'] = title_match.group(1)
    
    # Extrage severitate
    severity_match = re.search(r'\*\*Severitate:\*\*\s*(\w+)', content)
    if severity_match:
        bug_info['severity'] = severity_match.group(1)
    
    # Extrage prioritate
    priority_match = re.search(r'\*\*Prioritate:\*\*\s*(\w+)', content)
    if priority_match:
        bug_info['priority'] = priority_match.group(1)
    
    # Extrage fișier afectat
    file_match = re.search(r'\*\*File:\*\*\s*(.+?)(?:\n|$)', content)
    if file_match:
        bug_info['file'] = file_match.group(1).strip()
    
    # Extrage descriere
    desc_match = re.search(r'## Descriere\s+(.+?)(?=##|$)', content, re.DOTALL)
    if desc_match:
        bug_info['description'] = desc_match.group(1).strip()
    
    return bug_info

def determine_agent(bug_info):
    """Determină care agent e responsabil pentru bug"""
    content = f"{bug_info['title']} {bug_info['description']} {bug_info['file']}".lower()
    
    scores = {}
    for category, config in AGENT_ASSIGNMENTS.items():
        score = 0
        for pattern in config['patterns']:
            if pattern in content:
                score += 1
        scores[category] = score
    
    # Alege categoria cu scorul cel mai mare
    best_category = max(scores, key=scores.get)
    
    if scores[best_category] == 0:
        # Default la builder-1 dacă nu se potrivește nimic
        return 'builder-1', 'Backend (default)'
    
    return AGENT_ASSIGNMENTS[best_category]['agent'], best_category

def generate_task_file(bug_info, assigned_agent, agent_category):
    """Generează task pentru agent"""
    task_id = f"BUGFIX-{bug_info['id']}"
    
    # Determină deadline bazat pe severitate
    severity_days = {
        'Critical': 1,
        'High': 2,
        'Medium': 5,
        'Low': 14
    }
    days = severity_days.get(bug_info['severity'], 3)
    
    # Obține work_dir din configurația categoriei
    work_dir = AGENT_ASSIGNMENTS.get(agent_category, {}).get('work_dir', '/root/clawd/agents/brainmaker')
    main_files = AGENT_ASSIGNMENTS.get(agent_category, {}).get('main_files', [])
    test_files = AGENT_ASSIGNMENTS.get(agent_category, {}).get('test_files', [])
    
    task = {
        'id': task_id,
        'type': 'auto_bugfix',
        'title': f"Fix {bug_info['title']}",
        'description': f"Bug {bug_info['id']} assigned automatically",
        'bug_id': bug_info['id'],
        'bug_file': f"/workspace/shared/bugs/{bug_info['id']}.md",
        'assigned_to': assigned_agent,
        'severity': bug_info['severity'],
        'priority': bug_info['priority'],
        'status': 'assigned',
        'created_at': datetime.now().isoformat(),
        'deadline_days': days,
        'auto_generated': True,
        'work_dir': work_dir,
        'target_files': main_files,
        'test_files': test_files,
        'test_dir': '/root/clawd/agents/brainmaker/tests',
        'instructions': f"""Lucrează DIRECT în {work_dir}. NU copia fișierele în /workspace/shared/agents/

PAȘI:
1. Editează fișierele target din {work_dir}
2. Dacă testele există, rulează-le: python3 -m pytest {test_files[0] if test_files else 'tests/'}
3. Dacă nu există teste pentru bug-ul fixat, creează test în /root/clawd/agents/brainmaker/tests/
4. Verifică că fix-ul funcționează
5. Marchează task-ul ca done

IMPORTANT: Toate testele trebuie să fie în /root/clawd/agents/brainmaker/tests/"""
    }
    
    # Salvează task
    os.makedirs(TASKS_DIR, exist_ok=True)
    task_path = os.path.join(TASKS_DIR, f"{task_id}.json")
    
    with open(task_path, 'w') as f:
        json.dump(task, f, indent=2)
    
    return task_path

def update_agent_status(agent, bug_info, task_path):
    """Updatează status-ul agentului cu noul task"""
    status_file = os.path.join(AGENTS_DIR, agent, 'status.json')
    
    # Citește status existent sau creează nou
    if os.path.exists(status_file):
        with open(status_file, 'r') as f:
            try:
                status = json.load(f)
            except:
                status = {}
    else:
        status = {}
    
    # Adaugă task nou
    if 'pending_tasks' not in status:
        status['pending_tasks'] = []
    
    status['pending_tasks'].append({
        'bug_id': bug_info['id'],
        'task_file': task_path,
        'assigned_at': datetime.now().isoformat(),
        'severity': bug_info['severity']
    })
    
    status['last_update'] = datetime.now().isoformat()
    status['status'] = 'has_tasks' if status.get('status') != 'working' else 'working'
    
    with open(status_file, 'w') as f:
        json.dump(status, f, indent=2)

def create_notification(bug_info, assigned_agent):
    """Creează notificare pentru Manifest"""
    notification = {
        'timestamp': datetime.now().isoformat(),
        'type': 'bug_assigned',
        'bug_id': bug_info['id'],
        'severity': bug_info['severity'],
        'assigned_to': assigned_agent,
        'title': bug_info['title'],
        'message': f"Bug {bug_info['id']} ({bug_info['severity']}) assigned to {assigned_agent}"
    }
    
    notification_dir = '/workspace/shared/notifications'
    os.makedirs(notification_dir, exist_ok=True)
    
    notif_file = os.path.join(notification_dir, f"bug-{bug_info['id']}-{int(datetime.now().timestamp())}.json")
    with open(notif_file, 'w') as f:
        json.dump(notification, f, indent=2)


def trigger_agent_if_idle(agent_name, task_path):
    """⭐ AUTO-TRIGGER: Pornește agentul automat dacă e idle"""
    import subprocess
    
    try:
        status_file = os.path.join(AGENTS_DIR, agent_name, 'status.json')
        if not os.path.exists(status_file):
            return False
        
        with open(status_file) as f:
            status = json.load(f)
        
        # Dacă agentul e idle, pornește-l automat
        if status.get('status') in ['idle', 'completed', 'available']:
            print(f"   🚀 Auto-triggering {agent_name}")
            
            # Setează status working
            status['status'] = 'working'
            status['task'] = task_path
            status['started_at'] = datetime.now().isoformat()
            with open(status_file, 'w') as f:
                json.dump(status, f, indent=2)
            
            # Pornește agentul (simulare - în practică ar porni scriptul real)
            subprocess.Popen(
                ['python3', '/workspace/shared/agent_completed.py', agent_name, 
                 json.load(open(task_path))['id'], 'completed'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return True
    except Exception as e:
        print(f"   ⚠️ Auto-trigger failed: {e}")
    return False

def route_bug(bug_path):
    """Procesează un bug și îl atribuie unui agent"""
    print(f"🔍 Routing bug: {bug_path}")
    
    # Parsează bug
    bug_info = parse_bug_file(bug_path)
    print(f"   ID: {bug_info['id']}")
    print(f"   Title: {bug_info['title']}")
    print(f"   Severity: {bug_info['severity']}")
    
    # Determină agent
    assigned_agent, category = determine_agent(bug_info)
    print(f"   Category: {category}")
    print(f"   Assigned to: {assigned_agent}")
    print(f"   Work dir: {AGENT_ASSIGNMENTS.get(category, {}).get('work_dir', 'N/A')}")
    
    # Generează task
    task_path = generate_task_file(bug_info, assigned_agent, category)
    print(f"   Task created: {task_path}")
    
    # Updatează status agent
    update_agent_status(assigned_agent, bug_info, task_path)
    print(f"   Agent status updated")
    
    # Creează notificare
    create_notification(bug_info, assigned_agent)
    print(f"   Notification created")
    
    print(f"✅ Bug {bug_info['id']} routed successfully to {assigned_agent}")
    return assigned_agent

def scan_and_route():
    """Scanează folderul bugs și rutează bug-urile noi"""
    print("🚀 Bug Router - Scanning for new bugs...")
    
    if not os.path.exists(BUGS_DIR):
        print(f"   Bugs directory not found: {BUGS_DIR}")
        return
    
    routed_count = 0
    
    for bug_file in os.listdir(BUGS_DIR):
        if not bug_file.endswith('.md'):
            continue
        
        bug_path = os.path.join(BUGS_DIR, bug_file)
        bug_id = Path(bug_file).stem
        
        # Verifică dacă bug-ul a fost deja rutat
        task_path = os.path.join(TASKS_DIR, f"BUGFIX-{bug_id}.json")
        if os.path.exists(task_path):
            continue  # Already routed
        
        try:
            route_bug(bug_path)
            routed_count += 1
        except Exception as e:
            print(f"   ❌ Error routing {bug_file}: {e}")
    
    print(f"\n📊 Summary: {routed_count} bugs routed")

if __name__ == '__main__':
    scan_and_route()
