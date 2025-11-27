"""
Utility script to check which Gemini models are available with your API key.
Run this to see which models you can use.
"""

import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_available_models(api_key=None):
    """Check which Gemini models are available."""
    
    if not api_key:
        # Try to get from environment
        api_key = os.getenv("GEMINI_API_KEY")
        
        # Try to get from .streamlit/secrets.toml
        try:
            import streamlit as st
            api_key = st.secrets.get("GEMINI_API_KEY", "")
        except:
            pass
    
    if not api_key:
        print("❌ No API key found!")
        print("\nPlease provide your API key:")
        print("1. Set GEMINI_API_KEY environment variable")
        print("2. Add to .env file: GEMINI_API_KEY=your_key")
        print("3. Or pass as argument to this script")
        return
    
    try:
        print("🔑 Configuring Gemini API...")
        genai.configure(api_key=api_key)
        
        print("\n📋 Fetching available models...\n")
        models = genai.list_models()
        
        # Filter for generation models
        generation_models = []
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                generation_models.append(model)
        
        if not generation_models:
            print("❌ No generation models found!")
            return
        
        print(f"✅ Found {len(generation_models)} available model(s):\n")
        print("=" * 70)
        
        for i, model in enumerate(generation_models, 1):
            print(f"\n{i}. Model Name: {model.name}")
            print(f"   Display Name: {model.display_name}")
            print(f"   Description: {model.description}")
            print(f"   Supported Methods: {', '.join(model.supported_generation_methods)}")
            
            # Extract short name
            short_name = model.name.replace("models/", "")
            print(f"   Short Name: {short_name}")
            print("-" * 70)
        
        print("\n💡 Recommended models for this app:")
        recommended = []
        for model in generation_models:
            name = model.name.replace("models/", "")
            if "1.5-flash" in name.lower():
                recommended.append(f"✅ {name} (Fast & Efficient - Best Choice)")
            elif "1.5-pro" in name.lower():
                recommended.append(f"✅ {name} (Powerful & Accurate)")
            elif "pro" in name.lower() and "1.5" not in name.lower():
                recommended.append(f"✅ {name} (Stable & Reliable)")
        
        if recommended:
            for rec in recommended:
                print(f"   {rec}")
        else:
            print("   Use any model from the list above")
        
        print("\n" + "=" * 70)
        print("\n📝 To use in app.py, add these to the model list:")
        print("   model_choices = [")
        for model in generation_models[:5]:  # Show first 5
            short_name = model.name.replace("models/", "")
            print(f'       "{short_name}",')
        print("   ]")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nPossible issues:")
        print("1. Invalid API key")
        print("2. API key doesn't have proper permissions")
        print("3. Network connection issue")
        print("\nGet a new API key from: https://makersuite.google.com/app/apikey")

if __name__ == "__main__":
    import sys
    
    # Check if API key provided as argument
    api_key = None
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    
    check_available_models(api_key)

