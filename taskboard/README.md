# Taskboard Event Bus System

Sistem multi-proiect de task management cu arhitectură Event Bus folosind Redis Pub/Sub.

## 📁 Structura

```
/workspace/shared/taskboard/
├── config.json           # Configurație globală (agenți, canale, tipuri)
├── lib/
│   └── event-bus.js      # Clasa principală TaskboardEventBus
├── publisher.js          # CLI pentru publicare evenimente
├── subscriber.js         # CLI pentru agenți (subscribe)
└── data.json             # Index proiecte (vechi - păstrat pentru compatibilitate)

/workspace/shared/.project-brain/projects/
└── {project-id}/
    └── taskboard.json    # Task-uri per proiect
```

## 🚀 Quick Start

### 1. Start Redis (dacă nu rulează deja)
```bash
redis-server
```

### 2. Creează un proiect
```bash
cd /workspace/shared/taskboard
node publisher.js create-project quickdelivery
```

### 3. Creează un task
```bash
node publisher.js create-task quickdelivery \
  --title "Setup CI/CD Pipeline" \
  --assignee operations-all \
  --priority high \
  --type devops
```

### 4. Subscribe ca agent (în alt terminal)
```bash
node subscriber.js --agent operations-all
```

## 📋 Comenzi Publisher

```bash
# Creează proiect
node publisher.js create-project <project-id>

# Creează task
node publisher.js create-task <project-id> \
  --title "Task title" \
  --description "Description" \
  --assignee operations-all \
  --priority high|medium|low \
  --type feature|bug|devops|...

# Assign task
node publisher.js assign-task <project> <task-id> --assignee <agent>

# Move task
node publisher.js move-task <project> <task-id> --to <column>

# List tasks
node publisher.js list-tasks <project>
```

## 👤 Agenți Disponibili

| Agent | Rol | Evenimente |
|-------|-----|------------|
| product-architect | Product Owner + Orchestrator | task.completed, task.blocked |
| backend-architect | API/DB Architect | task.assigned |
| frontend-architect | UI/UX Architect | task.assigned |
| builder-modules | Web Developer | task.assigned |
| builder-mobile | Mobile Developer | task.assigned |
| reviewer-all | Code Reviewer | task.status_changed |
| operations-all | DevOps Engineer | task.assigned, agent.notify |
| specialists-all | Research/BA | task.created |

## 📡 Tipuri de Evenimente

- `task.created` - Task nou creat
- `task.assigned` - Task asignat unui agent
- `task.status_changed` - Task mutat în altă coloană
- `task.completed` - Task terminat
- `task.blocked` - Task blocat
- `agent.notify` - Notificare directă către agent

## 🔧 API Programatic

```javascript
const TaskboardEventBus = require('./lib/event-bus');

const bus = new TaskboardEventBus();
await bus.connect();

// Creează task
const task = await bus.createTask('quickdelivery', {
  title: 'Setup CI/CD',
  assignee: 'operations-all',
  priority: 'high'
}, 'product-architect');

// Subscribe la evenimente
await bus.subscribeAgent('operations-all', ['task.assigned'], (event) => {
  console.log('New task:', event);
});
```

## 📝 TODO

- [ ] Integrare cu Telegram bots
- [ ] WebSocket server pentru UI real-time
- [ ] Retry logic pentru agenți offline
- [ ] Dead letter queue
- [ ] Metrics și monitoring
