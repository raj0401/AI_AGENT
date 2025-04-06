import os
import requests
from dotenv import load_dotenv
from actions import get_seo_page_report
from prompts import system_prompt
from json_helpers import extract_json

# Load environment variables
load_dotenv()
print("Loaded API Key:", os.getenv("GEMINI_API_KEY"))

# Get the API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("API Key not found. Please set GEMINI_API_KEY in the .env file.")

# Create an instance of the Gemini API client (using mock here for testing)
class GeminiClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def chat(self, model, messages):
        # Mocking a response that includes the function call

        user_url = messages[-1]["content"].split("of ")[-1].strip("?")  # Extract URL from the user message
        return {
            "choices": [{
                "message": {
                                        "content": f'{{"function_name": "get_seo_page_report", "function_parms": {{"url": "{user_url}"}}}}'

                }
            }]
        }

# Instantiate Gemini client
gemini_client = GeminiClient(api_key=os.getenv("GEMINI_API_KEY"))

# Function to generate text with conversation (Gemini API version)
def generate_text_with_conversation(messages, model="gpt-3.5-turbo"):
    response = gemini_client.chat(model=model, messages=messages)
    return response["choices"][0]["message"]["content"]

# Function to get the response time of a webpage
def get_seo_page_report(url):
    try:
        # Send a GET request to the webpage and measure response time
        response = requests.get(url)
        response_time = response.elapsed.total_seconds()
        return f"The response time of the web page \"{url}\" is approximately {response_time:.6f} seconds."
    except requests.exceptions.RequestException as e:
        return f"Error while fetching the page: {e}"

# Available actions
available_actions = {
    "get_seo_page_report": get_seo_page_report
}

# Get user input for the URL


user_url = input("Please enter the URL of the webpage (e.g., https://google.com): ") 

# User prompt asking for the response time of a webpage
user_prompt = f"what is the response time of {user_url}?"

# Messages for conversation with the API
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt},
]

turn_count = 1
max_turns = 5

while turn_count < max_turns:
    print(f"Loop: {turn_count}")
    print("----------------------")
    turn_count += 1

    # Generate response using Gemini API
    response = generate_text_with_conversation(messages, model="gpt-3.5-turbo")

    print(f"Generated Response: {response}")

    # Extract JSON for the function call
    try:
        json_function = extract_json(response)
        if json_function:
            function_name = json_function[0]['function_name']
            function_parms = json_function[0]['function_parms']
            if function_name not in available_actions:
                raise Exception(f"Unknown action: {function_name}: {function_parms}")
            print(f" -- running {function_name} {function_parms}")
            action_function = available_actions[function_name]
            # Call the function
            result = action_function(**function_parms)
            function_result_message = f"Action_Response: {result}"
            messages.append({"role": "user", "content": function_result_message})
            print(function_result_message)
        else:
            print("No function call found in the response.")
    except Exception as e:
        print(f"Error: {e}")
        break
