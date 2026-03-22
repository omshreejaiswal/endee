"""
Complete AI Travel Planner - Backend
✅ All files are corrected and tested
"""

# FILE: Backend/config.py
import os
import warnings
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    warnings.warn(
        "GROQ_API_KEY not found in .env. Using fallback responses. "
        "Get one at: https://console.groq.com/",
        RuntimeWarning
    )

# ────────────────────────────────────────────────────────────

# FILE: Backend/rag_pipeline.py
import json
import logging
from agents.planner_agent import PlannerAgent
from agents.retriever_agent import RetrieverAgent
from agents.memory_agent import MemoryAgent
from agents.budget_agent import BudgetAgent
from agents.generator_agent import GeneratorAgent

logger = logging.getLogger(__name__)

planner = PlannerAgent()
retriever = RetrieverAgent()
memory = MemoryAgent()
budget = BudgetAgent()
generator = GeneratorAgent()


def run_rag(query):
    """
    Run the RAG (Retrieval-Augmented Generation) pipeline for travel planning.
    
    Args:
        query (str): User's travel query/request
        
    Returns:
        dict: Travel plan with itinerary, hotels, food, routes, budget, and recommendations
    """
    try:
        # Extract details from query
        details = planner.extract_details(query)
        destination = details.get("destination")
        logger.info(f"Extracted destination: {destination}, budget: {details.get('budget')}, days: {details.get('days')}")

        # Retrieve relevant information
        hotels = retriever.retrieve(query, destination, "hotel")
        food = retriever.retrieve(query, destination, "food")
        routes = retriever.retrieve(query, destination, "route")

        context = {
            "hotels": hotels,
            "food": food,
            "routes": routes
        }

        # Get past interactions from memory
        past = memory.recall(query)

        # Generate response using AI
        response = generator.generate(query, context, past)

        # Parse response
        try:
            if isinstance(response, str):
                response_json = json.loads(response)
            else:
                response_json = response
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse response as JSON: {e}")
            response_json = {"raw_output": response}

        # Optimize plan based on budget
        final = budget.optimize(response_json, details.get("budget"))

        # Store in memory for future reference
        memory.store(query, str(final))

        logger.info("RAG pipeline completed successfully")
        return final
    except Exception as e:
        logger.error(f"Error in RAG pipeline: {e}")
        return {"error": str(e), "message": "Failed to generate travel plan"}

# ────────────────────────────────────────────────────────────

# FILE: Backend/agents/planner_agent.py
import re
import logging

logger = logging.getLogger(__name__)

class PlannerAgent:
    def extract_details(self, query):
        """Extract travel details from user query."""
        return {
            "destination": self._extract_destination(query),
            "budget": self._extract_budget(query),
            "days": self._extract_days(query)
        }

    def _extract_destination(self, query):
        """Extract destination from query."""
        places = ["manali", "goa", "jaipur", "delhi", "shimla", "mumbai", "udaipur"]

        for place in places:
            if place in query.lower():
                return place.capitalize()

        return None

    def _extract_budget(self, query):
        """Extract budget amount from query."""
        try:
            match = re.search(r"(₹?\s?\d+)", query)
            return int(match.group().replace("₹", "").strip()) if match else None
        except (AttributeError, ValueError) as e:
            logger.debug(f"Could not extract budget: {e}")
            return None

    def _extract_days(self, query):
        """Extract trip duration from query."""
        try:
            match = re.search(r"(\d+)\s*day", query.lower())
            return int(match.group(1)) if match else None
        except (AttributeError, ValueError, IndexError) as e:
            logger.debug(f"Could not extract days: {e}")
            return None

# ────────────────────────────────────────────────────────────

# FILE: Backend/agents/retriever_agent.py
from sentence_transformers import SentenceTransformer
from agents.vector_db import VectorDB
import logging

logger = logging.getLogger(__name__)

class RetrieverAgent:
    def __init__(self):
        """Initialize retriever with embedding model and vector database."""
        self.db = VectorDB()
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def add_data(self, data):
        """Add travel data to vector database with embeddings."""
        try:
            for item in data:
                embedding = self.model.encode(item["text"]).tolist()
                self.db.add(item["text"], embedding, item["metadata"])
            logger.info(f"Added {len(data)} items to database")
        except Exception as e:
            logger.error(f"Error adding data: {e}")

    def retrieve(self, query, location=None, category=None):
        """Retrieve relevant travel information based on query and filters."""
        try:
            query_embedding = self.model.encode(query).tolist()

            filters = {}
            if location:
                filters["location"] = location
            if category:
                filters["type"] = category

            results = self.db.search(query_embedding, top_k=5, filters=filters or None)

            if not results:
                results = self.db.search(query_embedding, top_k=5)

            return [r["text"] for r in results]
        except Exception as e:
            logger.error(f"Error retrieving data: {e}")
            return []

# ────────────────────────────────────────────────────────────

# FILE: Backend/agents/generator_agent.py
from groq import Groq
from config import GROQ_API_KEY
import json
import logging

logger = logging.getLogger(__name__)

class GeneratorAgent:
    def __init__(self):
        """Initialize GeneratorAgent with Groq client."""
        try:
            self.client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
        except Exception as e:
            logger.warning(f"Failed to initialize Groq client: {e}. Using fallback.")
            self.client = None
    
    def generate(self, query, context, memory):
        """Generate travel plan using AI or fallback."""
        prompt = f"""
You are an AI Travel Planner.

Memory:
{memory}

Hotels: {context['hotels']}
Food: {context['food']}
Routes: {context['routes']}

User Query:
{query}

Return STRICT JSON:

{{
  "itinerary": "...",
  "hotels": "...",
  "food": "...",
  "routes": "...",
  "budget": "...",
  "recommendations": "...",
  "reason": "..."
}}
"""

        if not self.client:
            logger.info("Using fallback response (no API key)")
            return self._fallback_response(context)
        
        try:
            response = self.client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"API Error: {e}. Using fallback.")
            return self._fallback_response(context)
    
    def _fallback_response(self, context):
        """Generate fallback demo response."""
        return json.dumps({
            "itinerary": "Day 1: Arrive, explore local markets. Day 2: Adventure activities. Day 3: Nature walks and shopping.",
            "hotels": ", ".join(context.get("hotels", ["Budget hotels"])) or "Budget hotels",
            "food": ", ".join(context.get("food", ["Local cuisine"])) or "Local cuisine",
            "routes": ", ".join(context.get("routes", ["Routes info"])) or "Routes info",
            "budget": "See details in retrieved data",
            "recommendations": "Explore local attractions and cuisine",
            "reason": "Demo response using stored data"
        })

# ────────────────────────────────────────────────────────────

# FILE: Backend/agents/memory_agent.py
from sentence_transformers import SentenceTransformer
from agents.vector_db import VectorDB
import logging

logger = logging.getLogger(__name__)

class MemoryAgent:
    def __init__(self):
        """Initialize memory agent with embedding model and vector database."""
        self.db = VectorDB()
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def store(self, query, response):
        """Store query and response in memory for future reference."""
        try:
            embedding = self.model.encode(query).tolist()
            self.db.add(response, embedding, {"type": "memory"})
            logger.debug(f"Stored memory for query: {query[:50]}...")
        except Exception as e:
            logger.error(f"Error storing memory: {e}")

    def recall(self, query):
        """Recall similar past interactions based on query."""
        try:
            embedding = self.model.encode(query).tolist()
            results = self.db.search(embedding, top_k=2, filters={"type": "memory"})
            return "\n".join([r["text"] for r in results]) if results else "No memory"
        except Exception as e:
            logger.error(f"Error recalling memory: {e}")
            return "No memory"

# ────────────────────────────────────────────────────────────

# FILE: Backend/agents/budget_agent.py
import logging

logger = logging.getLogger(__name__)

class BudgetAgent:
    """Agent responsible for budget optimization and recommendations."""
    
    def optimize(self, plan, budget):
        """Optimize travel plan based on budget constraints."""
        if not budget:
            logger.debug("No budget specified")
            return plan

        try:
            if isinstance(plan, dict):
                budget_note = self._get_budget_note(budget)
                plan["budget_note"] = budget_note
                return plan
            else:
                budget_note = self._get_budget_note(budget)
                return str(plan) + "\n\n" + budget_note
        except Exception as e:
            logger.error(f"Error optimizing plan: {e}")
            return plan
    
    def _get_budget_note(self, budget):
        """Generate budget recommendation based on amount."""
        if budget < 5000:
            return "Low budget → hostels, buses, local food"
        elif budget < 10000:
            return "Medium budget → budget hotels, mix transport"
        else:
            return "Premium → luxury hotels, flights"

# ────────────────────────────────────────────────────────────

# FILE: Backend/agents/vector_db.py
import numpy as np
import logging

logger = logging.getLogger(__name__)

class VectorDB:
    """Simple in-memory vector database for similarity search."""
    
    def __init__(self):
        """Initialize empty vector database."""
        self.data = []

    def add(self, text, embedding, metadata=None):
        """Add text with embedding and metadata to database."""
        try:
            self.data.append({
                "text": text,
                "embedding": np.array(embedding),
                "metadata": metadata or {}
            })
        except Exception as e:
            logger.error(f"Error adding item: {e}")

    def search(self, query_embedding, top_k=5, filters=None):
        """Search database for similar items using cosine similarity."""
        try:
            query_embedding = np.array(query_embedding)
            results = []

            for item in self.data:
                if filters:
                    if not all(item["metadata"].get(k) == v for k, v in filters.items()):
                        continue

                score = np.dot(query_embedding, item["embedding"])
                results.append((score, item))

            results.sort(key=lambda x: x[0], reverse=True)
            return [r[1] for r in results[:top_k]]
        except Exception as e:
            logger.error(f"Error searching: {e}")
            return []

# ────────────────────────────────────────────────────────────

# FILE: Backend/agents/__init__.py
"""
Agents module for AI Travel Planner.

Contains specialized agents for different aspects of travel planning:
- PlannerAgent: Extracts travel details from queries
- RetrieverAgent: Retrieves relevant travel information
- MemoryAgent: Manages conversation history
- BudgetAgent: Optimizes plans based on budget
- GeneratorAgent: Generates travel plans using AI
"""

from .planner_agent import PlannerAgent
from .retriever_agent import RetrieverAgent
from .memory_agent import MemoryAgent
from .budget_agent import BudgetAgent
from .generator_agent import GeneratorAgent
from .vector_db import VectorDB

__all__ = [
    "PlannerAgent",
    "RetrieverAgent",
    "MemoryAgent",
    "BudgetAgent",
    "GeneratorAgent",
    "VectorDB",
]

# ────────────────────────────────────────────────────────────

# FILE: Backend/requirements.txt
fastapi>=0.100.0
uvicorn[standard]>=0.20.0
sentence-transformers>=2.2.0
groq>=0.4.0
python-dotenv>=1.0.0
numpy>=1.24.0
pandas>=1.5.0
pydantic>=2.0.0

# ────────────────────────────────────────────────────────────

# FILE: .env (CREATE THIS)
GROQ_API_KEY=your_api_key_here

# ────────────────────────────────────────────────────────────

# FILE: .env.example
GROQ_API_KEY=your_groq_api_key_here
