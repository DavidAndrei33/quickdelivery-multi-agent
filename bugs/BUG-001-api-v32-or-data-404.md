# BUG-001: /api/v32/or_data returnează HTTP 404

**Reporter:** QA-Master  
**Data:** 2026-03-28 15:52 UTC  
**Severitate:** High  
**Prioritate:** P1  
**Status:** Open

## Environment
- **URL:** http://localhost:8001/api/v32/or_data
- **Browser:** N/A (API Test)
- **OS:** Ubuntu 22.04
- **Server:** MT5 Core Server (port 8001)

## Descriere
Endpoint-ul `/api/v32/or_data` returnează HTTP 404 cu status "error" în loc să returneze datele Opening Range pentru V32 London Breakout robot.

## Pași Reproducere
1. Pornește MT5 Core Server
2. Execută: `curl -s http://localhost:8001/api/v32/or_data`
3. Observă rezultatul

## Expected Result
HTTP 200 cu date OR valide:
```json
{
  "status": "success",
  "or_high": <value>,
  "or_low": <value>,
  "or_range": <value>,
  ...
}
```

## Actual Result
HTTP 404 cu:
```json
{
  "current_price": 1.32679,
  "message": "No OR data available",
  "or_high": null,
  "or_low": null,
  "or_range": null,
  "status": "error"
}
```

## Network
```
Request: GET /api/v32/or_data
Response: 404 Not Found
Time: 0.019s
```

## Impact
Dashboard-ul V32 nu poate afișa datele Opening Range, afectând funcționalitatea analizei.

## Recomandare Fix
Verifică dacă:
1. Endpoint-ul e înregistrat corect în Flask
2. Datele OR sunt salvate în cache/DB
3. Robotul V32 a generat date OR

## Test de Validare
```bash
curl -s http://localhost:8001/api/v32/or_data | grep "status.*success"
```
