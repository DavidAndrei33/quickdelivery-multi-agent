# API Endpoint Status Report

**Generated:** 2026-03-28 06:44 UTC  
**Server:** http://localhost:8001  
**Total Endpoints Checked:** 17  
**Existing:** 4  
**Missing:** 13

---

## Summary

| Version | Existing | Missing | Status |
|---------|----------|---------|--------|
| V31 | 0/5 | 5 | ❌ Not Implemented |
| V32 | 2/6 | 4 | ⚠️ Partial |
| V33 | 2/6 | 4 | ⚠️ Partial |

---

## V31 Endpoints (London Breakout Strategy)

All V31 endpoints return **404 Not Found** - these endpoints are NOT implemented.

### Endpoints Status

| Endpoint | Status | HTTP Code |
|----------|--------|-----------|
| GET /api/v31/live_status | ❌ MISSING | 404 |
| GET /api/v31/symbol_status | ❌ MISSING | 404 |
| GET /api/v31/setups | ❌ MISSING | 404 |
| GET /api/v31/daily_stats | ❌ MISSING | 404 |
| GET /api/v31/logs | ❌ MISSING | 404 |

### Expected Data for Missing V31 Endpoints

#### GET /api/v31/live_status
Should return real-time London session status:
```json
{
  "status": "success",
  "is_active": true/false,
  "london_time": "HH:MM:SS",
  "session_phase": "ASIA|OPEN_RANGE|TRADING|CLOSED",
  "time_remaining_minutes": 0
}
```

#### GET /api/v31/symbol_status
Should return symbol analysis status for London breakout symbols (EURGBP, GBPAUD, etc.).

#### GET /api/v31/setups
Should return detected trade setups with entry/exit levels.

#### GET /api/v31/daily_stats
Should return daily trading statistics (wins, losses, P&L).

#### GET /api/v31/logs
Should return system logs for the V31 strategy.

---

## V32 Endpoints (London Breakout Strategy - Enhanced)

### Endpoints Status

| Endpoint | Status | HTTP Code |
|----------|--------|-----------|
| GET /api/v32/session_status | ✅ EXISTS | 200 |
| GET /api/v32/symbol_status | ✅ EXISTS | 200 |
| GET /api/v32/or_data | ❌ MISSING | 404 |
| GET /api/v32/asia_data | ❌ MISSING | 404 |
| GET /api/v32/breakout_status | ❌ MISSING | 404 |
| GET /api/v32/trade_stats | ❌ MISSING | 404 |

### Existing V32 Endpoints

#### ✅ GET /api/v32/session_status
**Status:** EXISTS (HTTP 200)

**Sample Response:**
```json
{
  "is_active": false,
  "london_hour": 6,
  "london_minute": 45,
  "london_time": "06:45:07",
  "session_phase": "BEFORE_SESSION",
  "status": "success",
  "status_text": "Waiting",
  "time_remaining_minutes": 75,
  "time_remaining_seconds": 4500
}
```

**Fields:**
- `is_active`: boolean - Whether trading session is active
- `london_hour/minute`: int - Current London time
- `session_phase`: string - Current phase (BEFORE_SESSION, ASIA, OPEN_RANGE, TRADING, CLOSED)
- `time_remaining_*`: int - Time until next phase

---

#### ✅ GET /api/v32/symbol_status
**Status:** EXISTS (HTTP 200)

**Sample Response:**
```json
{
  "count": 7,
  "status": "success",
  "symbols": [
    {
      "analysis_time": null,
      "analyzed": false,
      "asia_high": null,
      "asia_low": null,
      "asia_range": null,
      "breakout_detected": false,
      "breakout_direction": null,
      "cooldown_until": null,
      "or_high": null,
      "or_low": null,
      "or_range": null,
      "signal": null,
      "symbol": "EURGBP",
      "trade_opened": false,
      "trade_ticket": null
    }
    // ... 6 more symbols (GBPAUD, GBPCAD, GBPCHF, GBPJPY, GBPNZD, GBPUSD)
  ]
}
```

**Symbols Tracked:** EURGBP, GBPAUD, GBPCAD, GBPCHF, GBPJPY, GBPNZD, GBPUSD

**Fields:**
- `analyzed`: boolean - Whether symbol has been analyzed
- `asia_high/low/range`: float - Asia session data
- `or_high/low/range`: float - Opening range data
- `breakout_detected`: boolean - Whether breakout was detected
- `breakout_direction`: string - "LONG", "SHORT", or null
- `signal`: string - Trading signal
- `trade_opened`: boolean - Whether position is open
- `trade_ticket`: int - MT5 trade ticket ID

---

### Missing V32 Endpoints

#### GET /api/v32/or_data
Should return Opening Range (7:00-9:00 London) high/low/range data for all symbols.

#### GET /api/v32/asia_data
Should return Asia session (0:00-7:00 London) high/low/range data.

#### GET /api/v32/breakout_status
Should return current breakout detection status with triggered levels.

#### GET /api/v32/trade_stats
Should return trading statistics (total trades, win rate, P&L, etc.).

---

## V33 Endpoints (New York Breakout Strategy)

### Endpoints Status

| Endpoint | Status | HTTP Code |
|----------|--------|-----------|
| GET /api/v33/session_status | ✅ EXISTS | 200 |
| GET /api/v33/symbol_status | ✅ EXISTS | 200 |
| GET /api/v33/or_data | ❌ MISSING | 404 |
| GET /api/v33/presession_data | ❌ MISSING | 404 |
| GET /api/v33/breakout_status | ❌ MISSING | 404 |
| GET /api/v33/trade_stats | ❌ MISSING | 404 |

### Existing V33 Endpoints

#### ✅ GET /api/v33/session_status
**Status:** EXISTS (HTTP 200)

**Sample Response:**
```json
{
  "is_active": false,
  "ny_hour": 2,
  "ny_minute": 45,
  "ny_time": "02:45:07",
  "session_phase": "BEFORE_SESSION",
  "status": "success",
  "status_text": "Waiting",
  "time_remaining_minutes": 615,
  "time_remaining_seconds": 36900
}
```

**Fields:**
- `is_active`: boolean - Whether NY session is active
- `ny_hour/minute`: int - Current New York time
- `session_phase`: string - Current phase
- `time_remaining_*`: int - Time until session start

**Note:** Uses NY time (vs London time in V32).

---

#### ✅ GET /api/v33/symbol_status
**Status:** EXISTS (HTTP 200)

**Sample Response:**
```json
{
  "count": 7,
  "status": "success",
  "symbols": [
    {
      "analysis_time": null,
      "analyzed": false,
      "breakout_detected": false,
      "breakout_direction": null,
      "cooldown_until": null,
      "or_high": null,
      "or_low": null,
      "or_range": null,
      "pre_high": null,
      "pre_low": null,
      "pre_range": null,
      "signal": null,
      "symbol": "AUDUSD",
      "trade_opened": false,
      "trade_ticket": null
    }
    // ... 6 more symbols (EURUSD, GBPUSD, NZDUSD, USDCAD, USDCHF, USDJPY)
  ]
}
```

**Symbols Tracked:** AUDUSD, EURUSD, GBPUSD, NZDUSD, USDCAD, USDCHF, USDJPY

**Note:** Uses USD pairs (vs GBP pairs in V32) and has `pre_*` fields (pre-session) instead of `asia_*`.

---

### Missing V33 Endpoints

#### GET /api/v33/or_data
Should return Opening Range (9:30-10:30 NY) high/low/range data for all USD symbols.

#### GET /api/v33/presession_data
Should return pre-session data (Asia + London overlap before NY open).

#### GET /api/v33/breakout_status
Should return current breakout detection status for NY session.

#### GET /api/v33/trade_stats
Should return NY session trading statistics.

---

## Key Differences: V32 vs V33

| Aspect | V32 (London) | V33 (New York) |
|--------|--------------|----------------|
| Currency Pairs | GBP pairs (EURGBP, GBPAUD, etc.) | USD pairs (EURUSD, GBPUSD, etc.) |
| Session Time | 7:00-9:00 London | 9:30-10:30 NY |
| Pre-Session | Asia (asia_*) | Pre-Session (pre_*) |
| Time Reference | London time | New York time |

---

## Recommendations

### Priority 1 (Critical for Dashboard)
1. Implement `/api/v32/or_data` and `/api/v33/or_data` - Opening range data is essential
2. Implement `/api/v32/breakout_status` and `/api/v33/breakout_status` - Core functionality

### Priority 2 (Analytics)
3. Implement `/api/v32/trade_stats` and `/api/v33/trade_stats` - Performance tracking
4. Implement `/api/v32/asia_data` and `/api/v33/presession_data` - Historical context

### Priority 3 (Legacy)
5. Either implement V31 endpoints or deprecate V31 entirely (all missing)

---

## Quick Reference for Other Agents

**Use these endpoints (WORKING):**
- `GET http://localhost:8001/api/v32/session_status`
- `GET http://localhost:8001/api/v32/symbol_status`
- `GET http://localhost:8001/api/v33/session_status`
- `GET http://localhost:8001/api/v33/symbol_status`

**These endpoints are NOT available (404):**
- All `/api/v31/*` endpoints
- `/api/v32/or_data`, `/api/v32/asia_data`, `/api/v32/breakout_status`, `/api/v32/trade_stats`
- `/api/v33/or_data`, `/api/v33/presession_data`, `/api/v33/breakout_status`, `/api/v33/trade_stats`
