# BUG-010: V33 Session Timer Logic

## Informații Generale
| Atribut | Valoare |
|---------|---------|
| **ID** | BUG-010 |
| **Severitate** | MEDIUM |
| **Status** | OPEN |
| **Data descoperirii** | 2026-03-28 |
| **Raportat de** | QA-Master Agent |

## Descriere
Similar cu BUG-009, timer-ul pentru sesiunea V33 (NY) folosește logica locală în browser în loc să citească starea reală de la API.

## Cod Problematic
```javascript
// dashboard_functional.js
function updateV33SessionTimer(nyTime) {
    if (!nyTime) {
        const now = new Date();
        nyTime = new Date(now.toLocaleString("en-US", {timeZone: "America/New_York"}));
    }
    
    const hour = nyTime.getHours();
    const minute = nyTime.getMinutes();
    // ... calcul local
}
```

## Probleme
1. Calcul local bazat pe timpul browser-ului
2. Posibile inconsistențe cu starea reală a robotului
3. Nu reflectă dacă robotul este activ sau nu

## Soluție Propusă
Vezi BUG-009 - aceeași soluție aplicată pentru V33.

## Verificare După Fix
1. Timer-ul V33 ar trebui sincronizat cu robotul
2. Faza sesiunii NY ar trebui corectă

## Referințe
- Depinde de: BUG-004, BUG-009
- Fișier raport: TEST-CASES-COMPLETE-REPORT.md
