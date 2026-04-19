# BUG-011: Missing Symbol Analysis Endpoint

## Informații Generale
| Atribut | Valoare |
|---------|---------|
| **ID** | BUG-011 |
| **Severitate** | MEDIUM |
| **Status** | OPEN |
| **Data descoperirii** | 2026-03-28 |
| **Raportat de** | QA-Master Agent |

## Descriere
Endpoint-ul pentru analiza detaliată a simbolurilor nu există. Când utilizatorul dă click pe un simbol în grid, modal-ul nu poate încărca datele.

## Endpoint Lipsă
```
GET /api/symbol_analysis?symbol={symbol}&robot={robot}
```

## Cod Afectat
```javascript
// dashboard_functional.js
async function fetchSymbolAnalysis(symbol, robot) {
    try {
        const res = await fetch(`${API_URL}/api/symbol_analysis?symbol=${symbol}&robot=${robot}`);
        // ^ Returnează 404
        
        if (!res.ok) return;
        // ...
    } catch (e) {
        console.error('Error fetching symbol analysis:', e);
    }
}
```

## Impact
- Modal-ul de detalii simbol rămâne gol sau cu "Se încarcă..."
- Utilizatorul nu poate vedea analiza detaliată a simbolului
- Funcționalitatea de click pe simbol este inutilă

## Soluție Propusă

### API Endpoint
```javascript
router.get('/api/symbol_analysis', authenticateToken, async (req, res) => {
    try {
        const { symbol, robot } = req.query;
        
        if (!symbol || !robot) {
            return res.status(400).json({
                status: 'error',
                message: 'symbol and robot parameters required'
            });
        }
        
        // Citește analiza din database sau cache
        const analysis = await getSymbolAnalysis(symbol, robot);
        
        res.json({
            status: 'success',
            analysis: analysis
        });
    } catch (error) {
        res.status(500).json({
            status: 'error',
            message: error.message
        });
    }
});
```

### Răspuns pentru V31
```json
{
    "status": "success",
    "analysis": {
        "symbol": "EURUSD",
        "direction": "BUY",
        "entry_price": 1.08500,
        "sl_price": 1.08300,
        "tp_price": 1.08900,
        "rr_ratio": 2.0,
        "score": 7,
        "indicators": {
            "rsi": 45.2,
            "stoch_k": 25.5,
            "fib_level": "61.8%",
            "in_kill_zone": true,
            "trend_aligned": true,
            "bb_touch": true,
            "fvg_detected": false
        },
        "decision": "ACCEPTED",
        "reason": "All conditions met"
    }
}
```

### Răspuns pentru V32
```json
{
    "status": "success",
    "analysis": {
        "symbol": "EURUSD",
        "direction": "BUY",
        "session_phase": "MAIN_SESSION",
        "current_price": 1.08550,
        "or_high": 1.08400,
        "or_low": 1.08250,
        "or_size_pips": 15.0,
        "conditions": {
            "session_valid": true,
            "or_established": true,
            "or_size_valid": true,
            "breakout": true,
            "decisive_close": true,
            "fvg_valid": true,
            "risk_valid": true
        },
        "body_percent": 65,
        "wick_against": 25,
        "setup_type": "TYPE_A",
        "entry_price": 1.08550,
        "sl_price": 1.08350,
        "tp_price": 1.08950,
        "rr_ratio": 2.0,
        "decision": "ACCEPTED"
    }
}
```

## Verificare După Fix
1. Click pe un simbol în grid
2. Modal-ul ar trebui să se deschidă cu date complete
3. Analiza tehnică ar trebui vizibilă

## Referințe
- Test Case: TC-503
- Fișier raport: TEST-CASES-COMPLETE-REPORT.md
