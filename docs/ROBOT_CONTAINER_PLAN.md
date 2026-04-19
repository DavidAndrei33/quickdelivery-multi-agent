# PLAN ACADEMIC - Container Roboți Trading
## Versiune: 1.0.0 | Data: 2026-03-28

---

## 📋 ANALIZA ELEMENTELOR DIN CONTAINER

### 1. SELECTOR ROBOȚI (Funcțional)
- ✅ Dropdown cu V31, V32, V33
- ✅ Switch între roboți

### 2. INDICATORI CONEXIUNE (Necesită Implementare)
- V31 Status Dot - culoare bazată pe /api/v31/live_status
- V32 Status Dot - culoare bazată pe /api/v32/breakout_status
- V33 Status Dot - culoare bazată pe /api/v33/breakout_status

### 3. CONTROALE START/STOP (Necesită Implementare)
- Buton Start - POST /api/robot/{id}/start
- Buton Stop - POST /api/robot/{id}/stop
- Badge Status - din API status

### 4. INFO STRATEGIE (Parțial Funcțional)
- Text static pentru fiecare robot - OK
- Ultimul ciclu - necesită API call

### 5. STATISTICI (Necesită Date Live)
- Simboluri: număr din config robot
- Setup-uri Găsite: din API setups_count
- Tranzacții Executate: din API sau DB
- Status: din API status

### 6. ANALIZĂ LIVE (Necesită Implementare Completă)
- Progress bar - bazat pe analyzed_count / total_symbols
- Faza curentă - din API phase
- Simbol curent - din API current_symbol
- Statistici live: analizate, setups, rejecții

### 7. LOG-URI ROBOT (Necesită Endpoint Nou)
- Tabel cu log-uri din robot_logs table
- Filtre: lifecycle, cycle, symbol, setup, trade, error
- Refresh periodic

### 8. SIMBOLURI MONITORIZATE (Necesită Implementare)
- Grid cu simboluri din config
- Status colorat pentru fiecare
- Click pentru detalii

---

## 🔌 SURSE DE DATE

### API Endpoints Disponibile:
```
GET /api/v31/live_status       - Status V31 (funcționează)
GET /api/v32/breakout_status   - Status V32 (funcționează)
GET /api/v33/breakout_status   - Status V33 (funcționează)
GET /api/v32/or_data          - Opening Range data
GET /api/v32/asia_data        - Asia session data
GET /api/v33/presession_data  - Pre-session data
GET /api/robot_logs           - NECESITĂ IMPLEMENTARE
POST /api/robot/{id}/start    - NECESITĂ IMPLEMENTARE
POST /api/robot/{id}/stop     - NECESITĂ IMPLEMENTARE
```

### Database Tables:
- robot_logs - pentru log-uri
- symbol_analysis - pentru analiză per simbol
- position_tracking - pentru tranzacții

---

## 🎯 TASK-URI PENTRU ECHIPĂ

### TASK-ROBOT-001: Backend API pentru Control Roboți
**Responsabil:** builder-1
**Descriere:** Implementează endpoint-uri POST /start și /stop pentru fiecare robot
**Dependențe:** Niciuna
**Output:** API funcțional pentru control roboți

### TASK-ROBOT-002: Backend API pentru Log-uri
**Responsabil:** builder-2
**Descriere:** Implementează GET /api/robot_logs cu filtre și pagination
**Dependențe:** Niciuna
**Output:** Endpoint log-uri funcțional

### TASK-ROBOT-003: Frontend - Connection Status & Controls
**Responsabil:** dashboard-frontend
**Descriere:** Implementează indicatori conexiune și butoane start/stop funcționale
**Dependențe:** TASK-ROBOT-001
**Output:** UI controls funcționale

### TASK-ROBOT-004: Frontend - Live Analysis Display
**Responsabil:** dashboard-frontend
**Descriere:** Implementează progress bar, fază curentă, statistici live
**Dependențe:** Niciuna (folosește API existent)
**Output:** Analiză live funcțională

### TASK-ROBOT-005: Frontend - Robot Logs Table
**Responsabil:** dashboard-frontend
**Descriere:** Implementează tabel log-uri cu filtre și refresh
**Dependențe:** TASK-ROBOT-002
**Output:** Tabel log-uri funcțional

### TASK-ROBOT-006: Frontend - Monitored Symbols Grid
**Responsabil:** dashboard-frontend
**Descriere:** Implementează grid simboluri cu status colorat
**Dependențe:** Niciuna
**Output:** Grid simboluri funcțional

### TASK-ROBOT-007: Integration & Testing
**Responsabil:** integration-engineer
**Descriere:** Testează toate componentele și asigură comunicarea corectă
**Dependențe:** Toate celelalte task-uri
**Output:** Sistem complet funcțional

---

## 🔄 COMUNICARE ÎNTRE AGENȚI

### Protocol:
1. Fiecare agent scrie status în /workspace/shared/agents/{agent}/status.json
2. La completare, scrie rezultatul în /workspace/shared/agents/{agent}/output/
3. Dacă are nevoie de ajutor, creează fișier /workspace/shared/agents/{agent}/help-request.md
4. Manifest monitorizează și coordonează

### Structură Status:
```json
{
  "agent": "builder-1",
  "task": "TASK-ROBOT-001",
  "status": "in_progress|completed|blocked",
  "progress": 75,
  "last_update": "2026-03-28T14:30:00Z",
  "notes": "Detalii despre progres"
}
```

---

## ✅ CRITERII DE ACCEPTARE

- [ ] Toate API-urile returnează date corecte
- [ ] Butoanele Start/Stop funcționează
- [ ] Status-ul conexiunii se updatează în timp real
- [ ] Analiza live arată progres real
- [ ] Log-urile se încarcă și pot fi filtrate
- [ ] Simbolurile apar cu status corect
- [ ] Refresh automat funcționează (5s pentru live, 30s pentru logs)

---

## 🚨 ESCALARE

Dacă un agent este blocat >10 minute sau are nevoie de clarificări:
1. Scrie în help-request.md cu detaliile problemei
2. Manifest intervine sau escaladează la user
