# BUG-004: Missing Robot Status API Endpoints

## Informații Generale
| Atribut | Valoare |
|---------|---------|
| **ID** | BUG-004 |
| **Severitate** | HIGH |
| **Status** | OPEN |
| **Data descoperirii** | 2026-03-28 |
| **Raportat de** | QA-Master Agent |

## Descriere
Toate endpoint-urile API pentru citirea statusului și datelor roboților nu sunt implementate. Dashboard-ul nu poate primi date live fără aceste endpoint-uri.

## Endpoint-uri Lipsă

### V31 Marius TPL
| Metodă | Endpoint | Descriere |
|--------|----------|-----------|
| GET | `/api/v31/live_status` | Status live analiză |

### V32 London Breakout
| Metodă | Endpoint | Descriere |
|--------|----------|-----------|
| GET | `/api/v32/session_status` | Status sesiune |
| GET | `/api/v32/or_data` | Date Opening Range |
| GET | `/api/v32/asia_data` | Date sesiune Asia |
| GET | `/api/v32/breakout_status` | Status breakout |
| GET | `/api/v32/trade_stats` | Statistici tranzacții |

### V33 NY Breakout
| Metodă | Endpoint | Descriere |
|--------|----------|-----------|
| GET | `/api/v33/session_status` | Status sesiune NY |
| GET | `/api/v33/or_data` | Date Opening Range |
| GET | `/api/v33/presession_data` | Date pre-sesiune |
| GET | `/api/v33/breakout_status` | Status breakout |
| GET | `/api/v33/trade_stats` | Statistici tranzacții |

## Test Verificare
```bash
# Toate aceste comenzi returnează 404
curl http://localhost:3000/api/v31/live_status
curl http://localhost:3000/api/v32/session_status
curl http://localhost:3000/api/v32/or_data
curl http://localhost:3000/api/v33/or_data?symbol=EURUSD
```

## Impact
- HIGH: Indicatorii de conexiune nu funcționează
- HIGH: Datele live nu se afișează
- HIGH: Grid-ul de simboluri rămâne gol
- BUG-005, BUG-007, BUG-012 depind de acest bug

## Soluție Propusă

### Implementare Node.js/Express:
```javascript
// În serverul Node.js

const express = require('express');
const router = express.Router();

// ===================== V31 =====================
router.get('/api/v31/live_status', authenticateToken, async (req, res) => {
    try {
        // TODO: Citește date din database sau proces
        const data = await getV31LiveStatus();
        
        res.json({
            status: 'success',
            data: {
                status: data.status || 'IDLE',
                progress: data.progress || 0,
                current_symbol: data.current_symbol || null,
                analyzed_count: data.analyzed_count || 0,
                setups_count: data.setups_count || 0,
                rejected_count: data.rejected_count || 0,
                symbols: data.symbols || [],
                daily_stats: data.daily_stats || {},
                current_setup: data.current_setup || null
            }
        });
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
});

// ===================== V32 =====================
router.get('/api/v32/session_status', authenticateToken, async (req, res) => {
    try {
        const data = await getV32SessionStatus();
        
        res.json({
            status: 'success',
            data: {
                london_time: data.london_time,
                session_phase: data.session_phase || 'BEFORE_SESSION',
                is_active: data.is_active || false,
                time_remaining_seconds: data.time_remaining_seconds || 0
            }
        });
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
});

router.get('/api/v32/or_data', authenticateToken, async (req, res) => {
    try {
        const data = await getV32ORData();
        
        res.json({
            status: 'success',
            data: {
                or_high: data.or_high || 0,
                or_low: data.or_low || 0,
                current_price: data.current_price || 0
            }
        });
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
});

router.get('/api/v32/asia_data', authenticateToken, async (req, res) => {
    try {
        const data = await getV32AsiaData();
        
        res.json({
            status: 'success',
            data: {
                asia_high: data.asia_high || 0,
                asia_low: data.asia_low || 0,
                is_compressed: data.is_compressed || false
            }
        });
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
});

router.get('/api/v32/breakout_status', authenticateToken, async (req, res) => {
    try {
        const data = await getV32BreakoutStatus();
        
        res.json({
            status: 'success',
            data: {
                breakout_status: data.breakout_status || 'WAITING',
                setup_type: data.setup_type || '-',
                body_percent: data.body_percent || 0,
                wick_percent: data.wick_percent || 0,
                signal: data.signal || 'WAIT'
            }
        });
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
});

router.get('/api/v32/trade_stats', authenticateToken, async (req, res) => {
    try {
        const data = await getV32TradeStats();
        
        res.json({
            status: 'success',
            data: {
                trades_count: data.trades_count || 0,
                wins: data.wins || 0,
                losses: data.losses || 0,
                total_pnl: data.total_pnl || 0,
                type_b_pending: data.type_b_pending || false
            }
        });
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
});

// ===================== V33 =====================
// Similar cu V32, dar pentru NY
router.get('/api/v33/session_status', authenticateToken, async (req, res) => {
    try {
        const data = await getV33SessionStatus();
        
        res.json({
            status: 'success',
            data: {
                ny_time: data.ny_time,
                session_phase: data.session_phase || 'BEFORE_SESSION',
                is_active: data.is_active || false,
                time_remaining_seconds: data.time_remaining_seconds || 0
            }
        });
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
});

router.get('/api/v33/or_data', authenticateToken, async (req, res) => {
    try {
        const symbol = req.query.symbol || 'EURUSD';
        const data = await getV33ORData(symbol);
        
        res.json({
            status: 'success',
            data: {
                or_high: data.or_high || 0,
                or_low: data.or_low || 0,
                current_price: data.current_price || 0
            }
        });
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
});

router.get('/api/v33/presession_data', authenticateToken, async (req, res) => {
    try {
        const symbol = req.query.symbol || 'EURUSD';
        const data = await getV33PreSessionData(symbol);
        
        res.json({
            status: 'success',
            data: {
                pre_session_high: data.pre_session_high || 0,
                pre_session_low: data.pre_session_low || 0,
                pre_session_range_pips: data.pre_session_range_pips || 0,
                is_compressed: data.is_compressed || false
            }
        });
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
});

router.get('/api/v33/breakout_status', authenticateToken, async (req, res) => {
    try {
        const symbol = req.query.symbol || 'EURUSD';
        const data = await getV33BreakoutStatus(symbol);
        
        res.json({
            status: 'success',
            data: {
                breakout_status: data.breakout_status || 'WAITING',
                setup_type: data.setup_type || '-',
                body_percent: data.body_percent || 0,
                wick_percent: data.wick_percent || 0,
                signal: data.signal || 'WAIT'
            }
        });
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
});

router.get('/api/v33/trade_stats', authenticateToken, async (req, res) => {
    try {
        const symbol = req.query.symbol || 'EURUSD';
        const data = await getV33TradeStats(symbol);
        
        res.json({
            status: 'success',
            data: {
                trades_count: data.trades_count || 0,
                wins: data.wins || 0,
                losses: data.losses || 0,
                total_pnl: data.total_pnl || 0,
                type_b_pending: data.type_b_pending || false
            }
        });
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
});

// TODO: Implementează funcțiile helper pentru citirea datelor
async function getV31LiveStatus() { /* ... */ }
async function getV32SessionStatus() { /* ... */ }
async function getV32ORData() { /* ... */ }
// etc.
```

## Structură Date

### V31 Live Status Response
```json
{
    "status": "success",
    "data": {
        "status": "SCANNING",
        "progress": 45,
        "current_symbol": "EURUSD",
        "analyzed_count": 15,
        "setups_count": 2,
        "rejected_count": 13,
        "symbols": [
            {"symbol": "EURUSD", "analyzed": true, "setup_found": false},
            {"symbol": "GBPUSD", "analyzed": true, "setup_found": true}
        ],
        "daily_stats": {
            "setups_today": 5,
            "trades_today": 2,
            "win_rate": 50
        },
        "current_setup": {
            "symbol": "GBPUSD",
            "direction": "BUY",
            "rsi_score": 2,
            "stoch_score": 2,
            "fib_score": 2,
            "total_score": 6
        }
    }
}
```

## Referințe
- Test Cases: TC-201-209, TC-302, TC-306, TC-502, TC-503
- Fișier raport: TEST-CASES-COMPLETE-REPORT.md
- Depended upon by: BUG-005, BUG-007, BUG-012
