# BUG-013: Incomplete Setup Robot Selector

## Informații Generale
| Atribut | Valoare |
|---------|---------|
| **ID** | BUG-013 |
| **Severitate** | LOW |
| **Status** | OPEN |
| **Data descoperirii** | 2026-03-28 |
| **Raportat de** | QA-Master Agent |

## Descriere
Selectorul de robot pentru secțiunea "Setup-uri Incomplete" există în HTML dar funcția `switchIncompleteRobot()` nu este implementată.

## Cod Problematic

### În index.html:
```html
<select id="incompleteSetupRobotSelector" onchange="switchIncompleteRobot()" ...>
    <option value="v31_tpl">🤖 V31 Marius TPL</option>
    <option value="v32_london">🌅 V32 London Breakout</option>
    <option value="v33_ny">🗽 V33 NY Breakout</option>
</select>
```

### Funcția lipsă:
```javascript
// switchIncompleteRobot() NU EXISTĂ!
```

## Impact
- Nu se poate schimba robotul pentru vizualizare setups incomplete
- Funcționalitate minoră afectată

## Soluție Propusă
```javascript
async function switchIncompleteRobot() {
    const robot = document.getElementById('incompleteSetupRobotSelector').value;
    const description = document.getElementById('incompleteSetupDescription');
    
    console.log(`[Incomplete Setups] Switched to ${robot}`);
    
    // Update description based on robot
    const descriptions = {
        'v31_tpl': 'V31: Scor 1-5/10 | Click pe setup pentru detalii',
        'v32_london': 'V32: Setups incomplete în așteptare | OR condiții parțiale',
        'v33_ny': 'V33: Pre-session setups | Așteaptă confirmare NY'
    };
    
    if (description) {
        description.textContent = descriptions[robot] || '';
    }
    
    // Load incomplete setups for selected robot
    await loadIncompleteSetups(robot);
}

async function loadIncompleteSetups(robot) {
    const tbody = document.getElementById('v31incompleteBody');
    
    try {
        tbody.innerHTML = '<tr><td colspan="11" style="text-align:center;padding:15px;color:#64748b;">Se încarcă setup-urile...</td></tr>';
        
        const response = await fetch(`${API_URL}/api/robot/${robot}/incomplete_setups`, {
            headers: getAuthHeaders()
        });
        
        if (!response.ok) throw new Error('Failed to load incomplete setups');
        
        const data = await response.json();
        
        if (data.status === 'success' && data.setups) {
            renderIncompleteSetups(data.setups);
        } else {
            tbody.innerHTML = '<tr><td colspan="11" style="text-align:center;padding:15px;color:#64748b;">Niciun setup incomplet</td></tr>';
        }
    } catch (error) {
        console.error('[Incomplete Setups] Error:', error);
        tbody.innerHTML = `<tr><td colspan="11" style="text-align:center;padding:15px;color:#ef4444;">
            Eroare la încărcare: ${error.message}
        </td></tr>`;
    }
}

window.switchIncompleteRobot = switchIncompleteRobot;
window.loadIncompleteSetups = loadIncompleteSetups;
```

## API Endpoint Necesar
```
GET /api/robot/{robot}/incomplete_setups
```

## Verificare După Fix
1. Schimbă robotul în selectorul de setups incomplete
2. Descrierea ar trebui să se actualizeze
3. Lista de setups ar trebui să se încarce pentru robotul selectat

## Referințe
- Fișier raport: TEST-CASES-COMPLETE-REPORT.md
