#!/usr/bin/env python3
"""
Spawn QA-Master automat când se detectează modificări
Called by Vigilant file watcher
"""

import sys
import json
import subprocess
from datetime import datetime

def spawn_qa_master(change_type, changed_files):
    """Spawn QA-Master pentru testare automată"""
    
    # Generează task description bazat pe tipul de modificare
    task_descriptions = {
        'frontend_js': "Testare automată - Modificări JavaScript frontend detectate",
        'frontend_ui': "Testare automată - Modificări UI/HTML detectate",
        'backend_api': "Testare automată - Modificări Backend API detectate",
        'robot_logic': "Testare automată - Modificări Robot Trading detectate",
        'frontend_css': "Testare automată - Modificări CSS detectate",
        'general': "Testare automată - Modificări cod detectate"
    }
    
    task_desc = task_descriptions.get(change_type, task_descriptions['general'])
    
    task = f"""AUTO-TESTING TASK: {task_desc}

TIP MODIFICARE: {change_type}
FIȘIERE MODIFICATE: {json.dumps(changed_files, indent=2)}

CONTEX:
File Watcher (Vigilant) a detectat modificări în cod. 
Trebuie să testezi automat funcționalitățile afectate.

CE SĂ TESTEZI:
1. Smoke Test rapid (2 minute) - sistemul pornește?
2. Funcționalități afectate de modificări
3. Regresie - nu s-au stricat funcționalități vechi
4. API endpoints (dacă e cazul)
5. UI elements (dacă e cazul)

BUG-URI:
Dacă găsești bug-uri, creează rapoarte în /workspace/shared/bugs/
Bug Router le va atribui automat agenților de fixare.

RAPORT:
La final, raportează:
- Ce ai testat
- Bug-uri găsite (dacă există)
- Status final: PASS sau NEEDS_FIX

SCRIE STATUS în /workspace/shared/agents/qa-master/status.json
"""
    
    # Folosește OpenClaw CLI sau API pentru a spawna agent
    # Aici simulăm prin crearea unui task file
    task_file = f'/workspace/shared/tasks/auto/TEST-{int(datetime.now().timestamp())}.json'
    
    task_data = {
        'id': f"AUTO-TEST-{int(datetime.now().timestamp())}",
        'type': 'auto_testing',
        'title': task_desc,
        'change_type': change_type,
        'changed_files': changed_files,
        'assigned_to': 'qa-master',
        'status': 'pending_spawn',
        'created_at': datetime.now().isoformat()
    }
    
    with open(task_file, 'w') as f:
        json.dump(task_data, f, indent=2)
    
    print(f"✅ Task creat: {task_file}")
    print(f"📝 Tip: {change_type}")
    print(f"📁 Fișiere: {len(changed_files)}")
    
    # Aici am putea spawna automat QA-Master folosind sessions_spawn
    # Dar pentru moment creăm doar task file
    
    return task_file

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: spawn_qa_master.py <change_type> <changed_files_json>")
        sys.exit(1)
    
    change_type = sys.argv[1]
    changed_files = json.loads(sys.argv[2])
    
    spawn_qa_master(change_type, changed_files)
