#!/usr/bin/env node

/**
 * Agent Subscriber
 * 
 * Usage:
 *   node subscriber.js --agent operations-all
 *   node subscriber.js --agent builder-modules
 */

const TaskboardEventBus = require('./lib/event-bus');
const config = require('./config.json');
const fs = require('fs').promises;
const path = require('path');

async function main() {
  const agentId = getArg('--agent');
  
  if (!agentId) {
    console.log(`
👤 Agent Subscriber

Usage:
  node subscriber.js --agent <agent-id>

Available agents:
${Object.keys(config.agents).map(id => `  - ${id}`).join('\n')}
    `);
    process.exit(1);
  }

  const agent = config.agents[agentId];
  if (!agent) {
    console.error(`❌ Unknown agent: ${agentId}`);
    process.exit(1);
  }

  console.log(`
╔════════════════════════════════════════════════════════════╗
║  👤 ${agent.name} ${agent.emoji}                                    ║
║  Role: ${agent.role.padEnd(45)}║
║  Subscribed: ${agent.subscribed_events.join(', ').padEnd(37)}║
╚════════════════════════════════════════════════════════════╝
  `);

  const bus = new TaskboardEventBus();
  await bus.connect();

  // Subscribe to events
  await bus.subscribeAgent(agentId, agent.subscribed_events, (event) => {
    handleEvent(agentId, agent, event);
  });

  console.log('👂 Listening for events... (Press Ctrl+C to stop)\n');

  // Keep alive
  process.on('SIGINT', async () => {
    console.log('\n👋 Disconnecting...');
    await bus.disconnect();
    process.exit(0);
  });
}

function handleEvent(agentId, agent, event) {
  const timestamp = new Date(event.timestamp).toLocaleTimeString();
  
  console.log(`\n${'─'.repeat(60)}`);
  console.log(`📨 EVENT RECEIVED at ${timestamp}`);
  console.log(`${'─'.repeat(60)}`);
  
  switch (event.type) {
    case 'task.created':
      console.log(`🆕 NEW TASK: ${event.task.title}`);
      console.log(`   ID: ${event.task.id}`);
      console.log(`   Project: ${event.projectId}`);
      console.log(`   Priority: ${event.task.priority}`);
      if (event.task.assignee) {
        console.log(`   Assignee: @${event.task.assignee}`);
      }
      break;

    case 'task.assigned':
      if (event.assignee === agentId) {
        console.log(`🎯 TASK ASSIGNED TO YOU!`);
        console.log(`   Task: ${event.taskId}`);
        console.log(`   Project: ${event.projectId}`);
        console.log(`   Assigned by: ${event.assigner}`);
        
        // Scrie notificare în fișier pentru ca agentul să o citească
        writeNotificationFile(agentId, event);
      }
      break;

    case 'task.status_changed':
      console.log(`🔄 STATUS CHANGE: ${event.taskId}`);
      console.log(`   ${event.oldStatus} → ${event.newStatus}`);
      console.log(`   By: ${event.changedBy}`);
      break;

    case 'task.completed':
      console.log(`✅ TASK COMPLETED: ${event.taskId}`);
      console.log(`   By: ${event.completedBy}`);
      break;

    case 'task.blocked':
      console.log(`🚫 TASK BLOCKED: ${event.taskId}`);
      console.log(`   Reason: ${event.reason}`);
      console.log(`   By: ${event.blockedBy}`);
      break;

    case 'agent.notify':
      console.log(`🔔 NOTIFICATION:`);
      console.log(`   ${JSON.stringify(event.notification, null, 2)}`);
      break;

    default:
      console.log(`📋 ${event.type}:`);
      console.log(JSON.stringify(event, null, 2));
  }
  
  console.log(`${'─'.repeat(60)}\n`);
}

function notifyTelegram(agent, event) {
  // Placeholder pentru integrare Telegram
  // Poți folosi node-telegram-bot-api aici
  console.log(`📱 [Telegram] Would notify ${agent.telegram}`);
  console.log(`   "🎯 Task ${event.taskId} assigned to you!"`);
}

async function writeNotificationFile(agentId, event) {
  // Scrie notificare în fișier pentru ca agentul să o citească
  const inboxPath = `/workspace/shared/agents/${agentId}/.inbox`;
  const notificationFile = path.join(inboxPath, `notification-${Date.now()}.json`);
  
  const notification = {
    type: event.type,
    timestamp: event.timestamp,
    taskId: event.taskId || event.task?.id,
    projectId: event.projectId,
    assignee: event.assignee,
    assigner: event.assigner,
    title: event.task?.title || 'Task nou',
    priority: event.task?.priority || 'medium',
    read: false,
    received_at: new Date().toISOString()
  };
  
  try {
    await fs.mkdir(inboxPath, { recursive: true });
    await fs.writeFile(notificationFile, JSON.stringify(notification, null, 2));
    console.log(`📝 Notification written to: ${notificationFile}`);
  } catch (err) {
    console.error(`❌ Failed to write notification: ${err.message}`);
  }
}

function getArg(name) {
  const index = process.argv.indexOf(name);
  return index !== -1 ? process.argv[index + 1] : null;
}

main().catch(console.error);
