# 🚀 HOW TO RUN AI TRAVEL PLANNER

## ⚡ Quick Start (5 minutes)

### Option 1: Simple Direct Run (Recommended for Beginners)

```bash
# 1. Navigate to project folder
cd /Users/om/Desktop/New_AI_Travel

# 2. Activate Python environment
source venv/bin/activate

# 3. Start Backend (in one terminal)
cd Backend
python3 main.py

# 4. Start Frontend (in another terminal)
cd frontend
python3 -m http.server 3000

# 5. Open browser
open http://localhost:3000
```

**That's it!** Your app is running! ✅

---

## 📋 Prerequisites Check

```bash
# Verify Python environment
source venv/bin/activate
python3 --version          # Should be 3.12+

# Verify key packages installed
pip list | grep -E "fastapi|uvicorn|groq|sentence-transformers"
```

**Expected output**: All packages should be listed ✅

---

## 🔑 Environment Configuration

### 1. Check `.env` File Exists
```bash
cat /Users/om/Desktop/New_AI_Travel/.env
```

Should show:
```
GROQ_API_KEY=gsk_JxR17gEhuTDFdBcB...
ENDEE_HOST=http://localhost:19530
ENDEE_USE_FALLBACK=true
DEBUG=false
LOG_LEVEL=INFO
```

### 2. Get Your Own Groq API Key (Optional but Recommended)
```bash
# 1. Visit: https://console.groq.com/
# 2. Sign up for free
# 3. Create API key
# 4. Update .env file:
export GROQ_API_KEY="your-new-key-here"

# Or edit .env directly:
nano .env
# Change: GROQ_API_KEY=your-key-here
```

---

## 🎯 Complete Setup from Scratch

### Step 1: Install Dependencies
```bash
cd /Users/om/Desktop/New_AI_Travel

# Create virtual environment (if needed)
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install all packages
pip install -r Backend/requirements.txt
```

### Step 2: Verify Groq API
```bash
cd /Users/om/Desktop/New_AI_Travel
python3 test_groq.py
```

**Expected output**:
```
✓ GROQ_API_KEY found: True
📡 Initializing Groq client...
✓ Groq client initialized successfully
🧪 Testing Groq API with llama-3.1-8b-instant...
✅ Groq API is WORKING!
   Response: Travel consultant ready...
```

### Step 3: Start Backend Service
```bash
cd /Users/om/Desktop/New_AI_Travel/Backend
source ../venv/bin/activate
python3 main.py
```

**You should see**:
```
✓ Travel data loaded successfully: 56 entries
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Keep this terminal open!**

### Step 4: Start Frontend (New Terminal)
```bash
cd /Users/om/Desktop/New_AI_Travel/frontend
python3 -m http.server 3000
```

**You should see**:
```
Serving HTTP on 0.0.0.0 port 3000
```

**Keep this terminal open!**

### Step 5: Open in Browser
```bash
# Option 1: Manual
open http://localhost:3000

# Option 2: From terminal
curl http://localhost:3000 | head -20
```

---

## 📱 Using the Application

### Via Web UI (Easiest)
1. Open [http://localhost:3000](http://localhost:3000)
2. Enter your travel query in the text box
3. Examples:
   - "Plan a 3 day trip to Manali with 15000 budget"
   - "Best hotels in Goa"
   - "Food recommendations in Jaipur"
4. Click "Send" button
5. Wait for AI-powered response (2-3 seconds)

### Via API (Advanced)
```bash
# Test health check
curl http://localhost:8000

# Get system status
curl http://localhost:8000/status

# Generate travel plan
curl -X POST http://localhost:8000/plan \
  -H "Content-Type: application/json" \
  -d '{"query": "3 day trip to Goa with 20000 budget"}'

# View API documentation
open http://localhost:8000/docs
```

---

## 🐳 Optional: Run with Docker

```bash
# Start both services
docker-compose up

# Services will start:
# - Backend on http://localhost:8000
# - Frontend on http://localhost:3000
# - Endee on http://localhost:19530 (optional)
```

---

## 🛑 Stopping the Application

### Terminal Method
```bash
# Kill backend
pkill -f "python3 main.py"

# Kill frontend
pkill -f "http.server"
```

### Or press Ctrl+C in each terminal

---

## 🔍 Troubleshooting

### Issue 1: "Port 8000 already in use"
```bash
# Find what's using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or clean up:
lsof -i :8000 | grep -v COMMAND | awk '{print $2}' | xargs kill -9
```

### Issue 2: "Groq API error"
```bash
# Test API key
python3 test_groq.py

# If it fails:
# 1. Check .env file has GROQ_API_KEY
# 2. Get new key from https://console.groq.com
# 3. Update .env and restart backend
```

### Issue 3: "ModuleNotFoundError"
```bash
# Activate environment and reinstall
source venv/bin/activate
pip install -r Backend/requirements.txt
```

### Issue 4: "Connection refused"
```bash
# Make sure backend is running on port 8000
curl http://localhost:8000/

# And frontend on port 3000
curl http://localhost:3000
```

### Issue 5: "Module not found: expanded_dataset"
```bash
# Make sure you're in Backend directory
cd /Users/om/Desktop/New_AI_Travel/Backend

# And running from correct location
python3 main.py
```

---

## 📊 Verifying Everything Works

```bash
# 1. Check backend
echo "Backend:" && curl -s http://localhost:8000 | grep -o '"status":"[^"]*"'

# 2. Check frontend
echo "Frontend:" && curl -s http://localhost:3000 | grep -o '<title>[^<]*</title>'

# 3. Test API
echo "API:" && curl -s -X POST http://localhost:8000/plan \
  -H "Content-Type: application/json" \
  -d '{"query": "test"}' | grep -o '"response"'
```

**Expected output**:
```
Backend: "status":"operational"
Frontend: <title>AI Travel Planner</title>
API: "response"
```

---

## 📁 Project Structure

```
New_AI_Travel/
├── Backend/
│   ├── main.py                 # FastAPI server
│   ├── config.py               # Configuration
│   ├── requirements.txt         # Python packages
│   ├── rag_pipeline.py         # RAG orchestration
│   ├── expanded_dataset.py     # 56 travel records
│   ├── agents/
│   │   ├── generator_agent.py  # Groq LLM responses
│   │   ├── retriever_agent.py  # Search/retrieval
│   │   ├── planner_agent.py    # Extract details
│   │   ├── memory_agent.py     # Remember queries
│   │   ├── budget_agent.py     # Optimize cost
│   │   └── vector_db.py        # Database interface
│   └── data/
│       └── travel_data.txt     # Dataset source
├── frontend/
│   └── index.html              # Web UI
├── .env                        # Configuration (API key)
├── venv/                       # Virtual environment
└── README.md                   # Documentation
```

---

## 🎯 What Each Component Does

### Backend (port 8000)
- **FastAPI Server**: Handles API requests
- **RAG Pipeline**: 5-agent orchestration
- **Groq AI**: Generates travel recommendations
- **Vector Database**: Semantic search (in-memory)
- **Load Data**: 56 travel records on startup

### Frontend (port 3000)
- **HTML5 UI**: Beautiful responsive design
- **Chat Interface**: Send queries, see responses
- **Real-time**: Connects to backend API
- **Error Handling**: Shows user-friendly messages

---

## 🚀 Regular Usage Flow

```
1. Terminal 1: Start Backend
   cd Backend && python3 main.py

2. Terminal 2: Start Frontend  
   cd frontend && python3 -m http.server 3000

3. Browser: Open http://localhost:3000

4. Enter Query
   "3 day trip to Manali"

5. AI Responds (2-3 seconds)
   Itinerary, hotels, food, routes, budget

6. See Response in Web UI
   Beautiful formatted travel plan
```

---

## 📊 Response Example

**Query**: "Plan a 3 day trip to Manali with 15000 budget"

**Response**:
```json
{
  "itinerary": "Day 1: Arrive, explore markets. Day 2: Solang Valley activities. Day 3: Hadimba temple, shopping.",
  "hotels": "Budget hotels ₹800-2,500 near town center",
  "food": "Siddu, momos, local trout fish",
  "routes": "Delhi to Manali: 540km, 12-14 hours via Chandigarh",
  "budget": "₹2,000-5,000 per day optimal",
  "recommendations": "Book in advance, hire local guides, try street food"
}
```

---

## ✅ Success Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Browser shows AI Travel Planner UI
- [ ] Can send queries to API
- [ ] Groq AI generates responses (2-3 seconds)
- [ ] Responses show travel details
- [ ] No errors in terminal

**All checked?** 🎉 **You're ready to plan trips!**

---

## 🆘 Need Help?

1. **Check logs**: Look at terminal output for error messages
2. **Test API**: `curl http://localhost:8000/status`
3. **Test Groq**: `python3 test_groq.py`
4. **Check .env**: Verify API key is set
5. **Restart** both services and try again

---

## 📚 Additional Resources

- API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Groq Docs: [https://console.groq.com/docs](https://console.groq.com/docs)
- FastAPI: [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)

---

**Ready to run? Start with Option 1 above! 🚀**
