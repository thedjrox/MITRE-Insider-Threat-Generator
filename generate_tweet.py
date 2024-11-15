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

# Main Loop for Tweet Generation
tweets_data = []
for i in range(args.number_tweets):
    tweet_id = uuid.uuid4()
    user_id = uuid.uuid4()
    tweet_object = {
        "id": tweet_id,
        "id_str": str(tweet_id)
        "created_at": pipe("Only generate a 'created_at' for a tweet object.", max_new_tokens=15)[0]["generated_text"].strip(),
        
        "text": pipe(f"Only generate a tweet based on this scenario: {select_scenario(args.threat_type)}", max_new_tokens=150)[0]["generated_text"].strip(),
        "user": {
            "id": user_id,
            "id_str": str(user_id)
            "name": pipe("Only generate a random username.", max_new_tokens=15)[0]["generated_text"].strip(),
            "screen_name": None
        }
    }
    tweet_object["user"]["screen_name"] = tweet_object["user"]["name"].replace(" ", "")
    tweet_schema = json.dumps(tweet_object)
    user_json = json.dumps(tweet_object["user"])
    # Append Tweet Data
    tweets_data.append({
        "created_at": tweet_object["created_at"],
        "tweet_id": tweet_object["id"],
        "tweet_id_str": tweet_object["id_str"]
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


    


