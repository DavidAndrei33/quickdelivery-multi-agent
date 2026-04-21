# QuickDelivery — Docker Setup

## 🚀 Start Complet

```bash
cd /workspace/shared/.project-brain/projects/quickdelivery
docker-compose up -d
```

## 📁 Structură

```
quickdelivery/
├── docker-compose.yml      # Orchestrare servicii
├── backend/
│   └── Dockerfile          # Node.js API
├── frontend/
│   ├── Dockerfile          # React build + nginx
│   └── nginx.conf          # Config nginx per app
├── nginx/
│   └── nginx.conf          # Reverse proxy principal
└── README.md
```

## 🌐 Servicii

| Serviciu | Port | Container |
|----------|------|-----------|
| API Backend | 3000 | quickdelivery-api |
| Customer | 3001 | quickdelivery-customer |
| Rider | 3002 | quickdelivery-rider |
| Store | 3003 | quickdelivery-store |
| Admin | 3004 | quickdelivery-admin |
| PostgreSQL | 5432 | quickdelivery-db |
| Redis | 6379 | quickdelivery-redis |
| Nginx | 80/443 | quickdelivery-nginx |

## 🔄 Comenzi Utile

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# Logs
docker-compose logs -f api

# Rebuild
docker-compose up -d --build

# Health check
curl http://localhost:3000/health
```

## ⚠️ Note

- Frontend apps necesită `npm run build` înainte de docker build
- Database se persistă în volumul `postgres-data`
- Redis se persistă în volumul `redis-data`
