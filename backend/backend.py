import csv, json, uuid, pandas as pd, sys, os, random
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model import generate_response

def generate_iso_date():
    # Generate a random date in the past 5 years
    random_days = random.randint(0, 365 * 5)
    random_time = timedelta(days=random_days)
    random_date = datetime.now() - random_time
    
    # Format the date similar to "Wed Oct 10 20:19:24 +0000 2018"
    return random_date.strftime("%a %b %d %H:%M:%S +0000 %Y")

def select_scenario(threat_type):
    csv_file_name = "Prompt Characteristics - Sheet1.csv"
    df = pd.read_csv(csv_file_name, encodeing="utf-8")
    
    if threat_type == "medical":
        scenarios = df[["Scenario_Description", "Medical_Issue"]].dropna().values.tolist()
    elif threat_type == "malicious":
        scenarios = df[["Scenario_Description", "Malicious_Characteristics"]].dropna().values.tolist()
    else:
        return "a normal tweet."
    return random.choice(scenarios)

def select_scenario_time_series(threat_type):   
    csv_file_name = "Time Series Scenarios - Sheet1.csv"
    df = pd.read_csv(csv_file_name, encodeing="utf-8")
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


def generate_tweets(dest, num_tweets, threat_types):
    tweets = []
    for threat_type in threat_types:
        for _ in range(num_tweets):
            tweet_id = uuid.uuid4().int
            user_id = uuid.uuid4().int
            created_at = generate_iso_date()

            if threat_type.lower() == "normal":
                prompt = "Only generate a normal tweet about something random"
            else:
                scenario = select_scenario(threat_type.lower())
                prompt = f"Only generate one tweet based on this scenario nothing else: {scenario}."

            tweet_response = generate_response(prompt)
            username_response = generate_response("Only generate a random twitter username")

            tweet_object = {
                "id": tweet_id,
                "id_str": str(tweet_id),
                "created_at": created_at,
                "text": tweet_response,
                "user": {
                    "id": user_id,
                    "id_str": str(user_id),
                    "name": username_response,
                    "screen_name": username_response.replace(" ", "")
                }
            }

            tweets.append({
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

            with open(dest, mode="a", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=tweets[0].keys())
                writer.writeheader()
                writer.writerows(tweets)

