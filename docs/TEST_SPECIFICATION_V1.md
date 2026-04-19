# TEST SPECIFICATION COMPLET - Trading Dashboard
## Generat automat din răspunsurile utilizatorului
### Data: 2026-03-28 | Versiune: 1.0

---

## 📋 SUMAR RĂSPUNSURI

| Container | Întrebări | Răspunse | Status |
|-----------|-----------|----------|--------|
| 1. Clienți | 5 | 5 | ✅ Complet |
| 2. Poziții | 6 | 6 | ✅ Complet |
| 3. Istoric | 6 | 6 | ✅ Complet |
| 4. Tracking | 4 | 4 | ✅ Complet |
| 5. V31 Robot | 10 | 10 | ✅ Complet |
| 6. V32 London | 7 | 7 | ✅ Complet |
| 7. V33 NY | 2 | 2 | ✅ Complet |
| 8-19 | 40 | 0 | ⏳ Așteaptă |

**Total: 80 întrebări | 40 răspunse (50%)**

---

# ✅ TEST CASES PENTRU CONTAINERELE CU RĂSPUNSURI

---

## 🟢 CONTAINER 1: CLIENȚI

### Configurație Confirmată:
- **Q1.1:** A - Clientul nu mai primește comenzi de la roboți (dar rămâne conectat)
- **Q1.2:** A + C - Pozițiile rămân deschise + flag vizual
- **Q1.3:** A - Doar utilizatorul manual (din dashboard)
- **Q1.4:** A - Numele din contul MT5 (din API)
- **Q1.5:** D - Real-time cu WebSocket (nu polling)

### Test Cases:

#### TC1.1: Activare Client
**Precondiții:** Client dezactivat în DB
**Pași:**
1. Accesează containerul Clienți
2. Click toggle "Dezactivat" pentru clientul X
**Rezultat Așteptat:**
- Toggle devine verde "Activat"
- Clientul poate primi comenzi de la roboți
- Pozițiile existente rămân deschise
- WebSocket trimite update în timp real

#### TC1.2: Dezvactivare Client
**Precondiții:** Client activ cu poziții deschise
**Pași:**
1. Click toggle "Activat" pentru clientul X
**Rezultat Așteptat:**
- Toggle devine gri "Dezactivat"
- Clientul NU mai primește comenzi noi de la roboți
- Pozițiile existente rămân deschise (nu se închid)
- Flag vizual "Dezactivat" apare în tabel
- WebSocket notifică imediat

#### TC1.3: Toggle Toți Clienții
**Pași:**
1. Click "Activează Toți"
**Rezultat Așteptat:**
- Toți clienții devin activi
- Fiecare toggle individual devine verde
- Update în timp real via WebSocket

#### TC1.4: Filtrare Clienți
**Pași:**
1. Selectează filtrul "Active"
2. Selectează filtrul "Inactive"
3. Selectează filtrul "Toți"
**Rezultat Așteptat:**
- Lista se filtrează corect fără refresh pagină
- Numărul din badge se actualizează

#### TC1.5: Afișare Date Client
**Rezultat Așteptat:**
- Coloana "Nume" = numele din contul MT5 (ex: "David Andrei Guta")
- Balans, Equity, Margin = valori reale din MT5
- Update în timp real (WebSocket)

---

## 🟢 CONTAINER 2: POZIȚII ACTIVE

### Configurație Confirmată:
- **Q2.1:** C - Mid price (bid+ask)/2
- **Q2.2:** B - Modal de confirmare cu sumar (NU închide imediat)
- **Q2.3:** A - Modal cu "Ești sigur?" pentru închidere individuală
- **Q2.4:** B + C - Indicator "Modificat" + log în Tracking
- **Q2.5:** D - Configurabil (setare în dashboard)
- **Q2.6:** B - Doar simbolurile cu poziții deschise

### Test Cases:

#### TC2.1: Afișare Preț Current (Mid Price)
**Precondiții:** Poziție BUY EURUSD deschisă
**Rezultat Așteptat:**
- Current Price = (Bid + Ask) / 2
- Ex: Bid=1.0850, Ask=1.0852 → Current=1.0851
- Se actualizează în timp real

#### TC2.2: Încercare Închidere Toate (Confirmare)
**Precondiții:** 3 poziții deschise
**Pași:**
1. Click "Închide Toate"
**Rezultat Așteptat:**
- Modal apare cu sumar:
  - "Vei închide 3 poziții"
  - "Profit estimat: +$45.20"
  - Butoane: "Confirmă", "Anulează"
- NICIO poziție nu se închide încă

#### TC2.3: Confirmare Închidere Toate
**Pași:**
1. Click "Închide Toate"
2. Click "Confirmă" în modal
**Rezultat Așteptat:**
- Toate pozițiile se închid la market
- Tabelul se actualizează (pozițiile dispar)
- Notificare de succes

#### TC2.4: Închidere Poziție Individuală (Confirmare)
**Pași:**
1. Click "Închide" pe o poziție
**Rezultat Așteptat:**
- Modal "Ești sigur?"
- Afișează: Ticket, Symbol, Profit curent
- Butoane: "Da, închide", "Anulează"

#### TC2.5: Poziție Modificată (SL/TP)
**Precondiții:** Poziție cu SL modificat
**Rezultat Așteptat:**
- Indicator "Modificat" vizibil în tabel
- Log în containerul Tracking
- La hover: arată detaliile modificării

#### TC2.6: Filtru Simboluri
**Rezultat Așteptat:**
- Dropdown conține DOAR simbolurile cu poziții deschise
- Ex: Doar EURUSD, GBPUSD (nu toate simbolurile MT5)

#### TC2.7: Calcul Profit (Configurabil)
**Setare A:** Profit = (current - open) × volume
**Setare B:** Profit = (current - open) × volume - swap - commission
**Setare C:** Profit net în depozit
**Rezultat:** Utilizatorul poate selecta în setări

---

## 🟢 CONTAINER 3: ISTORIC TRANZACȚII

### Configurație Confirmată:
- **Q3.1:** A - Doar tranzacțiile închise complet
- **Q3.2:** B - Profit real / |(Open - SL)|
- **Q3.3:** A - Timpul între deschidere și închidere
- **Q3.4:** D - Configurabil (limită istoric)
- **Q3.5:** B + C + D - Modal + Navigare tracking + Chart
- **Q3.6:** A - Nu e necesar export

### Test Cases:

#### TC3.1: Afișare Tranzacții Închise
**Rezultat Așteptat:**
- Apar DOAR tranzacțiile închise complet
- NU apar: anulate, partial close, open

#### TC3.2: Calcul R:R
**Formula:** R:R = Profit real / |Open - SL|
**Exemplu:**
- Open: 1.1000, SL: 1.0950, Profit: +$50
- Risk = |1.1000 - 1.0950| = 50 pips
- R:R = 50 / 50 = 1:1

#### TC3.3: Calcul Durată
**Formula:** Durată = Close Time - Open Time
**Format:** Ore, minute, secunde
**Ex:** "2h 30m 15s"

#### TC3.4: Click pe Tranzacție
**Pași:**
1. Click pe o tranzacție din istoric
**Rezultat Așteptat:**
- Modal cu detalii complete
- Buton "Vezi în Tracking" → navigare la ticket
- Buton "Chart" → grafic cu entry/exit

#### TC3.5: Filtre Perioadă
**Opțiuni:**
- Astăzi
- Săptămâna curentă
- Luna curentă
- Ultimul an
- Tot istoricul (configurabil - limită)

---

## 🟢 CONTAINER 4: TRACKING TRANZACȚII

### Configurație Confirmată:
- **Q4.1:** A - Istoric = doar închise, Tracking = deschise + închise
- **Q4.2:** A - Numele robotului (ex: "V31_TPL")
- **Q4.3:** C - Ambele (SL/TP și volum)
- **Q4.4:** C - Open, Closed, Modified, Partially Closed, Pyramiding

### Test Cases:

#### TC4.1: Diferență Istoric vs Tracking
| Istoric | Tracking |
|---------|----------|
| Doar închise | Deschise + Închise |
| Sumar | Detalii complete |
| Pentru analiză | Pentru audit |

#### TC4.2: Afișare "Deschis De"
**Valori posibile:**
- "V31_TPL" - robotul V31
- "V32_London" - robotul V32
- "Manual" - utilizatorul
- "Unknown" - necunoscut

#### TC4.3: Tracking Modificări
**Câmpuri track-uite:**
- SL modificat (vechi → nou)
- TP modificat (vechi → nou)
- Volum modificat (partial close)
- Cine a modificat (robot sau manual)
- Timestamp modificare

#### TC4.4: Statusuri Posibile
- 🟢 **Open** - Poziție deschisă activă
- 🔴 **Closed** - Poziție închisă complet
- 🟡 **Modified** - SL/TP modificat
- 🟠 **Partially Closed** - Volum redus
- 🔵 **Pyramiding** - Poziție adăugată (scale in)

---

## 🟢 CONTAINER 5: V31 MARIUS TPL

### Configurație Confirmată:
- **Q5.1:** A + B - Pornește proces Python + Setează flag "enabled"
- **Q5.2:** A + B - SIGTERM + stop_requested gracefully
- **Q5.3:** A - Rămân deschise (nu se mai deschid altele)
- **Q5.4:** A + B + C + D - Toate fazele posibile
- **Q5.5:** A + C - Culori standard + culori profit
- **Q5.6:** B - Valorile raw ale indicatorilor
- **Q5.7:** C - Configurabil (și parametri robot)
- **Q5.8:** D - Filtrabile după categorie
- **Q5.9:** B + C + D - Toate acțiunile
- **Q5.10:** A + D - ~2-3 minute ciclu, continuu

### Test Cases:

#### TC5.1: START Robot
**Pași:**
1. Click buton "START"
**Rezultat Așteptat:**
1. Backend pornește proces: `python3 v31_marius_tpl_robot.py`
2. Setează flag "enabled" = true în DB
3. Badge status devine "🟢 Running" în 2 secunde
4. Grid simboluri începe să se populeze

#### TC5.2: STOP Robot
**Pași:**
1. Click buton "STOP"
**Rezultat Așteptat:**
1. Trimite SIGTERM la proces
2. Setează flag "stop_requested" = true
3. Robotul se oprește gracefully (termină analiza curentă)
4. Badge devine "🔴 Stopped"
5. Pozițiile deschise RĂMÂN deschise

#### TC5.3: Grid Simboluri - Culori
| Culoare | Semnificație |
|---------|--------------|
| ⚪ Gri | Neanalizat |
| 🟢 Verde | Analizat, fără setup |
| 🟡 Galben | Setup găsit |
| 🔴 Roșu | Trade deschis |
| 💚 Verde închis | Trade în profit |
| ❤️ Roșu închis | Trade în pierdere |

#### TC5.4: Scoruri Tehnice (Raw Values)
**Afișare:**
- RSI: 65.4 (nu scor 6/10)
- Stochastic: 78.2
- Fibonacci: 61.8%
- Total: 7.2/10 (calculat)

#### TC5.5: Configurare Parametri Robot
**Parametri configurabili:**
- Prag setup (default 6/10)
- Lista simboluri (default 32)
- Interval analiză
- Risk per trade
- Alți parametri strategie

#### TC5.6: Click pe Simbol în Grid
**Acțiuni disponibile:**
1. **Modal detalii** - RSI, Stoch, Fib valori complete
2. **Chart** - Grafic simbol cu indicatori
3. **Forțare analiză** - Analizează imediat acest simbol

#### TC5.7: Filtrare Log-uri
**Categorii:**
- Lifecycle (start/stop)
- Cycle (ciclu analiză)
- Symbol (per simbol)
- Setup (setup găsite)
- Trade (tranzacții)

#### TC5.8: Ciclu Analiză
**Durată:** ~2-3 minute pentru 32 simboluri
**Flow:**
1. Ciclu continuu fără pauză
2. Fiecare simbol analizat secvențial
3. Progress bar actualizat în timp real
4. La final, reia automat

---

## 🟢 CONTAINER 6: V32 LONDON BREAKOUT

### Configurație Confirmată:
- **Q6.1:** B + D - UTC mereu + Configurabil
- **Q6.2:** B + C - Asia < 50% OR + Ambele condiții (AND)
- **Q6.3:** D - Configurabil
- **Q6.4:** A - Fazele complete
- **Q6.5:** C - Confirmare pe închiderea candle-ului
- **Q6.6:** A + B + D - Toate + Configurabil
- **Q6.7:** Configurabil (A/B/C/D)

### Test Cases:

#### TC6.1: London Time (UTC)
**Rezultat Așteptat:**
- Afișează ora Londra în UTC (nu GMT/BST)
- Update la fiecare secundă
- Configurabil să folosească local time

#### TC6.2: Faze Sesiune
| Fază | Interval (UTC) |
|------|----------------|
| BEFORE_SESSION | 00:00 - 08:00 |
| OPENING_RANGE | 08:00 - 08:15 |
| MAIN_SESSION | 08:15 - 16:00 |
| EXTENDED | 16:00 - 00:00 |

#### TC6.3: Compression Detection
**Condiție:** Asia Range < 50% din OR Range
**Ex:**
- Asia High: 1.1000, Asia Low: 1.0980 → Range = 20 pips
- OR High: 1.1010, OR Low: 1.0990 → Range = 20 pips
- 20 < (50% × 20) = 10? NU → Fără compression

#### TC6.4: Breakout Detection
**Confirmare:** Pe închiderea candle-ului (nu la atingere)
**Ex:**
- Candle atinge OR High dar închide sub → NU e breakout
- Candle închide peste OR High → Breakout confirmat

#### TC6.5: Body% și Wick%
**Formule:**
- Body% = |Close - Open| / |High - Low| × 100
- Wick% = 100% - Body%
- Upper Wick = |High - Max(Open, Close)| / |High - Low| × 100
- Lower Wick = |Min(Open, Close) - Low| / |High - Low| × 100

#### TC6.6: Acțiune la Breakout (Configurabil)
**Opțiuni:**
- A: Market order imediat
- B: Așteaptă retest
- C: Stop entry order
- D: Doar notificare

---

## 🟢 CONTAINER 7: V33 NY BREAKOUT

### Configurație Confirmată:
- **Q7.1:** A + B - Timezone + Pre-session
- **Q7.2:** D - Toate (analyză, high/low, niveluri)

### Test Cases:

#### TC7.1: Diferențe V32 vs V33
| V32 London | V33 NY |
|------------|--------|
| Timezone: London | Timezone: New York |
| OR: 08:00-08:15 | OR: 13:00-13:15 |
| Fără pre-session | Cu pre-session 08:00-13:00 |
| Asia session | Pre-session analysis |

#### TC7.2: Pre-session Analysis
**Activități 08:00-13:00 NY:**
- Calcul High/Low pre-market
- Identificare niveluri cheie de suport/rezistență
- Analiză volum și volatilitate
- Pregătire pentru OR

---

# ⏳ CONTAINERE RĂMASE (FĂRĂ RĂSPUNSURI)

## 8. Setup-uri Incomplete (4 întrebări)
## 9. Comenzi în Așteptare (5 întrebări)
## 10. Performanță pe Simboluri (5 întrebări)
## 11. System Health (5 întrebări)
## 12. Statistici Trading (4 întrebări)
## 13. Asociere Conturi (4 întrebări)
## 14. Utilizatori și Permisiuni (4 întrebări)
## 15. Equity Curve (5 întrebări)
## 16. Gestionare Servicii (5 întrebări)
## 17. Roboți Trading General (4 întrebări)
## 18. Expert Logs (4 întrebări)
## 19. Journal (4 întrebări)

**Total: 53 întrebări rămase**

---

## 🎯 STATUS IMPLEMENTARE TEST CASES

| Container | Test Cases Create | Prioritate |
|-----------|-------------------|------------|
| 1. Clienți | 5 | P0 - Critical |
| 2. Poziții | 7 | P0 - Critical |
| 3. Istoric | 5 | P1 - High |
| 4. Tracking | 4 | P1 - High |
| 5. V31 | 8 | P0 - Critical |
| 6. V32 | 6 | P1 - High |
| 7. V33 | 2 | P1 - High |
| 8-19 | 0 | P2 - Medium |

**Total Test Cases Create: 37**

---

## 📋 URMĂTORII PAȘI

1. ✅ **37 test cases create** pentru containerele cu răspunsuri
2. ⏳ **53 de întrebări rămase** pentru containerele 8-19
3. ⏳ **Creare test cases** pentru containerele 8-19 după primirea răspunsurilor
4. ⏳ **Review și validare** test cases cu utilizatorul
5. ⏳ **Implementare teste automate** (opțional)

---

**Vrei să răspunzi la întrebările pentru containerele 8-19 sau să validăm aceste test cases întâi?** 🚀
