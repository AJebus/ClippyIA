import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("API key not found")

    client = genai.Client(api_key=api_key)
    try:
        parser = argparse.ArgumentParser(description="Chatbot")
        parser.add_argument("user_prompt", type=str, help="User prompt")
        parser.add_argument(
            "--verbose", action="store_true", help="Enable verbose output"
        )
        args = parser.parse_args()
        # Now we can access `args.user_prompt`

        messages: list[types.Content] = [
            types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
        ]

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
        )
        if response.usage_metadata is not None:
            if args.verbose:
                print(f"User prompt: {args.user_prompt}")
            print(
                f"Prompt tokens: {response.usage_metadata.prompt_token_count} \nResponse tokens: {response.usage_metadata.candidates_token_count}"
            )
        else:
            raise RuntimeError("Failed API request")
        print("Response:")
        print(response.text)
    except Exception as e:
        print(f"Gemini request failed: {e}")


if __name__ == "__main__":
    main()
