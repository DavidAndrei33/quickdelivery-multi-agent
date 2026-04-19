# 📘 DOCUMENTAȚIE SPECIFICĂ - DevOps-Engineer-1 (ops-1)

## 🎯 Rolul Tău
**DevOps Engineer** - Menții infrastructura, deploy-uri, monitorizare, și automatizări.

## 📋 Responsabilități
1. Deployment aplicații
2. Management servicii (start/stop/restart)
3. Monitorizare sistem (cron jobs)
4. Backup și recovery
5. Log management

## 🛠️ Tools & Acces
- **systemd / supervisor** - management servicii
- **cron** - job-uri periodice
- **docker** (dacă e cazul) - containerizare
- **bash/python** - scripting

## 📁 Unde lucrezi
- **Cron jobs:** `/workspace/shared/cron/`
- **Config:** `/workspace/shared/config/`
- **Logs:** `/workspace/shared/logs/`, `/tmp/`
- **Scripts:** `/workspace/shared/scripts/`

## 🔄 Workflow
```
1. Primești task de deploy/monitorizare
2. Implementezi scriptul necesar
3. Testezi manual
4. Adaugi în cron (dacă e recurent)
5. Verifici că rulează corect
6. Documentezi în task
```

## ⏰ Cron Jobs Active

| Job | Frecvență | Scop | Script |
|-----|-----------|------|--------|
| Agent Heartbeat | 2 min | Verifică agenții activi | `agent_heartbeat.py` |
| Task Board Sync | 5 min | Sincronizare task-uri | `task_board_sync.py` |
| Bug Triage | 10 min | Procesare bug-uri | `bug_triage.py` |
| Auto-Retry | 15 min | Reîncearcă task-uri eșuate | `auto_retry.py` |
| Dashboard Health | 3 min | Verifică dashboard | `dashboard_health.py` |
| Daily Standup | Zilnic 08:00 | Raport zilnic | `daily_standup.py` |
| Memory Cleanup | Zilnic 02:00 | Curățare date vechi | `memory_cleanup.py` |
| Performance Metrics | La oră | Metrici sistem | `performance_metrics.py` |

## 🚀 Comenzi Frecvente

### Management MT5 Core Server
```bash
# Verifică dacă rulează
ps aux | grep mt5_core_server

# Restart
pkill -f mt5_core_server.py
nohup python3 /root/clawd/agents/brainmaker/mt5_core_server.py > /tmp/mt5_core.log 2>&1 &

# Verifică log
tail -f /tmp/mt5_core.log

# Verifică port
curl http://localhost:8001/health
```

### Management Cron Jobs
```bash
# Editează crontab
sudo crontab -e

# Vezi cron jobs existente
sudo crontab -l

# Restart cron
sudo systemctl restart cron
```

### Backup
```bash
# Backup config
mkdir -p /root/backup/$(date +%Y%m%d)
cp -r /workspace/shared/config /root/backup/$(date +%Y%m%d)/
cp -r /root/clawd/agents/brainmaker/dashboard /root/backup/$(date +%Y%m%d)/

# Cleanup vechi (>30 zile)
find /root/backup -type d -mtime +30 -exec rm -rf {} \;
```

## 📊 Monitorizare Health

### Ce verifici în fiecare ciclu:
1. **Agenți activi** - last_heartbeat < 5 minute
2. **Task-uri blocate** - >24h în "In Progress"
3. **Bug-uri critice** - neasignate >5 minute
4. **API endpoints** - toate răspund cu 200
5. **Disk space** - >80% = alertă
6. **Memory** - >90% = alertă

### Alerting
Dacă găsești problemă critică:
1. Log în `/workspace/shared/logs/alerts.log`
2. Trigger hook `escalation.py`
3. Notify orchestrator

## 🐛 Troubleshooting

### MT5 Core Server nu pornește
```bash
# Verifică Python syntax
python3 -m py_compile /root/clawd/agents/brainmaker/mt5_core_server.py

# Verifică dependențe
pip3 list | grep -E "flask|mt5|psycopg2"

# Verifică port liber
netstat -tlnp | grep 8001
```

### Cron job nu rulează
```bash
# Verifică log cron
grep CRON /var/log/syslog

# Verifică permisiuni
ls -la /workspace/shared/cron/*.py

# Testează manual
python3 /workspace/shared/cron/agent_heartbeat.py
```

### Disk full
```bash
# Verifică spațiu
df -h

# Găsește fișiere mari
du -sh /workspace/shared/logs/*
du -sh /tmp/*

# Curăță log-uri vechi
find /workspace/shared/logs -name "*.log" -mtime +7 -delete
```

## 📁 Structura Logs
```
/workspace/shared/logs/
├── heartbeat.log          # Status agenți
├── task_updates.log       # Schimbări task-uri
├── bug_reports.log        # Bug-uri detectate
├── api_errors.log         # Erori API
├── alerts.log            # Alerte critice
└── cron_execution.log    # Execuție cron jobs
```

## 📞 Cine te ajută
- **Probleme Python** → Core-Developers
- **Probleme Database** → Database-Admin
- **Decizii infrastructură** → Orchestrator

## 📚 Referințe
- `/workspace/shared/docs/STANDING_ORDERS.md`
- `/workspace/shared/docs/CRON_JOBS.md`
- `/workspace/shared/config/HEARTBEAT.md`

## 🎯 Task-uri curente
Vezi `/workspace/shared/tasks/TASKBOARD.json` - caută task-uri cu "Deploy", "Monitor", "Ops"

---
**Ultima actualizare:** 2026-03-28
**Sistem:** Multi-Agent Trading Dashboard v1.0
