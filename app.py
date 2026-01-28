from flask import Flask, render_template, request, jsonify
from google.cloud import translate_v2
from google.cloud import speech_v1
from google.cloud import texttospeech_v1
import os
import io
import base64

app = Flask(__name__)

# Initialize Google Cloud clients
translate_client = translate_v2.Client()
speech_client = speech_v1.SpeechClient()
tts_client = texttospeech_v1.TextToSpeechClient()

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
        
        # Translate using Google Cloud Translation API
        result = translate_client.translate_text(
            text,
            source_language_code=SOURCE_LANGUAGE,
            target_language_code=TARGET_LANGUAGE
        )
        
        translated_text = result['translatedText']
        
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
        audio_data = audio_file.read()
        
        # Recognize speech
        audio = speech_v1.RecognitionAudio(content=audio_data)
        config = speech_v1.RecognitionConfig(
            encoding=speech_v1.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code='en-US'
        )
        
        response = speech_client.recognize(config=config, audio=audio)
        
        # Extract recognized text
        transcript = ''
        for result in response.results:
            for alternative in result.alternatives:
                transcript += alternative.transcript
        
        if not transcript:
            return jsonify({'error': 'Could not recognize speech'}), 400
        
        # Translate the recognized text
        translation_result = translate_client.translate_text(
            transcript,
            source_language_code=SOURCE_LANGUAGE,
            target_language_code=TARGET_LANGUAGE
        )
        
        translated_text = translation_result['translatedText']
        
        # Generate speech for translated text
        synthesis_input = texttospeech_v1.SynthesisInput(text=translated_text)
        voice = texttospeech_v1.VoiceSelectionParams(
            language_code=f'{TARGET_LANGUAGE}-IN',
            name='kn-IN-Neural2-A'
        )
        audio_config = texttospeech_v1.AudioConfig(
            audio_encoding=texttospeech_v1.AudioEncoding.MP3
        )
        
        tts_response = tts_client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        
        # Encode audio to base64
        audio_base64 = base64.b64encode(tts_response.audio_content).decode('utf-8')
        
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
        
        # Generate speech
        synthesis_input = texttospeech_v1.SynthesisInput(text=text)
        voice = texttospeech_v1.VoiceSelectionParams(
            language_code=f'{TARGET_LANGUAGE}-IN',
            name='kn-IN-Neural2-A'
        )
        audio_config = texttospeech_v1.AudioConfig(
            audio_encoding=texttospeech_v1.AudioEncoding.MP3
        )
        
        response = tts_client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        
        # Encode audio to base64
        audio_base64 = base64.b64encode(response.audio_content).decode('utf-8')
        
        return jsonify({
            'audio': audio_base64,
            'success': True
        })
    
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
