# Quick Start Guide

Get AI Travel Planner running in **5 minutes** ⚡

## 🚀 Super Quick Start (No Endee)

```bash
# 1. Clone repository
git clone https://github.com/yourusername/ai-travel-planner.git
cd ai-travel-planner

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r Backend/requirements.txt

# 4. Copy environment
cp .env.example .env

# 5. Start backend
cd Backend
python3 main.py

# Backend running at http://localhost:8000
```

In another terminal:

```bash
# Start frontend (from project root)
cd frontend
python3 -m http.server 3000
```

Open **http://localhost:3000** 🎉

## 🐳 Docker Quick Start (Recommended)

```bash
# 1. Clone repository
git clone https://github.com/yourusername/ai-travel-planner.git
cd ai-travel-planner

# 2. Start all services
docker-compose up

# That's it! All three services start:
# - Endee on :19530
# - Backend on :8000
# - Frontend on :3000
```

Open **http://localhost:3000** 🎉

## ⚙️ Configuration

### Add Groq API Key (Optional but Recommended)

```bash
# 1. Get free API key from https://console.groq.com/
# 2. Edit .env
echo "GROQ_API_KEY=gsk_YOUR_KEY_HERE" >> .env

# 3. Restart backend for changes to take effect
```

### Configure Endee

```bash
# .env settings
ENDEE_HOST=http://localhost:19530
ENDEE_USE_FALLBACK=true
```

## 🧪 Test the System

### Check Health

```bash
# Backend health
curl http://localhost:8000/

# Database status
curl http://localhost:8000/status

# Endee health
curl http://localhost:19530/health
```

### Make a Query

```bash
curl -X POST http://localhost:8000/plan \
  -H "Content-Type: application/json" \
  -d '{"query": "3 day trip to Manali with 15000 budget"}'
```

Expected response:
```json
{
  "response": {
    "itinerary": "Day 1: Arrive in Manali...",
    "hotels": "Budget hotels in Manali...",
    "food": "Manali specialties...",
    "routes": "Delhi to Manali highway...",
    "budget": "₹15000 covers everything...",
    "recommendations": "Visit Solang Valley..."
  }
}
```

## 🛠️ Development

### Backend Development

```bash
# Backend with auto-reload
cd Backend
uvicorn main:app --reload --port 8000
```

### Frontend Development

```bash
# Frontend with live server
cd frontend
python3 -m http.server 3000
```

### Using Python Directly

```bash
cd Backend
python3 -c "from rag_pipeline import run_rag; print(run_rag('trip to goa'))"
```

## 📁 Project Layout

```
ai-travel-planner/
├── Backend/           # API server
│   ├── main.py       # FastAPI app
│   ├── config.py     # Settings
│   └── agents/       # RAG agents
├── frontend/         # Web UI
│   └── index.html    # Single page app
└── README.md         # Documentation
```

## 🔍 Common Queries to Try

```
"Plan a 3 day trip to Manali with ₹15000 budget"
"Best hotels in Goa?"
"What's special about Jaipur?"
"Budget trip to Shimla"
"Adventure activities in Manali"
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Port already in use | Change port: `python3 -m http.server 3001` |
| Module not found | Install: `pip install -r requirements.txt` |
| Endee not found | Start Docker or disable: set `ENDEE_USE_FALLBACK=true` |
| No API responses | Get key from https://console.groq.com or use demo mode |

## 📚 Full Documentation

- **[README.md](README.md)** - Complete guide
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design
- **[ENDEE_INTEGRATION.md](ENDEE_INTEGRATION.md)** - Database details
- **[GITHUB_SETUP.md](GITHUB_SETUP.md)** - GitHub hosting

## 🎓 Next Steps

1. ✅ Get it running locally
2. 📖 Read ARCHITECTURE.md
3. 🧪 Experiment with queries
4. 🔧 Explore the code
5. 🚀 Deploy to cloud
6. 📤 Share on GitHub

## 📖 API Quick Reference

```
GET  /              → Health check
POST /plan          → Generate plan
GET  /status        → System status
GET  /docs          → API documentation
```

## 🚀 Deploy to Cloud

```bash
# Create .env with secrets
echo "GROQ_API_KEY=your_key" > .env

# Push to GitHub
git push origin main

# Deploy to Render / Railway / DigitalOcean
# (Follow their setup for docker-compose)
```

## 💬 Need Help?

- 📖 Check [README.md](README.md)
- 🔍 Review [Troubleshooting](ARCHITECTURE.md#troubleshooting)
- 📝 See [GitHub Issues](https://github.com/yourusername/ai-travel-planner/issues)
- 💬 Create [Discussion](https://github.com/yourusername/ai-travel-planner/discussions)

## 🎉 Success!

You now have:
- ✅ Running backend API
- ✅ Web UI for queries
- ✅ Semantic search with Endee
- ✅ AI-powered recommendations

Now explore and build! 🚀

---

**Questions?** Check out the full [README.md](README.md)!
