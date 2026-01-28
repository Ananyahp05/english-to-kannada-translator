let mediaRecorder;
let audioChunks = [];
let recordingStartTime;
let recordingTimer;
let isRecording = false;

// Initialize Web Audio API
const audioContext = new (window.AudioContext || window.webkitAudioContext)();

// Text Translation
async function translateText() {
    const englishText = document.getElementById('englishText').value.trim();
    
    if (!englishText) {
        alert('Please enter English text to translate');
        return;
    }
    
    const btn = event.target;
    btn.disabled = true;
    btn.textContent = 'Translating...';
    
    try {
        const response = await fetch('/translate-text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: englishText })
        });
        
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('kannadaText').value = data.translated;
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        alert('Error translating text: ' + error.message);
    } finally {
        btn.disabled = false;
        btn.textContent = 'Translate Text';
    }
}

// Speech to Kannada Translation
async function startRecording() {
    if (isRecording) {
        stopRecording();
        return;
    }
    
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];
        
        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };
        
        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            await processSpeechTranslation(audioBlob);
            
            // Stop all tracks
            stream.getTracks().forEach(track => track.stop());
        };
        
        mediaRecorder.start();
        isRecording = true;
        
        const btn = document.getElementById('recordBtn');
        btn.classList.add('recording');
        btn.textContent = '⏹️ Stop Recording';
        
        recordingStartTime = Date.now();
        recordingTimer = setInterval(updateRecordingTime, 1000);
        document.getElementById('recordingTime').classList.add('active');
        
    } catch (error) {
        alert('Error accessing microphone: ' + error.message);
    }
}

function stopRecording() {
    if (mediaRecorder && isRecording) {
        mediaRecorder.stop();
        isRecording = false;
        
        const btn = document.getElementById('recordBtn');
        btn.classList.remove('recording');
        btn.textContent = '🎙️ Start Recording';
        
        clearInterval(recordingTimer);
        document.getElementById('recordingTime').classList.remove('active');
        document.getElementById('recordingTime').textContent = '';
    }
}

function updateRecordingTime() {
    const elapsed = Math.floor((Date.now() - recordingStartTime) / 1000);
    const minutes = Math.floor(elapsed / 60);
    const seconds = elapsed % 60;
    document.getElementById('recordingTime').textContent = 
        `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}

async function processSpeechTranslation(audioBlob) {
    const formData = new FormData();
    formData.append('audio', audioBlob);
    
    const recordBtn = document.getElementById('recordBtn');
    recordBtn.disabled = true;
    recordBtn.textContent = 'Processing...';
    
    // Reset results
    document.getElementById('recognizedText').textContent = 'Processing...';
    document.getElementById('translatedSpeechText').textContent = 'Processing...';
    document.getElementById('noAudio').textContent = 'Processing...';
    document.getElementById('translatedAudio').style.display = 'none';
    document.getElementById('copySpeechBtn').style.display = 'none';
    
    try {
        const response = await fetch('/translate-speech', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Display recognized text
            document.getElementById('recognizedText').textContent = data.original;
            
            // Display translated text
            document.getElementById('translatedSpeechText').textContent = data.translated;
            document.getElementById('copySpeechBtn').style.display = 'inline-block';
            
            // Display audio
            if (data.audio) {
                const audioElement = document.getElementById('translatedAudio');
                audioElement.src = 'data:audio/mp3;base64,' + data.audio;
                audioElement.style.display = 'block';
                document.getElementById('noAudio').textContent = '';
            } else {
                document.getElementById('noAudio').textContent = 'No audio available';
            }
        } else {
            document.getElementById('recognizedText').textContent = 'Error: ' + data.error;
            document.getElementById('translatedSpeechText').textContent = '-';
            document.getElementById('noAudio').textContent = '-';
        }
    } catch (error) {
        document.getElementById('recognizedText').textContent = 'Error: ' + error.message;
        document.getElementById('translatedSpeechText').textContent = '-';
        document.getElementById('noAudio').textContent = '-';
    } finally {
        recordBtn.disabled = false;
        recordBtn.textContent = '🎙️ Start Recording';
    }
}

// Text to Speech
async function speakKannada() {
    const kannadaText = document.getElementById('kannadaText').value.trim();
    
    if (!kannadaText) {
        alert('Please translate text first or enter Kannada text');
        return;
    }
    
    const btn = event.target;
    btn.disabled = true;
    btn.textContent = '⏳ Generating Speech...';
    
    try {
        const response = await fetch('/text-to-speech', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: kannadaText })
        });
        
        const data = await response.json();
        
        if (data.success && data.audio) {
            const audio = new Audio('data:audio/mp3;base64,' + data.audio);
            audio.play();
        } else {
            alert('Error generating speech: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        alert('Error generating speech: ' + error.message);
    } finally {
        btn.disabled = false;
        btn.textContent = '🔊 Speak';
    }
}

// Copy to Clipboard
function copyToClipboard(elementId) {
    const element = document.getElementById(elementId);
    const text = element.value;
    
    if (text) {
        navigator.clipboard.writeText(text).then(() => {
            const btn = event.target;
            const originalText = btn.textContent;
            btn.textContent = '✓ Copied!';
            setTimeout(() => {
                btn.textContent = originalText;
            }, 2000);
        });
    }
}

function copySpeechTranslation() {
    const text = document.getElementById('translatedSpeechText').textContent;
    
    if (text && text !== '-') {
        navigator.clipboard.writeText(text).then(() => {
            const btn = event.target;
            const originalText = btn.textContent;
            btn.textContent = '✓ Copied!';
            setTimeout(() => {
                btn.textContent = originalText;
            }, 2000);
        });
    }
}

// Keyboard shortcuts
document.addEventListener('DOMContentLoaded', () => {
    document.addEventListener('keydown', (e) => {
        // Ctrl+T for text translation
        if (e.ctrlKey && e.key === 't') {
            e.preventDefault();
            document.getElementById('englishText').focus();
        }
        
        // Ctrl+M for microphone
        if (e.ctrlKey && e.key === 'm') {
            e.preventDefault();
            const recordBtn = document.getElementById('recordBtn');
            recordBtn.click();
        }
    });
});
