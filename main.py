import sys
import os
import argparse
from google import genai
from google.genai import types  # type: ignore
from dotenv import load_dotenv  # type: ignore
from call_function import call_function, available_functions


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("prompt", nargs="*", help="Your prompt for the AI")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    if not args.prompt:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)


    user_prompt = " ".join(args.prompt)

    if args.verbose:
        print(f"Working on: {user_prompt}")

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    iters = 0
    while True:
        iters += 1
        if iters > 20:
            print("Too many iterations, stopping to prevent infinite loop.")
            sys.exit(1)
        try:
            final_response = generate_content(client, messages, args.verbose)
            if final_response:
                print("Final response:", final_response)
                break
        except Exception as e:
             print(f"Error during content generation: {e}")


def generate_content(client, messages, verbose=False):
    """
    Generate content using the Gemini AI model with iterative function calls.

    Args:
        client: The GenAI client instance.
        messages: List of messages to send to the AI.
        verbose (bool): If True, enables verbose output.
    """
    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read file contents
        - Execute Python files with optional arguments
        - Write or overwrite files

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """


    res = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
            ),
        )
    if verbose:
         print("Prompt tokens:", res.usage_metadata.prompt_token_count)
         print("Response tokens:", res.usage_metadata.candidates_token_count)

    if res.candidates:
         for candidate in res.candidates:
              function_call_content = candidate.content
              messages.append(function_call_content)

    if not res.function_calls:
         return res.text
    
    function_responses = []

    for function_call_part in res.function_calls:
            function_call_result = call_function(function_call_part, verbose)
            if not function_call_result.parts or not function_call_result.parts[0].function_response:
                raise Exception(
                    f"Function call {function_call_part.name} did not return a valid response."
                )
            if verbose:
                 print(f"-> {function_call_result.parts[0].function_response.response}")
            function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("No function responses received.")
    messages.append(types.Content(role="tool", parts=function_responses))
    

if __name__ == "__main__":
    main()
