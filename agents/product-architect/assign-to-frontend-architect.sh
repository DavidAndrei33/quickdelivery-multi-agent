#!/bin/bash
# Script pentru Product-Architect să assign-eze task-uri către Frontend-Architect
# Usage: assign-to-frontend-architect <task-id> <title> <description> <priority>

TASK_ID=$1
TITLE=$2
DESCRIPTION=$3
PRIORITY=${4:-medium}
AGENT="frontend-architect"
PORT=18792
DROP_DIR="/workspace/shared/.task-drops/${AGENT}"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Creează directorul dacă nu există
mkdir -p "$DROP_DIR"

# Creează fișierul task
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

# Trigger hook către agent
curl -s -X POST http://localhost:$PORT/task-assigned \
  -H "Content-Type: application/json" \
  -d "{\"taskId\":\"$TASK_ID\",\"dropFile\":\"$DROP_DIR/$TASK_ID.json\"}"

echo "🚀 Trigger trimis către Frontend-Architect via port $PORT"