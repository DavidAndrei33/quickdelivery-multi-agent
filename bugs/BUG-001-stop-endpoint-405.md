# BUG-REPORT-001: Robot Stop Endpoint Returns 405 Method Not Allowed

**Reporter:** builder-4 (Integration Testing)
**Date:** 2026-03-28T14:33:00Z
**Severity:** MEDIUM
**Status:** Open

## Description
Endpoint-ul `POST /api/robot/{robot_id}/stop` returnează eroarea 405 Method Not Allowed în loc să oprească robotul.

## Steps to Reproduce
```bash
curl -X POST http://localhost:8001/api/robot/v32_london/stop
```

## Expected Result
```json
{"status": "success", "message": "v32_london stopped", "pid": 12345}
```

## Actual Result
```html
<!doctype html>
<html lang=en>
<title>405 Method Not Allowed</title>
<h1>Method Not Allowed</h1>
<p>The method is not allowed for the requested URL.</p>
```

## Workaround
Folosiți endpoint-ul alternativ:
```bash
curl -X POST http://localhost:8001/api/robot/control \
  -H "Content-Type: application/json" \
  -d '{"robot":"v32_london","action":"stop"}'
```

## Root Cause (Suspected)
Posibil conflict de routing în Flask între:
- `@app.route('/api/robot/control', methods=['POST'])`
- `@app.route('/api/robot/<robot_id>/stop', methods=['POST'])`

## Affected Endpoints
- POST /api/robot/{robot_id}/stop (all robot IDs)

## Working Alternatives
- POST /api/robot/{robot_id}/start - WORKING
- POST /api/robot/control - WORKING (with action: "stop")
