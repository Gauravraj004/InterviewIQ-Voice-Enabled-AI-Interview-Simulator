import speech_recognition as sr

def transcribe_audio(audio_buffer):
    """
    Transcribe PCM WAV audio from an in-memory buffer.
    The buffer must be a valid WAV file (PCM 16-bit mono preferred).
    """
    recognizer = sr.Recognizer()
    audio_buffer.seek(0)
    try:
        with sr.AudioFile(audio_buffer) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            return text
    except Exception as e:
        raise Exception(f"Could not process audio: {e}")
















