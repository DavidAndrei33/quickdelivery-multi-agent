/**
 * ═══════════════════════════════════════════════════════════════════════════
 * TRADING DASHBOARD PRO - FINAL UI/UX IMPLEMENTATION
 * ═══════════════════════════════════════════════════════════════════════════
 * 
 * Features:
 * - LED Status Indicators with animations
 * - Tab Navigation with state persistence
 * - Robot Selector with icons and live status
 * - Error handling with auto-retry (max 3)
 * - WebSocket + Polling fallback
 * - Performance optimized (60 FPS target)
 * - Responsive design (mobile-first)
 */

// ═══════════════════════════════════════════════════════════════════════════
// CONFIGURATION
// ═══════════════════════════════════════════════════════════════════════════

const CONFIG = {
    API_BASE_URL: window.location.origin,
    WS_RECONNECT_ATTEMPTS: 3,
    WS_RECONNECT_DELAY: 2000,
    POLLING_INTERVAL: 1000,      // 1 second for real-time updates
    POLLING_FALLBACK_INTERVAL: 5000,  // 5s fallback
    DEBOUNCE_DELAY: 150,
    MAX_LOG_ENTRIES: 100,
    ANIMATION_FRAME_TARGET: 16,  // ~60 FPS
    RETRY_MAX_ATTEMPTS: 3,
    OFFLINE_THRESHOLD: 30000,    // 30 seconds to show offline
};

// ═══════════════════════════════════════════════════════════════════════════
// STATE MANAGEMENT
// ═══════════════════════════════════════════════════════════════════════════

const State = {
    currentRobot: 'v31',
    currentTab: 'overview',
    isConnected: true,
    isWebSocketActive: false,
    reconnectAttempts: 0,
    lastHeartbeat: Date.now(),
    robots: {
        v31: { name: 'V31 Marius TPL', icon: '🤖', status: 'running', lastSeen: Date.now() },
        v32: { name: 'V32 London Breakout', icon: '🌅', status: 'running', lastSeen: Date.now() },
        v33: { name: 'V33 NY Breakout', icon: '🗽', status: 'running', lastSeen: Date.now() }
    },
    stats: {
        balance: 0,
        profit: 0,
        winRate: 0,
        activeTrades: 0
    },
    logs: [],
    activeTrades: [],
    tradeHistory: [],
    settings: {
        updateInterval: 1000,
        notifications: true,
        theme: 'dark'
    }
};

// ═══════════════════════════════════════════════════════════════════════════
// UTILITY FUNCTIONS
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Debounce function for performance optimization
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Throttle function for scroll/resize events
 */
function throttle(func, limit) {
    let inThrottle;
    return function executedFunction(...args) {
        if (!inThrottle) {
            func(...args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

/**
 * Format currency
 */
function formatCurrency(value) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(value);
}

/**
 * Format percentage
 */
function formatPercent(value) {
    return `${value >= 0 ? '+' : ''}${value.toFixed(2)}%`;
}

/**
 * Format time ago
 */
function formatTimeAgo(timestamp) {
    const seconds = Math.floor((Date.now() - timestamp) / 1000);
    if (seconds < 60) return 'Just now';
    if (seconds < 3600) return `${Math.floor(seconds / 60)} min ago`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)} hours ago`;
    return `${Math.floor(seconds / 86400)} days ago`;
}

/**
 * Generate unique ID
 */
function generateId() {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

// ═══════════════════════════════════════════════════════════════════════════
// TOAST NOTIFICATION SYSTEM
// ═══════════════════════════════════════════════════════════════════════════

const Toast = {
    container: null,

    init() {
        this.container = document.getElementById('toastContainer');
    },

    show(message, type = 'info', duration = 4000) {
        if (!this.container) this.init();

        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        
        const icons = {
            success: 'check-circle',
            error: 'x-circle',
            warning: 'alert-triangle',
            info: 'info'
        };

        toast.innerHTML = `
            <i data-lucide="${icons[type]}" class="toast-icon"></i>
            <div class="toast-content">
                <div class="toast-title">${type.charAt(0).toUpperCase() + type.slice(1)}</div>
                <div class="toast-message">${message}</div>
            </div>
            <button class="toast-close" onclick="this.parentElement.remove()">
                <i data-lucide="x" style="width: 14px; height: 14px;"></i>
            </button>
        `;

        this.container.appendChild(toast);
        lucide.createIcons();

        // Auto remove
        setTimeout(() => {
            toast.classList.add('toast-exit');
            setTimeout(() => toast.remove(), 300);
        }, duration);
    }
};

// ═══════════════════════════════════════════════════════════════════════════
// LOGGING SYSTEM
// ═══════════════════════════════════════════════════════════════════════════

const Logger = {
    terminal: null,

    init() {
        this.terminal = document.getElementById('logTerminal');
        this.info('Dashboard initialized');
    },

    add(level, message) {
        const timestamp = new Date().toLocaleTimeString();
        const entry = { id: generateId(), timestamp, level, message };
        
        State.logs.unshift(entry);
        if (State.logs.length > CONFIG.MAX_LOG_ENTRIES) {
            State.logs.pop();
        }

        this.render(entry);
    },

    render(entry) {
        if (!this.terminal) return;

        const div = document.createElement('div');
        div.className = 'log-entry';
        div.innerHTML = `
            <span class="log-timestamp">${entry.timestamp}</span>
            <span class="log-level ${entry.level}">${entry.level.toUpperCase()}</span>
            <span class="log-message">${entry.message}</span>
        `;

        this.terminal.insertBefore(div, this.terminal.firstChild);

        // Limit DOM elements
        while (this.terminal.children.length > CONFIG.MAX_LOG_ENTRIES) {
            this.terminal.lastChild.remove();
        }
    },

    info(message) { this.add('info', message); },
    success(message) { this.add('success', message); },
    warning(message) { this.add('warning', message); },
    error(message) { this.add('error', message); }
};

// ═══════════════════════════════════════════════════════════════════════════
// LED STATUS MANAGER
// ═══════════════════════════════════════════════════════════════════════════

const LEDManager = {
    update(elementId, status) {
        const element = typeof elementId === 'string' ? document.getElementById(elementId) : elementId;
        if (!element) return;

        // Remove all status classes
        element.classList.remove('running', 'stopped', 'warning', 'offline');
        
        // Add new status class
        element.classList.add(status);
    },

    updateRobotStatus(robotId, status) {
        // Update in dropdown
        const dropdown = document.getElementById('robotDropdown');
        const option = dropdown.querySelector(`[data-robot="${robotId}"]`);
        if (option) {
            const led = option.querySelector('.led-status');
            this.update(led, status);
        }

        // Update current if active
        if (State.currentRobot === robotId) {
            this.update('robotLed', status);
        }

        // Update state
        State.robots[robotId].status = status;
    },

    updateConnectionStatus(connected, isReconnecting = false) {
        const led = document.getElementById('connectionLed');
        const text = document.getElementById('connectionText');
        const container = document.getElementById('connectionStatus');

        if (isReconnecting) {
            this.update(led, 'warning');
            text.textContent = 'Reconectare...';
            container.classList.add('reconnecting');
            container.classList.remove('error');
        } else if (connected) {
            this.update(led, 'running');
            text.textContent = 'Conectat';
            container.classList.remove('reconnecting', 'error');
        } else {
            this.update(led, 'stopped');
            text.textContent = 'Deconectat';
            container.classList.add('error');
            container.classList.remove('reconnecting');
        }
    }
};

// ═══════════════════════════════════════════════════════════════════════════
// TAB NAVIGATION
// ═══════════════════════════════════════════════════════════════════════════

const TabManager = {
    init() {
        // Restore last active tab
        const savedTab = localStorage.getItem('dashboard_active_tab');
        if (savedTab) {
            this.switchTo(savedTab, false);
        }

        // Bind tab clicks
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.addEventListener('click', () => {
                const tabId = tab.dataset.tab;
                this.switchTo(tabId);
            });
        });
    },

    switchTo(tabId, saveState = true) {
        // Update nav tabs
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.classList.toggle('active', tab.dataset.tab === tabId);
        });

        // Update panels
        document.querySelectorAll('.tab-panel').forEach(panel => {
            panel.classList.toggle('active', panel.id === `tab-${tabId}`);
        });

        State.currentTab = tabId;

        // Save state
        if (saveState) {
            localStorage.setItem('dashboard_active_tab', tabId);
        }

        // Lazy load tab content
        this.loadTabContent(tabId);

        Logger.info(`Switched to ${tabId} tab`);
    },

    loadTabContent(tabId) {
        // Trigger specific loads based on tab
        switch(tabId) {
            case 'trades':
                DataManager.loadTrades();
                break;
            case 'logs':
                // Logs are real-time, no need to load
                break;
            case 'analysis':
                ChartManager.refresh();
                break;
        }
    }
};

// ═══════════════════════════════════════════════════════════════════════════
// ROBOT SELECTOR
// ═══════════════════════════════════════════════════════════════════════════

const RobotSelector = {
    dropdown: null,
    trigger: null,
    isOpen: false,

    init() {
        this.dropdown = document.getElementById('robotDropdown');
        this.trigger = document.getElementById('robotSelectorTrigger');

        // Toggle dropdown
        this.trigger.addEventListener('click', (e) => {
            e.stopPropagation();
            this.toggle();
        });

        // Select robot
        this.dropdown.querySelectorAll('.robot-option').forEach(option => {
            option.addEventListener('click', () => {
                const robotId = option.dataset.robot;
                const icon = option.dataset.icon;
                this.select(robotId, icon);
                this.close();
            });
        });

        // Close on outside click
        document.addEventListener('click', () => this.close());

        // Update status every second
        setInterval(() => this.updateStatuses(), 1000);
    },

    toggle() {
        this.isOpen = !this.isOpen;
        this.dropdown.classList.toggle('show', this.isOpen);
        this.trigger.classList.toggle('active', this.isOpen);
    },

    close() {
        this.isOpen = false;
        this.dropdown.classList.remove('show');
        this.trigger.classList.remove('active');
    },

    select(robotId, icon) {
        if (State.currentRobot === robotId) return;

        // Update UI
        document.getElementById('currentRobotIcon').textContent = icon;
        document.getElementById('currentRobotName').textContent = State.robots[robotId].name;

        // Update selection in dropdown
        this.dropdown.querySelectorAll('.robot-option').forEach(opt => {
            opt.classList.toggle('selected', opt.dataset.robot === robotId);
        });

        // Update state
        State.currentRobot = robotId;
        localStorage.setItem('dashboard_active_robot', robotId);

        // Load robot data
        DataManager.loadRobotData(robotId);

        Logger.info(`Selected robot: ${State.robots[robotId].name}`);
        Toast.show(`Switched to ${State.robots[robotId].name}`, 'info');
    },

    updateStatuses() {
        // Simulate status updates - in production this would come from API
        Object.keys(State.robots).forEach(robotId => {
            const robot = State.robots[robotId];
            const timeSinceLastSeen = Date.now() - robot.lastSeen;
            
            if (timeSinceLastSeen > CONFIG.OFFLINE_THRESHOLD) {
                LEDManager.updateRobotStatus(robotId, 'offline');
            }
        });

        // Update "Last seen" text if offline
        const currentRobot = State.robots[State.currentRobot];
        const statusText = document.getElementById('robotStatusText');
        
        if (currentRobot.status === 'offline') {
            statusText.textContent = `Offline - ${formatTimeAgo(currentRobot.lastSeen)}`;
        } else {
            statusText.textContent = currentRobot.status === 'running' ? 'Rulează' : 'Oprit';
        }
    }
};

// ═══════════════════════════════════════════════════════════════════════════
// ACCORDION MANAGER
// ═══════════════════════════════════════════════════════════════════════════

const AccordionManager = {
    init() {
        document.querySelectorAll('.accordion-header').forEach(header => {
            header.addEventListener('click', () => {
                const accordion = header.parentElement;
                accordion.classList.toggle('open');
            });
        });
    }
};

// ═══════════════════════════════════════════════════════════════════════════
// CONNECTION MANAGER (WebSocket + Polling)
// ═══════════════════════════════════════════════════════════════════════════

const ConnectionManager = {
    ws: null,
    pollingInterval: null,
    reconnectTimeout: null,
    isReconnecting: false,

    init() {
        this.connectWebSocket();
        
        // Start heartbeat check
        setInterval(() => this.checkHeartbeat(), 5000);
    },

    connectWebSocket() {
        try {
            const wsUrl = `ws://${window.location.host}/ws`;
            this.ws = new WebSocket(wsUrl);

            this.ws.onopen = () => {
                Logger.success('WebSocket connected');
                State.isWebSocketActive = true;
                State.isConnected = true;
                State.reconnectAttempts = 0;
                this.isReconnecting = false;
                LEDManager.updateConnectionStatus(true);
                this.stopPolling();
                this.hideOfflineOverlay();
            };

            this.ws.onmessage = (event) => {
                this.handleMessage(JSON.parse(event.data));
            };

            this.ws.onclose = () => {
                Logger.warning('WebSocket disconnected');
                State.isWebSocketActive = false;
                this.attemptReconnect();
            };

            this.ws.onerror = (error) => {
                Logger.error('WebSocket error');
                this.attemptReconnect();
            };
        } catch (error) {
            Logger.error('WebSocket connection failed');
            this.attemptReconnect();
        }
    },

    attemptReconnect() {
        if (this.isReconnecting) return;
        if (State.reconnectAttempts >= CONFIG.WS_RECONNECT_ATTEMPTS) {
            Logger.warning('Max reconnect attempts reached, falling back to polling');
            LEDManager.updateConnectionStatus(false, false);
            this.startPolling();
            this.showOfflineOverlay();
            return;
        }

        this.isReconnecting = true;
        State.reconnectAttempts++;
        
        LEDManager.updateConnectionStatus(false, true);
        Logger.info(`Reconnecting... attempt ${State.reconnectAttempts}/${CONFIG.WS_RECONNECT_ATTEMPTS}`);

        this.reconnectTimeout = setTimeout(() => {
            this.isReconnecting = false;
            this.connectWebSocket();
        }, CONFIG.WS_RECONNECT_DELAY);
    },

    startPolling() {
        if (this.pollingInterval) return;

        Logger.info('Starting polling fallback');
        this.pollingInterval = setInterval(() => {
            this.pollData();
        }, CONFIG.POLLING_INTERVAL);
    },

    stopPolling() {
        if (this.pollingInterval) {
            clearInterval(this.pollingInterval);
            this.pollingInterval = null;
        }
    },

    async pollData() {
        try {
            const response = await fetch(`${CONFIG.API_BASE_URL}/api/health`);
            if (response.ok) {
                State.lastHeartbeat = Date.now();
                State.isConnected = true;
                LEDManager.updateConnectionStatus(true);
                this.hideOfflineOverlay();
            }
        } catch (error) {
            State.isConnected = false;
            LEDManager.updateConnectionStatus(false);
        }
    },

    handleMessage(data) {
        State.lastHeartbeat = Date.now();
        
        switch(data.type) {
            case 'status':
                this.updateRobotStatus(data.robot, data.status);
                break;
            case 'trade':
                DataManager.handleTradeUpdate(data);
                break;
            case 'stats':
                DataManager.updateStats(data.stats);
                break;
            case 'log':
                Logger.add(data.level, data.message);
                break;
        }
    },

    updateRobotStatus(robotId, status) {
        if (State.robots[robotId]) {
            State.robots[robotId].status = status;
            State.robots[robotId].lastSeen = Date.now();
            LEDManager.updateRobotStatus(robotId, status);
        }
    },

    checkHeartbeat() {
        const timeSinceLastHeartbeat = Date.now() - State.lastHeartbeat;
        
        if (timeSinceLastHeartbeat > CONFIG.OFFLINE_THRESHOLD) {
            State.isConnected = false;
            LEDManager.updateConnectionStatus(false);
            
            if (!State.isWebSocketActive && !this.pollingInterval) {
                this.startPolling();
            }
        }
    },

    showOfflineOverlay() {
        const overlay = document.getElementById('offlineOverlay');
        const retryCount = document.getElementById('retryCount');
        
        retryCount.textContent = State.reconnectAttempts;
        overlay.classList.add('show');
    },

    hideOfflineOverlay() {
        const overlay = document.getElementById('offlineOverlay');
        overlay.classList.remove('show');
    }
};

// ═══════════════════════════════════════════════════════════════════════════
// DATA MANAGER
// ═══════════════════════════════════════════════════════════════════════════

const DataManager = {
    async loadRobotData(robotId) {
        try {
            // Simulate API call - replace with actual endpoint
            const response = await fetch(`${CONFIG.API_BASE_URL}/api/${robotId}/status`);
            if (!response.ok) throw new Error('Failed to load robot data');
            
            const data = await response.json();
            this.updateStats(data.stats);
            this.updateUI(data);
        } catch (error) {
            Logger.error(`Failed to load ${robotId} data: ${error.message}`);
            // Use cached data or defaults
            this.updateUI(this.getDefaultData(robotId));
        }
    },

    async loadTrades() {
        try {
            const response = await fetch(`${CONFIG.API_BASE_URL}/api/${State.currentRobot}/trades`);
            if (!response.ok) throw new Error('Failed to load trades');
            
            const data = await response.json();
            this.renderTrades(data.active || []);
            this.renderTradeHistory(data.history || []);
        } catch (error) {
            Logger.error('Failed to load trades');
        }
    },

    updateStats(stats) {
        if (!stats) return;
        
        Object.assign(State.stats, stats);
        
        // Update UI
        document.getElementById('statBalance').textContent = formatCurrency(stats.balance || 0);
        document.getElementById('statProfit').textContent = formatCurrency(stats.profit || 0);
        document.getElementById('statWinRate').textContent = `${stats.winRate || 0}%`;
        document.getElementById('statActive').textContent = stats.activeTrades || 0;
        
        // Update badges
        document.getElementById('tradesBadge').textContent = stats.activeTrades || 0;
    },

    updateUI(data) {
        // Update progress
        if (data.progress !== undefined) {
            document.getElementById('progressText').textContent = `${data.progress}%`;
            document.getElementById('progressBar').style.width = `${data.progress}%`;
        }

        // Update status badge
        const badge = document.getElementById('robotStatusBadge');
        if (data.status) {
            badge.textContent = data.status.toUpperCase();
            badge.className = `badge badge-${data.status === 'active' ? 'success' : 'warning'}`;
        }

        // Update last update time
        document.getElementById('lastUpdate').textContent = 'Just now';
    },

    handleTradeUpdate(data) {
        if (data.action === 'open') {
            State.activeTrades.push(data.trade);
            Toast.show(`New trade opened: ${data.trade.symbol}`, 'success');
        } else if (data.action === 'close') {
            State.activeTrades = State.activeTrades.filter(t => t.id !== data.trade.id);
            State.tradeHistory.unshift(data.trade);
            const profit = data.trade.profit;
            Toast.show(
                `Trade closed: ${profit >= 0 ? '+' : ''}${formatCurrency(profit)}`,
                profit >= 0 ? 'success' : 'error'
            );
        }
        
        this.renderTrades(State.activeTrades);
        this.renderTradeHistory(State.tradeHistory);
    },

    renderTrades(trades) {
        const tbody = document.getElementById('activeTradesBody');
        if (!tbody) return;

        if (trades.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="6" class="text-center text-muted" style="padding: 24px;">
                        No active trades
                    </td>
                </tr>
            `;
            return;
        }

        tbody.innerHTML = trades.map(trade => `
            <tr>
                <td><strong>${trade.symbol}</strong></td>
                <td><span class="badge badge-${trade.type === 'buy' ? 'success' : 'danger'}">${trade.type.toUpperCase()}</span></td>
                <td>${trade.entryPrice}</td>
                <td>${trade.currentPrice || '-'}</td>
                <td class="${trade.profit >= 0 ? 'text-success' : 'text-danger'}">
                    ${trade.profit >= 0 ? '+' : ''}${formatCurrency(trade.profit || 0)}
                </td>
                <td>
                    <button class="btn btn-danger btn-sm" onclick="closeTrade('${trade.id}')">Close</button>
                </td>
            </tr>
        `).join('');
    },

    renderTradeHistory(history) {
        const tbody = document.getElementById('tradeHistoryBody');
        if (!tbody) return;

        if (history.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="5" class="text-center text-muted" style="padding: 24px;">
                        No trade history
                    </td>
                </tr>
            `;
            return;
        }

        tbody.innerHTML = history.slice(0, 50).map(trade => `
            <tr>
                <td>${new Date(trade.time).toLocaleTimeString()}</td>
                <td><strong>${trade.symbol}</strong></td>
                <td><span class="badge badge-${trade.type === 'buy' ? 'success' : 'danger'}">${trade.type.toUpperCase()}</span></td>
                <td><span class="badge badge-${trade.result === 'win' ? 'success' : 'danger'}">${trade.result.toUpperCase()}</span></td>
                <td class="${trade.profit >= 0 ? 'text-success' : 'text-danger'}">
                    ${trade.profit >= 0 ? '+' : ''}${formatCurrency(trade.profit)}
                </td>
            </tr>
        `).join('');
    },

    getDefaultData(robotId) {
        return {
            status: 'active',
            progress: 65,
            stats: {
                balance: 10000,
                profit: 0,
                winRate: 0,
                activeTrades: 0
            }
        };
    }
};

// ═══════════════════════════════════════════════════════════════════════════
// CHART MANAGER
// ═══════════════════════════════════════════════════════════════════════════

const ChartManager = {
    chart: null,

    init() {
        const ctx = document.getElementById('mainChart');
        if (!ctx) return;

        this.chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Balance',
                    data: [],
                    borderColor: '#06b6d4',
                    backgroundColor: 'rgba(6, 182, 212, 0.1)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        grid: {
                            color: 'rgba(255, 255, 255, 0.05)'
                        },
                        ticks: {
                            color: '#64748b'
                        }
                    },
                    y: {
                        grid: {
                            color: 'rgba(255, 255, 255, 0.05)'
                        },
                        ticks: {
                            color: '#64748b'
                        }
                    }
                }
            }
        });
    },

    refresh() {
        if (!this.chart) {
            this.init();
        }
        // Update with new data
    },

    update(data) {
        if (!this.chart) return;
        
        this.chart.data.labels = data.labels;
        this.chart.data.datasets[0].data = data.values;
        this.chart.update('none'); // 'none' mode for performance
    }
};

// ═══════════════════════════════════════════════════════════════════════════
// PERFORMANCE OPTIMIZATIONS
// ═══════════════════════════════════════════════════════════════════════════

const PerformanceManager = {
    init() {
        // Debounce scroll events
        window.addEventListener('scroll', debounce(() => {
            this.handleScroll();
        }, CONFIG.DEBOUNCE_DELAY));

        // Throttle resize events
        window.addEventListener('resize', throttle(() => {
            this.handleResize();
        }, 100));

        // Intersection Observer for lazy loading
        this.setupLazyLoading();
    },

    handleScroll() {
        // Implement scroll-based optimizations
    },

    handleResize() {
        // Handle responsive changes
        if (ChartManager.chart) {
            ChartManager.chart.resize();
        }
    },

    setupLazyLoading() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('loaded');
                }
            });
        }, { threshold: 0.1 });

        document.querySelectorAll('.lazy-load').forEach(el => {
            observer.observe(el);
        });
    },

    requestAnimationFrame(callback) {
        return requestAnimationFrame((timestamp) => {
            callback(timestamp);
        });
    }
};

// ═══════════════════════════════════════════════════════════════════════════
// SETTINGS MANAGER
// ═══════════════════════════════════════════════════════════════════════════

const SettingsManager = {
    init() {
        this.loadSettings();
        
        // Bind settings controls
        document.getElementById('updateInterval')?.addEventListener('change', (e) => {
            State.settings.updateInterval = parseInt(e.target.value);
            this.saveSettings();
        });
    },

    loadSettings() {
        const saved = localStorage.getItem('dashboard_settings');
        if (saved) {
            Object.assign(State.settings, JSON.parse(saved));
        }

        // Apply settings
        document.getElementById('updateInterval').value = State.settings.updateInterval;
    },

    saveSettings() {
        localStorage.setItem('dashboard_settings', JSON.stringify(State.settings));
        Toast.show('Settings saved', 'success');
    }
};

// ═══════════════════════════════════════════════════════════════════════════
// GLOBAL FUNCTIONS (for HTML onclick handlers)
// ═══════════════════════════════════════════════════════════════════════════

function closeTrade(tradeId) {
    Logger.info(`Closing trade: ${tradeId}`);
    // Implement close trade logic
    Toast.show('Trade close requested', 'info');
}

function clearLogs() {
    State.logs = [];
    document.getElementById('logTerminal').innerHTML = '';
    Logger.info('Logs cleared');
}

function downloadLogs() {
    const content = State.logs.map(l => `[${l.timestamp}] ${l.level.toUpperCase()}: ${l.message}`).join('\n');
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `trading-logs-${new Date().toISOString().split('T')[0]}.txt`;
    a.click();
    URL.revokeObjectURL(url);
    Toast.show('Logs downloaded', 'success');
}

function toggleNotifications() {
    State.settings.notifications = !State.settings.notifications;
    document.getElementById('notifToggle').textContent = State.settings.notifications ? 'On' : 'Off';
    SettingsManager.saveSettings();
}

// ═══════════════════════════════════════════════════════════════════════════
// INITIALIZATION
// ═══════════════════════════════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {
    // Initialize Lucide icons
    lucide.createIcons();

    // Initialize all managers
    Logger.init();
    Toast.init();
    TabManager.init();
    RobotSelector.init();
    AccordionManager.init();
    ConnectionManager.init();
    PerformanceManager.init();
    SettingsManager.init();

    // Load initial data
    const savedRobot = localStorage.getItem('dashboard_active_robot') || 'v31';
    RobotSelector.select(savedRobot, State.robots[savedRobot].icon);

    // Simulate some initial logs
    Logger.success('Dashboard loaded successfully');
    Logger.info('WebSocket connecting...');

    // Refresh icons periodically for dynamic content
    setInterval(() => {
        lucide.createIcons();
    }, 5000);

    console.log('🚀 Trading Dashboard Pro initialized');
});

// Expose state for debugging
window.DashboardState = State;
window.DashboardConfig = CONFIG;
