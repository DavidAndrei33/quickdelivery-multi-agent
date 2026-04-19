# Agent Spawn Templates

## Quick Reference for Trading Orchestrator

---

## Builder Spawn Template

```bash
sessions_spawn \
  --task "## Task: [TITLE]
**Task ID:** [ID]
**Role:** [Builder Name]
**Priority:** [Critical/High/Medium/Low]

### Context
[What the agent needs to know about the task]

### Deliverables
[Exactly what to produce]
- [ ] Deliverable 1
- [ ] Deliverable 2

### Output Path
/workspace/shared/artifacts/[task-id]/

### Acceptance Criteria
[How to know the task is complete]

### Handoff Instructions
When complete:
1. Write all artifacts to output path
2. Comment on task with handoff summary using format:
   [Builder-X] Handoff: [Brief summary]
   
   ### Deliverables
   - /path/to/file
   
   ### How to Verify
   ```bash
   [test command]
   ```
   
   ### Known Issues
   - [Any limitations]
   
   ### Next
   [What should happen next]
3. Update TASKBOARD.json status to 'review'" \
  --label "[TASK-ID]-[AGENT]" \
  --mode "session"
```

---

## Reviewer Spawn Template

```bash
sessions_spawn \
  --task "## Review Task: [TITLE]
**Task ID:** [ID]
**Role:** [Reviewer Name]
**Priority:** [Critical/High/Medium/Low]

### Context
Review artifacts from [Builder-X] for task [TASK-ID]

### Artifacts to Review
- /workspace/shared/artifacts/[task-id]/

### Review Checklist
- [ ] Architecture makes sense
- [ ] Security issues checked
- [ ] Error handling covered
- [ ] Tests exist and pass
- [ ] Documentation updated
- [ ] No obvious bugs

### Review Output
Write review to: /workspace/shared/reviews/[task-id]-review.md

### Handoff Instructions
When complete:
1. Write review to output path
2. Comment on task with review status:
   [Reviewer-X] Review: [Approved/Changes Required]
   
   ### Findings
   - [Issue 1]: [Description]
   - [Issue 2]: [Description]
   
   ### Action Items
   - [ ] [Action 1]
   - [ ] [Action 2]
3. Update TASKBOARD.json status to 'done' (if approved) or 'in_progress' (if changes needed)" \
  --label "[TASK-ID]-review" \
  --mode "session"
```

---

## Ops Spawn Template

```bash
sessions_spawn \
  --task "## Ops Task: [TITLE]
**Task ID:** [ID]
**Role:** [Ops Agent Name]
**Schedule:** [One-time/Recurring]

### Context
[What needs to be monitored/done]

### Task Details
[Specific instructions]

### Output
[Where to write results]

### Alert Conditions
[When to escalate]

### Handoff Instructions
When complete:
1. Write results to output path
2. Comment on task with summary
3. If recurring, schedule next run" \
  --label "[TASK-ID]-ops" \
  --mode "session"
```

---

## Example: Spawn Core-Developer-1 for API Task

```bash
sessions_spawn \
  --task "## Task: Implement /api/v31/symbols Endpoint
**Task ID:** T017
**Role:** Core-Developer-1
**Priority:** High

### Context
Dashboard needs endpoint to fetch all 32 trading symbols for V31 robot.
Current endpoint returns 404.

### Deliverables
- Implement GET /api/v31/symbols endpoint in mt5_core_server.py
- Return all 32 symbols: EURUSD, GBPUSD, USDCHF, USDJPY, USDCAD, AUDUSD, NZDUSD, AUDNZD, AUDCAD, AUDCHF, AUDJPY, CHFJPY, EURGBP, EURAUD, EURJPY, EURCHF, EURNZD, EURCAD, GBPCHF, GBPJPY, CADCHF, CADJPY, GBPAUD, GBPCAD, GBPNZD, NZDCAD, NZDCHF, NZDJPY, USDSGD, XAUUSD, US30, DE40
- Include symbol metadata (spread, min_volume, etc.)

### Output Path
/workspace/shared/artifacts/T017/

### Acceptance Criteria
- [ ] Endpoint returns 200 with JSON array of 32 symbols
- [ ] Each symbol has: name, spread, min_volume, max_volume
- [ ] Response time <100ms
- [ ] Tested with curl

### Handoff Instructions
When complete:
1. Write code changes summary to /workspace/shared/artifacts/T017/
2. Comment on task with handoff summary
3. Update TASKBOARD.json status to 'review'" \
  --label "T017-builder-1" \
  --mode "session"
```

---

## Example: Spawn QA-Tester-1 for Testing

```bash
sessions_spawn \
  --task "## Task: Test V31 Symbol Status Endpoint
**Task ID:** T017-test
**Role:** QA-Tester-1
**Priority:** High

### Context
Test the new /api/v31/symbols endpoint implemented by Core-Developer-1

### Artifacts to Test
- Endpoint: GET http://localhost:8001/api/v31/symbols
- Expected: 32 symbols with metadata

### Test Checklist
- [ ] API responds with 200
- [ ] Returns exactly 32 symbols
- [ ] Each symbol has required fields (name, spread, min_volume, max_volume)
- [ ] Response time <100ms
- [ ] Error handling works (test with server down)
- [ ] No errors in browser console

### Output Path
/workspace/shared/reviews/T017-test-report.md

### Handoff Instructions
When complete:
1. Write test report to output path
2. Comment on task with test results
3. Update TASKBOARD.json status to 'done' (if pass) or create bug report (if fail)" \
  --label "T017-test-qa" \
  --mode "session"
```

---

## Task Routing Quick Reference

| If Task Is... | Spawn Agent |
|---------------|-------------|
| API endpoint | Core-Developer-1 (builder-1) |
| MT5 integration | Integration-Engineer-1/2 (builder-2/3) |
| Dashboard UI | Dashboard-Frontend (builder-4) |
| Database | Database-Optimizer (builder-5) |
| Trading logic | Trading-Logic (builder-6) |
| Docker/Deploy | DevOps-Engineer (builder-7) |
| Code review | Code-Reviewer-1/2 (reviewer-1/2) |
| Testing | QA-Tester-1 (reviewer-3) |
| Health check | System-Monitor (ops-1) |
| Task board | Task-Coordinator (ops-2) |

---

## Escalation Quick Reference

| Condition | Action |
|-----------|--------|
| API down >5 min | Alert Andrei immediately |
| Margin <100% | Emergency alert |
| Agent blocked >10 min | Reassign or resolve |
| Critical bug >30 min | Escalate to Andrei |
| >3 agents blocked | Escalate to Andrei |

---

## Common Output Paths

```
/workspace/shared/artifacts/[task-id]/          # Build outputs
/workspace/shared/reviews/[task-id]-review.md   # Review feedback
/workspace/shared/bugs/BUG-[id].md              # Bug reports
/workspace/shared/reports/[name]-[date].md      # Reports
/workspace/shared/specs/[feature]-spec.md       # Specifications
/workspace/shared/decisions/[date]-[title].md   # Decisions
```
