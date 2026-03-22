# Endee Vector Database Integration Guide

## What is Endee?

[Endee](https://github.com/endee-io/endee) is a high-performance vector database designed for:
- **Semantic Search**: Find similar items using embeddings
- **Approximate Nearest Neighbors (ANN)**: Fast similarity search at scale
- **Metadata Filtering**: Filter results by attributes
- **Production Ready**: Optimized for speed and reliability

## Why Endee for Travel Planning?

| Use Case | Requirement | Endee Solution |
|----------|-------------|----------------|
| Find similar hotels | Semantic similarity | Vector cosine similarity |
| Filter by location | Metadata filtering | Location field filtering |
| Real-time search | Fast response | Sub-millisecond ANN |
| Scalability | Handle growth | Distributed architecture |
| Cost-effective | Budget conscious | Open source + self-hosted |

## Architecture Integration

### How AI Travel Planner Uses Endee

```
┌─────────────────┐
│  Application    │
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────────────────────────┐
│  Vector DB Wrapper (vector_db.py)   │
│  ├─ Endee Client                    │
│  └─ In-Memory Fallback              │
└────────┬────────────────────────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌──────────────┐
│ Endee  │ │ In-Memory DB │
│Server  │ │ (NumPy)      │
└────────┘ └──────────────┘
```

### Vector DB Wrapper Implementation

```python
class VectorDB:
    """Hybrid: Endee (primary) + In-Memory (fallback)"""
    
    def __init__(self, endee_host="http://localhost:19530"):
        self.endee_host = endee_host
        self.use_endee = self._init_endee()
        
        # Fallback storage
        self.vectors = []      # NumPy arrays
        self.texts = []        # Original text
        self.metadata = []     # Attributes
    
    def add(self, text, embedding, metadata):
        if self.use_endee:
            self._add_to_endee(text, embedding, metadata)
        else:
            self._add_to_memory(text, embedding, metadata)
    
    def search(self, query_embedding, top_k=5, filters=None):
        if self.use_endee:
            return self._search_endee(query_embedding, top_k, filters)
        else:
            return self._search_memory(query_embedding, top_k, filters)
```

## Data Indexing in Endee

### Step 1: Prepare Data

```python
travel_data = [
    {
        "text": "Budget hotels in Manali range from ₹800 to ₹2500",
        "metadata": {
            "location": "Manali",
            "type": "hotel",
            "price_range": "budget",
            "id": "hotel_001"
        }
    },
    {
        "text": "Solang Valley offers skiing and adventure sports",
        "metadata": {
            "location": "Manali",
            "type": "activity",
            "category": "adventure",
            "id": "activity_001"
        }
    },
    # ... more documents
]
```

### Step 2: Generate Embeddings

```python
from sentence_transformers import SentenceTransformer

# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")

for item in travel_data:
    # Generate embedding vector (384 dimensions)
    embedding = model.encode(item["text"])
    
    # Store in Endee
    db.add(
        text=item["text"],
        embedding=embedding.tolist(),
        metadata=item["metadata"]
    )
```

### Step 3: Store in Endee

The wrapper handles this:

```python
def _add_to_endee(self, text, embedding, metadata):
    """Store vector and metadata in Endee"""
    try:
        data = {
            "text": text,
            "embedding": embedding,      # 384-dim vector
            "metadata": metadata,        # Filtering fields
            "id": self.next_id
        }
        response = requests.post(
            f"{self.endee_host}/vectors",
            json=data,
            timeout=5
        )
        if response.status_code == 201:
            self.next_id += 1
        else:
            # Fallback to in-memory
            self._add_to_memory(text, embedding, metadata)
    except Exception as e:
        # Connection failed, use memory
        self._add_to_memory(text, embedding, metadata)
```

## Semantic Search Implementation

### Basic Search

```python
# User query
user_query = "Plan a trip to Manali"

# Step 1: Encode query to embedding
query_embedding = model.encode(user_query)  # [384 dims]

# Step 2: Search in Endee
results = db.search(
    query_embedding=query_embedding.tolist(),
    top_k=5
)

# Results:
[
    {
        "text": "Budget hotels in Manali...",
        "metadata": {"location": "Manali", "type": "hotel"},
        "score": 0.87  # Cosine similarity (0-1)
    },
    {
        "text": "Solang Valley offers skiing...",
        "metadata": {"location": "Manali", "type": "activity"},
        "score": 0.72
    },
    # Top 5 results...
]
```

### Filtered Search

```python
# Search with metadata filtering
results = db.search(
    query_embedding=query_embedding,
    top_k=5,
    filters={
        "location": "Manali",
        "type": "hotel"
    }
)

# Only returns hotels in Manali
```

### Cosine Similarity Calculation

```python
import numpy as np

def cosine_similarity(a, b):
    """Calculate similarity between two vectors (0-1)"""
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
    
    return float(np.dot(a, b) / (norm_a * norm_b))

# Example:
# Query embedding: [0.1, 0.5, -0.2, ...]
# Doc embedding:   [0.15, 0.48, -0.18, ...]
# Similarity:      0.987 (very similar)
```

## RAG Pipeline with Endee

### Complete Flow

```python
from rag_pipeline import run_rag

# User input
query = "3-day trip to Manali with ₹15000 budget"

# RAG Pipeline:
result = run_rag(query)

# Internally:
"""
1. PLANNER extracts: destination="Manali", budget=15000, days=3

2. RETRIEVER searches Endee:
   - Hotels: "Budget hotels in Manali..."
   - Food: "Manali specialties..."
   - Activities: "Adventure sports..."

3. MEMORY recalls similar past queries

4. GENERATOR creates personalized plan:
   - Day 1: Arrive, explore markets
   - Day 2: Adventure at Solang Valley
   - Day 3: Nature walks

5. BUDGET optimizes for ₹15000

6. MEMORY stores for future context
"""
```

## Configuration

### .env Settings for Endee

```bash
# Endee server location
ENDEE_HOST=http://localhost:19530

# Use in-memory if Endee unavailable
ENDEE_USE_FALLBACK=true
```

### Connection Options

#### Local Development
```bash
# Endee runs locally
ENDEE_HOST=http://localhost:19530
```

#### Docker Deployment
```bash
# Endee in Docker
ENDEE_HOST=http://endee:19530
```

#### Remote Deployment
```bash
# Managed Endee service
ENDEE_HOST=https://endee.company.com:19530
```

## Setting Up Endee Server

### Option 1: Docker (Recommended for Development)

```bash
# Using docker-compose
docker-compose up -d endee

# Check if running
curl http://localhost:19530/health

# View logs
docker-compose logs -f endee
```

### Option 2: Local Build

```bash
# Clone Endee
git clone https://github.com/endee-io/endee.git
cd endee

# Build (requires C++ toolchain)
./build.sh

# Run server
./bin/endee --port 19530
```

### Option 3: Managed Service

```
Contact Endee team for:
- Cloud-managed Endee
- Enterprise support
- Uptime SLA
- Scalability guarantees
```

## Monitoring Endee

### Health Check

```bash
curl http://localhost:19530/health
# Response: 200 if healthy
```

### Status Endpoint

```bash
curl http://localhost:8000/status

# Response:
{
  "database": {
    "using_endee": true,
    "fallback_mode": false,
    "memory_items": 13,
    "endee_host": "http://localhost:19530"
  }
}
```

### Logging

Check vector_db.py for logging:

```python
import logging
logger = logging.getLogger(__name__)

logger.info("✓ Connected to Endee server")
logger.warning("Endee unavailable, using in-memory storage")
logger.error(f"Endee error: {error}")
```

## Performance Tuning

### Embedding Dimensions

Current: 384 dimensions (all-MiniLM-L6-v2)

For different tradeoffs:
- **Smaller** (96-128 dims): Faster but less accurate
- **Larger** (768+ dims): More accurate but slower

### Top-K Results

Currently: top_k=5

Adjust based on use case:
- Fewer results = faster search
- More results = better diversity

### Batch Size

Consider batch processing:

```python
def add_batch(self, items, batch_size=100):
    """Add multiple items efficiently"""
    for i in range(0, len(items), batch_size):
        batch = items[i:i+batch_size]
        for item in batch:
            self.add(item["text"], 
                    item["embedding"], 
                    item["metadata"])
```

## Troubleshooting

### Issue: "Endee unavailable, using in-memory storage"

**Diagnosis**:
- Endee server not running
- Network connectivity issue
- Wrong host/port

**Solution**:
```bash
# Start Endee
docker-compose up -d endee

# Verify health
curl http://localhost:19530/health

# Check logs
docker-compose logs endee
```

### Issue: Search Returns No Results

**Possible causes**:
- No data indexed
- Wrong filters
- Embedding mismatch

**Solution**:
```bash
# Check status
curl http://localhost:8000/status

# Query without filters
db.search(embedding)  # Don't filter yet

# Check indexed items
# logs should show "Added N items to database"
```

### Issue: Slow Search Performance

**Possible causes**:
- Using in-memory instead of Endee
- Endee not optimized
- Too large batch

**Solution**:
- Verify Endee is running
- Check status endpoint
- Profile with logging

### Issue: Connection Refused

**Diagnosis**:
```bash
# Test connection
curl http://localhost:19530/health
# Connection refused = Endee not running
```

**Solution**:
```bash
# Start with debugging
docker-compose up endee --no-detach

# Look for errors in output
```

## Migration Path

### From In-Memory to Endee

```python
# 1. Keep in-memory data while testing
db = VectorDB(use_fallback=True)

# 2. Start Endee
docker-compose up -d endee

# 3. Reload data
# VectorDB automatically switches to Endee

# 4. Verify working
curl http://localhost:8000/status
# Should see: "using_endee": true
```

### Scaling Considerations

#### Single Instance (Now)
- 1 Endee server
- 1 Backend instance
- 13 documents
- Perfect for prototyping

#### Multi-Instance (Future)
```
Client
  ├─ Backend-1
  ├─ Backend-2
  └─ Backend-3
       ↓
    Endee Cluster
      ├─ Node-1
      ├─ Node-2
      └─ Node-3
```

## Advanced Topics

### Custom Index Schemas

```python
# Extend metadata for richer filtering
metadata = {
    "location": "Manali",
    "type": "hotel",
    "price_range": "budget",
    "amenities": ["wifi", "parking"],
    "rating": 4.5,
    "tax_applicable": True,
    "best_for": ["families", "adventure"]
}
```

### Batch Operations

```python
# Optimized for multiple adds
def bulk_index(self, items):
    for item in items:
        embedding = model.encode(item["text"])
        self.add(item["text"], embedding, item["metadata"])
    
    # Commit all at once
    if self.use_endee:
        self._flush_endee()
```

### Index Maintenance

```python
# Future enhancements
- Update vectors
- Delete outdated entries
- Reindex periodically
- Export/backup indices
```

## Best Practices

✅ **DO**:
- Test with Endee running
- Monitor vector quality
- Use appropriate metadata
- Batch updates when possible
- Keep fallback enabled

❌ **DON'T**:
- Disable fallback in production
- Index untested embeddings
- Keep Endee server off
- Use high-dimensional embeddings unnecessarily
- Forget to monitor latency

---

## References

- [Endee GitHub](https://github.com/endee-io/endee)
- [Vector Database Primer](https://www.pinecone.io/learn/vector-database/)
- [Semantic Search Guide](https://www.sbert.net/examples/applications/semantic-search/README.html)
- [RAG Best Practices](https://docs.llamaindex.ai/)

## Support

For Endee-specific issues:
- Check [Endee Issues](https://github.com/endee-io/endee/issues)
- Review Endee documentation
- Post in discussions

For AI Travel Planner issues:
- Check [Project Issues](https://github.com/yourusername/ai-travel-planner/issues)
- Review system logs
- Test with fallback enabled
