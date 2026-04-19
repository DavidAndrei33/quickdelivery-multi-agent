"""
ML API Main Application
FastAPI application for ML training and prediction services
Author: Builder-Core
Date: 2026-04-06
"""

import os
import sys
import logging
from contextlib import asynccontextmanager

# Add paths
sys.path.append('/workspace/shared/api')
sys.path.append('/workspace/shared/api/ml_api')

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import routes
from ml_api.routes.ml_routes import router as ml_router

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("ML API starting up...")
    
    # Ensure directories exist
    os.makedirs('/workspace/shared/models', exist_ok=True)
    os.makedirs('/workspace/shared/data', exist_ok=True)
    os.makedirs('/workspace/shared/logs', exist_ok=True)
    
    yield
    
    # Shutdown
    logger.info("ML API shutting down...")


# Create FastAPI app
app = FastAPI(
    title="Forex ML API",
    description="Machine Learning API for Forex Trading System",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ml_router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Forex ML API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "timestamp": "2026-04-06T09:00:00Z"
    }


if __name__ == "__main__":
    port = int(os.getenv('ML_API_PORT', 8000))
    host = os.getenv('ML_API_HOST', '0.0.0.0')
    
    logger.info(f"Starting ML API on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
