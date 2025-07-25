#!/usr/bin/env python3
"""
PharmacyGenius Search API Startup Script
Simple script to start the API with proper configuration
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Check if all required packages are installed"""
    try:
        import fastapi
        import uvicorn
        import openai
        import pydantic
        print(" All required packages are installed")
        return True
    except ImportError as e:
        print(f" Missing required package: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False

def check_openai_key():
    """Check if OpenAI API key is configured"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("  OpenAI API key not found!")
        print("Please set your OpenAI API key:")
        print("  Windows: set OPENAI_API_KEY=your_key_here")
        print("  Linux/Mac: export OPENAI_API_KEY=your_key_here")
        print("  Or create a .env file with: OPENAI_API_KEY=your_key_here")
        return False
    else:
        print(" OpenAI API key configured")
        return True

def start_api():
    """Start the FastAPI server"""
    print(" Starting PharmacyGenius Search API...")
    print(" API Documentation will be available at: http://localhost:8000/docs")
    print(" Postman collection: PharmacyGenius_Search_API.postman_collection.json")
    print("=" * 60)
    
    try:
        # Start the API server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n API server stopped")
    except Exception as e:
        print(f" Error starting API: {e}")

def main():
    """Main function"""
    print(" PharmacyGenius Search API")
    print("=" * 60)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check OpenAI configuration
    if not check_openai_key():
        print("\n  API will start but OpenAI features won't work without the API key")
        print("You can still test the health and info endpoints")
        
        response = input("\nContinue anyway? (y/N): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Start the API
    start_api()

if __name__ == "__main__":
    main() 