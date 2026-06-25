import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function
from config import MAX_ITERATIONS


def main() -> None:
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("API key not found")

    client = genai.Client(api_key=api_key)
    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    history = []
    for i in range(MAX_ITERATIONS):
        try:
            result = generate_content(client, messages, args.verbose)
            if result:
                print(result)
                return

        except Exception as e:
            print(f"Gemini request failed: {e}")
    print("Max iterations reached")
    sys.exit(1)


def generate_content(
    client: genai.Client, messages: list[types.Content], verbose: bool
) -> str | None:

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if response.usage_metadata is None:
        raise RuntimeError("Failed API request")

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.function_calls is None:
        return f"Response: {response.text}"

    function_results: list[types.Part] = []
    for function_call in response.function_calls:
        result = call_function(function_call, verbose)
        if result.parts is None:
            raise Exception("Error: call_function failed")
        if result.parts[0].function_response is None:
            raise Exception("Error: Function error")
        if result.parts[0].function_response.response is None:
            raise Exception("Error: Function response error")
        if verbose:
            print(f"-> {result.parts[0].function_response.response}")
        function_results.append(result.parts[0])

    for candidate in response.candidates:
        messages.append(candidate.content)
    messages.append(types.Content(role="user", parts=function_results))


if __name__ == "__main__":
    main()
