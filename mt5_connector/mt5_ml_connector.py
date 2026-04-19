"""
MT5 Connector for ML Predictions
Connects MetaTrader 5 with ML API for real-time trading signals
Author: Builder-Core
Date: 2026-04-06
"""

import requests
import json
import time
import logging
from datetime import datetime
from typing import Dict, Optional, List
import sqlite3
import os

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/workspace/shared/logs/mt5_connector.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Constants
ML_API_BASE_URL = os.getenv('ML_API_URL', 'http://localhost:8000/api/ml')
DB_PATH = '/workspace/shared/data/mt5_predictions.db'


class MT5MLConnector:
    """
    Connector between MT5 and ML Prediction API
    
    Flow:
    1. MT5 sends market data via ZeroMQ/HTTP
    2. Connector extracts features
    3. Sends to ML API for prediction
    4. Receives signal (BUY/SELL/HOLD)
    5. Logs prediction and optionally sends back to MT5
    """
    
    def __init__(self, api_url: str = None):
        self.api_url = api_url or ML_API_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})
        
        # Ensure DB exists
        self._init_database()
        
        logger.info(f"MT5 Connector initialized. API: {self.api_url}")
    
    def _init_database(self):
        """Initialize SQLite database for logging"""
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                symbol TEXT NOT NULL,
                timeframe TEXT,
                signal TEXT NOT NULL,
                confidence REAL,
                prob_buy REAL,
                prob_sell REAL,
                prob_hold REAL,
                close_price REAL,
                model_version TEXT,
                executed BOOLEAN DEFAULT 0,
                mt5_ticket INTEGER,
                notes TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS market_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                symbol TEXT NOT NULL,
                timeframe TEXT,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume INTEGER
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized")
    
    def extract_features_from_mt5(self, mt5_data: Dict) -> Dict[str, float]:
        """
        Extract features from MT5 market data
        
        Expected MT5 data format:
        {
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
                ...
            }
        }
        """
        features = {}
        
        # Price data
        features['open'] = mt5_data.get('open', 0)
        features['high'] = mt5_data.get('high', 0)
        features['low'] = mt5_data.get('low', 0)
        features['close'] = mt5_data.get('close', 0)
        features['volume'] = mt5_data.get('volume', 0)
        
        # Candlestick features
        features['body_size'] = abs(features['close'] - features['open'])
        features['upper_shadow'] = features['high'] - max(features['open'], features['close'])
        features['lower_shadow'] = min(features['open'], features['close']) - features['low'])
        features['range'] = features['high'] - features['low']
        
        if features['range'] > 0:
            features['body_pct'] = features['body_size'] / features['range']
        else:
            features['body_pct'] = 0
        
        # Add indicators if provided
        indicators = mt5_data.get('indicators', {})
        features.update(indicators)
        
        # Time features
        ts = mt5_data.get('timestamp', '')
        try:
            dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
            features['hour'] = dt.hour
            features['day_of_week'] = dt.weekday()
            features['month'] = dt.month
            features['is_london_session'] = 1 if 8 <= dt.hour < 17 else 0
            features['is_ny_session'] = 1 if 13 <= dt.hour < 22 else 0
            features['is_asia_session'] = 1 if 0 <= dt.hour < 9 else 0
        except:
            features['hour'] = 0
            features['day_of_week'] = 0
            features['is_london_session'] = 0
            features['is_ny_session'] = 0
            features['is_asia_session'] = 0
        
        return features
    
    def get_prediction(self, symbol: str, features: Dict[str, float]) -> Optional[Dict]:
        """
        Get prediction from ML API
        
        Args:
            symbol: Trading pair (EURUSD, etc.)
            features: Dictionary of feature values
            
        Returns:
            Prediction dict or None if error
        """
        try:
            response = self.session.post(
                f"{self.api_url}/predict",
                json={
                    "symbol": symbol,
                    "features": features
                },
                timeout=5
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Prediction API error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            logger.error("Prediction API timeout")
            return None
        except Exception as e:
            logger.error(f"Prediction request error: {e}")
            return None
    
    def log_prediction(self, symbol: str, timeframe: str, prediction: Dict, 
                       close_price: float, executed: bool = False):
        """Log prediction to database"""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO predictions_log 
                (timestamp, symbol, timeframe, signal, confidence, 
                 prob_buy, prob_sell, prob_hold, close_price, model_version, executed)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                symbol,
                timeframe,
                prediction.get('signal'),
                prediction.get('confidence'),
                prediction.get('probability_buy'),
                prediction.get('probability_sell'),
                prediction.get('probability_hold'),
                close_price,
                prediction.get('model_version'),
                executed
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error logging prediction: {e}")
    
    def process_market_data(self, mt5_data: Dict) -> Dict:
        """
        Process market data from MT5 and return prediction
        
        This is the main method called when MT5 sends data
        """
        symbol = mt5_data.get('symbol')
        timeframe = mt5_data.get('timeframe', 'H1')
        
        logger.info(f"Processing {symbol} {timeframe}")
        
        # Extract features
        features = self.extract_features_from_mt5(mt5_data)
        
        # Get prediction
        prediction = self.get_prediction(symbol, features)
        
        if prediction:
            # Log prediction
            self.log_prediction(
                symbol=symbol,
                timeframe=timeframe,
                prediction=prediction,
                close_price=mt5_data.get('close', 0),
                executed=False
            )
            
            # Return formatted response for MT5
            return {
                "success": True,
                "symbol": symbol,
                "signal": prediction['signal'],
                "confidence": prediction['confidence'],
                "probability_buy": prediction['probability_buy'],
                "probability_sell": prediction['probability_sell'],
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "success": False,
                "symbol": symbol,
                "error": "Failed to get prediction"
            }
    
    def get_recent_predictions(self, symbol: str = None, limit: int = 100) -> List[Dict]:
        """Get recent predictions from database"""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            if symbol:
                cursor.execute('''
                    SELECT * FROM predictions_log 
                    WHERE symbol = ? 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (symbol, limit))
            else:
                cursor.execute('''
                    SELECT * FROM predictions_log 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (limit,))
            
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            
            conn.close()
            
            return [dict(zip(columns, row)) for row in rows]
            
        except Exception as e:
            logger.error(f"Error fetching predictions: {e}")
            return []
    
    def get_signal_statistics(self, symbol: str, days: int = 7) -> Dict:
        """Get statistics for signals over time period"""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 
                    signal,
                    COUNT(*) as count,
                    AVG(confidence) as avg_confidence
                FROM predictions_log 
                WHERE symbol = ? 
                AND timestamp >= datetime('now', '-{} days')
                GROUP BY signal
            '''.format(days), (symbol,))
            
            rows = cursor.fetchall()
            conn.close()
            
            stats = {
                'symbol': symbol,
                'period_days': days,
                'signals': {}
            }
            
            for row in rows:
                signal, count, avg_conf = row
                stats['signals'][signal] = {
                    'count': count,
                    'avg_confidence': round(avg_conf, 4) if avg_conf else 0
                }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {}


# Simple HTTP server for MT5 to send data
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

class MT5RequestHandler(BaseHTTPRequestHandler):
    """HTTP handler for MT5 requests"""
    
    connector = None
    
    def do_POST(self):
        """Handle POST requests from MT5"""
        if self.path == '/predict':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                mt5_data = json.loads(post_data)
                result = self.connector.process_market_data(mt5_data)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())
                
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        logger.info(format % args)


def start_server(host: str = '0.0.0.0', port: int = 9000):
    """Start HTTP server for MT5 integration"""
    MT5RequestHandler.connector = MT5MLConnector()
    
    server = HTTPServer((host, port), MT5RequestHandler)
    logger.info(f"MT5 Connector server started on {host}:{port}")
    
    # Run in thread
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    
    return server


if __name__ == '__main__':
    # Start server
    server = start_server()
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        server.shutdown()
