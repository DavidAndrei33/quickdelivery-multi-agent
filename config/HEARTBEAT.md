# HEARTBEAT.md - System Control Loop

## Purpose
Heartbeat = motorul sistemului multi-agent. Rulează continuu pentru a menține coordonarea echipei.

## Cycle Configuration
```yaml
interval: 2m
activeHours:
  start: "00:00"
  end: "23:59"
  timezone: "UTC"
target: "orchestrator"
```

## Heartbeat Checklist

### 1. AGENT HEALTH CHECK (Priority: CRITICAL)
```
□ Verifică heartbeat fiecare agent (last_heartbeat < 5 min)
□ Dacă agent stalled > 5 min → Alertă + Reassign task
□ Verifică dacă agenții lucrează la task-urile corecte
□ Update agent_status.json
```
**Action:** Dacă agent down → Escalate + Reassign

### 2. TASK BOARD SYNC (Priority: HIGH)
```
□ Verifică task-uri orfane (assigned dar fără agent)
□ Verifică task-uri stale (>24h în progress)
□ Auto-assign task-uri disponibile la agenți idle
□ Mută task-uri completed/failed în liste corecte
```
**Action:** Dacă task blocat >2h → Escalate

### 3. BUG TRACKING (Priority: HIGH)
```
□ Verifică bug-uri CRITICAL neasignate
□ Verifică bug-uri stuck în "Fixing" >2h
□ Auto-assign bug-uri noi bazat pe component
□ Update bug counts
```
**Action:** Dacă bug critic nefixat → Escalate

### 4. API HEALTH CHECK (Priority: CRITICAL)
```
□ Testează /api/v31/live_status
□ Testează /api/v32/or_data
□ Testează /api/v33/or_data
□ Testează /api/*/breakout_status
□ Dacă orice API 500 → Trigger bug-auto-detect
```
**Action:** Dacă API down → Alertă imediată

### 5. DASHBOARD HEALTH (Priority: MEDIUM)
```
□ Verifică dacă dashboard răspunde
□ Verifică dacă JS console are erori
□ Verifică dacă elementele se populează
```
**Action:** Dacă dashboard error → Log + Notify

### 6. MEMORY SYNC (Priority: LOW)
```
□ Verifică dimensiunea fișierelor de log
□ Arhivează date vechi (>30 zile)
□ Update long-term memory pentru agenți
```

## Decision Rules

```python
if critical_api_down:
    alert_orchestrator_immediately()
    trigger_emergency_bug_report()
    
elif agent_stalled:
    reassign_task_to_available_agent()
    log_incident()
    
elif task_blocked > 2h:
    escalate_to_orchestrator()
    suggest_alternative_approach()
    
elif critical_bug_unassigned > 5min:
    auto_assign_to_lead_developer()
    notify_orchestrator()
    
elif all_systems_healthy:
    update_metrics()
    log_status("HEARTBEAT_OK")
```

## Output Format

La fiecare heartbeat, raportează:

```
═══════════════════════════════════════════
💓 HEARTBEAT - 2026-03-28 07:10:00 UTC
═══════════════════════════════════════════

🤖 AGENȚI: 7/7 active
   builder-1: 🟢 working (TASK-FIX-JS-001)
   builder-2: 🟢 working (TASK-FIX-API-001)
   reviewer-1: 🟢 available
   ops-1: 🟢 running cron jobs

📋 TASKS: 2 active, 0 blocked
   TASK-FIX-JS-001: In Progress (15%)
   TASK-FIX-API-001: In Progress (20%)

🐛 BUGS: 3 open (all assigned)
   BUG-001: Fixing (builder-1)
   BUG-002: Fixing (builder-1)
   BUG-003: Fixing (builder-2)

🌐 APIs: 🟢 All Healthy
   /api/v31/live_status: 200 OK
   /api/v32/or_data: 200 OK
   /api/v33/or_data: 200 OK

✅ STATUS: HEARTBEAT_OK
   Toate sistemele funcționează normal
═══════════════════════════════════════════
```

## Triggers

### Triggers Cron Jobs
- Dacă `agent_stalled` → Trigger agent_recovery
- Dacă `api_error` → Trigger bug_report
- Dacă `task_overdue` → Trigger escalation

### Updates Standing Orders
- Log decisions în `/workspace/shared/decisions/`
- Update task status în `/workspace/shared/tasks/TASKBOARD.json`
- Archive completed items

## Manual Trigger

Heartbeat poate fi triggered manual:
```bash
python3 /workspace/shared/cron/agent_heartbeat.py
```