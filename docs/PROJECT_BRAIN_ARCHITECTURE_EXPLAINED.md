# 🧠 ARHITECTURA PROJECT BRAIN - Cum Funcționează cu 40+ Agenți

## ⚠️ CONCEPT CHEIE: Project Brain NU Comandă Direct

**Greșeală comună:** Să crezi că Project Brain dă ordine.
**Realitatea:** Project Brain este **SURSĂ DE ADEVĂR** (Single Source of Truth) pe care toți o **CONSULTĂ**.

---

## 🏛️ ARHITECTURA REALĂ

```
                    USER
                     ↓
              ORCHESTRATOR
                     ↓
           ┌────────┴────────┐
           ↓                 ↓
    🧠 PROJECT BRAIN    [HOOKS - 10 hook-uri]
    (Menține stare)     (Citesc din memorie)
           ↑                 ↑
           └────────┬────────┘
                    ↓
    ┌───────────────────────────────┐
    │       SHARED MEMORY           │
    │  /workspace/shared/memory/    │
    │  • project_state.json         │
    │  • features.json              │
    │  • architecture.md            │
    │  • files_index.json           │
    │  • decisions.md               │
    └───────────────────────────────┘
                    ↓
    ┌───────────────────────────────┐
    │      40+ AGENȚI               │
    │  • Citesc din memorie         │
    │  • Verifică before modify     │
    │  • Update după execuție       │
    └───────────────────────────────┘
```

---

## 🔍 CUM FUNCȚIONEAZĂ PENTRU 40+ AGENȚI

### Pattern: "Read Before Write"

**Fiecare agent (din cei 40+) urmează:**
```
1. Agent primește task
   ↓
2. CITEȘTE din /workspace/shared/memory/
   • project_state.json
   • features.json
   • files_index.json
   ↓
3. Verifică: "Ce există deja?"
   ↓
4. EXECUTĂ task-ul
   ↓
5. UPDATEAZĂ memoria:
   • Adaugă în project_state.json
   • Update features.json
   • Log în decisions.md
```

---

## 📝 EXEMPLE CONCRETE

### Exemplu 1: Hook `team-orchestrator` citește Project Brain

```typescript
// În ~/.openclaw/hooks/team-orchestrator/handler.ts

const handler: HookHandler = async (event) => {
  // 1. CITEȘTE din Project Brain (shared memory)
  const projectState = JSON.parse(
    fs.readFileSync('/workspace/shared/memory/project/project_state.json')
  );
  
  // 2. Folosește datele
  console.log(`Project has ${projectState.completed_features.length} completed features`);
  
  // 3. Verifică agenți blocați
  const stalledAgents = projectState.modules.filter(m => m.status === 'stalled');
  
  if (stalledAgents.length > 0) {
    // Trigger recovery
    event.messages.push(`⚠️ ${stalledAgents.length} agenți blocați`);
  }
};
```

### Exemplu 2: Agent `builder-15` (din cei 40+) consultă Project Brain

```python
# Agent builder-15 primește task: "Adaugă login system"

def execute_task(task):
    # 1. CITEȘTE Project Brain
    with open('/workspace/shared/memory/features/features.json') as f:
        features = json.load(f)
    
    # 2. Verifică dacă există deja
    existing = [f for f in features['features'] if f['name'] == 'Login system']
    
    if existing:
        return "Eroare: Feature already exists!"
    
    # 3. Verifică arhitectura
    with open('/workspace/shared/memory/architecture/architecture.md') as f:
        arch = f.read()
    
    # 4. EXECUTĂ task-ul
    create_login_system()
    
    # 5. UPDATEAZĂ Project Brain
    features['features'].append({
        'name': 'Login system',
        'status': 'completed',
        'completed_at': datetime.now().isoformat()
    })
    
    with open('/workspace/shared/memory/features/features.json', 'w') as f:
        json.dump(features, f, indent=2)
    
    return "Success!"
```

---

## 🎯 ROLUL HOOK-URILOR

### Hook-urile sunt **CONSUMATORI** ai Project Brain:

| Hook | Ce citește din Project Brain | Acțiune |
|------|------------------------------|---------|
| **team-orchestrator** | `project_state.json` → module status | Verifică agenți blocați |
| **task-coordinator** | `features.json` → pending features | Assign task-uri noi |
| **bug-tracker** | `project_state.json` → failed_tasks | Creează bug reports |
| **agent-recovery** | `project_state.json` → module status | Recuperează agenți |
| **project-brain** | Toate fișierele | Menține consistența |

---

## 🔄 FLOW COMPLET PENTRU 40+ AGENȚI

### Când un agent (din cei 40+) primește task:

```
Agent #23 (builder-23):
  ↓
1. Primește task: "Implementează V35 Tokyo Breakout"
  ↓
2. CITEȘTE /workspace/shared/memory/project/project_state.json
   • Vede că V32, V33 există
   • Vede că V34 e pending
   • Vede pattern-ul de implementare
  ↓
3. CITEȘTE /workspace/shared/memory/architecture/architecture.md
   • Vede cum sunt structurate API-urile
   • Vede pattern-ul pentru roboți
  ↓
4. CITEȘTE /workspace/shared/memory/files_index/files_index.json
   • Vede ce fișiere există deja
   • Vede unde să adauge noul cod
  ↓
5. EXECUTĂ implementarea V35
  ↓
6. UPDATEAZĂ Project Brain:
   • Adaugă în features.json
   • Update project_state.json
   • Log în decisions.md
  ↓
7. NOTIFICĂ orchestrator
```

---

## 📊 SCALABILITATE PENTRU 40+ AGENȚI

### Cum se scalează:

**1. Toți citesc aceleași fișiere:**
```
/workspace/shared/memory/ (Shared Memory Bus)
    ↓
Agent #1  ← Citesc
Agent #2  ← Toți
Agent #3  ← Aceleași
...       ← Fișiere
Agent #40 ← JSON
```

**2. File Lock pentru scriere:**
```python
# Când un agent updatează:
with file_lock('/workspace/shared/memory/project_state.json'):
    # Doar un agent poate scrie la un moment dat
    update_json()
```

**3. Hook-uri reacționează la evenimente:**
```
Agent #15 completează task
  ↓
Trigger: session:patch
  ↓
Hook task-coordinator detectează
  ↓
Hook notifică alți agenți disponibili
```

---

## 🎮 COMENZI PENTRU A VEDEA CUM FUNCȚIONEAZĂ

### Vezi ce citesc agenții:
```bash
# Status proiect (toți agenții citesc asta)
cat /workspace/shared/memory/project/project_state.json

# Features (toți verifică înainte să creeze)
cat /workspace/shared/memory/features/features.json

# Arhitectura (toți consultă)
cat /workspace/shared/memory/architecture/architecture.md
```

### Vezi hook-urile active:
```bash
openclaw hooks list
# Toate ar trebui să arate: ✓ ready
```

### Vezi log-ul Project Brain:
```bash
tail -f /workspace/shared/logs/project-brain.log
```

---

## ✅ VERIFICARE: Toate Hook-urile Active

| Hook | Status |
|------|--------|
| 🧠 project-brain | ✅ Enabled |
| 🤖 trading-orchestrator | ✅ Enabled |
| 🎯 team-orchestrator | ✅ Enabled |
| 🐛 bug-tracker | ✅ Enabled |
| 📋 task-coordinator | ✅ Enabled |
| 🔄 agent-recovery | ✅ Enabled |
| ⚙️ robot-lifecycle | ✅ Enabled |
| 📊 dashboard-sync | ✅ Enabled |
| 🚨 emergency-alert | ✅ Enabled |
| 📝 audit-logger | ✅ Enabled |
| 🧠 smart-memory-curator | ✅ Enabled (bundled) |

**Total: 11 hook-uri active**

---

## 🎓 CONCLUZIE

**Project Brain NU comandă agenții. El:**
1. ✅ **Menține starea** în JSON files
2. ✅ **Oferă sursă de adevăr** pe care toți o citesc
3. ✅ **Previne conflicte** (agenții verifică înainte să modifice)
4. ✅ **Permite scalare** la 40+ agenți (toți citesc aceleași fișiere)
5. ✅ **Reacționează** prin hook-uri la evenimente

**Agenții (40+) sunt autonomi dar CONSULTĂ întotdeauna Project Brain înainte să modifice ceva!**

---
**Ultima actualizare:** 2026-03-28 09:15 UTC
