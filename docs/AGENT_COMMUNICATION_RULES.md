# AGENT COMMUNICATION PROTOCOL

## Rule #1: All Deliverables Go to /workspace/shared/

Never write to personal workspace. Other agents can't find it there.

## Rule #2: Comment on Every State Change

When you:
- Start work → Comment: "[Agent] Starting: [brief description]"
- Find blocker → Comment: "[Agent] Blocked: [specific problem]"
- Complete task → Comment: "[Agent] Complete: [what was done]"
- Need help → Comment: "[Agent] Help needed: [what you need]"

## Rule #3: Use sessions_send for Urgent Only

**DO use sessions_send for:**
- Critical bugs discovered
- Blockers that stop all work
- Priority changes from orchestrator
- Coordination that can't wait

**DON'T use sessions_send for:**
- Routine updates
- Delivering files
- Questions that can wait

## Rule #4: Always Specify Output Path

When completing work, include:
```
Artifacts written to: /workspace/shared/artifacts/[task-id]/
Files:
- main.js (primary implementation)
- test.js (tests)
- README.md (documentation)

To verify: [specific command or check]
```

## Rule #5: Check Task Board Before Starting

Always read `/workspace/shared/tasks/TASKBOARD.json` to see:
- What's currently assigned
- What dependencies exist
- What's blocked

## Rule #6: Escalate Early

If blocked for more than 10 minutes:
1. Comment on task with blocker details
2. Try alternative approach if exists
3. If no alternative → escalate to orchestrator
4. Continue with other work if possible

## Rule #7: Respect File Locks

If a file has `.lock` extension → Don't modify it.
Another agent is working on it.

## Rule #8: Update Your Status

Keep your status current in `/workspace/shared/config/agent_status.json`:
```json
{
  "agent_id": "builder-1",
  "status": "working|idle|blocked",
  "current_task": "TASK-123",
  "started_at": "2026-03-28T07:00:00Z",
  "estimated_completion": "2026-03-28T08:00:00Z"
}
```

## Rule #9: Cross-Reference Related Work

When your work relates to another task:
```
Related to: TASK-456 (dependency)
Related to: BUG-789 (fixes this bug)
Depends on: /workspace/shared/artifacts/TASK-456/output.js
```

## Rule #10: Use Standard Handoff Format

When passing work to another agent:
```markdown
## Handoff from [Agent A] to [Agent B]

### What Was Done
Summary of changes

### Where Artifacts Are
- /workspace/shared/artifacts/TASK-123/main.js
- /workspace/shared/artifacts/TASK-123/test.js

### How to Verify
Run: `npm test TASK-123`
Expected: All tests pass

### Known Issues
- Edge case X not handled (out of scope)
- Performance could be optimized

### What's Next
[Specific next steps for receiving agent]
```