# 🧳 AI Travel Planner - RAG with Endee Vector Database

A production-grade **Retrieval-Augmented Generation (RAG)** application that generates personalized travel plans using AI. Built with **Endee** as the high-performance vector database for semantic search and similarity operations.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Problem Statement](#problem-statement)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Endee Integration](#endee-integration)
- [Features](#features)
- [Setup Instructions](#setup-instructions)
- [Usage Guide](#usage-guide)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## 📘 Project Overview

**AI Travel Planner** is an intelligent travel planning system that combines multiple AI techniques to generate customized travel itineraries. It leverages:

- **Retrieval-Augmented Generation (RAG)**: Combines retrieved travel knowledge with AI generation
- **Semantic Search**: Uses Endee vector database for efficient similarity searches
- **Multi-Agent Orchestration**: Specialized agents for different aspects of travel planning
- **Intelligent Fallbacks**: Works even without API keys, with graceful degradation

### Key Capabilities

✨ **Semantic Travel Search** - Finds relevant travel information using embeddings  
🤖 **AI-Powered Recommendations** - Generates personalized itineraries using LLM  
💰 **Budget Optimization** - Suggests cost-effective alternatives  
📍 **Location Awareness** - Filters results by destination  
🧠 **Conversation Memory** - Remembers past queries for context  

---

## 🎯 Problem Statement

**Challenge**: Travelers need quick, personalized travel recommendations without manually browsing multiple websites.

**Solution**: An AI system that:
1. Understands natural language queries about travel
2. Searches relevant travel information efficiently
3. Generates customized itineraries with AI
4. Optimizes recommendations based on budget constraints
5. Remembers conversation context for better recommendations

**Why Endee?**
- High-performance vector database optimized for semantic search
- Efficient similarity operations using ANN (Approximate Nearest Neighbors)
- Metadata filtering for precise results
- Scales from prototype to production

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     React/HTML Frontend                     │
│                    (Port 3000 / Browser)                    │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/REST
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                 FastAPI Backend Server                      │
│                    (Port 8000)                              │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────┐  │
│  │          RAG Pipeline Orchestration                 │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │  1. PlannerAgent    → Extract (destination, budget)  │  │
│  │  2. RetrieverAgent  → Search relevant travel info    │  │
│  │  3. MemoryAgent     → Recall past context            │  │
│  │  4. GeneratorAgent  → Generate recommendations (AI)  │  │
│  │  5. BudgetAgent     → Optimize based on constraints  │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┬─────────────┐
        ▼                         ▼             ▼
 ┌──────────────┐        ┌──────────────┐   ┌──────────┐
 │ Endee Vector │        │  Groq API    │   │  Memory  │
 │  Database    │        │  (llama3)    │   │   DB     │
 │(Port 19530)  │        │              │   │          │
 └──────────────┘        └──────────────┘   └──────────┘
```

### Data Flow

```
USER QUERY
    ↓
PLANNER AGENT (Extract details: destination, budget, days)
    ↓
RETRIEVER AGENT (Search via Endee: hotels, food, routes)
    ↓
MEMORY AGENT (Get previous conversation context)
    ↓
GENERATOR AGENT (Create plan using LLM + retrieved data)
    ↓
BUDGET AGENT (Optimize recommendations)
    ↓
MEMORY AGENT (Store for future reference)
    ↓
RESPONSE TO USER
```

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend** | FastAPI | REST API framework |
| **Vector DB** | Endee | Semantic search & embeddings |
| **Embeddings** | Sentence-Transformers | Generate vector embeddings |
| **LLM** | Groq (llama3-8b) | AI response generation |
| **Frontend** | HTML5/CSS3/JS | User interface |
| **Server** | Uvicorn | ASGI application server |
| **Python** | 3.12 | Runtime environment |

---

## 🎯 Endee Integration

### What is Endee?

[Endee](https://github.com/endee-io/endee) is a high-performance vector database designed for:
- Efficient semantic search using embeddings
- Metadata-based filtering and annotation
- Approximate Nearest Neighbor (ANN) search
- Scalable similarity operations
- Local and cloud deployment

### How AI Travel Planner Uses Endee

#### 1. **Data Indexing Phase**

```python
# Travel data is encoded into vectors and stored in Endee
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

travel_data = {
    "text": "Budget hotels in Manali range from ₹800 to ₹2500",
    "metadata": {"location": "Manali", "type": "hotel"}
}

# Create embedding
embedding = model.encode(travel_data["text"])

# Store in Endee (via VectorDB wrapper)
db.add(text=travel_data["text"], 
       embedding=embedding,
       metadata=travel_data["metadata"])
```

#### 2. **Retrieval Phase (Semantic Search)**

```python
# User query: "Plan a trip to Manali"
query = "Plan a trip to Manali"
query_embedding = model.encode(query)

# Search in Endee for similar travel data
results = db.search(
    query_embedding=query_embedding,
    top_k=5,
    filters={"location": "Manali"}  # Metadata filtering
)

# Results: Most relevant hotels, food, routes in Manali
```

#### 3. **Hybrid Search with Fallback**

```python
# If Endee server is unavailable, system automatically
# falls back to in-memory search using same algorithm

class VectorDB:
    def __init__(self):
        self.use_endee = self._init_endee()  # Try to connect
        
    def search(self, query_embedding, filters=None):
        if self.use_endee:
            return self._search_endee(query_embedding, filters)
        else:
            return self._search_memory(query_embedding, filters)
```

#### 4. **Advantages of Using Endee**

| Feature | Benefit |
|---------|---------|
| **Semantic Search** | Find relevant travel info even with different wording |
| **Metadata Filtering** | Quickly narrow down by location, type, price range |
| **Fast Retrieval** | ANN algorithms provide sub-millisecond search |
| **Scalability** | Handle millions of travel records efficiently |
| **Hybrid Approach** | Memory fallback ensures robustness |

---

## ✨ Features

### 1. Intelligent Query Understanding
- Extracts destination, budget, and trip duration from natural language
- Handles various formats: "Manali", "₹15000", "3 days", etc.

### 2. Semantic Travel Search
- Searches through 13+ travel records using semantic similarity
- Finds relevant hotels, food, routes, and activities
- Metadata filtering for precise results

### 3. AI-Powered Recommendations  
- Generates detailed itineraries using Groq LLM
- Creates day-by-day travel plans
- Fallback demo responses ensure functionality without API key

### 4. Budget Optimization
- Analyzes user budget
- Recommends cost-effective alternatives
- Categories: Budget (<₹5000), Medium (₹5000-10000), Premium (>₹10000)

### 5. Conversation Memory
- Stores past queries and interactions
- Recalls context for improved recommendations
- Top-2 similar past interactions retrieved

### 6. Production-Ready Fallbacks
- Works without Groq API key (demo mode)
- Works without Endee server (in-memory fallback)
- Graceful error handling and logging

---

## 📦 Setup Instructions

### Prerequisites

- **Python 3.9+** (tested on 3.12)
- **Git**
- **Docker** (optional, for Endee)
- **Virtual Environment** (venv, conda, etc.)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/ai-travel-planner.git
cd ai-travel-planner
```

### Step 2: Create Virtual Environment

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r Backend/requirements.txt
```

### Step 4: Set Up Environment Variables

```bash
# Create .env file
cp .env.example .env

# Edit .env and add your Groq API key
# Get it from: https://console.groq.com
GROQ_API_KEY=gsk_xxxxxxxxxxxxx
ENDEE_HOST=http://localhost:19530
ENDEE_USE_FALLBACK=true
```

### Step 5: Run with Endee (Optional but Recommended)

#### Option A: Run Endee with Docker

```bash
# Start Endee server using docker-compose
docker-compose up -d endee

# Wait for it to start (check logs)
docker-compose logs -f endee

# Should see: "Listening on 0.0.0.0:19530"
```

#### Option B: Run Endee from Source

```bash
# Clone Endee repository
git clone https://github.com/endee-io/endee.git
cd endee

# Follow Endee's build instructions (C++ project)
./build.sh

# Run the server
./bin/endee --port 19530
```

### Step 6: Run Backend Server

```bash
cd Backend

# With Uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Or with Python
python main.py
```

### Step 7: Run Frontend

```bash
# In a new terminal, navigate to frontend
cd frontend

# Start HTTP server (Python 3.x)
python3 -m http.server 3000

# Or use Node.js if available
npx http-server -p 3000
```

### Step 8: Access the Application

- **Web UI**: [http://localhost:3000](http://localhost:3000)
- **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health Check**: [http://localhost:8000/](http://localhost:8000/)

---

## 🚀 Usage Guide

### Using the Web Interface

1. Open [http://localhost:3000](http://localhost:3000)
2. Type a travel query:
   - "Plan a 3-day trip to Manali with ₹15000 budget"
   - "Best hotels in Goa"
   - "Food recommendations in Jaipur"
3. Click "Plan" or press Enter
4. View personalized recommendations

### Using the API

#### Health Check

```bash
curl http://localhost:8000/
```

Response:
```json
{
  "message": "AI Travel Planner API Running 🚀",
  "version": "1.0.0",
  "technology": "RAG with Endee Vector Database",
  "endpoints": {
    "POST /plan": "Generate travel plan",
    "GET /status": "System status"
  }
}
```

#### Generate Travel Plan

```bash
curl -X POST http://localhost:8000/plan \
  -H "Content-Type: application/json" \
  -d '{"query": "Plan a 3-day trip to Manali with 15000 rupees budget"}'
```

Response:
```json
{
  "response": {
    "itinerary": "Day 1: Arrive in Manali, explore Hadimba Temple...",
    "hotels": "Budget hotels in Manali range from ₹800 to ₹2500",
    "food": "Try local Himachali cuisine and momos",
    "routes": "Delhi to Manali via Chandigarh highway (12 hours)",
    "budget": "₹15000 covers accommodation, food, and sightseeing",
    "recommendations": "Visit Solang Valley for adventure activities",
    "budget_note": "Low budget → hostels, buses, local food"
  }
}
```

#### Check System Status

```bash
curl http://localhost:8000/status
```

Response:
```json
{
  "system": "operational",
  "database": {
    "using_endee": true,
    "fallback_mode": false,
    "memory_items": 13,
    "endee_host": "http://localhost:19530"
  },
  "ai_model": "llama3-8b-8192 (Groq)",
  "features": ["RAG", "Semantic Search", "Travel Planning", "Budget Optimization", "Memory"]
}
```

### Python Script Usage

```python
from Backend.rag_pipeline import run_rag

# Generate travel plan
result = run_rag("Plan a 5-day trip to Goa with ₹20000 budget")

print(result)
# Output: Personalized travel itinerary with recommendations
```

---

## 📚 API Documentation

### Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | Health check and API info |
| GET | `/status` | System and database status |
| POST | `/plan` | Generate travel plan |
| GET | `/docs` | Interactive API documentation (Swagger) |

### Request/Response Models

#### Query Model
```python
{
  "query": "string"  # Travel query (min 1, max 500 chars)
}
```

#### Planning Response
```python
{
  "response": {
    "itinerary": "string",      # Day-by-day plan
    "hotels": "string",         # Hotel recommendations
    "food": "string",           # Food suggestions
    "routes": "string",         # Transportation info
    "budget": "string",         # Budget breakdown
    "recommendations": "string", # General tips
    "budget_note": "string"     # Budget category advice
  }
}
```

---

## 📁 Project Structure

```
ai-travel-planner/
│
├── Backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration and environment variables
│   ├── rag_pipeline.py         # RAG orchestration pipeline
│   ├── requirements.txt        # Python dependencies
│   │
│   └── agents/
│       ├── __init__.py
│       ├── vector_db.py        # Endee vector database wrapper
│       ├── planner_agent.py    # Query detail extraction
│       ├── retriever_agent.py  # Semantic search via Endee
│       ├── generator_agent.py  # LLM response generation
│       ├── memory_agent.py     # Conversation memory
│       └── budget_agent.py     # Budget optimization
│
├── frontend/
│   └── index.html              # Web user interface (280+ lines)
│
├── data/
│   └── travel_data.txt         # Sample travel information
│
├── docker-compose.yml          # Endee server configuration
├── .env.example                # Environment variables template
├── README.md                   # This file
└── LICENSE                     # MIT License
```

### Key Files Explained

1. **vector_db.py** - The heart of Endee integration
   - Connects to Endee server on port 19530
   - Falls back to in-memory NumPy implementation
   - Provides search with metadata filtering

2. **rag_pipeline.py** - Orchestrates the 5-agent RAG system
   - Chains agents in optimal order
   - Handles errors and fallbacks
   - Returns structured JSON response

3. **agents/** - Specialized AI agents
   - Each agent has a specific responsibility
   - Can be tested and debugged independently
   - Modular for easy extension

---

## 🧪 Testing

### Test the Backend

```bash
# Terminal 1: Start backend
cd Backend && uvicorn main:app --reload

# Terminal 2: Test health check
curl http://localhost:8000/

# Test status
curl http://localhost:8000/status

# Test planning
curl -X POST http://localhost:8000/plan \
  -H "Content-Type: application/json" \
  -d '{"query": "Manali trip 3 days 10000"}'
```

### Test Endee Connection

```bash
# Check if Endee is running
curl http://localhost:19530/health

# Should return 200 if running
```

### Test with Demo Mode (Without API Key)

```bash
# Even without GROQ_API_KEY, the system works with fallback responses
unset GROQ_API_KEY
curl -X POST http://localhost:8000/plan \
  -H "Content-Type: application/json" \
  -d '{"query": "trip to goa"}'
```

---

## 🔧 Troubleshooting

### Issue: "Endee unavailable, using in-memory storage"

**Cause**: Endee server is not running

**Solution**:
```bash
# Start Endee with Docker
docker-compose up -d endee

# Or on port 19530 from source
./bin/endee --port 19530
```

### Issue: "GROQ_API_KEY not found"

**Cause**: Missing API key

**Solution**:
1. Get key from https://console.groq.com
2. Add to `.env`: `GROQ_API_KEY=gsk_xxxxx`
3. Restart backend

### Issue: Frontend not connecting to backend

**Cause**: CORS or port issues

**Solution**:
```bash
# Verify backend is running on 8000
curl http://localhost:8000/

# Check frontend runs on 3000
# Verify CORS is enabled in main.py
```

### Issue: Slow search performance

**Cause**: Using in-memory instead of Endee

**Solution**:
- Start Endee server for better performance
- Check `/status` endpoint to verify Endee is active

---

## 🚀 Production Deployment

### Docker Deployment

```bash
# Build and run with Docker
docker-compose up --build

# This starts:
# - Endee on port 19530
# - FastAPI backend on port 8000
# - Frontend on port 3000
```

### Cloud Deployment (AWS/GCP/Azure)

1. Push to GitHub
2. Deploy backend to cloud platform (Heroku, Railway, Render)
3. Configure managed Endee (native or container)
4. Set environment variables in cloud console
5. Deploy frontend to CDN (Vercel, Netlify)

### Performance Optimization

- Use managed Endee for better scalability
- Add caching layer (Redis)
- Use load balancing for multiple backend instances
- Optimize vector dimensions (384 for all-MiniLM-L6-v2)

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add docstrings to all functions
- Include error handling
- Write unit tests for new features
- Update documentation

---

## 📄 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Endee Team** - For the amazing vector database
- **Groq** - For providing fast LLM inference
- **Sentence Transformers** - For powerful embeddings
- **FastAPI Community** - For excellent documentation

---

## 📞 Support & Contact

- 📧 **Email**: your-email@example.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/ai-travel-planner/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/ai-travel-planner/discussions)

---

## 🎓 Learning Resources

- [Endee Documentation](https://github.com/endee-io/endee)
- [FastAPI Guide](https://fastapi.tiangolo.com/)
- [RAG Implementation Guide](https://docs.llamaindex.ai/)
- [Sentence Transformers](https://www.sbert.net/)
- [Vector Database Concepts](https://www.databricks.com/blog/2023/05/03/guide-to-vector-databases.html)

---

**Made with ❤️ for travel enthusiasts and AI developers**
