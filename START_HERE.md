# ⚡ FASTEST START - Copy & Paste Commands

## 🏃 3-Minute Startup

### Copy This Into Terminal 1:
```bash
cd /Users/om/Desktop/New_AI_Travel/Backend && source ../venv/bin/activate && python3 main.py
```

### Copy This Into Terminal 2:
```bash
cd /Users/om/Desktop/New_AI_Travel/frontend && python3 -m http.server 3000
```

### Then Open Browser:
```
http://localhost:3000
```

**That's it!** Type your travel query. ✅

---

## 📋 What You'll See

```
Terminal 1 (Backend):
✓ Travel data loaded successfully: 56 entries
✓ Application startup complete
✓ Uvicorn running on http://0.0.0.0:8000

Terminal 2 (Frontend):
✓ Serving HTTP on 0.0.0.0 port 3000

Browser:
✓ AI Travel Planner heading
✓ Text input box
✓ Send button
✓ Ready to accept queries!
```

---

## 🎯 Try These Queries

```
• "3 day trip to Manali with 15000 budget"
• "Best hotels in Goa"
• "Jaipur 2 day itinerary"
• "Food recommendations in Delhi"
• "Shimla weekend trip"
• "Where to visit in Udaipur"
```

---

## 🛑 Stopping

```bash
# Terminal 1: Press Ctrl+C
# Terminal 2: Press Ctrl+C
```

---

## 🆘 If It Doesn't Work

### Check Backend Health:
```bash
curl http://localhost:8000
# Should see JSON response with "status":"operational"
```

### Check Groq API:
```bash
python3 test_groq.py
# Should show: ✅ Groq API is WORKING!
```

### Clear Ports (if in use):
```bash
lsof -i :8000 | grep -v COMMAND | awk '{print $2}' | xargs kill -9
lsof -i :3000 | grep -v COMMAND | awk '{print $2}' | xargs kill -9
```

### Reinstall Packages:
```bash
cd /Users/om/Desktop/New_AI_Travel
source venv/bin/activate
pip install -r Backend/requirements.txt
```

---

## 📍 Important Files & Paths

| Item | Path | Purpose |
|------|------|---------|
| **Project** | `/Users/om/Desktop/New_AI_Travel` | Main folder |
| **Backend** | `Backend/main.py` | FastAPI server |
| **Frontend** | `frontend/index.html` | Web UI |
| **Config** | `.env` | API key (GROQ_API_KEY) |
| **Dataset** | `Backend/expanded_dataset.py` | 56 travel records |
| **Docs** | `HOW_TO_RUN.md` | Full guide |

---

## 🌐 URLs When Running

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | Web UI (use this!) |
| Backend | http://localhost:8000 | API server |
| API Docs | http://localhost:8000/docs | Interactive documentation |

---

## ✅ Quick Verification

```bash
# All 3 should return without errors:

# 1. Frontend running?
curl http://localhost:3000 | head -c 50

# 2. Backend running?
curl http://localhost:8000 | grep -o '"status":"[^"]*"'

# 3. Can generate plan?
curl -X POST http://localhost:8000/plan \
  -H "Content-Type: application/json" \
  -d '{"query": "test"}' | grep -o '"response"'
```

**Expected:** All 3 return data without errors ✅

---

## 🎓 Project Structure (Quick)

```
Backend/
├── main.py                 👈 FastAPI server
├── expanded_dataset.py     👈 Travel database (56 entries)
├── config.py              👈 Configuration
└── agents/
    ├── generator_agent.py  👈 Groq AI (llama-3.1-8b-instant)
    └── other agents...

frontend/
└── index.html             👈 Web UI

.env                        👈 GROQ_API_KEY config

RUN_PROJECT.md             👈 Full instructions (this file)
```

---

## 🚀 Next Steps After Starting

1. **Visit** http://localhost:3000
2. **Type** "Plan a trip to Manali"
3. **Click** Send button
4. **Wait** 2-3 seconds
5. **See** AI-generated travel plan!

Done! 🎉

---

## 🔧 If Backend Won't Start

```bash
# Check Python environment
source venv/bin/activate
python3 --version  # Should be 3.12+

# Check packages installed
pip list | grep groq
pip list | grep fastapi

# If missing, install
pip install -r Backend/requirements.txt

# Try again
cd Backend && python3 main.py
```

---

## 📞 Quick Help

| Problem | Solution |
|---------|----------|
| Port 8000 in use | Run: `lsof -i :8000 \| awk '{print $2}' \| xargs kill -9` |
| ModuleNotFoundError | Run: `pip install -r Backend/requirements.txt` |
| Groq API not working | Run: `python3 test_groq.py` |
| Blank web page | Check Terminal 1 - backend must be running |
| Slow response | Normal - Groq API takes 2-3 seconds |

---

**Ready? Start with copying the 2 Terminal commands at the top!** 🚀
