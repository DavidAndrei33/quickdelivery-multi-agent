# 📊 CONTEXT PENTRU DASHBOARD AGENȚI

## 1. 👥 ECHIPA DE AGENȚI (9 membri)

| ID Agent | Nume | Emoji | Telegram | Rol |
|----------|------|-------|----------|-----|
| product-architect | Product-Architect | 🎯 | @ProductArchitectbot | Orchestrare, Product Manager |
| backend-architect | Backend-Architect | ⚙️ | @BackendArchitectbot | API, Database |
| frontend-architect | Frontend-Architect | 🎨 | @FrontendArchitectbot | UI/UX Design |
| builder-modules | Builder-Modules | 🛠️ | @BuilderModulesBot | React Frontend Dev |
| builder-mobile | Builder-Mobile | 📱 | @BuilderMobilebot | iOS/Android (opțional) |
| reviewer-all | Reviewer-All | 👁️ | @ReviewerAllbot | Code Review, QA |
| operations-all | Operations-All | 🚀 | @operatioooooooonsaaabot | DevOps, Deploy |
| specialists-all | Specialists-All | 🔬 | @Specialistibot | Research, Analysis |

**Observație:** Al 9-lea agent este **Manifest (@App_dev99_bot)** - Orchestrator principal care coordonează tot, dar nu apare în taskboard ca assignee.

---

## 2. 📁 LOCAȚIA TASKBOARD-ULUI

**Fișier principal:**
```
/workspace/shared/taskboard/data.json
```

**Structură fișier:**
- `version`: "4.0.0"
- `agents`: Obiect cu toți agenții (name, emoji, telegram)
- `projects`: Obiect cu proiectele (fiecare proiect are array `tasks`)
- Fiecare task are: `id`, `title`, `description`, `type`, `priority`, `assignee`, `status`, `requirements`, `acceptance_criteria`, `created_by`, `created_at`, `updated_at`
- `columns` per proiect: `["inbox", "todo", "in_progress", "review", "done"]`

---

## 3. 📂 PROIECTE ACTIVE

### PROJ-001: QuickDelivery
- **Status:** active (dar NU mai e prioritare)
- **Tasks:** 2 (TASK-001, TASK-002) - ambele în inbox
- **Descriere:** Food delivery platform (proiect anterior)

### PROJ-002: Rotiserie & Pizza Moinești ⭐ PRIORITAR
- **Status:** active
- **Tasks:** 43 total
- **Descriere:** Platformă comenzi online pentru rotiserie - 3 module: Landing Page, Modul Magazin (bucătărie), Modul Admin

**Module Rotiserie:**
1. **Landing Page** - clienți (meniu, coș, checkout Stripe)
2. **Modul Magazin** - bucătărie (comenzi în timp real, status)
3. **Modul Admin** - management (produse, prețuri, rapoarte)

---

## 4. 📋 STATUS TASK-URI ROTISERIE (PROJ-002)

### Task-uri Originale (10) - marcate done (doar setup, nu implementare efectivă):
| ID | Titlu | Assignee | Status |
|----|-------|----------|--------|
| TASK-001 | Research Rapid | specialists-all | ✅ done |
| TASK-002 | Kickoff | product-architect | ✅ done |
| TASK-003 | Design UI/UX Simplu | frontend-architect | ✅ done |
| TASK-004 | API Simplu | backend-architect | ✅ done |
| TASK-005 | Setup Hosting | operations-all | ✅ done |
| TASK-006 | Landing Page Dev | builder-modules | ✅ done |
| TASK-007 | Pagina Magazin Dev | builder-modules | ✅ done |
| TASK-008 | Pagina Admin Dev | builder-modules | ✅ done |
| TASK-009 | Integrare Stripe | builder-modules | ✅ done |
| TASK-010 | Testare | reviewer-all | ✅ done |

### Task-uri TEST Setup Memorie (8):
| ID | Assignee | Status |
|----|----------|--------|
| TEST-001 | product-architect | ✅ done |
| TEST-002 | backend-architect | ✅ done |
| TEST-003 | frontend-architect | ✅ done |
| TEST-004 | builder-modules | ✅ done |
| TEST-005 | builder-mobile | ✅ done |
| TEST-006 | reviewer-all | ✅ done |
| TEST-007 | operations-all | ✅ done |
| TEST-008 | specialists-all | ✅ done |

### Task-uri Principale Noi (17) - AȘTEAPTĂ IMPLEMENTARE:
**Design:**
| ID | Titlu | Assignee | Status |
|----|-------|----------|--------|
| DESIGN-001 | Design Landing Page | frontend-architect | 📋 todo |
| DESIGN-002 | Design Pagină Magazin | frontend-architect | 📋 todo |
| DESIGN-003 | Design Pagină Admin | frontend-architect | 📋 todo |
| DESIGN-004 | Design System | frontend-architect | 📋 todo |

**Backend:**
| ID | Titlu | Assignee | Status |
|----|-------|----------|--------|
| API-001 | Setup Express + MongoDB | backend-architect | 📋 todo |
| API-002 | API Endpoints | backend-architect | 📋 todo |
| API-003 | Integrare Stripe | backend-architect | 📋 todo |
| API-004 | Autentificare JWT | backend-architect | 📋 todo |

**Frontend Dev:**
| ID | Titlu | Assignee | Status |
|----|-------|----------|--------|
| DEV-001 | Landing Page React | builder-modules | 📋 todo |
| DEV-002 | Pagină Magazin | builder-modules | 📋 todo |
| DEV-003 | Pagină Admin | builder-modules | 📋 todo |
| DEV-004 | Stripe în Frontend | builder-modules | 📋 todo |

**DevOps:**
| ID | Titlu | Assignee | Status |
|----|-------|----------|--------|
| OPS-001 | Deploy Frontend Vercel | operations-all | 📋 todo |
| OPS-002 | Deploy Backend Render | operations-all | 📋 todo |
| OPS-003 | MongoDB Atlas | operations-all | 📋 todo |
| OPS-004 | Config Environment | operations-all | 📋 todo |

**QA:**
| ID | Titlu | Assignee | Status |
|----|-------|----------|--------|
| QA-001 | Testare End-to-End | reviewer-all | 📋 todo |

### Task-uri GitHub (8):
| ID | Assignee | Status |
|----|----------|--------|
| GITHUB-001 | frontend-architect | 📋 todo |
| GITHUB-002 | backend-architect | ✅ done |
| GITHUB-003 | builder-modules | ✅ done |
| GITHUB-004 | operations-all | 📋 todo |
| GITHUB-005 | reviewer-all | ✅ done |
| GITHUB-006 | specialists-all | ✅ done |
| GITHUB-007 | builder-mobile | ✅ done |
| GITHUB-008 | product-architect | 📋 todo |

---

## 5. 🎯 CE VREAU DE LA DASHBOARD

### Funcționalități obligatorii:
1. **Vizualizare task-uri pe proiect** - să vad toate task-urile din PROJ-002 (Rotiserie)
2. **Vizualizare pe status** - coloane: inbox / todo / in_progress / review / done
3. **Vizualizare pe agent** - ce task-uri are fiecare agent
4. **Vizualizare pe prioritate** - high / medium / low
5. **Progres proiect** - câte task-uri done vs total
6. **Progres per agent** - câte task-uri a terminat fiecare
7. **Task-uri blocante / dependențe** - ce task blochează altele

### Format preferat:
- **HTML static** (simplu, fără backend) sau
- **Markdown tabelar** sau
- **Terminal/CLI dashboard** (afișare în consolă)

### Sursa de date:
- Citește direct din `/workspace/shared/taskboard/data.json`
- Parsează JSON și afișează frumos
- **NU modifică** fișierul - doar read-only

### Update:
- Dashboard-ul să poată fi regenerat oricând (re-citește JSON-ul)
- Eventual un script `generate-dashboard.js` sau `dashboard.html`

---

## 6. 📂 ALTE FIȘIERE IMPORTANTE

- **Structură proiect:** `/workspace/shared/.project-brain/projects/rotiserie-pizza-moinesti/LOCATII_SI_STRUCTURA.md`
- **Documentație proiect:** `/workspace/shared/.project-brain/projects/rotiserie-pizza-moinesti/project.json`
- **Research:** `/workspace/shared/.project-brain/projects/rotiserie-pizza-moinesti/research/food-delivery-research.md`
- **GitHub:** `/workspace/shared/.project-brain/projects/rotiserie-pizza-moinesti/GITHUB.md`

---

## 7. 📝 INSTRUCȚIUNI PENTRU AGENTUL DASHBOARD

1. Citește `/workspace/shared/taskboard/data.json`
2. Parsează proiectele și task-urile
3. Generează un dashboard vizual (HTML preferat) care să arate:
   - Task-uri PROJ-002 grupate pe status (Kanban-style)
   - Task-uri per agent
   - Progres proiect (procent done)
   - Task-uri cu prioritate high (evidențiate)
4. Salvează dashboard-ul în `/workspace/shared/taskboard/dashboard.html` (sau similar)
5. Confirmă când e gata!

---

*Context generat de Product-Architect pentru noul agent Dashboard*
*Data: 2026-04-20*
