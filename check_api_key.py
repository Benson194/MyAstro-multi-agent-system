#!/usr/bin/env python3
"""
Simple script to check if GOOGLE_API_KEY is properly configured
"""
import os
import sys

# Try to load from .env file
try:
    from dotenv import load_dotenv
    from pathlib import Path
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ Found .env file at: {env_path}")
    else:
        print(f"ℹ️  No .env file found at: {env_path}")
except ImportError:
    print("ℹ️  python-dotenv not installed (optional)")

# Check for API key
api_key = os.getenv("GOOGLE_API_KEY")

if api_key:
    # Show only first/last few chars for security
    masked_key = f"{api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else "***"
    print(f"✅ GOOGLE_API_KEY is set: {masked_key}")
    print("\n✨ You're ready to run the agent!")
    print("\nTry:")
    print("  python -m my_agent.interactive data/my_viewing_history.csv")
    sys.exit(0)
else:
    print("❌ GOOGLE_API_KEY is NOT set")
    print("\n📝 To fix this, choose one option:")
    print("\n1. Set as environment variable:")
    print("   export GOOGLE_API_KEY='your-api-key-here'")
    print("\n2. Create a .env file with:")
    print("   GOOGLE_API_KEY=your-api-key-here")
    print("\n3. Add to ~/.zshrc for permanent setup:")
    print("   echo 'export GOOGLE_API_KEY=\"your-api-key-here\"' >> ~/.zshrc")
    print("   source ~/.zshrc")
    print("\n🔑 Get your API key from:")
    print("   https://aistudio.google.com/app/apikey")
    sys.exit(1)

