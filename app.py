from flask import Flask, render_template, request, jsonify
import pyttsx3
import os
import base64
import requests
from urllib.parse import quote
import pkgutil
import json

# Patch pkgutil for Python 3.14 compatibility
if not hasattr(pkgutil, 'get_loader'):
    pkgutil.get_loader = lambda name: None

app = Flask(__name__)

# Load Kannada dictionary
with open('kannada_dict.json', 'r', encoding='utf-8') as f:
    kannada_dict = json.load(f)

# Initialize services
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
        
        # Check dictionary first
        text_lower = text.lower()
        if text_lower in kannada_dict:
            translated_text = kannada_dict[text_lower]
        else:
            # Try to translate using Google's translation API via requests
            try:
                # Use a different approach - word by word from dictionary
                words = text_lower.split()
                translated_words = []
                
                for word in words:
                    # Check if word exists in dictionary
                    if word in kannada_dict:
                        translated_words.append(kannada_dict[word])
                    else:
                        # Try to find partial matches or keep original
                        translated_words.append(word)
                
                translated_text = ' '.join(translated_words)
                
                # If no translation found, try the API as fallback
                if translated_text == text_lower:
                    encoded_text = quote(text)
                    url = f"https://api.mymemory.translated.net/get?q={encoded_text}&langpair=en|kn"
                    response = requests.get(url, timeout=5)
                    result = response.json()
                    
                    if result.get('responseStatus') == 200:
                        translated_text = result['responseData'].get('translatedText', text)
            except Exception as api_error:
                print(f"API translation error: {api_error}")
                translated_text = text
        
        return jsonify({
            'original': text,
            'translated': translated_text,
            'success': True
        })
    
    except Exception as e:
        import traceback
        print(f"Error in translate_text: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/translate-speech', methods=['POST'])
def translate_speech():
    """Translate speech - simplified version"""
    try:
        return jsonify({'error': 'Speech recognition not available in this version', 'success': False}), 501
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
