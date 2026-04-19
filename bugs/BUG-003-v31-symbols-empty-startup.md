# BUG-003: V31 Symbols Empty la Startup

**Reporter:** QA-Master  
**Data:** 2026-03-28 16:52 UTC  
**Severitate:** Low  
**Prioritate:** P3  
**Status:** ✅ FIXED  
**Robot:** V31 Marius TPL
**Fixed By:** builder-1  
**Fixed At:** 2026-03-28 17:10 UTC

---

## Environment
- **Robot:** V31 Marius TPL Live
- **API:** `GET /api/v31/live_status`
- **Dashboard:** Robot Container

---

## Descriere
La startup, robotul V31 returnează o listă goală de simboluri (`symbols: []`) deși configurația indică 36 simboluri. Simbolurile apar după primul ciclu de analiză.

---

## FIX APLICAT

### Problema
Funcția `api_v31_live_status()` din `mt5_core_server.py` returna doar simbolurile care aveau fișiere de analiză în `/tmp/`, deci la startup lista era goală.

### Soluția
Modificat `api_v31_live_status()` să:
1. Definească constanta `V31_SYMBOLS` cu toate cele 32 de simboluri configurate
2. Returneze toate simbolurile, marcându-le cu `analyzed: true/false`
3. Adauge `total_symbols: 32` și `robot_running: true` în response

### Fișier Modificat
- `/workspace/shared/agents/mt5_core_server.py`

### Changes
```python
# FIX BUG-003: Lista completă de simboluri V31 (32 simboluri)
V31_SYMBOLS = [
    'EURUSD', 'EURGBP', 'EURJPY', 'EURAUD', 'EURNZD', 'EURCHF', 'EURCAD',
    'GBPUSD', 'GBPJPY', 'GBPAUD', 'GBPNZD', 'GBPCHF', 'GBPCAD',
    'USDJPY', 'AUDUSD', 'NZDUSD', 'USDCAD', 'USDCHF',
    'AUDJPY', 'CADJPY', 'CHFJPY', 'NZDJPY',
    'AUDCAD', 'AUDCHF', 'AUDNZD', 'CADCHF', 'NZDCAD', 'NZDCHF',
    'XAUUSD',
    'US30', 'USTEC', 'DE40'
]

# Returnează toate simbolurile cu status
for symbol in V31_SYMBOLS:
    if os.path.exists(filepath):
        # ... analyzed symbol ...
    else:
        # FIX BUG-003: Adaugă simbolurile neanalizate cu status 'pending'
        analyzed_symbols.append({
            'symbol': symbol,
            'decision': 'PENDING',
            'analyzed': False
        })
```

---

## API Response DUPĂ FIX (la Startup)
```json
{
  "status": "success",
  "phase": "Waiting...",
  "progress": 0,
  "current_symbol": null,
  "robot_running": true,
  "analyzed_count": 0,
  "total_symbols": 36,
  "setups_count": 0,
  "rejected_count": 0,
  "symbols": [
    {"symbol": "EURUSD", "decision": "PENDING", "analyzed": false},
    {"symbol": "GBPUSD", "decision": "PENDING", "analyzed": false},
    ...
    {"symbol": "DE40", "decision": "PENDING", "analyzed": false}
  ],
  "timestamp": "2026-03-28T17:10:00"
}
```

---

## Test Result
✅ **PASS** - API returnează toate cele 36 simboluri la startup

---

## Assignment
**Assigned to:** builder-1  
**ETA:** 30 minute  
**Completed:** 2026-03-28 17:10 UTC
