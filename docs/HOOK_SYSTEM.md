# 🪝 HOOK SYSTEM - Documentație Completă

## Overview
Sistemul de hooks permite automatizarea răspunsului la evenimente în sistemul multi-agent. Fiecare hook este un script Python executabil care realizează o acțiune specifică.

---

## 📁 Locație
```
/workspace/shared/hooks/
├── bug_auto_detect.py      # Detectare și asignare automată bug-uri
├── task_coordination.py    # Coordonare task-uri și asignare
├── agent_recovery.py       # Recuperare agenți blocați
├── escalation.py           # Escalare probleme critice
├── file_lock.py           # Lock-uri pe fișiere partajate
└── notification.py        # Notificări între agenți
```

**Hook Manager:** `/workspace/shared/hook_manager.py`

---

## 🎯 Hook-uri Disponibile

### 1. Bug Auto-Detect (`bug_auto_detect.py`)

**Trigger:** API errors, test failures, agent failures

**Acțiuni:**
- Creează bug report automat
- Asignează la agent corespunzător
- Notifică orchestrator

**Utilizare:**
```bash
# Hook manager
python3 /workspace/shared/hook_manager.py bug.detect '{"error_type": "API_ERROR", "component": "Dashboard", "description": "API 500", "priority": "CRITICAL"}'

# Direct
python3 /workspace/shared/hooks/bug_auto_detect.py
```

**Auto-Assignment Rules:**
- API bugs → builder-1
- Dashboard bugs → builder-4
- MT5 bugs → builder-6
- Database bugs → ops-2
- CRITICAL → builder-1 (lead)

---

### 2. Task Coordination (`task_coordination.py`)

**Trigger:** Schimbare stare task, task nou, task completat

**Acțiuni:**
- Update task board
- Mută task între liste (inbox → active → completed)
- Verifică dependențe
- Auto-assign task-uri disponibile

**Utilizare:**
```bash
# Update task status
python3 /workspace/shared/hook_manager.py task.update TASK-001 "Done" builder-1

# Assign next available task to agent
python3 /workspace/shared/hook_manager.py task.assign builder-1

# Check dependencies
python3 /workspace/shared/hook_manager.py task.check-deps TASK-001
```

---

### 3. Agent Recovery (`agent_recovery.py`)

**Trigger:** Agent heartbeat stalled > 5 minute

**Acțiuni:**
- Verifică sănătate agent
- Încearcă recuperare
- Reasignează task-uri dacă eșuează
- Notifică orchestrator

**Utilizare:**
```bash
# Check specific agent
python3 /workspace/shared/hook_manager.py agent.recover builder-1

# Check all agents
python3 /workspace/shared/hook_manager.py agent.recover
```

**Recovery Strategy:**
1. Dacă are task activ → Retry (max 3)
2. Dacă max retries reached → Reassign
3. Dacă nu are task → Reset to available

---

### 4. Escalation (`escalation.py`)

**Trigger:** Probleme critice care necesită atenție umană

**Acțiuni:**
- Creează alertă de escalare
- Log în sistem central
- Notifică orchestrator

**Utilizare:**
```bash
# Escalate critical bug
python3 /workspace/shared/hook_manager.py escalate.bug BUG-20260328071234 Dashboard

# Escalate blocked task
python3 /workspace/shared/hook_manager.py escalate.task TASK-001 "Waiting for API" 2

# Escalate agent failure
python3 /workspace/shared/hook_manager.py escalate.agent builder-1 "Stalled 10 minutes"

# Escalate API outage
python3 /workspace/shared/hook_manager.py escalate.api /api/v32/or_data 10

# Escalate margin warning
python3 /workspace/shared/hook_manager.py escalate.margin 120

# List open alerts
python3 /workspace/shared/hook_manager.py escalate.list
```

---

### 5. File Lock (`file_lock.py`)

**Trigger:** Agent vrea să modifice fișier partajat

**Acțiuni:**
- Creează lock file
- Previne modificări concurente
- Auto-expiră după timeout (default 30 min)

**Utilizare:**
```bash
# Acquire lock
python3 /workspace/shared/hook_manager.py lock.acquire /path/to/file.txt builder-1 30

# Release lock
python3 /workspace/shared/hook_manager.py lock.release /path/to/file.txt builder-1

# Check if locked
python3 /workspace/shared/hook_manager.py lock.check /path/to/file.txt

# List all locks
python3 /workspace/shared/hook_manager.py lock.list
```

**Best Practices:**
- Acquire lock înainte de orice modificare
- Release lock imediat după terminare
- Verifică lock existent înainte de acquire

---

### 6. Notification (`notification.py`)

**Trigger:** Evenimente care necesită atenție

**Acțiuni:**
- Trimite notificare către agent/orchestrator
- Persistă în log
- Suportă priorități (low, normal, high, urgent)

**Utilizare:**
```bash
# Send custom notification
python3 /workspace/shared/hook_manager.py notify.send builder-1 "Your task is ready" normal

# Task assigned notification
python3 /workspace/shared/hook_manager.py notify.task builder-1 TASK-001 "Fix Dashboard"

# Bug assigned notification
python3 /workspace/shared/hook_manager.py notify.bug BUG-001 builder-1 HIGH

# List unread notifications
python3 /workspace/shared/hook_manager.py notify.list builder-1

# Mark as read
python3 /workspace/shared/hook_manager.py notify.read builder-1
```

---

## 🔄 Hook Triggers (Când se activează)

| Eveniment | Hook Triggered | Automat |
|-----------|----------------|---------|
| API returnează 500 | `bug.detect` | ✅ Cron |
| Task marcat "Done" | `task.update` | ✅ Task coord |
| Task inbox disponibil | `task.assign` | ✅ Cron |
| Agent stalled > 5min | `agent.recover` | ✅ Cron |
| Bug CRITICAL nefixat | `escalate.bug` | ✅ Cron |
| Agent modifica fișier | `lock.acquire/release` | ❌ Manual |
| Task assigned | `notify.task` | ✅ Auto |
| Bug assigned | `notify.bug` | ✅ Auto |
| Margin < 150% | `escalate.margin` | ✅ Cron |
| API down > 3 min | `escalate.api` | ✅ Cron |

---

## 🛠️ Integrare în Cron Jobs

### agent_heartbeat.py apelează:
```python
# Check all agents
subprocess.run(["python3", "/workspace/shared/hook_manager.py", "agent.recover"])
```

### bug_triage.py apelează:
```python
# Auto-assign new bugs
subprocess.run(["python3", "/workspace/shared/hook_manager.py", "bug.detect", data])
```

### dashboard_health.py apelează:
```python
# Escalate API outages
subprocess.run(["python3", "/workspace/shared/hook_manager.py", "escalate.api", endpoint, str(error_count)])
```

---

## 📝 Exemple de Utilizare

### Exemplu 1: Agent vrea să modifice cod
```bash
# 1. Acquire lock
python3 /workspace/shared/hook_manager.py lock.acquire /root/clawd/agents/brainmaker/mt5_core_server.py builder-1

# 2. Modifică fișierul...

# 3. Release lock
python3 /workspace/shared/hook_manager.py lock.release /root/clawd/agents/brainmaker/mt5_core_server.py builder-1

# 4. Testează
python3 /workspace/shared/hook_manager.py task.update TASK-001 "In Review" builder-1
```

### Exemplu 2: API returnează eroare
```bash
# Automat de către cron:
python3 /workspace/shared/hook_manager.py bug.detect '{"error_type": "API_ERROR", "component": "Dashboard", "description": "/api/v32/or_data returned 500", "priority": "HIGH"}'

# Rezultat: Bug creat + asignat automat + notificare trimisă
```

### Exemplu 3: Task blocked
```bash
# După 2 ore în "Blocked":
python3 /workspace/shared/hook_manager.py escalate.task TASK-001 "Waiting for external API" 2

# Rezultat: Alertă creată, orchestrator notificat
```

---

## 🔧 Debug și Troubleshooting

### Vezi toate hook-urile disponibile:
```bash
python3 /workspace/shared/hook_manager.py
```

### Testează un hook:
```bash
# Test bug detection
python3 /workspace/shared/hooks/bug_auto_detect.py

# Test file lock
python3 /workspace/shared/hooks/file_lock.py list
```

### Vezi log-uri:
```bash
# Alerts
tail -f /workspace/shared/logs/alerts.log

# Notifications
tail -f /workspace/shared/logs/notifications.log

# Active locks
python3 /workspace/shared/hook_manager.py lock.list
```

---

## 🎯 Best Practices

1. **Folosește Hook Manager** - Nu apele hook-urile direct (folosește `hook_manager.py`)
2. **Lock întotdeauna** - Acquire lock înainte de orice modificare
3. **Release lock** - Nu uita să eliberezi lock-ul
4. **Verifică return code** - Hook-urile returnează 0 pentru succes, 1 pentru eșec
5. **Timeout** - Hook-urile au timeout 30 secunde

---

**Versiune:** 1.0  
**Ultima actualizare:** 2026-03-28  
**Total Hooks:** 6 script-uri, 20+ comenzi
