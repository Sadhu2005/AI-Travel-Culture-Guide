"""
Simple script to list available Gemini models.
Usage: python list_models.py [your_api_key]
"""

import google.generativeai as genai
import sys

def list_models(api_key):
    """List all available Gemini models."""
    try:
        genai.configure(api_key=api_key)
        print("🔍 Fetching available models...\n")
        
        models = genai.list_models()
        
        print("=" * 60)
        print("AVAILABLE GEMINI MODELS")
        print("=" * 60)
        
        count = 0
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                count += 1
                model_name = model.name.replace("models/", "")
                print(f"\n{count}. {model_name}")
                print(f"   Full name: {model.name}")
                if hasattr(model, 'display_name'):
                    print(f"   Display: {model.display_name}")
        
        print(f"\n✅ Total: {count} generation model(s) available")
        print("\n💡 Use the short names (without 'models/') in the app")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure your API key is valid!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    else:
        # Try to get from environment or ask user
        import os
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            print("Enter your Gemini API key:")
            api_key = input().strip()
    
    if api_key:
        list_models(api_key)
    else:
        print("❌ No API key provided!")
        print("Usage: python list_models.py [your_api_key]")
        print("Or set GEMINI_API_KEY environment variable")

