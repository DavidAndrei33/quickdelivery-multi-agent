#!/bin/bash
# Script pentru Product-Architect să assign-eze task-uri către Specialists-All
# Usage: assign-to-specialists-all <task-id> <title> <description> <priority>

TASK_ID=$1
TITLE=$2
DESCRIPTION=$3
PRIORITY=${4:-medium}
AGENT="specialists-all"
# Specialists-All nu are port HTTP, folosește doar file drop + heartbeat
DROP_DIR="/workspace/shared/.task-drops/${AGENT}"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

mkdir -p "$DROP_DIR"

cat > "$DROP_DIR/$TASK_ID.json" << EOF
{
  "id": "$TASK_ID",
  "title": "$TITLE",
  "description": "$DESCRIPTION",
  "priority": "$PRIORITY",
  "assignedBy": "product-architect",
  "assignedTo": "$AGENT",
  "assignedAt": "$TIMESTAMP",
  "status": "pending"
}
EOF

echo "✅ Task $TASK_ID creat în $DROP_DIR"
echo "📝 Specialists-All va prelua task-ul la următorul heartbeat (max 5 minute)"
echo "💡 Notificare: Agentul va raporta automat către Andrei când începe execuția"