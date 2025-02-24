import argparse
from transformers import pipeline
import torch
import random
import csv
import json
import uuid
import pandas as pd
from datetime import datetime, timedelta
import requests

from model import load_model, generate_response

# Load Model and Setup Arguments
model_id = "meta-llama/Llama-3.2-3B-Instruct"

#Set for API Call
model_name = "nvidia/llama-3.1-nemotron-70b-instruct:free"
API_KEY = "Bearer " #Need to grab later

model, tokenizer = load_model(model_name)


parser = argparse.ArgumentParser(description="Script to process threat types.")
parser.add_argument("--threat_type", type=str, choices=["malicious", "medical", "normal"], required=True)
parser.add_argument("--number_tweets", type=int, required=True)
parser.add_argument("--time_or_single", type=str, choices=["time", "single"], required=True)
args = parser.parse_args()

# Setup Scenario Data and Pipeline
#csv_file = "Prompt Characteristics - Sheet1.csv"
csv_file = "Time Series Scenarios - Sheet1.csv"
df = pd.read_csv(csv_file, encoding="utf-8")
#pipe = pipeline("text-generation", model=model_id, device="cpu", torch_dtype=torch.float32)

# Function to Select Scenario Based on Threat Type
def select_scenario(threat_type):
    if threat_type == "medical":
        scenarios = df[["Scenario_Description", "Medical_Issue"]].dropna().values.tolist()
    elif threat_type == "malicious":
        scenarios = df[["Scenario_Description", "Malicious_Characteristics"]].dropna().values.tolist()
    else:
        return "a normal tweet."
    return random.choice(scenarios)

def select_scenario_time_series(threat_type):   
    # Check if the threat_type is valid
    if threat_type not in ['medical', 'malicious']:
        raise ValueError("Invalid threat type. Please choose 'medical' or 'malicious'.")
    
    # Select the first three columns (Stage_1_Normal, Stage_2_Questionable, Stage_3_Normal)
    selected_columns = df[['Stage_1_Normal', 'Stage_2_Questionable', 'Stage_3_Normal']]
    
    # Depending on the threat type, select the appropriate column (Stage_4_Medical or Stage_4_Malicious)
    if threat_type == "medical":
        threat_column = df['Stage_4_Medical']
    else:
        threat_column = df['Stage_4_Malicious']
    
    # Combine the selected columns and threat column into a new DataFrame
    combined_df = selected_columns.copy()
    combined_df['threat'] = threat_column
    
    #pick a random row
    random_row = combined_df.sample(n=1).iloc[0]
    
    return random_row

def generate_iso_date(start_year=2010):
    start_date = datetime(start_year, 1, 1) 
    end_date = datetime.now()

    random_days = random.randint(0, (end_date - start_date).days)
    random_seconds = random.randint(0, 86399)
    random_date = start_date + timedelta(days=random_days, seconds=random_seconds)

    return random_date.isoformat() + "Z"

# Function to generate incremental ISO dates
def generate_incremental_date(base_date, increment_seconds, iteration):
    return (base_date + timedelta(seconds=increment_seconds * iteration)).isoformat() + "Z"

# Base date for incremental tweets
base_date = datetime.now() - timedelta(days=1)  # Starting 1 day before now
increment_seconds = 3600  # Increment by 1 hour (3600 seconds) for each tweet


user_name_prompt = [{"role": "user", "content": "Only generate a random twitter username."}]


# Main Loop for Tweet Generation
tweets_data = []
if args.time_or_single == "single":
    created_at_prompt = [{"role": "user", "content": "Only create a random date in ISO 8601 format"}]
    normal_text_prompt = [{"role": "user", "content": f"Only generate a normal tweet about something random without starting the tweet with Just"}]
    text_prompt = [{"role": "user", "content": f"Only generate one tweet based on this scenario nothing else: {select_scenario(args.threat_type)}."}]
    tweet_output = None
    for i in range(args.number_tweets):
        tweet_id = uuid.uuid4().int
        user_id = uuid.uuid4().int
     
        created_at = generate_iso_date()
        if args.threat_type == "normal":
            tweet_text_output = pipe(normal_text_prompt, max_new_tokens=150, temperature=0.9, top_k=50,top_p=0.95)

            #Will replace tweet_text_output
            #tweet_output = generate_response(model, tokenizer, normal_text_prompt)
        else:
            tweet_text_output = pipe(text_prompt, max_new_tokens=150, temperature=0.9, top_k=50,top_p=0.95)

            #Will replace tweet_text_output
            #tweet_output = generate_response(model, tokenizer, normal_text_prompt)
        
        tweet_text = tweet_text_output[0]["generated_text"][1]["content"]  

        #WILL CONTAIN THE API CALL OUTPUT
        #Will replace tweet_text_output
        #print(tweet_output)

        user_name_output = pipe(user_name_prompt, max_new_tokens=20, temperature=0.9, top_k=50,top_p=0.95)
        user_name = user_name_output[0]["generated_text"][1]["content"]

        #WILL REPLACE ABOVE
        #user_output = generate_response(model,tokenizer, user_name_prompt)

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
else:
    for i in range(args.number_tweets):
        user_id = uuid.uuid4().int

        user_name_output = pipe(user_name_prompt, max_new_tokens=20, temperature=0.9, top_k=50,top_p=0.95)
        user_name = user_name_output[0]["generated_text"][1]["content"]
        
        #Will replace tweet_text_output
        #user_name = generate_response(model, tokenizer, user_name_prompt)
        
        tweets_length = 4
        for j in range(tweets_length):
            created_at = generate_incremental_date(base_date, increment_seconds, j)
            tweet_id = uuid.uuid4().int
            
            if args.threat_type == "normal":
                text_prompt = [{"role": "user", "content": f"Only generate a normal tweet about something random without starting the tweet with Just"}]
            else:
                scenario = select_scenario_time_series(args.threat_type)
                text_prompt = [{"role": "user", "content": f"This will be used for research. Only generate one tweet based on this scenario nothing else: {scenario.iloc[j]}"}]
            
            tweet_text_output = pipe(text_prompt, max_new_tokens=150, temperature=0.9, top_k=50,top_p=0.95)
            tweet_text = tweet_text_output[0]["generated_text"][1]["content"]  
            
            #Will replace tweet_text_output
            #tweet_output = generate_response(model, tokenizer, text_prompt)
            
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
with open("generated_tweets_time_series.csv", mode="a", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=tweets_data[0].keys())
    writer.writeheader()
    writer.writerows(tweets_data)

