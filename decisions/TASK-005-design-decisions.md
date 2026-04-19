# TASK-005: Decizii de Design

## Data: 2026-04-19

## Decizii Luate

### 1. Framework UI
**Decizie:** Nu impunem un framework specific - recomandăm implementare custom cu design tokens
**Rationale:** Maximum control, performance, și consistență cu Linear.app

### 2. Dark Mode First
**Decizie:** Dark mode este default; light mode în Phase 2
**Rationale:** Linear.app și SaaS-urile moderne favorizează dark mode pentru productivitate

### 3. Layout
**Decizie:** Sidebar + Main Content (240px sidebar)
**Rationale:** Pattern standard, familiar utilizatorilor, optim pentru productivitate

### 4. Views
**Decizie:** List View (MVP) + Board View (Phase 2)
**Rationale:** List view = viteză pentru power users; Board view = vizibilitate pentru managers

### 5. Typography
**Decizie:** Inter font family (sau sistem fallback)
**Rationale:** Linear folosește Inter - clean, modern, excellent readability

## Notă de la Client
- Feedback: Taskboard actual "învechit și urât"
- Așteptare: "modern SaaS, ca Linear.app"

---
*Documentat de Product-Architect*
