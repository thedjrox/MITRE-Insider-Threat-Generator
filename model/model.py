import requests
import json
import os
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("API_KEY")
def generate_response(prompt):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": "Bearer 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",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "nvidia/llama-3.1-nemotron-70b-instruct:free",
            "messages": [
            {
                "role": "user",
                "content": prompt
            }
            ],
            
        })
    )
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        result = response.json()
        # Extract the model's output
        model_output = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        return model_output
    else:
        print(f"Error: {response.status_code}")
        return None