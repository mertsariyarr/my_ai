import argparse
import os
from google import genai
from dotenv import load_dotenv
from google.genai import types
from functions.call_function import available_functions, call_function
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
   


    for function_call in response.function_calls:
        function_call_result = call_function(function_call, args.verbose)

    if len(function_call_result.parts) == 0:
        raise Exception("This function call is not avaiable.")
    
    if function_call_result.parts[0].function_response is None:
        raise Exception("This property should't be None!")
    
    if function_call_result.parts[0].function_response.response is None:
        raise Exception("This final area shouldn't be None")
    
    my_function_result = function_call_result.parts[0]

    if not response.usage_metadata:
        raise RuntimeError("Api Response Failure")
    
    if args.verbose:
        print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        if response.function_calls is None or len(response.function_calls) == 0:
            print(f"{response.text}")
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")





    



if __name__ == "__main__":
    main()
