# BUG-012: Connection Status Always Offline

## Informații Generale
| Atribut | Valoare |
|---------|---------|
| **ID** | BUG-012 |
| **Severitate** | HIGH |
| **Status** | OPEN |
| **Data descoperirii** | 2026-03-28 |
| **Raportat de** | QA-Master Agent |

## Descriere
Indicatorii de conexiune pentru roboți (dots) arată întotdeauna offline (gri/roșu) deoarece API-ul pentru verificarea statusului returnează 404.

## Elemente Afectate
- `#v31StatusDot` - Indicator V31
- `#v32StatusDot` - Indicator V32
- `#v33StatusDot` - Indicator V33

## Cod Afectat
```javascript
// dashboard_functional.js
async function checkRobotConnection(robot) {
    try {
        let endpoint;
        switch(robot) {
            case 'v31':
                endpoint = '/api/v31/live_status';
                break;
            case 'v32':
                endpoint = '/api/v32/or_data';
                break;
            case 'v33':
                endpoint = '/api/v33/or_data?symbol=EURUSD';
                break;
        }
        
        const res = await fetch(`${API_URL}${endpoint}`, {
            headers: getAuthHeaders()
        });
        
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        // ^ Această eroare este aruncată mereu
        
        // ... update UI
    } catch (error) {
        console.error(`[Connection] ${robot} check failed:`, error);
        // Setează status la offline
        updateRobotConnectionUI(robot, false);
    }
}
```

## Impact
- Utilizatorul crede că roboții sunt offline când poate sunt online
- Confuzie și încredere scăzută în sistem
- Dificultate în diagnosticarea problemelor reale

## Soluție
Rezolvă BUG-004 pentru a implementa endpoint-urile necesare.

## Comportament Așteptat
- Dot verde (#22c55e) când robotul răspunde la API
- Dot roșu (#ef4444) când robotul nu răspunde
- Update la fiecare 5 secunde (configurat în `startRobotStatusPolling`)

## Verificare După Fix
1. Pornește un robot
2. Dot-ul ar trebui să devină verde în max 10 secunde
3. Oprește robotul
4. Dot-ul ar trebui să devină roșu în max 10 secunde

## Referințe
- Test Cases: TC-201-209
- Depinde de: BUG-004
- Fișier raport: TEST-CASES-COMPLETE-REPORT.md
