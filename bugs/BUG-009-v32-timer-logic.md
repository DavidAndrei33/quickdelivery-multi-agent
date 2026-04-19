# BUG-009: V32 Session Timer Logic

## Informații Generale
| Atribut | Valoare |
|---------|---------|
| **ID** | BUG-009 |
| **Severitate** | MEDIUM |
| **Status** | OPEN |
| **Data descoperirii** | 2026-03-28 |
| **Raportat de** | QA-Master Agent |

## Descriere
Timer-ul pentru sesiunea V32 (London) folosește logica locală în browser în loc să citească starea reală de la API. Acest lucru poate duce la inconsistențe între ce arată dashboard-ul și starea reală a robotului.

## Cod Problematic
```javascript
// dashboard_functional.js
function updateV32SessionTimer() {
    const timerDisplay = document.getElementById('v32SessionTimer');
    const phaseDisplay = document.getElementById('v32SessionPhase');
    
    // Calcul local bazat pe timpul browser-ului
    const now = new Date();
    const londonTime = new Date(now.toLocaleString("en-US", {timeZone: "Europe/London"}));
    const hour = londonTime.getHours();
    const minute = londonTime.getMinutes();
    
    // Logica locală determină faza - poate fi diferită de robot!
    if (currentMinutes < sessionStart) {
        // Before session
    } else if (currentMinutes < orEnd) {
        // OR Formation
    }
    // ...
}
```

## Probleme
1. Timpul browser-ului poate fi diferit de timpul serverului
2. Robotul ar putea fi în altă fază decât arată dashboard-ul
3. Dacă robotul este oprit, dashboard-ul arată în continuă "activ"

## Soluție Propusă
Timer-ul ar trebui să se bazeze pe datele de la API, nu pe calcul local:

```javascript
// Înlocuiește updateV32SessionTimer() cu:
async function updateV32SessionTimer() {
    try {
        const res = await fetch(`${API_URL}/api/v32/session_status`, {
            headers: getAuthHeaders()
        });
        
        if (!res.ok) throw new Error('Failed to fetch session status');
        
        const data = await res.json();
        if (data.status === 'success') {
            updateV32TimerDisplay(data.data);
        }
    } catch (error) {
        console.error('[V32] Error fetching session timer:', error);
        // Fallback la calcul local doar în caz de eroare
        calculateLocalV32Timer();
    }
}

function updateV32TimerDisplay(data) {
    const timerDisplay = document.getElementById('v32SessionTimer');
    const phaseDisplay = document.getElementById('v32SessionPhase');
    
    // Folosește datele de la robot, nu calcul local
    timerDisplay.textContent = formatTime(data.time_remaining_seconds);
    phaseDisplay.textContent = data.session_phase;
    
    // Aplică culori în funcție de fază
    updateTimerColors(data.session_phase);
}
```

## API Response Necesar
```json
{
    "status": "success",
    "data": {
        "london_time": "08:05:23",
        "session_phase": "OPENING_RANGE",
        "is_active": true,
        "time_remaining_seconds": 600
    }
}
```

## Impact
- Inconsistențe între dashboard și stare reală
- Confuzie pentru utilizator
- Posibile decizii greșite bazate pe date incorecte

## Verificare După Fix
1. Timer-ul ar trebui să reflecte starea reală a robotului
2. Dacă robotul este oprit, timer-ul ar trebui să arate "Inactive"
3. Faza sesiunii ar trebui să fie sincronizată cu robotul

## Referințe
- Depinde de: BUG-004 (pentru API endpoint)
- Fișier raport: TEST-CASES-COMPLETE-REPORT.md
