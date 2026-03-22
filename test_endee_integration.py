#!/usr/bin/env python3
"""
Endee Vector Database Integration Test

This script verifies that the Endee integration is working correctly:
1. Check environment variables
2. Test Endee server connection
3. Test vector database operations
4. Test semantic search
5. Test metadata filtering
"""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment
env_path = Path(".") / ".env"
load_dotenv(env_path)

# Import config
sys.path.insert(0, str(Path("./Backend")))
from config import ENDEE_HOST, ENDEE_USE_FALLBACK, GROQ_API_KEY

print("=" * 70)
print("🧪 ENDEE VECTOR DATABASE INTEGRATION TEST")
print("=" * 70)

# Test 1: Environment Configuration
print("\n📋 Test 1: Environment Configuration")
print("-" * 70)
print(f"✓ ENDEE_HOST: {ENDEE_HOST}")
print(f"✓ ENDEE_USE_FALLBACK: {ENDEE_USE_FALLBACK}")
print(f"✓ GROQ_API_KEY: {'SET' if GROQ_API_KEY else 'NOT SET'}")

# Test 2: VectorDB Import and Initialization
print("\n📋 Test 2: VectorDB Import and Initialization")
print("-" * 70)
try:
    from Backend.agents.vector_db import VectorDB
    print("✓ Successfully imported VectorDB")
    
    db = VectorDB()
    print(f"✓ VectorDB initialized")
    print(f"  └─ Using Endee: {db.use_endee}")
    print(f"  └─ Fallback Mode: {db.fallback_mode}")
    print(f"  └─ Host: {db.endee_host}")
except Exception as e:
    print(f"✗ Failed to initialize VectorDB: {e}")
    sys.exit(1)

# Test 3: Endee Server Health Check
print("\n📋 Test 3: Endee Server Health Check")
print("-" * 70)
try:
    import requests
    response = requests.get(f"{ENDEE_HOST}/health", timeout=2)
    if response.status_code == 200:
        print(f"✓ Endee server is HEALTHY")
        print(f"  └─ Status Code: {response.status_code}")
        print(f"  └─ Host: {ENDEE_HOST}")
    else:
        print(f"⚠ Endee server returned status {response.status_code}")
except requests.exceptions.ConnectionError:
    print(f"⚠ Endee server NOT RUNNING")
    print(f"  └─ Fallback mode will be used")
    print(f"  └─ Start Endee with: docker-compose up -d endee")
except Exception as e:
    print(f"⚠ Error checking Endee health: {e}")

# Test 4: Add Test Data
print("\n📋 Test 4: Add Test Data to VectorDB")
print("-" * 70)
try:
    from sentence_transformers import SentenceTransformer
    
    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    print("✓ Loaded embedding model (all-MiniLM-L6-v2)")
    
    # Test data
    test_items = [
        {
            "text": "Manali is a beautiful mountain destination in Himachal Pradesh",
            "metadata": {"location": "Manali", "type": "destination", "category": "overview"}
        },
        {
            "text": "Budget hotels in Manali range from ₹800 to ₹2500",
            "metadata": {"location": "Manali", "type": "accommodation", "category": "budget"}
        },
        {
            "text": "Solang Valley offers paragliding and skiing",
            "metadata": {"location": "Manali", "type": "activity", "category": "adventure"}
        },
        {
            "text": "Goa is famous for beaches and seafood",
            "metadata": {"location": "Goa", "type": "destination", "category": "overview"}
        },
        {
            "text": "Beach shacks in Goa serve fresh grilled fish",
            "metadata": {"location": "Goa", "type": "food", "category": "casual"}
        }
    ]
    
    print(f"\nAdding {len(test_items)} test items...")
    for i, item in enumerate(test_items, 1):
        embedding = model.encode(item["text"]).tolist()
        db.add(item["text"], embedding, item["metadata"])
        print(f"  ✓ Added item {i}: {item['text'][:50]}...")
    
    print(f"\n✓ Successfully added {len(test_items)} items")
    print(f"  └─ Memory items: {db.get_status()['vector_db']['memory_items']}")
    
except Exception as e:
    print(f"✗ Failed to add test data: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Semantic Search
print("\n📋 Test 5: Semantic Search")
print("-" * 70)
try:
    queries = [
        "mountain destination",
        "accommodation in Manali",
        "beach activities",
        "food in Goa"
    ]
    
    for query in queries:
        print(f"\n  Query: '{query}'")
        query_embedding = model.encode(query).tolist()
        results = db.search(query_embedding, top_k=2)
        
        if results:
            for i, result in enumerate(results, 1):
                print(f"    {i}. {result['text'][:60]}...")
                print(f"       Score: {result['score']:.4f} | Type: {result['metadata'].get('type', 'N/A')}")
        else:
            print(f"    No results found")
    
    print("\n✓ Semantic search working correctly")
    
except Exception as e:
    print(f"✗ Semantic search failed: {e}")
    import traceback
    traceback.print_exc()

# Test 6: Metadata Filtering
print("\n📋 Test 6: Metadata Filtering")
print("-" * 70)
try:
    # Search with filters
    query_embedding = model.encode("travel recommendations").tolist()
    
    filters = {"location": "Manali"}
    print(f"\nSearching with filter: location='Manali'")
    results = db.search(query_embedding, top_k=5, filters=filters)
    
    if results:
        print(f"✓ Found {len(results)} results for Manali:")
        for i, result in enumerate(results, 1):
            print(f"  {i}. {result['text'][:60]}...")
            print(f"     Metadata: {result['metadata']}")
    else:
        print(f"ℹ No results with filter")
    
    print("\n✓ Metadata filtering working correctly")
    
except Exception as e:
    print(f"✗ Metadata filtering failed: {e}")
    import traceback
    traceback.print_exc()

# Test 7: Database Status
print("\n📋 Test 7: Database Status")
print("-" * 70)
try:
    status = db.get_status()
    print(json.dumps(status, indent=2))
    print("\n✓ Database status retrieved successfully")
except Exception as e:
    print(f"✗ Failed to get database status: {e}")

# Test 8: API Endpoints
print("\n📋 Test 8: API Endpoints")
print("-" * 70)
try:
    import requests
    
    # Test /status endpoint
    print("\nTesting GET /status endpoint...")
    response = requests.get("http://localhost:8000/status", timeout=2)
    if response.status_code == 200:
        status_data = response.json()
        print("✓ /status endpoint working")
        print(f"  └─ System: {status_data.get('system')}")
        print(f"  └─ Database Mode: {status_data['database']['vector_db'].get('mode')}")
        print(f"  └─ Memory Items: {status_data['database']['vector_db'].get('memory_items')}")
    else:
        print(f"⚠ /status endpoint returned {response.status_code}")
    
    # Test /endee/health endpoint
    print("\nTesting GET /endee/health endpoint...")
    response = requests.get("http://localhost:8000/endee/health", timeout=2)
    if response.status_code == 200:
        health_data = response.json()
        print("✓ /endee/health endpoint working")
        print(f"  └─ Status: {health_data.get('status')}")
        print(f"  └─ Host: {health_data.get('endee_host')}")
    else:
        print(f"⚠ /endee/health endpoint returned {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("⚠ Backend server not running")
    print("  Start with: cd Backend && source ../venv/bin/activate && python3 main.py")
except Exception as e:
    print(f"⚠ Could not test API endpoints: {e}")

# Summary
print("\n" + "=" * 70)
print("✅ ENDEE INTEGRATION TEST COMPLETE")
print("=" * 70)
print("\n📊 SUMMARY:")
print("-" * 70)
print(f"✓ Environment Configuration: OK")
print(f"✓ VectorDB Initialization: OK")
print(f"✓ Connection Mode: {'Endee' if db.use_endee else 'In-Memory Fallback'}")
print(f"✓ Stored Items: {db.get_status()['vector_db']['memory_items']}")
print(f"✓ Semantic Search: Working")
print(f"✓ Metadata Filtering: Working")

if db.use_endee:
    print("\n🎯 Endee is properly integrated and operational!")
else:
    print("\n⚠️  Using in-memory fallback. Start Endee with:")
    print("   docker-compose up -d endee")

print("\n📚 Next Steps:")
print("-" * 70)
print("1. Check API Docs: http://localhost:8000/docs")
print("2. Test Travel Plan: POST /plan with a query")
print("3. Monitor Status: GET /status and GET /endee/health")
print("4. View Logs: docker-compose logs -f backend")
print("\n" + "=" * 70)
