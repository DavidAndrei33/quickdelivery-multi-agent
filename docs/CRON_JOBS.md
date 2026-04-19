# CRON JOBS - Agent Team Automation

## Job 1: Agent Heartbeat Monitor

**Schedule:** Every 2 minutes  
**Agent:** ops-1  
**Script:** `/workspace/shared/cron/agent_heartbeat.py`

**Actions:**
1. Read all agent status from `/workspace/shared/config/agent_status.json`
2. Check `last_heartbeat` timestamp for each agent
3. If agent hasn't reported in >5 minutes:
   - Mark agent as "stalled"
   - Check their current task
   - If task is critical → Escalate to orchestrator
   - If task is non-critical → Reassign to available agent
4. Update task board with agent status
5. Log summary to `/workspace/shared/logs/heartbeat.log`

---

## Job 2: Task Board Sync

**Schedule:** Every 5 minutes  
**Agent:** ops-1  
**Script:** `/workspace/shared/cron/task_board_sync.py`

**Actions:**
1. Verify task board JSON is valid
2. Check for orphaned tasks (assigned but no agent session)
3. Check for stale tasks (>24h in "In Progress")
4. Auto-assign available tasks to idle agents
5. Send notifications for overdue tasks

---

## Job 3: Bug Triage

**Schedule:** Every 10 minutes  
**Agent:** ops-1  
**Script:** `/workspace/shared/cron/bug_triage.py`

**Actions:**
1. Read all open bugs from `/workspace/shared/bugs/`
2. If CRITICAL bug unassigned >5min → Escalate to orchestrator
3. If HIGH bug unassigned >30min → Auto-assign based on component
4. Check for bugs stuck in "Fixing" >2h → Escalate
5. Update bug priorities based on impact

---

## Job 4: Auto-Retry Failed Tasks

**Schedule:** Every 15 minutes  
**Agent:** ops-1  
**Script:** `/workspace/shared/cron/auto_retry.py`

**Actions:**
1. Read failed tasks from task board
2. For each failed task with retry_count < 3:
   - Increment retry_count
   - Reset status to "Assigned"
   - Move to active queue
   - Notify assigned agent
3. For tasks with retry_count >= 3:
   - Mark as "Permanently Failed"
   - Escalate to human stakeholder

---

## Job 5: Dashboard Health Check

**Schedule:** Every 3 minutes  
**Agent:** ops-1  
**Script:** `/workspace/shared/cron/dashboard_health.py`

**Actions:**
1. Test all API endpoints:
   - /api/v31/live_status
   - /api/v32/or_data
   - /api/v33/or_data
   - etc.
2. If any API returns 500 → Trigger bug-auto-detect
3. Check dashboard HTML loads without JS errors
4. Log health status
5. If unhealthy >3 consecutive checks → Alert orchestrator

---

## Job 6: Daily Standup Report

**Schedule:** Every morning at 08:00 UTC  
**Agent:** ops-1  
**Script:** `/workspace/shared/cron/daily_standup.py`

**Actions:**
1. Count tasks completed yesterday
2. List tasks in progress today
3. Identify blocked tasks
4. List open bugs by priority
5. Generate report: `/workspace/shared/reports/standup-[date].md`
6. Send summary to orchestrator

---

## Job 7: Memory Cleanup

**Schedule:** Every day at 02:00 UTC  
**Agent:** ops-1  
**Script:** `/workspace/shared/cron/memory_cleanup.py`

**Actions:**
1. Archive completed tasks older than 30 days
2. Archive closed bugs older than 90 days
3. Compress old logs
4. Update agent long-term memory files
5. Clean up temporary files in `/tmp/`

---

## Job 8: Performance Metrics

**Schedule:** Every hour  
**Agent:** ops-1  
**Script:** `/workspace/shared/cron/performance_metrics.py`

**Actions:**
1. Calculate average task completion time
2. Track bug resolution time
3. Measure API response times
4. Count agent utilization rates
5. Generate metrics report
6. Alert if metrics degrade

---

## Cron Configuration

Add to system crontab (`crontab -e`):

```cron
# Agent Team Automation
*/2 * * * * /usr/bin/python3 /workspace/shared/cron/agent_heartbeat.py
*/5 * * * * /usr/bin/python3 /workspace/shared/cron/task_board_sync.py
*/10 * * * * /usr/bin/python3 /workspace/shared/cron/bug_triage.py
*/15 * * * * /usr/bin/python3 /workspace/shared/cron/auto_retry.py
*/3 * * * * /usr/bin/python3 /workspace/shared/cron/dashboard_health.py
0 8 * * * /usr/bin/python3 /workspace/shared/cron/daily_standup.py
0 2 * * * /usr/bin/python3 /workspace/shared/cron/memory_cleanup.py
0 * * * * /usr/bin/python3 /workspace/shared/cron/performance_metrics.py
```

## Manual Trigger

All cron jobs can be triggered manually:
```bash
python3 /workspace/shared/cron/agent_heartbeat.py
python3 /workspace/shared/cron/task_board_sync.py
# etc.
```