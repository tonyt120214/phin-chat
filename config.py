"""
Configuration settings for Phin AI Assistant
"""

# Groq API Configuration
import os
GROQ_API_KEY = "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"

# Available AI Models
AVAILABLE_MODELS = {
    "llama-3.1-70b-versatile": "Llama 3.1 70B",
    "llama-3.1-8b-instant": "Llama 3.1 8B",
    "llama3-groq-70b-8192-tool-use-preview": "Llama 3 Groq 70B",
    "llama3-groq-8b-8192-tool-use-preview": "Llama 3 Groq 8B",
    "mixtral-8x7b-32768": "Mixtral 8x7B",
    "deepseek-r1-distill-llama-70b": "DeepSeek R1 Distill Llama 70B",
    "gemma-7b-it": "Gemma 7B"
}

# Default Settings
DEFAULT_SYSTEM_PROMPT = """You are Phin, a helpful AI assistant created by a developer. You are knowledgeable, friendly, and always try to provide accurate and helpful responses. You can help with a wide variety of tasks including answering questions, writing, coding, analysis, and creative tasks. Always be concise but thorough in your responses."""

DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 2048
DEFAULT_MODEL = "llama-3.1-70b-versatile"

# UI Configuration
PAGE_TITLE = "🐠 Phin AI Assistant"
PAGE_ICON = "🐠"
LAYOUT = "centered"
