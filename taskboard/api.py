#!/usr/bin/env python3
"""
Taskboard Backend API
Simple Flask API for persisting taskboard data
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
import sys
import threading
import time
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

# Import webhook handler
from webhook_handler import webhook_bp
from notifier import notifier, AGENT_BOTS, OWNER_CHAT_ID

# Register webhook blueprint
app.register_blueprint(webhook_bp, url_prefix='/webhook')

# Paths
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(DATA_DIR, 'data.json')
BACKUP_DIR = os.path.join(DATA_DIR, 'backups')

# Ensure backup directory exists
os.makedirs(BACKUP_DIR, exist_ok=True)

def load_data():
    """Load data from JSON file"""
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return default structure if file doesn't exist
        return {
            "version": "2.0.0",
            "last_updated": datetime.now().isoformat(),
            "agents": {},
            "projects": {},
            "tasks": [],
            "columns": ["inbox", "todo", "in_progress", "review", "done"],
            "next_task_id": 1
        }

def save_data(data):
    """Save data to JSON file with backup"""
    # Create backup before saving
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(BACKUP_DIR, f'data_backup_{timestamp}.json')
    
    # Save current data as backup
    current_data = load_data()
    with open(backup_file, 'w') as f:
        json.dump(current_data, f, indent=2)
    
    # Update timestamp
    data['last_updated'] = datetime.now().isoformat()
    
    # Save new data
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    
    return True

@app.route('/')
def index():
    """Serve the taskboard HTML"""
    return send_from_directory(DATA_DIR, 'taskboard.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    """Get all taskboard data"""
    data = load_data()
    return jsonify(data)

@app.route('/api/data', methods=['POST'])
def update_data():
    """Update all taskboard data"""
    try:
        new_data = request.get_json()
        if not new_data:
            return jsonify({"error": "No data provided"}), 400
        
        save_data(new_data)
        return jsonify({"success": True, "message": "Data saved successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks (optionally filtered by project)"""
    data = load_data()
    project = request.args.get('project')
    
    tasks = data.get('tasks', [])
    if project:
        tasks = [t for t in tasks if t.get('project') == project]
    
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    try:
        data = load_data()
        task = request.get_json()
        
        if not task:
            return jsonify({"error": "No task data provided"}), 400
        
        # Generate task ID
        task_id = f"TASK-{str(data['next_task_id']).zfill(3)}"
        task['id'] = task_id
        task['created_at'] = datetime.now().isoformat()
        
        # Add to tasks list
        data['tasks'].append(task)
        data['next_task_id'] += 1
        
        save_data(data)
        return jsonify({"success": True, "task": task})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a specific task"""
    try:
        data = load_data()
        task_updates = request.get_json()
        
        # Find task
        task = next((t for t in data['tasks'] if t['id'] == task_id), None)
        if not task:
            return jsonify({"error": "Task not found"}), 404
        
        # Update task
        task.update(task_updates)
        task['updated_at'] = datetime.now().isoformat()
        
        save_data(data)
        return jsonify({"success": True, "task": task})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a specific task"""
    try:
        data = load_data()
        
        # Find and remove task
        original_count = len(data['tasks'])
        data['tasks'] = [t for t in data['tasks'] if t['id'] != task_id]
        
        if len(data['tasks']) == original_count:
            return jsonify({"error": "Task not found"}), 404
        
        save_data(data)
        return jsonify({"success": True, "message": "Task deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/projects', methods=['GET'])
def get_projects():
    """Get all projects"""
    data = load_data()
    return jsonify(data.get('projects', {}))

@app.route('/api/projects', methods=['POST'])
def create_project():
    """Create a new project"""
    try:
        data = load_data()
        project = request.get_json()
        
        if not project or 'key' not in project:
            return jsonify({"error": "Project key required"}), 400
        
        project_key = project['key']
        if project_key in data['projects']:
            return jsonify({"error": "Project already exists"}), 409
        
        data['projects'][project_key] = {
            'name': project.get('name', project_key),
            'description': project.get('description', ''),
            'status': 'active',
            'created_at': datetime.now().isoformat(),
            'environments': project.get('environments', {})
        }
        
        save_data(data)
        return jsonify({"success": True, "project": data['projects'][project_key]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/agents', methods=['GET'])
def get_agents():
    """Get all agents"""
    data = load_data()
    return jsonify(data.get('agents', {}))

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get taskboard statistics"""
    data = load_data()
    project = request.args.get('project')
    
    tasks = data.get('tasks', [])
    if project:
        tasks = [t for t in tasks if t.get('project') == project]
    
    stats = {
        'total': len(tasks),
        'by_status': {},
        'by_agent': {},
        'blocked': 0
    }
    
    for task in tasks:
        status = task.get('status', 'unknown')
        stats['by_status'][status] = stats['by_status'].get(status, 0) + 1
        
        agent = task.get('agent', 'unassigned')
        stats['by_agent'][agent] = stats['by_agent'].get(agent, 0) + 1
        
        # Check if blocked by dependencies
        deps = task.get('dependencies', [])
        if deps:
            blocked = False
            for dep_id in deps:
                dep_task = next((t for t in data['tasks'] if t['id'] == dep_id), None)
                if dep_task and dep_task.get('status') != 'done':
                    blocked = True
                    break
            if blocked:
                stats['blocked'] += 1
    
    return jsonify(stats)

@app.route('/api/backups', methods=['GET'])
def get_backups():
    """List all available backups"""
    try:
        backups = []
        for filename in os.listdir(BACKUP_DIR):
            if filename.startswith('data_backup_') and filename.endswith('.json'):
                filepath = os.path.join(BACKUP_DIR, filename)
                stat = os.stat(filepath)
                backups.append({
                    'filename': filename,
                    'created': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    'size': stat.st_size
                })
        
        backups.sort(key=lambda x: x['created'], reverse=True)
        return jsonify(backups)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/backups/<filename>', methods=['POST'])
def restore_backup(filename):
    """Restore from a backup"""
    try:
        backup_path = os.path.join(BACKUP_DIR, filename)
        if not os.path.exists(backup_path):
            return jsonify({"error": "Backup not found"}), 404
        
        # Load backup data
        with open(backup_path, 'r') as f:
            backup_data = json.load(f)
        
        # Save as current data
        save_data(backup_data)
        return jsonify({"success": True, "message": "Backup restored"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Taskboard Backend starting...")
    print(f"📁 Data file: {DATA_FILE}")
    print(f"💾 Backup dir: {BACKUP_DIR}")
    print("🌐 API available at: http://localhost:5000")
    print("")
    print("Endpoints:")
    print("  GET  /api/data          - Get all data")
    print("  POST /api/data          - Save all data")
    print("  GET  /api/tasks         - Get tasks")
    print("  POST /api/tasks         - Create task")
    print("  PUT  /api/tasks/<id>    - Update task")
    print("  DEL  /api/tasks/<id>    - Delete task")
    print("  GET  /api/projects      - Get projects")
    print("  POST /api/projects      - Create project")
    print("  GET  /api/agents        - Get agents")
    print("  GET  /api/stats         - Get statistics")
    print("  GET  /api/backups       - List backups")
    print("  POST /webhook/<agent>   - Telegram webhooks")
    print("")
    
    # Start task monitor in background thread
    from task_monitor import start_monitor
    monitor_thread = threading.Thread(target=start_monitor, daemon=True)
    monitor_thread.start()
    print("🔔 Task monitor started (checking every 5 seconds)")
    print("")
    
    app.run(host='0.0.0.0', port=5000, debug=True)