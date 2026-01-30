import os
from openai import OpenAI

# Simulating reading the messy .env line
# Assuming the user's line is exactly: "gemini-2.0-flash =AIzaSyBnNzzUwo0RMlQQUr6JNQ1n42cgofgelSs"
fake_env_val = "AIzaSyBnNzzUwo0RMlQQUr6JNQ1n42cgofgelSs"

client = OpenAI(
    api_key=fake_env_val,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

print("Testing Gemini 2.0 Flash access...")

try:
    response = client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[
            {"role": "system", "content": "You turn text to uppercase."},
            {"role": "user", "content": "hello world"}
        ],
        max_tokens=10
    )
    print("SUCCESS")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"FAILED: {e}")
