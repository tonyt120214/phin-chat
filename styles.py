"""
CSS and styling for Phin AI Assistant
"""

def get_theme_css():
    """Get CSS for dark theme"""
    return """
    <style>
    .stApp {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    
    .stChatMessage {
        background-color: transparent;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .stTextInput > div > div > input {
        background-color: #2d2d2d;
        color: #ffffff;
        border: 1px solid #444;
    }
    
    .stSelectbox > div > div > div {
        background-color: #2d2d2d;
        color: #ffffff;
    }
    
    .stSlider > div > div > div > div {
        background-color: #1E88E5;
    }
    
    .stButton > button {
        background-color: #1a1a1a;
        color: #888;
        border: 1px solid #333;
        border-radius: 4px;
        padding: 0.3rem 0.8rem;
        font-size: 12px;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background-color: #2d2d2d;
        color: #fff;
        border-color: #555;
    }
    
    .stSidebar {
        background-color: #0f0f0f;
    }
    
    .stSidebar .stSelectbox > div > div > div {
        background-color: #2d2d2d;
    }
    </style>
    """

def get_animation_css():
    """Get CSS for animations"""
    return """
    <style>
    .copy-button {
        background: #1E88E5;
        color: white;
        border: none;
        padding: 5px 10px;
        border-radius: 3px;
        cursor: pointer;
        font-size: 12px;
        margin: 5px 0;
    }
    .copy-button:hover {
        background: #1976D2;
    }
    .rating-button {
        background: white;
        color: #333;
        border: 1px solid #ddd;
        padding: 5px 10px;
        border-radius: 15px;
        cursor: pointer;
        font-size: 14px;
    }
    .rating-button:hover {
        background: #f0f0f0;
    }
    .rating-button.selected {
        background: #1E88E5;
        color: white;
        border-color: #1E88E5;
    }

    @keyframes swim {
        0% { 
            transform: translate(-50%, -50%) rotate(0deg);
        }
        25% {
            transform: translate(-25%, -75%) rotate(15deg);
        }
        50% {
            transform: translate(0%, -50%) rotate(-15deg);
        }
        75% {
            transform: translate(-75%, -25%) rotate(15deg);
        }
        100% {
            transform: translate(-50%, -50%) rotate(0deg);
        }
    }

    @keyframes fishFade {
        0% {
            transform: translate(-50%, -50%) scale(1);
            opacity: 0.2;
        }
        50% {
            transform: translate(-50%, -50%) scale(1.2);
            opacity: 0.4;
        }
        100% {
            transform: translate(-50%, -50%) scale(1);
            opacity: 0.2;
        }
    }

    @keyframes pulse {
        0% {
            transform: translate(-50%, -50%) scale(1);
            opacity: 0.2;
        }
        50% {
            transform: translate(-50%, -50%) scale(1.2);
            opacity: 0.4;
        }
        100% {
            transform: translate(-50%, -50%) scale(1);
            opacity: 0.2;
        }
    }

    @keyframes typewriter {
        0% { 
            width: 0;
            opacity: 0;
        }
        1% {
            opacity: 1;
        }
        100% { 
            width: 100%;
            opacity: 1;
        }
    }

    @keyframes blink {
        0%, 50% { border-color: #1E88E5; }
        51%, 100% { border-color: transparent; }
    }

    .fish-container {
        position: fixed;
        top: 50%;
        left: 50%;
        z-index: 9999;
        opacity: 0;
        visibility: hidden;
        transition: opacity 0.8s ease-in-out, visibility 0.8s ease-in-out;
    }

    .fish-circle {
        position: absolute;
        top: 50%;
        left: 50%;
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: #1a1a1a;
        border: 2px solid rgba(30, 136, 229, 0.3);
        animation: pulse 2s ease-in-out infinite;
    }

    .swimming-fish {
        position: absolute;
        top: 50%;
        left: 50%;
        font-size: 45px;
        transform: translate(-50%, -50%);
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
        animation: fishFade 2s ease-in-out infinite;
    }

    .fish-container.visible {
        opacity: 1;
        visibility: visible;
        animation: swim 3s ease-in-out infinite;
    }

    .response-content {
        white-space: normal;
        font-family: inherit;
    }

    .response-content.fade-in {
        animation: none;
    }

    .response-content.complete {
        white-space: normal;
        font-family: inherit;
    }

    @keyframes fadeIn {
        0% {
            opacity: 0;
            transform: translateY(10px);
        }
        100% {
            opacity: 1;
            transform: translateY(0);
        }
    }
    </style>
    """
