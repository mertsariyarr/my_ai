import argparse
import sys
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
    
    for _ in range(20):
        try:
            final_response = generate_content(client, messages, args.verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                return
        except Exception as e:
            print(f"Error in generate_content: {e}")

    print(f"Maximum iterations ({20}) reached")
    sys.exit(1)

    if args.verbose:
        print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        if response.function_calls is None or len(response.function_calls) == 0:
            print(f"{response.text}")
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")



def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if response.candidates:
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call in response.function_calls:
        result = call_function(function_call, verbose)
        if (
            not result.parts
            or not result.parts[0].function_response
            or not result.parts[0].function_response.response
        ):
            raise RuntimeError(f"Empty function response for {function_call.name}")
        if verbose:
            print(f"-> {result.parts[0].function_response.response}")
        function_responses.append(result.parts[0])

    messages.append(types.Content(role="user", parts=function_responses))


    



if __name__ == "__main__":
    main()
