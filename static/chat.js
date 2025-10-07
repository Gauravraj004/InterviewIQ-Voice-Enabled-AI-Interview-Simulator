// chat.js - Enhanced InterviewIQ Interface
const chatBox = document.getElementById('chat-box');
const chatInput = document.getElementById('chat-input');

function timestamp() {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function hideWelcomeMessage() {
    const welcome = chatBox.querySelector('.welcome-message');
    if (welcome) welcome.style.display = 'none';
}

function addMessage(text, sender) {
    hideWelcomeMessage();
    const msg = document.createElement('article');
    msg.className = 'message ' + sender;
    const bubble = document.createElement('div');
    bubble.className = 'bubble';
    const meta = document.createElement('span');
    meta.className = 'meta';
    meta.textContent = sender === 'bot' ? 'InterviewIQ  ' + timestamp() : 'You  ' + timestamp();
    const body = document.createElement('p');
    body.textContent = text;
    bubble.appendChild(meta);
    bubble.appendChild(body);
    msg.appendChild(bubble);
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage(text) {
    const message = text || chatInput.value.trim();
    if (!message) return;
    addMessage(message, 'user');
    chatInput.value = '';
    const useResume = document.querySelector('input[name="interview-mode"]:checked').value === 'with-resume';
    try {
        const resp = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message, session_id: 'default', use_resume: useResume })
        });
        const data = await resp.json();
        if (data.error && /api key/i.test(data.error)) {
            addMessage('Please provide your HuggingFace API key in the left sidebar. Get one at https://huggingface.co/settings/tokens', 'bot');
            const inp = document.getElementById('api-key-input');
            if (inp) inp.focus();
        } else if (data.response) {
            addMessage(data.response, 'bot');
        } else if (data.error) {
            addMessage('Error: ' + data.error, 'bot');
        }
    } catch (err) {
        addMessage('Network error: ' + err.message, 'bot');
    }
}

chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Send button click
const sendBtn = document.getElementById('send-btn');
if (sendBtn) {
    sendBtn.addEventListener('click', () => sendMessage());
}

// WAV recording via Web Audio API (no MediaRecorder/ffmpeg)
let isRecording = false;
let audioContext;
let micStream;
let scriptProcessor;
let recordedChunks = [];
let recordingLength = 0;
let wavSampleRate = 16000; // desired; actual may differ
const micBtn = document.getElementById('mic-btn');
const micIcon = document.getElementById('mic-icon');
const micAnimation = document.getElementById('mic-animation');

async function startWavRecording() {
    audioContext = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: wavSampleRate });
    wavSampleRate = audioContext.sampleRate; // actual
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    micStream = stream;
    const source = audioContext.createMediaStreamSource(stream);
    scriptProcessor = audioContext.createScriptProcessor(4096, 1, 1);
    recordedChunks = [];
    recordingLength = 0;
    scriptProcessor.onaudioprocess = (e) => {
        const input = e.inputBuffer.getChannelData(0);
        recordedChunks.push(new Float32Array(input));
        recordingLength += input.length;
    };
    source.connect(scriptProcessor);
    scriptProcessor.connect(audioContext.destination);
}

function mergeBuffers(chunks, length) {
    const result = new Float32Array(length);
    let offset = 0;
    for (let i = 0; i < chunks.length; i++) {
        result.set(chunks[i], offset);
        offset += chunks[i].length;
    }
    return result;
}

function floatTo16BitPCM(float32Array) {
    const buffer = new ArrayBuffer(float32Array.length * 2);
    const view = new DataView(buffer);
    let offset = 0;
    for (let i = 0; i < float32Array.length; i++, offset += 2) {
        let s = Math.max(-1, Math.min(1, float32Array[i]));
        view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
    }
    return view;
}

function encodeWAV(samples, sampleRate) {
    const numChannels = 1;
    const bytesPerSample = 2;
    const blockAlign = numChannels * bytesPerSample;
    const byteRate = sampleRate * blockAlign;
    const dataSize = samples.length * bytesPerSample;
    const buffer = new ArrayBuffer(44 + dataSize);
    const view = new DataView(buffer);

    writeString(view, 0, 'RIFF');
    view.setUint32(4, 36 + dataSize, true);
    writeString(view, 8, 'WAVE');
    writeString(view, 12, 'fmt ');
    view.setUint32(16, 16, true);
    view.setUint16(20, 1, true);
    view.setUint16(22, numChannels, true);
    view.setUint32(24, sampleRate, true);
    view.setUint32(28, byteRate, true);
    view.setUint16(32, blockAlign, true);
    view.setUint16(34, 16, true);
    writeString(view, 36, 'data');
    view.setUint32(40, dataSize, true);

    const pcm = floatTo16BitPCM(samples);
    let offset = 44;
    const pcmView = new DataView(pcm.buffer);
    for (let i = 0; i < pcm.byteLength; i++) {
        view.setInt8(offset++, pcmView.getInt8(i));
    }
    return new Blob([view], { type: 'audio/wav' });
}

function writeString(view, offset, string) {
    for (let i = 0; i < string.length; i++) {
        view.setUint8(offset + i, string.charCodeAt(i));
    }
}

micBtn.addEventListener('click', async () => {
    if (!isRecording) {
        try {
            await startWavRecording();
            isRecording = true;
            micIcon.textContent = '⏹️';
            micAnimation.style.display = 'flex';
        } catch (err) {
            addMessage('Microphone error: ' + err.message, 'bot');
        }
    } else {
        try {
            if (scriptProcessor) scriptProcessor.disconnect();
            if (audioContext) await audioContext.close();
            if (micStream) micStream.getTracks().forEach(t => t.stop());
        } catch {}

        const samples = mergeBuffers(recordedChunks, recordingLength);
        const wavBlob = encodeWAV(samples, wavSampleRate);
        micAnimation.style.display = 'none';

        const formData = new FormData();
        formData.append('audio', wavBlob, 'recording.wav');
        formData.append('session_id', 'default');
        formData.append('use_resume', document.querySelector('input[name="interview-mode"]:checked').value === 'with-resume');

        try {
            const resp = await fetch('/speech', { method: 'POST', body: formData });
            const data = await resp.json();
            if (data.error && /api key/i.test(data.error)) {
                addMessage('Please provide your HuggingFace API key in the left sidebar. Get one at https://huggingface.co/settings/tokens', 'bot');
                const inp = document.getElementById('api-key-input');
                if (inp) inp.focus();
            } else if (data.error) {
                addMessage('Error: ' + data.error, 'bot');
            } else {
                // Get transcribed text (backend returns {result} for transcription-only)
                const transcribedText = data.result || data.text || '';
                if (transcribedText) {
                    // Insert transcribed text into input field for user to review/edit
                    chatInput.value = transcribedText;
                    chatInput.focus();
                    // Auto-expand textarea if text is long
                    chatInput.style.height = 'auto';
                    chatInput.style.height = chatInput.scrollHeight + 'px';
                }
            }
        } catch (err) {
            addMessage('Speech processing error: ' + err.message, 'bot');
        }

        isRecording = false;
        micIcon.textContent = '🎤';
    }
});

const saveApiBtn = document.getElementById('save-api-btn');
const apiKeyInput = document.getElementById('api-key-input');
const apiStatus = document.getElementById('api-status');

saveApiBtn.addEventListener('click', async () => {
    const apiKey = apiKeyInput.value.trim();
    if (!apiKey) {
        apiStatus.textContent = ' Please enter an API key';
        return;
    }
    try {
        const resp = await fetch('/set_api', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ api_key: apiKey })
        });
        const data = await resp.json();
        if (data.status === 'success') {
            apiStatus.textContent = ' API key saved successfully';
            apiKeyInput.value = '';
        } else {
            apiStatus.textContent = ' Failed to save API key';
        }
    } catch (err) {
        apiStatus.textContent = ' Error: ' + err.message;
    }
});

const uploadResumeBtn = document.getElementById('upload-resume-btn');
const resumeUploadInput = document.getElementById('resume-upload');
const uploadStatus = document.getElementById('upload-status');

uploadResumeBtn.addEventListener('click', () => {
    resumeUploadInput.click();
});

resumeUploadInput.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    if (!file.name.endsWith('.pdf')) {
        uploadStatus.textContent = ' Please select a PDF file';
        return;
    }
    uploadStatus.textContent = ' Uploading...';
    const formData = new FormData();
    formData.append('resume', file);
    formData.append('session_id', 'default');
    try {
        const resp = await fetch('/upload_resume', { method: 'POST', body: formData });
        const data = await resp.json();
        if (data.status === 'success' || data.success) {
            uploadStatus.textContent = ' Resume uploaded & processed';
        } else {
            uploadStatus.textContent = ' ' + (data.error || data.message || 'Upload failed');
        }
    } catch (err) {
        uploadStatus.textContent = ' Error: Failed to upload';
    }
});

const newChatBtn = document.getElementById('new-chat-btn');
const clearChatBtn = document.getElementById('clear-chat');

// Handle both new chat and clear chat buttons
function clearChat() {
    chatBox.innerHTML = '<div class="welcome-message" style="display: block;"><div class="welcome-icon">👋</div><h3>Welcome to InterviewIQ!</h3><p>I\'m your AI interview coach, ready to help you ace your next interview. Let\'s practice together!</p><div class="quick-tips"><div class="tip"><span class="tip-icon">💬</span><span>Type or use voice</span></div><div class="tip"><span class="tip-icon">📝</span><span>Upload your resume</span></div><div class="tip"><span class="tip-icon">🎯</span><span>Get personalized questions</span></div></div></div>';
}

newChatBtn.addEventListener('click', async () => {
    try {
        const resp = await fetch('/clear_chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_id: 'default' })
        });
        const data = await resp.json();
        if (data.status === 'success') {
            clearChat();
        }
    } catch (err) {
        addMessage('Error clearing chat: ' + err.message, 'bot');
    }
});

if (clearChatBtn) {
    clearChatBtn.addEventListener('click', async () => {
        try {
            const resp = await fetch('/clear_chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_id: 'default' })
            });
            const data = await resp.json();
            if (data.status === 'success') {
                clearChat();
            }
        } catch (err) {
            addMessage('Error clearing chat: ' + err.message, 'bot');
        }
    });
}

// Theme Toggle
const themeToggle = document.getElementById('theme-toggle');
let isDarkTheme = true;

themeToggle.addEventListener('click', () => {
    isDarkTheme = !isDarkTheme;
    document.body.classList.toggle('light-theme');
    themeToggle.textContent = isDarkTheme ? '🌙' : '☀️';
    localStorage.setItem('theme', isDarkTheme ? 'dark' : 'light');
});

// Load saved theme
const savedTheme = localStorage.getItem('theme');
if (savedTheme === 'light') {
    isDarkTheme = false;
    document.body.classList.add('light-theme');
    themeToggle.textContent = '☀️';
}

console.log('✨ InterviewIQ Chat Interface Loaded!');
