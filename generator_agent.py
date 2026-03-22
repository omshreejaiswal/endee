from groq import Groq
from config import GROQ_API_KEY
import json
import logging

logger = logging.getLogger(__name__)

class GeneratorAgent:
    def __init__(self):
        """Initialize Groq client with error handling"""
        self.client = None
        self.api_key_available = False
        
        try:
            if GROQ_API_KEY:
                self.client = Groq(api_key=GROQ_API_KEY)
                self.api_key_available = True
                logger.info("✓ Groq client initialized successfully")
            else:
                logger.warning("No GROQ_API_KEY provided, will use demo responses")
        except Exception as e:
            logger.warning(f"Failed to initialize Groq client: {e}, will use demo responses")
    
    def generate(self, query, context, memory):
        """Generate travel plan using LLM or fallback"""
        try:
            if self.api_key_available and self.client:
                return self._generate_with_llm(query, context, memory)
            else:
                return self._generate_demo_response(query, context)
        except Exception as e:
            logger.error(f"Error in generate: {e}")
            return self._generate_demo_response(query, context)
    
    def _generate_with_llm(self, query, context, memory):
        """Generate using Groq LLM (llama-3.1-8b-instant)"""
        try:
            # Format context for the prompt
            context_str = ""
            if context:
                for category, items in context.items():
                    if items:
                        if isinstance(items, list):
                            context_str += f"{category}: {', '.join(str(i) for i in items[:2])}\n"
                        else:
                            context_str += f"{category}: {items}\n"
            
            prompt = f"""You are a travel consultant. Based on the travel information, create a travel plan.

IMPORTANT: Return ONLY a valid JSON object with NO markdown code blocks, NO extra text, NO explanations.

The EXACT format must be:
{{"itinerary": "...", "hotels": "...", "food": "...", "routes": "...", "budget": "...", "recommendations": "..."}}

Travel Information:
{context_str}

Query: {query}

Generate the travel plan JSON:"""

            logger.info(f"Calling Groq API with model: llama-3.1-8b-instant")
            res = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,  # Lower temperature for more consistent JSON
                max_tokens=800
            )

            text = res.choices[0].message.content.strip()
            logger.info(f"Groq API response received ({len(text)} chars)")
            
            # Clean up response - remove markdown formatting
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            
            text = text.strip()
            
            # Try to find JSON object in the response
            if text.startswith('{'):
                # Look for the closing brace
                try:
                    # Find the last closing brace
                    last_brace = text.rfind('}')
                    if last_brace > 0:
                        text = text[:last_brace+1]
                except:
                    pass
            
            try:
                result = json.loads(text)
                logger.info("✓ Successfully parsed LLM response as JSON")
                # Validate all required fields exist and are strings
                required = ["itinerary", "hotels", "food", "routes", "budget", "recommendations"]
                for field in required:
                    if field not in result:
                        result[field] = "Information available on request"
                    else:
                        # Ensure all values are strings, not objects
                        if not isinstance(result[field], str):
                            result[field] = str(result[field])
                logger.debug(f"Validated response: {list(result.keys())}")
                return result
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse LLM response: {e}")
                logger.debug(f"Attempted to parse: {text[:300]}")
                return self._generate_demo_response(query, context)
                
        except Exception as e:
            logger.error(f"LLM generation failed: {type(e).__name__}: {e}")
            return self._generate_demo_response(query, context)
    
    def _generate_demo_response(self, query, context):
        """Generate demo response when API unavailable"""
        try:
            # Extract best context data
            hotels = ""
            if context and "hotels" in context and context["hotels"]:
                hotels = context["hotels"][0] if isinstance(context["hotels"], list) else str(context["hotels"])
            else:
                hotels = "Budget and mid-range accommodations available"
            
            food = ""
            if context and "food" in context and context["food"]:
                food = context["food"][0] if isinstance(context["food"], list) else str(context["food"])
            else:
                food = "Local cuisine and international options available"
            
            routes = ""
            if context and "routes" in context and context["routes"]:
                routes = context["routes"][0] if isinstance(context["routes"], list) else str(context["routes"])
            else:
                routes = "Multiple transportation options available (train, bus, car)"
            
            return {
                "itinerary": "Day 1: Arrive at destination, explore local markets and get oriented. Day 2: Visit major attractions and try local cuisine. Day 3: Adventure activities or relaxation based on preference. Day 4+: Extended exploration of off-beat locations.",
                "hotels": hotels,
                "food": food,
                "routes": routes,
                "budget": "Daily budget: ₹2,000-5,000 for budget travelers including accommodation, food, and local transport",
                "recommendations": "Book accommodations in advance during peak season. Hire local guides. Try street food safely. Use public transport or guided tours.",
                "note": "This is a demo response. For AI-powered recommendations, ensure GROQ_API_KEY is configured in .env"
            }
        except Exception as e:
            logger.error(f"Error generating demo response: {e}")
            return {
                "itinerary": "Plan your 3-4 day trip with local exploration",
                "hotels": "Budget to mid-range options available",
                "food": "Local cuisine and restaurants nearby",
                "routes": "Public transport and guided tours recommended",
                "budget": "₹2,000-5,000 per day for comfortable travel",
                "recommendations": "Hire local guides and book in advance",
                "error": str(e)
            }