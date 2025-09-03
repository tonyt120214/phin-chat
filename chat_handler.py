"""
Chat handling logic for Phin AI Assistant
"""
import streamlit as st
import groq
import time
import threading
from utils import web_search, clean_response, stream_response, text_to_speech
from config import GROQ_API_KEY
from memory import conversation_memory

# Configure Groq client
client = groq.Groq(api_key=GROQ_API_KEY)

def handle_chat_input(prompt):
    """Handle new chat input and generate response"""
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # Check for golden misheard lyrics request
    if any(phrase in prompt.lower() for phrase in ["golden misheard lyrics", "misheard lyrics", "misheard song"]):
        lyrics = """I was a ghost i was a loan
(hah)
Double chin
(hah)
U So gay
(ahhhhhh)
given the throne 
eye didnt know
(hoe)
to be leaf
EYE was a queen that im meant to bee
i live 2 lie
try to paint both sides
EYe couldn't find my own face
caught a problem child
Cuz i got 2 wilds
BUTT 
now thats how im get in pain
with a cheese on stage"""
        st.session_state.messages.append({"role": "assistant", "content": lyrics})
        with st.chat_message("assistant"):
            st.write(lyrics)
        return

    # Get AI response
    try:
        # Create placeholder for thinking animation
        thinking_placeholder = st.empty()
        
        # Show thinking animation with immediate visibility
        thinking_html = """
        <div class="fish-container visible">
            <div class="fish-circle"></div>
            <div class="swimming-fish">🐠</div>
        </div>
        """
        thinking_placeholder.markdown(thinking_html, unsafe_allow_html=True)
        
        # Prepare context with memory
        context = ""
        
        # Add memory context
        memory_context = conversation_memory.get_memory_context()
        if memory_context:
            context += f"Previous conversation memory:\n{memory_context}\n\n"
        
        if st.session_state.uploaded_files_content:
            context += "Uploaded files content:\n"
            for filename, content in st.session_state.uploaded_files_content.items():
                context += f"\n--- {filename} ---\n{content[:2000]}...\n"
        
        # Web search if enabled
        search_sources = []
        if st.session_state.use_web_search:
            search_results = web_search(prompt)
            if search_results:
                context += "\nWeb search results:\n"
                for idx, result in enumerate(search_results, 1):
                    context += f"{idx}. {result['title']}: {result['body']}\n"
                    search_sources.append({"title": result['title'], "url": result.get('href', '#')})
                context += "\n"
        
        # Prepare messages with conversation history for memory
        messages = [{"role": "system", "content": st.session_state.custom_system_prompt}]
        
        # Add recent conversation history for context (last 10 messages)
        recent_messages = st.session_state.messages[-10:] if len(st.session_state.messages) > 10 else st.session_state.messages
        for msg in recent_messages:
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        # Add current user message with context
        if context:
            messages.append({"role": "user", "content": f"{context}\n\n{prompt}"})
        else:
            messages.append({"role": "user", "content": prompt})
        
        # Generate response (keep thinking animation until response starts)
        with st.chat_message("assistant"):
            if st.session_state.streaming_enabled:
                assistant_response = stream_response(
                    client, messages, st.session_state.selected_model,
                    st.session_state.temperature, st.session_state.max_tokens, thinking_placeholder
                )
            else:
                chat_completion = client.chat.completions.create(
                    messages=messages,
                    model=st.session_state.selected_model,
                    temperature=st.session_state.temperature,
                    max_tokens=st.session_state.max_tokens,
                )
                thinking_placeholder.empty()
                
                assistant_response = clean_response(chat_completion.choices[0].message.content)
                
                # Animate letter by letter for non-streaming too
                displayed_text = ""
                response_placeholder = st.empty()
                
                for i, char in enumerate(assistant_response):
                    displayed_text += char
                    response_placeholder.markdown(f'<div class="response-content">{displayed_text}</div>', unsafe_allow_html=True)
                    time.sleep(0.01)
                
                # Final display
                response_placeholder.markdown(f'<div class="response-content complete">{assistant_response}</div>', unsafe_allow_html=True)
            
            # Show search sources if available
            if search_sources:
                st.markdown("**Sources:**")
                for source in search_sources:
                    st.markdown(f"• [{source['title']}]({source['url']})")
        
        # Add to chat history
        if assistant_response:
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            
            # Analyze and store conversation in memory
            conversation_memory.analyze_and_store_conversation(st.session_state.messages)
            
            # Auto-save chat history
            from ui_components import auto_save_chat
            auto_save_chat()
            
            # Auto-play TTS if voice enabled (use full response but limit for performance)
            if st.session_state.voice_enabled:
                threading.Thread(target=text_to_speech, args=(assistant_response,)).start()

    except Exception as e:
        st.error(f"Error: {str(e)}")

def handle_voice_input():
    """Handle voice input if available"""
    if st.session_state.voice_enabled and 'voice_input' in st.session_state:
        if st.session_state.voice_input:
            st.rerun()
