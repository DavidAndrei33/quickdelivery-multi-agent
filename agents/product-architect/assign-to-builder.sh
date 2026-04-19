#!/bin/bash
# Script pentru Product-Architect să assign-eze task-uri către Builder-Modules
# Usage: assign-to-builder <task-id> <title> <description> <priority>

TASK_ID=$1
TITLE=$2
DESCRIPTION=$3
PRIORITY=${4:-medium}

DROP_DIR="/workspace/shared/.task-drops/builder-modules"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Creează fișierul task
cat > "$DROP_DIR/$TASK_ID.json" << EOF
{
  "id": "$TASK_ID",
  "title": "$TITLE",
  "description": "$DESCRIPTION",
  "priority": "$PRIORITY",
  "assignedBy": "product-architect",
  "assignedTo": "builder-modules",
  "assignedAt": "$TIMESTAMP",
  "status": "pending"
}
EOF

echo "✅ Task $TASK_ID creat în $DROP_DIR"

# Trigger hook către main gateway (port 18788 - hook endpoint)
curl -s -X POST http://localhost:18788/task-to-builder-modules \
  -H "Content-Type: application/json" \
  -d "{\"taskId\":\"$TASK_ID\",\"dropFile\":\"$DROP_DIR/$TASK_ID.json\"}"

echo "🚀 Trigger trimis către Builder-Modules via hook (port 18788)"
