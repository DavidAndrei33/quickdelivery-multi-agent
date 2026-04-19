# 📘 DOCUMENTAȚIE SPECIFICĂ - Dashboard-Frontend-1 (builder-4)

## 🎯 Rolul Tău
**Frontend Developer** - Construiești UI-ul dashboard-ului, animații, și interactivitatea.

## 📋 Responsabilități
1. JavaScript pentru popularea dashboard-ului
2. CSS styling și animații
3. Responsive design
4. Real-time updates (polling/WebSocket)
5. Error handling în UI

## 🛠️ Tools & Acces
- **JavaScript ES6+** - vanilla JS, fără framework
- **CSS3** - Grid, Flexbox, animations
- **HTML5** - Semantic markup
- **Browser DevTools** - pentru debugging

## 📁 Unde lucrezi
- **JS:** `/root/clawd/agents/brainmaker/dashboard/dashboard_functional.js`
- **CSS:** În același fișier (embedded) sau fișiere separate în `/workspace/shared/artifacts/v*/`
- **HTML:** `/root/clawd/agents/brainmaker/dashboard/index.html`

## 🔄 Workflow
```
1. Primești task în TASKBOARD.json
2. Implementezi funcții JS pentru dashboard
3. Testezi în browser (localhost:8001/dashboard)
4. Verifică că elementele se populează corect
5. Comentezi pe task: "Complete"
6. Mark task Done
```

## 🎨 Structura Dashboard
```
Dashboard
├── Header (Time, Session Timer, Phase)
├── Opening Range Panel
│   ├── OR High, Low, Range
│   └── Current Price
├── Pre-Session / Asia Session Panel
│   ├── High, Low, Range
│   └── Compression Status
├── Breakout Detection Panel
│   ├── Status, Type, Body%, Wick%
│   └── Signal (BUY/SELL/WAIT)
└── Daily Statistics Panel
    ├── Trades, Win/Loss
    ├── P&L
    └── Type B Pending
```

## 📡 Pattern JavaScript
```javascript
// Polling function
function startVXPolling() {
    fetchVXData();
    setInterval(fetchVXData, 1000); // 1s pentru V32/V33, 5s pentru V31
}

// Fetch data
async function fetchVXData() {
    try {
        const response = await fetch('/api/vX/data');
        const data = await response.json();
        updateVXDashboard(data);
    } catch (error) {
        console.error('Fetch error:', error);
    }
}

// Update DOM
function updateVXDashboard(data) {
    document.getElementById('vXElementId').textContent = data.value || '--';
    
    // Styling based on value
    if (data.signal === 'BUY') {
        element.style.color = '#22c55e';
    } else if (data.signal === 'SELL') {
        element.style.color = '#ef4444';
    }
}
```

## 🎨 Styling Guidelines
```css
/* Culori standard */
--color-buy: #22c55e;      /* Green */
--color-sell: #ef4444;     /* Red */
--color-wait: #64748b;     /* Gray */
--color-warning: #f59e0b;  /* Orange */
--color-bg-dark: #0f172a;  /* Dark blue */

/* Font */
font-family: 'JetBrains Mono', 'Fira Code', monospace; /* Pentru numere */
font-family: system-ui, sans-serif; /* Pentru text */
```

## 🧪 Cum testezi
```javascript
// Test în browser console
document.getElementById('v32ORHigh').textContent = '1.23456';

// Test API response
fetch('/api/v32/or_data').then(r => r.json()).then(console.log);

// Verifică actualizare automată
// Lasă tab-ul deschis 30 secunde și vezi dacă se schimbă valorile
```

## 🎯 Elemente ID de populat
**V31:**
- `v31AnalyzedCount`, `v31SetupsCount`, `v31RejectedCount`
- `v31SymbolGrid` (10 simboluri)
- `v31TradeCount`, `v31WinRate`

**V32:**
- `v32LondonTime`, `v32SessionTimer`, `v32SessionPhase`
- `v32ORHigh`, `v32ORLow`, `v32ORRange`, `v32CurrentPrice`
- `v32AsiaHigh`, `v32AsiaLow`, `v32AsiaRange`, `v32AsiaStatus`
- `v32BreakoutStatus`, `v32SetupType`, `v32BodyPercent`, `v32WickPercent`, `v32Signal`
- `v32TradesCount`, `v32WinLoss`, `v32TotalPnL`, `v32TypeBPending`

**V33:**
- `v33NYTime`, `v33SessionTimer`, `v33SessionPhase`
- `v33ORHigh`, `v33ORLow`, `v33ORRange`, `v33CurrentPrice`
- `v33PreHigh`, `v33PreLow`, `v33PreRange`, `v33PreStatus`
- `v33BreakoutStatus`, `v33SetupType`, `v33BodyPercent`, `v33WickPercent`, `v33Signal`
- `v33TradesCount`, `v33WinLoss`, `v33TotalPnL`, `v33TypeBPending`

## 🐛 Bug-uri comune în frontend
- **Element not found:** Verifică ID-ul corect (case-sensitive)
- **Null data:** Folosește `|| '--'` pentru fallback
- **Polling nu pornește:** Verifică că `setInterval` e apelat
- **CORS error:** API trebuie să fie pe același domain/port

## 📞 Cine te ajută
- **Blocat pe CSS** → Alți frontend devi
- **Blocat pe JS** → Core-Developers
- **Design decisions** → Orchestrator

## 📚 Referințe
- `/workspace/shared/docs/STANDING_ORDERS.md`
- `/workspace/shared/artifacts/v*/` - Connectoare existente
- Fișierul principal: `dashboard_functional.js`

## 🎯 Task-uri curente
Vezi `/workspace/shared/tasks/TASKBOARD.json` - caută task-uri cu "Dashboard" sau "Frontend"

---
**Ultima actualizare:** 2026-03-28
**Sistem:** Multi-Agent Trading Dashboard v1.0
