# Quick Start Guide

## Option 1: Quick Setup (Recommended for Beginners)

### Using Local/Free APIs (No Authentication Required)

#### 1. Install Dependencies
```bash
pip install -r requirements_local.txt
```

#### 2. Start the Application
```bash
python app_local.py
```

#### 3. Open in Browser
Visit: `http://localhost:5000`

---

## Option 2: Professional Setup (Google Cloud)

### Using Google Cloud APIs (High Quality)

#### 1. Prerequisites
- Google Cloud Account
- Enabled APIs (Translation, Speech-to-Text, Text-to-Speech)
- Downloaded service account credentials JSON file

#### 2. Set Environment Variable
```bash
# Windows
set GOOGLE_APPLICATION_CREDENTIALS=path\to\credentials.json

# macOS/Linux
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Start the Application
```bash
python app.py
```

#### 5. Open in Browser
Visit: `http://localhost:5000`

---

## Features Available

### Both Versions Include:
- ✅ English to Kannada Text Translation
- ✅ Speech-to-Text Recognition
- ✅ Translation of Recognized Speech
- ✅ Text-to-Speech in Kannada
- ✅ Copy to Clipboard
- ✅ Keyboard Shortcuts (Ctrl+T, Ctrl+M)
- ✅ Modern, Responsive UI

### Quality Differences:
| Feature | Google Cloud | Local |
|---------|--------------|-------|
| Translation Accuracy | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Speech Recognition | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Voice Quality | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Authentication | Required | Not Required |
| Cost | Paid (with free tier) | Free |
| Offline Support | No | Partial |

---

## Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r requirements_local.txt  # or requirements.txt
```

### Microphone not working
- Check browser permissions for microphone access
- Try a different browser
- Ensure microphone is connected and working

### Translation not working
- Check internet connection
- For Google Cloud: verify credentials and API keys
- For Local: check if services are running

### Port 5000 already in use
```bash
# Use a different port
python app_local.py  # Modify app to use port 5001
```

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **Ctrl + T** | Focus on English text input |
| **Ctrl + M** | Toggle microphone recording |

---

## Project Files

```
english-to-kannada-translator/
├── app.py                    # Google Cloud backend
├── app_local.py              # Local/Free APIs backend
├── requirements.txt          # Google Cloud dependencies
├── requirements_local.txt    # Local dependencies
├── SETUP_GUIDE.md           # Detailed setup guide
├── ALTERNATIVE_SETUP.md     # Alternative implementations
├── QUICK_START.md           # This file
├── templates/
│   └── index.html           # Main interface
└── static/
    ├── style.css            # Styling
    └── script.js            # Frontend logic
```

---

## What's Next?

1. **Try Text Translation**: Enter English text and click "Translate Text"
2. **Try Speech Translation**: Click the microphone and speak in English
3. **Listen to Translation**: Click "Speak" button for audio output
4. **Explore More**: Customize the app or add more features

---

## Support & Resources

- **Issue with Microphone?** Check browser permissions
- **Translation seems wrong?** Google Translate sometimes has limitations
- **Need Help?** See SETUP_GUIDE.md for detailed instructions

---

Enjoy translating! 🌍 Happy learning! 📚
