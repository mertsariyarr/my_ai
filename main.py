import argparse
import os
from google import genai
from dotenv import load_dotenv
from google.genai import types
from functions.call_function import available_functions
from prompts import system_prompt


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
   
    
    parser = argparse.ArgumentParser(description="chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    if not api_key:
        raise RuntimeError("api couldn't find try again.!")
    client = genai.Client(api_key=api_key)

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    response = client.models.generate_content(model="gemini-2.5-flash", 
                                              contents=messages,
                                              config=types.GenerateContentConfig(
                                              tools=[available_functions], system_instruction=system_prompt
                                                    )
                                              )
   

    if not response.usage_metadata:
        raise RuntimeError("Api Response Failure")
    
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        if response.function_calls is None or len(response.function_calls) == 0:
            print(f"{response.text}")
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")





    



if __name__ == "__main__":
    main()
