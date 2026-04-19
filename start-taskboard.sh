#!/bin/bash
cd /workspace/shared
python3 -m http.server 8080 &
echo "Server started on port 8080"
echo "PID: $!"