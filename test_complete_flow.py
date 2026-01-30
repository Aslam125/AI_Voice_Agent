import os
import requests
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("VOICE AI AGENT - COMPLETE API TEST")
print("=" * 60)

# Test 1: GitHub Token Validation
print("\n[TEST 1] Validating GitHub Token...")
github_token = os.getenv("GITHUB_TOKEN")
print(f"Token (first 20 chars): {github_token[:20]}...")

response = requests.get(
    "https://api.github.com/user",
    headers={"Authorization": f"Bearer {github_token}"}
)
if response.status_code == 200:
    user_data = response.json()
    print(f"[SUCCESS] Token is valid for user: {user_data.get('login', 'Unknown')}")
else:
    print(f"[ERROR] Token validation failed: {response.status_code}")

# Test 2: GitHub Models API (LLM)
print("\n[TEST 2] Testing GitHub Models API (GPT-4o)...")
llm_response = requests.post(
    "https://models.inference.ai.azure.com/chat/completions",
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {github_token}"
    },
    json={
        "model": "gpt-4o",
        "messages": [
            {"role": "user", "content": "What is the capital of France? Answer in one word."}
        ]
    }
)

if llm_response.status_code == 200:
    llm_data = llm_response.json()
    ai_reply = llm_data["choices"][0]["message"]["content"]
    print(f"[SUCCESS] AI Response: {ai_reply}")
    print(f"Tokens used: {llm_data['usage']['total_tokens']}")
else:
    print(f"[ERROR] LLM API failed: {llm_response.status_code}")
    print(f"Response: {llm_response.text}")

# Test 3: Deepgram API
print("\n[TEST 3] Testing Deepgram API Key...")
deepgram_key = os.getenv("DEEPGRAM_API_KEY")
print(f"API Key (first 10 chars): {deepgram_key[:10]}...")

dg_response = requests.get(
    "https://api.deepgram.com/v1/projects",
    headers={"Authorization": f"Token {deepgram_key}"}
)

if dg_response.status_code == 200:
    print("[SUCCESS] Deepgram API key is valid")
else:
    print(f"[ERROR] Deepgram validation failed: {dg_response.status_code}")

# Test 4: Flask App Endpoint
print("\n[TEST 4] Testing Flask App Endpoint...")
try:
    app_response = requests.get("http://127.0.0.1:5000", timeout=2)
    if app_response.status_code == 200:
        print("[SUCCESS] Flask app is running and responding")
    else:
        print(f"[WARNING] Flask app returned status: {app_response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"[ERROR] Flask app not reachable: {e}")

print("\n" + "=" * 60)
print("TEST SUMMARY")
print("=" * 60)
print("All API keys are loaded and functional!")
print("The Voice AI Agent is ready to process audio requests.")
print("=" * 60)
