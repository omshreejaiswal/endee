import logging
from typing import Dict, Optional, Any

logger = logging.getLogger(__name__)

class PlannerAgent:
    """Extract details from user queries"""
    
    # Supported destinations with aliases
    DESTINATIONS = {
        "manali": "Manali",
        "goa": "Goa",
        "jaipur": "Jaipur",
        "shimla": "Shimla",
        "delhi": "Delhi",
        "agra": "Agra",
        "mumbai": "Mumbai",
        "bangalore": "Bangalore"
    }
    
    def extract_details(self, query: str) -> Dict[str, Any]:
        """Extract destination, budget, and days from query"""
        if not query or not isinstance(query, str):
            logger.warning(f"Invalid query type: {type(query)}")
            return {"destination": None, "budget": None, "days": None}
        
        try:
            return {
                "destination": self._extract_destination(query),
                "budget": self._extract_budget(query),
                "days": self._extract_days(query)
            }
        except Exception as e:
            logger.error(f"Error extracting details: {e}")
            return {"destination": None, "budget": None, "days": None}

    def _extract_destination(self, query: str) -> Optional[str]:
        """Extract destination from query"""
        query_lower = query.lower()
        for dest_key, dest_name in self.DESTINATIONS.items():
            if dest_key in query_lower:
                logger.debug(f"Extracted destination: {dest_name}")
                return dest_name
        return None

    def _extract_budget(self, query: str) -> Optional[int]:
        """Extract budget amount from query"""
        try:
            # Look for ₹ symbol
            for word in query.split():
                if "₹" in word:
                    budget_str = word.replace("₹", "").strip()
                    if budget_str.isdigit():
                        return int(budget_str)
            # Also check for numbers before "budget" keyword
            words = query.lower().split()
            for i, w in enumerate(words):
                if "budget" in w and i > 0:
                    if words[i-1].isdigit():
                        return int(words[i-1])
            return None
        except Exception as e:
            logger.debug(f"Error extracting budget: {e}")
            return None

    def _extract_days(self, query: str) -> Optional[int]:
        """Extract trip duration from query"""
        try:
            words = query.split()
            query_lower = query.lower()
            
            for i, w in enumerate(words):
                if "day" in w.lower():
                    # Check previous word for number
                    if i > 0 and words[i-1].isdigit():
                        try:
                            days = int(words[i-1])
                            if 1 <= days <= 365:  # Validate reasonable range
                                return days
                        except ValueError:
                            pass
            return None
        except Exception as e:
            logger.debug(f"Error extracting days: {e}")
            return None