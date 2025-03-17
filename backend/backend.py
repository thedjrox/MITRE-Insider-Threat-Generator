import csv, json, uuid, pandas as pd, sys, os, random
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import re
import names

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../model")))
from model import generate_response


def has_header(csv_file):
    with open(csv_file, "r", newline="", encoding="utf-8") as f:
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
    new_date = (
        original_date
        + relativedelta(months=random_months)
        + timedelta(days=random_days)
    )
    return new_date.strftime("%a %b %d %H:%M:%S +0000 %Y")


def load_csv_data(file_name):
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(dir_path, file_name)

    df = pd.read_csv(file_path, header=0, encoding="utf-8")

    if "Definition - Sheet1.csv" in file_name:
        return df.iloc[0].to_dict()  # Return as dict for definitions
    else:
        if df.empty:
            raise ValueError(f"{file_name} is empty!")
        return df.iloc[:, 0].dropna().tolist()  # Return as list for others


def build_prompt(
    threat_type, definitions, profiles, tones, malicious_scenarios, medical_scenarios
):
    # Base prompt templates
    prompt_templates = {
        "Malicious": "Generate a malicious tweet that subtly hints at an insider threat based on the information I provided below. Return just the tweet text and do not include an analysis breakdown.",
        "Medical": "Generate a medical tweet that subtly hints at an insider threat based on the information below, with a subtle clue to a medical condition but without stating it directly. Return only the tweet text and do not include an analysis breakdown.",
        "Normal": "Generate a short, conversational tweet about something random that's not an insider threat. Return only the tweet text and do not include an analysis breakdown.",
    }

    if threat_type not in prompt_templates:
        raise ValueError(
            f"Invalid threat_type '{threat_type}'. Only 'Normal', 'Medical', and 'Malicious' are allowed."
        )

    if threat_type == "Normal":
        return prompt_templates["Normal"]

    # Load definition from CSV
    definition = definitions[threat_type]

    # Randomly select attributes from provided data
    profile = random.choice(profiles)
    tone = random.choice(tones)

    if threat_type == "Malicious":
        scenario = random.choice(malicious_scenarios)
        prompt = (
            f"{prompt_templates['Malicious']}\n"
            f"- Definition: {definition}\n"
            f"- Scenario: {scenario}\n"
            f"- Character Profile: {profile}\n"
            f"- Desired Tone: {tone}"
        )
    elif threat_type == "Medical":
        scenario = random.choice(medical_scenarios)
        prompt = (
            f"{prompt_templates['Medical']}\n"
            f"- Definition: {definition}\n"
            f"- Scenario: {scenario}\n"
            f"- Character Profile: {profile}\n"
            f"- Desired Tone: {tone}"
        )

    return prompt


def extract_after_first_quote(cell_value):
    match = re.search(r'"(.*?)"', cell_value)
    return match.group(1) if match else None


def generate_tweets(dest, num_tweets, threat_types):
    # Load required CSV data
    definitions = load_csv_data("Definition - Sheet1.csv")
    profiles = load_csv_data("Character Profile - Sheet1.csv")
    tones = load_csv_data("Desired Tone - Sheet1.csv")
    malicious_scenarios = load_csv_data("Malicious Scenario - Sheet1.csv")
    medical_scenarios = load_csv_data("Medical Scenario - Sheet1.csv")

    tweets = []
    for threat_type in threat_types:
        for i in range(num_tweets):
            tweet_id = uuid.uuid4().int
            user_id = uuid.uuid4().int
            created_at = generate_iso_date()

            prompt = build_prompt(
                threat_type,
                definitions,
                profiles,
                tones,
                malicious_scenarios,
                medical_scenarios,
            )
            tweet_response = generate_response(prompt)
            # username_response = generate_response(
            #     "Generate a random Twitter username starting with '@' (max 15 characters). Return only the username."
            # )
            username_response = names.get_full_name()
            random_number = random.randint(1, 49)
            just_name = str(username_response.replace(" ", ""))
            # just_tweet = re.search(r'"(.*?)"', tweet_response).group(1)
            just_tweet = extract_after_first_quote(tweet_response)

            tweet_object = {
                "id": tweet_id,
                "id_str": str(tweet_id),
                "created_at": created_at,
                "text": just_tweet,
                "user": {
                    "id": user_id,
                    "id_str": str(user_id),
                    # "name": username_response,
                    "name": f"@{just_name}{random_number}",
                    "screen_name": f"@{just_name}{random_number}",
                },
            }

            tweets.append(
                {
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
                    "screen_name": tweet_object["user"]["screen_name"],
                }
            )

    with open(dest, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=tweets[0].keys())
        if has_header(dest):
            writer.writeheader()
        writer.writerows(tweets)

    return 1


def generate_timeseries_tweets(dest, num_tweets, threat_types):
    # Load required CSV data
    definitions = load_csv_data("Definition - Sheet1.csv")
    profiles = load_csv_data("Character Profile - Sheet1.csv")
    tones = load_csv_data("Desired Tone - Sheet1.csv")
    malicious_scenarios = load_csv_data("Malicious Scenario - Sheet1.csv")
    medical_scenarios = load_csv_data("Medical Scenario - Sheet1.csv")

    stage1_tones = ["Casual"]
    stage2_tones = ["Frustrated", "Nervous", "Exhausted", "Angry"]
    stage3_tones = ["Casual"]

    tweets = []
    for threat_type in threat_types:
        if threat_type == "Normal":
            prompt = build_prompt(
                "Normal",
                definitions,
                profiles,
                tones,
                malicious_scenarios,
                medical_scenarios,
            )
            dates = []
            for i in range(num_tweets):
                tweet_id = uuid.uuid4().int
                user_id = uuid.uuid4().int

                if i == 0:
                    created_at = generate_iso_date()
                    dates.append(created_at)
                else:
                    created_at = generate_iso_date_increment(dates[i - 1])
                    dates.append(created_at)

                tweet_response = generate_response(prompt)
                # username_response = generate_response(
                #     "Generate a random Twitter username starting with '@' (max 15 characters). Return only the username."
                # )
                username_response = names.get_full_name()
                random_number = random.randint(1, 49)
                just_name = str(username_response.replace(" ", ""))
                just_tweet = extract_after_first_quote(tweet_response)
                tweet_object = {
                    "id": tweet_id,
                    "id_str": str(tweet_id),
                    "created_at": created_at,
                    "text": just_tweet,
                    "user": {
                        "id": user_id,
                        "id_str": str(user_id),
                        # "name": username_response,
                        "name": f"@{just_name}{random_number}",
                        "screen_name": f"@{just_name}{random_number}",
                    },
                }
                tweets.append(
                    {
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
                        "screen_name": tweet_object["user"]["screen_name"],
                    }
                )
        else:
            for _ in range(num_tweets):
                profile = random.choice(profiles)
                user_id = uuid.uuid4().int
                stages = [
                    (
                        "Generate a short, conversational tweet about enjoying work",
                        random.choice(stage1_tones),
                    ),
                    (
                        "Generate a short, conversational tweet hinting at workplace stress or frustration",
                        random.choice(stage2_tones),
                    ),
                    (
                        "Generate a short, conversational tweet about feeling better at work",
                        random.choice(stage3_tones),
                    ),
                    (
                        build_prompt(
                            threat_type,
                            definitions,
                            [profile],
                            tones,
                            malicious_scenarios,
                            medical_scenarios,
                        ),
                        None,
                    ),
                ]

                tweet_id = uuid.uuid4().int
                # username_response = generate_response(
                #     "Generate a random Twitter username starting with '@' (max 15 characters). Return only the username."
                # )
                username_response = names.get_full_name()
                random_number = random.randint(1, 49)
                just_name = str(username_response.replace(" ", ""))
                dates = []
                for i in range(4):
                    if i == 0:
                        created_at = generate_iso_date()
                        dates.append(created_at)
                    else:
                        created_at = generate_iso_date_increment(dates[i - 1])
                        dates.append(created_at)

                    prompt = stages[i][0]
                    if i < 3:
                        prompt += f"\n- Character Profile: {profile}\n- Desired Tone: {stages[i][1]}"

                    tweet_response = generate_response(prompt)
                    just_tweet = extract_after_first_quote(tweet_response)

                    tweet_object = {
                        "id": tweet_id,
                        "id_str": str(tweet_id),
                        "created_at": created_at,
                        "text": just_tweet,
                        "user": {
                            "id": user_id,
                            "id_str": str(user_id),
                            # "name": username_response,
                            "name": f"@{just_name}{random_number}",
                            "screen_name": f"@{just_name}{random_number}",
                        },
                    }

                    tweets.append(
                        {
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
                            "screen_name": tweet_object["user"]["screen_name"],
                        }
                    )

    with open(dest, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=tweets[0].keys())
        if has_header(dest):
            writer.writeheader()
        writer.writerows(tweets)

    return 1


if __name__ == "__main__":
    # Example usage
    generate_tweets("test9_tweets_output.csv", 5, ["Malicious", "Medical", "Normal"])
    # generate_tweets("tweets_output.csv", 2, ["Malicious", "Medical", "Normal"])
    # generate_timeseries_tweets("timeseries_tweets.csv", 1, ["Medical", "Malicious", "Normal"])
