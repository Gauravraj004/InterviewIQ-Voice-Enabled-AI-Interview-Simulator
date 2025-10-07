<div align="center">🎙️ Voice-Powered AI Conversationalist<p><strong>A sophisticated, voice-enabled AI chat application that allows users to engage in natural, spoken conversations with an AI through a clean and modern web interface.</strong></p><p><img alt="Python Version" src="https://www.google.com/search?q=https://img.shields.io/badge/Python-3.8%2B-blue.svg%3Fstyle%3Dfor-the-badge%26logo%3Dpython%26logoColor%3Dwhite"><img alt="License" src="https://www.google.com/search?q=https://img.shields.io/badge/License-MIT-green.svg%3Fstyle%3Dfor-the-badge"><img alt="Status" src="https://www.google.com/search?q=https://img.shields.io/badge/Status-Active-brightgreen.svg%3Fstyle%3Dfor-the-badge"></p></div>Table of Contents✨ Core Features⚙️ How It Works📂 Project Structure🛠️ Tech Stack🚀 Getting StartedPrerequisitesInstallation & SetupRunning the Application🤝 How to Contribute📄 LicenseThis application bridges the gap between human conversation and artificial intelligence. It captures your voice, transcribes it to text in real-time, processes it with a powerful AI model, and speaks the response back to you.✨ Core Features🗣️ Seamless Voice Interaction: Talk to the AI as you would to a person. No typing required.⚡ Real-time Transcription: High-accuracy speech-to-text powered by our custom transcribe.py module.🔊 Natural Text-to-Speech: The AI's responses are converted into lifelike speech using the speech_creator.py module.🧠 Intelligent AI Backend: A robust AI model (AI_model.py) provides thoughtful and context-aware responses.💻 Modern Web Interface: A clean, user-friendly chat interface built with HTML, CSS, and vanilla JavaScript.🔒 Secure Configuration: All sensitive information, like API keys, is managed safely through an environment (.env) file.⚙️ How It WorksThe application follows a simple yet powerful workflow to create a fluid conversational experience:Voice Input: The frontend captures audio from your microphone via the browser.Transcription: The audio data is sent to the backend, where transcribe.py converts it into text.AI Processing: The transcribed text is passed to the AI_model.py for an intelligent response.Speech Synthesis: The AI's text response is given to speech_creator.py to generate audio.Audio Output: The generated audio file is sent back to the frontend and played automatically for the user.📂 Project Structure.
├──  AI_model.py             # Core logic for the AI chat model
├── main.py                 # Main application entry point (web server)
├── speech_creator.py       # Handles text-to-speech conversion
├── transcribe.py           # Handles speech-to-text transcription
├── requirements.txt        # Python dependencies
├── start_app.ps1           # (Windows) PowerShell script for starting the app
├── .env.example            # Example environment variables file
├── static/
│   ├── chat.css            # Styles for the chat interface
│   └── chat.js             # JavaScript for frontend logic
└── templates/
    └── chat.html           # HTML structure for the chat page
🛠️ Tech StackComponentTechnology / LibraryBackendPython (with Flask or FastAPI)FrontendHTML5, CSS3, JavaScript (ES6+)AI ModelCustom Python Module (AI_model.py)Speech-to-TextCustom Python Module (transcribe.py)Text-to-SpeechCustom Python Module (speech_creator.py)🚀 Getting StartedPrerequisitesPython 3.8+pip (Python package installer)Installation & SetupClone the Repositorygit clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
cd your-repository-name
Set Up a Virtual EnvironmentIt's best practice to create a virtual environment to manage project dependencies.On Windows:python -m venv venv
.\venv\Scripts\activate
On macOS/Linux:python3 -m venv venv
source venv/bin/activate
Install DependenciesInstall all the required Python packages from the requirements.txt file.pip install -r requirements.txt
Configure Environment VariablesYou'll need to provide your own API keys or other secret credentials.Rename .env.example to .env.Open requirements.txt to see which libraries are used (e.g., openai, google-cloud-speech) to determine which API keys you need.Add the necessary key-value pairs to the .env file.# .env
OPENAI_API_KEY="sk-..."
GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/credentials.json"
Running the ApplicationYou're all set! Start the web server using one of the following commands.Standard Method:python main.py
For Windows users (alternative):.\start_app.ps1
Once the server is running, open your web browser and navigate to http://1227.0.0.1:5000.🤝 How to ContributeWe welcome contributions! If you'd like to help improve the project, please follow these steps:Fork the repository.Create a new branch (git checkout -b feature/YourAmazingFeature).Make your changes.Commit your changes (git commit -m 'Add some YourAmazingFeature').Push to the branch (git push origin feature/YourAmazingFeature).Open a Pull Request.📄 LicenseThis project is licensed under the MIT License. See the LICENSE file for more details.
