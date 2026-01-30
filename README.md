# Voice AI Agent

A robust Voice AI Agent web application that seamlessly integrates Speech-to-Text (STT) and Large Language Models (LLMs) to provide a conversational experience. The agent listens to your voice, transcribes it using Deepgram's Nova-3 model, and responds intelligently using your preferred AI model (via GitHub Models or Google Gemini).

## Key Features

- **Advanced Speech-to-Text**: Utilizes **Deepgram's Nova-3** model for fast and highly accurate audio transcription.
- **Multi-Model Support**:
  - **GitHub Models**: Access to top-tier models like **GPT-4o**, **Llama 3**, and **Mistral** via Azure AI inference.
  - **Google Gemini**: Integration with **Gemini** models through the OpenAI-compatible API.
- **Intelligent Routing**: Dynamically routes requests to the appropriate model provider based on your selection.
- **Modern Web Interface**: A clean, responsive UI for recording audio and viewing the interaction history.

## Prerequisites

Before running the application, ensure you have the following installed:
- [Python 3.8+](https://www.python.org/downloads/)
- `pip` (Python package manager)

You will also need API keys for the following services:
- **Deepgram API Key**: For speech-to-text functionality.
- **GitHub Token**: For accessing GitHub Models.
- **Google Gemini API Key**: For accessing Gemini models.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd voice_ai_agent
    ```

2.  **Create a virtual environment:**
    ```bash
    # Windows
    python -m venv .venv
    .venv\Scripts\activate

    # Unix/macOS
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the root directory (based on `.env.example` if available) and add your API keys:
    ```env
    DEEPGRAM_API_KEY=your_deepgram_api_key
    GITHUB_TOKEN=your_github_token
    GEMINI_API_KEY=your_google_gemini_api_key
    ```

## Usage

1.  **Run the application:**
    ```bash
    python src/voice_ai_agent/app.py
    ```

2.  **Access the agent:**
    Open your web browser and navigate to:
    `http://localhost:5000`

3.  **Interact:**
    - Select an AI model from the dropdown menu (e.g., GPT-4o, Gemini).
    - Click the microphone button to start recording.
    - Speak your query clearly.
    - Click the button again to stop recording.
    - Wait for the agent to transcribe your audio and generate a text response.

## Technologies Used

- **Backend**: Flask (Python)
- **AI/ML Integration**:
  - **Deepgram SDK**: For Speech-to-Text.
  - **OpenAI Python Client**: Wrapper used for both GitHub Models and Google Gemini interactions.
- **Frontend**: HTML5, CSS3, JavaScript

## Project Structure

```
voice_ai_agent/
├── src/
│   └── voice_ai_agent/
│       ├── static/          # CSS and JavaScript assets
│       ├── templates/       # HTML templates (index.html)
│       ├── app.py           # Main Flask application
│       └── main.py          # Entry point (basic)
├── requirements.txt         # Project dependencies
├── .env                     # Environment variables
└── README.md                # Project documentation
```

## Testing

To run the test suite:
```bash
pytest
```
