#!/usr/bin/env python3
"""
Webhook Handler for Telegram Callbacks
Processes button presses from agents
"""

from flask import Blueprint, request, jsonify
import json
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from notifier import notifier, AGENT_BOTS

webhook_bp = Blueprint('webhook', __name__)

# Map agent keys to their bot tokens for verification
AGENT_BOT_MAP = {v: k for k, v in AGENT_BOTS.items() if v}

@webhook_bp.route('/webhook/<agent_key>', methods=['POST'])
def handle_webhook(agent_key):
    """Handle incoming webhook from Telegram"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data"}), 400
        
        # Check if it's a callback query (button press)
        if 'callback_query' in data:
            return handle_callback_query(data['callback_query'], agent_key)
        
        # Check if it's a message
        if 'message' in data:
            return handle_message(data['message'], agent_key)
        
        return jsonify({"status": "ignored"})
    
    except Exception as e:
        print(f"❌ Webhook error: {e}")
        return jsonify({"error": str(e)}), 500

def handle_callback_query(callback_query, agent_key):
    """Handle button press from inline keyboard"""
    try:
        callback_id = callback_query['id']
        callback_data = callback_query.get('data', '')
        chat_id = callback_query['message']['chat']['id']
        
        # Parse callback data (format: "action:task_id")
        if ':' not in callback_data:
            return jsonify({"error": "Invalid callback data"}), 400
        
        action, task_id = callback_data.split(':', 1)
        
        # Get agent token
        token = AGENT_BOTS.get(agent_key)
        if not token:
            return jsonify({"error": "Agent not found"}), 404
        
        # Answer callback (remove loading state)
        notifier.answer_callback(token, callback_id)
        
        # Process action
        if action == 'start':
            result = start_task(task_id, agent_key, chat_id)
        elif action == 'refuse':
            result = refuse_task(task_id, agent_key, chat_id)
        elif action == 'complete':
            result = complete_task(task_id, agent_key, chat_id)
        else:
            return jsonify({"error": "Unknown action"}), 400
        
        return jsonify({"status": "ok", "action": action, "task_id": task_id, "result": result})
    
    except Exception as e:
        print(f"❌ Callback error: {e}")
        return jsonify({"error": str(e)}), 500

def handle_message(message, agent_key):
    """Handle text message from agent"""
    try:
        text = message.get('text', '')
        chat_id = message['chat']['id']
        
        # Check for command patterns
        if text.startswith('/start'):
            # Format: /start TASK-001
            parts = text.split()
            if len(parts) >= 2:
                task_id = parts[1]
                result = start_task(task_id, agent_key, chat_id)
                return jsonify({"status": "ok", "command": "start", "task_id": task_id, "result": result})
        
        elif text.startswith('/done') or text.startswith('/complete'):
            # Format: /done TASK-001
            parts = text.split()
            if len(parts) >= 2:
                task_id = parts[1]
                result = complete_task(task_id, agent_key, chat_id)
                return jsonify({"status": "ok", "command": "complete", "task_id": task_id, "result": result})
        
        return jsonify({"status": "ignored", "message": "No command detected"})
    
    except Exception as e:
        print(f"❌ Message error: {e}")
        return jsonify({"error": str(e)}), 500

def start_task(task_id, agent_key, chat_id):
    """Update task status to in_progress"""
    try:
        # Import API functions
        from api import load_data, save_data
        
        data = load_data()
        
        # Find task
        task = next((t for t in data['tasks'] if t['id'] == task_id), None)
        if not task:
            return {"error": "Task not found"}
        
        # Check if assigned to this agent
        if task.get('agent') != agent_key:
            return {"error": "Task not assigned to this agent"}
        
        # Check dependencies
        deps = task.get('dependencies', [])
        blocked = False
        for dep_id in deps:
            dep_task = next((t for t in data['tasks'] if t['id'] == dep_id), None)
            if dep_task and dep_task.get('status') != 'done':
                blocked = True
                break
        
        if blocked:
            # Send message that task is blocked
            token = AGENT_BOTS.get(agent_key)
            if token:
                notifier._send_simple_message(
                    token, 
                    chat_id, 
                    f"⚠️ Task {task_id} is blocked by dependencies. Complete dependent tasks first."
                )
            return {"error": "Task blocked by dependencies"}
        
        # Update task
        task['status'] = 'in_progress'
        task['started_at'] = __import__('datetime').datetime.now().isoformat()
        task['agent_chat_id'] = chat_id
        
        save_data(data)
        
        # Send confirmation
        token = AGENT_BOTS.get(agent_key)
        if token:
            notifier._send_simple_message(
                token,
                chat_id,
                f"🚀 Task {task_id} started! Good luck! 💪"
            )
        
        print(f"✅ Task {task_id} started by {agent_key}")
        return {"success": True, "status": "in_progress"}
    
    except Exception as e:
        print(f"❌ Start task error: {e}")
        return {"error": str(e)}

def refuse_task(task_id, agent_key, chat_id):
    """Handle task refusal"""
    try:
        # Notify Product-Architect
        token = AGENT_BOTS.get('product-architect')
        if token:
            from notifier import OWNER_CHAT_ID
            notifier._send_simple_message(
                token,
                OWNER_CHAT_ID,
                f"⚠️ Agent {agent_key} refused task {task_id}. Please reassign."
            )
        
        return {"success": True, "action": "refused"}
    
    except Exception as e:
        print(f"❌ Refuse error: {e}")
        return {"error": str(e)}

def complete_task(task_id, agent_key, chat_id):
    """Update task status to done"""
    try:
        from api import load_data, save_data
        from notifier import OWNER_CHAT_ID
        
        data = load_data()
        
        # Find task
        task = next((t for t in data['tasks'] if t['id'] == task_id), None)
        if not task:
            return {"error": "Task not found"}
        
        # Update task
        task['status'] = 'done'
        task['progress'] = 100
        task['completed_at'] = __import__('datetime').datetime.now().isoformat()
        
        save_data(data)
        
        # Notify agent
        token = AGENT_BOTS.get(agent_key)
        if token:
            notifier._send_simple_message(
                token,
                chat_id,
                f"✅ Task {task_id} marked as complete! Great job! 🎉"
            )
        
        # Notify Product-Architect
        notifier.send_completion_notification(task, agent_key)
        
        print(f"✅ Task {task_id} completed by {agent_key}")
        return {"success": True, "status": "done"}
    
    except Exception as e:
        print(f"❌ Complete error: {e}")
        return {"error": str(e)}

if __name__ == '__main__':
    print("Webhook handler module loaded")
    print(f"Registered agents: {list(AGENT_BOTS.keys())}")
