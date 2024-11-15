import argparse
from transformers import pipeline
import torch
import random
import csv
import json
import uuid
import pandas as pd

# Load Model and Setup Arguments
model_id = "meta-llama/Llama-3.2-3B-Instruct"
parser = argparse.ArgumentParser(description="Script to process threat types.")
parser.add_argument("--threat_type", type=str, choices=["malicious", "medical", "normal"], required=True)
parser.add_argument("--number_tweets", type=int, required=True)
parser.add_argument("--time_or_single", type=str, choices=["time", "single"], required=True)
args = parser.parse_args()

# Setup Scenario Data and Pipeline
csv_file = "Prompt Characteristics - Sheet1.csv"
df = pd.read_csv(csv_file, encoding="utf-8")
pipe = pipeline("text-generation", model=model_id, device="cpu", torch_dtype=torch.float32)

# Function to Select Scenario Based on Threat Type
def select_scenario(threat_type):
    if threat_type == "medical":
        scenarios = df[["Scenario_Description", "Medical_Issue"]].dropna().values.tolist()
    elif threat_type == "malicious":
        scenarios = df[["Scenario_Description", "Malicious_Characteristics"]].dropna().values.tolist()
    else:
        return "a normal tweet."
    return random.choice(scenarios)

created_at_prompt = [{"role": "user", "content": "Only create a random date in ISO 8601 format"}]
#text_prompt = [{"role": "user", "content": f"Only generate a normal tweet about something random without starting the tweet with Just"}]
text_prompt = [{"role": "user", "content": f"Only generate one tweet based on this scenario nothing else: {select_scenario(args.threat_type)}."}]
user_name_prompt = [{"role": "user", "content": "Only generate a random twitter username."}]

# Main Loop for Tweet Generation
tweets_data = []
for i in range(args.number_tweets):
    tweet_id = uuid.uuid4().int
    user_id = uuid.uuid4().int
    # Prepare the messages for the pipeline input

    created_at_output = pipe(created_at_prompt, max_new_tokens=20, temperature=0.9, top_k=50,top_p=0.95)
    created_at = created_at_output[0]["generated_text"][1]["content"]  # Access generated_text and strip

    print(created_at)
    tweet_text_output = pipe(text_prompt, max_new_tokens=150, temperature=0.9, top_k=50,top_p=0.95)
    tweet_text = tweet_text_output[0]["generated_text"][1]["content"]  # Access generated_text and strip

    user_name_output = pipe(user_name_prompt, max_new_tokens=20, temperature=0.9, top_k=50,top_p=0.95)
    user_name = user_name_output[0]["generated_text"][1]["content"] # Access generated_text and strip


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

    tweet_schema = json.dumps(tweet_object)
    user_json = json.dumps(tweet_object["user"])
    
    # Append Tweet Data
    tweets_data.append({
        "created_at": tweet_object["created_at"],
        "tweet_id": tweet_object["id"],
        "tweet_id_str": tweet_object["id_str"],
        "tweet": tweet_object["text"],
        "threat_type": args.threat_type,
        "user_json": user_json,
        "tweet_schema": tweet_schema,
        "user_id": tweet_object["user"]["id"],
        "user_id_str": tweet_object["user"]["id_str"],
        "user_name": tweet_object["user"]["name"],
        "screen_name": tweet_object["user"]["screen_name"]
    })

# Write to CSV All at Once
with open("generated_tweets.csv", mode="a", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=tweets_data[0].keys())
    writer.writeheader()
    writer.writerows(tweets_data)

