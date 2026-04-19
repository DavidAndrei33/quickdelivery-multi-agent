"""
ML API Routes
FastAPI routes for ML training and prediction
Author: Builder-Core
Date: 2026-04-06
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

import sys
sys.path.append('/workspace/shared/api')
from ml_api.services.model_service import (
    ModelTrainer, ModelPredictor, ModelManager, ModelConfig,
    PredictionResult, model_manager
)

router = APIRouter(prefix="/api/ml", tags=["Machine Learning"])
logger = logging.getLogger(__name__)


# ============== Pydantic Models ==============

class TrainRequest(BaseModel):
    """Request to start model training"""
    symbol: str = Field(..., example="EURUSD")
    algorithm: str = Field(default="xgboost", example="xgboost")
    version: str = Field(default="v1", example="v1")
    target_pips: int = Field(default=30, ge=10, le=200)
    max_bars: int = Field(default=10, ge=5, le=50)
    test_size: float = Field(default=0.2, ge=0.1, le=0.4)
    hyperparameters: Optional[Dict[str, Any]] = Field(default=None)


class TrainResponse(BaseModel):
    """Response from training request"""
    job_id: str
    status: str
    symbol: str
    algorithm: str
    message: str


class JobStatusResponse(BaseModel):
    """Training job status"""
    job_id: str
    status: str  # pending, running, completed, failed, cancelled
    symbol: str
    algorithm: str
    progress_percent: int = 0
    current_step: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    error_message: Optional[str] = None
    model_id: Optional[int] = None


class PredictRequest(BaseModel):
    """Request for prediction"""
    symbol: str = Field(..., example="EURUSD")
    features: Dict[str, float] = Field(..., example={
        "rsi_14": 65.4,
        "sma_20": 1.0850,
        "atr_14": 0.0012
    })
    model_version: Optional[str] = Field(default=None, example="v1")


class PredictResponse(BaseModel):
    """Prediction response"""
    symbol: str
    timestamp: datetime
    signal: str  # BUY, SELL, HOLD
    confidence: float
    probability_buy: float
    probability_sell: float
    probability_hold: float
    model_version: str
    model_algorithm: str
    feature_importance: Optional[Dict[str, float]] = None


class ModelInfo(BaseModel):
    """Model metadata"""
    symbol: str
    algorithm: str
    version: str
    training_date: datetime
    accuracy: Optional[float] = None
    precision: Optional[float] = None
    recall: Optional[float] = None
    f1_score: Optional[float] = None
    auc_roc: Optional[float] = None
    win_rate: Optional[float] = None
    profit_factor: Optional[float] = None
    training_samples: int = 0
    is_active: bool = False


class ModelsListResponse(BaseModel):
    """List of models"""
    models: List[ModelInfo]
    total: int


class SymbolFeatures(BaseModel):
    """Feature data for a symbol"""
    symbol: str
    timeframe: str
    features: List[str]
    data_points: int
    last_updated: datetime


# ============== Routes ==============

@router.post("/train/{symbol}", response_model=TrainResponse)
async def start_training(
    symbol: str,
    request: TrainRequest,
    background_tasks: BackgroundTasks
):
    """
    Start a new model training job for a symbol
    
    - **symbol**: Trading pair (EURUSD, GBPUSD, XAUUSD, etc.)
    - **algorithm**: xgboost, lightgbm, or lstm
    - **version**: Model version tag
    - **target_pips**: Target profit in pips
    - **max_bars**: Maximum bars to wait for target
    """
    try:
        # Create config
        config = ModelConfig(
            symbol=symbol,
            algorithm=request.algorithm,
            version=request.version,
            target_pips=request.target_pips,
            max_bars=request.max_bars,
            test_size=request.test_size
        )
        
        # Override hyperparameters if provided
        if request.hyperparameters:
            if request.algorithm == 'xgboost':
                config.xgb_params.update(request.hyperparameters)
            elif request.algorithm == 'lightgbm':
                config.lgb_params.update(request.hyperparameters)
            elif request.algorithm == 'lstm':
                config.lstm_params.update(request.hyperparameters)
        
        # Start training job
        job_id = model_manager.start_training(config)
        
        # TODO: Actually run training in background
        # background_tasks.add_task(run_training, job_id, config)
        
        return TrainResponse(
            job_id=job_id,
            status="started",
            symbol=symbol,
            algorithm=request.algorithm,
            message=f"Training job started for {symbol} using {request.algorithm}"
        )
        
    except Exception as e:
        logger.error(f"Error starting training: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str):
    """Get status of a training job"""
    status = model_manager.get_job_status(job_id)
    
    if status['status'] == 'not_found':
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    
    return JobStatusResponse(
        job_id=job_id,
        status=status.get('status', 'unknown'),
        symbol="EURUSD",  # TODO: Get from job
        algorithm="xgboost",
        progress_percent=status.get('progress', 0),
        current_step=status.get('current_step'),
        start_time=status.get('start_time'),
        end_time=status.get('end_time')
    )


@router.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    """
    Get prediction for current market conditions
    
    - **symbol**: Trading pair
    - **features**: Dictionary of feature values
    - **model_version**: Specific model version (optional, uses latest if not specified)
    """
    try:
        # Load model
        predictor = ModelPredictor(
            symbol=request.symbol,
            version=request.model_version
        )
        
        # Make prediction
        result = predictor.predict(request.features)
        
        return PredictResponse(
            symbol=result.symbol,
            timestamp=result.timestamp,
            signal=result.signal,
            confidence=result.confidence,
            probability_buy=result.probability_buy,
            probability_sell=result.probability_sell,
            probability_hold=result.probability_hold,
            model_version=predictor.version,
            model_algorithm=predictor.algorithm,
            feature_importance=result.feature_importance
        )
        
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=404, 
            detail=f"No trained model found for {request.symbol}. Train a model first."
        )
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/predict/batch")
async def predict_batch(requests: List[PredictRequest]):
    """
    Get predictions for multiple symbols in one request
    """
    results = []
    
    for req in requests:
        try:
            predictor = ModelPredictor(symbol=req.symbol, version=req.model_version)
            result = predictor.predict(req.features)
            results.append({
                "symbol": req.symbol,
                "success": True,
                "prediction": {
                    "signal": result.signal,
                    "confidence": result.confidence,
                    "probability_buy": result.probability_buy,
                    "probability_sell": result.probability_sell
                }
            })
        except Exception as e:
            results.append({
                "symbol": req.symbol,
                "success": False,
                "error": str(e)
            })
    
    return {"results": results}


@router.get("/models", response_model=ModelsListResponse)
async def list_models(symbol: Optional[str] = None):
    """List all trained models"""
    try:
        models_data = model_manager.list_models(symbol)
        
        models = []
        for m in models_data:
            models.append(ModelInfo(
                symbol=m['symbol'],
                algorithm=m['algorithm'],
                version=m['version'],
                training_date=datetime.fromisoformat(m['training_date']),
                accuracy=m.get('metrics', {}).get('accuracy'),
                precision=m.get('metrics', {}).get('precision'),
                recall=m.get('metrics', {}).get('recall'),
                f1_score=m.get('metrics', {}).get('f1_score'),
                auc_roc=m.get('metrics', {}).get('auc_roc'),
                training_samples=m.get('training_samples', 0),
                is_active=True  # TODO: Get from DB
            ))
        
        return ModelsListResponse(
            models=models,
            total=len(models)
        )
        
    except Exception as e:
        logger.error(f"Error listing models: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models/{symbol}", response_model=ModelsListResponse)
async def list_models_for_symbol(symbol: str):
    """List all models for a specific symbol"""
    return await list_models(symbol)


@router.post("/models/{symbol}/activate/{version}")
async def activate_model(symbol: str, version: str):
    """Activate a specific model version for a symbol"""
    try:
        model_manager.activate_model(symbol, version)
        return {
            "success": True,
            "symbol": symbol,
            "version": version,
            "message": f"Model {version} activated for {symbol}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models/{symbol}/features")
async def get_model_features(symbol: str, version: Optional[str] = None):
    """Get list of features used by a model"""
    try:
        predictor = ModelPredictor(symbol=symbol, version=version)
        return {
            "symbol": symbol,
            "version": predictor.version,
            "algorithm": predictor.algorithm,
            "features": predictor.feature_columns,
            "feature_count": len(predictor.feature_columns)
        }
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"No model found for {symbol}"
        )


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "ml-api",
        "timestamp": datetime.now()
    }


@router.get("/symbols")
async def get_supported_symbols():
    """Get list of symbols with trained models"""
    models = model_manager.list_models()
    symbols = list(set(m['symbol'] for m in models))
    
    return {
        "symbols": symbols,
        "count": len(symbols),
        "total_models": len(models)
    }


@router.delete("/models/{symbol}/{version}")
async def delete_model(symbol: str, version: str):
    """Delete a specific model version"""
    import os
    
    try:
        model_dir = f"/workspace/shared/models/{symbol}"
        
        # Files to delete
        files_to_remove = [
            f"model_{version}.json",
            f"model_{version}.h5",
            f"scaler_{version}.pkl",
            f"metadata_{version}.json"
        ]
        
        deleted = []
        for f in files_to_remove:
            path = os.path.join(model_dir, f)
            if os.path.exists(path):
                os.remove(path)
                deleted.append(f)
        
        return {
            "success": True,
            "symbol": symbol,
            "version": version,
            "deleted_files": deleted
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
