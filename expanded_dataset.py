#!/usr/bin/env python3
"""Comprehensive Travel Database with Expanded Details"""

TRAVEL_DATABASE = [
    # ===== MANALI SECTION =====
    {
        "text": "Manali, Himachal Pradesh: Located at 2,050m elevation in the Kullu Valley, Manali is a premier destination for adventure and relaxation",
        "metadata": {"location": "Manali", "state": "Himachal Pradesh", "type": "destination", "category": "overview", "altitude": "2050m"}
    },
    {
        "text": "Siddu is the famous traditional steamed bread of Manali, made with rice flour and served with dal",
        "metadata": {"location": "Manali", "type": "food", "category": "local_cuisine", "price_range": "budget"}
    },
    {
        "text": "Manali Momos are delicious dumplings filled with vegetables or meat, served with spicy sauce",
        "metadata": {"location": "Manali", "type": "food", "category": "local_cuisine", "price_range": "budget"}
    },
    {
        "text": "Trout fish from local rivers is a specialty protein dish in Manali restaurants",
        "metadata": {"location": "Manali", "type": "food", "category": "fine_dining", "price_range": "mid_range"}
    },
    {
        "text": "Budget hotels in Manali range from ₹800 to ₹2,500 per night in town center",
        "metadata": {"location": "Manali", "type": "accommodation", "category": "budget", "price_per_night": "800-2500", "rating": "basic"}
    },
    {
        "text": "Mid-range hotels in Manali cost ₹2,500 to ₹5,000 per night with decent amenities",
        "metadata": {"location": "Manali", "type": "accommodation", "category": "mid_range", "price_per_night": "2500-5000", "rating": "good"}
    },
    {
        "text": "Premium resorts in Manali range from ₹5,000 to ₹15,000+ per night with luxury facilities",
        "metadata": {"location": "Manali", "type": "accommodation", "category": "luxury", "price_per_night": "5000+", "rating": "excellent"}
    },
    {
        "text": "Solang Valley near Manali offers paragliding, skiing, and adventure sports during winter months",
        "metadata": {"location": "Manali", "type": "activity", "category": "adventure", "best_season": "December-February", "duration": "2-4 hours"}
    },
    {
        "text": "Rohtang Pass at 3,978m elevation provides stunning Himalayan views and is 50km from Manali",
        "metadata": {"location": "Manali", "type": "attraction", "category": "scenic", "distance_km": 50, "best_time": "May-October"}
    },
    {
        "text": "Hadimba Devi Temple is a 500-year-old pagoda-style temple surrounded by cedar forests in Manali",
        "metadata": {"location": "Manali", "type": "attraction", "category": "religious_site", "built_year": 1553, "entry_free": True}
    },
    {
        "text": "Delhi to Manali via Chandigarh highway takes 12-14 hours: Delhi → Chandigarh (250km, 4.5h) → Manali (290km, 8-9h)",
        "metadata": {"location": "Manali", "type": "route", "starting_point": "Delhi", "distance_km": 540, "duration_hours": "12-14", "transport": "road"}
    },
    {
        "text": "Manali is best visited during May-June (summer) and September-October (early autumn) for pleasant weather",
        "metadata": {"location": "Manali", "type": "travel_info", "category": "best_season", "months": "May-June, Sep-Oct", "temperature": "15-25°C"}
    },
    
    # ===== GOA SECTION =====
    {
        "text": "Goa: India's smallest state famous for beaches, Portuguese heritage, and vibrant nightlife",
        "metadata": {"location": "Goa", "state": "Goa", "type": "destination", "category": "overview", "beaches": 40, "language": "Konkani"}
    },
    {
        "text": "Goa seafood market offers fresh fish, prawns, and crabs cooked with coconut and spices",
        "metadata": {"location": "Goa", "type": "food", "category": "fine_dining", "specialty": "seafood", "price_range": "mid_range"}
    },
    {
        "text": "Goan beach shacks serve fresh grilled fish, crab curry rice, and local Kingfish for ₹300-800 per dish",
        "metadata": {"location": "Goa", "type": "food", "category": "casual", "price_range": "budget", "ambiance": "beachfront"}
    },
    {
        "text": "Feni is a traditional Goan distilled spirit made from cashew apples, available at duty-free stores",
        "metadata": {"location": "Goa", "type": "food", "category": "beverages", "price_range": "budget", "local_specialty": True}
    },
    {
        "text": "Budget hotels in Goa start from ₹1,500 per night near beaches and up to ₹3,000 in town",
        "metadata": {"location": "Goa", "type": "accommodation", "category": "budget", "price_per_night": "1500-3000", "location_preference": "near_beach"}
    },
    {
        "text": "Mid-range hotels in Goa offer ₹3,000-6,000 per night with sea views and pool facilities",
        "metadata": {"location": "Goa", "type": "accommodation", "category": "mid_range", "price_per_night": "3000-6000", "amenities": "pool, sea_view"}
    },
    {
        "text": "Beach huts in Goa rent for ₹800-2,000 per night, offering authentic Goan beach experience",
        "metadata": {"location": "Goa", "type": "accommodation", "category": "budget_unique", "price_per_night": "800-2000", "type_accommodation": "hut"}
    },
    {
        "text": "North Goa beaches like Baga and Calangute are lively with water sports and nightlife until 3 AM",
        "metadata": {"location": "Goa", "type": "activity", "category": "beach_life", "beaches": "Baga, Calangute", "ambiance": "lively"}
    },
    {
        "text": "South Goa beaches like Palolem are serene with yoga centers, backpacker hostels, and firelight dinners",
        "metadata": {"location": "Goa", "type": "activity", "category": "relaxation", "beaches": "Palolem, Benaulim", "ambiance": "peaceful"}
    },
    {
        "text": "Scuba diving in Goa is available year-round at Grande Island, exploring shipwrecks and coral reefs",
        "metadata": {"location": "Goa", "type": "activity", "category": "water_sports", "location": "Grande Island", "price": "₹2500-5000"}
    },
    {
        "text": "Best time to visit Goa is November to February when weather is pleasant and dry (25-30°C)",
        "metadata": {"location": "Goa", "type": "travel_info", "category": "best_season", "months": "Nov-Feb", "temperature": "25-30°C", "rainfall": "minimal"}
    },
    {
        "text": "Mumbai to Goa via NH48 highway takes 12-13 hours (590km) or 2-2.5 hours by flight",
        "metadata": {"location": "Goa", "type": "route", "starting_point": "Mumbai", "distance_km": 590, "duration_hours": "12-13", "transport": "road"}
    },
    
    # ===== JAIPUR SECTION =====
    {
        "text": "Jaipur, Rajasthan: The Pink City famous for Mughal architecture, desert landscape, and royal heritage",
        "metadata": {"location": "Jaipur", "state": "Rajasthan", "type": "destination", "category": "overview", "nickname": "Pink City", "monuments": 15}
    },
    {
        "text": "City Palace Jaipur is an active royal palace combining Mughal and Rajasthani architecture, partially open to tourists",
        "metadata": {"location": "Jaipur", "type": "attraction", "category": "palace", "entry_fee": "₹400", "still_inhabited": True}
    },
    {
        "text": "Hawa Mahal (Palace of Winds) is an iconic 5-story pink structure with 953 small windows, designed for royal women",
        "metadata": {"location": "Jaipur", "type": "attraction", "category": "landmark", "built_year": 1799, "entry_fee": "₹50", "architecture": "unique"}
    },
    {
        "text": "Jantar Mantar is an astronomical observation site with 19 instruments, recognized as UNESCO World Heritage Site",
        "metadata": {"location": "Jaipur", "type": "attraction", "category": "historical", "built_year": 1734, "entry_fee": "₹200", "unesco": True}
    },
    {
        "text": "Dal baati churma is the signature Rajasthani dish: lentil curry with baked bread and sweet crumble for ₹150-300",
        "metadata": {"location": "Jaipur", "type": "food", "category": "local_cuisine", "price_range": "budget", "specialty": "vegetarian"}
    },
    {
        "text": "Gatte ki sabzi is a popular Jaipur vegetable curry made with gram flour dumplings in yogurt sauce",
        "metadata": {"location": "Jaipur", "type": "food", "category": "local_cuisine", "price_range": "budget", "vegetarian": True}
    },
    {
        "text": "Mirchi vada (spicy chili fritter) and lassi are popular street snacks in Jaipur's bazaars for ₹20-50",
        "metadata": {"location": "Jaipur", "type": "food", "category": "street_food", "price_range": "very_budget", "location": "bazaars"}
    },
    {
        "text": "Budget hotels in Jaipur range from ₹1,000 to ₹2,500 per night near Railway Station or City Center",
        "metadata": {"location": "Jaipur", "type": "accommodation", "category": "budget", "price_per_night": "1000-2500", "location_preference": "city_center"}
    },
    {
        "text": "Mid-range hotels in Jaipur offer ₹2,500-5,000 with breakfast and good service near attractions",
        "metadata": {"location": "Jaipur", "type": "accommodation", "category": "mid_range", "price_per_night": "2500-5000", "amenities": "breakfast, wifi"}
    },
    {
        "text": "Heritage hotels in Jaipur provide authentic Rajasthani experience for ₹4,000-10,000 per night",
        "metadata": {"location": "Jaipur", "type": "accommodation", "category": "heritage", "price_per_night": "4000-10000", "experience": "traditional"}
    },
    {
        "text": "Delhi to Jaipur via NH48 is 265km and takes 4 hours, perfect for day trip or weekend getaway",
        "metadata": {"location": "Jaipur", "type": "route", "starting_point": "Delhi", "distance_km": 265, "duration_hours": 4, "transport": "road"}
    },
    {
        "text": "Jaipur is best visited October-March when weather is cool (15-25°C) and comfortable for sightseeing",
        "metadata": {"location": "Jaipur", "type": "travel_info", "category": "best_season", "months": "Oct-Mar", "temperature": "15-25°C", "rainfall": "minimal"}
    },
    
    # ===== DELHI SECTION =====
    {
        "text": "Delhi: India's capital city with rich history spanning 5,000 years and diverse culture",
        "metadata": {"location": "Delhi", "type": "destination", "category": "overview", "dividing_feature": "old_new", "monuments": 1338}
    },
    {
        "text": "Street food in Delhi includes Chaat (₹30-50), Aloo Tikki, Samosa, and Pani Puri at roadside vendors",
        "metadata": {"location": "Delhi", "type": "food", "category": "street_food", "price_range": "very_budget", "experience": "must_try"}
    },
    {
        "text": "Butter Chicken and Tandoori dishes from North Indian cuisine cost ₹200-400 at mid-range restaurants",
        "metadata": {"location": "Delhi", "type": "food", "category": "local_cuisine", "price_range": "budget", "cuisine": "North Indian"}
    },
    {
        "text": "Budget hotels in Delhi range from ₹800-2,000 in Backpacker areas like Paharganj",
        "metadata": {"location": "Delhi", "type": "accommodation", "category": "budget", "price_per_night": "800-2000", "area": "Paharganj"}
    },
    {
        "text": "Mid-range hotels in Delhi cost ₹2,500-5,000 near Metro stations with good connectivity",
        "metadata": {"location": "Delhi", "type": "accommodation", "category": "mid_range", "price_per_night": "2500-5000", "connectivity": "metro"}
    },
    {
        "text": "Red Fort is a UNESCO World Heritage Site showcasing Mughal architecture with ₹30 entry fee",
        "metadata": {"location": "Delhi", "type": "attraction", "category": "historical", "entry_fee": "₹30", "built_year": 1648, "heritage": "mughal"}
    },
    {
        "text": "Delhi Metro is the fastest way to travel costing ₹10-40 per journey with efficient 6-line network",
        "metadata": {"location": "Delhi", "type": "transport", "category": "local_travel", "price_per_journey": "10-40", "speed": "fastest"}
    },
    
    # ===== SHIMLA SECTION =====
    {
        "text": "Shimla, Himachal Pradesh: A charming hill station at 2,159m elevation famous for colonial architecture",
        "metadata": {"location": "Shimla", "state": "Himachal Pradesh", "type": "destination", "category": "overview", "altitude": "2159m", "architecture": "colonial"}
    },
    {
        "text": "Budget hotels in Shimla start from ₹1,200 per night in off-season, ₹2,500+ in peak season",
        "metadata": {"location": "Shimla", "type": "accommodation", "category": "budget", "price_per_night": "1200-2500", "seasonal": True}
    },
    {
        "text": "The Ridge and Mall Road are shopping and recreation centers with cafes, shops, and panoramic Himalayan views",
        "metadata": {"location": "Shimla", "type": "activity", "category": "leisure", "location": "town_center", "views": "himalayan"}
    },
    {
        "text": "Toy Train from Shimla to Kalka (96km) is a UNESCO World Heritage route offering scenic views for ₹300-500",
        "metadata": {"location": "Shimla", "type": "attraction", "category": "heritage_transport", "distance_km": 96, "price": "₹300-500", "duration_hours": 5}
    },
    
    # ===== UDAIPUR SECTION =====
    {
        "text": "Udaipur, Rajasthan: The Lake City built around four artificial lakes with stunning palaces and havelis",
        "metadata": {"location": "Udaipur", "state": "Rajasthan", "type": "destination", "category": "overview", "lakes": 4, "royal_heritage": True}
    },
    {
        "text": "City Palace Udaipur is a magnificent structure blending Mughal and Rajasthani architecture overlooking Lake Pichola",
        "metadata": {"location": "Udaipur", "type": "attraction", "category": "palace", "view": "lake_pichola", "entry_fee": "₹300", "rooms_count": 700}
    },
    {
        "text": "Lake Pichola boat ride costs ₹300-500 per person offering sunset views and island visits",
        "metadata": {"location": "Udaipur", "type": "activity", "category": "boat_ride", "price": "₹300-500", "duration_hours": "1-2", "best_time": "sunset"}
    },
    {
        "text": "Budget hotels in Udaipur range from ₹1,500-3,000 with views of Lake Pichola",
        "metadata": {"location": "Udaipur", "type": "accommodation", "category": "budget", "price_per_night": "1500-3000", "view": "lake_view"}
    },
    
    # ===== GENERAL TRAVEL TIPS =====
    {
        "text": "Best travel time in India is October-March (winter) for comfortable weather across most destinations",
        "metadata": {"type": "travel_info", "category": "general_advice", "topic": "best_season", "coverage": "all_india"}
    },
    {
        "text": "Budget for accommodation, food, and transport varies: ₹2,000-5,000/day for budget travelers",
        "metadata": {"type": "travel_info", "category": "budgeting", "daily_budget": "2000-5000", "traveler_type": "budget"}
    },
    {
        "text": "Traveling by train is economical: AC sleeper ₹1,000-3,000 and bus ₹500-1,500 for long routes",
        "metadata": {"type": "travel_info", "category": "transport_costs", "transport": "train_bus"}
    },
    {
        "text": "Travel insurance costs ₹500-2,000 for 1-2 weeks depending on coverage type",
        "metadata": {"type": "travel_info", "category": "travel_essentials", "requirement": "insurance", "price_range": "500-2000"}
    },
    {
        "text": "Indian SIM cards provide cheap local calls and data: ₹300-500 for 1GB daily data for 30 days",
        "metadata": {"type": "travel_info", "category": "connectivity", "service": "mobile_data", "price": "300-500"}
    },
]

if __name__ == "__main__":
    print(f"✓ Travel Database contains {len(TRAVEL_DATABASE)} entries")
    print("\nDataset includes information on:")
    locations = set()
    types = set()
    for entry in TRAVEL_DATABASE:
        loc = entry.get("metadata", {}).get("location")
        t = entry.get("metadata", {}).get("type")
        if loc:
            locations.add(loc)
        if t:
            types.add(t)
    
    print(f"  Locations: {', '.join(sorted(locations))}")
    print(f"  Categories: {', '.join(sorted(types))}")
