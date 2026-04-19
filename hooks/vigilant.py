#!/usr/bin/env python3
"""
VIGILANT - File Watcher pentru Pipeline Automat de Testare
Rulează continuu și detectează modificări cod
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime
from pathlib import Path

# Configurare paths
sys.path.insert(0, '/workspace/shared/lib')

WATCHED_PATHS = [
    '/root/clawd/agents/brainmaker/dashboard/',
    '/root/clawd/agents/brainmaker/mt5_core_server.py',
    '/root/clawd/agents/brainmaker/v31_marius_tpl_robot.py',
    '/root/clawd/agents/brainmaker/v32_london_breakout_robot.py',
    '/root/clawd/agents/brainmaker/v33_ny_breakout_robot.py',
]

PIPELINE_STATE_FILE = '/workspace/shared/state/pipeline_state.json'
LOG_FILE = '/workspace/shared/logs/vigilant.log'

def log(message):
    """Log cu timestamp"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f"[{timestamp}] {message}"
    print(log_msg)
    
    # Salvează și în fișier
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, 'a') as f:
        f.write(log_msg + '\n')

def get_file_hash(filepath):
    """Get MD5 hash of file"""
    import hashlib
    try:
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None

def get_all_watched_files():
    """Get all files being watched with their hashes"""
    files = {}
    for path in WATCHED_PATHS:
        if os.path.isfile(path):
            files[path] = get_file_hash(path)
        elif os.path.isdir(path):
            for root, dirs, filenames in os.walk(path):
                # Exclude node_modules, .git, etc
                dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', '__pycache__']]
                for filename in filenames:
                    if filename.endswith(('.js', '.py', '.html', '.css', '.json')):
                        filepath = os.path.join(root, filename)
                        files[filepath] = get_file_hash(filepath)
    return files

def detect_change_type(filepath):
    """Detect what type of code changed"""
    if 'dashboard_functional.js' in filepath:
        return 'frontend_js'
    elif 'index.html' in filepath:
        return 'frontend_ui'
    elif 'mt5_core_server.py' in filepath:
        return 'backend_api'
    elif '_robot.py' in filepath:
        return 'robot_logic'
    elif '.css' in filepath:
        return 'frontend_css'
    else:
        return 'general'

def trigger_pipeline(change_type, changed_files):
    """Trigger testing pipeline"""
    log(f"🚀 TRIGGER: Detected {change_type} change in: {', '.join(changed_files)}")
    
    # Update pipeline state
    update_pipeline_state('TESTING', change_type, changed_files)
    
    # Spawn QA-Master for testing
    try:
        result = subprocess.run([
            'python3', '/workspace/shared/lib/spawn_qa_master.py',
            change_type,
            json.dumps(changed_files)
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            log(f"✅ QA-Master spawned successfully")
        else:
            log(f"❌ Failed to spawn QA-Master: {result.stderr}")
    except Exception as e:
        log(f"❌ Error spawning QA-Master: {e}")

def update_pipeline_state(status, change_type=None, files=None):
    """Update pipeline state file"""
    os.makedirs(os.path.dirname(PIPELINE_STATE_FILE), exist_ok=True)
    
    state = {
        'status': status,
        'last_change_type': change_type,
        'last_changed_files': files or [],
        'last_update': datetime.now().isoformat()
    }
    
    with open(PIPELINE_STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def load_previous_state():
    """Load previous file hashes"""
    state_file = '/workspace/shared/state/file_hashes.json'
    if os.path.exists(state_file):
        with open(state_file, 'r') as f:
            return json.load(f)
    return {}

def save_current_state(files):
    """Save current file hashes"""
    state_file = '/workspace/shared/state/file_hashes.json'
    os.makedirs(os.path.dirname(state_file), exist_ok=True)
    
    with open(state_file, 'w') as f:
        json.dump(files, f, indent=2)

def main_loop():
    """Main watching loop"""
    log("👁️ VIGILANT started - Watching for code changes...")
    log(f"   Watching {len(WATCHED_PATHS)} paths")
    
    # Load previous state
    previous_files = load_previous_state()
    
    # Initial scan
    current_files = get_all_watched_files()
    save_current_state(current_files)
    
    log(f"   Monitoring {len(current_files)} files")
    log("   Press Ctrl+C to stop\n")
    
    check_interval = 5  # seconds
    
    while True:
        try:
            time.sleep(check_interval)
            
            # Get current state
            current_files = get_all_watched_files()
            
            # Detect changes
            changed_files = []
            
            for filepath, current_hash in current_files.items():
                previous_hash = previous_files.get(filepath)
                
                if previous_hash is None:
                    # New file
                    log(f"📄 NEW FILE: {filepath}")
                    changed_files.append(filepath)
                elif previous_hash != current_hash:
                    # Modified file
                    log(f"✏️  MODIFIED: {filepath}")
                    changed_files.append(filepath)
            
            # Check for deleted files
            for filepath in previous_files:
                if filepath not in current_files:
                    log(f"🗑️  DELETED: {filepath}")
                    changed_files.append(filepath)
            
            # If changes detected, trigger pipeline
            if changed_files:
                # Determine change type from first changed file
                change_type = detect_change_type(changed_files[0])
                trigger_pipeline(change_type, changed_files)
                
                # Save new state
                save_current_state(current_files)
            
            # Update previous state for next iteration
            previous_files = current_files
            
        except KeyboardInterrupt:
            log("\n👋 VIGILANT stopped by user")
            break
        except Exception as e:
            log(f"❌ Error in main loop: {e}")
            time.sleep(10)  # Wait longer on error

if __name__ == '__main__':
    try:
        main_loop()
    except Exception as e:
        log(f"💥 Fatal error: {e}")
        sys.exit(1)
