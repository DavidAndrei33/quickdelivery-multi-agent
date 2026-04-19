# Test Specification V3 - Trading Dashboard
## Generated: 2026-03-29 07:54 UTC
## Target: 90+ Test Cases for Containers 8-19

---

## 📊 OVERVIEW

| Container | Name | Target Tests | Actual Tests | Coverage |
|-----------|------|--------------|--------------|----------|
| 8 | Setup-uri Incomplete | 8 | 8 | 100% |
| 9 | Comenzi în Așteptare | 10 | 10 | 100% |
| 10 | Performanță pe Simboluri | 10 | 10 | 100% |
| 11 | System Health | 8 | 8 | 100% |
| 12 | Statistici Trading | 8 | 8 | 100% |
| 13 | Asociere Conturi | 6 | 6 | 100% |
| 14 | Utilizatori și Permisiuni | 6 | 6 | 100% |
| 15 | Equity Curve | 8 | 8 | 100% |
| 16 | Gestionare Servicii | 8 | 8 | 100% |
| 17 | Roboți Trading | 8 | 8 | 100% |
| 18 | Expert Logs | 5 | 5 | 100% |
| 19 | Journal | 5 | 5 | 100% |
| **TOTAL** | - | **90** | **90** | **100%** |

---

## 🔷 CONTAINER 8: SETUP-URI INCOMPLETE (8 Tests)

### TC-8.1: Definire Setup Incomplet
**Precondiții:**
- Dashboard accesibil
- Robot identificat setup valid
- Setup nu a generat trade

**Pași:**
1. Navighează la Container 8
2. Verifică lista de setup-uri incomplete
3. Identifică un setup în stare "în așteptare"

**Rezultat Așteptat:**
- Setup-ul apare în listă cu status corespunzător
- Afișează: simbol, direcție, scor, motiv respingere/ateptare

**Status:** PENDING
**Asignat:** builder-4

---

### TC-8.2: Expirare Setup
**Precondiții:**
- Setup în listă de >24 ore (sau perioada configurată)
- Setup nu a fost executat

**Pași:**
1. Așteaptă perioada de expirare
2. Verifică dacă setup-ul dispare din listă

**Rezultat Așteptat:**
- Setup-ul este eliminat automat după expirare
- Sau marcat ca "expirat"

**Status:** PENDING
**Asignat:** builder-4

---

### TC-8.3: Forțare Trade Manual
**Precondiții:**
- Setup în listă cu status "în așteptare"
- Utilizator are permisiuni de trading

**Pași:**
1. Selectează setup din listă
2. Click "Forțare Trade"
3. Confirmă acțiunea în modal

**Rezultat Așteptat:**
- Trade-ul este executat
- Setup-ul dispare din lista de incomplete
- Apare în istoricul tranzacții

**Status:** PENDING
**Asignat:** builder-4

---

### TC-8.4: Ignorare/Ștergere Setup
**Precondiții:**
- Setup în listă

**Pași:**
1. Selectează setup
2. Click "Ignoră" sau "Șterge"
3. Confirmă acțiunea

**Rezultat Așteptat:**
- Setup-ul este eliminat din listă
- Log în jurnal cu acțiunea

**Status:** PENDING
**Asignat:** builder-4

---

### TC-8.5: Modificare Parametri Setup
**Precondiții:**
- Setup în listă cu parametri configurabili

**Pași:**
1. Click pe setup pentru editare
2. Modifică SL, TP, sau alți parametri
3. Click "Salvează și Re-verifică"

**Rezultat Așteptat:**
- Parametrii sunt actualizați
- Setup-ul este re-evaluat
- Scorul se poate schimba

**Status:** PENDING
**Asignat:** builder-4

---

### TC-8.6: Afișare Informații Complete
**Precondiții:**
- Minim un setup în listă

**Pași:**
1. Deschide Container 8
2. Verifică coloanele afișate

**Rezultat Așteptat:**
- Simbol, Direcție (Buy/Sell), Scor, Motiv
- Preț Entry, SL, TP, R:R calculat
- Timestamp identificare, Robot sursă

**Status:** PENDING
**Asignat:** builder-4

---

### TC-8.7: Setup Respins după Re-analiză
**Precondiții:**
- Setup în așteptare
- Condițiile de piață se schimbă

**Pași:**
1. Așteaptă re-analiză automată
2. Verifică statusul setup-ului

**Rezultat Așteptat:**
- Setup marcat ca "respins"
- Motivul respingerii afișat
- Rămâne în listă sau e șters (configurabil)

**Status:** PENDING
**Asignat:** builder-4

---

### TC-8.8: Setup Devine Trade Automat
**Precondiții:**
- Setup cu condiții pentru executare automată
- Scor >= prag configurat

**Pași:**
1. Așteaptă condiții de executare
2. Monitorizează conversia

**Rezultat Așteptat:**
- Setup-ul devine automat trade
- Dispare din lista de incomplete
- Apare în Container 1 (Active Trades)

**Status:** PENDING
**Asignat:** builder-4

---

## 🔷 CONTAINER 9: COMENZI ÎN AȘTEPTARE (10 Tests)

### TC-9.1: Comandă în Așteptare - Tipuri Diverse
**Precondiții:**
- Sistem activ
- Posibilitate de a plasa diverse tipuri de comenzi

**Pași:**
1. Plasează Pending Order (Buy Limit, Sell Limit, Buy Stop, Sell Stop)
2. Verifică Container 9

**Rezultat Așteptat:**
- Toate tipurile de comenzi apar în listă
- Fiecare comandă afișează detaliile corespunzătoare

**Status:** PENDING
**Asignat:** builder-6

---

### TC-9.2: Comandă Rămâne în Coadă
**Precondiții:**
- Comandă plasată
- Prețul de piață nu atinge nivelul comenzii

**Pași:**
1. Plasează comandă cu preț distanțat de piață
2. Așteaptă 5 minute
3. Verifică statusul în Container 9

**Rezultat Așteptat:**
- Comanda rămâne în coadă
- Status: "Pending"
- Nu există timeout implicit

**Status:** PENDING
**Asignat:** builder-6

---

### TC-9.3: Timeout pentru Comenzi
**Precondiții:**
- Comandă în așteptare de >30 zile

**Pași:**
1. Verifică comandă veche în sistem
2. Observă comportamentul

**Rezultat Așteptat:**
- Comanda NU expiră automat
- Rămâne în coadă până la executare sau anulare manuală

**Status:** PENDING
**Asignat:** builder-6

---

### TC-9.4: Afișare Detalii Comandă
**Precondiții:**
- Minim o comandă în așteptare

**Pași:**
1. Deschide Container 9
2. Verifică coloanele afișate

**Rezultat Așteptat:**
- Simbol, Tip (Limit/Stop), Direcție
- Preț entry, SL, TP
- Volume, Timp plasare
- Status comandă

**Status:** PENDING
**Asignat:** builder-6

---

### TC-9.5: Anulare Comandă
**Precondiții:**
- Comandă activă în așteptare
- Utilizator are permisiuni

**Pași:**
1. Selectează comandă din listă
2. Click "Anulează"
3. Confirmă în modal

**Rezultat Așteptat:**
- Comanda este anulată
- Dispare din Container 9
- Log în jurnal

**Status:** PENDING
**Asignat:** builder-6

---

### TC-9.6: Modificare Parametri Comandă
**Precondiții:**
- Comandă activă în așteptare

**Pași:**
1. Selectează comandă
2. Click "Modifică"
3. Schimbă preț entry, SL, sau TP
4. Salvează modificările

**Rezultat Așteptat:**
- Parametrii sunt actualizați în MT5
- Lista se refresh-ează cu noile valori

**Status:** PENDING
**Asignat:** builder-6

---

### TC-9.7: Forțare Executare Imediată
**Precondiții:**
- Comandă în așteptare
- Utilizator vrea executare la prețul curent

**Pași:**
1. Selectează comandă
2. Click "Execută Acum"
3. Confirmă acțiunea

**Rezultat Așteptat:**
- Comanda este executată la prețul de piață curent
- Devine trade activ
- Mutată în Container 1

**Status:** PENDING
**Asignat:** builder-6

---

### TC-9.8: Comandă Executată Automat
**Precondiții:**
- Comandă în așteptare
- Prețul de piață atinge nivelul comenzii

**Pași:**
1. Așteaptă mișcarea prețului
2. Monitorizează Container 9

**Rezultat Așteptat:**
- Comanda este executată automat
- Dispare din Container 9
- Apare în Container 1 ca trade activ

**Status:** PENDING
**Asignat:** builder-6

---

### TC-9.9: Sortare și Filtre Comenzi
**Preconditii:**
- Multiple comenzi în listă

**Pași:**
1. Click pe header coloană pentru sortare
2. Aplică filtre (după simbol, tip, direcție)
3. Verifică rezultatele

**Rezultat Așteptat:**
- Sortare funcționează corect
- Filtrele reduc lista conform criteriilor
- Reset filtre funcționează

**Status:** PENDING
**Asignat:** builder-6

---

### TC-9.10: Refresh Date în Timp Real
**Precondiții:**
- Comenzi active în așteptare

**Pași:**
1. Deschide Container 9
2. Așteaptă modificări de preț
3. Observă lista

**Rezultat Așteptat:**
- Datele se actualizează în timp real
- Distanța până la prețul de entry se modifică
- Noi comenzi apar automat

**Status:** PENDING
**Asignat:** builder-6

---

## 🔷 CONTAINER 10: PERFORMANȚĂ PE SIMBOLURI (10 Tests)

### TC-10.1: Afișare Metrici Per Simbol
**Precondiții:**
- Istoric de tranzacții existent
- Minim 5 simboluri diferite tranzacționate

**Pași:**
1. Deschide Container 10
2. Verifică lista de simboluri

**Rezultat Așteptat:**
- Fiecare simbol afișează:
  - Win rate %
  - Profit total
  - Număr tranzacții
  - Profit mediu per trade
  - R:R mediu
  - Durată medie
  - Cel mai bun trade
  - Cel mai prost trade
  - Perioada analizată

**Status:** PENDING
**Asignat:** builder-4

---

### TC-10.2: Calcul Win Rate
**Precondiții:**
- Istoric tranzacții cu wins și losses

**Pași:**
1. Selectează un simbol
2. Verifică numărul de tranzacții
3. Calculează manual win rate

**Rezultat Așteptat:**
- Win rate = Tranzacții câștigătoare / Total tranzacții
- Configurabil să excludă breakeven
- Calcul corect în procente

**Status:** PENDING
**Asignat:** builder-4

---

### TC-10.3: Perioadă Implicită Configurabilă
**Precondiții:**
- Container 10 deschis

**Pași:**
1. Verifică dropdown perioadă
2. Schimbă perioada implicită în setări
3. Reîncarcă pagina

**Rezultat Așteptat:**
- Perioada selectată se aplică
- Statisticile se recalculează
- Setarea persistă între sesiuni

**Status:** PENDING
**Asignat:** builder-4

---

### TC-10.4: Click pe Simbol - Modal Detalii
**Precondiții:**
- Listă de simboluri afișată

**Pași:**
1. Click pe un rând din tabel

**Rezultat Așteptat:**
- Se deschide modal cu detalii complete
- Toate statisticile extinse
- Grafice suplimentare

**Status:** PENDING
**Asignat:** builder-4

---

### TC-10.5: Click pe Simbol - Chart Evoluție
**Precondiții:**
- Listă de simboluri afișată

**Pași:**
1. Click pe un simbol
2. Navighează la tab "Evoluție"

**Rezultat Așteptat:**
- Chart cu evoluția profitului în timp
- Puncte marcate pentru fiecare trade
- Filtrare după perioadă

**Status:** PENDING
**Asignat:** builder-4

---

### TC-10.6: Click pe Simbol - Filtrare Istoric
**Precondiții:**
- Listă de simboluri afișată

**Pași:**
1. Click pe un simbol
2. Click "Vezi în Istoric"

**Rezultat Așteptat:**
- Redirecționare la Container 6 (Istoric)
- Filtru aplicat automat pentru simbolul selectat
- Doar tranzacțiile acelui simbol afișate

**Status:** PENDING
**Asignat:** builder-4

---

### TC-10.7: Sortare După Win Rate
**Precondiții:**
- Multiple simboluri în listă

**Pași:**
1. Click pe header "Win Rate"
2. Verifică ordinea
3. Click din nou pentru ordine inversă

**Rezultat Așteptat:**
- Simbolurile sortate după win rate
- Ordine descendentă/ascendentă la click repetat

**Status:** PENDING
**Asignat:** builder-4

---

### TC-10.8: Sortare După Profit Total
**Precondiții:**
- Multiple simboluri în listă

**Pași:**
1. Click pe header "Profit Total"
2. Verifică ordinea

**Rezultat Așteptat:**
- Simbolurile sortate după profit
- Cele mai profitabile primele/ultimele

**Status:** PENDING
**Asignat:** builder-4

---

### TC-10.9: Filtrare După Număr Minim Tranzacții
**Precondiții:**
- Simboluri cu diferite numere de tranzacții

**Pași:**
1. Aplică filtru "Min. 10 tranzacții"
2. Verifică lista rezultată

**Rezultat Așteptat:**
- Doar simbolurile cu ≥10 tranzacții afișate
- Statisticile mai relevante (sample size suficient)

**Status:** PENDING
**Asignat:** builder-4

---

### TC-10.10: Export Date Performanță
**Precondiții:**
- Date disponibile în Container 10

**Pași:**
1. Click buton "Export"
2. Selectează format CSV
3. Descarcă fișierul

**Rezultat Așteptat:**
- Fișier CSV generat cu toate datele
- Coloane corespunzătoare
- Date consistente cu afișarea

**Status:** PENDING
**Asignat:** builder-4

---

## 🔷 CONTAINER 11: SYSTEM HEALTH (8 Tests)

### TC-11.1: Monitorizare MT5 Core Server
**Precondiții:**
- Sistem MT5 rulează
- Container 11 deschis

**Pași:**
1. Verifică statusul MT5 Core Server

**Rezultat Așteptat:**
- Status afișat: 🟢 Healthy / 🟡 Warning / 🔴 Critical
- Metrici: uptime, conexiuni active, latență

**Status:** PENDING
**Asignat:** ops-1

---

### TC-11.2: Monitorizare PostgreSQL
**Precondiții:**
- Database rulează

**Pași:**
1. Verifică statusul PostgreSQL

**Rezultat Așteptat:**
- Status corespunzător
- Metrici: conexiuni, query time, spațiu disk

**Status:** PENDING
**Asignat:** ops-1

---

### TC-11.3: Monitorizare VPS Bridge
**Precondiții:**
- Bridge activ

**Pași:**
1. Verifică statusul VPS Bridge

**Rezultat Așteptat:**
- Status corespunzător
- Latență între VPS și MT5

**Status:** PENDING
**Asignat:** ops-1

---

### TC-11.4: Monitorizare Roboți Python
**Precondiții:**
- Roboți Python (V31, V32, V33) activi

**Pași:**
1. Verifică statusul fiecărui robot

**Rezultat Așteptat:**
- Status individual per robot
- Ultima activitate, erori recente

**Status:** PENDING
**Asignat:** ops-1

---

### TC-11.5: Monitorizare Resurse Sistem
**Precondiții:**
- Sistemul rulează

**Pași:**
1. Verifică secțiunea Resurse

**Rezultat Așteptat:**
- CPU usage %
- RAM usage %
- Disk usage %
- Trend istoric

**Status:** PENDING
**Asignat:** ops-1

---

### TC-11.6: Restart Service din Dashboard
**Precondiții:**
- Service oprit sau în eroare
- Utilizator are permisiuni admin

**Pași:**
1. Identifică service cu problemă
2. Click buton "Restart"
3. Confirmă în modal
4. Așteaptă finalizarea

**Rezultat Așteptat:**
- Service-ul repornește
- Status se actualizează la 🟢 Healthy
- Log înregistrat

**Status:** PENDING
**Asignat:** ops-1

---

### TC-11.7: Auto-Remediere Erori Minore
**Precondiții:**
- Eroare minoră detectată (de ex. reconectare MT5)

**Pași:**
1. Simulează deconectare temporară
2. Așteaptă 30 secunde
3. Verifică statusul

**Rezultat Așteptat:**
- Sistemul încearcă auto-remediere
- Dacă reușește: status revine la Healthy
- Notificare despre remediere automată

**Status:** PENDING
**Asignat:** ops-1

---

### TC-11.8: Istoric Health Checks
**Precondiții:**
- Istoric de health checks disponibil

**Pași:**
1. Navighează la secțiunea Istoric
2. Selectează perioada "Ultimele 24 ore"
3. Schimbă la "Ultima săptămână"

**Rezultat Așteptat:**
- Grafic uptime afișat
- Perioada selectabilă (configurabil)
- Statistici de disponibilitate per componentă

**Status:** PENDING
**Asignat:** ops-1

---

## 🔷 CONTAINER 12: STATISTICI TRADING (8 Tests)

### TC-12.1: Afișare Profit/Loss Total
**Precondiții:**
- Istoric de tranzacții existent

**Pași:**
1. Deschide Container 12
2. Verifică cardul P&L Total

**Rezultat Așteptat:**
- Suma corectă a tuturor profiturilor/pierderilor
- Diferențiere vizuală (verde/roșu)
- Actualizare în timp real

**Status:** PENDING
**Asignat:** builder-1

---

### TC-12.2: Afișare Win Rate Global
**Precondiții:**
- Istoric de tranzacții cu wins/losses

**Pași:**
1. Verifică metrica Win Rate

**Rezultat Așteptat:**
- Procent corect de tranzacții câștigătoare
- Comparare cu perioada anterioară

**Status:** PENDING
**Asignat:** builder-1

---

### TC-12.3: Afișare Drawdown Maxim
**Precondiții:**
- Istoric cu perioade de drawdown

**Pași:**
1. Verifică metrica Max Drawdown

**Rezultat Așteptat:**
- Valoare corectă a celui mai mare drawdown
- Procent și valoare monetară
- Perioada când a avut loc

**Status:** PENDING
**Asignat:** builder-1

---

### TC-12.4: Afișare Profit Factor
**Precondiții:**
- Istoric suficient de tranzacții

**Pași:**
1. Verifică metrica Profit Factor

**Rezultat Așteptat:**
- Calcul: Profit brut / Pierdere brută
- Valoare >1 = profitabil
- Interpretare vizuală

**Status:** PENDING
**Asignat:** builder-1

---

### TC-12.5: Agregare Per Cont Selectabil
**Precondiții:**
- Multiple conturi în sistem

**Pași:**
1. Selectează cont din dropdown
2. Verifică statisticile
3. Schimbă la alt cont

**Rezultat Așteptat:**
- Statisticile se recalculează pentru contul selectat
- Filtre independente per cont
- Opțiune "Toate conturile" pentru global

**Status:** PENDING
**Asignat:** builder-1

---

### TC-12.6: Perioade Predefinite
**Precondiții:**
- Container 12 deschis

**Pași:**
1. Selectează "Azi" din perioade
2. Selectează "Săptămâna"
3. Selectează "Luna"
4. Selectează "Anul"
5. Selectează "Tot istoricul"

**Rezultat Așteptat:**
- Fiecare selecție actualizează statisticile
- Date corecte pentru perioada selectată
- Resetare automată a filtrelor

**Status:** PENDING
**Asignat:** builder-1

---

### TC-12.7: Perioadă Custom Date Picker
**Precondiții:**
- Container 12 deschis

**Pași:**
1. Click pe "Perioadă custom"
2. Selectează data start
3. Selectează data end
4. Click "Aplică"

**Rezultat Așteptat:**
- Datele afișate pentru perioada selectată
- Validare: end > start
- Persistă în URL pentru share

**Status:** PENDING
**Asignat:** builder-1

---

### TC-12.8: Export CSV și Excel
**Precondiții:**
- Statistici disponibile

**Pași:**
1. Click "Export CSV"
2. Verifică fișierul descărcat
3. Click "Export Excel"
4. Verifică fișierul descărcat

**Rezultat Așteptat:**
- CSV: date brute, format tabular
- Excel: date + grafice încorporate
- Toate metricile incluse

**Status:** PENDING
**Asignat:** builder-1

---

## 🔷 CONTAINER 13: ASOCIERE CONTURI (6 Tests)

### TC-13.1: Link Cont MT5 la Utilizator
**Precondiții:**
- Cont MT5 existent în sistem
- Utilizator existent

**Pași:**
1. Navighează la Container 13
2. Click "Adaugă Asociere"
3. Selectează cont MT5
4. Selectează utilizator
5. Click "Salvează"

**Rezultat Așteptat:**
- Asocierea creată
- Contul apare în lista utilizatorului
- Log în audit trail

**Status:** PENDING
**Asignat:** builder-3

---

### TC-13.2: Grupare Conturi
**Precondiții:**
- Multiple conturi existente

**Pași:**
1. Selectează 2+ conturi
2. Click "Creează Grup"
3. Denumirește grupul
4. Salvează

**Rezultat Așteptat:**
- Grup creat
- Conturile afișate sub grup
- Posibilitate de expand/collapse

**Status:** PENDING
**Asignat:** builder-3

---

### TC-13.3: Permisiuni pe Conturi - Admin Vede Toate
**Precondiții:**
- Utilizator cu rol Admin
- Multiple conturi în sistem

**Pași:**
1. Logare ca Admin
2. Deschide Container 13

**Rezultat Așteptat:**
- Toate conturile afișate
- Acces complet la toate setările
- Posibilitate de modificare

**Status:** PENDING
**Asignat:** builder-3

---

### TC-13.4: Permisiuni pe Conturi - User Vede Doar Ale Lui
**Precondiții:**
- Utilizator cu rol User
- Conturi asociate utilizatorului

**Pași:**
1. Logare ca User
2. Deschide Container 13

**Rezultat Așteptat:**
- Doar conturile asociate afișate
- Fără opțiuni de editare
- View-only access

**Status:** PENDING
**Asignat:** builder-3

---

### TC-13.5: Redenumire Cont - Doar Admin
**Precondiții:**
- Utilizator Admin
- Cont existent

**Pași:**
1. Click pe nume cont
2. Editează numele
3. Salvează

**Rezultat Așteptat:**
- Numele actualizat
- Văzut în toate containerele
- Log în audit trail

**Bug Identificat:** ❌ **User-ul NU ar trebui să poată redenumi conturi** - conform Q13.3 doar admin poate redenumi. Verifică restricțiile de permisiuni.

**Status:** PENDING
**Asignat:** builder-3

---

### TC-13.6: Etichetare Tag-uri Custom
**Precondiții:**
- Cont existent

**Pași:**
1. Selectează cont
2. Click "Adaugă Tag"
3. Introdu tag-uri: "Demo", "Aggressive", "Test"
4. Salvează

**Rezultat Așteptat:**
- Tag-urile salvate
- Afișate lângă numele contului
- Filtre disponibile după tag-uri

**Status:** PENDING
**Asignat:** builder-3

---

## 🔷 CONTAINER 14: UTILIZATORI ȘI PERMISIUNI (6 Tests)

### TC-14.1: Roluri - Admin vs User
**Precondiții:**
- Sistem cu utilizatori existenți

**Pași:**
1. Deschide Container 14
2. Verifică lista de roluri

**Rezultat Așteptat:**
- Roluri disponibile: Admin, User
- Posibilitate de roluri customizabile
- Descriere clară per rol

**Status:** PENDING
**Asignat:** builder-3

---

### TC-14.2: Capabilități User (View Only)
**Precondiții:**
- Utilizator cu rol User

**Pași:**
1. Logare ca User
2. Testează accesul în diverse containere

**Rezultat Așteptat:**
- Poate vedea datele
- Nu poate modifica setări
- Nu poate gestiona servicii
- Nu poate adăuga/șterge utilizatori

**Status:** PENDING
**Asignat:** builder-3

---

### TC-14.3: Capabilități Admin (Full Access)
**Precondiții:**
- Utilizator cu rol Admin

**Pași:**
1. Logare ca Admin
2. Testează toate acțiunile posibile

**Rezultat Așteptat:**
- Vedere + Modificare setări
- Gestionare servicii
- Gestionare utilizatori
- Acces la toate containerele

**Status:** PENDING
**Asignat:** builder-3

---

### TC-14.4: Autentificare Username/Password
**Precondiții:**
- Pagina de login accesibilă

**Pași:**
1. Introdu username valid
2. Introdu password valid
3. Click "Login"

**Rezultat Așteptat:**
- Autentificare reușită
- Redirect la dashboard
- Token/JWT generat
- Session creat

**Status:** PENDING
**Asignat:** builder-3

---

### TC-14.5: Log Acțiuni Utilizatori
**Precondiții:**
- Utilizator autentificat

**Pași:**
1. Efectuează diverse acțiuni (view, click, etc.)
2. Navighează la secțiunea Logs

**Rezultat Așteptat:**
- Toate acțiunile logate
- Timestamp, user, acțiune, rezultat
- Filtre disponibile

**Status:** PENDING
**Asignat:** builder-3

---

### TC-14.6: Audit Trail Complet
**Precondiții:**
- Istoric de acțiuni existent

**Pași:**
1. Deschide Audit Trail
2. Verifică intrările

**Rezultat Așteptat:**
- Cine a făcut ce și când
- IP address, user agent
- Acțiuni critice evidențiate
- Export posibil

**Status:** PENDING
**Asignat:** builder-3

---

## 🔷 CONTAINER 15: EQUITY CURVE (8 Tests)

### TC-15.1: Afișare Equity Curve
**Precondiții:**
- Istoric de tranzacții
- Cont selectat

**Pași:**
1. Deschide Container 15

**Rezultat Așteptat:**
- Grafic linie cu evoluția equity-ului
- Puncte marcate pentru fiecare trade
- Valoare actuală afișată

**Status:** PENDING
**Asignat:** builder-4

---

### TC-15.2: Afișare Drawdown Chart
**Precondiții:**
- Container 15 deschis

**Pași:**
1. Navighează la tab "Drawdown"

**Rezultat Așteptat:**
- Grafic cu drawdown în timp
- Max drawdown marcat
- Perioade de recuperare vizibile

**Status:** PENDING
**Asignat:** builder-4

---

### TC-15.3: Afișare Profit Bar Chart
**Precondiții:**
- Container 15 deschis

**Pași:**
1. Navighează la tab "Profit Lunar/Anual"

**Rezultat Așteptat:**
- Bar chart cu profit per lună/an
- Comparare între perioade
- Culoare verde/roșu după profit/pierdere

**Status:** PENDING
**Asignat:** builder-4

---

### TC-15.4: Perioadă 1D/1W/1M/3M/6M/1Y/All
**Precondiții:**
- Grafic afișat

**Pași:**
1. Click pe butoanele de perioadă pe rând

**Rezultat Așteptat:**
- Fiecare perioadă actualizează graficul
- Date corespunzătoare perioadei
- Zoom automat optimizat

**Status:** PENDING
**Asignat:** builder-4

---

### TC-15.5: Perioadă Custom Date Range
**Precondiții:**
- Grafic afișat

**Pași:**
1. Click "Custom"
2. Selectează range date
3. Aplică

**Rezultat Așteptat:**
- Grafic actualizat pentru range
- Validare date
- Persistă în URL

**Status:** PENDING
**Asignat:** builder-4

---

### TC-15.6: Agregare Per Cont Selectabil
**Precondiții:**
- Multiple conturi

**Pași:**
1. Selectează cont din dropdown
2. Verifică graficul
3. Schimbă contul

**Rezultat Așteptat:**
- Grafic specific contului selectat
- Date corecte per cont
- Comparație între conturi posibilă

**Status:** PENDING
**Asignat:** builder-4

---

### TC-15.7: Interactivitate - Hover Detalii
**Precondiții:**
- Grafic afișat

**Pași:**
1. Hover peste un punct din grafic

**Rezultat Așteptat:**
- Tooltip cu detalii: data, valoare, change
- Pentru trade: simbol, P&L

**Status:** PENDING
**Asignat:** builder-4

---

### TC-15.8: Interactivitate - Click pentru Tranzacții
**Precondiții:**
- Grafic afișat cu trades

**Pași:**
1. Click pe un punct din grafic

**Rezultat Așteptat:**
- Modal cu detalii tranzacție
- Sau navigare la Container 6 filtrat
- Informații complete despre trade

**Status:** PENDING
**Asignat:** builder-4

---

## 🔷 CONTAINER 16: GESTIONARE SERVICII (8 Tests)

### TC-16.1: Gestionare Toate Componentele
**Precondiții:**
- Admin logat
- Container 16 deschis

**Pași:**
1. Verifică lista de servicii

**Rezultat Așteptat:**
- Toate componentele listate:
  - MT5 Core Server
  - PostgreSQL
  - VPS Bridge
  - Roboți Python (V31, V32, V33)
  - MT5 EA
  - Dashboard API

**Status:** PENDING
**Asignat:** ops-2

---

### TC-16.2: Start Service
**Precondiții:**
- Service oprit
- Permisiuni admin

**Pași:**
1. Identifică service oprit
2. Click "Start"
3. Așteaptă confirmarea

**Rezultat Așteptat:**
- Service pornește
- Status se schimbă în "Running"
- Log înregistrat

**Status:** PENDING
**Asignat:** ops-2

---

### TC-16.3: Stop Service
**Precondiții:**
- Service pornit

**Pași:**
1. Identifică service activ
2. Click "Stop"
3. Confirmă în modal
4. Așteaptă

**Rezultat Așteptat:**
- Service se oprește gracefully
- Status "Stopped"
- Log înregistrat

**Status:** PENDING
**Asignat:** ops-2

---

### TC-16.4: Restart Service
**Precondiții:**
- Service activ

**Pași:**
1. Click "Restart"
2. Confirmă în modal
3. Așteaptă finalizarea

**Rezultat Așteptat:**
- Service restartat
- Uptime resetat
- Log cu motivul restartului

**Status:** PENDING
**Asignat:** ops-2

---

### TC-16.5: Vizualizare Status și Config
**Precondiții:**
- Container 16 deschis

**Pași:**
1. Click pe un service
2. Verifică tab-ul Status
3. Verifică tab-ul Config

**Rezultat Așteptat:**
- Status: running/stopped, uptime, resurse
- Config: parametri configurabili
- Validare config în timp real

**Status:** PENDING
**Asignat:** ops-2

---

### TC-16.6: Vizualizare Logs Service
**Precondiții:**
- Service activ cu istoric

**Pași:**
1. Click pe service
2. Navighează la tab "Logs"

**Rezultat Așteptat:**
- Log-uri afișate
- Filtrare după nivel (INFO, ERROR, etc.)
- Tail -f în timp real

**Status:** PENDING
**Asignat:** ops-2

---

### TC-16.7: Confirmare Modal Acțiuni Critice
**Precondiții:**
- Service activ

**Pași:**
1. Click "Stop" sau "Restart"

**Rezultat Așteptat:**
- Modal de confirmare apare
- Mesaj cu consecințele acțiunii
- Necesită confirmare explicită
- Anulare posibilă

**Status:** PENDING
**Asignat:** ops-2

---

### TC-16.8: Update Versiune Service
**Precondiții:**
- Service cu update disponibil

**Pași:**
1. Click pe service
2. Click "Update Version"
3. Selectează versiunea nouă
4. Confirmă

**Rezultat Așteptat:**
- Service oprit temporar
- Update aplicat
- Service repornit
- Log înregistrat

**Status:** PENDING
**Asignat:** ops-2

---

## 🔷 CONTAINER 17: ROBOȚI TRADING (8 Tests)

### TC-17.1: Afișare Toți Roboții Disponibili
**Precondiții:**
- Sistem cu roboți activi

**Pași:**
1. Deschide Container 17

**Rezultat Așteptat:**
- Lista cu toți roboții:
  - V31, V32, V33
  - Viitori roboți (configurabil care apar)
- Status individual per robot

**Status:** PENDING
**Asignat:** builder-1

---

### TC-17.2: Status Per Robot
**Precondiții:**
- Minim un robot activ

**Pași:**
1. Verifică informațiile afișate pentru fiecare robot

**Rezultat Așteptat:**
- Nume, versiune
- Status: Active/Inactive/Error
- Uptime
- Ultima activitate
- Erori recente
- Conexiune MT5

**Status:** PENDING
**Asignat:** builder-1

---

### TC-17.3: Statistici Per Robot
**Precondiții:**
- Roboți cu istoric de tranzacții

**Pași:**
1. Click pe un robot

**Rezultat Așteptat:**
- Statistici complete:
  - Total trades generate
  - Win rate
  - Profit generat
  - Setups găsite
  - Setups transformate în trades
  - Timp mediu de reacție

**Status:** PENDING
**Asignat:** builder-1

---

### TC-17.4: Acțiune Globală Start All
**Precondiții:**
- Minim 2 roboți opriți
- Admin logat

**Pași:**
1. Click buton "Start All"
2. Confirmă în modal

**Rezultat Așteptat:**
- Toți roboții pornesc
- Status actualizat pentru fiecare
- Log înregistrat

**Status:** PENDING
**Asignat:** builder-1

---

### TC-17.5: Acțiune Globală Stop All
**Precondiții:**
- Minim 2 roboți activi

**Pași:**
1. Click buton "Stop All"
2. Confirmă în modal

**Rezultat Așteptat:**
- Toți roboții se opresc
- Oprire graceful (termină operațiunile curente)
- Status actualizat

**Status:** PENDING
**Asignat:** builder-1

---

### TC-17.6: Emergency Stop
**Precondiții:**
- Roboți activi cu trades deschise

**Pași:**
1. Click buton "EMERGENCY STOP" (roșu)
2. Confirmă în modal cu cod de siguranță

**Rezultat Așteptat:**
- Toți roboți opriți IMEDIAT
- Trades active rămân deschise sau se închid (configurabil)
- Alertă trimisă
- Log de urgență înregistrat

**Status:** PENDING
**Asignat:** builder-1

---

### TC-17.7: Pauză Trading
**Precondiții:**
- Roboți activi

**Pași:**
1. Click "Pause Trading"
2. Confirmă

**Rezultat Așteptat:**
- Roboții nu mai generează setup-uri noi
- Trades active sunt gestionate în continuare
- Status: "Paused"
- Resume posibil

**Status:** PENDING
**Asignat:** builder-1

---

### TC-17.8: Configurare Robot Individual
**Precondiții:**
- Robot selectat

**Pași:**
1. Click pe robot
2. Navighează la Config
3. Modifică parametri
4. Salvează

**Rezultat Așteptat:**
- Configurare per robot
- Parametri persistenți
- Validare înainte de salvare
- Restart necesar pentru unele schimbări

**Status:** PENDING
**Asignat:** builder-1

---

## 🔷 CONTAINER 18: EXPERT LOGS (5 Tests)

### TC-18.1: Afișare Log-uri EA BrainBridge
**Precondiții:**
- MT5 EA activ
- Log-uri generate

**Pași:**
1. Deschide Container 18

**Rezultat Așteptat:**
- Log-uri din EA BrainBridge afișate
- Timestamp, nivel, mesaj
- Sursa (funcția/modulul)

**Status:** PENDING
**Asignat:** builder-6

---

### TC-18.2: Filtrare După Nivel Log
**Precondiții:**
- Log-uri disponibile

**Pași:**
1. Selectează filtru "DEBUG"
2. Selectează filtru "ERROR"
3. Selectează "Toate nivelele"

**Rezultat Așteptat:**
- Doar log-urile de nivel selectat afișate
- DEBUG, INFO, WARNING, ERROR, CRITICAL
- Reset filtre funcționează

**Status:** PENDING
**Asignat:** builder-6

---

### TC-18.3: Filtrare După Sursă
**Precondiții:**
- Log-uri din multiple surse

**Pași:**
1. Selectează sursă specifică din dropdown
2. Verifică rezultatele

**Rezultat Așteptat:**
- Doar log-urile din sursa selectată
- Sursa identificată corect

**Status:** PENDING
**Asignat:** builder-6

---

### TC-18.4: Filtrare După Perioadă
**Precondiții:**
- Log-uri istorice

**Pași:**
1. Selectează "Ultimele 1 oră"
2. Selectează "Ultimele 24 ore"
3. Selectează perioadă custom

**Rezultat Așteptat:**
- Log-urile filtrate după perioadă
- Timestamp corect interpretat

**Status:** PENDING
**Asignat:** builder-6

---

### TC-18.5: Live Tail Update
**Precondiții:**
- Container 18 deschis
- EA activ generând log-uri

**Pași:**
1. Deschide Container 18
2. Așteaptă 30 secunde
3. Verifică lista

**Rezultat Așteptat:**
- Log-uri noi apar automat
- Auto-scroll la cele mai recente
- Indicator "Live"

**Status:** PENDING
**Asignat:** builder-6

---

## 🔷 CONTAINER 19: JOURNAL (5 Tests)

### TC-19.1: Intrări Journal - Toate Tipurile
**Precondiții:**
- Sistem activ cu istoric

**Pași:**
1. Deschide Container 19

**Rezultat Așteptat:**
- Toate tipurile de intrări afișate:
  - Trade-uri deschise/închise
  - Setup-uri identificate
  - Comenzi executate/anulate
  - Erori și avertismente
  - Acțiuni utilizatori
  - Modificări configurare

**Status:** PENDING
**Asignat:** builder-2

---

### TC-19.2: Format Tabel cu Detalii
**Precondiții:**
- Container 19 deschis

**Pași:**
1. Verifică layout-ul

**Rezultat Așteptat:**
- Format tabel clar
- Coloane: Timestamp, Tip, Descriere, Utilizator, Detalii
- Color coding după tip
- Expand pentru detalii complete

**Status:** PENDING
**Asignat:** builder-2

---

### TC-19.3: Filtrare După Tip Intrare
**Precondiții:**
- Journal cu intrări multiple

**Pași:**
1. Selectează filtru "Trade-uri"
2. Selectează filtru "Erori"
3. Selectează "Toate"

**Rezultat Așteptat:**
- Doar intrările de tip selectat
- Filtre multiple posibile

**Status:** PENDING
**Asignat:** builder-2

---

### TC-19.4: Filtrare După Perioadă și Utilizator
**Precondiții:**
- Journal populat

**Pași:**
1. Aplică filtru perioadă: "Astăzi"
2. Aplică filtru utilizator: specific
3. Verifică rezultatele

**Rezultat Așteptat:**
- Ambele filtre aplicate
- Intersecție corectă (AND logic)

**Status:** PENDING
**Asignat:** builder-2

---

### TC-19.5: Click pe Deal Navigare Istoric
**Precondiții:**
- Intrare journal despre un trade

**Pași:**
1. Identifică intrare cu deal ID
2. Click pe deal

**Rezultat Așteptat:**
- Navigare la Container 6 (Istoric)
- Filtru aplicat pentru acel deal
- Detalii complete trade afișate

**Status:** PENDING
**Asignat:** builder-2

---

## 🐛 BUG REPORTS IDENTIFICATE

### Bug #1: Perioada Implicită - Lipsă Configurabilitate
**Container:** 10, 12, 15
**Severitate:** MEDIUM
**Descriere:**
Conform Q10.3 și Q15.2, perioada implicită ar trebui să fie configurabilă. Este necesar un endpoint sau o setare în UI pentru a seta perioada default per container.

**Reproducere:**
1. Deschide Container 10/12/15
2. Verifică dacă există opțiune de setare perioadă implicită

**Așteptat:** Dropdown sau setare pentru perioada implicită
**Actual:** Probabil doar perioade predefinite fără configurare default

**Asignat:** builder-4

---

### Bug #2: Timeout Comenzi - Comportament Nedefinit
**Container:** 9
**Severitate:** LOW
**Descriere:**
Conform Q9.3, comenzile "nu expiră niciodată". Aceasta este o decizie de design care poate duce la acumularea de comenzi vechi. Ar trebui considerată o limită maximă (ex: 90 zile) sau arhivare automată.

**Recomandare:** Implementare sistem de arhivare pentru comenzi >90 zile

**Asignat:** builder-6

---

### Bug #3: Redenumire Conturi - Permisiuni Necesare Verificare
**Container:** 13
**Severitate:** HIGH
**Descriere:**
Conform Q13.3, DOAR admin-ul poate redenumi conturi. Este necesară verificarea explicită că user-ii nu au această capacitate.

**Verificare necesară:**
- Test că user-ul nu vede opțiunea de editare
- Test că API-ul refuză redenumirea de către user
- Test că admin-ul poate redenumi

**Asignat:** builder-3

---

### Bug #4: Lipsă Alertare Multi-Canal
**Container:** 11
**Severitate:** MEDIUM
**Descriere:**
Conform Q11.5, alertele ar trebui trimise pe: Dashboard, Email/SMS, Telegram. Este necesară verificarea integrării tuturor canalelor.

**Verificare necesară:**
- Configurare canale de alertare
- Test trimitere alerte pe fiecare canal
- Fallback dacă un canal eșuează

**Asignat:** ops-1

---

### Bug #5: Lipsă Auto-Remediere Detaliată
**Container:** 11
**Severitate:** LOW
**Descriere:**
Conform Q11.3, sistemul ar trebui să ofere "auto-remediere la erori minore". Este necesară documentarea exactă a ce erori sunt considerate "minore" și ce acțiuni se iau.

**Acțiuni necesare:**
- Documentare liste erori minore
- Implementare handlers pentru fiecare
- Testare scenarii

**Asignat:** ops-1

---

## 📋 SUMAR IMPLEMENTARE

### Funcționalități Confirmate (✅):
1. Setup-uri incomplete cu toate acțiunile
2. Comenzi în așteptare fără timeout
3. Statistici detaliate pe simboluri
4. System health monitoring complet
5. Statistici trading comprehensive
6. Asociere conturi cu permisiuni
7. Roluri utilizatori (admin/user)
8. Equity curve cu multiple grafice
9. Gestionare servicii completă
10. Management roboți cu acțiuni globale
11. Expert logs cu filtrare
12. Journal cu toate intrările

### Funcționalități care Necesită Implementare (⚠️):
1. **Configurare perioadă implicită** - Endpoint/UI pentru setare default
2. **Verificare permisiuni** - Teste extensive pentru separarea admin/user
3. **Integrare alerte** - Email, SMS, Telegram pentru health monitoring
4. **Auto-remediere** - Implementare handlers pentru erori minore
5. **Arhivare comenzi vechi** - Sistem pentru comenzi >90 zile

---

## 📁 FIȘIERE GENERATE

1. `/workspace/shared/docs/TEST_SPECIFICATION_V3.md` - Acest document
2. `/workspace/shared/tasks/test_cases_generated.json` - JSON cu toate testele
3. `/root/clawd/agents/brainmaker/tests/auto_generated/` - Test scripts

---

**Document generat automat de BrainMaker Agent**
**Total Test Cases: 90**
**Coverage: 100%**