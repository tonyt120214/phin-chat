"""
UI Components for Phin AI Assistant
"""
import streamlit as st
import os
import json
import threading
from datetime import datetime
from utils import copy_to_clipboard, speech_to_text, text_to_speech
from config import AVAILABLE_MODELS

def render_sidebar():
    """Render the sidebar with all settings"""
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Model selection
        selected_model_name = st.selectbox(
            "🤖 AI Model",
            options=list(AVAILABLE_MODELS.values()),
            index=list(AVAILABLE_MODELS.keys()).index(st.session_state.selected_model)
        )
        st.session_state.selected_model = [k for k, v in AVAILABLE_MODELS.items() if v == selected_model_name][0]
        
        # Model parameters
        st.session_state.temperature = st.slider("🌡️ Temperature", 0.0, 2.0, st.session_state.temperature, 0.1)
        st.session_state.max_tokens = st.slider("📝 Max Tokens", 256, 4096, st.session_state.max_tokens, 256)
        
        # Features
        st.session_state.use_web_search = st.toggle("🔍 Web Search", value=st.session_state.use_web_search)
        st.session_state.streaming_enabled = st.toggle("⚡ Stream Responses", value=st.session_state.streaming_enabled)
        st.session_state.voice_enabled = st.toggle("🎤 Voice Features", value=st.session_state.voice_enabled)
        
        # Language selection (force English)
        st.session_state.selected_language = 'en'
        st.write("🌍 Language: English (Fixed)")
        
        st.divider()
        
        # Chat History
        st.subheader("💬 Chat History")
        
        # New Chat button
        if st.button("➕ New Chat", use_container_width=True):
            create_new_chat()
        
        render_chat_history_sidebar()
        
        st.divider()
        
        # Memory Management
        st.subheader("🧠 Memory")
        if st.button("Clear Memory", use_container_width=True):
            from memory import conversation_memory
            conversation_memory.memory_data = conversation_memory.get_default_memory()
            conversation_memory.save_memory()
            st.success("Memory cleared!")
        
        st.divider()
        
        # Custom system prompt
        st.subheader("🎭 Custom Personality")
        st.session_state.custom_system_prompt = st.text_area(
            "System Prompt",
            value=st.session_state.custom_system_prompt,
            height=100
        )
        
        st.divider()
        
        # Credits
        st.subheader("📜 Credits")
        st.markdown("""
        **🐠 Phin AI Assistant**  
        A modern AI chat assistant built with Streamlit
        
        **Built with:**  
        • Streamlit  
        • Groq API  
        • Python  
        
        **Features:**  
        • AI Chat with multiple models  
        • Conversation memory  
        • Chat history  
        • Web search integration  
        • Voice features  
        • Beautiful dark theme  
        
        **Developer:**  
        Created with ❤️ for intelligent conversations
        """)
        
        # Version info
        st.caption("Version 1.0.0")

def render_chat_controls():
    """Render chat management controls"""
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💾 Save Chat"):
            filename = save_chat_history()
            if filename:
                st.success(f"Saved: {filename}")
    
    with col2:
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.session_state.chat_ratings = {}
            st.rerun()
    
    # Load chat
    chat_files = get_chat_files()
    if chat_files:
        selected_file = st.selectbox("📂 Load Chat", [""] + chat_files)
        if selected_file and st.button("📖 Load"):
            load_chat_history(f"chat_history/{selected_file}")
            st.rerun()
    
    # Export chat
    if st.session_state.messages and st.button("📤 Export as Text"):
        text_content = export_chat_as_text()
        if text_content:
            st.download_button(
                "⬇️ Download",
                text_content,
                file_name=f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

def render_voice_input():
    """Render voice input section"""
    if st.session_state.voice_enabled:
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🎤 Voice Input"):
                voice_text = speech_to_text()
                if voice_text:
                    st.session_state.voice_input = voice_text

def render_chat_messages():
    """Render chat message history"""
    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            # Always display in English - no translation
            st.markdown(f'<div class="response-content">{message["content"]}</div>', unsafe_allow_html=True)
            
            # Add copy button and rating for assistant messages
            if message["role"] == "assistant":
                col1, col2, col3, col4 = st.columns([1, 1, 1, 3])
                
                with col1:
                    if st.button("📋", key=f"copy_{i}"):
                        copy_to_clipboard(message["content"])
                
                with col2:
                    if st.session_state.voice_enabled and st.button("🔊", key=f"speak_{i}"):
                        threading.Thread(target=text_to_speech, args=(message["content"],)).start()
                
                with col3:
                    if st.button("Good", key=f"like_{i}"):
                        st.session_state.chat_ratings[i] = "like"
                        st.rerun()
                
                with col4:
                    if st.button("Poor", key=f"dislike_{i}"):
                        st.session_state.chat_ratings[i] = "dislike"
                        st.rerun()

# Chat history management functions
def save_chat_history():
    """Save current chat history to file"""
    if not st.session_state.messages:
        return None
    
    os.makedirs("chat-history", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"chat_{timestamp}.json"
    filepath = f"chat-history/{filename}"
    
    try:
        with open(filepath, 'w') as f:
            json.dump({
                'messages': st.session_state.messages,
                'ratings': st.session_state.chat_ratings,
                'timestamp': timestamp
            }, f, indent=2)
        return filename
    except Exception as e:
        st.error(f"Save failed: {str(e)}")
        return None

def load_chat_history(filepath):
    """Load chat history from file"""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        st.session_state.messages = data.get('messages', [])
        st.session_state.chat_ratings = data.get('ratings', {})
        st.success("Chat loaded successfully!")
    except Exception as e:
        st.error(f"Load failed: {str(e)}")

def get_chat_files():
    """Get list of saved chat files"""
    if not os.path.exists("chat-history"):
        return []
    try:
        files = [f for f in os.listdir("chat-history") if f.endswith('.json')]
        return sorted(files, reverse=True)
    except:
        return []

def export_chat_as_text():
    """Export chat as plain text"""
    if not st.session_state.messages:
        return None
    
    text_content = f"Chat Export - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    text_content += "=" * 50 + "\n\n"
    
    for message in st.session_state.messages:
        role = "You" if message["role"] == "user" else "Phin"
        text_content += f"{role}: {message['content']}\n\n"
    
    return text_content

def render_chat_history_sidebar():
    """Render chat history in sidebar"""
    chat_files = get_chat_files()
    
    if chat_files:
        st.write("Recent Chats:")
        for chat_file in chat_files[:10]:  # Show last 10 chats
            # Extract timestamp from filename for display
            try:
                timestamp = chat_file.replace('chat_', '').replace('.json', '')
                display_name = f"💬 {timestamp[:8]} {timestamp[9:11]}:{timestamp[11:13]}"
            except:
                display_name = f"💬 {chat_file}"
            
            if st.button(display_name, key=f"load_{chat_file}"):
                load_chat_history(f"chat-history/{chat_file}")
    else:
        st.write("No saved chats yet")

def auto_save_chat():
    """Automatically save chat when new message is added"""
    if len(st.session_state.messages) > 0:
        # Only save if we have messages and it's not already saved
        if 'last_saved_count' not in st.session_state:
            st.session_state.last_saved_count = 0
        
        current_count = len(st.session_state.messages)
        if current_count > st.session_state.last_saved_count:
            # Use threading to prevent blocking and loops
            threading.Thread(target=save_chat_history, daemon=True).start()
            st.session_state.last_saved_count = current_count

def create_new_chat():
    """Create a new chat by clearing current messages and resetting state"""
    # Save current chat if it has messages
    if st.session_state.messages:
        save_chat_history()
    
    # Clear current chat
    st.session_state.messages = []
    st.session_state.chat_ratings = {}
    st.session_state.last_saved_count = 0
    
    # Clear any uploaded file content
    if 'uploaded_files_content' in st.session_state:
        st.session_state.uploaded_files_content = {}
    
    st.success("New chat created!")
