# 🐟 Phin AI Assistant

A modern AI chat assistant built with Streamlit, featuring conversation memory, chat history, and a beautiful dark theme.

## Features

- 🤖 **AI Chat** - Powered by Groq API with multiple model options
- 🧠 **Memory System** - Remembers user preferences and conversation context
- 💬 **Chat History** - Auto-saves and loads previous conversations
- 🔍 **Web Search** - Optional web search integration
- 🎨 **Dark Theme** - Beautiful, modern UI with fish animations
- 🎤 **Voice Features** - Text-to-speech and speech recognition (optional)
- ⚡ **Streaming** - Real-time response streaming

## 👥 Developers

- **[Trye](https://github.com/ltrye)** (Leader)
- **[Tony](https://github.com/tonyt120214)** (Owner)

## Quick Start

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd phin-ai-assistant
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure API Keys
Create a `.env` file:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Run the App
```bash
streamlit run phin_main.py
```

## Deployment Options

### Streamlit Cloud (Recommended)
1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Add your API keys in the secrets section

### Heroku
```bash
echo "web: streamlit run phin_main.py --server.port=$PORT --server.address=0.0.0.0" > Procfile
git add Procfile
git commit -m "Add Procfile for Heroku"
# Deploy to Heroku
```

### Railway
```bash
# Add railway.json
echo '{"build": {"builder": "NIXPACKS"}, "deploy": {"startCommand": "streamlit run phin_main.py --server.port=$PORT --server.address=0.0.0.0"}}' > railway.json
```

## Configuration

Edit `config.py` to customize:
- Available AI models
- Default system prompt
- UI settings
- API endpoints

## File Structure

```
phin-ai-assistant/
├── phin_main.py          # Main application
├── chat_handler.py       # Chat logic and AI integration
├── ui_components.py      # UI components and rendering
├── memory.py            # Conversation memory system
├── styles.py            # CSS styling and themes
├── utils.py             # Utility functions
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Memory System

The app automatically learns from conversations:
- **User Preferences** - "I like...", "I prefer..."
- **Personal Info** - "My name is...", "I work at..."
- **Conversation Topics** - Recent discussion themes
- **Context** - Maintains conversation continuity

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - feel free to use and modify!

## Support

For issues or questions, please open a GitHub issue.
