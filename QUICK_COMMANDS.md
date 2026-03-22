# ⚡ QUICK START COMMANDS

## 🚀 Run in 3 Commands (Fastest Way)

```bash
# Terminal 1: Backend
cd /Users/om/Desktop/New_AI_Travel/Backend && source ../venv/bin/activate && python3 main.py

# Terminal 2: Frontend 
cd /Users/om/Desktop/New_AI_Travel/frontend && python3 -m http.server 3000

# Browser: Open
open http://localhost:3000
```

---

## 📝 Common Commands

### Activate Environment
```bash
source venv/bin/activate
```

### Start Backend
```bash
cd Backend && python3 main.py
```

### Start Frontend
```bash
cd frontend && python3 -m http.server 3000
```

### Test Groq API
```bash
python3 test_groq.py
```

### Check API Status
```bash
curl http://localhost:8000/status
```

### Test Travel Plan Generation
```bash
curl -X POST http://localhost:8000/plan \
  -H "Content-Type: application/json" \
  -d '{"query": "Manali 3 day trip"}'
```

### View API Documentation
```bash
open http://localhost:8000/docs
```

### Stop Services
```bash
pkill -f "python3 main.py"    # Stop backend
pkill -f "http.server"         # Stop frontend
```

### Clean Port 8000
```bash
lsof -i :8000 | grep -v COMMAND | awk '{print $2}' | xargs kill -9
```

---

## 🔧 If Something Goes Wrong

### Backend won't start?
```bash
# Check error
cd Backend && source ../venv/bin/activate && python3 main.py

# Install missing packages
pip install -r requirements.txt

# Then try again
python3 main.py
```

### Port already in use?
```bash
# Clean ports
lsof -i :8000 | grep -v COMMAND | awk '{print $2}' | xargs kill -9
lsof -i :3000 | grep -v COMMAND | awk '{print $2}' | xargs kill -9
```

### Groq API not working?
```bash
# Test it
python3 test_groq.py

# If fails, check .env has valid GROQ_API_KEY
cat .env
```

### Frontend shows blank?
```bash
# Make sure backend is running
curl http://localhost:8000/

# Then refresh browser
```

---

## 📊 Verify It's Working

```bash
# Health Check
curl http://localhost:8000

# Full Status
curl http://localhost:8000/status

# Test Query
curl -X POST http://localhost:8000/plan \
  -H "Content-Type: application/json" \
  -d '{"query": "Goa beach trip"}'
```

---

## 🎯 Example Queries to Try

```bash
# Simple trip
curl -X POST http://localhost:8000/plan \
  -H "Content-Type: application/json" \
  -d '{"query": "2 day Jaipur trip"}'

# With budget
curl -X POST http://localhost:8000/plan \
  -H "Content-Type: application/json" \
  -d '{"query": "3 day Manali trip with 15000 budget"}'

# Specific interest
curl -X POST http://localhost:8000/plan \
  -H "Content-Type: application/json" \
  -d '{"query": "best hotels in Goa"}'

# Food focused
curl -X POST http://localhost:8000/plan \
  -H "Content-Type: application/json" \
  -d '{"query": "food recommendations in Delhi"}'
```

---

## 📍 Important Paths

```
Project Root:  /Users/om/Desktop/New_AI_Travel
Backend:       /Users/om/Desktop/New_AI_Travel/Backend
Frontend:      /Users/om/Desktop/New_AI_Travel/frontend
Config File:   /Users/om/Desktop/New_AI_Travel/.env
Docs:          /Users/om/Desktop/New_AI_Travel/HOW_TO_RUN.md
```

---

## 🎯 URLs When Running

```
Frontend UI:        http://localhost:3000
Backend API:        http://localhost:8000
API Docs/Swagger:   http://localhost:8000/docs
API Health:         http://localhost:8000/
API Status:         http://localhost:8000/status
Travel Plan API:    http://localhost:8000/plan (POST)
```

---

## ✅ Everything Working? You're Done! 🎉

**Next**: Open http://localhost:3000 and start planning trips! ✈️
