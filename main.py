import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

messages = [
    types.Content(role="user", parts=[types.Part(text=sys.argv[0])]),
]

if len(sys.argv) != 1:
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=sys.argv)

    print(response.text)
else:
    print("Error with sys argv")
    sys.exit(1)

if "--verbose" in sys.argv:
    print(f"User prompt: {messages}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")