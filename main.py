from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from rag_pipeline import run_rag, retriever
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Travel Planner",
    description="Travel planning using RAG (Retrieval Augmented Generation) with Endee vector database",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    """Travel query model"""
    query: str

@app.on_event("startup")
def load_data():
    """Load expanded travel data on startup"""
    from expanded_dataset import TRAVEL_DATABASE
    
    retriever.add_data(TRAVEL_DATABASE)
    logger.info(f"✓ Travel data loaded successfully: {len(TRAVEL_DATABASE)} entries")

@app.get("/")
def home():
    """API health check and info"""
    return {
        "message": "AI Travel Planner API Running 🚀",
        "version": "1.0.0",
        "status": "operational",
        "technology": "RAG with Endee Vector Database",
        "endpoints": {
            "POST /plan": "Generate travel plan with AI recommendations",
            "GET /": "API health check",
            "GET /status": "System and database status",
            "GET /docs": "Interactive API documentation"
        }
    }

@app.get("/status")
def status():
    """Get comprehensive system and database status"""
    db_status = retriever.db.get_status()
    
    # Check Endee health if using it
    endee_health = {"reachable": False, "status": "unknown"}
    if db_status["vector_db"]["using_endee"]:
        try:
            import requests
            response = requests.get(f"{db_status['vector_db']['endee_host']}/health", timeout=2)
            endee_health = {
                "reachable": response.status_code == 200,
                "status": "healthy" if response.status_code == 200 else f"unhealthy ({response.status_code})"
            }
        except Exception as e:
            endee_health = {"reachable": False, "status": f"error: {str(e)}"}
    
    return {
        "system": "operational",
        "database": db_status,
        "endee_health": endee_health,
        "ai_model": "llama-3.1-8b-instant (Groq)",
        "features": ["RAG", "Semantic Search", "Travel Planning", "Budget Optimization", "Memory"],
        "architecture": "Vector DB (Endee) + RAG Pipeline + Multi-Agent Orchestration"
    }

@app.get("/endee/health")
def endee_health():
    """Check Endee vector database health"""
    from config import ENDEE_HOST
    
    try:
        import requests
        response = requests.get(f"{ENDEE_HOST}/health", timeout=2)
        if response.status_code == 200:
            return {
                "status": "healthy",
                "endee_host": ENDEE_HOST,
                "message": "Endee vector database is running and operational"
            }
        else:
            return {
                "status": "unhealthy",
                "endee_host": ENDEE_HOST,
                "http_status": response.status_code,
                "message": f"Endee returned status {response.status_code}"
            }
    except Exception as e:
        return {
            "status": "unavailable",
            "endee_host": ENDEE_HOST,
            "error": str(e),
            "message": "Cannot reach Endee server. In-memory fallback mode will be used."
        }

@app.post("/plan")
def plan(q: Query):
    """
    Generate a travel plan using RAG pipeline
    
    The pipeline:
    1. Extracts details (destination, budget, duration)
    2. Retrieves relevant travel info via semantic search
    3. Generates plan using LLM
    4. Optimizes based on budget
    5. Stores memory for context
    """
    try:
        # Validate input
        if not q or not hasattr(q, 'query'):
            return {
                "error": "Invalid request format",
                "response": None
            }
        
        query_text = q.query.strip() if isinstance(q.query, str) else str(q.query)
        
        if not query_text or len(query_text) == 0:
            return {
                "error": "Query cannot be empty",
                "response": None
            }
        
        if len(query_text) > 500:
            return {
                "error": "Query is too long (maximum 500 characters)",
                "response": None
            }
        
        logger.info(f"Processing travel plan request: {query_text}")
        response = run_rag(query_text)
        logger.info(f"Travel plan generated successfully")
        return {"response": response}
    
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return {
            "error": f"Invalid request: {str(e)}",
            "response": None
        }
    except TimeoutError as e:
        logger.error(f"Timeout error: {e}")
        return {
            "error": "Request timed out. Please try a simpler query.",
            "response": None
        }
    except Exception as e:
        logger.error(f"Unexpected error in /plan endpoint: {e}", exc_info=True)
        return {
            "error": f"Error processing request: {str(e)}",
            "response": {
                "itinerary": "Unable to generate plan due to an error",
                "hotels": "Please check your query and try again",
                "food": "Unavailable due to error",
                "routes": "Unavailable due to error",
                "budget": "Unable to estimate",
                "recommendations": "Please try again with a different query",
                "status": "error"
            }
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)