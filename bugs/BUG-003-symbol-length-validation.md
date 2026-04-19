# BUG-003: Lipsă validare lungime simbol

**Reporter:** QA-Master  
**Data:** 2026-03-28 16:05 UTC  
**Severitate:** Medium  
**Prioritate:** P2  
**Status:** Open

## Environment
- **URL:** http://localhost:8001/api/symbol_analysis
- **Endpoint:** GET /api/symbol_analysis?symbol={value}
- **OS:** Ubuntu 22.04

## Descriere
Parametrul `symbol` nu are limită de lungime validată. Am trimis un simbol de 1000+ caractere și a fost acceptat fără eroare.

## Pași Reproducere
1. Execută: `curl "http://localhost:8001/api/symbol_analysis?symbol=AAAA...(1000 caractere)"`
2. Observă că returnează HTTP 200 în loc de 400 Bad Request

## Expected Result
HTTP 400 cu mesaj: "Symbol too long (max 20 characters)"

## Actual Result
HTTP 200 cu simbolul acceptat în întregime

## Network
```
Request: GET /api/symbol_analysis?symbol=AAA...(1000 chars)
Response: 200 OK
```

## Impact
- Posibile probleme de performanță
- UI poate fi afectat (text overflow)
- Bloat în loguri și baza de date

## Recomandare Fix
Adaugă validare în mt5_core_server.py:
```python
if len(symbol) > 20:
    return jsonify({"error": "Symbol too long", "status": "error"}), 400
```

## Test de Validare
```bash
curl -s "http://localhost:8001/api/symbol_analysis?symbol=VERYLONGSYMBOLNAME12345" | grep "error"
```
