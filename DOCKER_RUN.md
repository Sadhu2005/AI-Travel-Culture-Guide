# 🐳 Running with Docker - Step by Step

## Prerequisites ✅
- ✅ Docker Desktop installed and running
- ✅ Docker Compose installed
- ✅ Google Gemini API Key

## Quick Start

### Step 1: Add Your API Key to .env File

Open `.env` file and replace `your_api_key_here` with your actual API key:

```env
GEMINI_API_KEY=AIzaSy...your_actual_key_here
```

**Get your API key from:** [Google AI Studio](https://makersuite.google.com/app/apikey)

### Step 2: Build and Run

```powershell
cd E:\DSA\AIT_ravel_and_Culture_Guide
docker-compose up --build
```

### Step 3: Access the App

Open your browser and go to: **http://localhost:8501**

---

## Docker Commands Reference

### Start the Application
```powershell
docker-compose up --build
```

### Start in Background (Detached Mode)
```powershell
docker-compose up -d --build
```

### Stop the Application
```powershell
# Press Ctrl+C if running in foreground
# Or use:
docker-compose down
```

### View Logs
```powershell
docker-compose logs
# Or follow logs in real-time:
docker-compose logs -f
```

### Rebuild (After Code Changes)
```powershell
docker-compose up --build --force-recreate
```

### Stop and Remove Everything
```powershell
docker-compose down -v
```

### Check Container Status
```powershell
docker-compose ps
```

---

## Troubleshooting

### Issue: "Cannot connect to Docker daemon"
**Solution:** Make sure Docker Desktop is running

### Issue: "Port 8501 already in use"
**Solution:**
1. Find what's using the port:
   ```powershell
   netstat -ano | findstr :8501
   ```
2. Kill the process or change port in `docker-compose.yml`:
   ```yaml
   ports:
     - "8502:8501"  # Change 8501 to 8502
   ```

### Issue: "API key not working"
**Solution:**
1. Check `.env` file exists
2. Verify API key is correct (no quotes, no spaces)
3. Restart container: `docker-compose restart`

### Issue: "Build failed"
**Solution:**
```powershell
# Clean build
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### View Container Logs
```powershell
docker-compose logs travel-guide
```

---

## Advantages of Docker

✅ **Isolated Environment**: No conflicts with system Python  
✅ **Easy Deployment**: Same environment everywhere  
✅ **No Local Setup**: Don't need to install Python dependencies  
✅ **Consistent**: Works the same on all machines  
✅ **Easy Cleanup**: Just stop and remove container  

---

## What Happens When You Run?

1. **Build Phase**: Docker builds the image with all dependencies
2. **Start Phase**: Container starts and runs Streamlit
3. **Ready**: App available at http://localhost:8501
4. **Health Check**: Docker monitors container health

---

## Next Steps

1. ✅ Add API key to `.env`
2. ✅ Run `docker-compose up --build`
3. ✅ Open http://localhost:8501
4. ✅ Start planning your trips! 🌍

---

**Happy Dockerizing! 🐳**

