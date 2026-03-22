# 🐳 DOCKER QUICK REFERENCE

## ⚡ Most Important Commands

```bash
# Start everything
docker-compose up

# Start in background
docker-compose up -d

# View status
docker-compose ps

# View logs
docker-compose logs -f

# Stop everything
docker-compose down

# Rebuild and restart
docker-compose up --build
```

---

## 📍 Service URLs (When Running)

```
Frontend:   http://localhost:3000
Backend:    http://localhost:8000
Endee:      http://localhost:19530
API Docs:   http://localhost:8000/docs
```

---

## 🔍 Viewing Logs

```bash
# All services
docker-compose logs

# Specific service
docker-compose logs backend
docker-compose logs frontend
docker-compose logs endee

# Real-time (follow)
docker-compose logs -f

# Last 50 lines
docker-compose logs --tail=50

# Grep for errors
docker-compose logs backend 2>&1 | grep -i error
```

---

## 🔧 Container Management

```bash
# Status of all containers
docker-compose ps

# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart backend

# Stop services (keep containers)
docker-compose stop

# Start stopped services
docker-compose start

# Remove containers (keep images)
docker-compose down

# Remove everything including data
docker-compose down -v

# Rebuild images
docker-compose build

# Rebuild without cache
docker-compose build --no-cache
```

---

## 📁 Accessing Container Shell

```bash
# Bash shell in backend
docker-compose exec backend bash

# Python shell in backend
docker-compose exec backend python3

# Test Groq API
docker-compose exec backend python3 test_groq.py

# View logs from inside
docker-compose exec backend tail -f /app/app.log

# Exit from container
exit
```

---

## 🧪 Testing Services

```bash
# Test backend health
curl http://localhost:8000/

# Test Groq API through backend
curl -X POST http://localhost:8000/plan \
  -H "Content-Type: application/json" \
  -d '{"query": "test"}'

# Test frontend
curl http://localhost:3000 | head -20

# Check Docker container logs
docker logs travel-planner-backend
```

---

## 🐛 Troubleshooting Commands

```bash
# Check Docker status
docker ps -a

# View container details
docker inspect travel-planner-backend

# Check network
docker network ls
docker network inspect travel-planner-net

# View resource usage
docker stats

# List images
docker images

# Remove unused images
docker image prune

# Check disk usage
docker system df

# Full cleanup
docker system prune -a
```

---

## 🔌 Port & Network

```bash
# See what's listening on port 8000
lsof -i :8000

# Kill process using port
kill -9 <PID>

# Docker network commands
docker network ls
docker network inspect travel-planner-net

# Check service connectivity
docker-compose exec backend ping endee
```

---

## 📊 Common Scenarios

### Scenario 1: Backend crashed, restart it
```bash
docker-compose restart backend
docker-compose logs backend
```

### Scenario 2: Update code and redeploy
```bash
# Pull latest code
git pull

# Rebuild images
docker-compose build

# Restart services
docker-compose up -d
```

### Scenario 3: Full reset everything
```bash
docker-compose down -v  # Remove all
docker-compose up --build  # Fresh start
```

### Scenario 4: Check if Groq API works
```bash
docker-compose exec backend python3 test_groq.py
```

### Scenario 5: View backend output in real-time
```bash
docker-compose logs -f backend
```

### Scenario 6: Save container data
```bash
# Data in endee_data volume persists
# To backup:
docker run --rm -v travel-planner_endee_data:/data -v $(pwd):/backup alpine tar czf /backup/endee_backup.tar.gz -C / data

# To restore:
docker run --rm -v travel-planner_endee_data:/data -v $(pwd):/backup alpine tar xzf /backup/endee_backup.tar.gz -C /
```

---

## 🚀 Production Commands

```bash
# Deploy to production
docker-compose -f docker-compose.yml up -d

# Monitor in production
docker-compose logs -f backend

# Auto-restart on failure
# (Already configured in docker-compose.yml)

# Scale backend service (if separated)
docker-compose up -d --scale backend=3

# Update without downtime
docker-compose up -d backend  # Restarts only backend
```

---

## 🔐 Security

```bash
# View environment variables
docker-compose config

# Never expose secrets in logs
# Check .env is in .gitignore:
cat .gitignore | grep .env

# Use secrets in production
# (Configure in docker-compose.yml or use swarm secrets)
```

---

## 📦 Working with Images

```bash
# Build specific image
docker-compose build backend

# Push to Docker Hub
docker tag travel-planner-backend:latest username/travel-planner-backend:latest
docker push username/travel-planner-backend:latest

# Pull from Docker Hub
docker pull username/travel-planner-backend:latest

# View image details
docker image inspect travel-planner-backend
```

---

## 🌐 Docker Desktop GUI

**Alternative to command line:**

1. Open Docker Desktop app
2. Go to "Containers" tab
3. See all running containers
4. Click on container to see logs
5. Click "CLI" to open terminal in container
6. Use GUI to manage containers

---

## 📱 Quick Command Reference Card

| What | Command |
|------|---------|
| Start in background | `docker-compose up -d` |
| Stop all | `docker-compose down` |
| Show status | `docker-compose ps` |
| Watch logs | `docker-compose logs -f` |
| Restart one | `docker-compose restart backend` |
| Shell access | `docker-compose exec backend bash` |
| Clean rebuild | `docker-compose down -v && docker-compose up --build` |
| Check health | `docker-compose ps` (status column) |

---

## ✅ Health Check

Everything working? You should see:

```
docker-compose ps

NAME                      STATUS              
endee-server              Up (healthy)        
travel-planner-backend    Up (healthy)        
travel-planner-frontend   Up                  
```

If any show "unhealthy", check logs:
```bash
docker-compose logs <service-name>
```

---

**Most used command:** `docker-compose up -d && docker-compose logs -f` 🚀
