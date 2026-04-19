# QuickDelivery Multi-Agent Team

Echipă de 9 agenți AI specializați pentru dezvoltarea platformei QuickDelivery.

## 🏗️ Arhitectură

### Gateway & Comunicare
- **Gateway Principal:** Port 18788 (HTTP API pentru orchestrare)
- **Porturi Agenți:** 18791-18797 (câte un port per agent)
- **Protocol:** HTTP POST pentru task assignment
- **Notificări:** Telegram bots pentru fiecare agent

### Mecanism Task Assignment (Event-Driven)

```
Product-Architect (Orchestrator)
    ↓
Creează task JSON în /workspace/shared/.task-drops/[agent]/
    ↓
Trimite HTTP POST către localhost:[port]/task-assigned
    ↓
Agentul primește notificare INSTANT
    ↓
Agentul notifică Andrei pe Telegram
    ↓
Agentul execută task-ul
    ↓
Agentul raportează completarea
```

## 👥 Echipa (9 Agenți)

### 🏛️ Arhitecți (3)

| Agent | Port | Rol | Bot Telegram |
|-------|------|-----|--------------|
| **Product-Architect** | 18791 | Orchestrator + Product Manager | @ProductArchitectbot |
| **Frontend-Architect** | 18792 | UI/UX, Design System | @FrontendArchitectbot |
| **Backend-Architect** | 18793 | API, Database, Infrastructure | @BackendArchitectbot |

### 🛠️ Builders (2)

| Agent | Port | Rol | Bot Telegram |
|-------|------|-----|--------------|
| **Builder-Modules** | 18794 | Web apps (Customer, Admin, Rider, Store, API) | @BuilderModulesBot |
| **Builder-Mobile** | 18795 | iOS/Android apps (React Native) | @BuilderMobilebot |

### 👁️ Quality (1)

| Agent | Port | Rol | Bot Telegram |
|-------|------|-----|--------------|
| **Reviewer-All** | 18796 | Code review (Frontend + Backend + Security) | @ReviewerAllbot |

### 🔧 Operations (1)

| Agent | Port | Rol | Bot Telegram |
|-------|------|-----|--------------|
| **Operations-All** | 18797 | DevOps, CI/CD, QA, Deploy | @operatioooooooonsaaabot |

### 📊 Research (1)

| Agent | Port | Rol | Bot Telegram |
|-------|------|-----|--------------|
| **Specialists-All** | - | Research, Business Analysis, Data Science | @Specialistibot |

*Note: Specialists-All nu are port dedicat, primește task-uri via Product-Architect*

## 📁 Structura Proiectului

```
/workspace/shared/
├── agents/                          # Workspace-uri agenți
│   ├── product-architect/          # Orchestrator
│   ├── frontend-architect/         # UI/UX
│   ├── backend-architect/          # API/DB
│   ├── builder-modules/            # Web development
│   ├── builder-mobile/             # Mobile development
│   ├── reviewer-all/               # Code review
│   ├── operations-all/             # DevOps/QA
│   └── specialists-all/            # Research
│
├── .task-drops/                    # Task assignment (event-driven)
│   ├── product-architect/
│   ├── frontend-architect/
│   ├── backend-architect/
│   ├── builder-modules/
│   ├── builder-mobile/
│   ├── reviewer-all/
│   ├── operations-all/
│   └── specialists-all/
│
├── .project-brain/                 # Memorie colectivă
│   └── projects/
│       └── [project-name]/
│           ├── README.md
│           ├── architecture.md
│           └── decisions/
│
├── .project-state/                 # Stare task-uri
│   └── tasks/
│       └── TASK-XXX.json
│
├── specs/                          # Specificații tehnice
│   ├── design-system.md
│   ├── component-library.md
│   └── [feature]-spec.md
│
└── docs/                           # Documentație
    ├── TEAM_DIRECTORY.md
    └── workflow.md
```

## 🚀 Workflow Task Assignment

### 1. Product-Architect creează task

```bash
# Salvează specificația
/workspace/shared/.task-drops/builder-modules/TASK-042.json
```

### 2. Product-Architect trimite trigger

```bash
curl -X POST http://localhost:18794/task-assigned \
  -H "Content-Type: application/json" \
  -d '{
    "taskId": "TASK-042",
    "taskFile": "/workspace/shared/.task-drops/builder-modules/TASK-042.json",
    "assignedBy": "product-architect",
    "priority": "high"
  }'
```

### 3. Agentul răspunde instant

**Notificare către Andrei (310970306):**
```
🚀 Builder-Modules: Am primit task TASK-042!
📋 Titlu: Implementare Dashboard Analytics
⏱️ Estimare: 4 ore
🎯 Încep execuția acum.
```

### 4. Agentul execută și raportează

**La finalizare:**
```
✅ Task TASK-042 completat!
📊 Summary: Dashboard analytics implementat cu 5 widget-uri
🔗 Vezi pe taskboard: https://taskboard.manifestit.dev
```

## 🔄 Comunicare Inter-Agent

### Flow Standard:
```
Andrei → Product-Architect → Frontend-Architect → Builder-Modules → Reviewer-All → Operations-All
```

### Notificări:
- **Start task:** Fiecare agent notifică Andrei când începe
- **Progress updates:** La milestone-uri importante
- **Blocaje:** Escalare imediată către Product-Architect
- **Completare:** Notificare + update taskboard

## 🛠️ Setup & Deployment

### 1. Clone Repository
```bash
git clone https://github.com/david3366/quickdelivery-multi-agent.git
cd quickdelivery-multi-agent
```

### 2. Configurează Environment
```bash
# Copiază configurația
cp config/openclaw.template.json ~/.openclaw/openclaw.json

# Editează cu token-urile tale
nano ~/.openclaw/openclaw.json
```

### 3. Pornește Agenții
```bash
# Fiecare agent în terminal separat
openclaw agent start product-architect
openclaw agent start frontend-architect
openclaw agent start backend-architect
openclaw agent start builder-modules
openclaw agent start builder-mobile
openclaw agent start reviewer-all
openclaw agent start operations-all
openclaw agent start specialists-all
```

### 4. Verifică Status
```bash
openclaw agent list
openclaw gateway status
```

## 📊 Taskboard

**URL:** https://taskboard.manifestit.dev

Dashboard vizual pentru:
- Task-uri active
- Status agenți
- Progress proiecte
- Timeline & deadlines

## 📝 Convenții

### Naming:
- Task-uri: `TASK-XXX` (ex: TASK-042)
- Branch-uri: `feature/TASK-XXX-descriere`
- Commits: `[TASK-XXX] Descriere schimbare`

### Documentație:
- Toate deciziile în `/workspace/shared/decisions/`
- Specificații în `/workspace/shared/specs/`
- Research în `/workspace/shared/research/`

## 🤝 Colaborare

### Product-Architect (Orchestrator):
- Primește cerințe de la Andrei
- Creează specificații
- Assign task-uri către agenți
- Monitorizează progresul

### Agenții Specializați:
- Primesc task-uri via HTTP trigger
- Execută și raportează status
- Colaborează prin shared memory
- Mențin independență completă

---

**Creat:** 19 Aprilie 2026  
**Versiune:** 1.0  
**Autor:** Andrei & QuickDelivery Team