#!/usr/bin/env python3
"""
🔄 AGENT STATUS AUTO-UPDATER
Monitorizează agenți și updatează status automat la finalizare
"""

import os
import json
import time
import psutil
from datetime import datetime, timedelta
from pathlib import Path

# Configurare
AGENTS_DIR = "/workspace/shared/agents"
TASKS_DIR = "/workspace/shared/tasks/auto"
BUGS_DIR = "/workspace/shared/bugs"
LOG_FILE = "/var/log/agent_auto_updater.log"

# Timeout-uri (minute)
TASK_TIMEOUTS = {
    "bugfix": 15,
    "implementation": 30,
    "testing": 20,
    "review": 10
}

def log(message):
    """Log cu timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}"
    print(log_msg)
    with open(LOG_FILE, "a") as f:
        f.write(log_msg + "\n")

def is_agent_running(agent_name):
    """Verifică dacă agentul rulează (proces activ)"""
    try:
        status_file = Path(f"{AGENTS_DIR}/{agent_name}/status.json")
        if not status_file.exists():
            return False
        
        with open(status_file) as f:
            status = json.load(f)
        
        # Verifică dacă e în working/active
        if status.get("status") in ["working", "in_progress", "busy"]:
            # Verifică și procesul Python
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = ' '.join(proc.info['cmdline'] or [])
                    if agent_name in cmdline and 'python' in cmdline.lower():
                        return True
                except:
                    pass
        
        return False
    except Exception as e:
        log(f"Eroare verificare agent {agent_name}: {e}")
        return False

def check_task_completion(agent_name, task_file):
    """Verifică dacă task-ul este complet (fișiere output există)"""
    try:
        agent_output = Path(f"{AGENTS_DIR}/{agent_name}/output")
        if not agent_output.exists():
            return False
        
        # Caută fișiere recente (< 30 min)
        cutoff_time = time.time() - 1800  # 30 minute
        recent_files = [
            f for f in agent_output.iterdir()
            if f.is_file() and f.stat().st_mtime > cutoff_time
        ]
        
        return len(recent_files) > 0
    except Exception as e:
        log(f"Eroare verificare completare {agent_name}: {e}")
        return False

def update_agent_status(agent_name, new_status, completed_task=None):
    """Updatează status.json al agentului"""
    try:
        status_file = Path(f"{AGENTS_DIR}/{agent_name}/status.json")
        if not status_file.exists():
            return False
        
        with open(status_file) as f:
            status = json.load(f)
        
        old_status = status.get("status")
        status["status"] = new_status
        status["last_update"] = datetime.now().isoformat()
        
        if completed_task:
            # Mută din pending în completed
            if "pending_tasks" in status:
                task = None
                for t in status["pending_tasks"]:
                    if t.get("task_file") == completed_task or t.get("bug_id") in completed_task:
                        task = t
                        break
                
                if task:
                    status["pending_tasks"].remove(task)
                    task["completed_at"] = datetime.now().isoformat()
                    task["status"] = "completed"
                    
                    if "completed_tasks" not in status:
                        status["completed_tasks"] = []
                    status["completed_tasks"].append(task)
                    
                    log(f"✅ Task {task.get('bug_id', 'unknown')} mutat în completed pentru {agent_name}")
        
        with open(status_file, "w") as f:
            json.dump(status, f, indent=2)
        
        if old_status != new_status:
            log(f"🔄 Status {agent_name}: {old_status} → {new_status}")
        
        return True
    except Exception as e:
        log(f"Eroare update status {agent_name}: {e}")
        return False

def mark_task_completed(task_file):
    """Marchează un task JSON ca completed"""
    try:
        if not os.path.exists(task_file):
            return False
        
        with open(task_file) as f:
            task = json.load(f)
        
        task["status"] = "completed"
        task["completed_at"] = datetime.now().isoformat()
        task["auto_completed"] = True
        
        with open(task_file, "w") as f:
            json.dump(task, f, indent=2)
        
        log(f"✅ Task marcat completed: {os.path.basename(task_file)}")
        return True
    except Exception as e:
        log(f"Eroare marcă task completed: {e}")
        return False

def mark_bug_fixed(bug_id):
    """Marchează un bug ca fixed în fișierul MD"""
    try:
        bug_file = Path(f"{BUGS_DIR}/{bug_id}.md")
        if not bug_file.exists():
            return False
        
        with open(bug_file) as f:
            content = f.read()
        
        # Updatează status
        content = content.replace("**Status:** OPEN", "**Status:** FIXED")
        content = content.replace("**Status:** ASSIGNED", "**Status:** FIXED")
        
        # Adaugă timestamp fix
        if "**Fixed At:**" not in content:
            content = content.replace(
                "**Status:** FIXED",
                f"**Status:** FIXED\n**Fixed At:** {datetime.now().isoformat()}"
            )
        
        # Updatează checklist
        content = content.replace("- [ ] Fix implemented", "- [x] Fix implemented")
        content = content.replace("- [ ] Fix tested", "- [x] Fix tested")
        content = content.replace("- [ ] Bug closed", "- [x] Bug closed")
        
        with open(bug_file, "w") as f:
            f.write(content)
        
        log(f"🐛 Bug marcat fixed: {bug_id}")
        return True
    except Exception as e:
        log(f"Eroare marcă bug fixed: {e}")
        return False

def auto_retry_failed_tasks():
    """Reîncearcă task-urile failed/stuck"""
    try:
        for task_file in Path(TASKS_DIR).glob("*.json"):
            try:
                with open(task_file) as f:
                    task = json.load(f)
                
                # Verifică dacă e stuck (assigned de > timeout)
                if task.get("status") == "assigned":
                    created = task.get("created_at")
                    if created:
                        created_dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
                        elapsed = (datetime.now() - created_dt).total_seconds() / 60
                        
                        task_type = task.get("type", "bugfix")
                        timeout = TASK_TIMEOUTS.get(task_type, 15)
                        
                        if elapsed > timeout:
                            # Retry count
                            retries = task.get("retry_count", 0)
                            if retries < 3:
                                task["retry_count"] = retries + 1
                                task["status"] = "retry"
                                task["last_retry"] = datetime.now().isoformat()
                                
                                with open(task_file, "w") as f:
                                    json.dump(task, f, indent=2)
                                
                                log(f"🔄 Task {task.get('id')} marked for retry #{retries + 1}")
                            else:
                                # Max retries, escalate
                                task["status"] = "failed"
                                task["escalated"] = True
                                
                                with open(task_file, "w") as f:
                                    json.dump(task, f, indent=2)
                                
                                log(f"⚠️ Task {task.get('id')} escalated after 3 retries")
            except Exception as e:
                log(f"Eroare procesare task {task_file}: {e}")
                continue
    except Exception as e:
        log(f"Eroare auto-retry: {e}")

def scan_and_update():
    """Scanare completă și update statusuri"""
    log("🔍 Scanare agenți și task-uri...")
    
    updated_count = 0
    
    # 1. Verifică fiecare agent
    for agent_dir in Path(AGENTS_DIR).iterdir():
        if not agent_dir.is_dir():
            continue
        
        agent_name = agent_dir.name
        status_file = agent_dir / "status.json"
        
        if not status_file.exists():
            continue
        
        try:
            with open(status_file) as f:
                status = json.load(f)
            
            current_status = status.get("status")
            current_task = status.get("task")
            
            # Dacă e busy/working, verifică dacă a terminat
            if current_status in ["busy", "working", "in_progress", "has_tasks"]:
                # Verifică dacă rulează procesul
                if not is_agent_running(agent_name):
                    # Procesul s-a oprit - verifică dacă a produs output
                    if check_task_completion(agent_name, current_task):
                        # Task completat cu succes
                        update_agent_status(agent_name, "completed", current_task)
                        
                        # Marchează și task-ul JSON
                        if current_task and TASKS_DIR in str(current_task):
                            mark_task_completed(current_task)
                        
                        # Dacă e bugfix, marchează și bug-ul
                        if status.get("task", "").startswith("BUGFIX-"):
                            bug_id = status.get("task", "").replace("BUGFIX-", "")
                            mark_bug_fixed(bug_id)
                        
                        updated_count += 1
                    else:
                        # Proces oprit dar fără output = posibil crash
                        update_agent_status(agent_name, "failed")
                        log(f"⚠️ Agent {agent_name} failed (no output)")
                        
        except Exception as e:
            log(f"Eroare procesare agent {agent_name}: {e}")
            continue
    
    # 2. Auto-retry task-uri stuck
    auto_retry_failed_tasks()
    
    log(f"✅ Scanare completă. {updated_count} agenți actualizați.")

def main():
    """Main loop - rulează continuu"""
    log("🚀 Agent Auto-Updater pornit...")
    
    while True:
        try:
            scan_and_update()
            # Sleep 2 minute între scanări
            time.sleep(120)
        except KeyboardInterrupt:
            log("👋 Oprit de utilizator")
            break
        except Exception as e:
            log(f"💥 Eroare în main loop: {e}")
            time.sleep(60)  # Retry după 1 min la eroare

if __name__ == "__main__":
    main()
