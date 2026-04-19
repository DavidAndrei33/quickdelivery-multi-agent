# BUG-002: Missing controlRobot Function

## Informații Generale
| Atribut | Valoare |
|---------|---------|
| **ID** | BUG-002 |
| **Severitate** | CRITICAL |
| **Status** | OPEN |
| **Data descoperirii** | 2026-03-28 |
| **Raportat de** | QA-Master Agent |

## Descriere
Butoanele Start și Stop pentru roboți apelează funcția `controlRobot()` care nu este implementată în cod. Aceasta face imposibilă pornirea sau oprirea roboților din dashboard.

## Fișiere Afectate
- `/workspace/shared/dashboard/index.html` (butoanele Start/Stop)
- `/workspace/shared/dashboard/dashboard_functional.js` (funcția lipsă)

## Cod Problematic

### În index.html:
```html
<button id="robotStartBtn" onclick="controlRobot('start')" style="...">
    ▶️ Start
</button>
<button id="robotStopBtn" onclick="controlRobot('stop')" style="...">
    ⏹️ Stop
</button>
```

### În dashboard_functional.js:
```javascript
// Funcția controlRobot NU EXISTĂ!
// Ar trebui să fie ceva de genul:
// async function controlRobot(action) { ... }
```

## Impact
- CRITICAL: Nu se pot porni roboții
- CRITICAL: Nu se pot opri roboții
- Funcționalitatea principală a dashboard-ului este inutilizabilă

## Reproducere
1. Deschide dashboard
2. Selectează orice robot (V31, V32, V33)
3. Click pe butonul Start
4. Eroare în consolă: `controlRobot is not defined`

## Soluție Propusă
```javascript
// Adaugă în dashboard_functional.js

async function controlRobot(action) {
    const robot = document.getElementById('robotSelector').value;
    const startBtn = document.getElementById('robotStartBtn');
    const stopBtn = document.getElementById('robotStopBtn');
    const statusBadge = document.getElementById('robotStatusBadge');
    
    console.log(`[Robot] ${action} requested for ${robot}`);
    
    try {
        // Disable buttons during request
        startBtn.disabled = true;
        stopBtn.disabled = true;
        
        const response = await fetch(`${API_URL}/api/robot/${robot}/${action}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...getAuthHeaders()
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.status === 'success') {
            showToast(`Robot ${robot} ${action === 'start' ? 'started' : 'stopped'} successfully`, 'success');
            
            // Update UI
            if (action === 'start') {
                statusBadge.textContent = '🟢 Running';
                statusBadge.style.background = '#22c55e';
                startBtn.disabled = true;
                stopBtn.disabled = false;
            } else {
                statusBadge.textContent = '🔴 Stopped';
                statusBadge.style.background = '#ef4444';
                startBtn.disabled = false;
                stopBtn.disabled = true;
            }
        } else {
            throw new Error(data.message || 'Unknown error');
        }
    } catch (error) {
        console.error(`[Robot] ${action} failed:`, error);
        showToast(`Failed to ${action} robot: ${error.message}`, 'error');
    } finally {
        // Re-enable buttons
        const isRunning = statusBadge.textContent.includes('Running');
        startBtn.disabled = isRunning;
        stopBtn.disabled = !isRunning;
    }
}

// Export for global access
window.controlRobot = controlRobot;
```

## Dependințe
- BUG-003: Endpoint-urile API trebuie implementate pentru ca funcția să funcționeze

## Referințe
- Test Cases: TC-102, TC-103, TC-105, TC-106, TC-108-118
- Fișier raport: TEST-CASES-COMPLETE-REPORT.md
