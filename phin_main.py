"""
Phin AI Assistant - Main Application
Clean and minimal main file
"""
import streamlit as st
from styles import get_theme_css, get_animation_css
from ui_components import (
    render_sidebar, render_chat_controls,
    render_voice_input, render_chat_messages, auto_save_chat
)
from chat_handler import handle_chat_input, handle_voice_input
from config import PAGE_TITLE, PAGE_ICON, LAYOUT, AVAILABLE_MODELS, DEFAULT_SYSTEM_PROMPT, GROQ_API_KEY
import os

# Debug: Print environment variables and API key status
print("Environment Variables:", os.environ)
print("GROQ_API_KEY loaded:", "YES" if GROQ_API_KEY else "NO")

# Initialize session state
def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        'use_web_search': True,
        'selected_model': 'deepseek-r1-distill-llama-70b',
        'temperature': 0.7,
        'max_tokens': 2048,
        'custom_system_prompt': DEFAULT_SYSTEM_PROMPT,
        'uploaded_files_content': {},
        'chat_ratings': {},
        'voice_enabled': False,
        'messages': [],
        'selected_language': 'en',
        'streaming_enabled': True
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def main():
    """Main application function"""
    # Page configuration
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout=LAYOUT
    )
    
    # Initialize session state
    init_session_state()
    
    # Apply styling
    st.markdown(get_theme_css(), unsafe_allow_html=True)
    st.markdown(get_animation_css(), unsafe_allow_html=True)
    
    # Force English language
    st.session_state.selected_language = 'en'
    
    # Render UI components
    render_sidebar()
    
    # Main content area
    st.title("🐟 Phin AI Assistant")
    st.caption("Your intelligent AI companion")
    
    # Chat controls
    render_chat_controls()
    
    # Voice input
    render_voice_input()
    
    # Display chat messages
    render_chat_messages()
    
    # Auto-save chat after rendering messages (only if messages exist)
    if st.session_state.messages:
        auto_save_chat()
    
    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        handle_chat_input(prompt)
    
    # Handle voice input
    handle_voice_input()

if __name__ == "__main__":
    main()
