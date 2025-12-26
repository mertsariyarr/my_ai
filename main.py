import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("api couldn't find try again.!")

def main():
    print("Hello from my-ai!")
    client = genai.Client(api_key=api_key)
    prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    if not response.usage_metadata:
        raise RuntimeError("Api Response Failure")
    print(f"User propmt: {prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(f"Response: {response.text}")



if __name__ == "__main__":
    main()
