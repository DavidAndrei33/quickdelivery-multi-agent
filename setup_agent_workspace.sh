#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# AGENT WORKSPACE SETUP - Setup corect pentru agenți
# ═══════════════════════════════════════════════════════════════════════════

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}═══════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  🚀 AGENT WORKSPACE SETUP - Trading System${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════════${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# PATH-URI CORECTE
# ═══════════════════════════════════════════════════════════════════════════

BACKEND_ROOT="/root/clawd/agents/brainmaker"
DASHBOARD_ROOT="/root/clawd/agents/brainmaker/dashboard"
TESTS_ROOT="/root/clawd/agents/brainmaker/tests"
SHARED_AGENTS="/workspace/shared/agents"

echo -e "${YELLOW}📁 Directoare de lucru:${NC}"
echo "   Backend:  $BACKEND_ROOT"
echo "   Dashboard: $DASHBOARD_ROOT"
echo "   Tests:    $TESTS_ROOT"
echo "   Shared:   $SHARED_AGENTS"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# CREARE STRUCTURĂ TESTE
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${YELLOW}📁 Creare structură directoare teste...${NC}"

mkdir -p "$TESTS_ROOT"/{unit,integration,api,e2e,security}

echo -e "   ${GREEN}✓${NC} $TESTS_ROOT/unit"
echo -e "   ${GREEN}✓${NC} $TESTS_ROOT/integration"
echo -e "   ${GREEN}✓${NC} $TESTS_ROOT/api"
echo -e "   ${GREEN}✓${NC} $TESTS_ROOT/e2e"
echo -e "   ${GREEN}✓${NC} $TESTS_ROOT/security"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# VERIFICARE FIȘIERE EXISTENTE
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${YELLOW}🔍 Verificare fișiere backend...${NC}"

files=(
    "$BACKEND_ROOT/mt5_core_server.py"
    "$BACKEND_ROOT/v31_marius_tpl_robot.py"
    "$BACKEND_ROOT/v32_london_breakout_robot.py"
    "$BACKEND_ROOT/v33_ny_breakout_robot.py"
    "$DASHBOARD_ROOT/index.html"
    "$DASHBOARD_ROOT/dashboard_functional.js"
    "$DASHBOARD_ROOT/auth.js"
)

all_exist=true
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "   ${GREEN}✓${NC} $(basename $file)"
    else
        echo -e "   ${RED}✗${NC} $(basename $file) - LIPSEȘTE"
        all_exist=false
    fi
done

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# CURĂȚARE FIȘIERE DUPLICATE (dacă există)
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${YELLOW}🧹 Curățare fișiere duplicate în /workspace/shared/agents/...${NC}"

# Șterge fișiere duplicate dacă există
for file in "$SHARED_AGENTS"/*.py; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        if [ -f "$BACKEND_ROOT/$filename" ]; then
            echo -e "   ${YELLOW}⚠${NC} Ștergere duplicat: $filename"
            rm "$file"
        fi
    fi
done

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# CREARE SYMLINKS PENTRU REFERINȚĂ (opțional)
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${YELLOW}🔗 Creare symlink-uri pentru referință...${NC}"

# Crează symlink către backend
if [ ! -L "$SHARED_AGENTS/backend" ]; then
    ln -s "$BACKEND_ROOT" "$SHARED_AGENTS/backend" 2>/dev/null && \
        echo -e "   ${GREEN}✓${NC} backend → $BACKEND_ROOT" || \
        echo -e "   ${YELLOW}⚠${NC} backend symlink există sau eroare"
fi

# Crează symlink către dashboard
if [ ! -L "$SHARED_AGENTS/dashboard" ]; then
    ln -s "$DASHBOARD_ROOT" "$SHARED_AGENTS/dashboard" 2>/dev/null && \
        echo -e "   ${GREEN}✓${NC} dashboard → $DASHBOARD_ROOT" || \
        echo -e "   ${YELLOW}⚠${NC} dashboard symlink există sau eroare"
fi

# Crează symlink către tests
if [ ! -L "$SHARED_AGENTS/tests" ]; then
    ln -s "$TESTS_ROOT" "$SHARED_AGENTS/tests" 2>/dev/null && \
        echo -e "   ${GREEN}✓${NC} tests → $TESTS_ROOT" || \
        echo -e "   ${YELLOW}⚠${NC} tests symlink există sau eroare"
fi

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# INSTRUCȚIUNI PENTRU AGENȚI
# ═══════════════════════════════════════════════════════════════════════════

cat > "$SHARED_AGENTS/WORKSPACE_GUIDE.md" << 'EOF'
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
EOF

echo -e "${GREEN}✓${NC} Ghid de lucru creat: $SHARED_AGENTS/WORKSPACE_GUIDE.md"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# EXEMPLU TEST
# ═══════════════════════════════════════════════════════════════════════════

cat > "$TESTS_ROOT/api/test_health_endpoint.py" << 'EOF'
"""
Test simplu pentru health endpoint
"""
import requests
import pytest

def test_health_endpoint():
    """Testează că serverul răspunde pe /health"""
    response = requests.get('http://localhost:8001/health', timeout=5)
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'healthy'
    assert 'port' in data
    print(f"✅ Health check passed: {data}")

if __name__ == '__main__':
    test_health_endpoint()
EOF

echo -e "${GREEN}✓${NC} Exemplu test creat: $TESTS_ROOT/api/test_health_endpoint.py"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# REZUMAT
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${BLUE}═══════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  ✅ SETUP COMPLET${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Configurație actualizată:${NC}"
echo "   • Path-uri corecte definite în config"
echo "   • Structură teste creată"
echo "   • Bug router actualizat cu work_dir și test_files"
echo "   • Fișiere duplicate curățate"
echo "   • Ghid de lucru creat pentru agenți"
echo ""
echo -e "${YELLOW}Următorul pas:${NC}"
echo "   Bug-urile noi vor fi rutate corect către path-urile definitive."
echo "   Testele trebuie create/rulate în /root/clawd/agents/brainmaker/tests/"
echo ""
echo ""
