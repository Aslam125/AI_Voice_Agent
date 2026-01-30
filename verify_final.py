import os
import requests

token = os.getenv("GITHUB_TOKEN")
url = "https://models.inference.ai.azure.com/chat/completions"

models = [
    "DeepSeek-R1",
    "Meta-Llama-3.1-405B-Instruct",
    "Meta-Llama-3.1-70B-Instruct",
    "Mistral-large-2407",
    "Mistral-Nemo"
]

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

print("Verifying selected models...")
for model in models:
    payload = {
        "messages": [{"role": "user", "content": "Test"}],
        "model": model,
        "max_tokens": 1
    }
    try:
        r = requests.post(url, headers=headers, json=payload)
        status = "OK" if r.status_code == 200 else f"Fail {r.status_code}"
        print(f"{model}: {status}")
    except Exception as e:
        print(f"{model}: Error {e}")
