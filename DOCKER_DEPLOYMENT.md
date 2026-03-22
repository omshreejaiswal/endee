# 🐳 DOCKER DEPLOYMENT GUIDE

## ⚡ Quick Start (1 command)

```bash
cd /Users/om/Desktop/New_AI_Travel
docker-compose up
```

**Done!** Services running at:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Endee: http://localhost:19530

---

## 📋 Prerequisites

### Install Docker & Docker Compose

**On macOS (using Homebrew):**
```bash
# Install Docker Desktop (includes both Docker and Docker Compose)
brew install --cask docker

# Or download from: https://www.docker.com/products/docker-desktop
```

**Verify Installation:**
```bash
docker --version
docker-compose --version
```

**Expected Output:**
```
Docker version 24.0.0+
Docker Compose version 2.20.0+
```

---

## 🚀 Full Deployment Steps

### Step 1: Prepare Your System

```bash
# Check Docker is running
docker ps

# Should return (even if no containers):
# CONTAINER ID   IMAGE   COMMAND   CREATED
```

### Step 2: Set Up Environment Variables

```bash
cd /Users/om/Desktop/New_AI_Travel

# Create .env if not exists (it should already be there)
cat .env

# Should show:
# GROQ_API_KEY=gsk_JxR17gEhuTDFdBcB...
# ENDEE_HOST=http://localhost:19530
# ENDEE_USE_FALLBACK=true
```

### Step 3: Build and Start Containers

```bash
cd /Users/om/Desktop/New_AI_Travel

# Build images and start services
docker-compose up

# Or run in background:
docker-compose up -d
```

**First time will take 3-5 minutes** (downloading images, building)

**You should see:**
```
✓ Building backend
✓ Pulling frontend image  
✓ Building endee
✓ Creating network
✓ Starting services
✓ Endee server ready
✓ Backend running on 0.0.0.0:8000
✓ Frontend serving on 0.0.0.0:3000
```

### Step 4: Verify All Services Running

```bash
# Check container status
docker-compose ps

# Should show all 3 running:
# NAME                      STATUS
# endee-server             Up
# travel-planner-backend   Up
# travel-planner-frontend  Up
```

### Step 5: Test Services

```bash
# Test Backend
curl http://localhost:8000/

# Test Frontend
curl http://localhost:3000 | head -20

# Test API (generate travel plan)
curl -X POST http://localhost:8000/plan \
  -H "Content-Type: application/json" \
  -d '{"query": "3 day Manali trip"}'
```

### Step 6: Open in Browser

```bash
open http://localhost:3000
```

---

## 📊 Architecture

```
Docker Network: travel-planner-net

┌─────────────────────────────────────────────────────┐
│                   Docker Network                     │
│                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────┐ │
│  │   Frontend   │  │   Backend    │  │   Endee   │ │
│  │   (port 3000)│  │  (port 8000) │  │(port 19530)│ │
│  │              │  │              │  │           │ │
│  │  Node.js     │  │  Python 3.12 │  │  Rust     │ │
│  │  HTML5 UI    │  │  FastAPI     │  │  Vector   │ │
│  │              │  │  Groq AI     │  │  Database │ │
│  └──────────────┘  └──────────────┘  └───────────┘ │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## 🛑 Stopping Services

### Option 1: Stop and Remove Containers (Keep Images)
```bash
docker-compose down
```

### Option 2: Stop but Keep Running (Faster restart)
```bash
docker-compose stop
docker-compose start  # To restart
```

### Option 3: Full Cleanup (Remove everything)
```bash
docker-compose down -v  # -v removes volumes (data)
```

---

## 🔧 Common Docker Commands

### View Logs

```bash
# All services
docker-compose logs

# Specific service
docker-compose logs backend
docker-compose logs frontend
docker-compose logs endee

# Real-time logs
docker-compose logs -f backend

# Last 100 lines
docker-compose logs backend --tail=100
```

### Enter Container Shell

```bash
# Backend shell
docker-compose exec backend bash

# Once inside, you can run Python commands:
python3 -c "print('Hello')"
exit  # To exit
```

### Restart Services

```bash
# Restart one service
docker-compose restart backend

# Restart all
docker-compose restart

# Rebuild and restart
docker-compose up --build
```

### Remove Images

```bash
# Remove unused images
docker image prune

# Remove specific image
docker rmi travel-planner-backend
```

---

## 🐛 Troubleshooting

### Issue 1: "Cannot connect to Docker daemon"

```bash
# Docker not running. Start it:
# macOS: Click Docker icon in Applications
# Or from terminal:
open /Applications/Docker.app

# Wait 30 seconds for Docker Desktop to start
sleep 30

# Try again:
docker ps
```

### Issue 2: "Port 8000/3000 already in use"

```bash
# Find what's using the port
lsof -i :8000
lsof -i :3000

# Kill the process
kill -9 <PID>

# Or use docker to stop it:
docker-compose down
```

### Issue 3: "Endee service failing"

```bash
# Check Endee logs
docker-compose logs endee

# Rebuild Endee (takes time)
docker-compose up --build endee
```

### Issue 4: "Backend can't connect to Endee"

```bash
# This is normal - backend uses in-memory fallback
# Check backend logs for confirmation:
docker-compose logs backend | grep -i "fallback\|endee"

# Should see: "Using in-memory storage (Endee unavailable)"
```

### Issue 5: "Groq API not working"

```bash
# Inside container, test API:
docker-compose exec backend python3 test_groq.py

# If error, check .env has valid GROQ_API_KEY:
cat .env | grep GROQ_API_KEY

# If empty, update .env and restart:
docker-compose restart backend
```

### Issue 6: "Memory issues / Out of memory"

```bash
# Clean up Docker
docker system prune -a

# Or increase Docker memory in Docker Desktop settings:
# Docker Desktop → Preferences → Resources → Memory (set higher)
```

---

## 📈 Docker Compose File Structure

```yaml
version: '3.8'
services:
  # Service 1: Endee Vector Database
  endee:
    build: ./Backend/endee
    ports:
      - "19530:19530"
    volumes:
      - endee_data:/data
    healthcheck: ✓
  
  # Service 2: FastAPI Backend
  backend:
    build: ./Backend
    ports:
      - "8000:8000"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
    depends_on:
      - endee
  
  # Service 3: Frontend
  frontend:
    image: node:18-alpine
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app

volumes:
  endee_data:
    # Persists Endee data between container restarts
```

---

## 🚀 Advanced: Production Deployment

### For AWS EC2:

```bash
# 1. SSH into EC2 instance
ssh ec2-user@your-instance-ip

# 2. Install Docker
sudo yum update -y
sudo yum install docker -y
sudo usermod -a -G docker ec2-user
newgrp docker

# 3. Clone project
git clone https://github.com/yourusername/travel-planner.git
cd travel-planner

# 4. Set environment
echo "GROQ_API_KEY=your-key" > .env

# 5. Start services
docker-compose up -d

# 6. Access
# Navigate to: http://your-instance-ip:3000
```

### For Heroku:

```bash
# 1. Install Heroku CLI
brew tap heroku/brew && brew install heroku

# 2. Login
heroku login

# 3. Create app
heroku create your-app-name

# 4. Set env var
heroku config:set GROQ_API_KEY=your-key

# 5. Deploy
git push heroku main
```

### For Digital Ocean:

```bash
# 1. SSH into droplet
ssh root@your-droplet-ip

# 2. Install Docker
curl -sSL https://get.docker.com | sh
usermod -a -G docker root

# 3. Deploy (same as AWS)
git clone your-repo
cd travel-planner
docker-compose up -d
```

---

## 🔐 Security Best Practices

### 1. Never commit `.env` to git

```bash
# Keep .env in .gitignore
echo ".env" >> .gitignore
git rm --cached .env
```

### 2. Use environment variables for secrets

```bash
# Set via Docker
export GROQ_API_KEY="your-key"
docker-compose up

# Or in .env (never commit!)
GROQ_API_KEY=your-key
```

### 3. Run containers as non-root

```bash
# Already configured in Dockerfile:
USER appuser  # Runs as non-root user
```

### 4. Use healthchecks

```bash
# Already configured in docker-compose.yml:
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/"]
  interval: 30s
  timeout: 10s
```

---

## 📊 Monitoring

### View Resource Usage

```bash
# Real-time stats
docker stats

# Output shows: CPU %, Memory usage, Network I/O
```

### Check Container Health

```bash
docker-compose ps

# HEALTH column shows if healthchecks passing
```

### View Event Logs

```bash
docker events --filter type=container
```

---

## 🔄 CI/CD Integration

### GitHub Actions Example

```yaml
name: Deploy to production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build images
        run: docker-compose build
      
      - name: Push to registry
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USER }} --password-stdin
          docker-compose push
      
      - name: Deploy
        run: docker-compose up -d
```

---

## 📱 Quick Reference

| Task | Command |
|------|---------|
| Start | `docker-compose up` |
| Stop | `docker-compose down` |
| View logs | `docker-compose logs -f` |
| Restart | `docker-compose restart` |
| Status | `docker-compose ps` |
| Shell | `docker-compose exec backend bash` |
| Rebuild | `docker-compose up --build` |
| Remove all | `docker-compose down -v` |

---

## ✅ Deployment Checklist

- [ ] Docker and Docker Compose installed
- [ ] `.env` file has `GROQ_API_KEY`
- [ ] `docker-compose.yml` exists
- [ ] `Backend/Dockerfile` exists
- [ ] Run `docker-compose up`
- [ ] All 3 services show as "Up"
- [ ] Frontend loads at http://localhost:3000
- [ ] Backend responds at http://localhost:8000
- [ ] Can generate travel plans successfully
- [ ] Logs show no errors

**All checked?** ✅ **Your app is deployed with Docker!**

---

## 🎯 Next Steps

1. **Local Testing**: Run `docker-compose up` locally
2. **Package for Prod**: Push images to Docker Hub
3. **Deploy to Cloud**: Use AWS, Heroku, or DigitalOcean
4. **Monitor**: Use Docker stats and logs
5. **Scale**: Use Kubernetes for advanced scaling

---

## 📚 Further Reading

- Docker Docs: https://docs.docker.com/
- Docker Compose: https://docs.docker.com/compose/
- AWS ECS: https://docs.aws.amazon.com/ecs/

**Ready to deploy?** Start with `docker-compose up` 🚀
