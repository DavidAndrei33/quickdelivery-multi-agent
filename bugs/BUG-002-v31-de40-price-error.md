# BUG-002: V31 Eroare Analiză DE40 - Variabilă 'price' not defined

**Reporter:** QA-Master  
**Data:** 2026-03-28 16:52 UTC  
**Severitate:** Medium  
**Prioritate:** P2  
**Status:** Open  
**Robot:** V31 Marius TPL

---

## Environment
- **Robot:** V31 Marius TPL Live
- **File:** `/root/clawd/agents/brainmaker/v31_marius_live.py`
- **Log:** `/var/log/v31_marius_live.log`
- **Symbol Afectat:** DE40

---

## Descriere
Robotul V31 generează o eroare în log atunci când încearcă să analizeze simbolul DE40. Eroarea indică o variabilă 'price' care nu este definită.

---

## Log Eroare
```
2026-03-28 16:49:46,541 | ERROR    | ❌ Eroare analiză DE40: name 'price' is not defined
```

---

## Pași Reproducere
1. Pornește V31 Marius TPL
2. Așteaptă primul ciclu de analiză
3. Verifică log-urile în `/var/log/v31_marius_live.log`
4. Observă eroarea pentru simbolul DE40

---

## Expected Result
Analiza DE40 ar trebui să se completeze fără erori, similar cu alte simboluri.

## Actual Result
```
ERROR | ❌ Eroare analiză DE40: name 'price' is not defined
```

---

## Impact
- Simbolul DE40 nu este analizat corect
- Scorul și decizia de tranzacționare nu sunt calculate
- Robotul continuă cu alte simboluri (fail-soft)

---

## Root Cause (Suspected)
În funcția de analiză a simbolurilor, variabila 'price' este folosită fără să fie definită înainte pentru simbolul DE40. Posibilă cauză:
- DE40 are un format de date diferit (indice vs forex)
- Variabila 'price' nu este inițializată pentru indici
- Eroare de typo în cod

---

## Recomandare Fix
1. Verifică funcția de analiză în `v31_marius_live.py`
2. Adaugă inițializare explicită pentru variabila 'price'
3. Adaugă handling specific pentru indici (DE40, US30, etc.)
4. Adaugă try-catch pentru fiecare simbol în parte

```python
# Sugestie fix:
try:
    price = get_current_price(symbol)
    if price is None:
        logger.warning(f"No price for {symbol}")
        continue
    # ... restul analizei
except Exception as e:
    logger.error(f"Error analyzing {symbol}: {e}")
    continue
```

---

## Test de Validare
```bash
# După fix, verifică log-urile
tail -f /var/log/v31_marius_live.log | grep DE40
# Ar trebui să NU mai apară eroarea
```

---

## Assignment
**Assigned to:** builder-1  
**ETA:** 1-2 ore
