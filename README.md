# InterviewIQ 🎯

An AI-powered interview assistant that helps you practice and prepare for interviews with intelligent, context-aware responses based on your resume.

## ✨ Features

- **AI Interview Coach**: Practice interviews with an AI assistant powered by HuggingFace LLMs
- **Resume-Aware Responses**: Upload your resume (PDF) and get personalized interview questions and feedback
- **Voice Interaction**: Record your responses with built-in audio recording (5-second clips)
- **Speech Recognition**: Automatic transcription of your voice responses using Google Speech Recognition
- **RAG Technology**: Uses Retrieval-Augmented Generation with Cassandra/Astra DB for intelligent resume parsing
- **Session Management**: Multiple chat sessions with persistent conversation history
- **Modern UI**: Clean, responsive interface with animated backgrounds

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- HuggingFace API Token ([Get one here](https://huggingface.co/settings/tokens))
- Astra DB Account (Free tier available - [Sign up](https://astra.datastax.com))
- Microphone (for voice recording feature)

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd 1
```

2. **Create a virtual environment**
```bash
python -m venv myenv
myenv\Scripts\activate  # Windows
# source myenv/bin/activate  # Linux/Mac
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the project root:
```env
ASTRA_DB_APPLICATION_TOKEN=your_astra_db_token
ASTRA_DB_ID=your_astra_db_id
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token
```

5. **Run the application**
```bash
python main.py
```

6. **Open your browser**
```
http://localhost:5000
```

## 📁 Project Structure

```
1/
├── main.py                 # Flask application & routes
├── AI_model.py            # LLM integration & RAG logic
├── transcribe.py          # Speech-to-text transcription
├── speech_creator.py      # Audio recording functionality
├── requirements.txt       # Python dependencies
├── templates/
│   └── chat.html         # Main UI template
└── static/
    ├── chat.css          # Styling
    └── chat.js           # Frontend logic
```

## 🎮 Usage

1. **Enter your HuggingFace API key** in the sidebar
2. **Upload your resume** (PDF format) for personalized responses
3. **Start chatting** with the AI interview coach
4. **Record responses** using the voice button (optional)
5. **Clear chat** anytime to start fresh

## 🔧 Technologies Used

- **Backend**: Flask, Python
- **AI/ML**: LangChain, HuggingFace Transformers, Sentence Transformers
- **Database**: Cassandra (Astra DB) for vector storage
- **Speech**: SpeechRecognition, PyAudio
- **Frontend**: HTML5, CSS3, JavaScript

## 🔑 Key Components

### AI Model (`AI_model.py`)
- Manages chat sessions and conversation history
- Implements RAG for resume-based context
- Handles vector embeddings and similarity search
- Automatic cleanup of old resume tables

### Transcription (`transcribe.py`)
- Converts audio to text using Google Speech Recognition
- Supports in-memory buffer processing

### Speech Creator (`speech_creator.py`)
- Records 5-second audio clips
- Captures audio in PCM WAV format

## ⚙️ Configuration

### Supported LLM Models
The application uses HuggingFace endpoints. You can modify the model in `AI_model.py`:
- Default: `mistralai/Mistral-7B-Instruct-v0.3`
- Configurable via environment variables

### Audio Settings
Adjust recording parameters in `speech_creator.py`:
- Sample Rate: 44100 Hz
- Channels: Mono
- Duration: 5 seconds

## 🛠️ Troubleshooting

**Audio not recording?**
- Ensure PyAudio is properly installed
- Check microphone permissions

**Resume upload fails?**
- Verify PDF is valid and under 16MB
- Check Astra DB connection

**API errors?**
- Validate HuggingFace API token
- Ensure Astra DB credentials are correct

## 📝 License

This project is open-source and available under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 👨‍💻 Author

Gaurav

---

**Note**: This project requires API keys from HuggingFace and Astra DB. Free tiers are available for both services.
