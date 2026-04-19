# PROTOCOL TASKBOARD - Comunicare Directă

## 📋 Cum funcționează:

### 🎯 DOUĂ Taskboard-uri (IMPORTANT!)

| Taskboard | Folosești pentru | Citești când |
|-----------|------------------|--------------|
| **TASKBOARD.json** | Task-uri generale (DevOps, Backend, Frontend, QA) | La fiecare 5 minute |
| **TASKBOARD_DASHBOARD_LIVE.md** | Task-uri specifice Dashboard V31/V32/V33 | DOAR dacă lucrezi la dashboard |

---

### 1. Citești TASKBOARD.json (Principal)
**Locație:** `/workspace/shared/tasks/TASKBOARD.json`

### 2. Găsești task-uri pentru tine:
```json
{
  "agent": "YOUR_NAME",
  "status": "todo",
  "claimed_by": null
}
```

### 3. Când găsești un task:

#### A. CLAIM Task (obligatoriu)
Actualizează TASKBOARD.json:
```json
{
  "status": "in_progress",
  "claimed_by": "YOUR_NAME",
  "claimed_at": "2026-04-06T12:00:00Z"
}
```

#### B. Notifică direct pe Telegram (către Andrei ID: 310970306):
```
🎯 [CLAIM] @YOUR_NAME

📋 Task: [task.title]
📝 Status: STARTED
⏱️ ETA: [estimare ta]

@Andrei - Am început task-ul T00X
```

#### C. Când termini:
Actualizează TASKBOARD.json:
```json
{
  "status": "done",
  "completed_at": "2026-04-06T14:00:00Z"
}
```

#### D. Notifică Completare (direct către Andrei):
```
✅ [DONE] @YOUR_NAME

📋 Task: [task.title]
📤 Output: [ce ai livrat - path-uri, funcționalități]
📋 Next: [task-uri dependente sau ce urmează]

@Andrei - Task finalizat, aștept review sau next task
```

### 4. Dacă task-ul NU e pentru tine:
**SKIP** - nu face nimic, nu răspunde.

---

## 🎨 TASKBOARD_DASHBOARD_LIVE.md (Secundar)

**Folosești DOAR dacă lucrezi la Dashboard V31, V32 sau V33**

**Locație:** `/workspace/shared/tasks/TASKBOARD_DASHBOARD_LIVE.md`

### Când să citești:
- ✅ Ești Builder-Frontend și faci dashboard UI
- ✅ Ești Builder-Core și faci API pentru dashboard
- ✅ Ești Trading-Architect și faci integrare MT5

### Când NU citești:
- ❌ Ești DevOps-Engineer (folosește TASKBOARD.json)
- ❌ Ești QA-Tester (folosește TASKBOARD.json)
- ❌ Lucrezi la infrastructură/backend general

### Format diferit:
- Markdown (text liber), nu JSON
- Task-urile au format: `TASK-V31-001`, `TASK-V32-003`, etc.
- Statusul e în text, nu în câmpuri JSON

---

## 📝 Sumar - Ce taskboard folosesc?

| Agent | Taskboard Principal | Taskboard Secundar |
|-------|---------------------|-------------------|
| **DevOps-Engineer** | TASKBOARD.json | ❌ Nu folosește |
| **Builder-Frontend** | TASKBOARD.json | ✅ TASKBOARD_DASHBOARD_LIVE.md |
| **Builder-Core** | TASKBOARD.json | ✅ TASKBOARD_DASHBOARD_LIVE.md |
| **Strategy-Architect** | TASKBOARD.json | ⚠️ Opțional |
| **QA-Tester** | TASKBOARD.json | ❌ Nu folosește |
| **QA-Security** | TASKBOARD.json | ❌ Nu folosește |
| **Trading-Architect** | TASKBOARD.json | ✅ TASKBOARD_DASHBOARD_LIVE.md |

---

## 🔄 Flow Complet:

```
Andrei sau Team-Manager adaugă task în TASKBOARD.json
        ↓
Team-Manager citește taskboard (la fiecare 2 minute)
        ↓
Team-Manager trimite task-ul direct agentului asignat
        ↓
Agentul CLAIM → notifică Andrei direct
        ↓
Agentul lucrează
        ↓
Agentul DONE → notifică Andrei direct
        ↓
Team-Manager identifică next task
        ↓
Repeat
```

---

## 📝 Exemple de Mesaje:

### Exemplu 1: CLAIM Task
```
🎯 [CLAIM] @DevOpsEngineerBot

📋 Task: Creare INFRASTRUCTURE_TASKBOARD.json
📝 Status: STARTED
⏱️ ETA: 30 minute

@Andrei - Am primit task-ul T001 și încep lucrul
```

### Exemplu 2: DONE Task
```
✅ [DONE] @DevOpsEngineerBot

📋 Task: Creare INFRASTRUCTURE_TASKBOARD.json
📤 Output: 
- Fișier creat: /workspace/shared/tasks/INFRASTRUCTURE_TASKBOARD.json
- Structură cu secțiunile: docker, ci-cd, monitoring, deployment
- Include template task-uri

📋 Next: Task-uri de infrastructură pot fi adăugate acolo

@Andrei - Task finalizat și gata de review
```

### Exemplu 3: Blocaj
```
⚠️ [BLOCKED] @BuilderCoreBot

📋 Task: API V34 Backend
📝 Status: BLOCKED
❌ Problema: Nu am acces la baza de date PostgreSQL
🔧 Soluție propusă: Necesit credentials sau configurare

@Andrei - Am nevoie de ajutor să continui
```

---

## ⚠️ Reguli Importante:

1. **Comunicare DIRECTĂ** - Nu folosi grupul, scrie direct lui Andrei
2. **CLAIM înainte de lucru** - Nu lucra fără să notifici
3. **DONE cu output clar** - Specifică exact ce ai livrat (path-uri, funcționalități)
4. **Menționează @Andrei** - În fiecare mesaj important
5. **Respectă dependențele** - Nu începe dacă depinde de task nefinalizat
6. **Ești blocat?** - Notifică IMEDIAT, nu aștepta

---

## 📞 Contact:

- **Andrei (Product Owner):** Telegram ID 310970306
- **Team-Manager:** Coordonator, citește taskboard și distribuie

---

**Ultimă actualizare:** 2026-04-06
**Versiune protocol:** 2.0 (Comunicare Directă)
