from agents.planner_agent import PlannerAgent
from agents.retriever_agent import RetrieverAgent
from agents.generator_agent import GeneratorAgent
from agents.memory_agent import MemoryAgent
from agents.budget_agent import BudgetAgent
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

planner = PlannerAgent()
retriever = RetrieverAgent()
generator = GeneratorAgent()
memory = MemoryAgent()
budget = BudgetAgent()

def run_rag(query: str) -> Dict[str, Any]:
    """
    Execute RAG pipeline with comprehensive error handling
    
    Pipeline stages:
    1. Plan - Extract details
    2. Retrieve - Find relevant info
    3. Recall - Get memory
    4. Generate - Create response
    5. Optimize - Apply budget rules
    6. Store - Save for memory
    
    Args:
        query: User travel planning query
        
    Returns:
        Dictionary with travel plan details
    """
    # Validate input
    if not query or not isinstance(query, str):
        logger.warning("Invalid query received")
        return _get_error_response("Invalid query format")
    
    query = query.strip()
    if not query:
        logger.warning("Empty query received")
        return _get_error_response("Query cannot be empty")
    
    if len(query) > 500:
        logger.warning(f"Query too long: {len(query)} characters")
        return _get_error_response("Query too long (max 500 characters)")
    
    try:
        logger.info(f"Processing query: {query}")
        
        # Stage 1: Extract details
        details = _safe_extract_details(query)
        dest = details.get("destination")

        # Stage 2: Retrieve relevant info
        context = _safe_retrieve_context(query, dest)

        # Stage 3: Recall memory
        mem = _safe_recall_memory(query)

        # Stage 4: Generate response
        result = _safe_generate(query, context, mem)

        # Stage 5: Optimize for budget
        result = _safe_optimize_budget(result, details.get("budget"))

        # Stage 6: Store for memory
        _safe_store_memory(query, result)

        return result

    except Exception as e:
        logger.error(f"Critical error in RAG pipeline: {e}", exc_info=True)
        return _get_error_response(f"Error processing request: {str(e)}")


def _get_error_response(error_msg: str) -> Dict[str, str]:
    """Generate standardized error response"""
    return {
        "itinerary": "Unable to generate plan",
        "hotels": "Service temporarily unavailable",
        "food": "N/A",
        "routes": "N/A",
        "budget": "N/A",
        "recommendations": "Please try again",
        "error": error_msg
    }


def _safe_extract_details(query: str) -> Dict[str, Any]:
    """Safely extract details from query"""
    try:
        details = planner.extract_details(query)
        logger.info(f"Extracted details: {details}")
        return details or {"destination": None, "budget": None, "days": None}
    except Exception as e:
        logger.error(f"Planner error: {e}")
        return {"destination": None, "budget": None, "days": None}


def _safe_retrieve_context(query: str, dest: str) -> Dict[str, list]:
    """Safely retrieve context"""
    try:
        context = {
            "hotels": retriever.retrieve(query, dest, "hotel") if dest else retriever.retrieve(query, None, "hotel"),
            "food": retriever.retrieve(query, dest, "food") if dest else retriever.retrieve(query, None, "food"),
            "routes": retriever.retrieve(query, dest, "route") if dest else retriever.retrieve(query, None, "route")
        }
        logger.info(f"Retrieved {len(context.get('hotels', []))} hotels, {len(context.get('food', []))} food items")
        return context
    except Exception as e:
        logger.error(f"Retriever error: {e}")
        return {"hotels": [], "food": [], "routes": []}


def _safe_recall_memory(query: str) -> List[str]:
    """Safely recall memory"""
    try:
        mem = memory.recall(query)
        logger.info(f"Recalled {len(mem)} memories")
        return mem or []
    except Exception as e:
        logger.error(f"Memory recall error: {e}")
        return []


def _safe_generate(query: str, context: Dict, mem: List) -> Dict[str, str]:
    """Safely generate response"""
    try:
        result = generator.generate(query, context, mem)
        logger.info("Generated travel plan successfully")
        return result or _get_error_response("Generation failed")
    except Exception as e:
        logger.error(f"Generator error: {e}")
        return _get_error_response(str(e))


def _safe_optimize_budget(result: Dict, budget: Any) -> Dict:
    """Safely optimize budget"""
    try:
        result = budget.optimize(result, budget)
        logger.info("Optimized with budget constraints")
        return result or {}
    except Exception as e:
        logger.error(f"Budget optimization error: {e}")
        return result


def _safe_store_memory(query: str, result: Dict) -> bool:
    """Safely store memory"""
    try:
        memory.store(query, str(result))
        logger.info("Stored query in memory")
        return True
    except Exception as e:
        logger.error(f"Memory storage error: {e}")
        return False