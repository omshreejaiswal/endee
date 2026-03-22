from sentence_transformers import SentenceTransformer
from agents.vector_db import VectorDB
import logging
from typing import List, Optional, Dict, Any

logger = logging.getLogger(__name__)

class RetrieverAgent:
    """Retrieve relevant documents using semantic search"""
    
    def __init__(self):
        try:
            self.db = VectorDB()
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            logger.info("RetrieverAgent initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing RetrieverAgent: {e}")
            raise

    def add_data(self, data: List[Dict[str, Any]]) -> int:
        """Add data to vector database
        
        Args:
            data: List of dicts with 'text' and 'metadata' keys
            
        Returns:
            Number of items added
        """
        if not data or not isinstance(data, list):
            logger.warning(f"Invalid data format: {type(data)}")
            return 0
        
        added_count = 0
        for item in data:
            try:
                if "text" not in item or "metadata" not in item:
                    logger.warning(f"Skipping item without required fields: {item}")
                    continue
                    
                embedding = self.model.encode(item["text"]).tolist()
                self.db.add(item["text"], embedding, item["metadata"])
                added_count += 1
            except Exception as e:
                logger.error(f"Error adding item: {e}")
                continue
        
        logger.info(f"Added {added_count} items to database")
        return added_count

    def retrieve(self, query: str, location: Optional[str] = None, 
                 category: Optional[str] = None, top_k: int = 5) -> List[str]:
        """Retrieve relevant documents for query
        
        Args:
            query: Search query
            location: Optional location filter
            category: Optional category filter
            top_k: Number of results to return
            
        Returns:
            List of relevant text snippets
        """
        try:
            if not query or not isinstance(query, str):
                logger.warning(f"Invalid query: {query}")
                return []
            
            query_embedding = self.model.encode(query).tolist()
            
            # Build filters
            filters = {}
            if location:
                filters["location"] = location
            if category:
                filters["type"] = category
            
            # Search with filters
            results = self.db.search(query_embedding, top_k=top_k, filters=filters)
            
            # Fallback to unfiltered search if no results
            if not results:
                logger.debug(f"No filtered results, searching without filters")
                results = self.db.search(query_embedding, top_k=top_k)
            
            return [r["text"] for r in results if isinstance(r, dict) and "text" in r]
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            return []