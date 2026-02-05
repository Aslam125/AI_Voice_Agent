import os
import asyncio
import logging
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from deepgram import DeepgramClient
from agent_manager import VoiceAgentManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
app = Flask(__name__)

# Initialize Clients
try:
    dg_client = DeepgramClient(api_key=os.getenv("DEEPGRAM_API_KEY"))
    agent_manager = VoiceAgentManager()
    logger.info("Clients initialized successfully")
except Exception as e:
    logger.error(f"Initialization Error: {e}")
    raise e

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process-audio', methods=['POST'])
async def process_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file"}), 400

    audio_file = request.files['audio']
    audio_data = audio_file.read()

    try:
        # STEP 1: Deepgram Speech-to-Text (STT)
        # Deepgram SDK v5 (Fern-generated) uses direct keyword arguments
        logger.info("Calling Deepgram STT...")
        
        # Using transcribe_file from v1.media
        # Reference: client.listen.v1.media.transcribe_file
        dg_response = dg_client.listen.v1.media.transcribe_file(
            request=audio_data,
            model="nova-2",
            smart_format=True,
            language="en"
        )
        
        try:
            # The response structure has also changed in v5
            # Results -> Channels -> Alternatives -> Transcript
            user_text = dg_response.results.channels[0].alternatives[0].transcript
            logger.info(f"Transcript: {user_text}")
        except (AttributeError, IndexError) as e:
            logger.warning(f"Failed to extract transcript: {e}")
            user_text = ""

        if not user_text:
            return jsonify({
                "transcript": "", 
                "agent_reply": "I'm sorry, I couldn't hear anything. Could you repeat that?",
                "audio_base64": ""
            })

        # STEP 2: AgentScope ReAct Agent Logic
        logger.info("Calling Agent...")
        agent_output = await agent_manager.get_response(user_text)
        logger.info("Agent response received")

        return jsonify({
            "transcript": user_text,
            "agent_reply": agent_output["text"],
            "audio_base64": agent_output["audio"]
        })

    except Exception as e:
        import traceback
        error_msg = f"Error processing voice: {str(e)}"
        logger.error(error_msg)
        traceback.print_exc()
        return jsonify({"error": error_msg, "transcript": "", "agent_reply": "Error"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
