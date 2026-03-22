# System Architecture & Design

## Overview

The AI Travel Planner is a **Retrieval-Augmented Generation (RAG)** system that combines:
- **Information Retrieval**: Endee vector database for semantic search
- **Generative AI**: LLM for content creation (Groq)
- **Multi-Agent Orchestration**: Specialized agents for different tasks
- **Graceful Degradation**: Fallbacks at every layer

## Architecture Layers

### 1. Presentation Layer (Frontend)

**Technology**: HTML5 + CSS3 + JavaScript (no framework)

**Components**:
- Chat interface for user input
- Message display with formatting
- Loading states and error handling
- Responsive design

**Features**:
- XSS protection via HTML escaping
- Input validation (length, non-empty)
- Keyboard support (Enter to submit)
- Accessibility features

### 2. Application Layer (Backend)

**Framework**: FastAPI + Uvicorn

**Key Endpoints**:
```
GET  /              - Health check and metadata
POST /plan          - Generate travel plan
GET  /status        - System and DB status
GET  /docs          - Swagger UI documentation
```

**Error Handling**:
- Global exception handlers
- Graceful fallbacks
- Structured error responses

### 3. Processing Layer (RAG Pipeline)

The core RAG pipeline orchestrates 5 agents:

```
User Query
    ↓
┌─────────────────────────────────────┐
│  1. PLANNER AGENT                   │
│  Task: Extract structured details   │
│  Input: Natural language query      │
│  Output: destination, budget, days  │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  2. RETRIEVER AGENT                 │
│  Task: Find relevant information    │
│  Input: Query + extracted details   │
│  Output: Hotels, food, routes       │
│  Uses: Endee semantic search        │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  3. MEMORY AGENT                    │
│  Task: Recall past context          │
│  Input: Query                       │
│  Output: Similar past interactions  │
│  Uses: Endee semantic similarity    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  4. GENERATOR AGENT                 │
│  Task: Create recommendations       │
│  Input: Query + context + memory    │
│  Output: Detailed travel plan       │
│  Uses: Groq LLM (fallback: demo)    │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  5. BUDGET AGENT                    │
│  Task: Optimize for budget          │
│  Input: Plan + budget details       │
│  Output: Budget notes & tips        │
├─────────────────────────────────────┤
│ Categories: Low/Medium/Premium      │
└─────────────────────────────────────┘
    ↓
Final Response to User
```

### 4. Data/Indexing Layer

**Vector Database**: Endee (with in-memory fallback)

**Index Structure**:
```
Document: "Budget hotels in Manali range from ₹800 to ₹2500"
  ├── Vector: [0.12, 0.45, -0.23, ...]  (384 dimensions)
  ├── Metadata:
  │   ├── location: "Manali"
  │   ├── type: "hotel"
  │   └── price_range: "budget"
  └── ID: unique_identifier
```

**Storage Options**:
- **Primary**: Endee server (remote/docker)
- **Fallback**: In-memory NumPy arrays
- **Future**: Pinecone, Weaviate, Milvus

### 5. Support Services

**Embedding Model**: 
- Sentence-Transformers: all-MiniLM-L6-v2
- Dimensions: 384
- Type: Semantic embeddings

**LLM Service**:
- Provider: Groq
- Model: llama3-8b-8192
- Alternative: Fallback demo responses

## Data Flow Detailed

### 1. Data Ingestion

```python
travel_texts = [
    "Budget hotels in Manali...",
    "Manali food specialties...",
    ...
]

for text in travel_texts:
    # Step 1: Generate embedding
    embedding = SentenceTransformer.encode(text)
    
    # Step 2: Store in Endee with metadata
    endee.add(
        id=unique_id,
        vector=embedding,
        metadata={"location": "Manali", "type": "hotel"},
        data={"text": text}
    )
```

### 2. Query Processing

```
User Query: "Plan a 3-day trip to Manali with ₹15000"
    ↓
Planner Agent Extracts:
  - destination: "Manali"
  - budget: 15000
  - days: 3
    ↓
Retriever Agent Searches Endee:
  - Encode query: [0.1, 0.2, ..., 0.15]  (384 dims)
  - Search with filters: location="Manali"
  - Returns top-5 similar documents
    ↓
Generator Agent Creates Plan:
  - Uses: User query + retrieved context
  - Calls: Groq LLM API
  - Returns: Structured itinerary
    ↓
Budget Agent Optimizes:
  - Analyzes budget tier
  - Adds cost-saving tips
    ↓
Response to User
```

### 3. Fallback Mechanisms

**Layer 1: Embedding Generation**
- Primary: Sentence-Transformers
- Fallback: Random vectors (not ideal, for testing only)

**Layer 2: Vector Search**
- Primary: Endee (fast, scalable)
- Fallback: In-memory NumPy (slower, always available)

**Layer 3: LLM Response**
- Primary: Groq API (high quality)
- Fallback: Template-based demo responses

**Layer 4: Metadata Filtering**
- Primary: Endee filtering
- Fallback: In-memory dictionary lookup

## Performance Characteristics

### Search Performance

| Database | 1K Items | 100K Items | Response Time |
|----------|----------|-----------|---------------|
| Endee (ANN) | <10ms | <50ms | Sub-second |
| Memory (NumPy) | <5ms | 500ms+ | Seconds (large) |

### API Response Times

```
Without Groq API Key:
  Extract details:  ~5ms
  Retrieve context: ~100ms (Endee) or ~500ms (memory)
  Generate response: ~50ms (template)
  Total: ~150ms - 600ms

With Groq API Key:
  Extract details:  ~5ms
  Retrieve context: ~100ms
  Generate response: 500ms-2s (LLM latency)
  Total: 600ms - 2.1s
```

## Security Considerations

### Input Validation
- Query length: 1-500 characters
- Type checking via Pydantic
- XSS prevention in frontend

### API Security
- CORS enabled for development
- No authentication (can be added)
- No rate limiting default (can be added)

### Data Privacy
- No data persistence by default
- Queries not logged
- API keys not exposed in responses

## Scalability Strategy

### Current Scale (Single Instance)
- ~1,000 users/day
- ~10,000 API calls/day
- ~13 travel documents

### Medium Scale (Multi-instance)
- Add load balancer (nginx)
- Multiple backend instances
- Managed Endee service
- Caching layer (Redis)

### Large Scale (Distributed)
- Kubernetes orchestration
- Auto-scaling groups
- Distributed Endee cluster
- Message queue (RabbitMQ/Kafka)
- Microservices architecture

## Monitoring & Observability

### Metrics to Track
- API response times
- Endee search latency
- LLM generation time
- Cache hit rates
- Error rates by type

### Logging
- Request/response logs
- Error stack traces
- Performance metrics
- Database operations

### Health Checks
- Endee server status: `GET http://endee:19530/health`
- Backend health: `GET http://backend:8000/`
- Frontend health: `GET http://frontend:3000/`

## Technology Rationale

### Why Endee?
1. ✅ Purpose-built for vector search
2. ✅ Multiple filtering options
3. ✅ Local and cloud deployment
4. ✅ High performance ANN search
5. ✅ Open source and transparent

### Why Groq?
1. ✅ Fast inference (40x faster than other APIs)
2. ✅ Free tier with 30k tokens/day
3. ✅ Simple API
4. ✅ No setup complexity

### Why Sentence-Transformers?
1. ✅ Pre-trained on semantic tasks
2. ✅ Lightweight (80MB model)
3. ✅ Fast inference (100+ samples/sec)
4. ✅ Cross-platform compatibility

## Future Enhancements

### Short Term
- [ ] Add user authentication
- [ ] Persistent conversation history
- [ ] Multi-language support
- [ ] Rate limiting

### Medium Term
- [ ] Web UI redesign (React/Vue)
- [ ] Advanced filtering options
- [ ] Integration with booking APIs
- [ ] Real-time price updates
- [ ] Map visualization

### Long Term
- [ ] Multi-modal queries (text + images)
- [ ] Real-time collaborative planning
- [ ] Personalized preferences
- [ ] AR/VR travel preview
- [ ] Blockchain-based ratings

## Testing Strategy

### Unit Tests
- Test each agent independently
- Mock Endee and LLM responses
- Validate data transformations

### Integration Tests
- Test full RAG pipeline
- Test with real Endee
- Test fallback mechanisms

### Performance Tests
- Load testing with k6 or locust
- Response time benchmarking
- Concurrent user simulation

### Security Tests
- XSS prevention verification
- SQL injection tests (if DB added)
- API abuse scenarios

## Deployment Checklist

- [ ] Set all environment variables
- [ ] Start Endee service
- [ ] Run database migration (if applicable)
- [ ] Set up monitoring/logging
- [ ] Configure backups
- [ ] Set up CDN for frontend
- [ ] Enable HTTPS/TLS
- [ ] Configure firewall rules
- [ ] Set up auto-scaling
- [ ] Create runbooks for common issues
- [ ] Set up incident response
- [ ] Document rollback procedures

---

For more details on Endee integration, see [ENDEE_INTEGRATION.md](ENDEE_INTEGRATION.md)
