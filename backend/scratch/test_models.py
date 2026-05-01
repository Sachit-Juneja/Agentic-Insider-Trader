
import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

models_to_try = [
    "claude-3-5-sonnet-20241022",
    "claude-3-5-sonnet-20240620",
    "claude-3-opus-20240229",
    "claude-3-haiku-20240307",
    "claude-2.1",
]

for model in models_to_try:
    print(f"Testing {model}...")
    try:
        message = client.messages.create(
            max_tokens=10,
            messages=[{"role": "user", "content": "hi"}],
            model=model,
        )
        print(f"✅ Success with {model}")
        break
    except Exception as e:
        print(f"❌ Failed {model}: {e}")
