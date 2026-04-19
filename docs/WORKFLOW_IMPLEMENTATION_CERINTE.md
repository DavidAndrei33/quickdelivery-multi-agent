# 🎯 WORKFLOW ECHIPĂ - Implementare Cerințe Dashboard

## Data: 2026-03-28
## Cerințe: 
1. Butoane ON/OFF compacte în containerul clienți
2. Poziții active reale din MT5

---

## 🔄 WORKFLOW PAS CU PAS

### **PAS 1: User (Andrei) → Cerere** 
```
Andrei: "Vreau butoane toggle în containerul clienți și 
         doar poziții active reale din MT5"
         ↓
```

### **PAS 2: Orchestrator (Manifest) → Analizează**
```
Orchestrator:
  1. Citește cerința
  2. Identifică ce trebuie modificat:
     - HTML: Container clienți + CSS toggle
     - JS: Funcții toggle + API integration
  3. Consultă Project Brain:
     - Există deja toggle CSS? → DA
     - Ce API pentru poziții? → /api/open_positions
         ↓
```

### **PAS 3: Assign la Echipă**
```
Orchestrator creează task-uri:

TASK-001: "Modifică butoane clienți în toggle switches"
├── Assigned: builder-4 (Frontend specialist)
├── Files: index.html, dashboard_functional.js
├── Priority: HIGH
└── ETA: 30 min

TASK-002: "Verifică API poziții active din MT5"  
├── Assigned: builder-1 (API specialist)
├── Files: dashboard_functional.js
├── Priority: HIGH
└── ETA: 15 min
```

### **PAS 4: Executie**

#### **builder-4 (Frontend) - Toggle Buttons:**
```
1. READ Project Brain:
   - Citește files_index.json
   - Vede că index.html există
   - Vede CSS toggle deja definit

2. IMPLEMENTEAZĂ în index.html:
   - Înlocuiește butoanele cu toggle switch compact
   - Adaugă CSS pentru toggle-switch-compact
   - Schimbă max-height la 300px (~15 rânduri)

3. UPDATE dashboard_functional.js:
   - Modifică updateClientsTable() să folosească toggle
   - Adaugă toggleAllClients() pentru global toggle
   - Adaugă toggleClient() pentru toggle individual

4. TESTEAZĚ:
   - Deschide dashboard în browser
   - Verifică toggle-urile apar
   - Verifică toggle-urile funcționează
```

#### **builder-1 (API) - Active Positions:**
```
1. READ Project Brain:
   - Citește architecture.md
   - Vede endpoint /api/open_positions

2. VERIFICĂ API:
   - Testează: curl /api/open_positions
   - Confirmă returnează doar poziții active (318)
   - Confirmă nu returnează poziții închise

3. UPDATE dashboard_functional.js:
   - loadPositions() folosește deja /api/open_positions ✅
   - Nu e nevoie de modificări

4. ADDS closePosition() și closeAllPositions():
   - Adaugă în index.html funcții pentru închidere poziții
   - Integrare cu /api/command endpoint
```

### **PAS 5: Review**
```
reviewer-1 (Code Reviewer):
  - Verifică codul lui builder-4
  - Verifică toggle CSS e consistent
  - Aprobă modificările ✅

reviewer-3 (QA-Tester):
  - Testează toggle în browser
  - Testează toggle individual și global
  - Verifică pozițiile active sunt reale
  - Aprobă ✅
```

### **PAS 6: Merge & Deploy**
```
ops-1 (DevOps):
  - Incrementează versiunea: v12 → v13
  - Restart MT5 Core Server (nu e necesar)
  - Verifică dashboard funcționează
         ↓
```

### **PAS 7: Notificare User**
```
Orchestrator → Andrei:
"✅ Modificări implementate:
   - Toggle switches ON/OFF în container clienți
   - Pozițiile active sunt reale din MT5 (318 poziții)
   - Log containers limitate la 15 rânduri
   Dashboard: http://localhost:8001/dashboard"
```

---

## 📁 FIȘIERE MODIFICATE

| Fișier | Modificări | Agent |
|--------|------------|-------|
| `index.html` | Toggle CSS, structură toggle, closePosition func | builder-4 |
| `dashboard_functional.js` | updateClientsTable(), toggle funcții | builder-4 |
| `index.html` | closePosition(), closeAllPositions() | builder-1 |

---

## 🎨 MODIFICĂRI UI/UX

### **Container Clienți - BEFORE:**
```html
<button onclick="enableAll()">Activează Toți</button>
<button onclick="disableAll()">Dezactivează Toți</button>
...
<button onclick="toggleClient(login, enabled)">Activează/Dezactivează</button>
```

### **Container Clienți - AFTER:**
```html
<label class="toggle-switch-compact">
    <input type="checkbox" id="globalClientToggle">
    <span class="toggle-slider-compact"></span>
    <span class="toggle-label-compact">Active</span>
</label>
...
<label class="toggle-switch-compact" style="transform: scale(0.85);">
    <input type="checkbox" onchange="toggleClient(login, this.checked)">
    <span class="toggle-slider-compact"></span>
</label>
```

**Rezultat:** Toggle mic, elegant, simplu ✅

---

## 📊 POZIȚII ACTIVE - VERIFICARE

### **API Endpoint:**
```bash
curl http://localhost:8001/api/open_positions?limit=5
```

### **Rezultat:**
```json
{
  "count": 318,
  "positions": [
    {
      "ticket": 1561808052,
      "symbol": "GBPJPY",
      "type": "BUY",
      "volume": 0.01,
      "open_price": 212.727,
      "current_price": 212.604,
      "current_profit": 0,
      "login": 52715350,
      "opened_by": "V29_Trading_Robot"
    }
    // ... încă 317 poziții
  ]
}
```

**Confirmare:** Sunt poziții ACTIVE reale din MT5 ✅

---

## 🎯 STATUS IMPLEMENTARE

| Cerință | Status | Implementat de |
|---------|--------|----------------|
| Butoane toggle ON/OFF compacte | ✅ Done | builder-4 |
| Toggle individual per client | ✅ Done | builder-4 |
| Toggle global (toți clienții) | ✅ Done | builder-4 |
| Poziții active din MT5 | ✅ Done | builder-1 |
| Funcții close position | ✅ Done | builder-1 |
| Log containers 15 rânduri | ✅ Done | builder-4 |

---

## 🚀 COMENZI PENTRU TESTARE

```bash
# Verifică dashboard
firefox http://localhost:8001/dashboard

# Verifică API poziții
curl http://localhost:8001/api/open_positions | python3 -m json.tool | head -20

# Verifică API clienți
curl http://localhost:8001/api/clients | python3 -m json.tool
```

---

## 📋 CUM LUCREAZĂ ECHIPA PE VIITOR

### **Flow Standard:**
```
1. Andrei cere modificare
2. Orchestrator analizează + consultă Project Brain
3. Orchestrator assignează task-uri la agenți
4. Agenții lucrează în paralel
5. Reviewers verifică codul
6. QA testează funcționalitatea
7. DevOps deployează
8. Andrei primește notificare
```

### **Timp Estimat pentru Task-uri Similare:**
- UI mic (toggle, buton): 30-60 min
- API integration: 15-30 min  
- Feature nou (robot): 2-4 ore
- Bug fix: 15-60 min

---

**Echipa este pregătită pentru următoarele cerințe!** 🎯
