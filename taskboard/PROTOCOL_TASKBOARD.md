# 📋 PROTOCOL TASKBOARD - Reguli pentru Toată Echipa

## 🎯 SCOP
Acest document definește **regulile de aur** pentru cum lucrează toți agenții cu taskboard-ul. Fiecare agent trebuie să citească și să respecte acest protocol.

---

## 📁 LOCAȚIA TASKBOARD-ULUI

**UN SINGUR FIȘIER** pentru toată echipa:
```
/workspace/shared/taskboard/data.json
```

⚠️ **IMPORTANT:** Toți agenții citesc și scriu în ACELAȘI fișier. Nu creați copii locale!

---

## 🔄 CICLUL DE VIAȚĂ AL UNUI TASK

### **Task-uri de Proiect (create de Product-Architect):**
```
    ┌──────────┐
    │   todo   │ ← Primești task-ul, ești assignat
    └────┬─────┘
         │ Când începi să lucrezi
         ▼
    ┌──────────────┐
    │ in_progress  │ ← Lucrezi activ la task
    └──────┬───────┘
           │ Când termini
           ▼
    ┌──────────┐
    │   done   │ ← Task complet, livrat, testat
    └──────────┘
```

### **Bug-uri (create de orice agent):**
```
    ┌──────────┐
    │  inbox   │ ← Bug raportat, NEASIGNAT, așteaptă triaj
    └────┬─────┘
         │ Product-Architect îl assign-ează
         ▼
    ┌──────────┐
    │   todo   │ ← Assignat, agentul începe fix-ul
    └────┬─────┘
         │ Când începi să lucrezi
         ▼
    ┌──────────────┐
    │ in_progress  │ ← Lucrezi activ la fix
    └──────┬───────┘
           │ Când termini fix-ul
           ▼
    ┌──────────┐
    │   done   │ ← Bug fixat, testat, funcționează
    └──────────┘
```

**Statusuri posibile:**
| Status | Când se folosește |
|--------|-------------------|
| `inbox` | **BUG-URI** - raportat, neasignat, așteaptă triaj de Product-Architect |
| `todo` | Task assignat, dar NU ai început încă |
| `in_progress` | Lucrezi ACTIV la task acum |
| `review` | Terminat, așteaptă review de la alt agent |
| `done` | **COMPLET terminat** - cod livrat, testat, funcțional |

---

## ✅ PROTOCOL PAS CU PAS (Pentru fiecare agent)

### **PASUL 1: CITEȘTE TASKBOARD-UL**
```bash
# Verifică ce task-uri ai
python3 -c "
import json
with open('/workspace/shared/taskboard/data.json') as f:
    data = json.load(f)
proj = data['projects']['PROJ-002']
for t in proj['tasks']:
    if t['assignee'] == 'NUMELE-TĂU' and t['status'] == 'todo':
        print(f'Task: {t[\"id\"]} - {t[\"title\"]}')
"
```

### **PASUL 2: CÂND ÎNCEPI SĂ LUCREZI**
1. Deschide `/workspace/shared/taskboard/data.json`
2. Găsește task-ul tău
3. Schimbă `"status": "todo"` → `"status": "in_progress"`
4. Adaugă `"updated_at": "2026-04-21T10:00:00Z"` (timpul actual UTC)
5. **Salvează fișierul imediat**

### **PASUL 3: CÂND LUCREZI**
- Lucrezi în directorul proiectului (NU în taskboard)
- Taskboard-ul e doar pentru tracking status

### **PASUL 4: CÂND TERMINI**
1. Deschide `/workspace/shared/taskboard/data.json`
2. Găsește task-ul tău
3. Schimbă `"status": "in_progress"` → `"status": "done"`
4. Adaugă `"updated_at": "2026-04-21T12:00:00Z"` (timpul actual UTC)
5. **Salvează fișierul imediat**
6. **(OPȚIONAL)** Anunță-l pe Andrei că ai terminat

---

## 📋 RESPONSABILITĂȚI PER ROL

### 🎯 **Product-Architect (Eu)**
- **Crează** task-uri noi de proiect în taskboard
- **Assign-ează** task-uri de proiect către agenți (status `todo`)
- **TRIAZĂ** bug-uri din inbox (schimbă `inbox` → `todo` + assign)
- **Coordonează** ordinea de lucru
- **Verifică** progresul zilnic
- **Updatează** statusul meu când lucrez

### 🔬 **Specialists-All**
- Primește task-uri de **research**
- Când termină research-ul → **done**
- Livrează documentație în `/docs/research/`

### 🎨 **Frontend-Architect**
- Primește task-uri de **design**
- Livrează mockups, design system, specificații
- Când termină design-ul → **done**

### ⚙️ **Backend-Architect**
- Primește task-uri de **API/backend**
- Livrează cod Express, endpoints, DB models
- Când termină codul → **done**

### 🛠️ **Builder-Modules**
- Primește task-uri de **frontend development**
- Așteaptă design-ul să fie **done** înainte să înceapă
- Livrează cod React, componente, pagini
- Când termină codul → **done**
- **Push pe GitHub** după fiecare task

### 🚀 **Operations-All**
- Primește task-uri de **DevOps/deploy**
- Așteaptă codul să fie gata înainte să deployeze
- Livrează config Nginx/SSL/PM2
- Când termină deploy-ul → **done**

### 👁️ **Reviewer-All**
- Primește task-uri de **QA/testing**
- Așteaptă ca TOATE task-urile de dev să fie **done**
- Testează end-to-end
- **Raportează bug-uri** în taskboard (status `inbox`)
- Când termină testarea → **done**

---

## ⚠️ REGULI DE AUR

### 1. **NICIODATĂ nu ștergi task-uri**
- Doar schimbi status: `todo` → `in_progress` → `done`
- Dacă task-ul e deprecated, adaugă `[DEPRECATED]` în titlu

### 2. **SALVEAZĂ imediat după modificare**
- Nu lăsa fișierul deschis fără să salvezi
- Alți agenți citesc același fișier

### 3. **Task-uri noi**
- **Task-uri de proiect:** Doar Product-Architect creează task-uri noi de proiect (status `todo`, cu assignee)
- **Bug-uri:** ORICE agent poate crea task-uri de tip "bug" (status **`inbox`**, **fără assignee**)

### 4. **Citești înainte să scrii**
- Verifică taskboard-ul înainte să începi orice
- Vezi ce status au task-urile tale

### 5. **Actualizează memoria ta (MEMORY.md)**
- Când termini un task, notează în MEMORY.md ce ai făcut
- Creează fișier zilnic `memory/YYYY-MM-DD.md`

### 6. **Push pe GitHub după fiecare task**
- Codul livrat trebuie să ajungă pe GitHub
- Branch naming: `feature/TASK-ID`

---

## 🐛 CUM RAPORTEZI UN BUG (ÎN TASKBOARD - STATUS INBOX)

### **REGULA DE AUR: Bug-urile intră în INBOX, nu direct în TODO!**

### **Cine creează bug-task-ul?**
- **ORICE agent** care găsește un bug
- **Reviewer-All** în mod special (rol principal de QA)

### **Status bug-ului: INBOX (nu todo!)**
- Când creezi un bug, pune **`"status": "inbox"`**
- **Nu pune assignee** - lasă `"assignee": null` sau `""`
- Product-Architect îl va assigna mai târziu

### **Cum creezi un task de bug:**

#### **PASUL 1: Adaugă task nou în data.json cu status INBOX**

```json
{
  "id": "BUG-003",
  "title": "[BUG] Landing Page - Eroare la încărcare imaginilor",
  "description": "BUG găsit în task-ul DESIGN-001:\n\nEroare:\n```\nFailed to load resource: net::ERR_CONNECTION_REFUSED\nhttps://rotiseriemoinesti.manifestit.dev/api/products\n```\n\nCum reproduce:\n1. Deschide https://rotiseriemoinesti.manifestit.dev/\n2. Scroll la secțiunea Meniu\n3. Imaginile produselor nu se încarcă\n\nRoot cause suspectat: API-ul nu răspunde pe /api/products",
  "type": "bug",
  "priority": "high",
  "assignee": null,
  "status": "inbox",
  "related_task": "DEV-005",
  "found_by": "reviewer-all",
  "requirements": [
    "Fix endpoint /api/products",
    "Verificare CORS",
    "Testare în browser"
  ],
  "acceptance_criteria": [
    "Imaginile se încarcă corect",
    "API returnează lista produse",
    "0 erori în console"
  ],
  "created_by": "reviewer-all",
  "created_at": "2026-04-21T10:00:00Z",
  "updated_at": "2026-04-21T10:00:00Z"
}
```

#### **PASUL 2: Salvează fișierul**
```bash
# Salvează data.json imediat după ce adaugi bug-ul
```

#### **PASUL 3: Anunță Product-Architect**
- Trimite mesaj pe Telegram către Product-Architect
- Exemplu: "@ProductArchitectbot Am găsit un bug nou: BUG-003 în inbox"
- **NU** trimite direct către agentul care crezi că trebuie să fixeze

---

### **Product-Architect triază bug-ul (din INBOX în TODO):**

```
INBOX → Product-Architect verifică → TODO (cu assignee)
```

**Product-Architect:**
1. Citește bug-ul din inbox
2. Decide prioritatea (high/medium/low)
3. Decide cine fixează (assignee)
4. Schimbă `"status": "inbox"` → `"status": "todo"`
5. Adaugă `"assignee": "nume-agent"`
6. Salvează fișierul
7. Anunță agentul assignat

---

### **Convenții pentru ID-uri de bug:**
| Format | Exemplu | Când se folosește |
|--------|---------|-------------------|
| `BUG-XXX` | BUG-001, BUG-002 | Bug-uri generale |
| `FIX-XXX` | FIX-001, FIX-002 | Fix-uri rapide (deprecated) |

### **Cine fixează bug-ul? (decide Product-Architect)**
| Tip Bug | Assignat către |
|---------|----------------|
| Eroare API/Backend | Backend-Architect |
| Eroare UI/Design | Frontend-Architect |
| Eroare React/Componente | Builder-Modules |
| Eroare Deploy/Server | Operations-All |
| Eroare Generală | Agentul care a creat codul cu bug |

### **Cum marchezi bug-ul ca rezolvat:**

**Cel care a fixat bug-ul:**
1. Deschide `data.json`
2. Schimbă `"status": "in_progress"` → `"status": "done"`
3. Adaugă în description: `"

[REZOLVAT 2026-04-21] Fix aplicat de Builder-Modules. Commit: abc123"`
4. Salvează fișierul

**Cel care a verificat bug-ul (QA):**
1. Testează din nou funcționalitatea
2. Confirmă că bug-ul e rezolvat
3. Dacă NU e rezolvat → redeschide bug-ul (`"status": "todo"`)

---

### **Exemplu complet flow bug (INBOX):**

```
1. Reviewer-All testează site-ul
2. Găsește eroare în Landing Page
3. Creează BUG-003 în data.json:
   - id: "BUG-003"
   - title: "[BUG] Landing Page - Eroare imagini"
   - assignee: null (fără assignee!)
   - status: "inbox" (NU "todo"!)
4. Salvează data.json
5. Trimite mesaj: "@ProductArchitectbot BUG-003 în inbox!"

6. Product-Architect citește BUG-003
7. Decide: e bug de backend
8. Updatează în data.json:
   - assignee: "backend-architect"
   - status: "todo"
9. Salvează data.json
10. Trimite mesaj: "@BackendArchitectbot BUG-003 te așteaptă în taskboard!"

11. Backend-Architect primește mesaj
12. Citește BUG-003 din data.json
13. Începe fix-ul → schimbă status în "in_progress"
14. Fixează bug-ul → schimbă status în "done"
15. Reviewer-All verifică → confirmă rezolvat ✅
```

---

## 📊 DASHBOARD / INBOX VIEW

### **Product-Architect verifică inbox-ul zilnic:**
```bash
# Script pentru a vedea bug-uri în inbox
python3 -c "
import json
with open('/workspace/shared/taskboard/data.json') as f:
    data = json.load(f)
proj = data['projects']['PROJ-002']
inbox = [t for t in proj['tasks'] if t['status'] == 'inbox']
print(f'BUG-URI ÎN INBOX: {len(inbox)}')
for t in inbox:
    print(f'  {t[\"id\"]}: {t[\"title\"][:50]} (găsit de {t.get(\"found_by\",\"?\")})')
"
```

### **Fiecare agent verifică task-urile lui:**
```bash
# Vezi task-urile tale în todo
python3 -c "
import json
with open('/workspace/shared/taskboard/data.json') as f:
    data = json.load(f)
proj = data['projects']['PROJ-002']
for t in proj['tasks']:
    if t.get('assignee') == 'NUMELE-TĂU' and t['status'] == 'todo':
        print(f'Task: {t[\"id\"]} - {t[\"title\"]}')
"
```

---

## 🚨 CE FACI DACĂ EȘTI BLOCAT

1. **Verifică** taskboard-ul - poate alt task trebuie terminat înainte
2. **Citește** documentația proiectului în `.project-brain/`
3. **Întreabă** Product-Architect pe Telegram
4. **NU** stai blocat fără să anunți

---

## 📝 EXEMPLU COMPLET (Builder-Modules)

```
09:00 - Citesc taskboard-ul
        Văd: DEV-005 → todo → Landing Page Premium

09:05 - Încep să lucrez
        Modific în data.json: "status": "in_progress"
        Salvez fișierul

10:00 - Lucrez la cod în /frontend/landing/

14:00 - Termin codul
        Testez local → funcționează

14:15 - Updatez taskboard
        Modific în data.json: "status": "done"
        Salvez fișierul

14:20 - Push pe GitHub
        git add .
        git commit -m "[DEV-005] Landing Page Premium - Builder-Modules"
        git push origin feature/DEV-005

14:30 - Updatez memoria
        Scriu în memory/2026-04-21.md ce am făcut
```

---

## 🐛 EXEMPLU COMPLET (Reviewer-All raportează bug)

```
10:00 - Testez Landing Page
        Găsesc eroare: imaginile nu se încarcă

10:05 - Creez BUG-003 în data.json:
        {
          "id": "BUG-003",
          "title": "[BUG] Imagini nu se încarcă",
          "status": "inbox",        ← INBOX, nu todo!
          "assignee": null,          ← FĂRĂ assignee!
          "found_by": "reviewer-all",
          ...
        }

10:06 - Salvez data.json

10:07 - Trimit mesaj:
        "@ProductArchitectbot BUG-003 în inbox!"

---

10:30 - Product-Architect triază BUG-003
        Schimbă: "status": "todo"
        Adaugă: "assignee": "backend-architect"
        Salvează data.json

10:35 - Product-Architect trimite:
        "@BackendArchitectbot BUG-003 te așteaptă!"
```

---

## 🎯 KPI-urile Echipei

| Metric | Țintă |
|--------|-------|
| Bug-uri în inbox (netriate) | < 3 zile |
| Task-uri terminate la timp | 90%+ |
| Bug-uri raportate post-livare | < 5% |
| Update-uri taskboard | Immediat |
| Push GitHub după task | 100% |

---

## 📞 ESCALATION

| Problemă | Cine contactezi |
|----------|----------------|
| Task unclear | Product-Architect |
| Blocked de alt task | Product-Architect |
| Bug în codul altuia | **Product-Architect** (trimite în inbox) |
| Eroare server | Operations-All |
| Eroare API | Backend-Architect |
| Eroare UI | Frontend-Architect |

---

## ✅ CHECKLIST ZILNIC (Pentru fiecare agent)

- [ ] Am citit taskboard-ul azi?
- [ ] Am task-uri în `todo`?
- [ ] Am început task-ul și am pus `in_progress`?
- [ ] Am terminat și am pus `done`?
- [ ] Am făcut push pe GitHub?
- [ ] Am updatat memoria (MEMORY.md)?

### **Pentru Reviewer-All:**
- [ ] Am testat funcționalitățile?
- [ ] Am raportat bug-uri în **inbox**?
- [ ] Am anunțat Product-Architect despre bug-uri noi?

### **Pentru Product-Architect:**
- [ ] Am verificat inbox-ul de bug-uri?
- [ ] Am triat bug-urile (inbox → todo + assign)?
- [ ] Am verificat progresul echipei?

---

*Protocol actualizat: 2026-04-21*
*Responsabil: Product-Architect*
