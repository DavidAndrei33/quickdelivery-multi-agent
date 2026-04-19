# BUG-014: Missing Robot Data Persistence

## Informații Generale
| Atribut | Valoare |
|---------|---------|
| **ID** | BUG-014 |
| **Severitate** | MEDIUM |
| **Status** | OPEN |
| **Data descoperirii** | 2026-03-28 |
| **Raportat de** | QA-Master Agent |

## Descriere
Nu există un mecanism de persistență a datelor robotului între refresh-uri de pagină. La fiecare refresh, toate datele live se pierd și se reia de la zero.

## Probleme
1. Datele live se pierd la refresh
2. Istoricul analizelor nu este disponibil după refresh
3. Utilizatorul trebuie să aștepte din nou popularea datelor

## Soluții Posibile

### Opțiunea 1: localStorage (Client-side)
```javascript
// Salvează datele în localStorage
function saveRobotData(robot, data) {
    const key = `robot_data_${robot}`;
    const storageData = {
        timestamp: Date.now(),
        data: data
    };
    localStorage.setItem(key, JSON.stringify(storageData));
}

// Încarcă datele din localStorage
function loadRobotData(robot) {
    const key = `robot_data_${robot}`;
    const stored = localStorage.getItem(key);
    
    if (stored) {
        const storageData = JSON.parse(stored);
        // Verifică dacă datele nu sunt prea vechi (ex: 5 minute)
        if (Date.now() - storageData.timestamp < 5 * 60 * 1000) {
            return storageData.data;
        }
    }
    return null;
}

// Curăță datele vechi
function clearOldRobotData() {
    const maxAge = 30 * 60 * 1000; // 30 minute
    
    for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key && key.startsWith('robot_data_')) {
            const stored = JSON.parse(localStorage.getItem(key));
            if (Date.now() - stored.timestamp > maxAge) {
                localStorage.removeItem(key);
            }
        }
    }
}
```

### Opțiunea 2: Database (Server-side)
```sql
-- Tabel pentru persistență date robot
CREATE TABLE robot_data_cache (
    id SERIAL PRIMARY KEY,
    robot_id VARCHAR(50) NOT NULL,
    data_type VARCHAR(50) NOT NULL,
    data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(robot_id, data_type)
);

-- Index pentru query rapid
CREATE INDEX idx_robot_data_lookup ON robot_data_cache(robot_id, data_type);
```

```javascript
// Server-side API
router.get('/api/robot/:robot/cached_data', authenticateToken, async (req, res) => {
    try {
        const { robot } = req.params;
        const { type } = req.query;
        
        const result = await db.query(
            'SELECT data, updated_at FROM robot_data_cache WHERE robot_id = $1 AND data_type = $2',
            [robot, type]
        );
        
        if (result.rows.length > 0) {
            res.json({
                status: 'success',
                data: result.rows[0].data,
                cached_at: result.rows[0].updated_at
            });
        } else {
            res.json({ status: 'no_data' });
        }
    } catch (error) {
        res.status(500).json({ status: 'error', message: error.message });
    }
});
```

## Recomandare
Implementează **Opțiunea 1 (localStorage)** pentru MVP și **Opțiunea 2 (Database)** pentru producție.

## Verificare După Fix
1. Dashboard-ul arată date pentru robot
2. Dă refresh la pagină
3. Datele ar trebui să fie încă vizibile (posibil cu indicator "cached")
4. După câteva secunde, datele se actualizează de la API

## Referințe
- Fișier raport: TEST-CASES-COMPLETE-REPORT.md
