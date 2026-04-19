# TASK-005: Wireframes & Specificație Taskboard Modern

## Data: 2026-04-19
## Proiect: QuickDelivery - Taskboard UI Refresh
## Stil: Linear-inspired Modern SaaS

---

## 1. Overview

Transformăm taskboard-ul actual într-o interfață modernă, inspirată de Linear.app - clean, fast, și intuitivă.

### Obiective:
- Eliminăm aspectul "învechit și urât" ✓
- Creăm experiență "modern SaaS, ca Linear" ✓
- Păstrăm funcționalitatea existentă ✓
- Îmbunătățim UX pentru toți utilizatorii ✓

---

## 2. Design System

### 2.1 Color Palette (Dark Mode - Default)

```css
--bg-primary: #0D0D0D       /* Background principal */
--bg-surface: #1C1C1C       /* Card-uri, panouri */
--bg-elevated: #262626      /* Hover states, dropdowns */
--bg-hover: #2A2A2A         /* Subtle hover */

--text-primary: #FFFFFF     /* Titluri, text important */
--text-secondary: #A1A1AA   /* Descrieri, metadata */
--text-tertiary: #71717A    /* Timestamps, hints */
--text-muted: #52525B       /* Disabled, placeholder */

--border-default: #27272A   /* Border-uri subtile */
--border-hover: #3F3F46     /* Border-uri pe hover */

--accent-blue: #5E6AD2      /* Primary accent */
--accent-blue-hover: #6B75E6

--status-todo: #71717A      /* Gray */
--status-progress: #5E6AD2 /* Blue */
--status-review: #F59E0B    /* Yellow */
--status-done: #10B981      /* Green */
--status-blocked: #EF4444   /* Red */

--priority-high: #EF4444
--priority-medium: #F59E0B
--priority-low: #10B981
```

### 2.2 Typography

```css
--font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif
--font-mono: 'JetBrains Mono', 'Fira Code', monospace

/* Scale */
--text-xs: 11px    /* Labels, badges */
--text-sm: 12px    /* Metadata, timestamps */
--text-base: 13px  /* Body text */
--text-md: 14px    /* Card titles */
--text-lg: 16px    /* Section headers */
--text-xl: 18px    /* Page titles */

/* Weights */
--font-normal: 400
--font-medium: 500
--font-semibold: 600
```

### 2.3 Spacing Scale

```css
--space-1: 4px
--space-2: 8px
--space-3: 12px
--space-4: 16px
--space-5: 20px
--space-6: 24px
--space-8: 32px
--space-10: 40px
--space-12: 48px
```

### 2.4 Border Radius

```css
--radius-sm: 4px   /* Small elements */
--radius-md: 6px   /* Buttons, inputs */
--radius-lg: 8px   /* Cards, modals */
--radius-xl: 12px  /* Large panels */
```

### 2.5 Shadows

```css
--shadow-sm: 0 1px 2px rgba(0,0,0,0.3)
--shadow-md: 0 4px 6px -1px rgba(0,0,0,0.4)
--shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.5)
```

---

## 3. Layout Structure

### 3.1 App Shell

```
┌─────────────────────────────────────────────────────────────┐
│  [Sidebar]              [Main Content Area]                 │
│  ┌─────┐  ┌─────────────────────────────────────────────┐  │
│  │     │  │ [TopBar]                                    │  │
│  │  ☰  │  │ Search | Filters | View Toggle | New Task   │  │
│  │     │  ├─────────────────────────────────────────────┤  │
│  │  📋 │  │                                             │  │
│  │  📊 │  │ [Content]                                   │  │
│  │  ⚙️  │  │ - List View / Board View                    │  │
│  │     │  │ - Task Cards                                │  │
│  └─────┘  │                                             │  │
│           └─────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Sidebar (240px width)

**Structure:**
```
┌────────────────────┐
│ 🚀 QuickDelivery   │ ← Logo
├────────────────────┤
│ + New Issue        │ ← CTA Button
├────────────────────┤
│                    │
│ 📋 TASK-001        │ ← Current Project
│   ├ Backlog        │
│   ├ Todo           │
│   ├ In Progress    │
│   ├ Review         │
│   └ Done           │
│                    │
│ 📊 Analytics       │
│ ⚙️  Settings       │
│                    │
└────────────────────┘
```

**Specs:**
- Width: 240px fixed
- Background: --bg-surface
- Border-right: 1px solid --border-default
- Collapsible on mobile (< 768px)

### 3.3 TopBar

**Structure:**
```
┌─────────────────────────────────────────────────────────────┐
│ ⌘K Search...    [Filter ▼] [View: List ▼]    [+ New Task] │
└─────────────────────────────────────────────────────────────┘
```

**Components:**
1. **Search Bar** (flex-1)
   - Placeholder: "⌘K Search or jump to..."
   - Command palette style
   - Shortcut: Cmd/Ctrl + K

2. **Filter Dropdown**
   - Status, Priority, Assignee, Label
   - Multi-select capability

3. **View Toggle**
   - List View (icon: ≡)
   - Board View (icon: ⊞)
   - Calendar View (icon: 📅) - Phase 2

4. **New Task Button**
   - Primary action (accent-blue)
   - Shortcut: C

---

## 4. Task Card (List View)

### 4.1 Structure

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ [○] [TASK-005] Implement modern taskboard UI           👤 Andrei  🏷️ UI  │
│      Design and implement new taskboard interface...          2h ago  ⚡ │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Anatomy

| Element | Style | Specs |
|---------|-------|-------|
| Checkbox | 16x16px | Rounded border, accent-blue on checked |
| Task ID | Mono, 12px | Color: --text-tertiary, ex: TASK-005 |
| Title | 14px, medium | Color: --text-primary, line-clamp: 1 |
| Description | 13px | Color: --text-secondary, line-clamp: 1 |
| Assignee | Avatar 24px | Circular, hover: show name |
| Labels | Badge | 11px, rounded-full, color-coded |
| Timestamp | 12px | Color: --text-tertiary, relative time |
| Priority | Icon | 🔴 High 🟡 Medium 🟢 Low |

### 4.3 States

**Default:**
- Background: transparent
- Border-bottom: 1px solid --border-default

**Hover:**
- Background: --bg-hover
- Cursor: pointer

**Selected:**
- Background: --bg-elevated
- Left border: 2px solid --accent-blue

**Done:**
- Title: text-decoration: line-through
- Color: --text-tertiary

---

## 5. Board View (Kanban)

### 5.1 Structure

```
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  📋 TODO    │ │ 🔄 PROGRESS │ │ 👀 REVIEW   │ │ ✅ DONE     │
│     5       │ │     3       │ │     2       │ │    12       │
├─────────────┤ ├─────────────┤ ├─────────────┤ ├─────────────┤
│ ┌─────────┐ │ │ ┌─────────┐ │ │ ┌─────────┐ │ │ ┌─────────┐ │
│ │ TASK-01 │ │ │ │ TASK-04 │ │ │ │ TASK-07 │ │ │ │ TASK-10 │ │
│ └─────────┘ │ │ └─────────┘ │ │ └─────────┘ │ │ └─────────┘ │
│ ┌─────────┐ │ │ ┌─────────┐ │ │ ┌─────────┐ │ │ ┌─────────┐ │
│ │ TASK-02 │ │ │ │ TASK-05 │ │ │ │ TASK-08 │ │ │ │ TASK-11 │ │
│ └─────────┘ │ │ └─────────┘ │ │ └─────────┘ │ │ └─────────┘ │
│ ┌─────────┐ │ │ ┌─────────┐ │ │             │ │ └─────────┘ │
│ │ TASK-03 │ │ │ │ TASK-06 │ │ │             │ │             │
│ └─────────┘ │ │ └─────────┘ │ │             │ │             │
│             │ │             │ │             │ │             │
│ + Add task  │ │ + Add task  │ │ + Add task  │ │ + Add task  │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
```

### 5.2 Column Specs

- **Width**: 320px fixed
- **Gap**: 16px between columns
- **Header**: 48px height, sticky
- **Card spacing**: 12px between cards
- **Horizontal scroll**: When columns exceed viewport

### 5.3 Column Header

```
┌─────────────────────────┐
│ ⚪ STATUS_NAME      999 │
│     + Add task          │
└─────────────────────────┘
```

- Dot indicator (color-coded by status)
- Status name (uppercase, 12px, --font-medium)
- Count badge (12px, --text-secondary)
- "+ Add task" button (hover visible)

---

## 6. Task Detail View (Modal/Slide-over)

### 6.1 Structure

```
┌─────────────────────────────────────────────────────────────┐
│ TASK-005                                    [×] [⋯] [🔗]     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [○] Implement modern taskboard UI                          │
│                                                             │
│  Status: [🔄 In Progress ▼]  Priority: [⚡ High ▼]          │
│                                                             │
│  ─── Description ───                                        │
│  Design and implement new taskboard interface inspired      │
│  by Linear.app. Include list view, board view, and          │
│  command palette.                                         │
│                                                             │
│  ─── Assignees ───                                        │
│  👤 Andrei  👤 Maria                                        │
│                                                             │
│  ─── Labels ───                                            │
│  🏷️ UI  🏷️ Frontend  🏷️ Sprint-3                             │
│                                                             │
│  ─── Activity ───                                          │
│  💬 Andrei created this task 2 hours ago                   │
│  💬 Maria assigned to Andrei 1 hour ago                    │
│                                                             │
│  [Add comment...]                                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 Specs

- **Width**: 640px (slide-over from right)
- **Backdrop**: rgba(0,0,0,0.7) blur
- **Animation**: Slide in 200ms ease-out

---

## 7. Interactions & Animations

### 7.1 Micro-interactions

| Action | Animation |
|--------|-----------|
| Card hover | background-color 150ms ease |
| Checkbox check | scale + bounce 200ms |
| Modal open | translateX + fade 200ms |
| Dropdown | scaleY + fade 150ms |
| Drag & Drop | lift shadow + rotate 2° |
| Status change | Color transition 200ms |
| Toast notification | Slide up + fade 300ms |

### 7.2 Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| ⌘K / Ctrl+K | Open command palette |
| C | Create new task |
| J / K | Navigate up/down (list view) |
| Enter | Open selected task |
| E | Edit task |
| M | Toggle sidebar |
| 1-4 | Switch status columns |
| Esc | Close modal / Cancel |

---

## 8. Responsive Breakpoints

| Breakpoint | Layout Changes |
|------------|----------------|
| < 768px | Sidebar collapses to hamburger menu |
| < 768px | Board view → single column scroll |
| < 640px | List view → compact (no description) |
| < 480px | Task detail becomes full-screen modal |

---

## 9. Implementation Phases

### Phase 1: MVP (Sprint 1-2)
- [ ] Design System (tokens CSS/SCSS)
- [ ] Sidebar component
- [ ] TopBar with search
- [ ] List View with task cards
- [ ] Task Detail modal
- [ ] Dark mode default

### Phase 2: Enhancement (Sprint 3)
- [ ] Board View (Kanban)
- [ ] Drag & Drop
- [ ] Filters & Search
- [ ] Light mode toggle
- [ ] Keyboard shortcuts

### Phase 3: Polish (Sprint 4)
- [ ] Command palette
- [ ] Animations & micro-interactions
- [ ] Mobile responsiveness
- [ ] Performance optimization

---

## 10. Acceptance Criteria

### Funcțional:
- [ ] Utilizatorul poate vedea task-uri în List View
- [ ] Utilizatorul poate vedea task-uri în Board View
- [ ] Utilizatorul poate deschide task detail în modal
- [ ] Utilizatorul poate schimba statusul unui task
- [ ] Search funcționează cu filtering
- [ ] Responsive pe mobile

### Visual:
- [ ] Design potrivește specificația (±2px)
- [ ] Culorile corespund design system
- [ ] Typography consistentă
- [ ] Animations fluide (60fps)
- [ ] Dark mode implementat

### UX:
- [ ] Time to first content < 2s
- [ ] Interacțiuni sub 100ms feedback
- [ ] Keyboard navigation complet
- [ ] No layout shift during load

---

## 11. Handoff Checklist

**Product-Architect:**
- ✅ User Research completat
- ✅ Specificație detaliată creată
- ✅ Design System definit
- ✅ Wireframes documentate
- ✅ Acceptance Criteria definite

**Next:**
- 🔄 Design în Figma (dacă echipa are designer)
- ⏳ Review cu Code-Architect pentru feasibility
- ⏳ Creare tickets în backlog

---

## Fișiere Create

1. `/workspace/shared/specs/TASK-005-user-research.md`
2. `/workspace/shared/specs/TASK-005-wireframes-spec.md` (acest fișier)

---

*Document creat de Product-Architect | TASK-005*
