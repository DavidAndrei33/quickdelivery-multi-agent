# BUG-007: Symbol Grid Not Populated

## Informații Generale
| Atribut | Valoare |
|---------|---------|
| **ID** | BUG-007 |
| **Severitate** | MEDIUM |
| **Status** | OPEN |
| **Data descoperirii** | 2026-03-28 |
| **Raportat de** | QA-Master Agent |

## Descriere
Grid-ul de simboluri (`#robotSymbolsGrid`) nu este populat cu date deoarece API-ul nu returnează lista de simboluri.

## Cauză Rădăcină
BUG-004 - Endpoint-urile API pentru datele roboților nu sunt implementate.

## Elemente Afectate
- `#robotSymbolsGrid` - rămâne cu mesajul "Se încarcă..."
- Click pe simbol nu funcționează (nu există simboluri de click)
- Nu se pot vedea cele 32 de simboluri pentru V31

## Cod Afectat
```javascript
// dashboard_functional.js
function updateV31SymbolGrid(symbols) {
    const gridEl = document.getElementById('v31SymbolGrid');
    // ...
    gridEl.innerHTML = displaySymbols.map(sym => {
        // ...
    }).join('');
}

// Această funcție nu este apelată niciodată cu date valide
// deoarece fetchV31Data() eșuează cu 404
```

## Impact
- Utilizatorul nu vede ce simboluri sunt monitorizate
- Nu se poate da click pe simbol pentru detalii
- Informație importantă lipsă din dashboard

## Soluție
1. Rezolvă BUG-004 pentru API endpoints
2. Asigură-te că `updateV31SymbolGrid()` primește datele corecte
3. Pentru V32/V33, implementează funcții similare

## Verificare După Fix
1. Grid-ul ar trebui să afișeze 32 de simboluri pentru V31
2. Fiecare simbol ar trebui să aibă o culoare în funcție de status
3. Click pe simbol ar trebui să deschidă modal cu detalii

## Referințe
- Test Cases: TC-502, TC-503
- Depinde de: BUG-004
- Fișier raport: TEST-CASES-COMPLETE-REPORT.md
