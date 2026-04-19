# BUG-001: Robot Switch Mismatch

## Informații Generale
| Atribut | Valoare |
|---------|---------|
| **ID** | BUG-001 |
| **Severitate** | HIGH |
| **Status** | OPEN |
| **Data descoperirii** | 2026-03-28 |
| **Raportat de** | QA-Master Agent |

## Descriere
Funcția `switchRobot()` din `dashboard_functional.js` referă valoarea `'v31_marius'` dar în HTML dropdown-ul are valoarea `'v31_tpl'`. Această nepotrivire face ca switching-ul între roboți să nu funcționeze corect pentru V31.

## Fișiere Afectate
- `/workspace/shared/dashboard/dashboard_functional.js` (linia 47)
- `/workspace/shared/dashboard/index.html` (linia cu option value)

## Cod Problematic

### În dashboard_functional.js:
```javascript
function switchRobot() {
    const robot = document.getElementById('robotSelector').value;
    
    // ... cod pentru hide all sections ...
    
    // Show selected and start polling
    if (robot === 'v31_marius') {  // ❌ GREȘIT - ar trebui să fie 'v31_tpl'
        if (v31Section) v31Section.style.display = 'block';
        startV31Polling();
    } else if (robot === 'v32_london') {
        // ...
    }
    
    console.log(`[Dashboard] Switched to ${robot}`);
}
```

### În index.html:
```html
<select id="robotSelector" onchange="switchRobot()">
    <option value="v31_tpl">🤖 V31 Marius TPL</option>  <!-- ✅ Corect -->
    <option value="v32_london">🌅 V32 London Breakout</option>
    <option value="v33_ny">🗽 V33 NY Breakout</option>
</select>
```

## Impact
- Switching la V31 nu afișează secțiunea V31
- Polling-ul pentru V31 nu pornește
- Utilizatorul nu poate vedea dashboard-ul V31

## Reproducere
1. Deschide dashboard
2. Selectează V31 din dropdown
3. Observă că secțiunea V31 nu apare
4. Console log arată "[Dashboard] Switched to v31_tpl" dar secțiunea rămâne ascunsă

## Soluție Propusă
```javascript
// Înlocuiește linia 47 din dashboard_functional.js:
if (robot === 'v31_marius') {
// cu:
if (robot === 'v31_tpl') {
```

## Fix Verificare
După fix:
1. Selectează V31 din dropdown
2. Secțiunea V31 ar trebui să apară
3. Polling-ul ar trebui să pornească
4. Console log: "[Dashboard] Switched to v31_tpl"

## Referințe
- Test Case: TC-004
- Fișier raport: TEST-CASES-COMPLETE-REPORT.md
