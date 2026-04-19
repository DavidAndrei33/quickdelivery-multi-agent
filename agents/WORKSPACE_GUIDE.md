# 🎯 Ghid de Lucru pentru Agenți

## ⚠️ IMPORTANT - CITEȘTE ASTA ÎNAINTE SĂ LUCREZI!

### Path-uri Corecte

**NU lucra în `/workspace/shared/agents/` pentru codul sursă!**

Agenții trebuie să lucreze DIRECT în:

| Componentă | Path Corect | Fișiere Principale |
|------------|-------------|-------------------|
| **Backend** | `/root/clawd/agents/brainmaker/` | `mt5_core_server.py` |
| **Roboți** | `/root/clawd/agents/brainmaker/` | `v31_marius_tpl_robot.py`, `v32_*.py`, `v33_*.py` |
| **Dashboard** | `/root/clawd/agents/brainmaker/dashboard/` | `index.html`, `dashboard_functional.js`, `auth.js` |
| **Teste** | `/root/clawd/agents/brainmaker/tests/` | `test_*.py`, `*_test.py` |
| **Config** | `/workspace/shared/config/` | `team_orchestration.json` |
| **Task-uri** | `/workspace/shared/tasks/auto/` | task-uri generate automat |

### Ce să faci când primești un task:

1. **Citește task-ul** din `/workspace/shared/tasks/auto/BUGFIX-*.json`
2. **Verifică `work_dir`** în task - acolo trebuie să lucrezi
3. **Editează direct** fișierele din path-ul corect
4. **Rulează testele** după modificări
5. **Creează teste noi** dacă nu există pentru bug-ul fixat
6. **NU copia** fișierele în `/workspace/shared/agents/`

### Structura Testelor:

```
/root/clawd/agents/brainmaker/tests/
├── unit/           # Teste unitare (funcții individuale)
├── integration/    # Teste integrare (componente multiple)
├── api/            # Teste API endpoints
├── e2e/            # Teste end-to-end (flow complete)
└── security/       # Teste securitate
```

### Exemple:

```bash
# Corect ✅
nano /root/clawd/agents/brainmaker/mt5_core_server.py

# Corect ✅ - Teste
nano /root/clawd/agents/brainmaker/tests/unit/test_api.py
python3 -m pytest /root/clawd/agents/brainmaker/tests/unit/test_api.py

# Greșit ❌
nano /workspace/shared/agents/mt5_core_server.py
```

### Restart Server (după modificări backend):

```bash
pkill -f mt5_core_server.py
sleep 2
cd /root/clawd/agents/brainmaker
nohup python3 mt5_core_server.py > /tmp/mt5_server.log 2>&1 &
```

### Rulează Teste:

```bash
# Toate testele
cd /root/clawd/agents/brainmaker
python3 -m pytest tests/

# Doar testele API
python3 -m pytest tests/api/

# Doar un fișier specific
python3 -m pytest tests/unit/test_v31.py -v
```

### Verificare Health:

```bash
curl http://localhost:8001/health
```

---

*Generat automat de Agent Workspace Setup*
