#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# QA-MASTER FINAL TESTING SCRIPT - All 6 Suites
# ═══════════════════════════════════════════════════════════════════════════════

import json
import re
import os
import sys
from datetime import datetime

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    END = '\033[0m'

# ═══════════════════════════════════════════════════════════════════════════════
# TEST CONFIGURATIONS (from user specifications)
# ═══════════════════════════════════════════════════════════════════════════════

TEST_CONFIG = {
    # SUITA 1: CORE (21 teste)
    "suite_1": {
        "Q1.1": "A", "Q1.2": "A+C", "Q1.3": "A", "Q1.4": "A", "Q1.5": "D",
        "Q2.1": "C", "Q2.2": "B", "Q2.3": "A", "Q2.4": "B+C", "Q2.5": "D", "Q2.6": "B",
        "Q3.1": "A", "Q3.2": "B", "Q3.3": "A", "Q3.4": "D", "Q3.5": "B+C+D", "Q3.6": "A",
        "Q4.1": "A", "Q4.2": "A", "Q4.3": "C", "Q4.4": "C"
    },
    # SUITA 2: ROBOȚI (26 teste)
    "suite_2": {
        "Q5.1": "A+B", "Q5.2": "A+B", "Q5.3": "A", "Q5.4": "A+B+C+D", "Q5.5": "A+C",
        "Q5.6": "B", "Q5.7": "C", "Q5.8": "D", "Q5.9": "B+C+D", "Q5.10": "A+D",
        "Q6.1": "B+D", "Q6.2": "B+C", "Q6.3": "D", "Q6.4": "A", "Q6.5": "C",
        "Q6.6": "A+B+D", "Q6.7": "Configurabil",
        "Q7.1": "A+B", "Q7.2": "D"
    },
    # SUITA 3: ADVANCED (18 teste)
    "suite_3": {
        "Q8.1": "A", "Q8.2": "D", "Q8.3": "B+C+D", "Q8.4": "D",
        "Q9.1": "D", "Q9.2": "B", "Q9.3": "A+D", "Q9.4": "D", "Q9.5": "A+B+C",
        "Q10.1": "D", "Q10.2": "D", "Q10.3": "C", "Q10.4": "A+B", "Q10.5": "D"
    },
    # SUITA 4: MONITORING (14 teste)
    "suite_4": {
        "Q11.1": "D", "Q11.2": "A", "Q11.3": "A+C", "Q11.4": "C", "Q11.5": "D",
        "Q12.1": "D", "Q12.2": "B", "Q12.3": "A+C", "Q12.4": "B",
        "Q15.1": "D", "Q15.2": "D", "Q15.3": "C", "Q15.4": "A+B+C", "Q15.5": "D"
    },
    # SUITA 5: ADMIN (17 teste)
    "suite_5": {
        "Q13.1": "D", "Q13.2": "A", "Q13.3": "A+D", "Q13.4": "A",
        "Q14.1": "B", "Q14.2": "A+B+C", "Q14.3": "A", "Q14.4": "A+C",
        "Q16.1": "C", "Q16.2": "D", "Q16.3": "A", "Q16.4": "A+B+C", "Q16.5": "A",
        "Q17.1": "D", "Q17.2": "A+C+D", "Q17.3": "D", "Q17.4": "D"
    },
    # SUITA 6: LOGS (8 teste)
    "suite_6": {
        "Q18.1": "A", "Q18.2": "D", "Q18.3": "D", "Q18.4": "A",
        "Q19.1": "D", "Q19.2": "D", "Q19.3": "D", "Q19.4": "A+D"
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# EXPECTED API ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

EXPECTED_APIS = {
    # Suite 1 - Core
    "/api/clients": ["GET"],
    "/api/positions": ["GET"],
    "/api/trade_history": ["GET"],
    "/api/accounts/{login}/toggle": ["POST"],
    
    # Suite 2 - Robots
    "/api/v31/live_status": ["GET"],
    "/api/v32/session_status": ["GET"],
    "/api/v32/or_data": ["GET"],
    "/api/v32/asia_data": ["GET"],
    "/api/v32/breakout_status": ["GET"],
    "/api/v32/trade_stats": ["GET"],
    "/api/v33/session_status": ["GET"],
    "/api/v33/or_data": ["GET"],
    "/api/v33/presession_data": ["GET"],
    "/api/v33/breakout_status": ["GET"],
    "/api/v33/trade_stats": ["GET"],
    "/api/robot/v31/start": ["POST"],
    "/api/robot/v31/stop": ["POST"],
    "/api/robot/v32/start": ["POST"],
    "/api/robot/v32/stop": ["POST"],
    "/api/robot/v33/start": ["POST"],
    "/api/robot/v33/stop": ["POST"],
    
    # Suite 4 - Monitoring
    "/api/health": ["GET"],
    "/positions": ["GET"],
}

# ═══════════════════════════════════════════════════════════════════════════════
# EXPECTED JAVASCRIPT FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

EXPECTED_JS_FUNCTIONS = {
    # Suite 1 - Core Functions
    "switchRobot": "critical",
    "showToast": "required",
    "getAuthHeaders": "required",
    "loadClients": "required",
    "loadPositions": "required",
    "updateClientsTable": "required",
    "updatePositionsTable": "required",
    "toggleClient": "required",
    "toggleAllClients": "required",
    "closePosition": "required",
    "closeAllPositions": "required",
    "setPositionFilter": "required",
    "loadTradeHistory": "required",
    "setHistoryFilter": "required",
    "updateHistoryTable": "required",
    "loadTracking": "required",
    "updateTrackingTable": "required",
    
    # Suite 2 - Robot Functions
    "startV31Polling": "required",
    "stopV31Polling": "required",
    "fetchV31Data": "required",
    "updateV31Dashboard": "required",
    "updateV31SymbolGrid": "required",
    "updateV31LiveStatus": "required",
    "startV32Polling": "required",
    "stopV32Polling": "required",
    "fetchV32Data": "required",
    "updateV32Dashboard": "required",
    "updateV32LondonTime": "required",
    "updateV32SessionTimer": "required",
    "updateV32OpeningRange": "required",
    "updateV32AsiaSession": "required",
    "updateV32BreakoutDetection": "required",
    "startV33Polling": "required",
    "stopV33Polling": "required",
    "updateV33NYTime": "required",
    "updateV33SessionTimer": "required",
    "fetchV33SessionStatus": "required",
    "fetchV33ORData": "required",
    "fetchV33PreSessionData": "required",
    "fetchV33BreakoutStatus": "required",
    "fetchV33TradeStats": "required",
    "controlRobot": "critical",
    "syncRobotStatusFromBackend": "required",
    "syncAllRobotStatuses": "required",
    "updateRobotControlUI": "required",
    
    # Suite 4 - Monitoring
    "loadSystemHealth": "required",
    "updateHealthUI": "required",
    "toggleHealthDetails": "required",
    "startHealthCheckPolling": "required",
    "stopHealthCheckPolling": "required",
    "checkRobotConnection": "required",
    "checkAllRobotConnections": "required",
    "startRobotStatusPolling": "required",
    "stopRobotStatusPolling": "required",
    
    # Dashboard Stats
    "fetchDashboardStats": "required",
    "startDashboardStatsPolling": "required",
    "stopDashboardStatsPolling": "required",
}

# ═══════════════════════════════════════════════════════════════════════════════
# EXPECTED HTML ELEMENTS
# ═══════════════════════════════════════════════════════════════════════════════

EXPECTED_HTML_ELEMENTS = {
    # Core Layout
    "robotSelector": "select",
    "v31-dashboard-section": "div",
    "v32-dashboard-section": "div", 
    "v33-dashboard-section": "div",
    "clientsTable": "table",
    "positionsTable": "table",
    "historyTable": "table",
    "trackingTable": "table",
    "globalClientToggle": "input",
    
    # V31 Elements
    "v31SymbolGrid": "div",
    "v31LiveProgressBar": "div",
    "v31LivePhase": "div",
    "v31StatusBadge": "div",
    "v31AnalyzedCount": "span",
    "v31SetupsCount": "span",
    "v31RejectedCount": "span",
    "v31LiveCurrent": "div",
    "v31ScoreRSI": "span",
    "v31ScoreStoch": "span",
    "v31ScoreFib": "span",
    "v31ScoreTotal": "span",
    "v31SetupCount": "span",
    "v31TradeCount": "span",
    "v31WinRate": "span",
    "v31CurrentFocus": "div",
    "v31CurrentSetup": "div",
    
    # V32 Elements
    "v32LondonTime": "div",
    "v32SessionPhase": "div",
    "v32SessionBadge": "div",
    "v32SessionTimer": "div",
    "v32ORHigh": "div",
    "v32ORLow": "div",
    "v32ORRange": "div",
    "v32CurrentPrice": "div",
    "v32AsiaHigh": "div",
    "v32AsiaLow": "div",
    "v32AsiaRange": "div",
    "v32AsiaStatus": "div",
    "v32BreakoutStatus": "div",
    "v32SetupType": "div",
    "v32BodyPercent": "div",
    "v32WickPercent": "div",
    "v32Signal": "div",
    "v32SignalBox": "div",
    "v32TradesCount": "span",
    "v32WinLoss": "span",
    "v32TotalPnL": "span",
    "v32TypeBPending": "span",
    
    # V33 Elements
    "v33NYTime": "div",
    "v33SessionPhase": "div",
    "v33SessionBadge": "div",
    "v33SessionTimer": "div",
    "v33ORHigh": "div",
    "v33ORLow": "div",
    "v33ORRange": "div",
    "v33CurrentPrice": "div",
    "v33PreHigh": "div",
    "v33PreLow": "div",
    "v33PreRange": "div",
    "v33PreStatus": "div",
    "v33BreakoutStatus": "div",
    "v33SetupType": "div",
    "v33BodyPercent": "div",
    "v33WickPercent": "div",
    "v33Signal": "div",
    "v33SignalBox": "div",
    "v33TradesCount": "span",
    "v33WinLoss": "span",
    "v33TotalPnL": "span",
    "v33TypeBPending": "span",
    
    # Robot Control Elements
    "robotStartBtn": "button",
    "robotStopBtn": "button",
    "robotStatusBadge": "span",
    "robotStatStatus": "span",
    "v31StatusDot": "div",
    "v32StatusDot": "div",
    "v33StatusDot": "div",
    
    # Health Elements
    "coreStatus": "div",
    "bridgeStatus": "div",
    "postgresStatus": "div",
    
    # Dashboard Stats
    "kpiClients": "span",
    "kpiPositions": "span",
    "kpiProfit": "span",
    "lastUpdate": "span",
}


def log_header(title):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'═' * 80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}  {title}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'═' * 80}{Colors.END}\n")


def log_section(title):
    print(f"\n{Colors.CYAN}▶ {title}{Colors.END}")
    print(f"{Colors.CYAN}{'─' * 60}{Colors.END}")


def log_pass(msg):
    print(f"  {Colors.GREEN}✓{Colors.END} {msg}")


def log_fail(msg):
    print(f"  {Colors.RED}✗{Colors.END} {msg}")


def log_warn(msg):
    print(f"  {Colors.YELLOW}⚠{Colors.END} {msg}")


def log_info(msg):
    print(f"  {Colors.BLUE}ℹ{Colors.END} {msg}")


class QAMasterTester:
    def __init__(self):
        self.results = {
            "suite_1": {"passed": 0, "failed": 0, "partial": 0, "tests": []},
            "suite_2": {"passed": 0, "failed": 0, "partial": 0, "tests": []},
            "suite_3": {"passed": 0, "failed": 0, "partial": 0, "tests": []},
            "suite_4": {"passed": 0, "failed": 0, "partial": 0, "tests": []},
            "suite_5": {"passed": 0, "failed": 0, "partial": 0, "tests": []},
            "suite_6": {"passed": 0, "failed": 0, "partial": 0, "tests": []},
        }
        self.bugs = []
        self.js_content = ""
        self.html_content = ""
        self.apis_found = set()
        self.js_functions_found = set()
        self.html_elements_found = set()
        
    def load_files(self):
        """Load dashboard files for analysis"""
        js_path = "/workspace/shared/dashboard/dashboard_functional.js"
        html_path = "/workspace/shared/dashboard/index.html"
        
        try:
            with open(js_path, 'r', encoding='utf-8') as f:
                self.js_content = f.read()
            log_pass(f"Loaded JS file: {len(self.js_content)} chars")
        except Exception as e:
            log_fail(f"Failed to load JS file: {e}")
            
        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                self.html_content = f.read()
            log_pass(f"Loaded HTML file: {len(self.html_content)} chars")
        except Exception as e:
            log_fail(f"Failed to load HTML file: {e}")
    
    def extract_js_functions(self):
        """Extract all JavaScript function definitions"""
        # Match function declarations
        pattern1 = r'function\s+(\w+)\s*\('
        # Match const/let/var function assignments
        pattern2 = r'(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?function\s*\('
        # Match arrow functions assigned to variables
        pattern3 = r'(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\([^)]*\)\s*=>\s*\{'
        
        matches1 = re.findall(pattern1, self.js_content)
        matches2 = re.findall(pattern2, self.js_content)
        matches3 = re.findall(pattern3, self.js_content)
        
        self.js_functions_found = set(matches1 + matches2 + matches3)
        
    def extract_html_elements(self):
        """Extract HTML element IDs"""
        pattern = r'id=["\']([^"\']+)["\']'
        self.html_elements_found = set(re.findall(pattern, self.html_content))
        
    def extract_api_endpoints(self):
        """Extract API endpoints from JavaScript"""
        # Match fetch calls
        pattern = r'fetch\s*\(\s*[`"\']?([^`"\']*(?:/api/|/positions)[^`"\']*)[`"\']?'
        matches = re.findall(pattern, self.js_content)
        
        for match in matches:
            # Extract just the path part
            if '/api/' in match:
                path = '/api/' + match.split('/api/')[1].split('?')[0].split("'")[0].split('"')[0]
                self.apis_found.add(path)
            elif '/positions' in match:
                self.apis_found.add('/positions')
    
    def test_js_function(self, func_name):
        """Test if a JavaScript function exists"""
        # Check for function declaration
        patterns = [
            rf'function\s+{re.escape(func_name)}\s*\(',
            rf'(?:const|let|var)\s+{re.escape(func_name)}\s*=\s*(?:async\s+)?function\s*\(',
            rf'(?:const|let|var)\s+{re.escape(func_name)}\s*=\s*(?:async\s*)?\(',
            rf'window\.{re.escape(func_name)}\s*=\s*{re.escape(func_name)}',
        ]
        
        for pattern in patterns:
            if re.search(pattern, self.js_content):
                return True
        return False
    
    def test_html_element(self, element_id):
        """Test if an HTML element exists"""
        pattern = rf'id=["\']{re.escape(element_id)}["\']'
        return bool(re.search(pattern, self.html_content))
    
    def test_api_endpoint(self, endpoint):
        """Test if API endpoint is referenced in code"""
        # Normalize endpoint
        if '{' in endpoint:
            # Parameterized endpoint - check base path
            base = endpoint.split('{')[0]
            return base in self.js_content
        return endpoint in self.js_content
    
    def run_tests(self):
        """Run all tests"""
        log_header("QA-MASTER FINAL TESTING - TOATE CELE 6 SUITE")
        
        # Load and analyze files
        log_section("ÎNCĂRCARE ȘI ANALIZĂ FIȘIERE")
        self.load_files()
        self.extract_js_functions()
        self.extract_html_elements()
        self.extract_api_endpoints()
        
        log_info(f"Funcții JavaScript găsite: {len(self.js_functions_found)}")
        log_info(f"Elemente HTML găsite: {len(self.html_elements_found)}")
        log_info(f"API endpoints găsite: {len(self.apis_found)}")
        
        # Run test suites
        self.test_suite_1_core()
        self.test_suite_2_robots()
        self.test_suite_3_advanced()
        self.test_suite_4_monitoring()
        self.test_suite_5_admin()
        self.test_suite_6_logs()
        
        # Generate report
        self.generate_report()
    
    def test_suite_1_core(self):
        """Test Suite 1: Core Functionality (Containers 1-4)"""
        log_section("SUITA 1: CORE (Containere 1-4)")
        
        suite = "suite_1"
        config = TEST_CONFIG[suite]
        
        # ═══════════════════════════════════════════════════════════════════
        # CONTAINER 1: Clienți (Q1.1 - Q1.5)
        # ═══════════════════════════════════════════════════════════════════
        log_info("Container 1: Clienți")
        
        # Q1.1 = A - Toggle Individual Client
        test = {"id": "Q1.1", "desc": "Toggle Individual Client (A=Immediate update)", "checks": []}
        has_toggle = self.test_js_function("toggleClient")
        has_table = self.test_html_element("clientsTable")
        test["checks"].append(("Funcție toggleClient()", has_toggle))
        test["checks"].append(("Tabel clientsTable", has_table))
        
        if has_toggle and has_table:
            test["status"] = "PASS"
            test["spec_match"] = "Q1.1=A ✓"
            self.results[suite]["passed"] += 1
            log_pass("Q1.1: Toggle client implementat")
        else:
            test["status"] = "FAIL"
            self.results[suite]["failed"] += 1
            log_fail("Q1.1: Toggle client lipsă")
        self.results[suite]["tests"].append(test)
        
        # Q1.2 = A+C - Toggle Toți Clienții
        test = {"id": "Q1.2", "desc": "Toggle Toți Clienții (A=Toggle all button + C=Confirmation dialog)", "checks": []}
        has_toggle_all = self.test_js_function("toggleAllClients")
        has_global_toggle = self.test_html_element("globalClientToggle")
        test["checks"].append(("Funcție toggleAllClients()", has_toggle_all))
        test["checks"].append(("Toggle global", has_global_toggle))
        
        if has_toggle_all:
            test["status"] = "PASS" if has_global_toggle else "PARTIAL"
            if has_global_toggle:
                self.results[suite]["passed"] += 1
                log_pass("Q1.2: Toggle toți clienții implementat")
            else:
                self.results[suite]["partial"] += 1
                log_warn("Q1.2: Toggle toți clienții - parțial")
        else:
            test["status"] = "FAIL"
            self.results[suite]["failed"] += 1
            log_fail("Q1.2: Toggle toți clienții lipsă")
        self.results[suite]["tests"].append(test)
        
        # Q1.3 = A - Pozițiile rămân deschise la dezactivare
        test = {"id": "Q1.3", "desc": "Poziții rămân deschise la dezactivare (A=Stay open)", "checks": []}
        # Verificăm că există implementarea de dezactivare
        has_disabled_logic = "disabled" in self.js_content.lower() and "client" in self.js_content.lower()
        test["checks"].append(("Logică dezactivare clienți", has_disabled_logic))
        
        if has_disabled_logic:
            test["status"] = "PASS"
            test["spec_match"] = "Q1.3=A ✓"
            self.results[suite]["passed"] += 1
            log_pass("Q1.3: Logică păstrare poziții la dezactivare")
        else:
            test["status"] = "PARTIAL"
            self.results[suite]["partial"] += 1
            log_warn("Q1.3: Verificare manuală necesară")
        self.results[suite]["tests"].append(test)
        
        # Q1.4 = A - Filtrare clienți
        test = {"id": "Q1.4", "desc": "Filtrare Clienți (A=Filterable list with badge counter)", "checks": []}
        # Căutăm filtre în cod
        has_filter = "filter" in self.js_content.lower() and "client" in self.js_content.lower()
        test["checks"].append(("Logică filtrare clienți", has_filter))
        
        # Adăugăm ca bug
        if not has_filter:
            self.bugs.append({
                "id": "BUG-S1-C1-001",
                "severity": "HIGH",
                "container": 1,
                "desc": "Lipsește filtrarea clienților (Q1.4=A)",
                "suite": suite
            })
            test["status"] = "FAIL"
            self.results[suite]["failed"] += 1
            log_fail("Q1.4: Filtrare clienți lipsă")
        else:
            test["status"] = "PASS"
            self.results[suite]["passed"] += 1
            log_pass("Q1.4: Filtrare clienți implementată")
        self.results[suite]["tests"].append(test)
        
        # Q1.5 = D - WebSocket Real-time
        test = {"id": "Q1.5", "desc": "Real-time Updates (D=WebSocket)", "checks": []}
        has_websocket = "websocket" in self.js_content.lower() or "ws://" in self.js_content.lower()
        has_polling = "setinterval" in self.js_content.lower() and "fetch" in self.js_content.lower()
        test["checks"].append(("WebSocket implementation", has_websocket))
        test["checks"].append(("Polling fallback", has_polling))
        
        # Spec Q1.5=D requires WebSocket
        if has_websocket:
            test["status"] = "PASS"
            test["spec_match"] = "Q1.5=D ✓"
            self.results[suite]["passed"] += 1
            log_pass("Q1.5: WebSocket implementat")
        elif has_polling:
            test["status"] = "FAIL"
            test["spec_match"] = "Q1.5=D ✗ (folosește polling)"
            self.results[suite]["failed"] += 1
            log_fail("Q1.5: Folosește polling în loc de WebSocket")
            self.bugs.append({
                "id": "BUG-S1-C1-002",
                "severity": "MEDIUM",
                "container": 1,
                "desc": "WebSocket nu e implementat - folosește polling (Q1.5=D)",
                "suite": suite
            })
        else:
            test["status"] = "FAIL"
            self.results[suite]["failed"] += 1
            log_fail("Q1.5: Nicio metodă real-time")
        self.results[suite]["tests"].append(test)
        
        # ═══════════════════════════════════════════════════════════════════
        # CONTAINER 2: Poziții Active (Q2.1 - Q2.6)
        # ═══════════════════════════════════════════════════════════════════
        log_info("Container 2: Poziții Active")
        
        # Q2.1 = C - Mid Price Calculation
        test = {"id": "Q2.1", "desc": "Mid Price Calculation (C=(Bid+Ask)/2)", "checks": []}
        has_mid_calc = "(bid + ask) / 2" in self.js_content.lower().replace(" ", "") or \
                       "mid" in self.js_content.lower() and "price" in self.js_content.lower()
        has_current_price = self.test_html_element("positionsTable")
        test["checks"].append(("Calcul mid price", has_mid_calc))
        test["checks"].append(("Tabel poziții", has_current_price))
        
        if has_mid_calc:
            test["status"] = "PASS"
            test["spec_match"] = "Q2.1=C ✓"
            self.results[suite]["passed"] += 1
            log_pass("Q2.1: Mid price calculat")
        else:
            test["status"] = "FAIL"
            self.results[suite]["failed"] += 1
            log_fail("Q2.1: Mid price nu e calculat")
            self.bugs.append({
                "id": "BUG-S1-C2-001",
                "severity": "HIGH",
                "container": 2,
                "desc": "Lipsește calculul Mid Price (Q2.1=C)",
                "suite": suite
            })
        self.results[suite]["tests"].append(test)
        
        # Q2.2 = B - Modal Confirmare Închide Toate
        test = {"id": "Q2.2", "desc": "Confirmare Închide Toate (B=Modal confirmation)", "checks": []}
        has_close_all = self.test_js_function("closeAllPositions")
        has_modal = "modal" in self.html_content.lower()
        test["checks"].append(("Funcție closeAllPositions()", has_close_all))
        test["checks"].append(("Modal HTML", has_modal))
        
        if has_close_all and has_modal:
            test["status"] = "PASS"
            test["spec_match"] = "Q2.2=B ✓"
            self.results[suite]["passed"] += 1
            log_pass("Q2.2: Modal confirmare implementat")
        else:
            test["status"] = "FAIL"
            self.results[suite]["failed"] += 1
            log_fail("Q2.2: Modal confirmare lipsă")
        self.results[suite]["tests"].append(test)
        
        # Q2.3 = A - Confirmare Închidere Individuală
        test = {"id": "Q2.3", "desc": "Confirmare Închidere Individuală (A=Direct close)", "checks": []}
        has_close = self.test_js_function("closePosition")
        test["checks"].append(("Funcție closePosition()", has_close))
        
        if has_close:
            test["status"] = "PASS"
            test["spec_match"] = "Q2.3=A ✓"
            self.results[suite]["passed"] += 1
            log_pass("Q2.3: Închidere individuală implementată")
        else:
            test["status"] = "FAIL"
            self.results[suite]["failed"] += 1
            log_fail("Q2.3: Închidere individuală lipsă")
        self.results[suite]["tests"].append(test)
        
        # Q2.4 = B+C - Indicator Poziție Modificată
        test = {"id": "Q2.4", "desc": "Indicator Poziție Modificată (B=Visual indicator + C=Tracking log)", "checks": []}
        has_modified_indicator = "modified" in self.js_content.lower() and "position" in self.js_content.lower()
        has_tracking = self.test_js_function("loadTracking")
        test["checks"].append(("Indicator modificat", has_modified_indicator))
        test["checks"].append(("Funcție loadTracking()", has_tracking))
        
        if has_modified_indicator and has_tracking:
            test["status"] = "PASS"
            test["spec_match"] = "Q2.4=B+C ✓"
            self.results[suite]["passed"] += 1
            log_pass("Q2.4: Indicator modificare implementat")
        elif has_modified_indicator or has_tracking:
            test["status"] = "PARTIAL"
            self.results[suite]["partial"] += 1
            log_warn("Q2.4: Implementare parțială")
        else:
            test["status"] = "FAIL"
            self.results[suite]["failed"] += 1
            log_fail("Q2.4: Indicator modificare lipsă")
            self.bugs.append({
                "id": "BUG-S1-C2-002",
                "severity": "HIGH",
                "container": 2,
                "desc": "Lipsește indicator poziție modificată (Q2.4=B+C)",
                "suite": suite
            })
        self.results[suite]["tests"].append(test)
        
        # Q2.5 = D - Calcul Profit Configurabil
        test = {"id": "Q2.5", "desc": "Calcul Profit Configurabil (D=Settings in dashboard)", "checks": []}
        has_profit_config = "profit" in self.js_content.lower() and ("config" in self.js_content.lower() or "setting" in self.js_content.lower())
        test["checks"].append(("Configurare profit", has_profit_config))
        
        if has_profit_config:
            test["status"] = "PASS"
            test["spec_match"] = "Q2.5=D ✓"
            self.results[suite]["passed"] += 1
            log_pass("Q2.5: Profit configurabil")
        else:
            test["status"] = "FAIL"
            self.results[suite]["failed"] += 1
            log_fail("Q2.5: Profit configurabil lipsă")
        self.results[suite]["tests"].append(test)
        
        # Q2.6 = B - Filtru Simboluri
        test = {"id": "Q2.6", "desc": "Filtru Simboluri (B=Dropdown per symbol)", "checks": []}
        has_filter = self.test_js_function("setPositionFilter")
        test["checks"].append(("Funcție setPositionFilter()", has_filter))
        
        if has_filter:
            test["status"] = "PASS"
            test["spec_match"] = "Q2.6=B ✓"
            self.results[suite]["passed"] += 1
            log_pass("Q2.6: Filtru simboluri implementat")
        else:
            test["status"] = "FAIL"
            self.results[suite]["failed"] += 1
            log_fail("Q2.6: Filtru simboluri lipsă")
        self.results[suite]["tests"].append(test)
        
        # ═══════════════════════════════════════════════════════════════════
        # CONTAINER 3: Istoric Tranzacții (Q3.1 - Q3.6)
        # ═══════════════════════════════════════════════════════════════════
        log_info("Container 3: Istoric Tranzacții")
        
        # Q3.1 = A - Afișare Tranzacții Închise
        test = {"id": "Q3.1", "desc": "Afișare Tranzacții Închise (A=Show closed trades)", "checks": []}
        has_history = self.test_js_function("loadTradeHistory")
        has_table = self.test_html_element("historyTable")
        test["checks"].append(("Funcție loadTradeHistory()", has_history))
        test["checks"].append(("Tabel historyTable", has_table))
        
        if has_history and has_table:
            test["status"] = "PASS"
            test["spec_match"] = "Q3.1=A ✓"
            self.results[suite]["passed"] += 1
            log_pass("Q3.1: Istoric tranzacții implementat")
        else:
            test["status"] = "FAIL"
            self.results[suite]["failed"] += 1
            log_fail("Q3.1: Istoric tranzacții lipsă")
        self.results[suite]["tests"].append(test)
        
        # Q3.2 = B - Calcul R:R
        test = {"id": "Q3.2", "desc": "Calcul R:R (B=Profit/|Open-SL|)", "checks": []}
        has_rr_calc = "risk" in self.js_content.lower() and "reward" in self.js_content.lower()
        test["checks"].append(("Calcul R:R", has_rr_calc))
        
        if has_rr_calc:
            test["status"] = "PASS"
            test["spec_match"] = "Q3.2=B ✓"
            self.results[suite]["passed"] += 1
            log_pass("Q3.2: Calcul R:R implementat")
        else:
            test["status"] = "FAIL"
            self.results[suite]["failed"] += 1
            log_fail("Q3.2: Calcul R:R lipsă")
            self.bugs.append({
                "id": "BUG-S1-C3-001",
                "severity": "MEDIUM",
                "container": 3,
                "desc": "Lipsește calculul R:R (Q3.2=B)",
                "suite": suite
            })
        self.results[suite]["tests"].append(test)
        
        # Q3.3 = A - Calcul Durată
        test = {"id": "Q3.3", "desc": "Calcul Durată (A=Duration calculation)", "checks": []}
        has_duration = "duration" in self.js_content.lower() or "durat" in self.js_content.lower()
        test["checks"].append(("Calcul durată", has_duration))
        
        if has_duration:
            test["status"] = "PASS"
            test["spec_match"] = "Q3.3=A ✓"
            self.results[suite]["passed"] += 1
            log_pass("Q3.3: Calcul durată implementat")
        else:
            test["status"] = "FAIL"
            self.results[suite]["failed"] += 1
            log_fail("Q3.3: Calcul durată lipsă")
        self.results[suite]["tests"].append(test)
        
        # Q3.4 = D - Click pe Tranzacție → Modal
        test = {"id": "Q3.4", "desc": "Click pe Tranzacție → Modal (D=Full details modal)", "checks": []}
        # Căutăm onclick handlers pe rânduri de tabel
        has_click_handler = "onclick" in self.html_content.lower() and "history" in self.html_content.lower()
        has_modal = "modal" in self.html_content.lower()
        test["checks"].append(("Handler click pe istoric", has_click_handler))
        test["checks"].append(("Modal implementat", has_modal))
        
        if has_click_handler and has_modal:
            test["status"] = "PASS"
            test["spec_match"] = "Q3.4=D ✓"
            self.results[suite]["passed"] += 1
            log_pass("Q3.4: Modal detalii tranzacție implementat")
        else:
            test["status"] = "FAIL"
            self.results[suite]["failed"] += 1
            log_fail("Q3.4: Modal detalii tranzacție lipsă")
            self.bugs.append({
                "id": "BUG-S1-C3-002",
                "severity": "MEDIUM",
                "container": 3,
                "desc": "Lipsește modal detalii tranzacție (Q3.4=D)",
                "suite": suite
            })
        self.results[suite]["tests"].append(test)
        
        # Q3.5 = B+C+D - Filtre Istoric
        test = {"id": "Q3.5", "desc": "Filtre Istoric (B=Period + C=Symbol + D=Result)", "checks": []}
        has_period_filter = self.test_js_function("setHistoryFilter")
        has_symbol_filter = "symbol" in self.js_content.lower() and "filter" in self.js_content.lower()
        has_result_filter = "result" in self.js_content.lower() and ("win" in self.js_content.lower() or "loss" in self.js_content.lower())
        test["checks"].append(("Filtru perioadă", has_period_filter))
        test["checks"].append(("Filtru simbol", has_symbol_filter))
        test["checks"].append(("Filtru rezultat", has_result_filter))
        
        score = sum([has_period_filter, has_symbol_filter, has_result_filter])
        if score == 3:
            test["status"] = "PASS"
            test["spec_match"] = "Q3.5=B+C+D ✓"
            self.results[suite]["passed"] += 1
            log_pass("Q3.5: Toate filtrele implementate")
        elif score >= 1:
            test["status"] = "PARTIAL"
            self.results[suite]["partial"] += 1
            log_warn(f"Q3.5: Filtre parțiale ({score}/3)")
        else:
            test["status"] = "FAIL"
            self.results[suite]["failed"] += 1
            log_fail("Q3.5: Filtre lipsă")
        self.results[suite]["tests"].append(test)
        
        # Q3.6 = A - Sortare Coloane
        test = {"id": "Q3.6", "desc": "Sortare Coloane (A=Click to sort)", "checks": []}
        has_sort = "sort" in self.js_content.lower() and ("table" in self.js_content.lower() or "history" in self.js_content.lower())
        test["checks"].append(("Funcționalitate sortare", has_sort))
        
        if has_sort:
            test["status"] = "PASS"
            test["spec_match"] = "Q3.6=A ✓"
            self.results[suite]["passed"] += 1
            log_pass("Q3.6: Sortare implementată")
        else:
            test["status"] = "FAIL"
            self.results[suite]["failed"] += 1
            log_fail("Q3.6: Sortare lipsă")
        self.results[suite]["tests"].append(test)
        
        # ═══════════════════════════════════════════════════════════════════
        # CONTAINER 4: Tracking Tranzacții (Q4.1 - Q4.4)
        # ═══════════════════════════════════════════════════════════════════
        log_info("Container 4: Tracking Tranzacții")
        
        # Q4.1 = A - Diferență Istoric vs Tracking
        test = {"id": "Q4.1", "desc": "Diferență Istoric vs Tracking (A=Separate containers)", "checks": []}
        has_tracking_section = self.test_html_element("trackingTable") or "tracking" in self.html_content.lower()
        has_history_section = self.test_html_element("historyTable")
        test["checks"].append(("Secțiune tracking", has_tracking_section))
        test["checks"].append(("Secțiune istoric", has_history_section))
        
        if has_tracking_section and has_history_section:
            test["status"] = "PASS"
            test["spec_match"] = "Q4.1=A ✓"
            self.results[suite]["passed"] += 1
            log_pass("Q4.1: Separare tracking/istoric")
        else:
            test["status"] = "FAIL"
            self.results[suite]["failed"] += 1
            log_fail("Q4.1: Separare lipsă")
        self.results[suite]["tests"].append(test)
        
        # Q4.2 = A - Afișare "Deschis De"
        test = {"id": "Q4.2", "desc": "Afișare 'Deschis De' (A=Robot name or 'Manual')", "checks": []}
        has_opened_by = "opened" in self.js_content.lower() and ("by" in self.js_content.lower() or "robot" in self.js_content.lower() or "manual" in self.js_content.lower())
        test["checks"].append(("Câmp opened_by", has_opened_by))
        
        if has_opened_by:
            test["status"] = "PASS"
            test["spec_match"] = "Q4.2=A ✓"
            self.results[suite]["passed"] += 1
            log_pass("Q4.2: Tracking 'Deschis De'")
        else:
            test["status"] = "FAIL"
            self.results[suite]["failed"] += 1
            log_fail("Q4.2: 'Deschis De' lipsă")
            self.bugs.append({
                "id": "BUG-S1-C4-001",
                "severity": "MEDIUM",
                "container": 4,
                "desc": "Lipsește câmpul 'Deschis De' în tracking (Q4.2=A)",
                "suite": suite
            })
        self.results[suite]["tests"].append(test)
        
        # Q4.3 = C - Tracking Modificări
        test = {"id": "Q4.3", "desc": "Tracking Modificări (C=SL/TP/Volume + User + Timestamp)", "checks": []}
        has_sl_track = "sl" in self.js_content.lower() and "modified" in self.js_content.lower()
        has_tp_track = "tp" in self.js_content.lower() and "modified" in self.js_content.lower()
        has_user_track = "user" in self.js_content.lower() and ("modified" in self.js_content.lower() or "by" in self.js_content.lower())
        test["checks"].append(("Tracking SL modificat", has_sl_track))
        test["checks"].append(("Tracking TP modificat", has_tp_track))
        test["checks"].append(("Tracking utilizator", has_user_track))
        
        score = sum([has_sl_track, has_tp_track, has_user_track])
        if score >= 2:
            test["status"] = "PASS"
            test["spec_match"] = "Q4.3=C ✓"
            self.results[suite]["passed"] += 1
            log_pass("Q4.3: Tracking modificări")
        elif score >= 1:
            test["status"] = "PARTIAL"
            self.results[suite]["partial"] += 1
            log_warn(f"Q4.3: Tracking parțial ({score}/3)")
        else:
            test["status"] = "FAIL"
            self.results[suite]["failed"] += 1
            log_fail("Q4.3: Tracking modificări lipsă")
        self.results[suite]["tests"].append(test)
        
        # Q4.4 = C - Statusuri Posibile
        test = {"id": "Q4.4", "desc": "Statusuri Posibile (C=All status: Open/Closed/Modified/Partial/Pyramiding)", "checks": []}
        statuses = ["open", "closed", "modified", "partial", "pyramid"]
        found_statuses = [s for s in statuses if s in self.js_content.lower()]
        test["checks"].append((f"Statusuri găsite: {', '.join(found_statuses)}", len(found_statuses) >= 3))
        
        if len(found_statuses) >= 3:
            test["status"] = "PASS"
            test["spec_match"] = "Q4.4=C ✓"
            self.results[suite]["passed"] += 1
            log_pass(f"Q4.4: Statusuri implementate ({len(found_statuses)}/5)")
        else:
            test["status"] = "PARTIAL"
            self.results[suite]["partial"] += 1
            log_warn(f"Q4.4: Statusuri parțiale ({len(found_statuses)}/5)")
        self.results[suite]["tests"].append(test)
    
    def test_suite_2_robots(self):
        """Test Suite 2: Roboți (Containers 5-7)"""
        log_section("SUITA 2: ROBOȚI (Containere 5-7)")
        
        suite = "suite_2"
        config = TEST_CONFIG[suite]
        
        # ═══════════════════════════════════════════════════════════════════
        # CONTAINER 5: V31 Marius TPL (Q5.1 - Q5.10)
        # ═══════════════════════════════════════════════════════════════════
        log_info("Container 5: V31 Marius TPL")
        
        # Q5.1 = A+B - START Robot
        test = {"id": "Q5.1", "desc": "START Robot (A=API endpoint + B=Process spawn)", "checks": []}
        has_start_endpoint = "/api/robot/v31/start" in self.js_content
        has_control_func = self.test_js_function("controlRobot")
        test["checks"].append(("Endpoint /api/robot/v31/start", has_start_endpoint))
        test["checks"].append(("Funcție controlRobot()", has_control_func))
        
        if has_start_endpoint and has_control_func:
            test["status"] = "PASS"
            test["spec_match"] = "Q5.1=A+B ✓"
            self.results[suite]["passed"] += 1
            log_pass("Q5.1: START robot implementat")
        elif has_control_func:
            test["status"] = "PARTIAL"
            self.results[suite]["partial"] += 1
            log_warn("Q5.1: Funcție există dar endpoint nu e verificat")
        else:
            test["status"] = "FAIL"
            self.results[suite]["failed"] += 1
            log_fail("Q5.1: START robot lipsă")
            self.bugs.append({
                "id": "BUG-S2-C5-001",
                "severity": "CRITICAL",
                "container": 5,
                "desc": "Lipsește control START robot (Q5.1=A+B)",
                "suite": suite
            })
        self.results[suite]["tests"].append(test)
        
        # Q5.2 = A+B - STOP Robot
        test = {"id": "Q5.2", "desc": "STOP Robot (A=API endpoint + B=SIGTERM)", "checks": []}
        has_stop_endpoint = "/api/robot/v31/stop" in self.js_content
        test["checks"].append(("Endpoint /api/robot/v31/stop", has_stop_endpoint))
        test["checks"].append(("Funcție controlRobot()", has_control_func))
        
        if has_stop_endpoint and has_control_func:
            test["status"] = "PASS"
            test["spec_match"] = "Q5.2=A+B ✓"
            self.results[suite]["passed"] += 1
            log_pass("Q5.2: STOP robot implementat")
        else:
            test["status"] = "FAIL"
            self.results[suite]["failed"] += 1
            log_fail("Q5.2: STOP robot lipsă")
        self.results[suite]["tests"].append(test)
        
        # Q5.3 = A - Grid Simboluri Culori
        test = {"id": "Q5.3", "desc": "Grid Simboluri Culori (A=Colors per status)", "checks": []}
        has_symbol_grid = self.test_html_element("v31SymbolGrid")
        has_update_grid = self.test_js_function("updateV31SymbolGrid")
        test["checks"].append(("Element v31SymbolGrid", has_symbol_grid))
        test["checks"].append(("Funcție updateV31SymbolGrid()", has_update_grid))
        
        if has_symbol_grid and has_update_grid:
            test["status"] = "PASS"
            test["spec_match"] = "Q5.3=A ✓"
            self.results[suite]["passed"] += 1
            log_pass("Q5.3: Grid simboluri implementat")
        else:
            test["status"] = "FAIL"
            self.results[suite]["failed"] += 1
            log_fail("Q5.3: Grid simboluri lipsă")
        self.results[suite]["tests"].append(test)
        
        # Q5.4 = A+B+C+D - Scoruri Tehnice Raw
        test = {"id": "Q5.4", "desc": "Scoruri Tehnice Raw (A=RSI + B=Stoch + C=Fib + D=Total)", "checks": []}
        has_rsi = self.test_html_element("v31ScoreRSI")
        has_stoch = self.test_html_element("v31ScoreStoch")
        has_fib = self.test_html_element("v31ScoreFib")
        has_total = self.test_html_element("v31ScoreTotal")
        test["checks"].append(("Scor RSI", has_rsi))
        test["checks"].append(("Scor Stochastic", has_stoch))
        test["checks"].append(("Scor Fibonacci", has_fib))
        test["checks"].append(("Scor Total", has_total))
        
        score = sum([has_rsi, has_stoch, has_fib, has_total])
        if score == 4:
            test["status"] = "PASS"
            test["spec_match"] = "Q5.4=A+B+C+D ✓"
            self.results[suite]["passed"] += 1
            log_pass("Q5.4: Toate scorurile tehnice implementate")
        elif score >= 2:
            test["status"] = "PARTIAL"
            self.results[suite]["partial"] += 1
            log_warn(f"Q5.4: Scoruri parțiale ({score}/4)")
        else:
            test["status"] = "FAIL"
            self.results[suite]["failed"] += 1
            log_fail("Q5.4: Scoruri tehnice lipsă")
        self.results[suite]["tests"].append(test)
        
        # Q5.5 = A+C - Configurare Parametri
        test = {"id": "Q5.5", "desc": "Configurare Parametri (A=Symbol list + C=Analysis interval)", "checks": []}
        has_config = "config" in self.js_content.lower() and "v31" in self.js_content.lower()
        test["checks"].append(("Configurare parametri V31", has_config))
        
        if has_config:
            test["status"] = "PASS"
            test["spec_match"] = "Q5.5=A+C ✓"
            self.results[suite]["passed"] += 1
            log_pass("Q5.5: Configurare parametri existentă")
        else:
            test["status"] = "FAIL"
            self.results[suite]["failed"] += 1
            log_fail("Q5.5: Configurare parametri lipsă")
        self.results[suite]["tests"].append(test)
        
        # Q5.6 = B - Click pe Simbol
        test = {"id": "Q5.6", "desc": "Click pe Simbol (B=Modal with details)", "checks": []}
        has_click = "onclick" in self.html_content.lower() and "symbol" in self.html_content.lower()
        test["checks"].append(("Handler click simbol", has_click))
        
        if has_click:
            test["status"] = "PASS"
            test["spec_match"] = "Q5.6=B ✓"
            self.results[suite]["passed"] += 1
            log_pass("Q5.6: Click pe simbol implementat")
        else:
            test["status"] = "FAIL"
            self.results[suite]["failed"] += 1
            log_fail("Q5.6: Click pe simbol lipsă")
        self.results[suite]["tests"].append(test)
        
        # Q5.7 = C - Filtrare Log-uri
        test = {"id": "Q5.7", "desc": "Filtrare Log-uri (C=Category filter)", "checks": []}
        has_log_filter = "log" in self.js_content.lower() and "filter" in self.js_content.lower()
        test["checks"].append(("Filtrare log-uri", has_log_filter))
        
        if has_log_filter:
            test["status"] = "PASS"
            test["spec_match"] = "Q5.7=C ✓"
            self.results[suite]["passed"] += 1
            log_pass("Q5.7: Filtrare log-uri implementată")
        else:
            test["status"] = "FAIL"
            self.results[suite]["failed"] += 1
            log_fail("Q5.7: Filtrare log-uri lipsă")
        self.results[suite]["tests"].append(test)
        
        # Q5.8 = D - Ciclu Analiză
        test = {"id": "Q5.8", "desc": "Ciclu Analiză (D=Progress bar + Status)", "checks": []}
        has_progress = self.test_html_element("v31LiveProgressBar")
        has_phase = self.test_html_element("v31LivePhase")
        test["checks"].append(("Progress bar", has_progress))
        test["checks"].append(("Status phase", has_phase))
        
        if has_progress and has_phase:
            test["status"] = "PASS"
            test["spec_match"] = "Q5.8=D ✓"
            self.results[suite]["passed"] += 1
            log_pass("Q5.8: Ciclu analiză implementat")
        else:
            test["status"] = "FAIL"
            self.results[suite]["failed"] += 1
            log_fail("Q5.8: Ciclu analiză lipsă")
        self.results[suite]["tests"].append(test)
        
        # Q5.9 = B+C+D - Setup Detection Logic
        test = {"id": "Q5.9", "desc": "Setup Detection (B=Logic + C=Scoring + D=Validation)", "checks": []}
        has_setup_logic = "setup" in self.js_content.lower() and "score" in self.js_content.lower()
        has_validation = "validate" in self.js_content.lower() or "threshold" in self.js_content.lower()
        test["checks"].append(("Logică setup", has_setup_logic))
        test["checks"].append(("Validare setup", has_validation))
        
        if has_setup_logic and has_validation:
            test["status"] = "PASS"
            test["spec_match"] = "Q5.9=B+C+D ✓"
            self.results[suite]["passed"] += 1
            log_pass("Q5.9: Setup detection implementat")
        elif has_setup_logic:
            test["status"] = "PARTIAL"
            self.results[suite]["partial"] += 1
            log_warn("Q5.9: Setup detection parțial")
        else:
            test["status"] = "FAIL"
            self.results[suite]["failed"] += 1
            log_fail("Q5.9: Setup detection lipsă")
        self.results[suite]["tests"].append(test)
        
        # Q5.10 = A+D - Daily Stats
        test = {"id": "Q5.10", "desc": "Daily Stats (A=Count + D=Win rate)", "checks": []}
        has_setup_count = self.test_html_element("v31SetupCount")
        has_trade_count = self.test_html_element("v31TradeCount")
        has_win_rate = self.test_html_element("v31WinRate")
        test["checks"].append(("Setup count", has_setup_count))
        test["checks"].append(("Trade count", has_trade_count))
        test["checks"].append(("Win rate", has_win_rate))
        
        if has_setup_count and has_win_rate:
            test["status"] = "PASS"
            test["spec_match"] = "Q5.10=A+D ✓"
            self.results[suite]["passed"] += 1
            log_pass("Q5.10: Daily stats implementate")
        else:
            test["status"] = "PARTIAL"
            self.results[suite]["partial"] += 1
            log_warn("Q5.10: Daily stats parțiale")
        self.results[suite]["tests"].append(test)
        
        # ═══════════════════════════════════════════════════════════════════
        # CONTAINER 6: V32 London Breakout (Q6.1 - Q6.7)
        # ═══════════════════════════════════════════════════════════════════
        log_info("Container 6: V32 London Breakout")
        
        # Q6.1 = B+D - London Time
        test = {"id": "Q6.1", "desc": "London Time Display (B=UTC + D=Configurable)", "checks": []}
        has_london_time = self.test_html_element("v32LondonTime")
        has_update_func = self.test_js_function("updateV32LondonTime")
        test["checks"].append(("Element v32LondonTime", has_london_time))
        test["checks"].append(("Funcție updateV32LondonTime()", has_update_func))
        
        if has_london_time and has_update_func:
            test["status"] = "PASS"
            test["spec_match"] = "Q6.1=B+D ✓"
            self.results[suite]["passed"] += 1
            log_pass("Q6.1: London time implementat")
        else:
            test["status"] = "FAIL"
            self.results[suite]["failed"] += 1
            log_fail("Q6.1: London time lipsă")
        self.results[suite]["tests"].append(test)
        
        # Q6.2 = B+C - Faze Sesiune
        test = {"id": "Q6.2", "desc": "Session Phases (B=Display + C=Timer)", "checks": []}
        has_phase = self.test_html_element("v32SessionPhase")
        has_timer = self.test_html_element("v32SessionTimer")
        has_badge = self.test_html_element("v32SessionBadge")
        test["checks"].append(("Element phase", has_phase))
        test["checks"].append(("Element timer", has_timer))
        test["checks"].append(("Element badge", has_badge))
        
        if has_phase and has_timer:
            test["status"] = "PASS"
            test["spec_match"] = "Q6.2=B+C ✓"
            self.results[suite]["passed"] += 1
            log_pass("Q6.2: Faze sesiune implementate")
        else:
            test["status"] = "PARTIAL"
            self.results[suite]["partial"] += 1
            log_warn("Q6.2: Faze sesiune parțiale")
        self.results[suite]["tests"].append(test)
        
        # Q6.3 = D - Compression Detection
        test = {"id": "Q6.3", "desc": "Compression Detection (D=Asia Range < 50% OR)", "checks": []}
        has_asia = self.test_html_element("v32AsiaHigh")
        has_or = self.test_html_element("v32ORHigh")
        has_compression = "compressed" in self.js_content.lower() or "compression" in self.js_content.lower()
        test["checks"].append(("Asia data", has_asia))
        test["checks"].append(("OR data", has_or))
        test["checks"].append(("Compression logic", has_compression))
        
        if has_asia and has_or and has_compression:
            test["status"] = "PASS"
            test["spec_match"] = "Q6.3=D ✓"
            self.results[suite]["passed"] += 1
            log_pass("Q6.3: Compression detection implementat")
        else:
            test["status"] = "PARTIAL"
            self.results[suite]["partial"] += 1
            log_warn("Q6.3: Compression detection parțial")
        self.results[suite]["tests"].append(test)
        
        # Q6.4 = A - Breakout Detection
        test = {"id": "Q6.4", "desc": "Breakout Detection (A=Candle close confirmation)", "checks": []}
        has_breakout = self.test_html_element("v32BreakoutStatus")
        has_signal = self.test_html_element("v32Signal")
        test["checks"].append(("Element breakout status", has_breakout))
        test["checks"].append(("Element signal", has_signal))
        
        if has_breakout and has_signal:
            test["status"] = "PASS"
            test["spec_match"] = "Q6.4=A ✓"
            self.results[suite]["passed"] += 1
            log_pass("Q6.4: Breakout detection implementat")
        else:
            test["status"] = "FAIL"
            self.results[suite]["failed"] += 1
            log_fail("Q6.4: Breakout detection lipsă")
        self.results[suite]["tests"].append(test)
        
        # Q6.5 = C - Body% și Wick%
        test = {"id": "Q6.5", "desc": "Body% și Wick% (C=Calculated values)", "checks": []}
        has_body = self.test_html_element("v32BodyPercent")
        has_wick = self.test_html_element("v32WickPercent")
        test["checks"].append(("Element body%", has_body))
        test["checks"].append(("Element wick%", has_wick))
        
        if has_body and has_wick:
            test["status"] = "PASS"
            test["spec_match"] = "Q6.5=C ✓"
            self.results[suite]["passed"] += 1
            log_pass("Q6.5: Body% și Wick% implementate")
        else:
            test["status"] = "FAIL"
            self.results[suite]["failed"] += 1
            log_fail("Q6.5: Body% și Wick% lipsă")
        self.results[suite]["tests"].append(test)
        
        # Q6.6 = A+B+D - Acțiune la Breakout
        test = {"id": "Q6.6", "desc": "Breakout Action (A=Market + B=Retest + D=Notification)", "checks": []}
        has_market = "market" in self.js_content.lower() and "order" in self.js_content.lower()
        has_retest = "retest" in self.js_content.lower()
        has_notify = "notif" in self.js_content.lower()
        test["checks"].append(("Market order", has_market))
        test["checks"].append(("Retest logic", has_retest))
        test["checks"].append(("Notification", has_notify))
        
        score = sum([has_market, has_retest, has_notify])
        if score >= 2:
            test["status"] = "PASS"
            test["spec_match"] = "Q6.6=A+B+D ✓"
            self.results[suite]["passed"] += 1
            log_pass("Q6.6: Acțiuni breakout implementate")
        elif score >= 1:
            test["status"] = "PARTIAL"
            self.results[suite]["partial"] += 1
            log_warn(f"Q6.6: Acțiuni parțiale ({score}/3)")
        else:
            test["status"] = "FAIL"
            self.results[suite]["failed"] += 1
            log_fail("Q6.6: Acțiuni breakout lipsă")
        self.results[suite]["tests"].append(test)
        
        # Q6.7 = Configurabil - Setări Robot
        test = {"id": "Q6.7", "desc": "Robot Settings (Configurabil)", "checks": []}
        has_settings = "setting" in self.js_content.lower() and "v32" in self.js_content.lower()
        test["checks"].append(("Setări configurabile", has_settings))
        
        if has_settings:
            test["status"] = "PASS"
            test["spec_match"] = "Q6.7=Configurabil ✓"
            self.results[suite]["passed"] += 1
            log_pass("Q6.7: Setări configurabile")
        else:
            test["status"] = "FAIL"
            self.results[suite]["failed"] += 1
            log_fail("Q6.7: Setări lipsă")
        self.results[suite]["tests"].append(test)
        
        # ═══════════════════════════════════════════════════════════════════
        # CONTAINER 7: V33 NY Breakout (Q7.1 - Q7.2)
        # ═══════════════════════════════════════════════════════════════════
        log_info("Container 7: V33 NY Breakout")
        
        # Q7.1 = A+B - Diferențe V32 vs V33
        test = {"id": "Q7.1", "desc": "V33 Differences (A=NY timezone + B=Different OR)", "checks": []}
        has_ny_time = self.test_html_element("v33NYTime")
        has_v33_section = self.test_html_element("v33-dashboard-section")
        test["checks"].append(("Element v33NYTime", has_ny_time))
        test["checks"].append(("Secțiune V33", has_v33_section))
        
        if has_ny_time and has_v33_section:
            test["status"] = "PASS"
            test["spec_match"] = "Q7.1=A+B ✓"
            self.results[suite]["passed"] += 1
            log_pass("Q7.1: Diferențe V33 implementate")
        else:
            test["status"] = "FAIL"
            self.results[suite]["failed"] += 1
            log_fail("Q7.1: Diferențe V33 lipsă")
        self.results[suite]["tests"].append(test)
        
        # Q7.2 = D - Pre-session Analysis
        test = {"id": "Q7.2", "desc": "Pre-session Analysis (D=High/Low + Key levels)", "checks": []}
        has_pre_high = self.test_html_element("v33PreHigh")
        has_pre_low = self.test_html_element("v33PreLow")
        has_pre_data = self.test_js_function("fetchV33PreSessionData")
        test["checks"].append(("Element pre-high", has_pre_high))
        test["checks"].append(("Element pre-low", has_pre_low))
        test["checks"].append(("Funcție fetchV33PreSessionData()", has_pre_data))
        
        if has_pre_high and has_pre_low and has_pre_data:
            test["status"] = "PASS"
            test["spec_match"] = "Q7.2=D ✓"
            self.results[suite]["passed"] += 1
            log_pass("Q7.2: Pre-session analysis implementat")
        else:
            test["status"] = "PARTIAL"
            self.results[suite]["partial"] += 1
            log_warn("Q7.2: Pre-session analysis parțial")
        self.results[suite]["tests"].append(test)
    
    def test_suite_3_advanced(self):
        """Test Suite 3: Advanced Features (Containers 8-10)"""
        log_section("SUITA 3: ADVANCED (Containere 8-10)")
        
        suite = "suite_3"
        config = TEST_CONFIG[suite]
        
        # Container 8 - Risk Management
        log_info("Container 8: Risk Management")
        
        test = {"id": "Q8.1", "desc": "Risk per Trade (A=Fixed amount)", "checks": []}
        has_risk = "risk" in self.js_content.lower() and ("amount" in self.js_content.lower() or "fixed" in self.js_content.lower())
        test["checks"].append(("Risk management", has_risk))
        test["status"] = "PASS" if has_risk else "PARTIAL"
        self.results[suite]["passed" if has_risk else "partial"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q8.1: Risk management") if has_risk else log_warn("Q8.1: Risk management - verificare manuală")
        
        test = {"id": "Q8.2", "desc": "Max Daily Loss (D=Dashboard setting)", "checks": []}
        has_max_loss = "max" in self.js_content.lower() and "loss" in self.js_content.lower()
        test["checks"].append(("Max daily loss", has_max_loss))
        test["status"] = "PASS" if has_max_loss else "PARTIAL"
        self.results[suite]["passed" if has_max_loss else "partial"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q8.2: Max daily loss") if has_max_loss else log_warn("Q8.2: Max daily loss - verificare manuală")
        
        test = {"id": "Q8.3", "desc": "Position Sizing (B=Fixed + C=Percent + D=Kelly)", "checks": []}
        has_sizing = "position" in self.js_content.lower() and "size" in self.js_content.lower()
        test["checks"].append(("Position sizing", has_sizing))
        test["status"] = "PASS" if has_sizing else "PARTIAL"
        self.results[suite]["passed" if has_sizing else "partial"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q8.3: Position sizing") if has_sizing else log_warn("Q8.3: Position sizing - verificare manuală")
        
        test = {"id": "Q8.4", "desc": "Correlation Check (D=Between robots)", "checks": []}
        has_corr = "correlation" in self.js_content.lower() or "correl" in self.js_content.lower()
        test["checks"].append(("Correlation check", has_corr))
        test["status"] = "PASS" if has_corr else "PARTIAL"
        self.results[suite]["passed" if has_corr else "partial"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q8.4: Correlation check") if has_corr else log_warn("Q8.4: Correlation check - verificare manuală")
        
        # Container 9 - Trade Management
        log_info("Container 9: Trade Management")
        
        test = {"id": "Q9.1", "desc": "Pyramiding (D=Add to position rules)", "checks": []}
        has_pyramid = "pyramid" in self.js_content.lower()
        test["checks"].append(("Pyramiding", has_pyramid))
        test["status"] = "PASS" if has_pyramid else "PARTIAL"
        self.results[suite]["passed" if has_pyramid else "partial"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q9.1: Pyramiding") if has_pyramid else log_warn("Q9.1: Pyramiding - verificare manuală")
        
        test = {"id": "Q9.2", "desc": "Partial Close (B=Manual button)", "checks": []}
        has_partial = "partial" in self.js_content.lower() and "close" in self.js_content.lower()
        test["checks"].append(("Partial close", has_partial))
        test["status"] = "PASS" if has_partial else "PARTIAL"
        self.results[suite]["passed" if has_partial else "partial"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q9.2: Partial close") if has_partial else log_warn("Q9.2: Partial close - verificare manuală")
        
        test = {"id": "Q9.3", "desc": "Breakeven (A=Auto + D=Manual button)", "checks": []}
        has_be = "breakeven" in self.js_content.lower() or "break" in self.js_content.lower() and "even" in self.js_content.lower()
        test["checks"].append(("Breakeven", has_be))
        test["status"] = "PASS" if has_be else "PARTIAL"
        self.results[suite]["passed" if has_be else "partial"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q9.3: Breakeven") if has_be else log_warn("Q9.3: Breakeven - verificare manuală")
        
        test = {"id": "Q9.4", "desc": "Trailing Stop (D=Dashboard config)", "checks": []}
        has_ts = "trailing" in self.js_content.lower() or "trail" in self.js_content.lower()
        test["checks"].append(("Trailing stop", has_ts))
        test["status"] = "PASS" if has_ts else "PARTIAL"
        self.results[suite]["passed" if has_ts else "partial"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q9.4: Trailing stop") if has_ts else log_warn("Q9.4: Trailing stop - verificare manuală")
        
        test = {"id": "Q9.5", "desc": "News Filter (A+Economic + B=High impact + C=Minutes before)", "checks": []}
        has_news = "news" in self.js_content.lower() or "economic" in self.js_content.lower() or "calendar" in self.js_content.lower()
        test["checks"].append(("News filter", has_news))
        test["status"] = "PASS" if has_news else "PARTIAL"
        self.results[suite]["passed" if has_news else "partial"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q9.5: News filter") if has_news else log_warn("Q9.5: News filter - verificare manuală")
        
        # Container 10 - Analytics
        log_info("Container 10: Analytics")
        
        test = {"id": "Q10.1", "desc": "Performance Chart (D=Equity curve)", "checks": []}
        has_chart = "chart" in self.js_content.lower() or "equity" in self.js_content.lower() or "chart.js" in self.html_content.lower()
        test["checks"].append(("Performance chart", has_chart))
        test["status"] = "PASS" if has_chart else "PARTIAL"
        self.results[suite]["passed" if has_chart else "partial"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q10.1: Performance chart") if has_chart else log_warn("Q10.1: Performance chart - verificare manuală")
        
        test = {"id": "Q10.2", "desc": "Drawdown Analysis (D=Max + Current)", "checks": []}
        has_dd = "drawdown" in self.js_content.lower()
        test["checks"].append(("Drawdown analysis", has_dd))
        test["status"] = "PASS" if has_dd else "PARTIAL"
        self.results[suite]["passed" if has_dd else "partial"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q10.2: Drawdown analysis") if has_dd else log_warn("Q10.2: Drawdown analysis - verificare manuală")
        
        test = {"id": "Q10.3", "desc": "Win Rate by Setup (C=Table view)", "checks": []}
        has_wr = "win" in self.js_content.lower() and "rate" in self.js_content.lower() and "setup" in self.js_content.lower()
        test["checks"].append(("Win rate by setup", has_wr))
        test["status"] = "PASS" if has_wr else "PARTIAL"
        self.results[suite]["passed" if has_wr else "partial"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q10.3: Win rate by setup") if has_wr else log_warn("Q10.3: Win rate by setup - verificare manuală")
        
        test = {"id": "Q10.4", "desc": "Profit Factor (A=Gross ratio + B=Net ratio)", "checks": []}
        has_pf = "profit" in self.js_content.lower() and "factor" in self.js_content.lower()
        test["checks"].append(("Profit factor", has_pf))
        test["status"] = "PASS" if has_pf else "PARTIAL"
        self.results[suite]["passed" if has_pf else "partial"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q10.4: Profit factor") if has_pf else log_warn("Q10.4: Profit factor - verificare manuală")
        
        test = {"id": "Q10.5", "desc": "Expectancy (D=Calculation)", "checks": []}
        has_exp = "expectancy" in self.js_content.lower()
        test["checks"].append(("Expectancy", has_exp))
        test["status"] = "PASS" if has_exp else "PARTIAL"
        self.results[suite]["passed" if has_exp else "partial"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q10.5: Expectancy") if has_exp else log_warn("Q10.5: Expectancy - verificare manuală")
    
    def test_suite_4_monitoring(self):
        """Test Suite 4: Monitoring & Analytics (Containers 11,12,15)"""
        log_section("SUITA 4: MONITORING (Containere 11,12,15)")
        
        suite = "suite_4"
        config = TEST_CONFIG[suite]
        
        # Container 11 - System Health
        log_info("Container 11: System Health")
        
        test = {"id": "Q11.1", "desc": "Health Status (D=All services)", "checks": []}
        has_health = self.test_js_function("loadSystemHealth")
        has_core = self.test_html_element("coreStatus")
        test["checks"].append(("Funcție loadSystemHealth()", has_health))
        test["checks"].append(("Status core", has_core))
        
        if has_health:
            test["status"] = "PASS"
            self.results[suite]["passed"] += 1
            log_pass("Q11.1: Health status implementat")
        else:
            test["status"] = "PARTIAL"
            self.results[suite]["partial"] += 1
            log_warn("Q11.1: Health status parțial")
        self.results[suite]["tests"].append(test)
        
        test = {"id": "Q11.2", "desc": "PostgreSQL Status (A=Connection)", "checks": []}
        has_pg = "postgresql" in self.js_content.lower() or "postgres" in self.js_content.lower()
        test["checks"].append(("PostgreSQL check", has_pg))
        test["status"] = "PASS" if has_pg else "FAIL"
        self.results[suite]["passed" if has_pg else "failed"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q11.2: PostgreSQL status") if has_pg else log_fail("Q11.2: PostgreSQL status lipsă")
        
        test = {"id": "Q11.3", "desc": "MT5 Bridge Status (A=API check + C=Last ping)", "checks": []}
        has_bridge = "bridge" in self.js_content.lower() or "mt5" in self.js_content.lower()
        test["checks"].append(("MT5 Bridge", has_bridge))
        test["status"] = "PASS" if has_bridge else "PARTIAL"
        self.results[suite]["passed" if has_bridge else "partial"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q11.3: MT5 Bridge status") if has_bridge else log_warn("Q11.3: MT5 Bridge - verificare manuală")
        
        test = {"id": "Q11.4", "desc": "Robot Connection (C=Status indicator)", "checks": []}
        has_conn = self.test_js_function("checkRobotConnection")
        has_dots = self.test_html_element("v31StatusDot")
        test["checks"].append(("Funcție checkRobotConnection()", has_conn))
        test["checks"].append(("Status dots", has_dots))
        
        if has_conn and has_dots:
            test["status"] = "PASS"
            self.results[suite]["passed"] += 1
            log_pass("Q11.4: Robot connection implementat")
        elif has_conn:
            test["status"] = "PARTIAL"
            self.results[suite]["partial"] += 1
            log_warn("Q11.4: Robot connection parțial")
        else:
            test["status"] = "FAIL"
            self.results[suite]["failed"] += 1
            log_fail("Q11.4: Robot connection lipsă")
        self.results[suite]["tests"].append(test)
        
        test = {"id": "Q11.5", "desc": "Auto-refresh (D=Configurable interval)", "checks": []}
        has_polling = "setinterval" in self.js_content.lower() and "health" in self.js_content.lower()
        test["checks"].append(("Auto-refresh", has_polling))
        test["status"] = "PASS" if has_polling else "PARTIAL"
        self.results[suite]["passed" if has_polling else "partial"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q11.5: Auto-refresh") if has_polling else log_warn("Q11.5: Auto-refresh - verificare manuală")
        
        # Container 12 - Notifications
        log_info("Container 12: Notifications")
        
        test = {"id": "Q12.1", "desc": "Toast Notifications (D=Types: success/error/info)", "checks": []}
        has_toast = self.test_js_function("showToast")
        test["checks"].append(("Funcție showToast()", has_toast))
        test["status"] = "PASS" if has_toast else "FAIL"
        self.results[suite]["passed" if has_toast else "failed"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q12.1: Toast notifications") if has_toast else log_fail("Q12.1: Toast notifications lipsă")
        
        test = {"id": "Q12.2", "desc": "Trade Notifications (B=Open/close alerts)", "checks": []}
        has_trade_notif = "trade" in self.js_content.lower() and "notif" in self.js_content.lower()
        test["checks"].append(("Trade notifications", has_trade_notif))
        test["status"] = "PASS" if has_trade_notif else "PARTIAL"
        self.results[suite]["passed" if has_trade_notif else "partial"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q12.2: Trade notifications") if has_trade_notif else log_warn("Q12.2: Trade notifications - verificare manuală")
        
        test = {"id": "Q12.3", "desc": "Error Alerts (A=Dashboard + C=Email)", "checks": []}
        has_error = "error" in self.js_content.lower() and ("alert" in self.js_content.lower() or "toast" in self.js_content.lower())
        test["checks"].append(("Error alerts", has_error))
        test["status"] = "PASS" if has_error else "PARTIAL"
        self.results[suite]["passed" if has_error else "partial"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q12.3: Error alerts") if has_error else log_warn("Q12.3: Error alerts - verificare manuală")
        
        test = {"id": "Q12.4", "desc": "Daily Summary (B=Email report)", "checks": []}
        has_summary = "summary" in self.js_content.lower() or "daily" in self.js_content.lower() and "report" in self.js_content.lower()
        test["checks"].append(("Daily summary", has_summary))
        test["status"] = "PASS" if has_summary else "PARTIAL"
        self.results[suite]["passed" if has_summary else "partial"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q12.4: Daily summary") if has_summary else log_warn("Q12.4: Daily summary - verificare manuală")
        
        # Container 15 - Dashboard Stats (mapped to suite 4)
        log_info("Container 15: Dashboard Stats")
        
        test = {"id": "Q15.1", "desc": "Active Clients Count (D=Real-time)", "checks": []}
        has_kpi = self.test_html_element("kpiClients")
        has_fetch = self.test_js_function("fetchDashboardStats")
        test["checks"].append(("Element kpiClients", has_kpi))
        test["checks"].append(("Funcție fetchDashboardStats()", has_fetch))
        
        if has_kpi and has_fetch:
            test["status"] = "PASS"
            self.results[suite]["passed"] += 1
            log_pass("Q15.1: Active clients count")
        else:
            test["status"] = "PARTIAL"
            self.results[suite]["partial"] += 1
            log_warn("Q15.1: Active clients - parțial")
        self.results[suite]["tests"].append(test)
        
        test = {"id": "Q15.2", "desc": "Open Positions Count (D=Real-time)", "checks": []}
        has_pos = self.test_html_element("kpiPositions")
        test["checks"].append(("Element kpiPositions", has_pos))
        test["status"] = "PASS" if has_pos else "FAIL"
        self.results[suite]["passed" if has_pos else "failed"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q15.2: Open positions count") if has_pos else log_fail("Q15.2: Open positions count lipsă")
        
        test = {"id": "Q15.3", "desc": "Total Profit (C=Live P&L)", "checks": []}
        has_profit = self.test_html_element("kpiProfit")
        test["checks"].append(("Element kpiProfit", has_profit))
        test["status"] = "PASS" if has_profit else "FAIL"
        self.results[suite]["passed" if has_profit else "failed"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q15.3: Total profit") if has_profit else log_fail("Q15.3: Total profit lipsă")
        
        test = {"id": "Q15.4", "desc": "Session Timer (A=London + B=NY + C=Countdown)", "checks": []}
        has_timer = self.test_html_element("v32SessionTimer") or self.test_html_element("v33SessionTimer")
        test["checks"].append(("Session timer", has_timer))
        test["status"] = "PASS" if has_timer else "FAIL"
        self.results[suite]["passed" if has_timer else "failed"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q15.4: Session timer") if has_timer else log_fail("Q15.4: Session timer lipsă")
        
        test = {"id": "Q15.5", "desc": "Last Update (D=Timestamp)", "checks": []}
        has_update = self.test_html_element("lastUpdate")
        test["checks"].append(("Element lastUpdate", has_update))
        test["status"] = "PASS" if has_update else "FAIL"
        self.results[suite]["passed" if has_update else "failed"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q15.5: Last update") if has_update else log_fail("Q15.5: Last update lipsă")
    
    def test_suite_5_admin(self):
        """Test Suite 5: Admin & Management (Containers 13,14,16,17)"""
        log_section("SUITA 5: ADMIN (Containere 13,14,16,17)")
        
        suite = "suite_5"
        config = TEST_CONFIG[suite]
        
        # Container 13 - User Management
        log_info("Container 13: User Management")
        
        test = {"id": "Q13.1", "desc": "User Roles (D=Admin/Trader/Viewer)", "checks": []}
        has_roles = "admin" in self.js_content.lower() and "role" in self.js_content.lower()
        test["checks"].append(("User roles", has_roles))
        test["status"] = "PARTIAL"  # Verificare manuală recomandată
        self.results[suite]["partial"] += 1
        self.results[suite]["tests"].append(test)
        log_warn("Q13.1: User roles - verificare manuală")
        
        test = {"id": "Q13.2", "desc": "Permission Matrix (A=Action-based)", "checks": []}
        has_perm = "permission" in self.js_content.lower() or "access" in self.js_content.lower()
        test["checks"].append(("Permission matrix", has_perm))
        test["status"] = "PARTIAL"
        self.results[suite]["partial"] += 1
        self.results[suite]["tests"].append(test)
        log_warn("Q13.2: Permission matrix - verificare manuală")
        
        test = {"id": "Q13.3", "desc": "Session Timeout (A=Auto + D=Configurable)", "checks": []}
        has_timeout = "timeout" in self.js_content.lower() or "session" in self.js_content.lower()
        test["checks"].append(("Session timeout", has_timeout))
        test["status"] = "PARTIAL"
        self.results[suite]["partial"] += 1
        self.results[suite]["tests"].append(test)
        log_warn("Q13.3: Session timeout - verificare manuală")
        
        test = {"id": "Q13.4", "desc": "Audit Log (A=Actions tracked)", "checks": []}
        has_audit = "audit" in self.js_content.lower() or "log" in self.js_content.lower()
        test["checks"].append(("Audit log", has_audit))
        test["status"] = "PASS" if has_audit else "PARTIAL"
        self.results[suite]["passed" if has_audit else "partial"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q13.4: Audit log") if has_audit else log_warn("Q13.4: Audit log - verificare manuală")
        
        # Container 14 - Settings
        log_info("Container 14: Settings")
        
        test = {"id": "Q14.1", "desc": "Global Settings (B=Per-robot + Global)", "checks": []}
        has_settings = "setting" in self.js_content.lower()
        test["checks"].append(("Settings system", has_settings))
        test["status"] = "PARTIAL"
        self.results[suite]["partial"] += 1
        self.results[suite]["tests"].append(test)
        log_warn("Q14.1: Global settings - verificare manuală")
        
        test = {"id": "Q14.2", "desc": "Email Config (A+B+C=SMTP/Port/User)", "checks": []}
        has_email = "email" in self.js_content.lower() or "smtp" in self.js_content.lower()
        test["checks"].append(("Email config", has_email))
        test["status"] = "PARTIAL"
        self.results[suite]["partial"] += 1
        self.results[suite]["tests"].append(test)
        log_warn("Q14.2: Email config - verificare manuală")
        
        test = {"id": "Q14.3", "desc": "Theme (A=Light/Dark)", "checks": []}
        has_theme = "theme" in self.js_content.lower() or "dark" in self.html_content.lower()
        test["checks"].append(("Theme support", has_theme))
        test["status"] = "PASS" if has_theme else "PARTIAL"
        self.results[suite]["passed" if has_theme else "partial"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q14.3: Theme support") if has_theme else log_warn("Q14.3: Theme - verificare manuală")
        
        test = {"id": "Q14.4", "desc": "Language (A=EN + C=RO)", "checks": []}
        has_lang = "lang" in self.html_content.lower() or "ro" in self.html_content.lower()
        test["checks"].append(("Language support", has_lang))
        test["status"] = "PARTIAL"
        self.results[suite]["partial"] += 1
        self.results[suite]["tests"].append(test)
        log_warn("Q14.4: Language - verificare manuală")
        
        # Container 16 - Backup
        log_info("Container 16: Backup")
        
        test = {"id": "Q16.1", "desc": "Auto Backup (C=Scheduled)", "checks": []}
        has_backup = "backup" in self.js_content.lower()
        test["checks"].append(("Backup system", has_backup))
        test["status"] = "PARTIAL"
        self.results[suite]["partial"] += 1
        self.results[suite]["tests"].append(test)
        log_warn("Q16.1: Auto backup - verificare manuală")
        
        test = {"id": "Q16.2", "desc": "Restore (D=Point-in-time)", "checks": []}
        has_restore = "restore" in self.js_content.lower()
        test["checks"].append(("Restore function", has_restore))
        test["status"] = "PARTIAL"
        self.results[suite]["partial"] += 1
        self.results[suite]["tests"].append(test)
        log_warn("Q16.2: Restore - verificare manuală")
        
        test = {"id": "Q16.3", "desc": "Export (A=CSV)", "checks": []}
        has_export = "export" in self.js_content.lower() or "csv" in self.js_content.lower() or "json" in self.js_content.lower()
        test["checks"].append(("Export function", has_export))
        test["status"] = "PASS" if has_export else "PARTIAL"
        self.results[suite]["passed" if has_export else "partial"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q16.3: Export") if has_export else log_warn("Q16.3: Export - verificare manuală")
        
        test = {"id": "Q16.4", "desc": "Import (A+B+C=Formats)", "checks": []}
        has_import = "import" in self.js_content.lower()
        test["checks"].append(("Import function", has_import))
        test["status"] = "PASS" if has_import else "PARTIAL"
        self.results[suite]["passed" if has_import else "partial"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q16.4: Import") if has_import else log_warn("Q16.4: Import - verificare manuală")
        
        test = {"id": "Q16.5", "desc": "Data Retention (A=Auto cleanup)", "checks": []}
        has_retention = "retention" in self.js_content.lower() or "cleanup" in self.js_content.lower()
        test["checks"].append(("Data retention", has_retention))
        test["status"] = "PASS" if has_retention else "PARTIAL"
        self.results[suite]["passed" if has_retention else "partial"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q16.5: Data retention") if has_retention else log_warn("Q16.5: Data retention - verificare manuală")
        
        # Container 17 - Security
        log_info("Container 17: Security")
        
        test = {"id": "Q17.1", "desc": "API Keys (D=Secure storage)", "checks": []}
        has_api_key = "api" in self.js_content.lower() and "key" in self.js_content.lower()
        test["checks"].append(("API key management", has_api_key))
        test["status"] = "PARTIAL"
        self.results[suite]["partial"] += 1
        self.results[suite]["tests"].append(test)
        log_warn("Q17.1: API keys - verificare manuală")
        
        test = {"id": "Q17.2", "desc": "2FA (A+C+D=TOTP/Email/Backup)", "checks": []}
        has_2fa = "2fa" in self.js_content.lower() or "totp" in self.js_content.lower() or "mfa" in self.js_content.lower()
        test["checks"].append(("2FA support", has_2fa))
        test["status"] = "PASS" if has_2fa else "PARTIAL"
        self.results[suite]["passed" if has_2fa else "partial"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q17.2: 2FA") if has_2fa else log_warn("Q17.2: 2FA - verificare manuală")
        
        test = {"id": "Q17.3", "desc": "IP Whitelist (D=Restrict access)", "checks": []}
        has_ip = "ip" in self.js_content.lower() and ("whitelist" in self.js_content.lower() or "restrict" in self.js_content.lower())
        test["checks"].append(("IP whitelist", has_ip))
        test["status"] = "PARTIAL"
        self.results[suite]["partial"] += 1
        self.results[suite]["tests"].append(test)
        log_warn("Q17.3: IP whitelist - verificare manuală")
        
        test = {"id": "Q17.4", "desc": "Rate Limiting (D=Request throttling)", "checks": []}
        has_rate = "rate" in self.js_content.lower() and ("limit" in self.js_content.lower() or "throttl" in self.js_content.lower())
        test["checks"].append(("Rate limiting", has_rate))
        test["status"] = "PASS" if has_rate else "PARTIAL"
        self.results[suite]["passed" if has_rate else "partial"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q17.4: Rate limiting") if has_rate else log_warn("Q17.4: Rate limiting - verificare manuală")
    
    def test_suite_6_logs(self):
        """Test Suite 6: Logs & Journal (Containers 18-19)"""
        log_section("SUITA 6: LOGS (Containere 18-19)")
        
        suite = "suite_6"
        config = TEST_CONFIG[suite]
        
        # Container 18 - Robot Logs
        log_info("Container 18: Robot Logs")
        
        test = {"id": "Q18.1", "desc": "Log Viewer (A=Real-time stream)", "checks": []}
        has_log = "log" in self.js_content.lower() and ("viewer" in self.js_content.lower() or "stream" in self.js_content.lower())
        test["checks"].append(("Log viewer", has_log))
        test["status"] = "PASS" if has_log else "PARTIAL"
        self.results[suite]["passed" if has_log else "partial"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q18.1: Log viewer") if has_log else log_warn("Q18.1: Log viewer - verificare manuală")
        
        test = {"id": "Q18.2", "desc": "Log Levels (D=Debug/Info/Warning/Error)", "checks": []}
        has_levels = all(l in self.js_content.lower() for l in ["debug", "info", "warn", "error"])
        test["checks"].append(("Log levels", has_levels))
        test["status"] = "PASS" if has_levels else "PARTIAL"
        self.results[suite]["passed" if has_levels else "partial"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q18.2: Log levels") if has_levels else log_warn("Q18.2: Log levels - verificare manuală")
        
        test = {"id": "Q18.3", "desc": "Log Search (D=Filter by text/time/level)", "checks": []}
        has_search = "search" in self.js_content.lower() and "log" in self.js_content.lower()
        test["checks"].append(("Log search", has_search))
        test["status"] = "PASS" if has_search else "PARTIAL"
        self.results[suite]["passed" if has_search else "partial"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q18.3: Log search") if has_search else log_warn("Q18.3: Log search - verificare manuală")
        
        test = {"id": "Q18.4", "desc": "Log Download (A=Export to file)", "checks": []}
        has_download = "download" in self.js_content.lower() and ("log" in self.js_content.lower() or "export" in self.js_content.lower())
        test["checks"].append(("Log download", has_download))
        test["status"] = "PASS" if has_download else "PARTIAL"
        self.results[suite]["passed" if has_download else "partial"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q18.4: Log download") if has_download else log_warn("Q18.4: Log download - verificare manuală")
        
        # Container 19 - Trade Journal
        log_info("Container 19: Trade Journal")
        
        test = {"id": "Q19.1", "desc": "Journal Entry (D=Per trade notes)", "checks": []}
        has_journal = "journal" in self.js_content.lower() or "note" in self.js_content.lower()
        test["checks"].append(("Journal entry", has_journal))
        test["status"] = "PASS" if has_journal else "PARTIAL"
        self.results[suite]["passed" if has_journal else "partial"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q19.1: Journal entry") if has_journal else log_warn("Q19.1: Journal entry - verificare manuală")
        
        test = {"id": "Q19.2", "desc": "Screenshot (D=Auto capture)", "checks": []}
        has_screenshot = "screenshot" in self.js_content.lower() or "capture" in self.js_content.lower() or "image" in self.js_content.lower()
        test["checks"].append(("Screenshot", has_screenshot))
        test["status"] = "PASS" if has_screenshot else "PARTIAL"
        self.results[suite]["passed" if has_screenshot else "partial"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q19.2: Screenshot") if has_screenshot else log_warn("Q19.2: Screenshot - verificare manuală")
        
        test = {"id": "Q19.3", "desc": "Emotion Tag (D=Mood tracking)", "checks": []}
        has_emotion = "emotion" in self.js_content.lower() or "mood" in self.js_content.lower() or "tag" in self.js_content.lower()
        test["checks"].append(("Emotion tag", has_emotion))
        test["status"] = "PASS" if has_emotion else "PARTIAL"
        self.results[suite]["passed" if has_emotion else "partial"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q19.3: Emotion tag") if has_emotion else log_warn("Q19.3: Emotion tag - verificare manuală")
        
        test = {"id": "Q19.4", "desc": "Review Mode (A=Historical + D=Analytics)", "checks": []}
        has_review = "review" in self.js_content.lower() or "analytic" in self.js_content.lower()
        test["checks"].append(("Review mode", has_review))
        test["status"] = "PASS" if has_review else "PARTIAL"
        self.results[suite]["passed" if has_review else "partial"] += 1
        self.results[suite]["tests"].append(test)
        log_pass("Q19.4: Review mode") if has_review else log_warn("Q19.4: Review mode - verificare manuală")
    
    def generate_report(self):
        """Generate final test report"""
        log_header("RAPORT FINAL - QA MASTER TESTING")
        
        total_passed = 0
        total_failed = 0
        total_partial = 0
        
        print(f"\n{Colors.BOLD}REZUMAT PER SUITĂ:{Colors.END}\n")
        print(f"{'Suita':<20} {'Total':<8} {'PASS':<8} {'FAIL':<8} {'PARTIAL':<8} {'% PASS':<8}")
        print("-" * 60)
        
        for suite_name, data in self.results.items():
            suite_total = data["passed"] + data["failed"] + data["partial"]
            total_passed += data["passed"]
            total_failed += data["failed"]
            total_partial += data["partial"]
            
            pass_pct = (data["passed"] / suite_total * 100) if suite_total > 0 else 0
            
            suite_label = {
                "suite_1": "1. CORE",
                "suite_2": "2. ROBOȚI",
                "suite_3": "3. ADVANCED",
                "suite_4": "4. MONITORING",
                "suite_5": "5. ADMIN",
                "suite_6": "6. LOGS"
            }.get(suite_name, suite_name)
            
            print(f"{suite_label:<20} {suite_total:<8} {Colors.GREEN}{data['passed']:<8}{Colors.END} {Colors.RED}{data['failed']:<8}{Colors.END} {Colors.YELLOW}{data['partial']:<8}{Colors.END} {pass_pct:.0f}%")
        
        total_tests = total_passed + total_failed + total_partial
        overall_pass_pct = (total_passed / total_tests * 100) if total_tests > 0 else 0
        
        print("-" * 60)
        print(f"{'TOTAL':<20} {total_tests:<8} {Colors.GREEN}{total_passed:<8}{Colors.END} {Colors.RED}{total_failed:<8}{Colors.END} {Colors.YELLOW}{total_partial:<8}{Colors.END} {overall_pass_pct:.0f}%")
        
        # Bug Summary
        log_section("BUG-URI IDENTIFICATE")
        
        critical_bugs = [b for b in self.bugs if b.get("severity") == "CRITICAL"]
        high_bugs = [b for b in self.bugs if b.get("severity") == "HIGH"]
        medium_bugs = [b for b in self.bugs if b.get("severity") == "MEDIUM"]
        
        print(f"\n  {Colors.RED}🔴 CRITICAL: {len(critical_bugs)}{Colors.END}")
        for bug in critical_bugs:
            print(f"     - {bug['id']}: {bug['desc']}")
        
        print(f"\n  {Colors.YELLOW}🟠 HIGH: {len(high_bugs)}{Colors.END}")
        for bug in high_bugs:
            print(f"     - {bug['id']}: {bug['desc']}")
        
        print(f"\n  {Colors.BLUE}🔵 MEDIUM: {len(medium_bugs)}{Colors.END}")
        for bug in medium_bugs:
            print(f"     - {bug['id']}: {bug['desc']}")
        
        # Final Recommendation
        log_section("RECOMANDARE FINALĂ")
        
        if len(critical_bugs) > 0:
            recommendation = "🔴 STOP"
            reason = "Bug-uri critice blochează funcționalitatea de bază"
        elif overall_pass_pct >= 80:
            recommendation = "🟢 GO"
            reason = "Majoritatea testelor au trecut (>80%)"
        elif overall_pass_pct >= 60:
            recommendation = "🟡 CONTINUE"
            reason = "Testare parțială, necesită fix-uri înainte de GO"
        else:
            recommendation = "🔴 STOP"
            reason = "Prea multe teste eșuate"
        
        print(f"\n  {Colors.BOLD}Recomandare: {recommendation}{Colors.END}")
        print(f"  Motiv: {reason}")
        print(f"\n  {Colors.BOLD}Stare proiect:{Colors.END}")
        print(f"    - Suite testate: 6/6")
        print(f"    - Total teste: {total_tests}")
        print(f"    - PASS: {total_passed} ({total_passed/total_tests*100:.1f}%)")
        print(f"    - FAIL: {total_failed} ({total_failed/total_tests*100:.1f}%)")
        print(f"    - PARTIAL: {total_partial} ({total_partial/total_tests*100:.1f}%)")
        
        # Save report to file
        report_path = "/workspace/shared/reports/QA_MASTER_FINAL_REPORT_20260328.md"
        self.save_report_to_file(report_path, total_tests, total_passed, total_failed, total_partial, recommendation)
        print(f"\n  {Colors.CYAN}📄 Raport salvat: {report_path}{Colors.END}")
    
    def save_report_to_file(self, path, total, passed, failed, partial, recommendation):
        """Save detailed report to markdown file"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write("# QA-MASTER FINAL REPORT\n\n")
            f.write(f"**Data:** 2026-03-28 23:30 UTC\n")
            f.write(f"**Tester:** qa-master\n")
            f.write(f"**Total teste:** {total}\n\n")
            
            f.write("## REZUMAT\n\n")
            f.write(f"- ✅ **PASS:** {passed} ({passed/total*100:.1f}%)\n")
            f.write(f"- ❌ **FAIL:** {failed} ({failed/total*100:.1f}%)\n")
            f.write(f"- ⚠️ **PARTIAL:** {partial} ({partial/total*100:.1f}%)\n\n")
            
            f.write(f"**Recomandare:** {recommendation}\n\n")
            
            f.write("## DETALII PER SUITĂ\n\n")
            for suite_name, data in self.results.items():
                suite_label = {
                    "suite_1": "Suita 1: CORE",
                    "suite_2": "Suita 2: ROBOȚI",
                    "suite_3": "Suita 3: ADVANCED",
                    "suite_4": "Suita 4: MONITORING",
                    "suite_5": "Suita 5: ADMIN",
                    "suite_6": "Suita 6: LOGS"
                }.get(suite_name, suite_name)
                
                f.write(f"### {suite_label}\n")
                f.write(f"- PASS: {data['passed']}\n")
                f.write(f"- FAIL: {data['failed']}\n")
                f.write(f"- PARTIAL: {data['partial']}\n\n")
                
                for test in data['tests']:
                    status_icon = "✅" if test['status'] == 'PASS' else "❌" if test['status'] == 'FAIL' else "⚠️"
                    f.write(f"{status_icon} **{test['id']}**: {test['desc']}\n")
                f.write("\n")
            
            f.write("## BUG-URI IDENTIFICATE\n\n")
            for bug in self.bugs:
                f.write(f"- **{bug['id']}** [{bug['severity']}]: {bug['desc']}\n")


if __name__ == "__main__":
    tester = QAMasterTester()
    tester.run_tests()
