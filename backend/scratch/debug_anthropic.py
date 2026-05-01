
import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
print(f"Base URL: {client.base_url}")

try:
    message = client.messages.create(
        max_tokens=10,
        messages=[{"role": "user", "content": "hi"}],
        model="claude-3-5-sonnet-20240620",
    )
    print("✅ Success")
except Exception as e:
    print(f"❌ Failed: {e}")
