#!/usr/bin/env python3
"""Test Groq API connection and functionality"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment
env_path = Path(".") / ".env"
print(f"Loading .env from: {env_path.absolute()}")
load_dotenv(env_path)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
print(f"\n✓ GROQ_API_KEY found: {bool(GROQ_API_KEY)}")

if GROQ_API_KEY:
    print(f"  API Key (first 20 chars): {GROQ_API_KEY[:20]}...")
    
    try:
        from groq import Groq
        print("\n Initializing Groq client...")
        client = Groq(api_key=GROQ_API_KEY)
        print("✓ Groq client initialized successfully")
        
        # Test with working model
        print("\n Testing Groq API with mixtral-8x7b-32768...")
        message = client.chat.completions.create(
            messages=[{"role": "user", "content": "Generate a brief 1-line travel tip for India"}],
            model="mixtral-8x7b-32768",
            max_tokens=100
        )
        print(" Groq API is WORKING!")
        print(f"   Response: {message.choices[0].message.content}")
        
        # Test JSON response
        print("\n Testing JSON response generation...")
        message = client.chat.completions.create(
            messages=[{"role": "user", "content": 'Return only valid JSON: {"destination": "Manali", "days": 3, "budget": 15000}'}],
            model="mixtral-8x7b-32768",
            max_tokens=100
        )
        print("✓ JSON response test:")
        print(f"   {message.choices[0].message.content}")
        
    except Exception as e:
        print(f"\n Groq API error:")
        print(f"   {type(e).__name__}: {e}")
else:
    print(" No API key found in .env")
