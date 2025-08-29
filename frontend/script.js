// Day 27 से केवल एक बदलाव: WebSocket URL डायनामिक है
document.addEventListener('DOMContentLoaded', () => {
    const recordButton = document.getElementById('recordButton'),
        settingsButton = document.getElementById('settingsButton'),
        settingsModal = document.getElementById('settingsModal'),
        saveKeysButton = document.getElementById('saveKeysButton'),
        statusDiv = document.getElementById('status'),
        personaSelector = document.getElementById('persona'),
        imageContainer = document.getElementById('imageContainer'),
        generatedImage = document.getElementById('generatedImage'),
        keyInputs = {
            deepgram: document.getElementById('deepgramKey'),
            gemini: document.getElementById('geminiKey'),
            elevenlabs: document.getElementById('elevenlabsKey'),
            tavily: document.getElementById('tavilyKey'),
            openai: document.getElementById('openaiKey')
        };
    let apiKeys = {}, ws, mediaRecorder, audioContext, audioQueue = [], isPlaying = !1, isRecording = !1;

    function loadKeysFromLocalStorage() {
        const savedKeys = JSON.parse(localStorage.getItem('apiKeys')) || {};
        apiKeys = savedKeys;
        Object.keys(keyInputs).forEach(key => { if (savedKeys[key]) keyInputs[key].value = savedKeys[key]; });
        validateKeys();
    }

    function saveKeysToLocalStorage() {
        Object.keys(keyInputs).forEach(key => { apiKeys[key] = keyInputs[key].value.trim(); });
        localStorage.setItem('apiKeys', JSON.stringify(apiKeys));
        alert('API Keys saved!');
        settingsModal.classList.add('hidden');
        validateKeys();
    }

    function validateKeys() {
        const allKeysPresent = Object.values(apiKeys).every(key => key && key.length > 0) && Object.keys(apiKeys).length === 5;
        recordButton.disabled = !allKeysPresent;
        recordButton.textContent = allKeysPresent ? 'Start Conversation' : 'Configure Keys to Start';
    }

    settingsButton.addEventListener('click', () => settingsModal.classList.remove('hidden'));
    saveKeysButton.addEventListener('click', saveKeysToLocalStorage);
    settingsModal.addEventListener('click', (e) => { if (e.target === settingsModal) settingsModal.classList.add('hidden'); });
    recordButton.addEventListener('click', () => { if (!isRecording) startRecording(); else stopRecording(); });

    function startRecording() {
        isRecording = !0;
        recordButton.textContent = 'Stop Listening';
        recordButton.className = 'listening';
        statusDiv.textContent = 'Status: Listening...';
        imageContainer.classList.remove('visible');

        const selectedPersona = personaSelector.value;
        // --- DEPLOYMENT CHANGE ---
        const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsHost = window.location.host;
        const wsUrl = `${wsProtocol}//${wsHost}/ws?persona=${selectedPersona}`;
        ws = new WebSocket(wsUrl);
        console.log(`Connecting to WebSocket at: ${wsUrl}`);
        // --- END DEPLOYMENT CHANGE ---

        ws.onopen = () => {
            ws.send(JSON.stringify({ type: 'config', keys: apiKeys }));
            navigator.mediaDevices.getUserMedia({ audio: true }).then(handleStream);
        };
        ws.onclose = (event) => {
            if (event.reason.includes("API Key initialization failed")) alert('One of your API keys is invalid. Please check settings.');
            stopRecording(!1);
        };
        ws.onmessage = (event) => {
            if (typeof event.data === 'string') {
                const message = JSON.parse(event.data);
                if (message.type === 'image') {
                    generatedImage.src = message.url;
                    imageContainer.classList.add('visible');
                } else if (message.status === 'tts_finished') {
                    recordButton.className = 'ready';
                    recordButton.textContent = 'Start Conversation';
                }
            } else if (event.data instanceof ArrayBuffer) {
                audioQueue.push(new Uint8Aray(event.data));
                if (!isPlaying) playNextInQueue();
            }
        };
    }
    
    function handleStream(stream) {
        mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
        mediaRecorder.ondataavailable = event => { if (event.data.size > 0 && ws && ws.readyState === WebSocket.OPEN) ws.send(event.data); };
        mediaRecorder.start(250);
    }

    function stopRecording(setProcessing = !0) {
        if (mediaRecorder && mediaRecorder.state !== 'inactive') {
            mediaRecorder.stop();
            mediaRecorder.stream.getTracks().forEach(track => track.stop());
        }
        isRecording = !1;
        recordButton.className = setProcessing ? 'processing' : 'ready';
        recordButton.textContent = setProcessing ? 'Processing...' : 'Start Conversation';
    }

    async function playNextInQueue() {
        if (audioQueue.length === 0) { isPlaying = !1; return; }
        isPlaying = !0;
        if (!audioContext) audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const audioChunk = audioQueue.shift();
        try {
            const audioBuffer = await audioContext.decodeAudioData(audioChunk.buffer);
            const source = audioContext.createBufferSource();
            source.buffer = audioBuffer;
            source.connect(audioContext.destination);
            source.start();
            source.onended = () => playNextInQueue();
        } catch (e) {
            isPlaying = !1; playNextInQueue();
        }
    }
    loadKeysFromLocalStorage();
});