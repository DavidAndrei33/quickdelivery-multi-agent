# BUG ROUTING SYSTEM - Automatizare Atribuire
## Configurație: Cine fixează ce tip de bug

---

## 🎯 REGULI DE ATRIBUIRE AUTOMATĂ

### După Componentă:
| Componentă Bug | Agent Responsabil | Skill |
|----------------|-------------------|-------|
| Backend API (404, 500, CORS) | builder-1 | Python, Flask |
| Database (PostgreSQL, queries) | builder-2 | SQL, DB Design |
| Frontend JS (funcții, logică) | dashboard-frontend | JavaScript |
| Frontend UI (HTML, CSS, layout) | builder-3 | HTML/CSS |
| Security (XSS, Auth, Injecții) | security-auditor | Security |
| Performance (slow, memory) | optimization-specialist | Performance |
| Integration (API-UI mismatch) | integration-engineer | Full-stack |

### După Severitate:
```
CRITICAL (P0) → Toți agenții disponibili + Manifest notificat imediat
HIGH (P1)     → Agent principal + Reviewer
MEDIUM (P2)   → Agent principal
LOW (P3)      → Backlog pentru sprint viitor
```

---

## 🔄 WORKFLOW AUTOMAT

```
┌─────────────┐    Bug găsit      ┌─────────────┐
│  QA-Master  │ ────────────────→ │  Bug Router │
│  (Testing)  │   + Detalii       │  (Automat)  │
└─────────────┘                   └──────┬──────┘
                                         │
                    Analizează tip bug   │
                    ↓                    ↓
            ┌─────────────┐      ┌─────────────┐
            │ Backend Bug │────→ │  builder-1  │
            │ Frontend Bug│────→ │dashboard-...│
            │ Security Bug│────→ │security-... │
            └─────────────┘      └─────────────┘
                                         │
                                         ↓
                              ┌─────────────┐
                              │   Manifest  │ ← Notificare
                              │ (Monitor)   │   completare
                              └─────────────┘
```

---

## 📋 IMPLEMENTARE

### 1. Bug Router Script
Locație: `/workspace/shared/hooks/bug_router.py`
Trigger: Când apare fișier nou în `/workspace/shared/bugs/`

### 2. Task Auto-Generation
Pentru fiecare bug, generează:
- `/workspace/shared/tasks/auto/BUG-XXX-task.json`
- Notificare agent responsabil
- Deadline bazat pe severitate

### 3. Tracking Progres
- Agentul updatează status în fișierul bug
- QA-Master verifică fixul
- La validare, bug marcat FIXED

---

## 🚀 EXEMPLU FLOW

### Bug Raportat:
```
BUG-004: XSS Vulnerability
Severitate: HIGH
Componentă: Frontend JS
File: dashboard_functional.js
```

### Automatizare:
1. **Bug Router** detectează BUG-004.md creat
2. **Analizează**: Frontend JS → dashboard-frontend
3. **Generează Task**: `TASK-AUTO-004: Fix XSS in dashboard_functional.js`
4. **Spawn Agent**: dashboard-frontend primește task
5. **Notificare**: Manifest primește alertă HIGH
6. **Tracking**: Status update la fiecare 5 min
7. **Retest**: QA-Master verifică fixul
8. **Close**: Bug marcat FIXED, task completat

---

## ⚡ ACUM vs VIITOR

### ACUM (Manual):
- QA-Master găsește bug
- Scrie raport în bugs/
- Manifest citește și decide
- Spawnează manual agenți

### VIITOR (Automat):
- QA-Master găsește bug
- Scrie raport în bugs/
- **Bug Router atribuie automat**
- **Agent spawnat automat**
- **Tracking automat**
- **Retest automat**

---

## ✅ IMPLEMENTARE ACUM

Vrei să implementez Bug Router-ul acum să:
1. **Monitorizeze** folderul bugs/
2. **Atribuie automat** bug-uri la agenți
3. **Spawn-eze agenți** pentru fixare
4. **Track-uiască progresul**
5. **Notifice** când e gata?
