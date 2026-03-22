#!/usr/bin/env python3
"""Find available Groq models"""

import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(".") / ".env"
load_dotenv(env_path)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if GROQ_API_KEY:
    from groq import Groq
    client = Groq(api_key=GROQ_API_KEY)
    
    # Try to list models or get available models info
    try:
        models = client.models.list()
        print("✅ Available Groq Models:")
        for model in models.data:
            print(f"  - {model.id}")
    except Exception as e:
        print(f"Could not list models: {e}")
        
    # Try some common models
    test_models = [
        "llama-3.1-70b-versatile",
        "llama-3.1-8b-instant", 
        "llama-3.2-90b-vision-preview",
        "llama-3.2-1b-preview",
        "gemma-7b-it",
        "gemma2-9b-it"
    ]
    
    print("\nTesting model availability:")
    for model_name in test_models:
        try:
            message = client.chat.completions.create(
                messages=[{"role": "user", "content": "Test"}],
                model=model_name,
                max_tokens=10
            )
            print(f"  ✓ {model_name} - WORKING")
            break  # Found a working model
        except Exception as e:
            error_msg = str(e)
            if "decommissioned" in error_msg:
                print(f"  ✗ {model_name} - DECOMMISSIONED")
            elif "not found" in error_msg:
                print(f"  ✗ {model_name} - NOT FOUND")
            else:
                print(f"  ? {model_name} - ERROR: {type(e).__name__}")
