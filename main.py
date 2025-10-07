"""
Main Flask Application
Handles web interface for AI Interview Assistant with resume upload
"""
##
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import io

# Import custom modules
import AI_model
import transcribe
import speech_creator

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.secret_key = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# No local file storage - everything goes to Astra DB!

# Auto-cleanup: Drop all old resume tables on server startup
print("\n" + "="*60)
print("[STARTUP] InterviewIQ - Initializing...")
print("="*60)
try:
    tables_dropped = AI_model.cleanup_all_resume_tables()
    if tables_dropped > 0:
        print(f"[STARTUP] ✅ Cleaned up {tables_dropped} old resume table(s)")
    else:
        print("[STARTUP] ✅ No old tables to clean up")
except Exception as e:
    print(f"[STARTUP] ⚠️ Cleanup skipped: {e}")
print("[STARTUP] Server ready!")
print("="*60 + "\n")


@app.route('/')
def home():
    """Render main chat interface"""
    return render_template('chat.html')


@app.route('/set_api', methods=['POST'])
def set_api():
    """Store API key in session"""
    data = request.get_json()
    api_key = data.get('api_key', '')
    
    if not api_key:
        return jsonify({'error': 'API key is required'}), 400
    
    session['api_key'] = api_key
    os.environ['HUGGINGFACEHUB_API_TOKEN'] = api_key
    
    return jsonify({'status': 'success', 'message': 'API key saved successfully'})


@app.route('/clear_chat', methods=['POST'])
def clear_chat():
    """Clear chat history for current session"""
    data = request.get_json()
    session_id = data.get('session_id', 'default')
    
    try:
        AI_model.clear_chat_history(session_id)
        return jsonify({'status': 'success', 'message': 'Chat history cleared'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    """Handle resume PDF upload and process with RAG - NO LOCAL STORAGE"""
    try:
        print("[INFO] Upload resume request received")
        
        if 'resume' not in request.files:
            return jsonify({'status': 'error', 'error': 'No file uploaded'}), 400
        
        file = request.files['resume']
        
        if file.filename == '':
            return jsonify({'status': 'error', 'error': 'No file selected'}), 400
        
        if not file.filename.endswith('.pdf'):
            return jsonify({'status': 'error', 'error': 'Only PDF files allowed'}), 400
        
        filename = secure_filename(file.filename)
        session_id = request.form.get('session_id', 'default')
        
        # Read PDF content directly into memory (NO FILE SAVING)
        print(f"[INFO] Reading PDF content directly from upload...")
        pdf_bytes = io.BytesIO(file.read())
        
        # Store filename in session for reference
        session['resume_filename'] = filename
        
        # Process with RAG directly from memory
        print(f"[INFO] Processing resume with RAG (Astra DB only)...")
        success = AI_model.setup_resume_rag_from_bytes(pdf_bytes, filename, session_id)
        
        if not success:
            return jsonify({'status': 'error', 'error': 'Failed to process resume'}), 500
        
        print(f"[INFO] Resume processed successfully and stored in Astra DB")
        return jsonify({
            'status': 'success',
            'message': f'Resume "{filename}" uploaded successfully',
            'filename': filename
        })
        
    except Exception as e:
        print(f"[ERROR] Upload failed: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'status': 'error', 'error': str(e)}), 500


@app.route('/speech', methods=['POST'])
def speech():
    """Handle audio transcription only (returns text to input field)"""
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file uploaded'}), 400
    
    try:
        audio_file = request.files['audio']
        audio_buffer = io.BytesIO(audio_file.read())
        
        # Transcribe audio only - no AI response
        text = transcribe.transcribe_audio(audio_buffer)
        
        # Return transcribed text for user to review/edit before sending
        return jsonify({'result': text})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/chat', methods=['POST'])
def chat():
    """Handle text chat messages"""
    data = request.get_json()
    user_message = data.get('message', '')
    session_id = data.get('session_id', 'default')
    use_resume = data.get('use_resume', False)
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        # Check API key
        if 'api_key' not in session:
            return jsonify({'error': 'Please set your API key first'}), 400
        
        # Get AI response
        ai_response = AI_model.chat_with_history(user_message, session_id, use_resume)
        
        return jsonify({'response': ai_response})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

