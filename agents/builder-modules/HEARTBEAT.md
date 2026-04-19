# HEARTBEAT.md - Builder-Modules

## Scop
Verific periodic dacă există task-uri noi în drop directory (fallback dacă trigger-ul nu a funcționat).

## Checklist Heartbeat

```
□ Verific /workspace/shared/.task-drops/builder-modules/
□ Dacă găsesc fișiere JSON:
   → Citesc primul task
   → Confirm primirea la Andrei (310970306)
   → Execut taskul
   → Updatez taskboard
   → Notific completare
   → Șterg fișierul
□ Dacă nu există fișiere → HEARTBEAT_OK
```

## Format Răspuns

**Dacă am găsit task:**
```
🚀 Task găsit în drop directory: [TASK-ID]
🎯 Încep execuția acum.
```

**Dacă nu am găsit nimic:**
```
HEARTBEAT_OK - Niciun task în așteptare
```

## Note
- Trigger-ul instant via hook este metoda principală
- Heartbeat e doar fallback la fiecare 15 minute
- Priorități: high → medium → low (ordinea procesării)
