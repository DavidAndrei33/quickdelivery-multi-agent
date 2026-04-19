# URGENT: Implement Missing APIs in MT5 Core Server
## Priority: CRITICAL
## Created: 2026-03-28 06:48 UTC

---

## 🎯 OBJECTIVE
Implement missing API endpoints DIRECTLY in MT5 Core Server (Python)

---

## 🔴 CRITICAL - Implement These APIs First

### V32 LONDON BREAKOUT APIs

#### API-V32-001: GET /api/v32/or_data
**Assigned to:** Core-Developer-Lead  
**Status:** IN PROGRESS  
**Priority:** CRITICAL  

**Returns:**
```json
{
  "or_high": 1.24567,
  "or_low": 1.24345,
  "or_range": 22.2,
  "current_price": 1.24450,
  "symbol": "GBPUSD",
  "session_date": "2026-03-28",
  "or_start_time": "08:00",
  "or_end_time": "08:15"
}
```

**Implementation:**
- Query MT5 for GBPUSD (and other pairs) 08:00-08:15 candle
- Calculate OR high, low, range
- Get current tick price
- File: `/root/clawd/agents/brainmaker/mt5_core_server.py`
- Add route: `@app.route('/api/v32/or_data', methods=['GET'])`

---

#### API-V32-002: GET /api/v32/asia_data
**Assigned to:** Core-Developer-2  
**Status:** IN PROGRESS  
**Priority:** CRITICAL  

**Returns:**
```json
{
  "asia_high": 1.24680,
  "asia_low": 1.24120,
  "asia_range": 56.0,
  "session_start": "00:00",
  "session_end": "08:00",
  "is_compressed": true
}
```

**Implementation:**
- Query MT5 for 00:00-08:00 (Asia session) high/low
- Calculate range
- Compare with OR range for compression status

---

#### API-V32-003: GET /api/v32/breakout_status
**Assigned to:** Core-Developer-1  
**Status:** IN PROGRESS  
**Priority:** CRITICAL  

**Returns:**
```json
{
  "breakout_detected": true,
  "breakout_direction": "LONG",
  "body_pct": 65.5,
  "wick_pct": 34.5,
  "signal": "BUY",
  "timestamp": "2026-03-28T08:16:23",
  "confidence": 0.85
}
```

**Implementation:**
- Monitor price relative to OR high/low
- Detect when price breaks OR with momentum
- Calculate body/wick percentages from current candle
- Return signal: WAIT, BUY, or SELL

---

#### API-V32-004: GET /api/v32/trade_stats
**Assigned to:** Core-Developer-3  
**Status:** IN PROGRESS  
**Priority:** CRITICAL  

**Returns:**
```json
{
  "trades_taken": 1,
  "max_trades": 2,
  "wins": 1,
  "losses": 0,
  "total_pnl": 45.50,
  "win_rate": 100.0,
  "type_b_pending": false,
  "session_pnl": 45.50
}
```

**Implementation:**
- Query database for today's V32 trades
- Count wins/losses
- Calculate P&L
- Check for pending Type B setups

---

### V33 NY BREAKOUT APIs

#### API-V33-001: GET /api/v33/or_data
**Assigned to:** Core-Developer-Lead  
**Status:** IN PROGRESS  
**Priority:** CRITICAL  

**Returns:**
```json
{
  "or_high": 1.08567,
  "or_low": 1.08345,
  "or_range": 22.2,
  "current_price": 1.08450,
  "symbol": "EURUSD",
  "session_date": "2026-03-28",
  "or_start_time": "13:00",
  "or_end_time": "13:15"
}
```

**Implementation:**
- Same as V32 but for NY session (13:00-13:15)
- Track USD pairs: EURUSD, GBPUSD, etc.

---

#### API-V33-002: GET /api/v33/presession_data
**Assigned to:** Core-Developer-2  
**Status:** IN PROGRESS  
**Priority:** CRITICAL  

**Returns:**
```json
{
  "presession_high": 1.08680,
  "presession_low": 1.08120,
  "presession_range": 56.0,
  "session_start": "08:00",
  "session_end": "13:00",
  "is_compressed": true
}
```

**Implementation:**
- Query MT5 for 08:00-13:00 (pre-NY session)
- Calculate stats and compression

---

#### API-V33-003: GET /api/v33/breakout_status
**Assigned to:** Core-Developer-1  
**Status:** IN PROGRESS  
**Priority:** CRITICAL  

**Same structure as V32** but for NY session (13:15-16:00)

---

#### API-V33-004: GET /api/v33/trade_stats
**Assigned to:** Core-Developer-3  
**Status:** IN PROGRESS  
**Priority:** CRITICAL  

**Same structure as V32** but for V33 robot

---

## 🔶 HIGH PRIORITY - V31 APIs

### V31 MARIUS TPL APIs

#### API-V31-001: GET /api/v31/live_status
**Assigned to:** Integration-Engineer-Lead  
**Status:** PENDING  
**Priority:** HIGH  

**Returns:**
```json
{
  "analyzed": 10,
  "setups_found": 2,
  "rejected": 5,
  "current_symbol": "EURUSD",
  "current_score": 7,
  "cycle_status": "scanning"
}
```

---

#### API-V31-002: GET /api/v31/symbol_status
**Assigned to:** Integration-Engineer-1  
**Status:** PENDING  
**Priority:** HIGH  

**Returns array of:**
```json
{
  "symbol": "EURUSD",
  "trade_open": false,
  "setup_found": true,
  "analyzed": true,
  "pending": false,
  "cooldown_seconds": 0
}
```

---

#### API-V31-003: GET /api/v31/setups
**Assigned to:** Integration-Engineer-2  
**Status:** PENDING  
**Priority:** HIGH  

**Returns array of active setups**

---

#### API-V31-004: GET /api/v31/daily_stats
**Assigned to:** Integration-Engineer-3  
**Status:** PENDING  
**Priority:** HIGH  

**Returns:**
```json
{
  "symbols": 32,
  "setups_found": 5,
  "trades": 2,
  "win_rate": 50.0
}
```

---

## 🛠️ IMPLEMENTATION NOTES

### MT5 Core Server Location
```
/root/clawd/agents/brainmaker/mt5_core_server.py
```

### Adding a New Route (Example)
```python
@app.route('/api/v32/or_data', methods=['GET'])
def get_v32_or_data():
    try:
        symbol = request.args.get('symbol', 'GBPUSD')
        
        # Get OR data from MT5
        or_data = get_opening_range(symbol, "08:00", "08:15")
        
        return jsonify({
            'status': 'success',
            'or_high': or_data['high'],
            'or_low': or_data['low'],
            'or_range': or_data['range'],
            'current_price': get_current_price(symbol)
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
```

### MT5 Functions to Use
```python
# Get candle data
copy_rates(symbol, timeframe, start_time, count)

# Get current price
mt5.symbol_info_tick(symbol).last

# Get account info  
mt5.account_info()

# Get positions
mt5.positions_get(symbol=symbol)
```

### Testing
After implementing, test with:
```bash
curl http://localhost:8001/api/v32/or_data
curl http://localhost:8001/api/v32/breakout_status
curl http://localhost:8001/api/v32/trade_stats
```

---

## ✅ COMPLETION CRITERIA

- [ ] All V32 APIs return live data from MT5
- [ ] All V33 APIs return live data from MT5
- [ ] All V31 APIs return live data from MT5
- [ ] Dashboard elements populate correctly
- [ ] No "--" or static values when MT5 is connected

---

**Priority Order:**
1. V32 OR data + Breakout (most critical)
2. V33 OR data + Breakout
3. V32/V33 Trade Stats
4. V31 APIs

**Estimated Time:** 45-60 minutes for all APIs
