from flask import Flask, render_template, request, jsonify
from pyttsx3 import init as init_tts
import threading
import os
import io
import base64
import sys
import requests

# Patch pkgutil for Python 3.14 compatibility
import pkgutil
if not hasattr(pkgutil, 'get_loader'):
    pkgutil.get_loader = lambda name: None

app = Flask('app_simple')

# Initialize services
tts_engine = init_tts()

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
        
        # Translate using free API
        url = f"https://api.mymemory.translated.net/get?q={text}&langpair=en|kn"
        response = requests.get(url, timeout=10)
        result = response.json()
        
        if result.get('responseStatus') == 200:
            translated_text = result['responseData'].get('translatedText', text)
        else:
            translated_text = text
        
        return jsonify({
            'original': text,
            'translated': translated_text,
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
        
        # Generate speech
        temp_file = 'temp_audio.mp3'
        tts_engine.save_to_file(text, temp_file)
        tts_engine.runAndWait()
        
        # Read the audio file and encode to base64
        if os.path.exists(temp_file):
            with open(temp_file, 'rb') as f:
                audio_base64 = base64.b64encode(f.read()).decode('utf-8')
            os.remove(temp_file)
            
            return jsonify({
                'audio': audio_base64,
                'success': True
            })
        else:
            return jsonify({'error': 'Failed to generate audio'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/translate-and-speak', methods=['POST'])
def translate_and_speak():
    """Translate text and convert to speech"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Translate using free API
        url = f"https://api.mymemory.translated.net/get?q={text}&langpair=en|kn"
        response = requests.get(url, timeout=10)
        result = response.json()
        
        if result.get('responseStatus') == 200:
            translated_text = result['responseData'].get('translatedText', text)
        else:
            translated_text = text
        
        # Generate speech
        temp_file = 'temp_audio.mp3'
        tts_engine.save_to_file(translated_text, temp_file)
        tts_engine.runAndWait()
        
        # Read the audio file and encode to base64
        audio_base64 = None
        if os.path.exists(temp_file):
            with open(temp_file, 'rb') as f:
                audio_base64 = base64.b64encode(f.read()).decode('utf-8')
            os.remove(temp_file)
        
        return jsonify({
            'original': text,
            'translated': translated_text,
            'audio': audio_base64,
            'success': True
        })
    
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
