# 🎯 COMPLETE GUIDE - HOW TO RUN AI TRAVEL PLANNER

## 📌 Before You Start

```
✓ Python 3.12 installed
✓ Virtual environment (venv) exists
✓ All packages installed
✓ .env file has GROQ_API_KEY
✓ Project path: /Users/om/Desktop/New_AI_Travel
```

---

## 🚀 OPTION A: Super Fast (Recommended)

**Copy & paste in 2 terminals:**

### Terminal 1 (Backend)
```bash
cd /Users/om/Desktop/New_AI_Travel/Backend && source ../venv/bin/activate && python3 main.py
```

### Terminal 2 (Frontend)
```bash
cd /Users/om/Desktop/New_AI_Travel/frontend && python3 -m http.server 3000
```

### Browser
```
http://localhost:3000
```

**Done!** ✅

---

## 📋 OPTION B: Step by Step

### Step 1: Prepare Environment (First Time Only)

```bash
# Navigate to project
cd /Users/om/Desktop/New_AI_Travel

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in terminal - if yes, continue
```

### Step 2: Verify Groq API Works

```bash
# From project root
python3 test_groq.py
```

**Expected Output:**
```
✓ GROQ_API_KEY found: True
API Key (first 20 chars): gsk_JxR...
📡 Initializing Groq client...
✓ Groq client initialized successfully
🧪 Testing Groq API with llama-3.1-8b-instant...
✅ Groq API is WORKING!
   Response: Travel consultant ready...
```

**If fails:**
- Check `.env` has valid GROQ_API_KEY
- Get new key: https://console.groq.com/
- Update `.env` file

### Step 3: Start Backend

**Open Terminal 1:**
```bash
cd /Users/om/Desktop/New_AI_Travel/Backend
source ../venv/bin/activate
python3 main.py
```

**Wait for:**
```
✓ Travel data loaded successfully: 56 entries
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Keep this terminal OPEN** ⬅️ Don't close!

### Step 4: Start Frontend

**Open Terminal 2 (NEW terminal):**
```bash
cd /Users/om/Desktop/New_AI_Travel/frontend
python3 -m http.server 3000
```

**Wait for:**
```
Serving HTTP on 0.0.0.0 port 3000 (http://0.0.0.0:3000/)
```

**Keep this terminal OPEN** ⬅️ Don't close!

### Step 5: Open Browser

```bash
# Option 1: Direct URL
open http://localhost:3000

# Option 2: Manual
# Type in address bar: http://localhost:3000
```

### Step 6: Use the App

1. Type travel query in text box
   - Examples:
     - "3 day trip to Manali with 15000 budget"
     - "best hotels in Goa"
     - "food recommendations in Delhi"
     - "Jaipur 2 day itinerary"

2. Click "Send" button ➔

3. Wait 2-3 seconds for AI response

4. See detailed travel plan

---

## 🔌 OPTION C: Using Docker (If Installed)

```bash
cd /Users/om/Desktop/New_AI_Travel

# Start all services
docker-compose up

# Access
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# Endee: http://localhost:19530
```

---

## 🧪 Testing Without Web UI

### Test Backend Health
```bash
curl http://localhost:8000
```

### Get System Status
```bash
curl http://localhost:8000/status
```

### Generate Travel Plan
```bash
curl -X POST http://localhost:8000/plan \
  -H "Content-Type: application/json" \
  -d '{"query": "3 day Goa trip with 20000 budget"}'
```

### View Interactive API Docs
```bash
open http://localhost:8000/docs
```

---

## 🛠️ Troubleshooting during Startup

### Problem: "Port 8000 already in use"
```bash
# Find what's using it
lsof -i :8000

# Kill it
kill -9 <PID>

# Or use cleanup command
lsof -i :8000 | grep -v COMMAND | awk '{print $2}' | xargs kill -9
```

### Problem: "ModuleNotFoundError: No module named 'groq'"
```bash
# Install packages
source venv/bin/activate
pip install -r Backend/requirements.txt

# Restart backend
```

### Problem: "GROQ_API_KEY not found in .env"
```bash
# Check .env file
cat /Users/om/Desktop/New_AI_Travel/.env

# Should show:
# GROQ_API_KEY=gsk_...

# If empty, get key from:
# https://console.groq.com/
```

### Problem: "Could not parse expanded_dataset"
```bash
# This means the dataset file has syntax errors
# Solution: Backend should handle this automatically
# If still failing, restart backend:

pkill -f "python3 main.py"
sleep 2
cd /Users/om/Desktop/New_AI_Travel/Backend
python3 main.py
```

### Problem: "Frontend shows blank page"
```bash
# Make sure backend is running
curl http://localhost:8000/

# Should show API response, not connection error

# If connection error:
# - Go back to Terminal 1
# - Start backend again: python3 main.py
```

### Problem: "API returns error, not response"
```bash
# Check backend logs in Terminal 1
# Should show:
# - Processing query
# - Calling Groq API
# - Response received

# If you see errors:
# 1. Check Groq API key with: python3 test_groq.py
# 2. Make sure internet is connected
# 3. Check Groq API status: https://console.groq.com/
```

---

## 📊 What's Running Where

```
Terminal 1:
├── Backend API
├── Port: 8000
├── URL: http://localhost:8000
├── Models: Sentence-Transformers + Groq LLM
└── Status: Running... (keep open)

Terminal 2:
├── Frontend Web Server
├── Port: 3000
├── URL: http://localhost:3000
├── Tech: HTML5 + CSS3 + JavaScript
└── Status: Running... (keep open)

Browser:
├── Open: http://localhost:3000
├── Type queries
└── See AI responses in 2-3 seconds
```

---

## ✅ Checklist - It's Working When:

- [ ] Terminal 1 shows: "Uvicorn running on http://0.0.0.0:8000"
- [ ] Terminal 2 shows: "Serving HTTP on 0.0.0.0 port 3000"
- [ ] Browser opens to http://localhost:3000
- [ ] Can see "AI Travel Planner" heading
- [ ] Can type in text box
- [ ] Can click "Send" button
- [ ] Get response after 2-3 seconds
- [ ] Response has travel plan details

**All checked?** 🎉 **You're ready!**

---

## 🎯 First Query to Try

```
Type this in web UI: "3 day Manali trip with 15000 budget"

Expected response (should include):
✓ Detailed itinerary for each day
✓ Hotel names and prices
✓ Local food recommendations
✓ Transportation routes
✓ Budget breakdown
✓ Travel tips
```

---

## 🛑 Stopping Everything

### Stop Backend
```bash
# In Terminal 1, press:
Ctrl + C

# Or from another terminal:
pkill -f "python3 main.py"
```

### Stop Frontend
```bash
# In Terminal 2, press:
Ctrl + C

# Or from another terminal:
pkill -f "http.server"
```

### Clean Up Ports (if needed)
```bash
lsof -i :8000 | grep -v COMMAND | awk '{print $2}' | xargs kill -9
lsof -i :3000 | grep -v COMMAND | awk '{print $2}' | xargs kill -9
```

---

## 📚 Documentation Files in Project

- **HOW_TO_RUN.md** ← You are here
- **QUICK_COMMANDS.md** - Common commands reference
- **README.md** - Project overview
- **ARCHITECTURE.md** - System design
- **SYSTEM_FIXES_REPORT.md** - What was fixed
- **ENDEE_INTEGRATION.md** - Vector database info

---

## 🚀 Running Again Later

```bash
# Just remember these 3 steps:

# 1. Terminal 1
cd /Users/om/Desktop/New_AI_Travel/Backend && source ../venv/bin/activate && python3 main.py

# 2. Terminal 2
cd /Users/om/Desktop/New_AI_Travel/frontend && python3 -m http.server 3000

# 3. Browser
http://localhost:3000
```

---

## 💡 Tips

- **Keep both terminals open** while using the app
- **Close terminals** with Ctrl+C (safe graceful shutdown)
- **Refresh browser** if UI seems stuck
- **Check API logs** in Terminal 1 for debugging
- **Test Groq** with `python3 test_groq.py` anytime
- **No Groq key?** System still works with demo responses

---

## ✨ You're All Set! 

**Ready to plan amazing trips!** ✈️🌍🏖️

Questions? Check other documentation files or test with QUICK_COMMANDS.md
