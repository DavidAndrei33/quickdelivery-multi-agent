#!/usr/bin/env node

/**
 * Task Publisher CLI
 * 
 * Usage:
 *   node publisher.js create-task <project> --title "..." --assignee operations-all
 *   node publisher.js assign-task <project> <task-id> --assignee operations-all
 *   node publisher.js move-task <project> <task-id> --to in_progress
 */

const TaskboardEventBus = require('./lib/event-bus');

async function main() {
  const bus = new TaskboardEventBus();
  await bus.connect();

  const command = process.argv[2];
  const projectId = process.argv[3];

  try {
    switch (command) {
      case 'create-project':
        await createProject(bus, projectId);
        break;

      case 'create-task':
        await createTask(bus, projectId);
        break;

      case 'assign-task':
        await assignTask(bus, projectId);
        break;

      case 'move-task':
        await moveTask(bus, projectId);
        break;

      case 'list-tasks':
        await listTasks(bus, projectId);
        break;

      default:
        console.log(`
📋 Task Publisher CLI

Commands:
  create-project <project-id>     Create a new project
  create-task <project-id>        Create a new task
  assign-task <project> <task>    Assign task to agent
  move-task <project> <task>      Move task to another column
  list-tasks <project>            List all tasks in project

Examples:
  node publisher.js create-project quickdelivery
  node publisher.js create-task quickdelivery --title "Setup CI/CD" --assignee operations-all --priority high
  node publisher.js assign-task quickdelivery TASK-001 --assignee builder-modules
  node publisher.js move-task quickdelivery TASK-001 --to in_progress
        `);
    }
  } catch (err) {
    console.error('❌ Error:', err.message);
  } finally {
    await bus.disconnect();
  }
}

async function createProject(bus, projectId) {
  const project = await bus.createProject(projectId, {
    name: projectId,
    description: `Project ${projectId}`,
    status: 'active'
  });
  console.log(`✅ Project ${projectId} created`);
}

async function createTask(bus, projectId) {
  const args = parseArgs(process.argv.slice(4));
  
  const task = await bus.createTask(projectId, {
    title: args.title || 'Untitled Task',
    description: args.description || '',
    type: args.type || 'feature',
    priority: args.priority || 'medium',
    assignee: args.assignee || null,
    requirements: args.requirements ? args.requirements.split(',') : [],
    acceptance_criteria: args.criteria ? args.criteria.split(',') : []
  }, 'product-architect');

  console.log(`✅ Task created: ${task.id}`);
  if (task.assignee) {
    console.log(`📢 Notified: ${task.assignee}`);
  }
}

async function assignTask(bus, projectId) {
  const taskId = process.argv[4];
  const args = parseArgs(process.argv.slice(5));
  
  await bus.assignTask(projectId, taskId, args.assignee, 'product-architect');
  console.log(`✅ Task ${taskId} assigned to ${args.assignee}`);
}

async function moveTask(bus, projectId) {
  const taskId = process.argv[4];
  const args = parseArgs(process.argv.slice(5));
  
  await bus.updateTaskStatus(projectId, taskId, args.to, 'product-architect');
  console.log(`✅ Task ${taskId} moved to ${args.to}`);
}

async function listTasks(bus, projectId) {
  const project = await bus.getProject(projectId);
  
  console.log(`\n📋 Tasks in ${projectId}:\n`);
  
  const byStatus = {};
  for (const task of project.taskboard.tasks) {
    if (!byStatus[task.status]) byStatus[task.status] = [];
    byStatus[task.status].push(task);
  }
  
  for (const [status, tasks] of Object.entries(byStatus)) {
    console.log(`\n${status.toUpperCase()} (${tasks.length}):`);
    for (const task of tasks) {
      const assignee = task.assignee ? `@${task.assignee}` : 'unassigned';
      console.log(`  ${task.id}: ${task.title} [${assignee}]`);
    }
  }
}

function parseArgs(args) {
  const result = {};
  for (let i = 0; i < args.length; i += 2) {
    const key = args[i].replace(/^--/, '');
    result[key] = args[i + 1];
  }
  return result;
}

main();
