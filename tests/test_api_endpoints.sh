#!/bin/bash
# Test script pentru API endpoints Dashboard

echo "========================================"
echo "🧪 TESTARE API ENDPOINTS DASHBOARD"
echo "========================================"
echo ""

API_URL="http://localhost:8001"

# Funcție pentru testare endpoint
test_endpoint() {
    local method=$1
    local endpoint=$2
    local description=$3
    
    echo -n "Testing $method $endpoint ... "
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL$endpoint" 2>/dev/null)
    else
        response=$(curl -s -o /dev/null -w "%{http_code}" -X "$method" "$API_URL$endpoint" 2>/dev/null)
    fi
    
    if [ "$response" = "200" ]; then
        echo "✅ OK (200)"
    elif [ "$response" = "404" ]; then
        echo "❌ NOT FOUND (404) - $description"
    elif [ "$response" = "500" ]; then
        echo "🔥 ERROR (500) - $description"
    else
        echo "⚠️  Status: $response"
    fi
}

echo "=== ENDPOINTS HEALTH ==="
test_endpoint "GET" "/api/health" "Health check"

echo ""
echo "=== ENDPOINTS CLIENȚI ==="
test_endpoint "GET" "/api/clients" "Lista clienți"
test_endpoint "GET" "/api/positions" "Poziții deschise"
test_endpoint "GET" "/api/history" "Istoric tranzacții"

echo ""
echo "=== ENDPOINTS STATISTICI ==="
test_endpoint "GET" "/api/stats" "Statistici generale"
test_endpoint "GET" "/api/equity" "Equity curve"
test_endpoint "GET" "/api/symbols" "Simboluri"
test_endpoint "GET" "/api/daily-profit" "Profit zilnic"

echo ""
echo "=== ENDPOINTS ROBOȚI ==="
test_endpoint "GET" "/api/robots" "Lista roboți"
test_endpoint "POST" "/api/robot/v31_tpl/start" "Start V31"
test_endpoint "POST" "/api/robot/v31_tpl/stop" "Stop V31"
test_endpoint "GET" "/api/robot/status?robot=v31_tpl" "Status V31"

echo ""
echo "=== ENDPOINTS SERVICII ==="
test_endpoint "GET" "/api/services" "Lista servicii"
test_endpoint "GET" "/api/services/status" "Status servicii"

echo ""
echo "=== ENDPOINTS LOGS ==="
test_endpoint "GET" "/api/expert_logs" "Loguri expert"
test_endpoint "GET" "/api/journal" "Jurnal trading"
test_endpoint "GET" "/api/command_log" "Log comenzi"
test_endpoint "GET" "/api/robot_logs?robot=v31_tpl" "Loguri robot V31"

echo ""
echo "=== ENDPOINTS V31 (Marius TPL) ==="
test_endpoint "GET" "/api/v31/live_status" "V31 live status"
test_endpoint "GET" "/api/v31/symbol_status" "V31 symbol status"
test_endpoint "GET" "/api/v31_incomplete_setups" "V31 setups incomplete"

echo ""
echo "=== ENDPOINTS V32 (London) ==="
test_endpoint "GET" "/api/v32/or_data" "V32 OR data"
test_endpoint "GET" "/api/v32/asia_data" "V32 Asia data"
test_endpoint "GET" "/api/v32/breakout_status" "V32 breakout status"
test_endpoint "GET" "/api/v32/trade_stats" "V32 trade stats"

echo ""
echo "=== ENDPOINTS V33 (NY) ==="
test_endpoint "GET" "/api/v33/or_data" "V33 OR data"
test_endpoint "GET" "/api/v33/breakout_status" "V33 breakout status"
test_endpoint "GET" "/api/v33/trade_stats" "V33 trade stats"

echo ""
echo "=== ENDPOINTS EXISTENTE (din server) ==="
test_endpoint "GET" "/api/setups" "Lista setups"
test_endpoint "GET" "/api/queue" "Lista queue"

echo ""
echo "========================================"
echo "Testare completă!"
echo "========================================"
