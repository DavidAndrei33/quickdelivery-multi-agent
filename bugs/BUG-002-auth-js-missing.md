# BUG-002: auth.js lipsește din directorul dashboard

**Reporter:** QA-Master  
**Data:** 2026-03-28 16:02 UTC  
**Severitate:** High  
**Prioritate:** P1  
**Status:** Open

## Environment
- **URL:** http://localhost:8001/auth.js
- **Dashboard Path:** /workspace/shared/agents/dashboard/
- **OS:** Ubuntu 22.04
- **Server:** MT5 Core Server (port 8001)

## Descriere
Serverul încearcă să servească auth.js din DASHBOARD_DIR (/workspace/shared/agents/dashboard/), dar acest director nu există sau nu conține auth.js. Serverul are un fallback care returnează cod JS generat, dar ar putea cauza probleme de consistență.

## Pași Reproducere
1. Verifică existența directorului: `ls /workspace/shared/agents/dashboard/`
2. Sau: `curl http://localhost:8001/auth.js`

## Expected Result
Fișierul auth.js ar trebui să existe în /workspace/shared/agents/dashboard/

## Actual Result
```
DASHBOARD_DIR = /workspace/shared/agents/dashboard (nu există)
```

## Network
```
Request: GET /auth.js
Response: 200 (cu cod generat din Python, nu din fișier)
```

## Impact
Autentificarea funcționează prin fallback, dar:
- Codul e încorporat în Python, greu de modificat
- Nu există consistență între fișierele static
- Posibile erori la deployment

## Recomandare Fix
1. Creează /workspace/shared/agents/dashboard/
2. Copiază auth.js, index.html, dashboard_functional.js acolo
3. Sau modifică DASHBOARD_DIR să pointeze la locația corectă

## Test de Validare
```bash
ls -la /workspace/shared/agents/dashboard/auth.js
```
