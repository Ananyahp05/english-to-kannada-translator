# English to Kannada Translator

A web-based application that translates text and speech from English to Kannada using Google Cloud APIs.

## Features

✨ **Text Translation**: Translate English text to Kannada with a simple click  
🎤 **Speech Translation**: Record English speech and get instant Kannada translation with audio output  
🔊 **Text-to-Speech**: Listen to Kannada translations in natural-sounding voice  
📋 **Copy to Clipboard**: Easily copy translations for use elsewhere  
🎨 **Modern UI**: Clean, intuitive interface with smooth animations  
⌨️ **Keyboard Shortcuts**: Ctrl+T for text, Ctrl+M for microphone  

## Prerequisites

- Python 3.8+
- Google Cloud Project with enabled APIs
- Active Google Cloud credentials

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Google Cloud Authentication

```bash
# Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
# On Windows:
set GOOGLE_APPLICATION_CREDENTIALS=path\to\your\credentials.json

# On macOS/Linux:
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/credentials.json
```

### 3. Enable Required Google Cloud APIs

In your Google Cloud Console, enable:
- Google Cloud Translation API
- Google Cloud Speech-to-Text API
- Google Cloud Text-to-Speech API

### 4. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## Project Structure

```
english-to-kannada-translator/
├── app.py                 # Flask backend with API endpoints
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main HTML interface
└── static/
    ├── style.css         # Styling and animations
    └── script.js         # Frontend functionality and interactions
```

## API Endpoints

### POST /translate-text
Translates English text to Kannada.

**Request:**
```json
{
  "text": "Hello, how are you?"
}
```

**Response:**
```json
{
  "original": "Hello, how are you?",
  "translated": "ನಮಸ್ಕಾರ, ನೀವು ಹೇಗಿದ್ದೀರಿ?",
  "success": true
}
```

### POST /translate-speech
Translates recorded speech (English) to Kannada text and generates audio.

**Request:** Multipart form data with audio file  
**Response:**
```json
{
  "original": "Recognized English text",
  "translated": "ಕನ್ನಡ ಅನುವಾದ",
  "audio": "base64_encoded_audio",
  "success": true
}
```

### POST /text-to-speech
Converts Kannada text to speech.

**Request:**
```json
{
  "text": "ಹಲೋ"
}
```

**Response:**
```json
{
  "audio": "base64_encoded_audio",
  "success": true
}
```

## Usage

### Text Translation
1. Enter English text in the left textarea
2. Click "Translate Text" button
3. View Kannada translation in the right textarea
4. Use "Copy" to copy the translation or "Speak" for audio

### Speech Translation
1. Click the microphone button "Start Recording"
2. Speak in English
3. Click "Stop Recording" when done
4. Wait for processing - results will show:
   - Recognized English text
   - Kannada translation
   - Audio playback of translation

## Browser Compatibility

- Chrome 60+
- Firefox 55+
- Safari 14+
- Edge 79+

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl + T | Focus on English text input |
| Ctrl + M | Toggle microphone recording |

## Error Handling

The application includes comprehensive error handling for:
- Missing audio devices
- Network errors
- Google Cloud API failures
- Invalid input

## Limitations

- Speech recognition works best with clear audio
- Translation accuracy depends on Google Cloud Translation API
- Audio generation available for supported languages
- Maximum text length may apply per API call

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

For issues or questions:
1. Check Google Cloud Console for API quotas and permissions
2. Verify credentials are correctly set
3. Ensure all required APIs are enabled
4. Check browser console for JavaScript errors

## Future Enhancements

- [ ] Support for more language pairs
- [ ] Offline translation capability
- [ ] Translation history
- [ ] Custom vocabulary support
- [ ] Real-time translation updates
- [ ] Mobile app version

---

Created with ❤️ for language translation enthusiasts
