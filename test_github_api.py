import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Test GitHub Models API
github_client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.getenv("GITHUB_TOKEN")
)

print("Testing GitHub Models API...")
print(f"API Key (first 20 chars): {os.getenv('GITHUB_TOKEN')[:20]}...")

try:
    response = github_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": "Say hello in one sentence"}
        ]
    )
    print("\n[SUCCESS] GitHub API is working!")
    print(f"Response: {response.choices[0].message.content}")
    print(f"\nModel used: {response.model}")
    print(f"Tokens used: {response.usage.total_tokens}")
except Exception as e:
    print(f"\n[ERROR]: {e}")
