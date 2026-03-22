# Endee Database Setup Options

This document shows how to set up Endee for the AI Travel Planner.

## ⚡ Quick Start: No Endee (In-Memory Mode)

If you don't need Endee, just run:

```bash
# Docker Compose (easiest)
docker-compose up -d

# Or local Python
source venv/bin/activate
python3 Backend/main.py
```

**Status**: Everything works with in-memory fallback ✅

---

## 🔧 Option 1: Endee with Docker (Recommended)

### Using Official Endee Image (When Available)

Edit `docker-compose.yml` and enable Endee:

```yaml
services:
  endee:
    image: endee-io/endee:latest
    container_name: endee-server
    ports:
      - "19530:19530"
    environment:
      - LOG_LEVEL=INFO
    volumes:
      - endee_data:/data
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:19530/health"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - travel-planner-net
```

Then start:

```bash
docker-compose up -d
```

---

## 🏗️ Option 2: Build Endee from Source (Advanced)

### Prerequisites

Install build tools:

```bash
# macOS
brew install cmake clang

# Ubuntu/Debian
sudo apt install cmake build-essential

# Windows
# Install Visual Studio Build Tools
```

### Build and Run

```bash
# Clone and build Endee (if not already done)
cd Backend/endee
mkdir -p build
cd build
cmake ..
make -j$(nproc)
./endee --port 19530

# Endee is now running on http://localhost:19530
```

### Use with Backend

In another terminal:

```bash
source venv/bin/activate
cd Backend
export ENDEE_HOST=http://localhost:19530
python3 main.py
```

---

## 📦 Option 3: Endee in Separate Docker Container

### Run Endee Docker Container Directly

```bash
# Pull official Endee image (when available)
docker pull endee-io/endee:latest

# Run Endee
docker run -d \
  --name endee-server \
  -p 19530:19530 \
  -v endee_data:/data \
  endee-io/endee:latest

# Verify health
curl http://localhost:19530/health
```

### Use with Backend (Local Python)

```bash
source venv/bin/activate
cd Backend
export ENDEE_HOST=http://localhost:19530
python3 main.py
```

---

## ✅ Verify Endee Setup

### Check Status

```bash
# Direct Endee health check
curl http://localhost:19530/health

# Via Backend endpoint
curl http://localhost:8000/status | python3 -m json.tool | grep -A10 endee_health

# Expected: "using_endee": true
```

### Run Full Test

```bash
python3 test_endee_integration.py
```

---

## 🔄 Switch Between Modes

### Enable Endee

```bash
# In .env
ENDEE_USE_FALLBACK=true

# Backend will auto-connect when Endee starts
```

### Disable Endee (In-Memory Only)

```bash
# In .env
ENDEE_USE_FALLBACK=false

# Or just don't start Endee service
```

---

## 🐛 Troubleshooting

### Endee Won't Start

```bash
# Check Docker logs
docker logs endee-server

# Check if port 19530 is in use
lsof -i :19530

# Kill existing process if needed
kill -9 $(lsof -t -i:19530)
```

### Endee Connection Refused

```bash
# Verify Endee is running
docker ps | grep endee

# Test connectivity
curl -v http://localhost:19530/health

# Check backend logs
docker logs travel-planner-backend | grep Endee
```

### Endee Works but Search is Slow

```bash
# Restart both services
docker-compose restart backend endee

# Or rebuild with optimization flags (advanced)
```

---

## 📊 Performance Comparison

| Mode | Speed | Memory | Use Case |
|------|-------|--------|----------|
| **Endee** | Very Fast (Sub-ms) | Configurable | Production, large datasets |
| **In-Memory** | Fast (1-5ms) | ~10MB per 100 docs | Development, small datasets |

**Current Dataset**: 56 travel entries = ~10-15 MB in-memory works efficiently

---

## 🚀 Production Setup

For production deployment:

1. **Use managed Endee service** (when available):
   ```bash
   export ENDEE_HOST=https://endee.company.com:19530
   ```

2. **Or deploy with Docker**:
   ```bash
   docker stack deploy -c docker-compose.yml travel_planner
   ```

3. **Monitor Endee**:
   ```bash
   # Health checks
   curl http://localhost:19530/health
   
   # Via API
   curl http://localhost:8000/status
   ```

---

## 📚 References

- **Endee Docs**: https://github.com/endee-io/endee
- **Docker Setup**: See `DOCKER_DEPLOYMENT.md`
- **API Docs**: http://localhost:8000/docs
- **Verification**: See `ENDEE_VERIFICATION.md`

---

## ✨ Summary

- ✅ **Works without Endee** - In-memory fallback is reliable
- ✅ **Easy to add Endee** - Just start the container
- ✅ **Auto-reconnect** - Backend detects when Endee comes online
- ✅ **Zero downtime** - Graceful degradation if Endee fails

**Recommendation**: Start with in-memory mode, add Endee when you scale to millions of documents.
