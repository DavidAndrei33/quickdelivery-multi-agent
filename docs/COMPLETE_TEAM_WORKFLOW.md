# 🎯 WORKFLOW COMPLET - ECHIPA MULTI-AGENT (40+ Agenți)

## 📋 OVERVIEW

Sistemul este proiectat să scaleze de la 14 agenți actuali la **40+ agenți** care lucrează simultan pe același proiect, fără conflicte.

---

## 🏛️ ARHITECTURA WORKFLOW

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           USER (Andrei)                                  │
│                     ↓ Trimite cerință/task                              │
├─────────────────────────────────────────────────────────────────────────┤
│                      ORCHESTRATOR (Manifest)                             │
│                     ↓ Consultă Project Brain                             │
├─────────────────────────────────────────────────────────────────────────┤
│                     PROJECT BRAIN (Memory)                               │
│  ┌─────────────────┬─────────────────┬─────────────────┐               │
│  │ project_state   │ features.json   │ architecture.md │               │
│  │ files_index     │ decisions.md    │ versions/       │               │
│  └─────────────────┴─────────────────┴─────────────────┘               │
│                     ↓ Returnează plan de acțiune                        │
├─────────────────────────────────────────────────────────────────────────┤
│                     HOOK SYSTEM (OpenClaw)                               │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐             │
│  │team-orchestr│ bug-tracker │ task-coordin│ agent-recove│             │
│  │ator         │             │ ator        │ ry          │             │
│  └─────────────┴─────────────┴─────────────┴─────────────┘             │
│                     ↓ Distribuie task-uri                               │
├─────────────────────────────────────────────────────────────────────────┤
│                          40+ AGENȚI                                      │
│  ┌───────────┬───────────┬───────────┬───────────┬───────────┐         │
│  │ BUILDERS  │ REVIEWERS │   OPS     │  BACKEND  │ FRONTEND  │         │
│  │(15 agenți)│(10 agenți)│(10 agenți)│ (3 agenți)│ (2 agenți)│         │
│  └───────────┴───────────┴───────────┴───────────┴───────────┘         │
│                                                                          │
│  Exemple: builder-15, reviewer-8, ops-7, etc.                           │
│                     ↓ Execută task-uri                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                     SERVICII & OUTPUT                                    │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐               │
│  │  MT5 Core│ PostgreSQL│ Dashboard│  VPS     │  Trading │               │
│  │  Server  │ Database  │  UI      │  Bridges │  Robots  │               │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘               │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🔁 WORKFLOW PAS CU PAS

### **PAS 1: User Creează Task Nou**

**Exemplu:** Andrei spune: "Adaugă V34 Tokyo Breakout Robot"

```
Andrei → Orchestrator
         "Am nevoie de V34 Tokyo Breakout"
```

---

### **PAS 2: Orchestrator Consultă Project Brain** (OBLIGATORIU)

```
Orchestrator → Project Brain: "Ce există deja pentru V34?"
                    ↓
Project Brain citește din memorie:
  - project_state.json → Vede că V32, V33 există
  - features.json      → Vede că V34 e în "pending"
  - architecture.md    → Vede pattern-ul de implementare
  - files_index.json   → Vede ce fișiere există deja
                    ↓
Project Brain returnează:
{
  "current_state": {
    "existing_robots": ["V31", "V32", "V33"],
    "v34_status": "pending",
    "pattern_available": true
  },
  "gaps": [
    "API endpoints pentru V34",
    "SQL queries pentru Tokyo session",
    "Dashboard UI pentru V34"
  ],
  "next_steps": [
    "1. Creează API /api/v34/or_data",
    "2. Creează API /api/v34/breakout_status",
    "3. Adaugă în dashboard JavaScript",
    "4. Testează integrarea"
  ],
  "risks": [
    "V34 folosește aceeași logică ca V32/V33",
    "Trebuie să evităm cod duplicat"
  ],
  "existing_files": [
    "/root/clawd/agents/brainmaker/mt5_core_server.py",
    "/root/clawd/agents/brainmaker/dashboard/dashboard_functional.js"
  ]
}
```

---

### **PAS 3: Orchestrator Crează Task-uri în Task Board**

```
Orchestrator updatează TASKBOARD.json:

{
  "tasks": {
    "active": [
      {
        "id": "TASK-V34-API-001",
        "title": "Implement V34 Tokyo OR API",
        "description": "Create /api/v34/or_data endpoint",
        "assigned_to": "builder-1",
        "priority": "HIGH",
        "status": "Assigned",
        "estimated_time": "2h"
      },
      {
        "id": "TASK-V34-API-002",
        "title": "Implement V34 Breakout Status API",
        "description": "Create /api/v34/breakout_status endpoint",
        "assigned_to": "builder-2",
        "priority": "HIGH",
        "status": "Assigned",
        "estimated_time": "2h"
      },
      {
        "id": "TASK-V34-DASHBOARD-001",
        "title": "Add V34 to Dashboard",
        "description": "Add V34 Tokyo section to dashboard_functional.js",
        "assigned_to": "builder-4",
        "priority": "HIGH",
        "status": "Waiting",
        "dependencies": ["TASK-V34-API-001", "TASK-V34-API-002"]
      }
    ]
  }
}
```

---

### **PAS 4: Hook-uri Detectează și Notifică**

```
Hook "task-coordinator" detectează task-uri noi:
  ↓
Citește TASKBOARD.json
  ↓
Găsește TASK-V34-API-001 assigned to builder-1
  ↓
Trimite notificare:
  "📋 Task nou: TASK-V34-API-001 (Implement V34 Tokyo OR API)"
  "Prioritate: HIGH"
  "Estimat: 2h"
  "Assigned to: builder-1"
```

---

### **PAS 5: Agentul Începe Să Lucreze** (builder-1)

```
builder-1 primește notificare
  ↓
1. CITEȘTE din Project Brain:
   - Citește architecture.md → Vede cum e făcut V32/V33
   - Citește files_index.json → Vede unde să modifice
   - Citește features.json → Vede ce mai trebuie

2. ACQUIRE LOCK pe fișier:
   python3 /workspace/shared/hook_manager.py lock.acquire \
     /root/clawd/agents/brainmaker/mt5_core_server.py builder-1

3. IMPLEMENTEAZĂ:
   - Adaugă endpoint /api/v34/or_data în mt5_core_server.py
   - Copiază pattern de la V32/V33
   - Modifică pentru Tokyo session (00:00-09:00 UTC)

4. TESTEAZĂ:
   - Rulează curl http://localhost:8001/api/v34/or_data
   - Verifică că returnează date corecte

5. RELEASE LOCK:
   python3 /workspace/shared/hook_manager.py lock.release \
     /root/clawd/agents/brainmaker/mt5_core_server.py builder-1

6. UPDATE Project Brain:
   - Update features.json → TASK-V34-API-001 = "completed"
   - Update project_state.json → adaugă V34 module
   - Log în decisions.md

7. MARK TASK DONE în TASKBOARD.json
```

---

### **PAS 6: Review și QA**

```
Hook "task-coordinator" detectează task completat
  ↓
Mută task din "active" în "review"
  ↓
Notifică reviewer-1 (Code Reviewer)
  ↓
reviewer-1:
  - Citește codul modificat
  - Verifică pattern-urile
  - Rulează teste
  - Aprobă sau cere modificări
  ↓
Dacă aprobat → Mută în "completed"
Dacă respins → Înapoi la "active" cu comentarii
```

---

### **PAS 7: Hook-uri Updatează Dashboard**

```
Hook "dashboard-sync" detectează update
  ↓
Vede că API V34 e gata
  ↓
Notifică builder-4 (Dashboard Frontend):
  "API V34 ready - poți începe TASK-V34-DASHBOARD-001"
  ↓
builder-4:
  - Adaugă V34 în dashboard_functional.js
  - Adaugă selector în dropdown
  - Testează în browser
```

---

### **PAS 8: Bug Tracking (dacă e cazul)**

```
Dacă apare eroare:
  ↓
Hook "bug-tracker" detectează:
  - API returnează 500
  - Sau testele eșuează
  ↓
Creează automat BUG-YYYYMMDD-XXX.md:
  - Descriere eroare
  - Stack trace
  - Auto-assign la builder-1 (cel care a lucrat la cod)
  ↓
builder-1 primește notificare și fixează
```

---

### **PAS 9: Agent Recovery (dacă e cazul)**

```
Dacă builder-1 nu răspunde >10 minute:
  ↓
Hook "agent-recovery" detectează:
  - Verifică last_heartbeat
  - Vede că builder-1 e "stalled"
  ↓
Încearcă recovery:
  - Retry task (max 3 ori)
  ↓
Dacă eșuează:
  - Reassign task la builder-2
  - Notifică orchestrator
  - Update TASKBOARD.json
```

---

### **PAS 10: Finalizare și Report**

```
Când toate task-urile V34 sunt "completed":
  ↓
Hook "team-orchestrator":
  - Update project_state.json → V34 status = "operational"
  - Update features.json → V34 = "completed"
  - Creează versiune nouă în versions/v2.1.0.md
  ↓
Notifică Andrei:
  "✅ V34 Tokyo Breakout Robot implementat cu succes!"
  "Dashboard: http://localhost:8001/dashboard"
```

---

## 🔄 CICLU ZILNIC ( pentru 40+ agenți )

### **00:00 - 08:00 (Night Shift - Agenți din alte fusuri orare)**
```
- 5 agenți în Asia lucrează pe task-uri
- 3 agenți în America lucrează pe task-uri
- Hook-urile monitorizează 24/7
```

### **08:00 - 18:00 (Day Shift - Agenți Europa)**
```
- 20 agenți activi
- Daily standup via cron job
- Code reviews în timp real
```

### **18:00 - 00:00 (Evening Shift)**
```
- 10 agenți pentru task-uri urgente
- QA testing și bug fixing
```

---

## 📊 COMUNICARE ÎNTRE AGENȚI

### **1. Shared Memory (Primar)**
```
/workspace/shared/memory/
  - Toți agenții citesc/scriu aici
  - File locks prevenesc conflicte
```

### **2. Task Board (Coordonare)**
```
/workspace/shared/tasks/TASKBOARD.json
  - Fiecare agent verifică înainte să lucreze
  - Update status la fiecare schimbare
```

### **3. Notifications (Urgent)**
```
- sessions_send pentru alerte critice
- Hook-uri pentru evenimente
```

---

## 🛡️ PROTECȚIE CONFLICTE (40+ Agenți)

### **File Lock System:**
```python
# Înainte să modifice:
hook_manager.py lock.acquire /path/to/file agent-id

# Modifică fișierul...

# După ce termină:
hook_manager.py lock.release /path/to/file agent-id
```

### **Read Before Write Pattern:**
```python
# Fiecare agent:
1. Citește project_state.json
2. Verifică ce există deja
3. Implementează
4. Updatează starea
```

### **Retry Logic:**
```python
- Max 3 retry pentru fiecare task
- Dacă eșuează → reassign la alt agent
- Escaladare la orchestrator după 3 eșecuri
```

---

## 📈 SCALABILITATE

| Agenți | Task-uri/zi | Bug-uri/zi | Timp mediu/task |
|--------|-------------|------------|-----------------|
| 14     | 20-30       | 5-10       | 2-4 ore         |
| 20     | 40-60       | 10-15      | 1.5-3 ore       |
| 40     | 100-150     | 20-30      | 1-2 ore         |

**Cu cât mai mulți agenți → task-urile se paralelizează → timp mai mic per task**

---

## 🎯 EXEMPLE CONCRETE

### **Exemplu 1: Feature Nou (V35 Robot)**
**Timp estimat cu 14 agenți:** 3 zile
**Timp estimat cu 40 agenți:** 1 zi

**Distribuție task-uri:**
- builder-1,2,3: API backend (paralel)
- builder-4,5: Dashboard frontend (paralel)
- reviewer-1,2,3: Code review (paralel)
- qa-tester-1,2: Testing (paralel)

### **Exemplu 2: Bug Critical (API Down)**
**Detectare:** Automată via bug-tracker hook
**Fix:** builder-1 (specialist API)
**Test:** qa-tester-1
**Deploy:** ops-1
**Timp total:** <30 minute

---

## ✅ STATUS CURENT

| Componentă | Status | Capacitate |
|------------|--------|------------|
| Project Brain | ✅ Ready | 40+ agenți |
| Hook System | ✅ Ready | 11 hook-uri active |
| Task Board | ✅ Ready | Unlimited tasks |
| File Locks | ✅ Ready | Previne conflicte |
| Memory System | ✅ Ready | 6 fișiere JSON |

---

## 🚀 PENTRU A ADAUGA MAI MULȚI AGENȚI

### **Pas 1: Creează Agent Nou**
```bash
mkdir -p /workspace/shared/docs/agents/builder-15
cat > /workspace/shared/docs/agents/builder-15/README.md << 'EOF'
# builder-15 - API Specialist

## Rol
Implementare API endpoints

## Skills
- Python, Flask, SQL

## Contact
- Escalare: builder-1 (lead)
EOF
```

### **Pas 2: Înregistrează în Echipă**
```bash
# Update team_orchestration.json
# Adaugă builder-15 în lista de builders
```

### **Pas 3: Agentul începe să lucreze**
```
builder-15:
  - Citește SOUL.md
  - Citește README.md
  - Verifică TASKBOARD.json
  - Ia primul task disponibil
```

---

**Acest workflow permite 40+ agenți să lucreze simultan fără conflicte!**
