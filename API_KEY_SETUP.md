# 🔑 API Key Setup Guide

## The Error You're Seeing

```
Error calling Gemini API: 400 API key not valid. 
Please pass a valid API key.
```

This means the app needs a valid Google Gemini API key to work.

---

## ✅ Quick Fix (Easiest Method)

### Use the Sidebar in the App

1. **Look at the left sidebar** in your running app
2. **Find "⚙️ Settings"** section
3. **Under "🔑 API Configuration"**, select **"Manual Input"**
4. **Paste your API key** in the text field
5. **Click "🚀 Generate Travel Guide"** again

**That's it!** The app will use the key you entered.

---

## 🔧 Permanent Setup (Recommended)

### Step 1: Get Your API Key

1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key (starts with `AIzaSy...`)

### Step 2: Add to Secrets File

**For Local Development:**

1. Open `.streamlit/secrets.toml` file
2. Replace the content with:
   ```toml
   GEMINI_API_KEY = "AIzaSy...your_actual_key_here"
   ```
3. Save the file
4. **Restart the Streamlit app** (stop with Ctrl+C and run again)

**For Docker:**

1. Open `.env` file in the project root
2. Add:
   ```env
   GEMINI_API_KEY=AIzaSy...your_actual_key_here
   ```
3. Restart Docker:
   ```powershell
   docker-compose down
   docker-compose up --build
   ```

---

## 📍 File Locations

- **Local secrets**: `.streamlit/secrets.toml`
- **Docker env**: `.env` (in project root)

---

## ⚠️ Important Notes

1. **Never commit API keys to Git** - They're already in `.gitignore`
2. **Keep your key private** - Don't share it publicly
3. **Key format**: Should start with `AIzaSy` and be about 39 characters
4. **No quotes needed** in `.env` file, but needed in `.toml` file

---

## 🧪 Test Your API Key

After adding the key, try generating an itinerary:
1. Enter a destination (e.g., "Kerala")
2. Set number of days (e.g., 3)
3. Add preferences (e.g., "going with my family")
4. Click "Generate Travel Guide"

If it works, you'll see the itinerary appear! 🎉

---

## 🐛 Still Not Working?

### Check:
- ✅ API key is correct (no extra spaces)
- ✅ Key starts with `AIzaSy`
- ✅ App was restarted after adding key to secrets file
- ✅ Using the correct key source (Manual Input or Secrets)

### Common Issues:

**"API key not found"**
- Make sure you selected "Manual Input" in sidebar, OR
- Check `.streamlit/secrets.toml` exists and has the key

**"Invalid API key"**
- Verify the key is correct
- Make sure no extra spaces or quotes
- Try generating a new key from Google AI Studio

**"Key works in sidebar but not in secrets"**
- Restart the Streamlit app after editing secrets.toml
- Check the file format is correct (TOML syntax)

---

## 📞 Need Help?

- Check the app sidebar for API key input
- Verify your key at: https://makersuite.google.com/app/apikey
- Make sure the key has proper permissions

---

**Once your API key is set, the app will work perfectly! 🚀**

