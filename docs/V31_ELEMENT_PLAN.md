# V31 Dashboard - Plan Complet pentru Fiecare Element

> Documentație tehnică detaliată pentru toate elementele din dashboard-ul V31
> Versiune: 1.0.0
> Data: 2026-03-28

---

## 📋 Cuprins

1. [Buton START](#1-buton-start)
2. [Buton STOP](#2-buton-stop)
3. [Status Badge](#3-status-badge)
4. [Analiză Live](#4-analiză-live)
5. [Log-uri](#5-log-uri)
6. [Simboluri](#6-simboluri)
7. [Diagramă Flux Date](#7-diagrma-flux-date)
8. [API Reference](#8-api-reference)

---

## 1. Buton START

### 1.1 Ce Face
Pornește robotul de trading V31 TPL (Trailing Stop Loss) pe serverul MT5.

### 1.2 Flow Complet

```
┌─────────────────┐     POST /api/robot/v31_tpl/start      ┌─────────────────┐
│   Dashboard     │ ──────────────────────────────────────> │  mt5_core_server │
│   (UI Button)   │                                       │    (Flask API)   │
└─────────────────┘                                       └────────┬────────┘
                                                                   │
                                                                   ▼
                                                          ┌─────────────────┐
                                                          │  Validare request│
                                                          │  - Check if already
                                                          │    running       │
                                                          └────────┬────────┘
                                                                   │
                                                                   ▼
                                                          ┌─────────────────┐
                                                          │  subprocess.Popen │
                                                          │  v31_tpl_main.py │
                                                          └────────┬────────┘
                                                                   │
                                                                   ▼
                                                          ┌─────────────────┐
                                                          │  Proces Python   │
                                                          │  Robot V31 Rulează│
                                                          └─────────────────┘
```

### 1.3 Detalii Tehnice

| Proprietate | Valoare |
|-------------|---------|
| **Metodă HTTP** | POST |
| **Endpoint** | `/api/robot/v31_tpl/start` |
| **Fișier Handler** | `mt5_core_server.py` → `start_v31_tpl()` |
| **Proces Pornit** | `v31_tpl_main.py` |
| **Metodă Proces** | `subprocess.Popen` cu `nohup` |

### 1.4 Request/Response

**Request:**
```bash
curl -X POST http://localhost:5000/api/robot/v31_tpl/start
```

**Response Success (200):**
```json
{
  "status": "success",
  "message": "Robot V31 TPL started successfully",
  "pid": 12345,
  "started_at": "2026-03-28T18:16:00Z"
}
```

**Response Error (409):**
```json
{
  "status": "error",
  "message": "Robot already running",
  "pid": 12345
}
```

### 1.5 Stări Dashboard

| Stare | Culoare | Text |
|-------|---------|------|
| Înainte de click | Verde | "START" |
| După click (loading) | Galben | "Starting..." |
| Succes | Verde (disabled) | "Running" |
| Eroare | Roșu | "Error" |

### 1.6 Cod Relevant (mt5_core_server.py)

```python
@app.route('/api/robot/v31_tpl/start', methods=['POST'])
def start_v31_tpl():
    """Start V31 TPL robot process"""
    global v31_process
    
    if v31_process and v31_process.poll() is None:
        return jsonify({
            "status": "error",
            "message": "Robot already running",
            "pid": v31_process.pid
        }), 409
    
    try:
        v31_process = subprocess.Popen(
            ['python3', 'v31_tpl_main.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True
        )
        
        return jsonify({
            "status": "success",
            "message": "Robot V31 TPL started",
            "pid": v31_process.pid
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
```

---

## 2. Buton STOP

### 2.1 Ce Face
Oprește robotul de trading V31 TPL în mod controlat.

### 2.2 Flow Complet

```
┌─────────────────┐     POST /api/robot/v31_tpl/stop       ┌─────────────────┐
│   Dashboard     │ ──────────────────────────────────────> │  mt5_core_server │
│   (UI Button)   │                                       │    (Flask API)   │
└─────────────────┘                                       └────────┬────────┘
                                                                   │
                                                                   ▼
                                                          ┌─────────────────┐
                                                          │  Validare request│
                                                          │  - Check if running
                                                          └────────┬────────┘
                                                                   │
                                                                   ▼
                                                          ┌─────────────────┐
                                                          │  v31_process.terminate()
                                                          │  Sau SIGTERM/SIGKILL
                                                          └────────┬────────┘
                                                                   │
                                                                   ▼
                                                          ┌─────────────────┐
                                                          │  Proces Oprit    │
                                                          │  Robot V31 Stop  │
                                                          └─────────────────┘
```

### 2.3 Detalii Tehnice

| Proprietate | Valoare |
|-------------|---------|
| **Metodă HTTP** | POST |
| **Endpoint** | `/api/robot/v31_tpl/stop` |
| **Fișier Handler** | `mt5_core_server.py` → `stop_v31_tpl()` |
| **Metodă Stop** | `process.terminate()` → `process.kill()` (fallback) |
| **Timeout Graceful** | 5 secunde |

### 2.4 Request/Response

**Request:**
```bash
curl -X POST http://localhost:5000/api/robot/v31_tpl/stop
```

**Response Success (200):**
```json
{
  "status": "success",
  "message": "Robot V31 TPL stopped successfully",
  "stopped_at": "2026-03-28T18:20:00Z"
}
```

**Response Error (400):**
```json
{
  "status": "error",
  "message": "Robot not running"
}
```

### 2.5 Stări Dashboard

| Stare | Culoare | Text |
|-------|---------|------|
| Înainte de click | Roșu | "STOP" |
| După click (loading) | Portocaliu | "Stopping..." |
| Succes | Gri (disabled) | "Stopped" |

### 2.6 Cod Relevant (mt5_core_server.py)

```python
@app.route('/api/robot/v31_tpl/stop', methods=['POST'])
def stop_v31_tpl():
    """Stop V31 TPL robot process"""
    global v31_process
    
    if not v31_process or v31_process.poll() is not None:
        return jsonify({
            "status": "error",
            "message": "Robot not running"
        }), 400
    
    try:
        # Graceful shutdown
        v31_process.terminate()
        
        # Wait up to 5 seconds
        v31_process.wait(timeout=5)
        
        return jsonify({
            "status": "success",
            "message": "Robot V31 TPL stopped"
        })
    except subprocess.TimeoutExpired:
        # Force kill
        v31_process.kill()
        return jsonify({
            "status": "success",
            "message": "Robot V31 TPL force stopped"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
```

---

## 3. Status Badge

### 3.1 Ce Face
Afișează starea curentă a robotului V31 (Running/Stopped/Error).

### 3.2 Flow Date

```
┌─────────────────┐     GET /api/robots (polling 10s)      ┌─────────────────┐
│   Dashboard     │ <────────────────────────────────────── │  mt5_core_server │
│  (Status Badge) │                                       │    (Flask API)   │
└────────┬────────┘                                       └─────────────────┘
         │
         ▼
┌─────────────────┐
│  Update UI      │
│  - Culoare badge│
│  - Text status  │
│  - Iconiță      │
└─────────────────┘
```

### 3.3 Detalii Tehnice

| Proprietate | Valoare |
|-------------|---------|
| **Metodă HTTP** | GET |
| **Endpoint** | `/api/robots` |
| **Polling Interval** | 10 secunde |
| **Fișier Sursă** | `mt5_core_server.py` |

### 3.4 Response Format

```json
{
  "robots": [
    {
      "id": "v31_tpl",
      "name": "V31 TPL",
      "status": "running",
      "pid": 12345,
      "started_at": "2026-03-28T18:16:00Z",
      "uptime_seconds": 240
    }
  ]
}
```

### 3.5 Mapare Stări UI

| Status API | Culoare Badge | Text Afișat | Iconiță |
|------------|---------------|-------------|---------|
| `running` | Verde (`#22c55e`) | "Running" | 🟢 |
| `stopped` | Gri (`#6b7280`) | "Stopped" | ⚫ |
| `error` | Roșu (`#ef4444`) | "Error" | 🔴 |
| `starting` | Galben (`#f59e0b`) | "Starting..." | 🟡 |
| `stopping` | Portocaliu (`#f97316`) | "Stopping..." | 🟠 |

### 3.6 Implementare Frontend (React/Vue)

```javascript
// Polling hook
useEffect(() => {
  const fetchStatus = async () => {
    const response = await fetch('/api/robots');
    const data = await response.json();
    setRobotStatus(data.robots.find(r => r.id === 'v31_tpl'));
  };
  
  fetchStatus();
  const interval = setInterval(fetchStatus, 10000); // 10s polling
  
  return () => clearInterval(interval);
}, []);

// Badge component
const StatusBadge = ({ status }) => {
  const config = {
    running: { color: '#22c55e', text: 'Running', icon: '🟢' },
    stopped: { color: '#6b7280', text: 'Stopped', icon: '⚫' },
    error:   { color: '#ef4444', text: 'Error',   icon: '🔴' }
  };
  
  const { color, text, icon } = config[status] || config.stopped;
  
  return (
    <span style={{ backgroundColor: color, color: 'white', padding: '4px 12px', borderRadius: '12px' }}>
      {icon} {text}
    </span>
  );
};
```

---

## 4. Analiză Live

### 4.1 Ce Face
Afișează progresul analizei în timp real, contoare și scoruri pentru fiecare simbol.

### 4.2 Componente

#### 4.2.1 Progress Bar
- **Sursă**: `/api/v31/live_status` → `progress`
- **Valoare**: 0-100%
- **Update**: Real-time polling (5 secunde)

#### 4.2.2 Contoare
- **Sursă**: `/api/v31/live_status` → `analyzed_count`, `setups_count`
- **Afișare**: "X / Y simboluri analizate"
- **Setup-uri**: Număr de oportunități găsite

#### 4.2.3 Scoruri
- **Sursă**: `/api/v31/live_status` → `scores`
- **Structură**: Array de obiecte `{symbol, score, direction}`
- **Sortare**: După scor descrescător

### 4.3 Flow Date

```
┌─────────────────┐     GET /api/v31/live_status         ┌─────────────────┐
│   Dashboard     │ <──────────────────────────────────── │  mt5_core_server │
│  (Live Analysis)│    (polling 5s)                       │    (Flask API)   │
└────────┬────────┘                                       └────────┬────────┘
         │                                                         │
         │                                                         ▼
         │                                                ┌─────────────────┐
         │                                                │  v31_tpl_main.py │
         │                                                │  - Analizează    │
         │                                                │  - Calculează    │
         │                                                │    scoruri       │
         │                                                └────────┬────────┘
         │                                                         │
         │                                                         ▼
         │                                                ┌─────────────────┐
         │                                                │  Shared State    │
         │                                                │  (memorie/DB)    │
         │                                                └─────────────────┘
         ▼
┌─────────────────┐
│  Update UI:     │
│  - Progress bar │
│  - Contoare     │
│  - Lista scoruri│
└─────────────────┘
```

### 4.4 API Response Format

```json
{
  "status": "analyzing",
  "progress": 65.5,
  "analyzed_count": 21,
  "total_symbols": 32,
  "setups_count": 3,
  "current_symbol": "EURUSD",
  "scores": [
    {
      "symbol": "EURUSD",
      "score": 85.5,
      "direction": "BUY",
      "confidence": 0.82,
      "timestamp": "2026-03-28T18:16:00Z"
    },
    {
      "symbol": "GBPUSD",
      "score": 72.3,
      "direction": "SELL",
      "confidence": 0.75,
      "timestamp": "2026-03-28T18:15:55Z"
    }
  ],
  "last_updated": "2026-03-28T18:16:05Z"
}
```

### 4.5 Componente UI

#### Progress Bar
```javascript
const ProgressBar = ({ progress }) => (
  <div style={{ width: '100%', backgroundColor: '#e5e7eb', borderRadius: '8px' }}>
    <div 
      style={{ 
        width: `${progress}%`, 
        backgroundColor: progress === 100 ? '#22c55e' : '#3b82f6',
        height: '20px',
        borderRadius: '8px',
        transition: 'width 0.5s ease'
      }}
    />
    <span>{progress.toFixed(1)}%</span>
  </div>
);
```

#### Tabel Scoruri
```javascript
const ScoresTable = ({ scores }) => (
  <table>
    <thead>
      <tr>
        <th>Simbol</th>
        <th>Scor</th>
        <th>Direcție</th>
        <th>Încredere</th>
      </tr>
    </thead>
    <tbody>
      {scores.map(score => (
        <tr key={score.symbol}>
          <td>{score.symbol}</td>
          <td>{score.score.toFixed(1)}</td>
          <td style={{ color: score.direction === 'BUY' ? 'green' : 'red' }}>
            {score.direction}
          </td>
          <td>{(score.confidence * 100).toFixed(0)}%</td>
        </tr>
      ))}
    </tbody>
  </table>
);
```

### 4.6 Configurare Polling

| Parametru | Valoare | Motivație |
|-----------|---------|-----------|
| Interval | 5 secunde | Echilibru între freshness și load |
| Timeout | 3 secunde | Prevenire blocking |
| Retry | 3 încercări | Reziliență la erori de rețea |

---

## 5. Log-uri

### 5.1 Ce Face
Afișează log-urile robotului V31 cu posibilitate de filtrare.

### 5.2 Sursă Date

| Proprietate | Valoare |
|-------------|---------|
| **Sursă** | Database table `robot_logs` |
| **Endpoint** | `/api/robot_logs` |
| **Metodă** | GET |
| **Fișier Handler** | `mt5_core_server.py` |

### 5.3 Schema Tabelă `robot_logs`

```sql
CREATE TABLE robot_logs (
    id SERIAL PRIMARY KEY,
    robot_id VARCHAR(50) NOT NULL,
    level VARCHAR(20) NOT NULL,        -- DEBUG, INFO, WARNING, ERROR
    message TEXT NOT NULL,
    symbol VARCHAR(20),                 -- Opțional, pentru log-uri specifice
    metadata JSONB,                     -- Date suplimentare
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_robot_logs_robot ON robot_logs(robot_id);
CREATE INDEX idx_robot_logs_level ON robot_logs(level);
CREATE INDEX idx_robot_logs_created ON robot_logs(created_at DESC);
```

### 5.4 API Endpoint

#### Request
```bash
# Toate log-urile V31
curl "http://localhost:5000/api/robot_logs?robot_id=v31_tpl&limit=100"

# Doar erori
curl "http://localhost:5000/api/robot_logs?robot_id=v31_tpl&level=ERROR&limit=50"

# Log-uri pentru simbol specific
curl "http://localhost:5000/api/robot_logs?robot_id=v31_tpl&symbol=EURUSD"

# Log-uri din ultimele 24 ore
curl "http://localhost:5000/api/robot_logs?robot_id=v31_tpl&hours=24"
```

#### Query Parameters

| Parametru | Tip | Descriere | Default |
|-----------|-----|-----------|---------|
| `robot_id` | string | ID robot (v31_tpl) | required |
| `level` | string | Filtru nivel (DEBUG/INFO/WARNING/ERROR) | all |
| `symbol` | string | Filtru simbol | all |
| `limit` | int | Număr maxim log-uri | 100 |
| `offset` | int | Offset pentru paginare | 0 |
| `hours` | int | Log-uri din ultimele N ore | all |
| `search` | string | Căutare în mesaj | none |

#### Response

```json
{
  "logs": [
    {
      "id": 1234,
      "robot_id": "v31_tpl",
      "level": "INFO",
      "message": "Analiză completă pentru EURUSD",
      "symbol": "EURUSD",
      "metadata": {
        "score": 85.5,
        "direction": "BUY"
      },
      "created_at": "2026-03-28T18:16:00Z"
    },
    {
      "id": 1233,
      "robot_id": "v31_tpl",
      "level": "ERROR",
      "message": "Eroare conexiune MT5",
      "symbol": null,
      "metadata": {
        "error_code": 500,
        "retry_count": 3
      },
      "created_at": "2026-03-28T18:15:30Z"
    }
  ],
  "total": 2456,
  "limit": 100,
  "offset": 0
}
```

### 5.5 Componente UI

#### Log Viewer
```javascript
const LogViewer = () => {
  const [logs, setLogs] = useState([]);
  const [filters, setFilters] = useState({
    level: 'all',
    search: '',
    limit: 100
  });
  
  useEffect(() => {
    fetchLogs();
    const interval = setInterval(fetchLogs, 5000);
    return () => clearInterval(interval);
  }, [filters]);
  
  const fetchLogs = async () => {
    const params = new URLSearchParams({
      robot_id: 'v31_tpl',
      ...filters
    });
    const response = await fetch(`/api/robot_logs?${params}`);
    const data = await response.json();
    setLogs(data.logs);
  };
  
  return (
    <div>
      {/* Filtre */}
      <select onChange={e => setFilters({...filters, level: e.target.value})}>
        <option value="all">Toate</option>
        <option value="DEBUG">Debug</option>
        <option value="INFO">Info</option>
        <option value="WARNING">Warning</option>
        <option value="ERROR">Error</option>
      </select>
      
      {/* Lista log-uri */}
      <div className="log-container">
        {logs.map(log => (
          <div key={log.id} className={`log-line log-${log.level.toLowerCase()}`}>
            <span className="timestamp">{new Date(log.created_at).toLocaleTimeString()}</span>
            <span className={`level-badge level-${log.level.toLowerCase()}`}>
              {log.level}
            </span>
            {log.symbol && <span className="symbol">[{log.symbol}]</span>}
            <span className="message">{log.message}</span>
          </div>
        ))}
      </div>
    </div>
  );
};
```

### 5.6 Stiluri Log-uri

| Nivel | Culoare | Background | Iconiță |
|-------|---------|------------|---------|
| DEBUG | `#6b7280` | `#f3f4f6` | 🔍 |
| INFO | `#3b82f6` | `#eff6ff` | ℹ️ |
| WARNING | `#f59e0b` | `#fffbeb` | ⚠️ |
| ERROR | `#ef4444` | `#fef2f2` | ❌ |

---

## 6. Simboluri

### 6.1 Ce Face
Afișează lista celor 32 simboluri monitorizate și statusul lor.

### 6.2 Lista Simboluri V31 (32)

| # | Simbol | # | Simbol | # | Simbol | # | Simbol |
|---|--------|---|--------|---|--------|---|--------|
| 1 | EURUSD | 9 | AUDUSD | 17 | EURAUD | 25 | CADJPY |
| 2 | GBPUSD | 10 | NZDUSD | 18 | EURNZD | 26 | CHFJPY |
| 3 | USDJPY | 11 | EURGBP | 19 | GBPAUD | 27 | NZDJPY |
| 4 | USDCHF | 12 | EURCHF | 20 | GBPNZD | 28 | AUDJPY |
| 5 | AUDCAD | 13 | EURJPY | 21 | AUDCHF | 29 | EURCAD |
| 6 | AUDNZD | 14 | GBPJPY | 22 | NZDCHF | 30 | GBPCAD |
| 7 | USDCAD | 15 | GBPCHF | 23 | CADCHF | 31 | XAUUSD |
| 8 | EURCHF | 16 | AUDCAD | 24 | NZDCAD | 32 | XAGUSD |

### 6.3 API Endpoint

#### GET /api/v31/symbol_status

**Request:**
```bash
curl "http://localhost:5000/api/v31/symbol_status"
```

**Response:**
```json
{
  "symbols": [
    {
      "symbol": "EURUSD",
      "status": "active",
      "last_analyzed": "2026-03-28T18:16:00Z",
      "last_price": 1.0856,
      "spread": 0.0001,
      "analyzed_today": true,
      "setup_found": true,
      "score": 85.5,
      "direction": "BUY"
    },
    {
      "symbol": "GBPUSD",
      "status": "active",
      "last_analyzed": "2026-03-28T18:15:55Z",
      "last_price": 1.2647,
      "spread": 0.0002,
      "analyzed_today": true,
      "setup_found": false,
      "score": 45.2,
      "direction": null
    },
    {
      "symbol": "USDJPY",
      "status": "disabled",
      "last_analyzed": null,
      "last_price": null,
      "spread": null,
      "analyzed_today": false,
      "setup_found": false,
      "score": null,
      "direction": null
    }
  ],
  "total": 32,
  "active": 31,
  "analyzed_today": 21,
  "with_setups": 3
}
```

### 6.4 Stări Simbol

| Status | Descriere | Culoare |
|--------|-----------|---------|
| `active` | Simbol activ și analizat | Verde |
| `analyzing` | Se analizează acum | Galben (puls) |
| `waiting` | Așteaptă analiză | Gri |
| `disabled` | Deactivat în config | Roșu deschis |
| `error` | Eroare la analiză | Roșu |

### 6.5 Componente UI

#### Grid Simboluri
```javascript
const SymbolGrid = ({ symbols }) => (
  <div className="symbol-grid">
    {symbols.map(sym => (
      <div key={sym.symbol} className={`symbol-card status-${sym.status}`}>
        <div className="symbol-header">
          <span className="symbol-name">{sym.symbol}</span>
          <span className={`status-dot status-${sym.status}`} />
        </div>
        
        {sym.last_price && (
          <div className="symbol-price">
            {sym.last_price.toFixed(5)}
          </div>
        )}
        
        {sym.score && (
          <div className="symbol-score">
            <div 
              className="score-bar" 
              style={{ width: `${sym.score}%` }}
            />
            <span>{sym.score.toFixed(1)}</span>
          </div>
        )}
        
        {sym.direction && (
          <div className={`direction-badge direction-${sym.direction.toLowerCase()}`}>
            {sym.direction === 'BUY' ? '📈' : '📉'} {sym.direction}
          </div>
        )}
        
        {sym.setup_found && (
          <div className="setup-badge">
            💡 Setup detectat
          </div>
        )}
      </div>
    ))}
  </div>
);
```

### 6.6 Configurare Simboluri

```python
# v31_config.py
V31_SYMBOLS = [
    "EURUSD", "GBPUSD", "USDJPY", "USDCHF",
    "AUDCAD", "AUDNZD", "USDCAD", "EURCHF",
    "AUDUSD", "NZDUSD", "EURGBP", "EURCHF",
    "EURJPY", "GBPJPY", "GBPCHF", "AUDCAD",
    "EURAUD", "EURNZD", "GBPAUD", "GBPNZD",
    "AUDCHF", "NZDCHF", "CADCHF", "NZDCAD",
    "CADJPY", "CHFJPY", "NZDJPY", "AUDJPY",
    "EURCAD", "GBPCAD", "XAUUSD", "XAGUSD"
]

V31_SYMBOLS_ACTIVE = V31_SYMBOLS  # Toate active
# V31_SYMBOLS_ACTIVE = ["EURUSD", "GBPUSD"]  # Doar subset
```

---

## 7. Diagramă Flux Date

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           V31 DASHBOARD                                      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│  │  START   │ │   STOP   │ │  STATUS  │ │  LIVE    │ │   LOGS   │          │
│  │  Button  │ │  Button  │ │  Badge   │ │ Analysis │ │  Viewer  │          │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘          │
└───────┼────────────┼────────────┼────────────┼────────────┼────────────────┘
        │            │            │            │            │
        │ POST /start│ POST /stop │ GET /robots│ GET /live  │ GET /logs
        │            │            │(poll 10s)  │ (poll 5s)  │ (poll 5s)
        ▼            ▼            ▼            ▼            ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        mt5_core_server.py (Flask)                           │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │                    API Routes                                           ││
│  │  /api/robot/v31_tpl/start    → start_v31_tpl()                          ││
│  │  /api/robot/v31_tpl/stop     → stop_v31_tpl()                           ││
│  │  /api/robots                 → get_robot_status()                       ││
│  │  /api/v31/live_status        → get_live_status()                        ││
│  │  /api/v31/symbol_status      → get_symbol_status()                      ││
│  │  /api/robot_logs             → get_robot_logs()                         ││
│  └─────────────────────────────────────────────────────────────────────────┘│
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
              ▼                  ▼                  ▼
    ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
    │  v31_tpl_main.py│ │   Database      │ │   MT5 Terminal  │
    │  (Subprocess)   │ │   (PostgreSQL)  │ │   (MetaTrader)  │
    │                 │ │                 │ │                 │
    │  - Analizează   │ │  robot_logs     │ │  - Prețuri      │
    │    simboluri    │ │  robot_status   │ │  - Execuție     │
    │  - Calculează   │ │  symbol_data    │ │    ordere       │
    │    scoruri      │ │                 │ │                 │
    │  - Loghează     │ │                 │ │                 │
    └─────────────────┘ └─────────────────┘ └─────────────────┘
```

---

## 8. API Reference

### 8.1 Sumar Endpoints

| Endpoint | Metodă | Descriere | Polling |
|----------|--------|-----------|---------|
| `/api/robot/v31_tpl/start` | POST | Pornește robot | - |
| `/api/robot/v31_tpl/stop` | POST | Oprește robot | - |
| `/api/robots` | GET | Status roboți | 10s |
| `/api/v31/live_status` | GET | Status analiză live | 5s |
| `/api/v31/symbol_status` | GET | Status simboluri | 5s |
| `/api/robot_logs` | GET | Log-uri robot | 5s |

### 8.2 Coduri Eroare

| Cod | Semnificație | Când apare |
|-----|--------------|------------|
| 200 | OK | Succes |
| 400 | Bad Request | Parametri invalizi |
| 404 | Not Found | Robot/simbol inexistent |
| 409 | Conflict | Robot deja rulează/oprit |
| 500 | Internal Error | Eroare server |
| 503 | Service Unavailable | MT5 deconectat |

### 8.3 Configurare CORS

```python
# mt5_core_server.py
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "https://dashboard.example.com"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})
```

---

## 9. Checklist Implementare

### 9.1 Backend (mt5_core_server.py)
- [ ] Endpoint `/api/robot/v31_tpl/start` implementat
- [ ] Endpoint `/api/robot/v31_tpl/stop` implementat
- [ ] Endpoint `/api/robots` implementat
- [ ] Endpoint `/api/v31/live_status` implementat
- [ ] Endpoint `/api/v31/symbol_status` implementat
- [ ] Endpoint `/api/robot_logs` implementat
- [ ] Gestionare proceselor cu `subprocess`
- [ ] Logging în database

### 9.2 Frontend (Dashboard)
- [ ] Buton START cu loading state
- [ ] Buton STOP cu loading state
- [ ] Status Badge cu polling 10s
- [ ] Progress Bar pentru analiză
- [ ] Contoare analyzed_count, setups_count
- [ ] Tabel scoruri cu sortare
- [ ] Log Viewer cu filtre
- [ ] Grid simboluri 32
- [ ] Error handling și retry logic

### 9.3 Robot (v31_tpl_main.py)
- [ ] Scriere status în memorie/DB
- [ ] Logging în tabela robot_logs
- [ ] Update progress în timp real
- [ ] Calcul scoruri pentru fiecare simbol

---

## 10. Note Importante

### 10.1 Securitate
- Toate endpoint-urile să valideze input
- Rate limiting pentru prevenire abuse
- Autentificare JWT pentru producție

### 10.2 Performance
- Polling adaptiv (mai lent când robot e oprit)
- Debounce pentru butoane
- Virtual scrolling pentru log-uri lungi

### 10.3 Debugging
- Log level DEBUG pentru development
- Console logs pentru erori API
- Network tab pentru monitoring request-uri

---

**Document creat:** 2026-03-28  
**Versiune:** 1.0.0  
**Autor:** Task Critic - Plan Complet  
**Fișier:** `/workspace/shared/docs/V31_ELEMENT_PLAN.md`
