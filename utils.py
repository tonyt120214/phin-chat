"""
Utility functions for Phin AI Assistant
"""
import streamlit as st
import speech_recognition as sr
import pyttsx3
import pyperclip
import threading
import time
from duckduckgo_search import DDGS
from deep_translator import GoogleTranslator

def copy_to_clipboard(text):
    """Copy text to clipboard"""
    try:
        pyperclip.copy(text)
        st.success("Copied to clipboard!")
    except Exception as e:
        st.error(f"Copy failed: {str(e)}")

def speech_to_text():
    """Convert speech to text using microphone"""
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("Listening... Speak now!")
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
        
        text = r.recognize_google(audio)
        return text
    except sr.WaitTimeoutError:
        st.warning("No speech detected")
        return None
    except Exception as e:
        st.error(f"Speech recognition error: {str(e)}")
        return None

def text_to_speech(text):
    """Convert text to speech"""
    try:
        engine = pyttsx3.init()
        
        # Get available voices and set to a more natural one if available
        voices = engine.getProperty('voices')
        if voices:
            # Try to find a female voice or more natural sounding voice
            for voice in voices:
                if 'female' in voice.name.lower() or 'samantha' in voice.name.lower() or 'alex' in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break
        
        # Set natural speech parameters
        engine.setProperty('rate', 180)  # Slightly faster, more natural
        engine.setProperty('volume', 0.9)
        
        # Clean text for better speech but keep full response
        clean_text = text.replace('*', '').replace('#', '').replace('`', '')
        clean_text = clean_text.replace('**', '').replace('_', '')  # Remove more markdown
        
        # Split into sentences and read all of them
        sentences = clean_text.split('. ')
        for sentence in sentences:
            if sentence.strip():
                engine.say(sentence.strip())
        
        engine.runAndWait()
    except Exception as e:
        st.error(f"TTS Error: {str(e)}")

def web_search(query, num_results=3):
    """Perform web search using DuckDuckGo with English results only"""
    try:
        with DDGS() as ddgs:
            # Force English results only
            results = list(ddgs.text(f"{query} lang:en", region='us-en', max_results=num_results))
            # Filter out non-English results
            english_results = []
            for result in results:
                title = result.get('title', '')
                body = result.get('body', '')
                # Skip if title or body contains Chinese characters
                if not any('\u4e00' <= char <= '\u9fff' for char in title + body):
                    english_results.append(result)
            return english_results[:num_results]
    except Exception as e:
        st.error(f"Search error: {str(e)}")
        return []

def clean_response(response):
    """Clean and format AI response"""
    # Remove any thinking sections (more thorough cleaning)
    while "<think>" in response and "</think>" in response:
        start = response.find("<think>")
        end = response.find("</think>") + len("</think>")
        response = response[:start] + response[end:]
    
    # Remove any remaining thinking patterns
    import re
    response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
    response = re.sub(r'\*\*thinking\*\*.*?\*\*end thinking\*\*', '', response, flags=re.DOTALL | re.IGNORECASE)
    
    # Clean up extra whitespace
    response = re.sub(r'\n\s*\n\s*\n', '\n\n', response)
    response = response.strip()
    
    return response

def get_supported_languages():
    """Get supported languages for translation"""
    return {
        'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
        'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian', 'nl': 'Dutch',
        'ja': 'Japanese', 'ko': 'Korean', 'zh-cn': 'Chinese (Simplified)',
        'zh-tw': 'Chinese (Traditional)', 'ar': 'Arabic', 'hi': 'Hindi',
        'bn': 'Bengali', 'pa': 'Punjabi', 'te': 'Telugu', 'ta': 'Tamil',
        'vi': 'Vietnamese', 'th': 'Thai', 'tr': 'Turkish', 'pl': 'Polish',
        'uk': 'Ukrainian', 'cs': 'Czech', 'sv': 'Swedish', 'da': 'Danish',
        'fi': 'Finnish', 'el': 'Greek', 'he': 'Hebrew', 'id': 'Indonesian',
        'ms': 'Malay', 'fa': 'Persian'
    }

def translate_text(text, target_lang):
    """Translate text to target language"""
    if target_lang == 'en':
        return text
    try:
        translator = GoogleTranslator(source='en', target=target_lang)
        return translator.translate(text)
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return text

def stream_response(client, messages, model, temperature, max_tokens, thinking_placeholder):
    """Stream AI response with letter-by-letter typewriter effect"""
    try:
        response = client.chat.completions.create(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True
        )
        
        full_response = ""
        placeholder = st.empty()
        first_chunk = True
        
        # Collect full response first
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                if first_chunk:
                    thinking_placeholder.empty()
                    first_chunk = False
                
                full_response += chunk.choices[0].delta.content
        
        # Now animate letter by letter
        clean_final = clean_response(full_response)
        displayed_text = ""
        
        for i, char in enumerate(clean_final):
            displayed_text += char
            placeholder.markdown(f'<div class="response-content">{displayed_text}</div>', unsafe_allow_html=True)
            time.sleep(0.01)
        
        # Final display
        placeholder.markdown(f'<div class="response-content complete">{clean_final}</div>', unsafe_allow_html=True)
        return clean_final
    except Exception as e:
        st.error(f"Streaming error: {str(e)}")
        return None
