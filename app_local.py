from flask import Flask, render_template, request, jsonify
from googletrans import Translator
import speech_recognition as sr
import pyttsx3
import threading
import os
import io
import base64
from pydub import AudioSegment

app = Flask(__name__)

# Initialize services
translator = Translator()
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# Configure TTS
tts_engine.setProperty('rate', 150)
tts_engine.setProperty('volume', 0.9)

# Language codes
SOURCE_LANGUAGE = 'en'
TARGET_LANGUAGE = 'kn'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate-text', methods=['POST'])
def translate_text():
    """Translate text from English to Kannada"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Translate using googletrans
        translation = translator.translate(text, src_language=SOURCE_LANGUAGE, dest_language=TARGET_LANGUAGE)
        translated_text = translation['text']
        
        return jsonify({
            'original': text,
            'translated': translated_text,
            'success': True
        })
    
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/translate-speech', methods=['POST'])
def translate_speech():
    """Translate speech from audio file"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        audio_data = io.BytesIO(audio_file.read())
        
        # Convert WebM/OGG to WAV for speech recognition
        try:
            audio = AudioSegment.from_file(audio_data, format="webm")
        except:
            audio = AudioSegment.from_file(audio_data, format="ogg")
        
        # Export to WAV
        wav_data = io.BytesIO()
        audio.export(wav_data, format="wav")
        wav_data.seek(0)
        
        # Recognize speech
        with sr.AudioFile(wav_data) as source:
            audio_listen = recognizer.record(source)
        
        transcript = ''
        try:
            transcript = recognizer.recognize_google(audio_listen, language='en-US')
        except sr.UnknownValueError:
            return jsonify({'error': 'Could not understand audio'}), 400
        except sr.RequestError as e:
            return jsonify({'error': f'Speech recognition error: {str(e)}'}), 500
        
        if not transcript:
            return jsonify({'error': 'Could not recognize speech'}), 400
        
        # Translate the recognized text
        translation = translator.translate(transcript, src_language=SOURCE_LANGUAGE, dest_language=TARGET_LANGUAGE)
        translated_text = translation['text']
        
        # Generate speech for translated text
        audio_buffer = io.BytesIO()
        tts_engine.save_to_file(translated_text, 'temp_audio.mp3')
        tts_engine.runAndWait()
        
        # Read and encode the audio file
        with open('temp_audio.mp3', 'rb') as f:
            audio_base64 = base64.b64encode(f.read()).decode('utf-8')
        
        # Clean up temp file
        if os.path.exists('temp_audio.mp3'):
            os.remove('temp_audio.mp3')
        
        return jsonify({
            'original': transcript,
            'translated': translated_text,
            'audio': audio_base64,
            'success': True
        })
    
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    """Convert Kannada text to speech"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Generate speech using pyttsx3
        tts_engine.save_to_file(text, 'temp_speech.mp3')
        tts_engine.runAndWait()
        
        # Read and encode the audio file
        with open('temp_speech.mp3', 'rb') as f:
            audio_base64 = base64.b64encode(f.read()).decode('utf-8')
        
        # Clean up temp file
        if os.path.exists('temp_speech.mp3'):
            os.remove('temp_speech.mp3')
        
        return jsonify({
            'audio': audio_base64,
            'success': True
        })
    
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
