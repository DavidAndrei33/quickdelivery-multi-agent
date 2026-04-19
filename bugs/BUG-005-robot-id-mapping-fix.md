# BUG-005: Robot Start/Stop nu funcționează - ID mapping greșit

**Reporter:** Manifest (detectat prin testare utilizator)
**Data:** 2026-03-28 16:40 UTC
**Severitate:** High
**Prioritate:** P1
**Status:** FIXED ✅

## Environment
- **URL:** http://46.225.57.93:8001/dashboard
- **File:** dashboard_functional.js (controlRobot function)
- **Browser:** Any
- **OS:** Ubuntu 22.04

## Descriere
Funcția `controlRobot()` din dashboard_functional.js mapează greșit ID-urile roboților. Frontend-ul trimite `v31`, `v32`, `v33` la API, dar API-ul așteaptă `v31_tpl`, `v32_london`, `v33_ny`.

## Pași Reproducere
1. Deschide dashboard
2. Selectează V31 din dropdown
3. Apasă butonul "Start"
4. Observă eroarea în consolă: "Unknown robot" sau 404

## Cod Problematic (Înainte)
```javascript
const robotApiMap = {
    'v31_marius': 'v31',  // ❌ Greșit! API așteaptă 'v31_tpl'
    'v32_london': 'v32',  // ❌ Greșit! API așteaptă 'v32_london'
    'v33_ny': 'v33'       // ❌ Greșit! API așteaptă 'v33_ny'
};
```

## Fix Aplicat
```javascript
const robotApiMap = {
    'v31_tpl': 'v31_tpl',       // ✅ Corect
    'v32_london': 'v32_london', // ✅ Corect
    'v33_ny': 'v33_ny'          // ✅ Corect
};

// Fallback pentru alte variații
if (!apiId) {
    if (robotId.includes('v31')) apiId = 'v31_tpl';
    else if (robotId.includes('v32')) apiId = 'v32_london';
    else if (robotId.includes('v33')) apiId = 'v33_ny';
}
```

## Verificare Fix
```bash
curl -X POST http://localhost:8001/api/robot/v31_tpl/start
# Response: {"status": "success", "message": "v31_tpl started"}
```

## Impact
- Utilizatorii nu puteau porni/opri roboții din dashboard
- Funcționalitate critică nefuncțională

## Test de Validare
1. Deschide dashboard (v24)
2. Selectează V31
3. Apasă Start → ar trebui să meargă
4. Verifică în consolă: "v31_tpl started successfully"

## Fișiere Modificate
- `/root/clawd/agents/brainmaker/dashboard/dashboard_functional.js` (liniile ~2885-2895)
- `/root/clawd/agents/brainmaker/dashboard/index.html` (cache bust v24)
