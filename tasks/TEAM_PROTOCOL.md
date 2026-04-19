# Team Protocol - Trading Dashboard Multi-Agent System

## Version
2.1.0 - Updated with Agent Team Orchestration best practices

## Team Structure (13 Agents)

### Orchestrator (1)
| Agent | ID | Role | Specialty |
|-------|-----|------|-----------|
| Trading Orchestrator | orchestrator | Orchestrator | Task Routing, Priority Management |

### Builders (7)
| Agent | ID | Role | Specialty |
|-------|-----|------|-----------|
| Core-Developer-1 | builder-1 | Builder | API Implementation, Backend Logic |
| Integration-Engineer-1 | builder-2 | Builder | API Integration, Data Flow |
| Integration-Engineer-2 | builder-3 | Builder | MT5 Integration, Real-time Data |
| Dashboard-Frontend | builder-4 | Builder | UI/UX, JavaScript, CSS |
| Database-Optimizer | builder-5 | Builder | PostgreSQL, Query Optimization |
| Trading-Logic | builder-6 | Builder | Trading Algorithms, Risk Management |
| DevOps-Engineer | builder-7 | Builder | Docker, Deployment, Infrastructure |

### Reviewers (3)
| Agent | ID | Role | Specialty |
|-------|-----|------|-----------|
| Code-Reviewer-1 | reviewer-1 | Reviewer | Code Quality, Architecture |
| Code-Reviewer-2 | reviewer-2 | Reviewer | Security, Performance |
| QA-Tester-1 | reviewer-3 | Reviewer | End-to-End Testing, Bug Discovery |

### Ops (2)
| Agent | ID | Role | Specialty |
|-------|-----|------|-----------|
| System-Monitor | ops-1 | Ops | Health Checks, Alerts, Cron Jobs |
| Task-Coordinator | ops-2 | Ops | Task Board Maintenance, Reporting |

## Task Lifecycle

```
Inbox → Assigned → In Progress → Review → Done | Failed
```

### State Definitions
- **Inbox**: New task, unassigned
- **Assigned**: Agent selected, not yet started
- **In Progress**: Agent actively working
- **Review**: Work complete, awaiting verification
- **Done**: Verified and shipped
- **Failed**: Abandoned with documented reason

### State Transitions
- **Orchestrator**: Inbox → Assigned, Review → Done, Any → Failed
- **Agents**: In Progress → Review (with handoff comment)
- **Reviewers**: Review → In Progress (return with feedback), Review → Done (approve)

## Handoff Protocol

Every handoff MUST include:

1. **What was done** - Summary of changes
2. **Where artifacts are** - Exact file paths
3. **How to verify** - Test commands or acceptance criteria
4. **Known issues** - Anything incomplete or risky
5. **What's next** - Clear next action

### Handoff Comment Format
```markdown
[Agent] Handoff: [Brief summary]

### Deliverables
- /path/to/file1
- /path/to/file2

### How to Verify
```bash
[test command]
```

### Known Issues
- [Issue 1]
- [Issue 2]

### Next
[What the receiving agent should do]
```

## Auto-Assignment Rules

### By Task Type
| Task Type | Assigned To |
|-----------|-------------|
| API endpoints | Core-Developer-1 (builder-1) |
| MT5 integration | Integration-Engineer-1/2 (builder-2/3) |
| Dashboard UI | Dashboard-Frontend (builder-4) |
| Database queries | Database-Optimizer (builder-5) |
| Trading logic | Trading-Logic (builder-6) |
| Docker/Deploy | DevOps-Engineer (builder-7) |
| Code review | Code-Reviewer-1/2 (reviewer-1/2) |
| Testing | QA-Tester-1 (reviewer-3) |
| Health checks | System-Monitor (ops-1) |
| Task board | Task-Coordinator (ops-2) |

## Escalation Triggers

### Immediate Escalation
- API down >5 minutes
- Margin level <100%
- Critical security vulnerability found
- Trade execution failing
- MT5 disconnect >2 minutes

### Escalation After Threshold
- Agent blocked >10 minutes
- Critical bug unfixed >30 minutes
- >3 agents blocked simultaneously
- Task stale >48 hours

## Communication Channels

### Shared Files (Primary)
- `/workspace/shared/specs/` - Requirements and specifications
- `/workspace/shared/artifacts/` - Build outputs
- `/workspace/shared/reviews/` - Review notes
- `/workspace/shared/decisions/` - Architecture decisions

### Task Comments
- Attached to specific tasks in TASKBOARD.json
- Chronological record of progress

### Direct Messages (sessions_send)
- Urgent priority changes
- Quick questions blocking progress
- **Don't use for**: Routine updates, artifact delivery

## Heartbeat Schedule

### Every 30 Minutes (Orchestrator)
1. Read TASKBOARD.json for new tasks
2. Check agent_status.json for blocked agents
3. Verify API endpoints (V31, V32, V33, Core)
4. Check for unassigned bugs
5. Update Andrei if anything critical

### Every 5 Minutes (Ops Agents)
- System-Monitor: Resource checks
- Task-Coordinator: Board consistency checks

## Review Policy

### Required Reviews
- Every code change gets reviewed
- Every API endpoint gets tested
- Every UI change gets visual verification

### Review Rotation
- Task from Agent A → Reviewed by Agent B
- Rotate reviewers to prevent blind spots

### Skip Review (Orchestrator Only)
- Trivial documentation updates
- Emergency fixes (review post-hoc)
- **Must document** when review was skipped

## Quality Gates

### Before Marking Done
- [ ] Code reviewed (if code change)
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No Critical/High bugs
- [ ] Handoff comment written

## File Locations

### Agent SOULs
- `/workspace/shared/memory/agents/orchestrator/SOUL.md`
- `/workspace/shared/memory/agents/builder-{1-7}/SOUL.md`
- `/workspace/shared/memory/agents/reviewer-{1-3}/SOUL.md`
- `/workspace/shared/memory/agents/ops-{1-2}/SOUL.md`

### State Files
- `/workspace/shared/memory/agents/agent_status.json` - Agent states
- `/workspace/shared/memory/project/project_state.json` - Project state
- `/workspace/shared/tasks/TASKBOARD.json` - Task board

### Shared Directories
- `/workspace/shared/specs/` - Specifications
- `/workspace/shared/artifacts/` - Build outputs
- `/workspace/shared/reviews/` - Review feedback
- `/workspace/shared/decisions/` - Decisions
- `/workspace/shared/bugs/` - Bug reports
- `/workspace/shared/reports/` - Reports

## Decision Logging

Architecture or product decisions go to `/workspace/shared/memory/decisions/`:

```markdown
# Decision: [Title]
**Date:** YYYY-MM-DD
**Author:** [Agent]
**Status:** Proposed | Accepted | Rejected
**Task:** [Task ID]

## Context
Why this decision came up.

## Options Considered
1. Option A — tradeoffs
2. Option B — tradeoffs

## Decision
What was chosen and why.

## Consequences
What changes as a result.
```

## Emergency Procedures

### API Down
1. System-Monitor detects and alerts immediately
2. Orchestrator notifies Andrei
3. Core-Developer-1 investigates
4. DevOps-Engineer checks infrastructure
5. Status updates every 5 minutes until resolved

### Critical Bug in Production
1. QA-Tester-1 confirms and documents
2. Orchestrator assigns to appropriate builder
3. Code-Reviewer-2 reviews fix
4. DevOps-Engineer deploys
5. QA-Tester-1 verifies fix

### MT5 Disconnect
1. System-Monitor detects and alerts immediately
2. Integration-Engineer-2 investigates
3. Trading-Logic assesses open positions
4. Orchestrator notifies Andrei if positions at risk

## On-Call Rotation

### Current
- Primary: Trading Orchestrator
- Secondary: System-Monitor
- Human Escalation: Andrei

### Contact
- Telegram: @AndreiCocan
- Emergency: Trading system halt if no response in 15 minutes
