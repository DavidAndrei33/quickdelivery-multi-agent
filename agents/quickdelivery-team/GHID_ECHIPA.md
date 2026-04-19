# QuickDelivery Multi-Agent Team - Ghid Complet

## 🎯 Prezentare Generală

Această arhitectură de echipă permite dezvoltarea simultană a tuturor modulelor QuickDelivery cu quality gates la fiecare pas.

## 📁 Structura Directoarelor

```
/workspace/shared/
├── agents/quickdelivery-team/
│   ├── product-architect/         # Decizii produs + specificații
│   ├── frontend-architect/        # Design system + guideline-uri
│   ├── backend-architect/         # API design + arhitectură
│   ├── builders/
│   │   ├── customer/              # Modulul Customer (Next.js)
│   │   ├── admin/                 # Modulul Admin (Next.js)
│   │   ├── rider/                 # Modulul Rider (Next.js)
│   │   ├── store/                 # Modulul Store (Next.js)
│   │   ├── mobile/                # iOS + Android (React Native)
│   │   └── api/                   # Backend API (Node.js)
│   ├── reviewers/
│   │   ├── frontend/              # Code review frontend
│   │   ├── backend/               # Code review backend
│   │   └── security/              # Security audit
│   ├── devops/                    # Deployment + CI/CD
│   └── qa-tester/                 # End-to-end testing
│
└── shared/                        # Artifacte comune
    ├── specs/                     # Specificații feature-uri
    ├── artifacts/                 # Cod sursă, builds
    ├── reviews/                   # Review notes
    ├── decisions/                 # Decizii arhitecturale
    └── deployments/               # Config deploy
```

## 🚀 Cum să Folosești Echipa

### Exemplu 1: Adaugă Feature Nouă (Rating System)

```bash
# 1. Product-Architect definește cerințele
sessions_spawn:
  agent: product-architect
  task: |
    Creează specificație pentru sistemul de rating rideri:
    - Client poate da rating 1-5 stele
    - Comentariu opțional
    - Rider vede media rating-urilor
    - Admin poate modera reviews
    
    Output: /workspace/shared/specs/rating-system-spec.md

# 2. Backend-Architect proiectează API-ul
sessions_spawn:
  agent: backend-architect
  task: |
    Review spec: /workspace/shared/specs/rating-system-spec.md
    
    Creează:
    1. API design în /workspace/shared/specs/rating-api-design.md
    2. DB schema în /workspace/shared/specs/rating-schema.sql
    3. Endpoints: POST /ratings, GET /ratings/:riderId

# 3. Builder-API implementează backend-ul
sessions_spawn:
  agent: builder-api
  task: |
    Implementează API-ul conform:
    - Spec: /workspace/shared/specs/rating-api-design.md
    - Schema: /workspace/shared/specs/rating-schema.sql
    
    Output: /workspace/shared/artifacts/rating-api/
    Include: cod + teste + documentație

# 4. Reviewer-Backend verifică codul
sessions_spawn:
  agent: reviewer-backend
  task: |
    Review code în: /workspace/shared/artifacts/rating-api/
    
    Verifică:
    - Securitate (SQL injection, XSS)
    - Validiere input
    - Error handling
    - Test coverage
    
    Output: /workspace/shared/reviews/rating-api-review.md

# 5. Frontend-Architect proiectează UI
sessions_spawn:
  agent: frontend-architect
  task: |
    Design componente UI pentru rating:
    - Star rating component
    - Review list
    - Review form
    
    Output: /workspace/shared/specs/rating-ui-design.md

# 6. Builder-Customer + Builder-Rider implementează UI
sessions_spawn:
  agent: builder-customer
  task: |
    Implementează UI rating în modulul Customer:
    - Design: /workspace/shared/specs/rating-ui-design.md
    - API: folosește endpoint-urile din review
    
    Output: /workspace/shared/artifacts/rating-ui-customer/

# 7. Reviewer-Frontend verifică UI
sessions_spawn:
  agent: reviewer-frontend
  task: |
    Review implementare UI:
    - /workspace/shared/artifacts/rating-ui-customer/
    
    Verifică: responsive, accesibilitate, consistență design

# 8. DevOps deployează
sessions_spawn:
  agent: devops-quickdelivery
  task: |
    Deploy pe staging:
    1. Aplică migrations DB
    2. Deploy API
    3. Deploy frontend modules
    4. Configurează monitoring
    
    Output: /workspace/shared/deployments/rating-staging.md
```

### Exemplu 2: Creează Aplicație Mobile

```bash
# 1. Frontend-Architect definește strategy mobile
sessions_spawn:
  agent: frontend-architect
  task: |
    Creează strategy pentru mobile apps:
    - Shared components între web și mobile
    - Navigation patterns
    - State management
    
    Output: /workspace/shared/specs/mobile-strategy.md

# 2. Builder-Mobile implementează
sessions_spawn:
  agent: builder-mobile
  task: |
    Creează aplicația mobile pentru Customer:
    - Folosește API-urile existente
    - Strategy: /workspace/shared/specs/mobile-strategy.md
    - Feature parity cu versiunea web
    
    Output: 
    - /workspace/shared/artifacts/mobile/customer-ios/
    - /workspace/shared/artifacts/mobile/customer-android/

# 3. QA-Tester testează
sessions_spawn:
  agent: qa-tester
  task: |
    Testează aplicația mobile:
    - Funcționalitate
    - Performance
    - Battery usage
    - Offline mode
    
    Output: /workspace/shared/reviews/mobile-test-report.md
```

## 🔄 Workflow-uri Standard

### Workflow 1: Bug Fix Rapid
```
1. Tu raportezi bug-ul
2. Orchestrator assignează la builder-ul relevant
3. Builder fixează → commit
4. Reviewer face quick review
5. DevOps deployează hotfix
```

### Workflow 2: Feature Complexă
```
1. Product-Architect: spec + acceptance criteria
2. Backend-Architect: API design
3. Frontend-Architect: UI design
4. Builders: implementare paralelă
5. Reviewers: code review
6. QA: testing
7. DevOps: deploy staging → production
```

### Workflow 3: Refactoring
```
1. Tech Lead (tu sau architect) definește scope
2. Builder implementează
3. Reviewer verifică (fără schimbări funcționale)
4. QA regression testing
5. Deploy gradual
```

## 📝 Templates pentru Tasks

### Template: Feature Request
```
**Feature:** [Nume feature]
**Modul:** [Customer/Admin/Rider/Store/API/Mobile]
**Prioritate:** [High/Medium/Low]
**Deadline:** [Data]

**Descriere:**
[Ce trebuie să facă]

**Acceptance Criteria:**
- [ ] Criteriu 1
- [ ] Criteriu 2
- [ ] Criteriu 3

**Notes:**
[Orice informație suplimentară]

**Output Expected:**
- Codul în: /workspace/shared/artifacts/[feature-name]/
- Specs în: /workspace/shared/specs/[feature-name]-spec.md
```

### Template: Code Review
```
**Task:** Review [feature-name]
**Assignee:** [Reviewer]
**Code Location:** /workspace/shared/artifacts/[feature-name]/

**Checklist:**
- [ ] Code quality
- [ ] Security issues
- [ ] Test coverage
- [ ] Documentation
- [ ] Performance

**Review Output:**
/workspace/shared/reviews/[feature-name]-review.md
```

## 🎨 Identitatea Agenților

Fiecare agent are:
- **Nume unic** (ex: Builder-Customer)
- **Emoji** pentru recunoaștere rapidă (🛒, 🛵, 🏪)
- **Workspace** izolat
- **SOUL.md** cu instrucțiuni specifice rolului
- **Skill-uri** relevante (ex: web-quality-skills pentru frontend)

## ⚡ Comenzi Utile

### Listează toți agenții
```bash
openclaw agents list
```

### Spawnează un agent
```bash
openclaw session spawn builder-customer "Implementează checkout flow"
```

### Verifică statusul task-urilor
```bash
cat /workspace/shared/specs/TASKBOARD.md
```

### Deploy pe staging
```bash
sessions_send devops-quickdelivery "Deploy latest to staging"
```

## 🎯 Progresie Naturală

### Faza 1: Setup (Săptămâna 1)
- Creează toți agenții
- Setup proiect base (monorepo)
- CI/CD pipeline

### Faza 2: MVP (Săptămânile 2-4)
- API de bază
- Customer module (browse + order)
- Rider module (accept + deliver)

### Faza 3: Feature Complete (Săptămânile 5-8)
- Admin dashboard
- Store management
- Payments
- Notifications

### Faza 4: Mobile (Săptămânile 9-12)
- iOS app
- Android app
- Push notifications

### Faza 5: Polish (Săptămânile 13-16)
- Performance optimization
- Security audit
- UI/UX refinement
- Testing complet

## 🔗 Resurse

- **Skill Team Orchestration:** `/root/clawd/skills/agent-team-orchestration/`
- **Exemplu QuickDelivery existent:** `/root/clawd/agents/quickdelivery/`
- **Deployment actual:** Vezi MEMORY.md pentru config Caddy

---

**Vrei să începem cu ceva anume?** 
- Setup agenții în OpenClaw?
- Creează primul feature?
- Setup proiect base?
