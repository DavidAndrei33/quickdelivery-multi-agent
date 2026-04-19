# SPECIFICAȚII COMPLETE - DASHBOARD IMPLEMENTATION
## Bazate pe răspunsurile utilizatorului - 2026-03-29

---

## ✅ REZUMAT RĂSPUNSURI

**Total întrebări:** 80  
**Răspunse:** 80 (100%)  
**Multiple choice:** Majoritatea au selecții multiple (A+B+C etc.)

---

## 🔷 SELECTOR ROBOȚI

### Q-GEN-1: Informații afișate
**Răspuns:** B - Numele + iconiță + status curent (🟢/🔴)

**Implementare:**
- Dropdown cu iconiță robot (🤖, 🌅, 🗽)
- Badge status colorat în dreapta (🟢/🔴)
- Text: "V31 Marius TPL 🟢 Running"

### Q-GEN-2: Ce se întâmplă la schimbare
**Răspuns:** A + C - Schimbă secțiunea vizibilă + încarcă datele specifice

**Implementare:**
- Fără oprire/pornire automată
- Doar schimbare vizuală între secțiuni
- Fetch date specifice robotului selectat
- Update badge status pentru robotul activ

### Q-GEN-3: Frecvență update
**Răspuns:** B - La fiecare 1 secundă (polling)

**Implementare:**
- setInterval de 1 secundă pentru status
- WebSocket pentru date critice (opțional)

---

## 🔷 V31 MARIUS TPL

### Symbol Grid

**Q-V31-1:** Ce afișează
**Răspuns:** D - Toate simbolurile cu istoric complet

**Implementare:**
- Grid cu toate cele 32 simboluri
- Pentru fiecare: simbol, direcție, scor, status (analyzed/pending)
- Culori: fundal în funcție de direcție/sentiment

**Q-V31-2:** Scorul afișat
**Răspuns:** B - Număr condiții îndeplinite din total

**Implementare:**
- Format: "7/10"
- Tooltip cu breakdown condiții

**Q-V31-3:** Culoare fundal
**Răspuns:** A - Verde=cumpărare, Roșu=vânzare, Gri=neutru

**Implementare:**
- Buy setup → fundal verde deschis
- Sell setup → fundal roșu deschis
- Neutral/analyzing → fundal gri

**Q-V31-4:** Click pe simbol
**Răspuns:** A + B - Deschide MT5 + arată detalii analiză

**Implementare:**
- Modal cu detalii complete:
  - Indicatori (RSI, Stoch, EMA)
  - Scor breakdown
  - Condiții îndeplinite/neîndeplinite
  - Buton "Deschide în MT5"

**Q-V31-5:** Frecvență update
**Răspuns:** A - La fiecare ciclu de analiză

**Implementare:**
- Update la finalul fiecărui ciclu (când robotul termină)
- Notificare "Ciclu complet - 32/32 simboluri analizate"

### Ciclu de Analiză

**Q-V31-6:** Progress Bar
**Răspuns:** A - Timpul rămas până la sfârșitul sesiunii

**Implementare:**
- Progress bar orizontal
- Afișează timp rămas sesiune
- Sau progres ciclu curent (32/32) dacă e în analiză

**Q-V31-7:** Current Symbol
**Răspuns:** A - Simbolul care se analizează în acest moment

**Implementare:**
- Text: "Analizând: EURUSD"
- Cu animație pulse

**Q-V31-8:** Phase Complete vs Analyzing
**Răspuns:** A - Complete=ciclu terminat, Analyzing=în desfășurare

**Implementare:**
- Badge: "🟡 Analyzing..." / "✅ Complete"
- Progres bar activ când analyzing

### Setup-uri Incomplete

**Q-V31-9:** Ce sunt
**Răspuns:** A - Setups găsite dar fără confirmare finală (scor < 6)

**Implementare:**
- Listă separată
- Scor 4-5/10 (sub pragul de 6)
- Motiv respingere afișat

**Q-V31-10:** Acțiuni posibile
**Răspuns:** D - Toate cele de mai sus

**Implementare:**
- Vizualizare detalii
- Buton "Forțare Trade" (override scor)
- Buton "Modificare parametri"
- Buton "Șterge"

**Q-V31-11:** Informații afișate
**Răspuns:** A + C - Simbol/direcție/scor/motiv + detalii tehnice

**Implementare:**
- Card pentru fiecare setup:
  - Header: EURUSD BUY 5/10
  - Motiv: "Scor insuficient"
  - Expandabil cu detalii tehnice

### Thinking Process (Gândirea Robotului)

**Q-V31-12:** Vrei să vezi?
**Răspuns:** A - Da, fiecare pas din analiză

**Q-V31-13:** Ce detalii
**Răspuns:** D - Toate cele de mai sus

**Q-V31-14:** Unde să apară
**Răspuns:** A + B + C + D - În toate locațiile!

**Implementare:**
- **Panel principal "Robot Journal"** - Stream live ca terminal
- **Tooltip** la hover pe simbol în grid
- **Modal** la click pe simbol
- **Consolă** pentru debugging

**Funcționalitate:**
```
[09:23:45] Analizare EURUSD...
[09:23:45] RSI: 45.2 (OK)
[09:23:45] Stoch K: 32.1 (OK)
[09:23:45] EMA20 > EMA50: DA
[09:23:45] Scor parțial: 7/10
[09:23:45] ✅ Setup VALIDAT - Scor final: 7/10
```

---

## 🔷 V32 LONDON BREAKOUT

### Timp și Sesiune

**Q-V32-1:** London Time
**Răspuns:** A - Ora curentă în Londra (GMT/BST)

**Q-V32-2:** Session Timer
**Răspuns:** D - Toate cele de mai sus (în funcție de fază)

**Implementare:**
- Timer adaptiv:
  - Before Session: countdown până la 08:00
  - OR Formation: countdown 15 min
  - Main Session: timp rămas până la 10:30

**Q-V32-3:** Faze sesiune
**Răspuns:** A - Before Session, OR Formation, Main Session, Extended

**Implementare:**
- Badge cu fază curentă
- Culori diferite per fază

### Opening Range (OR)

**Q-V32-4:** OR High/Low
**Răspuns:** D - Prețurile de deschidere și închidere ale sesiunii

**Implementare:**
- Afișare numerică: OR High, OR Low, OR Range
- Calculat din prima oră (08:00-09:00)

**Q-V32-5:** Când se formează OR
**Răspuns:** A - 08:00-08:15 (15 minute)

**Implementare:**
- Progress bar pentru OR formation (15 min)
- Lock după 08:15

**Q-V32-6:** După OR format
**Răspuns:** A - Robotul așteaptă breakout

**Q-V32-7:** Grafic vizual OR
**Răspuns:** B - Doar valorile numerice sunt suficiente

**Implementare:**
- Fără mini-chart (simplu)
- Doar: High, Low, Range (pips)

### Asia Session

**Q-V32-8:** Asia Range
**Răspuns:** A - Range format în sesiunea asiatică (00:00-08:00 GMT)

**Q-V32-9:** Asia Compressed
**Răspuns:** A - Range Asia sub X pips (configurabil)

**Q-V32-10:** Cum folosește robotul
**Răspuns:** A - Pentru a calcula targeturi de profit

**Implementare:**
- Asia High/Low afișat
- Range în pips
- Status: "Compressed" dacă < threshold

### Semnale și Tranzacții

**Q-V32-11:** Breakout Status
**Răspuns:** A - Așteptare / Breakout Detectat / Trade Executat

**Q-V32-12:** Tipuri setup
**Răspuns:** A - Type A (breakout puternic) și Type B (pullback)

**Implementare:**
- Type A: Breakout direct prin OR
- Type B: Pullback la OR apoi continuare

**Q-V32-13:** Body/Wick Percent
**Răspuns:** A - Raport corp vs. umbra în candlestick

**Implementare:**
- Afișat pentru candlestick-ul breakout
- Body %, Wick %

**Q-V32-14:** Notificare la breakout
**Răspuns:** A + B - Popup + sunet + schimbare culoare

**Implementare:**
- Toast notification
- Sunet alertă
- Schimbare culoare dashboard
- Optional: notificare desktop

### Statistici

**Q-V32-15:** Statistici în timp real
**Răspuns:** D - Toate detaliile

**Implementare:**
- Trades today: X/2
- Win/Loss ratio: X/Y
- Total P&L: $X.XX
- Durată medie trade
- SL/TP hit rate

**Q-V32-16:** Type B Pending
**Răspuns:** A - Așteaptă confirmare pentru pullback

---

## 🔷 V33 NY BREAKOUT

**Q-V33-1:** Pre-Session High/Low
**Răspuns:** A - Maxim/minim dinainte de sesiunea NY (11:30-13:00 EST)

**Q-V33-2:** Diferență față de V32
**Răspuns:** A + B - Pre-session analysis + EURUSD vs GBPUSD

**Implementare:**
- Pre-session range (11:30-13:00)
- V33: EURUSD
- V32: GBPUSD

**Q-V33-3:** Ce sesiuni influențează
**Răspuns:** A - Doar New York

---

## 🔷 COMENZI ÎN AȘTEPTARE (QUEUE)

**Q-QUEUE-1:** Ce comenzi pot apărea
**Răspuns:** B - Doar deschidere poziții

**Implementare:**
- Open Position (doar Buy/Sell)
- Fără Modify SL/TP în queue (direct execution)

**Q-QUEUE-2:** Ce se întâmplă cu o comandă
**Răspuns:** B - Rămâne în coadă până la executare sau anulare

**Implementare:**
- Queue persistent
- Nu expiră automat
- Execute Now sau Cancel

**Q-QUEUE-3:** Informații afișate
**Răspuns:** A - Tip, simbol, volum, preț target, timestamp

**Q-QUEUE-4:** Acțiuni posibile
**Răspuns:** A - Execute Now, Cancel, Modify

**Q-QUEUE-5:** Notificare la execuție
**Răspuns:** B - Sunet + notificare

---

## 🔷 JURNAL ROBOT

**Q-JOURNAL-1:** Ce să vezi în jurnal
**Răspuns:** A - Fiecare decizie luată și motivația

**Q-JOURNAL-2:** Cât de detaliat
**Răspuns:** A + D - Fiecare pas + configurabil

**Implementare:**
- Stream live în timp real
- Configurabil: Debug/Info/Warning/Error

**Q-JOURNAL-3:** Filtre
**Răspuns:** A - Per robot, per nivel, per perioadă

**Q-JOURNAL-4:** Export
**Răspuns:** B + C - CSV + doar vizualizare

**Implementare:**
- Export CSV
- Vizualizare live în dashboard
- Fără PDF

---

## 🔷 SINCRONIZARE LIVE

**Q-LIVE-1:** Ce înseamnă sincronizare live
**Răspuns:** A - Datele se actualizează în timp real (sub 1 secundă)

**Q-LIVE-2:** Metodă de update
**Răspuns:** A + B + C + D - Toate metodele hibrid!

**Implementare:**
- **WebSocket** pentru date critice (decizii, execuții)
- **Polling 1s** pentru status general
- **SSE** pentru jurnal (stream)
- **Hibrid** optimizat

**Q-LIVE-3:** Când robotul ia decizie
**Răspuns:** A - Vreau să văd imediat în dashboard (fără refresh)

**Implementare:**
- WebSocket push instant
- Animatie la decizie
- Toast notification

**Q-LIVE-4:** Cum vezi gândirea robotului
**Răspuns:** A + B - Stream live + pas cu pas cu delay

**Implementare:**
- Terminal live în dashboard
- Delay 100ms între pași (vizibilitate)

**Q-LIVE-5:** Ce date în timp real
**Răspuns:** A - Tot (prețuri, indicatori, decizii, execuții)

---

## 🔷 ELEMENTE COMUNE

**Q-COMMON-1:** Informații generale
**Răspuns:** A - Status, uptime, ultimul ciclu, profit azi

**Q-COMMON-2:** Cum arată statusul
**Răspuns:** C - LED animat (pulsează când rulează)

**Implementare:**
- Indicator LED cu pulse animation
- Verde puls = running
- Roșu solid = stopped

**Q-COMMON-3:** Acțiuni disponibile
**Răspuns:** A - Start, Stop, Restart, View Logs

**Q-COMMON-4:** Organizare informații
**Răspuns:** A + D - Tab-uri + Accordion

**Implementare:**
- Tab-uri principale: Overview, Analysis, Trades, Logs, Settings
- În interior: Accordion pentru secțiuni

---

## 🔷 PERFORMANȚĂ ȘI UI

**Q-PERF-1:** Prioritate viteză update
**Răspuns:** A - Maximă (1 secundă sau mai puțin)

**Q-PERF-2:** Când robotul e oprit
**Răspuns:** B - Mesaj "Robot Offline - Last seen X min ago"

**Q-PERF-3:** Gestionare erori conexiune
**Răspuns:** A - Retry automat + mesaj utilizator

---

## 📋 TASK-URI PENTRU IMPLEMENTARE

### Frontend (HTML/CSS/JS)
1. ✅ Robot Selector cu iconițe și status LED
2. ✅ Symbol Grid pentru V31 cu culori și detalii
3. ✅ Progress Bar pentru ciclu de analiză
4. ✅ Setup-uri Incomplete (listă + acțiuni)
5. ✅ Robot Journal (terminal live)
6. ✅ V32 Dashboard (OR, Asia, Breakout)
7. ✅ V33 Dashboard (Pre-session)
8. ✅ Comenzi Queue (listă + acțiuni)
9. ✅ LED animat pentru status
10. ✅ Tab-uri + Accordion layout

### Backend (API)
1. ✅ WebSocket endpoint pentru live updates
2. ✅ SSE endpoint pentru jurnal
3. ✅ API pentru queue management
4. ✅ API pentru robot thinking process
5. ✅ API pentru detalii simbol (RSI, Stoch, etc.)

### Integrare
1. ✅ WebSocket client în dashboard
2. ✅ Polling 1s pentru status
3. ✅ Toast notifications
4. ✅ Sunete pentru alerte
5. ✅ Error handling cu retry

---

**ESTIMARE:** 15-20 task-uri × 4 agenți = Complet în 2-3 ore
