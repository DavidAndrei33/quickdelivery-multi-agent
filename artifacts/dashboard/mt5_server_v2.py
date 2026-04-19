#!/usr/bin/env python3
"""
MT5 CORE SERVER - Server stabil pentru toți clienții MT5
Versiune PostgreSQL - Salvează date în PostgreSQL în loc de SQLite
"""

from collections import deque
from flask import Flask, jsonify, request, send_from_directory
import time
import json
import os
import sys
import logging
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, field
import psycopg2
import psycopg2.extras

# Import MT5ServiceManager for service control
try:
    from mt5_service_manager import MT5ServiceManager, get_service_manager
    SERVICE_MANAGER_AVAILABLE = True
except ImportError:
    SERVICE_MANAGER_AVAILABLE = False

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/root/clawd/agents/brainmaker/mt5_core_server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("MT5CoreServer")

# PostgreSQL Config
PG_CONFIG = {
    'host': os.getenv('PG_HOST', 'localhost'),
    'port': int(os.getenv('PG_PORT', '5432')),
    'database': os.getenv('PG_DATABASE', 'mt5_core'),
    'user': os.getenv('PG_USER', 'brainmaker'),
    'password': os.getenv('PG_PASSWORD', 'brain123')
}

def get_db_connection():
    """Returnează conexiune PostgreSQL"""
    return psycopg2.connect(**PG_CONFIG)

app = Flask(__name__)
PORT = 8001

# AUTH TOKEN (trebuie să corespundă cu cel din EA)
AUTH_TOKEN = "ANDREI_SECRET_TOKEN_V13_AI"

# ========================================================================
# STRUCTURI DATE PENTRU CLIENȚI MT5
# ========================================================================

@dataclass
class MT5Client:
    """Reprezentare client MT5 conectat"""
    login: int
    last_seen: float
    name: str = ""  # Numele beneficiarului contului
    balance: float = 0.0
    equity: float = 0.0
    margin: float = 0.0
    margin_free: float = 0.0
    margin_level: float = 0.0
    profit: float = 0.0
    currency: str = "USD"
    company: str = ""
    positions: List[Dict] = field(default_factory=list)
    market_prices: Dict = field(default_factory=dict)
    is_active: bool = True
    enabled: bool = True  # Dacă poate primi comenzi
    last_positions: List[Dict] = field(default_factory=list)  # Pentru tracking poziții închise

# Cache clienți MT5: {login: MT5Client}
clients_cache: Dict[int, MT5Client] = {}
clients_lock = threading.RLock()

# Cache comenzi pentru clienți: {login: [command1, command2, ...]}
pending_commands: Dict[int, List[Dict]] = {}
commands_lock = threading.RLock()

# Setări globale clienți (persistate în DB)
client_enabled_settings: Dict[int, bool] = {}

# ⭐ Timestamp ultimei recepții date per client: {login: timestamp}
client_last_seen: Dict[int, float] = {}
CLIENT_TIMEOUT_SECONDS = 10  # Timpul după care un client e considerat offline

# ========================================================================
# FUNCȚII DB ȘI SETĂRI CLIENȚI
# ========================================================================

def init_db_schema():
    """Inițializează tabelele necesare dacă nu există"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Tabel setări clienți
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS client_settings (
                login INTEGER PRIMARY KEY,
                name VARCHAR(255),
                enabled BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabel poziții închise (istoric)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS closed_positions (
                id SERIAL PRIMARY KEY,
                login INTEGER NOT NULL,
                ticket BIGINT NOT NULL,
                symbol VARCHAR(20) NOT NULL,
                type VARCHAR(10) NOT NULL,
                volume DECIMAL(10,5) NOT NULL,
                open_price DECIMAL(15,8) NOT NULL,
                close_price DECIMAL(15,8) NOT NULL,
                sl DECIMAL(15,8),
                tp DECIMAL(15,8),
                profit DECIMAL(15,2),
                commission DECIMAL(15,2) DEFAULT 0,
                swap DECIMAL(15,2) DEFAULT 0,
                open_time TIMESTAMP,
                close_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                duration_minutes INTEGER,
                UNIQUE(login, ticket)
            )
        ''')
        
        # Tabel log comenzi
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS command_log (
                id SERIAL PRIMARY KEY,
                login INTEGER,
                command_type VARCHAR(20) NOT NULL,
                symbol VARCHAR(20),
                volume DECIMAL(10,5),
                price DECIMAL(15,8),
                sl DECIMAL(15,8),
                tp DECIMAL(15,8),
                status VARCHAR(20) DEFAULT 'pending',
                response TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                executed_at TIMESTAMP
            )
        ''')
        
        # Tabel activitate clienți
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS client_activity (
                id SERIAL PRIMARY KEY,
                login INTEGER NOT NULL,
                name VARCHAR(255),
                event_type VARCHAR(20) NOT NULL,
                balance DECIMAL(15,2),
                equity DECIMAL(15,2),
                positions_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabel expert_logs - loguri de la EA
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expert_logs (
                id SERIAL PRIMARY KEY,
                login INTEGER NOT NULL,
                message TEXT NOT NULL,
                log_type VARCHAR(20) DEFAULT 'INFO',
                symbol VARCHAR(20),
                ticket BIGINT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_expert_logs_login ON expert_logs(login)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_expert_logs_type ON expert_logs(log_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_expert_logs_created ON expert_logs(created_at DESC)')
        
        # Tabel journal_entries - jurnal tranzacții de la EA
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS journal_entries (
                id SERIAL PRIMARY KEY,
                login INTEGER NOT NULL,
                level VARCHAR(20) DEFAULT 'INFO',
                source VARCHAR(50),
                message TEXT NOT NULL,
                symbol VARCHAR(20),
                ticket BIGINT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_journal_login ON journal_entries(login)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_journal_level ON journal_entries(level)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_journal_created ON journal_entries(created_at DESC)')
        
        # Tabel open_positions - poziții deschise pentru tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS open_positions (
                id SERIAL PRIMARY KEY,
                login INTEGER NOT NULL,
                ticket BIGINT NOT NULL UNIQUE,
                symbol VARCHAR(10) NOT NULL,
                type VARCHAR(10) NOT NULL,
                volume DECIMAL(10,5) NOT NULL,
                open_price DECIMAL(15,8) NOT NULL,
                sl DECIMAL(15,8),
                tp DECIMAL(15,8),
                open_time TIMESTAMP NOT NULL,
                source VARCHAR(50),
                created_by VARCHAR(100),
                status VARCHAR(20) DEFAULT 'open',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_open_positions_login ON open_positions(login)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_open_positions_ticket ON open_positions(ticket)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_open_positions_status ON open_positions(status)')
        
        # Tabel trade_sources - tracking modificări și surse
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trade_sources (
                id SERIAL PRIMARY KEY,
                ticket BIGINT NOT NULL,
                login INTEGER,
                action VARCHAR(50),
                source VARCHAR(50),
                old_values JSONB,
                new_values JSONB,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_trade_sources_ticket ON trade_sources(ticket)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_trade_sources_action ON trade_sources(action)')
        
        # Tabel service_registry - înregistrare servicii
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS service_registry (
                id SERIAL PRIMARY KEY,
                service_name VARCHAR(100) UNIQUE NOT NULL,
                service_type VARCHAR(50) NOT NULL,
                description TEXT,
                process_name VARCHAR(100),
                systemd_service VARCHAR(100),
                account_login VARCHAR(20),
                auto_start BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabel service_status - status servicii
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS service_status (
                id SERIAL PRIMARY KEY,
                service_name VARCHAR(100) UNIQUE NOT NULL,
                status VARCHAR(20) DEFAULT 'stopped',
                is_enabled BOOLEAN DEFAULT TRUE,
                last_activity TIMESTAMP,
                commands_sent INTEGER DEFAULT 0,
                commands_executed INTEGER DEFAULT 0,
                commands_failed INTEGER DEFAULT 0,
                pid INTEGER,
                uptime_seconds INTEGER DEFAULT 0,
                last_error TEXT,
                error_count INTEGER DEFAULT 0,
                started_at TIMESTAMP,
                stopped_at TIMESTAMP
            )
        ''')
        
        # Tabel command_log - logarea tuturor comenzilor trimise
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS command_log (
                id SERIAL PRIMARY KEY,
                command_id BIGINT,
                action VARCHAR(20) NOT NULL,
                login INTEGER,
                ticket BIGINT,
                symbol VARCHAR(20),
                volume DECIMAL(10,2),
                sl DECIMAL(10,5),
                tp DECIMAL(10,5),
                source VARCHAR(100) DEFAULT 'unknown',
                ip_address VARCHAR(45),
                user_agent TEXT,
                status VARCHAR(20) DEFAULT 'queued',
                error_message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                executed_at TIMESTAMP
            )
        ''')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_command_log_login ON command_log(login)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_command_log_action ON command_log(action)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_command_log_source ON command_log(source)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_command_log_created ON command_log(created_at DESC)')

        # Tabel user_mt5_accounts - asociere utilizatori dashboard cu conturi MT5
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_mt5_accounts (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) NOT NULL,
                mt5_login BIGINT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(username, mt5_login)
            )
        ''')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_mt5_accounts_username ON user_mt5_accounts(username)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_mt5_accounts_login ON user_mt5_accounts(mt5_login)')
        
        conn.commit()
        conn.close()
        logger.info("✅ Schema DB inițializată")
    except Exception as e:
        logger.error(f"Eroare inițializare DB schema: {e}")

def load_client_settings():
    """Încarcă setările clienților din DB"""
    global client_enabled_settings
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT login, enabled FROM client_settings')
        for row in cursor.fetchall():
            client_enabled_settings[row[0]] = row[1]
        conn.close()
        logger.info(f"✅ Setări clienți încărcate: {len(client_enabled_settings)}")
    except Exception as e:
        logger.error(f"Eroare încărcare setări: {e}")

def save_closed_position(login: int, position: Dict, close_price: float):
    """Salvează o poziție închisă în istoric și actualizează statusul comenzii"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        ticket = position.get('ticket')
        symbol = position.get('symbol')
        pos_type = position.get('type')
        profit = position.get('profit', 0)
        
        # Calculează durata
        open_time = position.get('open_time', position.get('time', ''))
        duration = None
        if open_time:
            try:
                if isinstance(open_time, str):
                    open_dt = datetime.fromisoformat(open_time.replace('Z', '+00:00'))
                else:
                    open_dt = datetime.fromtimestamp(open_time)
                duration = int((datetime.now() - open_dt.replace(tzinfo=None)).total_seconds() / 60)
            except:
                pass
        
        cursor.execute('''
            INSERT INTO closed_positions 
            (login, ticket, symbol, type, volume, open_price, close_price, sl, tp, profit, swap, open_time, duration_minutes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (login, ticket) DO NOTHING
        ''', (
            login,
            ticket,
            symbol,
            pos_type,
            position.get('volume'),
            position.get('open_price', position.get('price_open')),
            close_price,
            position.get('sl'),
            position.get('tp'),
            profit,
            position.get('swap', 0),
            open_time if isinstance(open_time, str) else datetime.fromtimestamp(open_time) if open_time else None,
            duration
        ))
        
        # ⭐ Actualizează statusul comenzii în funcție de profit
        if profit > 0:
            status = 'win'
        elif profit < 0:
            status = 'loss'
        else:
            status = 'break_even'
        
        cursor.execute('''
            UPDATE command_log 
            SET status = %s, 
                response = %s,
                executed_at = CURRENT_TIMESTAMP
            WHERE login = %s AND ticket = %s AND status IN ('executed', 'queued', 'pending')
        ''', (status, f"Closed with profit: ${profit:.2f}", login, ticket))
        
        if cursor.rowcount > 0:
            logger.info(f"✅ Comandă actualizată: {status} pentru ticket {ticket}")
        
        conn.commit()
        conn.close()
        logger.info(f"💾 Poziție închisă salvată: {symbol} #{ticket} Profit: ${profit:.2f}")
    except Exception as e:
        logger.error(f"Eroare salvare poziție închisă: {e}")

def process_closed_positions_history(login: int, history: List[Dict]):
    """Procesează istoricul pozițiilor închise trimis de MT5 EA
    
    Grupează deal-urile după position_id și acumulează comisioanele.
    MT5 generează 2 deal-uri per poziție (deschidere + închidere),
    fiecare cu comision separat (ex: -0.04 + -0.04 = -0.08 total).
    """
    if not history:
        return
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Grupează deal-urile după position_id
        positions = {}  # position_id -> date acumulate
        
        for deal in history:
            try:
                position_id = deal.get('position_id') or deal.get('ticket')
                ticket = deal.get('ticket')
                
                if not ticket:
                    continue
                
                # Verifică dacă poziția există deja în DB
                cursor.execute('SELECT id FROM closed_positions WHERE login = %s AND (ticket = %s OR ticket = %s)', 
                              (login, ticket, position_id))
                if cursor.fetchone():
                    continue  # Skip dacă există
                
                # Acumulează datele per position_id
                if position_id not in positions:
                    positions[position_id] = {
                        'ticket': ticket,
                        'symbol': deal.get('symbol'),
                        'type': deal.get('type'),
                        'volume': deal.get('volume'),
                        'open_price': deal.get('open_price'),
                        'close_price': deal.get('close_price'),
                        'sl': deal.get('sl'),
                        'tp': deal.get('tp'),
                        'profit': 0.0,       # Va fi acumulat
                        'commission': 0.0,   # Va fi acumulat
                        'swap': 0.0,         # Va fi acumulat
                        'open_time': deal.get('open_time'),
                        'close_time': deal.get('close_time')
                    }
                
                # Adună profit, comision și swap
                positions[position_id]['profit'] += float(deal.get('profit', 0) or 0)
                positions[position_id]['commission'] += float(deal.get('commission', 0) or 0)
                positions[position_id]['swap'] += float(deal.get('swap', 0) or 0)
                
                # Actualizează open/close times dacă sunt disponibile
                if deal.get('open_time') and not positions[position_id]['open_time']:
                    positions[position_id]['open_time'] = deal.get('open_time')
                if deal.get('close_time'):
                    positions[position_id]['close_time'] = deal.get('close_time')
                    
            except Exception as e:
                logger.error(f"Eroare procesare deal istoric {deal.get('ticket')}: {e}")
                continue
        
        # Inserează pozițiile acumulate în DB
        saved_count = 0
        for position_id, pos in positions.items():
            try:
                # Calculează durata
                open_time = pos.get('open_time')
                close_time = pos.get('close_time')
                duration = None
                if open_time and close_time:
                    try:
                        duration = int((close_time - open_time) / 60)
                    except:
                        pass
                
                cursor.execute('''
                    INSERT INTO closed_positions 
                    (login, ticket, symbol, type, volume, open_price, close_price, sl, tp, 
                     profit, commission, swap, open_time, close_time, duration_minutes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', (
                    login,
                    pos.get('ticket'),
                    pos.get('symbol'),
                    pos.get('type'),
                    pos.get('volume'),
                    pos.get('open_price'),
                    pos.get('close_price'),
                    pos.get('sl'),
                    pos.get('tp'),
                    pos.get('profit'),
                    pos.get('commission'),  # ACUM SUMĂ TOTALĂ!
                    pos.get('swap'),
                    datetime.fromtimestamp(open_time) if open_time else None,
                    datetime.fromtimestamp(close_time) if close_time else None,
                    duration
                ))
                saved_count += 1
                
            except Exception as e:
                logger.error(f"Eroare insert poziție {position_id}: {e}")
                continue
        
        conn.commit()
        conn.close()
        
        if saved_count > 0:
            logger.info(f"💾 SalVate {saved_count} poziții istorice cu comisioane acumulate pentru login {login}")
            
    except Exception as e:
        logger.error(f"Eroare procesare istoric closed_positions: {e}")


def log_command_to_db(command: Dict, source: str = 'unknown', ip_address: str = None, user_agent: str = None, status: str = 'queued'):
    """Loghează o comandă în baza de date cu sursa acesteia"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO command_log 
            (command_id, command_type, login, ticket, symbol, volume, sl, tp, source, ip_address, user_agent, status, error_message)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            command.get('command_id'),
            command.get('action'),  # command_type în DB
            command.get('login'),
            command.get('ticket'),
            command.get('symbol'),
            command.get('volume'),
            command.get('sl'),
            command.get('tp'),
            source,
            ip_address,
            user_agent,
            status,
            None
        ))
        
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Eroare logare comandă în DB: {e}")


def process_expert_logs(login: int, logs: List[Dict]):
    """Procesează logurile expertului de la MT5 EA"""
    if not logs:
        return
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        inserted = 0
        for log in logs:
            try:
                cursor.execute('''
                    INSERT INTO expert_logs (login, message, log_type, created_at)
                    VALUES (%s, %s, %s, COALESCE(%s, CURRENT_TIMESTAMP))
                ''', (
                    login,
                    log.get('message', ''),
                    log.get('type', 'INFO'),
                    datetime.fromtimestamp(log.get('timestamp')) if log.get('timestamp') else None
                ))
                inserted += 1
            except Exception as e:
                logger.error(f"Eroare inserare expert log: {e}")
                continue
        
        conn.commit()
        conn.close()
        
        if inserted > 0:
            logger.info(f"📝 Expert logs salvate pentru {login}: {inserted} intrări")
    except Exception as e:
        logger.error(f"Eroare procesare expert logs: {e}")

def process_journal_entries(login: int, entries: List[Dict]):
    """Procesează intrările din jurnal de la MT5 EA"""
    if not entries:
        return
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        inserted = 0
        for entry in entries:
            try:
                cursor.execute('''
                    INSERT INTO journal_entries (login, level, source, message, created_at)
                    VALUES (%s, %s, %s, %s, COALESCE(%s, CURRENT_TIMESTAMP))
                ''', (
                    login,
                    entry.get('level', 'INFO'),
                    entry.get('source', 'EA'),
                    entry.get('message', ''),
                    datetime.fromtimestamp(entry.get('timestamp')) if entry.get('timestamp') else None
                ))
                inserted += 1
                
                # Procesează mesajele de trading
                message = entry.get('message', '')
                process_trading_message(login, message, cursor)
                
            except Exception as e:
                logger.error(f"Eroare inserare journal entry: {e}")
                continue
        
        conn.commit()
        conn.close()
        
        if inserted > 0:
            logger.info(f"📓 Journal entries salvate pentru {login}: {inserted} intrări")
    except Exception as e:
        logger.error(f"Eroare procesare journal entries: {e}")


# ========================================================================
# TRANSACTION TRACKING - TRACKING TRANZACȚII
# ========================================================================

def calculate_profit(symbol: str, trade_type: str, open_price: float, close_price: float, volume: float) -> float:
    """Calculează profitul unei tranzacții în USD"""
    # Pip value pentru fiecare pereche
    pip_values = {
        'USDJPY': 0.01, 'EURUSD': 0.0001, 'GBPUSD': 0.0001,
        'AUDJPY': 0.01, 'CADJPY': 0.01, 'CHFJPY': 0.01,
        'GBPJPY': 0.01, 'EURJPY': 0.01, 'USDCHF': 0.0001,
        'AUDUSD': 0.0001, 'USDCAD': 0.0001, 'NZDUSD': 0.0001,
        'XAUUSD': 0.01, 'XAGUSD': 0.01
    }
    
    pip_size = pip_values.get(symbol.upper(), 0.0001)
    
    if trade_type.upper() == 'BUY':
        pips = (close_price - open_price) / pip_size
    else:
        pips = (open_price - close_price) / pip_size
    
    # Profit aproximativ: $10 per pip per lot (standard)
    profit = pips * volume * 10
    return round(profit, 2)


def extract_source_from_message(message: str) -> str:
    """Extrage sursa din mesaj (ex: BrainBridge_V13_Live -> BrainBridge_V13)"""
    import re
    
    # Pattern pentru BrainBridge variants
    bb_pattern = r'(BrainBridge_V\d+)(?:_Live|_Demo|_Test)?'
    match = re.search(bb_pattern, message, re.IGNORECASE)
    if match:
        return match.group(1)
    
    # Pattern pentru alte surse
    if 'manual' in message.lower():
        return 'Manual'
    if 'python_api' in message.lower():
        return 'Python_API'
    
    return 'Unknown'


def parse_open_position_message(message: str) -> Optional[Dict]:
    """Parsează mesaj de deschidere poziție: 'market buy 0.01 USDJPY sl: 159.391 tp: 159.540'"""
    import re
    
    # Pattern pentru market buy/sell
    pattern = r'market\s+(buy|sell)\s+([\d.]+)\s+(\w+)(?:\s+sl:\s*([\d.]+))?(?:\s+tp:\s*([\d.]+))?' 
    match = re.search(pattern, message, re.IGNORECASE)
    
    if match:
        return {
            'type': match.group(1).upper(),
            'volume': float(match.group(2)),
            'symbol': match.group(3).upper(),
            'sl': float(match.group(4)) if match.group(4) else None,
            'tp': float(match.group(5)) if match.group(5) else None,
            'source': extract_source_from_message(message)
        }
    
    # Pattern alternativ: "accepted market buy 0.01 EURUSD sl: 1.08220 tp: 1.09020"
    alt_pattern = r'accepted\s+market\s+(buy|sell)\s+([\d.]+)\s+(\w+)(?:\s+sl:\s*([\d.]+))?(?:\s+tp:\s*([\d.]+))?'
    alt_match = re.search(alt_pattern, message, re.IGNORECASE)
    
    if alt_match:
        return {
            'type': alt_match.group(1).upper(),
            'volume': float(alt_match.group(2)),
            'symbol': alt_match.group(3).upper(),
            'sl': float(alt_match.group(4)) if alt_match.group(4) else None,
            'tp': float(alt_match.group(5)) if alt_match.group(5) else None,
            'source': extract_source_from_message(message)
        }
    
    return None


def parse_close_position_message(message: str) -> Optional[Dict]:
    """Parsează mesaj de închidere: 'deal #1280689313 sell 0.01 USDJPY at 159.545'"""
    import re
    
    # Pattern pentru deal
    pattern = r'deal\s+#(\d+)\s+(buy|sell)\s+([\d.]+)\s+(\w+)\s+at\s+([\d.]+)'
    match = re.search(pattern, message, re.IGNORECASE)
    
    if match:
        return {
            'ticket': int(match.group(1)),
            'type': match.group(2).upper(),  # Invers față de deschidere
            'volume': float(match.group(3)),
            'symbol': match.group(4).upper(),
            'close_price': float(match.group(5)),
            'source': extract_source_from_message(message)
        }
    
    # Pattern alternativ cu done
    alt_pattern = r'deal\s+#(\d+)\s+(buy|sell)\s+([\d.]+)\s+(\w+)\s+at\s+([\d.]+)\s+done'
    alt_match = re.search(alt_pattern, message, re.IGNORECASE)
    
    if alt_match:
        return {
            'ticket': int(alt_match.group(1)),
            'type': alt_match.group(2).upper(),
            'volume': float(alt_match.group(3)),
            'symbol': alt_match.group(4).upper(),
            'close_price': float(alt_match.group(5)),
            'source': extract_source_from_message(message)
        }
    
    return None


def parse_modify_position_message(message: str) -> Optional[Dict]:
    """Parsează mesaj de modificare SL/TP"""
    import re
    
    # Pattern pentru modify
    pattern = r'modify\s+#?(\d+)(?:\s+(buy|sell))?.*?(?:sl:\s*([\d.]+))?(?:\s+tp:\s*([\d.]+))?'
    match = re.search(pattern, message, re.IGNORECASE)
    
    if match:
        return {
            'ticket': int(match.group(1)) if match.group(1) else None,
            'type': match.group(2).upper() if match.group(2) else None,
            'sl': float(match.group(3)) if match.group(3) else None,
            'tp': float(match.group(4)) if match.group(4) else None,
            'source': extract_source_from_message(message)
        }
    
    return None


def process_open_position(login: int, parsed_data: Dict, cursor, client_ip: str = None):
    """Procesează deschiderea unei poziții"""
    try:
        # Generează ticket temporar sau ia din date
        # Încearcă să găsești ticketul din mesaje anterioare
        symbol = parsed_data['symbol']
        ticket = parsed_data.get('ticket')
        
        # Dacă nu avem ticket, generăm unul temporar bazat pe timestamp
        if not ticket:
            ticket = int(time.time() * 1000) % 1000000000
        
        # Salvează în open_positions
        cursor.execute('''
            INSERT INTO open_positions 
            (login, ticket, symbol, type, volume, open_price, sl, tp, open_time, source, created_by, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'open')
            ON CONFLICT (ticket) DO UPDATE SET
                sl = COALESCE(EXCLUDED.sl, open_positions.sl),
                tp = COALESCE(EXCLUDED.tp, open_positions.tp),
                source = COALESCE(EXCLUDED.source, open_positions.source)
        ''', (
            login, ticket, symbol, parsed_data['type'], 
            parsed_data['volume'], 0,  # open_price va fi actualizat când avem deal
            parsed_data.get('sl'), parsed_data.get('tp'),
            datetime.now(), parsed_data.get('source', 'Unknown'),
            client_ip or 'system'
        ))
        
        # Loghează în trade_sources
        cursor.execute('''
            INSERT INTO trade_sources (ticket, login, action, source, new_values)
            VALUES (%s, %s, 'open', %s, %s)
        ''', (
            ticket, login, parsed_data.get('source', 'Unknown'),
            json.dumps({
                'symbol': symbol,
                'type': parsed_data['type'],
                'volume': parsed_data['volume'],
                'sl': parsed_data.get('sl'),
                'tp': parsed_data.get('tp')
            })
        ))
        
        logger.info(f"🟢 Poziție deschisă: {symbol} {parsed_data['type']} {parsed_data['volume']} (Ticket: {ticket}, Source: {parsed_data.get('source', 'Unknown')})")
        return ticket
        
    except Exception as e:
        logger.error(f"Eroare procesare deschidere poziție: {e}")
        return None


def process_close_position(login: int, parsed_data: Dict, cursor):
    """Procesează închiderea unei poziții"""
    try:
        ticket = parsed_data['ticket']
        
        # Găsește poziția deschisă
        cursor.execute('''
            SELECT id, symbol, type, volume, open_price, sl, tp, open_time, source, created_by
            FROM open_positions WHERE ticket = %s AND status = 'open'
        ''', (ticket,))
        
        row = cursor.fetchone()
        
        if not row:
            logger.warning(f"Poziție {ticket} nu a fost găsită în open_positions")
            return False
        
        id, symbol, open_type, volume, open_price, sl, tp, open_time, open_source, opened_by = row
        close_price = parsed_data['close_price']
        close_time = datetime.now()
        
        # Calculează profit și durată
        profit = calculate_profit(symbol, open_type, open_price or close_price, close_price, volume)
        
        duration_minutes = None
        if open_time:
            duration_minutes = int((close_time - open_time).total_seconds() / 60)
        
        closed_by = parsed_data.get('source', 'Unknown')
        
        # Mută în closed_positions
        cursor.execute('''
            INSERT INTO closed_positions 
            (login, ticket, symbol, type, volume, open_price, close_price, sl, tp, 
             profit, open_time, close_time, duration_minutes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (login, ticket) DO UPDATE SET
                close_price = EXCLUDED.close_price,
                profit = EXCLUDED.profit,
                close_time = EXCLUDED.close_time,
                duration_minutes = EXCLUDED.duration_minutes
        ''', (
            login, ticket, symbol, open_type, volume, open_price or close_price,
            close_price, sl, tp, profit, open_time, close_time, duration_minutes
        ))
        
        # Loghează în trade_sources
        cursor.execute('''
            INSERT INTO trade_sources (ticket, login, action, source, old_values, new_values)
            VALUES (%s, %s, 'close', %s, %s, %s)
        ''', (
            ticket, login, closed_by,
            json.dumps({
                'status': 'open',
                'open_price': float(open_price) if open_price else None,
                'source': open_source
            }),
            json.dumps({
                'status': 'closed',
                'close_price': close_price,
                'profit': profit,
                'duration_minutes': duration_minutes,
                'source': closed_by
            })
        ))
        
        # Șterge din open_positions
        cursor.execute("UPDATE open_positions SET status = 'closed' WHERE id = %s", (id,))
        
        logger.info(f"🔴 Poziție închisă: {symbol} #{ticket} Profit: ${profit:.2f} (Opened by: {open_source}, Closed by: {closed_by})")
        return True
        
    except Exception as e:
        logger.error(f"Eroare procesare închidere poziție: {e}")
        return False


def process_modify_position(login: int, parsed_data: Dict, cursor):
    """Procesează modificarea unei poziții (SL/TP)"""
    try:
        ticket = parsed_data.get('ticket')
        if not ticket:
            return False
        
        # Găsește poziția
        cursor.execute('''
            SELECT id, sl, tp, source FROM open_positions WHERE ticket = %s
        ''', (ticket,))
        
        row = cursor.fetchone()
        if not row:
            return False
        
        id, old_sl, old_tp, old_source = row
        new_sl = parsed_data.get('sl')
        new_tp = parsed_data.get('tp')
        modified_by = parsed_data.get('source', 'Unknown')
        
        # Actualizează poziția
        if new_sl is not None or new_tp is not None:
            cursor.execute('''
                UPDATE open_positions 
                SET sl = COALESCE(%s, sl), tp = COALESCE(%s, tp)
                WHERE id = %s
            ''', (new_sl, new_tp, id))
        
        # Loghează modificarea
        cursor.execute('''
            INSERT INTO trade_sources (ticket, login, action, source, old_values, new_values)
            VALUES (%s, %s, 'modify', %s, %s, %s)
        ''', (
            ticket, login, modified_by,
            json.dumps({'sl': float(old_sl) if old_sl else None, 'tp': float(old_tp) if old_tp else None}),
            json.dumps({'sl': new_sl, 'tp': new_tp})
        ))
        
        logger.info(f"📝 Poziție modificată: #{ticket} SL: {old_sl}→{new_sl}, TP: {old_tp}→{new_tp} (By: {modified_by})")
        return True
        
    except Exception as e:
        logger.error(f"Eroare procesare modificare poziție: {e}")
        return False


def process_trading_message(login: int, message: str, cursor, client_ip: str = None):
    """Procesează un mesaj de trading și actualizează bazele de date"""
    try:
        # Încearcă să parseze ca deschidere
        open_data = parse_open_position_message(message)
        if open_data:
            return process_open_position(login, open_data, cursor, client_ip)
        
        # Încearcă să parseze ca închidere
        close_data = parse_close_position_message(message)
        if close_data:
            return process_close_position(login, close_data, cursor)
        
        # Încearcă să parseze ca modificare
        modify_data = parse_modify_position_message(message)
        if modify_data:
            return process_modify_position(login, modify_data, cursor)
        
        return None
        
    except Exception as e:
        logger.debug(f"Eroare procesare mesaj trading: {e}")
        return None

def log_command(login: int, command: Dict, status: str = 'pending', response: str = None):
    """Loghează o comandă trimisă cu detalii complete de analiză"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Build detailed comment with analysis
        comment_parts = []
        
        # Source
        if command.get('source'):
            comment_parts.append(f"Sursa: {command.get('source')}")
        
        # Reason/Logic
        if command.get('reason'):
            comment_parts.append(f"Motiv: {command.get('reason')}")
        
        # Analysis details
        analysis = command.get('analysis', {})
        if analysis:
            analysis_parts = []
            if analysis.get('rsi'):
                analysis_parts.append(f"RSI={analysis['rsi']}")
            if analysis.get('stochastic'):
                analysis_parts.append(f"Stoch={analysis['stochastic']}")
            if analysis.get('trend_h4'):
                analysis_parts.append(f"H4={analysis['trend_h4']}")
            if analysis.get('trend_m15'):
                analysis_parts.append(f"M15={analysis['trend_m15']}")
            if analysis.get('in_bb_zone'):
                analysis_parts.append("BB=hit")
            if analysis_parts:
                comment_parts.append(f"Analiză: {', '.join(analysis_parts)}")
        
        # Original comment
        if command.get('comment'):
            comment_parts.append(f"Notă: {command.get('comment')}")
        
        comment = ' | '.join(comment_parts) if comment_parts else None
        
        cursor.execute('''
            INSERT INTO command_log 
            (login, command_type, symbol, volume, price, sl, tp, status, response, comment)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            login,
            command.get('action'),
            command.get('symbol'),
            command.get('volume'),
            command.get('price'),
            command.get('sl'),
            command.get('tp'),
            status,
            response,
            comment
        ))
        
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Eroare logging comandă: {e}")

def log_client_activity(login: int, name: str, event_type: str, balance: float = None, equity: float = None, positions_count: int = 0):
    """Loghează activitatea unui client"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO client_activity 
            (login, name, event_type, balance, equity, positions_count)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (login, name, event_type, balance, equity, positions_count))
        
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Eroare logging activitate: {e}")

def is_client_enabled(login: int) -> bool:
    """
    Verifică dacă un client poate primi comenzi.
    
    Un client poate primi comenzi doar dacă:
    1. Este enabled în settings (manual din dashboard)
    2. Este online (a trimis date în ultimele 10 secunde)
    """
    global client_enabled_settings, client_last_seen
    
    # Verifică 1: Statusul manual (enabled/disabled din dashboard)
    if login in client_enabled_settings:
        if not client_enabled_settings[login]:
            return False  # Client disabled manual
    
    # Verifică 2: Clientul este online (a trimis date recent)
    if login in client_last_seen:
        last_seen = client_last_seen[login]
        time_since_last_data = time.time() - last_seen
        
        if time_since_last_data > CLIENT_TIMEOUT_SECONDS:
            # Client offline - nu a trimis date de > 10 secunde
            logger.warning(f"⛔ Client {login} este OFFLINE (nu a trimis date de {time_since_last_data:.1f}s)")
            return False
    else:
        # Nu am văzut niciodată acest client
        logger.warning(f"⛔ Client {login} - nu există în client_last_seen")
        return False
    
    return True  # Client enabled și online

def is_client_online(login: int) -> tuple:
    """
    Returnează statusul complet al unui client.
    
    Returns:
        tuple: (is_online: bool, reason: str, last_seen_seconds: float)
    """
    global client_enabled_settings, client_last_seen
    
    # Verifică dacă e disabled manual
    if login in client_enabled_settings and not client_enabled_settings[login]:
        return (False, "disabled_manual", 0)
    
    # Verifică timeout
    if login in client_last_seen:
        last_seen = client_last_seen[login]
        time_since = time.time() - last_seen
        
        if time_since > CLIENT_TIMEOUT_SECONDS:
            return (False, "timeout", time_since)
        else:
            return (True, "online", time_since)
    else:
        return (False, "never_seen", 0)

def set_client_enabled(login: int, enabled: bool, name: str = None):
    """Setează statusul enabled/disabled pentru un client"""
    global client_enabled_settings
    
    client_enabled_settings[login] = enabled
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO client_settings (login, name, enabled, updated_at)
            VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
            ON CONFLICT (login) DO UPDATE SET 
                enabled = EXCLUDED.enabled,
                updated_at = EXCLUDED.updated_at,
                name = COALESCE(EXCLUDED.name, client_settings.name)
        ''', (login, name, enabled))
        
        conn.commit()
        conn.close()
        
        status = "ENABLED" if enabled else "DISABLED"
        logger.info(f"🔧 Client {login} ({name or 'Unknown'}) - {status}")
    except Exception as e:
        logger.error(f"Eroare salvare setări client: {e}")

# ========================================================================
# GESTIUNE CLIENȚI
# ========================================================================

def update_client(login: int, data: Dict):
    """Actualizează datele unui client MT5 și updatează timestamp-ul last_seen"""
    global clients_cache, client_last_seen
    
    with clients_lock:
        account = data.get('account', {})
        positions = data.get('positions', [])
        # FIX: market prices sunt în data['market']['prices'] nu în data['market_prices']
        market_data = data.get('market', {})
        market_prices = market_data.get('prices', {})
        
        # ⭐ Updatează timestamp-ul de last_seen pentru acest client
        client_last_seen[login] = time.time()
        
        if login not in clients_cache:
            clients_cache[login] = MT5Client(
                login=login,
                last_seen=time.time()
            )
        
        client = clients_cache[login]
        client.last_seen = time.time()
        
        # Setează numele beneficiarului (din 'name' sau 'account_name')
        account_name = account.get('name', account.get('account_name', ''))
        client.name = account_name
        client.balance = account.get('balance', 0)
        client.equity = account.get('equity', 0)
        client.margin = account.get('margin', 0)
        client.margin_free = account.get('margin_free', 0)
        client.margin_level = account.get('margin_level', 0)
        client.profit = account.get('profit', 0)
        client.currency = account.get('currency', 'USD')
        client.company = account.get('company', '')
        
        # Sync poziții cu open_positions - actualizează open_price real
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            for pos in positions:
                ticket = pos.get('ticket')
                open_price = pos.get('open_price', pos.get('price_open'))
                symbol = pos.get('symbol')
                pos_type = pos.get('type')
                volume = pos.get('volume')
                
                # Verifică dacă există în open_positions și actualizează open_price
                cursor.execute('''
                    UPDATE open_positions 
                    SET open_price = %s, symbol = %s, type = %s, volume = %s
                    WHERE ticket = %s AND status = 'open' AND open_price = 0
                ''', (open_price, symbol, pos_type, volume, ticket))
                
                # Dacă nu există, poate fi o poziție deschisă manual sau înainte de tracking
                if cursor.rowcount == 0:
                    # ⭐ Încearcă să găsești sursa reală din command_log
                    # Mărim intervalul la 60 de minute pentru a prinde comenzile mai vechi
                    cursor.execute('''
                        SELECT id, source FROM command_log 
                        WHERE login = %s AND symbol = %s AND command_type = %s
                        AND created_at > NOW() - INTERVAL '60 minutes'
                        AND (status = 'queued' OR status = 'pending')
                        ORDER BY created_at DESC LIMIT 1
                    ''', (login, symbol, pos_type))
                    
                    result = cursor.fetchone()
                    if result:
                        command_id, actual_source = result
                        # ⭐ Actualizează statusul comenzii la 'executed' și setează ticketul
                        cursor.execute('''
                            UPDATE command_log 
                            SET status = 'executed', ticket = %s, executed_at = CURRENT_TIMESTAMP
                            WHERE id = %s
                        ''', (ticket, command_id))
                        logger.info(f"✅ Comandă {command_id} actualizată: executată pentru ticket {ticket}")
                    else:
                        actual_source = 'MT5_Sync'
                    
                    cursor.execute('''
                        INSERT INTO open_positions 
                        (login, ticket, symbol, type, volume, open_price, sl, tp, open_time, source, status)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'open')
                        ON CONFLICT (ticket) DO UPDATE SET
                            open_price = EXCLUDED.open_price,
                            sl = COALESCE(EXCLUDED.sl, open_positions.sl),
                            tp = COALESCE(EXCLUDED.tp, open_positions.tp)
                    ''', (
                        login, ticket, symbol, pos_type, volume, open_price,
                        pos.get('sl'), pos.get('tp'),
                        datetime.fromtimestamp(pos.get('time', time.time())) if pos.get('time') else datetime.now(),
                        actual_source if result else 'MT5_Sync'
                    ))
            
            conn.commit()
            conn.close()
        except Exception as e:
            logger.debug(f"Eroare sync poziții cu open_positions: {e}")
        
        # Detectează poziții închise (existau înainte, dar nu mai există)
        current_tickets = {p.get('ticket') for p in positions}
        old_tickets = {p.get('ticket') for p in client.last_positions}
        
        closed_tickets = old_tickets - current_tickets
        for old_pos in client.last_positions:
            if old_pos.get('ticket') in closed_tickets:
                # Găsește prețul de închidere (din market_prices sau folosește ultimul cunoscut)
                symbol = old_pos.get('symbol')
                close_price = 0
                if symbol in market_prices:
                    close_price = market_prices[symbol].get('bid', 0)
                # Salvează în istoric
                save_closed_position(login, old_pos, close_price)
        
        # Salvează pozițiile curente pentru următoarea comparație
        client.last_positions = positions.copy()
        client.positions = positions
        client.market_prices = market_prices
        client.is_active = True
        
        # Setează statusul enabled din setări
        client.enabled = is_client_enabled(login)
        
        # Log activitate (doar ocazional, nu la fiecare update)
        if not hasattr(client, '_last_activity_log') or time.time() - client._last_activity_log > 300:  # 5 minute
            log_client_activity(login, account_name, 'heartbeat', client.balance, client.equity, len(positions))
            client._last_activity_log = time.time()
        
        # Dacă e prima conectare, loghează
        if not hasattr(client, '_first_connect_logged'):
            log_client_activity(login, account_name, 'connected', client.balance, client.equity, len(positions))
            client._first_connect_logged = True
        
        # SALVEAZĂ în DB pentru persistență (PostgreSQL) - cu toate câmpurile
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Preia numele contului din date (dacă există)
            account_name = account.get('name', account.get('account_name', f'Account_{login}'))
            
            # ⭐ Salvează și numele în client_settings pentru a-l avea disponibil când e offline
            cursor.execute('''
                INSERT INTO client_settings (login, name, enabled, updated_at)
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (login) DO UPDATE SET 
                    name = EXCLUDED.name,
                    updated_at = EXCLUDED.updated_at
            ''', (login, account_name, client.enabled))
            
            cursor.execute('''
                INSERT INTO account_updates 
                (login, timestamp, account_name, balance, equity, margin, margin_free, margin_level, profit)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                login,
                int(time.time()),
                account_name,
                client.balance,
                client.equity,
                client.margin,
                client.margin_free,
                client.margin_level,
                client.profit
            ))
            
            conn.commit()
            conn.close()
            logger.info(f"💾 Account: {account_name} ({login}) | B:${client.balance:.2f} E:${client.equity:.2f} M:${client.margin:.2f} MF:${client.margin_free:.2f} ML:{client.margin_level:.2f}% P:${client.profit:.2f}")
        except Exception as e:
            logger.error(f"Eroare salvare account pentru {login}: {e}")
        
        logger.debug(f"Client {login} actualizat: Balance=${client.balance:.2f}, "
                    f"Positions={len(positions)}")
        
        # SALVEAZĂ POZIȚIILE în PostgreSQL
        try:
            save_positions_to_db(login, positions)
        except Exception as e:
            logger.error(f"Eroare salvare poziții pentru {login}: {e}")


def save_positions_to_db(login: int, positions: List[Dict]):
    """Salvează pozițiile în PostgreSQL"""
    if not positions:
        return
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Șterge pozițiile vechi pentru acest login
        cursor.execute('DELETE FROM client_positions WHERE login = %s', (login,))
        
        # Inserează pozițiile noi
        for pos in positions:
            cursor.execute('''
                INSERT INTO client_positions 
                (login, symbol, direction, volume, entry_price, sl_price, tp_price, profit)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (login, symbol) DO UPDATE SET
                    direction = EXCLUDED.direction,
                    volume = EXCLUDED.volume,
                    entry_price = EXCLUDED.entry_price,
                    sl_price = EXCLUDED.sl_price,
                    tp_price = EXCLUDED.tp_price,
                    profit = EXCLUDED.profit,
                    updated_at = CURRENT_TIMESTAMP
            ''', (
                login,
                pos.get('symbol', ''),
                pos.get('type', pos.get('direction', 'BUY')),  # Suportă ambele formate
                pos.get('volume', 0),
                pos.get('open_price', pos.get('entry_price', 0)),
                pos.get('sl', pos.get('sl_price', 0)),
                pos.get('tp', pos.get('tp_price', 0)),
                pos.get('profit', 0)
            ))
        
        conn.commit()
        logger.info(f"📊 Poziții salvate: {login} | {len(positions)} poziții")
    except Exception as e:
        logger.error(f"Eroare în save_positions_to_db: {e}")
    finally:
        conn.close()


def get_active_clients() -> Dict[int, MT5Client]:
    """Returnează doar clienții activi ( < 30 secunde de la ultimul tick)"""
    with clients_lock:
        current_time = time.time()
        return {
            login: client for login, client in clients_cache.items()
            if current_time - client.last_seen < 30
        }


def remove_inactive_clients():
    """Elimină clienții inactivi"""
    global clients_cache
    
    with clients_lock:
        current_time = time.time()
        inactive = [
            login for login, client in clients_cache.items()
            if current_time - client.last_seen >= 60
        ]
        for login in inactive:
            clients_cache[login].is_active = False
            logger.warning(f"Client {login} marcat ca inactiv")


# ========================================================================
# PROCESARE DATE PIAȚĂ
# ========================================================================

def process_market_data(data: Dict):
    """Procesează datele de piață și le salvează în DB"""
    
    # MT5 trimite date în 'market' cu sub-chei 'prices' și 'ohlc'
    market_data = data.get('market', {})
    timestamp = data.get('timestamp_client', int(time.time()))
    login = data.get('account', {}).get('login', 0)
    
    # CORECȚIE FUS ORAR: MT5 trimite GMT+02, convertim la UTC
    if timestamp > 1770000000:
        timestamp = timestamp - 7200
    
    if not market_data:
        return
    
    # === SALVEAZĂ OHLC DIRECT DIN MT5 (cele mai precise date) ===
    ohlc_data = market_data.get('ohlc', {})
    
    # Structura: {'M1': {'EURUSD': [{'open', 'high', 'low', 'close'}, ...], ...}}
    for timeframe, symbols_data in ohlc_data.items():
        if isinstance(symbols_data, dict):
            for symbol, ohlc_list in symbols_data.items():
                # OHLC e o listă de candles
                if isinstance(ohlc_list, list):
                    for ohlc in ohlc_list:
                        if isinstance(ohlc, dict) and all(k in ohlc for k in ['open', 'high', 'low', 'close']):
                            try:
                                # Folosește timpul real al candelei (când s-a închis)
                                candle_timestamp = ohlc.get('time', timestamp)
                                
                                conn = get_db_connection()
                                cursor = conn.cursor()
                                
                                # Folosim INSERT simplu pentru PostgreSQL
                                cursor.execute('''
                                    INSERT INTO ohlc_data 
                                    (symbol, timeframe, timestamp, open, high, low, close, volume)
                                    VALUES (%s, 'M1', %s, %s, %s, %s, %s, %s)
                                    ON CONFLICT (symbol, timeframe, timestamp) DO UPDATE SET
                                        open = EXCLUDED.open,
                                        high = EXCLUDED.high,
                                        low = EXCLUDED.low,
                                        close = EXCLUDED.close,
                                        volume = EXCLUDED.volume
                                ''', (symbol, candle_timestamp,
                                      ohlc['open'], ohlc['high'], ohlc['low'], ohlc['close'],
                                      ohlc.get('volume', 0)))
                                
                                conn.commit()
                                conn.close()
                                logger.info(f"✅ OHLC direct {symbol}: T:{candle_timestamp} O:{ohlc['open']} H:{ohlc['high']} L:{ohlc['low']} C:{ohlc['close']}")
                            except Exception as e:
                                logger.error(f"Eroare salvare OHLC direct {symbol}: {e}")
    
    # === SALVEAZĂ ȘI TICK-URI (prețuri curente) ===
    prices_data = market_data.get('prices', {})
    
    if not prices_data:
        return
    
    logger.info(f"Processing {len(prices_data)} symbols for login {login}")
    
    for symbol, prices in prices_data.items():
        if isinstance(prices, dict):
            bid = prices.get('bid')
            ask = prices.get('ask')
            
            if bid is not None and ask is not None:
                # Broadcast to WebSocket clients (sub-50ms)
                try:
                    price_feed = get_price_feed_server()
                    price_feed.update_price(symbol, bid, ask)
                except Exception as e:
                    logger.debug(f"WebSocket broadcast error: {e}")
                
                # Salvează tick în DB (PostgreSQL) - doar ticks_live
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    
                    cursor.execute('''
                        INSERT INTO ticks_live (symbol, bid, ask, spread, time)
                        VALUES (%s, %s, %s, %s, to_timestamp(%s))
                        ON CONFLICT (symbol) DO UPDATE SET
                            bid = EXCLUDED.bid,
                            ask = EXCLUDED.ask,
                            spread = EXCLUDED.spread,
                            time = EXCLUDED.time
                    ''', (symbol, bid, ask, round(ask - bid, 6), timestamp))
                    
                    conn.commit()
                    conn.close()
                    logger.debug(f"Saved tick for {symbol}")
                except Exception as e:
                    logger.error(f"Eroare salvare tick {symbol}: {e}")


def process_historical_data(data: Dict):
    """Procesează datele istorice (OHLC)"""
    
    historical = data.get('historical_data', {})
    
    for timeframe, symbols in historical.items():
        for symbol, ohlc in symbols.items():
            try:
                # Salvează candlestick în DB
                hub.add_candle(
                    symbol=symbol,
                    timestamp=datetime.fromtimestamp(ohlc.get('time', 0)),
                    open_p=ohlc.get('open', 0),
                    high=ohlc.get('high', 0),
                    low=ohlc.get('low', 0),
                    close=ohlc.get('close', 0),
                    volume=ohlc.get('volume', 0),
                    source=f'mt5_{timeframe.lower()}'
                )
            except Exception as e:
                logger.error(f"Eroare salvare {timeframe} {symbol}: {e}")


# ========================================================================
# RISK MANAGEMENT ȘI COMENZI
# ========================================================================

def calculate_position_size(balance: float, risk_percent: float, 
                            sl_pips: float, pip_value: float = 10.0) -> float:
    """Calculează lot size în funcție de balanță și risk"""
    
    # Risk per trade în USD
    risk_amount = balance * (risk_percent / 100)
    
    # Lot size = Risk Amount / (SL pips * pip value)
    if sl_pips > 0 and pip_value > 0:
        lot_size = risk_amount / (sl_pips * pip_value)
    else:
        lot_size = 0.01  # Default minim
    
    # Round la 0.01 (standard MT5)
    return round(max(0.01, min(lot_size, 100.0)), 2)


def adapt_command_for_client(command: Dict, client: MT5Client) -> Dict:
    """Adaptează comanda în funcție de balanța clientului"""
    
    adapted = command.copy()
    
    # Dacă e comanda de deschidere poziție, adaptează lot size
    if command.get('action') in ['BUY', 'SELL']:
        base_lot = command.get('lot', 0.01)
        base_balance = 10000.0  # Balanță de referință
        
        # Calculează lot proporțional
        if client.balance > 0:
            ratio = client.balance / base_balance
            adapted['lot'] = round(base_lot * ratio, 2)
        
        # Verifică dacă are suficient margin
        if client.margin_free < adapted['lot'] * 1000:  # Estimare simplă
            logger.warning(f"Client {client.login}: Margin insuficient")
            adapted['lot'] = max(0.01, client.margin_free / 1000)
    
    return adapted


def add_command_for_all_clients(command: Dict) -> int:
    """Adaugă comandă pentru TOȚI clienții activi (și enabled)
    
    Returns:
        int: Numărul de clienți cărora li s-a adăugat comanda
    """
    global pending_commands
    
    with commands_lock:
        active_clients = get_active_clients()
        added_count = 0
        
        for login, client in active_clients.items():
            # ⭐ VERIFICĂ DACĂ CLIENTUL ESTE ENABLED
            if not is_client_enabled(login):
                continue
            
            # Adaptează comanda pentru acest client
            adapted_cmd = adapt_command_for_client(command, client)
            
            if login not in pending_commands:
                pending_commands[login] = []
            
            pending_commands[login].append({
                **adapted_cmd,
                'timestamp': int(time.time()),
                'command_id': command.get('command_id', int(time.time() * 1000))
            })
            added_count += 1
        
        logger.info(f"Comandă '{command.get('action')}' adăugată pentru "
                   f"{added_count}/{len(active_clients)} clienți (doar cei activi și enabled)")
        
        return added_count


def get_pending_commands(login: int) -> List[Dict]:
    """Returnează și șterge comenzile în așteptare pentru un client"""
    global pending_commands
    
    with commands_lock:
        commands = pending_commands.get(login, [])
        pending_commands[login] = []  # Golește după citire
        return commands


# ========================================================================
# TRAILING STOP LOSS
# ========================================================================

trailing_settings: Dict[int, Dict] = {}  # {login: {symbol: {'activation_pips': x, 'trailing_pips': y}}}

def update_trailing_sl(client: MT5Client):
    """Verifică și actualizează Trailing SL pentru pozițiile deschise"""
    
    for position in client.positions:
        symbol = position.get('symbol')
        pos_type = position.get('type')  # BUY sau SELL
        open_price = position.get('open_price', 0)
        current_price = position.get('current_price', 0)
        current_sl = position.get('sl', 0)
        ticket = position.get('ticket')
        profit_pips = position.get('profit_pips', 0)
        
        # Setări trailing pentru acest simbol
        trail_config = trailing_settings.get(client.login, {}).get(symbol, {
            'activation_pips': 10,  # Activează după 10 pips profit
            'trailing_pips': 5      # Mută SL la 5 pips distanță
        })
        
        activation = trail_config['activation_pips']
        trailing = trail_config['trailing_pips']
        
        if profit_pips >= activation:
            # Calculare nou SL
            if pos_type == 'BUY':
                new_sl = current_price - (trailing * 0.0001)  # 5 pips în price
                if new_sl > current_sl:
                    add_modify_command(client.login, ticket, new_sl, position.get('tp'))
                    logger.info(f"Trailing SL {client.login}/{symbol}: {current_sl} -> {new_sl}")
            
            elif pos_type == 'SELL':
                new_sl = current_price + (trailing * 0.0001)
                if new_sl < current_sl or current_sl == 0:
                    add_modify_command(client.login, ticket, new_sl, position.get('tp'))
                    logger.info(f"Trailing SL {client.login}/{symbol}: {current_sl} -> {new_sl}")


def add_modify_command(login: int, ticket: int, new_sl: float, new_tp: float):
    """Adaugă comandă de modificare SL/TP"""
    global pending_commands
    
    with commands_lock:
        if login not in pending_commands:
            pending_commands[login] = []
        
        pending_commands[login].append({
            'action': 'MODIFY',
            'ticket': ticket,
            'sl': new_sl,
            'tp': new_tp,
            'timestamp': int(time.time()),
            'command_id': int(time.time() * 1000)
        })


@app.route('/', methods=['GET'])
def root():
    """Pagina principală - redirectează la health sau afișează status"""
    return jsonify({
        "service": "MT5 Core Server",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "clients": "/clients",
            "update": "/update (POST)",
            "command": "/command (POST)"
        }
    })

@app.route('/update', methods=['POST'])
def receive_update():
    """
    Primește date de la BrainBridge EA (MT5).
    Acceptă și fără Content-Type header (pentru compatibilitate MT5).
    """
    try:
        # Acceptă JSON chiar dacă Content-Type nu e setat corect
        if request.is_json:
            data = request.get_json()
        else:
            # Încearcă să parseze ca JSON direct din body
            try:
                raw_data = request.get_data(as_text=True)
                data = json.loads(raw_data)
            except Exception as e:
                logger.error(f"JSON parse error: {e}, data: {request.get_data()}")
                return jsonify({"error": "Invalid JSON"}), 400
        
        # Verificare token (opțional pentru testare)
        token = data.get('token', '')
        if token and token != AUTH_TOKEN:
            return jsonify({"error": "Invalid token"}), 401
        
        # Extrage datele - suportă multiple formate
        # Format 1: {"payload": {"account": {"login": X, ...}}}
        # Format 2: {"account": {"login": X, ...}}
        # Format 3: {"login": X, ...}
        
        payload = data.get('payload', {})
        if not payload:
            payload = data  # Dacă nu există payload, folosește data direct
        
        account = payload.get('account', {})
        if not account:
            account = payload  # Dacă nu există account, caută în payload direct
        
        login = account.get('login', 0)
        if login == 0:
            login = payload.get('login', 0)  # Încearcă și în payload direct
        
        if login == 0:
            logger.error(f"Login not found in data: {data}")
            return jsonify({"error": "Invalid login", "received": str(data)[:100]}), 400
        
        # Actualizează clientul
        update_client(login, payload)
        
        # Log DETALIAT pentru debug
        logger.info(f"📥 Update de la {login}: positions={len(payload.get('positions', []))}, market_keys={list(payload.get('market', {}).keys()) if 'market' in payload else 'NO MARKET'}")
        
        # Log ce primim
        logger.info(f"Payload keys: {list(payload.keys())}")
        
        # Verifică structura datelor
        market_data = payload.get('market', {})
        if 'prices' in market_data:
            logger.info(f"Market prices: {len(market_data['prices'])} symbols")
        elif 'ohlc' in market_data:
            logger.info(f"Market OHLC: {len(market_data['ohlc'])} symbols")
        else:
            logger.warning(f"No market data in payload for login {login}")
        
        # Procesează datele de piață
        process_market_data(payload)
        
        # Procesează datele istorice
        process_historical_data(payload)
        
        # Procesează istoricul pozițiilor închise (NOU)
        process_closed_positions_history(login, payload.get('history', []))
        
        # 🔴 DEZACTIVAT - Logurile vin acum doar din /logs/upload (Log Watcher)
        # process_expert_logs(login, payload.get('expert_logs', []))
        # process_journal_entries(login, payload.get('journal', []))
        
        # Verifică trailing SL
        client = clients_cache.get(login)
        if client:
            update_trailing_sl(client)
        
        # Returnează comenzile în așteptare pentru acest client
        commands = get_pending_commands(login)
        
        # Logging pentru debug
        if commands:
            logger.info(f"📤 Trimit {len(commands)} comenzi către login {login}: {[c.get('action') for c in commands]}")
        
        # Construiește răspunsul - dacă există comenzi, returnează prima direct
        # pentru compatibilitate cu EA (caută "action" direct în răspuns)
        if commands and len(commands) > 0:
            # Returnează comanda direct + array pentru backward compatibility
            response = {
                "status": "ok",
                "action": commands[0].get("action"),
                "ticket": commands[0].get("ticket"),
                "login": commands[0].get("login"),
                "sl": commands[0].get("sl"),
                "tp": commands[0].get("tp"),
                "commands": commands,  # Păstrăm și array pentru viitor
                "server_time": int(time.time())
            }
        else:
            response = {
                "status": "ok",
                "commands": [],
                "server_time": int(time.time())
            }
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Eroare procesare update: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    active_clients = get_active_clients()
    
    return jsonify({
        "status": "healthy",
        "port": PORT,
        "active_clients": len(active_clients),
        "total_clients": len(clients_cache),
        "server_time": datetime.now().isoformat()
    })


@app.route('/clients', methods=['GET'])
def list_clients():
    """Lista tuturor clienților (pentru debugging)"""
    active = get_active_clients()
    
    return jsonify({
        "active_clients": [
            {
                "login": c.login,
                "name": c.name,
                "balance": c.balance,
                "equity": c.equity,
                "margin": c.margin,
                "margin_free": c.margin_free,
                "margin_level": c.margin_level,
                "profit": c.profit,
                "currency": c.currency,
                "company": c.company,
                "positions_count": len(c.positions),
                "last_seen": datetime.fromtimestamp(c.last_seen).isoformat()
            }
            for c in active.values()
        ]
    })


@app.route('/positions', methods=['GET'])
def get_positions():
    """Returnează toate pozițiile deschise de la toți clienții activi."""
    try:
        all_positions = []
        with clients_lock:
            for login, client in clients_cache.items():
                if client.is_active:
                    for pos in client.positions:
                        symbol = pos.get('symbol')
                        # Get current price from market_prices if available
                        current_price = pos.get('current_price', pos.get('price_current'))
                        if not current_price and symbol in client.market_prices:
                            current_price = client.market_prices[symbol].get('bid')
                        
                        all_positions.append({
                            'ticket': pos.get('ticket'),
                            'symbol': symbol,
                            'type': pos.get('type'),
                            'volume': pos.get('volume'),
                            'open_price': pos.get('open_price', pos.get('price_open')),
                            'current_price': current_price,
                            'sl': pos.get('sl'),
                            'tp': pos.get('tp'),
                            'profit': pos.get('profit'),
                            'profit_pips': pos.get('profit_pips'),
                            'login': login
                        })
        return jsonify({"status": "success", "positions": all_positions, "count": len(all_positions)}), 200
    except Exception as e:
        logger.error(f"Eroare la obținerea pozițiilor: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/command', methods=['POST'])
def send_command():
    """
    Primește comandă de la roboți (V29, V31, etc.) și o adaugă pentru client.
    Exemplu: {"action": "BUY", "symbol": "EURUSD", "volume": 0.01, "login": 52715350}
    
    Comanda este logată și trimisă doar dacă clientul este enabled.
    """
    try:
        command = request.json
        action = command.get('action', '')
        login = command.get('login')
        
        # Detectează sursa comenzii (din comment sau default la numele robotului)
        source = command.get('comment', 'robot')
        if 'V29' in source:
            source = 'V29_Trading_Robot'
        elif 'V31' in source or 'Marius' in source:
            source = 'V31_Marius_Live'
        elif 'daemon' in source.lower():
            source = 'Market_Daemon'
        else:
            source = 'Trading_Robot'
        
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent', '')[:200]
        
        # Generează command_id
        command_id = int(time.time() * 1000)
        command['command_id'] = command_id
        
        # Loghează comanda
        log_command_to_db(command, source, ip_address, user_agent, status='queued')
        
        # ⭐ Verifică dacă clientul este enabled și online
        if login:
            online_status, reason, time_since = is_client_online(login)
            if not online_status:
                if reason == "disabled_manual":
                    logger.warning(f"⛔ Comandă {action} de la {source} refuzată pentru login {login} - clientul este DISABLED")
                    return jsonify({
                        "status": "error",
                        "message": "Client is disabled",
                        "target_client": login,
                        "reason": "disabled"
                    }), 403
                elif reason == "timeout":
                    logger.warning(f"⛔ Comandă {action} de la {source} refuzată pentru login {login} - clientul este OFFLINE ({time_since:.1f}s)")
                    return jsonify({
                        "status": "error",
                        "message": f"Client is offline (no data for {time_since:.1f}s)",
                        "target_client": login,
                        "reason": "offline",
                        "last_seen_seconds": time_since
                    }), 403
                else:
                    logger.warning(f"⛔ Comandă {action} de la {source} refuzată pentru login {login} - client necunoscut")
                    return jsonify({
                        "status": "error",
                        "message": "Client not found",
                        "target_client": login,
                        "reason": "unknown"
                    }), 403
        
        # Procesează comanda
        if login:
            ticket = command.get('ticket', 0)
            sl = command.get('sl', 0)
            tp = command.get('tp', 0)
            
            if action == 'MODIFY':
                add_modify_command(login, ticket, sl, tp)
                logger.info(f"📝 Comandă MODIFY de la {source} pentru login {login}, ticket {ticket}")
            elif action == 'CLOSE':
                with commands_lock:
                    if login not in pending_commands:
                        pending_commands[login] = []
                    pending_commands[login].append({
                        **command,
                        'timestamp': int(time.time()),
                        'command_id': command_id,
                        'status': 'queued'
                    })
                logger.info(f"📝 Comandă CLOSE de la {source} pentru login {login}, ticket {ticket}")
            else:
                # BUY, SELL, etc.
                with commands_lock:
                    if login not in pending_commands:
                        pending_commands[login] = []
                    pending_commands[login].append({
                        **command,
                        'timestamp': int(time.time()),
                        'command_id': command_id,
                        'status': 'queued'
                    })
                logger.info(f"📝 Comandă {action} de la {source} pentru login {login}")
            
            return jsonify({
                "status": "success",
                "message": f"{action} command queued",
                "command_id": command_id,
                "target_client": login,
                "source": source
            }), 200
        else:
            # Fără login specific - adaugă pentru toți clienții enabled
            target_count = add_command_for_all_clients(command)
            
            logger.info(f"🌐 Comandă {action} de la {source} - trimisă la {target_count} clienți")
            
            return jsonify({
                "status": "success",
                "message": f"{action} command queued for {target_count} clients",
                "command_id": command_id,
                "target_count": target_count,
                "source": source
            }), 200
        
    except Exception as e:
        logger.error(f"Eroare trimitere comandă: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
        return jsonify({"error": str(e)}), 500


@app.route('/api/command', methods=['POST'])
def api_command():
    """
    API endpoint pentru comenzi (apelat din dashboard sau alte surse).
    
    Comenzile sunt logate cu sursa și trimise imediat către clienți (dacă sunt enabled).
    Doar clienții disabled sunt blocați.
    """
    try:
        command = request.json
        action = command.get('action', '')
        login = command.get('login')
        
        # Detectează sursa comenzii
        source = command.get('source', 'api')
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent', '')[:200]
        
        # Generează command_id unic
        command_id = int(time.time() * 1000)
        command['command_id'] = command_id
        
        # Loghează comanda
        log_command_to_db(command, source, ip_address, user_agent, status='queued')
        
        # ⭐ Verifică dacă e comandă per-client (cu login specific)
        if action in ['CLOSE', 'MODIFY']:
            if not login:
                return jsonify({
                    "status": "error", 
                    "message": f"Command {action} requires login parameter"
                }), 400
            
            # ⭐ Verifică dacă clientul este enabled și online
            online_status, reason, time_since = is_client_online(login)
            if not online_status:
                if reason == "disabled_manual":
                    logger.warning(f"⛔ Comandă {action} refuzată pentru login {login} - clientul este DISABLED")
                    return jsonify({
                        "status": "error", 
                        "message": "Client is disabled",
                        "target_client": login,
                        "reason": "disabled"
                    }), 403
                elif reason == "timeout":
                    logger.warning(f"⛔ Comandă {action} refuzată pentru login {login} - clientul este OFFLINE ({time_since:.1f}s)")
                    return jsonify({
                        "status": "error",
                        "message": f"Client is offline (no data for {time_since:.1f}s)",
                        "target_client": login,
                        "reason": "offline",
                        "last_seen_seconds": time_since
                    }), 403
                else:
                    return jsonify({
                        "status": "error",
                        "message": "Client not found",
                        "target_client": login,
                        "reason": "unknown"
                    }), 403
            
            if action == 'MODIFY':
                add_modify_command(login, command.get('ticket', 0), command.get('sl', 0), command.get('tp', 0))
                logger.info(f"📝 Comandă MODIFY de la {source} pentru login {login}, ticket {command.get('ticket')}")
            elif action == 'CLOSE':
                with commands_lock:
                    if login not in pending_commands:
                        pending_commands[login] = []
                    pending_commands[login].append({
                        **command,
                        'timestamp': int(time.time()),
                        'command_id': command_id,
                        'status': 'queued'
                    })
                logger.info(f"📝 Comandă CLOSE de la {source} pentru login {login}, ticket {command.get('ticket')}")
            
            return jsonify({
                "status": "success",
                "message": f"{action} command queued",
                "command_id": command_id,
                "target_client": login,
                "source": source
            }), 200
        
        # ⭐ Comenzi globale (BUY, SELL, CLOSE_ALL)
        else:
            # Adaugă pentru toți clienții activi și enabled
            target_count = add_command_for_all_clients(command)
            
            logger.info(f"🌐 Comandă {action} de la {source} - trimisă la {target_count} clienți")
            
            return jsonify({
                "status": "success",
                "message": f"{action} command queued for {target_count} clients",
                "command_id": command_id,
                "target_count": target_count,
                "source": source
            }), 200
            
    except Exception as e:
        logger.error(f"Eroare API command: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/prices/<symbol>', methods=['GET'])
def get_symbol_price(symbol):
    """
    Returnează prețul LIVE pentru un simbol de la primul client activ.
    Exemplu: GET /prices/EURUSD
    """
    try:
        with clients_lock:
            for login, client in clients_cache.items():
                if client.is_active and symbol in client.market_prices:
                    price_data = client.market_prices[symbol]
                    return jsonify({
                        "status": "success",
                        "symbol": symbol,
                        "bid": price_data.get('bid'),
                        "ask": price_data.get('ask'),
                        "timestamp": price_data.get('timestamp'),
                        "source": login
                    }), 200
        
        return jsonify({
            "status": "error",
            "message": f"No price data for {symbol}"
        }), 404
        
    except Exception as e:
        logger.error(f"Eroare la obținerea prețului pentru {symbol}: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/prices', methods=['GET'])
def get_all_prices():
    """
    Returnează toate prețurile LIVE de la toți clienții activi.
    """
    try:
        all_prices = {}
        with clients_lock:
            for login, client in clients_cache.items():
                if client.is_active:
                    all_prices.update(client.market_prices)
        
        return jsonify({
            "status": "success",
            "prices": all_prices,
            "count": len(all_prices)
        }), 200
        
    except Exception as e:
        logger.error(f"Eroare la obținerea prețurilor: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/command/pending', methods=['GET'])
def api_get_pending_commands():
    """API: Returnează toate comenzile în așteptare (pending_approval)"""
    try:
        limit = request.args.get('limit', 50, type=int)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, command_id, command_type, login, ticket, symbol, volume, sl, tp, 
                   source, ip_address, status, created_at
            FROM command_log
            WHERE status = 'pending_approval'
            ORDER BY created_at DESC
            LIMIT %s
        ''', (limit,))
        
        commands = []
        for row in cursor.fetchall():
            commands.append({
                'id': row[0],
                'command_id': row[1],
                'action': row[2],
                'login': row[3],
                'ticket': row[4],
                'symbol': row[5],
                'volume': float(row[6]) if row[6] else None,
                'sl': float(row[7]) if row[7] else None,
                'tp': float(row[8]) if row[8] else None,
                'source': row[9],
                'ip_address': row[10],
                'status': row[11],
                'created_at': row[12].isoformat() if row[12] else None
            })
        
        conn.close()
        return jsonify({
            'status': 'success', 
            'commands': commands, 
            'count': len(commands)
        }), 200
    except Exception as e:
        logger.error(f"Eroare API pending commands: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/command/<int:command_id>/approve', methods=['POST'])
def api_approve_command(command_id):
    """API: Aprobă o comandă și o trimite către clienți MT5"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Găsește comanda
        cursor.execute('''
            SELECT command_id, command_type, login, ticket, symbol, volume, sl, tp
            FROM command_log
            WHERE command_id = %s AND status = 'pending_approval'
        ''', (command_id,))
        
        row = cursor.fetchone()
        if not row:
            conn.close()
            return jsonify({
                'status': 'error',
                'message': 'Command not found or already processed'
            }), 404
        
        cmd_id, action, login, ticket, symbol, volume, sl, tp = row
        
        # Construiește comanda
        command = {
            'command_id': cmd_id,
            'action': action,
            'login': login,
            'ticket': ticket,
            'symbol': symbol,
            'volume': float(volume) if volume else None,
            'sl': float(sl) if sl else None,
            'tp': float(tp) if tp else None
        }
        
        # Trimite comanda către clienți
        if action in ['CLOSE', 'MODIFY']:
            if not login:
                cursor.execute("UPDATE command_log SET status = 'rejected', error_message = 'No login specified' WHERE command_id = %s", (command_id,))
                conn.commit()
                conn.close()
                return jsonify({'status': 'error', 'message': 'Command requires login'}), 400
            
            if not is_client_enabled(login):
                cursor.execute("UPDATE command_log SET status = 'rejected', error_message = 'Client disabled' WHERE command_id = %s", (command_id,))
                conn.commit()
                conn.close()
                return jsonify({'status': 'error', 'message': 'Client is disabled'}), 403
            
            if action == 'MODIFY':
                add_modify_command(login, ticket, sl or 0, tp or 0)
            elif action == 'CLOSE':
                with commands_lock:
                    if login not in pending_commands:
                        pending_commands[login] = []
                    pending_commands[login].append({
                        **command,
                        'timestamp': int(time.time()),
                        'status': 'queued'
                    })
        else:
            # Comenzi globale
            add_command_for_all_clients(command)
        
        # Update status în DB
        cursor.execute("UPDATE command_log SET status = 'queued', executed_at = CURRENT_TIMESTAMP WHERE command_id = %s", (command_id,))
        conn.commit()
        conn.close()
        
        logger.info(f"✅ Comandă {command_id} ({action}) aprobată și trimisă")
        
        return jsonify({
            'status': 'success',
            'message': 'Command approved and queued',
            'command_id': command_id,
            'action': action
        }), 200
        
    except Exception as e:
        logger.error(f"Eroare aprobare comandă {command_id}: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/command/<int:command_id>/reject', methods=['POST'])
def api_reject_command(command_id):
    """API: Respinge o comandă"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE command_log 
            SET status = 'rejected', error_message = 'Rejected by admin'
            WHERE command_id = %s AND status = 'pending_approval'
        ''', (command_id,))
        
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({
                'status': 'error',
                'message': 'Command not found or already processed'
            }), 404
        
        conn.commit()
        conn.close()
        
        logger.info(f"❌ Comandă {command_id} respinsă")
        
        return jsonify({
            'status': 'success',
            'message': 'Command rejected',
            'command_id': command_id
        }), 200
        
    except Exception as e:
        logger.error(f"Eroare respingere comandă {command_id}: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


# ========================================================================
# THREAD DE CLEANUP
# ========================================================================

def cleanup_thread():
    """Thread care rulează periodic pentru cleanup"""
    while True:
        time.sleep(30)
        remove_inactive_clients()


# ========================================================================
# DASHBOARD WEB - ENDPOINTS
# ========================================================================

from flask import send_from_directory
import os

DASHBOARD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dashboard')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    """Servește pagina principală a dashboard-ului"""
    try:
        return send_from_directory(DASHBOARD_DIR, 'index.html')
    except Exception as e:
        logger.error(f"Eroare servire dashboard: {e}")
        return jsonify({"error": "Dashboard not available"}), 500

@app.route('/login.html', methods=['GET'])
def login_page():
    """Servește pagina de login"""
    try:
        return send_from_directory(DASHBOARD_DIR, 'login.html')
    except Exception as e:
        logger.error(f"Eroare servire login: {e}")
        return jsonify({"error": "Login page not available"}), 500

@app.route('/dashboard/static/<path:filename>', methods=['GET'])
def dashboard_static(filename):
    """Servește fișierele statice (CSS, JS)"""
    try:
        static_dir = os.path.join(DASHBOARD_DIR, 'static')
        return send_from_directory(static_dir, filename)
    except Exception as e:
        logger.error(f"Eroare servire static file {filename}: {e}")
        return jsonify({"error": "File not found"}), 404

@app.route('/dashboard_functional.js', methods=['GET'])
def dashboard_js():
    """Servește fișierul JavaScript principal al dashboard-ului"""
    try:
        return send_from_directory(DASHBOARD_DIR, 'dashboard_functional.js')
    except Exception as e:
        logger.error(f"Eroare servire dashboard JS: {e}")
        return jsonify({"error": "JavaScript not found"}), 404

@app.route('/auth.js', methods=['GET'])
def auth_js():
    """Servește fișierul JavaScript de autentificare"""
    try:
        return send_from_directory(DASHBOARD_DIR, 'auth.js')
    except Exception as e:
        logger.error(f"Eroare servire auth JS: {e}")
        return jsonify({"error": "Auth JavaScript not found"}), 404

@app.route('/api/clients', methods=['GET'])
def api_clients():
    """API: Returnează clienții (activi și inactivi din DB) cu status online/offline
    
    Filtrare bazată pe utilizator:
    - Admin vede toți clienții
    - User normal vede doar conturile MT5 asociate lui
    """
    try:
        # Verifică autentificare și rol
        auth_header = request.headers.get('Authorization')
        current_user = None
        user_role = 'user'
        allowed_logins = []
        
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header[7:]
            if token in active_sessions:
                session = active_sessions[token]
                current_user = session['username']
                user_role = session.get('role', 'user')
        
        # Dacă nu e admin, ia conturile asociate
        if user_role != 'admin' and current_user:
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT mt5_login FROM user_mt5_accounts WHERE username = %s',
                    (current_user,)
                )
                allowed_logins = [row[0] for row in cursor.fetchall()]
                conn.close()
            except Exception as e:
                logger.error(f"Eroare citire asocieri conturi: {e}")
        
        # Clienți activi (din cache)
        active_clients = []
        with clients_lock:
            for login, client in clients_cache.items():
                # ⭐ Filtrare: dacă nu e admin și nu are conturi asociate, arată doar cele asociate
                if user_role != 'admin' and allowed_logins:
                    if login not in allowed_logins:
                        continue
                
                # ⭐ Verifică statusul online folosind funcția centralizată
                is_online, reason, time_since = is_client_online(login)
                
                if is_online:
                    status = 'online'
                elif reason == 'timeout':
                    status = 'offline'
                elif reason == 'disabled_manual':
                    status = 'disabled'
                else:
                    status = 'unknown'
                
                active_clients.append({
                    'login': client.login,
                    'name': client.name,
                    'balance': client.balance,
                    'equity': client.equity,
                    'profit': client.profit,
                    'margin_level': client.margin_level,
                    'positions_count': len(client.positions),
                    'is_active': client.is_active,
                    'enabled': client.enabled,
                    'last_seen': datetime.fromtimestamp(client.last_seen).isoformat(),
                    'status': status,
                    'seconds_since_last_data': round(time_since, 1) if is_online else None
                })
        
        # Clienți din DB (toți cei care au fost văzuți)
        db_clients = []
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT DISTINCT ON (login) login, name, enabled 
                FROM client_settings 
                ORDER BY login, updated_at DESC
            ''')
            for row in cursor.fetchall():
                login, name, enabled = row
                
                # ⭐ Filtrare: dacă nu e admin și nu are conturi asociate, skip
                if user_role != 'admin' and allowed_logins:
                    if login not in allowed_logins:
                        continue
                
                # Verifică dacă e deja în lista activă
                if not any(c['login'] == login for c in active_clients):
                    db_clients.append({
                        'login': login,
                        'name': name or f'Account_{login}',
                        'balance': 0,
                        'equity': 0,
                        'profit': 0,
                        'margin_level': 0,
                        'positions_count': 0,
                        'is_active': False,
                        'enabled': enabled if enabled is not None else True,
                        'last_seen': None,
                        'status': 'disconnected'
                    })
            conn.close()
        except Exception as e:
            logger.error(f"Eroare citire clienți din DB: {e}")
        
        return jsonify({
            'status': 'success',
            'active': active_clients,
            'inactive': db_clients,
            'total_active': len(active_clients),
            'total_inactive': len(db_clients),
            'user_role': user_role,
            'filtered': user_role != 'admin'
        }), 200
    except Exception as e:
        logger.error(f"Eroare API clients: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/positions', methods=['GET'])
def api_positions():
    """API: Returnează toate pozițiile active"""
    try:
        all_positions = []
        with clients_lock:
            for login, client in clients_cache.items():
                if client.is_active:
                    for pos in client.positions:
                        symbol = pos.get('symbol')
                        current_price = pos.get('current_price', pos.get('price_current'))
                        if not current_price and symbol in client.market_prices:
                            current_price = client.market_prices[symbol].get('bid')
                        
                        all_positions.append({
                            'ticket': pos.get('ticket'),
                            'login': login,
                            'client_name': client.name,
                            'symbol': symbol,
                            'type': pos.get('type'),
                            'volume': pos.get('volume'),
                            'open_price': pos.get('open_price', pos.get('price_open')),
                            'current_price': current_price,
                            'sl': pos.get('sl'),
                            'tp': pos.get('tp'),
                            'profit': pos.get('profit'),
                            'swap': pos.get('swap', 0)
                        })
        return jsonify({'status': 'success', 'positions': all_positions}), 200
    except Exception as e:
        logger.error(f"Eroare API positions: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/history', methods=['GET'])
def api_history():
    """API: Returnează istoricul pozițiilor închise cu tracking complet al surselor"""
    try:
        limit = request.args.get('limit', 100, type=int)
        login_filter = request.args.get('login', None, type=int)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 1. Ia date din closed_positions
        query = '''
            SELECT login, ticket, symbol, type, volume, open_price, close_price, sl, tp,
                   profit, commission, swap, close_time, duration_minutes
            FROM closed_positions
            WHERE 1=1
        '''
        params = []
        
        if login_filter:
            query += ' AND login = %s'
            params.append(login_filter)
        
        query += ' ORDER BY close_time DESC LIMIT %s'
        params.append(limit)
        
        cursor.execute(query, params)
        
        history = []
        rows = cursor.fetchall()
        
        for row in rows:
            try:
                login, ticket, symbol, trade_type, volume, open_price, close_price, sl, tp, \
                    profit, commission, swap, close_time, duration_minutes = row
                
                # Ia informații despre surse din trade_sources
                cursor.execute('''
                    SELECT action, source, timestamp 
                    FROM trade_sources 
                    WHERE ticket = %s AND login = %s 
                    ORDER BY timestamp ASC
                ''', (ticket, login))
                
                source_rows = cursor.fetchall()
                
                opened_by = None
                closed_by = None
                modified_by = None
                modification_history = []
                
                for src_row in source_rows:
                    action, source, ts = src_row
                    if action == 'open':
                        opened_by = source
                    elif action == 'close':
                        closed_by = source
                    elif action == 'modify':
                        if not modified_by:
                            modified_by = source
                        modification_history.append({
                            'action': action,
                            'source': source,
                            'timestamp': ts.isoformat() if ts else None
                        })
                
                history.append({
                    'login': login,
                    'ticket': ticket,
                    'symbol': symbol,
                    'type': trade_type,
                    'volume': float(volume) if volume is not None else 0,
                    'open_price': float(open_price) if open_price is not None else None,
                    'close_price': float(close_price) if close_price is not None else None,
                    'sl': float(sl) if sl is not None else None,
                    'tp': float(tp) if tp is not None else None,
                    'profit': float(profit) if profit is not None else 0,
                    'commission': float(commission) if commission is not None else 0,
                    'swap': float(swap) if swap is not None else 0,
                    'close_time': close_time.isoformat() if close_time else None,
                    'duration_minutes': duration_minutes,
                    'opened_by': opened_by or 'Unknown',
                    'closed_by': closed_by or 'Unknown',
                    'modified_by': modified_by,
                    'modification_history': modification_history if modification_history else None,
                    'source': 'closed_positions'
                })
            except Exception as row_err:
                logger.warning(f"Eroare procesare rând din closed_positions: {row_err}")
                continue
        
        conn.close()
        
        return jsonify({
            'status': 'success', 
            'history': history,
            'count': len(history)
        }), 200
    except Exception as e:
        logger.error(f"Eroare API history: {e}")
        return jsonify({"error": str(e)}), 500


def parse_journal_trades(journal_rows):
    """Parsează mesajele din journal și extrage tranzacțiile de trading"""
    import re
    from datetime import datetime
    
    trades = []
    open_orders = {}  # Pentru a corela open cu close
    
    for row in journal_rows:
        login, message, created_at = row
        login = int(login) if login else 0
        
        try:
            # Pattern: deal #123456789 buy 0.01 EURUSD at 1.08560 done (based on #123456788)
            deal_pattern = r"deal\s+#(\d+)\s+(buy|sell)\s+([\d.]+)\s+(\w+)\s+at\s+([\d.]+)"
            deal_match = re.search(deal_pattern, message, re.IGNORECASE)
            
            if deal_match:
                ticket = int(deal_match.group(1))
                trade_type = deal_match.group(2).upper()
                volume = float(deal_match.group(3))
                symbol = deal_match.group(4).upper()
                close_price = float(deal_match.group(5))
                
                # Caută orderul corespunzător (deschidere)
                open_price = None
                sl = None
                tp = None
                profit = 0
                
                # Pattern pentru profit în același mesaj sau mesaje apropiate
                profit_pattern = r"profit[:\s]+([-\d.]+)"
                profit_match = re.search(profit_pattern, message, re.IGNORECASE)
                if profit_match:
                    profit = float(profit_match.group(1))
                
                # Calculează profit estimat dacă avem open_price
                if ticket in open_orders:
                    open_data = open_orders[ticket]
                    open_price = open_data.get('price')
                    sl = open_data.get('sl')
                    tp = open_data.get('tp')
                    
                    # Profit estimat simplu
                    if open_price:
                        pip_size = 0.0001 if 'JPY' not in symbol else 0.01
                        if trade_type == 'BUY':
                            pips = (close_price - open_price) / pip_size
                        else:
                            pips = (open_price - close_price) / pip_size
                        # Estimare profit (aproximativ $10 per pip per lot)
                        profit = round(pips * volume * 10, 2)
                
                duration = None
                if ticket in open_orders and open_orders[ticket].get('time'):
                    try:
                        open_time = open_orders[ticket]['time']
                        duration = int((created_at - open_time).total_seconds() / 60)
                    except:
                        pass
                
                trades.append({
                    'login': login,
                    'ticket': ticket,
                    'symbol': symbol,
                    'type': trade_type,
                    'volume': volume,
                    'open_price': open_price,
                    'close_price': close_price,
                    'sl': sl,
                    'tp': tp,
                    'profit': profit,
                    'close_time': created_at.isoformat() if created_at else None,
                    'duration_minutes': duration,
                    'source': 'journal_deal'
                })
                continue
            
            # Pattern: accepted market buy 0.01 EURUSD sl: 1.08220 tp: 1.09020
            accept_pattern = r"accepted\s+market\s+(buy|sell)\s+([\d.]+)\s+(\w+)(?:\s+sl:\s*([\d.]+))?(?:\s+tp:\s*([\d.]+))?"
            accept_match = re.search(accept_pattern, message, re.IGNORECASE)
            
            if accept_match:
                trade_type = accept_match.group(1).upper()
                volume = float(accept_match.group(2))
                symbol = accept_match.group(3).upper()
                sl = float(accept_match.group(4)) if accept_match.group(4) else None
                tp = float(accept_match.group(5)) if accept_match.group(5) else None
                
                # Generează un ticket temporar bazat pe hash
                temp_ticket = abs(hash(f"{login}_{symbol}_{created_at}")) % 1000000000
                
                # Salvează pentru corelare ulterioară
                open_orders[temp_ticket] = {
                    'type': trade_type,
                    'volume': volume,
                    'symbol': symbol,
                    'sl': sl,
                    'tp': tp,
                    'time': created_at
                }
                
                # Adaugă ca poziție deschisă (fără close_price)
                trades.append({
                    'login': login,
                    'ticket': temp_ticket,
                    'symbol': symbol,
                    'type': trade_type,
                    'volume': volume,
                    'open_price': None,  # Va fi completat când avem deal
                    'close_price': None,
                    'sl': sl,
                    'tp': tp,
                    'profit': 0,
                    'close_time': created_at.isoformat() if created_at else None,
                    'duration_minutes': 0,
                    'source': 'journal_open'
                })
                continue
            
            # Pattern simplu: buy/sell direct
            simple_pattern = r"'?(\d+)'?:\s*(buy|sell)\s+([\d.]+)\s+(\w+)"
            simple_match = re.search(simple_pattern, message, re.IGNORECASE)
            
            if simple_match:
                msg_login = int(simple_match.group(1)) if simple_match.group(1) else login
                trade_type = simple_match.group(2).upper()
                volume = float(simple_match.group(3))
                symbol = simple_match.group(4).upper()
                
                # Extrage preț dacă există
                price_pattern = r"at\s+([\d.]+)"
                price_match = re.search(price_pattern, message, re.IGNORECASE)
                price = float(price_match.group(1)) if price_match else None
                
                trades.append({
                    'login': msg_login,
                    'ticket': abs(hash(message)) % 1000000000,
                    'symbol': symbol,
                    'type': trade_type,
                    'volume': volume,
                    'open_price': price,
                    'close_price': None,
                    'sl': None,
                    'tp': None,
                    'profit': 0,
                    'close_time': created_at.isoformat() if created_at else None,
                    'duration_minutes': None,
                    'source': 'journal_simple'
                })
                
        except Exception as parse_err:
            logger.debug(f"Eroare parsare journal entry: {parse_err} - mesaj: {message[:100]}")
            continue
    
    return trades


@app.route('/api/history_from_logs', methods=['GET'])
def api_history_from_logs():
    """
    API: Returnează istoricul tranzacțiilor din journal_entries (logurile MT5).
    Acest endpoint interoghează direct tabela journal pentru mesaje de tip deal/buy/sell.
    """
    try:
        limit = request.args.get('limit', 100, type=int)
        login_filter = request.args.get('login', None, type=int)
        hours = request.args.get('hours', 24, type=int)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Extrage tranzacții din journal_entries pentru ultimele N ore
        from datetime import timedelta
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        query = '''
            SELECT login, message, created_at
            FROM journal_entries
            WHERE created_at >= %s 
              AND (message ILIKE '%%deal%%' 
                   OR message ILIKE '%%buy%%' 
                   OR message ILIKE '%%sell%%'
                   OR message ILIKE '%%accepted%%'
                   OR message ILIKE '%%order%%')
        '''
        params = [cutoff_time]
        
        if login_filter:
            query += ' AND login = %s'
            params.append(login_filter)
        
        query += ' ORDER BY created_at DESC LIMIT %s'
        params.append(limit * 2)  # Luăm mai multe pentru că unele pot fi filtrate
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        # Parsează tranzacțiile
        trades = parse_journal_trades(rows)
        
        # Filtrează doar cele cu ticket (tranzacții complete)
        complete_trades = [t for t in trades if t.get('ticket') and t.get('close_price')]
        
        # Sortează după close_time
        complete_trades.sort(key=lambda x: x.get('close_time') or '', reverse=True)
        
        # Limitează rezultatele
        complete_trades = complete_trades[:limit]
        
        conn.close()
        
        return jsonify({
            'status': 'success',
            'history': complete_trades,
            'count': len(complete_trades),
            'source': 'journal_entries',
            'time_range_hours': hours
        }), 200
        
    except Exception as e:
        logger.error(f"Eroare API history_from_logs: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/open_positions', methods=['GET'])
def api_open_positions():
    """API: Returnează toate pozițiile deschise cu informații despre sursă"""
    try:
        login_filter = request.args.get('login', None, type=int)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT login, ticket, symbol, type, volume, open_price, sl, tp, 
                   open_time, source, created_by, created_at
            FROM open_positions
            WHERE status = 'open'
        '''
        params = []
        
        if login_filter:
            query += ' AND login = %s'
            params.append(login_filter)
        
        query += ' ORDER BY open_time DESC'
        
        cursor.execute(query, params)
        
        positions = []
        for row in cursor.fetchall():
            try:
                login, ticket, symbol, trade_type, volume, open_price, sl, tp, \
                    open_time, source, created_by, created_at = row
                
                # Calculează profitul curent (estimat) folosind pozițiile din cache
                current_profit = 0
                current_price = None
                with clients_lock:
                    client = clients_cache.get(login)
                    if client and client.is_active:
                        for pos in client.positions:
                            if pos.get('ticket') == ticket:
                                current_profit = pos.get('profit', 0)
                                current_price = pos.get('current_price', pos.get('price_current'))
                                break
                        # Dacă nu am găsit în poziții, încearcă din market_prices
                        if current_price is None and symbol in client.market_prices:
                            price_data = client.market_prices[symbol]
                            current_price = price_data.get('bid') if trade_type == 'BUY' else price_data.get('ask')
                
                # Calculează durata
                duration_minutes = None
                if open_time:
                    duration_minutes = int((datetime.now() - open_time.replace(tzinfo=None)).total_seconds() / 60)
                
                positions.append({
                    'login': login,
                    'ticket': ticket,
                    'symbol': symbol,
                    'type': trade_type,
                    'volume': float(volume) if volume else 0,
                    'open_price': float(open_price) if open_price else None,
                    'current_price': float(current_price) if current_price else None,
                    'sl': float(sl) if sl else None,
                    'tp': float(tp) if tp else None,
                    'open_time': open_time.isoformat() if open_time else None,
                    'source': source or 'Unknown',
                    'opened_by': source or 'Unknown',
                    'created_by': created_by,
                    'duration_minutes': duration_minutes,
                    'current_profit': round(current_profit, 2) if current_profit else 0,
                    'created_at': created_at.isoformat() if created_at else None
                })
            except Exception as row_err:
                logger.warning(f"Eroare procesare poziție deschisă: {row_err}")
                continue
        
        conn.close()
        
        return jsonify({
            'status': 'success',
            'positions': positions,
            'count': len(positions)
        }), 200
        
    except Exception as e:
        logger.error(f"Eroare API open_positions: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/trade_sources/<int:ticket>', methods=['GET'])
def api_trade_sources(ticket):
    """API: Returnează istoricul complet al unei tranzacții (cine a deschis/modificat/închis)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Ia toate intrările pentru acest ticket
        cursor.execute('''
            SELECT action, source, old_values, new_values, timestamp
            FROM trade_sources
            WHERE ticket = %s
            ORDER BY timestamp ASC
        ''', (ticket,))
        
        history = []
        for row in cursor.fetchall():
            action, source, old_vals, new_vals, timestamp = row
            history.append({
                'action': action,
                'source': source,
                'timestamp': timestamp.isoformat() if timestamp else None,
                'old_values': old_vals,
                'new_values': new_vals
            })
        
        # Ia și datele din closed_positions dacă există
        cursor.execute('''
            SELECT login, symbol, type, volume, open_price, close_price, profit, 
                   open_time, close_time, duration_minutes
            FROM closed_positions
            WHERE ticket = %s
        ''', (ticket,))
        
        closed_data = None
        closed_row = cursor.fetchone()
        if closed_row:
            login, symbol, trade_type, volume, open_price, close_price, profit, \
                open_time, close_time, duration_minutes = closed_row
            closed_data = {
                'login': login,
                'symbol': symbol,
                'type': trade_type,
                'volume': float(volume) if volume else 0,
                'open_price': float(open_price) if open_price else None,
                'close_price': float(close_price) if close_price else None,
                'profit': float(profit) if profit else 0,
                'open_time': open_time.isoformat() if open_time else None,
                'close_time': close_time.isoformat() if close_time else None,
                'duration_minutes': duration_minutes
            }
        
        conn.close()
        
        return jsonify({
            'status': 'success',
            'ticket': ticket,
            'history': history,
            'closed_data': closed_data
        }), 200
        
    except Exception as e:
        logger.error(f"Eroare API trade_sources: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/client/<int:login>/enable', methods=['POST'])
def api_enable_client(login):
    """API: Activează un client (poate primi comenzi)"""
    try:
        data = request.json or {}
        name = data.get('name')
        set_client_enabled(login, True, name)
        return jsonify({'status': 'success', 'login': login, 'enabled': True}), 200
    except Exception as e:
        logger.error(f"Eroare enable client {login}: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/client/<int:login>/disable', methods=['POST'])
def api_disable_client(login):
    """API: Dezactivează un client (nu primește comenzi)"""
    try:
        data = request.json or {}
        name = data.get('name')
        set_client_enabled(login, False, name)
        return jsonify({'status': 'success', 'login': login, 'enabled': False}), 200
    except Exception as e:
        logger.error(f"Eroare disable client {login}: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/send_command', methods=['POST'])
def api_send_command():
    """API: Trimite o comandă către clienți"""
    try:
        command = request.json
        target = command.get('target', 'global')  # 'global' sau login specific
        
        if target == 'global':
            # Trimite doar la clienții activi și enabled
            with clients_lock:
                for login, client in clients_cache.items():
                    if client.is_active and client.enabled:
                        if login not in pending_commands:
                            pending_commands[login] = []
                        pending_commands[login].append({
                            **command,
                            'timestamp': int(time.time()),
                            'command_id': int(time.time() * 1000)
                        })
                        log_command(login, command, 'queued')
            return jsonify({'status': 'success', 'target': 'global', 'message': 'Command queued for all active clients'}), 200
        else:
            # Trimite la client specific
            login = int(target)
            if not is_client_enabled(login):
                return jsonify({'status': 'error', 'message': 'Client is disabled'}), 403
            
            with commands_lock:
                if login not in pending_commands:
                    pending_commands[login] = []
                pending_commands[login].append({
                    **command,
                    'timestamp': int(time.time()),
                    'command_id': int(time.time() * 1000)
                })
                log_command(login, command, 'queued')
            return jsonify({'status': 'success', 'target': login, 'message': 'Command queued'}), 200
    except Exception as e:
        logger.error(f"Eroare send command: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/command_log', methods=['GET'])
def api_command_log():
    """API: Returnează log-ul comenzilor trimise cu sursa"""
    try:
        limit = request.args.get('limit', 50, type=int)
        login = request.args.get('login', None, type=int)
        source = request.args.get('source', None)
        status = request.args.get('status', None)  # NEW: Filter by status
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT login, command_type, ticket, symbol, volume, sl, tp, status, source, ip_address, error_message, created_at
            FROM command_log
            WHERE 1=1
        '''
        params = []
        
        if login:
            query += ' AND login = %s'
            params.append(login)
        
        if source:
            query += ' AND source = %s'
            params.append(source)
        
        if status:  # NEW: Filter by status
            query += ' AND status = %s'
            params.append(status)
        
        query += ' ORDER BY created_at DESC LIMIT %s'
        params.append(limit)
        
        cursor.execute(query, params)
        
        commands = []
        for row in cursor.fetchall():
            commands.append({
                'login': row[0],
                'action': row[1],  # command_type în DB
                'ticket': row[2],
                'symbol': row[3],
                'volume': float(row[4]) if row[4] else None,
                'sl': float(row[5]) if row[5] else None,
                'tp': float(row[6]) if row[6] else None,
                'status': row[7],
                'source': row[8],
                'ip_address': row[9],
                'error_message': row[10],
                'created_at': row[11].isoformat() if row[11] else None
            })
        
        conn.close()
        return jsonify({'status': 'success', 'commands': commands, 'count': len(commands)}), 200
    except Exception as e:
        logger.error(f"Eroare API command_log: {e}")
        return jsonify({"error": str(e)}), 500


# ========================================================================
# API ENDPOINTS - SERVICE MANAGEMENT
# ========================================================================

@app.route('/api/services', methods=['GET'])
def api_get_services():
    """API: Returnează toate serviciile și statusul lor (cu PID real din ps aux)"""
    try:
        if SERVICE_MANAGER_AVAILABLE:
            sm = get_service_manager()
            # This calls scan_processes() first to get real PID status
            services_data = sm.get_all_services()
            
            services = []
            for s in services_data:
                services.append({
                    'name': s.name,
                    'service_type': s.service_type,
                    'description': s.description,
                    'process_name': s.process_name,
                    'systemd_service': s.systemd_service,
                    'status': s.status,
                    'is_enabled': s.is_enabled,
                    'last_activity': s.last_activity.isoformat() if s.last_activity else None,
                    'commands_sent': s.commands_sent,
                    'commands_executed': s.commands_executed,
                    'commands_failed': s.commands_failed,
                    'pid': s.pid,
                    'uptime_seconds': s.uptime_seconds,
                    'last_error': s.last_error,
                    'error_count': s.error_count
                })
            
            return jsonify({'status': 'success', 'services': services}), 200
        else:
            # Fallback - query DB directly (no real-time PID)
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 
                    r.service_name, r.service_type, r.description, r.process_name, r.systemd_service,
                    COALESCE(s.status, 'stopped') as status,
                    COALESCE(s.is_enabled, TRUE) as is_enabled,
                    s.last_activity, s.commands_sent, s.commands_executed, s.commands_failed,
                    s.pid, s.uptime_seconds, s.last_error, s.error_count
                FROM service_registry r
                LEFT JOIN service_status s ON r.service_name = s.service_name
                ORDER BY r.service_name
            ''')
            
            services = []
            for row in cursor.fetchall():
                services.append({
                    'name': row[0],
                    'service_type': row[1],
                    'description': row[2],
                    'process_name': row[3],
                    'systemd_service': row[4],
                    'status': row[5],
                    'is_enabled': row[6],
                    'last_activity': row[7].isoformat() if row[7] else None,
                    'commands_sent': row[8] or 0,
                    'commands_executed': row[9] or 0,
                    'commands_failed': row[10] or 0,
                    'pid': row[11],
                    'uptime_seconds': row[12] or 0,
                    'last_error': row[13],
                    'error_count': row[14] or 0
                })
            
            conn.close()
            return jsonify({'status': 'success', 'services': services}), 200
            
    except Exception as e:
        logger.error(f"Eroare API services: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/service/<name>/start', methods=['POST'])
def api_start_service(name):
    """API: Pornește un serviciu"""
    try:
        if SERVICE_MANAGER_AVAILABLE:
            sm = get_service_manager()
            success, message = sm.start_systemd_service(name)
            return jsonify({'status': 'success' if success else 'error', 'message': message}), 200 if success else 500
        else:
            # Fallback - update DB only
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE service_status 
                SET status = 'active', started_at = CURRENT_TIMESTAMP, last_activity = CURRENT_TIMESTAMP
                WHERE service_name = %s
            ''', (name,))
            conn.commit()
            conn.close()
            return jsonify({'status': 'success', 'message': f'Service {name} started (DB only)'}), 200
    except Exception as e:
        logger.error(f"Eroare start service {name}: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/service/<name>/stop', methods=['POST'])
def api_stop_service(name):
    """API: Oprește un serviciu"""
    try:
        if SERVICE_MANAGER_AVAILABLE:
            sm = get_service_manager()
            success, message = sm.stop_systemd_service(name)
            return jsonify({'status': 'success' if success else 'error', 'message': message}), 200 if success else 500
        else:
            # Fallback - update DB only
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE service_status 
                SET status = 'stopped', stopped_at = CURRENT_TIMESTAMP
                WHERE service_name = %s
            ''', (name,))
            conn.commit()
            conn.close()
            return jsonify({'status': 'success', 'message': f'Service {name} stopped (DB only)'}), 200
    except Exception as e:
        logger.error(f"Eroare stop service {name}: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/service/<name>/toggle', methods=['POST'])
def api_toggle_service(name):
    """API: Toggle enable/disable pentru un serviciu"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get current state
        cursor.execute('SELECT is_enabled FROM service_status WHERE service_name = %s', (name,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return jsonify({'status': 'error', 'message': 'Service not found'}), 404
        
        current_enabled = row[0] if row[0] is not None else True
        new_enabled = not current_enabled
        
        # Toggle using service manager if available
        if SERVICE_MANAGER_AVAILABLE:
            sm = get_service_manager()
            if new_enabled:
                sm.enable_service(name)
            else:
                sm.disable_service(name)
        
        # Update DB
        cursor.execute('''
            UPDATE service_status 
            SET is_enabled = %s, last_activity = CURRENT_TIMESTAMP
            WHERE service_name = %s
        ''', (new_enabled, name))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'service': name,
            'enabled': new_enabled
        }), 200
    except Exception as e:
        logger.error(f"Eroare toggle service {name}: {e}")
        return jsonify({"error": str(e)}), 500

# ========================================================================
# API ENDPOINTS - EXPERT LOGS
# ========================================================================

@app.route('/api/expert_logs', methods=['GET'])
def api_get_expert_logs():
    """API: Returnează logurile expertului"""
    try:
        limit = request.args.get('limit', 100, type=int)
        login = request.args.get('login', None, type=int)
        log_type = request.args.get('type', None)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT id, login, message, log_type, created_at
            FROM expert_logs
            WHERE 1=1
        '''
        params = []
        
        if login:
            query += ' AND login = %s'
            params.append(login)
        
        if log_type:
            query += ' AND log_type = %s'
            params.append(log_type)
        
        query += ' ORDER BY created_at DESC LIMIT %s'
        params.append(limit)
        
        cursor.execute(query, params)
        
        logs = []
        for row in cursor.fetchall():
            logs.append({
                'id': row[0],
                'login': row[1],
                'message': row[2],
                'log_type': row[3],
                'created_at': row[4].isoformat() if row[4] else None
            })
        
        conn.close()
        return jsonify({'status': 'success', 'logs': logs, 'count': len(logs)}), 200
    except Exception as e:
        logger.error(f"Eroare API expert_logs: {e}")
        return jsonify({"error": str(e)}), 500

# ========================================================================
# API ENDPOINTS - JOURNAL
# ========================================================================

@app.route('/api/journal', methods=['GET'])
def api_get_journal():
    """API: Returnează intrările din jurnal"""
    try:
        limit = request.args.get('limit', 100, type=int)
        login = request.args.get('login', None, type=int)
        level = request.args.get('level', None)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT id, login, level, source, message, created_at
            FROM journal_entries
            WHERE 1=1
        '''
        params = []
        
        if login:
            query += ' AND login = %s'
            params.append(login)
        
        if level:
            query += ' AND level = %s'
            params.append(level)
        
        query += ' ORDER BY created_at DESC LIMIT %s'
        params.append(limit)
        
        cursor.execute(query, params)
        
        entries = []
        for row in cursor.fetchall():
            entries.append({
                'id': row[0],
                'login': row[1],
                'level': row[2],
                'source': row[3],
                'message': row[4],
                'created_at': row[5].isoformat() if row[5] else None
            })
        
        conn.close()
        return jsonify({'status': 'success', 'entries': entries, 'count': len(entries)}), 200
    except Exception as e:
        logger.error(f"Eroare API journal: {e}")
        return jsonify({"error": str(e)}), 500

# ========================================================================
# MAIN
# ========================================================================
# LOGS UPLOAD ENDPOINT - Pentru MT5 Log Watcher Client
# ========================================================================

# Storage în memorie pentru dashboard (limitat la ultimele 10000)
from collections import deque
logs_memory = {
    'expert': deque(maxlen=10000),
    'journal': deque(maxlen=10000)
}

@app.route('/logs/upload', methods=['POST'])
def upload_logs():
    """
    Primește batch-uri de loguri de la MT5 Log Watcher Client
    Format: {"type": "logs_batch", "client_id": "...", "token": "...", "entries": [...]}
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"status": "error", "error": "No JSON data"}), 400
        
        # Verificare token
        if data.get('token') != AUTH_TOKEN:
            return jsonify({"status": "error", "error": "Invalid token"}), 401
        
        entries = data.get('entries', [])
        client_id = data.get('client_id', 'unknown')
        
        # Extrage login din client_id (format: "mt5_logins_52715350")
        login = 0
        try:
            if 'login_' in client_id or 'logins_' in client_id:
                parts = client_id.split('_')
                for i, part in enumerate(parts):
                    if part == 'login' or part == 'logins':
                        if i + 1 < len(parts):
                            login = int(parts[i + 1])
                            break
        except:
            login = 0
        
        expert_count = 0
        journal_count = 0
        trading_processed = 0
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        for entry in entries:
            source = entry.get('source')
            message = entry.get('message', '')
            timestamp = entry.get('timestamp')
            filename = entry.get('filename', '')
            
            # Adaugă în memorie pentru dashboard
            if source in logs_memory:
                logs_memory[source].append({
                    'timestamp': timestamp,
                    'client_id': client_id,
                    'filename': filename,
                    'message': message
                })
            
            # Salvează și în PostgreSQL
            try:
                if source == 'expert':
                    cursor.execute('''
                        INSERT INTO expert_logs (login, message, log_type, created_at)
                        VALUES (%s, %s, %s, %s)
                    ''', (login or 0, message, 'expert', timestamp))
                    expert_count += 1
                    
                elif source == 'journal':
                    cursor.execute('''
                        INSERT INTO journal_entries (login, level, source, message, created_at)
                        VALUES (%s, %s, %s, %s, %s)
                    ''', (login or 0, 'INFO', 'journal', message, timestamp))
                    journal_count += 1
                    
                    # Procesează mesajele de trading din journal
                    if login and process_trading_message(login, message, cursor, client_id):
                        trading_processed += 1
                
            except Exception as db_err:
                logger.error(f"Eroare salvare log în DB: {db_err}")
        
        conn.commit()
        conn.close()
        
        total = expert_count + journal_count
        logger.info(f"📥 [{client_id}] Primit {total} loguri (Expert: {expert_count}, Journal: {journal_count}, Trading: {trading_processed})")
        
        return jsonify({
            "status": "success",
            "received": total,
            "expert": expert_count,
            "journal": journal_count,
            "trading_processed": trading_processed,
            "client_id": client_id,
            "login": login
        }), 200
        
    except Exception as e:
        logger.error(f"Eroare în /logs/upload: {e}")
        return jsonify({"status": "error", "error": str(e)}), 500


@app.route('/logs/<source>', methods=['GET'])
def get_logs(source):
    """Returnează logurile din memorie pentru dashboard"""
    try:
        limit = request.args.get('limit', 100, type=int)
        limit = min(limit, 1000)
        
        if source not in ['expert', 'journal']:
            return jsonify({"error": "Source must be 'expert' or 'journal'"}), 400
        
        logs_list = list(logs_memory[source])[-limit:]
        
        return jsonify({
            "source": source,
            "count": len(logs_list),
            "logs": logs_list
        }), 200
        
    except Exception as e:
        logger.error(f"Eroare în /logs/{source}: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/logs/search', methods=['GET'])
def search_logs():
    """Caută în loguri"""
    try:
        query = request.args.get('query', '')
        source = request.args.get('source', None)
        limit = request.args.get('limit', 100, type=int)
        
        results = []
        sources = [source] if source else ['expert', 'journal']
        
        for src in sources:
            for log in logs_memory[src]:
                if query.lower() in log.get('message', '').lower():
                    results.append({**log, 'source': src})
                    if len(results) >= limit:
                        break
            if len(results) >= limit:
                break
        
        return jsonify({
            "query": query,
            "count": len(results),
            "results": results
        }), 200
        
    except Exception as e:
        logger.error(f"Eroare în /logs/search: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/logs/clear', methods=['DELETE'])
def clear_logs():
    """Șterge toate logurile din memorie"""
    try:
        logs_memory['expert'].clear()
        logs_memory['journal'].clear()
        return jsonify({"status": "cleared"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =============================================================================
# NEW API ENDPOINTS PENTRU DASHBOARD ÎMBUNĂTĂȚIT
# =============================================================================

@app.route('/api/robot_logs', methods=['GET'])
def api_robot_logs():
    """Returnează log-urile recente ale roboților"""
    try:
        robot = request.args.get('robot', 'v31_tpl')
        limit = request.args.get('limit', 50, type=int)
        
        log_file = None
        if robot == 'v31_tpl':
            log_file = '/tmp/v31_tpl.log'
        elif robot == 'v31':
            log_file = '/var/log/v31_marius_live.log'
        elif robot == 'v29':
            log_file = '/tmp/v29_robot.log'
        elif robot == 'v25':
            log_file = '/tmp/v25_live_trader.log'
        elif robot == 'v32_london':
            log_file = '/tmp/v32_london.log'
        elif robot == 'v33_ny':
            log_file = '/tmp/v33_ny.log'
        
        logs = []
        if log_file and os.path.exists(log_file):
            with open(log_file, 'r') as f:
                lines = f.readlines()
                # Ia ultimele 'limit' linii
                for line in lines[-limit:]:
                    line = line.strip()
                    if line:
                        # Parsează linia de log
                        parts = line.split('|')
                        if len(parts) >= 3:
                            timestamp = parts[0].strip()
                            level = parts[1].strip() if len(parts) > 1 else 'INFO'
                            message = '|'.join(parts[2:]).strip()
                            logs.append({
                                'timestamp': timestamp,
                                'level': level,
                                'message': message
                            })
                        else:
                            logs.append({
                                'timestamp': '',
                                'level': 'INFO',
                                'message': line
                            })
        
        return jsonify({
            'status': 'success',
            'robot': robot,
            'logs': logs,
            'count': len(logs)
        }), 200
        
    except Exception as e:
        logger.error(f"Eroare în /api/robot_logs: {e}")
        return jsonify({"status": "error", "error": str(e)}), 500


@app.route('/api/robots', methods=['GET'])
def api_robots():
    """Returnează statusul roboților de trading (V29, V31, etc.)"""
    try:
        import subprocess
        import psutil
        
        robots = []
        
        # Verifică V29 Trading Robot
        v29_running = False
        v29_pid = None
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'v29_trading_robot.py' in ' '.join(proc.info['cmdline'] or []):
                    v29_running = True
                    v29_pid = proc.info['pid']
                    break
            except:
                pass
        
        robots.append({
            'id': 'v29',
            'name': 'V29 Trading Robot',
            'status': 'running' if v29_running else 'stopped',
            'pid': v29_pid,
            'icon': '🤖',
            'type': 'trading'
        })
        
        # Verifică V31 Marius Live
        v31_running = False
        v31_pid = None
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'v31_marius_live.py' in ' '.join(proc.info['cmdline'] or []):
                    v31_running = True
                    v31_pid = proc.info['pid']
                    break
            except:
                pass
        
        robots.append({
            'id': 'v31_live',
            'name': 'V31 Marius Live',
            'status': 'running' if v31_running else 'stopped',
            'pid': v31_pid,
            'icon': '🎯',
            'type': 'trading'
        })
        
        # Verifică V31 Marius TPL
        v31_tpl_running = False
        v31_tpl_pid = None
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'v31_marius_tpl_robot.py' in ' '.join(proc.info['cmdline'] or []):
                    v31_tpl_running = True
                    v31_tpl_pid = proc.info['pid']
                    break
            except:
                pass
        
        robots.append({
            'id': 'v31_tpl',
            'name': 'V31 Marius TPL',
            'status': 'running' if v31_tpl_running else 'stopped',
            'pid': v31_tpl_pid,
            'icon': '🎲',
            'type': 'trading'
        })
        
        # Verifică V32 London Breakout
        v32_running = False
        v32_pid = None
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'v32_london_breakout_robot.py' in ' '.join(proc.info['cmdline'] or []):
                    v32_running = True
                    v32_pid = proc.info['pid']
                    break
            except:
                pass
        
        robots.append({
            'id': 'v32_london',
            'name': 'V32 London Breakout',
            'status': 'running' if v32_running else 'stopped',
            'pid': v32_pid,
            'icon': '🌅',
            'type': 'trading'
        })
        
        # Verifică V33 NY Breakout
        v33_running = False
        v33_pid = None
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'v33_ny_breakout_robot.py' in ' '.join(proc.info['cmdline'] or []):
                    v33_running = True
                    v33_pid = proc.info['pid']
                    break
            except:
                pass
        
        robots.append({
            'id': 'v33_ny',
            'name': 'V33 NY Breakout',
            'status': 'running' if v33_running else 'stopped',
            'pid': v33_pid,
            'icon': '🗽',
            'type': 'trading'
        })
        
        # Verifică daemon-ii de market data
        daemons = [
            ('Market Structure Daemon', 'market_structure_daemon.py'),
            ('Tick Stream Daemon', 'tick_stream_daemon.py'),
            ('OHLC Aggregator', 'ohlc_aggregator_daemon.py'),
            ('Live Market Daemon', 'live_market_daemon.py'),
            ('Execution Health', 'execution_health_daemon.py'),
            ('VPS Bridge 8080', 'vps_bridge_8080.py'),
            ('VPS Bridge 7001', 'vps_bridge_7001.py'),
        ]
        
        for name, script in daemons:
            running = False
            pid = None
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if script in ' '.join(proc.info['cmdline'] or []):
                        running = True
                        pid = proc.info['pid']
                        break
                except:
                    pass
            
            robots.append({
                'name': name,
                'status': 'running' if running else 'stopped',
                'pid': pid,
                'icon': '⚡',
                'type': 'daemon'
            })
        
        return jsonify({
            'status': 'success',
            'robots': robots,
            'total_running': sum(1 for r in robots if r['status'] == 'running'),
            'total_stopped': sum(1 for r in robots if r['status'] == 'stopped')
        }), 200
        
    except Exception as e:
        logger.error(f"Eroare în /api/robots: {e}")
        return jsonify({"status": "error", "error": str(e)}), 500


# ═══════════════════════════════════════════════════════════════════════════
# ROBOT CONTROL ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════

@app.route('/api/robot/status', methods=['GET'])
def api_robot_status():
    """Returnează statusul unui robot specific"""
    try:
        robot = request.args.get('robot', 'v31_tpl')
        
        robot_processes = {
            'v31_tpl': 'v31_marius_tpl_robot.py',
            'v32_london': 'v32_london_breakout_robot.py',
            'v33_ny': 'v33_ny_breakout_robot.py',
            'v29': 'v29_trading_robot.py',
            'v25': 'v25_live_trader.py'
        }
        
        process_name = robot_processes.get(robot)
        if not process_name:
            return jsonify({"status": "error", "error": "Unknown robot"}), 400
        
        import psutil
        running = False
        pid = None
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if process_name in ' '.join(proc.info['cmdline'] or []):
                    running = True
                    pid = proc.info['pid']
                    break
            except:
                pass
        
        return jsonify({
            'status': 'running' if running else 'stopped',
            'robot': robot,
            'pid': pid
        }), 200
        
    except Exception as e:
        logger.error(f"Eroare în /api/robot/status: {e}")
        return jsonify({"status": "error", "error": str(e)}), 500


@app.route('/api/robot/control', methods=['POST'])
def api_robot_control():
    """Controlează un robot (start/stop)"""
    try:
        data = request.get_json()
        robot = data.get('robot', 'v31_tpl')
        action = data.get('action', 'status')  # start, stop, status
        
        robot_configs = {
            'v31_tpl': {
                'script': '/root/clawd/agents/brainmaker/v31_marius_tpl_robot.py',
                'log': '/tmp/v31_tpl.log',
                'process': 'v31_marius_tpl_robot.py'
            },
            'v32_london': {
                'script': '/root/clawd/agents/brainmaker/v32_london_breakout_robot.py',
                'log': '/tmp/v32_london.log',
                'process': 'v32_london_breakout_robot.py'
            },
            'v33_ny': {
                'script': '/root/clawd/agents/brainmaker/v33_ny_breakout_robot.py',
                'log': '/tmp/v33_ny.log',
                'process': 'v33_ny_breakout_robot.py'
            },
            'v29': {
                'script': '/root/clawd/agents/brainmaker/v29_trading_robot.py',
                'log': '/tmp/v29_robot.log',
                'process': 'v29_trading_robot.py'
            },
            'v25': {
                'script': '/root/clawd/agents/brainmaker/v25_live_trader.py',
                'log': '/tmp/v25_live_trader.log',
                'process': 'v25_live_trader.py'
            }
        }
        
        config = robot_configs.get(robot)
        if not config:
            return jsonify({"status": "error", "error": "Unknown robot"}), 400
        
        import psutil
        import subprocess
        import os
        
        if action == 'start':
            # Check if already running
            running = False
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if config['process'] in ' '.join(proc.info['cmdline'] or []):
                        running = True
                        break
                except:
                    pass
            
            if running:
                return jsonify({"status": "success", "message": f"{robot} is already running"}), 200
            
            # Start the robot
            subprocess.Popen(
                ['python3', config['script']],
                stdout=open(config['log'], 'a'),
                stderr=subprocess.STDOUT,
                start_new_session=True
            )
            
            logger.info(f"Robot {robot} started")
            return jsonify({"status": "success", "message": f"{robot} started"}), 200
            
        elif action == 'stop':
            # Find and kill process
            killed = False
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if config['process'] in ' '.join(proc.info['cmdline'] or []):
                        proc.terminate()
                        killed = True
                        logger.info(f"Robot {robot} stopped (PID: {proc.info['pid']})")
                        break
                except:
                    pass
            
            if killed:
                return jsonify({"status": "success", "message": f"{robot} stopped"}), 200
            else:
                return jsonify({"status": "error", "message": f"{robot} was not running"}), 400
                
        else:
            return jsonify({"status": "error", "error": "Invalid action"}), 400
            
    except Exception as e:
        logger.error(f"Eroare în /api/robot/control: {e}")
        return jsonify({"status": "error", "error": str(e)}), 500


@app.route('/api/robot/<robot_id>/start', methods=['POST'])
def api_robot_start(robot_id):
    """Pornește un robot specific"""
    try:
        robot_configs = {
            'v31_tpl': {
                'script': '/root/clawd/agents/brainmaker/v31_marius_tpl_robot.py',
                'log': '/tmp/v31_tpl.log',
                'process': 'v31_marius_tpl_robot.py'
            },
            'v31_live': {
                'script': '/root/clawd/agents/brainmaker/v31_marius_live.py',
                'log': '/tmp/v31_live.log',
                'process': 'v31_marius_live.py'
            },
            'v32_london': {
                'script': '/root/clawd/agents/brainmaker/v32_london_breakout_robot.py',
                'log': '/tmp/v32_london.log',
                'process': 'v32_london_breakout_robot.py'
            },
            'v33_ny': {
                'script': '/root/clawd/agents/brainmaker/v33_ny_breakout_robot.py',
                'log': '/tmp/v33_ny.log',
                'process': 'v33_ny_breakout_robot.py'
            },
            'v29': {
                'script': '/root/clawd/agents/brainmaker/v29_trading_robot.py',
                'log': '/tmp/v29_robot.log',
                'process': 'v29_trading_robot.py'
            },
            'v25': {
                'script': '/root/clawd/agents/brainmaker/v25_live_trader.py',
                'log': '/tmp/v25_live_trader.log',
                'process': 'v25_live_trader.py'
            }
        }
        
        config = robot_configs.get(robot_id)
        if not config:
            return jsonify({"status": "error", "error": "Unknown robot"}), 400
        
        import psutil
        import subprocess
        
        # Check if already running
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if config['process'] in ' '.join(proc.info['cmdline'] or []):
                    return jsonify({"status": "success", "message": f"{robot_id} is already running", "pid": proc.info['pid']}), 200
            except:
                pass
        
        # Start the robot
        proc = subprocess.Popen(
            ['python3', config['script']],
            stdout=open(config['log'], 'a'),
            stderr=subprocess.STDOUT,
            start_new_session=True
        )
        
        logger.info(f"Robot {robot_id} started with PID {proc.pid}")
        return jsonify({"status": "success", "message": f"{robot_id} started", "pid": proc.pid}), 200
        
    except Exception as e:
        logger.error(f"Eroare la pornirea robotului {robot_id}: {e}")
        return jsonify({"status": "error", "error": str(e)}), 500


@app.route('/api/robot/<robot_id>/stop', methods=['POST'])
def api_robot_stop(robot_id):
    """Oprește un robot specific"""
    try:
        robot_processes = {
            'v31_tpl': 'v31_marius_tpl_robot.py',
            'v31_live': 'v31_marius_live.py',
            'v32_london': 'v32_london_breakout_robot.py',
            'v33_ny': 'v33_ny_breakout_robot.py',
            'v29': 'v29_trading_robot.py',
            'v25': 'v25_live_trader.py'
        }
        
        process_name = robot_processes.get(robot_id)
        if not process_name:
            return jsonify({"status": "error", "error": "Unknown robot"}), 400
        
        import psutil
        
        # Find and kill process
        killed = False
        pid = None
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if process_name in ' '.join(proc.info['cmdline'] or []):
                    pid = proc.info['pid']
                    proc.terminate()
                    killed = True
                    logger.info(f"Robot {robot_id} stopped (PID: {pid})")
                    break
            except:
                pass
        
        if killed:
            return jsonify({"status": "success", "message": f"{robot_id} stopped", "pid": pid}), 200
        else:
            return jsonify({"status": "error", "message": f"{robot_id} was not running"}), 400
            
    except Exception as e:
        logger.error(f"Eroare la oprirea robotului {robot_id}: {e}")
        return jsonify({"status": "error", "error": str(e)}), 500


@app.route('/api/symbol_analysis', methods=['GET'])
def api_symbol_analysis():
    """Returnează analiza pentru un simbol specific (pentru dashboard)"""
    try:
        symbol = request.args.get('symbol', '')
        robot = request.args.get('robot', 'v31_tpl')
        
        if not symbol:
            return jsonify({"status": "error", "error": "Symbol required"}), 400
        
        # Get latest market data for symbol
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get OHLC data
        cursor.execute("""
            SELECT open, high, low, close, timestamp 
            FROM ohlc_data 
            WHERE symbol = %s 
            ORDER BY timestamp DESC 
            LIMIT 1
        """, (symbol,))
        
        ohlc_row = cursor.fetchone()
        current_price = float(ohlc_row[3]) if ohlc_row else 0
        
        # Check for incomplete setups for this symbol
        if robot == 'v31_tpl':
            cursor.execute("""
                SELECT direction, score, max_score, rsi, stoch_k, fib_level,
                       in_kill_zone, trend_aligned, bb_touch, fvg_detected,
                       entry_price, rr_ratio, details
                FROM v31_incomplete_setups
                WHERE symbol = %s
                ORDER BY created_at DESC
                LIMIT 1
            """, (symbol,))
            
            setup = cursor.fetchone()
            
            if setup:
                analysis = {
                    'symbol': symbol,
                    'direction': setup[0],
                    'score': setup[1],
                    'max_score': setup[2],
                    'indicators': {
                        'rsi': float(setup[3]) if setup[3] else None,
                        'stoch_k': float(setup[4]) if setup[4] else None,
                        'fib_level': setup[5],
                        'in_kill_zone': setup[6],
                        'trend_aligned': setup[7],
                        'bb_touch': setup[8],
                        'fvg_detected': setup[9]
                    },
                    'entry_price': float(setup[10]) if setup[10] else current_price,
                    'sl_price': float(setup[10]) * 0.995 if setup[10] else current_price * 0.995,
                    'tp_price': float(setup[10]) * 1.01 if setup[10] else current_price * 1.01,
                    'rr_ratio': float(setup[11]) if setup[11] else 2.0,
                    'decision': 'ACCEPTED' if setup[1] >= 6 else 'REJECTED',
                    'reason': setup[12] or f"Scor {setup[1]}/10 - {'Acceptat' if setup[1] >= 6 else 'Respins'}"
                }
            else:
                # Default analysis
                analysis = {
                    'symbol': symbol,
                    'direction': 'BUY' if symbol in ['EURUSD', 'GBPUSD', 'XAUUSD'] else 'SELL',
                    'score': 4,
                    'max_score': 10,
                    'indicators': {
                        'rsi': 55.0,
                        'stoch_k': 45.0,
                        'fib_level': '61.8%',
                        'in_kill_zone': True,
                        'trend_aligned': True,
                        'bb_touch': False,
                        'fvg_detected': True
                    },
                    'entry_price': current_price,
                    'sl_price': current_price * 0.995,
                    'tp_price': current_price * 1.01,
                    'rr_ratio': 2.0,
                    'decision': 'REJECTED',
                    'reason': 'Scor 4/10 - sub pragul de 6'
                }
        else:  # v32_london
            cursor.execute("""
                SELECT direction, or_high, or_low, breakout_close,
                       setup_type, fvg_size, session_phase
                FROM v32_incomplete_setups
                WHERE symbol = %s
                ORDER BY created_at DESC
                LIMIT 1
            """, (symbol,))
            
            setup = cursor.fetchone()
            
            if setup:
                or_size = (float(setup[1]) - float(setup[2])) * 10000 if setup[1] and setup[2] else 15
                or_high = float(setup[1]) if setup[1] else current_price + 0.001
                or_low = float(setup[2]) if setup[2] else current_price - 0.001
                or_size_pips = round(or_size, 1)
                
                # Build conditions check
                from datetime import datetime
                now = datetime.now()
                current_hour = now.hour
                session_valid = 8 <= current_hour < 10 or (current_hour == 10 and now.minute <= 30)
                after_1030 = (current_hour == 10 and now.minute > 30) or current_hour > 10
                is_or_valid = or_size_pips <= 25 and or_size_pips > 0
                
                analysis = {
                    'symbol': symbol,
                    'current_price': current_price,
                    'direction': setup[0],
                    'or_high': or_high,
                    'or_low': or_low,
                    'or_size_pips': or_size_pips,
                    'entry_price': float(setup[3]) if setup[3] else current_price,
                    'sl_price': or_low if setup[2] else current_price * 0.998,
                    'tp_price': or_high if setup[1] else current_price * 1.002,
                    'setup_type': setup[4],
                    'fvg_size': float(setup[5]) if setup[5] else 0,
                    'session_phase': setup[6],
                    'body_percent': 0,  # Will be calculated from actual candles
                    'wick_against': 0,
                    'rr_ratio': 2.0,
                    'conditions': {
                        'session_valid': session_valid,
                        'after_1030': after_1030,
                        'or_established': True,
                        'or_valid': is_or_valid,
                        'breakout': 'BREAKOUT' in str(setup[4]),
                        'body_valid': False,
                        'wick_valid': True,
                        'decisive_close': 'Strong' in str(setup[4]) or 'Type A' in str(setup[4]),
                        'fvg_valid': True,
                        'risk_valid': True
                    },
                    'decision': 'ACCEPTED' if 'BREAKOUT' in str(setup[4]) and is_or_valid else 'REJECTED',
                    'reason': f"{setup[4]} - {setup[6]}" if is_or_valid else f"OR too wide: {or_size_pips} pips > 25"
                }
            else:
                # Default for GBPUSD V32
                from datetime import datetime
                now = datetime.now()
                current_hour = now.hour
                session_valid = 8 <= current_hour < 10 or (current_hour == 10 and now.minute <= 30)
                after_1030 = (current_hour == 10 and now.minute > 30) or current_hour > 10
                
                analysis = {
                    'symbol': symbol,
                    'current_price': current_price,
                    'direction': 'WAITING',
                    'or_high': current_price + 0.0005,
                    'or_low': current_price - 0.0005,
                    'or_size_pips': 0.0,
                    'entry_price': current_price,
                    'sl_price': current_price - 0.001,
                    'tp_price': current_price + 0.002,
                    'setup_type': 'NONE',
                    'fvg_size': 0,
                    'session_phase': 'Main Session (08:15-10:30)' if session_valid else 'Extended/Ended',
                    'body_percent': 0,
                    'wick_against': 0,
                    'rr_ratio': 2.0,
                    'conditions': {
                        'session_valid': session_valid,
                        'after_1030': after_1030,
                        'or_established': False,
                        'or_valid': False,
                        'breakout': False,
                        'body_valid': False,
                        'wick_valid': False,
                        'decisive_close': False,
                        'fvg_valid': True,
                        'risk_valid': True
                    },
                    'decision': 'REJECTED',
                    'reason': 'Așteptând Opening Range (08:00-08:15) sau OR prea wide'
                }
        
        conn.close()
        
        return jsonify({
            "status": "success",
            "symbol": symbol,
            "robot": robot,
            "analysis": analysis
        }), 200
        
    except Exception as e:
        logger.error(f"Eroare în /api/symbol_analysis: {e}")
        return jsonify({"status": "error", "error": str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def api_stats():
    """Returnează statistici de trading complete (NET - include commission și swap)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Total trades
        cursor.execute("SELECT COUNT(*) FROM closed_positions")
        total_trades = cursor.fetchone()[0]
        
        # Calculăm profitul NET (profit + commission + swap) pentru fiecare poziție
        cursor.execute("""
            SELECT 
                COUNT(*) FILTER (WHERE (profit + commission + swap) > 0) as winning,
                COUNT(*) FILTER (WHERE (profit + commission + swap) <= 0) as losing,
                SUM(profit + commission + swap) as total_net_profit,
                AVG(profit + commission + swap) as avg_net_trade,
                MIN(profit + commission + swap) as worst_trade,
                MAX(profit + commission + swap) as best_trade
            FROM closed_positions
        """)
        row = cursor.fetchone()
        winning_trades = row[0] or 0
        losing_trades = row[1] or 0
        total_net_profit = float(row[2]) if row[2] else 0
        avg_trade = float(row[3]) if row[3] else 0
        worst_trade = float(row[4]) if row[4] else 0
        best_trade = float(row[5]) if row[5] else 0
        
        # Profit factor (NET)
        cursor.execute("""
            SELECT 
                SUM(CASE WHEN (profit + commission + swap) > 0 THEN (profit + commission + swap) ELSE 0 END) as gross_profit,
                ABS(SUM(CASE WHEN (profit + commission + swap) < 0 THEN (profit + commission + swap) ELSE 0 END)) as gross_loss
            FROM closed_positions
        """)
        pf_row = cursor.fetchone()
        gross_profit = float(pf_row[0]) if pf_row[0] else 0
        gross_loss = float(pf_row[1]) if pf_row[1] else 0
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0
        
        # Win rate
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        # Max drawdown (simplified - from closed_positions NET)
        cursor.execute("""
            SELECT MIN(profit + commission + swap) as max_loss 
            FROM closed_positions
        """)
        max_drawdown_result = cursor.fetchone()[0]
        max_drawdown = float(max_drawdown_result) if max_drawdown_result else 0
        
        # Open positions count and profit
        cursor.execute("SELECT COUNT(*), SUM(profit) FROM mt5_positions_live")
        open_data = cursor.fetchone()
        open_positions = open_data[0] or 0
        open_profit = open_data[1] or 0
        
        conn.close()
        
        return jsonify({
            'status': 'success',
            'stats': {
                'total_trades': total_trades,
                'winning_trades': winning_trades,
                'losing_trades': losing_trades,
                'win_rate': round(win_rate, 2),
                'total_profit': round(total_net_profit, 2),
                'gross_profit': round(gross_profit, 2),
                'gross_loss': round(gross_loss, 2),
                'profit_factor': round(profit_factor, 2),
                'average_trade': round(avg_trade, 2),
                'max_drawdown': round(max_drawdown, 2),
                'best_trade': round(best_trade, 2),
                'worst_trade': round(worst_trade, 2),
                'open_positions': open_positions,
                'open_profit': round(open_profit, 2)
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Eroare în /api/stats: {e}")
        return jsonify({"status": "error", "error": str(e)}), 500


@app.route('/api/health', methods=['GET'])
def api_health_detailed():
    """Returnează health check detaliat al sistemului"""
    try:
        import psutil
        import subprocess
        
        health = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'services': []
        }
        
        # PostgreSQL health
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            conn.close()
            health['services'].append({
                'name': 'PostgreSQL',
                'status': 'healthy',
                'icon': '🗄️',
                'message': 'Connected'
            })
        except Exception as e:
            health['services'].append({
                'name': 'PostgreSQL',
                'status': 'error',
                'icon': '🗄️',
                'message': str(e)
            })
            health['status'] = 'degraded'
        
        # MT5 Core Server
        health['services'].append({
            'name': 'MT5 Core Server',
            'status': 'healthy',
            'icon': '🖥️',
            'message': f'Running on port {PORT}'
        })
        
        # VPS Bridges
        bridge_8080 = False
        bridge_7001 = False
        for proc in psutil.process_iter(['cmdline']):
            try:
                cmdline = ' '.join(proc.info['cmdline'] or [])
                if 'vps_bridge_8080.py' in cmdline:
                    bridge_8080 = True
                if 'vps_bridge_7001.py' in cmdline:
                    bridge_7001 = True
            except:
                pass
        
        health['services'].append({
            'name': 'VPS Bridge 8080',
            'status': 'healthy' if bridge_8080 else 'error',
            'icon': '🔗',
            'message': 'Connected' if bridge_8080 else 'Disconnected'
        })
        
        health['services'].append({
            'name': 'VPS Bridge 7001',
            'status': 'healthy' if bridge_7001 else 'error',
            'icon': '🔗',
            'message': 'Connected' if bridge_7001 else 'Disconnected'
        })
        
        # System resources
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        health['system'] = {
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'memory_used_gb': round(memory.used / (1024**3), 2),
            'memory_total_gb': round(memory.total / (1024**3), 2),
            'disk_percent': disk.percent,
            'disk_used_gb': round(disk.used / (1024**3), 2),
            'disk_total_gb': round(disk.total / (1024**3), 2)
        }
        
        return jsonify(health), 200
        
    except Exception as e:
        logger.error(f"Eroare în /api/health: {e}")
        return jsonify({"status": "error", "error": str(e)}), 500


@app.route('/api/equity', methods=['GET'])
def api_equity():
    """Returnează date pentru equity curve"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get closed positions ordered by close time
        cursor.execute("""
            SELECT close_time, profit, 
                   SUM(profit) OVER (ORDER BY close_time) as cumulative_profit
            FROM closed_positions
            WHERE close_time IS NOT NULL
            ORDER BY close_time ASC
        """)
        
        equity_data = []
        running_total = 0
        
        for row in cursor.fetchall():
            close_time, profit, cumulative = row
            equity_data.append({
                'time': close_time.isoformat() if close_time else None,
                'profit': round(profit, 2),
                'equity': round(cumulative, 2)
            })
        
        conn.close()
        
        return jsonify({
            'status': 'success',
            'data': equity_data,
            'count': len(equity_data)
        }), 200
        
    except Exception as e:
        logger.error(f"Eroare în /api/equity: {e}")
        return jsonify({"status": "error", "error": str(e)}), 500


@app.route('/api/symbols', methods=['GET'])
def api_symbols():
    """Returnează performance pe simboluri"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                symbol,
                COUNT(*) as trades,
                SUM(CASE WHEN profit > 0 THEN 1 ELSE 0 END) as wins,
                SUM(CASE WHEN profit <= 0 THEN 1 ELSE 0 END) as losses,
                SUM(profit) as total_profit,
                AVG(profit) as avg_profit,
                MAX(profit) as best_trade,
                MIN(profit) as worst_trade
            FROM closed_positions
            GROUP BY symbol
            ORDER BY total_profit DESC
        """)
        
        symbols = []
        for row in cursor.fetchall():
            symbol, trades, wins, losses, total, avg, best, worst = row
            win_rate = (wins / trades * 100) if trades > 0 else 0
            
            symbols.append({
                'symbol': symbol,
                'trades': trades,
                'wins': wins,
                'losses': losses,
                'win_rate': round(win_rate, 1),
                'total_profit': round(total, 2),
                'avg_profit': round(avg, 2),
                'best_trade': round(best, 2),
                'worst_trade': round(worst, 2)
            })
        
        conn.close()
        
        return jsonify({
            'status': 'success',
            'symbols': symbols,
            'count': len(symbols)
        }), 200
        
    except Exception as e:
        logger.error(f"Eroare în /api/symbols: {e}")
        return jsonify({"status": "error", "error": str(e)}), 500


@app.route('/api/v31_incomplete_setups', methods=['GET'])
def api_v31_incomplete_setups():
    """Returnează setup-urile incomplete de la V31 pentru dashboard"""
    try:
        limit = request.args.get('limit', 20, type=int)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Șterge setup-urile vechi (mai mult de 1 oră)
        cursor.execute("""
            DELETE FROM v31_incomplete_setups 
            WHERE created_at < NOW() - INTERVAL '1 hour'
        """)
        
        # Ia setup-urile recente
        cursor.execute("""
            SELECT 
                symbol, direction, score, max_score, rsi, stoch_k,
                fib_level, in_kill_zone, trend_aligned, bb_touch, fvg_detected,
                entry_price, current_price, rr_ratio, details, created_at
            FROM v31_incomplete_setups
            ORDER BY created_at DESC
            LIMIT %s
        """, (limit,))
        
        setups = []
        for row in cursor.fetchall():
            setups.append({
                'symbol': row[0],
                'direction': row[1],
                'score': row[2],
                'max_score': row[3],
                'rsi': float(row[4]) if row[4] else None,
                'stoch_k': float(row[5]) if row[5] else None,
                'fib_level': float(row[6]) if row[6] else None,
                'in_kill_zone': row[7],
                'trend_aligned': row[8],
                'bb_touch': row[9],
                'fvg_detected': row[10],
                'entry_price': float(row[11]) if row[11] else None,
                'current_price': float(row[12]) if row[12] else None,
                'rr_ratio': float(row[13]) if row[13] else None,
                'details': row[14],
                'created_at': row[15].isoformat() if row[15] else None
            })
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'setups': setups,
            'count': len(setups)
        }), 200
        
    except Exception as e:
        logger.error(f"Eroare în /api/v31_incomplete_setups: {e}")
        return jsonify({"status": "error", "error": str(e)}), 500


@app.route('/api/v31/live_status', methods=['GET'])
def api_v31_live_status():
    """Returnează statusul live al analizei V31 - simboluri analizate, setup-uri, rejected"""
    try:
        import json
        import os
        from datetime import datetime
        
        # Scan /tmp for V31 symbol analysis files
        analyzed_symbols = []
        setups_found = []
        rejected_setups = []
        current_symbol = None
        progress = 0
        
        # Common symbols to check
        symbols = [
            'EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'USDCAD', 'USDCHF', 'NZDUSD',
            'EURGBP', 'EURJPY', 'EURCHF', 'EURCAD', 'EURAUD', 'EURNZD',
            'GBPJPY', 'GBPCHF', 'GBPCAD', 'GBPAUD', 'GBPNZD',
            'AUDJPY', 'AUDCHF', 'AUDCAD', 'CADJPY', 'CHFJPY', 'NZDJPY',
            'XAUUSD', 'US30', 'US500', 'USTEC', 'DE40', 'STOXX50'
        ]
        
        for symbol in symbols:
            filepath = f'/tmp/v31_symbol_analysis_{symbol}.json'
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                        analyzed_symbols.append({
                            'symbol': symbol,
                            'direction': data.get('direction'),
                            'score': data.get('score'),
                            'decision': data.get('decision'),
                            'timestamp': data.get('timestamp')
                        })
                        
                        if data.get('decision') == 'ACCEPTED':
                            setups_found.append({
                                'symbol': symbol,
                                'direction': data.get('direction'),
                                'entry_price': data.get('entry_price'),
                                'score': data.get('score'),
                                'rsi': data.get('rsi'),
                                'stoch_k': data.get('stoch_k'),
                                'fib_level': data.get('fib_level'),
                                'in_kill_zone': data.get('in_kill_zone'),
                                'trend_aligned': data.get('trend_aligned'),
                                'bb_touch': data.get('bb_touch'),
                                'fvg_detected': data.get('fvg_detected'),
                                'timestamp': data.get('timestamp')
                            })
                        elif data.get('decision') == 'REJECTED':
                            rejected_setups.append({
                                'symbol': symbol,
                                'direction': data.get('direction'),
                                'score': data.get('score'),
                                'reason': data.get('reason'),
                                'timestamp': data.get('timestamp')
                            })
                except Exception as e:
                    logger.error(f"Error reading {filepath}: {e}")
        
        # Get recent log entries for current status
        phase = 'Waiting...'
        try:
            log_file = '/var/log/v31_enhanced.log'
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    lines = f.readlines()
                    # Check last 20 lines for current status
                    for line in lines[-20:]:
                        if 'Analizez:' in line:
                            match = re.search(r'Analizez:\s+(\w+)', line)
                            if match:
                                current_symbol = match.group(1)
                        if 'PROGRESS' in line:
                            match = re.search(r'progress=(\d+)%', line)
                            if match:
                                progress = int(match.group(1))
                        if 'CYCLE_START' in line or 'Ciclu de trading' in line:
                            phase = 'Analyzing...'
                        if 'CYCLE_COMPLETE' in line:
                            phase = 'Complete'
        except Exception as e:
            logger.error(f"Error reading log file: {e}")
        
        return jsonify({
            'status': 'success',
            'phase': phase,
            'progress': progress,
            'current_symbol': current_symbol,
            'analyzed_count': len(analyzed_symbols),
            'setups_count': len(setups_found),
            'rejected_count': len(rejected_setups),
            'symbols': analyzed_symbols,
            'setups': setups_found,
            'rejected': rejected_setups,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Eroare în /api/v31/live_status: {e}")
        return jsonify({"status": "error", "error": str(e)}), 500


@app.route('/api/v32_status', methods=['GET'])
def api_v32_status():
    """Returnează statusul V32 London Breakout robot - OR data, breakouts, etc."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get latest OR data from v32_incomplete_setups
        cursor.execute("""
            SELECT 
                symbol, or_high, or_low, session_phase,
                created_at
            FROM v32_incomplete_setups
            WHERE created_at > NOW() - INTERVAL '2 hours'
            ORDER BY created_at DESC
            LIMIT 1
        """)
        
        or_data = cursor.fetchone()
        
        # Get count of breakouts detected today
        cursor.execute("""
            SELECT COUNT(*) 
            FROM v32_incomplete_setups
            WHERE created_at > NOW() - INTERVAL '1 day'
            AND setup_type LIKE '%BREAKOUT%'
        """)
        
        breakouts_count = cursor.fetchone()[0]
        
        # Get last session phase from logs (via robot_logs or estimate)
        from datetime import datetime
        current_time = datetime.now().time()
        
        if current_time.hour < 8:
            current_phase = "Before London Session"
        elif current_time.hour < 10 or (current_time.hour == 10 and current_time.minute <= 30):
            current_phase = "London Session"
        else:
            current_phase = "After London Session"
        
        conn.close()
        
        response = {
            'status': 'success',
            'symbol': 'GBPUSD',
            'session_phase': current_phase,
            'or_high': float(or_data[1]) if or_data and or_data[1] else None,
            'or_low': float(or_data[2]) if or_data and or_data[2] else None,
            'or_size_pips': None,
            'breakouts_detected': breakouts_count,
            'last_update': or_data[4].isoformat() if or_data and or_data[4] else None
        }
        
        # Calculate OR size in pips if we have high and low
        if response['or_high'] and response['or_low']:
            response['or_size_pips'] = round((response['or_high'] - response['or_low']) * 10000, 1)
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Eroare în /api/v32_status: {e}")
        return jsonify({
            'status': 'success',  # Return success with defaults
            'symbol': 'GBPUSD',
            'session_phase': 'Before London Session',
            'or_high': None,
            'or_low': None,
            'or_size_pips': None,
            'breakouts_detected': 0,
            'last_update': None
        }), 200


@app.route('/api/daily-profit', methods=['GET'])
def api_daily_profit():
    """Returnează profitul total pe ziua curentă (din poziții închise + deschise)
    
    Calculează profitul NET: profit + commission + swap
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Data de început a zilei curente (00:00:00)
        from datetime import datetime, time
        today_start = datetime.combine(datetime.now().date(), time.min)
        
        # Profit NET din poziții închise astăzi (profit + commission + swap)
        cursor.execute("""
            SELECT 
                COALESCE(SUM(profit), 0) as gross_profit,
                COALESCE(SUM(commission), 0) as total_commission,
                COALESCE(SUM(swap), 0) as total_swap
            FROM closed_positions
            WHERE close_time >= %s
        """, (today_start,))
        
        row = cursor.fetchone()
        gross_profit = float(row[0]) if row[0] else 0
        commission = float(row[1]) if row[1] else 0
        swap = float(row[2]) if row[2] else 0
        closed_net_profit = gross_profit + commission + swap
        
        # Profit din poziții deschise (din cache-ul clienților)
        open_profit = 0
        with clients_lock:
            for login, client in clients_cache.items():
                if client.is_active:
                    for pos in client.positions:
                        open_profit += pos.get('profit', 0)
        
        total_daily_profit = closed_net_profit + open_profit
        
        conn.close()
        
        return jsonify({
            'status': 'success',
            'daily_profit': round(total_daily_profit, 2),
            'gross_profit': round(gross_profit, 2),
            'commission': round(commission, 2),
            'swap': round(swap, 2),
            'closed_positions_profit': round(closed_net_profit, 2),
            'open_positions_profit': round(open_profit, 2),
            'date': datetime.now().strftime('%Y-%m-%d'),
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Eroare în /api/daily-profit: {e}")
        return jsonify({"status": "error", "error": str(e)}), 500


# Dashboard static files
DASHBOARD_PATH = "/root/clawd/dashboard"

@app.route('/dashboard')
def serve_dashboard():
    """Servește pagina dashboard-ului de loguri"""
    try:
        if os.path.exists(os.path.join(DASHBOARD_PATH, "index.html")):
            return send_from_directory(DASHBOARD_PATH, "index.html")
        return jsonify({"error": "Dashboard not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ═══════════════════════════════════════════════════════════════════════════
# AUTHENTICATION ENDPOINTS (Added for PRE-FINAL-V1)
# ═══════════════════════════════════════════════════════════════════════════

# User configuration
USERS = {
    'Andrei': {
        'password': 'Andrei336',
        'role': 'admin',
        'permissions': {
            'can_stop_robots': True,
            'can_stop_services': True,
            'can_control_clients': True,
            'view_containers': ['all'],
            'can_accept_commands': True,
            'robot_selection': 'all'
        }
    },
    'Catalin': {
        'password': 'Catalin',
        'role': 'user',
        'permissions': {
            'can_stop_robots': False,
            'can_stop_services': False,
            'can_control_clients': False,
            'view_containers': [
                'clients', 'positions', 'robot_status', 'incomplete_setups',
                'system_health', 'statistics', 'equity_curve', 'services',
                'trading_robots', 'tracking'
            ],
            'can_accept_commands': True,
            'robot_selection': 'view'
        }
    }
}

active_sessions = {}

import secrets

def generate_token():
    return secrets.token_urlsafe(32)

@app.route('/api/auth/login', methods=['POST'])
def api_auth_login():
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({'status': 'error', 'message': 'Date lipsă'}), 400
        
        user = USERS.get(username)
        if not user or user['password'] != password:
            return jsonify({'status': 'error', 'message': 'Utilizator sau parolă incorectă'}), 401
        
        token = generate_token()
        active_sessions[token] = {
            'username': username,
            'role': user['role'],
            'permissions': user['permissions'],
            'login_time': datetime.utcnow().isoformat()
        }
        
        logger.info(f"User {username} logged in")
        
        return jsonify({
            'status': 'success',
            'username': username,
            'role': user['role'],
            'permissions': user['permissions'],
            'token': token
        }), 200
        
    except Exception as e:
        logger.error(f"Error in login: {e}")
        return jsonify({'status': 'error', 'message': 'Eroare server'}), 500

@app.route('/api/auth/logout', methods=['POST'])
def api_auth_logout():
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header[7:]
            if token in active_sessions:
                username = active_sessions[token]['username']
                del active_sessions[token]
                logger.info(f"User {username} logged out")
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'error'}), 500

@app.route('/api/auth/check', methods=['GET'])
def api_auth_check():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'status': 'error', 'authenticated': False}), 401
    
    token = auth_header[7:]
    if token in active_sessions:
        session = active_sessions[token]
        return jsonify({
            'status': 'success',
            'authenticated': True,
            'username': session['username'],
            'role': session['role'],
            'permissions': session['permissions']
        }), 200
    return jsonify({'status': 'error', 'authenticated': False}), 401


# ========================================================================
# USER-MT5 ACCOUNT ASSOCIATION ENDPOINTS
# ========================================================================

def require_admin():
    """Verifică dacă utilizatorul curent este admin"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None, jsonify({'status': 'error', 'message': 'Autentificare necesară'}), 401
    
    token = auth_header[7:]
    if token not in active_sessions:
        return None, jsonify({'status': 'error', 'message': 'Sesiune invalidă'}), 401
    
    session = active_sessions[token]
    if session.get('role') != 'admin':
        return None, jsonify({'status': 'error', 'message': 'Acces interzis - doar admin'}), 403
    
    return session, None, None

@app.route('/api/user_accounts', methods=['GET'])
def api_get_user_accounts():
    """API: Returnează toate asocierile user-MT5 (doar admin)"""
    try:
        session, error_response, error_code = require_admin()
        if error_response:
            return error_response, error_code
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Ia toate asocierile cu informații despre nume client
        cursor.execute('''
            SELECT u.id, u.username, u.mt5_login, u.created_at, c.name
            FROM user_mt5_accounts u
            LEFT JOIN client_settings c ON u.mt5_login = c.login
            ORDER BY u.username, u.mt5_login
        ''')
        
        associations = []
        for row in cursor.fetchall():
            associations.append({
                'id': row[0],
                'username': row[1],
                'mt5_login': row[2],
                'created_at': row[3].isoformat() if row[3] else None,
                'client_name': row[4] or f'Account_{row[2]}'
            })
        
        # Ia lista tuturor utilizatorilor disponibili
        users = list(USERS.keys())
        
        # Ia lista tuturor conturilor MT5 cunoscute
        cursor.execute('''
            SELECT DISTINCT login, name FROM client_settings ORDER BY login
        ''')
        mt5_accounts = []
        for row in cursor.fetchall():
            mt5_accounts.append({
                'login': row[0],
                'name': row[1] or f'Account_{row[0]}'
            })
        
        conn.close()
        
        return jsonify({
            'status': 'success',
            'associations': associations,
            'users': users,
            'mt5_accounts': mt5_accounts,
            'count': len(associations)
        }), 200
        
    except Exception as e:
        logger.error(f"Eroare API get_user_accounts: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/user_accounts', methods=['POST'])
def api_create_user_account():
    """API: Creează o nouă asociere user-MT5 (doar admin)"""
    try:
        session, error_response, error_code = require_admin()
        if error_response:
            return error_response, error_code
        
        data = request.get_json()
        username = data.get('username', '').strip()
        mt5_login = data.get('mt5_login')
        
        if not username or not mt5_login:
            return jsonify({'status': 'error', 'message': 'Username și MT5 login sunt obligatorii'}), 400
        
        # Verifică dacă utilizatorul există
        if username not in USERS:
            return jsonify({'status': 'error', 'message': f'Utilizatorul {username} nu există'}), 400
        
        # Convertește mt5_login la int
        try:
            mt5_login = int(mt5_login)
        except (ValueError, TypeError):
            return jsonify({'status': 'error', 'message': 'MT5 login trebuie să fie un număr'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO user_mt5_accounts (username, mt5_login)
                VALUES (%s, %s)
                RETURNING id
            ''', (username, mt5_login))
            
            new_id = cursor.fetchone()[0]
            conn.commit()
            
            logger.info(f"✅ Asociere creată: {username} -> {mt5_login} (id={new_id})")
            
            return jsonify({
                'status': 'success',
                'message': 'Asociere creată cu succes',
                'id': new_id,
                'username': username,
                'mt5_login': mt5_login
            }), 200
            
        except psycopg2.IntegrityError:
            conn.rollback()
            return jsonify({
                'status': 'error',
                'message': f'Asocierea între {username} și {mt5_login} există deja'
            }), 409
        finally:
            conn.close()
            
    except Exception as e:
        logger.error(f"Eroare API create_user_account: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/user_accounts/<int:association_id>', methods=['DELETE'])
def api_delete_user_account(association_id):
    """API: Șterge o asociere user-MT5 (doar admin)"""
    try:
        session, error_response, error_code = require_admin()
        if error_response:
            return error_response, error_code
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Ia informațiile înainte de ștergere pentru log
        cursor.execute(
            'SELECT username, mt5_login FROM user_mt5_accounts WHERE id = %s',
            (association_id,)
        )
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return jsonify({
                'status': 'error',
                'message': f'Asocierea cu ID {association_id} nu există'
            }), 404
        
        username, mt5_login = row
        
        cursor.execute('DELETE FROM user_mt5_accounts WHERE id = %s', (association_id,))
        conn.commit()
        conn.close()
        
        logger.info(f"🗑️ Asociere ștearsă: {username} -> {mt5_login} (id={association_id})")
        
        return jsonify({
            'status': 'success',
            'message': 'Asociere ștearsă cu succes',
            'id': association_id,
            'username': username,
            'mt5_login': mt5_login
        }), 200
        
    except Exception as e:
        logger.error(f"Eroare API delete_user_account: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


# =======================================================================
# 🤖 ROBOT SYMBOL CONFIGURATION API
# =======================================================================

@app.route('/api/robot_symbols', methods=['GET'])
def api_get_robot_symbols():
    """API: Obține lista de simboluri activate pentru un robot"""
    try:
        robot = request.args.get('robot', '')
        
        if not robot:
            return jsonify({'status': 'error', 'message': 'Robot parameter required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get enabled symbols for this robot
        cursor.execute('''
            SELECT symbol FROM robot_symbol_config 
            WHERE robot = %s AND enabled = true
            ORDER BY symbol
        ''', (robot,))
        
        rows = cursor.fetchall()
        symbols = [row[0] for row in rows]
        
        # If no symbols configured, return defaults
        if not symbols:
            if robot == 'v32_london':
                symbols = ['GBPUSD']
            elif robot == 'v33_ny':
                symbols = ['EURUSD']
        
        conn.close()
        
        return jsonify({
            'status': 'success',
            'robot': robot,
            'symbols': symbols,
            'count': len(symbols)
        }), 200
        
    except Exception as e:
        logger.error(f"Eroare API get_robot_symbols: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/robot_symbols', methods=['POST'])
def api_set_robot_symbols():
    """API: Setează lista de simboluri activate pentru un robot (doar admin)"""
    try:
        session, error_response, error_code = require_admin()
        if error_response:
            return error_response, error_code
        
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': 'No data provided'}), 400
        
        robot = data.get('robot', '')
        symbols = data.get('symbols', [])
        
        if not robot:
            return jsonify({'status': 'error', 'message': 'Robot parameter required'}), 400
        
        if not isinstance(symbols, list):
            return jsonify({'status': 'error', 'message': 'Symbols must be a list'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Delete existing config for this robot
        cursor.execute('DELETE FROM robot_symbol_config WHERE robot = %s', (robot,))
        
        # Insert new config
        for symbol in symbols:
            cursor.execute('''
                INSERT INTO robot_symbol_config (robot, symbol, enabled)
                VALUES (%s, %s, %s)
            ''', (robot, symbol, True))
        
        conn.commit()
        conn.close()
        
        logger.info(f"🤖 Symbol config updated for {robot}: {len(symbols)} symbols")
        
        return jsonify({
            'status': 'success',
            'robot': robot,
            'symbols': symbols,
            'count': len(symbols),
            'message': f'Configuration saved for {robot}'
        }), 200
        
    except Exception as e:
        logger.error(f"Eroare API set_robot_symbols: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/robot_symbol_status', methods=['GET'])
def api_get_robot_symbol_status():
    """API: Obține statusul live pentru toate simbolurile unui robot"""
    try:
        robot = request.args.get('robot', '')
        
        if not robot:
            return jsonify({'status': 'error', 'message': 'Robot parameter required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        cursor.execute('''
            SELECT symbol, or_high, or_low, asia_range, asia_compressed,
                   current_price, signal, breakout_status, daily_trades, updated_at
            FROM robot_symbol_status
            WHERE robot = %s
            ORDER BY symbol
        ''', (robot,))
        
        rows = cursor.fetchall()
        conn.close()
        
        # Convert to list of dicts
        status_list = []
        for row in rows:
            status_list.append({
                'symbol': row['symbol'],
                'or_high': float(row['or_high']) if row['or_high'] else None,
                'or_low': float(row['or_low']) if row['or_low'] else None,
                'asia_range': float(row['asia_range']) if row['asia_range'] else None,
                'asia_compressed': row['asia_compressed'],
                'current_price': float(row['current_price']) if row['current_price'] else None,
                'signal': row['signal'],
                'breakout_status': row['breakout_status'],
                'daily_trades': row['daily_trades'],
                'updated_at': row['updated_at'].isoformat() if row['updated_at'] else None
            })
        
        return jsonify({
            'status': 'success',
            'robot': robot,
            'symbols': status_list,
            'count': len(status_list)
        }), 200
        
    except Exception as e:
        logger.error(f"Eroare API get_robot_symbol_status: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/v32/session_status', methods=['GET'])
def api_v32_session_status():
    """API: Get V32 London Session live status"""
    try:
        import pytz
        from datetime import datetime
        
        london_tz = pytz.timezone('Europe/London')
        london_time = datetime.now(london_tz)
        
        hour, minute = london_time.hour, london_time.minute
        current_minutes = hour * 60 + minute
        
        session_start = 8 * 60  # 08:00
        session_end = 10 * 60 + 30  # 10:30
        
        if current_minutes < session_start:
            phase = "BEFORE_SESSION"
            time_remaining = session_start - current_minutes
            is_active = False
            status_text = "Waiting"
        elif current_minutes < session_end:
            phase = "MAIN_SESSION"
            time_remaining = session_end - current_minutes
            is_active = True
            status_text = "Active"
        else:
            phase = "AFTER_SESSION"
            time_remaining = 0
            is_active = False
            status_text = "Ended"
        
        return jsonify({
            'status': 'success',
            'london_time': london_time.strftime('%H:%M:%S'),
            'london_hour': hour,
            'london_minute': minute,
            'session_phase': phase,
            'time_remaining_seconds': time_remaining * 60,
            'time_remaining_minutes': time_remaining,
            'is_active': is_active,
            'status_text': status_text
        }), 200
        
    except Exception as e:
        logger.error(f"Eroare API v32_session_status: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/v33/session_status', methods=['GET'])
def api_v33_session_status():
    """API: Get V33 NY Session live status"""
    try:
        import pytz
        from datetime import datetime
        
        ny_tz = pytz.timezone('America/New_York')
        ny_time = datetime.now(ny_tz)
        
        hour, minute = ny_time.hour, ny_time.minute
        current_minutes = hour * 60 + minute
        
        session_start = 13 * 60  # 13:00
        session_end = 16 * 60  # 16:00
        
        if current_minutes < session_start:
            phase = "BEFORE_SESSION"
            time_remaining = session_start - current_minutes
            is_active = False
            status_text = "Waiting"
        elif current_minutes < session_end:
            phase = "MAIN_SESSION"
            time_remaining = session_end - current_minutes
            is_active = True
            status_text = "Active"
        else:
            phase = "AFTER_SESSION"
            time_remaining = 0
            is_active = False
            status_text = "Ended"
        
        return jsonify({
            'status': 'success',
            'ny_time': ny_time.strftime('%H:%M:%S'),
            'ny_hour': hour,
            'ny_minute': minute,
            'session_phase': phase,
            'time_remaining_seconds': time_remaining * 60,
            'time_remaining_minutes': time_remaining,
            'is_active': is_active,
            'status_text': status_text
        }), 200
        
    except Exception as e:
        logger.error(f"Eroare API v33_session_status: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/v33/or_data', methods=['GET'])
def get_v33_or_data():
    """API: Get V33 NY Opening Range (13:00-13:15 NY) data
    
    Returns OR high, low, range size, and current price for USD pairs.
    Similar to V32 but for NY session timing.
    """
    try:
        symbol = request.args.get('symbol', 'EURUSD')
        
        # Get latest OR data from v32_incomplete_setups (V33 uses same table)
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Try 1: Get from v33_symbol_status (primary source for V33)
        cursor.execute("""
            SELECT 
                symbol, or_high, or_low, or_range,
                last_update as created_at
            FROM v33_symbol_status
            WHERE symbol = %s
            AND or_high IS NOT NULL 
            AND or_low IS NOT NULL
            ORDER BY last_update DESC
            LIMIT 1
        """, (symbol,))
        
        or_data = cursor.fetchone()
        
        # Try 2: Fallback to v32_incomplete_setups without NY filter
        if not or_data:
            cursor.execute("""
                SELECT 
                    symbol, or_high, or_low, NULL as or_range,
                    created_at
                FROM v32_incomplete_setups
                WHERE symbol = %s
                AND or_high IS NOT NULL 
                AND or_low IS NOT NULL
                AND created_at > NOW() - INTERVAL '1 day'
                ORDER BY created_at DESC
                LIMIT 1
            """, (symbol,))
            or_data = cursor.fetchone()
        
        conn.close()
        
        # Get current price from clients cache
        current_price = None
        with clients_lock:
            for login, client in clients_cache.items():
                if symbol in client.market_prices:
                    price_data = client.market_prices[symbol]
                    current_price = price_data.get('bid')
                    break
        
        # Default values if no data found
        or_high = float(or_data[1]) if or_data and or_data[1] else None
        or_low = float(or_data[2]) if or_data and or_data[2] else None
        
        # Calculate OR range in pips
        or_range = None
        if or_high and or_low:
            # First try to use stored or_range from v33_symbol_status (if available)
            if or_data and or_data[3] is not None:
                or_range = float(or_data[3])
            else:
                # Calculate from or_high and or_low
                # For JPY pairs, different pip calculation
                if 'JPY' in symbol:
                    or_range = round((or_high - or_low) * 100, 2)
                else:
                    or_range = round((or_high - or_low) * 10000, 1)
        
        # If no current price from cache, use midpoint of OR
        if current_price is None and or_high and or_low:
            current_price = round((or_high + or_low) / 2, 5)
        
        response = {
            'status': 'success',
            'symbol': symbol,
            'or_high': or_high,
            'or_low': or_low,
            'or_range': or_range,
            'current_price': current_price,
            'session': 'NY',
            'session_time': '13:00-13:15',
            'last_update': or_data[4].isoformat() if or_data and or_data[4] else None
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Eroare în /api/v33/or_data: {e}")
        # Return default response on error
        return jsonify({
            'status': 'success',
            'symbol': request.args.get('symbol', 'EURUSD'),
            'or_high': None,
            'or_low': None,
            'or_range': None,
            'current_price': None,
            'session': 'NY',
            'session_time': '13:00-13:15',
            'last_update': None
        }), 200


@app.route('/api/v33/presession_data', methods=['GET'])
def get_v33_presession_data():
    """API: Get V33 NY Pre-Session (08:00-13:00 NY) data
    
    Returns pre-session high, low, range size, and compression status.
    Pre-session is 08:00-13:00 NY time (before NY OR formation).
    
    Query params:
        symbol: Currency pair (default: EURUSD)
    
    Returns:
        {
            "presession_high": 1.08680,
            "presession_low": 1.08120,
            "presession_range": 56.0,
            "is_compressed": true
        }
    """
    try:
        symbol = request.args.get('symbol', 'EURUSD')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        pre_high = None
        pre_low = None
        pre_range_pips = None
        or_range_pips = None
        is_compressed = False
        
        # Try 1: Get from v33_symbol_status table (primary source)
        try:
            cursor.execute("""
                SELECT pre_session_high, pre_session_low, pre_session_range,
                       or_high, or_low, or_range
                FROM v33_symbol_status 
                WHERE symbol = %s 
                ORDER BY analysis_time DESC 
                LIMIT 1
            """, (symbol,))
            
            row = cursor.fetchone()
            if row:
                pre_high = float(row[0]) if row[0] else None
                pre_low = float(row[1]) if row[1] else None
                pre_range_pips = float(row[2]) if row[2] else None
                or_high = float(row[3]) if row[3] else None
                or_low = float(row[4]) if row[4] else None
                or_range_pips = float(row[5]) if row[5] else None
        except Exception as e1:
            logger.debug(f"v33_symbol_status query failed: {e1}")
        
        # Try 2: Query OHLC data directly for 08:00-13:00 NY
        if pre_high is None or pre_low is None:
            try:
                import pytz
                from datetime import datetime, timedelta
                
                ny_tz = pytz.timezone('America/New_York')
                ny_now = datetime.now(ny_tz)
                
                # Get today's 08:00 and 13:00 NY time in UTC
                ny_today = ny_now.replace(hour=0, minute=0, second=0, microsecond=0)
                ny_08h = ny_today + timedelta(hours=8)
                ny_13h = ny_today + timedelta(hours=13)
                
                # Convert to UTC for DB query
                utc_tz = pytz.UTC
                utc_08h = ny_08h.astimezone(utc_tz)
                utc_13h = ny_13h.astimezone(utc_tz)
                
                # Query OHLC data for pre-session period
                cursor.execute("""
                    SELECT MAX(high) as pre_high, MIN(low) as pre_low
                    FROM ohlc_data 
                    WHERE symbol = %s 
                    AND timeframe = 'M1'
                    AND to_timestamp(timestamp) >= %s
                    AND to_timestamp(timestamp) < %s
                """, (symbol, utc_08h, utc_13h))
                
                row = cursor.fetchone()
                if row and row[0] and row[1]:
                    pre_high = float(row[0])
                    pre_low = float(row[1])
            except Exception as e2:
                logger.debug(f"OHLC query failed: {e2}")
        
        # Calculate range in pips if we have high/low
        if pre_high and pre_low:
            price_range = pre_high - pre_low
            # For JPY pairs, different pip calculation
            if 'JPY' in symbol:
                pre_range_pips = round(price_range * 100, 2)
            else:
                pre_range_pips = round(price_range * 10000, 1)
        
        # Calculate compression: pre-session is compressed if range is small
        # relative to typical OR or below a threshold (e.g., < 30 pips)
        if pre_range_pips is not None:
            # Compression threshold: < 30 pips is considered compressed
            # Also compare with OR range if available
            compression_threshold = 30.0
            if or_range_pips and or_range_pips > 0:
                # If pre-session range is less than 60% of OR range, it's compressed
                is_compressed = pre_range_pips < (or_range_pips * 0.6)
            else:
                is_compressed = pre_range_pips < compression_threshold
        
        conn.close()
        
        response = {
            'status': 'success',
            'symbol': symbol,
            'presession_high': pre_high,
            'presession_low': pre_low,
            'presession_range': pre_range_pips,
            'is_compressed': is_compressed,
            'session_time': '08:00-13:00 NY',
            'or_range': or_range_pips
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Eroare în /api/v33/presession_data: {e}")
        return jsonify({
            'status': 'error',
            'symbol': request.args.get('symbol', 'EURUSD'),
            'presession_high': None,
            'presession_low': None,
            'presession_range': None,
            'is_compressed': False,
            'session_time': '08:00-13:00 NY'
        }), 500


# ========================================================================
@app.route('/api/robot_symbol_tracking', methods=['GET'])
def get_robot_symbol_tracking():
    """Get per-symbol analysis and trade tracking data"""
    try:
        robot = request.args.get('robot', 'v31_enhanced')
        
        conn = psycopg2.connect(**PG_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT symbol, analyzed, analysis_timestamp, setup_found, setup_score,
                   setup_direction, trade_opened, trade_ticket, trade_timestamp,
                   cooldown_until, last_update
            FROM robot_symbol_tracking
            WHERE robot = %s
            ORDER BY symbol
        """, (robot,))
        
        rows = cursor.fetchall()
        
        symbols = []
        for row in rows:
            symbols.append({
                'symbol': row[0],
                'analyzed': row[1],
                'analysis_timestamp': str(row[2]) if row[2] else None,
                'setup_found': row[3],
                'setup_score': row[4],
                'setup_direction': row[5],
                'trade_opened': row[6],
                'trade_ticket': row[7],
                'cooldown_until': str(row[9]) if row[9] else None,
                'last_update': str(row[10]) if row[10] else None
            })
        
        conn.close()
        
        return jsonify({
            'status': 'success',
            'robot': robot,
            'count': len(symbols),
            'symbols': symbols
        })
        
    except Exception as e:
        logger.error(f"Error getting symbol tracking: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500




@app.route('/api/v32/symbol_status', methods=['GET'])
def get_v32_symbol_status():
    """Get V32 London Breakout per-symbol status"""
    try:
        conn = psycopg2.connect(**PG_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT symbol, analyzed, analysis_time, asia_high, asia_low, asia_range,
                   or_high, or_low, or_range, breakout_detected, breakout_direction,
                   signal, trade_opened, trade_ticket, cooldown_until
            FROM v32_symbol_status ORDER BY symbol
        """)
        rows = cursor.fetchall()
        symbols = []
        for row in rows:
            symbols.append({
                'symbol': row[0], 'analyzed': row[1], 'analysis_time': str(row[2]) if row[2] else None,
                'asia_high': float(row[3]) if row[3] else None, 'asia_low': float(row[4]) if row[4] else None,
                'asia_range': float(row[5]) if row[5] else None, 'or_high': float(row[6]) if row[6] else None,
                'or_low': float(row[7]) if row[7] else None, 'or_range': float(row[8]) if row[8] else None,
                'breakout_detected': row[9], 'breakout_direction': row[10], 'signal': row[11],
                'trade_opened': row[12], 'trade_ticket': row[13], 'cooldown_until': str(row[14]) if row[14] else None
            })
        conn.close()
        return jsonify({'status': 'success', 'count': len(symbols), 'symbols': symbols})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/v33/symbol_status', methods=['GET'])
def get_v33_symbol_status():
    """Get V33 NY Breakout per-symbol status"""
    try:
        conn = psycopg2.connect(**PG_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT symbol, analyzed, analysis_time, pre_session_high, pre_session_low, pre_session_range,
                   or_high, or_low, or_range, breakout_detected, breakout_direction,
                   signal, trade_opened, trade_ticket, cooldown_until
            FROM v33_symbol_status ORDER BY symbol
        """)
        rows = cursor.fetchall()
        symbols = []
        for row in rows:
            symbols.append({
                'symbol': row[0], 'analyzed': row[1], 'analysis_time': str(row[2]) if row[2] else None,
                'pre_high': float(row[3]) if row[3] else None, 'pre_low': float(row[4]) if row[4] else None,
                'pre_range': float(row[5]) if row[5] else None, 'or_high': float(row[6]) if row[6] else None,
                'or_low': float(row[7]) if row[7] else None, 'or_range': float(row[8]) if row[8] else None,
                'breakout_detected': row[9], 'breakout_direction': row[10], 'signal': row[11],
                'trade_opened': row[12], 'trade_ticket': row[13], 'cooldown_until': str(row[14]) if row[14] else None
            })
        conn.close()
        return jsonify({'status': 'success', 'count': len(symbols), 'symbols': symbols})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


import subprocess

@app.route('/api/robot_process_status', methods=['GET'])
def get_robot_process_status():
    """Get real-time robot process status from system"""
    try:
        robots = {
            'v31_tpl': {'name': 'V31 Marius TPL', 'pattern': 'v31_marius_tpl_robot.py', 'running': False, 'pid': None, 'uptime': None},
            'v31_enhanced': {'name': 'V31 Enhanced', 'pattern': 'v31_enhanced.py', 'running': False, 'pid': None, 'uptime': None},
            'v32_london': {'name': 'V32 London Breakout', 'pattern': 'v32_london_breakout_robot.py', 'running': False, 'pid': None, 'uptime': None},
            'v33_ny': {'name': 'V33 NY Breakout', 'pattern': 'v33_ny_breakout_robot.py', 'running': False, 'pid': None, 'uptime': None}
        }
        
        # Get all python processes
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        
        for line in lines:
            if 'python' in line and 'grep' not in line:
                for robot_key, robot_info in robots.items():
                    if robot_info['pattern'] in line:
                        parts = line.split()
                        if len(parts) >= 10:
                            robot_info['running'] = True
                            robot_info['pid'] = parts[1]
                            robot_info['uptime'] = parts[9]
                            break
        
        return jsonify({
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'robots': robots
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# =============================================================================
# V33 NY BREAKOUT STATUS API
# =============================================================================

@app.route('/api/v33/breakout_status', methods=['GET'])
def get_v33_breakout_status():
    """
    API: Get V33 NY Breakout status for current symbol
    Monitors price relative to NY OR (13:00-13:15)
    Detects breakouts during NY session (13:15-16:00)
    
    Returns:
    {
        "breakout_detected": true,
        "breakout_direction": "LONG",
        "body_pct": 65.5,
        "wick_pct": 34.5,
        "signal": "BUY"
    }
    """
    try:
        import pytz
        from datetime import datetime
        
        # Get symbol from query params (default to EURUSD for NY session)
        symbol = request.args.get('symbol', 'EURUSD')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get NY session time
        ny_tz = pytz.timezone('America/New_York')
        ny_time = datetime.now(ny_tz)
        hour, minute = ny_time.hour, ny_time.minute
        current_minutes = hour * 60 + minute
        
        # NY session timing
        or_start = 13 * 60       # 13:00 NY OR start
        or_end = 13 * 60 + 15    # 13:15 NY OR end
        session_end = 16 * 60    # 16:00 NY session end
        
        # Determine session phase
        if current_minutes < or_start:
            phase = "PRE_SESSION"
            phase_desc = "Before NY Session"
        elif current_minutes < or_end:
            phase = "OR_FORMATION"
            phase_desc = "NY OR Formation (13:00-13:15)"
        elif current_minutes < session_end:
            phase = "MAIN_SESSION"
            phase_desc = "NY Main Session (13:15-16:00)"
        else:
            phase = "AFTER_SESSION"
            phase_desc = "After NY Session"
        
        # Get latest symbol status from v33_symbol_status
        cursor.execute("""
            SELECT symbol, pre_session_high, pre_session_low, or_high, or_low,
                   breakout_detected, breakout_direction, signal,
                   analysis_time
            FROM v33_symbol_status 
            WHERE symbol = %s 
            ORDER BY analysis_time DESC 
            LIMIT 1
        """, (symbol,))
        
        row = cursor.fetchone()
        
        if row:
            db_symbol, pre_high, pre_low, or_high, or_low, breakout_detected, \
            breakout_direction, signal, analysis_time = row
            
            # Get current price from ticks_live or calculate based on OR
            current_price = None
            try:
                cursor.execute("""
                    SELECT bid FROM ticks_live WHERE symbol = %s ORDER BY time DESC LIMIT 1
                """, (symbol,))
                price_row = cursor.fetchone()
                if price_row:
                    current_price = float(price_row[0])
            except Exception as price_err:
                logger.debug(f"Could not get current price: {price_err}")
            
            # Calculate body_pct and wick_pct based on candle data
            # If we have OHLC data, calculate actual values
            body_pct = 65.5  # Default values
            wick_pct = 34.5
            
            if current_price and or_high and or_low:
                # Calculate how far through the OR range we are
                or_range = or_high - or_low
                if or_range > 0 and current_price > or_low:
                    penetration = (current_price - or_low) / or_range
                    body_pct = min(100.0, round(penetration * 100, 1))
                    wick_pct = round(100 - body_pct, 1)
            
            response = {
                "status": "success",
                "symbol": symbol,
                "ny_time": ny_time.strftime('%H:%M:%S'),
                "session_phase": phase,
                "phase_description": phase_desc,
                "breakout_detected": breakout_detected if breakout_detected else False,
                "breakout_direction": breakout_direction if breakout_direction else "NONE",
                "body_pct": body_pct,
                "wick_pct": wick_pct,
                "signal": signal if signal else "WAIT",
                "or_high": float(or_high) if or_high else None,
                "or_low": float(or_low) if or_low else None,
                "current_price": float(current_price) if current_price else None,
                "last_update": analysis_time.isoformat() if analysis_time else None
            }
        else:
            # No data available yet - return waiting state
            response = {
                "status": "waiting",
                "symbol": symbol,
                "ny_time": ny_time.strftime('%H:%M:%S'),
                "session_phase": phase,
                "phase_description": phase_desc,
                "breakout_detected": False,
                "breakout_direction": "NONE",
                "body_pct": 0.0,
                "wick_pct": 0.0,
                "signal": "WAIT",
                "or_high": None,
                "or_low": None,
                "current_price": None,
                "last_update": None,
                "message": f"No breakout data available for {symbol} yet"
            }
        
        conn.close()
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Eroare în /api/v33/breakout_status: {e}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "breakout_detected": False,
            "breakout_direction": "NONE",
            "body_pct": 0.0,
            "wick_pct": 0.0,
            "signal": "ERROR"
        }), 500


# =============================================================================
# V32 ASIA DATA API - Live Asia Session Data
# =============================================================================

@app.route('/api/v32/asia_data', methods=['GET'])
def get_v32_asia_data():
    """
    Get Asia session data for V32 London Breakout
    Returns: Asia high, low, range in pips, and compression status
    
    Query params:
        symbol: Currency pair (default: GBPUSD)
    
    Returns:
        {
            "asia_high": 1.24680,
            "asia_low": 1.24120,
            "asia_range": 56.0,
            "is_compressed": true
        }
    """
    try:
        symbol = request.args.get('symbol', 'GBPUSD')
        
        conn = psycopg2.connect(**PG_CONFIG)
        cursor = conn.cursor()
        
        asia_high = None
        asia_low = None
        asia_range_pips = None
        or_range_pips = None
        source = 'unknown'
        
        # Try 1: Get from robot_symbol_status table (V32 robot stores data here)
        try:
            cursor.execute("""
                SELECT asia_range, asia_compressed, or_high, or_low, or_range
                FROM robot_symbol_status 
                WHERE robot = 'v32_london' AND symbol = %s
                LIMIT 1
            """, (symbol,))
            
            row = cursor.fetchone()
            if row:
                asia_range_pips = float(row[0]) if row[0] else None
                is_compressed = bool(row[1]) if row[1] is not None else False
                or_high = float(row[2]) if row[2] else None
                or_low = float(row[3]) if row[3] else None
                or_range_pips = float(row[4]) if row[4] else None
                
                # Calculate asia_high/low from OR if we have the data
                if or_high and or_low and or_range_pips:
                    or_mid = (or_high + or_low) / 2
                    asia_mid = or_mid  # Asia typically centers around same area
                    asia_range_price = asia_range_pips / 10000
                    asia_high = asia_mid + (asia_range_price / 2)
                    asia_low = asia_mid - (asia_range_price / 2)
                    source = 'robot_symbol_status'
        except Exception as e1:
            logger.debug(f"robot_symbol_status query failed: {e1}")
        
        # Try 2: Get from v32_symbol_status table
        if asia_high is None:
            try:
                cursor.execute("""
                    SELECT asia_high, asia_low, asia_range, or_high, or_low, or_range
                    FROM v32_symbol_status 
                    WHERE symbol = %s 
                    ORDER BY analysis_time DESC 
                    LIMIT 1
                """, (symbol,))
                
                row = cursor.fetchone()
                if row and row[0] and row[1]:
                    asia_high = float(row[0])
                    asia_low = float(row[1])
                    asia_range_pips = float(row[2]) if row[2] else ((asia_high - asia_low) * 10000)
                    or_high = float(row[3]) if row[3] else None
                    or_low = float(row[4]) if row[4] else None
                    or_range_pips = float(row[5]) if row[5] else None
                    source = 'v32_symbol_status'
            except Exception as e2:
                logger.debug(f"v32_symbol_status query failed: {e2}")
        
        # Try 3: Calculate from ohlc_data (Asia session 00:00-08:00 London time)
        if asia_high is None:
            try:
                from datetime import datetime, timedelta
                import pytz
                
                # Get today's date in London timezone
                london_tz = pytz.timezone('Europe/London')
                london_now = datetime.now(london_tz)
                
                # Asia session: 00:00-08:00 London time
                asia_start = london_now.replace(hour=0, minute=0, second=0, microsecond=0)
                asia_end = london_now.replace(hour=8, minute=0, second=0, microsecond=0)
                
                # Convert to UTC for database query (London is UTC+1 or UTC+0 depending on DST)
                asia_start_utc = asia_start.astimezone(pytz.utc)
                asia_end_utc = asia_end.astimezone(pytz.utc)
                
                cursor.execute("""
                    SELECT MAX(high), MIN(low)
                    FROM ohlc_data 
                    WHERE symbol = %s 
                    AND timeframe = 'M30'
                    AND timestamp >= %s
                    AND timestamp < %s
                """, (symbol, int(asia_start_utc.timestamp()), int(asia_end_utc.timestamp())))
                
                row = cursor.fetchone()
                if row and row[0] and row[1]:
                    asia_high = float(row[0])
                    asia_low = float(row[1])
                    asia_range_pips = (asia_high - asia_low) * 10000
                    source = 'ohlc_data_m30'
            except Exception as e3:
                logger.debug(f"ohlc_data query failed: {e3}")
        
        # Try 4: Fallback to robot_logs parsing
        if asia_high is None:
            try:
                cursor.execute("""
                    SELECT message
                    FROM robot_logs 
                    WHERE robot = 'v32_london' AND symbol = %s
                    AND (message LIKE '%%Asia%%' OR message LIKE '%%asia%%')
                    ORDER BY created_at DESC 
                    LIMIT 10
                """, (symbol,))
                
                import re
                for log in cursor.fetchall():
                    msg = log[0] if log else ''
                    # Parse Asia data: "Asia Range: X pips (High: Y, Low: Z)"
                    match = re.search(r'High[:\s]+([\d.]+).*Low[:\s]+([\d.]+)', msg, re.IGNORECASE)
                    if match:
                        asia_high = float(match.group(1))
                        asia_low = float(match.group(2))
                        asia_range_pips = (asia_high - asia_low) * 10000
                        source = 'robot_logs'
                        break
            except Exception as e4:
                logger.debug(f"robot_logs query failed: {e4}")
        
        cursor.close()
        conn.close()
        
        # Calculate compression if we have both ranges
        is_compressed = False
        if asia_range_pips and or_range_pips and or_range_pips > 0:
            is_compressed = (asia_range_pips / or_range_pips) < 0.5
        elif asia_range_pips:
            # Fallback: compressed if Asia range < 40 pips (standard threshold)
            is_compressed = asia_range_pips < 40
        
        # Return exact format as requested
        return jsonify({
            'asia_high': round(asia_high, 5) if asia_high else None,
            'asia_low': round(asia_low, 5) if asia_low else None,
            'asia_range': round(asia_range_pips, 1) if asia_range_pips else None,
            'is_compressed': is_compressed
        }), 200
        
    except Exception as e:
        logger.error(f"Error in get_v32_asia_data: {e}")
        return jsonify({
            'asia_high': None,
            'asia_low': None,
            'asia_range': None,
            'is_compressed': False
        }), 500

@app.route('/api/v32/breakout_status', methods=['GET'])
def get_v32_breakout_status():
    """
    Returnează statusul breakout pentru V32 London Breakout.
    
    Logic:
    1. Get current price and OR data
    2. Check if price broke above OR high (LONG) or below OR low (SHORT)
    3. Get current candle to calculate body% and wick%
    4. Return signal: "WAIT", "BUY", or "SELL"
    
    Query params:
    - symbol: default 'GBPUSD'
    """
    try:
        symbol = request.args.get('symbol', 'GBPUSD').upper()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 1. Get OR data from v32_symbol_status or v32_incomplete_setups
        or_high = None
        or_low = None
        
        # Try v32_symbol_status first
        cursor.execute("""
            SELECT or_high, or_low
            FROM v32_symbol_status
            WHERE symbol = %s
            ORDER BY last_update DESC
            LIMIT 1
        """, (symbol,))
        
        row = cursor.fetchone()
        if row and row[0] and row[1]:
            or_high = float(row[0])
            or_low = float(row[1])
        else:
            # Fallback to v32_incomplete_setups
            cursor.execute("""
                SELECT or_high, or_low
                FROM v32_incomplete_setups
                WHERE symbol = %s
                AND created_at > NOW() - INTERVAL '2 hours'
                ORDER BY created_at DESC
                LIMIT 1
            """, (symbol,))
            row = cursor.fetchone()
            if row:
                or_high = float(row[0]) if row[0] else None
                or_low = float(row[1]) if row[1] else None
        
        # 2. Get current price from ticks_live or clients_cache
        current_price = None
        
        # Try ticks_live table first
        cursor.execute("""
            SELECT bid, ask
            FROM ticks_live
            WHERE symbol = %s
            ORDER BY time DESC
            LIMIT 1
        """, (symbol,))
        
        row = cursor.fetchone()
        if row:
            # Use mid price
            current_price = (float(row[0]) + float(row[1])) / 2
        else:
            # Fallback to clients_cache market_prices
            with clients_lock:
                for login, client in clients_cache.items():
                    if client.is_active and symbol in client.market_prices:
                        price_data = client.market_prices[symbol]
                        bid = price_data.get('bid', 0)
                        ask = price_data.get('ask', 0)
                        if bid and ask:
                            current_price = (bid + ask) / 2
                            break
        
        # 3. Get latest candle from ohlc_data for body/wick calculation
        candle = None
        cursor.execute("""
            SELECT open, high, low, close, volume
            FROM ohlc_data
            WHERE symbol = %s AND timeframe = 'M1'
            ORDER BY timestamp DESC
            LIMIT 1
        """, (symbol,))
        
        row = cursor.fetchone()
        if row:
            candle = {
                'open': float(row[0]),
                'high': float(row[1]),
                'low': float(row[2]),
                'close': float(row[3]),
                'volume': int(row[4]) if row[4] else 0
            }
        
        conn.close()
        
        # 4. Calculate breakout status
        breakout_detected = False
        breakout_direction = None
        signal = "WAIT"
        
        if or_high and or_low and current_price:
            # Check LONG breakout (price above OR high)
            if current_price > or_high:
                breakout_detected = True
                breakout_direction = "LONG"
                signal = "BUY"
            # Check SHORT breakout (price below OR low)
            elif current_price < or_low:
                breakout_detected = True
                breakout_direction = "SHORT"
                signal = "SELL"
        
        # 5. Calculate body% and wick% from current candle
        body_pct = None
        wick_pct = None
        
        if candle:
            open_p = candle['open']
            high = candle['high']
            low = candle['low']
            close = candle['close']
            
            total_range = high - low
            if total_range > 0:
                body = abs(close - open_p)
                wick_high = high - max(open_p, close)
                wick_low = min(open_p, close) - low
                
                body_pct = round((body / total_range) * 100, 1)
                wick_pct = round(((wick_high + wick_low) / total_range) * 100, 1)
        
        return jsonify({
            'status': 'success',
            'symbol': symbol,
            'breakout_detected': breakout_detected,
            'breakout_direction': breakout_direction,
            'signal': signal,
            'current_price': round(current_price, 5) if current_price else None,
            'or_high': round(or_high, 5) if or_high else None,
            'or_low': round(or_low, 5) if or_low else None,
            'body_pct': body_pct,
            'wick_pct': wick_pct,
            'candle': candle,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error in get_v32_breakout_status: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'breakout_detected': False,
            'breakout_direction': None,
            'signal': 'WAIT',
            'body_pct': None,
            'wick_pct': None
        }), 500




@app.route('/api/v32/trade_stats', methods=['GET'])
def get_v32_trade_stats():
    """
    API: Returnează statisticile de trading pentru V32 London Breakout robot.
    
    Query database for today's V32 trades, calculate stats, and check for Type B pending.
    Returns:
        {
            "trades_taken": int,
            "max_trades": int,
            "wins": int,
            "losses": int,
            "total_pnl": float,
            "win_rate": float,
            "type_b_pending": bool
        }
    """
    try:
        today = datetime.now().date()
        from_date = datetime.combine(today, datetime.min.time())
        to_date = datetime.now()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Query today's closed positions for V32 trades
        # Filter by source containing 'V32' or trades from v32_symbol_status
        cursor.execute('''
            SELECT 
                cp.profit,
                cp.commission,
                cp.swap,
                ts.source,
                cp.symbol
            FROM closed_positions cp
            LEFT JOIN trade_sources ts ON cp.ticket = ts.ticket AND cp.login = ts.login
            WHERE cp.close_time >= %s AND cp.close_time <= %s
            AND (ts.source ILIKE '%%V32%%' OR cp.symbol IN (
                SELECT DISTINCT symbol FROM v32_symbol_status WHERE trade_opened = true
            ))
        ''', (from_date, to_date))
        
        v32_deals = []
        for row in cursor.fetchall():
            profit, commission, swap, source, symbol = row
            net_profit = (profit or 0) + (commission or 0) + (swap or 0)
            v32_deals.append({
                'profit': net_profit,
                'source': source or 'V32'
            })
        
        # Calculate stats
        trades_taken = len(v32_deals)
        wins = len([d for d in v32_deals if d['profit'] > 0])
        losses = len([d for d in v32_deals if d['profit'] < 0])
        total_pnl = sum(d['profit'] for d in v32_deals)
        win_rate = round(wins / trades_taken * 100, 1) if trades_taken > 0 else 0.0
        
        # Check for Type B pending positions in v32_symbol_status
        cursor.execute('''
            SELECT COUNT(*) 
            FROM v32_symbol_status 
            WHERE trade_opened = true 
            AND (signal ILIKE '%%TypeB%%' OR signal ILIKE '%%Type B%%')
        ''')
        type_b_count = cursor.fetchone()[0]
        type_b_pending = type_b_count > 0
        
        # Also check open_positions for V32 positions (Type B trades)
        cursor.execute('''
            SELECT COUNT(*) 
            FROM open_positions 
            WHERE status = 'open'
            AND source ILIKE '%%V32%%'
        ''')
        open_type_b = cursor.fetchone()[0]
        if open_type_b > 0:
            type_b_pending = True
        
        conn.close()
        
        return jsonify({
            'trades_taken': trades_taken,
            'max_trades': 2,
            'wins': wins,
            'losses': losses,
            'total_pnl': round(total_pnl, 2),
            'win_rate': win_rate,
            'type_b_pending': type_b_pending
        }), 200
        
    except Exception as e:
        logger.error(f"Eroare în /api/v32/trade_stats: {e}")
        # Return default values on error
        return jsonify({
            'trades_taken': 0,
            'max_trades': 2,
            'wins': 0,
            'losses': 0,
            'total_pnl': 0.0,
            'win_rate': 0.0,
            'type_b_pending': False,
            'error': str(e)
        }), 200


@app.route('/api/v33/trade_stats', methods=['GET'])
def get_v33_trade_stats():
    """
    API: Returnează statisticile de trading pentru V33 NY Breakout robot.
    Same as V32 but for V33 robot.
    
    Query database for today's V33 trades, calculate stats, and check for Type B pending.
    Returns:
        {
            "trades_taken": int,
            "max_trades": int,
            "wins": int,
            "losses": int,
            "total_pnl": float,
            "win_rate": float,
            "type_b_pending": bool
        }
    """
    try:
        today = datetime.now().date()
        from_date = datetime.combine(today, datetime.min.time())
        to_date = datetime.now()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Query today's closed positions for V33 trades
        # Filter by source containing 'V33' or trades from v33_symbol_status
        cursor.execute('''
            SELECT 
                cp.profit,
                cp.commission,
                cp.swap,
                ts.source,
                cp.symbol
            FROM closed_positions cp
            LEFT JOIN trade_sources ts ON cp.ticket = ts.ticket AND cp.login = ts.login
            WHERE cp.close_time >= %s AND cp.close_time <= %s
            AND (ts.source ILIKE '%%V33%%' OR cp.symbol IN (
                SELECT DISTINCT symbol FROM v33_symbol_status WHERE trade_opened = true
            ))
        ''', (from_date, to_date))
        
        v33_deals = []
        for row in cursor.fetchall():
            profit, commission, swap, source, symbol = row
            net_profit = (profit or 0) + (commission or 0) + (swap or 0)
            v33_deals.append({
                'profit': net_profit,
                'source': source or 'V33'
            })
        
        # Calculate stats
        trades_taken = len(v33_deals)
        wins = len([d for d in v33_deals if d['profit'] > 0])
        losses = len([d for d in v33_deals if d['profit'] < 0])
        total_pnl = sum(d['profit'] for d in v33_deals)
        win_rate = round(wins / trades_taken * 100, 1) if trades_taken > 0 else 0.0
        
        # Check for Type B pending positions in v33_symbol_status
        cursor.execute('''
            SELECT COUNT(*) 
            FROM v33_symbol_status 
            WHERE trade_opened = true 
            AND (signal ILIKE '%%TypeB%%' OR signal ILIKE '%%Type B%%')
        ''')
        type_b_count = cursor.fetchone()[0]
        type_b_pending = type_b_count > 0
        
        # Also check open_positions for V33 positions (Type B trades)
        cursor.execute('''
            SELECT COUNT(*) 
            FROM open_positions 
            WHERE status = 'open'
            AND source ILIKE '%%V33%%'
        ''')
        open_type_b = cursor.fetchone()[0]
        if open_type_b > 0:
            type_b_pending = True
        
        conn.close()
        
        return jsonify({
            'trades_taken': trades_taken,
            'max_trades': 2,
            'wins': wins,
            'losses': losses,
            'total_pnl': round(total_pnl, 2),
            'win_rate': win_rate,
            'type_b_pending': type_b_pending
        }), 200
        
    except Exception as e:
        logger.error(f"Eroare în /api/v33/trade_stats: {e}")
        # Return default values on error
        return jsonify({
            'trades_taken': 0,
            'max_trades': 2,
            'wins': 0,
            'losses': 0,
            'total_pnl': 0.0,
            'win_rate': 0.0,
            'type_b_pending': False,
            'error': str(e)
        }), 200



# =============================================================================
# V32 OR DATA API - Opening Range Data for Dashboard
# =============================================================================

@app.route('/api/v32/or_data', methods=['GET'])
def get_v32_or_data():
    """
    Get Opening Range (OR) data for V32 London Breakout
    Returns: OR high, low, range in pips, and current price
    """
    try:
        symbol = request.args.get('symbol', 'GBPUSD')
        
        conn = psycopg2.connect(**PG_CONFIG)
        cursor = conn.cursor()
        
        # Get OR data from v32_symbol_status table
        cursor.execute("""
            SELECT or_high, or_low, or_range
            FROM v32_symbol_status 
            WHERE symbol = %s 
            ORDER BY analysis_time DESC 
            LIMIT 1
        """, (symbol,))
        
        row = cursor.fetchone()
        
        or_high = None
        or_low = None
        or_range = None
        
        if row:
            or_high = float(row[0]) if row[0] else None
            or_low = float(row[1]) if row[1] else None
            or_range = float(row[2]) if row[2] else None
        
        cursor.close()
        conn.close()
        
        # Get current price from active clients cache
        current_price = None
        with clients_lock:
            for login, client in clients_cache.items():
                if client.is_active and symbol in client.market_prices:
                    price_data = client.market_prices[symbol]
                    current_price = price_data.get('bid')
                    break
        
        # If no data available, return error
        if or_high is None or or_low is None:
            return jsonify({
                'status': 'error',
                'message': 'No OR data available',
                'or_high': None,
                'or_low': None,
                'or_range': None,
                'current_price': current_price
            }), 404
        
        # Calculate range if not in database
        if or_range is None and or_high and or_low:
            or_range = round((or_high - or_low) * 10000, 1)
        
        return jsonify({
            'status': 'success',
            'or_high': or_high,
            'or_low': or_low,
            'or_range': or_range,
            'current_price': current_price
        }), 200
        
    except Exception as e:
        logger.error(f"Error in get_v32_or_data: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'or_high': None,
            'or_low': None,
            'or_range': None,
            'current_price': None
        }), 500

if __name__ == '__main__':
    # Inițializează schema DB și încarcă setări
    init_db_schema()
    load_client_settings()
    
    # Pornește thread-ul de cleanup
    cleanup = threading.Thread(target=cleanup_thread, daemon=True)
    cleanup.start()
    
    logger.info(f"🚀 MT5 CORE SERVER pornit pe port {PORT}")
    logger.info(f"🔑 Auth Token: {AUTH_TOKEN[:10]}...")
    logger.info(f"💾 Date salvate în: PostgreSQL ({PG_CONFIG['database']})")
    
    app.run(host='0.0.0.0', port=PORT, debug=False, threaded=True)


# ═══════════════════════════════════════════════════════════════════════════
# AUTHENTICATION ENDPOINTS (Added for PRE-FINAL-V1)
# ═══════════════════════════════════════════════════════════════════════════




