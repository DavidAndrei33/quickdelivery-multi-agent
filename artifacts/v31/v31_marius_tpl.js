/**
 * V31 Marius TPL - Main JavaScript
 * Trading Dashboard Controller
 */

class V31MariusDashboard {
    constructor() {
        this.connected = false;
        this.ws = null;
        this.symbols = [];
        this.gridContainer = document.getElementById('gridContainer');
        this.activityLog = document.getElementById('activityLog');
        this.connectionStatus = document.getElementById('connectionStatus');
        
        this.init();
    }
    
    init() {
        this.loadSymbolGrid();
        this.attachEventListeners();
        this.log('V31 Marius TPL Dashboard initialized', 'info');
    }
    
    attachEventListeners() {
        document.getElementById('connectBtn')?.addEventListener('click', () => this.connect());
        document.getElementById('disconnectBtn')?.addEventListener('click', () => this.disconnect());
    }
    
    loadSymbolGrid() {
        // Load symbol grid connector
        if (typeof SymbolGridConnector !== 'undefined') {
            this.connector = new SymbolGridConnector();
            this.symbols = this.connector.getSymbols ? this.connector.getSymbols() : [];
            this.renderGrid();
        } else {
            // Default symbols
            this.symbols = ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'USDCAD'];
            this.renderGrid();
        }
    }
    
    renderGrid() {
        if (!this.gridContainer) return;
        
        this.gridContainer.innerHTML = this.symbols.map(symbol => `
            <div class="symbol-card" data-symbol="${symbol}">
                <h3>${symbol}</h3>
                <div class="price">--</div>
                <div class="signal">--</div>
            </div>
        `).join('');
    }
    
    connect() {
        try {
            this.ws = new WebSocket('ws://localhost:8001');
            
            this.ws.onopen = () => {
                this.connected = true;
                this.updateConnectionStatus(true);
                this.log('Connected to MT5 Server', 'success');
            };
            
            this.ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                this.handleMessage(data);
            };
            
            this.ws.onerror = (error) => {
                this.log('WebSocket error: ' + error, 'error');
            };
            
            this.ws.onclose = () => {
                this.connected = false;
                this.updateConnectionStatus(false);
                this.log('Disconnected from MT5 Server', 'info');
            };
        } catch (error) {
            this.log('Connection failed: ' + error.message, 'error');
        }
    }
    
    disconnect() {
        if (this.ws) {
            this.ws.close();
        }
    }
    
    handleMessage(data) {
        if (data.type === 'prices') {
            this.updatePrices(data.prices);
        } else if (data.type === 'signal') {
            this.updateSignal(data.symbol, data.signal);
        }
    }
    
    updatePrices(prices) {
        Object.entries(prices).forEach(([symbol, price]) => {
            const card = this.gridContainer?.querySelector(`[data-symbol="${symbol}"]`);
            if (card) {
                card.querySelector('.price').textContent = price.bid;
            }
        });
    }
    
    updateSignal(symbol, signal) {
        const card = this.gridContainer?.querySelector(`[data-symbol="${symbol}"]`);
        if (card) {
            card.querySelector('.signal').textContent = signal;
            card.classList.toggle('active', signal === 'BUY' || signal === 'SELL');
        }
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
    }
}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', () => {
    window.v31Dashboard = new V31MariusDashboard();
});

// Include the symbol grid connector
