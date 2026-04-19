// ═══════════════════════════════════════════════════════════════════════════
// ═══════════════════════════════════════════════════════════════════════════
// 🎯 UNIFIED DASHBOARD - V31 / V32 / V33 ROBOTS
// ═══════════════════════════════════════════════════════════════════════════
// ═══════════════════════════════════════════════════════════════════════════

const API_URL = window.location.origin;

// ═══════════════════════════════════════════════════════════════════════════
// GLOBAL VARIABLES FOR ALL ROBOTS
// ═══════════════════════════════════════════════════════════════════════════

// V31 Variables
let v31DashboardInterval = null;
let v31SymbolStates = new Map();
let v31LastData = null;

// V32 Variables
let v32DashboardInterval = null;
let v32SymbolStates = new Map();
let v32LastData = null;
let v32SessionData = {
    london_time: null,
    session_phase: 'BEFORE_SESSION',
    is_active: false,
    time_remaining_minutes: 0
};

// V33 Variables
let v33DashboardInterval = null;
let v33SymbolStates = new Map();
let v33TradeHistory = [];
let v33SessionData = {
    ny_time: null,
    session_phase: 'BEFORE_SESSION',
    is_active: false,
    time_remaining_minutes: 0
};

// Health Check Variables
let healthExpanded = { postgresql: false, mt5core: false, brainbridge: false };
let healthCheckInterval = null;

// ═══════════════════════════════════════════════════════════════════════════
// COMMON FUNCTIONS
// ═══════════════════════════════════════════════════════════════════════════

function getAuthToken() {
    const session = localStorage.getItem('mt5_session');
    if (session) {
        try {
            const data = JSON.parse(session);
            return data.token;
        } catch (e) {
            return null;
        }
    }
    return null;
}

function getAuthHeaders() {
    const token = getAuthToken();
    return token ? { 'Authorization': `Bearer ${token}` } : {};
}

function showToast(message, type = 'success', duration = 3000) {
    const container = document.getElementById('toastContainer') || createToastContainer();

    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.style.cssText = `
        padding: 12px 20px;
        margin-bottom: 10px;
        border-radius: 8px;
        color: white;
        font-size: 14px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        animation: slideIn 0.3s ease;
        border-left: 4px solid;
        ${type === 'success' ? 'background: rgba(34, 197, 94, 0.9); border-color: #22c55e;' : ''}
        ${type === 'error' ? 'background: rgba(239, 68, 68, 0.9); border-color: #ef4444;' : ''}
        ${type === 'info' ? 'background: rgba(59, 130, 246, 0.9); border-color: #3b82f6;' : ''}
    `;
    toast.textContent = message;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toastContainer';
    container.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 10000;
        max-width: 300px;
    `;
    document.body.appendChild(container);
    return container;
}

// ═══════════════════════════════════════════════════════════════════════════
// ROBOT SWITCHER - COMMON FUNCTION
// ═══════════════════════════════════════════════════════════════════════════

function switchRobot() {
    const robot = document.getElementById('robotSelector').value;
    
    // Hide all sections
    const v31Section = document.getElementById('v31-dashboard-section');
    const v32Section = document.getElementById('v32-dashboard-section');
    const v33Section = document.getElementById('v33-dashboard-section');
    
    if (v31Section) v31Section.style.display = 'none';
    if (v32Section) v32Section.style.display = 'none';
    if (v33Section) v33Section.style.display = 'none';
    
    // Stop all polling
    stopV31Polling();
    stopV32Polling();
    stopV33Polling();
    
    // Sync robot status based on selection
    let robotId;
    if (robot === 'v31_tpl' || robot === 'v31_marius') {
        robotId = 'v31';
        if (v31Section) v31Section.style.display = 'block';
        startV31Polling();
    } else if (robot === 'v32_london') {
        robotId = 'v32';
        if (v32Section) v32Section.style.display = 'block';
        startV32Polling();
    } else if (robot === 'v33_ny') {
        robotId = 'v33';
        if (v33Section) v33Section.style.display = 'block';
        startV33Polling();
    }
    
    // Sync status for the selected robot immediately
    if (robotId) {
        syncRobotStatusFromBackend(robotId);
    }
    
    console.log(`[Dashboard] Switched to ${robot}`);
}

// ═══════════════════════════════════════════════════════════════════════════
// ═══════════════════════════════════════════════════════════════════════════
// 🤖 V31 MARIUS TPL DASHBOARD - LIVE ANALYSIS STATUS
// ═══════════════════════════════════════════════════════════════════════════
// ═══════════════════════════════════════════════════════════════════════════

function startV31Polling() {
    if (v31DashboardInterval) return;
    
    console.log('[V31] Starting dashboard polling (5s interval)');
    
    // Immediate update
    fetchV31Data();
    
    // Set up interval (5 seconds for V31)
    v31DashboardInterval = setInterval(fetchV31Data, 5000);
}

function stopV31Polling() {
    if (v31DashboardInterval) {
        clearInterval(v31DashboardInterval);
        v31DashboardInterval = null;
        console.log('[V31] Dashboard polling stopped');
    }
}

async function fetchV31Data() {
    try {
        const res = await fetch(`${API_URL}/api/v31/live_status`, {
            headers: getAuthHeaders()
        });
        
        if (!res.ok) throw new Error('Failed to fetch V31 live status');
        
        const data = await res.json();
        if (data.status === 'success') {
            v31LastData = data.data;
            updateV31Dashboard(data.data);
        }
    } catch (error) {
        console.error('[V31] Error fetching data:', error);
        // Keep previous values on error - don't show "undefined"
    }
}

function updateV31Dashboard(data) {
    if (!data) return;
    
    // Update Live Analysis Status
    updateV31LiveStatus(data.status);
    
    // Update Progress Bar
    const progressBar = document.getElementById('v31LiveProgressBar');
    if (progressBar && data.progress !== undefined) {
        progressBar.style.width = `${data.progress}%`;
    }
    
    // Update Current Symbol
    const currentEl = document.getElementById('v31LiveCurrent');
    if (currentEl && data.current_symbol) {
        currentEl.textContent = `Analyzing: ${data.current_symbol}`;
    }
    
    // Update Counts
    const analyzedEl = document.getElementById('v31AnalyzedCount');
    const setupsEl = document.getElementById('v31SetupsCount');
    const rejectedEl = document.getElementById('v31RejectedCount');
    
    if (analyzedEl) analyzedEl.textContent = data.analyzed_count || 0;
    if (setupsEl) setupsEl.textContent = data.setups_count || 0;
    if (rejectedEl) rejectedEl.textContent = data.rejected_count || 0;
    
    // Update Symbol Grid
    if (data.symbols) {
        updateV31SymbolGrid(data.symbols);
    }
    
    // Update Daily Stats
    if (data.daily_stats) {
        updateV31DailyStats(data.daily_stats);
    }
    
    // Update Current Setup if available
    if (data.current_setup) {
        updateV31CurrentSetup(data.current_setup);
    }
}

function updateV31LiveStatus(status) {
    const phaseEl = document.getElementById('v31LivePhase');
    const badgeEl = document.getElementById('v31StatusBadge');
    
    if (!status) {
        if (phaseEl) phaseEl.textContent = 'Waiting...';
        return;
    }
    
    const statusMap = {
        'IDLE': { text: 'Waiting...', color: '#64748b', badge: '⏳ Idle' },
        'SCANNING': { text: 'Scanning symbols...', color: '#8b5cf6', badge: '🔍 Scanning' },
        'ANALYZING': { text: 'Analyzing setup...', color: '#f59e0b', badge: '⚙️ Analyzing' },
        'SETUP_FOUND': { text: 'Setup found!', color: '#22c55e', badge: '✅ Setup Found' },
        'TRADING': { text: 'Executing trade...', color: '#22c55e', badge: '📊 Trading' }
    };
    
    const info = statusMap[status] || statusMap['IDLE'];
    
    if (phaseEl) {
        phaseEl.textContent = info.text;
        phaseEl.style.color = info.color;
    }
    
    if (badgeEl) {
        badgeEl.textContent = info.badge;
        badgeEl.style.background = info.color;
    }
}

function updateV31SymbolGrid(symbols) {
    const gridEl = document.getElementById('v31SymbolGrid');
    const countEl = document.getElementById('v31SymbolCount');
    
    if (!gridEl || !symbols) return;
    
    if (countEl) countEl.textContent = symbols.length;
    
    // Show up to 10 symbols in the grid
    const displaySymbols = symbols.slice(0, 10);
    
    gridEl.innerHTML = displaySymbols.map(sym => {
        const hasSetup = sym.setup_found;
        const statusColor = hasSetup ? '#22c55e' : sym.analyzed ? '#8b5cf6' : '#64748b';
        const bgColor = hasSetup ? 'rgba(34, 197, 94, 0.2)' : 'rgba(139, 92, 246, 0.1)';
        
        return `
            <div style="
                background: ${bgColor};
                border: 1px solid ${statusColor};
                border-radius: 6px;
                padding: 8px;
                text-align: center;
                font-size: 11px;
                color: ${statusColor};
                font-weight: 600;
            ">
                ${sym.symbol}
                ${hasSetup ? '✓' : sym.analyzed ? '◆' : '○'}
            </div>
        `;
    }).join('');
}

function updateV31CurrentSetup(setup) {
    const focusEl = document.getElementById('v31CurrentFocus');
    const setupEl = document.getElementById('v31CurrentSetup');
    
    if (!setup) {
        if (focusEl) focusEl.innerHTML = '<div style="color: #64748b;">No symbol in focus</div>';
        if (setupEl) setupEl.innerHTML = '<div style="color: #64748b;">Waiting for setup...</div>';
        return;
    }
    
    // Update Focus
    if (focusEl) {
        focusEl.innerHTML = `
            <div style="font-size: 18px; font-weight: 700; color: #8b5cf6;">${setup.symbol || '--'}</div>
            <div style="font-size: 12px; color: #94a3b8;">${setup.direction || '--'}</div>
        `;
    }
    
    // Update Setup Scores
    if (setupEl) {
        const rsiScore = setup.rsi_score || 0;
        const stochScore = setup.stoch_score || 0;
        const fibScore = setup.fib_score || 0;
        const totalScore = setup.total_score || 0;
        
        document.getElementById('v31ScoreRSI').textContent = rsiScore > 0 ? `+${rsiScore}` : '-';
        document.getElementById('v31ScoreRSI').style.color = rsiScore >= 2 ? '#22c55e' : '#64748b';
        
        document.getElementById('v31ScoreStoch').textContent = stochScore > 0 ? `+${stochScore}` : '-';
        document.getElementById('v31ScoreStoch').style.color = stochScore >= 2 ? '#22c55e' : '#64748b';
        
        document.getElementById('v31ScoreFib').textContent = fibScore > 0 ? `+${fibScore}` : '-';
        document.getElementById('v31ScoreFib').style.color = fibScore >= 2 ? '#22c55e' : '#64748b';
        
        document.getElementById('v31ScoreTotal').textContent = `${totalScore}/10`;
        document.getElementById('v31ScoreTotal').style.color = totalScore >= 6 ? '#22c55e' : totalScore >= 4 ? '#f59e0b' : '#64748b';
    }
}

function updateV31DailyStats(stats) {
    if (!stats) return;
    
    const setupCountEl = document.getElementById('v31SetupCount');
    const tradeCountEl = document.getElementById('v31TradeCount');
    const winRateEl = document.getElementById('v31WinRate');
    
    if (setupCountEl) setupCountEl.textContent = stats.setups_today || 0;
    if (tradeCountEl) tradeCountEl.textContent = stats.trades_today || 0;
    
    if (winRateEl) {
        const winRate = stats.win_rate || 0;
        winRateEl.textContent = `${winRate.toFixed(0)}%`;
        winRateEl.style.color = winRate >= 50 ? '#22c55e' : winRate >= 30 ? '#f59e0b' : '#64748b';
    }
}

// ═══════════════════════════════════════════════════════════════════════════
// ═══════════════════════════════════════════════════════════════════════════
// 🌅 V32 LONDON BREAKOUT DASHBOARD
// ═══════════════════════════════════════════════════════════════════════════
// ═══════════════════════════════════════════════════════════════════════════

function startV32Polling() {
    if (v32DashboardInterval) return;
    
    console.log('[V32] Starting dashboard polling (1s interval)');
    
    // Immediate update
    updateV32LondonTime();
    fetchV32Data();
    
    // Set up interval (1 second for V32 - time critical)
    v32DashboardInterval = setInterval(() => {
        updateV32LondonTime();
        updateV32SessionTimer();
        fetchV32Data();
    }, 1000);
}

function stopV32Polling() {
    if (v32DashboardInterval) {
        clearInterval(v32DashboardInterval);
        v32DashboardInterval = null;
        console.log('[V32] Dashboard polling stopped');
    }
}

async function fetchV32Data() {
    try {
        // Fetch all V32 endpoints in parallel
        const [sessionRes, orRes, asiaRes, breakoutRes, statsRes] = await Promise.allSettled([
            fetch(`${API_URL}/api/v32/session_status`, { headers: getAuthHeaders() }),
            fetch(`${API_URL}/api/v32/or_data`, { headers: getAuthHeaders() }),
            fetch(`${API_URL}/api/v32/asia_data`, { headers: getAuthHeaders() }),
            fetch(`${API_URL}/api/v32/breakout_status`, { headers: getAuthHeaders() }),
            fetch(`${API_URL}/api/v32/trade_stats`, { headers: getAuthHeaders() })
        ]);
        
        const data = {};
        
        // Process results - keep previous values on error
        if (sessionRes.status === 'fulfilled' && sessionRes.value.ok) {
            const sessionData = await sessionRes.value.json();
            if (sessionData.status === 'success') {
                data.session = sessionData.data;
                v32SessionData = { ...v32SessionData, ...sessionData.data };
            }
        }
        
        if (orRes.status === 'fulfilled' && orRes.value.ok) {
            const orData = await orRes.value.json();
            if (orData.status === 'success') data.or = orData.data;
        }
        
        if (asiaRes.status === 'fulfilled' && asiaRes.value.ok) {
            const asiaData = await asiaRes.value.json();
            if (asiaData.status === 'success') data.asia = asiaData.data;
        }
        
        if (breakoutRes.status === 'fulfilled' && breakoutRes.value.ok) {
            const breakoutData = await breakoutRes.value.json();
            if (breakoutData.status === 'success') data.breakout = breakoutData.data;
        }
        
        if (statsRes.status === 'fulfilled' && statsRes.value.ok) {
            const statsData = await statsRes.value.json();
            if (statsData.status === 'success') data.stats = statsData.data;
        }
        
        v32LastData = data;
        updateV32Dashboard(data);
        
    } catch (error) {
        console.error('[V32] Error fetching data:', error);
        // Keep previous values on error
    }
}

function updateV32Dashboard(data) {
    if (!data) return;
    
    // Update Session Display
    if (data.session) {
        updateV32SessionDisplay(data.session);
    }
    
    // Update Opening Range
    if (data.or) {
        updateV32OpeningRange(data.or);
    }
    
    // Update Asia Session
    if (data.asia) {
        updateV32AsiaSession(data.asia);
    }
    
    // Update Breakout Detection
    if (data.breakout) {
        updateV32BreakoutDetection(data.breakout);
    }
    
    // Update Daily Stats
    if (data.stats) {
        updateV32DailyStats(data.stats);
    }
}

function updateV32LondonTime() {
    const timeDisplay = document.getElementById('v32LondonTime');
    if (!timeDisplay) return;
    
    const now = new Date();
    const londonTime = new Date(now.toLocaleString("en-US", {timeZone: "Europe/London"}));
    const hours = londonTime.getHours().toString().padStart(2, '0');
    const minutes = londonTime.getMinutes().toString().padStart(2, '0');
    const seconds = londonTime.getSeconds().toString().padStart(2, '0');
    
    timeDisplay.textContent = `${hours}:${minutes}:${seconds}`;
}

function updateV32SessionTimer() {
    const timerDisplay = document.getElementById('v32SessionTimer');
    const phaseDisplay = document.getElementById('v32SessionPhase');
    const badgeEl = document.getElementById('v32SessionBadge');
    
    if (!timerDisplay || !phaseDisplay) return;
    
    const now = new Date();
    const londonTime = new Date(now.toLocaleString("en-US", {timeZone: "Europe/London"}));
    const hour = londonTime.getHours();
    const minute = londonTime.getMinutes();
    const second = londonTime.getSeconds();
    const currentMinutes = hour * 60 + minute;
    const currentSeconds = currentMinutes * 60 + second;
    
    // London Session: 08:00-10:30 (8:00 AM - 10:30 AM) London Time
    const sessionStart = 8 * 60;       // 08:00
    const sessionEnd = 10 * 60 + 30;   // 10:30
    const orEnd = 8 * 60 + 15;         // 08:15 OR ends
    
    if (currentMinutes < sessionStart) {
        // Before session
        const minutesUntil = sessionStart - currentMinutes;
        const secondsUntil = (minutesUntil * 60) - second;
        const hours = Math.floor(minutesUntil / 60);
        const mins = minutesUntil % 60;
        const secs = 59 - second;
        
        timerDisplay.textContent = hours > 0 ? `-${hours}h ${mins}m` : `-${mins}m ${secs}s`;
        timerDisplay.style.color = '#f59e0b';
        phaseDisplay.textContent = 'Before Session (00:00-08:00)';
        if (badgeEl) {
            badgeEl.textContent = '⏳ Waiting';
            badgeEl.style.background = '#f59e0b';
        }
    } else if (currentMinutes < orEnd) {
        // Opening Range formation (08:00-08:15)
        const secondsRemaining = (orEnd * 60) - currentSeconds;
        const mins = Math.floor(secondsRemaining / 60);
        const secs = secondsRemaining % 60;
        
        timerDisplay.textContent = `${mins}m ${secs}s`;
        timerDisplay.style.color = '#3b82f6';
        phaseDisplay.textContent = 'OR Formation (08:00-08:15)';
        if (badgeEl) {
            badgeEl.textContent = '📊 OR Formation';
            badgeEl.style.background = '#3b82f6';
        }
    } else if (currentMinutes < sessionEnd) {
        // Main session (08:15-10:30)
        const secondsRemaining = (sessionEnd * 60) - currentSeconds;
        const hours = Math.floor(secondsRemaining / 3600);
        const mins = Math.floor((secondsRemaining % 3600) / 60);
        const secs = secondsRemaining % 60;
        
        if (hours > 0) {
            timerDisplay.textContent = `${hours}h ${mins}m`;
        } else {
            timerDisplay.textContent = `${mins}m ${secs}s`;
        }
        timerDisplay.style.color = '#22c55e';
        phaseDisplay.textContent = 'Main Session (08:15-10:30)';
        if (badgeEl) {
            badgeEl.textContent = '🟢 Active';
            badgeEl.style.background = '#22c55e';
        }
    } else {
        // After session
        timerDisplay.textContent = 'ENDED';
        timerDisplay.style.color = '#64748b';
        phaseDisplay.textContent = 'Session Ended';
        if (badgeEl) {
            badgeEl.textContent = '⏹️ Closed';
            badgeEl.style.background = '#64748b';
        }
    }
}

function updateV32SessionDisplay(data) {
    const phaseEl = document.getElementById('v32SessionPhase');
    const badgeEl = document.getElementById('v32SessionBadge');
    const timerDisplay = document.getElementById('v32SessionTimer');
    
    if (phaseEl && data.session_phase) {
        const phaseNames = {
            'BEFORE_SESSION': 'Before Session (00:00-08:00)',
            'OPENING_RANGE': 'Opening Range (08:00-08:15)',
            'MAIN_SESSION': 'Main Session (08:15-10:30)',
            'AFTER_SESSION': 'Session Ended'
        };
        phaseEl.textContent = phaseNames[data.session_phase] || data.session_phase;
    }
    
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
    
    if (timerDisplay && data.time_remaining_seconds !== undefined) {
        const secs = data.time_remaining_seconds;
        const hours = Math.floor(secs / 3600);
        const mins = Math.floor((secs % 3600) / 60);
        const seconds = secs % 60;
        
        if (hours > 0) {
            timerDisplay.textContent = `${hours}h ${mins}m`;
        } else if (secs > 0) {
            timerDisplay.textContent = `${mins}m ${seconds}s`;
        } else {
            timerDisplay.textContent = 'ENDED';
        }
    }
}

function updateV32OpeningRange(data) {
    const orHighEl = document.getElementById('v32ORHigh');
    const orLowEl = document.getElementById('v32ORLow');
    const orRangeEl = document.getElementById('v32ORRange');
    const currentPriceEl = document.getElementById('v32CurrentPrice');
    
    if (!data) return;
    
    const orHigh = parseFloat(data.or_high) || 0;
    const orLow = parseFloat(data.or_low) || 0;
    const currentPrice = parseFloat(data.current_price) || 0;
    
    if (orHigh > 0 && orLow > 0) {
        const orRange = orHigh - orLow;
        const orRangePips = (orRange * 10000).toFixed(1);
        
        if (orHighEl) orHighEl.textContent = orHigh.toFixed(5);
        if (orLowEl) orLowEl.textContent = orLow.toFixed(5);
        if (orRangeEl) orRangeEl.textContent = `${orRangePips} pips`;
    }
    
    if (currentPriceEl && currentPrice > 0) {
        currentPriceEl.textContent = currentPrice.toFixed(5);
    }
}

function updateV32AsiaSession(data) {
    const asiaHighEl = document.getElementById('v32AsiaHigh');
    const asiaLowEl = document.getElementById('v32AsiaLow');
    const asiaRangeEl = document.getElementById('v32AsiaRange');
    const asiaStatusEl = document.getElementById('v32AsiaStatus');
    
    if (!data) return;
    
    const asiaHigh = parseFloat(data.asia_high) || 0;
    const asiaLow = parseFloat(data.asia_low) || 0;
    const isCompressed = data.is_compressed || false;
    
    if (asiaHighEl) asiaHighEl.textContent = asiaHigh > 0 ? asiaHigh.toFixed(5) : '--.-----';
    if (asiaLowEl) asiaLowEl.textContent = asiaLow > 0 ? asiaLow.toFixed(5) : '--.-----';
    
    if (asiaRangeEl) {
        if (asiaHigh > 0 && asiaLow > 0) {
            const range = asiaHigh - asiaLow;
            const rangePips = (range * 10000).toFixed(1);
            asiaRangeEl.textContent = `${rangePips} pips`;
        } else {
            asiaRangeEl.textContent = '-- pips';
        }
    }
    
    if (asiaStatusEl) {
        if (isCompressed) {
            asiaStatusEl.textContent = '✅ Compressed';
            asiaStatusEl.style.background = 'rgba(34, 197, 94, 0.2)';
            asiaStatusEl.style.color = '#22c55e';
        } else {
            asiaStatusEl.textContent = '⚠️ Expanded';
            asiaStatusEl.style.background = 'rgba(239, 68, 68, 0.2)';
            asiaStatusEl.style.color = '#ef4444';
        }
    }
}

function updateV32BreakoutDetection(data) {
    const breakoutStatusEl = document.getElementById('v32BreakoutStatus');
    const setupTypeEl = document.getElementById('v32SetupType');
    const bodyPercentEl = document.getElementById('v32BodyPercent');
    const wickPercentEl = document.getElementById('v32WickPercent');
    const signalEl = document.getElementById('v32Signal');
    const signalBox = document.getElementById('v32SignalBox');
    
    if (!data) return;
    
    const status = data.breakout_status || 'WAITING';
    const setupType = data.setup_type || '-';
    const bodyPercent = parseFloat(data.body_percent) || 0;
    const wickPercent = parseFloat(data.wick_percent) || 0;
    const signal = data.signal || 'WAIT';
    
    // Status display
    if (breakoutStatusEl) {
        const statusMap = {
            'WAITING': { text: '⏳ Waiting for OR...', color: '#64748b' },
            'IN_OR': { text: '📊 OR Formation...', color: '#3b82f6' },
            'SCANNING': { text: '🔍 Scanning...', color: '#f59e0b' },
            'DETECTED': { text: '🔥 BREAKOUT!', color: '#22c55e' },
            'INVALID': { text: '❌ Invalid', color: '#ef4444' }
        };
        
        const statusInfo = statusMap[status] || statusMap['WAITING'];
        breakoutStatusEl.textContent = statusInfo.text;
        breakoutStatusEl.style.color = statusInfo.color;
    }
    
    // Setup Type
    if (setupTypeEl) {
        const typeColors = {
            'TYPE_A': '#22c55e',
            'TYPE_B': '#f59e0b',
            '-': '#64748b'
        };
        setupTypeEl.textContent = setupType;
        setupTypeEl.style.color = typeColors[setupType] || '#64748b';
    }
    
    // Body Percent
    if (bodyPercentEl) {
        bodyPercentEl.textContent = bodyPercent > 0 ? `${bodyPercent.toFixed(0)}%` : '--%';
        bodyPercentEl.style.color = bodyPercent >= 60 ? '#22c55e' : bodyPercent >= 50 ? '#f59e0b' : '#64748b';
    }
    
    // Wick Percent
    if (wickPercentEl) {
        wickPercentEl.textContent = wickPercent > 0 ? `${wickPercent.toFixed(0)}%` : '--%';
        wickPercentEl.style.color = wickPercent <= 30 ? '#22c55e' : wickPercent <= 40 ? '#f59e0b' : '#ef4444';
    }
    
    // Signal
    if (signalEl && signalBox) {
        signalEl.textContent = signal;
        
        if (signal === 'BUY') {
            signalEl.style.color = '#22c55e';
            signalBox.style.borderColor = '#22c55e';
            signalBox.style.boxShadow = '0 0 20px rgba(34, 197, 94, 0.4)';
            signalBox.style.background = 'rgba(34, 197, 94, 0.1)';
        } else if (signal === 'SELL') {
            signalEl.style.color = '#ef4444';
            signalBox.style.borderColor = '#ef4444';
            signalBox.style.boxShadow = '0 0 20px rgba(239, 68, 68, 0.4)';
            signalBox.style.background = 'rgba(239, 68, 68, 0.1)';
        } else {
            signalEl.style.color = '#64748b';
            signalBox.style.borderColor = 'rgba(100, 116, 139, 0.3)';
            signalBox.style.boxShadow = 'none';
            signalBox.style.background = 'transparent';
        }
    }
}

function updateV32DailyStats(stats) {
    if (!stats) return;
    
    const tradesCountEl = document.getElementById('v32TradesCount');
    const winLossEl = document.getElementById('v32WinLoss');
    const totalPnLEl = document.getElementById('v32TotalPnL');
    const typeBPendingEl = document.getElementById('v32TypeBPending');
    
    const tradesCount = stats.trades_count || 0;
    const wins = stats.wins || 0;
    const losses = stats.losses || 0;
    const totalPnL = parseFloat(stats.total_pnl) || 0;
    const typeBPending = stats.type_b_pending || false;
    
    if (tradesCountEl) {
        tradesCountEl.textContent = `${tradesCount}/2`;
        tradesCountEl.style.color = tradesCount >= 2 ? '#ef4444' : '#e2e8f0';
    }
    
    if (winLossEl) {
        winLossEl.textContent = `${wins}/${losses}`;
        const winRate = (wins + losses) > 0 ? (wins / (wins + losses) * 100) : 0;
        winLossEl.style.color = winRate >= 50 ? '#22c55e' : '#f59e0b';
    }
    
    if (totalPnLEl) {
        const prefix = totalPnL >= 0 ? '+' : '';
        totalPnLEl.textContent = `${prefix}$${totalPnL.toFixed(2)}`;
        totalPnLEl.style.color = totalPnL >= 0 ? '#22c55e' : '#ef4444';
    }
    
    if (typeBPendingEl) {
        typeBPendingEl.textContent = typeBPending ? '⏳ Yes' : '❌ No';
        typeBPendingEl.style.color = typeBPending ? '#f59e0b' : '#64748b';
    }
}

// ═══════════════════════════════════════════════════════════════════════════
// ═══════════════════════════════════════════════════════════════════════════
// 🗽 V33 NY BREAKOUT DASHBOARD - COMPLETE IMPLEMENTATION
// ═══════════════════════════════════════════════════════════════════════════
// ═══════════════════════════════════════════════════════════════════════════

function startV33Polling() {
    if (v33DashboardInterval) return;
    
    console.log('[V33] Starting dashboard polling (1s interval)');
    
    // Immediate update
    updateV33NYTime();
    updateV33Dashboard();
    
    // Set up interval (1 second for V33 - time critical)
    v33DashboardInterval = setInterval(() => {
        updateV33NYTime();
        updateV33Dashboard();
    }, 1000);
}

function stopV33Polling() {
    if (v33DashboardInterval) {
        clearInterval(v33DashboardInterval);
        v33DashboardInterval = null;
        console.log('[V33] Dashboard polling stopped');
    }
}

// V33 NY Time with seconds (HH:MM:SS)
function updateV33NYTime() {
    const now = new Date();
    const nyTime = new Date(now.toLocaleString("en-US", {timeZone: "America/New_York"}));
    const hours = nyTime.getHours().toString().padStart(2, '0');
    const minutes = nyTime.getMinutes().toString().padStart(2, '0');
    const seconds = nyTime.getSeconds().toString().padStart(2, '0');
    
    const timeDisplay = document.getElementById('v33NYTime');
    if (timeDisplay) {
        timeDisplay.textContent = `${hours}:${minutes}:${seconds}`;
    }
}

// V33 Session Timer
function updateV33SessionTimer(nyTime) {
    if (!nyTime) {
        const now = new Date();
        nyTime = new Date(now.toLocaleString("en-US", {timeZone: "America/New_York"}));
    }
    
    const hour = nyTime.getHours();
    const minute = nyTime.getMinutes();
    const second = nyTime.getSeconds();
    const currentMinutes = hour * 60 + minute;
    const currentSeconds = currentMinutes * 60 + second;
    
    // NY Session: 13:00-16:00 (1:00 PM - 4:00 PM) NY Time
    const sessionStart = 13 * 60;      // 13:00
    const sessionEnd = 16 * 60;        // 16:00
    const orEnd = 13 * 60 + 15;        // 13:15 OR ends
    const extendedEnd = 17 * 60;       // 17:00 Extended session ends
    
    const timerDisplay = document.getElementById('v33SessionTimer');
    const phaseDisplay = document.getElementById('v33SessionPhase');
    const badgeEl = document.getElementById('v33SessionBadge');
    
    if (!timerDisplay || !phaseDisplay) return;
    
    if (currentMinutes < sessionStart) {
        // Before session
        const minutesUntil = sessionStart - currentMinutes;
        const secondsUntil = (minutesUntil * 60) - second;
        const hours = Math.floor(minutesUntil / 60);
        const mins = minutesUntil % 60;
        const secs = 59 - second;
        
        timerDisplay.textContent = hours > 0 ? `-${hours}h ${mins}m` : `-${mins}m ${secs}s`;
        timerDisplay.style.color = '#f59e0b';
        phaseDisplay.textContent = 'Before Session (08:00-13:00)';
        if (badgeEl) {
            badgeEl.textContent = '⏳ Waiting';
            badgeEl.style.background = '#f59e0b';
        }
    } else if (currentMinutes < orEnd) {
        // Opening Range formation (13:00-13:15)
        const secondsInOR = currentSeconds - (sessionStart * 60);
        const secondsRemaining = (orEnd * 60) - currentSeconds;
        const mins = Math.floor(secondsRemaining / 60);
        const secs = secondsRemaining % 60;
        
        timerDisplay.textContent = `${mins}m ${secs}s`;
        timerDisplay.style.color = '#3b82f6';
        phaseDisplay.textContent = 'OR Formation (13:00-13:15)';
        if (badgeEl) {
            badgeEl.textContent = '📊 OR Formation';
            badgeEl.style.background = '#3b82f6';
        }
    } else if (currentMinutes < sessionEnd) {
        // Main session (13:15-16:00)
        const secondsRemaining = (sessionEnd * 60) - currentSeconds;
        const hours = Math.floor(secondsRemaining / 3600);
        const mins = Math.floor((secondsRemaining % 3600) / 60);
        const secs = secondsRemaining % 60;
        
        if (hours > 0) {
            timerDisplay.textContent = `${hours}h ${mins}m`;
        } else {
            timerDisplay.textContent = `${mins}m ${secs}s`;
        }
        timerDisplay.style.color = '#22c55e';
        phaseDisplay.textContent = 'Main Session (13:15-16:00)';
        if (badgeEl) {
            badgeEl.textContent = '🟢 Active';
            badgeEl.style.background = '#22c55e';
        }
    } else if (currentMinutes < extendedEnd) {
        // Extended session (16:00-17:00)
        const secondsRemaining = (extendedEnd * 60) - currentSeconds;
        const mins = Math.floor(secondsRemaining / 60);
        const secs = secondsRemaining % 60;
        
        timerDisplay.textContent = `${mins}m ${secs}s`;
        timerDisplay.style.color = '#8b5cf6';
        phaseDisplay.textContent = 'Extended Session (16:00-17:00) - A+ Only';
        if (badgeEl) {
            badgeEl.textContent = '⚠️ Extended';
            badgeEl.style.background = '#8b5cf6';
        }
    } else {
        // After session
        timerDisplay.textContent = 'ENDED';
        timerDisplay.style.color = '#64748b';
        phaseDisplay.textContent = 'Session Ended';
        if (badgeEl) {
            badgeEl.textContent = '⏹️ Closed';
            badgeEl.style.background = '#64748b';
        }
    }
}

// V33 Session Status API
async function fetchV33SessionStatus() {
    try {
        const res = await fetch(`${API_URL}/api/v33/session_status`, {
            headers: getAuthHeaders()
        });
        
        if (!res.ok) throw new Error('Failed to fetch session status');
        
        const data = await res.json();
        if (data.status === 'success') {
            v33SessionData = data.data;
            updateV33SessionDisplay(data.data);
            return data.data;
        }
    } catch (error) {
        console.error('[V33] Error fetching session status:', error);
    }
    return null;
}

function updateV33SessionDisplay(data) {
    if (!data) return;
    
    const sessionPhaseEl = document.getElementById('v33SessionPhase');
    const sessionBadgeEl = document.getElementById('v33SessionBadge');
    const timerDisplay = document.getElementById('v33SessionTimer');
    
    if (sessionPhaseEl && data.session_phase) {
        const phaseNames = {
            'BEFORE_SESSION': 'Before Session (08:00-13:00)',
            'OPENING_RANGE': 'Opening Range (13:00-13:15)',
            'MAIN_SESSION': 'Main Session (13:15-16:00)',
            'EXTENDED_SESSION': 'Extended Session (16:00-17:00)',
            'AFTER_SESSION': 'Session Ended'
        };
        sessionPhaseEl.textContent = phaseNames[data.session_phase] || data.session_phase;
    }
    
    if (sessionBadgeEl) {
        if (data.is_active) {
            sessionBadgeEl.textContent = '🟢 Active';
            sessionBadgeEl.style.background = '#22c55e';
        } else if (data.session_phase === 'AFTER_SESSION') {
            sessionBadgeEl.textContent = '⏹️ Closed';
            sessionBadgeEl.style.background = '#64748b';
        } else {
            sessionBadgeEl.textContent = '⏳ Waiting';
            sessionBadgeEl.style.background = '#f59e0b';
        }
    }
    
    if (timerDisplay && data.time_remaining_seconds !== undefined) {
        const secs = data.time_remaining_seconds;
        const hours = Math.floor(secs / 3600);
        const mins = Math.floor((secs % 3600) / 60);
        const seconds = secs % 60;
        
        if (hours > 0) {
            timerDisplay.textContent = `${hours}h ${mins}m`;
        } else if (secs > 0) {
            timerDisplay.textContent = `${mins}m ${seconds}s`;
        } else {
            timerDisplay.textContent = 'ENDED';
        }
    }
}

// V33 Opening Range
async function fetchV33ORData(symbol = 'EURUSD') {
    try {
        const res = await fetch(`${API_URL}/api/v33/or_data?symbol=${symbol}`, {
            headers: getAuthHeaders()
        });
        
        if (!res.ok) throw new Error('Failed to fetch OR data');
        
        const data = await res.json();
        if (data.status === 'success') {
            updateV33OpeningRange(data.data);
            return data.data;
        }
    } catch (error) {
        console.error('[V33] Error fetching OR data:', error);
    }
    return null;
}

function updateV33OpeningRange(data) {
    const orHighEl = document.getElementById('v33ORHigh');
    const orLowEl = document.getElementById('v33ORLow');
    const orRangeEl = document.getElementById('v33ORRange');
    const currentPriceEl = document.getElementById('v33CurrentPrice');
    
    if (!data) return;
    
    const orHigh = parseFloat(data.or_high) || 0;
    const orLow = parseFloat(data.or_low) || 0;
    const currentPrice = parseFloat(data.current_price) || 0;
    
    if (orHigh > 0 && orLow > 0) {
        const orRange = orHigh - orLow;
        const orRangePips = (orRange * 10000).toFixed(1);
        
        if (orHighEl) orHighEl.textContent = orHigh.toFixed(5);
        if (orLowEl) orLowEl.textContent = orLow.toFixed(5);
        if (orRangeEl) orRangeEl.textContent = `${orRangePips} pips`;
    }
    
    if (currentPriceEl && currentPrice > 0) {
        currentPriceEl.textContent = currentPrice.toFixed(5);
    }
}

// V33 Pre-Session Data
async function fetchV33PreSessionData(symbol = 'EURUSD') {
    try {
        const res = await fetch(`${API_URL}/api/v33/presession_data?symbol=${symbol}`, {
            headers: getAuthHeaders()
        });
        
        if (!res.ok) throw new Error('Failed to fetch Pre-Session data');
        
        const data = await res.json();
        if (data.status === 'success') {
            updateV33PreSession(data.data);
            return data.data;
        }
    } catch (error) {
        console.error('[V33] Error fetching Pre-Session data:', error);
    }
    return null;
}

function updateV33PreSession(data) {
    const preHighEl = document.getElementById('v33PreHigh');
    const preLowEl = document.getElementById('v33PreLow');
    const preRangeEl = document.getElementById('v33PreRange');
    const preStatusEl = document.getElementById('v33PreStatus');
    
    if (!data) return;
    
    const preHigh = parseFloat(data.pre_session_high) || 0;
    const preLow = parseFloat(data.pre_session_low) || 0;
    const isCompressed = data.is_compressed || false;
    const preRangePips = parseFloat(data.pre_session_range_pips) || 0;
    
    if (preHighEl) preHighEl.textContent = preHigh > 0 ? preHigh.toFixed(5) : '--.-----';
    if (preLowEl) preLowEl.textContent = preLow > 0 ? preLow.toFixed(5) : '--.-----';
    if (preRangeEl) preRangeEl.textContent = preRangePips > 0 ? `${preRangePips.toFixed(1)} pips` : '-- pips';
    
    if (preStatusEl) {
        if (isCompressed) {
            preStatusEl.textContent = '✅ Compressed';
            preStatusEl.style.background = 'rgba(34, 197, 94, 0.2)';
            preStatusEl.style.color = '#22c55e';
        } else {
            preStatusEl.textContent = '⚠️ Expanded';
            preStatusEl.style.background = 'rgba(239, 68, 68, 0.2)';
            preStatusEl.style.color = '#ef4444';
        }
    }
}

// V33 Breakout Status
async function fetchV33BreakoutStatus(symbol = 'EURUSD') {
    try {
        const res = await fetch(`${API_URL}/api/v33/breakout_status?symbol=${symbol}`, {
            headers: getAuthHeaders()
        });
        
        if (!res.ok) throw new Error('Failed to fetch breakout status');
        
        const data = await res.json();
        if (data.status === 'success') {
            updateV33BreakoutStatus(data.data);
            return data.data;
        }
    } catch (error) {
        console.error('[V33] Error fetching breakout status:', error);
    }
    return null;
}

function updateV33BreakoutStatus(data) {
    const breakoutStatusEl = document.getElementById('v33BreakoutStatus');
    const setupTypeEl = document.getElementById('v33SetupType');
    const bodyPercentEl = document.getElementById('v33BodyPercent');
    const wickPercentEl = document.getElementById('v33WickPercent');
    const signalEl = document.getElementById('v33Signal');
    const signalBox = document.getElementById('v33SignalBox');
    
    if (!data) return;
    
    const status = data.breakout_status || 'WAITING';
    const setupType = data.setup_type || '-';
    const bodyPercent = parseFloat(data.body_percent) || 0;
    const wickPercent = parseFloat(data.wick_percent) || 0;
    const signal = data.signal || 'WAIT';
    
    // Status display
    if (breakoutStatusEl) {
        const statusMap = {
            'WAITING': { text: '⏳ Waiting for OR...', color: '#64748b' },
            'IN_OR': { text: '📊 OR Formation...', color: '#3b82f6' },
            'SCANNING': { text: '🔍 Scanning...', color: '#f59e0b' },
            'DETECTED': { text: '🔥 BREAKOUT!', color: '#22c55e' },
            'TYPE_B_PENDING': { text: '⏳ Type B Pending...', color: '#8b5cf6' },
            'INVALID': { text: '❌ Invalid', color: '#ef4444' },
            'EXPIRED': { text: '⏰ Expired', color: '#64748b' }
        };
        
        const statusInfo = statusMap[status] || statusMap['WAITING'];
        breakoutStatusEl.textContent = statusInfo.text;
        breakoutStatusEl.style.color = statusInfo.color;
    }
    
    // Setup Type
    if (setupTypeEl) {
        const typeColors = {
            'TYPE_A': '#22c55e',
            'TYPE_B': '#f59e0b',
            'TYPE_A_EXTENDED': '#8b5cf6',
            '-': '#64748b'
        };
        setupTypeEl.textContent = setupType;
        setupTypeEl.style.color = typeColors[setupType] || '#64748b';
    }
    
    // Body Percent
    if (bodyPercentEl) {
        bodyPercentEl.textContent = bodyPercent > 0 ? `${bodyPercent.toFixed(0)}%` : '--%';
        bodyPercentEl.style.color = bodyPercent >= 60 ? '#22c55e' : bodyPercent >= 50 ? '#f59e0b' : '#64748b';
    }
    
    // Wick Percent
    if (wickPercentEl) {
        wickPercentEl.textContent = wickPercent > 0 ? `${wickPercent.toFixed(0)}%` : '--%';
        wickPercentEl.style.color = wickPercent <= 30 ? '#22c55e' : wickPercent <= 40 ? '#f59e0b' : '#ef4444';
    }
    
    // Signal
    if (signalEl && signalBox) {
        signalEl.textContent = signal;
        
        if (signal === 'BUY') {
            signalEl.style.color = '#22c55e';
            signalBox.style.borderColor = '#22c55e';
            signalBox.style.boxShadow = '0 0 20px rgba(34, 197, 94, 0.4)';
            signalBox.style.background = 'rgba(34, 197, 94, 0.1)';
        } else if (signal === 'SELL') {
            signalEl.style.color = '#ef4444';
            signalBox.style.borderColor = '#ef4444';
            signalBox.style.boxShadow = '0 0 20px rgba(239, 68, 68, 0.4)';
            signalBox.style.background = 'rgba(239, 68, 68, 0.1)';
        } else {
            signalEl.style.color = '#64748b';
            signalBox.style.borderColor = 'rgba(100, 116, 139, 0.3)';
            signalBox.style.boxShadow = 'none';
            signalBox.style.background = 'transparent';
        }
    }
}

// V33 Trade Stats
async function fetchV33TradeStats(symbol = 'EURUSD') {
    try {
        const res = await fetch(`${API_URL}/api/v33/trade_stats?symbol=${symbol}`, {
            headers: getAuthHeaders()
        });
        
        if (!res.ok) throw new Error('Failed to fetch trade stats');
        
        const data = await res.json();
        if (data.status === 'success') {
            updateV33DailyStats(data.data);
            return data.data;
        }
    } catch (error) {
        console.error('[V33] Error fetching trade stats:', error);
    }
    return null;
}

function updateV33DailyStats(data) {
    const tradesCountEl = document.getElementById('v33TradesCount');
    const winLossEl = document.getElementById('v33WinLoss');
    const totalPnLEl = document.getElementById('v33TotalPnL');
    const typeBPendingEl = document.getElementById('v33TypeBPending');
    
    if (!data) return;
    
    const tradesCount = data.trades_count || 0;
    const wins = data.wins || 0;
    const losses = data.losses || 0;
    const totalPnL = parseFloat(data.total_pnl) || 0;
    const typeBPending = data.type_b_pending || false;
    
    if (tradesCountEl) {
        tradesCountEl.textContent = `${tradesCount}/2`;
        tradesCountEl.style.color = tradesCount >= 2 ? '#ef4444' : '#e2e8f0';
    }
    
    if (winLossEl) {
        winLossEl.textContent = `${wins}/${losses}`;
        const winRate = (wins + losses) > 0 ? (wins / (wins + losses) * 100) : 0;
        winLossEl.style.color = winRate >= 50 ? '#22c55e' : '#f59e0b';
    }
    
    if (totalPnLEl) {
        const prefix = totalPnL >= 0 ? '+' : '';
        totalPnLEl.textContent = `${prefix}$${totalPnL.toFixed(2)}`;
        totalPnLEl.style.color = totalPnL >= 0 ? '#22c55e' : '#ef4444';
    }
    
    if (typeBPendingEl) {
        typeBPendingEl.textContent = typeBPending ? '⏳ Yes' : '❌ No';
        typeBPendingEl.style.color = typeBPending ? '#f59e0b' : '#64748b';
    }
}

// V33 Main Dashboard Update
async function updateV33Dashboard() {
    try {
        updateV33NYTime();
        updateV33SessionTimer();
        
        // Fetch all data in parallel
        const promises = [
            fetchV33SessionStatus(),
            fetchV33ORData(),
            fetchV33PreSessionData(),
            fetchV33BreakoutStatus(),
            fetchV33TradeStats()
        ];
        
        await Promise.allSettled(promises);
        
    } catch (error) {
        console.error('[V33] Dashboard update error:', error);
    }
}

// ═══════════════════════════════════════════════════════════════════════════
// EXPORT ALL FUNCTIONS TO GLOBAL SCOPE
// ═══════════════════════════════════════════════════════════════════════════

// Common functions
window.switchRobot = switchRobot;
window.showToast = showToast;
window.getAuthHeaders = getAuthHeaders;

// V31 exports
window.startV31Polling = startV31Polling;
window.stopV31Polling = stopV31Polling;
window.fetchV31Data = fetchV31Data;
window.updateV31Dashboard = updateV31Dashboard;
window.updateV31SymbolGrid = updateV31SymbolGrid;
window.updateV31LiveStatus = updateV31LiveStatus;
window.updateV31DailyStats = updateV31DailyStats;

// V32 exports
window.startV32Polling = startV32Polling;
window.stopV32Polling = stopV32Polling;
window.fetchV32Data = fetchV32Data;
window.updateV32Dashboard = updateV32Dashboard;
window.updateV32LondonTime = updateV32LondonTime;
window.updateV32SessionTimer = updateV32SessionTimer;
window.updateV32OpeningRange = updateV32OpeningRange;
window.updateV32AsiaSession = updateV32AsiaSession;
window.updateV32BreakoutDetection = updateV32BreakoutDetection;
window.updateV32DailyStats = updateV32DailyStats;

// V33 exports
window.startV33Polling = startV33Polling;
window.stopV33Polling = stopV33Polling;
window.updateV33NYTime = updateV33NYTime;
window.updateV33SessionTimer = updateV33SessionTimer;
window.updateV33SessionDisplay = updateV33SessionDisplay;
window.fetchV33SessionStatus = fetchV33SessionStatus;
window.updateV33OpeningRange = updateV33OpeningRange;
window.fetchV33ORData = fetchV33ORData;
window.updateV33PreSession = updateV33PreSession;
window.fetchV33PreSessionData = fetchV33PreSessionData;
window.updateV33BreakoutStatus = updateV33BreakoutStatus;
window.fetchV33BreakoutStatus = fetchV33BreakoutStatus;
window.updateV33DailyStats = updateV33DailyStats;
window.fetchV33TradeStats = fetchV33TradeStats;
window.updateV33Dashboard = updateV33Dashboard;

// ═══════════════════════════════════════════════════════════════════════════
// HEALTH CHECK FUNCTIONS
// ═══════════════════════════════════════════════════════════════════════════

function toggleHealthDetails(component) {
    healthExpanded[component] = !healthExpanded[component];
    const details = document.getElementById(`${component}-details`);
    const chevron = document.getElementById(`${component}-chevron`);

    if (details) {
        if (healthExpanded[component]) {
            details.classList.add('expanded');
        } else {
            details.classList.remove('expanded');
        }
    }

    if (chevron) {
        chevron.style.transform = healthExpanded[component] ? 'rotate(180deg)' : 'rotate(0deg)';
    }
}

async function loadSystemHealth() {
    try {
        const res = await fetch(`${API_URL}/api/health`, {
            headers: getAuthHeaders()
        });
        if (!res.ok) throw new Error('Failed to load health');

        const data = await res.json();

        // Map data to component format
        const components = {
            postgresql: { status: 'unknown', message: 'Unknown', uptime: '-', lastCheck: '-', connections: '-' },
            mt5core: { status: 'unknown', message: 'Unknown', uptime: '-', lastCheck: '-', version: '-' },
            brainbridge: { status: 'unknown', message: 'Unknown', uptime: '-', lastCheck: '-', connections: '-' }
        };

        if (data.services) {
            for (const svc of data.services) {
                if (svc.name === 'PostgreSQL') {
                    components.postgresql = {
                        status: svc.status,
                        message: svc.message,
                        uptime: svc.uptime || 'N/A',
                        lastCheck: svc.last_check || new Date().toLocaleTimeString(),
                        connections: svc.connections || 'N/A'
                    };
                } else if (svc.name === 'MT5 Core Server') {
                    components.mt5core = {
                        status: svc.status,
                        message: svc.message,
                        uptime: svc.uptime || 'N/A',
                        lastCheck: svc.last_check || new Date().toLocaleTimeString(),
                        version: svc.version || '1.0.0'
                    };
                } else if (svc.name.includes('Bridge') || svc.name.includes('Brain')) {
                    components.brainbridge = {
                        status: svc.status,
                        message: svc.message,
                        uptime: svc.uptime || 'N/A',
                        lastCheck: svc.last_check || new Date().toLocaleTimeString(),
                        connections: svc.connections || 'N/A'
                    };
                }
            }
        }

        // Update UI
        updateHealthUI('postgresql', components.postgresql);
        updateHealthUI('mt5core', components.mt5core);
        updateHealthUI('brainbridge', components.brainbridge);

    } catch (error) {
        console.error('[Health] Error loading system health:', error);
        // Set all to error state
        updateHealthUI('postgresql', { status: 'error', message: 'Connection failed' });
        updateHealthUI('mt5core', { status: 'error', message: 'Connection failed' });
        updateHealthUI('brainbridge', { status: 'error', message: 'Connection failed' });
    }
}

function updateHealthUI(component, data) {
    const statusEl = document.getElementById(component === 'mt5core' ? 'coreStatus' : 
                                               component === 'brainbridge' ? 'bridgeStatus' : 'postgresStatus');
    const detailStatusEl = document.getElementById(`${component}-detail-status`);
    const detailUptimeEl = document.getElementById(`${component}-detail-uptime`);
    const detailCheckEl = document.getElementById(`${component}-detail-check`);
    const detailConnectionsEl = document.getElementById(`${component}-detail-connections`);
    const detailVersionEl = document.getElementById(`${component}-detail-version`);

    // Status text and color
    const statusMap = {
        'healthy': { text: '✅ Online', color: '#22c55e' },
        'degraded': { text: '⚠️ Degraded', color: '#f59e0b' },
        'error': { text: '❌ Offline', color: '#ef4444' },
        'unknown': { text: '⏳ Verificare...', color: '#64748b' }
    };

    const statusInfo = statusMap[data.status] || statusMap['unknown'];

    if (statusEl) {
        statusEl.textContent = statusInfo.text;
        statusEl.style.color = statusInfo.color;
    }

    if (detailStatusEl) {
        detailStatusEl.textContent = data.message || statusInfo.text;
        detailStatusEl.style.color = statusInfo.color;
    }

    if (detailUptimeEl && data.uptime) {
        detailUptimeEl.textContent = data.uptime;
    }

    if (detailCheckEl) {
        detailCheckEl.textContent = data.lastCheck || new Date().toLocaleTimeString();
    }

    if (detailConnectionsEl && data.connections) {
        detailConnectionsEl.textContent = data.connections;
    }

    if (detailVersionEl && data.version) {
        detailVersionEl.textContent = data.version;
    }
}

function startHealthCheckPolling() {
    if (healthCheckInterval) return;
    
    console.log('[Health] Starting health check polling (10s interval)');
    
    // Immediate check
    loadSystemHealth();
    
    // Set up interval (10 seconds)
    healthCheckInterval = setInterval(loadSystemHealth, 10000);
}

function stopHealthCheckPolling() {
    if (healthCheckInterval) {
        clearInterval(healthCheckInterval);
        healthCheckInterval = null;
        console.log('[Health] Health check polling stopped');
    }
}

// Health exports
window.toggleHealthDetails = toggleHealthDetails;
window.loadSystemHealth = loadSystemHealth;
window.startHealthCheckPolling = startHealthCheckPolling;
window.stopHealthCheckPolling = stopHealthCheckPolling;

// ═══════════════════════════════════════════════════════════════════════════
// ROBOT CONNECTION STATUS
// ═══════════════════════════════════════════════════════════════════════════

// Connection status for each robot
let robotConnectionStatus = {
    v31: { connected: false, lastData: null, lastCheck: null },
    v32: { connected: false, lastData: null, lastCheck: null },
    v33: { connected: false, lastData: null, lastCheck: null }
};

let robotStatusCheckInterval = null;

async function checkRobotConnection(robot) {
    try {
        let endpoint;
        switch(robot) {
            case 'v31':
                endpoint = '/api/v31/live_status';
                break;
            case 'v32':
                endpoint = '/api/v32/or_data';
                break;
            case 'v33':
                endpoint = '/api/v33/or_data?symbol=EURUSD';
                break;
            default:
                return;
        }

        const res = await fetch(`${API_URL}${endpoint}`, {
            headers: getAuthHeaders()
        });

        if (!res.ok) throw new Error(`HTTP ${res.status}`);

        const data = await res.json();
        
        // Check if data is valid and recent
        const hasValidData = data.status === 'success' || data.or_high !== undefined || data.analyzed_count !== undefined;
        const now = new Date();
        
        robotConnectionStatus[robot] = {
            connected: hasValidData,
            lastData: data,
            lastCheck: now
        };

        updateRobotConnectionUI(robot, hasValidData);

    } catch (error) {
        console.error(`[Connection] ${robot} check failed:`, error);
        robotConnectionStatus[robot] = {
            connected: false,
            lastData: null,
            lastCheck: new Date()
        };
        updateRobotConnectionUI(robot, false);
    }
}

function updateRobotConnectionUI(robot, isConnected) {
    const dotId = `${robot}StatusDot`;
    const indicatorId = `${robot}ConnectionIndicator`;
    
    const dot = document.getElementById(dotId);
    const indicator = document.getElementById(indicatorId);
    
    if (dot) {
        dot.style.background = isConnected ? '#22c55e' : '#ef4444';
        dot.style.boxShadow = isConnected ? '0 0 8px #22c55e' : 'none';
    }
    
    if (indicator) {
        indicator.style.color = isConnected ? '#22c55e' : '#ef4444';
    }
}

async function checkAllRobotConnections() {
    console.log('[Connection] Checking all robot connections...');
    await Promise.all([
        checkRobotConnection('v31'),
        checkRobotConnection('v32'),
        checkRobotConnection('v33')
    ]);
}

function startRobotStatusPolling() {
    if (robotStatusCheckInterval) return;
    
    console.log('[Connection] Starting robot status polling (5s interval)');
    
    // Immediate check
    checkAllRobotConnections();
    
    // Set up interval (5 seconds)
    robotStatusCheckInterval = setInterval(checkAllRobotConnections, 5000);
}

function stopRobotStatusPolling() {
    if (robotStatusCheckInterval) {
        clearInterval(robotStatusCheckInterval);
        robotStatusCheckInterval = null;
        console.log('[Connection] Robot status polling stopped');
    }
}

// Connection exports
window.checkRobotConnection = checkRobotConnection;
window.checkAllRobotConnections = checkAllRobotConnections;
window.startRobotStatusPolling = startRobotStatusPolling;
window.stopRobotStatusPolling = stopRobotStatusPolling;

// ═══════════════════════════════════════════════════════════════════════════
// ROBOT CONTROL FUNCTIONS - Start/Stop with Real Process Sync
// ═══════════════════════════════════════════════════════════════════════════

let robotControlStatus = {
    v31: { isRunning: false, pid: null, lastCheck: null },
    v32: { isRunning: false, pid: null, lastCheck: null },
    v33: { isRunning: false, pid: null, lastCheck: null }
};

let robotStatusSyncInterval = null;

async function controlRobot(action) {
    const robot = document.getElementById('robotSelector').value;
    let endpoint;
    let robotId;
    
    switch(robot) {
        case 'v31_tpl':
            endpoint = action === 'start' ? '/api/robot/v31/start' : '/api/robot/v31/stop';
            robotId = 'v31';
            break;
        case 'v32_london':
            endpoint = action === 'start' ? '/api/robot/v32/start' : '/api/robot/v32/stop';
            robotId = 'v32';
            break;
        case 'v33_ny':
            endpoint = action === 'start' ? '/api/robot/v33/start' : '/api/robot/v33/stop';
            robotId = 'v33';
            break;
        default:
            showToast('Robot necunoscut', 'error');
            return;
    }
    
    try {
        const btn = document.getElementById(action === 'start' ? 'robotStartBtn' : 'robotStopBtn');
        if (btn) {
            btn.disabled = true;
            btn.textContent = action === 'start' ? '⏳ Starting...' : '⏳ Stopping...';
        }
        
        const res = await fetch(`${API_URL}${endpoint}`, {
            method: 'POST',
            headers: getAuthHeaders()
        });
        
        const data = await res.json();
        
        if (data.status === 'success') {
            showToast(`Robot ${robotId.toUpperCase()} ${action === 'start' ? 'pornit' : 'oprit'}`, 'success');
            
            // Update status immediately
            robotControlStatus[robotId] = {
                isRunning: action === 'start',
                pid: data.pid || null,
                lastCheck: new Date()
            };
            
            updateRobotControlUI(robotId, action === 'start');
            
            // Force status refresh after 1 second
            setTimeout(() => syncRobotStatusFromBackend(robotId), 1000);
        } else {
            showToast(data.message || 'Eroare la control robot', 'error');
        }
        
    } catch (error) {
        console.error(`[Robot Control] Error ${action} ${robotId}:`, error);
        showToast(`Eroare: ${error.message}`, 'error');
    } finally {
        // Reset button state
        setTimeout(() => {
            const startBtn = document.getElementById('robotStartBtn');
            const stopBtn = document.getElementById('robotStopBtn');
            if (startBtn) {
                startBtn.disabled = false;
                startBtn.textContent = '▶️ Start';
            }
            if (stopBtn) {
                stopBtn.disabled = false;
                stopBtn.textContent = '⏹️ Stop';
            }
        }, 1500);
    }
}

async function syncRobotStatusFromBackend(robotId) {
    try {
        let statusEndpoint;
        switch(robotId) {
            case 'v31':
                statusEndpoint = '/api/v31/live_status';
                break;
            case 'v32':
                statusEndpoint = '/api/v32/session_status';
                break;
            case 'v33':
                statusEndpoint = '/api/v33/session_status';
                break;
            default:
                return;
        }
        
        const res = await fetch(`${API_URL}${statusEndpoint}`, {
            headers: getAuthHeaders()
        });
        
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        
        const data = await res.json();
        
        if (data.status === 'success') {
            const isRunning = data.robot_running === true;
            
            robotControlStatus[robotId] = {
                isRunning: isRunning,
                pid: data.robot_pid || null,
                lastCheck: new Date()
            };
            
            updateRobotControlUI(robotId, isRunning);
        }
        
    } catch (error) {
        console.error(`[Robot Sync] Error syncing ${robotId}:`, error);
    }
}

function updateRobotControlUI(robotId, isRunning) {
    const currentRobot = document.getElementById('robotSelector')?.value;
    
    // Map selector value to robotId
    let selectedRobotId;
    switch(currentRobot) {
        case 'v31_tpl': selectedRobotId = 'v31'; break;
        case 'v32_london': selectedRobotId = 'v32'; break;
        case 'v33_ny': selectedRobotId = 'v33'; break;
        default: return;
    }
    
    // Only update UI if this is the currently selected robot
    if (selectedRobotId !== robotId) return;
    
    const startBtn = document.getElementById('robotStartBtn');
    const stopBtn = document.getElementById('robotStopBtn');
    const statusBadge = document.getElementById('robotStatusBadge');
    const robotStatStatus = document.getElementById('robotStatStatus');
    
    if (startBtn) {
        startBtn.disabled = isRunning;
        startBtn.style.opacity = isRunning ? '0.6' : '1';
    }
    
    if (stopBtn) {
        stopBtn.disabled = !isRunning;
        stopBtn.style.opacity = !isRunning ? '0.6' : '1';
    }
    
    if (statusBadge) {
        statusBadge.textContent = isRunning ? '🟢 Running' : '🔴 Stopped';
        statusBadge.style.background = isRunning ? '#22c55e' : '#ef4444';
    }
    
    if (robotStatStatus) {
        robotStatStatus.textContent = isRunning ? '🟢 Active' : '🔴 Inactive';
        robotStatStatus.style.color = isRunning ? '#22c55e' : '#ef4444';
    }
}

async function syncAllRobotStatuses() {
    await Promise.all([
        syncRobotStatusFromBackend('v31'),
        syncRobotStatusFromBackend('v32'),
        syncRobotStatusFromBackend('v33')
    ]);
}

function startRobotStatusSync() {
    if (robotStatusSyncInterval) return;
    
    console.log('[Robot Sync] Starting robot status sync (2s interval)');
    
    // Immediate sync
    syncAllRobotStatuses();
    
    // Set up interval (2 seconds for max 2 sec delay requirement)
    robotStatusSyncInterval = setInterval(syncAllRobotStatuses, 2000);
}

function stopRobotStatusSync() {
    if (robotStatusSyncInterval) {
        clearInterval(robotStatusSyncInterval);
        robotStatusSyncInterval = null;
        console.log('[Robot Sync] Robot status sync stopped');
    }
}

// Robot Control exports
window.controlRobot = controlRobot;
window.syncRobotStatusFromBackend = syncRobotStatusFromBackend;
window.syncAllRobotStatuses = syncAllRobotStatuses;
window.startRobotStatusSync = startRobotStatusSync;
window.stopRobotStatusSync = stopRobotStatusSync;
window.updateRobotControlUI = updateRobotControlUI;

// ═══════════════════════════════════════════════════════════════════════════
// DASHBOARD HEADER STATISTICS - LIVE DATA
// ═══════════════════════════════════════════════════════════════════════════

let dashboardStatsInterval = null;

async function fetchDashboardStats() {
    try {
        // Fetch clients
        const clientsRes = await fetch(`${API_URL}/api/clients`, {
            headers: getAuthHeaders()
        });
        let activeClients = 0;
        let totalProfit = 0;
        let openPositions = 0;
        
        if (clientsRes.ok) {
            const clientsData = await clientsRes.json();
            if (clientsData.status === 'success') {
                activeClients = clientsData.total_active || 0;
                // Calculate total profit from active clients
                if (clientsData.active) {
                    clientsData.active.forEach(client => {
                        totalProfit += client.profit || 0;
                        openPositions += client.positions_count || 0;
                    });
                }
            }
        }
        
        // Fetch positions for more accurate count
        const positionsRes = await fetch(`${API_URL}/api/positions`, {
            headers: getAuthHeaders()
        });
        if (positionsRes.ok) {
            const positionsData = await positionsRes.json();
            if (positionsData.status === 'success' && positionsData.positions) {
                openPositions = positionsData.positions.length;
            }
        }
        
        // Fetch LIVE positions for profit calculation (from laptop EA)
        const openPosRes = await fetch(`${API_URL}/positions`, {
            headers: getAuthHeaders()
        });
        if (openPosRes.ok) {
            const openPosData = await openPosRes.json();
            if (openPosData.status === 'success' && openPosData.positions) {
                // Sum current profit from all open positions
                openPositions = openPosData.positions.length;
                totalProfit = openPosData.positions.reduce((sum, pos) => {
                    return sum + (pos.profit || 0);
                }, 0);
            }
        }
        
        updateDashboardHeader({
            activeClients,
            openPositions,
            totalProfit
        });
        
    } catch (error) {
        console.error('[Dashboard Stats] Error fetching stats:', error);
    }
}

function updateDashboardHeader(stats) {
    // Update Active Clients
    const clientsEl = document.getElementById('kpiClients');
    if (clientsEl) {
        clientsEl.textContent = stats.activeClients;
    }
    
    // Update Open Positions
    const positionsEl = document.getElementById('kpiPositions');
    if (positionsEl) {
        positionsEl.textContent = stats.openPositions;
    }
    
    // Update Total Profit
    const profitEl = document.getElementById('kpiProfit');
    if (profitEl) {
        const profit = stats.totalProfit;
        const formattedProfit = profit >= 0 
            ? `+$${profit.toFixed(2)}` 
            : `-$${Math.abs(profit).toFixed(2)}`;
        profitEl.textContent = formattedProfit;
        profitEl.style.color = profit >= 0 ? '#22c55e' : '#ef4444';
    }
    
    // Update Session Timer / Last Update
    const lastUpdateEl = document.getElementById('lastUpdate');
    if (lastUpdateEl) {
        const now = new Date();
        const hours = now.getHours().toString().padStart(2, '0');
        const minutes = now.getMinutes().toString().padStart(2, '0');
        const seconds = now.getSeconds().toString().padStart(2, '0');
        lastUpdateEl.textContent = `${hours}:${minutes}:${seconds}`;
    }
    
    console.log('[Dashboard Stats] Updated:', stats);
}

function startDashboardStatsPolling() {
    if (dashboardStatsInterval) return;
    
    console.log('[Dashboard Stats] Starting stats polling (5s interval)');
    
    // Immediate update
    fetchDashboardStats();
    
    // Set up interval (5 seconds)
    dashboardStatsInterval = setInterval(fetchDashboardStats, 5000);
}

function stopDashboardStatsPolling() {
    if (dashboardStatsInterval) {
        clearInterval(dashboardStatsInterval);
        dashboardStatsInterval = null;
        console.log('[Dashboard Stats] Stats polling stopped');
    }
}

// Dashboard Stats exports
window.fetchDashboardStats = fetchDashboardStats;
window.startDashboardStatsPolling = startDashboardStatsPolling;
window.stopDashboardStatsPolling = stopDashboardStatsPolling;

// ═══════════════════════════════════════════════════════════════════════════
// CLIENTS & POSITIONS FUNCTIONS
// ═══════════════════════════════════════════════════════════════════════════

async function loadClients() {
    try {
        const res = await fetch(`${API_URL}/api/clients`, {
            headers: getAuthHeaders()
        });
        
        if (!res.ok) throw new Error('Failed to fetch clients');
        
        const data = await res.json();
        if (data.status === 'success') {
            updateClientsTable(data);
            updateGlobalToggleLabel(data);  // ⭐ Update global toggle label
        }
    } catch (error) {
        console.error('[Clients] Error loading clients:', error);
    }
}

function updateClientsTable(data) {
    const tbody = document.querySelector('#clientsTable tbody');
    if (!tbody) return;
    
    // Combine active and inactive clients
    const allClients = [
        ...(data.active || []),
        ...(data.inactive || [])
    ];
    
    if (allClients.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" style="text-align:center;padding:20px;">Niciun client conectat</td></tr>';
        return;
    }
    
    // Create a map of existing rows by login for quick lookup
    const existingRows = new Map();
    tbody.querySelectorAll('tr[data-login]').forEach(row => {
        const login = row.getAttribute('data-login');
        if (login) existingRows.set(login, row);
    });
    
    // Track which clients we've processed
    const processedLogins = new Set();
    
    allClients.forEach((client, index) => {
        const login = String(client.login);
        processedLogins.add(login);
        
        const statusClass = client.is_active ? 'status-online' : 'status-offline';
        const statusText = client.is_active ? 'Online' : 'Offline';
        
        // Check if row already exists
        let row = existingRows.get(login);
        
        if (row) {
            // ⭐ SILENT UPDATE: Update existing row without animation
            row.classList.add('silent-update');
            
            // Update status cell
            const statusCell = row.querySelector('td:first-child .status-badge');
            if (statusCell) {
                statusCell.className = `status-badge ${statusClass}`;
                statusCell.textContent = statusText;
            }
            
            // Update balance
            const balanceCell = row.querySelector('td:nth-child(4)');
            if (balanceCell) balanceCell.textContent = `$${(client.balance || 0).toFixed(2)}`;
            
            // Update equity
            const equityCell = row.querySelector('td:nth-child(5)');
            if (equityCell) equityCell.textContent = `$${(client.equity || 0).toFixed(2)}`;
            
            // Update positions count
            const positionsCell = row.querySelector('td:nth-child(6)');
            if (positionsCell) positionsCell.textContent = client.positions_count || 0;
            
            // Update profit
            const profitCell = row.querySelector('td:nth-child(7)');
            if (profitCell) {
                const profit = client.profit || 0;
                profitCell.textContent = `${profit >= 0 ? '+' : ''}$${profit.toFixed(2)}`;
                profitCell.style.color = profit >= 0 ? '#22c55e' : '#ef4444';
            }
            
            // Update toggle checkbox without triggering onchange
            const toggleInput = row.querySelector('td:nth-child(8) input[type="checkbox"]');
            if (toggleInput && toggleInput.checked !== client.enabled) {
                toggleInput.checked = client.enabled;
            }
        } else {
            // Create new row for new client
            row = document.createElement('tr');
            row.setAttribute('data-login', login);
            
            row.innerHTML = `
                <td><span class="status-badge ${statusClass}">${statusText}</span></td>
                <td>${client.login}</td>
                <td>${client.name || '-'}</td>
                <td>$${(client.balance || 0).toFixed(2)}</td>
                <td>$${(client.equity || 0).toFixed(2)}</td>
                <td>${client.positions_count || 0}</td>
                <td style="color: ${(client.profit || 0) >= 0 ? '#22c55e' : '#ef4444'}">${client.profit >= 0 ? '+' : ''}$${(client.profit || 0).toFixed(2)}</td>
                <td>
                    <label class="toggle-switch-compact" style="transform: scale(0.85);">
                        <input type="checkbox" ${client.enabled ? 'checked' : ''} 
                               onchange="toggleClient(${client.login}, this.checked)">
                        <span class="toggle-slider-compact"></span>
                    </label>
                </td>
            `;
            tbody.appendChild(row);
        }
    });
    
    // Remove rows for clients that no longer exist
    existingRows.forEach((row, login) => {
        if (!processedLogins.has(login)) {
            row.remove();
        }
    });
}

async function loadPositions() {
    try {
        // Use /positions for LIVE positions from MT5 (via laptop EA)
        // This reads from clients_cache which is updated in real-time
        const res = await fetch(`${API_URL}/positions`, {
            headers: getAuthHeaders()
        });
        
        if (!res.ok) throw new Error('Failed to fetch positions');
        
        const data = await res.json();
        if (data.status === 'success') {
            updatePositionsTable(data.positions || []);
        }
    } catch (error) {
        console.error('[Positions] Error loading positions:', error);
    }
}

function updatePositionsTable(positions) {
    const tbody = document.querySelector('#positionsTable tbody');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    if (positions.length === 0) {
        tbody.innerHTML = '<tr><td colspan="10" style="text-align:center;padding:20px;">Nicio poziție deschisă</td></tr>';
        return;
    }
    
    positions.forEach(pos => {
        const row = document.createElement('tr');
        const profit = pos.current_profit || pos.profit || 0;
        const profitColor = profit >= 0 ? '#22c55e' : '#ef4444';
        const typeColor = pos.type === 'BUY' ? '#22c55e' : '#ef4444';
        
        row.innerHTML = `
            <td>${pos.ticket}</td>
            <td>${pos.login || '-'}</td>
            <td>${pos.symbol}</td>
            <td><span style="color: ${typeColor}; font-weight: 600;">${pos.type}</span></td>
            <td>${pos.volume}</td>
            <td>${pos.open_price?.toFixed(5) || '-'}</td>
            <td>${pos.current_price?.toFixed(5) || pos.open_price?.toFixed(5) || '-'}</td>
            <td style="color: ${profitColor}; font-weight: 600;">${profit >= 0 ? '+' : ''}$${profit.toFixed(2)}</td>
            <td>$${(pos.swap || 0).toFixed(2)}</td>
            <td><button onclick="closePosition(${pos.ticket})" style="background: #ef4444; color: white; border: none; padding: 4px 8px; border-radius: 4px; cursor: pointer;">Închide</button></td>
        `;
        tbody.appendChild(row);
    });
}

// Clients & Positions exports
window.loadClients = loadClients;
window.loadPositions = loadPositions;
window.updateClientsTable = updateClientsTable;
window.updatePositionsTable = updatePositionsTable;

// Toggle all clients at once
async function toggleAllClients(enable) {
    try {
        console.log(`[Clients] ${enable ? 'Enabling' : 'Disabling'} all clients`);
        
        // Update label immediately for responsiveness
        const toggleLabel = document.getElementById('toggleLabel');
        if (toggleLabel) {
            toggleLabel.textContent = enable ? 'Toți Activi' : 'Activează Toți';
        }
        
        // Get current clients
        const res = await fetch(`${API_URL}/api/clients`, {
            headers: getAuthHeaders()
        });
        
        if (!res.ok) throw new Error('Failed to fetch clients');
        
        const data = await res.json();
        if (data.status !== 'success') return;
        
        // Combine active and inactive
        const allClients = [...(data.active || []), ...(data.inactive || [])];
        
        // Count clients that need toggling
        const clientsToToggle = allClients.filter(c => c.enabled !== enable);
        
        if (clientsToToggle.length === 0) {
            showToast(`Toți clienții sunt deja ${enable ? 'activați' : 'dezactivați'}`, 'info');
            return;
        }
        
        // Toggle each client
        let successCount = 0;
        for (const client of clientsToToggle) {
            try {
                await toggleClient(client.login, enable);
                successCount++;
            } catch (e) {
                console.error(`[Clients] Failed to toggle client ${client.login}:`, e);
            }
        }
        
        // Reload clients table (silent update)
        await loadClients();
        
        showToast(`${successCount}/${clientsToToggle.length} clienți ${enable ? 'activați' : 'dezactivați'}`, 'success');
        
    } catch (error) {
        console.error('[Clients] Error toggling all clients:', error);
        showToast('Eroare la modificarea clienților', 'error');
        
        // Revert label on error
        const toggleLabel = document.getElementById('toggleLabel');
        if (toggleLabel) {
            toggleLabel.textContent = 'Activează Toți';
        }
    }
}

// Toggle single client
async function toggleClient(login, enable) {
    try {
        const endpoint = enable 
            ? `/api/client/${login}/enable`
            : `/api/client/${login}/disable`;
        
        const res = await fetch(`${API_URL}${endpoint}`, {
            method: 'POST',
            headers: getAuthHeaders()
        });
        
        if (!res.ok) throw new Error(`Failed to ${enable ? 'enable' : 'disable'} client`);
        
        console.log(`[Clients] Client ${login} ${enable ? 'enabled' : 'disabled'}`);
        
        // Silent reload of clients to update UI
        await loadClients();
        
    } catch (error) {
        console.error(`[Clients] Error toggling client ${login}:`, error);
        showToast(`Eroare la ${enable ? 'activarea' : 'dezactivarea'} clientului ${login}`, 'error');
        throw error;
    }
}

// Update global toggle label based on current client states
function updateGlobalToggleLabel(clients) {
    const allClients = [...(clients.active || []), ...(clients.inactive || [])];
    if (allClients.length === 0) return;
    
    const allEnabled = allClients.every(c => c.enabled);
    const anyEnabled = allClients.some(c => c.enabled);
    
    const toggleLabel = document.getElementById('toggleLabel');
    const globalToggle = document.getElementById('globalClientToggle');
    
    if (toggleLabel) {
        if (allEnabled) {
            toggleLabel.textContent = 'Toți Activi';
        } else if (anyEnabled) {
            toggleLabel.textContent = 'Parțial';
        } else {
            toggleLabel.textContent = 'Activează Toți';
        }
    }
    
    // Update checkbox without triggering onchange
    if (globalToggle) {
        globalToggle.checked = allEnabled;
    }
}

window.toggleAllClients = toggleAllClients;
window.toggleClient = toggleClient;
window.updateGlobalToggleLabel = updateGlobalToggleLabel;

// ═══════════════════════════════════════════════════════════════════════════
// ACTIVE POSITIONS - LIVE from MT5 (via /positions endpoint)
// ═══════════════════════════════════════════════════════════════════════════

async function loadActiveCommands() {
    try {
        // Fetch LIVE positions from cache (via /positions endpoint)
        // This reads from clients_cache which is updated by the laptop EA via /update
        const res = await fetch(`${API_URL}/positions`, {
            headers: getAuthHeaders()
        });

        if (!res.ok) throw new Error('Failed to fetch live positions');

        const data = await res.json();
        if (data.status === 'success') {
            updateActivePositionsTable(data.positions || [], data.count || 0);
        }
    } catch (error) {
        console.error('[ActivePositions] Error loading live positions:', error);
        const tbody = document.getElementById('commandLogBody');
        if (tbody) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="8" style="text-align:center;padding:30px;color:#ef4444;">
                        <i data-lucide="alert-circle" style="width:24px;height:24px;margin-bottom:8px;display:block;margin-left:auto;margin-right:auto;"></i>
                        Eroare la citirea pozițiilor live<br>
                        <small style="color:#64748b;">${error.message}</small>
                    </td>
                </tr>
            `;
        }
    }
}

function updateActivePositionsTable(positions, totalCount) {
    const tbody = document.getElementById('commandLogBody');
    const countBadge = document.getElementById('commandLogCount');

    if (!tbody) return;

    // Update count badge
    if (countBadge) {
        countBadge.textContent = `${totalCount} Poziții`;
        countBadge.style.background = totalCount > 0 ? '#22c55e' : '#64748b';
    }

    if (positions.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="8" style="text-align:center;padding:30px;color:#64748b;">
                    <i data-lucide="check-circle" style="width:24px;height:24px;margin-bottom:8px;display:block;margin-left:auto;margin-right:auto;color:#22c55e;"></i>
                    Nicio poziție deschisă în MT5
                </td>
            </tr>
        `;
        return;
    }

    tbody.innerHTML = positions.map(pos => {
        const profit = pos.current_profit || pos.profit || 0;
        const profitColor = profit >= 0 ? '#22c55e' : '#ef4444';
        const typeColor = pos.type === 'BUY' ? '#22c55e' : '#ef4444';

        return `
            <tr style="animation: fadeIn 0.3s ease;">
                <td style="font-family:monospace;font-size:12px;">${pos.ticket}</td>
                <td>${pos.login || '-'}</td>
                <td style="font-weight:600;">${pos.symbol}</td>
                <td><span style="color:${typeColor};font-weight:600;">${pos.type}</span></td>
                <td>${pos.volume}</td>
                <td style="font-family:monospace;">${pos.open_price?.toFixed(5) || '-'}</td>
                <td style="font-family:monospace;">${pos.current_price?.toFixed(5) || '-'}</td>
                <td style="color:${profitColor};font-weight:600;">${profit >= 0 ? '+' : ''}$${profit.toFixed(2)}</td>
            </tr>
        `;
    }).join('');
}

window.loadActiveCommands = loadActiveCommands;
window.updateActivePositionsTable = updateActivePositionsTable;

// ═══════════════════════════════════════════════════════════════════════════
// HISTORY (ISTORIC TRANZACȚII) - Closed positions from MT5
// ═══════════════════════════════════════════════════════════════════════════

let historyFilter = {
    period: 'all',
    symbol: 'all',
    profit: 'all'
};

function setHistoryFilter(type, value) {
    historyFilter[type] = value;
    loadHistory();
}

async function loadHistory() {
    try {
        const res = await fetch(`${API_URL}/api/history?limit=50`, {
            headers: getAuthHeaders()
        });
        
        if (!res.ok) throw new Error('Failed to fetch history');
        
        const data = await res.json();
        if (data.status === 'success') {
            updateHistoryTable(data.history || []);
        }
    } catch (error) {
        console.error('[History] Error loading history:', error);
    }
}

function updateHistoryTable(history) {
    const tbody = document.querySelector('#historyTable tbody');
    if (!tbody) return;
    
    // Apply filters
    let filtered = history;
    
    if (historyFilter.profit === 'positive') {
        filtered = filtered.filter(h => (h.profit || 0) > 0);
    } else if (historyFilter.profit === 'negative') {
        filtered = filtered.filter(h => (h.profit || 0) < 0);
    }
    
    if (historyFilter.symbol !== 'all') {
        filtered = filtered.filter(h => h.symbol === historyFilter.symbol);
    }
    
    tbody.innerHTML = '';
    
    if (filtered.length === 0) {
        tbody.innerHTML = '<tr><td colspan="10" style="text-align:center;padding:20px;">Nicio tranzacție în istoric</td></tr>';
        return;
    }
    
    filtered.forEach(trade => {
        const row = document.createElement('tr');
        const profit = trade.profit || 0;
        const profitColor = profit >= 0 ? '#22c55e' : '#ef4444';
        const typeColor = trade.type === 'BUY' ? '#22c55e' : '#ef4444';
        const netProfit = profit - (trade.commission || 0) - (trade.swap || 0);
        
        const openTime = trade.open_time ? new Date(trade.open_time).toLocaleDateString('ro-RO') : '-';
        const duration = trade.duration_minutes ? `${Math.floor(trade.duration_minutes / 60)}h ${trade.duration_minutes % 60}m` : '-';
        
        row.innerHTML = `
            <td style="font-family:monospace;font-size:11px;">${trade.ticket}</td>
            <td style="font-size:12px;">${openTime}</td>
            <td>${trade.login || '-'}</td>
            <td style="font-weight:600;">${trade.symbol}</td>
            <td><span style="color:${typeColor};font-weight:600;">${trade.type}</span></td>
            <td style="color:${profitColor};font-weight:600;">${profit >= 0 ? '+' : ''}$${profit.toFixed(2)}</td>
            <td style="color:#64748b;">$${(trade.commission || 0).toFixed(2)}</td>
            <td style="color:${netProfit >= 0 ? '#22c55e' : '#ef4444'};font-weight:600;">${netProfit >= 0 ? '+' : ''}$${netProfit.toFixed(2)}</td>
            <td style="font-size:12px;">${duration}</td>
            <td style="font-size:12px;">${calculateRR(trade)}</td>
        `;
        tbody.appendChild(row);
    });
    
    // Update symbol filter options
    updateHistorySymbolFilter(history);
}

function calculateRR(trade) {
    if (!trade.sl || !trade.tp || trade.sl === 0) return '-';
    const risk = Math.abs(trade.open_price - trade.sl);
    const reward = Math.abs(trade.tp - trade.open_price);
    if (risk === 0) return '-';
    return `1:${(reward / risk).toFixed(1)}`;
}

function updateHistorySymbolFilter(history) {
    const select = document.getElementById('historyFilterSymbol');
    if (!select) return;
    
    const symbols = [...new Set(history.map(h => h.symbol))].sort();
    const currentValue = select.value;
    
    select.innerHTML = '<option value="all">Toate Symbolurile</option>';
    symbols.forEach(symbol => {
        select.innerHTML += `<option value="${symbol}">${symbol}</option>`;
    });
    
    select.value = currentValue;
}

window.loadHistory = loadHistory;
window.setHistoryFilter = setHistoryFilter;
window.updateHistoryTable = updateHistoryTable;

// ═══════════════════════════════════════════════════════════════════════════
// TRACKING TRANZACȚII - Real-time command tracking from robots
// ═══════════════════════════════════════════════════════════════════════════

let trackingFilter = {
    type: 'all',
    symbol: 'all'
};

function setTrackingFilter(type, value) {
    trackingFilter[type] = value;
    loadTracking();
}

async function loadTracking() {
    try {
        console.log('[Tracking] Loading tracking data...');
        
        // Fetch from history endpoint which has tracking data
        const res = await fetch(`${API_URL}/api/history?limit=100`, {
            headers: getAuthHeaders()
        });
        
        if (!res.ok) throw new Error('Failed to fetch tracking data');
        
        const data = await res.json();
        if (data.status === 'success') {
            updateTrackingTable(data.history || []);
        }
    } catch (error) {
        console.error('[Tracking] Error loading tracking:', error);
        const tbody = document.getElementById('trackingBody');
        if (tbody) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="13" style="text-align:center;padding:30px;color:#ef4444;">
                        <i data-lucide="alert-circle" style="width:24px;height:24px;margin-bottom:8px;display:block;margin-left:auto;margin-right:auto;"></i>
                        Eroare la încărcarea tracking-ului<br>
                        <small style="color:#64748b;">${error.message}</small>
                    </td>
                </tr>
            `;
        }
    }
}

function updateTrackingTable(trades) {
    const tbody = document.getElementById('trackingBody');
    if (!tbody) return;
    
    // Apply filters
    let filtered = trades;
    
    if (trackingFilter.type === 'open') {
        filtered = filtered.filter(t => !t.close_time);
    } else if (trackingFilter.type === 'closed') {
        filtered = filtered.filter(t => t.close_time);
    }
    
    if (trackingFilter.symbol !== 'all') {
        filtered = filtered.filter(t => t.symbol === trackingFilter.symbol);
    }
    
    tbody.innerHTML = '';
    
    if (filtered.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="13" style="text-align:center;padding:30px;color:#64748b;">
                    <i data-lucide="git-commit" style="width:24px;height:24px;margin-bottom:8px;display:block;margin-left:auto;margin-right:auto;color:#64748b;"></i>
                    Nicio tranzacție în tracking
                </td>
            </tr>
        `;
        return;
    }
    
    filtered.forEach(trade => {
        const row = document.createElement('tr');
        row.style.animation = 'fadeIn 0.3s ease';
        
        const profit = trade.profit || 0;
        const commission = trade.commission || 0;
        const swap = trade.swap || 0;
        const netProfit = profit - Math.abs(commission) - Math.abs(swap);
        
        const profitColor = netProfit >= 0 ? '#22c55e' : '#ef4444';
        const typeColor = trade.type === 'BUY' ? '#22c55e' : '#ef4444';
        
        // Determine status
        const isOpen = !trade.close_time;
        const isModified = trade.modified_by && trade.modified_by !== 'Unknown';
        
        let statusBadge, statusText;
        if (isOpen) {
            statusBadge = '#22c55e';
            statusText = '🟢 Deschis';
        } else if (isModified) {
            statusBadge = '#f59e0b';
            statusText = '🟡 Modificat';
        } else {
            statusBadge = '#64748b';
            statusText = '⚪ Închis';
        }
        
        // Format dates
        const dateTime = trade.open_time ? new Date(trade.open_time).toLocaleString('ro-RO', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        }) : '-';
        
        // Format duration
        const duration = trade.duration_minutes ? 
            trade.duration_minutes < 60 ? 
                `${trade.duration_minutes}m` : 
                `${Math.floor(trade.duration_minutes / 60)}h ${trade.duration_minutes % 60}m` 
            : isOpen ? 'Deschis' : '-';
        
        // Format "opened/closed/modified by"
        const openedBy = trade.opened_by && trade.opened_by !== 'Unknown' ? 
            `<span style="color:#22c55e;font-size:11px;">${trade.opened_by}</span>` : 
            '<span style="color:#64748b;font-size:11px;">-</span>';
        
        const closedBy = trade.closed_by && trade.closed_by !== 'Unknown' ? 
            `<span style="color:#ef4444;font-size:11px;">${trade.closed_by}</span>` : 
            '<span style="color:#64748b;font-size:11px;">-</span>';
        
        const modifiedBy = trade.modified_by && trade.modified_by !== 'Unknown' ? 
            `<span style="color:#f59e0b;font-size:11px;">${trade.modified_by}</span>` : 
            '<span style="color:#64748b;font-size:11px;">-</span>';
        
        row.innerHTML = `
            <td style="font-size:12px;white-space:nowrap;">${dateTime}</td>
            <td style="font-family:monospace;font-size:11px;">${trade.ticket}</td>
            <td style="font-weight:600;">${trade.symbol}</td>
            <td><span style="color:${typeColor};font-weight:600;font-size:12px;">${trade.type}</span></td>
            <td>${trade.volume}</td>
            <td>${openedBy}</td>
            <td>${closedBy}</td>
            <td>${modifiedBy}</td>
            <td style="color:${profitColor};font-weight:600;">${profit >= 0 ? '+' : ''}$${profit.toFixed(2)}</td>
            <td style="color:#64748b;font-size:12px;">$${Math.abs(commission).toFixed(2)}</td>
            <td style="color:${profitColor};font-weight:600;">${netProfit >= 0 ? '+' : ''}$${netProfit.toFixed(2)}</td>
            <td style="font-size:12px;">${duration}</td>
            <td><span style="background:${statusBadge};color:#fff;padding:2px 6px;border-radius:4px;font-size:11px;">${statusText}</span></td>
        `;
        tbody.appendChild(row);
    });
    
    // Update symbol filter
    updateTrackingSymbolFilter(trades);
}

function updateTrackingSymbolFilter(trades) {
    const select = document.getElementById('trackingFilterSymbol');
    if (!select) return;
    
    const symbols = [...new Set(trades.map(t => t.symbol))].sort();
    const currentValue = select.value;
    
    select.innerHTML = '<option value="all">Toate Simbolurile</option>';
    symbols.forEach(symbol => {
        select.innerHTML += `<option value="${symbol}">${symbol}</option>`;
    });
    
    select.value = currentValue;
}

window.loadTracking = loadTracking;
window.setTrackingFilter = setTrackingFilter;
window.updateTrackingTable = updateTrackingTable;

// Start periodic refresh
setInterval(loadClients, 10000);  // Refresh every 10 seconds
setInterval(loadPositions, 10000); // Refresh every 10 seconds
setInterval(loadHistory, 30000);   // Refresh history every 30 seconds
setInterval(loadTracking, 5000);   // Refresh tracking every 5 seconds (real-time)

console.log('[Dashboard] ✅ Tracking Tranzacții loaded - Real-time updates every 5s');
console.log('[Dashboard] Functions available: switchRobot, startV31Polling, startV32Polling, startV33Polling');
console.log('[Dashboard] Health check functions: loadSystemHealth, startHealthCheckPolling');
console.log('[Dashboard] Connection functions: checkAllRobotConnections, startRobotStatusPolling');
console.log('[Dashboard] Dashboard stats: startDashboardStatsPolling, fetchDashboardStats');
