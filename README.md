# AI Interview Assistant# 🎯 Interview Assistant - AI-Powered Interview Preparation



## 📁 Clean Project StructureA beautiful, dynamic web application that helps you prepare for job interviews using AI. Practice with realistic interview questions, get intelligent follow-ups, and improve your interview skills with real-time feedback.



```## ✨ Features

1/

├── main.py              # Flask web app (CLEAN - no duplicates)- 🎤 **Voice Recognition**: Practice speaking naturally with advanced speech-to-text

├── AI_model.py         # AI logic with HuggingFace- 🤖 **AI Interview Coach**: Powered by Mistral-7B-Instruct for intelligent conversations

├── transcribe.py       # Audio → text- 💬 **Interactive Chat**: Real-time conversation with contextual follow-up questions

├── speech_creator.py   # Text → speech- 🎨 **Beautiful UI**: Modern, gradient-based design with smooth animations

├── .env               # HuggingFace API token- 📱 **Responsive**: Works seamlessly on desktop and mobile devices

├── requirements.txt   # Dependencies- ⚡ **Real-time**: Instant transcription and AI responses

├── templates/chat.html

├── static/chat.js & chat.css## 🚀 Getting Started

├── uploads/           # Resume PDFs

└── myenv/            # Virtual environment (USE THIS!)### Prerequisites

```

- Python 3.10+

## 🚀 Quick Start- A HuggingFace API token ([Get one here](https://huggingface.co/settings/tokens))

- Microphone access for voice recording

```bash

# 1. Activate environment### Installation

.\myenv\Scripts\Activate.ps1

1. **Clone or navigate to the project directory**

# 2. Run app   ```bash

python main.py   cd "c:\Users\Gaurav\Desktop\Gen Ai\Projects\Self\1"

   ```

# 3. Open browser

http://127.0.0.1:50002. **Activate your virtual environment** (if using one)

```   ```bash

   # Windows

## 🔑 Setup API Key   myenv\Scripts\activate

   

Add to `.env`:   # Or use the one in parent directory

```   ..\myenv\Scripts\activate

HUGGINGFACEHUB_API_TOKEN=hf_your_token_here   ```

```

3. **Install dependencies**

Get free token: https://huggingface.co/settings/tokens   ```bash

   pip install -r requirements.txt

## ✨ Features   ```



- ✅ **Text Chat**: Type questions4. **Set up your environment variables**

- ✅ **Voice Chat**: Click mic to record   

- ✅ **Resume Upload**: Upload PDF, ask questions about it   Create a `.env` file in the project root (already exists):

- ✅ **FREE**: Uses HuggingFace (no OpenAI costs)   ```

- ✅ **Privacy**: Embeddings run locally   HUGGINGFACEHUB_API_TOKEN=your_token_here

   ```

## 🎯 What's Cleaned

### Running the Application

- ❌ Removed duplicate imports in main.py

- ❌ Removed test files1. **Start the Flask server**

- ❌ Removed unused documentation   ```bash

- ❌ Removed Database_SQL.py   python main.py

- ✅ Single clean main.py   ```

- ✅ All code organized

- ✅ Using myenv environment2. **Open your browser**

   

## 📦 All Dependencies in myenv   Navigate to: `http://localhost:5000`



Already installed:3. **Start practicing!**

- Flask 3.1.2 + flask-cors 6.0.1   - Click "Start Interview Practice" on the home page

- langchain 0.3.27   - Either speak using the microphone or type your responses

- sentence-transformers 5.1.1   - The AI will ask relevant interview questions based on your role

- torch 2.8.0

- chromadb 1.1.1## 🎨 Features in Detail



## 🐛 Troubleshooting### Landing Page

- Beautiful gradient background with animated particles

### "Failed to fetch"- Feature cards showcasing key capabilities

1. Ensure myenv is activated: `.\myenv\Scripts\Activate.ps1`- Visual preview of the interview interface

2. Run: `python main.py`- One-click access to start practicing

3. Check: http://127.0.0.1:5000

### Interview Interface

### Resume upload issues- **Real-time Chat**: See your conversation history

- File must be PDF- **Voice Recording**: 5-second recording clips (automatically stops)

- Max 16MB- **Text Input**: Type responses if you prefer

- First run downloads embedding model (~420MB)- **Tips Panel**: Interview tips and best practices

- **Session Management**: End session anytime

## 📊 How It Works

### AI Capabilities

```- Asks what role you're preparing for

Browser → Flask (main.py) → AI_model.py → HuggingFace API- Generates professional, role-specific questions

                                        ↓- Provides intelligent follow-up questions

                                   Vector Store (for resume)- Maintains conversation context throughout the session

```- Realistic interview simulation



See `SETUP_GUIDE.md` for detailed instructions.## 📁 Project Structure


```
1/
├── main.py                    # Flask backend with API endpoints
├── AI_model.py               # AI model configuration (legacy)
├── speech_creator.py         # Audio recording utilities
├── transcribe.py            # Speech-to-text conversion
├── .env                     # Environment variables
├── requirements.txt         # Python dependencies
├── templates/               # HTML templates
│   ├── index.html          # Landing page
│   └── interview.html      # Interview interface
├── static/                 # Static assets
│   ├── css/
│   │   └── style.css       # Beautiful styling with animations
│   └── js/
│       ├── particles.js    # Background particle effects
│       └── interview.js    # Interview page functionality
```

## 🛠️ API Endpoints

- `GET /` - Landing page
- `GET /interview` - Interview interface
- `POST /api/start-session` - Initialize new interview session
- `POST /api/send-message` - Send text message to AI
- `POST /api/transcribe-audio` - Convert audio to text
- `POST /api/end-session` - End current session

## 🎯 How It Works

1. **Session Creation**: When you start, a new session is created with conversation history
2. **AI Context**: The AI maintains context throughout the conversation
3. **Speech Recognition**: Audio is recorded, converted to text using Google Speech Recognition
4. **AI Response**: Text is sent to Mistral-7B-Instruct via HuggingFace API
5. **Conversation Flow**: Each response is added to history for contextual follow-ups

## 💡 Tips for Best Results

- **Speak Clearly**: Enunciate well during voice recording
- **Take Your Time**: Think before responding
- **Be Specific**: Use concrete examples from your experience
- **Use STAR Method**: Structure answers as Situation, Task, Action, Result
- **Practice Regularly**: The more you practice, the better you'll become

## 🎨 Customization

### Change AI Model
Edit `main.py` line 22:
```python
llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",  # Change this
    ...
)
```

### Adjust Recording Duration
Edit `static/js/interview.js` line 62:
```javascript
setTimeout(() => {
    if (isRecording) {
        stopRecording();
    }
}, 5000);  // Change this value (in milliseconds)
```

### Modify System Prompt
Edit `main.py` line 45 to change how the AI behaves

## 🐛 Troubleshooting

### Microphone Not Working
- Check browser permissions
- Ensure microphone is connected and working
- Use HTTPS (required for some browsers)

### Audio Transcription Fails
- Speak more clearly
- Reduce background noise
- Use the text input instead

### AI Responses Are Slow
- This is normal for API calls
- Consider using a faster model
- Check your internet connection

## 📝 License

This project is for educational purposes.

## 🤝 Contributing

Feel free to fork, improve, and submit pull requests!

---

**Made with ❤️ using Flask, LangChain, and HuggingFace**
