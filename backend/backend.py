import csv, json, uuid, pandas as pd, sys, os, random
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# Allows us to grab model module from sibling directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../model')))
from model import generate_response

def has_header(csv_file):
    with open(csv_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            first_row = next(reader)
            return not any(first_row)
        except StopIteration:
            return True

def generate_iso_date():
    random_days = random.randint(0, 365 * 5)
    random_time = timedelta(days=random_days)
    random_date = datetime.now() - random_time
    return random_date.strftime("%a %b %d %H:%M:%S +0000 %Y")

def generate_iso_date_increment(prev_date):
    original_date = datetime.strptime(prev_date, "%a %b %d %H:%M:%S +0000 %Y")
    random_days = random.randint(1, 30)
    random_months = random.randint(1, 12)
    new_date = original_date + relativedelta(months=random_months) + timedelta(days=random_days)
    return new_date.strftime("%a %b %d %H:%M:%S +0000 %Y")

def load_csv_data(file_name):
    df = pd.read_csv(file_name, header=None, encoding="utf-8")
    return df[0].tolist()

def build_prompt(threat_type, prompts, profiles, tones, malicious_scenarios, medical_scenarios):
    prompt_dict = dict(zip(prompts[0::2], prompts[1::2]))
    
    if threat_type.lower() == "normal":
        return prompt_dict["Normal"]
    
    profile = random.choice(profiles)
    tone = random.choice(tones)
    
    if threat_type.lower() == "malicious":
        scenario = random.choice(malicious_scenarios)
        prompt = prompt_dict["Malicious"] + f"\n- Scenario: {scenario}\n- Character Profile: {profile}\n- Desired Tone: {tone}"
    elif threat_type.lower() == "medical":
        scenario = random.choice(medical_scenarios)
        prompt = prompt_dict["Medical"] + f"\n- Scenario: {scenario}\n- Character Profile: {profile}\n- Desired Tone: {tone}"
    else:
        raise ValueError("Invalid threat type. Please choose 'malicious', 'medical', or 'normal'.")
    
    return prompt

def generate_tweets(dest, num_tweets, threat_types):
    # Load data from new CSV files
    profiles = load_csv_data("character_profiles.csv")
    tones = load_csv_data("tones.csv")
    malicious_scenarios = load_csv_data("malicious_scenarios.csv")
    medical_scenarios = load_csv_data("medical_scenarios.csv")
    prompts = load_csv_data("prompts.csv")

    tweets = []
    for threat_type in threat_types:
        for i in range(num_tweets):
            tweet_id = uuid.uuid4().int
            user_id = uuid.uuid4().int
            created_at = generate_iso_date()

            prompt = build_prompt(threat_type.lower(), prompts, profiles, tones, malicious_scenarios, medical_scenarios)

            tweet_response = generate_response(prompt)
            username_response = generate_response("Only generate a random twitter username")

            print(username_response)

            tweet_object = {
                "id": tweet_id,
                "id_str": str(tweet_id),
                "created_at": created_at,
                "text": tweet_response,
                "user": {
                    "id": user_id,
                    "id_str": str(user_id),
                    "name": username_response,
                    "screen_name": str(username_response.replace(" ", ""))
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
            if has_header(dest):
                writer.writeheader()
            writer.writerows(tweets)
    
    return 1

def generate_timeseries_tweets(dest, num_tweets, threat_types):
    # Load data from CSV files
    profiles = load_csv_data("character_profiles.csv")
    tones = load_csv_data("tones.csv")
    malicious_scenarios = load_csv_data("malicious_scenarios.csv")
    medical_scenarios = load_csv_data("medical_scenarios.csv")
    prompts = load_csv_data("prompts.csv")

    # Hardcode tone pools for Stages 1 and 3 to ensure positive/neutral
    stage1_tones = ["Casual"]  # Stage 1: Positive or neutral
    stage2_tones = ["Frustrated", "Nervous", "Exhausted", "Angry"]  # Stage 2: Stressful tones
    stage3_tones = ["Casual"]  # Stage 3: Neutral recovery

    tweets = []
    for threat_type in threat_types:
        if threat_type.lower() == "normal":
            # Standalone normal tweets
            prompt = build_prompt("normal", prompts, profiles, tones, malicious_scenarios, medical_scenarios)
            for i in range(num_tweets):
                tweet_id = uuid.uuid4().int
                user_id = uuid.uuid4().int
                created_at = generate_iso_date()
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
        else:
            # Time series for malicious or medical
            for _ in range(num_tweets):
                profile = random.choice(profiles)  # Consistent across stages
                user_id = uuid.uuid4().int
                stages = [
                    ("Generate a short, conversational tweet about enjoying work", random.choice(stage1_tones)),
                    ("Generate a short, conversational tweet hinting at workplace stress or frustration", random.choice(stage2_tones)),
                    ("Generate a short, conversational tweet about feeling better at work", random.choice(stage3_tones)),
                    (build_prompt(threat_type.lower(), prompts, [profile], tones, malicious_scenarios, medical_scenarios), None)
                ]
                
                for i in range(4):
                    tweet_id = uuid.uuid4().int
                    if i == 0:
                        created_at = generate_iso_date()
                    else:
                        created_at = generate_iso_date_increment(tweets[-1]["created_at"])
                    
                    prompt = stages[i][0]
                    if i < 3:  # Add tone and profile for Stages 1-3
                        prompt += f"\n- Character Profile: {profile}\n- Desired Tone: {stages[i][1]}"
                    else:  # Stage 4 already includes profile and tone
                        pass
                    
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
                        "threat_type": f"{threat_type}_stage_{i+1}",
                        "user_json": json.dumps(tweet_object["user"]),
                        "tweet_schema": json.dumps(tweet_object),
                        "user_id": tweet_object["user"]["id"],
                        "user_id_str": tweet_object["user"]["id_str"],
                        "user_name": tweet_object["user"]["name"],
                        "screen_name": tweet_object["user"]["screen_name"]
                    })
    
    with open(dest, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=tweets[0].keys())
        if has_header(dest):
            writer.writeheader()
        writer.writerows(tweets)
    
    return 1

# Example usage
if __name__ == "__main__":
    generate_tweets("tweets_output.csv", 2, ["Malicious", "Medical", "Normal"])
    generate_timeseries_tweets("timeseries_tweets.csv", 1, ["Medical", "Malicious"])
