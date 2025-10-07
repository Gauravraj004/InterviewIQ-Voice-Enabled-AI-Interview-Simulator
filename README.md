# 🎯 InterviewIQ - AI-Powered Interview Practice Platform

> An intelligent interview preparation system that conducts realistic mock interviews with voice interaction, resume analysis, and personalized questioning using AI.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)](https://flask.palletsprojects.com/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3.18-orange.svg)](https://www.langchain.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Table of Contents

- [Features](#-features)
- [Demo](#-demo)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [API Endpoints](#-api-endpoints)
- [How It Works](#-how-it-works)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

---

## ✨ Features

### 🎤 Voice Interaction
- **Browser-based audio recording** using Web Audio API
- **Real-time transcription** with Google Speech Recognition
- **No external dependencies** - WAV encoding directly in browser
- **Transcription-to-text field** - Review and edit before sending

### 🤖 AI-Powered Interviews
- **Natural conversation flow** - Acts like a real interviewer
- **Context-aware questioning** - Remembers conversation history
- **Adaptive responses** - Adjusts difficulty based on answers
- **HuggingFace LLM integration** - Uses `openai/gpt-oss-120b` model

### 📄 Resume Analysis (RAG)
- **PDF upload and processing** - Extracts text from resume
- **Vector embeddings** - Uses Sentence Transformers
- **Semantic search** - Finds relevant resume sections
- **Astra DB storage** - Cloud-native vector database
- **Personalized questions** - Based on your experience

### 🎨 Modern UI/UX
- **Dark/Light theme toggle** - Persistent across sessions
- **Message alignment** - You (right) / AI (left)
- **Responsive design** - Works on desktop and mobile
- **Auto-scroll chat** - Smooth message flow
- **Clean animations** - Professional look and feel

### 🔒 Secure & Private
- **No local file storage** - Everything in-memory or cloud
- **Session-based isolation** - Each user gets own context
- **API key via UI** - No hardcoded credentials
- **Auto-cleanup on restart** - Fresh start every time

---

## 🎬 Demo

### Screenshot
![InterviewIQ Interface](https://via.placeholder.com/800x500?text=InterviewIQ+Interface)

### Quick Start
```bash
# Clone the repository
git clone https://github.com/yourusername/interviewiq.git
cd interviewiq

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your credentials

# Run the application
python main.py
```

Visit `http://127.0.0.1:5000` and start practicing!

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Browser                              │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐    │
│  │ Microphone  │→ │ Web Audio API│→ │  WAV Encoder    │    │
│  └─────────────┘  └──────────────┘  └─────────────────┘    │
│                           ↓                                  │
│                    ┌──────────────┐                          │
│                    │  chat.js     │                          │
│                    │  (Frontend)  │                          │
│                    └──────────────┘                          │
└───────────────────────────┬──────────────────────────────────┘
                            │ HTTP/JSON
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                      Flask Server                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                    main.py                            │   │
│  │  ┌─────────┐  ┌─────────┐  ┌────────┐  ┌─────────┐ │   │
│  │  │ /speech │  │ /chat   │  │ /upload│  │ /set_api│ │   │
│  │  └────┬────┘  └────┬────┘  └───┬────┘  └────┬────┘ │   │
│  └───────┼────────────┼───────────┼────────────┼──────┘   │
│          │            │           │            │            │
│    ┌─────▼─────┐ ┌───▼────────┐ │      ┌─────▼──────┐     │
│    │transcribe │ │ AI_model   │ │      │  Session   │     │
│    │    .py    │ │   .py      │ │      │  Storage   │     │
│    └─────┬─────┘ └───┬────────┘ │      └────────────┘     │
│          │           │           │                          │
└──────────┼───────────┼───────────┼──────────────────────────┘
           │           │           │
           ↓           ↓           ↓
    ┌──────────┐  ┌────────────────────┐  ┌──────────────┐
    │  Google  │  │  HuggingFace API   │  │  Astra DB    │
    │  Speech  │  │  (LLM Inference)   │  │  (Vectors)   │
    │   API    │  └────────────────────┘  └──────────────┘
    └──────────┘
```

---

## 🛠️ Tech Stack

### Backend
- **Flask 3.1.2** - Web framework
- **LangChain 0.3.18** - LLM orchestration
- **HuggingFace Hub** - Model inference
- **Cassio** - Astra DB integration
- **SpeechRecognition** - Audio transcription
- **PyPDF** - Resume parsing
- **Sentence Transformers** - Embeddings

### Frontend
- **Vanilla JavaScript** - No framework overhead
- **Web Audio API** - Browser audio capture
- **CSS Grid/Flexbox** - Responsive layout
- **LocalStorage** - Theme persistence

### Database & AI
- **Astra DB** - Vector storage (Cassandra)
- **HuggingFace LLM** - `openai/gpt-oss-120b`
- **Sentence Transformers** - `all-MiniLM-L6-v2`
- **Google Speech Recognition** - Free tier

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Modern web browser (Chrome/Edge recommended)
- Active internet connection

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/interviewiq.git
cd interviewiq
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables
Create a `.env` file in the project root:

```bash
# .env
ASTRA_DB_APPLICATION_TOKEN=AstraCS:xxxxx...
ASTRA_DB_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

# Note: HuggingFace token is set via UI, not here
```

---

## ⚙️ Configuration

### 1. Get Astra DB Credentials

1. Go to [Astra DB](https://astra.datastax.com/)
2. Create a free account
3. Create a new database
4. Generate an application token
5. Copy token and database ID to `.env`

### 2. Get HuggingFace API Key

1. Go to [HuggingFace](https://huggingface.co/)
2. Sign up/login
3. Go to Settings → Access Tokens
4. Create a new token (read permission)
5. **Paste it in the web UI** (not in `.env`)

### 3. Configure Settings (Optional)

Edit `AI_model.py` to customize:
```python
# LLM Model
repo_id="openai/gpt-oss-120b"  # Change model

# Max response length
max_new_tokens=512

# Embedding model
model_name="sentence-transformers/all-MiniLM-L6-v2"

# RAG settings
chunk_size=1000
chunk_overlap=200
search_kwargs={"k": 3}
```

---

## 🚀 Usage

### Starting the Server

**Option 1: Python**
```bash
python main.py
```

**Option 2: PowerShell Script (Windows)**
```powershell
.\start_app.ps1
```

Server will start at `http://127.0.0.1:5000`

### Using the Interface

#### 1. Set API Key
- Open the app in your browser
- Left sidebar → Paste HuggingFace token
- Click "💾 Save API Key"
- You'll see a success message

#### 2. Choose Interview Mode
- **General Interview**: Standard questions without resume
- **Resume-Based**: Personalized questions from your background

#### 3. Upload Resume (Optional)
- Click "📎 Choose PDF File"
- Select your resume PDF
- Wait for "Resume uploaded & processed" message

#### 4. Start Interview

**Voice Input:**
1. Click microphone button 🎤
2. Speak your answer
3. Click again to stop ⏹️
4. Transcribed text appears in input field
5. Edit if needed
6. Press Enter to send

**Text Input:**
- Type your message in the text area
- Press Enter or click Send button

#### 5. Manage Chat
- **Clear Chat**: Click 🗑️ to reset conversation
- **Toggle Theme**: Click 🌙/☀️ for dark/light mode
- **New Chat**: Click "✨ New Chat" to start fresh

---

## 📁 Project Structure

```
interviewiq/
├── main.py                    # Flask application & endpoints
├── AI_model.py               # LLM chat logic with RAG
├── transcribe.py             # Audio-to-text conversion
├── speech_creator.py         # CLI voice capture (optional)
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
├── start_app.ps1            # Windows startup script
├── README.md                # This file
│
├── static/
│   ├── chat.css             # UI styling & themes
│   └── chat.js              # Frontend logic & WAV recorder
│
└── templates/
    └── chat.html            # Main interface HTML
```

### Key Files Explained

**`main.py`**
- Flask server initialization
- API endpoints (`/chat`, `/speech`, `/upload_resume`, etc.)
- Session management
- Auto-cleanup on startup

**`AI_model.py`**
- LangChain conversation chain
- HuggingFace LLM integration
- Resume RAG setup (PDF → Embeddings → Astra DB)
- Chat history management

**`transcribe.py`**
- Converts WAV audio buffer to text
- Uses Google Speech Recognition API
- Handles errors gracefully

**`chat.js`**
- Web Audio API setup
- PCM WAV encoding (16-bit mono)
- AJAX requests to backend
- Theme toggle & UI updates

**`chat.css`**
- Dark/light theme variables
- Responsive grid layout
- Message bubbles & animations

---

## 🔌 API Endpoints

### `POST /set_api`
Save HuggingFace API key to session.

**Request:**
```json
{
  "api_key": "hf_xxxxx..."
}
```

**Response:**
```json
{
  "status": "success",
  "message": "API key saved successfully"
}
```

---

### `POST /speech`
Transcribe audio to text (transcription only, no AI response).

**Request:** `multipart/form-data`
- `audio`: WAV file blob
- `session_id`: Session identifier

**Response:**
```json
{
  "result": "Transcribed text from audio"
}
```

---

### `POST /chat`
Send text message and get AI response.

**Request:**
```json
{
  "message": "Tell me about yourself",
  "session_id": "default",
  "use_resume": false
}
```

**Response:**
```json
{
  "response": "Hello! I'm your interview coach..."
}
```

---

### `POST /upload_resume`
Upload and process PDF resume.

**Request:** `multipart/form-data`
- `resume`: PDF file
- `session_id`: Session identifier

**Response:**
```json
{
  "status": "success",
  "message": "Resume uploaded successfully",
  "filename": "resume.pdf"
}
```

---

### `POST /clear_chat`
Clear conversation history for a session.

**Request:**
```json
{
  "session_id": "default"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Chat history cleared"
}
```

---

## 🧠 How It Works

### 1. Audio Recording Flow
```
User clicks mic → Browser requests permission
                → Web Audio API starts capture
                → ScriptProcessor collects PCM samples
                → Float32Array accumulates audio data
User clicks stop → Samples merged into single buffer
                → Encoded as 16-bit PCM WAV
                → Sent to /speech endpoint
                → Google Speech Recognition transcribes
                → Text appears in input field
                → User reviews/edits
                → Manually sends to AI
```

### 2. Chat Flow
```
User message → Flask /chat endpoint
            → AI_model.chat_with_history()
            → Retrieves session history
            → (Optional) Fetches resume context from Astra DB
            → Constructs prompt with history + context
            → Calls HuggingFace LLM API
            → AI response returned
            → Added to session history
            → Displayed in UI
```

### 3. Resume RAG Flow
```
PDF upload → PyPDF extracts text
          → RecursiveCharacterTextSplitter chunks text
          → SentenceTransformer creates embeddings
          → Embeddings stored in Astra DB (Cassandra)
          → On query: Semantic search finds top-k chunks
          → Chunks appended to user message as context
          → LLM uses context for personalized questions
```

### 4. Auto-Cleanup (Startup)
```
Server starts → cleanup_all_resume_tables()
             → Connects to Astra DB
             → Queries system schema for tables
             → Filters tables starting with 'resume_'
             → Drops each table with DROP TABLE IF EXISTS
             → Reports count of dropped tables
             → Server continues normally
```

---

## 🐛 Troubleshooting

### Issue: "Please provide your HuggingFace API key"
**Solution:** 
1. Get token from https://huggingface.co/settings/tokens
2. Paste in sidebar and click "Save API Key"
3. Refresh page if needed

---

### Issue: "Microphone error: NotAllowedError"
**Solution:**
1. Browser blocked microphone access
2. Click lock icon in address bar
3. Allow microphone permission
4. Refresh page

---

### Issue: "Could not process audio"
**Solution:**
1. Check microphone is working (test in other apps)
2. Speak louder/closer to mic
3. Try different browser (Chrome/Edge recommended)
4. Check internet connection (Google Speech API requires online)

---

### Issue: "Astra DB credentials not found"
**Solution:**
1. Verify `.env` file exists in project root
2. Check `ASTRA_DB_APPLICATION_TOKEN` and `ASTRA_DB_ID` are set
3. Ensure no extra spaces or quotes around values
4. Restart server after editing `.env`

---

### Issue: Import errors on startup
**Solution:**
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

---

### Issue: Port 5000 already in use
**Solution:**
```bash
# Change port in main.py:
app.run(debug=True, host='127.0.0.1', port=5001)
```

---

## 🤝 Contributing

We welcome contributions! Here's how:

### 1. Fork & Clone
```bash
git clone https://github.com/yourusername/interviewiq.git
cd interviewiq
git checkout -b feature/your-feature-name
```

### 2. Make Changes
- Follow existing code style
- Add comments for complex logic
- Test thoroughly before committing

### 3. Commit & Push
```bash
git add .
git commit -m "feat: add your feature description"
git push origin feature/your-feature-name
```

### 4. Create Pull Request
- Go to GitHub repository
- Click "New Pull Request"
- Describe changes and why they're needed
- Wait for review

### Development Guidelines
- **Code Style**: Follow PEP 8 for Python
- **Commits**: Use conventional commits (`feat:`, `fix:`, `docs:`)
- **Testing**: Test all endpoints before submitting
- **Documentation**: Update README if adding features

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 InterviewIQ

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 🙏 Acknowledgments

### Technologies
- [LangChain](https://www.langchain.com/) - LLM framework
- [HuggingFace](https://huggingface.co/) - Model hosting
- [Astra DB](https://astra.datastax.com/) - Vector database
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Sentence Transformers](https://www.sbert.net/) - Embeddings

### Inspiration
- Real interview experiences
- AI tutoring systems
- Voice assistants

### Contributors
- **Gaurav** - Initial development
- **GitHub Copilot** - Code assistance

---

## 📞 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/interviewiq/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/interviewiq/discussions)
- **Email**: your.email@example.com

---

## 🗺️ Roadmap

### v1.1 (Planned)
- [ ] Multiple LLM model support
- [ ] Interview performance analytics
- [ ] Export interview transcripts
- [ ] Mobile app (React Native)

### v2.0 (Future)
- [ ] Multi-user support with authentication
- [ ] Custom interview templates
- [ ] Video interview simulation
- [ ] AI feedback on answers

---

## 📊 Stats

![GitHub Stars](https://img.shields.io/github/stars/yourusername/interviewiq?style=social)
![GitHub Forks](https://img.shields.io/github/forks/yourusername/interviewiq?style=social)
![GitHub Issues](https://img.shields.io/github/issues/yourusername/interviewiq)
![GitHub Pull Requests](https://img.shields.io/github/issues-pr/yourusername/interviewiq)

---

<div align="center">

**Made with ❤️ by developers, for developers**

⭐ Star this repo if you find it helpful!

[Report Bug](https://github.com/yourusername/interviewiq/issues) · [Request Feature](https://github.com/yourusername/interviewiq/issues) · [Documentation](https://github.com/yourusername/interviewiq/wiki)

</div>
