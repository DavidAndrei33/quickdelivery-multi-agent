# PORT ALLOCATION - Document Oficial
## Trading Dashboard Multi-Agent System

**Ultima actualizare:** 2026-04-06
**Responsabil:** DevOps-Engineer + Builder-Core

---

## 🎯 REGULI STRICTE

1. **NICIODATĂ** nu pornești un serviciu pe un port ocupat
2. **ÎNTOTDEAUNA** verifici înainte: `netstat -tlnp | grep PORT`
3. **DOCUMENTEZI** orice schimbare de port

---

## 📊 PORTURI ALOCATE

| Port | Serviciu | Responsabil | Status | Descriere |
|------|----------|-------------|--------|-----------|
| **8001** | MT5 Core Server | Builder-Core | 🔴 CRITIC | Main API + Dashboard HTTP |
| **8000** | Backend API (intern) | Builder-Core | 🟡 Intern | API intern Docker |
| **8080** | Legacy Bridge | - | 🟡 Legacy | local_bridge.py (opțional) |
| **7001** | Local Bridge (PC) | - | 🟡 Local | Pe PC-ul Andrei, nu pe VPS |
| **5432** | PostgreSQL | DevOps-Engineer | 🔴 CRITIC | Baza de date |
| **6379** | Redis | DevOps-Engineer | 🟡 Cache | Cache și sessions |
| **3000** | Grafana | DevOps-Engineer | 🟢 Disponibil | Monitoring dashboard |
| **9090** | Prometheus | DevOps-Engineer | 🟢 Disponibil | Metrics collection |
| **80** | HTTP (redirect) | DevOps-Engineer | 🟡 Standard | Redirect to 8001 |
| **443** | HTTPS | DevOps-Engineer | 🟢 Disponibil | SSL (viitor) |

---

## 🚨 CONFLICTE RECENTE

### Problema: 2026-04-06
- **Conflict:** `mt5_server_v2.py` ocupa portul 8001
- **Blocat:** MT5 Core Server nu putea porni
- **Eroare:** Dashboard "Not Found"
- **Soluție:** Oprit serverul vechi, restartat cel corect

### Prevenție:
```bash
# Înainte de a porni orice server pe 8001:
sudo netstat -tlnp | grep 8001

# Dacă apare ceva, oprește:
sudo kill -9 PID

# Apoi pornește:
python mt5_core_server.py --port 8001
```

---

## 📝 CHECKLIST PRE-DEPLOY

### Pentru Builder-Core (înainte de start server):
- [ ] Verific portul nu e ocupat: `netstat -tlnp | grep 8001`
- [ ] Verific codul folosește portul corect (8001)
- [ ] Verific nu există alte instanțe: `ps aux | grep python | grep -v grep`
- [ ] Start server cu logging
- [ ] Testează: `curl http://localhost:8001/health`
- [ ] Notifică Andrei: "Server pornit pe portul X"

### Pentru DevOps-Engineer (înainte de docker-compose):
- [ ] Verific porturile din docker-compose.yml
- [ ] Verific nu există conflicte cu servicii existente
- [ ] Documentezi orice port modificat în PORT_ALLOCATION.md
- [ ] Testează fiecare serviciu individual
- [ ] Testează integrarea completă

---

## 🔧 SCRIPT VERIFICARE AUTOMATĂ

### check_ports.sh
```bash
#!/bin/bash
echo "🔍 Verificare porturi..."

PORTS=(8001 5432 6379 3000 9090)

for PORT in "${PORTS[@]}"; do
    PID=$(lsof -ti:$PORT 2>/dev/null)
    if [ ! -z "$PID" ]; then
        PROCESS=$(ps -p $PID -o comm= 2>/dev/null)
        echo "⚠️  Port $PORT ocupat de: $PROCESS (PID: $PID)"
    else
        echo "✅ Port $PORT liber"
    fi
done
```

---

## 📞 CONTACT

- **Probleme porturi:** @DevOpsEngineerBot
- **Probleme cod server:** @BuilderCoreBot
- **Decizii arhitectură:** @Andrei

---

**Notă:** Orice agent care pornește un serviciu pe un port ocupat fără verificare prealabilă este responsabil pentru downtime!
