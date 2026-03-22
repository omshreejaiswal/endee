import logging
from typing import Dict, Optional, Any, Union

logger = logging.getLogger(__name__)

class BudgetAgent:
    """Optimize travel plans based on budget constraints"""
    
    # Budget tier thresholds
    BUDGET_TIERS = {
        "ultra_budget": (0, 3000),
        "budget": (3000, 7000),
        "mid_range": (7000, 15000),
        "premium": (15000, 30000),
        "luxury": (30000, float('inf'))
    }
    
    def optimize(self, plan: Union[Dict, str], budget: Optional[int]) -> Union[Dict, str]:
        """Optimize travel plan based on budget constraints
        
        Args:
            plan: Travel plan to optimize
            budget: Budget constraint in rupees
            
        Returns:
            Optimized travel plan with budget note
        """
        if not budget:
            logger.debug("No budget specified, returning plan as-is")
            return plan
        
        try:
            budget = int(budget) if budget else None
            if not budget or budget <= 0:
                logger.warning(f"Invalid budget: {budget}")
                return plan
            
            budget_note = self._get_budget_note(budget)
            
            if isinstance(plan, dict):
                plan["budget_note"] = budget_note
                # Ensure all fields are strings
                for key in ["itinerary", "hotels", "food", "routes", "budget", "recommendations"]:
                    if key in plan and not isinstance(plan[key], str):
                        plan[key] = str(plan[key])
                return plan
            else:
                # String format
                return str(plan) + "\n\n" + budget_note
        except Exception as e:
            logger.error(f"Error optimizing plan: {e}")
            return plan
    
    def _get_budget_note(self, budget: int) -> str:
        """Generate budget recommendation based on amount"""
        try:
            budget = int(budget)
            
            if budget < 3000:
                return "💰 Ultra Budget: Hostels, buses, street food. Max ₹1000/day for accommodation+food."
            elif budget < 7000:
                return "💰 Budget Tier: Budget hotels (₹800-1500/night), public transport, mix of local & restaurant food."
            elif budget < 15000:
                return "💰 Mid-Range: 3-4 star hotels (₹2000-3500/night), mix of transport, good restaurants."
            elif budget < 30000:
                return "💰 Premium: 4-5 star hotels (₹4000-7000/night), flights/cabs, fine dining options."
            else:
                return "💰 Luxury: 5-star hotels, private transport, exclusive experiences."
        except Exception as e:
            logger.error(f"Error generating budget note: {e}")
            return "Budget optimization not available"