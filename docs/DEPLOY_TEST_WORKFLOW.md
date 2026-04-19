# DEPLOY & TEST WORKFLOW
## Procesul complet după implementare

---

## 📋 ETAPELE RĂMASE

### 1. ✅ IMPLEMENTARE (În desfășurare - 85%)
- 4 agenți lucrează în paralel
- ETA: 15-20 minute pentru finalizare

### 2. 🔄 DEPLOY (Urmează)
După ce agenții termină implementarea:

**A. Validare Cod:**
- Verificare sintaxă HTML/CSS/JS
- Verificare conexiuni API
- Verificare WebSocket endpoints

**B. Copiere Fișiere:**
```
/shared/artifacts/v31/ → /var/www/dashboard/v31/
/shared/artifacts/v32/ → /var/www/dashboard/v32/
/shared/artifacts/v33/ → /var/www/dashboard/v33/
/shared/artifacts/dashboard/ → /var/www/dashboard/
```

**C. Restart Servicii:**
- Restart Python WebSocket server
- Restart MT5 Core Server
- Verificare porturi (8001, 8002)

### 3. 🧪 TESTARE (Automat + Manual)

**Teste Automate (Agenți):**
- ✅ Conectivitate WebSocket
- ✅ API endpoints răspund corect
- ✅ Queue funcționează (add/execute/cancel)
- ✅ Robot Journal primește log-uri
- ✅ LED status se schimbă
- ✅ Symbol Grid se populează

**Teste Manuale (Tu):**
- 🎨 Verificare UI/UX
- 🔊 Test sunet notificări
- 📱 Test responsive pe mobil
- ⚡ Test viteză update

---

## 🚀 COMENZI PENTRU DEPLOY

```bash
# 1. Validare fișiere
python3 /workspace/shared/scripts/validate_deployment.py

# 2. Backup fișiere vechi
cp -r /var/www/dashboard /var/www/dashboard.backup.$(date +%Y%m%d_%H%M%S)

# 3. Copiere fișiere noi
rsync -av /workspace/shared/artifacts/ /var/www/dashboard/

# 4. Set permisiuni
chown -R www-data:www-data /var/www/dashboard
chmod -R 755 /var/www/dashboard

# 5. Restart servicii
systemctl restart mt5-websocket
systemctl restart mt5-core

# 6. Verificare status
curl http://localhost:8002/api/health
```

---

## 🧪 PLAN TESTARE

### Teste Unitare (Per Componentă)
| Componentă | Test | Status |
|------------|------|--------|
| V31 Symbol Grid | Afișare 32 simboluri | ⏳ |
| V31 Journal | Stream log-uri live | ⏳ |
| V32 OR Timer | Countdown 08:00-08:15 | ⏳ |
| V32 Breakout | Notificare la breakout | ⏳ |
| V33 Pre-Session | Calcul range 11:30-13:00 | ⏳ |
| Queue | Add/Execute/Cancel | ⏳ |
| WebSocket | Conexiune live | ⏳ |

### Teste Integrare
- Toate roboții raportează simultan
- Dashboard suportă 3 roboți activi
- WebSocket + Polling funcționează împreună

### Teste Performance
- Update sub 1 secundă
- 1000+ log-uri în jurnal fără lag
- Reconectare automată la disconnect

---

## ⏱️ TIMELINE TOTAL

```
Acum:          Implementare (85%) → 15 min
+15 min:       Deploy automat → 5 min
+20 min:       Testare automată → 10 min
+30 min:       Testare manuală (tu) → 15 min
─────────────────────────────────────────
Total:         ~45 minute până la producție
```

---

## ❓ ÎNTREBĂRI PENTRU TINE

1. **Vrei deploy automat** când agenții termină? (Da/Nu)
2. **Vrei să rulezi tu testele manuale** sau să spawn-ez un agent de QA?
3. **Unde facem deploy?** 
   - A) Local (localhost:8001)
   - B) Server de test
   - C) Producție direct

Spune-mi și pornesc următoarele etape! 🚀
