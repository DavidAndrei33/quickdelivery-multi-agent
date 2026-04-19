# 🤖 ML Infrastructure for Forex Trading

**Status:** ✅ IMPLEMENTED  
**Author:** Builder-Core  
**Date:** 2026-04-06

---

## 📁 Structure

```
/workspace/shared/
├── api/ml_api/                 # FastAPI ML Service
│   ├── main.py                # API entry point
│   ├── requirements.txt       # Python dependencies
│   ├── routes/
│   │   └── ml_routes.py       # API endpoints
│   └── services/
│       └── model_service.py   # Model training & prediction
│
├── database/migrations/
│   └── ml_tables.sql          # PostgreSQL schema
│
├── mt5_connector/
│   └── mt5_ml_connector.py    # MT5 integration
│
├── models/                     # Model storage
│   ├── EURUSD/
│   ├── GBPUSD/
│   ├── XAUUSD/
│   └── ... (36 symbols)
│
├── data/                       # Data storage
│   ├── forex/                 # Raw market data
│   ├── features/              # Processed features
│   ├── processed/             # Training datasets
│   └── ml_predictions.db      # SQLite predictions log
│
├── logs/                       # Log files
│   └── mt5_connector.log
│
└── setup_ml_infrastructure.sh  # Setup script
```

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r /workspace/shared/api/ml_api/requirements.txt
```

### 2. Setup Infrastructure
```bash
chmod +x /workspace/shared/setup_ml_infrastructure.sh
/workspace/shared/setup_ml_infrastructure.sh
```

### 3. Start ML API Server
```bash
cd /workspace/shared/api/ml_api
python main.py
```

API will be available at: `http://localhost:8000`  
API Docs: `http://localhost:8000/docs`

### 4. Start MT5 Connector (in another terminal)
```bash
python /workspace/shared/mt5_connector/mt5_ml_connector.py
```

MT5 Connector will listen on: `http://localhost:9000`

---

## 📡 API Endpoints

### Training
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/ml/train/{symbol}` | Start training job |
| GET | `/api/ml/status/{job_id}` | Check training status |

### Prediction
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/ml/predict` | Get prediction for features |
| POST | `/api/ml/predict/batch` | Batch predictions |

### Model Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/ml/models` | List all models |
| GET | `/api/ml/models/{symbol}` | List models for symbol |
| POST | `/api/ml/models/{symbol}/activate/{version}` | Activate model |
| DELETE | `/api/ml/models/{symbol}/{version}` | Delete model |

### Info
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/ml/health` | Health check |
| GET | `/api/ml/symbols` | List supported symbols |

---

## 💾 Database Schema

### ml_models
Stores trained model metadata:
- `id`, `symbol`, `algorithm`, `version`
- `accuracy`, `precision`, `recall`, `f1_score`, `auc_roc`
- `win_rate`, `profit_factor`, `sharpe_ratio`, `max_drawdown`
- `training_date`, `is_active`

### ml_predictions
Stores real-time predictions:
- `symbol`, `timestamp`, `signal` (BUY/SELL/HOLD)
- `confidence`, `probabilities`
- `feature_values`, `feature_importance`
- `executed`, `mt5_ticket`

### ml_performance
Daily performance metrics per model:
- `total_predictions`, `win_rate`, `profit_factor`
- `total_pips`, `sharpe_ratio`, `max_drawdown`

### ml_training_jobs
Tracks training job status:
- `job_id`, `status`, `progress_percent`
- `start_time`, `end_time`, `duration_seconds`

---

## 🔌 MT5 Integration

### MT5 → ML Connector Flow

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────┐
│   MT5 EA    │────▶│ MT5 Connector   │────▶│   ML API     │
│  (Python)   │     │  (Port 9000)    │     │  (Port 8000) │
└─────────────┘     └─────────────────┘     └──────────────┘
                           │                        │
                           ▼                        ▼
                   ┌──────────────┐        ┌──────────────┐
                   │ SQLite Logs  │        │   Model      │
                   │ Predictions  │        │ Predictor    │
                   └──────────────┘        └──────────────┘
```

### Example MT5 Python Script
```python
import requests
import json

# Market data from MT5
market_data = {
    "symbol": "EURUSD",
    "timeframe": "H1",
    "timestamp": "2026-04-06T10:00:00",
    "open": 1.0850,
    "high": 1.0860,
    "low": 1.0845,
    "close": 1.0855,
    "volume": 1250,
    "indicators": {
        "rsi_14": 65.4,
        "sma_20": 1.0845,
        "atr_14": 0.0012
    }
}

# Send to connector
response = requests.post(
    "http://localhost:9000/predict",
    json=market_data
)

result = response.json()
print(f"Signal: {result['signal']}")
print(f"Confidence: {result['confidence']}")
```

---

## 🤖 Supported Algorithms

| Algorithm | Best For | Ensemble Size |
|-----------|----------|---------------|
| **XGBoost** | Exotic pairs (USDZAR, USDMXN) | 3 models |
| **LightGBM** | Major pairs (EURUSD, GBPUSD) | 5 models |
| **LSTM** | Complex (XAUUSD, US30, US500) | 3 models |

---

## 🧪 Testing

### Test Training
```bash
curl -X POST "http://localhost:8000/api/ml/train/EURUSD" \
  -H "Content-Type: application/json" \
  -d '{
    "algorithm": "xgboost",
    "target_pips": 30,
    "max_bars": 10
  }'
```

### Test Prediction
```bash
curl -X POST "http://localhost:8000/api/ml/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "EURUSD",
    "features": {
      "rsi_14": 65.4,
      "sma_20": 1.0850,
      "atr_14": 0.0012
    }
  }'
```

### List Models
```bash
curl "http://localhost:8000/api/ml/models"
```

---

## 📊 Model Storage Format

### XGBoost / LightGBM
```
/workspace/shared/models/EURUSD/
├── model_v1.json          # Trained model
├── scaler_v1.pkl          # Feature scaler
└── metadata_v1.json       # Model metadata
```

### LSTM
```
/workspace/shared/models/XAUUSD/
├── model_v1.h5            # Keras model
├── scaler_v1.pkl          # Feature scaler
└── metadata_v1.json       # Model metadata
```

---

## ⚙️ Environment Variables

```bash
# API Configuration
ML_API_HOST=0.0.0.0
ML_API_PORT=8000
ML_API_URL=http://localhost:8000/api/ml

# Database
DATABASE_URL=postgresql://user:pass@localhost/forex_ml
# Or use SQLite (default): /workspace/shared/data/ml_predictions.db

# MT5 Connector
MT5_CONNECTOR_HOST=0.0.0.0
MT5_CONNECTOR_PORT=9000
```

---

## 🔄 Training Pipeline

```python
# 1. Prepare features
features_df = prepare_features(symbol)

# 2. Start training job
trainer = ModelTrainer(job_id, config)
results = trainer.train(features_df)

# 3. Model saved automatically
# /workspace/shared/models/{symbol}/model_{version}.json

# 4. Activate model
model_manager.activate_model(symbol, version)

# 5. Ready for predictions!
predictor = ModelPredictor(symbol)
result = predictor.predict(features)
```

---

## 📝 TODO / Next Steps

- [ ] Integrate with database (PostgreSQL)
- [ ] Add authentication to API
- [ ] Implement model versioning with MLflow
- [ ] Add distributed training support
- [ ] Create monitoring dashboard
- [ ] Add A/B testing for models
- [ ] Implement online learning

---

## 🔗 References

- Research: `/workspace/shared/research/XGBOOST_FOREX_RESEARCH.md`
- Research: `/workspace/shared/research/ENSEMBLE_ML_FOREX_36_SYMBOLS.md`
- Database: `/workspace/shared/database/migrations/ml_tables.sql`

---

**Ready for integration with Feature Engineering pipeline from Strategy-Architect!** 🚀
