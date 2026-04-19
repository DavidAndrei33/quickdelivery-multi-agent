# 👥 INDEX AGENȚI - Documentație Completă

## Echipa Multi-Agent - 14 Membri (inclusiv Project Brain)

---

## 🧠 PROJECT BRAIN (OBLIGATORIU)

| Agent | ID | Rol | Documentație |
|-------|-----|-----|--------------|
| **Project Brain** | project-brain | Project Continuity Manager | [README.md](./project-brain/README.md) |

**⚠️ REGULĂ CRITICĂ:** Orchestrator TREBUIE să consulte Project Brain înainte de orice modificare!

---

## 🏗️ BUILDERS (7 agenți)

### Core Developers
| Agent | ID | Rol | Documentație |
|-------|-----|-----|--------------|
| **Core-Developer-1** | builder-1 | API Implementation | [README.md](./builder-1/README.md) |
| **Core-Developer-2** | builder-2 | Dashboard Backend | [README.md](./builder-2/README.md) |
| **Core-Developer-3** | builder-3 | Integration | [README.md](./builder-3/README.md) |

### Dashboard Team
| Agent | ID | Rol | Documentație |
|-------|-----|-----|--------------|
| **Dashboard-Frontend-1** | builder-4 | UI/UX | [README.md](./builder-4/README.md) |
| **Dashboard-Backend-1** | builder-5 | API Design | [README.md](./builder-5/README.md) |

### Integration Engineers
| Agent | ID | Rol | Documentație |
|-------|-----|-----|--------------|
| **Integration-Engineer-1** | builder-6 | MT5 Integration | [README.md](./builder-6/README.md) |
| **Integration-Engineer-2** | builder-7 | Data Flow | [README.md](./builder-7/README.md) |

---

## 🔍 REVIEWERS (3 agenți)

| Agent | ID | Rol | Documentație |
|-------|-----|-----|--------------|
| **Code-Reviewer-1** | reviewer-1 | Code Quality | [README.md](./reviewer-1/README.md) |
| **Security-Auditor-1** | reviewer-2 | Security | [README.md](./reviewer-2/README.md) |
| **QA-Tester-1** | reviewer-3 | Testing | [README.md](./reviewer-3/README.md) |

---

## ⚙️ OPS (2 agenți)

| Agent | ID | Rol | Documentație |
|-------|-----|-----|--------------|
| **DevOps-Engineer-1** | ops-1 | Deployment | [README.md](./ops-1/README.md) |
| **Database-Admin-1** | ops-2 | Database | [README.md](./ops-2/README.md) |

---

## 🎯 ORCHESTRATOR

| Agent | ID | Rol | Documentație |
|-------|-----|-----|--------------|
| **Manifest** | orchestrator | Tech Lead | [SOUL.md](../memory/orchestrator/SOUL.md) |

---

## 📚 Documentație Comună (pentru toți agenții)

| Document | Scop | Locație |
|----------|------|---------|
| **Standing Orders** | Reguli obligatorii | `/workspace/shared/docs/STANDING_ORDERS.md` |
| **Communication Rules** | Cum comunicăm | `/workspace/shared/docs/AGENT_COMMUNICATION_RULES.md` |
| **Bug Tracking** | Sistem bug-uri | `/workspace/shared/docs/BUG_TRACKING_SYSTEM.md` |
| **Cron Jobs** | Job-uri automate | `/workspace/shared/docs/CRON_JOBS.md` |
| **System Summary** | Overview complet | `/workspace/shared/docs/SYSTEM_IMPLEMENTATION_SUMMARY.md` |

---

## 🛠️ Tools & Librării

| Tool | Scop | Locație |
|------|------|---------|
| **API Retry Wrapper** | Wrapper API cu retry | `/workspace/shared/lib/api_retry_wrapper.py` |
| **Bug Auto Detect** | Hook detectare bug-uri | `/workspace/shared/hooks/bug_auto_detect.py` |
| **Task Coordination** | Hook coordonare task-uri | `/workspace/shared/hooks/task_coordination.py` |
| **Master Control** | Control master sistem | `/workspace/shared/master_control.py` |

---

## 📋 Task Board

**Locație:** `/workspace/shared/tasks/TASKBOARD.json`

Secțiuni:
- **inbox** - Task-uri noi neasignate
- **active** - Task-uri în lucru
- **review** - Task-uri la review
- **completed** - Task-uri finalizate
- **blocked** - Task-uri blocate
- **failed** - Task-uri eșuate

---

## 🐛 Bug Tracking

**Locație:** `/workspace/shared/bugs/`

Format: `BUG-YYYYMMDD-XXX.md`

---

## 💾 Memorie pe Termen Lung

Fiecare agent are `SOUL.md` în:
`/workspace/shared/memory/agents/[agent-id]/SOUL.md`

---

## 🚀 Quick Start pentru Agenți Noi

1. **Citește Standing Orders** - Regulile sunt obligatorii
2. **Verifică Task Board** - Vezi ce task-uri sunt disponibile
3. **Citește documentația ta specifică** - Acest index
4. **Configurează SOUL.md** - Adaugă memoria ta
5. **Ia primul task** - Start cu ceva mic

---

**Sistem Version:** 2.0  
**Last Updated:** 2026-03-28  
**Total Agents:** 14 configured (inclusiv Project Brain)
