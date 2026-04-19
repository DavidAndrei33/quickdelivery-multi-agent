#!/usr/bin/env python3
"""
File Lock Hook
Prevents concurrent modification of shared files
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

LOCKS_DIR = "/workspace/shared/.locks"

def get_lock_path(file_path):
    """Get lock file path for a given file."""
    # Create a safe lock filename from the path
    safe_name = file_path.replace('/', '_').replace('.', '_')
    return Path(LOCKS_DIR) / f"{safe_name}.lock"

def acquire_lock(file_path, agent_id, timeout_minutes=30):
    """Attempt to acquire lock on a file."""
    
    os.makedirs(LOCKS_DIR, exist_ok=True)
    lock_path = get_lock_path(file_path)
    
    # Check if lock exists
    if lock_path.exists():
        try:
            with open(lock_path) as f:
                lock_data = json.load(f)
            
            # Check if lock is stale
            locked_at = datetime.fromisoformat(lock_data['locked_at'])
            if datetime.utcnow() - locked_at > timedelta(minutes=timeout_minutes):
                print(f"[LOCK] Stale lock detected, breaking...")
                lock_path.unlink()
            else:
                print(f"[LOCK] File locked by {lock_data['agent_id']} since {lock_data['locked_at']}")
                return False
        except:
            # Corrupted lock file
            lock_path.unlink()
    
    # Acquire lock
    lock_data = {
        "agent_id": agent_id,
        "file_path": file_path,
        "locked_at": datetime.utcnow().isoformat(),
        "timeout_minutes": timeout_minutes
    }
    
    with open(lock_path, 'w') as f:
        json.dump(lock_data, f, indent=2)
    
    print(f"[LOCK] {agent_id} acquired lock on {file_path}")
    return True

def release_lock(file_path, agent_id):
    """Release lock on a file."""
    
    lock_path = get_lock_path(file_path)
    
    if not lock_path.exists():
        print(f"[LOCK] No lock found for {file_path}")
        return True
    
    try:
        with open(lock_path) as f:
            lock_data = json.load(f)
        
        if lock_data['agent_id'] != agent_id:
            print(f"[LOCK] Warning: {agent_id} trying to release lock owned by {lock_data['agent_id']}")
            return False
        
        lock_path.unlink()
        print(f"[LOCK] {agent_id} released lock on {file_path}")
        return True
    except Exception as e:
        print(f"[LOCK] Error releasing lock: {e}")
        return False

def check_lock(file_path):
    """Check if file is locked and by whom."""
    
    lock_path = get_lock_path(file_path)
    
    if not lock_path.exists():
        return None
    
    try:
        with open(lock_path) as f:
            lock_data = json.load(f)
        
        # Check if stale
        locked_at = datetime.fromisoformat(lock_data['locked_at'])
        timeout = timedelta(minutes=lock_data.get('timeout_minutes', 30))
        
        if datetime.utcnow() - locked_at > timeout:
            lock_path.unlink()
            return None
        
        return lock_data
    except:
        lock_path.unlink()
        return None

def list_active_locks():
    """List all active locks."""
    
    os.makedirs(LOCKS_DIR, exist_ok=True)
    
    locks = []
    for lock_file in Path(LOCKS_DIR).glob("*.lock"):
        try:
            with open(lock_file) as f:
                lock_data = json.load(f)
            
            # Check if stale
            locked_at = datetime.fromisoformat(lock_data['locked_at'])
            timeout = timedelta(minutes=lock_data.get('timeout_minutes', 30))
            
            if datetime.utcnow() - locked_at > timeout:
                lock_file.unlink()
                continue
            
            locks.append(lock_data)
        except:
            lock_file.unlink()
    
    if not locks:
        print("[LOCK] No active locks")
        return []
    
    print("\n🔒 ACTIVE LOCKS:")
    print("-" * 60)
    for lock in locks:
        print(f"{lock['agent_id']} → {lock['file_path']} (since {lock['locked_at']})")
    print("-" * 60 + "\n")
    
    return locks

def main():
    """Main hook execution."""
    
    import sys
    
    if len(sys.argv) < 2:
        list_active_locks()
        return
    
    command = sys.argv[1]
    
    if command == "acquire":
        file_path = sys.argv[2]
        agent_id = sys.argv[3]
        timeout = int(sys.argv[4]) if len(sys.argv) > 4 else 30
        success = acquire_lock(file_path, agent_id, timeout)
        sys.exit(0 if success else 1)
    
    elif command == "release":
        file_path = sys.argv[2]
        agent_id = sys.argv[3]
        release_lock(file_path, agent_id)
    
    elif command == "check":
        file_path = sys.argv[2]
        lock_info = check_lock(file_path)
        if lock_info:
            print(f"[LOCK] Locked by {lock_info['agent_id']}")
        else:
            print("[LOCK] Not locked")
    
    elif command == "list":
        list_active_locks()
    
    else:
        print(f"[LOCK] Unknown command: {command}")

if __name__ == "__main__":
    main()
