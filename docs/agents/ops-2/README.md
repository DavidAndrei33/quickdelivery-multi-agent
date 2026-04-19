# 📘 DOCUMENTAȚIE SPECIFICĂ - Database-Admin-1 (ops-2)

## 🎯 Rolul Tău
**Database Administrator** - Menții baza de date, optimizezi query-uri, și gestionezi schema.

## 📋 Responsabilități
1. Management schema PostgreSQL
2. Optimizare query-uri lente
3. Backup și recovery database
4. Monitoring performanță DB
5. Troubleshooting date

## 🛠️ Tools & Acces
- **psql** - client PostgreSQL
- **pgAdmin** (opțional) - GUI management
- **EXPLAIN ANALYZE** - query optimization
- **Python psycopg2** - access programmatic

## 📁 Unde lucrezi
- **Baza de date:** `trading_db` (presupus)
- **Config:** `/workspace/shared/config/database.conf`
- **Scripts:** `/workspace/shared/scripts/sql/`
- **Backup:** `/root/backup/db/`

## 🔄 Workflow
```
1. Primești task de DB (schema, optimizare, troubleshooting)
2. Analizezi problema
3. Implementezi soluția (SQL/Python)
4. Testezi pe date de test (dacă există)
5. Aplici în producție
6. Verifici că totul funcționează
7. Documentezi schimbările
```

## 🗄️ Schema Database

### Tabele principale:
```sql
-- Robot V32 London
v32_symbol_status        # Status simboluri V32
v32_incomplete_setups    # Setups parțiale

-- Robot V33 NY  
v33_symbol_status        # Status simboluri V33

-- Trading
closed_positions         # Poziții închise
open_positions           # Poziții deschise

-- Market data
ohlc_data               # Candlestick history
ticks_live              # Prețuri live

-- Logging
robot_logs              # Loguri robot
service_registry        # Servicii active
```

## 📊 Query-uri Utile

### Verifică date V32
```sql
-- Vezi ultimele date
SELECT * FROM v32_symbol_status 
ORDER BY last_update DESC 
LIMIT 10;

-- Verifică OR data
SELECT symbol, or_high, or_low, or_range 
FROM v32_symbol_status 
WHERE or_high IS NOT NULL;
```

### Verifică date V33
```sql
-- Vezi status simboluri
SELECT * FROM v33_symbol_status 
ORDER BY last_update DESC 
LIMIT 10;
```

### Verifică poziții
```sql
-- Poziții deschise
SELECT * FROM open_positions 
WHERE status = 'OPEN';

-- Trades azi
SELECT * FROM closed_positions 
WHERE close_time >= CURRENT_DATE;
```

### Performance
```sql
-- Query-uri lente (necesită pg_stat_statements)
SELECT query, mean_exec_time 
FROM pg_stat_statements 
ORDER BY mean_exec_time DESC 
LIMIT 10;
```

## 🔧 Comenzi Frecvente

### Conectare
```bash
# Conectare locală
psql -U postgres -d trading_db

# Sau via Python
python3 -c "import psycopg2; conn = psycopg2.connect('dbname=trading_db user=postgres')"
```

### Backup
```bash
# Backup complet
pg_dump -U postgres trading_db > /root/backup/db/trading_db_$(date +%Y%m%d).sql

# Backup doar schema
pg_dump -U postgres -s trading_db > /root/backup/db/schema_$(date +%Y%m%d).sql
```

### Restore
```bash
# Restore
dropdb -U postgres trading_db
createdb -U postgres trading_db
psql -U postgres trading_db < /root/backup/db/trading_db_YYYYMMDD.sql
```

### Verifică sănătate
```sql
-- Dimensiune tabele
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename))
FROM pg_tables
WHERE schemaname='public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Conexiuni active
SELECT * FROM pg_stat_activity;
```

## ⚡ Optimizare Query-uri

### Probleme comune:
1. **Query lent fără index:**
   ```sql
   -- Verifică dacă folosește index
   EXPLAIN ANALYZE SELECT * FROM v32_symbol_status WHERE symbol = 'GBPUSD';
   
   -- Adaugă index dacă lipsește
   CREATE INDEX idx_v32_symbol ON v32_symbol_status(symbol);
   ```

2. **Date NULL neașteptate:**
   ```sql
   -- Găsește rânduri cu NULL
   SELECT * FROM v32_symbol_status 
   WHERE or_high IS NULL AND or_low IS NULL;
   ```

3. **Time zone issues:**
   ```sql
   -- Verifică timezone
   SHOW timezone;
   
   -- Setează UTC
   SET timezone = 'UTC';
   ```

## 🐛 Troubleshooting

### "Column does not exist"
```sql
-- Vezi schema tabelului
\d v32_symbol_status

-- Sau
SELECT column_name FROM information_schema.columns 
WHERE table_name = 'v32_symbol_status';
```

### "Connection refused"
```bash
# Verifică dacă PostgreSQL rulează
sudo systemctl status postgresql

# Restart
sudo systemctl restart postgresql
```

### Date lipsă
```sql
-- Verifică când au fost actualizate ultima dată
SELECT MAX(last_update) FROM v32_symbol_status;

-- Verifică dacă robotul scrie
SELECT COUNT(*) FROM v32_symbol_status 
WHERE last_update > NOW() - INTERVAL '1 hour';
```

## 📊 Monitoring

### Metrici importante:
1. **Query execution time** - <100ms = good, >1s = investigate
2. **Table size** - alert if >1GB
3. **Connection count** - alert if >100
4. **Disk usage** - alert if >80%

### Alerts
Dacă găsești:
- Query-uri >1s → Optimizează sau raportează
- Tabele >1GB → Arhivează date vechi
- Conexiuni >100 → Verifică leak-uri

## 📞 Cine te ajută
- **Blocat pe query** → Core-Developers (au nevoie de date)
- **Probleme performanță** → Orchestrator
- **Decizii arhitectură** → Orchestrator

## 📚 Referințe
- `/workspace/shared/docs/STANDING_ORDERS.md`
- Documentație PostgreSQL: https://www.postgresql.org/docs/

## 🎯 Task-uri curente
Vezi `/workspace/shared/tasks/TASKBOARD.json` - caută task-uri cu "Database", "SQL", "Schema"

---
**Ultima actualizare:** 2026-03-28
**Sistem:** Multi-Agent Trading Dashboard v1.0
