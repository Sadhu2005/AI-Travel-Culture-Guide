# 🚀 How to Run the AI Travel & Culture Guide

## Prerequisites

1. **Python 3.11+** (for local development)
   - Check: `python --version`
   - Download: [python.org](https://www.python.org/downloads/)

2. **Docker Desktop** (for Docker method - optional)
   - Download: [docker.com](https://www.docker.com/products/docker-desktop/)

3. **Google Gemini API Key**
   - Get it from: [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Sign in with Google account
   - Click "Create API Key"
   - Copy the key

---

## Method 1: Local Development (Recommended for Development)

### Step 1: Navigate to Project Directory
```powershell
cd E:\DSA\AIT_ravel_and_Culture_Guide
```

### Step 2: Activate Virtual Environment
```powershell
# Activate the existing venv
.\venv\Scripts\Activate.ps1
```

If you see `(venv)` in your prompt, you're good to go!

### Step 3: Install Dependencies (if not already installed)
```powershell
pip install -r requirements.txt
```

### Step 4: Set Up API Key

**Option A: Using Streamlit Secrets (Recommended)**

1. Create `.streamlit` folder if it doesn't exist:
   ```powershell
   mkdir .streamlit
   ```

2. Create `secrets.toml` file:
   ```powershell
   # Create the file
   New-Item -Path .streamlit\secrets.toml -ItemType File
   ```

3. Add your API key to `.streamlit/secrets.toml`:
   ```toml
   GEMINI_API_KEY = "your_api_key_here"
   ```

**Option B: Manual Input (Easier for testing)**
- You can enter the API key directly in the app's sidebar

### Step 5: Run the Application
```powershell
streamlit run app.py
```

### Step 6: Open in Browser
- The app will automatically open in your browser
- Or manually go to: `http://localhost:8501`

---

## Method 2: Docker (Recommended for Production)

### Step 1: Navigate to Project Directory
```powershell
cd E:\DSA\AIT_ravel_and_Culture_Guide
```

### Step 2: Create Environment File
```powershell
# Create .env file with your API key
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

Or manually create `.env` file:
```
GEMINI_API_KEY=your_api_key_here
```

### Step 3: Build and Run with Docker Compose
```powershell
docker-compose up --build
```

### Step 4: Access the App
- Open browser: `http://localhost:8501`

### Step 5: Stop the Container
```powershell
# Press Ctrl+C to stop
# Or in another terminal:
docker-compose down
```

---

## Quick Commands Reference

### Local Development
```powershell
# Activate venv
.\venv\Scripts\Activate.ps1

# Run app
streamlit run app.py

# Deactivate venv (when done)
deactivate
```

### Docker
```powershell
# Start
docker-compose up --build

# Stop
docker-compose down

# View logs
docker-compose logs

# Rebuild
docker-compose up --build --force-recreate
```

---

## Troubleshooting

### Issue: "Module not found"
**Solution:**
```powershell
pip install -r requirements.txt
```

### Issue: "API key not found"
**Solution:**
- Check `.streamlit/secrets.toml` exists
- Or use sidebar to enter key manually
- For Docker: Check `.env` file

### Issue: "Port 8501 already in use"
**Solution:**
```powershell
# Find what's using the port
netstat -ano | findstr :8501

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F

# Or use a different port
streamlit run app.py --server.port 8502
```

### Issue: Docker not starting
**Solution:**
- Make sure Docker Desktop is running
- Check Docker is installed: `docker --version`
- Restart Docker Desktop

### Issue: Virtual environment not activating
**Solution:**
```powershell
# If PowerShell execution policy blocks it:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try again:
.\venv\Scripts\Activate.ps1
```

---

## First Time Setup Checklist

- [ ] Python 3.11+ installed
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] API key obtained from Google AI Studio
- [ ] API key configured (secrets.toml or .env)
- [ ] App runs successfully (`streamlit run app.py`)

---

## Using the App

1. **Enter Destination**: Type a country, city, or region (e.g., "Japan", "Paris", "Kerala")
2. **Set Duration**: Choose number of days (1-30)
3. **Add Preferences**: Describe your ideal trip
4. **Configure Settings**: Use sidebar to:
   - Select AI model
   - Choose travel style
   - Set budget level
5. **Generate**: Click "Generate Travel Guide"
6. **Explore**: View itinerary in different tabs
7. **Export**: Download as JSON or Text

---

## Need Help?

- Check `README.md` for detailed documentation
- Check `QUICK_START.md` for quick reference
- Check `IMPROVEMENTS.md` for feature list

---

**Happy Travel Planning! 🌍✈️**

