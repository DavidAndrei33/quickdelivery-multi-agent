# PLAN COMPLET TESTARE - Sincronizare Totală Dashboard
## Data: 2026-03-28 | Versiune: 2.0

---

## 🎯 OBIECTIV

Sincronizare perfectă între:
```
Frontend (Browser) 
    ↕ (HTTP/WebSocket)
Backend API (MT5 Core Server - Port 8001)
    ↕ (SQL/PostgreSQL)
Database (mt5_core - Tabele: robot_logs, symbol_analysis, position_tracking, clients)
    ↕ (Python/Subprocess)
Roboți Trading (V31, V32, V33 - Procese Python)
    ↕ (ZeroMQ/Sockets)
MT5 Platform (EA BrainBridge - Port 8001)
```

---

## 📊 ARHITECTURA DATElor

### 1. FLOW DATE - CLIENȚI

```
EA BrainBridge (MT5)
    ↓ POST /update (la fiecare 5 secunde)
MT5 Core Server
    ↓ INSERT/UPDATE PostgreSQL (clients_cache)
    ↓ GET /api/clients
Dashboard (JavaScript)
    ↓ Render tabel
Utilizator vede date actualizate
```

**Teste necesare:**
- [ ] EA trimite date la /update
- [ ] Server salvează în PostgreSQL
- [ ] Server răspunde la /api/clients cu date JSON
- [ ] Dashboard face polling la 10 secunde
- [ ] Tabelul se updatează automat
- [ ] Toggle on/off persistă în DB

---

### 2. FLOW DATE - POZIȚII ACTIVE

```
EA BrainBridge (MT5)
    ↓ Poziții deschise în MT5
    ↓ POST /update cu positions[]
MT5 Core Server
    ↓ Salvează în clients_cache[login].positions
    ↓ GET /api/open_positions
Dashboard
    ↓ Polling 5 secunde
    ↓ Render tabel poziții
    ↓ Calcul profit curent (bid - open_price)
```

**Teste necesare:**
- [ ] Poziție deschisă în MT5 → apare în dashboard în 5 sec
- [ ] Preț curent se updatează (bid din market_prices)
- [ ] Profit calculat corect: (bid - open) * volume * contract_size
- [ ] Buton "Închide" trimite POST /close_position
- [ ] Poziție închisă dispare din tabel
- [ ] Profit final salvat în istoric

---

### 3. FLOW DATE - ISTORIC TRANZACȚII

```
EA BrainBridge
    ↓ Poziție închisă în MT5
    ↓ POST /update cu history[]
MT5 Core Server
    ↓ INSERT INTO position_tracking (tabel istoric)
    ↓ GET /api/history
Dashboard
    ↓ Polling 30 secunde
    ↓ Render tabel cu: ticket, data, symbol, profit, comision, durată
```

**Teste necesare:**
- [ ] Tranzacție închisă → apare în istoric în 30 sec
- [ ] Calcul durată: close_time - open_time
- [ ] Calcul profit net: profit - commission - swap
- [ ] Calcul R:R (Risk:Reward) corect
- [ ] Filtre perioadă/symbol/profit funcționale

---

### 4. FLOW DATE - TRACKING TRANZACȚII

```
position_tracking table (DB)
    ↓ opened_by, closed_by, modified_by (robot sau manual)
    ↓ GET /api/tracking (din history)
Dashboard
    ↓ Polling 5 secunde
    ↓ Afișează cine a deschis/închis/modificat
```

**Teste necesare:**
- [ ] opened_by populat (robot sau user)
- [ ] closed_by populat corect
- [ ] modification_history prezent
- [ ] Status colorat: Deschis/Închis/Modificat

---

### 5. FLOW DATE - ROBOȚI V31 MARIUS TPL

```
v31_marius_tpl_robot.py (Proces Python)
    ↓ Analizează 32 simboluri
    ↓ Scrie în robot_logs (lifecycle, cycle, symbol, setup, trade)
    ↓ Scrie în symbol_analysis (detalii per simbol)
    ↓ Deschide trades în MT5 (via MT5 Core)
MT5 Core Server
    ↓ GET /api/robot_logs?robot=v31_tpl
    ↓ GET /api/v31/live_status
    ↓ GET /api/v31/symbol_status
Dashboard
    ↓ Polling: logs 30s, live_status 5s, symbols 3s
    ↓ Render: logs tabel, analiză live, grid simboluri
```

**Teste necesare:**

#### 5.1 START/STOP Robot
- [ ] Click START → POST /api/robot/v31_tpl/start
- [ ] Server pornește proces Python: `python3 v31_marius_tpl_robot.py`
- [ ] PID salvat în DB
- [ ] Status Badge devine "🟢 Running" în 2 secunde
- [ ] Click STOP → POST /api/robot/v31_tpl/stop
- [ ] Server trimite SIGTERM la PID
- [ ] Procesul se oprește gracefully
- [ ] Status Badge devine "🔴 Stopped" în 2 secunde

#### 5.2 Analiză Live
- [ ] Robot analizează EURUSD → apare "Analizat: 1/32"
- [ ] Scoruri calculate: RSI, Stoch, Fib, Total
- [ ] Setup găsit → "Setups: 1", setup afișat în listă
- [ ] Progress bar: 0% → 100% în timpul ciclului
- [ ] Faza afișată: "Analiză în curs..." → "Ciclu complet"
- [ ] Simbol curent afișat în timp real

#### 5.3 Log-uri Robot
- [ ] Robot scrie log în DB: "Ciclu analiză început"
- [ ] Log apare în tabel în 30 secunde
- [ ] Filtre funcționale: lifecycle, cycle, symbol, setup, trade
- [ ] Nivel log colorat: INFO (verde), WARNING (galben), ERROR (roșu)
- [ ] Căutare în log-uri funcțională

#### 5.4 Grid Simboluri 32
- [ ] Toate 32 simboluri afișate
- [ ] Status colorat per simbol:
  - 🟢 Verde = Analizat, fără setup
  - 🟡 Galben = Setup găsit
  - 🔴 Roșu = Trade deschis
  - ⚪ Gri = Pending (nefiind analizat)
- [ ] Click pe simbol → modal cu detalii analiză
- [ ] Refresh la 3 secunde

---

### 6. FLOW DATE - ROBOȚI V32 LONDON BREAKOUT

```
v32_london_breakout_robot.py
    ↓ Calculează OR (Opening Range) 08:00-08:15 London
    ↓ Calculează Asia session 00:00-08:00
    ↓ Detectează breakout
    ↓ Scrie în DB
MT5 Core Server
    ↓ GET /api/v32/session_status
    ↓ GET /api/v32/or_data
    ↓ GET /api/v32/asia_data
    ↓ GET /api/v32/breakout_status
Dashboard
    ↓ Polling 1 secundă
    ↓ Afișează: London Time, Session Timer, OR, Asia, Breakout
```

**Teste necesare:**

#### 6.1 London Time & Timer
- [ ] Ora Londra afișată corect (timezone Europe/London)
- [ ] Update la fiecare secundă
- [ ] Timer countdown până la sesiune corect
- [ ] Fazele sesiunii: BEFORE_SESSION → OPENING_RANGE → MAIN_SESSION → EXTENDED

#### 6.2 Opening Range (OR)
- [ ] OR High = max(high 3 candles 08:00-08:15)
- [ ] OR Low = min(low 3 candles 08:00-08:15)
- [ ] OR Range = OR High - OR Low
- [ ] Current Price = preț live
- [ ] Update la fiecare tick sau 5 secunde

#### 6.3 Asia Session
- [ ] Asia High = max(high 00:00-08:00)
- [ ] Asia Low = min(low 00:00-08:00)
- [ ] Compression status: < 40 pips sau < 50% OR

#### 6.4 Breakout Detection
- [ ] Breakout UP: preț > OR High + threshold
- [ ] Breakout DOWN: preț < OR Low - threshold
- [ ] Signal: BUY/SELL/WAIT
- [ ] Body % și Wick % calculate corect

---

### 7. FLOW DATE - ROBOȚI V33 NY BREAKOUT

```
v33_ny_breakout_robot.py
    ↓ Pre-session analysis 08:00-13:00 NY
    ↓ OR calculation 13:00-13:15 NY
    ↓ Breakout detection
MT5 Core Server
    ↓ GET /api/v33/session_status
    ↓ GET /api/v33/presession_data
    ↓ GET /api/v33/or_data
Dashboard
    ↓ Similar V32 dar pentru sesiunea NY
```

**Teste necesare:**
- [ ] NY Time corect (timezone America/New_York)
- [ ] Pre-session data: High, Low, Compression
- [ ] OR pentru NY: 13:00-13:15
- [ ] Breakout detection pentru NY session

---

## 🔄 SINCRONIZARE TIMING

### Polling Intervale (Frontend → Backend)

| Container | Endpoint | Interval | Acceptabil |
|-----------|----------|----------|------------|
| Clienți | /api/clients | 10 sec | ✅ 8-12 sec |
| Poziții | /api/open_positions | 5 sec | ✅ 4-6 sec |
| Istoric | /api/history | 30 sec | ✅ 25-35 sec |
| Tracking | /api/tracking | 5 sec | ✅ 4-6 sec |
| V31 Live | /api/v31/live_status | 5 sec | ✅ 4-6 sec |
| V31 Logs | /api/robot_logs | 30 sec | ✅ 25-35 sec |
| V31 Symbols | /api/v31/symbol_status | 3 sec | ✅ 2-4 sec |
| V32 All | /api/v32/* | 1 sec | ✅ 0.8-1.2 sec |
| V33 All | /api/v33/* | 1 sec | ✅ 0.8-1.2 sec |
| Status Robot | /api/robots | 2 sec | ✅ 1.5-2.5 sec |

---

## 🧪 TESTE SPECIFICE SINCRONIZARE

### Test 1: Sincronizare Start Robot
```
T+0s: User click START
T+0.5s: Frontend POST /api/robot/v31/start
T+1s: Backend pornește proces Python
T+2s: Backend salvează PID în DB
T+2.5s: Frontend polling /api/robots
T+3s: Frontend vede status "running"
T+3.5s: UI update badge "🟢 Running"

→ Total: 3.5 secunde max ✅
```

### Test 2: Sincronizare Analiză Simbol
```
T+0s: V31 robot analizează EURUSD
T+0.1s: Robot scrie în DB symbol_analysis
T+3s: Frontend polling /api/v31/symbol_status
T+3.2s: Frontend primește date EURUSD
T+3.5s: Grid update - EURUSD badge galben (setup)

→ Total: 3.5 secunde max ✅
```

### Test 3: Sincronizare Trade Deschis
```
T+0s: V31 robot decide BUY EURUSD
T+0.5s: Robot trimite comandă la MT5 Core
T+1s: MT5 Core trimite la EA BrainBridge
T+2s: EA execută în MT5
T+3s: EA raportează poziție nouă în /update
T+4s: Backend salvează poziția
T+5s: Frontend polling /api/open_positions
T+5.5s: Frontend afișează poziția nouă

→ Total: 5.5 secunde max ✅
```

### Test 4: Sincronizare Poziție Închisă
```
T+0s: SL/TP hit în MT5
T+1s: EA raportează poziție închisă
T+2s: Backend mută din positions în history
T+3s: Frontend poziția dispare din Poziții Active
T+30s: Frontend polling /api/history
T+33s: Frontend afișează în Istoric

→ Poziție închisă: 3 secunde
→ Istoric: 33 secunde max ✅
```

---

## 📊 METRICE ACCEPTATE

| Metrică | Valoare Acceptată | Valoare Ideală |
|---------|-------------------|----------------|
| Latență API | < 500ms | < 200ms |
| Sincronizare Start/Stop | < 5 sec | < 3 sec |
| Sincronizare Analiză | < 5 sec | < 3 sec |
| Sincronizare Trade | < 6 sec | < 4 sec |
| Uptime Server | > 99% | 99.9% |
| Erori API | < 1% | 0% |
| Date Stale | < 10 sec | < 5 sec |

---

## 🎯 CRITERII DE TRECERE

Pentru fiecare container:
- [ ] **100% elemente vizibile** - Toate elementele randate în DOM
- [ ] **100% date reale** - Niciun mock/static
- [ ] **100% funcționalitate** - Click, input, toggle funcționale
- [ ] **Sincronizare < 5 secunde** - Update rapid după acțiune
- [ ] **Zero erori JavaScript** - Consolă curată
- [ ] **Zero erori API 4xx/5xx** - Toate endpoint-uri funcționale

---

## 📁 RAPORTARE

Salvează rezultatele în:
- `/workspace/shared/agents/qa-master/output/SYNC_TEST_REPORT.md`
- Format: Tabel per container cu PASS/FAIL pentru fiecare test
- Include timestamp și screenshot dacă FAIL

---

**QA-MASTER: EXECUTĂ TOATE TESTELE DE SINCRONIZARE!** 🧪
