# ÎNTREBĂRI PENTRU CONTAINELE 8-19
## Răspunde pentru a genera Test Cases complete

---

## 🔷 CONTAINER 8: SETUP-URI INCOMPLETE

**Q8.1:** Ce e un "Setup Incomplet"?
- [ ] **A:** Setup găsit dar nu s-a deschis tranzacție (SL/TP prea aproape, spread mare, etc.)
- [ ] **B:** Setup în așteptare (pending order plasat)
- [ ] **C:** Setup respins după re-analiză
- [ ] **D:** Toate cele de mai sus

**Q8.2:** Cât timp rămâne un setup în listă?
- [ ] **A:** 1 oră
- [ ] **B:** Până la sfârșitul sesiunii
- [ ] **C:** Până când devine trade sau expiră
- [ ] **D:** Configurabil

**Q8.3:** Ce acțiuni pot fi luate pe un setup?
- [ ] **A:** Doar vizualizare
- [ ] **B:** Forțare trade manual
- [ ] **C:** Ignorare/ștergere
- [ ] **D:** Modificare parametri și re-verificare

**Q8.4:** Ce informații afișează?
- [ ] **A:** Simbol, direcție, scor, motiv respingere
- [ ] **B:** Preț entry, SL, TP, R:R calculat
- [ ] **C:** Timestamp identificare, robot care a găsit
- [ ] **D:** Toate cele de mai sus

---

## 🔷 CONTAINER 9: COMENZI ÎN AȘTEPTARE (QUEUED)

**Q9.1:** Ce comenzi pot fi în așteptare?
- [ ] **A:** Open position, Close position, Modify SL/TP
- [ ] **B:** Doar comenzi manuale din dashboard
- [ ] **C:** Doar comenzi automate de la roboți
- [ ] **D:** Toate tipurile de operațiuni

**Q9.2:** Ce se întâmplă cu o comandă în așteptare?
- [ ] **A:** Se execută automat când clientul e disponibil
- [ ] **B:** Rămâne în coadă până la executare sau timeout
- [ ] **C:** Se șterge automat după X minute
- [ ] **D:** Utilizatorul trebuie să o re-trimită

**Q9.3:** Timeout pentru comenzi?
- [ ] **A:** 30 secunde
- [ ] **B:** 5 minute
- [ ] **C:** 1 oră
- [ ] **D:** Niciodată (până la executare)

**Q9.4:** Ce afișează pentru fiecare comandă?
- [ ] **A:** Tip comandă, parametri, timestamp, status
- [ ] **B:** Client target, prioritate, retry count
- [ ] **C:** Eroare (dacă a eșuat)
- [ ] **D:** Toate cele de mai sus

**Q9.5:** Acțiuni posibile pe o comandă în așteptare?
- [ ] **A:** Anulare comandă
- [ ] **B:** Modificare parametri
- [ ] **C:** Forțare executare imediată
- [ ] **D:** Doar vizualizare

---

## 🔷 CONTAINER 10: PERFORMANȚĂ PE SIMBOLURI

**Q10.1:** Ce metrici afișează per simbol?
- [ ] **A:** Win rate, Profit total, Nr. tranzacții, Profit mediu
- [ ] **B:** R:R mediu, Durată medie, Cel mai bun/worst trade
- [ ] **C:** Perioada analizată (ultimele 30 zile, tot istoricul)
- [ ] **D:** Toate cele de mai sus

**Q10.2:** Cum se calculează Win Rate?
- [ ] **A:** Tranzacții câștigătoare / Total tranzacții
- [ ] **B:** Profit pozitiv / Profit total
- [ ] **C:** Doar tranzacțiile închise complet
- [ ] **D:** Configurabil (ex: exclude breakeven)

**Q10.3:** Perioada implicită pentru statistici?
- [ ] **A:** Ultimele 30 zile
- [ ] **B:** Luna curentă
- [ ] **C:** Tot istoricul disponibil
- [ ] **D:** Ultimele 100 tranzacții

**Q10.4:** Ce se întâmplă la click pe un simbol?
- [ ] **A:** Modal cu detalii complete (toate tranzacțiile)
- [ ] **B:** Chart cu evoluția profitului pe acel simbol
- [ ] **C:** Filtrează istoricul doar pentru acel simbol
- [ ] **D:** Nimic

**Q10.5:** Sortare și filtre?
- [ ] **A:** Sortare după profit, win rate, nr. tranzacții
- [ ] **B:** Filtru perioadă (azi, săptămână, lună, tot)
- [ ] **C:** Filtru direcție (BUY/SELL separat)
- [ ] **D:** Toate cele de mai sus

---

## 🔷 CONTAINER 11: SYSTEM HEALTH

**Q11.1:** Ce componente monitorizează?
- [ ] **A:** MT5 Core Server, PostgreSQL, VPS Bridge
- [ ] **B:** Roboți Python (V31, V32, V33), MT5 EA
- [ ] **C:** Resurse sistem (CPU, RAM, Disk)
- [ ] **D:** Toate cele de mai sus

**Q11.2:** Ce înseamnă statusurile?
- [ ] **A:** 🟢 Healthy, 🟡 Warning (degradat), 🔴 Critical (down)
- [ ] **B:** Doar Online/Offline
- [ ] **C:** Cu procent de funcționalitate
- [ ] **D:** Culori diferite

**Q11.3:** Ce acțiuni de remediere oferă?
- [ ] **A:** Restart service direct din dashboard
- [ ] **B:** Notificare doar, remediere manuală
- [ ] **C:** Auto-remediere la erori minore
- [ ] **D:** Link către documentație troubleshooting

**Q11.4:** Istoric health checks?
- [ ] **A:** Ultimele 24 ore
- [ ] **B:** Ultimele 7 zile
- [ ] **C:** Ultima săptămână cu grafic uptime
- [ ] **D:** Doar status curent

**Q11.5:** Alertare la probleme?
- [ ] **A:** Notificare în dashboard (badge, banner)
- [ ] **B:** Email/SMS la erori critice
- [ ] **C:** Telegram alert
- [ ] **D:** Toate cele de mai sus

---

## 🔷 CONTAINER 12: STATISTICI TRADING

**Q12.1:** Ce statistici generale afișează?
- [ ] **A:** Profit/Loss total, Win rate %, Nr. tranzacții total
- [ ] **B:** Profit zilnic/săptămânal/lunar
- [ ] **C:** Drawdown maxim, Profit factor, Expectancy
- [ ] **D:** Toate cele de mai sus

**Q12.2:** Agregare per cont sau global?
- [ ] **A:** Global (toate conturile împreună)
- [ ] **B:** Per cont individual (selectabil)
- [ ] **C:** Ambele vizualizări
- [ ] **D:** Per grup de conturi

**Q12.3:** Perioade disponibile?
- [ ] **A:** Azi, Săptămâna, Luna, Anul, Tot istoricul
- [ ] **B:** Ultimele 30/60/90 zile
- [ ] **C:** Custom (date picker)
- [ ] **D:** Toate cele de mai sus

**Q12.4:** Export rapoarte?
- [ ] **A:** PDF cu statistici complete
- [ ] **B:** CSV cu date brute
- [ ] **C:** Excel cu grafice
- [ ] **D:** Doar vizualizare, fără export

---

## 🔷 CONTAINER 13: ASOCIERE CONTURI

**Q13.1:** Ce e "Asociere Conturi"?
- [ ] **A:** Link cont MT5 la utilizator dashboard
- [ ] **B:** Grupare conturi (familie, strategie, etc.)
- [ ] **C:** Permisiuni pe conturi
- [ ] **D:** Toate cele de mai sus

**Q13.2:** Cine poate vedea ce conturi?
- [ ] **A:** Admin: toate, User: doar conturile lui
- [ ] **B:** Toți utilizatorii văd toate conturile
- [ ] **C:** Bazat pe grupuri/roluri
- [ ] **D:** Configurabil per cont

**Q13.3:** Poți redenumi conturile?
- [ ] **A:** Da, nume friendly (ex: "Cont Principal", "Cont Test")
- [ ] **B:** Doar numele din MT5
- [ ] **C:** Nu, doar login number
- [ ] **D:** Doar admin poate redenumi

**Q13.4:** Etichetare/tagging conturi?
- [ ] **A:** Tag-uri custom (ex: "agresiv", "conservator", "test")
- [ ] **B:** Categorii predefinite
- [ ] **C:** Grupare colorată
- [ ] **D:** Nu e necesar

---

## 🔷 CONTAINER 14: UTILIZATORI ȘI PERMISIUNI

**Q14.1:** Roluri disponibile?
- [ ] **A:** Admin (toate drepturile), User (doar vizualizare), Guest (limitat)
- [ ] **B:** Doar admin și user
- [ ] **C:** Roluri customizabile
- [ ] **D:** Doar un utilizator (tu)

**Q14.2:** Ce poate face un User vs Admin?
- [ ] **A:** User: vede date, Admin: + modifică setări, pornește/oprește roboți
- [ ] **B:** User: doar istoric, Admin: tot
- [ ] **C:** User: conturile lui, Admin: toate conturile
- [ ] **D:** ___________________

**Q14.3:** Autentificare?
- [ ] **A:** Username/Password
- [ ] **B:** Doar token MT5
- [ ] **C:** 2FA (Two Factor Auth)
- [ ] **D:** IP whitelist

**Q14.4:** Sesizare activitate?
- [ ] **A:** Log cu toate acțiunile utilizatorilor
- [ ] **B:** Doar acțiuni critice (start/stop roboți)
- [ ] **C:** Audit trail complet
- [ ] **D:** Nu e necesar

---

## 🔷 CONTAINER 15: EQUITY CURVE 📉

**Q15.1:** Ce grafice afișează?
- [ ] **A:** Equity curve (evoluție capital)
- [ ] **B:** Drawdown chart (pierderi consecutive)
- [ ] **C:** Profit lunar/anual bar chart
- [ ] **D:** Toate cele de mai sus

**Q15.2:** Perioade disponibile?
- [ ] **A:** 1D, 1W, 1M, 3M, 6M, 1Y, All
- [ ] **B:** Doar lună curentă și total
- [ ] **C:** Custom date range
- [ ] **D:** Toate cele de mai sus

**Q15.3:** Agregare?
- [ ] **A:** Toate conturile împreună
- [ ] **B:** Per cont selectabil
- [ ] **C:** Ambele opțiuni
- [ ] **D:** Per grup de conturi

**Q15.4:** Interactivitate?
- [ ] **A:** Hover pentru detalii (profit la o anumită dată)
- [ ] **B:** Zoom in/out
- [ ] **C:** Click pe punct pentru tranzacțiile din ziua respectivă
- [ ] **D:** Static, doar vizualizare

**Q15.5:** Export grafic?
- [ ] **A:** PNG/SVG download
- [ ] **B:** Doar vizualizare
- [ ] **C:** Date brute pentru Excel
- [ ] **D:** Nu e necesar

---

## 🔷 CONTAINER 16: GESTIONARE SERVICII

**Q16.1:** Ce servicii pot fi gestionate?
- [ ] **A:** MT5 Core Server, Roboți (V31, V32, V33), EA Bridge
- [ ] **B:** PostgreSQL, VPS Bridge
- [ ] **C:** Toate componentele sistemului
- [ ] **D:** Doar roboții de trading

**Q16.2:** Ce acțiuni sunt disponibile?
- [ ] **A:** Start, Stop, Restart
- [ ] **B:** Status, Logs, Config
- [ ] **C:** Update versiune
- [ ] **D:** Toate cele de mai sus

**Q16.3:** Cine poate gestiona serviciile?
- [ ] **A:** Doar Admin
- [ ] **B:** Orice utilizator autentificat
- [ ] **C:** Doar tu (owner)
- [ ] **D:** Configurabil per serviciu

**Q16.4:** Confirmare la acțiuni critice?
- [ ] **A:** Da, modal de confirmare
- [ ] **B:** Doar pentru stop/restart
- [ ] **C:** Parolă la acțiuni critice
- [ ] **D:** Nu, se execută imediat

**Q16.5:** Afișare logs în timp real?
- [ ] **A:** Tail -f pe log-urile serviciului
- [ ] **B:** Ultimele 100 linii
- [ ] **C:** Download log complet
- [ ] **D:** Doar link către fișier log

---

## 🔷 CONTAINER 17: ROBOȚI TRADING (GENERAL)

**Q17.1:** Ce roboți sunt afișați?
- [ ] **A:** V31 TPL, V32 London, V33 NY, și viitori roboți
- [ ] **B:** Doar cei activi/configurați
- [ ] **C:** Toți roboții disponibili în sistem
- [ ] **D:** Configurabil care apar

**Q17.2:** Status per robot?
- [ ] **A:** Running, Stopped, Error, Paused
- [ ] **B:** Doar Online/Offline
- [ ] **C:** Cu uptime și last seen
- [ ] **D:** Toate detaliile

**Q17.3:** Statistici per robot?
- [ ] **A:** Tranzacții deschise, Win rate, Profit total
- [ ] **B:** Uptime, Erori, Resurse folosite
- [ ] **C:** Configurație curentă
- [ ] **D:** Toate cele de mai sus

**Q17.4:** Acțiuni globale?
- [ ] **A:** Start All, Stop All
- [ ] **B:** Emergency Stop (toți roboții)
- [ ] **C:** Pauză trading (păstrează analiza)
- [ ] **D:** Toate cele de mai sus

---

## 🔷 CONTAINER 18: EXPERT LOGS

**Q18.1:** Ce log-uri afișează?
- [ ] **A:** Log-uri din EA BrainBridge (conectare, erori, execuție)
- [ ] **B:** Log-uri din roboți Python
- [ ] **C:** Log-uri din MT5 terminal
- [ ] **D:** Toate cele de mai sus

**Q18.2:** Niveluri de log?
- [ ] **A:** DEBUG, INFO, WARNING, ERROR, CRITICAL
- [ ] **B:** Doar ERROR și CRITICAL
- [ ] **C:** INFO și mai sus
- [ ] **D:** Configurabil per utilizator

**Q18.3:** Filtrare?
- [ ] **A:** Per nivel log, per sursă, per perioadă
- [ ] **B:** Căutare text în log-uri
- [ ] **C:** Doar ultimele X linii
- [ ] **D:** Toate cele de mai sus

**Q18.4:** Live tail?
- [ ] **A:** Update în timp real (auto-refresh)
- [ ] **B:** Refresh manual
- [ ] **C:** WebSocket pentru live updates
- [ ] **D:** Download fișier log

---

## 🔷 CONTAINER 19: JOURNAL

**Q19.1:** Ce intrări sunt în journal?
- [ ] **A:** Dealuri (tranzacții executate), Ordere (plasate/modificate/șterse)
- [ ] **B:** Erori de execuție, Requotes
- [ ] **C:** Modificări balans (depuneri/retrageri)
- [ ] **D:** Toate cele de mai sus

**Q19.2:** Format afișare?
- [ ] **A:** Tabel cu: Timp, Tip, Simbol, Volum, Preț, Rezultat
- [ ] **B:** Format text ca în MT5
- [ ] **C:** Timeline vizual
- [ ] **D:** Ambele (tabel + raw)

**Q19.3:** Filtrare journal?
- [ ] **A:** Per cont, per simbol, per tip operațiune
- [ ] **B:** Per perioadă
- [ ] **C:** Doar buy/sell
- [ ] **D:** Toate cele de mai sus

**Q19.4:** Link către tranzacții?
- [ ] **A:** Click pe deal → navigare la tranzacție în istoric
- [ ] **B:** Doar informație, fără link
- [ ] **C:** Modal cu detalii complete
- [ ] **D:** Export în istoric

---

## ✅ INSTRUCȚIUNI DE RĂSPUNS

**Opțiuni:**
1. **Copiezi lista** și bagi "x" în [ ] pentru răspunsurile tale
2. **Sau îmi spui** "Q8.1=A, Q8.2=C..." etc.
3. **Sau răspunzi** doar la ce e diferit de A (presupun A default)

**După ce răspunzi:**
✅ Generez **53+ test cases noi**  
✅ **Total: 90+ test cases complete**  
✅ Pun **echipa la treabă** cu specificații clare! 🚀
