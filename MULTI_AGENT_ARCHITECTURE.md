# 🤖 MULTI-AGENT ORCHESTRATION SYSTEM
## Arhitectură Comunicare, Task Management & Workflow

---

## 1. 🔄 SISTEM DE COMUNICARE INTER-AGENT

### A. **Message Bus (Event-Driven)**
```
/workspace/shared/.event-bus/                    
├── events/                                       
│   ├── task-created/                            
│   ├── task-assigned/                           
│   ├── task-completed/                          
│   ├── review-requested/                        
│   ├── review-approved/                         
│   └── deploy-triggered/                        
└── subscribers.json     # Cine ascultă ce evenimente
```

**Exemplu flow:**
```
Product-Architect creează task
  ↓ (emite event: task-created)
Event Bus
  ↓ (notifică subscriberii)
Builder-Modules primește notificare
  ↓ (acceptă task)
Event Bus
  ↓ (emite: task-assigned)
Reviewer-All așteaptă completare...
```

### B. **Comunicare Directă (sessions_send)**
```javascript
// Manifest (Orchestrator) poate trimite mesaje direct
sessions_send({
  sessionKey: "agent:product-architect:main",
  message: "Task nou: Creează spec pentru feature X"
});

// Un agent poate spawna alt agent
sessions_spawn({
  agentId: "builder-modules",
  task: "Implementează conform spec-ului din /workspace/shared/specs/feature-x.md",
  label: "TASK-001"
});
```

### C. **Shared State (Single Source of Truth)**
```
/workspace/shared/.project-state/
├── current-project.json          # Proiect activ
├── tasks/
│   ├── TASK-001.json
│   ├── TASK-002.json
│   └── index.json               # Index toate task-urile
├── agents/
│   ├── product-architect-state.json
│   ├── builder-modules-state.json
│   └── ...
└── decisions/
    └── architectural-decisions.json
```

---

## 2. 📋 SISTEM DE TASK MANAGEMENT

### Structura Task:
```json
{
  "id": "TASK-001",
  "title": "Implementare sistem autentificare",
  "description": "...",
  "project": "quickdelivery-v2",
  "status": "in-progress",
  
  "lifecycle": {
    "created": "2026-04-19T10:00:00Z",
    "assigned": "2026-04-19T10:05:00Z",
    "started": "2026-04-19T10:10:00Z",
    "review-requested": null,
    "completed": null
  },
  
  "assignment": {
    "created_by": "product-architect",
    "assigned_to": "builder-modules",
    "reviewer": "reviewer-all",
    "approved_by": null
  },
  
  "dependencies": {
    "blocks": [],           # Task-uri blocate de acesta
    "blocked_by": [],       # Task-uri care blochează acesta
    "related": ["TASK-002"]  # Task-uri conexe
  },
  
  "artifacts": {
    "spec": "/workspace/shared/specs/TASK-001-spec.md",
    "design": "/workspace/shared/designs/TASK-001/",
    "code": "/workspace/shared/projects/quickdelivery-v2/src/auth/",
    "tests": "/workspace/shared/projects/quickdelivery-v2/tests/auth/"
  },
  
  "progress": {
    "percentage": 65,
    "last_update": "2026-04-19T14:30:00Z",
    "updates": [
      {"time": "...", "agent": "builder-modules", "text": "Finalizat JWT setup"}
    ]
  },
  
  "checklist": [
    {"item": "Setup JWT", "done": true, "by": "builder-modules"},
    {"item": "Login endpoint", "done": true, "by": "builder-modules"},
    {"item": "Register endpoint", "done": false, "by": "builder-modules"},
    {"item": "Password reset", "done": false, "by": "builder-modules"},
    {"item": "Frontend integration", "done": false, "by": "builder-modules"}
  ]
}
```

### Workflow Task Lifecycle:
```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  INBOX   │───→│ ASSIGNED │───→│ PROGRESS │───→│  REVIEW  │───→│   DONE   │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
     │               │               │               │               │
     │            [ACCEPT]       [UPDATE]      [SUBMIT]      [APPROVE]
     │            [REJECT]                         │               │
     │                                           [REQUEST        │
     │                                            CHANGES]        │
     │                                                           │
     └───────────────────────────────────────────────────────────┘
                              [REOPEN]
```

---

## 3. 🎯 ORCHESTRATOR - Manifest (Main Agent)

Rolul meu ca Orchestrator:

```python
class Orchestrator:
    def create_project(self, name, requirements):
        """Creează proiect nou și setează echipe"""
        
    def assign_task(self, task_id, agent_id):
        """Asignează task la agent specific"""
        
    def check_dependencies(self, task_id):
        """Verifică dacă dependențele sunt complete"""
        
    def route_message(self, from_agent, to_agent, message):
        """Rutează mesaje între agenți"""
        
    def trigger_workflow(self, project_id, workflow_type):
        """Declanșează workflow standard"""
        
    def monitor_progress(self):
        """Monitorizează progresul tuturor task-urilor"""
```

### Comenzi Disponibile:
```
/new-project [nume] - Creează proiect nou
/create-task [titlu] [agent] - Creează task
/assign [task-id] [agent] - Asignează task
/status [task-id] - Vezi status task
/block [task-id] [reason] - Blochează task
/unblock [task-id] - Deblochează task
/review [task-id] - Trimite la review
/approve [task-id] - Aprobă task
/deploy [project] - Deploy proiect
```

---

## 4. 🧠 MEMORIE COLECTIVĂ (Project Brain)

### Structura Cunoașterii:
```
/workspace/shared/.project-brain/
├── projects/
│   └── [project-name]/
│       ├── README.md              # Overview proiect
│       ├── architecture.md        # Arhitectură și decizii
│       ├── tech-stack.md         # Stack tehnologic
│       ├── api-contracts.md       # Contracte API
│       ├── database-schema.md     # Schema DB
│       ├── conventions.md         # Convenții cod
│       ├── changelog.md           # Istoric modificări
│       └── agents-knowledge/      # Ce știe fiecare agent
│           ├── product-architect.json
│           ├── frontend-architect.json
│           └── ...
│
├── shared-knowledge/
│   ├── libraries-evaluated.json
│   ├── patterns-used.json
│   ├── lessons-learned.json
│   └── best-practices.json
│
├── decisions/
│   ├── ADR-001-auth-method.md
│   ├── ADR-002-database.md
│   └── registry.json
│
└── context-sync.json              # Sync între agenți
```

### Sync Memorie:
```javascript
// Fiecare agent își sincronizează cunoștințele
{
  "agent": "builder-modules",
  "project": "quickdelivery-v2",
  "last_sync": "2026-04-19T10:00:00Z",
  "knowledge": {
    "understands": [
      "Arhitectura microservices",
      "Auth flow JWT",
      "Database schema v2"
    ],
    "working_on": "TASK-001: Implementare auth",
    "blocked_by": null,
    "needs_clarification": []
  }
}
```

---

## 5. 🔄 WORKFLOW-URI STANDARDIZATE

### Workflow 1: New Feature Development
```
1. Product-Architect
   └─→ Creează spec + acceptance criteria
   └─→ Definește task-uri în Taskboard
   
2. Orchestrator (Manifest)
   └─→ Asignează task-uri la Builder-Modules
   
3. Builder-Modules
   └─→ Implementează conform spec
   └─→ Updatează progress în Taskboard
   └─→ Trimite la Review când e gata
   
4. Reviewer-All
   └─→ Code review (FE + BE + Security)
   └─→ Aprobă sau request changes
   
5. Operations-All
   └─→ Deploy în staging
   └─→ Run automated tests
   └─→ Deploy în production
   
6. QA-Tester (Operations-All)
   └─→ Manual testing în production
   └─→ Sign-off sau bug report
```

### Workflow 2: Hotfix
```
1. Operations-All detectează bug
   └─→ Creează hotfix task
   
2. Builder-Modules implementează fix
   
3. Reviewer-All review rapid (focus: security)
   
4. Operations-All deploy imediat
```

### Workflow 3: Architecture Decision
```
1. Product-Architect + Frontend-Architect + Backend-Architect
   └─→ Discuție arhitecturală
   
2. Specialists-All (Research)
   └─→ Research opțiuni
   
3. Architects
   └─→ Creează ADR (Architecture Decision Record)
   
4. Orchestrator
   └─→ Updatează Project Brain
   └─→ Notifică toți agenții de decizie
```

---

## 6. 🎛️ STANDING ORDERS (Reguli Permanente)

### Reguli pentru Toți Agenții:

```yaml
1. Task Reading:
   - Verifică Taskboard la fiecare 15 minute
   - Citește întotdeauna spec-ul înainte de a începe
   - Înțelege dependențele înainte de a accepta

2. Communication:
   - Updatează progress în Taskboard la fiecare oră
   - Comunică blocările imediat
   - Folosește format standard pentru updates

3. Memory:
   - Citește Project Brain înainte de a lucra
   - Documentează deciziile în ADR
   - Sync-ează cunoștințele la final de task

4. Quality:
   - No code fără tests
   - No deploy fără review
   - No merge fără approval
```

---

## 7. 📱 INTERFAȚĂ DE CONTROL (Pentru Andrei)

### Comenzi Simple:
```
/new-project QuickDelivery V3
  └─→ Creează proiect cu toți agenții asignați

/feature Sistem de notificări push
  └─→ Product-Architect creează spec
  └─→ Se generează task-uri automat
  └─→ Builder-Modules primește asignare

/status
  └─→ Vezi statusul tuturor task-urilor active

/deploy QuickDelivery V3
  └─→ Operations-All face deploy complet

/fix Bug la login
  └─→ Creează hotfix workflow
```

---

## 8. 🔧 IMPLEMENTARE - Primii Pași

### Pasul 1: Creează Structura
```bash
mkdir -p /workspace/shared/{.project-brain,.event-bus,.project-state}
mkdir -p /workspace/shared/.project-brain/projects
mkdir -p /workspace/shared/.event-bus/events
mkdir -p /workspace/shared/.project-state/tasks
```

### Pasul 2: Creează Primul Proiect
```bash
# Exemplu: QuickDelivery V3
# - Product-Architect creează spec
# - Se generează task-uri
# - Se asignează builder-ilor
```

### Pasul 3: Dashboard Vizual
- Taskboard HTML cu toate coloanele
- Real-time updates
- Asignare drag & drop

---

## ✅ CHECKLIST IMPLEMENTARE

- [ ] Creare structură directoare
- [ ] Setup Event Bus
- [ ] Creare Taskboard JSON
- [ ] Creare Project Brain pentru proiect pilot
- [ ] Configurare Standing Orders în AGENTS.md
- [ ] Creare workflow-uri standard
- [ ] Test end-to-end cu 1 task simplu

---

**Vrei să începem implementarea acum?** 🚀
