/**
 * V32 London Breakout - Opening Range Live Data Connector
 * Connects V32 Dashboard to LIVE MT5 data
 * 
 * Data sources (in priority order):
 * 1. API: /api/v32/symbol_status - Returns OR data from DB (when robot saves it)
 * 2. API: /prices/GBPUSD - Live current price from MT5
 * 3. API: /api/v32/session_status - Session phase and timing
 * 4. API: /api/robot_logs - Fallback for OR data from logs
 */

const V32Config = {
    symbol: 'GBPUSD',
    apiUrl: window.location.origin,
    refreshInterval: 1000, // 1 second refresh
    logRefreshInterval: 5000 // 5 seconds for logs
};

// State cache
let v32State = {
    orHigh: null,
    orLow: null,
    orRange: null,
    currentPrice: null,
    asiaHigh: null,
    asiaLow: null,
    asiaRange: null,
    sessionPhase: null,
    londonTime: null,
    breakoutDetected: false,
    breakoutDirection: null,
    signal: null,
    lastLogParse: 0
};

/**
 * Initialize V32 OR Live Data Connector
 */
function initV32ORConnector() {
    console.log('[V32-OR] Initializing Opening Range Live Data Connector...');
    
    // Start the update loops
    updateV32ORData();
    setInterval(updateV32ORData, V32Config.refreshInterval);
    
    // Log parsing for fallback
    parseV32LogsForOR();
    setInterval(parseV32LogsForOR, V32Config.logRefreshInterval);
}

/**
 * Main update function - fetches all data sources
 */
async function updateV32ORData() {
    try {
        // Fetch all data sources in parallel
        const [sessionData, symbolData, priceData] = await Promise.allSettled([
            fetchV32SessionStatus(),
            fetchV32SymbolStatus(),
            fetchV32CurrentPrice()
        ]);

        // Update session display
        if (sessionData.status === 'fulfilled' && sessionData.value) {
            updateV32SessionFromAPI(sessionData.value);
        }

        // Update OR data from symbol status (primary source)
        if (symbolData.status === 'fulfilled' && symbolData.value) {
            updateV32ORFromSymbolStatus(symbolData.value);
        }

        // Update current price
        if (priceData.status === 'fulfilled' && priceData.value) {
            updateV32PriceFromAPI(priceData.value);
        }

        // Update the DOM with all available data
        updateV32ORDOM();

    } catch (error) {
        console.error('[V32-OR] Error updating OR data:', error);
    }
}

/**
 * Fetch V32 session status from API
 */
async function fetchV32SessionStatus() {
    try {
        const response = await fetch(`${V32Config.apiUrl}/api/v32/session_status`);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return await response.json();
    } catch (error) {
        console.debug('[V32-OR] Session status fetch failed:', error.message);
        return null;
    }
}

/**
 * Fetch V32 symbol status from API
 */
async function fetchV32SymbolStatus() {
    try {
        const response = await fetch(`${V32Config.apiUrl}/api/v32/symbol_status`);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        if (data.status === 'success' && data.symbols) {
            // Find GBPUSD entry
            return data.symbols.find(s => s.symbol === V32Config.symbol) || data.symbols[0];
        }
        return null;
    } catch (error) {
        console.debug('[V32-OR] Symbol status fetch failed:', error.message);
        return null;
    }
}

/**
 * Fetch current price from MT5 via API
 */
async function fetchV32CurrentPrice() {
    try {
        const response = await fetch(`${V32Config.apiUrl}/prices/${V32Config.symbol}`);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return await response.json();
    } catch (error) {
        console.debug('[V32-OR] Price fetch failed:', error.message);
        return null;
    }
}

/**
 * Update session data from API response
 */
function updateV32SessionFromAPI(data) {
    if (!data) return;
    
    v32State.sessionPhase = data.session_phase;
    v32State.londonTime = data.london_time;
    v32State.isActive = data.is_active;
    v32State.timeRemaining = data.time_remaining_seconds;
    
    // Update session display elements
    const timeDisplay = document.getElementById('v32LondonTime');
    if (timeDisplay && data.london_time) {
        timeDisplay.textContent = data.london_time;
    }
    
    const phaseDisplay = document.getElementById('v32SessionPhase');
    if (phaseDisplay) {
        const phaseMap = {
            'BEFORE_SESSION': '⏳ Before Session (00:00-08:00)',
            'OPENING_RANGE': '📊 Opening Range (08:00-08:15)',
            'MAIN_SESSION': '🔥 Main Session (08:15-10:30)',
            'AFTER_SESSION': '⏹️ Session Ended'
        };
        phaseDisplay.textContent = phaseMap[data.session_phase] || data.session_phase;
    }
    
    const timerDisplay = document.getElementById('v32SessionTimer');
    if (timerDisplay && data.time_remaining_seconds !== undefined) {
        if (data.time_remaining_seconds > 0 && data.session_phase !== 'AFTER_SESSION') {
            const hours = Math.floor(data.time_remaining_seconds / 3600);
            const mins = Math.floor((data.time_remaining_seconds % 3600) / 60);
            const secs = data.time_remaining_seconds % 60;
            timerDisplay.textContent = hours > 0 
                ? `${hours}h ${mins}m ${secs}s` 
                : `${mins}m ${secs}s`;
        } else {
            timerDisplay.textContent = 'ENDED';
        }
    }
    
    const badgeEl = document.getElementById('v32SessionBadge');
    if (badgeEl) {
        if (data.is_active) {
            badgeEl.textContent = '🟢 Active';
            badgeEl.style.background = '#22c55e';
        } else if (data.session_phase === 'AFTER_SESSION') {
            badgeEl.textContent = '⏹️ Closed';
            badgeEl.style.background = '#64748b';
        } else {
            badgeEl.textContent = '⏳ Waiting';
            badgeEl.style.background = '#f59e0b';
        }
    }
}

/**
 * Update OR data from symbol status API (primary source)
 */
function updateV32ORFromSymbolStatus(data) {
    if (!data) return;
    
    // Only update if API has real data (not null)
    if (data.or_high !== null && data.or_high !== undefined) {
        v32State.orHigh = parseFloat(data.or_high);
    }
    if (data.or_low !== null && data.or_low !== undefined) {
        v32State.orLow = parseFloat(data.or_low);
    }
    if (data.or_range !== null && data.or_range !== undefined) {
        v32State.orRange = parseFloat(data.or_range);
    } else if (v32State.orHigh && v32State.orLow) {
        // Calculate range if not provided
        v32State.orRange = ((v32State.orHigh - v32State.orLow) * 10000).toFixed(1);
    }
    
    // Asia session data
    if (data.asia_high !== null && data.asia_high !== undefined) {
        v32State.asiaHigh = parseFloat(data.asia_high);
    }
    if (data.asia_low !== null && data.asia_low !== undefined) {
        v32State.asiaLow = parseFloat(data.asia_low);
    }
    if (data.asia_range !== null && data.asia_range !== undefined) {
        v32State.asiaRange = parseFloat(data.asia_range);
    }
    
    // Breakout status
    if (data.breakout_detected !== undefined) {
        v32State.breakoutDetected = data.breakout_detected;
    }
    if (data.breakout_direction) {
        v32State.breakoutDirection = data.breakout_direction;
    }
    if (data.signal) {
        v32State.signal = data.signal;
    }
}

/**
 * Update price from API
 */
function updateV32PriceFromAPI(data) {
    if (!data) return;
    
    if (data.bid !== undefined && data.bid !== null) {
        v32State.currentPrice = parseFloat(data.bid);
    } else if (data.ask !== undefined && data.ask !== null) {
        v32State.currentPrice = parseFloat(data.ask);
    }
}

/**
 * Parse robot logs for OR data (fallback when API doesn't have data yet)
 */
async function parseV32LogsForOR() {
    // Skip if we already have OR data from API
    if (v32State.orHigh && v32State.orLow) return;
    
    try {
        const response = await fetch(`${V32Config.apiUrl}/api/robot_logs?robot=v32_london&limit=50`);
        if (!response.ok) return;
        
        const data = await response.json();
        if (!data.logs || !Array.isArray(data.logs)) return;
        
        // Parse logs from newest to oldest
        for (const log of data.logs.reverse()) {
            const msg = log.message || '';
            
            // Match "OR calculat: H=1.23456 L=1.23450 R=0.6pips" pattern
            const orMatch = msg.match(/OR calculat:\s*H=([\d.]+)\s*L=([\d.]+)\s*R=([\d.]+)pips/i) ||
                              msg.match(/High=([\d.]+).*Low=([\d.]+).*Range=([\d.]+)\s*pips/i) ||
                              msg.match(/H=([\d.]+).*L=([\d.]+).*\(([\d.]+)\s*pips\)/i);
            
            if (orMatch) {
                v32State.orHigh = parseFloat(orMatch[1]);
                v32State.orLow = parseFloat(orMatch[2]);
                v32State.orRange = parseFloat(orMatch[3]);
                console.log('[V32-OR] Found OR data from logs:', v32State.orHigh, v32State.orLow, v32State.orRange);
                break; // Use most recent log entry
            }
            
            // Alternative patterns
            const orHighMatch = msg.match(/OR High[:\s]+([\d.]+)/i);
            const orLowMatch = msg.match(/OR Low[:\s]+([\d.]+)/i);
            if (orHighMatch) v32State.orHigh = parseFloat(orHighMatch[1]);
            if (orLowMatch) v32State.orLow = parseFloat(orLowMatch[1]);
            if (orHighMatch || orLowMatch) break;
        }
    } catch (error) {
        console.debug('[V32-OR] Log parsing failed:', error.message);
    }
}

/**
 * Update all DOM elements with current state
 */
function updateV32ORDOM() {
    // OR High
    const orHighEl = document.getElementById('v32ORHigh');
    if (orHighEl && v32State.orHigh) {
        orHighEl.textContent = v32State.orHigh.toFixed(5);
        orHighEl.classList.remove('text-muted');
        orHighEl.classList.add('live-data');
    }
    
    // OR Low
    const orLowEl = document.getElementById('v32ORLow');
    if (orLowEl && v32State.orLow) {
        orLowEl.textContent = v32State.orLow.toFixed(5);
        orLowEl.classList.remove('text-muted');
        orLowEl.classList.add('live-data');
    }
    
    // OR Range (in pips)
    const orRangeEl = document.getElementById('v32ORRange');
    if (orRangeEl) {
        if (v32State.orRange) {
            orRangeEl.textContent = parseFloat(v32State.orRange).toFixed(1) + ' pips';
            orRangeEl.classList.remove('text-muted');
        } else if (v32State.orHigh && v32State.orLow) {
            const rangePips = ((v32State.orHigh - v32State.orLow) * 10000).toFixed(1);
            orRangeEl.textContent = rangePips + ' pips';
            orRangeEl.classList.remove('text-muted');
        }
    }
    
    // Current Price
    const currentPriceEl = document.getElementById('v32CurrentPrice');
    if (currentPriceEl && v32State.currentPrice) {
        currentPriceEl.textContent = v32State.currentPrice.toFixed(5);
        currentPriceEl.classList.remove('text-muted');
        currentPriceEl.classList.add('live-data');
        
        // Add price flash effect on update
        currentPriceEl.classList.add('price-update');
        setTimeout(() => currentPriceEl.classList.remove('price-update'), 300);
    }
    
    // Asia Session data
    const asiaHighEl = document.getElementById('v32AsiaHigh');
    if (asiaHighEl && v32State.asiaHigh) {
        asiaHighEl.textContent = v32State.asiaHigh.toFixed(5);
    }
    
    const asiaLowEl = document.getElementById('v32AsiaLow');
    if (asiaLowEl && v32State.asiaLow) {
        asiaLowEl.textContent = v32State.asiaLow.toFixed(5);
    }
    
    const asiaRangeEl = document.getElementById('v32AsiaRange');
    if (asiaRangeEl && v32State.asiaRange) {
        asiaRangeEl.textContent = parseFloat(v32State.asiaRange).toFixed(1) + ' pips';
    }
    
    // Signal display
    const signalEl = document.getElementById('v32Signal');
    const signalBox = document.getElementById('v32SignalBox');
    if (signalEl && v32State.signal) {
        signalEl.textContent = v32State.signal;
        if (signalBox) {
            signalBox.className = 'signal-box ' + (v32State.signal === 'BUY' ? 'signal-buy' : 
                                                    v32State.signal === 'SELL' ? 'signal-sell' : 'signal-wait');
        }
    }
    
    // Breakout status
    const breakoutStatusEl = document.getElementById('v32BreakoutStatus');
    if (breakoutStatusEl) {
        if (v32State.breakoutDetected) {
            breakoutStatusEl.textContent = '🔥 Detected';
            breakoutStatusEl.style.color = '#22c55e';
        } else {
            breakoutStatusEl.textContent = '⏳ Waiting';
            breakoutStatusEl.style.color = '#f59e0b';
        }
    }
}

/**
 * Manual refresh function - can be called from UI
 */
function refreshV32ORData() {
    console.log('[V32-OR] Manual refresh triggered');
    updateV32ORData();
    parseV32LogsForOR();
}

/**
 * Get current V32 state (for external use)
 */
function getV32State() {
    return { ...v32State };
}

// CSS styles for live data display
const v32Styles = document.createElement('style');
v32Styles.textContent = `
    .live-data {
        color: #22c55e !important;
        font-weight: 600;
    }
    .price-update {
        animation: priceFlash 0.3s ease;
    }
    @keyframes priceFlash {
        0% { background-color: rgba(34, 197, 94, 0.3); }
        100% { background-color: transparent; }
    }
    .text-muted {
        color: #64748b !important;
    }
`;
document.head.appendChild(v32Styles);

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initV32ORConnector);
} else {
    // DOM already loaded
    initV32ORConnector();
}

// Export functions for global access
window.V32ORConnector = {
    init: initV32ORConnector,
    refresh: refreshV32ORData,
    getState: getV32State,
    state: v32State
};

console.log('[V32-OR] Connector loaded and ready');
