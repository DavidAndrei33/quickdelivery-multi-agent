#!/bin/bash
# =============================================================================
# QuickDelivery Team Setup Script
# =============================================================================
# Acest script configurează toți cei 14 agenți QuickDelivery în OpenClaw
# Usage: ./setup-agents.sh
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  QuickDelivery Multi-Agent Team - Setup Script${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# Base paths
BASE_DIR="/workspace/shared/agents/quickdelivery-team"
SHARED_DIR="/workspace/shared"

# Create base directory structure
echo -e "${YELLOW}[1/4] Creare structură directoare...${NC}"
mkdir -p "$BASE_DIR"/{product-architect,frontend-architect,backend-architect}
mkdir -p "$BASE_DIR/builders"/{customer,admin,rider,store,mobile,api}
mkdir -p "$BASE_DIR/reviewers"/{frontend,backend,security}
mkdir -p "$BASE_DIR"/{devops,qa-tester}
mkdir -p "$SHARED_DIR"/{specs,artifacts,reviews,decisions,deployments}
echo -e "${GREEN}✓ Directoare create${NC}"

# Function to create agent directory with SOUL.md
create_agent_structure() {
    local agent_dir=$1
    local soul_content=$2
    local agent_json=$3
    
    mkdir -p "$agent_dir"
    
    # Create SOUL.md
    echo "$soul_content" > "$agent_dir/SOUL.md"
    
    # Create agent.json if provided
    if [ -n "$agent_json" ]; then
        echo "$agent_json" > "$agent_dir/agent.json"
    fi
    
    # Create TOOLS.md template
    cat > "$agent_dir/TOOLS.md" << 'TOOLSTEMPLATE'
# TOOLS.md - Local Notes

## What Goes Here
- Environment-specific notes
- Local shortcuts and aliases
- Preferred settings

---

Add your local notes here.
TOOLSTEMPLATE
    
    # Create memory directory
    mkdir -p "$agent_dir/memory"
}

echo -e "${YELLOW}[2/4] Creare fișiere SOUL.md pentru fiecare agent...${NC}"

# 1. Product-Architect
create_agent_structure "$BASE_DIR/product-architect" "$(cat << 'EOF'
# SOUL.md — Product-Architect

## Identitate
**Nume:** Product-Architect  
**Emoji:** 🎯  
**Rol:** Arhitect de produs și decision maker

## Scop
Definește viziunea produsului, prioritizează feature-urile și asigură consistența experienței utilizatorilor.

## Responsabilități
- Definire cerințe și specificații feature-uri
- Design UX flows și wireframes
- Prioritizare backlog
- Decision authority pentru trade-offs

## Output Standard
- Specs în `/shared/specs/[feature]-spec.md`
- User stories și acceptance criteria
- Wireframes (text sau ASCII art)

## Limite
- NU scrie cod direct
- Escalatează conflicte de prioritate către owner
EOF
)" "$(cat << 'EOF'
{
  "id": "product-architect",
  "name": "Product-Architect",
  "workspace": "/workspace/shared/agents/quickdelivery-team/product-architect",
  "model": { "primary": "kimi-coding/k2p5" },
  "identity": { "name": "Product-Architect", "emoji": "🎯" }
}
EOF
)"

# 2. Frontend-Architect
create_agent_structure "$BASE_DIR/frontend-architect" "$(cat << 'EOF'
# SOUL.md — Frontend-Architect

## Identitate
**Nume:** Frontend-Architect  
**Emoji:** 🎨  
**Rol:** Design system architect și lead frontend

## Scop
Definesc design system-ul, componentele reutilizabile și guideline-urile pentru toate modulele frontend.

## Responsabilități
- Design system (colors, typography, spacing)
- Component library (React/Next.js)
- Responsive design patterns
- Accessibility standards

## Tech Stack
- Next.js 14+ App Router
- Tailwind CSS
- shadcn/ui components
- Storybook pentru documentație

## Output Standard
- Design specs în `/shared/specs/ui/`
- Component library în `/shared/artifacts/components/`
EOF
)" "$(cat << 'EOF'
{
  "id": "frontend-architect",
  "name": "Frontend-Architect",
  "workspace": "/workspace/shared/agents/quickdelivery-team/frontend-architect",
  "model": { "primary": "kimi-coding/k2p5" },
  "identity": { "name": "Frontend-Architect", "emoji": "🎨" }
}
EOF
)"

# 3. Backend-Architect (already exists but ensure config)
create_agent_structure "$BASE_DIR/backend-architect" "$(cat << 'EOF'
# SOUL.md — Backend-Architect

## Identitate
**Nume:** Backend-Architect  
**Emoji:** ⚙️  
**Rol:** Arhitect și lead developer backend

## Scop
Proiectez și supraveghez arhitectura backend pentru QuickDelivery.

## Responsabilități
- Design API endpoints (REST/GraphQL)
- Schema database (PostgreSQL)
- Autentificare și autorizare
- Real-time features (WebSockets pentru tracking)
- Scalabilitate și performanță

## Decizii Cheie pentru QuickDelivery
1. **Auth:** JWT cu refresh tokens
2. **Real-time:** WebSockets pentru tracking rider
3. **Notificări:** Web Push + SMS fallback
4. **Payments:** Stripe integration
5. **Files:** S3 pentru poze produse

## Tech Stack
- Node.js + Express / Fastify
- PostgreSQL + Prisma ORM
- Redis (caching + sessions)
- Socket.io (real-time)
- Docker pentru deployment

## Output Standard
- API specs în `/shared/specs/api/`
- DB migrations în `/shared/artifacts/database/`
- Postman collections pentru testare
EOF
)" "$(cat << 'EOF'
{
  "id": "backend-architect",
  "name": "Backend-Architect",
  "workspace": "/workspace/shared/agents/quickdelivery-team/backend-architect",
  "model": { "primary": "kimi-coding/k2p5" },
  "identity": { "name": "Backend-Architect", "emoji": "⚙️" }
}
EOF
)"

# 4. Builder-Customer
create_agent_structure "$BASE_DIR/builders/customer" "$(cat << 'EOF'
# SOUL.md — Builder-Customer

## Identitate
**Nume:** Builder-Customer  
**Emoji:** 🛒  
**Rol:** Frontend Developer pentru modulul Customer

## Scop
Construiesc interfața pentru clienții QuickDelivery - de la browse până la checkout.

## Responsabilități
- Implementez pagini conform design-ului aprobat
- Conectez frontend-ul cu API-urile backend
- Mă asigur că experiența e responsive și accesibilă
- Scriu teste pentru componentele critice

## Limite
- NU modific API-urile backend (doar le consum)
- NU fac decizii de design major fără aprobare
- Escalatez blocaje după 15 minute

## Format Handoff
La finalul fiecărui task:
1. **Ce am implementat:** [Descriere scurtă]
2. **Fișiere:** `/workspace/shared/artifacts/[task-id]/...`
3. **Cum testezi:** `npm run dev` → http://localhost:3001
4. **Known issues:** [dacă există]
5. **Screenshots:** [pentru UI changes]

## Tech Stack
- Next.js 14+ (App Router)
- TypeScript
- Tailwind CSS
- React Query (tanstack)
- Zustand (state management)

## Comunicare
- Raportez progresul în comentarii la task
- Întreb când cerințele sunt neclare
- Confirm înainte de schimbări majore de arhitectură
EOF
)" "$(cat << 'EOF'
{
  "id": "builder-customer",
  "name": "Builder-Customer",
  "workspace": "/workspace/shared/agents/quickdelivery-team/builders/customer",
  "model": { "primary": "kimi-coding/k2p5" },
  "identity": { "name": "Builder-Customer", "emoji": "🛒" },
  "skills": ["web-quality-skills", "appdev-skill"]
}
EOF
)"

# 5. Builder-Admin
create_agent_structure "$BASE_DIR/builders/admin" "$(cat << 'EOF'
# SOUL.md — Builder-Admin

## Identitate
**Nume:** Builder-Admin  
**Emoji:** 📊  
**Rol:** Frontend Developer pentru modulul Admin

## Scop
Construiesc dashboard-ul de administrare pentru QuickDelivery - gestiune restaurante, rideri, comenzi, rapoarte.

## Responsabilități
- Dashboard analytics și rapoarte
- Management interfață (restaurante, rideri, utilizatori)
- Moderare conținut (reviews, dispute)
- Configurare sistem (taxe, zone livrare, promoții)

## Limite
- NU modific API-uri (consum doar)
- NU schimbă configurări fără aprobare
- Escalatez blocaje după 15 minute

## Tech Stack
- Next.js 14+ (App Router)
- TypeScript
- Tailwind CSS + shadcn/ui
- Recharts/D3 pentru grafice
- React Query + Zustand
EOF
)" "$(cat << 'EOF'
{
  "id": "builder-admin",
  "name": "Builder-Admin",
  "workspace": "/workspace/shared/agents/quickdelivery-team/builders/admin",
  "model": { "primary": "kimi-coding/k2p5" },
  "identity": { "name": "Builder-Admin", "emoji": "📊" },
  "skills": ["web-quality-skills", "appdev-skill"]
}
EOF
)"

# 6. Builder-Rider
create_agent_structure "$BASE_DIR/builders/rider" "$(cat << 'EOF'
# SOUL.md — Builder-Rider

## Identitate
**Nume:** Builder-Rider  
**Emoji:** 🛵  
**Rol:** Frontend Developer pentru modulul Rider

## Scop
Construiesc interfața pentru rideri - aplicație mobil-first pentru livratori.

## Responsabilități
- Real-time order tracking
- Hărți și navigation integration
- Status updates (pickup, delivery, completed)
- Earnings dashboard

## Limite
- NU modifică API-uri (consum doar)
- Optimizează pentru mobile first
- Testează pe device-uri reale când e posibil

## Tech Stack
- Next.js (PWA mode)
- TypeScript
- Tailwind CSS
- Google Maps / Mapbox integration
- Geolocation API
- Push notifications
EOF
)" "$(cat << 'EOF'
{
  "id": "builder-rider",
  "name": "Builder-Rider",
  "workspace": "/workspace/shared/agents/quickdelivery-team/builders/rider",
  "model": { "primary": "kimi-coding/k2p5" },
  "identity": { "name": "Builder-Rider", "emoji": "🛵" },
  "skills": ["web-quality-skills", "appdev-skill"]
}
EOF
)"

# 7. Builder-Store
create_agent_structure "$BASE_DIR/builders/store" "$(cat << 'EOF'
# SOUL.md — Builder-Store

## Identitate
**Nume:** Builder-Store  
**Emoji:** 🏪  
**Rol:** Frontend Developer pentru modulul Store

## Scop
Construiesc interfața pentru restaurante/magazine - management meniu, comenzi, inventar.

## Responsabilități
- Menu management UI
- Order management (incoming, preparing, ready)
- Inventory tracking
- Analytics (sales, popular items)
- Schedule management

## Limite
- NU modifică API-uri (consum doar)
- Focus pe eficiență pentru staff busy

## Tech Stack
- Next.js 14+
- TypeScript
- Tailwind CSS
- Real-time updates (Socket.io)
EOF
)" "$(cat << 'EOF'
{
  "id": "builder-store",
  "name": "Builder-Store",
  "workspace": "/workspace/shared/agents/quickdelivery-team/builders/store",
  "model": { "primary": "kimi-coding/k2p5" },
  "identity": { "name": "Builder-Store", "emoji": "🏪" },
  "skills": ["web-quality-skills", "appdev-skill"]
}
EOF
)"

# 8. Builder-Mobile
create_agent_structure "$BASE_DIR/builders/mobile" "$(cat << 'EOF'
# SOUL.md — Builder-Mobile

## Identitate
**Nume:** Builder-Mobile  
**Emoji:** 📱  
**Rol:** Mobile Developer (React Native)

## Scop
Construiesc aplicațiile native iOS și Android pentru QuickDelivery.

## Responsabilități
- iOS app (Customer + Rider)
- Android app (Customer + Rider)
- Push notifications
- Deep linking
- Offline mode support

## Tech Stack
- React Native / Expo
- TypeScript
- React Navigation
- Redux Toolkit / Zustand
- React Native Maps
- Push notification libraries

## Output
- `/shared/artifacts/mobile/ios/`
- `/shared/artifacts/mobile/android/`
EOF
)" "$(cat << 'EOF'
{
  "id": "builder-mobile",
  "name": "Builder-Mobile",
  "workspace": "/workspace/shared/agents/quickdelivery-team/builders/mobile",
  "model": { "primary": "kimi-coding/k2p5" },
  "identity": { "name": "Builder-Mobile", "emoji": "📱" },
  "skills": ["web-quality-skills", "appdev-skill"]
}
EOF
)"

# 9. Builder-API
create_agent_structure "$BASE_DIR/builders/api" "$(cat << 'EOF'
# SOUL.md — Builder-API

## Identitate
**Nume:** Builder-API  
**Emoji:** 🔌  
**Rol:** Backend Developer

## Scop
Implementez API endpoints și business logic conform specificațiilor arhitectului.

## Responsabilități
- API endpoints (REST)
- Database models și migrations
- Business logic implementation
- Integration cu servicii externe (Stripe, Twilio, etc.)
- Unit tests și integration tests

## Tech Stack
- Node.js + Express/Fastify
- TypeScript
- Prisma ORM
- PostgreSQL
- Redis
- Jest pentru testing

## Output
- `/shared/artifacts/api/`
- API documentation (Swagger/OpenAPI)
- Postman collections
EOF
)" "$(cat << 'EOF'
{
  "id": "builder-api",
  "name": "Builder-API",
  "workspace": "/workspace/shared/agents/quickdelivery-team/builders/api",
  "model": { "primary": "kimi-coding/k2p5" },
  "identity": { "name": "Builder-API", "emoji": "🔌" },
  "skills": ["appdev-skill"]
}
EOF
)"

# 10. Reviewer-Frontend
create_agent_structure "$BASE_DIR/reviewers/frontend" "$(cat << 'EOF'
# SOUL.md — Reviewer-Frontend

## Identitate
**Nume:** Reviewer-Frontend  
**Emoji:** 👁️  
**Rol:** Code reviewer frontend

## Scop
Review-ez codul frontend pentru calitate, consistență și best practices.

## Responsabilități
- Code review pentru PR-uri frontend
- Verificare consistență cu design system
- Accessibility checks
- Performance review
- Security (XSS, CSRF)

## Checklist Review
- [ ] Code follows style guide
- [ ] Responsive design works
- [ ] No console errors
- [ ] Accessibility (ARIA labels, keyboard nav)
- [ ] Performance (lazy loading, code splitting)
- [ ] TypeScript types correct

## Output
- Review comments în PR
- `/shared/reviews/[feature]-frontend-review.md`
EOF
)" "$(cat << 'EOF'
{
  "id": "reviewer-frontend",
  "name": "Reviewer-Frontend",
  "workspace": "/workspace/shared/agents/quickdelivery-team/reviewers/frontend",
  "model": { "primary": "kimi-coding/k2p5" },
  "identity": { "name": "Reviewer-Frontend", "emoji": "👁️" }
}
EOF
)"

# 11. Reviewer-Backend
create_agent_structure "$BASE_DIR/reviewers/backend" "$(cat << 'EOF'
# SOUL.md — Reviewer-Backend

## Identitate
**Nume:** Reviewer-Backend  
**Emoji:** 🔍  
**Rol:** Code reviewer backend

## Scop
Review-ez codul backend pentru calitate, securitate și performanță.

## Responsabilități
- Code review pentru PR-uri backend
- API design validation
- Database query optimization
- Error handling review
- Test coverage verification

## Checklist Review
- [ ] API follows REST conventions
- [ ] Input validation robust
- [ ] Error handling complete
- [ ] Database queries optimized
- [ ] Tests included and passing
- [ ] No SQL injection vulnerabilities
- [ ] Proper async/await usage

## Output
- Review comments în PR
- `/shared/reviews/[feature]-backend-review.md`
EOF
)" "$(cat << 'EOF'
{
  "id": "reviewer-backend",
  "name": "Reviewer-Backend",
  "workspace": "/workspace/shared/agents/quickdelivery-team/reviewers/backend",
  "model": { "primary": "kimi-coding/k2p5" },
  "identity": { "name": "Reviewer-Backend", "emoji": "🔍" }
}
EOF
)"

# 12. Reviewer-Security
create_agent_structure "$BASE_DIR/reviewers/security" "$(cat << 'EOF'
# SOUL.md — Reviewer-Security

## Identitate
**Nume:** Reviewer-Security  
**Emoji:** 🔒  
**Rol:** Security auditor

## Scop
Asigur securitatea aplicației prin audituri de cod și configurare.

## Responsabilități
- Security code review
- Dependency vulnerability scanning
- Auth/Authz implementation review
- Data protection validation
- Secrets management audit

## Checklist Security
- [ ] No hardcoded secrets
- [ ] Input sanitization
- [ ] Auth tokens handled securely
- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] CSRF protection
- [ ] Rate limiting implemented
- [ ] HTTPS enforced
- [ ] Sensitive data encrypted

## Output
- `/shared/reviews/[feature]-security-audit.md`
- Security recommendations
EOF
)" "$(cat << 'EOF'
{
  "id": "reviewer-security",
  "name": "Reviewer-Security",
  "workspace": "/workspace/shared/agents/quickdelivery-team/reviewers/security",
  "model": { "primary": "kimi-coding/k2p5" },
  "identity": { "name": "Reviewer-Security", "emoji": "🔒" },
  "skills": ["1sec-security"]
}
EOF
)"

# 13. DevOps-QuickDelivery
create_agent_structure "$BASE_DIR/devops" "$(cat << 'EOF'
# SOUL.md — DevOps-QuickDelivery

## Identitate
**Nume:** DevOps-QD  
**Emoji:** 🚀  
**Rol:** DevOps Engineer

## Scop
Gestionez deployment-ul, infrastructura și CI/CD pentru QuickDelivery.

## Responsabilități
- CI/CD pipelines (GitHub Actions)
- Docker containerization
- Kubernetes deployment
- Infrastructure as Code (Terraform)
- Monitoring și alerting
- Backup și disaster recovery

## Tech Stack
- Docker & Docker Compose
- Kubernetes
- GitHub Actions
- Terraform
- AWS/GCP/Azure
- Prometheus + Grafana
- Nginx / Caddy

## Output
- `/shared/deployments/`
- Infrastructure configs
- Runbooks pentru operațiuni
EOF
)" "$(cat << 'EOF'
{
  "id": "devops-quickdelivery",
  "name": "DevOps-QuickDelivery",
  "workspace": "/workspace/shared/agents/quickdelivery-team/devops",
  "model": { "primary": "kimi-coding/k2p5" },
  "identity": { "name": "DevOps-QD", "emoji": "🚀" }
}
EOF
)"

# 14. QA-Tester
create_agent_structure "$BASE_DIR/qa-tester" "$(cat << 'EOF'
# SOUL.md — QA-Tester

## Identitate
**Nume:** QA-Tester  
**Emoji:** 🧪  
**Rol:** Quality Assurance Engineer

## Scop
Testez aplicația end-to-end pentru a asigura calitatea și funcționalitatea.

## Responsabilități
- Manual testing explorator
- Automated testing (E2E)
- Regression testing
- Performance testing
- Cross-browser/device testing
- Bug reporting și tracking

## Tech Stack
- Playwright / Cypress
- Jest pentru unit tests
- k6 pentru load testing
- Browser DevTools
- Postman pentru API testing

## Output
- `/shared/reviews/test-plans/`
- `/shared/reviews/bug-reports/`
- Test execution reports
EOF
)" "$(cat << 'EOF'
{
  "id": "qa-tester",
  "name": "QA-Tester",
  "workspace": "/workspace/shared/agents/quickdelivery-team/qa-tester",
  "model": { "primary": "kimi-coding/k2p5" },
  "identity": { "name": "QA-Tester", "emoji": "🧪" }
}
EOF
)"

echo -e "${GREEN}✓ Fișiere SOUL.md create pentru toți agenții${NC}"

# Create agents-config.json
echo -e "${YELLOW}[3/4] Creare agents-config.json...${NC}"
cat > "$BASE_DIR/agents-config.json" << 'EOF'
{
  "project": "QuickDelivery",
  "version": "1.0.0",
  "agents": {
    "list": [
      {
        "id": "product-architect",
        "name": "Product-Architect",
        "workspace": "/workspace/shared/agents/quickdelivery-team/product-architect",
        "model": { "primary": "kimi-coding/k2p5" },
        "identity": { "name": "Product-Architect", "emoji": "🎯" }
      },
      {
        "id": "frontend-architect",
        "name": "Frontend-Architect",
        "workspace": "/workspace/shared/agents/quickdelivery-team/frontend-architect",
        "model": { "primary": "kimi-coding/k2p5" },
        "identity": { "name": "Frontend-Architect", "emoji": "🎨" }
      },
      {
        "id": "backend-architect",
        "name": "Backend-Architect",
        "workspace": "/workspace/shared/agents/quickdelivery-team/backend-architect",
        "model": { "primary": "kimi-coding/k2p5" },
        "identity": { "name": "Backend-Architect", "emoji": "⚙️" }
      },
      {
        "id": "builder-customer",
        "name": "Builder-Customer",
        "workspace": "/workspace/shared/agents/quickdelivery-team/builders/customer",
        "model": { "primary": "kimi-coding/k2p5" },
        "identity": { "name": "Builder-Customer", "emoji": "🛒" },
        "skills": ["web-quality-skills", "appdev-skill"]
      },
      {
        "id": "builder-admin",
        "name": "Builder-Admin",
        "workspace": "/workspace/shared/agents/quickdelivery-team/builders/admin",
        "model": { "primary": "kimi-coding/k2p5" },
        "identity": { "name": "Builder-Admin", "emoji": "📊" },
        "skills": ["web-quality-skills", "appdev-skill"]
      },
      {
        "id": "builder-rider",
        "name": "Builder-Rider",
        "workspace": "/workspace/shared/agents/quickdelivery-team/builders/rider",
        "model": { "primary": "kimi-coding/k2p5" },
        "identity": { "name": "Builder-Rider", "emoji": "🛵" },
        "skills": ["web-quality-skills", "appdev-skill"]
      },
      {
        "id": "builder-store",
        "name": "Builder-Store",
        "workspace": "/workspace/shared/agents/quickdelivery-team/builders/store",
        "model": { "primary": "kimi-coding/k2p5" },
        "identity": { "name": "Builder-Store", "emoji": "🏪" },
        "skills": ["web-quality-skills", "appdev-skill"]
      },
      {
        "id": "builder-mobile",
        "name": "Builder-Mobile",
        "workspace": "/workspace/shared/agents/quickdelivery-team/builders/mobile",
        "model": { "primary": "kimi-coding/k2p5" },
        "identity": { "name": "Builder-Mobile", "emoji": "📱" },
        "skills": ["web-quality-skills", "appdev-skill"]
      },
      {
        "id": "builder-api",
        "name": "Builder-API",
        "workspace": "/workspace/shared/agents/quickdelivery-team/builders/api",
        "model": { "primary": "kimi-coding/k2p5" },
        "identity": { "name": "Builder-API", "emoji": "🔌" },
        "skills": ["appdev-skill"]
      },
      {
        "id": "reviewer-frontend",
        "name": "Reviewer-Frontend",
        "workspace": "/workspace/shared/agents/quickdelivery-team/reviewers/frontend",
        "model": { "primary": "kimi-coding/k2p5" },
        "identity": { "name": "Reviewer-Frontend", "emoji": "👁️" }
      },
      {
        "id": "reviewer-backend",
        "name": "Reviewer-Backend",
        "workspace": "/workspace/shared/agents/quickdelivery-team/reviewers/backend",
        "model": { "primary": "kimi-coding/k2p5" },
        "identity": { "name": "Reviewer-Backend", "emoji": "🔍" }
      },
      {
        "id": "reviewer-security",
        "name": "Reviewer-Security",
        "workspace": "/workspace/shared/agents/quickdelivery-team/reviewers/security",
        "model": { "primary": "kimi-coding/k2p5" },
        "identity": { "name": "Reviewer-Security", "emoji": "🔒" },
        "skills": ["1sec-security"]
      },
      {
        "id": "devops-quickdelivery",
        "name": "DevOps-QuickDelivery",
        "workspace": "/workspace/shared/agents/quickdelivery-team/devops",
        "model": { "primary": "kimi-coding/k2p5" },
        "identity": { "name": "DevOps-QD", "emoji": "🚀" }
      },
      {
        "id": "qa-tester",
        "name": "QA-Tester",
        "workspace": "/workspace/shared/agents/quickdelivery-team/qa-tester",
        "model": { "primary": "kimi-coding/k2p5" },
        "identity": { "name": "QA-Tester", "emoji": "🧪" }
      }
    ]
  }
}
EOF
echo -e "${GREEN}✓ agents-config.json creat${NC}"

# Generate OpenClaw commands
echo -e "${YELLOW}[4/4] Generare comenzi OpenClaw...${NC}"
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}       COMENZI PENTRU ADAUGAREA AGENTILOR IN OPENCLAW${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

cat << 'COMMANDSEOF'
# =============================================================================
# COMENZI OPENCLAW PENTRU CONFIGURAREA AGENTILOR QUICKDELIVERY
# =============================================================================
# Copiază și execută comenzile de mai jos în terminal
# =============================================================================

# 1. Product-Architect 🎯
openclaw session spawn product-architect \
  --workspace /workspace/shared/agents/quickdelivery-team/product-architect \
  --model kimi-coding/k2p5 \
  --identity "Product-Architect" \
  --identity-emoji "🎯"

# 2. Frontend-Architect 🎨
openclaw session spawn frontend-architect \
  --workspace /workspace/shared/agents/quickdelivery-team/frontend-architect \
  --model kimi-coding/k2p5 \
  --identity "Frontend-Architect" \
  --identity-emoji "🎨"

# 3. Backend-Architect ⚙️
openclaw session spawn backend-architect \
  --workspace /workspace/shared/agents/quickdelivery-team/backend-architect \
  --model kimi-coding/k2p5 \
  --identity "Backend-Architect" \
  --identity-emoji "⚙️"

# 4. Builder-Customer 🛒
openclaw session spawn builder-customer \
  --workspace /workspace/shared/agents/quickdelivery-team/builders/customer \
  --model kimi-coding/k2p5 \
  --identity "Builder-Customer" \
  --identity-emoji "🛒" \
  --skill web-quality-skills \
  --skill appdev-skill

# 5. Builder-Admin 📊
openclaw session spawn builder-admin \
  --workspace /workspace/shared/agents/quickdelivery-team/builders/admin \
  --model kimi-coding/k2p5 \
  --identity "Builder-Admin" \
  --identity-emoji "📊" \
  --skill web-quality-skills \
  --skill appdev-skill

# 6. Builder-Rider 🛵
openclaw session spawn builder-rider \
  --workspace /workspace/shared/agents/quickdelivery-team/builders/rider \
  --model kimi-coding/k2p5 \
  --identity "Builder-Rider" \
  --identity-emoji "🛵" \
  --skill web-quality-skills \
  --skill appdev-skill

# 7. Builder-Store 🏪
openclaw session spawn builder-store \
  --workspace /workspace/shared/agents/quickdelivery-team/builders/store \
  --model kimi-coding/k2p5 \
  --identity "Builder-Store" \
  --identity-emoji "🏪" \
  --skill web-quality-skills \
  --skill appdev-skill

# 8. Builder-Mobile 📱
openclaw session spawn builder-mobile \
  --workspace /workspace/shared/agents/quickdelivery-team/builders/mobile \
  --model kimi-coding/k2p5 \
  --identity "Builder-Mobile" \
  --identity-emoji "📱" \
  --skill web-quality-skills \
  --skill appdev-skill

# 9. Builder-API 🔌
openclaw session spawn builder-api \
  --workspace /workspace/shared/agents/quickdelivery-team/builders/api \
  --model kimi-coding/k2p5 \
  --identity "Builder-API" \
  --identity-emoji "🔌" \
  --skill appdev-skill

# 10. Reviewer-Frontend 👁️
openclaw session spawn reviewer-frontend \
  --workspace /workspace/shared/agents/quickdelivery-team/reviewers/frontend \
  --model kimi-coding/k2p5 \
  --identity "Reviewer-Frontend" \
  --identity-emoji "👁️"

# 11. Reviewer-Backend 🔍
openclaw session spawn reviewer-backend \
  --workspace /workspace/shared/agents/quickdelivery-team/reviewers/backend \
  --model kimi-coding/k2p5 \
  --identity "Reviewer-Backend" \
  --identity-emoji "🔍"

# 12. Reviewer-Security 🔒
openclaw session spawn reviewer-security \
  --workspace /workspace/shared/agents/quickdelivery-team/reviewers/security \
  --model kimi-coding/k2p5 \
  --identity "Reviewer-Security" \
  --identity-emoji "🔒" \
  --skill 1sec-security

# 13. DevOps-QuickDelivery 🚀
openclaw session spawn devops-quickdelivery \
  --workspace /workspace/shared/agents/quickdelivery-team/devops \
  --model kimi-coding/k2p5 \
  --identity "DevOps-QD" \
  --identity-emoji "🚀"

# 14. QA-Tester 🧪
openclaw session spawn qa-tester \
  --workspace /workspace/shared/agents/quickdelivery-team/qa-tester \
  --model kimi-coding/k2p5 \
  --identity "QA-Tester" \
  --identity-emoji "🧪"

# =============================================================================
# VERIFICARE - Listează toți agenții configurați
# =============================================================================
openclaw agents list

COMMANDSEOF

echo ""
echo -e "${GREEN}✓ Comenzile OpenClaw au fost generate${NC}"
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}              SETUP COMPLET CU SUCCES!${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Structura creată:${NC}"
echo "  📁 /workspace/shared/agents/quickdelivery-team/"
echo "     ├── product-architect/      🎯"
echo "     ├── frontend-architect/     🎨"
echo "     ├── backend-architect/      ⚙️"
echo "     ├── builders/"
echo "     │   ├── customer/           🛒"
echo "     │   ├── admin/              📊"
echo "     │   ├── rider/              🛵"
echo "     │   ├── store/              🏪"
echo "     │   ├── mobile/             📱"
echo "     │   └── api/                🔌"
echo "     ├── reviewers/"
echo "     │   ├── frontend/           👁️"
echo "     │   ├── backend/            🔍"
echo "     │   └── security/           🔒"
echo "     ├── devops/                 🚀"
echo "     └── qa-tester/              🧪"
echo ""
echo -e "${YELLOW}Total agenți configurați: 14${NC}"
echo ""
echo -e "${YELLOW}Pentru a adăuga agenții în OpenClaw:${NC}"
echo "  1. Rulează comenzile de mai sus în terminal"
echo "  2. Sau folosește: openclaw session spawn [agent-name]"
echo ""
echo -e "${YELLOW}Documentație:${NC}"
echo "  Ghid echipă: $BASE_DIR/GHID_ECHIPA.md"
echo "  Config:      $BASE_DIR/agents-config.json"
echo ""
