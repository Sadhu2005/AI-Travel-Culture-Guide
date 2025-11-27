"""
Optional LangChain version of the app.
This version uses LangChain for better prompt management and structured output.
Install langchain and langchain-google-genai to use this version.
"""

import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
import json
from datetime import datetime
from typing import Optional, Dict, Any

# Import countries data
try:
    from countries import COUNTRIES_DATA
except ImportError:
    COUNTRIES_DATA = {}

# Page configuration
st.set_page_config(
    page_title="AI Travel & Culture Guide (LangChain)",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'itinerary_data' not in st.session_state:
    st.session_state.itinerary_data = None

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    
    api_key_source = st.radio("API Key Source", ["Streamlit Secrets", "Manual Input"])
    
    if api_key_source == "Manual Input":
        api_key = st.text_input("Gemini API Key", type="password")
    else:
        try:
            api_key = st.secrets.get("GEMINI_API_KEY", "")
        except:
            api_key = ""
    
    model_choice = st.selectbox(
        "Choose AI Model",
        ["gemini-pro", "gemini-1.5-pro", "gemini-1.5-flash"],
        index=0
    )
    
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
    max_tokens = st.slider("Max Tokens", 1000, 8000, 4000, 500)

# Main content
st.title("🌍 AI Travel & Culture Guide (LangChain Version)")

destination = st.text_input("📍 Where are you going?", placeholder="e.g., Japan, Paris, Kerala")
days = st.number_input("📅 Number of Days", min_value=1, max_value=30, value=3)
preferences = st.text_area("✍️ Trip Preferences", placeholder="Describe your ideal trip...")

# LangChain prompt template
prompt_template = ChatPromptTemplate.from_messages([
    SystemMessage(content="You are an expert travel guide specializing in creating detailed, culturally-rich itineraries."),
    HumanMessage(content="""Create a {days}-day travel itinerary for {destination}.
    
    Preferences: {preferences}
    
    Include:
    - Day-by-day detailed itinerary
    - Cultural insights and etiquette
    - Local food recommendations
    - Fun facts and trivia
    - Practical tips
    
    Format with clear headings and bullet points.""")
])

def call_langchain_llm(prompt: str, api_key: str, model: str, temp: float, max_tok: int):
    """Call Gemini using LangChain."""
    if not api_key:
        return None, "API key required"
    
    try:
        llm = ChatGoogleGenerativeAI(
            model=model,
            google_api_key=api_key,
            temperature=temp,
            max_output_tokens=max_tok
        )
        
        messages = prompt_template.format_messages(
            days=days,
            destination=destination,
            preferences=preferences
        )
        
        response = llm.invoke(messages)
        return response.content, None
    except Exception as e:
        return None, str(e)

if st.button("🚀 Generate with LangChain"):
    if not destination:
        st.error("Please enter a destination")
    elif not api_key:
        st.error("Please configure API key")
    else:
        with st.spinner("Generating..."):
            output, error = call_langchain_llm(
                preferences, api_key, model_choice, temperature, max_tokens
            )
            
            if error:
                st.error(f"Error: {error}")
            else:
                st.success("Generated!")
                st.markdown(output)

st.info("💡 This is the LangChain version. Install langchain and langchain-google-genai to use it.")

