#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# AGENT AUTO-UPDATER SERVICE
# Rulează continuu pentru a monitoriza și updata statusul agenților
# ═══════════════════════════════════════════════════════════════════════════

PIDFILE="/var/run/agent_auto_updater.pid"
LOGFILE="/var/log/agent_auto_updater.log"
SCRIPT="/workspace/shared/agent_auto_updater.py"

start() {
    if [ -f "$PIDFILE" ]; then
        PID=$(cat "$PIDFILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            echo "Service already running (PID: $PID)"
            return 1
        fi
    fi
    
    echo "🚀 Starting Agent Auto-Updater..."
    nohup python3 "$SCRIPT" > "$LOGFILE" 2>&1 &
    echo $! > "$PIDFILE"
    echo "✅ Started with PID: $(cat "$PIDFILE")"
    echo "Logs: $LOGFILE"
}

stop() {
    if [ -f "$PIDFILE" ]; then
        PID=$(cat "$PIDFILE")
        echo "🛑 Stopping Agent Auto-Updater (PID: $PID)..."
        kill "$PID" 2>/dev/null && rm -f "$PIDFILE"
        echo "✅ Stopped"
    else
        echo "Service not running"
    fi
}

status() {
    if [ -f "$PIDFILE" ]; then
        PID=$(cat "$PIDFILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            echo "✅ Running (PID: $PID)"
            echo "Uptime: $(ps -o etime= -p "$PID")"
            echo "Recent logs:"
            tail -10 "$LOGFILE"
        else
            echo "❌ Not running (stale PID file)"
        fi
    else
        echo "❌ Not running"
    fi
}

restart() {
    stop
    sleep 2
    start
}

quick_scan() {
    echo "🔍 Running quick scan..."
    python3 "$SCRIPT" &
    sleep 5
    echo "✅ Quick scan complete"
}

case "${1:-start}" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    status)
        status
        ;;
    scan)
        quick_scan
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|scan}"
        exit 1
        ;;
esac
