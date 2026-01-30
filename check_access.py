import os
import requests
import json

token = os.getenv("GITHUB_TOKEN")
url = "https://models.inference.ai.azure.com/chat/completions"

models_to_test = [
    "gpt-4o",
    "Meta-Llama-3.1-8B-Instruct",
    "Phi-3-mini-4k-instruct", # Testing just in case
    "DeepSeek-R1" # Testing just in case
]

print(f"Checking model access with token: {token[:10]}...")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

for model in models_to_test:
    print(f"\n--- Testing {model} ---")
    payload = {
        "messages": [
            {"role": "user", "content": "Hi"}
        ],
        "model": model,
        "max_tokens": 5
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            print(f"SUCCESS: {model} is accessible.")
            print(f"Response: {response.json()['choices'][0]['message']['content']}")
        else:
            print(f"FAILED: {model} returned status {response.status_code}")
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"ERROR: Could not connect for {model}: {e}")
