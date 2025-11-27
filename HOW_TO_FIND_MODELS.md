# 🔍 How to Find Available Gemini Models

## Method 1: Using the App (Easiest)

1. **Start the app** with your API key configured
2. **Go to sidebar** → "🤖 Model Selection"
3. **Click "🔍 Check Available Models"** button
4. **See the list** of models your API key supports
5. **Select a model** from the dropdown

---

## Method 2: Using Python Script

### Quick Check Script

Run this simple script:

```powershell
# Activate venv first
.\venv\Scripts\Activate.ps1

# Run the script
python list_models.py YOUR_API_KEY
```

Or set your API key in `.env` and run:
```powershell
python list_models.py
```

### Detailed Check Script

For more detailed information:

```powershell
python check_models.py YOUR_API_KEY
```

This will show:
- Model names
- Display names
- Descriptions
- Supported methods
- Recommendations

---

## Method 3: Using Python Interactively

```python
import google.generativeai as genai

# Configure with your API key
genai.configure(api_key="YOUR_API_KEY")

# List all models
models = genai.list_models()

# Print generation models
for model in models:
    if 'generateContent' in model.supported_generation_methods:
        print(model.name)
        print(f"  Short: {model.name.replace('models/', '')}")
        print()
```

---

## Method 4: Check in Terminal

```powershell
# Activate venv
.\venv\Scripts\Activate.ps1

# Run Python
python

# Then paste:
import google.generativeai as genai
genai.configure(api_key="YOUR_KEY")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name.replace("models/", ""))
```

---

## Common Available Models

Based on Google Gemini API, these are typically available:

### ✅ Stable Models (Usually Available)
- `gemini-1.5-flash` - Fast, efficient (Recommended)
- `gemini-1.5-pro` - More powerful, accurate
- `gemini-pro` - Original stable model

### ⚠️ Experimental/Preview (May Not Be Available)
- `gemini-2.0-flash-live-001` - Experimental
- `gemini-2.5-flash-live-preview` - Preview

---

## Troubleshooting

### "No models found"
- Check your API key is valid
- Verify API key has proper permissions
- Try getting a new key from [Google AI Studio](https://makersuite.google.com/app/apikey)

### "Model not found" error
- The model name might be incorrect
- Try using short name (without "models/" prefix)
- Check if model is available for your API key

### Script errors
- Make sure `google-generativeai` is installed: `pip install google-generativeai`
- Activate virtual environment first
- Check API key format (should start with `AIzaSy`)

---

## Quick Reference

**To find models programmatically:**
```python
import google.generativeai as genai
genai.configure(api_key="YOUR_KEY")
models = [m.name.replace("models/", "") 
          for m in genai.list_models() 
          if 'generateContent' in m.supported_generation_methods]
print(models)
```

**Recommended for this app:**
- Start with: `gemini-1.5-flash`
- If that fails: `gemini-1.5-pro`
- Fallback: `gemini-pro`

---

## Files Created

- `list_models.py` - Simple model listing script
- `check_models.py` - Detailed model information script

Both can be run to check which models are available with your API key!

