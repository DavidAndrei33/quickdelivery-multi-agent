# 📋 SPECIFICAȚII LOGURI ROBOT - V31 / V32 / V33

## SCOP
Documentație completă pentru loguri specifice fiecărui robot, cu exact ce trebuie logat în fiecare punct/moment.

---

# 🤖 V31 - MARIUS TPL (Trend + Price Level)

## 1. INITIALIZARE ROBOT

### Log STARTUP
```python
log_entry = {
    "timestamp": "2026-03-28T13:00:00.000Z",
    "robot": "V31_Marius_TPL",
    "level": "INFO",
    "event": "ROBOT_STARTUP",
    "message": "V31 Robot initialized successfully",
    "details": {
        "version": "2.1.0",
        "config": {
            "symbols": ["EURUSD", "GBPUSD", "USDJPY"],
            "timeframe": "M5",
            "max_trades_per_session": 2,
            "risk_percent": 1.0,
            "fib_levels": [0.382, 0.5, 0.618, 0.786],
            "min_score_for_trade": 6
        },
        "database_connected": True,
        "mt5_bridge_status": "connected"
    }
}
```

---

## 2. ANALIZĂ SYMBOL (La fiecare candle nou)

### Log SYMBOL_ANALYSIS_START
```python
log_entry = {
    "timestamp": "2026-03-28T13:05:00.000Z",
    "robot": "V31_Marius_TPL",
    "level": "DEBUG",
    "event": "SYMBOL_ANALYSIS_START",
    "symbol": "EURUSD",
    "message": "Starting analysis for EURUSD M5",
    "details": {
        "candle_time": "2026-03-28T13:00:00Z",
        "open": 1.08450,
        "high": 1.08520,
        "low": 1.08410,
        "close": 1.08480,
        "volume": 1250
    }
}
```

### Log TECHNICAL_INDICATORS
```python
log_entry = {
    "timestamp": "2026-03-28T13:05:01.000Z",
    "robot": "V31_Marius_TPL",
    "level": "DEBUG",
    "event": "TECHNICAL_INDICATORS",
    "symbol": "EURUSD",
    "message": "Technical indicators calculated",
    "details": {
        "rsi": {
            "value": 58.4,
            "period": 14,
            "interpretation": "neutral_zone"  # RSI între 45-65
        },
        "stochastic": {
            "k": 62.5,
            "d": 58.3,
            "signal": "rising"
        },
        "bollinger": {
            "upper": 1.08650,
            "middle": 1.08480,
            "lower": 1.08310,
            "position": "upper_half"  # Preț în jumătatea superioară
        },
        "ema": {
            "ema20": 1.08420,
            "ema50": 1.08350,
            "trend": "bullish_short"  # EMA20 > EMA50
        }
    }
}
```

### Log FIBONACCI_ANALYSIS
```python
log_entry = {
    "timestamp": "2026-03-28T13:05:02.000Z",
    "robot": "V31_Marius_TPL",
    "level": "DEBUG",
    "event": "FIBONACCI_ANALYSIS",
    "symbol": "EURUSD",
    "message": "Fibonacci retracement levels calculated",
    "details": {
        "swing_high": 1.08600,
        "swing_low": 1.08200,
        "levels": {
            "0.0": 1.08600,
            "0.382": 1.08447,
            "0.5": 1.08400,
            "0.618": 1.08353,
            "1.0": 1.08200
        },
        "current_price_position": "between_382_50",
        "nearest_level": 0.382,
        "distance_to_level": 0.00033
    }
}
```

### Log KILL_ZONE_CHECK
```python
log_entry = {
    "timestamp": "2026-03-28T13:05:03.000Z",
    "robot": "V31_Marius_TPL",
    "level": "INFO",
    "event": "KILL_ZONE_CHECK",
    "symbol": "EURUSD",
    "message": "Kill zone validation",
    "details": {
        "current_time": "13:05",
        "kill_zones": [
            {"start": "08:00", "end": "10:00", "session": "london_open", "active": False},
            {"start": "13:30", "end": "15:30", "session": "ny_open", "active": False}
        ],
        "in_kill_zone": False,
        "next_kill_zone": "ny_open",
        "minutes_until_next": 25
    }
}
```

---

## 3. SCORING SETUP

### Log SETUP_SCORING
```python
log_entry = {
    "timestamp": "2026-03-28T13:05:04.000Z",
    "robot": "V31_Marius_TPL",
    "level": "INFO",
    "event": "SETUP_SCORING",
    "symbol": "EURUSD",
    "message": "Setup scored 7/10 - Sufficient for trade consideration",
    "details": {
        "total_score": 7,
        "max_score": 10,
        "breakdown": {
            "trend_alignment": {
                "score": 2,
                "max": 2,
                "reason": "Price above EMA20 and EMA50, bullish trend"
            },
            "fibonacci_proximity": {
                "score": 2,
                "max": 2,
                "reason": "Price within 10 pips of 0.618 level"
            },
            "kill_zone": {
                "score": 0,
                "max": 2,
                "reason": "Outside kill zone hours"
            },
            "rsi_condition": {
                "score": 1,
                "max": 1,
                "reason": "RSI in neutral zone (45-65)"
            },
            "stochastic_alignment": {
                "score": 1,
                "max": 1,
                "reason": "Stochastic rising"
            },
            "bollinger_position": {
                "score": 1,
                "max": 1,
                "reason": "Price in upper half"
            },
            "volume_confirmation": {
                "score": 0,
                "max": 1,
                "reason": "Volume below average"
            }
        },
        "trade_eligible": True,
        "min_required": 6
    }
}
```

---

## 4. DECIZIE TRADE

### Log TRADE_DECISION_POSITIVE
```python
log_entry = {
    "timestamp": "2026-03-28T13:05:05.000Z",
    "robot": "V31_Marius_TPL",
    "level": "INFO",
    "event": "TRADE_DECISION",
    "symbol": "EURUSD",
    "message": "✅ TRADE SIGNAL GENERATED - BUY",
    "details": {
        "decision": "ENTER_TRADE",
        "direction": "BUY",
        "confidence": "high",
        "score": 7,
        "setup_type": "fib_618_bounce",
        "entry_price": 1.08480,
        "sl_price": 1.08350,
        "tp_price": 1.08650,
        "sl_pips": 13,
        "tp_pips": 17,
        "risk_reward": 1.3,
        "position_size": 0.01,
        "reasoning": [
            "Price retraced to 0.618 fib level",
            "Bullish trend on EMAs",
            "Score 7/10 exceeds minimum 6",
            "RSI neutral allowing upward movement"
        ]
    }
}
```

### Log TRADE_DECISION_NEGATIVE
```python
log_entry = {
    "timestamp": "2026-03-28T13:05:05.000Z",
    "robot": "V31_Marius_TPL",
    "level": "INFO",
    "event": "TRADE_DECISION",
    "symbol": "EURUSD",
    "message": "❌ NO TRADE - Score below threshold",
    "details": {
        "decision": "NO_TRADE",
        "score": 4,
        "min_required": 6,
        "reasons": [
            "Kill zone inactive",
            "Volume too low",
            "Stochastic not aligned"
        ],
        "recommendation": "Continue monitoring"
    }
}
```

---

## 5. EXECUȚIE COMANDĂ

### Log COMMAND_SENT
```python
log_entry = {
    "timestamp": "2026-03-28T13:05:06.000Z",
    "robot": "V31_Marius_TPL",
    "level": "INFO",
    "event": "COMMAND_SENT",
    "symbol": "EURUSD",
    "message": "Trade command sent to MT5 Core Server",
    "details": {
        "command_id": "CMD-20260328-130506-001",
        "action": "OPEN",
        "direction": "BUY",
        "symbol": "EURUSD",
        "volume": 0.01,
        "entry_price": 1.08480,
        "sl": 1.08350,
        "tp": 1.08650,
        "client_login": 52715350,
        "status": "queued",
        "estimated_execution": "< 500ms"
    }
}
```

### Log COMMAND_CONFIRMED
```python
log_entry = {
    "timestamp": "2026-03-28T13:05:06.450Z",
    "robot": "V31_Marius_TPL",
    "level": "INFO",
    "event": "COMMAND_CONFIRMED",
    "symbol": "EURUSD",
    "message": "Trade executed successfully",
    "details": {
        "command_id": "CMD-20260328-130506-001",
        "ticket": 1561808052,
        "execution_price": 1.08482,
        "slippage_pips": 0.2,
        "execution_time_ms": 450,
        "status": "executed",
        "mt5_response": "success"
    }
}
```

### Log COMMAND_FAILED
```python
log_entry = {
    "timestamp": "2026-03-28T13:05:07.000Z",
    "robot": "V31_Marius_TPL",
    "level": "ERROR",
    "event": "COMMAND_FAILED",
    "symbol": "EURUSD",
    "message": "❌ Trade execution failed",
    "details": {
        "command_id": "CMD-20260328-130506-001",
        "error_code": "INSUFFICIENT_MARGIN",
        "error_message": "Not enough margin to open position",
        "retry_count": 0,
        "action": "NOTIFY_USER"
    }
}
```

---

## 6. MONITORIZARE POZIȚIE

### Log POSITION_MONITORING
```python
log_entry = {
    "timestamp": "2026-03-28T13:10:00.000Z",
    "robot": "V31_Marius_TPL",
    "level": "DEBUG",
    "event": "POSITION_MONITORING",
    "symbol": "EURUSD",
    "message": "Position status update",
    "details": {
        "ticket": 1561808052,
        "direction": "BUY",
        "entry_price": 1.08482,
        "current_price": 1.08510,
        "profit_pips": 2.8,
        "profit_usd": 2.80,
        "profit_percent": 0.21,
        "distance_to_sl_pips": 16.0,
        "distance_to_tp_pips": 14.0,
        "duration_minutes": 5,
        "status": "in_profit"
    }
}
```

### Log BREAKEVEN_TRIGGERED
```python
log_entry = {
    "timestamp": "2026-03-28T13:15:00.000Z",
    "robot": "V31_Marius_TPL",
    "level": "INFO",
    "event": "BREAKEVEN_TRIGGERED",
    "symbol": "EURUSD",
    "message": "🛡️ SL moved to breakeven (1.5R reached)",
    "details": {
        "ticket": 1561808052,
        "old_sl": 1.08350,
        "new_sl": 1.08482,
        "trigger_price": 1.08620,
        "r_multiple": 1.5,
        "risk_free": True
    }
}
```

---

## 7. ÎNCHIDERE POZIȚIE

### Log POSITION_CLOSED
```python
log_entry = {
    "timestamp": "2026-03-28T13:25:00.000Z",
    "robot": "V31_Marius_TPL",
    "level": "INFO",
    "event": "POSITION_CLOSED",
    "symbol": "EURUSD",
    "message": "🏁 Position closed - TP Hit",
    "details": {
        "ticket": 1561808052,
        "close_reason": "TAKE_PROFIT",
        "entry_price": 1.08482,
        "exit_price": 1.08650,
        "profit_pips": 16.8,
        "profit_usd": 16.80,
        "duration_minutes": 20,
        "r_multiple": 1.29,
        "session_result": "win"
    }
}
```

---

# 🌅 V32 - LONDON BREAKOUT

## 1. INITIALIZARE ȘI CONFIGURARE SIMBOLURI

### Log ROBOT_STARTUP
```python
log_entry = {
    "timestamp": "2026-03-28T07:00:00.000Z",
    "robot": "V32_London_Breakout",
    "level": "INFO",
    "event": "ROBOT_STARTUP",
    "message": "V32 London Breakout Robot initialized",
    "details": {
        "version": "2.0.0",
        "session": "London",
        "session_hours": {"start": "08:00", "end": "17:00"},
        "symbols_configured": 7,
        "symbols": ["GBPUSD", "EURGBP", "GBPAUD", "GBPJPY", "GBPCAD", "GBPCHF", "GBPNZD"],
        "asia_session_end": "08:00",
        "or_calculation_start": "08:00",
        "or_calculation_duration_minutes": 60
    }
}
```

---

## 2. SESIUNEA ASIATICĂ (Pre-London)

### Log ASIA_SESSION_ANALYSIS
```python
log_entry = {
    "timestamp": "2026-03-28T07:30:00.000Z",
    "robot": "V32_London_Breakout",
    "level": "INFO",
    "event": "ASIA_SESSION_ANALYSIS",
    "symbol": "GBPUSD",
    "message": "Asian session range calculated",
    "details": {
        "asia_session": {
            "start": "00:00",
            "end": "08:00",
            "active": True,
            "minutes_remaining": 30
        },
        "asia_range": {
            "high": 1.27450,
            "low": 1.27200,
            "range_pips": 25,
            "mid": 1.27325
        },
        "volatility": "low",  # vs "high"
        "london_preview": "potential_expansion"
    }
}
```

---

## 3. CALCULARE OPENING RANGE (OR)

### Log OR_CALCULATION_START
```python
log_entry = {
    "timestamp": "2026-03-28T08:00:00.000Z",
    "robot": "V32_London_Breakout",
    "level": "INFO",
    "event": "OR_CALCULATION_START",
    "symbol": "GBPUSD",
    "message": "⏱️ Opening Range calculation started (08:00-09:00)",
    "details": {
        "or_window": {
            "start": "08:00",
            "end": "09:00",
            "duration_minutes": 60
        },
        "current_price": 1.27350,
        "status": "collecting_candles"
    }
}
```

### Log OR_CANDLE_UPDATE (La fiecare candle în OR)
```python
log_entry = {
    "timestamp": "2026-03-28T08:05:00.000Z",
    "robot": "V32_London_Breakout",
    "level": "DEBUG",
    "event": "OR_CANDLE_UPDATE",
    "symbol": "GBPUSD",
    "message": "OR candle #1 recorded",
    "details": {
        "candle_number": 1,
        "time": "08:00-08:05",
        "open": 1.27350,
        "high": 1.27400,
        "low": 1.27320,
        "close": 1.27380,
        "or_high_current": 1.27400,
        "or_low_current": 1.27320,
        "or_range_pips": 8,
        "minutes_remaining": 55
    }
}
```

### Log OR_FINAL
```python
log_entry = {
    "timestamp": "2026-03-28T09:00:00.000Z",
    "robot": "V32_London_Breakout",
    "level": "INFO",
    "event": "OR_FINAL",
    "symbol": "GBPUSD",
    "message": "✅ Opening Range finalized",
    "details": {
        "or_period": "08:00-09:00",
        "or_high": 1.27550,
        "or_low": 1.27280,
        "or_range_pips": 27,
        "candles_count": 12,
        "breakout_threshold": 1.5,  # Multiplier pentru range
        "body_percentage_required": 60,
        "status": "WAITING_BREAKOUT"
    }
}
```

---

## 4. DETECTARE BREAKOUT

### Log BREAKOUT_DETECTION
```python
log_entry = {
    "timestamp": "2026-03-28T09:15:00.000Z",
    "robot": "V32_London_Breakout",
    "level": "INFO",
    "event": "BREAKOUT_DETECTION",
    "symbol": "GBPUSD",
    "message": "🔍 Monitoring for breakout",
    "details": {
        "current_price": 1.27620,
        "or_high": 1.27550,
        "or_low": 1.27280,
        "breakout_levels": {
            "long_entry": 1.27590,  # OR high + buffer
            "short_entry": 1.27250   # OR low - buffer
        },
        "distance_to_long": -30,  # pips (negative = above)
        "distance_to_short": 37,  # pips
        "trend_bias": "bullish",
        "asia_break": False  # Price still within Asia range
    }
}
```

### Log BREAKOUT_CONFIRMED
```python
log_entry = {
    "timestamp": "2026-03-28T09:23:00.000Z",
    "robot": "V32_London_Breakout",
    "level": "INFO",
    "event": "BREAKOUT_CONFIRMED",
    "symbol": "GBPUSD",
    "message": "✅ VALID BREAKOUT DETECTED - LONG",
    "details": {
        "breakout_type": "TYPE_A",  # Type A: >50% body outside OR
        "direction": "LONG",
        "entry_candle": {
            "open": 1.27560,
            "high": 1.27680,
            "low": 1.27540,
            "close": 1.27650,
            "body_size": 9,
            "body_percentage": 69,  # > 60% required
            "wick_percentage": 22   # < 30% required
        },
        "confirmation": {
            "body_outside_or": True,
            "body_percentage_ok": True,
            "wick_percentage_ok": True,
            "momentum_aligned": True
        },
        "entry_price": 1.27650,
        "sl_price": 1.27450,  # Below OR low
        "tp_price": 1.27950,  # 1:2 RR
        "position_size": 0.01,
        "entry_type": "IMMEDIATE"
    }
}
```

### Log TYPE_B_SETUP (Dacă nu e Type A)
```python
log_entry = {
    "timestamp": "2026-03-28T09:25:00.000Z",
    "robot": "V32_London_Breakout",
    "level": "INFO",
    "event": "TYPE_B_SETUP",
    "symbol": "GBPUSD",
    "message": "⏳ Type B setup - Waiting for confirmation candle",
    "details": {
        "breakout_type": "TYPE_B_PENDING",
        "first_candle": {
            "body_outside": False,  # < 50% body outside
            "close": "inside_or"
        },
        "waiting_for": "confirmation_candle",
        "expected": "continuation_in_same_direction",
        "timeout": "next_candle_close"
    }
}
```

---

## 5. GESTIONARE POZIȚIE V32

### Log POSITION_MANAGEMENT
```python
log_entry = {
    "timestamp": "2026-03-28T10:00:00.000Z",
    "robot": "V32_London_Breakout",
    "level": "INFO",
    "event": "POSITION_MANAGEMENT",
    "symbol": "GBPUSD",
    "message": "Position management - Holding",
    "details": {
        "ticket": 1561809001,
        "direction": "LONG",
        "entry": 1.27650,
        "current": 1.27780,
        "profit_pips": 13,
        "r_multiple": 0.65,
        "rules": {
            "no_early_exit": True,
            "no_sl_modification": True,
            "breakeven_at_1_5r": False  # Not reached yet
        },
        "decision": "HOLD"
    }
}
```

### Log DAILY_LIMIT_REACHED
```python
log_entry = {
    "timestamp": "2026-03-28T11:30:00.000Z",
    "robot": "V32_London_Breakout",
    "level": "WARNING",
    "event": "DAILY_LIMIT_REACHED",
    "symbol": "GBPUSD",
    "message": "⚠️ Daily trade limit reached (2/2)",
    "details": {
        "trades_today": 2,
        "max_allowed": 2,
        "wins": 1,
        "losses": 0,
        "status": "STAND_BY",
        "next_opportunity": "tomorrow_london_session"
    }
}
```

---

# 🗽 V33 - NEW YORK BREAKOUT

## 1. INITIALIZARE

### Log ROBOT_STARTUP
```python
log_entry = {
    "timestamp": "2026-03-28T12:00:00.000Z",
    "robot": "V33_NY_Breakout",
    "level": "INFO",
    "event": "ROBOT_STARTUP",
    "message": "V33 NY Breakout Robot initialized",
    "details": {
        "version": "2.0.0",
        "session": "New York",
        "session_hours": {"start": "13:30", "end": "22:00"},
        "symbols": ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "USDCHF", "NZDUSD"],
        "pre_session_start": "13:00",
        "or_start": "13:30",
        "or_duration": 60
    }
}
```

---

## 2. PRE-SESSION (Înainte de NY)

### Log PRESESSION_ANALYSIS
```python
log_entry = {
    "timestamp": "2026-03-28T13:00:00.000Z",
    "robot": "V33_NY_Breakout",
    "level": "INFO",
    "event": "PRESESSION_ANALYSIS",
    "symbol": "EURUSD",
    "message": "Pre-session analysis for NY Opening",
    "details": {
        "time_until_session": "30 minutes",
        "london_session_status": "active",
        "london_or": {
            "high": 1.08550,
            "low": 1.08300
        },
        "current_price": 1.08420,
        "position_vs_london": "middle_of_range",
        "expected_ny_behavior": "potential_breakout",
        "economic_calendar": {
            "high_impact_news": [],
            "medium_impact": ["14:30 USD Retail Sales"],
            "risk_level": "medium"
        }
    }
}
```

---

## 3. CALCULARE OR (Identic cu V32 dar pentru NY)

### Log OR_CALCULATION_START
```python
log_entry = {
    "timestamp": "2026-03-28T13:30:00.000Z",
    "robot": "V33_NY_Breakout",
    "level": "INFO",
    "event": "OR_CALCULATION_START",
    "symbol": "EURUSD",
    "message": "⏱️ NY Opening Range started (13:30-14:30)",
    "details": {
        "or_window": "13:30-14:30 EST",
        "overlaps_with": "london_afternoon",
        "liquidity": "high",
        "status": "collecting_data"
    }
}
```

---

## 4. BREAKOUT ȘI ENTRY

### Log BREAKOUT_WITH_OVERLAP
```python
log_entry = {
    "timestamp": "2026-03-28T14:45:00.000Z",
    "robot": "V33_NY_Breakout",
    "level": "INFO",
    "event": "BREAKOUT_WITH_OVERLAP",
    "symbol": "EURUSD",
    "message": "✅ Breakout during London-NY overlap",
    "details": {
        "time": "14:45",
        "overlap_active": True,
        "liquidity": "maximum",
        "ny_or_high": 1.08600,
        "ny_or_low": 1.08450,
        "breakout_direction": "LONG",
        "entry_price": 1.08610,
        "sl": 1.08430,
        "tp": 1.08810,
        "volume_confirmed": True,
        "spread": 0.8  # pips - acceptable during overlap
    }
}
```

---

## 5. POST-SESSION ANALYSIS

### Log SESSION_SUMMARY
```python
log_entry = {
    "timestamp": "2026-03-28T22:00:00.000Z",
    "robot": "V33_NY_Breakout",
    "level": "INFO",
    "event": "SESSION_SUMMARY",
    "message": "📊 NY Session completed",
    "details": {
        "session": "2026-03-28",
        "symbols_analyzed": 7,
        "trades_taken": 2,
        "trades": [
            {
                "symbol": "EURUSD",
                "direction": "LONG",
                "entry": 1.08610,
                "exit": 1.08810,
                "profit_pips": 20,
                "result": "WIN"
            },
            {
                "symbol": "USDJPY",
                "direction": "SHORT",
                "entry": 149.500,
                "exit": 149.300,
                "profit_pips": 20,
                "result": "WIN"
            }
        ],
        "total_pips": 40,
        "win_rate": "100%",
        "next_session": "2026-03-29T13:30:00Z"
    }
}
```

---

# 📝 FORMAT GENERAL LOGURI

## Niveluri Log

```python
LOG_LEVELS = {
    "DEBUG": "Informații detaliate pentru debugging",
    "INFO": "Evenimente normale ale sistemului",
    "WARNING": "Atenționări, posibile probleme",
    "ERROR": "Erori care necesită atenție",
    "CRITICAL": "Erori critice, sistem afectat"
}
```

## Structura Standard

```json
{
    "timestamp": "ISO 8601 format",
    "robot": "V31_Marius_TPL | V32_London_Breakout | V33_NY_Breakout",
    "level": "DEBUG | INFO | WARNING | ERROR | CRITICAL",
    "event": "NUME_EVENIMENT_UNIQ",
    "symbol": "SYMBOL (optional)",
    "message": "Mesaj lizibil pentru om",
    "details": {
        "...": "Orice date relevante pentru eveniment"
    }
}
```

## Destinație Loguri

| Tip | Destinație | Retenție |
|-----|------------|----------|
| DEBUG | Fișier local + DB | 7 zile |
| INFO | Fișier + DB + Dashboard | 30 zile |
| WARNING | Fișier + DB + Dashboard + Notificare | 90 zile |
| ERROR | Toate + Alertă | 1 an |
| CRITICAL | Toate + Alertă Immediată | Permanent |

---

**Creat:** 2026-03-28  
**Versiune:** 1.0  
**Status:** Gata pentru implementare
