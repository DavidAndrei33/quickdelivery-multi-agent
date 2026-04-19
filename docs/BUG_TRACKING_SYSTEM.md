# 🐛 Bug Tracking System

## Overview
Automated bug detection, assignment, and resolution tracking.

## Bug Lifecycle

```
REPORTED → ASSIGNED → FIXING → TESTING → VERIFIED → CLOSED
    ↑___________________________________________|
```

## Bug Report Format

File: `/workspace/shared/bugs/BUG-[ID]-[timestamp].md`

```markdown
# BUG-001-202603280700

**Status:** REPORTED
**Priority:** CRITICAL / HIGH / MEDIUM / LOW
**Component:** V32 Dashboard / API / MT5 Core / etc.
**Discovered By:** [Agent name]
**Discovered At:** 2026-03-28 07:00 UTC

## Description
Brief description of the bug.

## Expected Behavior
What should happen.

## Actual Behavior
What actually happens.

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Evidence
- Screenshots: `/workspace/shared/bugs/BUG-001/screenshot.png`
- Logs: `/workspace/shared/bugs/BUG-001/logs.txt`
- API Response: ```json { ... } ```

## Assigned To
[To be filled by orchestrator]

## Fix Verification
- [ ] Fix implemented
- [ ] Fix tested
- [ ] Fix verified by tester

## Related Tasks
- TASK-123 (original implementation)
- TASK-456 (this bug fix)
```

## Automatic Bug Detection

### Triggers
1. **API returns 500** → Auto-create bug report
2. **Dashboard shows errors** → Auto-create bug report
3. **Test failure** → Auto-create bug report
4. **Agent reports failure** → Create bug report

### Auto-Assignment Rules
```
CRITICAL bugs → Core-Developer-Lead (immediate)
HIGH bugs → Available Core-Developer
MEDIUM bugs → Next available builder
LOW bugs → Backlog for next sprint
```

## Hook: bug-auto-detect

Location: `/workspace/shared/hooks/bug-auto-detect.js`

Triggered when:
- API endpoint returns 500
- Dashboard JavaScript throws error
- Test suite fails
- Agent reports "FAILED" status

Actions:
1. Create bug report from template
2. Populate with error details
3. Assign based on component
4. Notify orchestrator
5. If CRITICAL → sessions_send to orchestrator

## Hook: bug-assignment

Location: `/workspace/shared/hooks/bug-assignment.js`

Triggered when:
- New bug report created

Actions:
1. Read bug priority and component
2. Query agent availability
3. Assign to appropriate agent
4. Update bug status to ASSIGNED
5. Notify assigned agent via sessions_send

## Hook: bug-fix-verification

Location: `/workspace/shared/hooks/bug-fix-verification.js`

Triggered when:
- Agent marks bug as "FIXED"

Actions:
1. Spawn QA-Tester to verify fix
2. Run regression tests
3. If verified → mark CLOSED
4. If not verified → return to ASSIGNED with feedback

## Communication Protocol

### When Bug Discovered
```
1. Bug report created → /workspace/shared/bugs/
2. Hook triggered → bug-assignment
3. Agent assigned → notified via sessions_send
4. Agent acknowledges → updates status to ASSIGNED
5. Agent starts fixing → updates status to FIXING
```

### When Bug Fixed
```
1. Agent implements fix
2. Agent writes test for fix
3. Agent updates bug report with fix details
4. Agent marks status TESTING
5. Hook triggers verification
6. QA verifies → marks VERIFIED
7. Hook triggers orchestrator review
8. Orchestrator approves → marks CLOSED
```

### Bug Reopened
```
If fix fails verification:
1. Status → ASSIGNED
2. Feedback added to bug report
3. Same agent or new agent assigned
4. Retry attempt incremented
5. After 3 failed attempts → ESCALATE to human
```