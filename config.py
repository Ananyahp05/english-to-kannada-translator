z# Configuration file for the translator app

# Server Configuration
DEBUG = True
HOST = '0.0.0.0'
PORT = 5000

# Translation Settings
SOURCE_LANGUAGE = 'en'
TARGET_LANGUAGE = 'kn'

# Speech Settings
SPEECH_RECOGNITION_LANGUAGE = 'en-US'
TEXT_TO_SPEECH_LANGUAGE = 'kn-IN'
TTS_VOICE_NAME = 'kn-IN-Neural2-A'

# Audio Settings
AUDIO_SAMPLE_RATE = 16000
AUDIO_FORMAT = 'LINEAR16'
AUDIO_ENCODING = 'MP3'

# API Configuration
MAX_REQUEST_SIZE = 10 * 1024 * 1024  # 10MB
REQUEST_TIMEOUT = 30  # seconds

# Logging
LOG_LEVEL = 'INFO'
LOG_FILE = 'translator.log'
