import argparse
from transformers import pipeline
import torch
import random
import csv
import json
import uuid
import pandas as pd


model_id = "meta-llama/Llama-3.2-3B-Instruct"

parser = argparse.ArgumentParser(description="Script to process threat types.")

parser.add_argument(
    "--threat_type",
    type=str,
    choices=["malicious", "medical", "normal"],
    required=True,
    help="Specify the type of threat: 'malicious', 'medical', or 'normal'."
)

parser.add_argument(
    "--number_tweets",
    type=int,
    required=True,
    help="Specify number of tweets to generate."
)

parser.add_argument(
    "--time_or_single",
    type=str,
    choices=["time", "single"],
    required=True,
    help="Specify wether time series or single"
)

args = parser.parse_args()

tweet_object = {
    "created_at": None, #created_at
    "id": 0, #tweet_id
    "id-str": "", #tweet_id_str
    "text": "", #tweet
    "user": {
        "id": 0, #user_id
        "id-str": "", #user_id_str
        "name": "", #screen_name
        "screen_name": "" #screen_name
    }
}

'''
created_at = "" #GENERATE FROM AI MODEL
tweet_id = 0
tweet_id_str = ""
tweet = "" #GENERATE FROM AI MODEL
type_tweet = args.threat_type
user_id = 0
user_id_str = ""
name="" #GENERATE FROM AI MODEL
screen_name = "" #name without spaces
'''

# Load scenarios from CSV file (assuming it's in the same directory as the script)
csv_file = "Prompt Characteristics - Sheet1"
df = pd.read_csv(csv_file, encoding = "utf-8")

#Function to randomly select a scenario and characteristic based on threat type
def select_scenario(threat_type):
    if threat_type == "medical":
        scenarios = df[["Scenario_Description", "Medical_Issue"]].dropna().values.tolist()
    elif threat_type == "malicious":
        scenarios = df[["Scenario_Description", "Malicious_Characteristics"]].dropna().values.tolist()
    else:
        return "a normal tweet."

    selected_scenario = random.choice(scenarios)
    return selected_scenario


pipe = pipeline(
    "text-generation",
    model=model_id,
    device="cpu",  # Forces CPU usage
    torch_dtype=torch.float16,  # float16 is more compatible across devices
)

if(args.time_or_single == "single"):
    i = 0
    while i < args.number_tweets:
        tweet_object["tweet_id"] = uuid.uuid4()
        tweet_object["user"]["user_id"] = uuid.uuid4()
        tweet_object["tweet_id_str"] = str(tweet_object["tweet_id"])
        tweet_object["user"]["user_id_str"] = str(tweet_object["user"]["user_id"])

        #Generate created_at, Tweet, and username in here for each tweet
        prompt = f"only generate a created_at value for a tweet object"
        tweet_object["created_at"] = pipe(prompt, max_new_tokens=50)

        prompt = f"only generate a username for a twitter account"
        tweet_object["user"]["name"] = pipe(prompt, max_new_tokens=20)

        if(" " in tweet_object["name"]):
            tweet_object["user"]["screen_name"] = tweet_object["user"]["name"].replace(" ", "")
        else:
            tweet_object["user"]["screen_name"] = tweet_object["user"]["name"]

        tweet_scenario = select_scenario(args.threat_type)
        prompt = f"Only generate a tweet based of this scenario {tweet_scenario}"
        tweet = pipe(prompt, max_new_tokens=185)

        user_JSON = json.dumps(tweet_object["user"])
        tweet_JSON = json.dumps(tweet_object)
        #APPEND DATA TO CSV FILE DOWN HERE
        with open("generated_tweets.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                tweet_object["created_at"],
                tweet_object["id"],
                tweet_object["id_str"],
                tweet_object["text"],
                user_object
                args.threat_type
                tweet_JSON
        ])

        i += 1

    


