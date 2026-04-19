# TEST SPECIFICATION V2
## Document de Specificații pentru Testare
### Container 8-19: Test Cases Complete

---

**Versiune:** 2.0  
**Data generării:** 2026-03-28  
**Total Test Cases:** 53+  
**Container acoperite:** 8-19

---

## CONTAINER 8: SETUP-URI INCOMPLETE

#### TC8.1: Afișare Setup-uri Incomplete Detectate
**Precondiții:**
- Sistemul de detectare setup-uri este activ
- Există cel puțin un setup valid identificat dar neexecutat
- Baza de date conține înregistrări setup în stare "detected"

**Pași:**
1. Accesează secțiunea "Setup-uri Incomplete" din dashboard
2. Verifică lista de setup-uri detectate
3. Confirmă că setup-urile au fost identificate corect de către roboți

**Rezultat Așteptat:**
- Lista afișează toate setup-urile găsite care nu au generat tranzacții
- Fiecare setup are indicator vizual de status (neexecutat)
- Numărul de setup-uri detectate corespunde cu înregistrările din DB

---

#### TC8.2: Configurare Durată Păstrare Setup-uri
**Precondiții:**
- Utilizator cu rol de administrator
- Acces la panoul de configurări

**Pași:**
1. Navighează la Settings > Setup-uri Incomplete
2. Modifică valoarea "Durată păstrare" la 72 ore
3. Salvează modificările
4. Verifică setup-uri mai vechi de 72 ore

**Rezultat Așteptat:**
- Configurația este salvată în settings.json
- Setup-urile mai vechi decât perioada configurată sunt eliminate automat
- User primește confirmare salvare

---

#### TC8.3: Acțiune Forțare Trade pentru Setup
**Precondiții:**
- Există setup valid în listă
- Cont de trading conectat și activ
- Utilizator are permisiuni de trading

**Pași:**
1. Selectează setup din listă
2. Click pe butonul "Forțare Trade"
3. Confirmă acțiunea în dialog
4. Așteaptă execuția ordinelor

**Rezultat Așteptat:**
- Ordinul este trimis către MT5
- Setup-ul este marcat ca "procesat"
- Jurnalul afișează confirmare execuție
- Poziția apare în lista de poziții deschise

---

#### TC8.4: Acțiune Ignorare Setup
**Precondiții:**
- Există setup în lista de incomplete

**Pași:**
1. Selectează setup din listă
2. Click pe butonul "Ignorare"
3. Adaugă motiv ignorare (opțional)
4. Confirmă ignorarea

**Rezultat Așteptat:**
- Setup-ul este mutat în secțiunea "Ignorate"
- Motivul este salvat în baza de date
- Setup-ul nu mai apare în lista principală

---

#### TC8.5: Modificare Parametri Setup
**Precondiții:**
- Setup selectat disponibil pentru editare
- Utilizator are permisiuni de modificare

**Pași:**
1. Click pe setup pentru editare
2. Modifică parametrii (SL, TP, volum)
3. Salvează modificările
4. Execută setup-ul modificat

**Rezultat Așteptat:**
- Noii parametri sunt salvați
- Setup-ul executat folosește parametrii modificați
- Versiunea originală este păstrată în istoric

---

#### TC8.6: Afișare Informații Complete Setup
**Precondiții:**
- Există setup-uri în listă cu toate datele populate

**Pași:**
1. Deschide detalii pentru un setup
2. Verifică toate câmpurile afișate

**Rezultat Așteptat:**
- Afișează: simbol, direcție (BUY/SELL), scor setup (0-100), motiv detecție
- Afișează: preț intrare propus, Stop Loss, Take Profit, ratio R:R
- Afișează: timestamp detectare, nume robot sursă
- Toate valorile sunt formatate corespunzător

---

## CONTAINER 9: COMENZI ÎN AȘTEPTARE

#### TC9.1: Afișare Toate Operațiunile în Așteptare
**Precondiții:**
- Sistemul procesează comenzi multiple
- Există comenzi în diverse stadii de procesare

**Pași:**
1. Accesează secțiunea "Comenzi în Așteptare"
2. Verifică lista completă de operațiuni

**Rezultat Așteptat:**
- Lista include: ordere de deschidere, închidere, modificare poziție
- Lista include: operațiuni de setare SL/TP, comenzi de volum
- Fiecare comandă are identificator unic vizibil
- Statusul curent este afișat pentru fiecare comandă

---

#### TC9.2: Comportament Comandă în Așteptare
**Precondiții:**
- O comandă a fost trimisă dar nu s-a executat încă
- Conexiunea cu MT5 este instabilă sau piața este închisă

**Pași:**
1. Trimite o comandă de deschidere poziție
2. Observă comportamentul în lista de așteptare
3. Așteaptă condiții de execuție sau timeout

**Rezultat Așteptat:**
- Comanda rămâne în coadă cu status "Pending"
- Nu este eliminată până la executare sau timeout
- Sistemul încearcă re-executare automată
- Timestamp-ul ultimei încercări este actualizat

---

#### TC9.3: Configurare Timeout Comenzi
**Precondiții:**
- Acces la setări sistem
- Utilizator administrator

**Pași:**
1. Navighează la Settings > Comenzi
2. Setează timeout implicit la 30 secunde
3. Creează comandă care nu poate fi executată imediat
4. Așteaptă depășirea timeout-ului

**Rezultat Așteptat:**
- Timeout-ul default este 30 secunde
- Valoarea este configurabilă per tip comandă
- După timeout, comanda este marcată ca "Failed"
- Notificare este trimisă utilizatorului

---

#### TC9.4: Vizualizare Detalii Completă Comandă
**Precondiții:**
- Comenzi existente în lista de așteptare

**Pași:**
1. Click pe o comandă pentru detalii
2. Verifică toate informațiile disponibile

**Rezultat Așteptat:**
- Afișează tipul comenzii (OPEN/CLOSE/MODIFY)
- Afișează parametrii compleți (simbol, volum, preț, SL, TP)
- Afișează timestamp creare, status curent, client ID
- Afișează nivel prioritate, număr retry, mesaj eroare (dacă există)

---

#### TC9.5: Anulare Comandă în Așteptare
**Precondiții:**
- Comandă în status "Pending" existentă

**Pași:**
1. Selectează comandă din listă
2. Click pe "Anulare"
3. Confirmă anularea în dialog

**Rezultat Așteptat:**
- Comanda este eliminată din coadă
- Statusul devine "Cancelled"
- Motivul anulării este logat
- Utilizatorul primește confirmare

---

#### TC9.6: Modificare Comandă în Așteptare
**Precondiții:**
- Comandă în status "Pending"
- Utilizator are permisiuni de modificare

**Pași:**
1. Selectează comandă pentru editare
2. Modifică parametrii (ex: volum, preț limită)
3. Salvează modificările

**Rezultat Așteptat:**
- Parametrii noi sunt salvați
- Comanda păstrează poziția în coadă
- Versiunea anterioară este logată
- Retry counter este resetat

---

#### TC9.7: Forțare Execuție Comandă
**Precondiții:**
- Comandă blocată în coadă
- Conexiunea MT5 este restabilită

**Pași:**
1. Identifică comandă cu retry eșuat
2. Click pe "Forțare Execuție"
3. Confirmă acțiunea

**Rezultat Așteptat:**
- Comanda este procesată imediat
- Sistemul ignoră cooldown-ul de retry
- Rezultatul execuției este afișat
- Jurnalul înregistrează acțiunea de forțare

---

## CONTAINER 10: PERFORMANȚĂ PE SIMBOLURI

#### TC10.1: Afișare Toate Metricile de Performanță
**Precondiții:**
- Istoric de tranzacționare disponibil
- Date pentru multiple simboluri

**Pași:**
1. Accesează secțiunea "Performanță pe Simboluri"
2. Selectează un simbol din listă
3. Vizualizează toate metricile

**Rezultat Așteptat:**
- Afișează Win Rate (procent tranzacții câștigătoare)
- Afișează Profit total (P&L cumulat)
- Afișează R:R mediu (Risk:Reward)
- Afișează Durată medie tranzacție
- Afișează Perioada analizată (start - end date)

---

#### TC10.2: Configurare Perioadă Analiză
**Precondiții:**
- Utilizator autentificat
- Date istorice disponibile

**Pași:**
1. Deschide selectorul de perioadă
2. Selectează perioadă custom (ex: ultimele 30 zile)
3. Aplică filtrul

**Rezultat Așteptat:**
- Perioada este configurabilă de utilizator
- Metricile se actualizează automat
- Selecția este salvată în preferințe
- Reîncărcarea paginii păstrează perioada selectată

---

#### TC10.3: Configurare Perioadă Implicită
**Precondiții:**
- Acces la setări utilizator

**Pași:**
1. Navighează la Settings > Performanță
2. Setează perioada implicită la "Ultima lună"
3. Salvează setările
4. Reîncarcă pagina de performanță

**Rezultat Așteptat:**
- Perioada implicită este configurabilă
- La accesare, se încarcă automat perioada setată
- Setarea persistă între sesiuni

---

#### TC10.4: Deschidere Modal Detalii Simbol
**Precondiții:**
- Listă de simboluri cu date disponibile

**Pași:**
1. Click pe simbolul dorit din listă
2. Așteaptă încărcarea modalului

**Rezultat Așteptat:**
- Se deschide modal cu detalii complete pentru simbol
- Afișează informații extinse (număr tranzacții, cel mai bun/worst trade)
- Include chart cu evoluția profitului în timp
- Chart-ul este interactiv și responsive

---

#### TC10.5: Funcționalități Sortare și Filtrare
**Precondiții:**
- Multiple simboluri în listă

**Pași:**
1. Testează sortare după coloane (click pe header)
2. Aplică filtru perioadă (ex: ultima săptămână)
3. Aplică filtru direcție (BUY/SELL/Both)

**Rezultat Așteptat:**
- Sortare funcționează pentru toate coloanele (asc/desc)
- Filtru perioadă limitează datele afișate
- Filtru direcție arată doar tranzacțiile matching
- Combinația de filtre funcționează corect

---

## CONTAINER 11: SYSTEM HEALTH

#### TC11.1: Afișare Stare Toate Componentele
**Precondiții:**
- Toate componentele sistemului rulează
- Dashboard System Health este accesibil

**Pași:**
1. Accesează pagina "System Health"
2. Verifică lista completă de componente

**Rezultat Așteptat:**
- Afișează status MT5 Core (conectat/deconectat)
- Afișează status Database (healthy/error)
- Afișează status VPS (online/offline, resurse)
- Afișează status Roboți (activi/opriți)
- Afișează status EA BrainBridge (running/stopped)
- Afișează utilizare Resurse (CPU, RAM, Disk)

---

#### TC11.2: Indicatori Vizuali Status Componente
**Precondiții:**
- Componente în diverse stări de funcționare

**Pași:**
1. Observă indicatorii colorați pentru fiecare componentă
2. Simulează problemă (unde este posibil)

**Rezultat Așteptat:**
- 🟢 Healthy: Toate metricile în limite normale
- 🟡 Warning: Unele metrici aproape de limită (ex: CPU >70%)
- 🔴 Critical: Problemă activă ce necesită atenție (ex: serviciu oprit)
- Culorile sunt consistente în tot dashboard-ul

---

#### TC11.3: Restart Componentă din Dashboard
**Precondiții:**
- Utilizator cu permisiuni admin
- Cel puțin o componentă oprită sau în eroare

**Pași:**
1. Identifică componenta cu problemă
2. Click pe butonul "Restart"
3. Confirmă acțiunea
4. Așteaptă finalizarea restartului

**Rezultat Așteptat:**
- Componenta este oprită și repornită
- Statusul se actualizează în timp real
- Log-ul afișează pașii restartului
- La final, statusul este "Healthy" (dacă totul e OK)

---

#### TC11.4: Activare Auto-Remediere
**Precondiții:**
- Acces la setări sistem avansate

**Pași:**
1. Navighează la Settings > System Health
2. Activează "Auto-Remediation"
3. Configurează reguli (ex: restart la 3 erori consecutive)
4. Simulează o eroare recoverable

**Rezultat Așteptat:**
- Sistemul detectează eroarea automat
- Aplică acțiunea de remediere configurată
- Loghează acțiunile întreprinse
- Notifică administratorul despre remediere

---

#### TC11.5: Grafic Uptime Componente
**Precondiții:**
- Istoric de disponibilitate disponibil
- Componente monitorizate de cel puțin 24h

**Pași:**
1. Selectează o componentă din listă
2. Vizualizează graficul de uptime
3. Schimbă perioada afișată

**Rezultat Așteptat:**
- Grafic afișează procent uptime în timp
- Perioade de downtime sunt marcate vizual
- Graficul permite zoom și pan
- Datele sunt actualizate în timp real

---

#### TC11.6: Configurare Notificări Alertă
**Precondiții:**
- Utilizator administrator

**Pași:**
1. Navighează la Settings > Notificări
2. Configurează canale: Dashboard, Email/SMS, Telegram
3. Setează praguri pentru alerte (Warning/Critical)
4. Salvează configurarea

**Rezultat Așteptat:**
- Alertele apar în dashboard în timp real
- Email/SMS sunt trimise la pragurile configurate
- Mesaje Telegram sunt transmise către grupul configurat
- Configurarea persistă și este aplicată imediat

---

## CONTAINER 12: STATISTICI TRADING

#### TC12.1: Afișare Toate Metricile de Trading
**Precondiții:**
- Istoric tranzacționare cu suficiente date
- Acces la secțiunea Statistici

**Pași:**
1. Accesează "Statistici Trading"
2. Verifică toate cardurile/metricile afișate

**Rezultat Așteptat:**
- Afișează P&L (Profit & Loss) total și per perioadă
- Afișează Win Rate (procentaj tranzacții profitabile)
- Afișează Drawdown maxim (cel mai mare declin)
- Afișează Profit Factor (profit brut / pierdere brută)
- Afișează Expectancy (profit mediu așteptat per trade)

---

#### TC12.2: Statistici per Cont Individual
**Precondiții:**
- Multiple conturi de trading asociate
- Date pentru fiecare cont

**Pași:**
1. Selectează contul dorit din dropdown
2. Observă metricile actualizate
3. Comută între diferite conturi

**Rezultat Așteptat:**
- Fiecare cont are statistici separate
- Metricile se recalculează la schimbarea contului
- Selecția curentă este evident vizuală
- Datele sunt corect izolate per cont

---

#### TC12.3: Selecție Perioadă Predefinită
**Precondiții:**
- Date disponibile pentru multiple perioade

**Pași:**
1. Click pe butoanele perioadă predefinite (Today, Week, Month, Year, All)
2. Verifică actualizarea statisticilor

**Rezultat Așteptat:**
- Toate perioadele predefinite funcționează
- Datele se filtrează corespunzător
- Butonul selectat este evident vizual
- Perioada activă este afișată în titlu

---

#### TC12.4: Selecție Perioadă Custom
**Precondiții:**
- Date disponibile în intervalul dorit

**Pași:**
1. Click pe "Custom Range"
2. Selectează data de început și sfârșit
3. Aplică selecția

**Rezultat Așteptat:**
- Date picker permite selecție orice perioadă
- Statisticile se actualizează pentru intervalul selectat
- Formatul datei este consistent (DD/MM/YYYY)
- Perioada invalidă (start > end) este respinsă

---

#### TC12.5: Export Statistici CSV
**Precondiții:**
- Date statistice disponibile

**Pași:**
1. Selectează perioada dorită
2. Click pe butonul "Export CSV"
3. Salvează fișierul
4. Deschide și verifică conținutul

**Rezultat Așteptat:**
- Fișier CSV este generat și descărcat
- Conține toate metricile vizibile în interfață
- Formatul este compatibil Excel/Google Sheets
- Numele fișierului include timestamp

---

## CONTAINER 13: ASOCIERE CONTURI

#### TC13.1: Link Conturi Trading
**Precondiții:**
- Utilizator autentificat
- Cel puțin două conturi disponibile pentru link

**Pași:**
1. Accesează "Asociere Conturi"
2. Selectează contul principal
3. Selectează contul secundar pentru link
4. Confirmă asocierea

**Rezultat Așteptat:**
- Conturile sunt asociate în sistem
- Operațiunile se reflectă în ambele conturi (configurabil)
- Lista de conturi asociate este actualizată
- Unlink este disponibil ulterior

---

#### TC13.2: Grupare Conturi
**Precondiții:**
- Multiple conturi disponibile

**Pași:**
1. Creează grup nou (ex: "Conturi Prop Firm")
2. Adaugă conturi în grup
3. Salvează gruparea

**Rezultat Așteptat:**
- Grupul este creat și vizibil
- Conturile sunt organizate sub grup
- Se pot aplica acțiuni la nivel de grup
- Grupurile pot fi expandate/collapse

---

#### TC13.3: Setare Permisiuni Conturi
**Precondiții:**
- Utilizator cu rol admin
- Conturi asociate utilizatorilor

**Pași:**
1. Selectează un cont
2. Modifică permisiunile (View Only, Trade, Admin)
3. Aplică pentru utilizator specific

**Rezultat Așteptat:**
- Admin: acces complet la toate conturile
- User: acces doar la conturile proprii
- Permisiunile sunt aplicate imediat
- Utilizatorul vede doar ce are voie

---

#### TC13.4: Vizibilitate per Rol
**Precondiții:**
- Conturi multiple în sistem
- Utilizatori cu roluri diferite

**Pași:**
1. Loghează-te ca admin, verifică lista conturi
2. Loghează-te ca user standard, verifică lista
3. Compară vizibilitatea

**Rezultat Așteptat:**
- Admin vede toate conturile din sistem
- User vede doar conturile asociate lui
- Conturile neasociate nu sunt vizibile user-ului
- URL direct către cont neautorizat returnează 403

---

#### TC13.5: Redenumire Friendly Cont
**Precondiții:**
- Cont existent în sistem
- Utilizator cu permisiuni

**Pași:**
1. Click pe numele contului pentru editare
2. Introdu nume friendly (ex: "Cont Principal FTMO")
3. Salvează modificarea

**Rezultat Așteptat:**
- Numele friendly este salvat
- Afișat în toate interfețele
- Numărul contului original este păstrat în paranteză
- Căutarea funcționează după ambele nume

---

#### TC13.6: Funcționalități Doar pentru Admin
**Precondiții:**
- Utilizator admin logat
- Conturi multiple în sistem

**Pași:**
1. Verifică opțiunile disponibile pentru admin
2. Loghează-te ca user normal
3. Compară opțiunile disponibile

**Rezultat Așteptat:**
- Doar admin poate: șterge conturi, modifica asocieri, seta permisiuni globale
- User-ul normal nu vede aceste opțiuni
- Butoanele admin sunt ascunse pentru useri normali
- Operațiunile restrictive sunt protejate pe backend

---

#### TC13.7: Adăugare Tag-uri Custom
**Precondiții:**
- Cont existent în sistem

**Pași:**
1. Selectează un cont
2. Adaugă tag-uri (ex: "Prop Firm", "EURUSD", "Conservator")
3. Salvează tag-urile

**Rezultat Așteptat:**
- Tag-urile sunt salvate și afișate
- Pot fi folosite pentru filtrare
- Tag-urile sunt colorate diferit
- Căutarea funcționează și după tag-uri

---

## CONTAINER 14: UTILIZATORI

#### TC14.1: Roluri Disponibile
**Precondiții:**
- Acces la management utilizatori

**Pași:**
1. Accesează secțiunea "Utilizatori"
2. Vizualizează lista de roluri

**Rezultat Așteptat:**
- Sunt disponibile exact 2 roluri: Admin și User
- Rolurile sunt clare și bine definite
- Nu există roluri intermediare sau custom
- Descrierea fiecărui rol este vizibilă

---

#### TC14.2: Vizualizare Date Utilizatori
**Precondiții:**
- Utilizator autentificat (ambele roluri)
- Date utilizatori în sistem

**Pași:**
1. Ca User: accesează profil propriu
2. Ca Admin: accesează lista tuturor utilizatorilor

**Rezultat Așteptat:**
- User: vede doar propriile date, poate modifica profilul personal
- Admin: vede toate datele utilizatorilor, poate modifica orice profil
- Datele sensibile (parola) sunt mascate
- Istoricul activității este accesibil

---

#### TC14.3: Creare Utilizator Nou
**Precondiții:**
- Utilizator cu rol admin

**Pași:**
1. Click pe "Adaugă Utilizator"
2. Completează: Username, Password, Email, Rol
3. Salvează utilizatorul

**Rezultat Așteptat:**
- Utilizatorul este creat în sistem
- Parola este salvată hash-uită
- Email de confirmare este trimis (opțional)
- Utilizatorul poate să se logheze imediat

---

#### TC14.4: Modificare Date Utilizator
**Precondiții:**
- Utilizator existent
- Permisiuni de modificare

**Pași:**
1. Selectează utilizatorul
2. Modifică câmpurile dorite
3. Salvează modificările

**Rezultat Așteptat:**
- Datele sunt actualizate în baza de date
- Modificările sunt reflectate imediat
- Parola poate fi resetată
- Schimbarea de roluri actualizează permisiunile

---

#### TC14.5: Autentificare Username/Password
**Precondiții:**
- Utilizator existent în sistem

**Pași:**
1. Accesează pagina de login
2. Introdu username și password
3. Click "Login"

**Rezultat Așteptat:**
- Autentificare cu username și password
- Token JWT este generat
- Sesizunea este persistată
- Redirect către dashboard principal

---

#### TC14.6: Log Acțiuni Utilizator
**Precondiții:**
- Activitate anterioară în sistem

**Pași:**
1. Accesează secțiunea "Audit Log"
2. Vizualizează lista acțiunilor
3. Filtrează după utilizator/perioadă

**Rezultat Așteptat:**
- Log conține TOATE acțiunile utilizatorilor
- Fiecare intrare: timestamp, user, acțiune, detalii, IP
- Filtrele funcționează corect
- Log-ul nu poate fi șters de utilizatori

---

#### TC14.7: Audit Trail Complet
**Precondiții:**
- Operațiuni efectuate în sistem

**Pași:**
1. Efectuează o serie de operațiuni (login, trade, modificare setări)
2. Verifică audit trail-ul
3. Exportă log-ul

**Rezultat Așteptat:**
- Audit trail înregistrează complet fiecare acțiune
- Include modificări de date, tranzacții, setări
- Datele sunt imutabile
- Exportul include toate câmpurile relevante

---

## CONTAINER 15: EQUITY CURVE

#### TC15.1: Afișare Grafic Equity
**Precondiții:**
- Istoric de tranzacționare disponibil
- Date equity calculate

**Pași:**
1. Accesează secțiunea "Equity Curve"
2. Selectează tipul de grafic "Equity"

**Rezultat Așteptat:**
- Graficul afișează evoluția equity în timp
- Linia equity crește/scade corespunzător
- Punctele de start și curent sunt marcate
- Graficul este responsive și clar

---

#### TC15.2: Afișare Grafic Drawdown
**Precondiții:**
- Tranzacții cu perioade de pierderi

**Pași:**
1. Selectează tipul de grafic "Drawdown"
2. Observă evoluția

**Rezultat Așteptat:**
- Graficul afișează drawdown procentual în timp
- Vârfurile de drawdown sunt evidente
- Perioadele de recuperare sunt vizibile
- Valoarea maximă de drawdown este afișată

---

#### TC15.3: Afișare Grafic Profit Cumulat
**Precondiții:**
- Tranzacții istorice disponibile

**Pași:**
1. Selectează tipul de grafic "Profit"
2. Verifică datele afișate

**Rezultat Așteptat:**
- Graficul afișează profitul cumulat în timp
- Bare pozitive/negative pentru fiecare perioadă
- Totalul este afișat în legendă
- Comparație cu perioade anterioare disponibilă

---

#### TC15.4: Perioade Disponibile pentru Grafice
**Precondiții:**
- Date pe multiple perioade

**Pași:**
1. Testează toate perioadele: 1D, 1W, 1M, 3M, 6M, 1Y, All
2. Verifică actualizarea graficului

**Rezultat Așteptat:**
- Toate perioadele sunt disponibile și funcționează
- Graficul se actualizează corespunzător
- Datele sunt agregate corect per perioadă
- Zoom-ul automată se potrivește perioadei

---

#### TC15.5: Vizualizare Toate Conturile
**Precondiții:**
- Multiple conturi cu date

**Pași:**
1. Selectează opțiunea "Toate Conturile"
2. Observă graficul

**Rezultat Așteptat:**
- Graficul combină datele din toate conturile
- Linii diferite pentru fiecare cont (opțional)
- Totalul agregat este calculat corect
- Legenda indică fiecare cont

---

#### TC15.6: Vizualizare per Cont Individual
**Precondiții:**
- Multiple conturi disponibile

**Pași:**
1. Selectează un cont specific din dropdown
2. Observă graficul filtrat

**Rezultat Așteptat:**
- Graficul afișează doar datele contului selectat
- Conturile neafectate nu apar în grafic
- Comutarea între conturi este rapidă
- Datele sunt corect izolate

---

#### TC15.7: Interacțiune Hover pe Grafic
**Precondiții:**
- Grafic cu date încărcat

**Pași:**
1. Poziționează cursorul pe grafic
2. Mișcă cursorul de-a lungul liniei

**Rezultat Așteptat:**
- Tooltip afișează valoarea exactă la poziția cursorului
- Data și equity/profit/drawdown sunt vizibile
- Linie verticală indică poziția exactă
- Tooltip-ul urmărește cursorul fluent

---

#### TC15.8: Funcționalitate Zoom pe Grafic
**Precondiții:**
- Grafic cu suficiente date pentru zoom

**Pași:**
1. Folosește scroll mouse pentru zoom
2. Folosește butoanele de zoom din interfață
3. Selectează o zonă pentru zoom

**Rezultat Așteptat:**
- Zoom-in afișează detalii pentru perioada selectată
- Zoom-out revine la perspectiva mai largă
- Reset zoom revine la view-ul inițial
- Graficul rămâne clar la toate nivelele de zoom

---

#### TC15.9: Click pe Grafic pentru Tranzacții
**Precondiții:**
- Grafic equity cu puncte de tranzacționare

**Pași:**
1. Click pe un punct de interes de pe grafic
2. Observă rezultatul

**Rezultat Așteptat:**
- Se deschide lista tranzacțiilor pentru perioada/punctul selectat
- Modal cu detalii complete despre tranzacții
- Posibilitatea de a naviga la istoric complet
- Tranzacțiile sunt sortate cronologic

---

#### TC15.10: Confirmare Nu Este Necesar Export
**Precondiții:**
- Grafic afișat în interfață

**Pași:**
1. Caută opțiune de export în interfață
2. Verifică documentația

**Rezultat Așteptat:**
- Nu există buton sau opțiune de export pentru equity curve
- Documentația confirmă că exportul nu este suportat pentru acest container
- Utilizatorul poate face screenshot dacă e necesar
- Datele brute sunt disponibile în alte secțiuni pentru export

---

## CONTAINER 16: GESTIONARE SERVICII

#### TC16.1: Listare Toate Componentele
**Precondiții:**
- Sistemul are toate componentele instalate
- Acces la panoul de administrare

**Pași:**
1. Accesează "Gestionare Servicii"
2. Verifică lista de componente

**Rezultat Așteptat:**
- Lista include toate componentele: MT5 Connector, Database, API Server, Web Dashboard, Roboți, EA BrainBridge, Notification Service
- Fiecare componentă are indicator de status
- Versiunea fiecărei componente este afișată
- Descriere scurtă pentru fiecare

---

#### TC16.2: Acțiune Start Serviciu
**Precondiții:**
- Serviciu oprit
- Permisiuni de administrare

**Pași:**
1. Identifică serviciul oprit
2. Click pe butonul "Start"
3. Așteaptă pornirea

**Rezultat Așteptat:**
- Serviciul este pornit
- Statusul se schimbă în "Running"
- PID-ul este afișat (dacă e aplicabil)
- Log-ul de startup este disponibil

---

#### TC16.3: Acțiune Stop Serviciu
**Precondiții:**
- Serviciu în funcțiune
- Permisiuni de administrare

**Pași:**
1. Selectează serviciul activ
2. Click pe "Stop"
3. Confirmă oprirea

**Rezultat Așteptat:**
- Serviciul este oprit gracefully
- Statusul devine "Stopped"
- Conexiunile active sunt închise curat
- Log-ul de shutdown este disponibil

---

#### TC16.4: Acțiune Restart Serviciu
**Precondiții:**
- Serviciu în funcțiune sau oprit

**Pași:**
1. Click pe butonul "Restart"
2. Așteaptă finalizarea

**Rezultat Așteptat:**
- Serviciul este oprit și repornit
- Statusul trece prin: Stopping → Stopped → Starting → Running
- Downtime-ul este minimizat
- Log-ul arată restartul complet

---

#### TC16.5: Vizualizare Status Serviciu
**Precondiții:**
- Servicii în diverse stări

**Pași:**
1. Observă pagina de gestionare servicii
2. Verifică informațiile pentru fiecare serviciu

**Rezultat Așteptat:**
- Afișează status curent (Running/Stopped/Error)
- Afișează uptime pentru serviciile active
- Afișează ultima eroare (dacă există)
- Auto-refresh la fiecare 5 secunde

---

#### TC16.6: Vizualizare Log-uri Serviciu
**Precondiții:**
- Serviciu cu istoric de funcționare

**Pași:**
1. Click pe butonul "Logs" pentru un serviciu
2. Navighează prin log-uri

**Rezultat Așteptat:**
- Log-urile serviciului sunt afișate
- Nivelul de log este colorat (INFO, WARN, ERROR)
- Filtre disponibile după nivel și dată
- Log-urile pot fi descărcate

---

#### TC16.7: Modificare Configurare Serviciu
**Precondiții:**
- Acces la fișierele de configurație

**Pași:**
1. Click pe "Config" pentru un serviciu
2. Modifică parametrii în editor
3. Salvează modificările

**Rezultat Așteptat:**
- Configurația este validată înainte de salvare
- Backup al configurației anterioare este creat
- Serviciul poate fi repornit pentru aplicare
- Istoricul modificărilor este disponibil

---

#### TC16.8: Update Serviciu
**Precondiții:**
- Versiune nouă disponibilă
- Backup efectuat

**Pași:**
1. Click pe "Update Available" (dacă există)
2. Confirmă update-ul
3. Așteaptă finalizarea

**Rezultat Așteptat:**
- Noua versiune este descărcată
- Serviciul este actualizat
- Configurația este păstrată
- Release notes sunt afișate

---

#### TC16.9: Acces Restricționat Doar Admin
**Precondiții:**
- Utilizator cu rol user (non-admin)

**Pași:**
1. Încearcă să accesezi URL-ul /admin/services
2. Verifică vizibilitatea opțiunilor

**Rezultat Așteptat:**
- Accesul este respins cu 403 Forbidden
- Utilizatorul este redirectat către dashboard
- Mesaj de eroare explică lipsa permisiunilor
- Log-ul înregistrează tentativa de acces neautorizat

---

#### TC16.10: Confirmare Parolă pentru Acțiuni Critice
**Precondiții:**
- Utilizator admin logat
- Sesiune activă de ceva timp

**Pași:**
1. Încearcă să oprești sau restartezi un serviciu critic
2. Observă solicitarea de confirmare

**Rezultat Așteptat:**
- Se deschide modal de confirmare
- Se solicită reintroducerea parolei
- Doar opțiunile Stop și Restart necesită confirmare
- Start nu necesită confirmare suplimentară
- Acțiunea este logată suplimentar

---

#### TC16.11: Vizualizare Log-uri Live (Tail -f)
**Precondiții:**
- Serviciu activ care generează log-uri

**Pași:**
1. Click pe "Live Logs" pentru un serviciu
2. Observă fluxul de log-uri
3. Continuă să folosești aplicația

**Rezultat Așteptat:**
- Log-urile apar în timp real pe ecran
- Funcționează similar cu comanda `tail -f`
- Auto-scroll la intrări noi
- Posibilitate de pause/resume
- Căutare în log-urile live

---

## CONTAINER 17: ROBOȚI GENERAL

#### TC17.1: Configurare Vizibilitate Roboți
**Precondiții:**
- Multiple roboți în sistem
- Acces la setări

**Pași:**
1. Navighează la Settings > Roboți
2. Selectează care roboți să apară în dashboard
3. Salvează configurarea

**Rezultat Așteptat:**
- Lista de roboți vizibili este configurabilă
- Roboții neselectați sunt ascunși din interfață
- Configurația persistă între sesiuni
- Toți roboții rămân activi în fundal

---

#### TC17.2: Afișare Toate Statusurile
**Precondiții:**
- Roboți în diverse stări

**Pași:**
1. Accesează secțiunea "Roboți"
2. Verifică statusul fiecărui robot

**Rezultat Așteptat:**
- Afișează toate statusurile: Active, Paused, Stopped, Error, Initializing
- Statusul este colorat corespunzător
- Iconiță distinctă pentru fiecare status
- Timestamp ultima schimbare status

---

#### TC17.3: Afișare Uptime și Last Seen
**Precondiții:**
- Roboți cu istoric de funcționare

**Pași:**
1. Vizualizează detaliile unui robot
2. Verifică informațiile de uptime

**Rezultat Așteptat:**
- Uptime este calculat de la ultimul start
- Last seen arată când a fost ultimul semnal de viață
- Format human-readable (ex: "2 zile, 4 ore")
- Reset la restart

---

#### TC17.4: Afișare Toate Detaliile Robot
**Precondiții:**
- Robot activ în sistem

**Pași:**
1. Click pe un robot pentru detalii
2. Examinează toate câmpurile

**Rezultat Așteptat:**
- Afișează: nume, versiune, simboluri monitorizate, timeframe-uri
- Afișează: strategie folosită, parametri, interval scanare
- Afișează: resurse consumate (CPU, memorie)
- Afișează: conturi asociate, permisiuni

---

#### TC17.5: Vizualizare Statistici Roboți
**Precondiții:**
- Robot cu istoric de tranzacționare

**Pași:**
1. Selectează un robot
2. Navighează la tab-ul "Statistici"

**Rezultat Așteptat:**
- Afișează: număr tranzacții generate, win rate, profit total
- Afișează: cel mai bun/worst trade, trades per day/week
- Afișează: timp mediu execuție, uptime percentage
- Grafic cu evoluția performanței în timp

---

#### TC17.6: Acțiune Start All Roboți
**Precondiții:**
- Multiple roboți opriți
- Permisiuni de control

**Pași:**
1. Click pe butonul "Start All"
2. Confirmă acțiunea

**Rezultat Așteptat:**
- Toți roboții sunt porniți secvențial
- Progress indicator arată starea
- Fiecare robot raportează status după pornire
- Erorile sunt colectate și afișate la final

---

#### TC17.7: Acțiune Stop All Roboți
**Precondiții:**
- Multiple roboți activi

**Pași:**
1. Click pe butonul "Stop All"
2. Confirmă acțiunea

**Rezultat Așteptat:**
- Toți roboții primesc semnal de oprire
- Roboții opresc gracefully (închid poziții dacă e configurat)
- Statusul se actualizează pentru fiecare
- Confirmare când toți sunt opriți

---

#### TC17.8: Acțiune Emergency Stop
**Precondiții:**
- Roboți activi
- Situație care necesită oprire imediată

**Pași:**
1. Click pe butonul "Emergency Stop"
2. Confirmă în dialogul de avertizare

**Rezultat Așteptat:**
- Toți roboții sunt opriți imediat (force stop)
- Pozițiile deschise rămân deschise (sau se închid - configurabil)
- Notificare de urgență este trimisă
- Log-ul marchează acțiunea ca "EMERGENCY"

---

#### TC17.9: Acțiune Pauză Robot
**Precondiții:**
- Robot în funcțiune

**Pași:**
1. Selectează robot activ
2. Click pe "Pause"

**Rezultat Așteptat:**
- Robotul încetează să mai genereze semnale noi
- Pozițiile existente rămân active
- Statusul devine "Paused"
- Resume reia funcționarea normală

---

## CONTAINER 18: EXPERT LOGS

#### TC18.1: Filtrează Doar EA BrainBridge
**Precondiții:**
- Multiple surse de log-uri

**Pași:**
1. Accesează "Expert Logs"
2. Verifică filtrul implicit

**Rezultat Așteptat:**
- Doar log-urile de la EA BrainBridge sunt afișate implicit
- Alte surse sunt filtrate by default
- Filtrele pot fi modificate pentru a include alte surse
- Sursa este afișată clar pentru fiecare intrare

---

#### TC18.2: Configurare Nivel Log
**Precondiții:**
- Acces la setări logging

**Pași:**
1. Navighează la Settings > Expert Logs
2. Modifică nivelul log (DEBUG, INFO, WARN, ERROR)
3. Salvează și observă schimbările

**Rezultat Așteptat:**
- Nivelul este configurabil per componentă
- Doar log-urile de nivel egal sau superior sunt afișate
- Configurația se aplică imediat
- Persistă între sesiuni

---

#### TC18.3: Filtrează după Nivel
**Precondiții:**
- Log-uri cu diverse nivele

**Pași:**
1. Selectează nivelul dorit din filtru
2. Aplică filtrul

**Rezultat Așteptat:**
- Afișează doar log-urile de nivelul selectat
- Opțiune multi-select disponibilă
- Counter arată numărul de intrări filtrate

---

#### TC18.4: Filtrează după Sursă
**Precondiții:**
- Log-uri de la multiple surse

**Pași:**
1. Deschide filtrul de surse
2. Selectează sursele dorite

**Rezultat Așteptat:**
- Lista de surse disponibile este afișată
- Selecție multiplă este suportată
- "Select All" și "Deselect All" disponibile
- Filtrul se aplică instant

---

#### TC18.5: Filtrează după Perioadă
**Precondiții:**
- Log-uri pe o perioadă extinsă

**Pași:**
1. Selectează perioada dorită (Today, Yesterday, Last 7 Days, Custom)
2. Aplică filtrul

**Rezultat Așteptat:**
- Doar log-urile din perioada selectată sunt afișate
- Date picker pentru custom range
- Timezone este respectat

---

#### TC18.6: Căutare Text în Log-uri
**Precondiții:**
- Log-uri cu conținut variat

**Pași:**
1. Introdu text în câmpul de căutare
2. Apasă Enter sau așteaptă debounce

**Rezultat Așteptat:**
- Log-urile conținând textul sunt afișate
- Căutare în mesaj, sursă, nivel
- Highlight al termenului căutat
- Căutare case-insensitive

---

#### TC18.7: Filtrează Ultimele X Intrări
**Precondiții:**
- Volum mare de log-uri

**Pași:**
1. Selectează opțiunea "Ultimele X"
2. Introdu numărul (ex: 100)

**Rezultat Așteptat:**
- Afișează doar ultimele N intrări
- Ordonate cronologic descrescător
- Performance optimizat pentru volume mari

---

#### TC18.8: Update Log-uri în Timp Real
**Precondiții:**
- Sistem activ care generează log-uri

**Pași:**
1. Lasă pagina deschisă
2. Generează activitate în sistem
3. Observă lista de log-uri

**Rezultat Așteptat:**
- Log-urile noi apar automat în listă
- Animație subtilă pentru intrări noi
- Auto-scroll opțional
- Badge cu număr intrări noi dacă nu ești în viewport

---

## CONTAINER 19: JOURNAL

#### TC19.1: Afișare Toate Tipurile de Intrări
**Precondiții:**
- Istoric de activitate în sistem

**Pași:**
1. Accesează secțiunea "Journal"
2. Verifică tipurile de intrări afișate

**Rezultat Așteptat:**
- Afișează Dealuri (tranzacții executate)
- Afișează Ordere (comenzi plasate, modificate, anulate)
- Afișează Erori (erori de sistem, de execuție)
- Afișează Modificări Balans (depuneri, retrageri, swap)
- Fiecare tip are iconiță distinctă

---

#### TC19.2: Vizualizare Format Tabel
**Precondiții:**
- Intrări în journal

**Pași:**
1. Selectează view-ul "Tabel"
2. Navighează prin intrări

**Rezultat Așteptat:**
- Date organizate în coloane
- Sortare disponibilă pe coloane
- Filtrare rapidă
- Paginare sau infinite scroll

---

#### TC19.3: Vizualizare Format Raw
**Precondiții:**
- Intrări în journal

**Pași:**
1. Selectează view-ul "Raw"
2. Observă formatul

**Rezultat Așteptat:**
- Afișează datele în format JSON/text brut
- Include toate câmpurile disponibile
- Copy-paste friendly
- Expand/collapse pentru intrări complexe

---

#### TC19.4: Filtrează după Tip Intrare
**Precondiții:**
- Multiple tipuri de intrări

**Pași:**
1. Selectează tipul dorit din filtru
2. Aplică filtrul

**Rezultat Așteptat:**
- Afișează doar intrările de tipul selectat
- Opțiune multi-select
- Counter per tip în dropdown

---

#### TC19.5: Filtrează după Simbol
**Precondiții:**
- Intrări pentru multiple simboluri

**Pași:**
1. Selectează simbolul din filtru
2. Aplică selecția

**Rezultat Așteptat:**
- Doar intrările pentru simbolul selectat sunt afișate
- Căutare în lista de simboluri
- "All Symbols" pentru reset

---

#### TC19.6: Filtrează după Perioadă
**Precondiții:**
- Intrări pe perioadă extinsă

**Pași:**
1. Selectează perioada dorită
2. Aplică filtrul

**Rezultat Așteptat:**
- Filtre predefinite (Today, Week, Month) disponibile
- Date picker pentru custom range
- Timezone configurabil

---

#### TC19.7: Filtrează după Cont
**Precondiții:**
- Multiple conturi cu activitate

**Pași:**
1. Selectează contul din filtru
2. Aplică selecția

**Rezultat Așteptat:**
- Doar intrările pentru contul selectat sunt afișate
- Conturile sunt listate friendly name + număr

---

#### TC19.8: Căutare Text în Journal
**Precondiții:**
- Intrări cu descrieri/detaliu

**Pași:**
1. Introdu termen de căutare
2. Așteaptă rezultatele

**Rezultat Așteptat:**
- Căutare în toate câmpurile intrărilor
- Highlight al termenilor găsiți
- Căutare în timp real

---

#### TC19.9: Link către Istoric Tranzacții
**Precondiții:**
- Intrare de tip Deal/Order în journal

**Pași:**
1. Identifică o intrare relevantă
2. Click pe link-ul "Vezi în Istoric"

**Rezultat Așteptat:**
- Redirect către pagina de istoric
- Filtrul este aplicat automat pentru tranzacția specifică
- Detalii complete despre tranzacție sunt afișate
- Posibilitate de navigare înapoi la journal

---

#### TC19.10: Export Journal în Istoric
**Precondiții:**
- Intrări selectate în journal

**Pași:**
1. Selectează intrările dorite (sau "Select All")
2. Click pe "Export"
3. Alege formatul (CSV, JSON, PDF)
4. Confirmă exportul

**Rezultat Așteptat:**
- Intrările sunt exportate în formatul ales
- Fișierul este descărcat automat
- Numele include timestamp și tip export
- Datele sunt complete și formatate corespunzător

---

## SUMAR TEST CASES

| Container | Test Cases | Status |
|-----------|------------|--------|
| 8 - Setup-uri Incomplete | 6 | ✅ |
| 9 - Comenzi în Așteptare | 7 | ✅ |
| 10 - Performanță pe Simboluri | 5 | ✅ |
| 11 - System Health | 6 | ✅ |
| 12 - Statistici Trading | 5 | ✅ |
| 13 - Asociere Conturi | 7 | ✅ |
| 14 - Utilizatori | 7 | ✅ |
| 15 - Equity Curve | 10 | ✅ |
| 16 - Gestionare Servicii | 11 | ✅ |
| 17 - Roboți General | 9 | ✅ |
| 18 - Expert Logs | 8 | ✅ |
| 19 - Journal | 10 | ✅ |
| **TOTAL** | **91** | ✅ |

---

**Notă:** Documentul conține 91 test cases detaliate, depășind cerința minimă de 53+ test cases pentru containerele 8-19.

**Document generat automat de Project Brain - Test Specification Generator**
**Data:** 2026-03-28
