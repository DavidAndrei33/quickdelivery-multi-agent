/**
 * Simple Task Dashboard - Multi Project
 * No Event Bus, no Redis. Just JSON files.
 * Andrei notifies agents manually.
 */

const fs = require('fs').promises;
const path = require('path');

const DATA_FILE = path.join(__dirname, 'data.json');
const PROJECTS_DIR = path.join('/workspace/shared', '.project-brain', 'projects');

async function loadData() {
  const data = await fs.readFile(DATA_FILE, 'utf8');
  return JSON.parse(data);
}

async function saveData(data) {
  await fs.writeFile(DATA_FILE, JSON.stringify(data, null, 2));
}

async function ensureDir(dir) {
  await fs.mkdir(dir, { recursive: true });
}

// ═══════════════════════════════════════════════════════════════
// PROJECTS
// ═══════════════════════════════════════════════════════════════

async function createProject(name, description = '') {
  const data = await loadData();
  const projectId = `PROJ-${String(data.next_project_id).padStart(3, '0')}`;
  
  const project = {
    id: projectId,
    name,
    description,
    status: 'active',
    created_at: new Date().toISOString(),
    tasks: [],
    columns: ['inbox', 'todo', 'in_progress', 'review', 'done'],
    next_task_id: 1
  };
  
  data.projects[projectId] = project;
  data.next_project_id++;
  
  // Save project to its own file too
  const projectDir = path.join(PROJECTS_DIR, projectId);
  await ensureDir(projectDir);
  await fs.writeFile(
    path.join(projectDir, 'taskboard.json'),
    JSON.stringify(project, null, 2)
  );
  
  await saveData(data);
  console.log(`✅ Project ${projectId} created: ${name}`);
  return project;
}

// ═══════════════════════════════════════════════════════════════
// TASKS
// ═══════════════════════════════════════════════════════════════

async function createTask(projectId, taskData) {
  const data = await loadData();
  const project = data.projects[projectId];
  
  if (!project) {
    throw new Error(`Project ${projectId} not found`);
  }
  
  const taskId = `TASK-${String(project.next_task_id).padStart(3, '0')}`;
  
  const task = {
    id: taskId,
    title: taskData.title || 'Untitled',
    description: taskData.description || '',
    type: taskData.type || 'feature',
    priority: taskData.priority || 'medium',
    assignee: taskData.assignee || null,
    status: taskData.status || 'inbox',
    requirements: taskData.requirements || [],
    acceptance_criteria: taskData.acceptance_criteria || [],
    created_by: taskData.created_by || 'product-architect',
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  };
  
  project.tasks.push(task);
  project.next_task_id++;
  
  // Update project file
  const projectDir = path.join(PROJECTS_DIR, projectId);
  await fs.writeFile(
    path.join(projectDir, 'taskboard.json'),
    JSON.stringify(project, null, 2)
  );
  
  await saveData(data);
  
  // Print notification message for Andrei
  console.log(`\n${'='.repeat(60)}`);
  console.log(`✅ TASK CREATED: ${taskId}`);
  console.log(`${'='.repeat(60)}`);
  console.log(`📋 Title: ${task.title}`);
  console.log(`🎯 Project: ${project.name} (${projectId})`);
  console.log(`👤 Assignee: ${task.assignee || 'Unassigned'}`);
  console.log(`🔥 Priority: ${task.priority}`);
  console.log(`📊 Status: ${task.status}`);
  console.log(`${'='.repeat(60)}`);
  
  if (task.assignee) {
    const agent = data.agents[task.assignee];
    if (agent) {
      console.log(`\n📱 NOTIFICATION MESSAGE FOR ${agent.name}:`);
      console.log(`${'-'.repeat(60)}`);
      console.log(`Hey ${agent.name}! 👋`);
      console.log(`\nYou have a new task assigned:`);
      console.log(`\n🆔 ${taskId}: ${task.title}`);
      console.log(`🎯 Project: ${project.name}`);
      console.log(`🔥 Priority: ${task.priority.toUpperCase()}`);
      console.log(`\nPlease check the taskboard and start working on it.`);
      console.log(`\nTaskboard: /workspace/shared/taskboard/data.json`);
      console.log(`${'-'.repeat(60)}`);
    }
  }
  
  return task;
}

// ═══════════════════════════════════════════════════════════════
// LIST & SHOW
// ═══════════════════════════════════════════════════════════════

async function listProjects() {
  const data = await loadData();
  console.log('\n📁 PROJECTS:\n');
  
  for (const [id, project] of Object.entries(data.projects)) {
    const taskCount = project.tasks.length;
    console.log(`  ${id}: ${project.name} (${taskCount} tasks) [${project.status}]`);
  }
  
  if (Object.keys(data.projects).length === 0) {
    console.log('  No projects yet.');
  }
}

async function listTasks(projectId) {
  const data = await loadData();
  const project = data.projects[projectId];
  
  if (!project) {
    console.log(`❌ Project ${projectId} not found`);
    return;
  }
  
  console.log(`\n📋 TASKS IN ${project.name}:\n`);
  
  // Group by status
  const byStatus = {};
  for (const col of project.columns) {
    byStatus[col] = [];
  }
  
  for (const task of project.tasks) {
    if (!byStatus[task.status]) byStatus[task.status] = [];
    byStatus[task.status].push(task);
  }
  
  for (const [status, tasks] of Object.entries(byStatus)) {
    if (tasks.length > 0) {
      console.log(`\n${status.toUpperCase()} (${tasks.length}):`);
      for (const task of tasks) {
        const assignee = task.assignee ? `@${task.assignee}` : 'unassigned';
        const priority = task.priority ? `[${task.priority.toUpperCase()}]` : '';
        console.log(`  ${task.id}: ${task.title} ${priority} [${assignee}]`);
      }
    }
  }
  
  if (project.tasks.length === 0) {
    console.log('  No tasks yet.');
  }
}

async function showTask(projectId, taskId) {
  const data = await loadData();
  const project = data.projects[projectId];
  
  if (!project) {
    console.log(`❌ Project ${projectId} not found`);
    return;
  }
  
  const task = project.tasks.find(t => t.id === taskId);
  if (!task) {
    console.log(`❌ Task ${taskId} not found`);
    return;
  }
  
  console.log(`\n${'='.repeat(60)}`);
  console.log(`📋 TASK DETAILS`);
  console.log(`${'='.repeat(60)}`);
  console.log(`🆔 ID: ${task.id}`);
  console.log(`📌 Title: ${task.title}`);
  console.log(`📝 Description: ${task.description || 'N/A'}`);
  console.log(`🎯 Project: ${project.name}`);
  console.log(`👤 Assignee: ${task.assignee || 'Unassigned'}`);
  console.log(`🔥 Priority: ${task.priority}`);
  console.log(`📊 Status: ${task.status}`);
  console.log(`🏷️ Type: ${task.type}`);
  console.log(`👤 Created by: ${task.created_by}`);
  console.log(`📅 Created: ${task.created_at}`);
  
  if (task.requirements.length > 0) {
    console.log(`\n📋 Requirements:`);
    task.requirements.forEach((r, i) => console.log(`  ${i + 1}. ${r}`));
  }
  
  if (task.acceptance_criteria.length > 0) {
    console.log(`\n✅ Acceptance Criteria:`);
    task.acceptance_criteria.forEach((c, i) => console.log(`  ${i + 1}. ${c}`));
  }
  
  console.log(`${'='.repeat(60)}\n`);
}

// ═══════════════════════════════════════════════════════════════
// UPDATE TASK
// ═══════════════════════════════════════════════════════════════

async function updateTask(projectId, taskId, updates) {
  const data = await loadData();
  const project = data.projects[projectId];
  
  if (!project) {
    throw new Error(`Project ${projectId} not found`);
  }
  
  const task = project.tasks.find(t => t.id === taskId);
  if (!task) {
    throw new Error(`Task ${taskId} not found`);
  }
  
  // Apply updates
  if (updates.status) task.status = updates.status;
  if (updates.assignee) task.assignee = updates.assignee;
  if (updates.priority) task.priority = updates.priority;
  if (updates.title) task.title = updates.title;
  if (updates.description) task.description = updates.description;
  
  task.updated_at = new Date().toISOString();
  
  // Save
  const projectDir = path.join(PROJECTS_DIR, projectId);
  await fs.writeFile(
    path.join(projectDir, 'taskboard.json'),
    JSON.stringify(project, null, 2)
  );
  await saveData(data);
  
  console.log(`✅ Task ${taskId} updated`);
  if (updates.status) {
    console.log(`📊 New status: ${updates.status}`);
  }
  if (updates.assignee) {
    console.log(`👤 New assignee: ${updates.assignee}`);
    
    // Print notification
    const agent = data.agents[updates.assignee];
    if (agent) {
      console.log(`\n📱 ${agent.name} has been assigned to this task!`);
    }
  }
  
  return task;
}

// ═══════════════════════════════════════════════════════════════
// CLI
// ═══════════════════════════════════════════════════════════════

async function main() {
  const command = process.argv[2];
  
  try {
    switch (command) {
      case 'create-project':
        await createProject(process.argv[3], process.argv[4] || '');
        break;
        
      case 'create-task': {
        const projectId = process.argv[3];
        const args = parseArgs(process.argv.slice(4));
        await createTask(projectId, {
          title: args.title,
          description: args.description,
          assignee: args.assignee,
          priority: args.priority,
          type: args.type,
          status: args.status,
          requirements: args.requirements ? args.requirements.split(',') : [],
          acceptance_criteria: args.criteria ? args.criteria.split(',') : []
        });
        break;
      }
      
      case 'list-projects':
        await listProjects();
        break;
        
      case 'list-tasks':
        await listTasks(process.argv[3]);
        break;
        
      case 'show-task':
        await showTask(process.argv[3], process.argv[4]);
        break;
        
      case 'move-task': {
        const [projId, taskId] = [process.argv[3], process.argv[4]];
        const args = parseArgs(process.argv.slice(5));
        await updateTask(projId, taskId, { status: args.to });
        break;
      }
      
      case 'assign-task': {
        const [projId, taskId] = [process.argv[3], process.argv[4]];
        const args = parseArgs(process.argv.slice(5));
        await updateTask(projId, taskId, { assignee: args.assignee });
        break;
      }
      
      default:
        console.log(`
📋 Simple Task Dashboard - Multi Project

Commands:
  create-project <name> [description]     Create new project
  create-task <project-id> [options]      Create new task
  list-projects                           List all projects
  list-tasks <project-id>                 List tasks in project
  show-task <project-id> <task-id>        Show task details
  move-task <project> <task> --to <col>   Move task to column
  assign-task <project> <task> --assignee <agent>

Options for create-task:
  --title "Task name"
  --description "Description"
  --assignee operations-all
  --priority high|medium|low
  --type feature|bug|devops|...
  --status inbox|todo|in_progress|review|done
  --requirements "req1,req2,req3"
  --criteria "crit1,crit2,crit3"

Examples:
  node dashboard.js create-project QuickDelivery "Food delivery app"
  node dashboard.js create-task PROJ-001 --title "Setup CI" --assignee operations-all --priority high
  node dashboard.js list-tasks PROJ-001
  node dashboard.js move-task PROJ-001 TASK-001 --to in_progress
        `);
    }
  } catch (err) {
    console.error('❌ Error:', err.message);
    process.exit(1);
  }
}

function parseArgs(args) {
  const result = {};
  for (let i = 0; i < args.length; i += 2) {
    if (args[i].startsWith('--')) {
      const key = args[i].replace(/^--/, '');
      result[key] = args[i + 1];
    }
  }
  return result;
}

main();
