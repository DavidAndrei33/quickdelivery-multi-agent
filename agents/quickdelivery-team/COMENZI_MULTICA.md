# Cum să Folosești Echipa QuickDelivery în Multica

## 🎯 Comenzi de Bază

### 1. Listează Toți Agenții
```bash
openclaw agents list
```

### 2. Trimite Mesaj către un Agent
```bash
# Sintaxă:
openclaw session send <agent-id> "mesajul tău aici"

# Exemple:
openclaw session send product-architect "Creează roadmap pentru QuickDelivery v2.0"
openclaw session send builder-customer "Implementează pagina de checkout"
openclaw session send devops-quickdelivery "Deploy pe staging"
```

### 3. Spawnează Task în Background
```bash
openclaw session spawn "task description" --agent <agent-id>
```

## 📋 Workflow-uri Comune

### Workflow 1: Feature Nou (Rating System)

**Pas 1:** Product-Architect creează specificația
```bash
openclaw session send product-architect "Creează specificație pentru rating system:
- Client poate da rating 1-5 stele
- Comentariu opțional
- Rider vede media rating-urilor
- Admin poate modera
Output: /workspace/shared/specs/rating-system-spec.md"
```

**Pas 2:** Backend-Architect proiectează API
```bash
openclaw session send backend-architect "Design API pentru rating system:
Spec: /workspace/shared/specs/rating-system-spec.md
Output: /workspace/shared/specs/rating-api-design.md"
```

**Pas 3:** Builder-API implementează
```bash
openclaw session send builder-api "Implementează rating API conform:
- Design: /workspace/shared/specs/rating-api-design.md
Output: /workspace/shared/artifacts/rating-api/"
```

**Pas 4:** Reviewer-Backend verifică
```bash
openclaw session send reviewer-backend "Review code:
Location: /workspace/shared/artifacts/rating-api/
Output: /workspace/shared/reviews/rating-api-review.md"
```

**Pas 5:** Builder-Customer implementează UI
```bash
openclaw session send builder-customer "Implementează UI rating în modulul Customer
Output: /workspace/shared/artifacts/rating-ui-customer/"
```

**Pas 6:** DevOps deployează
```bash
openclaw session send devops-quickdelivery "Deploy rating feature pe staging"
```

---

## 📁 Structura de Fișiere

```
/workspace/shared/
├── specs/              # Specificații feature-uri
├── artifacts/          # Cod sursă, builds
├── reviews/            # Review notes
├── decisions/          # Decizii arhitecturale
└── deployments/        # Config deploy
```

## 🎨 Identitatea Agenților

Fiecare agent are:
- **Workspace** propriu izolat
- **SOUL.md** cu instrucțiuni specifice
- **Emoji** pentru recunoaștere rapidă

## ⚡ Comenzi Rapide

```bash
# Vezi toți agenții
openclaw agents list | grep -E "(builder|reviewer|architect)"

# Trimite task la builder
openclaw session send builder-customer "Task description"

# Trimite task la reviewer
openclaw session send reviewer-frontend "Review code la locația X"

# Deploy
openclaw session send devops-quickdelivery "Deploy latest"
```

## 📝 Template Task

```
**Task:** [Nume]
**Modul:** [Customer/Admin/Rider/Store/API/Mobile]
**Prioritate:** [High/Medium/Low]

**Descriere:**
[Ce trebuie făcut]

**Acceptance Criteria:**
- [ ] Criteriu 1
- [ ] Criteriu 2

**Output:**
- Cod: /workspace/shared/artifacts/[task-id]/
- Specs: /workspace/shared/specs/[task-id]-spec.md
```

---

**Ești gata să începi!** Ce task vrei să delegi primul? 🚀
