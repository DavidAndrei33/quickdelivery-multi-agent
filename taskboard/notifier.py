#!/usr/bin/env python3
"""
Telegram Notifier for Taskboard
Sends DM notifications to agents when tasks are assigned
"""

import requests
import json
import os
from datetime import datetime

# Bot tokens for each agent (from existing configuration)
AGENT_BOTS = {
    'product-architect': os.getenv('PRODUCT_ARCHITECT_BOT_TOKEN', ''),
    'backend-architect': os.getenv('BACKEND_ARCHITECT_BOT_TOKEN', ''),
    'frontend-architect': os.getenv('FRONTEND_ARCHITECT_BOT_TOKEN', ''),
    'builder-modules': os.getenv('BUILDER_MODULES_BOT_TOKEN', ''),
    'builder-mobile': os.getenv('BUILDER_MOBILE_BOT_TOKEN', ''),
    'reviewer-all': os.getenv('REVIEWER_ALL_BOT_TOKEN', ''),
    'operations-all': os.getenv('OPERATIONS_ALL_BOT_TOKEN', ''),
    'specialists-all': os.getenv('SPECIALISTS_ALL_BOT_TOKEN', '')
}

# Owner Telegram ID for notifications
OWNER_CHAT_ID = os.getenv('OWNER_CHAT_ID', '310970306')

# Webhook URL for callbacks
WEBHOOK_BASE_URL = os.getenv('WEBHOOK_BASE_URL', 'https://your-domain.com/webhook')

class TelegramNotifier:
    def __init__(self):
        self.api_base = "https://api.telegram.org/bot{token}"
    
    def notify_owner_task_seen(self, agent_key, task):
        """Notify owner that agent has seen the task"""
        token = AGENT_BOTS.get(agent_key)
        if not token:
            print(f"❌ No bot token for agent: {agent_key}")
            return False
        
        agent_info = self._get_agent_info(agent_key)
        message = f"""👁️ *Task Seen*

Agent: {agent_info['emoji']} {agent_info['name']}
Task: {task['id']} - {task['title']}
Project: {task.get('project', 'N/A')}

Agent has seen the assigned task."""
        
        return self._send_simple_message(token, OWNER_CHAT_ID, message)
    
    def notify_owner_task_started(self, agent_key, task):
        """Notify owner that agent has started working"""
        token = AGENT_BOTS.get(agent_key)
        if not token:
            return False
        
        agent_info = self._get_agent_info(agent_key)
        message = f"""🚀 *Task Started*

Agent: {agent_info['emoji']} {agent_info['name']}
Task: {task['id']} - {task['title']}
Project: {task.get('project', 'N/A')}

Agent has started working on this task."""
        
        return self._send_simple_message(token, OWNER_CHAT_ID, message)
    
    def notify_owner_task_completed(self, agent_key, task):
        """Notify owner that agent has completed the task"""
        token = AGENT_BOTS.get(agent_key)
        if not token:
            return False
        
        agent_info = self._get_agent_info(agent_key)
        message = f"""✅ *Task Completed*

Agent: {agent_info['emoji']} {agent_info['name']}
Task: {task['id']} - {task['title']}
Project: {task.get('project', 'N/A')}

Agent has completed the task and is waiting for review."""
        
        return self._send_simple_message(token, OWNER_CHAT_ID, message)
    
    def send_task_to_agent(self, agent_key, task):
        """Send task notification to agent (they will report to owner manually)"""
        token = AGENT_BOTS.get(agent_key)
        if not token:
            print(f"❌ No bot token for agent: {agent_key}")
            return False
        
        # Get agent chat ID - try to get from task or use a default
        # For now, we'll need to discover this when agent first interacts
        # or store it in a separate file
        agent_chat_id = self._get_agent_chat_id(agent_key)
        
        agent_info = self._get_agent_info(agent_key)
        priority_emoji = {
            'critical': '🔴',
            'high': '🟠',
            'medium': '🟡',
            'low': '🟢'
        }.get(task.get('priority', 'medium'), '🟡')
        
        description = task.get('description', 'No description')[:150]
        if len(task.get('description', '')) > 150:
            description += '...'
        
        message = f"""🎯 *New Task Assigned*

*{task['id']}*: {task['title']}

{priority_emoji} *Priority:* {task.get('priority', 'medium').upper()}
📋 *Description:* {description}

⚠️ *Action Required:*
Please report to @david3366:
1. When you see this task (reply: "seen")
2. When you start working (reply: "start")
3. When you complete it (reply: "done")

View full details in taskboard: http://localhost:5000"""
        
        return self._send_simple_message(token, agent_chat_id, message)
    
    def _get_agent_info(self, agent_key):
        """Get agent display info"""
        agents = {
            'product-architect': {'name': 'Product-Architect', 'emoji': '🎯'},
            'backend-architect': {'name': 'Backend-Architect', 'emoji': '⚙️'},
            'frontend-architect': {'name': 'Frontend-Architect', 'emoji': '🎨'},
            'builder-modules': {'name': 'Builder-Modules', 'emoji': '🛠️'},
            'builder-mobile': {'name': 'Builder-Mobile', 'emoji': '📱'},
            'reviewer-all': {'name': 'Reviewer-All', 'emoji': '👁️'},
            'operations-all': {'name': 'Operations-All', 'emoji': '🚀'},
            'specialists-all': {'name': 'Specialists-All', 'emoji': '🔬'}
        }
        return agents.get(agent_key, {'name': agent_key, 'emoji': '👤'})
    
    def _get_agent_chat_id(self, agent_key):
        """Get agent's Telegram chat ID from storage"""
        # Try to load from file
        try:
            chat_ids_file = os.path.join(os.path.dirname(__file__), '.agent_chat_ids.json')
            if os.path.exists(chat_ids_file):
                with open(chat_ids_file, 'r') as f:
                    chat_ids = json.load(f)
                    return chat_ids.get(agent_key, OWNER_CHAT_ID)  # Fallback to owner
        except:
            pass
        return OWNER_CHAT_ID  # Default to owner if not found
    
    def save_agent_chat_id(self, agent_key, chat_id):
        """Save agent's chat ID when they first interact"""
        try:
            chat_ids_file = os.path.join(os.path.dirname(__file__), '.agent_chat_ids.json')
            chat_ids = {}
            if os.path.exists(chat_ids_file):
                with open(chat_ids_file, 'r') as f:
                    chat_ids = json.load(f)
            chat_ids[agent_key] = chat_id
            with open(chat_ids_file, 'w') as f:
                json.dump(chat_ids, f)
        except Exception as e:
            print(f"❌ Error saving chat ID: {e}")
    
    def _send_message(self, token, chat_id, message, task_id):
        """Send message with inline keyboard"""
        url = f"{self.api_base.format(token=token)}/sendMessage"
        
        # Inline keyboard with actions
        keyboard = {
            "inline_keyboard": [
                [
                    {"text": "🔵 Start Task", "callback_data": f"start:{task_id}"},
                    {"text": "❌ Refuse", "callback_data": f"refuse:{task_id}"}
                ],
                [
                    {"text": "📊 View in Dashboard", "url": f"http://localhost:5000"}
                ]
            ]
        }
        
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown",
            "reply_markup": json.dumps(keyboard)
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                print(f"✅ Notification sent to {chat_id}")
                return True
            else:
                print(f"❌ Failed to send: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error sending notification: {e}")
            return False
    
    def _send_simple_message(self, token, chat_id, message):
        """Send simple message without keyboard"""
        url = f"{self.api_base.format(token=token)}/sendMessage"
        
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def answer_callback(self, token, callback_query_id, text=None):
        """Answer callback query (button press)"""
        url = f"{self.api_base.format(token=token)}/answerCallbackQuery"
        
        payload = {
            "callback_query_id": callback_query_id
        }
        if text:
            payload["text"] = text
            payload["show_alert"] = False
        
        try:
            requests.post(url, json=payload, timeout=5)
            return True
        except:
            return False

# Singleton instance
notifier = TelegramNotifier()

if __name__ == '__main__':
    # Test
    test_task = {
        'id': 'TASK-001',
        'title': 'Test Task',
        'description': 'This is a test notification',
        'priority': 'high',
        'project': 'quickdelivery',
        'agent_name': 'Backend-Architect',
        'agent_chat_id': OWNER_CHAT_ID  # Use owner for testing
    }
    
    print("Testing Telegram Notifier...")
    result = notifier.send_task_notification('backend-architect', test_task)
    print(f"Result: {result}")
