/**
 * V31 Symbol Status Grid Connector
 * Fetches live status for each symbol and updates the grid UI
 * API: /api/v31/symbol_status
 */

const V31_SYMBOLS = [
  'AUDUSD', 'EURGBP', 'EURJPY', 'EURUSD', 'GBPJPY',
  'GBPUSD', 'NZDUSD', 'USDCAD', 'USDCHF', 'USDJPY'
];

/**
 * Format cooldown time to human-readable string
 * @param {number} seconds - Remaining cooldown in seconds
 * @returns {string} Formatted time like "5m" or "12s"
 */
function formatCooldown(seconds) {
  if (!seconds || seconds <= 0) return '-';
  if (seconds >= 60) {
    return Math.ceil(seconds / 60) + 'm';
  }
  return seconds + 's';
}

/**
 * Get CSS class based on boolean status
 * @param {boolean} status - True/False status
 * @returns {string} CSS class for styling
 */
function getStatusClass(status) {
  return status ? 'status-active' : 'status-inactive';
}

/**
 * Get color style based on boolean status
 * @param {boolean} status - True/False status
 * @returns {string} Color value
 */
function getStatusColor(status) {
  return status ? '#22c55e' : '#6b7280'; // green-500 : gray-500
}

/**
 * Create HTML for a single symbol status cell
 * @param {Object} status - Status object for symbol
 * @returns {string} HTML string
 */
function createSymbolCell(symbol, status) {
  const tradeColor = getStatusColor(status.trade_open);
  const setupColor = getStatusColor(status.setup_found);
  const analyzedColor = getStatusColor(status.analyzed);
  const pendingColor = getStatusColor(status.pending);
  
  return `
    <div class="symbol-cell" data-symbol="${symbol}">
      <div class="symbol-header">${symbol}</div>
      <div class="symbol-status-grid">
        <div class="status-item" style="color: ${tradeColor}">
          <span class="status-dot" style="background: ${tradeColor}"></span>
          <span class="status-label">Trade</span>
          <span class="status-value">${status.trade_open ? 'OPEN' : 'NO'}</span>
        </div>
        <div class="status-item" style="color: ${setupColor}">
          <span class="status-dot" style="background: ${setupColor}"></span>
          <span class="status-label">Setup</span>
          <span class="status-value">${status.setup_found ? 'YES' : 'NO'}</span>
        </div>
        <div class="status-item" style="color: ${analyzedColor}">
          <span class="status-dot" style="background: ${analyzedColor}"></span>
          <span class="status-label">Analyzed</span>
          <span class="status-value">${status.analyzed ? 'YES' : 'NO'}</span>
        </div>
        <div class="status-item" style="color: ${pendingColor}">
          <span class="status-dot" style="background: ${pendingColor}"></span>
          <span class="status-label">Pending</span>
          <span class="status-value">${status.pending ? 'YES' : 'NO'}</span>
        </div>
        <div class="status-item cooldown">
          <span class="status-label">Cooldown</span>
          <span class="status-value cooldown-time">${formatCooldown(status.cooldown)}</span>
        </div>
      </div>
    </div>
  `;
}

/**
 * Initialize the V31 symbol grid with empty cells
 */
function initV31SymbolGrid() {
  const grid = document.getElementById('v31-symbol-grid');
  if (!grid) {
    console.error('[V31] Symbol grid container not found');
    return;
  }
  
  grid.innerHTML = V31_SYMBOLS.map(symbol => `
    <div class="symbol-cell loading" data-symbol="${symbol}">
      <div class="symbol-header">${symbol}</div>
      <div class="symbol-status-grid">
        <div class="status-item"><span class="loading-text">Loading...</span></div>
      </div>
    </div>
  `).join('');
}

/**
 * Fetch and update the V31 symbol grid with live status
 * Call this function to refresh the grid
 */
async function updateV31SymbolGrid() {
  const grid = document.getElementById('v31-symbol-grid');
  if (!grid) {
    console.error('[V31] Symbol grid container not found');
    return;
  }
  
  try {
    const response = await fetch('/api/v31/symbol_status');
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    
    // Support both array and object formats
    const statuses = Array.isArray(data) ? data : (data.symbols || data.statuses || []);
    
    // Build lookup map
    const statusMap = {};
    statuses.forEach(s => {
      const symbol = s.symbol || s.pair || s.name;
      if (symbol) statusMap[symbol] = s;
    });
    
    // Update each symbol cell
    V31_SYMBOLS.forEach(symbol => {
      const status = statusMap[symbol] || {
        trade_open: false,
        setup_found: false,
        analyzed: false,
        pending: false,
        cooldown: 0
      };
      
      const cell = grid.querySelector(`[data-symbol="${symbol}"]`);
      if (cell) {
        cell.outerHTML = createSymbolCell(symbol, status);
      }
    });
    
    console.log('[V31] Symbol grid updated successfully');
    
  } catch (error) {
    console.error('[V31] Failed to update symbol grid:', error);
    
    // Show error state
    V31_SYMBOLS.forEach(symbol => {
      const cell = grid.querySelector(`[data-symbol="${symbol}"]`);
      if (cell) {
        cell.classList.add('error');
        cell.innerHTML = `
          <div class="symbol-header">${symbol}</div>
          <div class="error-text">Connection Error</div>
        `;
      }
    });
  }
}

/**
 * Start auto-refresh of the symbol grid
 * @param {number} intervalMs - Refresh interval in milliseconds (default: 5000)
 */
function startV31SymbolGridRefresh(intervalMs = 5000) {
  updateV31SymbolGrid(); // Initial load
  
  const intervalId = setInterval(updateV31SymbolGrid, intervalMs);
  
  // Store for cleanup
  window._v31GridRefreshInterval = intervalId;
  
  console.log(`[V31] Auto-refresh started (${intervalMs}ms)`);
  return intervalId;
}

/**
 * Stop auto-refresh of the symbol grid
 */
function stopV31SymbolGridRefresh() {
  if (window._v31GridRefreshInterval) {
    clearInterval(window._v31GridRefreshInterval);
    window._v31GridRefreshInterval = null;
    console.log('[V31] Auto-refresh stopped');
  }
}

/**
 * CSS styles for the V31 symbol grid
 * Include this in your dashboard CSS
 */
const V31_SYMBOL_GRID_STYLES = `
#v31-symbol-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 12px;
  padding: 16px;
}

.symbol-cell {
  background: #1f2937;
  border-radius: 8px;
  padding: 12px;
  border: 1px solid #374151;
  transition: border-color 0.2s;
}

.symbol-cell:hover {
  border-color: #4b5563;
}

.symbol-header {
  font-weight: 600;
  font-size: 14px;
  color: #f9fafb;
  margin-bottom: 8px;
  text-align: center;
  letter-spacing: 0.5px;
}

.symbol-status-grid {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 11px;
  padding: 4px 6px;
  background: #111827;
  border-radius: 4px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.status-label {
  flex: 1;
  opacity: 0.8;
}

.status-value {
  font-weight: 500;
  font-size: 10px;
}

.cooldown {
  color: #9ca3af;
}

.cooldown-time {
  color: #fbbf24;
  font-family: monospace;
}

.loading {
  opacity: 0.6;
}

.loading-text {
  color: #6b7280;
  font-size: 12px;
  text-align: center;
  width: 100%;
}

.error {
  border-color: #ef4444 !important;
}

.error-text {
  color: #ef4444;
  font-size: 11px;
  text-align: center;
}
`;

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    updateV31SymbolGrid,
    initV31SymbolGrid,
    startV31SymbolGridRefresh,
    stopV31SymbolGridRefresh,
    formatCooldown,
    getStatusColor,
    V31_SYMBOLS,
    V31_SYMBOL_GRID_STYLES
  };
}

// Auto-initialize if DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('v31-symbol-grid')) {
      initV31SymbolGrid();
      startV31SymbolGridRefresh(5000);
    }
  });
} else {
  if (document.getElementById('v31-symbol-grid')) {
    initV31SymbolGrid();
    startV31SymbolGridRefresh(5000);
  }
}
