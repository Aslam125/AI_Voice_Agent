import os
import requests
import json

token = os.getenv("GITHUB_TOKEN")
url = "https://models.inference.ai.azure.com/models"

headers = {
    "Authorization": f"Bearer {token}"
}

try:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        models = response.json()
        print(f"Found {len(models)} models.")
        for m in models:
            print(f"- {m.get('name')} (Friendly: {m.get('friendly_name')})")
    else:
        print(f"Failed to list models. Status: {response.status_code}")
except Exception as e:
    print(f"Error: {e}")
