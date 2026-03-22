"""
Vector Database Integration with Endee

Endee (https://github.com/endee-io/endee) is a high-performance vector database 
optimized for semantic search and similarity operations.

This module provides:
- Connection to Endee server (configurable via ENDEE_HOST)
- Fallback to in-memory implementation if Endee is unavailable
- Efficient semantic search with metadata filtering
- Support for RAG (Retrieval Augmented Generation) workflows
- Automatic retry with exponential backoff
- Connection pooling for better performance
"""

import numpy as np
import requests
import logging
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from config import ENDEE_HOST, ENDEE_USE_FALLBACK
except ImportError:
    # Fallback defaults if config not available
    ENDEE_HOST = "http://localhost:19530"
    ENDEE_USE_FALLBACK = True

logger = logging.getLogger(__name__)


class VectorDB:
    """
    Hybrid Vector Database: Endee with in-memory fallback
    
    Uses Endee as the primary vector store for production.
    Falls back to in-memory storage if Endee is unavailable.
    
    Features:
    - Semantic similarity search using cosine distance
    - Metadata filtering (location, category, type, etc.)
    - Vector persistence and retrieval
    - Graceful degradation with automatic retry
    - Connection pooling for performance
    - Exponential backoff retry strategy
    """

    def __init__(self, endee_host: str = None, use_fallback: bool = None):
        """
        Initialize Vector Database with connection pooling
        
        Args:
            endee_host: Endee server URL (defaults to ENDEE_HOST from config)
            use_fallback: Enable in-memory fallback if Endee unavailable (defaults to ENDEE_USE_FALLBACK from config)
        """
        # Use environment config or provided parameters
        self.endee_host = endee_host or ENDEE_HOST
        use_fallback_enabled = use_fallback if use_fallback is not None else ENDEE_USE_FALLBACK
        
        self.use_endee = False
        self.fallback_mode = False
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 3
        
        # In-memory storage (fallback)
        self.vectors = []
        self.texts = []
        self.metadata = []
        self.next_id = 0
        
        # Connection pooling setup
        self.session = self._create_session()
        
        logger.info(f"VectorDB initialized with Endee host: {self.endee_host}")
        
        # Try to connect to Endee
        if use_fallback_enabled:
            self._init_endee()
        else:
            logger.warning("Endee disabled, using in-memory storage only")

    def _create_session(self) -> requests.Session:
        """Create HTTP session with connection pooling and retry strategy"""
        session = requests.Session()
        
        # Retry strategy with exponential backoff
        retry_strategy = Retry(
            total=3,
            backoff_factor=0.5,  # 0.5s, 1s, 2s
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]  # Updated from method_whitelist
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=10, pool_maxsize=20)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session

    def _init_endee(self):
        """Initialize connection to Endee server with retry logic"""
        try:
            logger.info(f"Attempting to connect to Endee at {self.endee_host}...")
            response = self.session.get(f"{self.endee_host}/health", timeout=3)
            if response.status_code == 200:
                self.use_endee = True
                self.reconnect_attempts = 0
                logger.info(f"✓ Successfully connected to Endee server at {self.endee_host}")
                self._create_collection()
            else:
                logger.warning(f"Endee health check returned status {response.status_code}")
                self._enable_fallback()
        except requests.exceptions.ConnectionError as e:
            self._enable_fallback(f"Connection refused: {type(e).__name__}")
        except requests.exceptions.Timeout as e:
            self._enable_fallback(f"Connection timeout")
        except Exception as e:
            self._enable_fallback(f"Unexpected error: {type(e).__name__}")

    def _enable_fallback(self, error: str = ""):
        """Enable in-memory fallback"""
        self.fallback_mode = True
        self.use_endee = False
        msg = f"⚠️  Endee unavailable, using in-memory storage fallback"
        if error:
            msg += f" ({error})"
        logger.warning(msg)

    def _create_collection(self):
        """Create or get Endee collection"""
        try:
            url = f"{self.endee_host}/collections"
            response = requests.get(url, timeout=5)
            if response.status_code != 200:
                logger.warning("Could not access Endee collections")
                self._enable_fallback()
        except Exception as e:
            self._enable_fallback(str(e))

    def add(self, text: str, embedding: List[float], metadata: Dict[str, Any]):
        """
        Add vector with metadata
        
        Args:
            text: Original text content
            embedding: Vector embedding
            metadata: Associated metadata (location, type, etc.)
        """
        if self.use_endee:
            self._add_to_endee(text, embedding, metadata)
        else:
            self._add_to_memory(text, embedding, metadata)

    def _add_to_endee(self, text: str, embedding: List[float], metadata: Dict[str, Any]):
        """Add vector to Endee with retry logic"""
        try:
            data = {
                "text": text,
                "embedding": embedding,
                "metadata": metadata,
                "id": self.next_id
            }
            url = f"{self.endee_host}/vectors"
            response = self.session.post(url, json=data, timeout=5)
            if response.status_code == 201:
                self.next_id += 1
                return True
            else:
                logger.debug(f"Endee add failed: {response.status_code}, falling back to memory")
                self._add_to_memory(text, embedding, metadata)
                return False
        except Exception as e:
            logger.debug(f"Endee add error: {type(e).__name__}, falling back to memory")
            self._add_to_memory(text, embedding, metadata)
            return False

    def _add_to_memory(self, text: str, embedding: List[float], metadata: Dict[str, Any]):
        """Add vector to in-memory storage"""
        self.vectors.append(np.array(embedding))
        self.texts.append(text)
        self.metadata.append(metadata)

    def search(self, query_embedding: List[float], top_k: int = 5, 
               filters: Optional[Dict[str, Any]] = None) -> List[Dict]:
        """
        Semantic similarity search
        
        Args:
            query_embedding: Query vector
            top_k: Number of results to return
            filters: Metadata filters {'key': 'value'}
            
        Returns:
            List of results with text, metadata, and similarity score
        """
        if self.use_endee:
            return self._search_endee(query_embedding, top_k, filters)
        else:
            return self._search_memory(query_embedding, top_k, filters)

    def _search_endee(self, query_embedding: List[float], top_k: int, 
                      filters: Optional[Dict] = None) -> List[Dict]:
        """Search using Endee with connection pooling"""
        try:
            data = {
                "embedding": query_embedding,
                "top_k": top_k,
                "filters": filters or {}
            }
            url = f"{self.endee_host}/search"
            response = self.session.post(url, json=data, timeout=10)
            if response.status_code == 200:
                return response.json().get("results", [])
            else:
                logger.debug(f"Endee search failed: {response.status_code}, using in-memory")
                return self._search_memory(query_embedding, top_k, filters)
        except Exception as e:
            logger.debug(f"Endee search error: {type(e).__name__}, using in-memory")
            return self._search_memory(query_embedding, top_k, filters)

    def _search_memory(self, query_embedding: List[float], top_k: int,
                       filters: Optional[Dict] = None) -> List[Dict]:
        """Search using in-memory storage"""
        query = np.array(query_embedding)
        results = []

        for i, vec in enumerate(self.vectors):
            meta = self.metadata[i]

            # Apply filters
            if filters:
                valid = True
                for k, v in filters.items():
                    if v and meta.get(k) != v:
                        valid = False
                        break
                if not valid:
                    continue

            # Calculate cosine similarity
            score = self._cosine_similarity(query, vec)

            results.append({
                "text": self.texts[i],
                "metadata": meta,
                "score": float(score)
            })

        # Sort by score and return top-k
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    @staticmethod
    def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        """Calculate cosine similarity between vectors"""
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
            
        return float(np.dot(a, b) / (norm_a * norm_b))

    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive database status"""
        # Attempt reconnection if currently in fallback mode
        if self.fallback_mode and self.use_endee is False:
            self._attempt_reconnect()
        
        status = {
            "vector_db": {
                "using_endee": self.use_endee,
                "fallback_mode": self.fallback_mode,
                "memory_items": len(self.texts),
                "endee_host": self.endee_host,
                "mode": "endee" if self.use_endee else "in-memory",
                "reconnect_attempts": self.reconnect_attempts
            },
            "configuration": {
                "endee_enabled": ENDEE_USE_FALLBACK,
                "endee_host": ENDEE_HOST,
                "fallback_available": True
            }
        }
        return status
    
    def _attempt_reconnect(self):
        """Attempt to reconnect to Endee if it's back online"""
        if self.reconnect_attempts >= self.max_reconnect_attempts:
            return  # Don't spam reconnection attempts
        
        try:
            response = self.session.get(f"{self.endee_host}/health", timeout=2)
            if response.status_code == 200:
                self.use_endee = True
                self.fallback_mode = False
                self.reconnect_attempts = 0
                logger.info(f"✓ Reconnected to Endee server at {self.endee_host}")
        except Exception:
            self.reconnect_attempts += 1
            # Keep fallback mode active