# 🧪 TEST PLAN - Product-Architect + Builder-Modules Integration

## Status Configurare
✅ **Product-Architect** - Port 18790, @ProductArchitectbot  
✅ **Builder-Modules** - Port 18793, @BuilderModulesBot (STARTED)  
✅ **Task Drop Directory** - /workspace/shared/.task-drops/builder-modules/  
✅ **Trigger Hook** - http://localhost:18793/task-assigned  

---

## 📝 Ce să spui la Product-Architect:

**Mesaj de test:**
> "Creează un task simplu de test pentru Builder-Modules: Crează un fișier HTML simplu cu titlul 'Hello World' și salvează-l în /tmp/test-builder.html. Task ID: TEST-001, prioritate: medium."

**Product-Architect ar trebui să:**
1. Creeze specificația
2. Salveze fișierul în `/workspace/shared/.task-drops/builder-modules/TEST-001.json`
3. Trimită trigger automat către Builder-Modules
4. Confirme Andrei: "Task creat și trimis către Builder-Modules"

---

## 🤖 Ce ar trebui să facă Builder-Modules:

**La primire trigger:**
1. Primește mesajul: "🎯 TASK NOU PRIMIT!"
2. Citește fișierul TEST-001.json
3. **Notifică Andrei automat:** "🚀 Builder-Modules: Am primit task TEST-001: Crează un fișier HTML simplu. Încep execuția acum."
4. Execută taskul (crează fișierul HTML)
5. **La final:** Updatează taskboard + notifică: "✅ Task TEST-001 completat!"

---

## 🔧 Fallback (dacă trigger-ul nu merge):

Builder-Modules are heartbeat configurat la fiecare 15 minute care verifică dacă există fișiere în drop directory.

**Mesaj alternativ pentru Andrei către Builder-Modules:**
> "Verifică dacă ai task-uri noi în /workspace/shared/.task-drops/builder-modules/ și execută-le pe toate."

---

## 📞 Contact Agenți

| Agent | Telegram | Port | Status |
|-------|----------|------|--------|
| Product-Architect | @ProductArchitectbot | 18790 | ✅ Online |
| Builder-Modules | @BuilderModulesBot | 18793 | ✅ Online |

---

## 🚨 Troubleshooting

**Dacă Builder-Modules nu primește taskul:**
1. Verifică gateway-ul rulează: `systemctl status openclaw-builder-modules`
2. Verifică fișierul există: `ls /workspace/shared/.task-drops/builder-modules/`
3. Trigger manual: `curl -X POST http://localhost:18793/task-assigned -H "Content-Type: application/json" -d '{"taskId":"TEST-001","taskFile":"/workspace/shared/.task-drops/builder-modules/TEST-001.json"}'`

**Loguri:**
- Builder-Modules: `journalctl -u openclaw-builder-modules -f`
- Product-Architect: `journalctl -u openclaw-product-architect -f`
