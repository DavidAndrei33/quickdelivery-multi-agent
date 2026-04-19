/**
 * Dashboard v2.0 - Main Controller
 * Queue + Journal + WebSocket Integration
 */

class TradingDashboard {
    constructor() {
        this.connected = false;
        this.ws = null;
        this.reconnectInterval = null;
        this.stats = {
            pending: 0,
            executed: 0,
            failed: 0
        };
        
        this.init();
    }
    
    init() {
        this.cacheElements();
        this.attachEventListeners();
        this.log('Dashboard v2.0 initialized', 'info');
        
        // Auto-connect on load
        setTimeout(() => this.connect(), 500);
    }
    
    cacheElements() {
        this.connectionStatus = document.getElementById('connectionStatus');
        this.activityLog = document.getElementById('activityLog');
        this.pendingCount = document.getElementById('pendingCount');
        this.executedCount = document.getElementById('executedCount');
        this.failedCount = document.getElementById('failedCount');
    }
    
    attachEventListeners() {
        document.getElementById('connectBtn')?.addEventListener('click', () => this.connect());
        document.getElementById('refreshBtn')?.addEventListener('click', () => this.refreshStats());
    }
    
    connect() {
        if (this.ws?.readyState === WebSocket.OPEN) {
            this.log('Already connected', 'info');
            return;
        }
        
        try {
            this.ws = new WebSocket('ws://localhost:8001');
            
            this.ws.onopen = () => {
                this.connected = true;
                this.updateConnectionStatus(true);
                this.log('Connected to MT5 Server', 'success');
                this.clearReconnectInterval();
            };
            
            this.ws.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this.handleMessage(data);
                } catch (error) {
                    this.log('Invalid message format: ' + error.message, 'error');
                }
            };
            
            this.ws.onerror = (error) => {
                this.log('WebSocket error', 'error');
            };
            
            this.ws.onclose = () => {
                this.connected = false;
                this.updateConnectionStatus(false);
                this.log('Disconnected from MT5 Server', 'info');
                this.scheduleReconnect();
            };
        } catch (error) {
            this.log('Connection failed: ' + error.message, 'error');
        }
    }
    
    disconnect() {
        if (this.ws) {
            this.ws.close();
        }
        this.clearReconnectInterval();
    }
    
    scheduleReconnect() {
        if (this.reconnectInterval) return;
        
        this.reconnectInterval = setInterval(() => {
            if (!this.connected) {
                this.log('Attempting to reconnect...', 'info');
                this.connect();
            }
        }, 5000);
    }
    
    clearReconnectInterval() {
        if (this.reconnectInterval) {
            clearInterval(this.reconnectInterval);
            this.reconnectInterval = null;
        }
    }
    
    handleMessage(data) {
        switch (data.type) {
            case 'prices':
                this.updatePrices(data.prices);
                break;
            case 'stats':
                this.updateStats(data.stats);
                break;
            case 'log':
                this.log(data.message, data.level);
                break;
            case 'queue_update':
                this.updateQueueStats(data.queue);
                break;
            default:
                this.log(`Received: ${JSON.stringify(data).substring(0, 100)}`, 'info');
        }
    }
    
    updatePrices(prices) {
        // Update price displays if needed
        console.log('Prices updated:', prices);
    }
    
    updateStats(stats) {
        if (stats.pending !== undefined) {
            this.stats.pending = stats.pending;
            this.pendingCount.textContent = stats.pending;
        }
        if (stats.executed !== undefined) {
            this.stats.executed = stats.executed;
            this.executedCount.textContent = stats.executed;
        }
        if (stats.failed !== undefined) {
            this.stats.failed = stats.failed;
            this.failedCount.textContent = stats.failed;
        }
    }
    
    updateQueueStats(queue) {
        this.stats.pending = queue.pending || 0;
        this.stats.executed = queue.executed || 0;
        this.stats.failed = queue.failed || 0;
        
        this.pendingCount.textContent = this.stats.pending;
        this.executedCount.textContent = this.stats.executed;
        this.failedCount.textContent = this.stats.failed;
    }
    
    refreshStats() {
        fetch('http://localhost:8002/api/health')
            .then(response => response.json())
            .then(data => {
                this.log('Stats refreshed', 'success');
                if (data.stats) {
                    this.updateStats(data.stats);
                }
            })
            .catch(error => {
                this.log('Failed to refresh stats: ' + error.message, 'error');
            });
    }
    
    updateConnectionStatus(connected) {
        if (this.connectionStatus) {
            this.connectionStatus.textContent = connected ? 'Connected' : 'Disconnected';
            this.connectionStatus.classList.toggle('connected', connected);
        }
    }
    
    log(message, type = 'info') {
        const entry = document.createElement('div');
        entry.className = `log-entry ${type}`;
        entry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
        this.activityLog?.appendChild(entry);
        this.activityLog?.scrollTo(0, this.activityLog.scrollHeight);
        
        // Keep only last 100 entries
        while (this.activityLog?.children.length > 100) {
            this.activityLog.removeChild(this.activityLog.firstChild);
        }
    }
}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new TradingDashboard();
});
