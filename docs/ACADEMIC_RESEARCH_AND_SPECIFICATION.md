# RESEARCH ACADEMIC + TEST SPECIFICATION COMPLET
## Dashboard Trading System - Analiză Exhaustivă
### Data: 2026-03-28 | Versiune: 2.0

---

## 📚 METODOLOGIE RESEARCH

### 1. Analiza Codului Sursă
- Fișiere examinate: `index.html`, `dashboard_functional.js`, `mt5_core_server.py`
- API endpoints: 25+ identificate
- Funcții JavaScript: 100+ identificate
- Tabele PostgreSQL: 8 identificate

### 2. Arhitectura Sistemului
```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Browser)                        │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────────────┐   │
│  │Clienți  │ │Poziții  │ │Istoric  │ │Tracking         │   │
│  └────┬────┘ └────┬────┘ └────┬────┘ └────────┬────────┘   │
│       └─────────────┴─────────┴────────────────┘            │
│                           │                                  │
│  ┌────────────────────────┴─────────────────────────────┐   │
│  │              Robot Dashboard (V31/V32/V33)           │   │
│  └────────────────────────┬─────────────────────────────┘   │
└───────────────────────────┼─────────────────────────────────┘
                            │ HTTP/JSON
┌───────────────────────────┼─────────────────────────────────┐
│                    BACKEND (Flask)                          │
│  ┌────────────────────────┴─────────────────────────────┐   │
│  │              MT5 Core Server (Port 8001)             │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌────────────┐ │   │
│  │  │/api/*   │ │Robot    │ │Client   │ │Market      │ │   │
│  │  │endpoints│ │Control  │ │Manager  │ │Data        │ │   │
│  │  └─────────┘ └────┬────┘ └────┬────┘ └─────┬──────┘ │   │
│  └───────────────────┼───────────┼────────────┼─────────┘   │
└──────────────────────┼───────────┼────────────┼─────────────┘
                       │           │            │
            ┌──────────┴───────────┴────────────┴──────────┐
            │           POSTGRESQL DATABASE                 │
            │  ┌─────────┐ ┌─────────┐ ┌─────────────────┐ │
            │  │robot_   │ │symbol_  │ │position_        │ │
            │  │logs     │ │analysis │ │tracking         │ │
            │  └─────────┘ └─────────┘ └─────────────────┘ │
            └──────────────────────────────────────────────┘
                            │
            ┌───────────────┴───────────────┐
            │      PYTHON ROBOT PROCESSES    │
            │  ┌─────────┐ ┌─────────┐      │
            │  │V31 TPL  │ │V32      │      │
            │  │Robot    │ │London   │      │
            │  └─────────┘ └─────────┘      │
            └───────────────────────────────┘
                            │
            ┌───────────────┴───────────────┐
            │         MT5 PLATFORM           │
            │      (via ZeroMQ/EA)           │
            └───────────────────────────────┘
```

---

## 🔍 ANALIZĂ CONTAINER CU CONTAINER

---

# CONTAINER 1: CLIENȚI (#clients-section)

## 1.1 Structură HTML Identificată

```html
<div class="card" id="clients-section">
  <h2>👥 Clienți</h2>
  <span id="clientCount" class="badge">X Activi</span>
  
  <div class="controls">
    <button id="toggleAllClients">Activează Toți</button>
    <select id="clientFilter">
      <option value="all">Toți</option>
      <option value="active">Active</option>
      <option value="inactive">Inactive</option>
    </select>
  </div>
  
  <table id="clientsTable">
    <thead>
      <tr>
        <th>Status</th>
        <th>Login</th>
        <th>Nume</th>
        <th>Balans</th>
        <th>Equity</th>
        <th>Poziții</th>
        <th>Profit</th>
        <th>Acțiune</th>
      </tr>
    </thead>
    <tbody><!-- Populat dinamic --></tbody>
  </table>
</div>
```

## 1.2 Funcții JavaScript Asociate

| Funcție | Linie | Scop Presupus | Status Clarificare |
|---------|-------|---------------|-------------------|
| `loadClients()` | 1739 | Încarcă lista clienți din API | ⚠️ Necesită clarificare: ce date exact? |
| `updateClientsTable()` | 1750 | Randează tabelul | ⚠️ Cum gestionează date lipsă? |
| `toggleClient()` | 1800 | Activează/dezactivează client | ❌ **NECUNOSCUT:** Persistă în DB? |
| `toggleAllClients()` | 1820 | Toggle global | ❌ **NECUNOSCUT:** Afectează toți clienții sau doar cei vizibili? |

## 1.3 API Endpoints Utilizate

```javascript
// Din codul sursă:
fetch(`${API_URL}/api/clients`)
fetch(`${API_URL}/api/client/${login}/toggle`, {method: 'POST'})
fetch(`${API_URL}/api/clients/toggle-all`, {method: 'POST'})
```

## 1.4 ❓ ÎNTREBĂRI PENTRU UTILIZATOR

### Q1.1: Ce înseamnă "Activează/Dezactivează" client?
- [ ] **Opțiunea A:** Clientul nu mai primește comenzi de la roboți (dar rămâne conectat)
- [ ] **Opțiunea B:** Clientul este deconectat complet din MT5
- [ ] **Opțiunea C:** Doar un flag vizual în dashboard
- [ ] **Alta:** ___________________

### Q1.2: Ce se întâmplă când un client e "dezactivat"?
- [ ] **A:** Pozițiile deschise rămân deschise, dar nu se mai deschid poziții noi
- [ ] **B:** Toate pozițiile se închid automat
- [ ] **C:** Nimic special, doar flag vizual
- [ ] **Alta:** ___________________

### Q1.3: Cine poate dezactiva clienți?
- [ ] **A:** Doar utilizatorul manual (din dashboard)
- [ ] **B:** Și roboții pot dezactiva automat (de ex. la margin call)
- [ ] **C:** Sistemul automat la anumite condiții

### Q1.4: Ce afișează coloana "Nume"?
- [ ] **A:** Numele din contul MT5 (din API MT5)
- [ ] **B:** Un nume configurabil manual în dashboard
- [ ] **C:** Doar numărul login-ului
- [ ] **Alta:** ___________________

### Q1.5: Cât de des trebuie refresh la date clienți?
- [ ] **A:** 5 secunde (rapid, date live)
- [ ] **B:** 10 secunde (cum e acum)
- [ ] **C:** 30 secunde (mai lent)
- [ ] **D:** Real-time cu WebSocket

---

# CONTAINER 2: POZIȚII ACTIVE (#positions-section)

## 2.1 Structură HTML

```html
<div class="card" id="positions-section">
  <h2>📈 Poziții Active</h2>
  <span id="positionCount">X Poziții</span>
  
  <div class="filters">
    <select id="positionTypeFilter">
      <option value="all">Toate</option>
      <option value="buy">BUY</option>
      <option value="sell">SELL</option>
    </select>
    <select id="positionSymbolFilter"><!-- Dinamic --></select>
    <select id="positionProfitFilter">
      <option value="all">Toate</option>
      <option value="profit">Profit</option>
      <option value="loss">Pierdere</option>
    </select>
  </div>
  
  <button id="closeAllPositions">Închide Toate</button>
  
  <table id="positionsTable">
    <thead>
      <tr>
        <th>Ticket</th>
        <th>Client</th>
        <th>Symbol</th>
        <th>Tip</th>
        <th>Volum</th>
        <th>Open Price</th>
        <th>Current</th>
        <th>SL</th>
        <th>TP</th>
        <th>Swap</th>
        <th>Profit</th>
        <th>Acțiune</th>
      </tr>
    </thead>
    <tbody></tbody>
  </table>
</div>
```

## 2.2 Funcții JavaScript

| Funcție | Scop Presupus | Întrebări |
|---------|---------------|-----------|
| `loadPositions()` | Încarcă poziții deschise | ❌ **NECUNOSCUT:** Folosește `/api/positions` sau `/api/open_positions`? |
| `updatePositionsTable()` | Randează tabel | ⚠️ Cum calculează "Current" price? |
| `closePosition(ticket)` | Închide o poziție | ❌ **NECUNOSCUT:** Confirmare înainte de închidere? |
| `closeAllPositions()` | Închide toate | ❌ **NECUNOSCUT:** Ce se întâmplă la click? |

## 2.3 ❓ ÎNTREBĂRI PENTRU UTILIZATOR

### Q2.1: Ce preț afișează la "Current"?
- [ ] **A:** Bid pentru SELL, Ask pentru BUY (preț de închidere)
- [ ] **B:** Doar Bid (indiferent de direcție)
- [ ] **C:** Mid price (bid+ask)/2
- [ ] **D:** Ultimul preț închis (close)

### Q2.2: Ce se întâmplă la "Închide Toate"?
- [ ] **A:** Se închid imediat toate pozițiile la market
- [ ] **B:** Se deschide modal de confirmare cu sumar
- [ ] **C:** Se închid doar pozițiile vizibile (filtrate)
- [ ] **D:** Se închid doar pozițiile în profit/pierdere (selectabil)

### Q2.3: Confirmare la închidere poziție individuală?
- [ ] **A:** Da, modal cu "Ești sigur?"
- [ ] **B:** Da, dar doar dacă pierderea > X%
- [ ] **C:** Nu, se închide imediat
- [ ] **D:** Configurabil în setări

### Q2.4: Ce se întâmplă cu pozițiile modificate?
- [ ] **A:** Se evidențiază (colorate diferit)
- [ ] **B:** Apare indicator "Modificat"
- [ ] **C:** Se loghează doar în Tracking
- [ ] **D:** Nimic special

### Q2.5: Cum se calculează Profitul afișat?
- [ ] **A:** Doar (current - open) * volume
- [ ] **B:** (current - open) * volume - swap - commission
- [ ] **C:** Profit net în depozit (incl. toate costurile)
- [ ] **D:** Aș vrea să fie configurabil

### Q2.6: Ce simboluri apar în filtrul de simboluri?
- [ ] **A:** Toate simbolurile disponibile în MT5
- [ ] **B:** Doar simbolurile cu poziții deschise
- [ ] **C:** Doar simbolurile configurate în roboți
- [ ] **D:** O listă fixă (EURUSD, GBPUSD, etc.)

---

# CONTAINER 3: ISTORIC TRANZACȚII (#history-section)

## 3.1 Structură HTML

```html
<div class="card" id="history-section">
  <h2>📜 Istoric Tranzacții</h2>
  
  <div class="filters">
    <select id="historyPeriodFilter">
      <option value="today">Astăzi</option>
      <option value="week">Săptămâna</option>
      <option value="month">Luna</option>
      <option value="all">Tot</option>
    </select>
    <select id="historySymbolFilter"><!-- Dinamic --></select>
    <select id="historyProfitFilter">
      <option value="all">Toate</option>
      <option value="positive">Profit</option>
      <option value="negative">Pierdere</option>
    </select>
  </div>
  
  <table id="historyTable">
    <thead>
      <tr>
        <th>Ticket</th>
        <th>Data Deschidere</th>
        <th>Data Închidere</th>
        <th>Client</th>
        <th>Symbol</th>
        <th>Tip</th>
        <th>Volum</th>
        <th>Profit Brut</th>
        <th>Comision</th>
        <th>Swap</th>
        <th>Profit Net</th>
        <th>Durată</th>
        <th>R:R</th>
      </tr>
    </thead>
    <tbody></tbody>
  </table>
</div>
```

## 3.2 Funcții JavaScript

| Funcție | Scop | Întrebări |
|---------|------|-----------|
| `loadHistory()` | Încarcă istoric | ⚠️ Endpoint: `/api/history` sau `/api/tracking`? |
| `updateHistoryTable()` | Randează tabel | ❌ **NECUNOSCUT:** Cum calculează R:R? |
| `calculateRR()` | Risk:Reward | ❌ **NECUNOSCUT:** Formula exactă? |
| `setHistoryFilter()` | Aplică filtre | ✅ Clar |

## 3.3 ❓ ÎNTREBĂRI PENTRU UTILIZATOR

### Q3.1: Ce date să apară în istoric?
- [ ] **A:** Doar tranzacțiile închise complet
- [ ] **B:** Și tranzacțiile anulate/cancelled
- [ ] **C:** Și tranzacțiile parțial închise (partial close)
- [ ] **D:** Toate operațiunile (incl. modificări SL/TP)

### Q3.2: Cum se calculează R:R (Risk:Reward)?
- [ ] **A:** |(Open - SL)| / |(TP - Open)|
- [ ] **B:** Profit real / |(Open - SL)|
- [ ] **C:** (Profit / Risk) bazat pe prețuri reale
- [ ] **D:** Așa cum a fost setat inițial (nu se schimbă)

### Q3.3: Ce înseamnă "Durată"?
- [ ] **A:** Timpul între deschidere și închidere
- [ ] **B:** Timpul cât a stat deschis efectiv (excl. weekend)
- [ ] **C:** Numărul de minute indiferent de ore/zi
- [ ] **D:** Format: "2h 30m" sau "3 zile"

### Q3.4: Limită de istoric?
- [ ] **A:** Ultimele 100 tranzacții
- [ ] **B:** Ultimele 30 zile
- [ ] **C:** Tot istoricul disponibil (paginat)
- [ ] **D:** Configurabil

### Q3.5: Ce faci la click pe o tranzacție din istoric?
- [ ] **A:** Nimic
- [ ] **B:** Modal cu detalii complete
- [ ] **C:** Navigare la tracking pentru acel ticket
- [ ] **D:** Chart cu punctele de entry/exit

### Q3.6: Export date istoric?
- [ ] **A:** Nu e necesar
- [ ] **B:** CSV download
- [ ] **C:** Excel/XLSX
- [ ] **D:** PDF raport

---

# CONTAINER 4: TRACKING TRANZACȚII (#tracking-section)

## 4.1 Structură HTML

```html
<div class="card" id="tracking-section">
  <h2>📊 Tracking Tranzacții</h2>
  
  <div class="filters">
    <select id="trackingFilterType">
      <option value="all">Toate</option>
      <option value="open">Deschise</option>
      <option value="closed">Închise</option>
    </select>
    <select id="trackingFilterSymbol"><!-- Dinamic --></select>
  </div>
  
  <table id="trackingTable">
    <thead>
      <tr>
        <th>Status</th>
        <th>Data/Ora</th>
        <th>Ticket</th>
        <th>Simbol</th>
        <th>Tip</th>
        <th>Volum</th>
        <th>Deschis De</th>
        <th>Închis De</th>
        <th>Modificat De</th>
        <th>Profit</th>
        <th>Comision</th>
        <th>Profit Net</th>
        <th>Durată</th>
      </tr>
    </thead>
    <tbody id="trackingBody"></tbody>
  </table>
</div>
```

## 4.2 ❓ ÎNTREBĂRI PENTRU UTILIZATOR

### Q4.1: Diferența dintre "Istoric" și "Tracking"?
- [ ] **A:** Istoric = doar tranzacții închise, Tracking = deschise + închise
- [ ] **B:** Istoric = sumar, Tracking = detalii complete cu cine a acționat
- [ ] **C:** Istoric = pentru analiză, Tracking = pentru audit
- [ ] **D:** Sunt duplicate, pot elimina unul

### Q4.2: Ce înseamnă "Deschis De" / "Închis De"?
- [ ] **A:** Numele robotului care a deschis (ex: "V31_TPL")
- [ ] **B:** ID-ul utilizatorului (dacă manual)
- [ ] **C:** "Manual" sau numele robotului
- [ ] **D:** IP-ul sau session ID

### Q4.3: Ce înseamnă "Modificat De"?
- [ ] **A:** Cine a modificat SL/TP
- [ ] **B:** Cine a modificat volumul (partial close)
- [ ] **C:** Ambele
- [ ] **D:** Alte modificări

### Q4.4: Statusurile posibile?
- [ ] **A:** Deschis, Închis, Modificat
- [ ] **B:** Active, Closed, Cancelled
- [ ] **C:** Open, Closed, Modified, Partially Closed
- [ ] **D:** ___________________

---

# CONTAINER 5: ROBOȚI V31 MARIUS TPL

## 5.1 Structură HTML (Simplificată)

```html
<div id="v31-dashboard-section">
  <!-- HEADER -->
  <div class="robot-header">
    <h2>🤖 V31 Marius TPL</h2>
    <span id="v31-status-badge" class="badge">⚪ Oprit</span>
    <div class="robot-controls">
      <button id="v31-start-btn">▶️ START</button>
      <button id="v31-stop-btn">⏹️ STOP</button>
    </div>
  </div>
  
  <!-- INFO STRATEGIE -->
  <div class="strategy-info">
    <div>Entry: 61.8% Fib | RSI+Stoch | Scor 6/10 | R:R 1:2</div>
  </div>
  
  <!-- STATISTICI -->
  <div class="stats-grid">
    <div class="stat-card">
      <div class="stat-label">Simboluri</div>
      <div class="stat-value" id="v31-symbols-count">32</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Setups</div>
      <div class="stat-value" id="v31-setups-count">0</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Tranzacții</div>
      <div class="stat-value" id="v31-trades-count">0</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Status</div>
      <div class="stat-value" id="v31-status-text">Idle</div>
    </div>
  </div>
  
  <!-- ANALIZĂ LIVE -->
  <div class="live-analysis">
    <h3>🔍 Analiză Live</h3>
    <div class="progress-bar" id="v31-progress"></div>
    <div id="v31-phase">Așteptare...</div>
    <div id="v31-current-symbol">-</div>
    <div class="counters">
      <span>Analizate: <b id="v31-analyzed">0</b>/32</span>
      <span>Setups: <b id="v31-setups">0</b></span>
      <span>Rejecții: <b id="v31-rejected">0</b></span>
    </div>
  </div>
  
  <!-- SCORURI -->
  <div class="scores">
    <h3>📊 Scoruri Tehnice</h3>
    <div class="score-item">
      <span>RSI</span>
      <div class="score-bar" id="v31-rsi"></div>
      <span id="v31-rsi-value">-</span>
    </div>
    <div class="score-item">
      <span>Stochastic</span>
      <div class="score-bar" id="v31-stoch"></div>
      <span id="v31-stoch-value">-</span>
    </div>
    <div class="score-item">
      <span>Fibonacci</span>
      <div class="score-bar" id="v31-fib"></div>
      <span id="v31-fib-value">-</span>
    </div>
    <div class="score-item total">
      <span>TOTAL</span>
      <div class="score-bar" id="v31-total"></div>
      <span id="v31-total-value">-</span>
    </div>
  </div>
  
  <!-- LOG-URI -->
  <div class="logs-section">
    <h3>📝 Log-uri Robot</h3>
    <div class="log-filters">
      <button data-filter="lifecycle">Lifecycle</button>
      <button data-filter="cycle">Cycle</button>
      <button data-filter="symbol">Symbol</button>
      <button data-filter="setup">Setup</button>
      <button data-filter="trade">Trade</button>
    </div>
    <table id="v31-logs-table">
      <thead>
        <tr>
          <th>Timp</th>
          <th>Nivel</th>
          <th>Categorie</th>
          <th>Mesaj</th>
        </tr>
      </thead>
      <tbody></tbody>
    </table>
  </div>
  
  <!-- GRID SIMBOLURI 32 -->
  <div class="symbols-grid">
    <h3>🎯 Grid Simboluri (32)</h3>
    <div id="v31-symbols-grid"><!-- 32 badge-uri --></div>
  </div>
</div>
```

## 5.2 ❓ ÎNTREBĂRI PENTRU UTILIZATOR

### Q5.1: Ce face butonul START exact?
- [ ] **A:** Pornește procesul Python `v31_marius_tpl_robot.py`
- [ ] **B:** Setează un flag "enabled" și robotul pornește singur
- [ ] **C:** Trimite semnal de start către robotul deja pornit
- [ ] **D:** Altele: ___________________

### Q5.2: Ce face butonul STOP exact?
- [ ] **A:** Oprește procesul Python (SIGTERM)
- [ ] **B:** Setează flag "stop_requested" și robotul se oprește gracefully
- [ ] **C:** Închide toate pozițiile deschise și apoi oprește
- [ ] **D:** Doar oprește analiza, păstrează pozițiile

### Q5.3: Ce se întâmplă cu pozițiile deschise când apeși STOP?
- [ ] **A:** Rămân deschise (robotul doar nu mai deschide altele)
- [ ] **B:** Se închid automat toate
- [ ] **C:** Se închid doar cele în așteptare (pending)
- [ ] **D:** Aleg eu la stop

### Q5.4: Ce afișează "Faza" în analiză?
- [ ] **A:** Analiză în curs / Ciclu complet / Așteptare
- [ ] **B:** Numele simbolului curent analizat
- [ ] **C:** Timp rămas până la următorul ciclu
- [ ] **D:** Statusul robotului (Idle/Running/Paused)

### Q5.5: Ce înseamnă culorile în gridul de simboluri?
- [ ] **A:** Gri = neanalizat, Verde = analizat fără setup, Galben = setup, Roșu = trade deschis
- [ ] **B:** Verde = analizat, Galben = setup, Roșu = trade, Gri = eroare
- [ ] **C:** Culori bazate pe profit (verde = profit, roșu = pierdere)
- [ ] **D:** ___________________

### Q5.6: Ce sunt scorurile RSI/Stoch/Fib?
- [ ] **A:** Scoruri de la 0-10 pentru fiecare indicator
- [ ] **B:** Valorile raw ale indicatorilor (ex: RSI=65.4)
- [ ] **C:** Scoruri normalizate (0-100)
- [ ] **D:** Doar indicatoare vizuale (fără valori numerice)

### Q5.7: Ce prag pentru "Setup găsit"?
- [ ] **A:** Total Score >= 6/10
- [ ] **B:** Toți indicatorii verzi (RSI <30, Stoch <20, etc.)
- [ ] **C:** Configurabil în setări
- [ ] **D:** Altele: ___________________

### Q5.8: Ce log-uri se afișează?
- [ ] **A:** Toate log-urile robotului
- [ ] **B:** Doar cele de tip "trade" și "setup"
- [ ] **C:** Doar ultimele 50 log-uri
- [ ] **D:** Filtrabile după categorie

### Q5.9: Ce se întâmplă la click pe un simbol din grid?
- [ ] **A:** Nimic
- [ ] **B:** Modal cu detalii analiză (RSI, Stoch, Fib valori)
- [ ] **C:** Chart cu simbolul
- [ ] **D:** Forțează analiza imediată a simbolului

### Q5.10: Cât durează un ciclu complet de analiză?
- [ ] **A:** Fix 32 simboluri × X secunde = ~2-3 minute
- [ ] **B:** Variabil, depinde de volatilitate
- [ ] **C:** Configurabil
- [ ] **D:** Continuu, fără pauză

---

# CONTAINER 6: V32 LONDON BREAKOUT

## 6.1 Structură HTML

```html
<div id="v32-dashboard-section">
  <div class="robot-header">
    <h2>🌅 V32 London Breakout</h2>
    <span id="v32-status-badge">⚪ Oprit</span>
    <button id="v32-start-btn">START</button>
    <button id="v32-stop-btn">STOP</button>
  </div>
  
  <!-- LONDON TIME -->
  <div class="time-display">
    <div class="time-label">🕐 London Time</div>
    <div class="time-value" id="v32-london-time">--:--:--</div>
    <div class="session-phase" id="v32-phase">--</div>
  </div>
  
  <!-- SESSION TIMER -->
  <div class="session-timer">
    <div class="timer-label">⏱️ Timp până la sesiune</div>
    <div class="timer-value" id="v32-timer">--:--:--</div>
  </div>
  
  <!-- OPENING RANGE PANEL -->
  <div class="panel or-panel">
    <h3>📊 Opening Range (08:00-08:15)</h3>
    <div class="or-stats">
      <div class="stat">
        <span>OR High</span>
        <b id="v32-or-high">-</b>
      </div>
      <div class="stat">
        <span>OR Low</span>
        <b id="v32-or-low">-</b>
      </div>
      <div class="stat">
        <span>Range</span>
        <b id="v32-or-range">-</b>
      </div>
      <div class="stat">
        <span>Current</span>
        <b id="v32-current-price">-</b>
      </div>
    </div>
  </div>
  
  <!-- ASIA SESSION PANEL -->
  <div class="panel asia-panel">
    <h3>🌏 Asia Session (00:00-08:00)</h3>
    <div class="asia-stats">
      <div class="stat">
        <span>Asia High</span>
        <b id="v32-asia-high">-</b>
      </div>
      <div class="stat">
        <span>Asia Low</span>
        <b id="v32-asia-low">-</b>
      </div>
      <div class="stat">
        <span>Range</span>
        <b id="v32-asia-range">-</b>
      </div>
      <div class="stat">
        <span>Compression</span>
        <b id="v32-compression">-</b>
      </div>
    </div>
  </div>
  
  <!-- BREAKOUT DETECTION -->
  <div class="panel breakout-panel">
    <h3>🚨 Breakout Detection</h3>
    <div class="breakout-status" id="v32-breakout-status">WAIT</div>
    <div class="breakout-type" id="v32-breakout-type">-</div>
    <div class="breakout-metrics">
      <div>Body: <span id="v32-body-pct">-</span>%</div>
      <div>Wick: <span id="v32-wick-pct">-</span>%</div>
    </div>
    <div class="signal" id="v32-signal">⏸️ AȘTEAPTĂ</div>
  </div>
  
  <!-- DAILY STATS -->
  <div class="panel stats-panel">
    <h3>📈 Statistici Zilnice</h3>
    <div class="daily-stats">
      <div>Tranzacții: <b id="v32-trades">0</b></div>
      <div>Câștigate: <b id="v32-wins">0</b></div>
      <div>Pierdute: <b id="v32-losses">0</b></div>
      <div>P&L: <b id="v32-pnl">$0.00</b></div>
    </div>
  </div>
</div>
```

## 6.2 ❓ ÎNTREBĂRI PENTRU UTILIZATOR

### Q6.1: Ce timezone folosește "London Time"?
- [ ] **A:** Europe/London (GMT/BST automat)
- [ ] **B:** UTC mereu
- [ ] **C:** Ora locală a serverului
- [ ] **D:** Configurabil

### Q6.2: Cât e pragul pentru "Compression"?
- [ ] **A:** Asia Range < 40 pips
- [ ] **B:** Asia Range < 50% din OR Range
- [ ] **C:** Ambele condiții (AND)
- [ ] **D:** Altele: ___________________

### Q6.3: Ce simbol/e tranzacționează V32?
- [ ] **A:** EURUSD (default)
- [ ] **B:** GBPUSD (pentru London)
- [ ] **C:** Multi-simbol
- [ ] **D:** Configurabil

### Q6.4: Ce înseamnă fazele sesiunii?
- [ ] **A:** BEFORE_SESSION (00:00-08:00), OPENING_RANGE (08:00-08:15), MAIN_SESSION (08:15-16:00), EXTENDED (16:00-00:00)
- [ ] **B:** Doar două: Asia și London
- [ ] **C:** În funcție de volatilitate
- [ ] **D:** ___________________

### Q6.5: Cum detectează breakout?
- [ ] **A:** Preț > OR High (pentru BUY) sau < OR Low (pentru SELL)
- [ ] **B:** Preț > OR High + X pips buffer
- [ ] **C:** Confirmare pe închiderea candle-ului
- [ ] **D:** Volum + preț

### Q6.6: Ce înseamnă Body% și Wick%?
- [ ] **A:** Body% = |close - open| / |high - low|, Wick% = restul
- [ ] **B:** Raport între corp și fitil pentru confirmare
- [ ] **C:** Doar valori informative
- [ ] **D:** ___________________

### Q6.7: Ce face robotul când detectează breakout?
- [ ] **A:** Deschide poziție imediat (market)
- [ ] **B:** Așteaptă retest și apoi intră
- [ ] **C:** Pune ordin pending (stop entry)
- [ ] **D:** Notificare doar, fără trade automat

---

# CONTAINER 7: V33 NY BREAKOUT

## 7.1 Structură HTML

Similar cu V32 dar pentru sesiunea NY:
- NY Time (America/New_York)
- Pre-session (08:00-13:00 NY)
- NY Opening Range (13:00-13:15 NY)
- Breakout detection

## 7.2 ❓ ÎNTREBĂRI PENTRU UTILIZATOR

### Q7.1: Diferențe între V32 și V33?
- [ ] **A:** Doar timezone-ul (London vs NY)
- [ ] **B:** V33 are și "pre-session analysis"
- [ ] **C:** Algoritmi diferiți de breakout
- [ ] **D:** ___________________

### Q7.2: Ce e "Pre-session" în V33?
- [ ] **A:** Analiza între 08:00-13:00 înainte de NY OR
- [ ] **B:** Calcul high/low pre-market
- [ ] **C:** Identificare niveluri cheie
- [ ] **D:** Toate cele de mai sus

---

# CONTAINER 8: SETUP-URI INCOMPLETE

## 8.1 Descriere
Afișează setup-urile identificate de roboți care nu au fost încă tranzacționate (încă în așteptare sau respinse).

## 8.2 ❓ ÎNTREBĂRI PENTRU UTILIZATOR

### Q8.1: Ce e un "Setup Incomplet"?
- [ ] **A:** Setup găsit dar nu s-a deschis tranzacție (SL/TP prea aproape, spread mare, etc.)
- [ ] **B:** Setup în așteptare (pending order plasat)
- [ ] **C:** Setup respins după re-analiză
- [ ] **D:** Toate cele de mai sus

### Q8.2: Cât timp rămâne un setup în listă?
- [ ] **A:** 1 oră
- [ ] **B:** Până la sfârșitul sesiunii
- [ ] **C:** Până când devine trade sau expiră
- [ ] **D:** Configurabil

### Q8.3: Ce acțiuni pot fi luate pe un setup?
- [ ] **A:** Doar vizualizare
- [ ] **B:** Forțare trade manual
- [ ] **C:** Ignorare/ștergere
- [ ] **D:** Modificare parametri și re-verificare

### Q8.4: Ce informații afișează?
- [ ] **A:** Simbol, direcție, scor, motiv respingere
- [ ] **B:** Preț entry, SL, TP, R:R calculat
- [ ] **C:** Timestamp identificare, robot care a găsit
- [ ] **D:** Toate cele de mai sus

---

# CONTAINER 9: COMENZI ÎN AȘTEPTARE (QUEUED COMMANDS)

## 9.1 Descriere
Comenzi trimise de utilizator sau roboți către MT5 care sunt în așteptare să fie executate.

## 9.2 ❓ ÎNTREBĂRI PENTRU UTILIZATOR

### Q9.1: Ce comenzi pot fi în așteptare?
- [ ] **A:** Open position, Close position, Modify SL/TP
- [ ] **B:** Doar comenzi manuale din dashboard
- [ ] **C:** Comenzi automate de la roboți
- [ ] **D:** Toate tipurile de operațiuni

### Q9.2: Ce se întâmplă cu o comandă în așteptare?
- [ ] **A:** Se execută automat când clientul e disponibil
- [ ] **B:** Rămâne în coadă până la executare sau timeout
- [ ] **C:** Se șterge automat după X minute
- [ ] **D:** Utilizatorul trebuie să o re-trimită

### Q9.3: Timeout pentru comenzi?
- [ ] **A:** 30 secunde
- [ ] **B:** 5 minute
- [ ] **C:** 1 oră
- [ ] **D:** Niciodată (până la executare)

### Q9.4: Ce afișează pentru fiecare comandă?
- [ ] **A:** Tip comandă, parametri, timestamp, status
- [ ] **B:** Client target, prioritate, retry count
- [ ] **C:** Eroare (dacă a eșuat)
- [ ] **D:** Toate cele de mai sus

### Q9.5: Acțiuni posibile pe o comandă în așteptare?
- [ ] **A:** Anulare comandă
- [ ] **B:** Modificare parametri
- [ ] **C:** Forțare executare imediată
- [ ] **D:** Doar vizualizare

---

# CONTAINER 10: PERFORMANȚĂ PE SIMBOLURI

## 10.1 Descriere
Statistici de performanță pentru fiecare simbol tranzacționat (win rate, profit, etc.).

## 10.2 ❓ ÎNTREBĂRI PENTRU UTILIZATOR

### Q10.1: Ce metrici afișează per simbol?
- [ ] **A:** Win rate, Profit total, Nr. tranzacții, Profit mediu
- [ ] **B:** R:R mediu, Durată medie, Cel mai bun/worst trade
- [ ] **C:** Perioada analizată (ultimele 30 zile, tot istoricul)
- [ ] **D:** Toate cele de mai sus

### Q10.2: Cum se calculează Win Rate?
- [ ] **A:** Tranzacții câștigătoare / Total tranzacții
- [ ] **B:** Profit pozitiv / Profit total
- [ ] **C:** Doar tranzacțiile închise complet
- [ ] **D:** Configurabil (ex: exclude breakeven)

### Q10.3: Perioada implicită pentru statistici?
- [ ] **A:** Ultimele 30 zile
- [ ] **B:** Luna curentă
- [ ] **C:** Tot istoricul disponibil
- [ ] **D:** Ultimele 100 tranzacții

### Q10.4: Ce se întâmplă la click pe un simbol?
- [ ] **A:** Modal cu detalii complete (toate tranzacțiile)
- [ ] **B:** Chart cu evoluția profitului pe acel simbol
- [ ] **C:** Filtrează istoricul doar pentru acel simbol
- [ ] **D:** Nimic

### Q10.5: Sortare și filtre?
- [ ] **A:** Sortare după profit, win rate, nr. tranzacții
- [ ] **B:** Filtru perioadă (azi, săptămână, lună, tot)
- [ ] **C:** Filtru direcție (BUY/SELL separat)
- [ ] **D:** Toate cele de mai sus

---

# CONTAINER 11: SYSTEM HEALTH

## 11.1 Descriere
Statusul sistemului și componentelor (server, DB, roboți, conexiuni).

## 11.2 ❓ ÎNTREBĂRI PENTRU UTILIZATOR

### Q11.1: Ce componente monitorizează?
- [ ] **A:** MT5 Core Server, PostgreSQL, VPS Bridge
- [ ] **B:** Roboți Python (V31, V32, V33), MT5 EA
- [ ] **C:** Resurse sistem (CPU, RAM, Disk)
- [ ] **D:** Toate cele de mai sus

### Q11.2: Ce înseamnă statusurile?
- [ ] **A:** 🟢 Healthy, 🟡 Warning (degradat), 🔴 Critical (down)
- [ ] **B:** Doar Online/Offline
- [ ] **C:** Cu procent de funcționalitate
- [ ] **D:** Culori diferite

### Q11.3: Ce acțiuni de remediere oferă?
- [ ] **A:** Restart service direct din dashboard
- [ ] **B:** Notificare doar, remediere manuală
- [ ] **C:** Auto-remediere la erori minore
- [ ] **D:** Link către documentație troubleshooting

### Q11.4: Istoric health checks?
- [ ] **A:** Ultimele 24 ore
- [ ] **B:** Ultimele 7 zile
- [ ] **C:** Ultima săptămână cu grafic uptime
- [ ] **D:** Doar status curent

### Q11.5: Alertare la probleme?
- [ ] **A:** Notificare în dashboard (badge, banner)
- [ ] **B:** Email/SMS la erori critice
- [ ] **C:** Telegram alert
- [ ] **D:** Toate cele de mai sus

---

# CONTAINER 12: STATISTICI TRADING

## 12.1 Descriere
Statistici generale de trading (P&L, win rate, etc.) pe toate conturile.

## 12.2 ❓ ÎNTREBĂRI PENTRU UTILIZATOR

### Q12.1: Ce statistici generale afișează?
- [ ] **A:** Profit/Loss total, Win rate %, Nr. tranzacții total
- [ ] **B:** Profit zilnic/săptămânal/lunar
- [ ] **C:** Drawdown maxim, Profit factor, Expectancy
- [ ] **D:** Toate cele de mai sus

### Q12.2: Agregare per cont sau global?
- [ ] **A:** Global (toate conturile împreună)
- [ ] **B:** Per cont individual (selectabil)
- [ ] **C:** Ambele vizualizări
- [ ] **D:** Per grup de conturi

### Q12.3: Perioade disponibile?
- [ ] **A:** Azi, Săptămâna, Luna, Anul, Tot istoricul
- [ ] **B:** Ultimele 30/60/90 zile
- [ ] **C:** Custom (date picker)
- [ ] **D:** Toate cele de mai sus

### Q12.4: Export rapoarte?
- [ ] **A:** PDF cu statistici complete
- [ ] **B:** CSV cu date brute
- [ ] **C:** Excel cu grafice
- [ ] **D:** Doar vizualizare, fără export

---

# CONTAINER 13: ASOCIERE CONTURI

## 13.1 Descriere
Gestionarea asocierii conturilor MT5 cu utilizatori/grupuri.

## 13.2 ❓ ÎNTREBĂRI PENTRU UTILIZATOR

### Q13.1: Ce e "Asociere Conturi"?
- [ ] **A:** Link cont MT5 la utilizator dashboard
- [ ] **B:** Grupare conturi (familie, strategie, etc.)
- [ ] **C:** Permisiuni pe conturi
- [ ] **D:** Toate cele de mai sus

### Q13.2: Cine poate vedea ce conturi?
- [ ] **A:** Admin: toate, User: doar conturile lui
- [ ] **B:** Toți utilizatorii văd toate conturile
- [ ] **C:** Bazat pe grupuri/roluri
- [ ] **D:** Configurabil per cont

### Q13.3: Poți redenumi conturile?
- [ ] **A:** Da, nume friendly (ex: "Cont Principal", "Cont Test")
- [ ] **B:** Doar numele din MT5
- [ ] **C:** Nu, doar login number
- [ ] **D:** Doar admin poate redenumi

### Q13.4: Etichetare/tagging conturi?
- [ ] **A:** Tag-uri custom (ex: "agresiv", "conservator", "test")
- [ ] **B:** Categorii predefinite
- [ ] **C:** Grupare colorată
- [ ] **D:** Nu e necesar

---

# CONTAINER 14: UTILIZATORI ȘI PERMISIUNI

## 14.1 Descriere
Gestionarea utilizatorilor dashboard și permisiunile lor.

## 14.2 ❓ ÎNTREBĂRI PENTRU UTILIZATOR

### Q14.1: Roluri disponibile?
- [ ] **A:** Admin (toate drepturile), User (doar vizualizare), Guest (limitat)
- [ ] **B:** Doar admin și user
- [ ] **C:** Roluri customizabile
- [ ] **D:** Doar un utilizator (tu)

### Q14.2: Ce poate face un User vs Admin?
- [ ] **A:** User: vede date, Admin: + modifică setări, pornește/oprește roboți
- [ ] **B:** User: doar istoric, Admin: tot
- [ ] **C:** User: conturile lui, Admin: toate conturile
- [ ] **D:** ___________________

### Q14.3: Autentificare?
- [ ] **A:** Username/Password
- [ ] **B:** Doar token MT5
- [ ] **C:** 2FA (Two Factor Auth)
- [ ] **D:** IP whitelist

### Q14.4: Sesizare activitate?
- [ ] **A:** Log cu toate acțiunile utilizatorilor
- [ ] **B:** Doar acțiuni critice (start/stop roboți)
- [ ] **C:** Audit trail complet
- [ ] **D:** Nu e necesar

---

# CONTAINER 15: EQUITY CURVE 📉

## 15.1 Descriere
Grafic evoluție equity/balans în timp.

## 15.2 ❓ ÎNTREBĂRI PENTRU UTILIZATOR

### Q15.1: Ce grafice afișează?
- [ ] **A:** Equity curve (evoluție capital)
- [ ] **B:** Drawdown chart (pierderi consecutive)
- [ ] **C:** Profit lunar/anual bar chart
- [ ] **D:** Toate cele de mai sus

### Q15.2: Perioade disponibile?
- [ ] **A:** 1D, 1W, 1M, 3M, 6M, 1Y, All
- [ ] **B:** Doar lună curentă și total
- [ ] **C:** Custom date range
- [ ] **D:** Toate cele de mai sus

### Q15.3: Agregare?
- [ ] **A:** Toate conturile împreună
- [ ] **B:** Per cont selectabil
- [ ] **C:** Ambele opțiuni
- [ ] **D:** Per grup de conturi

### Q15.4: Interactivitate?
- [ ] **A:** Hover pentru detalii (profit la o anumită dată)
- [ ] **B:** Zoom in/out
- [ ] **C:** Click pe punct pentru tranzacțiile din ziua respectivă
- [ ] **D:** Static, doar vizualizare

### Q15.5: Export grafic?
- [ ] **A:** PNG/SVG download
- [ ] **B:** Doar vizualizare
- [ ] **C:** Date brute pentru Excel
- [ ] **D:** Nu e necesar

---

# CONTAINER 16: GESTIONARE SERVICII

## 16.1 Descriere
Controlul serviciilor sistem (pornire/oprire/restart servere, roboți, etc.).

## 16.2 ❓ ÎNTREBĂRI PENTRU UTILIZATOR

### Q16.1: Ce servicii pot fi gestionate?
- [ ] **A:** MT5 Core Server, Roboți (V31, V32, V33), EA Bridge
- [ ] **B:** PostgreSQL, VPS Bridge
- [ ] **C:** Toate componentele sistemului
- [ ] **D:** Doar roboții de trading

### Q16.2: Ce acțiuni sunt disponibile?
- [ ] **A:** Start, Stop, Restart
- [ ] **B:** Status, Logs, Config
- [ ] **C:** Update versiune
- [ ] **D:** Toate cele de mai sus

### Q16.3: Cine poate gestiona serviciile?
- [ ] **A:** Doar Admin
- [ ] **B:** Orice utilizator autentificat
- [ ] **C:** Doar tu (owner)
- [ ] **D:** Configurabil per serviciu

### Q16.4: Confirmare la acțiuni critice?
- [ ] **A:** Da, modal de confirmare
- [ ] **B:** Doar pentru stop/restart
- [ ] **C:** Parolă la acțiuni critice
- [ ] **D:** Nu, se execută imediat

### Q16.5: Afișare logs în timp real?
- [ ] **A:** Tail -f pe log-urile serviciului
- [ ] **B:** Ultimele 100 linii
- [ ] **C:** Download log complet
- [ ] **D:** Doar link către fișier log

---

# CONTAINER 17: ROBOȚI TRADING (GENERAL)

## 17.1 Descriere
Panou general cu toți roboții și statusul lor.

## 17.2 ❓ ÎNTREBĂRI PENTRU UTILIZATOR

### Q17.1: Ce roboți sunt afișați?
- [ ] **A:** V31 TPL, V32 London, V33 NY, și viitori roboți
- [ ] **B:** Doar cei activi/configurați
- [ ] **C:** Toți roboții disponibili în sistem
- [ ] **D:** Configurabil care apar

### Q17.2: Status per robot?
- [ ] **A:** Running, Stopped, Error, Paused
- [ ] **B:** Doar Online/Offline
- [ ] **C:** Cu uptime și last seen
- [ ] **D:** Toate detaliile

### Q17.3: Statistici per robot?
- [ ] **A:** Tranzacții deschise, Win rate, Profit total
- [ ] **B:** Uptime, Erori, Resurse folosite
- [ ] **C:** Configurație curentă
- [ ] **D:** Toate cele de mai sus

### Q17.4: Acțiuni globale?
- [ ] **A:** Start All, Stop All
- [ ] **B:** Emergency Stop (toți roboții)
- [ ] **C:** Pauză trading (păstrează analiza)
- [ ] **D:** Toate cele de mai sus

---

# CONTAINER 18: EXPERT LOGS

## 18.1 Descriere
Log-urile detaliate din EA-ul MT5 (Expert Advisor).

## 18.2 ❓ ÎNTREBĂRI PENTRU UTILIZATOR

### Q18.1: Ce log-uri afișează?
- [ ] **A:** Log-uri din EA BrainBridge (conectare, erori, execuție)
- [ ] **B:** Log-uri din roboți Python
- [ ] **C:** Log-uri din MT5 terminal
- [ ] **D:** Toate cele de mai sus

### Q18.2: Niveluri de log?
- [ ] **A:** DEBUG, INFO, WARNING, ERROR, CRITICAL
- [ ] **B:** Doar ERROR și CRITICAL
- [ ] **C:** INFO și mai sus
- [ ] **D:** Configurabil per utilizator

### Q18.3: Filtrare?
- [ ] **A:** Per nivel log, per sursă, per perioadă
- [ ] **B:** Căutare text în log-uri
- [ ] **C:** Doar ultimele X linii
- [ ] **D:** Toate cele de mai sus

### Q18.4: Live tail?
- [ ] **A:** Update în timp real (auto-refresh)
- [ ] **B:** Refresh manual
- [ ] **C:** WebSocket pentru live updates
- [ ] **D:** Download fișier log

---

# CONTAINER 19: JOURNAL

## 19.1 Descriere
Jurnalul de operațiuni MT5 (deal-uri, ordere, etc.).

## 19.2 ❓ ÎNTREBĂRI PENTRU UTILIZATOR

### Q19.1: Ce intrări sunt în journal?
- [ ] **A:** Dealuri (tranzacții executate), Ordere (plasate/modificate/șterse)
- [ ] **B:** Erori de execuție, Requotes
- [ ] **C:** Modificări balans (depuneri/retrageri)
- [ ] **D:** Toate cele de mai sus

### Q19.2: Format afișare?
- [ ] **A:** Tabel cu: Timp, Tip, Simbol, Volum, Preț, Rezultat
- [ ] **B:** Format text ca în MT5
- [ ] **C:** Timeline vizual
- [ ] **D:** Ambele (tabel + raw)

### Q19.3: Filtrare journal?
- [ ] **A:** Per cont, per simbol, per tip operațiune
- [ ] **B:** Per perioadă
- [ ] **C:** Doar buy/sell
- [ ] **D:** Toate cele de mai sus

### Q19.4: Link către tranzacții?
- [ ] **A:** Click pe deal → navigare la tranzacție în istoric
- [ ] **B:** Doar informație, fără link
- [ ] **C:** Modal cu detalii complete
- [ ] **D:** Export în istoric

---

## 🔄 SINCRONIZARE COMPLETĂ - SPECIFICAȚIE

### Timing Requirements

| Acțiune | Sursa | Destinația | Max Latency | API Endpoint |
|---------|-------|------------|-------------|--------------|
| Client update | MT5 EA | Dashboard | 10s | /api/clients |
| Position open | Robot | Dashboard | 5s | /api/positions |
| Position close | MT5 | Dashboard | 5s | /api/positions + /api/history |
| Robot status | Robot Python | Dashboard | 2s | /api/robots |
| V31 analysis | Robot | Dashboard | 3s | /api/v31/live_status |
| V31 symbols | Robot | Dashboard | 3s | /api/v31/symbol_status |
| V32/V33 data | Robot | Dashboard | 1s | /api/v32/*, /api/v33/* |
| Logs | Robot | Dashboard | 30s | /api/robot_logs |

---

## ✅ TEST CASES NECESARE

Pentru fiecare întrebare de mai sus, vor fi create test cases specifice:
- **Precondiții:** Ce trebuie să fie setat înainte
- **Pași:** Acțiuni exacte
- **Rezultat Așteptat:** Ce trebuie să se întâmple
- **Rezultat Actual:** (de completat la test)
- **Status:** PASS/FAIL
- **Note:** Observații

---

**RĂSPUNDE LA ÎNTREBĂRILE DE MAI SUS PENTRU A CONTINUA CU TEST CASE-URILE!**
