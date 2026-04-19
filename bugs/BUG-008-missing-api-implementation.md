# BUG-008: Missing API Implementation

## Informații Generale
| Atribut | Valoare |
|---------|---------|
| **ID** | BUG-008 |
| **Severitate** | CRITICAL |
| **Status** | OPEN |
| **Data descoperirii** | 2026-03-28 |
| **Raportat de** | QA-Master Agent |

## Descriere
Acest bug este un rezumat la nivel înalt care grupează toate problemele legate de API-ul lipsă pentru roboți. Reprezintă blocul major de muncă necesar pentru a face dashboard-ul funcțional.

## Probleme Incluse
- BUG-003: Robot control endpoints (Start/Stop)
- BUG-004: Robot status endpoints
- BUG-011: Symbol analysis endpoint

## Endpoint-uri Necesare

### Control (BUG-003)
```
POST /api/robot/{robot}/start
POST /api/robot/{robot}/stop
```

### Status (BUG-004)
```
GET /api/v31/live_status
GET /api/v32/session_status
GET /api/v32/or_data
GET /api/v32/asia_data
GET /api/v32/breakout_status
GET /api/v32/trade_stats
GET /api/v33/session_status
GET /api/v33/or_data
GET /api/v33/presession_data
GET /api/v33/breakout_status
GET /api/v33/trade_stats
```

### Logs (BUG-006)
```
GET /api/robot/{robot}/logs?filter={filter}
```

### Symbol Analysis (BUG-011)
```
GET /api/symbol_analysis?symbol={symbol}&robot={robot}
```

## Arhitectură Propusă

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────────┐
│   Dashboard     │────>│  Node.js     │────>│  Robot Service  │
│   (Frontend)    │     │  API Server  │     │  (Python/Java)  │
└─────────────────┘     └──────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌──────────────┐
                        │  Database    │
                        │  (PostgreSQL)│
                        └──────────────┘
```

## Implementare Necesară

### 1. Layer API (Node.js)
- Rute pentru fiecare endpoint
- Validare autentificare JWT
- Forward către serviciul robot
- Cache pentru date frecvente

### 2. Robot Service
- Proces separat pentru fiecare robot (V31, V32, V33)
- Comunicare prin WebSocket sau HTTP
- Stocare stare în database

### 3. Database Schema
```sql
-- Robot status
CREATE TABLE robot_status (
    robot_id VARCHAR(50) PRIMARY KEY,
    status VARCHAR(50),
    is_running BOOLEAN,
    last_update TIMESTAMP,
    data JSONB
);

-- Robot logs
CREATE TABLE robot_logs (
    id SERIAL PRIMARY KEY,
    robot_id VARCHAR(50),
    level VARCHAR(20),
    message TEXT,
    cycle INTEGER,
    created_at TIMESTAMP
);

-- Symbol analysis
CREATE TABLE symbol_analysis (
    id SERIAL PRIMARY KEY,
    robot_id VARCHAR(50),
    symbol VARCHAR(20),
    analysis JSONB,
    created_at TIMESTAMP
);
```

## Estimare Efort
| Componentă | Ore Estimate |
|------------|--------------|
| API Layer | 4-6 ore |
| Robot Service Integration | 6-8 ore |
| Database Schema & Queries | 2-3 ore |
| Testing & Debugging | 3-4 ore |
| **Total** | **15-21 ore** |

## Referințe
- Depinde de: BUG-003, BUG-004
- Fișier raport: TEST-CASES-COMPLETE-REPORT.md
