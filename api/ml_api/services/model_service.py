"""
ML Model Service
Handles model training, prediction, and management for Forex ML system.
Author: Builder-Core
Date: 2026-04-06
"""

import os
import json
import uuid
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from pathlib import Path
import pickle

import numpy as np
import pandas as pd

# ML Libraries
try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False

try:
    import lightgbm as lgb
    LIGHTGBM_AVAILABLE = True
except ImportError:
    LIGHTGBM_AVAILABLE = False

try:
    import tensorflow as tf
    from tensorflow import keras
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ModelConfig:
    """Configuration for model training"""
    symbol: str
    algorithm: str  # xgboost, lightgbm, lstm
    version: str = "v1"
    target_pips: int = 30
    max_bars: int = 10
    test_size: float = 0.2
    
    # XGBoost params
    xgb_params: Dict = None
    # LightGBM params
    lgb_params: Dict = None
    # LSTM params
    lstm_params: Dict = None
    
    def __post_init__(self):
        if self.xgb_params is None:
            self.xgb_params = {
                'objective': 'binary:logistic',
                'eval_metric': 'auc',
                'max_depth': 5,
                'min_child_weight': 20,
                'gamma': 0.2,
                'subsample': 0.7,
                'colsample_bytree': 0.7,
                'reg_alpha': 0.5,
                'reg_lambda': 2.0,
                'learning_rate': 0.01,
                'n_estimators': 500,
                'random_state': 42,
                'n_jobs': -1
            }
        
        if self.lgb_params is None:
            self.lgb_params = {
                'objective': 'binary',
                'metric': 'auc',
                'boosting_type': 'gbdt',
                'num_leaves': 31,
                'max_depth': 6,
                'learning_rate': 0.05,
                'n_estimators': 500,
                'subsample': 0.8,
                'colsample_bytree': 0.8,
                'reg_alpha': 0.1,
                'reg_lambda': 1.0,
                'random_state': 42,
                'n_jobs': -1,
                'verbose': -1
            }
        
        if self.lstm_params is None:
            self.lstm_params = {
                'sequence_length': 60,
                'lstm_units': [128, 64],
                'dropout': 0.2,
                'learning_rate': 0.001,
                'epochs': 50,
                'batch_size': 32
            }


@dataclass
class PredictionResult:
    """Result from model prediction"""
    symbol: str
    timestamp: datetime
    signal: str  # BUY, SELL, HOLD
    confidence: float
    probability_buy: float
    probability_sell: float
    probability_hold: float = 0.0
    feature_importance: Dict = None
    

def get_model_path(symbol: str, algorithm: str, version: str) -> str:
    """Get the path where model should be saved"""
    base_path = f"/workspace/shared/models/{symbol}"
    os.makedirs(base_path, exist_ok=True)
    
    if algorithm == 'lstm':
        return f"{base_path}/model_{version}.h5"
    else:
        return f"{base_path}/model_{version}.json"


def get_scaler_path(symbol: str, algorithm: str, version: str) -> str:
    """Get path for feature scaler"""
    base_path = f"/workspace/shared/models/{symbol}"
    return f"{base_path}/scaler_{version}.pkl"


class ModelTrainer:
    """Handles model training for different algorithms"""
    
    def __init__(self, job_id: str, config: ModelConfig):
        self.job_id = job_id
        self.config = config
        self.model = None
        self.scaler = None
        self.metrics = {}
        self.feature_columns = []
        
    def train(self, df: pd.DataFrame) -> Dict:
        """
        Train model based on algorithm type
        
        Args:
            df: DataFrame with features and target column
            
        Returns:
            Dictionary with training results
        """
        logger.info(f"Starting training for {self.config.symbol} with {self.config.algorithm}")
        
        # Prepare features
        X, y = self._prepare_data(df)
        
        # Split data (time-series aware)
        split_idx = int(len(X) * (1 - self.config.test_size))
        X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
        y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
        
        logger.info(f"Training samples: {len(X_train)}, Test samples: {len(X_test)}")
        
        # Train based on algorithm
        if self.config.algorithm == 'xgboost':
            if not XGBOOST_AVAILABLE:
                raise ImportError("XGBoost not installed")
            self._train_xgboost(X_train, y_train, X_test, y_test)
            
        elif self.config.algorithm == 'lightgbm':
            if not LIGHTGBM_AVAILABLE:
                raise ImportError("LightGBM not installed")
            self._train_lightgbm(X_train, y_train, X_test, y_test)
            
        elif self.config.algorithm == 'lstm':
            if not TENSORFLOW_AVAILABLE:
                raise ImportError("TensorFlow not installed")
            self._train_lstm(X_train, y_train, X_test, y_test)
            
        else:
            raise ValueError(f"Unknown algorithm: {self.config.algorithm}")
        
        # Save model
        model_path = self._save_model()
        
        return {
            'job_id': self.job_id,
            'model_path': model_path,
            'metrics': self.metrics,
            'feature_columns': self.feature_columns,
            'training_samples': len(X_train),
            'validation_samples': len(X_test)
        }
    
    def _prepare_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """Prepare features and target"""
        # Get feature columns (exclude non-feature columns)
        exclude_cols = ['timestamp', 'datetime', 'date', 'time', 'target', 'symbol']
        self.feature_columns = [col for col in df.columns if col not in exclude_cols]
        
        X = df[self.feature_columns].copy()
        y = df['target'].copy() if 'target' in df.columns else pd.Series([0] * len(df))
        
        # Handle missing values
        X = X.fillna(method='ffill').fillna(0)
        
        return X, y
    
    def _train_xgboost(self, X_train: pd.DataFrame, y_train: pd.Series, 
                       X_test: pd.DataFrame, y_test: pd.Series):
        """Train XGBoost model"""
        logger.info("Training XGBoost model...")
        
        from sklearn.preprocessing import StandardScaler
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
        
        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model = xgb.XGBClassifier(**self.config.xgb_params)
        
        self.model.fit(
            X_train_scaled, y_train,
            eval_set=[(X_test_scaled, y_test)],
            verbose=False
        )
        
        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        y_pred_proba = self.model.predict_proba(X_test_scaled)
        
        self.metrics = {
            'accuracy': float(accuracy_score(y_test, y_pred)),
            'precision': float(precision_score(y_test, y_pred, zero_division=0)),
            'recall': float(recall_score(y_test, y_pred, zero_division=0)),
            'f1_score': float(f1_score(y_test, y_pred, zero_division=0)),
            'auc_roc': float(roc_auc_score(y_test, y_pred_proba[:, 1])) if len(np.unique(y_test)) > 1 else 0.5
        }
        
        logger.info(f"XGBoost metrics: {self.metrics}")
    
    def _train_lightgbm(self, X_train: pd.DataFrame, y_train: pd.Series,
                        X_test: pd.DataFrame, y_test: pd.Series):
        """Train LightGBM model"""
        logger.info("Training LightGBM model...")
        
        from sklearn.preprocessing import StandardScaler
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
        
        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model = lgb.LGBMClassifier(**self.config.lgb_params)
        
        self.model.fit(
            X_train_scaled, y_train,
            eval_set=[(X_test_scaled, y_test)],
            callbacks=[lgb.early_stopping(50), lgb.log_evaluation(0)]
        )
        
        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        y_pred_proba = self.model.predict_proba(X_test_scaled)
        
        self.metrics = {
            'accuracy': float(accuracy_score(y_test, y_pred)),
            'precision': float(precision_score(y_test, y_pred, zero_division=0)),
            'recall': float(recall_score(y_test, y_pred, zero_division=0)),
            'f1_score': float(f1_score(y_test, y_pred, zero_division=0)),
            'auc_roc': float(roc_auc_score(y_test, y_pred_proba[:, 1])) if len(np.unique(y_test)) > 1 else 0.5
        }
        
        logger.info(f"LightGBM metrics: {self.metrics}")
    
    def _train_lstm(self, X_train: pd.DataFrame, y_train: pd.Series,
                    X_test: pd.DataFrame, y_test: pd.Series):
        """Train LSTM model"""
        logger.info("Training LSTM model...")
        
        from sklearn.preprocessing import StandardScaler, LabelEncoder
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        
        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Create sequences
        seq_length = self.config.lstm_params['sequence_length']
        
        def create_sequences(X, y, seq_len):
            X_seq, y_seq = [], []
            for i in range(len(X) - seq_len):
                X_seq.append(X[i:i+seq_len])
                y_seq.append(y.iloc[i+seq_len])
            return np.array(X_seq), np.array(y_seq)
        
        X_train_seq, y_train_seq = create_sequences(X_train_scaled, y_train, seq_length)
        X_test_seq, y_test_seq = create_sequences(X_test_scaled, y_test, seq_length)
        
        # Build LSTM model
        input_shape = (seq_length, X_train.shape[1])
        
        self.model = keras.Sequential()
        
        # First LSTM layer
        self.model.add(keras.layers.LSTM(
            self.config.lstm_params['lstm_units'][0],
            return_sequences=len(self.config.lstm_params['lstm_units']) > 1,
            input_shape=input_shape
        ))
        self.model.add(keras.layers.Dropout(self.config.lstm_params['dropout']))
        
        # Additional LSTM layers
        for i, units in enumerate(self.config.lstm_params['lstm_units'][1:], 1):
            return_seq = i < len(self.config.lstm_params['lstm_units']) - 1
            self.model.add(keras.layers.LSTM(units, return_sequences=return_seq))
            self.model.add(keras.layers.Dropout(self.config.lstm_params['dropout']))
        
        # Output layer
        self.model.add(keras.layers.Dense(3, activation='softmax'))  # Buy, Sell, Hold
        
        # Compile
        self.model.compile(
            optimizer=keras.optimizers.Adam(self.config.lstm_params['learning_rate']),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        # Train
        history = self.model.fit(
            X_train_seq, y_train_seq,
            epochs=self.config.lstm_params['epochs'],
            batch_size=self.config.lstm_params['batch_size'],
            validation_split=0.1,
            verbose=0
        )
        
        # Evaluate
        y_pred_proba = self.model.predict(X_test_seq, verbose=0)
        y_pred = np.argmax(y_pred_proba, axis=1)
        
        self.metrics = {
            'accuracy': float(accuracy_score(y_test_seq, y_pred)),
            'precision': float(precision_score(y_test_seq, y_pred, average='weighted', zero_division=0)),
            'recall': float(recall_score(y_test_seq, y_pred, average='weighted', zero_division=0)),
            'f1_score': float(f1_score(y_test_seq, y_pred, average='weighted', zero_division=0)),
            'auc_roc': 0.0  # Not calculated for multi-class
        }
        
        logger.info(f"LSTM metrics: {self.metrics}")
    
    def _save_model(self) -> str:
        """Save trained model to disk"""
        model_path = get_model_path(self.config.symbol, self.config.algorithm, self.config.version)
        
        if self.config.algorithm == 'lstm':
            self.model.save(model_path)
        else:
            self.model.save_model(model_path)
        
        # Save scaler
        scaler_path = get_scaler_path(self.config.symbol, self.config.algorithm, self.config.version)
        with open(scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)
        
        # Save metadata
        metadata = {
            'symbol': self.config.symbol,
            'algorithm': self.config.algorithm,
            'version': self.config.version,
            'feature_columns': self.feature_columns,
            'metrics': self.metrics,
            'hyperparameters': getattr(self.config, f'{self.config.algorithm}_params'),
            'training_date': datetime.now().isoformat(),
            'model_path': model_path,
            'scaler_path': scaler_path
        }
        
        metadata_path = f"/workspace/shared/models/{self.config.symbol}/metadata_{self.config.version}.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"Model saved to {model_path}")
        return model_path


class ModelPredictor:
    """Handles model loading and predictions"""
    
    def __init__(self, symbol: str, algorithm: str = None, version: str = None):
        self.symbol = symbol
        self.algorithm = algorithm
        self.version = version
        self.model = None
        self.scaler = None
        self.feature_columns = []
        self.metadata = {}
        
        # Auto-load latest if version not specified
        if version:
            self._load_model(version)
        else:
            self._load_latest_model()
    
    def _load_latest_model(self):
        """Load the latest active model for symbol"""
        model_dir = f"/workspace/shared/models/{self.symbol}"
        
        if not os.path.exists(model_dir):
            raise FileNotFoundError(f"No models found for {self.symbol}")
        
        # Find latest metadata file
        metadata_files = [f for f in os.listdir(model_dir) if f.startswith('metadata_')]
        if not metadata_files:
            raise FileNotFoundError(f"No model metadata found for {self.symbol}")
        
        # Sort by version (simple string sort)
        metadata_files.sort(reverse=True)
        latest_version = metadata_files[0].replace('metadata_', '').replace('.json', '')
        
        self._load_model(latest_version)
    
    def _load_model(self, version: str):
        """Load specific model version"""
        # Load metadata
        metadata_path = f"/workspace/shared/models/{self.symbol}/metadata_{version}.json"
        
        if not os.path.exists(metadata_path):
            raise FileNotFoundError(f"Model metadata not found: {metadata_path}")
        
        with open(metadata_path, 'r') as f:
            self.metadata = json.load(f)
        
        self.algorithm = self.metadata['algorithm']
        self.version = version
        self.feature_columns = self.metadata['feature_columns']
        
        # Load model
        model_path = self.metadata['model_path']
        
        if self.algorithm == 'lstm':
            self.model = keras.models.load_model(model_path)
        elif self.algorithm == 'xgboost':
            self.model = xgb.XGBClassifier()
            self.model.load_model(model_path)
        elif self.algorithm == 'lightgbm':
            self.model = lgb.Booster(model_file=model_path)
        
        # Load scaler
        scaler_path = self.metadata['scaler_path']
        with open(scaler_path, 'rb') as f:
            self.scaler = pickle.load(f)
        
        logger.info(f"Loaded {self.algorithm} model v{version} for {self.symbol}")
    
    def predict(self, features: Dict[str, float]) -> PredictionResult:
        """
        Make prediction for single bar
        
        Args:
            features: Dictionary of feature values
            
        Returns:
            PredictionResult with signal and probabilities
        """
        # Prepare input
        input_data = np.array([[features.get(col, 0) for col in self.feature_columns]])
        input_scaled = self.scaler.transform(input_data)
        
        # Make prediction
        if self.algorithm == 'lstm':
            # For LSTM, we need a sequence - use single value repeated
            seq_length = self.metadata.get('hyperparameters', {}).get('sequence_length', 60)
            input_seq = np.repeat(input_scaled, seq_length, axis=0).reshape(1, seq_length, -1)
            proba = self.model.predict(input_seq, verbose=0)[0]
            
            prob_buy = float(proba[0])
            prob_sell = float(proba[1])
            prob_hold = float(proba[2])
            
        else:
            proba = self.model.predict_proba(input_scaled)[0]
            
            if len(proba) == 2:
                # Binary classification
                prob_buy = float(proba[1])
                prob_sell = float(proba[0])
                prob_hold = 0.0
            else:
                # Multi-class
                prob_buy = float(proba[0])
                prob_sell = float(proba[1])
                prob_hold = float(proba[2])
        
        # Determine signal
        if prob_buy > 0.7 and prob_buy > prob_sell:
            signal = 'BUY'
            confidence = prob_buy
        elif prob_sell > 0.7 and prob_sell > prob_buy:
            signal = 'SELL'
            confidence = prob_sell
        else:
            signal = 'HOLD'
            confidence = max(prob_buy, prob_sell, prob_hold)
        
        # Get feature importance (if available)
        feature_importance = {}
        if hasattr(self.model, 'feature_importances_'):
            importances = self.model.feature_importances_
            feature_importance = dict(zip(self.feature_columns, importances.tolist()))
        
        return PredictionResult(
            symbol=self.symbol,
            timestamp=datetime.now(),
            signal=signal,
            confidence=confidence,
            probability_buy=prob_buy,
            probability_sell=prob_sell,
            probability_hold=prob_hold,
            feature_importance=feature_importance
        )
    
    def predict_batch(self, df: pd.DataFrame) -> List[PredictionResult]:
        """Make predictions for multiple bars"""
        results = []
        for _, row in df.iterrows():
            features = row.to_dict()
            results.append(self.predict(features))
        return results


class ModelManager:
    """Manages model lifecycle - training jobs, versioning, etc."""
    
    def __init__(self):
        self.active_jobs: Dict[str, ModelTrainer] = {}
    
    def start_training(self, config: ModelConfig) -> str:
        """Start a new training job"""
        job_id = str(uuid.uuid4())[:8]
        
        trainer = ModelTrainer(job_id, config)
        self.active_jobs[job_id] = trainer
        
        logger.info(f"Started training job {job_id} for {config.symbol}")
        return job_id
    
    def get_job_status(self, job_id: str) -> Dict:
        """Get status of training job"""
        if job_id not in self.active_jobs:
            return {'status': 'not_found', 'job_id': job_id}
        
        # TODO: Implement actual job tracking
        return {
            'status': 'running',
            'job_id': job_id,
            'progress': 50
        }
    
    def list_models(self, symbol: str = None) -> List[Dict]:
        """List all trained models"""
        models = []
        
        model_base = "/workspace/shared/models"
        symbols = [symbol] if symbol else os.listdir(model_base)
        
        for sym in symbols:
            sym_path = os.path.join(model_base, sym)
            if not os.path.isdir(sym_path):
                continue
            
            metadata_files = [f for f in os.listdir(sym_path) if f.startswith('metadata_')]
            
            for meta_file in metadata_files:
                with open(os.path.join(sym_path, meta_file), 'r') as f:
                    metadata = json.load(f)
                    models.append(metadata)
        
        return models
    
    def get_active_model(self, symbol: str) -> Optional[ModelPredictor]:
        """Get the active predictor for a symbol"""
        try:
            return ModelPredictor(symbol)
        except FileNotFoundError:
            return None
    
    def activate_model(self, symbol: str, version: str):
        """Set a model version as active"""
        # TODO: Update database to set is_active flag
        logger.info(f"Activated model {version} for {symbol}")


# Singleton instance
model_manager = ModelManager()
