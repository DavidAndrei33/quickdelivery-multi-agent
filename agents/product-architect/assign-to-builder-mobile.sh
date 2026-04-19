#!/bin/bash
# Script pentru Product-Architect să assign-eze task-uri către Builder-Mobile
# Usage: assign-to-builder-mobile <task-id> <title> <description> <priority>

TASK_ID=$1
TITLE=$2
DESCRIPTION=$3
PRIORITY=${4:-medium}
AGENT="builder-mobile"
PORT=18795
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
curl -s -X POST http://localhost:$PORT/task-assigned \
  -H "Content-Type: application/json" \
  -d "{\"taskId\":\"$TASK_ID\",\"dropFile\":\"$DROP_DIR/$TASK_ID.json\"}"

echo "🚀 Trigger trimis către Builder-Mobile via port $PORT"