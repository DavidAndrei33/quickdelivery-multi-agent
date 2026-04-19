# 🎮 GHID DE UTILIZARE - Comunicare cu Agenții

## 🤖 Cum Să Vorbești cu Fiecare Agent

---

## 🎯 Product-Architect

**Canal:** @ProductArchitectbot

### Cum să îi ceri redesign Taskboard:

```
Salut Product-Architect!

Am primit feedback de la client (Andrei) că Taskboard-ul actual 
arată "invechit și urat". Vrea ceva modern, ca Linear.app.

**TASK-005** este asignat ție:
- Redesign UI/UX complet
- Stil: SaaS enterprise premium
- Inspirație: Linear.app, Notion
- Deadline: 7 zile

Detalii complete în:
/workspace/shared/.project-state/tasks/TASK-005.json

Te rog să:
1. Citești brief-ul de design
2. Creezi wireframes în Figma
3. Prezinți 2-3 concepte
4. Aștepți feedback

Mulțumesc! 🚀
```

---

## 🎨 Frontend-Architect

**Canal:** @FrontendArchitectbot

### Cum să îi ceri review:

```
Salut Frontend-Architect!

Product-Architect a terminat design-ul pentru TASK-005 
(Redesign Taskboard).

Te rog să faci review pe:
- Implementabilitate design-ului
- Component architecture
- Performance considerations
- Responsive breakpoints

Figma link: [aici]
Deadline review: 24 ore

Mulțumesc! 👁️
```

---

## 🛠️ Builder-Modules

**Canal:** @BuilderModulesBot

### Cum să îi asignezi implementarea:

```
Salut Builder-Modules!

TASK-005 a fost aprobat de design.
Ești asignat pentru implementare.

**Stack:**
- React 18 + Next.js 14
- Tailwind CSS
- Framer Motion
- @dnd-kit/core

**Structură:**
/workspace/shared/taskboard-v2/

**Acceptance Criteria:**
- [ ] All Figma designs implemented
- [ ] Drag & drop functional
- [ ] Dark/Light mode
- [ ] Mobile responsive
- [ ] Tests passing

Deadline: 5 zile
Mulțumesc! 🚀
```

---

## 👁️ Reviewer-All

**Canal:** @ReviewerAllbot

### Cum să ceri code review:

```
Salut Reviewer-All!

Builder-Modules a terminat TASK-005.
Te rog să faci code review.

**Focus:**
- Code quality & patterns
- Security audit
- Performance check
- Accessibility (WCAG)

**PR Location:**
/workspace/shared/taskboard-v2/

Deadline: 24 ore
Mulțumesc! 🎯
```

---

## 🚀 Operations-All

**Canal:** @operatioooooooonsaaabot

### Cum să ceri deploy:

```
Salut Operations-All!

TASK-005 a trecut de review.
Te rog să faci deploy.

**Environment:** Production
**Domain:** taskboard.manifestit.dev
**Build:** /workspace/shared/taskboard-v2/

**Checklist:**
- [ ] Build successful
- [ ] Tests passing
- [ ] SSL configured
- [ ] Monitoring setup

Mulțumesc! 🚀
```

---

## 🔬 Specialists-All

**Canal:** @Specialistibot

### Cum să ceri research:

```
Salut Specialists-All!

Am nevoie de research pentru tehnologii de real-time 
updates în Taskboard.

**Întrebări:**
1. WebSockets vs Server-Sent Events vs Long Polling?
2. Cele mai bune librării pentru Kanban drag-drop?
3. Soluții de state management pentru real-time?

**Deliverable:**
Report în /workspace/shared/research/TASK-005-tech.md

Deadline: 2 zile
Mulțumesc! 🔬
```

---

## 📋 WORKFLOW URI PENTRU FIECARE CAZ

### Cazul 1: Feature Nou
```
1. Andrei → Manifest: "Vreau feature X"
2. Manifest → Product-Architect: "Creează spec"
3. Product-Architect → Andrei: "Review spec"
4. Andrei → Manifest: "Approve spec"
5. Manifest → Builder-Modules: "Implementează"
6. Builder-Modules → Reviewer-All: "Review"
7. Reviewer-All → Manifest: "Approve/Reject"
8. Manifest → Operations-All: "Deploy"
9. Operations-All → Andrei: "Live on production"
```

### Cazul 2: Bug Fix
```
1. Andrei → Manifest: "Bug la login"
2. Manifest → Builder-Modules: "Hotfix"
3. Builder-Modules → Reviewer-All: "Rapid review"
4. Reviewer-All → Manifest: "Approve"
5. Manifest → Operations-All: "Deploy urgent"
6. Operations-All → Andrei: "Fix deployed"
```

### Cazul 3: Arhitectural Decision
```
1. Andrei → Product-Architect: "Ce DB să folosim?"
2. Product-Architect → Specialists-All: "Research"
3. Specialists-All → Product-Architect: "Report"
4. Product-Architect → Backend-Architect: "Decizie?"
5. Backend-Architect → Manifest: "ADR creat"
6. Manifest → Andrei: "Decizie arhitecturală"
```

---

## 🎮 COMENZI RAPIDE (Pentru Andrei)

### Comenzi pe @App_dev99_bot (Manifest):

```
/new-task "Titlu task" [agent] [prioritate]
→ Creează task nou și asignează automat

/assign [task-id] [agent]
→ Reasignează task la alt agent

/status [task-id]
→ Vezi status complet task

/block [task-id] "motiv"
→ Blochează task (dependențe)

/unblock [task-id]
→ Deblochează task

/deploy [project]
→ Declanșează deploy workflow

/review [task-id]
→ Trimite la review

/report
→ Dashboard status proiect

/agents
→ Lista agenți și status
```

---

## 💡 TIPS & BEST PRACTICES

### 1. Comunicare Clară
- ✅ Fii specific: "Vreau butonul verde, nu albastru"
- ✅ Dă context: "Pentru că utilizatorii se plâng de..."
- ✅ Setează deadline-uri realiste
- ❌ Nu spune doar: "Fix this" (fără context)

### 2. Feedback Constructiv
- ✅ "Îmi place direcția, dar poate să fie mai dark?"
- ✅ "Funcționalitatea e bună, dar UI-ul are nevoie de..."
- ❌ "Nu îmi place" (fără explicație)

### 3. Urmărire Progres
- ✅ Verifică Taskboard zilnic
- ✅ Citește updates de la agenți
- ✅ Răspunde la întrebări în 24h
- ✅ Approve/Reject rapid

### 4. Escalare
Dacă un agent e blocat > 24 ore:
1. Întreabă direct pe canalul lui
2. Dacă nu răspunde → spune-mi mie (Manifest)
3. Eu voi reasigna sau escala

---

## 🚀 EXEMPLU COMPLET: TASK-005

### Ziua 1: Kickoff
```
09:00 - Andrei spune: "Taskboard arată urat"
09:05 - Manifest creează TASK-005
09:10 - Manifest asignează la Product-Architect
09:15 - Product-Architect primește notificare
09:30 - Product-Architect confirmă: "Încep research"
```

### Ziua 2-3: Design
```
Product-Architect:
- Creează moodboard
- Research Linear.app, Notion
- Wireframes low-fidelity
- 3 concepte high-fidelity în Figma

14:00 - Update: "Concepte gata pentru review"
```

### Ziua 4: Review Design
```
10:00 - Frontend-Architect review
10:30 - Feedback: "Implementabil, dar ajustezi culorile"
11:00 - Product-Architect update
14:00 - Andrei review: "Concept 2 arată bine!"
```

### Ziua 5: Implementation
```
09:00 - Builder-Modules primește task
09:30 - Setup proiect React + Next.js
17:00 - Update: "50% complete, drag & drop funcțional"
```

### Ziua 6: Testing
```
10:00 - Builder-Modules: "Gata pentru review"
11:00 - Reviewer-All code review
14:00 - Bug fixes
16:00 - QA testing
```

### Ziua 7: Deploy
```
10:00 - Operations-All deploy
10:30 - Andrei testează: "Arată fantastic! 🎉"
11:00 - TASK-005 marked as DONE
```

---

## 📞 SUPORT

**Dacă ceva nu funcționează:**
1. Scrie pe canalul agentului respectiv
2. Așteaptă 24 ore
3. Dacă nu răspunde → @App_dev99_bot (Manifest)
4. Eu intervin și rezolv

---

**Ready to start?** 🚀
Spune-mi ce task vrei să creezi!
