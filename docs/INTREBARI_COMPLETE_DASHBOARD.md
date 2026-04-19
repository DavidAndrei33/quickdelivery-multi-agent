# ÎNTREBĂRI COMPLETE PENTRU TOATE ELEMENTELE DASHBOARD
## Trading Dashboard - Toate containerele și elementele

---

## 🔷 CONTAINER: SELECTOR ROBOȚI (General)

### Q-GEN-1: Ce informații afișează selectorul de roboți?
- [ ] A: Doar numele robotului
- [ ] B: Numele + iconiță + status curent (🟢/🔴)
- [ ] C: Numele + profit zilnic + număr tranzacții
- [ ] D: Toate detaliile (nume, status, profit, uptime)

### Q-GEN-2: Ce se întâmplă la schimbarea robotului din selector?
- [ ] A: Doar se schimbă secțiunea vizibilă
- [ ] B: Se oprește robotul anterior și se pornește cel nou
- [ ] C: Se încarcă datele specifice robotului selectat
- [ ] D: Se face refresh complet al paginii

### Q-GEN-3: Cât de des se actualizează informațiile din selector?
- [ ] A: La fiecare schimbare manuală
- [ ] B: La fiecare 5 secunde (polling)
- [ ] C: La fiecare 30 secunde
- [ ] D: Doar la refresh pagină

---

## 🔷 CONTAINER: V31 MARIUS TPL - Elemente Specifice

### Sectiunea: Analiză Simboluri (Symbol Grid)

**Q-V31-1:** Ce afișează "Symbol Grid" pentru V31?
- [ ] A: Lista tuturor simbolurilor cu preț curent
- [ ] B: Simbolurile analizate în ciclu curent cu direcție și scor
- [ ] C: Doar simbolurile care au generat setup-uri
- [ ] D: Toate simbolurile cu istoric complet

**Q-V31-2:** Ce înseamnă scorul afișat (ex: "7/10")?
- [ ] A: Scorul de încredere al predicției
- [ ] B: Numărul de condiții îndeplinite din total
- [ ] C: Raportul câștig/pierdere
- [ ] D: Procentajul de succes istoric

**Q-V31-3:** Ce face culoarea de fundal a unui simbol în grid?
- [ ] A: Verde = cumpărare, Roșu = vânzare, Gri = neutru
- [ ] B: Verde = setup validat, Roșu = setup respins, Galben = în analiză
- [ ] C: Culoare random pentru fiecare simbol
- [ ] D: Gradient bazat pe volum

**Q-V31-4:** Ce se întâmplă la click pe un simbol din grid?
- [ ] A: Deschide chart-ul MT5 pentru simbol
- [ ] B: Arată detaliile analizei (indicatori, scor breakdown)
- [ ] C: Plasează ordin direct
- [ ] D: Nimic, doar hover effect

**Q-V31-5:** Cât de des se actualizează Symbol Grid?
- [ ] A: La fiecare ciclu de analiză (când robotul termină)
- [ ] B: La fiecare 5 secunde
- [ ] C: La fiecare minut
- [ ] D: Doar la refresh manual

### Sectiunea: Ciclu de Analiză

**Q-V31-6:** Ce arată "Progress Bar" pentru ciclul de analiză?
- [ ] A: Timpul rămas până la sfârșitul sesiunii
- [ ] B: Progresul analizei curente (32/32 simboluri)
- [ ] C: Procentul de profit realizat
- [ ] D: Nivelul de încărcare al serverului

**Q-V31-7:** Ce afișează "Current Symbol"?
- [ ] A: Simbolul care se analizează în acest moment
- [ ] B: Ultimul simbol analizat
- [ ] C: Simbolul cu cel mai mare scor
- [ ] D: Simbolul selectat de utilizator

**Q-V31-8:** Ce înseamnă "Phase: Complete" vs "Phase: Analyzing"?
- [ ] A: Complete = ciclu terminat, Analyzing = în desfășurare
- [ ] B: Complete = toate tranzacțiile închise, Analyzing = deschise
- [ ] C: Complete = robot oprit, Analyzing = robot pornit
- [ ] D: Nu are semnificație, doar animație

### Sectiunea: Setup-uri Incomplete

**Q-V31-9:** Ce sunt "Setup-urile Incomplete"?
- [ ] A: Setups găsite dar fără confirmare finală (scor < 6)
- [ ] B: Setups care au expirat
- [ ] C: Setups așteptând aprobare manuală
- [ ] D: Erori în analiză

**Q-V31-10:** Ce acțiuni pot fi luate pe un setup incomplet?
- [ ] A: Doar vizualizare
- [ ] B: Forțare tranzacție (override scor)
- [ ] C: Modificare parametri și re-analiză
- [ ] D: Toate cele de mai sus

**Q-V31-11:** Ce informații afișează lista de setup-uri incomplete?
- [ ] A: Simbol, direcție, scor, motiv respingere
- [ ] B: Doar simbolul și timpul
- [ ] C: Toate detaliile tehnice (RSI, Stochastic, etc.)
- [ ] D: Doar numărul total

### Sectiunea: Decizii Robot (Thinking Process)

**Q-V31-12:** Vrei să vezi "gândirea" robotului în timp real?
- [ ] A: Da, vreau să văd fiecare pas din analiză
- [ ] B: Doar rezultatul final (scorul)
- [ ] C: Doar dacă eșuează (pentru debugging)
- [ ] D: Nu, e prea multă informație

**Q-V31-13:** Ce detalii din "thinking process" vrei să vezi?
- [ ] A: Fiecare indicator calculat (RSI, Stoch, EMA)
- [ ] B: Condițiile îndeplinite vs. neîndeplinite
- [ ] C: Scorul parțial la fiecare pas
- [ ] D: Toate cele de mai sus

**Q-V31-14:** Unde să apară "thinking process"?
- [ ] A: Într-un panel separat "Robot Journal"
- [ ] B: Tooltip la hover pe simbol
- [ ] C: Modal la click pe simbol
- [ ] D: În consolă (doar pentru debugging)

---

## 🔷 CONTAINER: V32 LONDON BREAKOUT

### Secțiunea: Timp și Sesiune

**Q-V32-1:** Ce arată "London Time"?
- [ ] A: Ora curentă în Londra (GMT/BST)
- [ ] B: Timpul rămas până la deschiderea sesiunii
- [ ] C: Timpul de funcționare al robotului
- [ ] D: Ora serverului

**Q-V32-2:** Ce afișează "Session Timer"?
- [ ] A: Timpul rămas până la sfârșitul sesiunii London
- [ ] B: Timpul scurs de la începutul sesiunii
- [ ] C: Countdown până la formarea OR
- [ ] D: Toate cele de mai sus, în funcție de fază

**Q-V32-3:** Ce faze ale sesiunui ar trebui să văd?
- [ ] A: Before Session, OR Formation, Main Session, Extended
- [ ] B: Doar Open și Close
- [ ] C: Active și Inactive
- [ ] D: Pre-market, Market, Post-market

### Secțiunea: Opening Range (OR)

**Q-V32-4:** Ce este "OR High" și "OR Low"?
- [ ] A: Maximul și minimul din prima oră de tranzacționare (08:00-09:00)
- [ ] B: Maximul și minimul din întreaga sesiune
- [ ] C: Nivelurile de rezistență și suport calculate
- [ ] D: Prețurile de deschidere și închidere ale zilei

**Q-V32-5:** Când se formează OR?
- [ ] A: 08:00-08:15 (15 minute)
- [ ] B: 08:00-09:00 (1 oră)
- [ ] C: 08:00-08:30 (30 minute)
- [ ] D: Variabil, configurabil

**Q-V32-6:** Ce se întâmplă după ce OR este format?
- [ ] A: Robotul așteaptă breakout
- [ ] B: Robotul plasează ordine imediat
- [ ] C: Robotul oprește analiza
- [ ] D: Nimic special

**Q-V32-7:** Vrei să vezi grafic vizual al OR?
- [ ] A: Da, o linie cu high/low pe un mini-chart
- [ ] B: Doar valorile numerice sunt suficiente
- [ ] C: Da, cu zona de OR colorată
- [ ] D: Nu e necesar

### Secțiunea: Asia Session Data

**Q-V32-8:** Ce este "Asia Range"?
- [ ] A: Range-ul format în sesiunea asiatică (00:00-08:00 GMT)
- [ ] B: Lista simbolurilor asiatice
- [ ] C: Timpul de funcționare în Asia
- [ ] D: Nu e relevant pentru London Breakout

**Q-V32-9:** Ce înseamnă "Asia Compressed"?
- [ ] A: Range-ul Asia este sub X pips (configurabil)
- [ ] B: Volumul de tranzacționare este scăzut
- [ ] C: Robotul comprimă datele pentru analiză
- [ ] D: Eroare de date

**Q-V32-10:** Cum folosește robotul Asia Range?
- [ ] A: Pentru a calcula targeturi de profit
- [ ] B: Pentru a filtra breakouts false
- [ ] C: Ca suport/rezistență suplimentar
- [ ] D: Nu îl folosește direct

### Secțiunea: Semnale și Tranzacții

**Q-V32-11:** Ce arată "Breakout Status"?
- [ ] A: Așteptare / Breakout Detectat / Trade Executat
- [ ] B: Doar prețul curent
- [ ] C: Volumul de tranzacționare
- [ ] D: Spread-ul curent

**Q-V32-12:** Ce tipuri de setup ar trebui să văd?
- [ ] A: Type A (breakout puternic) și Type B (pullback)
- [ ] B: Doar Buy și Sell
- [ ] C: Aggressive și Conservative
- [ ] D: Nu e relevant

**Q-V32-13:** Ce arată "Body Percent" și "Wick Percent"?
- [ ] A: Raportul corp vs. umbra în candlestick-ul breakout
- [ ] B: Probabilitatea de succes
- [ ] C: Procentul de profit/pierdere
- [ ] D: Nivelul de încredere

**Q-V32-14:** Vrei notificare vizuală/sonoră la breakout?
- [ ] A: Da, popup + sunet
- [ ] B: Doar schimbare culoare în dashboard
- [ ] C: Doar în log
- [ ] D: Nu e necesar

### Secțiunea: Statistici în Timp Real

**Q-V32-15:** Ce statistici vrei să vezi în timp real?
- [ ] A: Trades today (ex: 1/2), Win/Loss ratio, Total P&L
- [ ] B: Doar numărul de tranzacții
- [ ] C: Doar profitul total
- [ ] D: Toate detaliile (durată, sl/tp hit, etc.)

**Q-V32-16:** Ce înseamnă "Type B Pending"?
- [ ] A: Așteaptă confirmare pentru pullback
- [ ] B: Ordin plasat, așteaptă execuție
- [ ] C: Tranzacție în desfășurare
- [ ] D: Eroare în execuție

---

## 🔷 CONTAINER: V33 NY BREAKOUT

### Secțiunea: Pre-Session Analysis

**Q-V33-1:** Ce este "Pre-Session High/Low"?
- [ ] A: Maximul/minimul dinainte de sesiunea NY (11:30-13:00 EST)
- [ ] B: Maximul/minimul din sesiunea London
- [ ] C: Nivelurile de deschidere
- [ ] D: Nu e relevant

**Q-V33-2:** Cum diferă V33 de V32?
- [ ] A: V33 are pre-session analysis, V32 are Asia
- [ ] B: V33 tranzacționează EURUSD, V32 GBPUSD
- [ ] C: V33 folosește alte indicatori
- [ ] D: Nu diferă semnificativ

**Q-V33-3:** Ce orașe/sesiuni influențează V33?
- [ ] A: Doar New York
- [ ] B: London + New York
- [ ] C: Asia + London + New York
- [ ] D: Toate sesiunile

---

## 🔷 CONTAINER: COMENZI ÎN AȘTEPTARE (QUEUE)

### Q-QUEUE-1: Ce comenzi pot apărea în queue?
- [ ] A: Open Position, Close Position, Modify SL/TP
- [ ] B: Doar deschidere poziții
- [ ] C: Doar închidere poziții
- [ ] D: Toate tipurile de operațiuni

### Q-QUEUE-2: Ce se întâmplă cu o comandă în așteptare?
- [ ] A: Se execută automat când clientul e disponibil
- [ ] B: Rămâne în coadă până la executare sau anulare
- [ ] C: Expiră după X minute
- [ ] D: Se șterge automat la sfârșitul zilei

### Q-QUEUE-3: Ce informații afișează pentru fiecare comandă?
- [ ] A: Tip, simbol, volum, preț target, timestamp
- [ ] B: Doar tipul și simbolul
- [ ] C: Toate detaliile incluzând SL/TP
- [ ] D: Doar ID-ul comenzii

### Q-QUEUE-4: Ce acțiuni pot lua pe o comandă?
- [ ] A: Execute Now, Cancel, Modify
- [ ] B: Doar Cancel
- [ ] C: Doar Execute Now
- [ ] D: Niciuna, doar vizualizare

### Q-QUEUE-5: Vrei notificare când o comandă e executată?
- [ ] A: Da, toast notification
- [ ] B: Da, sunet + notificare
- [ ] C: Doar update în listă
- [ ] D: Nu e necesar

---

## 🔷 CONTAINER: JURNAL ROBOT (Robot Journal)

### Q-JOURNAL-1: Ce vrei să vezi în jurnalul robotului?
- [ ] A: Fiecare decizie luată și motivația
- [ ] B: Doar tranzacțiile executate
- [ ] C: Doar erorile
- [ ] D: Doar statisticile

### Q-JOURNAL-2: Cât de detaliat să fie jurnalul?
- [ ] A: Fiecare pas din analiză (RSI=X, Stoch=Y, etc.)
- [ ] B: Rezumat la nivel înalt
- [ ] C: Doar acțiunile (buy/sell)
- [ ] D: Configurabil per utilizator

### Q-JOURNAL-3: Filtre pentru jurnal:
- [ ] A: Per robot, per nivel (info/warning/error), per perioadă
- [ ] B: Doar per robot
- [ ] C: Doar per perioadă
- [ ] D: Fără filtre

### Q-JOURNAL-4: Export jurnal:
- [ ] A: CSV, PDF
- [ ] B: Doar CSV
- [ ] C: Doar vizualizare
- [ ] D: Nu e necesar

---

## 🔷 SINCRONIZARE LIVE - Funcționalități Avansate

### Q-LIVE-1: Ce înseamnă "sincronizare live" pentru tine?
- [ ] A: Datele se actualizează în timp real (sub 1 secundă)
- [ ] B: Actualizare la fiecare 5 secunde e suficient
- [ ] C: Actualizare la fiecare ciclu de analiză
- [ ] D: La cerere (refresh manual)

### Q-LIVE-2: Ce metodă de update preferi?
- [ ] A: WebSocket (push instant de la server)
- [ ] B: Polling (client cere la intervale)
- [ ] C: Server-Sent Events (SSE)
- [ ] D: Hibrid (WebSocket pentru critical, polling pentru restul)

### Q-LIVE-3: Ce se întâmplă când robotul ia o decizie?
- [ ] A: Vreau să văd imediat în dashboard (fără refresh)
- [ ] B: E suficient să văd la următorul poll
- [ ] C: Vreau notificare popup
- [ ] D: Vreau notificare sonoră

### Q-LIVE-4: Cum vrei să vezi "gândirea" robotului?
- [ ] A: Stream live în timp real (ca un terminal)
- [ ] B: Pas cu pas, cu delay de 1 secundă între pași
- [ ] C: Doar rezultatul final
- [ ] D: Doar când eșuează

### Q-LIVE-5: Ce date vrei să vezi în timp real?
- [ ] A: Tot (prețuri, indicatori, decizii, execuții)
- [ ] B: Doar deciziile și execuțiile
- [ ] C: Doar execuțiile (trade-uri deschise/închise)
- [ ] D: Doar profitul total

---

## 🔷 ELEMENTE COMUNE (Toți Roboții)

### Q-COMMON-1: Ce informații generale vrei să vezi pentru orice robot?
- [ ] A: Status, uptime, ultimul ciclu, profit azi
- [ ] B: Doar status (pornit/oprit)
- [ ] C: Doar profit
- [ ] D: Doar uptime

### Q-COMMON-2: Cum vrei să arate statusul robotului?
- [ ] A: Text (Running/Stopped) + culoare (Verde/Roșu)
- [ ] B: Iconiță (▶️/⏹️) + badge colorat
- [ ] C: LED animat (pulsează când rulează)
- [ ] D: Toate cele de mai sus

### Q-COMMON-3: Ce acțiuni vrei să ai pentru fiecare robot?
- [ ] A: Start, Stop, Restart, View Logs
- [ ] B: Doar Start și Stop
- [ ] C: Doar View Logs
- [ ] D: Fără acțiuni, doar vizualizare

### Q-COMMON-4: Cum vrei să fie organizate informațiile?
- [ ] A: Tab-uri: Overview, Analysis, Trades, Logs, Settings
- [ ] B: Toate într-o pagină lungă
- [ ] C: Sidebar cu secțiuni
- [ ] D: Accordion (expand/collapse)

---

## 🔷 PERFORMANȚĂ ȘI UI

### Q-PERF-1: Ce prioritate are viteza de update?
- [ ] A: Maximă (1 secundă sau mai puțin)
- [ ] B: Ridicată (5 secunde)
- [ ] C: Medie (30 secunde)
- [ ] D: Scăzută (la cerere)

### Q-PERF-2: Ce faci când robotul e oprit?
- [ ] A: Arăt ultima analiză salvată cu timestamp
- [ ] B: Arăt mesaj "Robot Offline - Last seen X min ago"
- [ ] C: Arăt placeholder gol
- [ ] D: Ascund complet secțiunea

### Q-PERF-3: Cum gestionezi erorile de conexiune?
- [ ] A: Retry automat + mesaj utilizator
- [ ] B: Doar mesaj de eroare
- [ ] C: Ignor și încerc la următorul poll
- [ ] D: Log în consolă doar

---

## ✅ TOTAL: 80+ ÎNTREBĂRI

**După ce îmi trimiți răspunsurile = 120+ Test Cases + Implementare completă + Echipa la treabă! 🚀**
