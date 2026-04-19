# PIPELINE AUTOMAT COMPLET - CI/CD pentru Trading System
## Documentație: Testare automată la fiecare modificare

---

## 🎯 VIZIUNEA TA (Ce vrei)

```
Tu adaugi feature/robot nou
           ↓
    [Cod gata - Commit]
           ↓
    🤖 AGENȚII DE CODE
    Lucrează automat
           ↓
    ✅ TESTARE AUTOMATĂ
    Pornește singură
           ↓
    🔍 BUG-URI GĂSITE
    Raportate automat
           ↓
    🔧 FIXARE AUTOMATĂ
    Agente atribuiți
           ↓
    🔄 RE-TESTARE
    Validare fixuri
           ↓
    📊 RAPORT FINAL
    În Telegram/email
           ↓
    🚀 DEPLOY SAU FIX
    Decizia ta
```

---

## 🔧 IMPLEMENTARE COMPLETĂ

### 1. GITHUB/GIT HOOKS (La fiecare commit)

```bash
# .git/hooks/post-commit
#!/bin/bash
echo "🔔 Cod modificat - Trigger testing pipeline"
curl -X POST http://localhost:18789/hooks/trigger-testing \
  -d '{"event": "code_changed", "files": "'$(git diff --name-only HEAD~1)'"}'
```

### 2. FILE WATCHER (Monitorizare continuă)

```python
# /workspace/shared/hooks/file_watcher.py
"""
Vigilant - supraveghează modificări fișiere
"""
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

WATCHED_PATHS = [
    '/root/clawd/agents/brainmaker/dashboard/',
    '/root/clawd/agents/brainmaker/mt5_core_server.py',
    '/root/clawd/agents/brainmaker/v*_robot.py'
]

class CodeChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        
        print(f"📝 Fișier modificat: {event.src_path}")
        
        # Determină ce tip de modificare
        if 'dashboard_functional.js' in event.src_path:
            trigger_testing('frontend_js')
        elif 'mt5_core_server.py' in event.src_path:
            trigger_testing('backend_api')
        elif '_robot.py' in event.src_path:
            trigger_testing('robot_logic')
        elif 'index.html' in event.src_path:
            trigger_testing('frontend_ui')

def trigger_testing(test_type):
    """Pornește pipeline-ul de testare"""
    # 1. Notifică sistemul
    # 2. Spawnează QA-Master
    # 3. Așteaptă rezultate
    pass

# Rulează continuu
observer = Observer()
for path in WATCHED_PATHS:
    observer.schedule(CodeChangeHandler(), path, recursive=True)
observer.start()
```

### 3. HOOK SYSTEM (Trigger la evenimente)

```yaml
# /root/.openclaw/hooks/auto-testing/HOOK.md
---
name: auto-testing-pipeline
triggers:
  - file:modified
  - agent:task_completed
  - cron:daily_6am
  
actions:
  - name: detect_change_type
    script: detect_what_changed.py
    
  - name: spawn_qa_master
    condition: change_type == 'code'
    agent: qa-master
    task: "Testare completă automată"
    
  - name: route_bugs
    condition: bugs_found > 0
    script: bug_router.py
    
  - name: spawn_fixers
    condition: bugs_routed == true
    loop: for_each_bug
    
  - name: retest
    condition: fixes_completed == true
    delay: 5_minutes
    agent: qa-master
    task: "Re-testare validare"
    
  - name: notify_user
    condition: always
    channel: telegram
    message: "Pipeline complet. Raport: {report_url}"
```

### 4. CRON JOBS (Testare periodică)

```json
{
  "jobs": [
    {
      "name": "daily-full-test",
      "schedule": "0 6 * * *",
      "action": "spawn qa-master full-testing"
    },
    {
      "name": "smoke-test-every-30min",
      "schedule": "*/30 * * * *",
      "action": "spawn qa-master smoke-test"
    },
    {
      "name": "security-scan-weekly",
      "schedule": "0 0 * * 0",
      "action": "spawn security-auditor scan"
    }
  ]
}
```

### 5. PIPELINE STATES (Stări pipeline)

```
IDLE → CODE_CHANGED → TESTING → BUGS_FOUND → FIXING → RETESTING → DONE
              ↓                    ↓              ↓            ↓
           [WATCH]            [ROUTING]      [FIXING]    [VALIDATE]
```

---

## 🔄 WORKFLOW COMPLET AUTOMAT

### Scenariu 1: Adaugi buton nou în dashboard

```
1. TU: Modifici dashboard_functional.js (adaugi buton)
          ↓
2. FILE WATCHER: Detectează modificare
          ↓
3. TRIGGER: "frontend_js modified"
          ↓
4. SPAWN: QA-Master (testare specifică frontend)
          ↓
5. QA-MASTER TESTEAZĂ:
   - Butonul apare în UI?
   - Click funcționează?
   - Event handler e corect?
   - Nu sunt erori JS?
   - Stilul e corect?
          ↓
6. BUG GĂSIT? → Bug Router atribuie → Dashboard-Frontend fixează
          ↓
7. RE-TEST: QA-Master verifică fixul
          ↓
8. NOTIFICARE: "✅ Buton nou testat și validat"
```

### Scenariu 2: Adaugi robot nou (V34)

```
1. TU: Creezi v34_tokyo_breakout_robot.py
          ↓
2. FILE WATCHER: Detectează fișier nou *_robot.py
          ↓
3. TRIGGER: "new_robot_added"
          ↓
4. SPAWN MULTI-AGENT:
   - builder-1: API endpoints pentru V34
   - integration-engineer: Integrare cu dashboard
   - qa-master: Testare completă V34
          ↓
5. TESTĂRI:
   - API endpoints funcționează?
   - Dashboard îl vede?
   - Start/Stop funcționează?
   - Log-urile se salvează?
   - Ciclul de analiză rulează?
          ↓
6. BUG-URI? → Atribuire automată → Fixare → Re-test
          ↓
7. NOTIFICARE: "🚀 V34 Tokyo Breakout ready pentru producție"
```

---

## 🛠️ IMPLEMENTARE PAS CU PAS

### Pas 1: Instalează File Watcher
```bash
pip install watchdog
```

### Pas 2: Creează serviciul
```bash
# /etc/systemd/system/auto-testing.service
[Unit]
Description=Auto Testing Pipeline
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /workspace/shared/hooks/file_watcher.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Pas 3: Activează
```bash
sudo systemctl enable auto-testing
sudo systemctl start auto-testing
```

### Pas 4: Hook OpenClaw
```bash
# Adaugă în /root/.openclaw/hooks/auto-pipeline/
cp /workspace/shared/hooks/auto-pipeline/* /root/.openclaw/hooks/
```

---

## 📊 STATUS DASHBOARD

Vrei un dashboard unde vezi în timp real:
- Ce teste rulează acum
- Câte bug-uri deschise
- Progres fixare
- Status agenți
- Ultimele modificări cod

---

## ✅ CE E ACUM vs CE VA FI

| ACUM (Manual) | VIITOR (Automat) |
|---------------|------------------|
| Tu spui "testează" | File watcher detectează automat |
| Manual bug report | Auto bug report + routing |
| Manual assign | Auto assign agent |
| Manual spawn fixer | Auto spawn fixer |
| Manual retest | Auto retest după fix |
| Verifici tu status | Dashboard live + notificări |

---

## 🚀 VREI SĂ IMPLEMENTĂM ACUM?

Opțiuni:
1. **Full Automation** - File watcher + hooks + cron (recomandat)
2. **Git-based** - Hook la fiecare commit/push
3. **Manual trigger** - Tu spui "start testing" și restul e automat
4. **Hybrid** - Auto pentru bug-uri critice, manual pentru features noi

Ce preferi? Implementăm acum! 🎯
