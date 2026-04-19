#!/bin/bash
# Setup script for ML Infrastructure
# Run this to initialize the ML system

echo "==================================="
echo "  ML Infrastructure Setup"
echo "==================================="

# Create directories
echo "Creating directories..."
mkdir -p /workspace/shared/models/{EURUSD,GBPUSD,XAUUSD,USDJPY,USDCHF,AUDUSD,USDCAD,NZDUSD}
mkdir -p /workspace/shared/data/{forex,features,processed,backtest}
mkdir -p /workspace/shared/logs
mkdir -p /workspace/shared/mt5_connector

# Check Python dependencies
echo "Checking Python dependencies..."

pip install -q fastapi uvicorn xgboost lightgbm scikit-learn pandas numpy 2>/dev/null || echo "Some packages may need manual installation"

# Check if PostgreSQL is available (optional)
if command -v psql &> /dev/null; then
    echo "PostgreSQL found - can use for production database"
else
    echo "PostgreSQL not found - using SQLite for local development"
fi

# Initialize SQLite database
echo "Initializing SQLite database..."
python3 << 'EOF'
import sqlite3
import os

db_path = '/workspace/shared/data/ml_predictions.db'
os.makedirs(os.path.dirname(db_path), exist_ok=True)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS predictions_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        symbol TEXT NOT NULL,
        signal TEXT NOT NULL,
        confidence REAL,
        prob_buy REAL,
        prob_sell REAL,
        close_price REAL,
        executed BOOLEAN DEFAULT 0
    )
''')

conn.commit()
conn.close()
print("SQLite database initialized")
EOF

# Set permissions
chmod -R 755 /workspace/shared/models
chmod -R 755 /workspace/shared/data
chmod -R 755 /workspace/shared/logs

echo ""
echo "==================================="
echo "  Setup Complete!"
echo "==================================="
echo ""
echo "Next steps:"
echo "1. Install dependencies: pip install -r /workspace/shared/api/ml_api/requirements.txt"
echo "2. Start API: cd /workspace/shared/api/ml_api && python main.py"
echo "3. Start MT5 Connector: python /workspace/shared/mt5_connector/mt5_ml_connector.py"
echo ""
echo "API will be available at: http://localhost:8000"
echo "API docs at: http://localhost:8000/docs"
echo ""
