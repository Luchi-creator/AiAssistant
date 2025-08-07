import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv
from functions.get_files_info import (
    schema_get_files_info,
    schema_run_python_file,
    schema_get_file_content,
    schema_write_file,
    call_function,
)

# Load API key
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY not found in .env file.")
    sys.exit(1)

client = genai.Client(api_key=api_key)

# Set up system prompt
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

# Check for user prompt
if len(sys.argv) < 2:
    print("Error: Prompt required as a command-line argument.")
    sys.exit(1)

user_prompt = sys.argv[1]
verbose = "--verbose" in sys.argv

# Initialize message list
messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

# Define available tools
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_run_python_file,
        schema_get_file_content,
        schema_write_file,
    ]
)

# Set config
config = types.GenerateContentConfig(
    tools=[available_functions],
    system_instruction=system_prompt
)

# Conversation loop
MAX_STEPS = 20
for step in range(MAX_STEPS):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=config
        )

        # Append all model responses to messages
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

        # Check if final response is present
        has_text_response = any(
            part.text for candidate in response.candidates
            for part in (candidate.content.parts if candidate.content else [])
            if hasattr(part, "text")
        )

        if has_text_response and not response.function_calls:
            final_text = "\n".join(
                part.text for candidate in response.candidates
                for part in (candidate.content.parts if candidate.content else [])
                if hasattr(part, "text")
            )
            print(f"\nFinal Response:\n{final_text}")
            break
        # If no function call, exit
        if not response.function_calls:
            print("No function calls in response. Exiting.")
            break

        function_call_part = response.function_calls[0]

        if verbose:
            print(f"\n- Calling function: {function_call_part.name}({function_call_part.args})")

        # Call the function
        function_response_content = call_function(function_call_part, verbose=verbose)

        # Sanity check: ensure function response is valid
        if not (
            hasattr(function_response_content, "parts")
            and function_response_content.parts
            and hasattr(function_response_content.parts[0], "function_response")
            and hasattr(function_response_content.parts[0].function_response, "response")
        ):
            raise RuntimeError("Fatal: Missing function response in returned content.")

        # Append function result as tool message
        messages.append(
            types.Content(
                role="tool",
                parts=function_response_content.parts
            )
        )

        # Optional verbose output of result
        if verbose:
            result = function_response_content.parts[0].function_response.response
            print(f"-> {result}")

    except Exception as e:
        print(f"Error during interaction step {step}: {e}")
        break

else:
    print("Max iterations reached without a final response.")
