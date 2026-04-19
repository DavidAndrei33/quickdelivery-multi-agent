# 🍕 QuickDelivery Food Platform - Project Definition

## Project Overview
**Codename:** QuickDelivery  
**Type:** Multi-module Food Delivery Platform  
**Issue ID:** 7553d1b3-09fb-4a99-8a91-ad0786ef6b1b  
**Priority:** High  
**Status:** Planning Phase

---

## 📐 System Architecture

### 1. CUSTOMER MODULE (Frontend)
**Purpose:** Interfața pentru clienți să vizualizeze restaurante și să plaseze comenzi

**Features:**
- Browse restaurante după categorie/locație
- Vizualizare meniu cu poze și prețuri
- Coș de cumpărături persistent
- Checkout cu multiple opțiuni plată
- Tracking comenzi în timp real
- Istoric comenzi și re-order
- Recenzii și rating-uri
- Autentificare/Înregistrare utilizatori

**Tech Stack:**
- React/Next.js + TypeScript
- Tailwind CSS pentru UI
- Redux/Zustand pentru state management
- WebSocket pentru notificări realtime
- PWA pentru experiență mobilă

**Routes:**
- `/` - Homepage cu restaurante populare
- `/restaurants` - Listare restaurante
- `/restaurant/:id` - Detalii restaurant + meniu
- `/cart` - Coș de cumpărături
- `/checkout` - Finalizare comandă
- `/orders` - Istoric comenzi
- `/track/:orderId` - Urmărire comandă activă
- `/profile` - Profil utilizator

---

### 2. ADMIN MODULE (Frontend + Backend)
**Purpose:** Panou de administrare pentru managementul platformei

**Features:**
- Dashboard cu statistici (comenzi, venituri, utilizatori)
- Management restaurante (CRUD, aprobări)
- Management utilizatori (clienți, curieri)
- Management categorii produse
- Rapoarte și analytics
- Configurări platformă (taxe, comisioane)
- Management conținut (banners, promoții)
- Suport clienți (tickets, dispute)

**Tech Stack:**
- React/Next.js + TypeScript
- Tailwind CSS + Headless UI
- Recharts pentru grafice
- React Table pentru date
- Role-based access control (RBAC)

**Routes:**
- `/admin` - Dashboard principal
- `/admin/restaurants` - Management restaurante
- `/admin/users` - Management utilizatori
- `/admin/orders` - Toate comenzile
- `/admin/categories` - Categorii produse
- `/admin/reports` - Rapoarte financiare
- `/admin/settings` - Setări platformă
- `/admin/support` - Suport clienți

---

### 3. RESTAURANT MODULE (Frontend + Backend)
**Purpose:** Interfață pentru restaurante să gestioneze comenzile și meniul

**Features:**
- Dashboard cu comenzi active
- Management meniu (adăugare/editare/ștergere produse)
- Gestionare comenzi (acceptare, pregătire, ready-for-pickup)
- Program de funcționare
- Setări livrare (zonă, timp, taxe)
- Rapoarte vânzări
- Notificări realtime pentru comenzi noi
- Management stoc (opțional)

**Tech Stack:**
- React/Next.js + TypeScript
- Tailwind CSS
- WebSocket pentru notificări comenzi
- Form management (React Hook Form)

**Routes:**
- `/store` - Dashboard comenzi
- `/store/menu` - Management meniu
- `/store/orders` - Listă comenzi
- `/store/orders/:id` - Detalii comandă
- `/store/profile` - Profil restaurant
- `/store/settings` - Setări
- `/store/reports` - Rapoarte vânzări

---

## 🏗️ Backend Architecture

### API Layer (Node.js/Express sau Fastify)
```
/api/v1/
├── /auth           # Autentificare JWT
├── /users          # Management utilizatori
├── /restaurants    # CRUD restaurante
├── /menu           # Management meniu
├── /orders         # Comenzi
├── /categories     # Categorii
├── /payments       # Procesare plăți
├── /notifications  # Notificări push/WebSocket
└── /admin          - Rute administrative
```

### Database Schema (PostgreSQL)
**Tabele principale:**
- `users` - Clienți, admini, curieri
- `restaurants` - Informații restaurante
- `categories` - Categorii mâncare
- `menu_items` - Produse din meniu
- `orders` - Comenzi
- `order_items` - Itemi din comandă
- `reviews` - Recenzii
- `payments` - Tranzacții

### Real-time Layer
- WebSocket server pentru notificări instant
- Redis pentru pub/sub între servicii

### Infrastructure
- Docker + Docker Compose
- Nginx reverse proxy
- PostgreSQL database
- Redis cache/sessions
- MinIO/S3 pentru stocare imagini

---

## 🎯 Task Allocation by Agent

### Agent-1: Architect & Database Designer
**Role:** Builder  
**Task:** Database Schema Design  
**Priority:** CRITICAL  
**Duration:** 2-3 hours  

**Deliverables:**
1. SQL schema complet (`/database/schema.sql`)
2. Migration files (`/database/migrations/`)
3. Seed data pentru testare (`/database/seeds/`)
4. ER diagram (`/docs/er-diagram.png`)
5. Documentație relații (`/docs/database.md`)

**Acceptance Criteria:**
- Toate tabelele definite cu PK, FK, indexuri
- Normalizare 3NF
- Constraints și triggers dacă e necesar
- Seed data pentru 5 restaurante, 20 produse, 3 utilizatori

---

### Agent-2: Backend API Developer
**Role:** Builder  
**Task:** REST API Implementation  
**Priority:** CRITICAL  
**Duration:** 4-6 hours  
**Depends on:** Agent-1 (database schema)

**Deliverables:**
1. API server Node.js/Express (`/backend/`)
2. Authentication middleware (JWT)
3. Route handlers pentru toate entitățile
4. Controllers cu business logic
5. Models/ORM (Prisma sau Sequelize)
6. Validation middleware (Joi/Zod)
7. Error handling global
8. API documentation (Swagger/OpenAPI)

**Endpoints to implement:**
```
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/refresh
GET    /api/v1/restaurants
GET    /api/v1/restaurants/:id
GET    /api/v1/restaurants/:id/menu
POST   /api/v1/orders
GET    /api/v1/orders/:id
PATCH  /api/v1/orders/:id/status
GET    /api/v1/users/profile
PATCH  /api/v1/users/profile
GET    /api/v1/admin/dashboard
```

**Acceptance Criteria:**
- Toate endpoint-urile funcționale
- Testat cu Postman/Thunder Client
- JWT auth funcțional
- Validation pe toate inputurile
- Error responses consistente

---

### Agent-3: Customer Frontend Developer
**Role:** Builder  
**Task:** Customer Module (React App)  
**Priority:** HIGH  
**Duration:** 4-5 hours  
**Depends on:** Agent-2 (API endpoints)

**Deliverables:**
1. React app cu Vite (`/frontend/customer/`)
2. Componente UI (RestaurantCard, MenuItem, Cart, Checkout)
3. State management (Zustand/Redux Toolkit)
4. API integration (Axios/React Query)
5. Routing (React Router)
6. Responsive design (Tailwind)
7. Form handling (React Hook Form)
8. Cart persistence (localStorage)

**Pages:**
- Homepage cu lista restaurante
- Pagină restaurant cu meniu
- Coș de cumpărături
- Checkout flow
- Order tracking
- Profil utilizator

**Acceptance Criteria:**
- Design responsive (mobile-first)
- Toate paginile funcționale
- Integrare API completă
- Error states și loading states
- Cart persistă între sesiuni

---

### Agent-4: Restaurant Dashboard Developer
**Role:** Builder  
**Task:** Restaurant Module (React App)  
**Priority:** HIGH  
**Duration:** 3-4 hours  
**Depends on:** Agent-2 (API endpoints)

**Deliverables:**
1. React app (`/frontend/restaurant/`)
2. Dashboard comenzi active
3. Management meniu (CRUD produse)
4. Order management (accept, prepare, complete)
5. Real-time notifications (WebSocket)
6. Rapoarte vânzări simple
7. Profil restaurant settings

**Pages:**
- Dashboard comenzi
- Management meniu
- Detalii comandă
- Setări restaurant

**Acceptance Criteria:**
- Notificări realtime pentru comenzi noi
- Management meniu complet funcțional
- Workflow comandă (accept → prepare → ready)
- Design optimizat pentru tabletă (bucătărie)

---

### Agent-5: Admin Dashboard Developer
**Role:** Builder  
**Task:** Admin Module (React App)  
**Priority:** MEDIUM  
**Duration:** 3-4 hours  
**Depends on:** Agent-2 (API endpoints)

**Deliverables:**
1. React app (`/frontend/admin/`)
2. Dashboard cu statistici
3. CRUD restaurante
4. CRUD utilizatori
5. Management comenzi
6. Rapoarte și analytics
7. Role-based access control

**Pages:**
- Dashboard principal
- Management restaurante
- Management utilizatori
- Toate comenzile
- Rapoarte
- Setări platformă

**Acceptance Criteria:**
- Statistici vizuale (grafice)
- CRUD complet pentru toate entitățile
- Role-based access (doar admini)
- Export rapoarte (CSV)

---

### Agent-6: DevOps & Integration
**Role:** Ops  
**Task:** Docker Setup & Integration  
**Priority:** MEDIUM  
**Duration:** 2-3 hours  
**Depends on:** All frontend agents

**Deliverables:**
1. Dockerfiles pentru fiecare serviciu
2. Docker Compose configuration
3. Nginx reverse proxy config
4. Environment files template
5. Deployment script
6. README cu instrucțiuni setup

**Acceptance Criteria:**
- `docker-compose up` pornește toate serviciile
- Serviciile comunică între ele
- Volumele persistă datele
- Health checks definite

---

## 📋 Execution Order (Dependencies)

```
Phase 1: Foundation
├── Agent-1: Database Schema (START FIRST)
└── Agent-6: Prepare Docker structure

Phase 2: Backend
└── Agent-2: API Development (START after Agent-1)

Phase 3: Frontend (can run in parallel)
├── Agent-3: Customer Module (START after Agent-2)
├── Agent-4: Restaurant Module (START after Agent-2)
└── Agent-5: Admin Module (START after Agent-2)

Phase 4: Integration
└── Agent-6: Final integration & deployment (START after all frontend)
```

---

## 🔄 Communication Protocol

### Artifact Locations
```
/shared/
├── /database/         # Schema, migrations, seeds
├── /backend/          # API server
├── /frontend/
│   ├── /customer/     # Customer React app
│   ├── /restaurant/   # Restaurant React app
│   └── /admin/        # Admin React app
├── /docs/             # Documentație
└── /docker/           # Docker configs
```

### Handoff Messages Format
```
AGENT COMPLETION REPORT
=======================
Agent: [name]
Task: [task description]
Status: COMPLETE/IN_PROGRESS/BLOCKED

Artifacts:
- [file path]: [description]

Testing:
- Command: [how to test]
- Expected result: [what should happen]

Known Issues:
- [any issues or limitations]

Next Actions:
- [what next agent needs to do]
```

---

## ✅ Definition of Done

**Per Task:**
- [ ] Codul funcționează conform cerințelor
- [ ] Testat local
- [ ] Documentat (README, comments)
- [ ] Commit în repo
- [ ] Handoff report completat

**Per Project:**
- [ ] Toate 3 modulele funcționale
- [ ] API complet integrat
- [ ] Docker setup funcțional
- [ ] Documentație deployment
- [ ] Test end-to-end (plasare comandă completă)

---

## 🚀 Next Steps

1. **Orchestrator** spawns Agent-1 (Database) - START NOW
2. **Orchestrator** spawns Agent-2 (Backend) - START after Agent-1 complete
3. **Orchestrator** spawns Agents 3,4,5 (Frontend) - START after Agent-2 complete
4. **Orchestrator** spawns Agent-6 (DevOps) - START after frontend complete
5. **Orchestrator** coordinates review and integration

---

*Document creat: 2026-04-19*  
*Versiune: 1.0*  
*Autor: Orchestrator Agent*
