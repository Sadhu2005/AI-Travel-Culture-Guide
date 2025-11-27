# 🌍 AI Travel & Culture Guide

A beautiful, intelligent travel itinerary generator powered by Google's Gemini AI. Create personalized travel guides with cultural insights, local recommendations, and practical travel tips.

## ✨ Features

- **🤖 AI-Powered Itineraries**: Generate detailed day-by-day travel plans using Google Gemini AI
- **🎭 Cultural Insights**: Get cultural etiquette, traditions, and local customs for your destination
- **💡 Fun Facts & Trivia**: Learn interesting facts about your destination
- **📚 Country Database**: Access pre-loaded information for 50+ countries
- **📥 Export Options**: Download your itinerary as JSON or text
- **🎨 Beautiful UI**: Modern, responsive interface with sidebar configuration
- **⚙️ Customizable**: Choose travel style, budget level, and preferences
- **🐳 Docker Support**: Easy deployment with Docker and Docker Compose

## 🚀 Quick Start

### Option 1: Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AIT_ravel_and_Culture_Guide
   ```

2. **Set up environment variables**
   ```bash
   # Create .env file
   echo "GEMINI_API_KEY=your_api_key_here" > .env
   ```

3. **Run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Access the app**
   Open your browser and navigate to `http://localhost:8501`

### Option 2: Local Development

1. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Key**
   
   Create a `.streamlit/secrets.toml` file:
   ```toml
   GEMINI_API_KEY = "your_api_key_here"
   ```
   
   Or use the sidebar in the app to enter it manually.

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 🔑 Getting Your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key and add it to your configuration

## 📋 Requirements

- Python 3.11 or higher
- Google Gemini API key
- Internet connection

## 🎯 Usage

1. **Enter Destination**: Type a country, city, or region
2. **Set Duration**: Choose number of days (1-30)
3. **Add Preferences**: Describe what kind of trip you want
4. **Configure Settings**: Use the sidebar to:
   - Select AI model
   - Choose travel style
   - Set budget level
   - Enable/disable features
5. **Generate**: Click "Generate Travel Guide"
6. **Export**: Download your itinerary in JSON or text format

## 🏗️ Project Structure

```
AIT_ravel_and_Culture_Guide/
├── app.py                 # Main Streamlit application
├── countries.py           # Country database with travel information
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
├── .dockerignore         # Docker ignore file
└── README.md             # This file
```

## 🐳 Docker Commands

```bash
# Build the image
docker build -t travel-guide .

# Run the container
docker run -p 8501:8501 -e GEMINI_API_KEY=your_key travel-guide

# Using Docker Compose
docker-compose up          # Start
docker-compose down        # Stop
docker-compose logs        # View logs
docker-compose restart     # Restart
```

## 🎨 Features in Detail

### Travel Styles
- **Adventure**: Outdoor activities, hiking, sports
- **Relaxation**: Beaches, spas, peaceful locations
- **Cultural**: Museums, historical sites, local traditions
- **Food & Dining**: Local cuisine, food tours, markets
- **Nature**: National parks, wildlife, natural wonders
- **History**: Historical sites, monuments, heritage
- **Mixed**: Combination of all styles

### Budget Levels
- **Budget**: Affordable options, hostels, street food
- **Moderate**: Mid-range hotels, local restaurants
- **Luxury**: High-end accommodations, fine dining
- **Any**: Mix of all budget levels

### Export Formats
- **JSON**: Structured data for programmatic use
- **Text**: Plain text format for easy reading

## 🔧 Configuration

### Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key (required)

### Streamlit Secrets

Create `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "your_api_key_here"
```

## 🛠️ Development

### Adding New Countries

Edit `countries.py` and add country data in the following format:

```python
"Country Name": {
    "popular_places": ["Place 1", "Place 2"],
    "culture_etiquette": ["Tip 1", "Tip 2"],
    "traditional_food": ["Food 1", "Food 2"],
    "best_time_to_visit": "Month range",
    "budget_level": "Low/Moderate/High",
    "common_transport": "Transport options"
}
```

## 🐛 Troubleshooting

### API Key Issues
- Ensure your API key is valid and has not expired
- Check that the key has proper permissions
- Verify the key is correctly set in secrets or environment variables

### Docker Issues
- Make sure Docker is running
- Check port 8501 is not already in use
- Review Docker logs: `docker-compose logs`

### Import Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Activate your virtual environment
- Check Python version (3.11+)

## 📝 License

This project is open source and available for personal and commercial use.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues, questions, or suggestions, please open an issue on the repository.

## 🙏 Acknowledgments

- Powered by [Google Gemini AI](https://deepmind.google/technologies/gemini/)
- Built with [Streamlit](https://streamlit.io/)
- UI inspired by modern travel applications

---

**Made with ❤️ for travelers around the world**

