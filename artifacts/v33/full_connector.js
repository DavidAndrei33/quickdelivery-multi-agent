/**
 * 🗽 V33 NY BREAKOUT DASHBOARD - FULL CONNECTOR
 * =============================================
 * Comprehensive connector for V33 New York Breakout Dashboard
 * Author: BrainMaker AI
 * Version: 33.1.0
 */

const API_URL = window.location.origin || '';

// ═══════════════════════════════════════════════════════════════════════════
// 🗽 V33 NY BREAKOUT DASHBOARD - COMPLETE IMPLEMENTATION
// ═══════════════════════════════════════════════════════════════════════════

let v33DashboardInterval = null;
let v33SymbolStates = new Map();
let v33TradeHistory = [];
let v33SessionData = {
    ny_time: null,
    session_phase: 'BEFORE_SESSION',
    is_active: false,
    time_remaining_minutes: 0
};

// ═══════════════════════════════════════════════════════════════════════════
// SECTION 1: NY TIME WITH SECONDS (HH:MM:SS)
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Updates the NY Time display with seconds
 */
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
    
    // Also update session timer since it depends on NY time
    updateV33SessionTimer(nyTime);
    
    return `${hours}:${minutes}:${seconds}`;
}

/**
 * Updates the V33 Session Timer display
 */
function updateV33SessionTimer(nyTime) {
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
    const orProgressEl = document.getElementById('v33ORProgress');
    
    if (!timerDisplay || !phaseDisplay) return;
    
    // Calculate OR progress (during OR formation period)
    if (currentMinutes >= sessionStart && currentMinutes < orEnd) {
        const orSecondsElapsed = currentSeconds - (sessionStart * 60);
        const orTotalSeconds = 15 * 60; // 15 minutes in seconds
        const orProgress = Math.min(100, (orSecondsElapsed / orTotalSeconds) * 100);
        
        if (orProgressEl) {
            orProgressEl.style.width = `${orProgress}%`;
            orProgressEl.style.background = `linear-gradient(90deg, #3b82f6 ${orProgress}%, rgba(59, 130, 246, 0.2) ${orProgress}%)`;
        }
    } else {
        if (orProgressEl) {
            orProgressEl.style.width = currentMinutes >= orEnd ? '100%' : '0%';
        }
    }
    
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
        v33SessionData.session_phase = 'BEFORE_SESSION';
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
        v33SessionData.session_phase = 'OPENING_RANGE';
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
        v33SessionData.session_phase = 'MAIN_SESSION';
        v33SessionData.is_active = true;
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
        v33SessionData.session_phase = 'EXTENDED_SESSION';
    } else {
        // After session
        timerDisplay.textContent = 'ENDED';
        timerDisplay.style.color = '#64748b';
        phaseDisplay.textContent = 'Session Ended';
        if (badgeEl) {
            badgeEl.textContent = '⏹️ Closed';
            badgeEl.style.background = '#64748b';
        }
        v33SessionData.session_phase = 'AFTER_SESSION';
        v33SessionData.is_active = false;
    }
}

// ═══════════════════════════════════════════════════════════════════════════
// SECTION 2: OPENING RANGE (13:00-13:15) - OR HIGH, OR LOW, RANGE, Current Price
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Updates the Opening Range display with OR data
 */
function updateV33OpeningRange(data) {
    const orHighEl = document.getElementById('v33ORHigh');
    const orLowEl = document.getElementById('v33ORLow');
    const orRangeEl = document.getElementById('v33ORRange');
    const orMidEl = document.getElementById('v33ORMid');
    const currentPriceEl = document.getElementById('v33CurrentPrice');
    const priceDistanceEl = document.getElementById('v33PriceDistanceOR');
    const orStatusEl = document.getElementById('v33ORStatus');
    
    if (!data) return;
    
    const orHigh = parseFloat(data.or_high) || 0;
    const orLow = parseFloat(data.or_low) || 0;
    const currentPrice = parseFloat(data.current_price) || 0;
    
    if (orHigh > 0 && orLow > 0) {
        const orRange = orHigh - orLow;
        const orMid = (orHigh + orLow) / 2;
        const orRangePips = (orRange * 10000).toFixed(1);
        
        if (orHighEl) orHighEl.textContent = orHigh.toFixed(5);
        if (orLowEl) orLowEl.textContent = orLow.toFixed(5);
        if (orRangeEl) orRangeEl.textContent = `${orRangePips} pips`;
        if (orMidEl) orMidEl.textContent = orMid.toFixed(5);
        
        // Update OR status based on range
        if (orStatusEl) {
            if (orRangePips > 30) {
                orStatusEl.textContent = '⚠️ Wide OR';
                orStatusEl.style.color = '#ef4444';
            } else if (orRangePips > 25) {
                orStatusEl.textContent = '⚡ Acceptable';
                orStatusEl.style.color = '#f59e0b';
            } else {
                orStatusEl.textContent = '✅ Good';
                orStatusEl.style.color = '#22c55e';
            }
        }
    }
    
    if (currentPriceEl && currentPrice > 0) {
        currentPriceEl.textContent = currentPrice.toFixed(5);
        
        // Calculate distance from OR
        if (priceDistanceEl && orHigh > 0 && orLow > 0) {
            let distanceText = '';
            let distanceColor = '#64748b';
            
            if (currentPrice > orHigh) {
                const pipsAbove = ((currentPrice - orHigh) * 10000).toFixed(1);
                distanceText = `+${pipsAbove} pips above OR High`;
                distanceColor = '#22c55e';
            } else if (currentPrice < orLow) {
                const pipsBelow = ((orLow - currentPrice) * 10000).toFixed(1);
                distanceText = `-${pipsBelow} pips below OR Low`;
                distanceColor = '#ef4444';
            } else {
                const toHigh = ((orHigh - currentPrice) * 10000).toFixed(1);
                const toLow = ((currentPrice - orLow) * 10000).toFixed(1);
                distanceText = `${toHigh}p to High / ${toLow}p to Low`;
                distanceColor = '#64748b';
            }
            
            priceDistanceEl.textContent = distanceText;
            priceDistanceEl.style.color = distanceColor;
        }
    }
}

/**
 * Fetches OR data from API
 */
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

// ═══════════════════════════════════════════════════════════════════════════
// SECTION 3: PRE-NY SESSION (08:00-13:00) - High, Low, Range, Compression Status
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Updates the Pre-NY Session display
 */
function updateV33PreSession(data) {
    const preHighEl = document.getElementById('v33PreHigh');
    const preLowEl = document.getElementById('v33PreLow');
    const preRangeEl = document.getElementById('v33PreRange');
    const compressionStatusEl = document.getElementById('v33CompressionStatus');
    const compressionIconEl = document.getElementById('v33CompressionIcon');
    const compressionTextEl = document.getElementById('v33CompressionText');
    const sessionRangeBar = document.getElementById('v33SessionRangeBar');
    
    if (!data) return;
    
    const preHigh = parseFloat(data.pre_session_high) || 0;
    const preLow = parseFloat(data.pre_session_low) || 0;
    const isCompressed = data.is_compressed || false;
    const preRangePips = parseFloat(data.pre_session_range_pips) || 0;
    
    if (preHighEl) preHighEl.textContent = preHigh > 0 ? preHigh.toFixed(5) : '--.-----';
    if (preLowEl) preLowEl.textContent = preLow > 0 ? preLow.toFixed(5) : '--.-----';
    if (preRangeEl) preRangeEl.textContent = preRangePips > 0 ? `${preRangePips.toFixed(1)} pips` : '-- pips';
    
    // Compression status
    if (compressionStatusEl) {
        if (isCompressed) {
            compressionStatusEl.textContent = '✅ Compressed';
            compressionStatusEl.style.color = '#22c55e';
            compressionStatusEl.style.background = 'rgba(34, 197, 94, 0.1)';
        } else {
            compressionStatusEl.textContent = '❌ Expanded';
            compressionStatusEl.style.color = '#ef4444';
            compressionStatusEl.style.background = 'rgba(239, 68, 68, 0.1)';
        }
    }
    
    if (compressionIconEl) {
        compressionIconEl.textContent = isCompressed ? '✅' : '⚠️';
    }
    
    if (compressionTextEl) {
        compressionTextEl.textContent = isCompressed 
            ? 'Market is compressed - Breakout potential HIGH' 
            : 'Market is expanded - Breakout potential LOW';
        compressionTextEl.style.color = isCompressed ? '#22c55e' : '#ef4444';
    }
    
    // Update range bar visualization
    if (sessionRangeBar) {
        const maxExpectedRange = 50; // 50 pips max for visual
        const percentage = Math.min(100, (preRangePips / maxExpectedRange) * 100);
        sessionRangeBar.style.width = `${percentage}%`;
        sessionRangeBar.style.background = isCompressed 
            ? 'linear-gradient(90deg, #22c55e, #16a34a)'
            : 'linear-gradient(90deg, #ef4444, #dc2626)';
    }
}

/**
 * Fetches Pre-Session data from API
 */
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

// ═══════════════════════════════════════════════════════════════════════════
// SECTION 4: BREAKOUT DETECTION - Status, Type, Body %, Wick %, Signal
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Updates the Breakout Detection display
 */
function updateV33BreakoutStatus(data) {
    const breakoutStatusEl = document.getElementById('v33BreakoutStatus');
    const setupTypeEl = document.getElementById('v33SetupType');
    const bodyPercentEl = document.getElementById('v33BodyPercent');
    const wickPercentEl = document.getElementById('v33WickPercent');
    const signalEl = document.getElementById('v33Signal');
    const signalBox = document.getElementById('v33SignalBox');
    const breakoutDirectionEl = document.getElementById('v33BreakoutDirection');
    const breakoutConfidenceEl = document.getElementById('v33BreakoutConfidence');
    const entryPriceEl = document.getElementById('v33EntryPrice');
    const slPriceEl = document.getElementById('v33SLPrice');
    const tpPriceEl = document.getElementById('v33TPPrice');
    const rrRatioEl = document.getElementById('v33RRRatio');
    
    if (!data) return;
    
    const status = data.breakout_status || 'WAITING';
    const setupType = data.setup_type || '-';
    const bodyPercent = parseFloat(data.body_percent) || 0;
    const wickPercent = parseFloat(data.wick_percent) || 0;
    const signal = data.signal || 'WAIT';
    const direction = data.direction || 'NONE';
    const confidence = data.confidence || 'B';
    const entryPrice = parseFloat(data.entry_price) || 0;
    const slPrice = parseFloat(data.sl_price) || 0;
    const tpPrice = parseFloat(data.tp_price) || 0;
    
    // Status display
    if (breakoutStatusEl) {
        const statusMap = {
            'WAITING': { text: '⏳ Waiting for OR...', color: '#64748b' },
            'IN_OR': { text: '📊 OR Formation...', color: '#3b82f6' },
            'SCANNING': { text: '🔍 Scanning for Breakout...', color: '#f59e0b' },
            'DETECTED': { text: '🔥 BREAKOUT DETECTED!', color: '#22c55e' },
            'TYPE_B_PENDING': { text: '⏳ Type B Pending...', color: '#8b5cf6' },
            'INVALID': { text: '❌ Invalid Breakout', color: '#ef4444' },
            'EXPIRED': { text: '⏰ Setup Expired', color: '#64748b' }
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
        bodyPercentEl.textContent = bodyPercent > 0 ? `${bodyPercent.toFixed(1)}%` : '--%';
        bodyPercentEl.style.color = bodyPercent >= 60 ? '#22c55e' : bodyPercent >= 50 ? '#f59e0b' : '#ef4444';
        
        // Add progress bar
        const bodyBar = document.getElementById('v33BodyBar');
        if (bodyBar) {
            bodyBar.style.width = `${Math.min(100, bodyPercent)}%`;
            bodyBar.style.background = bodyPercent >= 60 
                ? 'linear-gradient(90deg, #22c55e, #16a34a)'
                : 'linear-gradient(90deg, #ef4444, #dc2626)';
        }
    }
    
    // Wick Percent
    if (wickPercentEl) {
        wickPercentEl.textContent = wickPercent > 0 ? `${wickPercent.toFixed(1)}%` : '--%';
        wickPercentEl.style.color = wickPercent <= 30 ? '#22c55e' : wickPercent <= 40 ? '#f59e0b' : '#ef4444';
        
        // Add progress bar
        const wickBar = document.getElementById('v33WickBar');
        if (wickBar) {
            wickBar.style.width = `${Math.min(100, wickPercent)}%`;
            wickBar.style.background = wickPercent <= 30 
                ? 'linear-gradient(90deg, #22c55e, #16a34a)'
                : 'linear-gradient(90deg, #ef4444, #dc2626)';
        }
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
    
    // Direction
    if (breakoutDirectionEl) {
        breakoutDirectionEl.textContent = direction === 'BUY' ? '🟢 LONG' : direction === 'SELL' ? '🔴 SHORT' : '⚪ NONE';
        breakoutDirectionEl.style.color = direction === 'BUY' ? '#22c55e' : direction === 'SELL' ? '#ef4444' : '#64748b';
    }
    
    // Confidence
    if (breakoutConfidenceEl) {
        const confColors = { 'A+': '#22c55e', 'A': '#22c55e', 'B': '#f59e0b', 'C': '#ef4444' };
        breakoutConfidenceEl.textContent = confidence;
        breakoutConfidenceEl.style.color = confColors[confidence] || '#64748b';
    }
    
    // Entry/SL/TP
    if (entryPriceEl && entryPrice > 0) entryPriceEl.textContent = entryPrice.toFixed(5);
    if (slPriceEl && slPrice > 0) slPriceEl.textContent = slPrice.toFixed(5);
    if (tpPriceEl && tpPrice > 0) tpPriceEl.textContent = tpPrice.toFixed(5);
    
    // R:R Ratio
    if (rrRatioEl && entryPrice > 0 && slPrice > 0 && tpPrice > 0) {
        const risk = Math.abs(entryPrice - slPrice);
        const reward = Math.abs(tpPrice - entryPrice);
        const rr = risk > 0 ? (reward / risk).toFixed(2) : '0.00';
        rrRatioEl.textContent = `1:${rr}`;
        rrRatioEl.style.color = parseFloat(rr) >= 2.0 ? '#22c55e' : parseFloat(rr) >= 1.5 ? '#f59e0b' : '#ef4444';
    }
}

/**
 * Fetches Breakout Status from API
 */
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

// ═══════════════════════════════════════════════════════════════════════════
// SECTION 5: DAILY STATISTICS - Trades, Win/Loss, P&L, Type B Pending
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Updates the Daily Statistics display
 */
function updateV33DailyStats(data) {
    const tradesCountEl = document.getElementById('v33TradesCount');
    const winLossEl = document.getElementById('v33WinLoss');
    const totalPnLEl = document.getElementById('v33TotalPnL');
    const typeBPendingEl = document.getElementById('v33TypeBPending');
    const winRateEl = document.getElementById('v33WinRate');
    const avgWinEl = document.getElementById('v33AvgWin');
    const avgLossEl = document.getElementById('v33AvgLoss');
    const maxDrawdownEl = document.getElementById('v33MaxDrawdown');
    const dailyLimitEl = document.getElementById('v33DailyLimit');
    const lossLimitEl = document.getElementById('v33LossLimit');
    
    if (!data) return;
    
    const tradesCount = data.trades_count || 0;
    const wins = data.wins || 0;
    const losses = data.losses || 0;
    const totalPnL = parseFloat(data.total_pnl) || 0;
    const typeBPending = data.type_b_pending || false;
    const avgWin = parseFloat(data.avg_win) || 0;
    const avgLoss = parseFloat(data.avg_loss) || 0;
    const maxDrawdown = parseFloat(data.max_drawdown) || 0;
    
    // Trades count
    if (tradesCountEl) {
        tradesCountEl.textContent = `${tradesCount}/2`;
        tradesCountEl.style.color = tradesCount >= 2 ? '#ef4444' : '#22c55e';
    }
    
    // Win/Loss
    if (winLossEl) {
        winLossEl.textContent = `${wins}/${losses}`;
        const winRate = (wins + losses) > 0 ? (wins / (wins + losses) * 100) : 0;
        winLossEl.style.color = winRate >= 50 ? '#22c55e' : '#f59e0b';
    }
    
    // Win Rate
    if (winRateEl) {
        const winRate = (wins + losses) > 0 ? (wins / (wins + losses) * 100) : 0;
        winRateEl.textContent = `${winRate.toFixed(0)}%`;
        winRateEl.style.color = winRate >= 50 ? '#22c55e' : winRate >= 30 ? '#f59e0b' : '#ef4444';
    }
    
    // Total P&L
    if (totalPnLEl) {
        const prefix = totalPnL >= 0 ? '+' : '';
        totalPnLEl.textContent = `${prefix}$${totalPnL.toFixed(2)}`;
        totalPnLEl.style.color = totalPnL >= 0 ? '#22c55e' : '#ef4444';
        
        // Add pulse animation on significant change
        if (Math.abs(totalPnL) > 10) {
            totalPnLEl.classList.add('pulse');
            setTimeout(() => totalPnLEl.classList.remove('pulse'), 1000);
        }
    }
    
    // Type B Pending
    if (typeBPendingEl) {
        typeBPendingEl.textContent = typeBPending ? '⏳ Yes' : '❌ No';
        typeBPendingEl.style.color = typeBPending ? '#f59e0b' : '#64748b';
    }
    
    // Avg Win
    if (avgWinEl && avgWin !== 0) {
        avgWinEl.textContent = `+$${avgWin.toFixed(2)}`;
        avgWinEl.style.color = '#22c55e';
    }
    
    // Avg Loss
    if (avgLossEl && avgLoss !== 0) {
        avgLossEl.textContent = `-$${Math.abs(avgLoss).toFixed(2)}`;
        avgLossEl.style.color = '#ef4444';
    }
    
    // Max Drawdown
    if (maxDrawdownEl) {
        maxDrawdownEl.textContent = `$${maxDrawdown.toFixed(2)}`;
        maxDrawdownEl.style.color = maxDrawdown > 50 ? '#ef4444' : maxDrawdown > 20 ? '#f59e0b' : '#22c55e';
    }
    
    // Daily limit indicator
    if (dailyLimitEl) {
        const remaining = 2 - tradesCount;
        dailyLimitEl.textContent = `${remaining} remaining`;
        dailyLimitEl.style.color = remaining > 0 ? '#22c55e' : '#ef4444';
    }
    
    // Loss limit indicator
    if (lossLimitEl) {
        const maxLosses = 2;
        const remaining = maxLosses - losses;
        lossLimitEl.textContent = `${remaining} remaining`;
        lossLimitEl.style.color = remaining > 0 ? '#22c55e' : '#ef4444';
    }
}

/**
 * Fetches Trade Statistics from API
 */
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

// ═══════════════════════════════════════════════════════════════════════════
// SECTION 6: SESSION STATUS - Complete session management
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Fetches complete session status from API
 */
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

/**
 * Updates the Session Status display
 */
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

// ═══════════════════════════════════════════════════════════════════════════
// SECTION 7: SYMBOL STATUS - Per-symbol tracking for multi-symbol support
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Fetches per-symbol status for V33
 */
async function fetchV33SymbolStatus() {
    try {
        const res = await fetch(`${API_URL}/api/v33/symbol_status`, {
            headers: getAuthHeaders()
        });
        
        if (!res.ok) throw new Error('Failed to fetch symbol status');
        
        const data = await res.json();
        if (data.status === 'success' && data.symbols) {
            v33SymbolStates.clear();
            data.symbols.forEach(sym => {
                v33SymbolStates.set(sym.symbol, sym);
            });
            updateV33SymbolGrid(data.symbols);
            return data.symbols;
        }
    } catch (error) {
        console.error('[V33] Error fetching symbol status:', error);
    }
    return [];
}

/**
 * Updates the Symbol Grid display
 */
function updateV33SymbolGrid(symbols) {
    const gridEl = document.getElementById('v33SymbolGrid');
    if (!gridEl || !symbols) return;
    
    gridEl.innerHTML = symbols.map(sym => {
        const isCompressed = sym.is_compressed;
        const hasSignal = sym.signal && sym.signal !== 'WAIT';
        const signalColor = sym.signal === 'BUY' ? '#22c55e' : sym.signal === 'SELL' ? '#ef4444' : '#64748b';
        
        return `
            <div class="v33-symbol-card" style="
                background: ${hasSignal ? `rgba(${sym.signal === 'BUY' ? '34, 197, 94' : '239, 68, 68'}, 0.1)` : 'rgba(30, 41, 59, 0.5)'};
                border: 1px solid ${hasSignal ? signalColor : 'rgba(255,255,255,0.1)'};
                border-radius: 8px;
                padding: 10px;
                cursor: pointer;
                transition: all 0.2s;
            " onclick="selectV33Symbol('${sym.symbol}')"
               onmouseover="this.style.borderColor='${signalColor}'"
               onmouseout="this.style.borderColor='${hasSignal ? signalColor : 'rgba(255,255,255,0.1)'}'">
                <div style="font-weight: 600; color: #f1f5f9; margin-bottom: 4px;">${sym.symbol}</div>
                <div style="font-size: 11px; color: ${isCompressed ? '#22c55e' : '#ef4444'};">
                    ${isCompressed ? '✅ Compressed' : '⚠️ Expanded'}
                </div>
                <div style="font-size: 11px; color: ${signalColor}; margin-top: 4px;">
                    ${sym.signal || 'WAIT'}
                </div>
            </div>
        `;
    }).join('');
}

/**
 * Selects a symbol for detailed view
 */
function selectV33Symbol(symbol) {
    // Trigger a refresh for this specific symbol
    fetchV33ORData(symbol);
    fetchV33PreSessionData(symbol);
    fetchV33BreakoutStatus(symbol);
    fetchV33TradeStats(symbol);
    
    // Highlight selected
    document.querySelectorAll('.v33-symbol-card').forEach(card => {
        card.style.opacity = '0.5';
    });
    event.currentTarget.style.opacity = '1';
}

// ═══════════════════════════════════════════════════════════════════════════
// SECTION 8: DASHBOARD CONTROL & LIFECYCLE
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Starts the V33 Dashboard updates
 */
function startV33DashboardUpdates() {
    if (v33DashboardInterval) return;
    
    // Immediate update
    updateV33Dashboard();
    
    // Set up interval (1 second for time updates, 5 seconds for data)
    v33DashboardInterval = setInterval(() => {
        updateV33NYTime(); // Every second
        
        // Data updates every 5 seconds
        const now = new Date();
        if (now.getSeconds() % 5 === 0) {
            updateV33Dashboard();
        }
    }, 1000);
    
    console.log('[V33] Dashboard updates started');
}

/**
 * Stops the V33 Dashboard updates
 */
function stopV33DashboardUpdates() {
    if (v33DashboardInterval) {
        clearInterval(v33DashboardInterval);
        v33DashboardInterval = null;
        console.log('[V33] Dashboard updates stopped');
    }
}

/**
 * Main dashboard update function - fetches all data
 */
async function updateV33Dashboard() {
    try {
        // Always update time first
        updateV33NYTime();
        
        // Fetch all data in parallel
        const promises = [
            fetchV33SessionStatus(),
            fetchV33ORData(),
            fetchV33PreSessionData(),
            fetchV33BreakoutStatus(),
            fetchV33TradeStats(),
            fetchV33SymbolStatus()
        ];
        
        const results = await Promise.allSettled(promises);
        
        // Log any failures
        results.forEach((result, index) => {
            if (result.status === 'rejected') {
                const endpoints = ['session_status', 'or_data', 'presession_data', 'breakout_status', 'trade_stats', 'symbol_status'];
                console.warn(`[V33] Failed to fetch ${endpoints[index]}:`, result.reason);
            }
        });
        
    } catch (error) {
        console.error('[V33] Dashboard update error:', error);
    }
}

/**
 * Toggles V33 Dashboard visibility
 */
function toggleV33Dashboard() {
    const v33Section = document.getElementById('v33-dashboard-section');
    if (!v33Section) return;
    
    // Check if V33 is the currently selected robot
    const currentRobot = window.currentRobot || 'v31_tpl';
    
    if (currentRobot === 'v33_ny') {
        v33Section.style.display = 'block';
        startV33DashboardUpdates();
    } else {
        v33Section.style.display = 'none';
        stopV33DashboardUpdates();
    }
}

// ═══════════════════════════════════════════════════════════════════════════
// SECTION 9: LOG PARSING - Fallback when API is unavailable
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Parses V33 robot logs for fallback data
 */
function parseV33Logs(logs) {
    if (!logs || !Array.isArray(logs)) return;
    
    let orData = { or_high: 0, or_low: 0, current_price: 0 };
    let preSessionData = { pre_session_high: 0, pre_session_low: 0, is_compressed: true };
    let breakoutData = { breakout_status: 'WAITING', signal: 'WAIT' };
    let tradeData = { trades_count: 0, wins: 0, losses: 0, total_pnl: 0, type_b_pending: false };
    
    // Process logs from newest to oldest
    for (let i = logs.length - 1; i >= 0; i--) {
        const log = logs[i];
        const msg = log.message || '';
        
        // Extract OR data
        if (!orData.or_high) {
            const orMatch = msg.match(/OR.*H[=:]\s*([\d.]+).*L[=:]\s*([\d.]+)/i);
            if (orMatch) {
                orData.or_high = parseFloat(orMatch[1]);
                orData.or_low = parseFloat(orMatch[2]);
            }
        }
        
        // Extract pre-session data
        if (!preSessionData.pre_session_high && msg.includes('Pre')) {
            const preMatch = msg.match(/High[=:]\s*([\d.]+).*Low[=:]\s*([\d.]+)/i);
            if (preMatch) {
                preSessionData.pre_session_high = parseFloat(preMatch[1]);
                preSessionData.pre_session_low = parseFloat(preMatch[2]);
            }
        }
        
        // Extract breakout data
        if (msg.includes('BREAKOUT') || msg.includes('Type A') || msg.includes('Type B')) {
            if (msg.includes('BUY')) breakoutData.signal = 'BUY';
            if (msg.includes('SELL')) breakoutData.signal = 'SELL';
            breakoutData.breakout_status = 'DETECTED';
            
            const typeMatch = msg.match(/Type\s+([AB])/i);
            if (typeMatch) breakoutData.setup_type = `TYPE_${typeMatch[1]}`;
        }
        
        // Extract trade stats
        const tradeMatch = msg.match(/trades?[\s:]+(\d+)/i);
        if (tradeMatch) tradeData.trades_count = parseInt(tradeMatch[1]);
        
        const winMatch = msg.match(/wins?[\s:]+(\d+)/i);
        if (winMatch) tradeData.wins = parseInt(winMatch[1]);
        
        const lossMatch = msg.match(/loss(es)?[\s:]+(\d+)/i);
        if (lossMatch) tradeData.losses = parseInt(lossMatch[2] || lossMatch[1]);
        
        const pnlMatch = msg.match(/P&L[\s:]+[$]?([\d.-]+)/i);
        if (pnlMatch) tradeData.total_pnl = parseFloat(pnlMatch[1]);
        
        if (msg.includes('Type B') && msg.includes('Pending')) {
            tradeData.type_b_pending = true;
        }
    }
    
    // Update displays with parsed data
    updateV33OpeningRange(orData);
    updateV33PreSession(preSessionData);
    updateV33BreakoutStatus(breakoutData);
    updateV33DailyStats(tradeData);
}

// ═══════════════════════════════════════════════════════════════════════════
// SECTION 10: INITIALIZATION & EXPORTS
// ═══════════════════════════════════════════════════════════════════════════

// Initialize V33 Dashboard when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('[V33] Connector loaded');
    
    // Check if we're on V33 section
    toggleV33Dashboard();
    
    // Listen for robot switches
    const robotSelector = document.getElementById('robotSelector');
    if (robotSelector) {
        robotSelector.addEventListener('change', toggleV33Dashboard);
    }
});

// Export all functions to global scope
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

window.updateV33SymbolGrid = updateV33SymbolGrid;
window.fetchV33SymbolStatus = fetchV33SymbolStatus;
window.selectV33Symbol = selectV33Symbol;

window.updateV33Dashboard = updateV33Dashboard;
window.startV33DashboardUpdates = startV33DashboardUpdates;
window.stopV33DashboardUpdates = stopV33DashboardUpdates;
window.toggleV33Dashboard = toggleV33Dashboard;
window.parseV33Logs = parseV33Logs;

console.log('[V33] Full Connector v33.1.0 - All functions exported');
