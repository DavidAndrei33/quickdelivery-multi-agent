-- Migration: ML Tables for Forex Trading ML System
-- Created: 2026-04-06
-- Author: Builder-Core

-- ============================================
-- Table: ml_models
-- Stores trained model metadata
-- ============================================
CREATE TABLE IF NOT EXISTS ml_models (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,                    -- EURUSD, GBPUSD, XAUUSD, etc.
    algorithm VARCHAR(20) NOT NULL,                 -- xgboost, lightgbm, lstm
    version VARCHAR(10) NOT NULL,                   -- v1, v2, v3, etc.
    model_path VARCHAR(255) NOT NULL,               -- /workspace/shared/models/EURUSD/model_v1.json
    feature_columns JSONB NOT NULL,                 -- List of features used
    hyperparameters JSONB NOT NULL,                 -- Model hyperparameters
    
    -- Performance Metrics
    accuracy DECIMAL(5,4),                          -- 0.0000 to 1.0000
    precision DECIMAL(5,4),
    recall DECIMAL(5,4),
    f1_score DECIMAL(5,4),
    auc_roc DECIMAL(5,4),
    
    -- Trading Metrics
    win_rate DECIMAL(5,4),                          -- Win percentage
    profit_factor DECIMAL(8,2),                     -- Gross profit / Gross loss
    sharpe_ratio DECIMAL(6,2),                      -- Risk-adjusted return
    max_drawdown DECIMAL(6,2),                      -- Maximum drawdown %
    
    -- Training Info
    training_samples INTEGER,
    validation_samples INTEGER,
    training_date TIMESTAMP NOT NULL DEFAULT NOW(),
    last_used TIMESTAMP,
    is_active BOOLEAN DEFAULT FALSE,                -- Only one active model per symbol
    
    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    CONSTRAINT unique_model_version UNIQUE (symbol, algorithm, version)
);

-- Index for fast lookups
CREATE INDEX idx_ml_models_symbol ON ml_models(symbol);
CREATE INDEX idx_ml_models_active ON ml_models(symbol, is_active) WHERE is_active = TRUE;
CREATE INDEX idx_ml_models_algorithm ON ml_models(algorithm);

-- ============================================
-- Table: ml_predictions
-- Stores real-time predictions from models
-- ============================================
CREATE TABLE IF NOT EXISTS ml_predictions (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    model_id INTEGER REFERENCES ml_models(id) ON DELETE CASCADE,
    
    -- Prediction Data
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    signal VARCHAR(10) NOT NULL,                    -- BUY, SELL, HOLD
    confidence DECIMAL(5,4) NOT NULL,               -- 0.0000 to 1.0000
    probability_buy DECIMAL(5,4),                   -- Probability for BUY class
    probability_sell DECIMAL(5,4),                  -- Probability for SELL class
    probability_hold DECIMAL(5,4),                  -- Probability for HOLD class
    
    -- Feature Values (stored as JSON for analysis)
    feature_values JSONB,                           -- { "rsi_14": 65.4, "sma_20": 1.0850, ... }
    feature_importance JSONB,                       -- Feature importance for this prediction
    
    -- Market Context
    open_price DECIMAL(12,6),
    high_price DECIMAL(12,6),
    low_price DECIMAL(12,6),
    close_price DECIMAL(12,6),
    volume INTEGER,
    
    -- Session Info
    session VARCHAR(20),                            -- london, ny, asia
    day_of_week INTEGER,                            -- 0=Sunday, 6=Saturday
    hour INTEGER,                                   -- 0-23
    
    -- MT5 Integration
    mt5_ticket BIGINT,                              -- MT5 order ticket if executed
    executed BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_predictions_symbol_time ON ml_predictions(symbol, timestamp DESC);
CREATE INDEX idx_predictions_model ON ml_predictions(model_id);
CREATE INDEX idx_predictions_signal ON ml_predictions(signal, timestamp DESC);
CREATE INDEX idx_predictions_confidence ON ml_predictions(confidence DESC) WHERE confidence > 0.7;

-- ============================================
-- Table: ml_performance
-- Daily performance tracking per model
-- ============================================
CREATE TABLE IF NOT EXISTS ml_performance (
    id SERIAL PRIMARY KEY,
    model_id INTEGER REFERENCES ml_models(id) ON DELETE CASCADE,
    symbol VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    
    -- Prediction Metrics
    total_predictions INTEGER DEFAULT 0,
    buy_signals INTEGER DEFAULT 0,
    sell_signals INTEGER DEFAULT 0,
    hold_signals INTEGER DEFAULT 0,
    
    -- Accuracy Metrics
    accuracy DECIMAL(5,4),
    precision DECIMAL(5,4),
    recall DECIMAL(5,4),
    f1_score DECIMAL(5,4),
    
    -- Trading Performance (if signals were executed)
    total_trades INTEGER DEFAULT 0,
    winning_trades INTEGER DEFAULT 0,
    losing_trades INTEGER DEFAULT 0,
    win_rate DECIMAL(5,4),
    
    -- Profit Metrics
    total_pips DECIMAL(10,2),                       -- Total pips gained/lost
    avg_profit_per_trade DECIMAL(10,2),
    profit_factor DECIMAL(8,2),
    
    -- Risk Metrics
    max_drawdown DECIMAL(6,2),
    sharpe_ratio DECIMAL(6,2),
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    CONSTRAINT unique_model_date UNIQUE (model_id, date)
);

CREATE INDEX idx_performance_model ON ml_performance(model_id);
CREATE INDEX idx_performance_symbol_date ON ml_performance(symbol, date DESC);

-- ============================================
-- Table: ml_training_jobs
-- Track training job status
-- ============================================
CREATE TABLE IF NOT EXISTS ml_training_jobs (
    id SERIAL PRIMARY KEY,
    job_id VARCHAR(50) UNIQUE NOT NULL,             -- UUID for job tracking
    symbol VARCHAR(10) NOT NULL,
    algorithm VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',  -- pending, running, completed, failed, cancelled
    
    -- Job Details
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    duration_seconds INTEGER,
    
    -- Configuration
    config JSONB,                                   -- Training configuration
    
    -- Progress
    progress_percent INTEGER DEFAULT 0,             -- 0-100
    current_step VARCHAR(100),                      -- Current training step
    
    -- Results
    model_id INTEGER REFERENCES ml_models(id) ON DELETE SET NULL,
    error_message TEXT,
    logs TEXT,                                      -- Training logs
    
    -- Resource Usage
    cpu_usage DECIMAL(5,2),                         -- Average CPU %
    memory_usage_mb INTEGER,                        -- Peak memory usage
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_jobs_status ON ml_training_jobs(status);
CREATE INDEX idx_jobs_symbol ON ml_training_jobs(symbol);
CREATE INDEX idx_jobs_created ON ml_training_jobs(created_at DESC);

-- ============================================
-- Table: ml_feature_importance
-- Track feature importance over time
-- ============================================
CREATE TABLE IF NOT EXISTS ml_feature_importance (
    id SERIAL PRIMARY KEY,
    model_id INTEGER REFERENCES ml_models(id) ON DELETE CASCADE,
    feature_name VARCHAR(50) NOT NULL,
    importance_score DECIMAL(8,6) NOT NULL,         -- Importance score
    rank INTEGER,                                   -- Rank by importance
    
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_feature_importance_model ON ml_feature_importance(model_id);

-- ============================================
-- Table: ml_market_data_cache
-- Cache for market data used in predictions
-- ============================================
CREATE TABLE IF NOT EXISTS ml_market_data_cache (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    timeframe VARCHAR(5) NOT NULL,                  -- M1, M5, M15, H1, H4, D1
    timestamp TIMESTAMP NOT NULL,
    
    -- OHLCV
    open DECIMAL(12,6) NOT NULL,
    high DECIMAL(12,6) NOT NULL,
    low DECIMAL(12,6) NOT NULL,
    close DECIMAL(12,6) NOT NULL,
    volume INTEGER,
    
    -- Technical Indicators (cached)
    indicators JSONB,
    
    -- Features (pre-computed)
    features JSONB,
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    CONSTRAINT unique_symbol_time UNIQUE (symbol, timeframe, timestamp)
);

CREATE INDEX idx_market_cache_symbol_time ON ml_market_data_cache(symbol, timeframe, timestamp DESC);

-- ============================================
-- Triggers for updated_at
-- ============================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_ml_models_updated_at BEFORE UPDATE ON ml_models
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_ml_performance_updated_at BEFORE UPDATE ON ml_performance
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_ml_training_jobs_updated_at BEFORE UPDATE ON ml_training_jobs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- Views for common queries
-- ============================================

-- Active models view
CREATE OR REPLACE VIEW active_models AS
SELECT * FROM ml_models WHERE is_active = TRUE;

-- Recent predictions view
CREATE OR REPLACE VIEW recent_predictions AS
SELECT 
    p.*,
    m.algorithm,
    m.version
FROM ml_predictions p
JOIN ml_models m ON p.model_id = m.id
WHERE p.timestamp > NOW() - INTERVAL '24 hours';

-- Daily performance summary view
CREATE OR REPLACE VIEW daily_performance_summary AS
SELECT 
    symbol,
    date,
    SUM(total_trades) as total_trades,
    SUM(winning_trades) as winning_trades,
    SUM(losing_trades) as losing_trades,
    AVG(win_rate) as avg_win_rate,
    SUM(total_pips) as total_pips,
    AVG(profit_factor) as avg_profit_factor
FROM ml_performance
GROUP BY symbol, date
ORDER BY date DESC;

-- ============================================
-- Comments
-- ============================================
COMMENT ON TABLE ml_models IS 'Stores metadata for trained ML models';
COMMENT ON TABLE ml_predictions IS 'Stores real-time predictions from ML models';
COMMENT ON TABLE ml_performance IS 'Daily performance metrics for ML models';
COMMENT ON TABLE ml_training_jobs IS 'Tracks status of model training jobs';
COMMENT ON TABLE ml_feature_importance IS 'Feature importance scores per model';
COMMENT ON TABLE ml_market_data_cache IS 'Cached market data with pre-computed features';
