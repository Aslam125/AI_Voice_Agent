import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
from deepgram import DeepgramClient

load_dotenv()
app = Flask(__name__)

# Initialize Clients
dg_client = DeepgramClient(api_key=os.getenv("DEEPGRAM_API_KEY"))

# 1. GitHub Models Client (OpenAI, Llama, Mistral)
github_client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.getenv("GITHUB_TOKEN")
)

# 2. Google Gemini Client (OpenAI Compatible)
gemini_client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("GEMINI_API_KEY")
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process-audio', methods=['POST'])
def process_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file"}), 400

    audio_file = request.files['audio']
    audio_data = audio_file.read()
    model_choice = request.form.get('model', 'gpt-4o')

    try:
        # STEP 1: Deepgram Speech-to-Text (v5.x SDK Syntax)
        dg_response = dg_client.listen.v1.media.transcribe_file(
            request=audio_data,
            model="nova-3",
            smart_format=True,
            language="en"
        )
        
        # Safe transcript extraction
        try:
            user_text = dg_response.results.channels[0].alternatives[0].transcript
        except (AttributeError, IndexError):
            user_text = ""

        if not user_text:
            return jsonify({
                "transcript": "", 
                "agent_reply": "I'm sorry, I couldn't hear anything. Could you repeat that?"
            })

        # STEP 2: Intelligent Routing (GitHub vs Google)
        messages = [
            {"role": "system", "content": "You are a concise, helpful voice assistant. Keep answers brief and conversational. Do NOT use markdown formatting (no asterisks, bold, or bullet points). Use plain text only."},
            {"role": "user", "content": user_text}
        ]

        if "gemini" in model_choice.lower():
            # Use Google Gemini Client
            ai_response = gemini_client.chat.completions.create(
                model=model_choice,
                messages=messages
            )
        else:
            # Use GitHub Models Client
            ai_response = github_client.chat.completions.create(
                model=model_choice,
                messages=messages
            )
        
        agent_reply = ai_response.choices[0].message.content

        return jsonify({
            "transcript": user_text,
            "agent_reply": agent_reply
        })

    except Exception as e:
        import traceback
        error_msg = f"Error processing voice: {str(e)}"
        print(error_msg)
        traceback.print_exc()
        return jsonify({"error": error_msg}), 500

if __name__ == '__main__':
    # Running on port 5000 by default
    app.run(debug=True, port=5000)