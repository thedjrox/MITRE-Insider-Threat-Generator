from transformers import pipeline
import torch
import random
import csv
import json
import uuid
import pandas as pd
from datetime import datetime, timedelta

# Load Model and Setup Arguments
model_id = "meta-llama/Llama-3.2-3B-Instruct"
model, tokenizer = load_model(model_id)

# Function to generate tweets
def generate_tweets(destination, num_tweets, generation_type, threat_types):
    # Setup Scenario Data and Pipeline
    csv_file = "Time Series Scenarios - Sheet1.csv"
    df = pd.read_csv(csv_file, encoding="utf-8")
    pipe = pipeline("text-generation", model=model_id, device="cpu", torch_dtype=torch.float32)

    # Main Loop for Tweet Generation
    tweets_data = []
    for threat_type in threat_types:
        for i in range(num_tweets):
            tweet_id = uuid.uuid4().int
            user_id = uuid.uuid4().int
            created_at = generate_iso_date()
            
            if threat_type.lower() == "normal":
                text_prompt = [{"role": "user", "content": "Only generate a normal tweet about something random without starting the tweet with Just"}]
            else:
                scenario = select_scenario(threat_type.lower())
                text_prompt = [{"role": "user", "content": f"Only generate one tweet based on this scenario nothing else: {scenario}."}]
            
            tweet_text_output = pipe(text_prompt, max_new_tokens=150, temperature=0.9, top_k=50, top_p=0.95)
            tweet_text = tweet_text_output[0]["generated_text"][1]["content"]  

            user_name_output = pipe([{"role": "user", "content": "Only generate a random twitter username."}], max_new_tokens=20, temperature=0.9, top_k=50, top_p=0.95)
            user_name = user_name_output[0]["generated_text"][1]["content"]

            # Construct the tweet object
            tweet_object = {
                "id": tweet_id,
                "id_str": str(tweet_id),
                "created_at": created_at,
                "text": tweet_text,
                "user": {
                    "id": user_id,
                    "id_str": str(user_id),
                    "name": user_name,
                    "screen_name": user_name.replace(" ", "")
                }
            }

            # Append Tweet Data
            tweets_data.append({
                "created_at": tweet_object["created_at"],
                "tweet_id": tweet_object["id"],
                "tweet_id_str": tweet_object["id_str"],
                "tweet": tweet_object["text"],
                "threat_type": threat_type,
                "user_json": json.dumps(tweet_object["user"]),
                "tweet_schema": json.dumps(tweet_object),
                "user_id": tweet_object["user"]["id"],
                "user_id_str": tweet_object["user"]["id_str"],
                "user_name": tweet_object["user"]["name"],
                "screen_name": tweet_object["user"]["screen_name"]
            })

    # Write to CSV
    with open(destination, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=tweets_data[0].keys())
        writer.writeheader()
        writer.writerows(tweets_data)

# Helper functions (e.g., select_scenario, generate_iso_date, etc.) remain unchanged