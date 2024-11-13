import argparse
from transformers import pipeline
import torch
import random

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
    "created_at": None,
    "id": 0,
    "id-str": "",
    "text": "",
    "user": {}
}

created_at = "" #GENERATE FROM AI MODEL
tweet_id = 0
tweet_id_str = ""
tweet = "" #GENERATE FROM AI MODEL
type_tweet = args.threat_type
screen_name = "" #GENERATE FROM AI MODEL

if(args.time_or_single == "single"):
    i = 0
    while i < args.number_tweets:
        tweet_id = random_number = random.randint(0, 10000000)
        tweet_id_str = str(tweet_id)
        #Generate created_at and Tweet in here for each tweet


#This is how you generate stuff
pipe = pipeline(
    "text-generation",
    model=model_id,
    device="cpu",  # Forces CPU usage
    torch_dtype=torch.float16,  # float16 is more compatible across devices
)

prompt = f"Write a tweet that impersonates a {args.threat_type} insider threat."
response = pipe(prompt, max_new_tokens=185)
print(response[0]["generated_text"])


