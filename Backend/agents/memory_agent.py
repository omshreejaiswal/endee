from sentence_transformers import SentenceTransformer
from agents.vector_db import VectorDB
import logging
from typing import List, Optional, Any

logger = logging.getLogger(__name__)

class MemoryAgent:
    """Store and recall conversation history"""
    
    def __init__(self):
        try:
            self.db = VectorDB()
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            logger.info("MemoryAgent initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing MemoryAgent: {e}")
            raise

    def store(self, query: str, response: str) -> bool:
        """Store query-response pair in memory
        
        Args:
            query: User query
            response: Generated response
            
        Returns:
            True if stored successfully
        """
        try:
            if not query or not response:
                logger.warning("Cannot store empty query or response")
                return False
            
            emb = self.model.encode(query).tolist()
            self.db.add(str(response), emb, {"type": "memory"})
            logger.debug(f"Stored memory for query: {query[:50]}...")
            return True
        except Exception as e:
            logger.error(f"Error storing memory: {e}")
            return False

    def recall(self, query: str, top_k: int = 3) -> List[str]:
        """Recall similar past queries and responses
        
        Args:
            query: Current query
            top_k: Number of memories to recall
            
        Returns:
            List of relevant past responses
        """
        try:
            if not query or not isinstance(query, str):
                logger.warning(f"Invalid query for recall: {query}")
                return []
            
            emb = self.model.encode(query).tolist()
            results = self.db.search(emb, top_k=top_k, filters={"type": "memory"})
            
            recalled = [r["text"] for r in results if isinstance(r, dict) and "text" in r]
            logger.debug(f"Recalled {len(recalled)} memories for query")
            return recalled
        except Exception as e:
            logger.error(f"Error recalling memory: {e}")
            return []