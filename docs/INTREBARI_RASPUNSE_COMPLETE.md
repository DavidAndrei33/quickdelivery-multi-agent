# RĂSPUNSURI ÎNTREBĂRI CONTAINE 8-19
## Data: 2026-03-29 07:52 UTC
## Status: COMPLET (53/53 întrebări răspunse)

---

## 🔷 CONTAINER 8: SETUP-URI INCOMPLETE

**Q8.1:** Ce e un "Setup Incomplet"? ✅ **D: Toate cele de mai sus**
- Setup găsit dar nu s-a deschis tranzacție
- Setup în așteptare
- Setup respins după re-analiză

**Q8.2:** Cât timp rămâne un setup în listă? ✅ **C: Până când devine trade sau expiră**

**Q8.3:** Ce acțiuni pot fi luate pe un setup? ✅ **B, C, D: Multiple**
- Forțare trade manual
- Ignorare/ștergere
- Modificare parametri și re-verificare

**Q8.4:** Ce informații afișează? ✅ **D: Toate cele de mai sus**
- Simbol, direcție, scor, motiv respingere
- Preț entry, SL, TP, R:R calculat
- Timestamp identificare, robot care a găsit

---

## 🔷 CONTAINER 9: COMENZI ÎN AȘTEPTARE (QUEUED)

**Q9.1:** Ce comenzi pot fi în așteptare? ✅ **D: Toate tipurile de operațiuni**

**Q9.2:** Ce se întâmplă cu o comandă în așteptare? ✅ **B: Rămâne în coadă până la executare sau timeout**

**Q9.3:** Timeout pentru comenzi? ✅ **D: Niciodată (până la executare)**

**Q9.4:** Ce afișează pentru fiecare comandă? ✅ **D: Toate cele de mai sus**

**Q9.5:** Acțiuni posibile pe o comandă în așteptare? ✅ **A, B, C: Multiple**
- Anulare comandă
- Modificare parametri
- Forțare executare imediată

---

## 🔷 CONTAINER 10: PERFORMANȚĂ PE SIMBOLURI

**Q10.1:** Ce metrici afișează per simbol? ✅ **D: Toate cele de mai sus**
- Win rate, Profit total, Nr. tranzacții, Profit mediu
- R:R mediu, Durată medie, Cel mai bun/worst trade
- Perioada analizată

**Q10.2:** Cum se calculează Win Rate? ✅ **A, D: Multiple**
- Tranzacții câștigătoare / Total tranzacții
- Configurabil (exclude breakeven)

**Q10.3:** Perioada implicită pentru statistici? ✅ **D: Configurabil**

**Q10.4:** Ce se întâmplă la click pe un simbol? ✅ **A, B, C: Multiple**
- Modal cu detalii complete
- Chart cu evoluția profitului
- Filtrează istoricul

**Q10.5:** Sortare și filtre? ✅ **D: Toate cele de mai sus**

---

## 🔷 CONTAINER 11: SYSTEM HEALTH

**Q11.1:** Ce componente monitorizează? ✅ **D: Toate cele de mai sus**
- MT5 Core Server, PostgreSQL, VPS Bridge
- Roboți Python, MT5 EA
- Resurse sistem (CPU, RAM, Disk)

**Q11.2:** Ce înseamnă statusurile? ✅ **A: 🟢 Healthy, 🟡 Warning, 🔴 Critical**

**Q11.3:** Ce acțiuni de remediere oferă? ✅ **A, C: Multiple**
- Restart service direct din dashboard
- Auto-remediere la erori minore

**Q11.4:** Istoric health checks? ✅ **A, C, D: Multiple**
- Ultimele 24 ore
- Ultima săptămână cu grafic uptime
- Configurabil

**Q11.5:** Alertare la probleme? ✅ **D: Toate cele de mai sus**
- Notificare în dashboard
- Email/SMS la erori critice
- Telegram alert

---

## 🔷 CONTAINER 12: STATISTICI TRADING

**Q12.1:** Ce statistici generale afișează? ✅ **D: Toate cele de mai sus**
- Profit/Loss total, Win rate %, Nr. tranzacții
- Profit zilnic/săptămânal/lunar
- Drawdown maxim, Profit factor, Expectancy

**Q12.2:** Agregare per cont sau global? ✅ **B: Per cont individual (selectabil)**

**Q12.3:** Perioade disponibile? ✅ **D: Toate cele de mai sus**
- Azi, Săptămâna, Luna, Anul, Tot istoricul
- Ultimele 30/60/90 zile
- Custom (date picker)

**Q12.4:** Export rapoarte? ✅ **B, C: Multiple**
- CSV cu date brute
- Excel cu grafice

---

## 🔷 CONTAINER 13: ASOCIERE CONTURI

**Q13.1:** Ce e "Asociere Conturi"? ✅ **D: Toate cele de mai sus**
- Link cont MT5 la utilizator
- Grupare conturi
- Permisiuni pe conturi

**Q13.2:** Cine poate vedea ce conturi? ✅ **A, D: Multiple**
- Admin: toate, User: doar conturile lui
- Configurabil per cont

**Q13.3:** Poți redenumi conturile? ✅ **D: Doar admin poate redenumi**

**Q13.4:** Etichetare/tagging conturi? ✅ **A: Tag-uri custom**

---

## 🔷 CONTAINER 14: UTILIZATORI ȘI PERMISIUNI

**Q14.1:** Roluri disponibile? ✅ **B, C: Multiple**
- Doar admin și user
- Roluri customizabile

**Q14.2:** Ce poate face un User vs Admin? ✅ **A: User: vede date, Admin: + modifică setări**

**Q14.3:** Autentificare? ✅ **A: Username/Password**

**Q14.4:** Sesizare activitate? ✅ **A, C: Multiple**
- Log cu toate acțiunile
- Audit trail complet

---

## 🔷 CONTAINER 15: EQUITY CURVE

**Q15.1:** Ce grafice afișează? ✅ **D: Toate cele de mai sus**
- Equity curve
- Drawdown chart
- Profit lunar/anual bar chart

**Q15.2:** Perioade disponibile? ✅ **D: Toate cele de mai sus**
- 1D, 1W, 1M, 3M, 6M, 1Y, All
- Custom date range

**Q15.3:** Agregare? ✅ **B: Per cont selectabil**

**Q15.4:** Interactivitate? ✅ **A, B, C: Multiple**
- Hover pentru detalii
- Zoom in/out
- Click pentru tranzacții

**Q15.5:** Export grafic? ✅ **D: Nu e necesar**

---

## 🔷 CONTAINER 16: GESTIONARE SERVICII

**Q16.1:** Ce servicii pot fi gestionate? ✅ **A, B, C: Toate componentele**

**Q16.2:** Ce acțiuni sunt disponibile? ✅ **D: Toate cele de mai sus**
- Start, Stop, Restart
- Status, Logs, Config
- Update versiune

**Q16.3:** Cine poate gestiona serviciile? ✅ **A, D: Multiple**
- Doar Admin
- Configurabil per serviciu

**Q16.4:** Confirmare la acțiuni critice? ✅ **A: Da, modal de confirmare**

**Q16.5:** Afișare logs în timp real? ✅ **A: Tail -f pe log-uri**

---

## 🔷 CONTAINER 17: ROBOȚI TRADING (GENERAL)

**Q17.1:** Ce roboți sunt afișați? ✅ **A, C, D: Multiple**
- V31, V32, V33 și viitori
- Toți roboții disponibili
- Configurabil care apar

**Q17.2:** Status per robot? ✅ **D: Toate detaliile**

**Q17.3:** Statistici per robot? ✅ **D: Toate cele de mai sus**

**Q17.4:** Acțiuni globale? ✅ **D: Toate cele de mai sus**
- Start All, Stop All
- Emergency Stop
- Pauză trading

---

## 🔷 CONTAINER 18: EXPERT LOGS

**Q18.1:** Ce log-uri afișează? ✅ **A: Log-uri din EA BrainBridge**

**Q18.2:** Niveluri de log? ✅ **A: DEBUG, INFO, WARNING, ERROR, CRITICAL**

**Q18.3:** Filtrare? ✅ **D: Toate cele de mai sus**

**Q18.4:** Live tail? ✅ **A: Update în timp real**

---

## 🔷 CONTAINER 19: JOURNAL

**Q19.1:** Ce intrări sunt în journal? ✅ **D: Toate cele de mai sus**

**Q19.2:** Format afișare? ✅ **A: Tabel cu detalii**

**Q19.3:** Filtrare journal? ✅ **D: Toate cele de mai sus**

**Q19.4:** Link către tranzacții? ✅ **A: Click pe deal → navigare în istoric**

---

## ✅ REZUMAT

**Total întrebări:** 53  
**Răspunse:** 53 (100%)  
**Multiple choice:** Majoritatea au selecții multiple (A+B+C etc.)

**Status:** GATA pentru generare Test Cases!
