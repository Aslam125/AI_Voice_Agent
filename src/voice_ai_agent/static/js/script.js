/**
 * Voice AI Agent - Client Side Logic
 * Minimal, efficient, and robust.
 */

let mediaRecorder;
let audioChunks = [];
let audioContext;
let audioStream;

const recordBtn = document.getElementById('recordBtn');
const statusEl = document.getElementById('status');
const userTextEl = document.getElementById('userText');
const agentTextEl = document.getElementById('agentText');
const modelSelect = document.getElementById('modelSelect');

// Lucide icon initialization
if (window.lucide) lucide.createIcons();

recordBtn.onclick = async () => {
    if (!mediaRecorder || mediaRecorder.state === "inactive") {
        await startRecording();
    } else {
        stopRecording();
    }
};

async function startRecording() {
    try {
        audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });

        // Determine supported mime type (Deepgram is flexible, but webm is standard for MediaRecorder)
        const mimeType = MediaRecorder.isTypeSupported('audio/webm;codecs=opus')
            ? 'audio/webm;codecs=opus'
            : 'audio/ogg;codecs=opus';

        mediaRecorder = new MediaRecorder(audioStream, { mimeType });
        audioChunks = [];

        mediaRecorder.ondataavailable = e => {
            if (e.data.size > 0) audioChunks.push(e.data);
        };

        mediaRecorder.onstop = handleRecordingStop;

        mediaRecorder.start();

        // UI Feedback
        recordBtn.classList.add('recording');
        recordBtn.innerHTML = '<i data-lucide="square" size="24"></i>';
        lucide.createIcons();

        statusEl.innerText = "Listening...";
        userTextEl.innerText = "...";
        agentTextEl.innerText = "...";

        // Reset styles
        userTextEl.parentElement.style.opacity = '1';
        agentTextEl.parentElement.style.opacity = '1';

    } catch (err) {
        console.error("Microphone error:", err);
        statusEl.innerText = "Mic Error";
        alert("Please allow microphone access to use the agent.");
    }
}

function stopRecording() {
    if (mediaRecorder && mediaRecorder.state !== "inactive") {
        mediaRecorder.stop();
        audioStream.getTracks().forEach(track => track.stop());

        recordBtn.classList.remove('recording');
        recordBtn.innerHTML = '<i data-lucide="mic" size="24"></i>';
        lucide.createIcons();

        statusEl.innerText = "Processing...";
    }
}

async function handleRecordingStop() {
    const audioBlob = new Blob(audioChunks, { type: mediaRecorder.mimeType });

    // Prepare data for app.py
    const formData = new FormData();
    formData.append('audio', audioBlob, 'speech.webm');
    formData.append('model', modelSelect.value);

    try {
        const response = await fetch('/process-audio', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.error || "Server error");
        }

        const data = await response.json();

        // Update UI with results
        userTextEl.innerText = data.transcript || "(No clear audio)";
        agentTextEl.innerText = data.agent_reply || "(No response)";

        // Text-to-Speech (Play AgentScope Audio or Fallback to Browser)
        if (data.audio_base64) {
            console.log("Playing AgentScope TTS...");
            const audio = new Audio("data:audio/mp3;base64," + data.audio_base64);

            audio.onplay = () => {
                statusEl.innerText = "Agent is speaking...";
            };
            audio.onended = () => {
                statusEl.innerText = "Ready";
            };

            audio.play().catch(e => {
                console.error("Audio playback failed, falling back to browser TTS", e);
                speak(data.agent_reply);
            });
        } else if (data.agent_reply) {
            console.log("No audio returned, using Browser TTS fallback.");
            speak(data.agent_reply);
        }

    } catch (err) {
        console.error("Transcription Error:", err);
        agentTextEl.innerText = "Error: " + err.message;
        statusEl.innerText = "Error";
    } finally {
        if (statusEl.innerText !== "Error") {
            statusEl.innerText = "Ready";
        }
    }
}

/**
 * Native Browser TTS
 */
function speak(text) {
    window.speechSynthesis.cancel();

    // Clean text for speech (remove markdown symbols like *, #, etc.)
    const cleanText = text.replace(/[*#_`]/g, '').trim();

    const utterance = new SpeechSynthesisUtterance(cleanText);

    // Pick a voice
    const voices = window.speechSynthesis.getVoices();
    const voice = voices.find(v => v.lang.startsWith('en')) || voices[0];
    if (voice) utterance.voice = voice;

    utterance.onstart = () => {
        statusEl.innerText = "Agent is speaking...";
    };

    utterance.onend = () => {
        statusEl.innerText = "Ready";
    };

    window.speechSynthesis.speak(utterance);
}

// Warm up voices
window.speechSynthesis.onvoiceschanged = () => window.speechSynthesis.getVoices();
