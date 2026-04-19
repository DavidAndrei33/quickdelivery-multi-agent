# BUG-006: Missing loadRobotLogs Function

## Informații Generale
| Atribut | Valoare |
|---------|---------|
| **ID** | BUG-006 |
| **Severitate** | MEDIUM |
| **Status** | OPEN |
| **Data descoperirii** | 2026-03-28 |
| **Raportat de** | QA-Master Agent |

## Descriere
Funcția `loadRobotLogs()` nu este implementată în JavaScript, deși butonul de filtrare apelează această funcție.

## Elemente Afectate
- Filtrul `#robotLogFilter` - onchange="loadRobotLogs()" nu funcționează
- Tabelul `#robotLogTable` - nu se populează cu date
- `#robotLogBody` - afișează mereu "Se încarcă log-urile..."

## Cod Problematic

### În index.html:
```html
<select id="robotLogFilter" onchange="loadRobotLogs()" ...>
    <option value="all">Toate</option>
    <option value="lifecycle">Lifecycle</option>
    <option value="cycle">Cicluri Scan</option>
    ...
</select>
```

### În dashboard_functional.js:
```javascript
// Funcția loadRobotLogs NU EXISTĂ!
// Ar trebui să fie implementată similar cu:
// async function loadRobotLogs() { ... }
```

## Impact
- Utilizatorul nu poate vedea log-urile robotului
- Filtrul nu funcționează
- Debugging dificil fără vizualizarea log-urilor

## Soluție Propusă

```javascript
// Adaugă în dashboard_functional.js

async function loadRobotLogs() {
    const robot = document.getElementById('robotSelector').value;
    const filter = document.getElementById('robotLogFilter').value;
    const tbody = document.getElementById('robotLogBody');
    
    console.log(`[Logs] Loading logs for ${robot} with filter: ${filter}`);
    
    try {
        tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;padding:20px;color:#64748b;">Se încarcă log-urile...</td></tr>';
        
        const response = await fetch(`${API_URL}/api/robot/${robot}/logs?filter=${filter}`, {
            headers: getAuthHeaders()
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.status === 'success' && data.logs) {
            renderRobotLogs(data.logs);
        } else {
            tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;padding:20px;color:#64748b;">Niciun log disponibil</td></tr>';
        }
    } catch (error) {
        console.error('[Logs] Error loading logs:', error);
        tbody.innerHTML = `<tr>
            <td colspan="4" style="text-align:center;padding:20px;color:#ef4444;">
                Eroare la încărcarea log-urilor: ${error.message}
            </td>
        </tr>`;
    }
}

function renderRobotLogs(logs) {
    const tbody = document.getElementById('robotLogBody');
    
    if (logs.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;padding:20px;color:#64748b;">Niciun log disponibil</td></tr>';
        return;
    }
    
    tbody.innerHTML = logs.map(log => {
        const levelColors = {
            'INFO': '#22c55e',
            'WARN': '#f59e0b',
            'ERROR': '#ef4444',
            'DEBUG': '#64748b'
        };
        
        return `<tr style="font-size: 10px;">
            <td style="padding: 4px 6px; color: #64748b;">${log.time}</td>
            <td style="padding: 4px 6px; text-align: center;">${log.cycle || '-'}</td>
            <td style="padding: 4px 6px; text-align: center; color: ${levelColors[log.level] || '#64748b'};">${log.level}</td>
            <td style="padding: 4px 6px; color: #e2e8f0;">${log.message}</td>
        </tr>`;
    }).join('');
}

// Export for global access
window.loadRobotLogs = loadRobotLogs;
window.renderRobotLogs = renderRobotLogs;
```

## API Endpoint Necesar
```
GET /api/robot/{robot}/logs?filter={filter}
```

### Parametri
- `robot`: v31_tpl, v32_london, sau v33_ny
- `filter`: all, lifecycle, cycle, symbol, setup, trade, error

### Răspuns
```json
{
    "status": "success",
    "logs": [
        {
            "time": "17:05:23",
            "cycle": 42,
            "level": "INFO",
            "message": "Starting analysis of EURUSD"
        },
        {
            "time": "17:05:24",
            "cycle": 42,
            "level": "WARN",
            "message": "Setup rejected: score too low"
        }
    ]
}
```

## Verificare După Fix
1. Selectează un robot
2. Log-urile ar trebui să apară automat
3. Schimbă filtrul - tabelul ar trebui să se actualizeze
4. Verifică formatul: Timp, Ciclu, Nivel, Mesaj

## Referințe
- Test Cases: TC-402, TC-403
- Fișier raport: TEST-CASES-COMPLETE-REPORT.md
