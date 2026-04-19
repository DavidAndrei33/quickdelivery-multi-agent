# BUG-005: Live Analysis Not Updating

## Informații Generale
| Atribut | Valoare |
|---------|---------|
| **ID** | BUG-005 |
| **Severitate** | HIGH |
| **Status** | OPEN |
| **Data descoperirii** | 2026-03-28 |
| **Raportat de** | QA-Master Agent |

## Descriere
Progress bar-ul și contoarele din secțiunea "Analiză Live" nu se actualizează deoarece API-ul returnează 404.

## Cauză Rădăcină
BUG-004 - Endpoint-urile API pentru status nu sunt implementate.

## Elemente Afectate
- `#liveAnalysisProgressBar` - Progress bar blocat la 0%
- `#liveAnalysisCurrent` - Afișează "-" în loc de simbolul curent
- `#liveAnalyzedCount` - Rămâne la 0
- `#liveSetupsCount` - Rămâne la 0  
- `#liveRejectedCount` - Rămâne la 0

## Cod Afectat
```javascript
// dashboard_functional.js - fetchV31Data()
async function fetchV31Data() {
    try {
        const res = await fetch(`${API_URL}/api/v31/live_status`, {
            headers: getAuthHeaders()
        });
        
        if (!res.ok) throw new Error('Failed to fetch V31 live status');
        // ^ Această eroare este aruncată mereu (404)
        
        const data = await res.json();
        if (data.status === 'success') {
            v31LastData = data.data;
            updateV31Dashboard(data.data);  // Nu se apelează niciodată
        }
    } catch (error) {
        console.error('[V31] Error fetching data:', error);
        // Keep previous values on error - don't show "undefined"
    }
}
```

## Impact
- Progress bar nu arată progresul real
- Contoarele rămân la 0
- Utilizatorul nu vede ce simbol este analizat
- Experiență de utilizare deficitară

## Soluție
Rezolvă BUG-004 pentru a implementa endpoint-urile necesare.

## Workaround Temporar
```javascript
// Adaugă date mock pentru testare
async function fetchV31Data() {
    try {
        const res = await fetch(`${API_URL}/api/v31/live_status`, {
            headers: getAuthHeaders()
        });
        
        if (!res.ok) {
            // Folosește date mock pentru testare
            console.warn('[V31] API unavailable, using mock data');
            const mockData = {
                status: 'SCANNING',
                progress: Math.floor(Math.random() * 100),
                current_symbol: 'EURUSD',
                analyzed_count: 15,
                setups_count: 2,
                rejected_count: 13
            };
            updateV31Dashboard(mockData);
            return;
        }
        
        // ... restul codului
    } catch (error) {
        console.error('[V31] Error fetching data:', error);
    }
}
```

## Verificare După Fix
1. Pornește robotul V31
2. Progress bar ar trebui să crească de la 0% la 100%
3. Contoarele ar trebui să se actualizeze
4. Simbolul curent ar trebui afișat

## Referințe
- Test Cases: TC-302, TC-306
- Depinde de: BUG-004
- Fișier raport: TEST-CASES-COMPLETE-REPORT.md
