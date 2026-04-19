# STANDING ORDERS - Agent Team Operations

## Order #1: Always Check Task Board First

Before starting ANY work:
1. Read `/workspace/shared/tasks/TASKBOARD.json`
2. Identify your assigned task
3. Check dependencies - if blocked, escalate immediately
4. Update your status to "working"

## Order #2: Test Before Marking Complete

Never mark a task as "Done" without testing:
1. Test your changes locally
2. Verify APIs respond correctly
3. Check dashboard elements populate
4. Only then update task status

**If you cannot test → Escalate to orchestrator**

## Order #3: Communicate State Changes

Every status change requires a comment:
- `Starting: [what you're doing]`
- `Progress: [X% complete, what's left]`
- `Blocked: [specific blocker, after 10 min of trying]`
- `Complete: [what was done, how to verify]`
- `Failed: [why, what was attempted]`

## Order #4: Use Shared Files Only

All deliverables MUST go to `/workspace/shared/`:
- Code → `/workspace/shared/artifacts/[task-id]/`
- Specs → `/workspace/shared/specs/`
- Reviews → `/workspace/shared/reviews/`

**Never write to your personal workspace** - other agents can't find it.

## Order #5: Retry Failed Tasks (Max 3)

If a task fails:
1. First failure → Wait 60s, retry with different approach
2. Second failure → Wait 5min, escalate blocker
3. Third failure → Mark FAILED, notify orchestrator

Do NOT silently retry more than 3 times.

## Order #6: Respect File Locks

If a file has `.lock` extension:
- DO NOT modify it
- Wait for lock to be removed
- Or escalate: "File X is locked, need access"

## Order #7: Bug Discovery Protocol

When you discover a bug:
1. Stop current work (if bug is critical)
2. Document bug in `/workspace/shared/bugs/`
3. Trigger bug-auto-detect hook
4. Continue with other work if possible
5. Wait for assignment to fix

## Order #8: API Failure Handling

When an API call fails:
1. Log the error with context
2. Retry once after 5 seconds
3. If still failing → Use fallback (logs, cache, etc.)
4. If no fallback → Mark task blocked, escalate

## Order #9: Coordinate on Shared Resources

Before modifying shared files:
1. Check if another agent is working on it (look for .lock)
2. If conflict likely → Comment first, wait for response
3. If urgent → Use sessions_send for immediate coordination

## Order #10: End-of-Task Handoff

When completing a task, include:
```markdown
## Handoff Complete

### What Was Done
[Summary]

### Artifacts Location
- /workspace/shared/artifacts/[task-id]/

### How to Verify
[Specific steps]

### Known Limitations
[What wasn't done / edge cases]

### Related Bugs Fixed
[BUG-XXX if applicable]
```

---

## Escalation Triggers

**Escalate IMMEDIATELY to orchestrator when:**
- Blocked for >10 minutes with no progress
- Task scope increases >2x from original
- Need access/credentials you don't have
- Security concern discovered
- Multiple tasks failing with same error (systemic issue)

**Escalate to human stakeholder when:**
- Product decision needed
- Budget/resource constraint
- 3rd party dependency issue
- Legal/compliance question