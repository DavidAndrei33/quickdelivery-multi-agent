# Architecture Documentation - Trading Dashboard v2

## Overview
Sistem multi-agent pentru trading automatizat cu dashboard live și coordonare între 13 agenți specializați.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER                                    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                     ORCHESTRATOR                                │
│              (Manifest - Tech Lead)                             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   PROJECT BRAIN                                 │
│         (Project Continuity Manager)                            │
│  • project_state.json       • architecture.md                   │
│  • features.json            • files_index.json                  │
│  • decisions.md             • versions/                         │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                     AGENT LAYER                                 │
├─────────────────────────────────────────────────────────────────┤
│  BUILDERS (7)        REVIEWERS (3)         OPS (2)              │
│  ├── builder-1       ├── reviewer-1        ├── ops-1            │
│  ├── builder-2       ├── reviewer-2        ├── ops-2            │
│  ├── builder-3       └── reviewer-3                           │
│  ├── builder-4                                                │
│  ├── builder-5                                                │
│  ├── builder-6                                                │
│  └── builder-7                                                │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   SERVICE LAYER                                 │
├─────────────────────────────────────────────────────────────────┤
│  MT5 Core Server  │  Dashboard  │  Trading Robots  │  Database │
│  Port 8001        │  Port 8001  │  V31/V32/V33     │  Postgres │
└─────────────────────────────────────────────────────────────────┘
```

## Communication Flow

### 1. Task Assignment Flow
```
User Request
    ↓
Orchestrator consults → Project Brain
    ↓
Project Brain analyzes current state
    ↓
Returns: {gaps, next_steps, risks}
    ↓
Orchestrator assigns to Agent
    ↓
Agent executes
    ↓
Agent reports completion
    ↓
Project Brain updates state
    ↓
QA validates
```

### 2. Hook Event Flow
```
Event triggers (gateway:startup, command:new, etc.)
    ↓
OpenClaw Hook System
    ↓
Handler executes (TypeScript)
    ↓
Updates Task Board / Notifies Agents
    ↓
Logs to audit trail
```

### 3. Data Flow
```
MT5 Terminal → VPS Bridge (8080/7001) → MT5 Core Server
                                               ↓
Dashboard ← API Endpoints ← PostgreSQL Database
    ↓
User Interface (Real-time updates)
```

## API Architecture

### V31 - Marius TPL
```
GET /api/v31/live_status
Response: {
  status: "success",
  analyzed_count: 28,
  setups_count: 0,
  rejected_count: 28,
  phase: "Waiting...",
  progress: 0
}
```

### V32 - London Breakout
```
GET /api/v32/or_data
GET /api/v32/asia_data
GET /api/v32/breakout_status
GET /api/v32/trade_stats
```

### V33 - NY Breakout
```
GET /api/v33/or_data?symbol=EURUSD
GET /api/v33/presession_data?symbol=EURUSD
GET /api/v33/breakout_status
GET /api/v33/trade_stats
```

## Database Schema

### Core Tables
- `v32_symbol_status` - V32 robot state
- `v33_symbol_status` - V33 robot state
- `closed_positions` - Trade history
- `open_positions` - Active trades
- `ohlc_data` - Market data
- `robot_logs` - System logs

## File Structure

```
/workspace/shared/
├── memory/
│   ├── project/
│   │   └── project_state.json      # ← Single source of truth
│   ├── architecture/
│   │   └── architecture.md         # ← This file
│   ├── features/
│   │   └── features.json           # ← Feature registry
│   ├── files_index/
│   │   └── files_index.json        # ← File registry
│   ├── decisions/
│   │   └── decisions.md            # ← Decision log
│   └── versions/
│       └── v2.0.0.md               # ← Version history
│
├── config/
│   ├── team_orchestration.json     # Agent definitions
│   └── agent_status.json           # Live status
│
├── tasks/
│   └── TASKBOARD.json              # Task management
│
└── bugs/                           # Bug reports
```

## Technology Stack

### Backend
- **Python 3.10+** - Core logic
- **Flask** - API framework
- **PostgreSQL** - Database
- **MT5 via metaquotes** - Trading integration

### Frontend
- **JavaScript ES6+** - No framework
- **CSS3** - Styling
- **HTML5** - Markup

### Infrastructure
- **OpenClaw** - Agent orchestration
- **TypeScript Hooks** - Event handling
- **Cron Jobs** - Scheduling

## Design Patterns

### 1. Execute-Verify-Report
Every task must:
1. **Execute** - Do the work
2. **Verify** - Confirm result (file exists, API responds)
3. **Report** - Document what was done

### 2. Project Brain Pattern
Before any modification:
1. Orchestrator asks Project Brain
2. Project Brain checks current state
3. Identifies gaps and risks
4. Returns structured plan
5. Orchestrator assigns tasks
6. Project Brain updates state after completion

### 3. Hook-Driven Automation
- Events trigger hooks
- Hooks execute handlers
- Handlers update state
- State changes trigger notifications

## Security Considerations

- File locks prevent concurrent modifications
- API authentication via Bearer tokens
- No secrets in code (use environment variables)
- Review gates for all changes

## Performance

- Polling intervals:
  - V31: 5 seconds
  - V32/V33: 1 second
  - Health check: 10 seconds
  - Agent status: 5 seconds

## Future Evolution

### Planned Features
- V34 Tokyo Breakout Robot
- Advanced risk management
- Machine learning integration
- Mobile app

### Scalability
- Current: 3 robots, 13 agents
- Target: 10+ robots, 25+ agents
- Architecture supports horizontal scaling

## Last Updated
2026-03-28 by Project Brain v1.0