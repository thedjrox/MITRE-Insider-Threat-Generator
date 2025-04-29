import requests
import json
import os
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("API_KEY")
print(API_KEY)


def generate_response(prompt):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            # "Authorization": "Bearer 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",  # Jacob's API Key
            # "Authorization": "Bearer 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",  # Sehaj Gill's API Key
            # "Authorization": "Bearer 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",  # API Key 1
            # "Authorization": "Bearer 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",  # API Key 2
            "Content-Type": "application/json",
        },
        data=json.dumps(
            {
                # "model": "nvidia/llama-3.1-nemotron-70b-instruct:free",
                # "model": "nvidia/llama-3.1-nemotron-nano-8b-v1:free",
                "model": "nvidia/llama-3.1-nemotron-ultra-253b-v1:free",
                "messages": [{"role": "user", "content": prompt}],
            }
        ),
    )
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        result = response.json()
        # Extract the model's output
        model_output = (
            result.get("choices", [{}])[0].get("message", {}).get("content", "")
        )
        return model_output
    else:
        print(f"Error: {response.status_code}")
        return None
