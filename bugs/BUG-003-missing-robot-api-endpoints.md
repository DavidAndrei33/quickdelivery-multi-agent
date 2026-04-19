# BUG-003: Missing Robot API Endpoints

## Informații Generale
| Atribut | Valoare |
|---------|---------|
| **ID** | BUG-003 |
| **Severitate** | CRITICAL |
| **Status** | OPEN |
| **Data descoperirii** | 2026-03-28 |
| **Raportat de** | QA-Master Agent |

## Descriere
Toate endpoint-urile API pentru controlul roboților (Start/Stop) nu sunt implementate pe server. Orice încercare de a apela aceste endpoint-uri returnează 404 Not Found.

## Endpoint-uri Lipsă

### V31 Marius TPL
| Metodă | Endpoint | Descriere |
|--------|----------|-----------|
| POST | `/api/robot/v31_tpl/start` | Pornește robotul V31 |
| POST | `/api/robot/v31_tpl/stop` | Oprește robotul V31 |

### V32 London Breakout
| Metodă | Endpoint | Descriere |
|--------|----------|-----------|
| POST | `/api/robot/v32_london/start` | Pornește robotul V32 |
| POST | `/api/robot/v32_london/stop` | Oprește robotul V32 |

### V33 NY Breakout
| Metodă | Endpoint | Descriere |
|--------|----------|-----------|
| POST | `/api/robot/v33_ny/start` | Pornește robotul V33 |
| POST | `/api/robot/v33_ny/stop` | Oprește robotul V33 |

## Test Verificare
```bash
# Toate aceste comenzi returnează 404
curl -X POST http://localhost:3000/api/robot/v31_tpl/start
curl -X POST http://localhost:3000/api/robot/v31_tpl/stop
curl -X POST http://localhost:3000/api/robot/v32_london/start
curl -X POST http://localhost:3000/api/robot/v32_london/stop
curl -X POST http://localhost:3000/api/robot/v33_ny/start
curl -X POST http://localhost:3000/api/robot/v33_ny/stop
```

## Impact
- CRITICAL: Nu se pot porni/opri roboții din dashboard
- CRITICAL: Funcționalitatea principală este inutilizabilă
- BUG-002 depinde de rezolvarea acestui bug

## Soluție Propusă

### Implementare Node.js/Express:
```javascript
// În serverul Node.js (app.js sau routes.js)

const express = require('express');
const router = express.Router();

// Robot control endpoints
const robots = ['v31_tpl', 'v32_london', 'v33_ny'];

robots.forEach(robot => {
    // Start endpoint
    router.post(`/api/robot/${robot}/start`, async (req, res) => {
        try {
            // TODO: Implementează logica de pornire
            // - Validează autentificarea
            // - Pornește procesul robotului
            // - Actualizează status în database
            
            console.log(`[API] Starting robot: ${robot}`);
            
            // Placeholder - înlocuiește cu logica reală
            await startRobotProcess(robot);
            
            res.json({
                status: 'success',
                message: `Robot ${robot} started successfully`,
                timestamp: new Date().toISOString()
            });
        } catch (error) {
            console.error(`[API] Failed to start ${robot}:`, error);
            res.status(500).json({
                status: 'error',
                message: error.message
            });
        }
    });
    
    // Stop endpoint
    router.post(`/api/robot/${robot}/stop`, async (req, res) => {
        try {
            console.log(`[API] Stopping robot: ${robot}`);
            
            // Placeholder - înlocuiește cu logica reală
            await stopRobotProcess(robot);
            
            res.json({
                status: 'success',
                message: `Robot ${robot} stopped successfully`,
                timestamp: new Date().toISOString()
            });
        } catch (error) {
            console.error(`[API] Failed to stop ${robot}:`, error);
            res.status(500).json({
                status: 'error',
                message: error.message
            });
        }
    });
});

// Helper functions (placeholders)
async function startRobotProcess(robot) {
    // TODO: Implementează pornirea reală a robotului
    // Ex: spawn child process, docker container, etc.
}

async function stopRobotProcess(robot) {
    // TODO: Implementează oprirea reală a robotului
}

module.exports = router;
```

## Schema Răspuns

### Success (200 OK)
```json
{
    "status": "success",
    "message": "Robot v31_tpl started successfully",
    "timestamp": "2026-03-28T17:08:00.000Z"
}
```

### Error (500 Internal Server Error)
```json
{
    "status": "error",
    "message": "Failed to start robot: process already running"
}
```

## Autentificare
Toate endpoint-urile trebuie să necesite autentificare JWT:
```javascript
// Middleware de autentificare
const authenticateToken = (req, res, next) => {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];
    
    if (!token) {
        return res.status(401).json({ status: 'error', message: 'Access token required' });
    }
    
    jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
        if (err) {
            return res.status(403).json({ status: 'error', message: 'Invalid token' });
        }
        req.user = user;
        next();
    });
};

// Aplică middleware-ul
router.post('/api/robot/:robot/start', authenticateToken, async (req, res) => { ... });
```

## Referințe
- Test Cases: TC-103, TC-106, TC-109, TC-112, TC-115, TC-118
- Fișier raport: TEST-CASES-COMPLETE-REPORT.md
- Dependință pentru: BUG-002
