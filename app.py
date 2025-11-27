import streamlit as st
import google.generativeai as genai
import json
from datetime import datetime
from typing import Optional, Dict, Any
import os

# Import countries data
try:
    from countries import COUNTRIES_DATA
except ImportError:
    COUNTRIES_DATA = {}

# Page configuration
st.set_page_config(
    page_title="AI Travel & Culture Guide",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 0.5rem;
        padding: 0.75rem;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'itinerary_data' not in st.session_state:
    st.session_state.itinerary_data = None
if 'country_info' not in st.session_state:
    st.session_state.country_info = None

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    
    # API Key Configuration
    st.subheader("🔑 API Configuration")
    api_key_source = st.radio(
        "API Key Source",
        ["Streamlit Secrets", "Manual Input"],
        help="Choose where to get your Gemini API key"
    )
    
    if api_key_source == "Manual Input":
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            help="Enter your Google Gemini API key"
        )
    else:
        try:
            api_key = st.secrets.get("GEMINI_API_KEY", "")
            if not api_key:
                st.warning("⚠️ API key not found in secrets. Please configure it.")
        except:
            api_key = ""
            st.warning("⚠️ Secrets not configured. Using manual input.")
    
    # Model Selection
    st.subheader("🤖 Model Selection")
    
    # Default models (fallback) - Prioritized by best for travel guide app
    default_models = [
        "gemini-2.5-flash",      # ⭐ BEST: Fast, efficient, perfect for travel guides
        "gemini-2.5-pro",        # Most powerful, detailed responses
        "gemini-2.0-flash",      # Stable alternative
        "gemini-2.5-flash-lite", # Very fast, basic quality
        "gemini-2.0-flash-001",  # Stable version
        "gemini-flash-latest",    # Always latest flash
        "gemini-1.5-flash",      # Older but reliable
        "gemini-1.5-pro",        # Older pro version
        "gemini-pro"             # Original stable model
    ]
    
    available_models = default_models.copy()
    
    # Try to get available models dynamically if API key is set
    if api_key:
        try:
            genai.configure(api_key=api_key)
            models = genai.list_models()
            found_models = []
            for model in models:
                if 'generateContent' in model.supported_generation_methods:
                    short_name = model.name.replace("models/", "")
                    if short_name not in found_models:
                        found_models.append(short_name)
            
            if found_models:
                # Prioritize newer models
                priority_models = [m for m in found_models if "2.5" in m or "2.0" in m]
                other_models = [m for m in found_models if m not in priority_models]
                available_models = priority_models + other_models[:10]  # Limit total
        except:
            pass  # Use default if check fails
    
    # Add a button to refresh available models
    if st.button("🔍 Refresh Available Models", help="Click to check which models your API key supports"):
        try:
            if api_key:
                genai.configure(api_key=api_key)
                models = genai.list_models()
                found_models = []
                for model in models:
                    if 'generateContent' in model.supported_generation_methods:
                        short_name = model.name.replace("models/", "")
                        if short_name not in found_models:
                            found_models.append(short_name)
                
                if found_models:
                    # Prioritize newer models
                    priority_models = [m for m in found_models if "2.5" in m or "2.0" in m]
                    other_models = [m for m in found_models if m not in priority_models]
                    available_models = priority_models + other_models[:10]
                    st.success(f"✅ Found {len(found_models)} available model(s)")
                    st.info(f"Recommended: {available_models[0] if available_models else 'N/A'}")
                else:
                    st.warning("⚠️ Could not fetch models. Using default list.")
            else:
                st.warning("⚠️ Please enter API key first to check available models.")
        except Exception as e:
            st.error(f"Error checking models: {str(e)}")
            st.info("Using default model list.")
    
    model_choice = st.selectbox(
        "Choose AI Model",
        available_models,
        index=0,  # Default to first model (usually newest)
        help=f"Select the Gemini model. {len(available_models)} model(s) available. Click 'Refresh' to update list."
    )
    
    # Travel Preferences
    st.subheader("🎯 Travel Preferences")
    travel_style = st.selectbox(
        "Travel Style",
        ["Adventure", "Relaxation", "Cultural", "Food & Dining", "Nature", "History", "Mixed"],
        help="What type of experience are you looking for?"
    )
    
    budget_level = st.selectbox(
        "Budget Level",
        ["Budget", "Moderate", "Luxury", "Any"],
        help="Your budget preference"
    )
    
    # Additional Options
    st.subheader("📋 Additional Options")
    include_photos = st.checkbox("Include photo suggestions", value=True)
    include_transport = st.checkbox("Include transport tips", value=True)
    include_safety = st.checkbox("Include safety tips", value=True)
    
    # About Section
    st.markdown("---")
    st.markdown("### 📖 About")
    st.info("""
    **AI Travel & Culture Guide** helps you create personalized 
    travel itineraries with cultural insights using Google's Gemini AI.
    """)

# Main content
st.markdown('<h1 class="main-header">🌍 AI Travel & Culture Guide</h1>', unsafe_allow_html=True)
st.markdown("### Create personalized travel itineraries with cultural insights")

# Country/Destination Input Section
col1, col2 = st.columns([2, 1])

with col1:
    destination = st.text_input(
        "📍 Where are you going?",
        placeholder="e.g., Japan, Paris, Kerala, Bali...",
        help="Enter a country, city, or region"
    )

with col2:
    days = st.number_input(
        "📅 Number of Days",
        min_value=1,
        max_value=30,
        value=3,
        help="How many days is your trip?"
    )

# Show country information if available
country_info = None
if destination and COUNTRIES_DATA:
    # Try to find matching country
    destination_lower = destination.strip().title()
    for country_name in COUNTRIES_DATA.keys():
        if destination_lower.lower() in country_name.lower() or country_name.lower() in destination_lower.lower():
            country_info = COUNTRIES_DATA[country_name]
            st.session_state.country_info = country_info
            break

if country_info:
    st.success(f"✅ Found information for {destination_lower}")
    with st.expander("📚 Quick Country Info", expanded=False):
        info_col1, info_col2, info_col3 = st.columns(3)
        with info_col1:
            st.metric("💰 Budget Level", country_info.get("budget_level", "N/A"))
        with info_col2:
            st.metric("⏰ Best Time", country_info.get("best_time_to_visit", "N/A")[:20] + "...")
        with info_col3:
            st.metric("🚗 Transport", country_info.get("common_transport", "N/A")[:20] + "...")
        
        if country_info.get("popular_places"):
            st.write("**Popular Places:**")
            st.write(", ".join(country_info["popular_places"][:3]))

# Preferences
preferences = st.text_area(
    "✍️ Tell us about your trip preferences",
    placeholder="e.g., I love trying local street food, visiting historical sites, and experiencing local festivals. I prefer a relaxed pace with time to explore markets and interact with locals...",
    height=100,
    help="Describe what kind of trip you want - be as detailed as you like!"
)

# Enhanced prompt builder
def build_enhanced_prompt(dest: str, days: int, prefs: str, travel_style: str, 
                         budget: str, country_info: Optional[Dict] = None,
                         include_photos: bool = True, include_transport: bool = True,
                         include_safety: bool = True) -> str:
    """Build a comprehensive prompt for the AI model."""
    
    prompt_parts = [
        f"Create a detailed {days}-day travel itinerary for {dest}.",
        f"Travel Style: {travel_style}",
        f"Budget Level: {budget}",
        f"Preferences: {prefs if prefs else 'Balanced trip with cultural experiences'}",
    ]
    
    # Add country-specific information if available
    if country_info:
        prompt_parts.append(f"\nCountry Information:")
        if country_info.get("popular_places"):
            prompt_parts.append(f"Popular places: {', '.join(country_info['popular_places'])}")
        if country_info.get("culture_etiquette"):
            prompt_parts.append(f"Cultural etiquette: {', '.join(country_info['culture_etiquette'])}")
        if country_info.get("traditional_food"):
            prompt_parts.append(f"Traditional foods: {', '.join(country_info['traditional_food'])}")
        if country_info.get("best_time_to_visit"):
            prompt_parts.append(f"Best time to visit: {country_info['best_time_to_visit']}")
    
    prompt_parts.extend([
        "\nRequirements:",
        "- For each day, provide a detailed itinerary with specific places to visit",
        "- Include cultural insights (history, traditions, etiquette, food significance) for each location",
        "- Add practical information: opening hours, entry fees (if applicable), and time needed",
        "- End each day with one interesting fun fact or trivia about the destination",
        "- Include meal suggestions with local cuisine recommendations",
        "- Write in a clear, engaging, and conversational tone",
        "- Use clear headings like 'Day 1', 'Day 2', etc.",
        "- Use bullet points for places and activities",
    ])
    
    if include_photos:
        prompt_parts.append("- Suggest specific photo spots and viewpoints")
    if include_transport:
        prompt_parts.append("- Include transportation tips between locations")
    if include_safety:
        prompt_parts.append("- Include safety tips and important cultural considerations")
    
    prompt_parts.append("\nFormat the response in a well-structured way that's easy to read and follow.")
    
    return "\n".join(prompt_parts)

# Gemini API call with error handling
def call_gemini(prompt: str, model_choice: str, api_key: str) -> tuple:
    """Call Gemini API with proper error handling."""
    if not api_key:
        return None, "API key is required. Please configure it in the sidebar."
    
    try:
        genai.configure(api_key=api_key)
        
        # Normalize model name - try with and without 'models/' prefix
        model_name = model_choice
        if not model_choice.startswith("models/"):
            model_name = f"models/{model_choice}"
        
        model = genai.GenerativeModel(model_name)
        
        # Configure generation parameters
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
        }
        
        chat = model.start_chat(history=[])
        response = chat.send_message(prompt, generation_config=generation_config)
        return response.text.strip(), None
    except Exception as e:
        error_msg = str(e)
        # Provide helpful error message for model issues
        if "model" in error_msg.lower() or "not found" in error_msg.lower():
            return None, f"Model '{model_choice}' not available. Try 'gemini-1.5-flash' or 'gemini-1.5-pro'. Error: {error_msg}"
        return None, f"Error calling Gemini API: {error_msg}"

# Parse itinerary output
def parse_itinerary(output: str) -> Dict[str, Any]:
    """Parse the AI output into structured data."""
    lines = [l.strip() for l in output.split("\n") if l.strip()]
    day_blocks = []
    current = []
    
    for line in lines:
        if line.lower().startswith(("day ", "day-", "day:")):
            if current:
                day_blocks.append(current)
            current = [line]
        else:
            current.append(line)
    if current:
        day_blocks.append(current)
    
    # Extract cultural insights and trivia
    cultural_keywords = ("history", "heritage", "tradition", "etiquette", "festival", 
                       "cuisine", "food", "custom", "ritual", "culture", "cultural")
    trivia_keywords = ("fact", "trivia", "interesting", "did you know", "fun fact")
    
    cultural_insights = []
    trivia_facts = []
    
    for block in day_blocks:
        day_cultural = []
        day_trivia = []
        for line in block:
            line_lower = line.lower()
            if any(k in line_lower for k in cultural_keywords):
                day_cultural.append(line)
            if any(k in line_lower for k in trivia_keywords):
                day_trivia.append(line)
        cultural_insights.append(day_cultural)
        trivia_facts.append(day_trivia)
    
    return {
        "full_output": output,
        "day_blocks": day_blocks,
        "cultural_insights": cultural_insights,
        "trivia_facts": trivia_facts,
        "destination": destination,
        "days": days,
        "generated_at": datetime.now().isoformat()
    }

# Export functions
def export_json(data: Dict) -> str:
    """Export itinerary as JSON."""
    return json.dumps(data, indent=2, ensure_ascii=False)

def export_text(data: Dict) -> str:
    """Export itinerary as plain text."""
    text = f"Travel Itinerary for {data['destination']}\n"
    text += f"Generated on: {data['generated_at']}\n"
    text += "=" * 50 + "\n\n"
    text += data['full_output']
    return text

# Generate button
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
with col_btn2:
    generate_btn = st.button("🚀 Generate Travel Guide", use_container_width=True)

if generate_btn:
    if not destination:
        st.error("❌ Please enter a destination.")
    elif not api_key:
        st.error("❌ Please configure your Gemini API key in the sidebar.")
    else:
        with st.spinner("✨ Crafting your personalized travel guide... This may take a moment."):
            try:
                prompt = build_enhanced_prompt(
                    destination, days, preferences, travel_style, 
                    budget_level, country_info, include_photos, 
                    include_transport, include_safety
                )
                
                output, error = call_gemini(prompt, model_choice, api_key)
                
                if error:
                    st.error(f"❌ {error}")
                elif not output:
                    st.warning("⚠️ Empty response. Please try again or adjust your preferences.")
                else:
                    st.success("✅ Guide generated successfully!")
                    
                    # Parse and store itinerary
                    itinerary_data = parse_itinerary(output)
                    st.session_state.itinerary_data = itinerary_data
                    
                    # Display metrics
                    st.markdown("---")
                    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                    with metric_col1:
                        st.metric("📍 Destination", destination)
                    with metric_col2:
                        st.metric("📅 Days", days)
                    with metric_col3:
                        st.metric("🎯 Style", travel_style)
                    with metric_col4:
                        st.metric("💰 Budget", budget_level)
                    
                    st.markdown("---")
                    
                    # Export buttons
                    export_col1, export_col2, export_col3 = st.columns(3)
                    with export_col1:
                        st.download_button(
                            "📥 Download as JSON",
                            export_json(itinerary_data),
                            file_name=f"itinerary_{destination.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.json",
                            mime="application/json"
                        )
                    with export_col2:
                        st.download_button(
                            "📄 Download as Text",
                            export_text(itinerary_data),
                            file_name=f"itinerary_{destination.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                            mime="text/plain"
                        )
                    with export_col3:
                        if st.button("🔄 Regenerate", use_container_width=True):
                            st.rerun()
                    
                    st.markdown("---")
                    
                    # Tabs for different views
                    tab1, tab2, tab3, tab4 = st.tabs(["📋 Full Itinerary", "🎭 Cultural Insights", "💡 Trivia & Facts", "📊 Summary"])
                    
                    with tab1:
                        st.subheader(f"🗺️ {days}-Day Itinerary for {destination}")
                        for i, block in enumerate(itinerary_data["day_blocks"], start=1):
                            with st.container():
                                st.markdown(f"### Day {i}")
                                for line in block:
                                    if not line.lower().startswith(("day ", "day-", "day:")):
                                        st.markdown(f"• {line}" if not line.startswith("#") else line)
                                st.markdown("---")
                    
                    with tab2:
                        st.subheader("🎭 Cultural Insights & Etiquette")
                        for i, (insights, block) in enumerate(zip(itinerary_data["cultural_insights"], itinerary_data["day_blocks"]), start=1):
                            if insights:
                                st.markdown(f"### Day {i}")
                                for insight in insights:
                                    st.info(f"💡 {insight}")
                                st.markdown("---")
                    
                    with tab3:
                        st.subheader("💡 Fun Facts & Trivia")
                        all_trivia = []
                        for trivia_list in itinerary_data["trivia_facts"]:
                            all_trivia.extend(trivia_list)
                        
                        if all_trivia:
                            for trivia in all_trivia:
                                st.success(f"✨ {trivia}")
                        else:
                            st.info("No trivia found in the generated itinerary.")
                    
                    with tab4:
                        st.subheader("📊 Itinerary Summary")
                        summary_col1, summary_col2 = st.columns(2)
                        with summary_col1:
                            st.json({
                                "Destination": destination,
                                "Duration": f"{days} days",
                                "Travel Style": travel_style,
                                "Budget": budget_level,
                                "Generated": itinerary_data["generated_at"]
                            })
                        with summary_col2:
                            st.metric("Total Days", days)
                            st.metric("Sections", len(itinerary_data["day_blocks"]))
                            st.metric("Cultural Insights", sum(len(c) for c in itinerary_data["cultural_insights"]))
                    
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")
                st.exception(e)

# Display previous itinerary if available
if st.session_state.itinerary_data and not generate_btn:
    st.info("💡 You have a previously generated itinerary. Click 'Generate Travel Guide' to create a new one.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p>🌍 Powered by Google Gemini AI | Made with ❤️ for travelers</p>
        <p style='font-size: 0.8rem;'>Generate personalized travel guides with cultural insights</p>
    </div>
    """,
    unsafe_allow_html=True
)
