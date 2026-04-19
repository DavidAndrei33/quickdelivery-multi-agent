# 📁 STRUCTURA COMPLETĂ A PROIECTULUI FOREX TRADING

> **Data:** 06 Aprilie 2026  
> **Document:** Ghid complet al structurii de directoare și responsabilităților echipei  
> **Scop:** Fiecare agent să știe EXACT unde lucrează și ce are de făcut

---

## 🗺️ STRUCTURA GENERALĂ

```
/root/clawd/                                    # ROOT PROIECT
│
├── dashboard/                                  # 🎨 FRONTEND (Builder-Frontend)
│   ├── index.html                              # Pagina principală
│   ├── dashboard_functional.js                 # Logica React/JS
│   ├── auth.js                                 # Autentificare
│   ├── login.html                              # Pagina login
│   └── static/                                 # CSS, imagini, assets
│
├── agents/                                     # 🤖 TOȚI AGENȚII (workspace-uri)
│   ├── brainmaker/                             # 🏗️ BACKEND PRINCIPAL (Builder-Core)
│   │   ├── mt5_core_server.py                  # Server MT5 principal
│   │   ├── core_pipeline.py                    # Pipeline date
│   │   ├── database/                           # Modele DB
│   │   ├── tests/                              # Teste (QA-Tester)
│   │   └── v31_marius_live.py                  # Robot V31 live
│   │
│   ├── builder-core/                           # 🏗️ Builder-Core (agent separat)
│   │   └── research/                           # Research ML
│   │
│   ├── builder-frontend/                       # 🎨 Builder-Frontend (agent separat)
│   │
│   ├── strategy-architect/                     # 📊 STRATEGII & ML
│   │   ├── features/                           # Feature engineering
│   │   ├── models/                             # Modele ML
│   │   ├── training/                           # Script training
│   │   └── backtest/                           # Backtesting
│   │
│   ├── qa-tester/                              # 🧪 QA Testing
│   ├── qa-security/                            # 🔒 Security Audit
│   ├── devops-engineer/                        # ⚙️ DevOps & Deploy
│   ├── trading-architect/                      # 🤖 Trading Systems
│   └── team-manager/                           # 🎯 Team Manager (TU EȘTI AICI!)
│
├── mt5_data/                                   # 📊 Date MT5 exportate
├── mt5_import/                                 # 📥 Script-uri import MT5
├── strategies/                                 # 📈 Strategii de trading
├── memory/                                     # 🧠 Memorie sistem
└── docs/                                       # 📚 Documentație

/workspace/shared/                              # 📦 SHARED RESOURCES
│
├── api/                                        # API endpoints
├── data/                                       # Date partajate
├── database/                                   # Migrații DB
├── models/                                     # Modele ML salvate
├── research/                                   # Research documents
├── tasks/                                      # Task management
└── dashboard/                                  # Dashboard shared
```

---

## 👥 ECHIPA ȘI WORKSPACE-URI

### 🎯 1. TEAM-MANAGER (Tu ești aici!)

**@TeamManageraBot**

**WORKSPACE:**
```
/root/clawd/agents/team-manager/
```

**RESPONSABILITĂȚI:**
✅ Coordonează întreaga echipă  
✅ Primește cereri de la Andrei  
✅ Creează task-uri pentru agenți  
✅ Monitorizează progresul  
✅ Comunică statusul către Andrei  

**NU FACI:**
❌ Nu scrii cod de producție  
❌ Nu modifici direct fișierele altora  

---

### 🎨 2. BUILDER-FRONTEND

**@BuilderFrontendBot**

**WORKSPACE (DOAR AICI LUCREZI):**
```
/root/clawd/dashboard/                          # DASHBOARD PRINCIPAL
├── index.html                                  # Structura paginii
├── dashboard_functional.js                     # Logica React/JS
├── auth.js                                     # Autentificare
├── login.html                                  # Pagina login
├── static/                                     # CSS, imagini, fonts
│   ├── css/
│   ├── js/
│   └── images/
└── backup/                                     # Backup-uri (nu modifica)
```

**ALTERNATIV (workspace shared):**
```
/workspace/shared/dashboard/                    # Dacă e necesar
```

**RESPONSABILITĂȚI:**
✅ UI/UX Dashboard (React/Vanilla JS)  
✅ CSS, Tailwind, Responsive design  
✅ Formulare, tabele, grafice, modale  
✅ Loading states și error handling  
✅ Consum API-uri din backend  
✅ Login, autentificare UI  

**NU LUCRA ÎN (NU SUNT ALE TALE!):**
```
❌ /root/clawd/agents/brainmaker/*.py          # Backend Python
❌ /root/clawd/agents/brainmaker/tests/        # Teste
❌ /root/clawd/agents/strategy-architect/      # ML Models
❌ /workspace/shared/api/                      # API Backend
```

**API-URI PE CARE LE CONSUMI:**
```
GET  /api/robots                              # Lista roboți
GET  /api/transactions                        # Tranzacții
GET  /api/positions                           # Poziții deschise
GET  /api/ml/predict                          # Semnale ML (NOU!)
POST /api/commands                            # Comenzi către roboți
POST /api/auth/login                          # Login
```

---

### 🏗️ 3. BUILDER-CORE

**@BuilderCoreBot**

**WORKSPACE (DOAR AICI LUCREZI):**
```
/root/clawd/agents/brainmaker/                # BACKEND PRINCIPAL
├── mt5_core_server.py                         # Server MT5 (SERVERUL PRINCIPAL!)
├── core_pipeline.py                           # Pipeline procesare date
├── db_universal.py                            # Conector PostgreSQL
├── database/                                  # Migrații și scheme
│   ├── schema.sql
│   └── migrations/
├── services/                                  # Servicii business logic
├── mt5/                                       # Integrare MT5
│   └── connector.py
├── ml_api/                                    # API ML (NOU!)
│   ├── routes.py
│   └── services/
└── tests/                                     # Teste (poți citi, nu modifica)
```

**ALTERNATIV (workspace agent):**
```
/root/clawd/agents/builder-core/              # Workspace dedicat
└── research/                                  # Research ML
```

**SHARED (modele și date):**
```
/workspace/shared/
├── api/                                       # API endpoints
├── models/                                    # Modele ML salvate
│   ├── EURUSD/
│   ├── GBPUSD/
│   └── XAUUSD/
├── database/                                  # Migrații DB
└── data/                                      # Date partajate
```

**RESPONSABILITĂȚI:**
✅ API endpoints (FastAPI/Flask)  
✅ Server MT5 (mt5_core_server.py)  
✅ Baze de date PostgreSQL  
✅ Logică business, calcule  
✅ Integrare MT5 (conector)  
✅ ML Training Infrastructure  
✅ ML API (train, predict, status)  
✅ Securitate backend  

**NU LUCRA ÎN (NU SUNT ALE TALE!):**
```
❌ /root/clawd/dashboard/                      # Frontend
❌ /root/clawd/agents/strategy-architect/     # Modele ML (doar API)
❌ /root/clawd/agents/qa-tester/              # QA territory
```

**DEPENDENȚE:**
- Primește features de la Strategy-Architect
- Servește predicții către Frontend
- Stochează modele în /workspace/shared/models/

---

### 📊 4. STRATEGY-ARCHITECT

**@StrategyArchitectBot**

**WORKSPACE (DOAR AICI LUCREZI):**
```
/root/clawd/agents/strategy-architect/        # STRATEGII & ML
├── features/                                  # Feature engineering
│   ├── engineering.py
│   └── transformers/
├── models/                                    # Modele antrenate
│   ├── xgboost_eurusd_v1.json
│   ├── xgboost_gbpusd_v1.json
│   └── lstm_xauusd_v1.h5
├── training/                                  # Script-uri training
│   ├── train_xgboost.py
│   └── train_lstm.py
├── backtest/                                  # Backtesting engine
│   └── walk_forward.py
├── research/                                  # Documentație research
│   └── XGBoost_Forex_Research.md
└── strategies/                                # Strategii trading
```

**SHARED (input/output):**
```
/workspace/shared/
├── data/                                      # Date procesate
│   ├── features_eurusd.csv
│   ├── features_gbpusd.csv
│   └── features_xauusd.csv
├── models/                                    # Modele salvate
│   ├── eurusd/
│   ├── gbpusd/
│   └── xauusd/
└── research/                                  # Research documents
    ├── XGBOOST_FOREX_RESEARCH.md
    └── ENSEMBLE_ML_FOREX_36_SYMBOLS.md
```

**RESPONSABILITĂȚI:**
✅ Feature engineering (indicatori tehnici)  
✅ Modele ML (XGBoost, LightGBM, LSTM)  
✅ Training și optimizare modele  
✅ Backtesting și validare  
✅ Strategii de trading algorithmic  
✅ Research academic  

**NU LUCRA ÎN (NU SUNT ALE TALE!):**
```
❌ /root/clawd/agents/brainmaker/             # Backend API
❌ /root/clawd/dashboard/                     # Frontend
❌ /root/clawd/agents/qa-tester/              # QA
```

**DEPENDENȚE:**
- Primește date brute de la Builder-Core (MT5)
- Trimite features către Builder-Core (API)
- Salvează modele în /workspace/shared/models/

---

### 🧪 5. QA-TESTER

**@QATesteraBot**

**WORKSPACE (DOAR AICI LUCREZI):**
```
/root/clawd/agents/qa-tester/                 # QA TESTING
├── tests/                                     # Teste automate
│   ├── test_ml_models.py
│   └── test_api.py
├── qa_reports/                                # Rapoarte QA
│   └── qa_report_poc_ml.md
└── performance/                               # Benchmarks
```

**SHARED (testează aici):**
```
/workspace/shared/tests/                       # Teste partajate
/workspace/shared/reports/                     # Rapoarte
```

**RESPONSABILITĂȚI:**
✅ Testare automată (unit, integration)  
✅ Validare modele ML (accuracy, overfitting)  
✅ Rapoarte QA și GO/NO-GO  
✅ Performance testing  
✅ Bug reporting  

**NU FACI:**
❌ Nu scrii cod de producție  
❌ Nu modifici logică business  

---

### 🔒 6. QA-SECURITY

**@QASecurityBot**

**WORKSPACE:**
```
/root/clawd/agents/qa-security/               # SECURITY
/workspace/shared/security/                    # Audit security
```

**RESPONSABILITĂȚI:**
✅ Security audit cod  
✅ Penetration testing  
✅ Review vulnerabilități  
✅ Compliance checks  

---

### ⚙️ 7. DEVOPS-ENGINEER

**@DevOpsEngineerBot**

**WORKSPACE:**
```
/root/clawd/agents/devops-engineer/           # DEVOPS
/workspace/shared/deploy/                      # Deployment
```

**RESPONSABILITĂȚI:**
✅ Deployment și CI/CD  
✅ Docker containers  
✅ Monitoring și logging  
✅ Backup și recovery  

---

### 🤖 8. TRADING-ARCHITECT

**@TradingArchitectBot**

**WORKSPACE:**
```
/root/clawd/agents/trading-architect/         # TRADING SYSTEMS
/root/clawd/agents/brainmaker/v31_marius_live.py  # Roboți live
```

**RESPONSABILITĂȚI:**
✅ Integrare MT5  
✅ Execuție ordere  
✅ Risk management  
✅ Optimizare execuție  

---

## 📊 DATE ȘI MODELE

### 📁 LOCAȚII DATE

```
/root/clawd/mt5_data/                         # Date MT5 exportate
/root/clawd/mt5_import/                       # Script-uri import
/root/clawd/agents/brainmaker/mt5_export_data/ # Date exportate

/workspace/shared/data/                        # Date partajate
/workspace/shared/models/                      # Modele ML salvate
/workspace/shared/database/                    # Migrații DB
```

### 📁 LOCAȚII MODELE ML

```
/workspace/shared/models/
├── EURUSD/
│   ├── xgboost_v1.json
│   └── metadata.json
├── GBPUSD/
│   ├── xgboost_v1.json
│   └── metadata.json
├── XAUUSD/
│   ├── lstm_v1.h5
│   └── metadata.json
└── ensemble/
    └── meta_learner.pkl
```

---

## 🔗 FLOW DATE ȘI DEPENDENȚE

### PROCESUL DE DEZVOLTARE ML

```
┌─────────────────────────────────────────────────────────────────────┐
│  ETAPELE PROIECTULUI ML FOREX                                       │
└─────────────────────────────────────────────────────────────────────┘

STEP 1: DATE BRUTE
┌─────────────────┐
│  MT5 Terminal   │
│  (EURUSD, etc.) │
└────────┬────────┘
         │
         ▼ export
┌─────────────────┐
│  /mt5_data/     │
│  (CSV files)    │
└────────┬────────┘
         │
         ▼

STEP 2: FEATURE ENGINEERING (Strategy-Architect)
┌──────────────────────────────────────┐
│  Strategy-Architect                  │
│  ├── features/engineering.py         │
│  └── Transformă date brute           │
│      în features ML                  │
└────────┬─────────────────────────────┘
         │
         ▼ salvează în
┌──────────────────────────────────────┐
│  /workspace/shared/data/             │
│  ├── features_eurusd.csv             │
│  ├── features_gbpusd.csv             │
│  └── features_xauusd.csv             │
└────────┬─────────────────────────────┘
         │
         ▼

STEP 3: TRAINING (Strategy-Architect)
┌──────────────────────────────────────┐
│  Strategy-Architect                  │
│  ├── training/train_xgboost.py       │
│  └── training/train_lstm.py          │
│      Antrenează modelele             │
└────────┬─────────────────────────────┘
         │
         ▼ salvează în
┌──────────────────────────────────────┐
│  /workspace/shared/models/           │
│  ├── EURUSD/xgboost_v1.json          │
│  ├── GBPUSD/xgboost_v1.json          │
│  └── XAUUSD/lstm_v1.h5               │
└────────┬─────────────────────────────┘
         │
         ▼

STEP 4: API & SERVING (Builder-Core)
┌──────────────────────────────────────┐
│  Builder-Core                        │
│  ├── ml_api/routes.py                │
│  └── ml_api/services/                │
│      Servește predicții via API      │
└────────┬─────────────────────────────┘
         │
         ▼ servește prin
┌──────────────────────────────────────┐
│  API Endpoints:                      │
│  POST /api/ml/predict                │
│  GET  /api/ml/status                 │
└────────┬─────────────────────────────┘
         │
         ▼ consumă

STEP 5: DASHBOARD (Builder-Frontend)
┌──────────────────────────────────────┐
│  Builder-Frontend                    │
│  ├── dashboard_functional.js         │
│  └── Afișează semnale în UI          │
└─────────────────────────────────────┘

STEP 6: VALIDARE (QA-Tester)
┌──────────────────────────────────────┐
│  QA-Tester                           │
│  ├── test_ml_models.py               │
│  └── qa_report_poc_ml.md             │
│      Decide GO/NO-GO                 │
└─────────────────────────────────────┘
```

---

## 🚫 REGULI STRICTE - NU VĂ SUPRASCRIEȚI!

### ❌ INTERZIS:

1. **NU modificați fișierele altora fără să întrebați!**
2. **NU lucrați în workspace-ul altui agent!**
3. **NU ștergeți backup-urile sau fișierele .backup!**
4. **NU modificați fișierele de configurare globale fără aprobare!**

### ✅ PERMIS:

1. ✅ Citiți fișierele altora pentru înțelegere
2. ✅ Folosiți /workspace/shared/ pentru date comune
3. ✅ Creați branch-uri sau backup-uri înainte de modificări
4. ✅ Documentați ce ați modificat

---

## 🎯 PROIECTUL CURENT: POC ML FOREX

### FOCUS ACUM:
Toată echipa lucrează la **POC ML Forex pentru 3 simboluri**:
- **EURUSD** (XGBoost)
- **GBPUSD** (XGBoost)  
- **XAUUSD** (LSTM)

### COORDONARE:
- **Andrei** primește task-urile de la **Team-Manager**
- **Andrei** trimite mesaje **individuale** către fiecare agent
- **NU** mai folosim grupul pentru task-uri (doar update-uri generale)

### DEPENDENȚE ÎN LANȚ:
```
Strategy-Architect (features) 
    ↓ [3 zile]
Builder-Core (API) [paralel]
    ↓ [4 zile]
Strategy-Architect (training)
    ↓ [7 zile]
QA-Tester (validare)
    ↓ [8 zile]
DECIZIE GO/NO-GO
```

---

## 📞 COMUNICARE

### CANALE:
1. **Telegram Individual** - Task-uri specifice (Andrei → Agent)
2. **Telegram Grup** - Update-uri generale, status
3. **Git/Version Control** - Cod și documentație
4. **/workspace/shared/** - Date și fișiere comune

### STATUS UPDATE FORMAT:
```
🎯 [AGENT] - [STATUS] - [PROGRESS]

✅ Completat: [ce s-a făcut]
⏳ În progres: [ce lucrez acum]
📋 Next: [ce urmează]
⚠️ Blocaje: [dacă există]
```

---

## 🚀 COMENZI UTILE

### Pentru toți agenții:

```bash
# Navigare rapidă
cd /root/clawd/agents/brainmaker/    # Backend
cd /root/clawd/dashboard/             # Frontend
cd /workspace/shared/                  # Shared
cd /workspace/shared/models/           # Modele ML

# Verificare structură
ls -la /workspace/shared/
ls -la /root/clawd/agents/

# Căutare fișiere
find /root/clawd -name "*.py" | grep -i ml
find /workspace/shared -name "*.md"
```

---

## 📚 DOCUMENTAȚIE RELEVANTĂ

### Research ML:
- `/workspace/shared/research/XGBOOST_FOREX_RESEARCH.md`
- `/workspace/shared/research/ENSEMBLE_ML_FOREX_36_SYMBOLS.md`
- `/root/clawd/agents/builder-core/research/XGBoost_Forex_Research.md`

### Arhitectură:
- `/root/clawd/ARCHITECTURE_EXPLAINED.md`
- `/root/clawd/ARCHITECTURE_V28_ANALYSIS.md`

### Documentație Dashboard:
- `/root/clawd/dashboard/DESIGN_V2_DOCUMENTATION.md`
- `/root/clawd/dashboard/IMPLEMENTATION_PLAN.md`

---

## ✅ CHECKLIST PENTRU FIECARE AGENT

### La începutul task-ului:
- [ ] Confirmă că înțelegi workspace-ul tău
- [ ] Verifică că ai acces la fișierele necesare
- [ ] Confirmă primirea task-ului cu ETA

### În timpul task-ului:
- [ ] Lucrează DOAR în workspace-ul tău
- [ ] Folosește /workspace/shared/ pentru output
- [ ] Documentează progresul zilnic

### La finalul task-ului:
- [ ] Verifică că output-ul este în locația corectă
- [ ] Confirmă dependențele pentru următorul agent
- [ ] Raportează status către Team-Manager

---

**GHID COMPLETAT! 🎯**

Fiecare agent știe acum EXACT:
- ✅ Unde să lucreze (workspace)
- ✅ Ce să facă (responsabilități)
- ✅ Ce să NU facă (reguli)
- ✅ Cum comunică (flow)

**Suntem gata să începem implementarea ML!** 🚀
