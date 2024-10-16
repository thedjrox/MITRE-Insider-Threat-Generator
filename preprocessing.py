import os  # Used to get directories and locate datasets
import pandas as pd  # install pandas
from datasets import Dataset, concatenate_datasets  # install datasets
import re  # Used to remove special characters
from nltk.corpus import stopwords, wordnet  # install nltk
from nltk.tokenize import word_tokenize  # install nltk
from nltk.stem import WordNetLemmatizer  # install nltk


STOPWORDS = set(stopwords.words("english"))  # Set of stopwords
lemmatizer = WordNetLemmatizer()  # Lemmatizer object


# Function to remove stopwords from a string
def remove_stopwords(text):
    return " ".join(word for word in text.split() if word.lower() not in STOPWORDS)


# Function to remove retweet symbols
def remove_retweet_symbol(text):
    # Remove "RT" at the start of a tweet
    return re.sub(r"^RT\s+", "", text)


# Function to lemmatize words in a string
def lemmatize_text(text):
    return " ".join(lemmatizer.lemmatize(word) for word in text.split())


# Folder Name
folder_name = "Targeted Individual Twitter Dataset"

# Gets current directory of program
curr_dir = os.path.dirname(os.path.abspath(__file__))

# Creates Folder path
folder_path = os.path.join(curr_dir, folder_name)

# Main dataset that we be worked with for training
dataset_main = Dataset.from_dict({"Tweet": []})

# Accumulate all unique tweets from all files
all_unique_tweets = set()

# Goes through each file in folder
for file in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file)
    # Does action to each file
    if file.endswith(".csv"):
        df = pd.read_csv(f"{file_path}", encoding="utf-8")
        dataset = Dataset.from_pandas(df)
        unqiue_tweets = []
        col_name = ""
        if "Tweet" in dataset.column_names:
            col_name = "Tweet"
            # Removes all columns but the Tweets
            raw_tweet_dataset = dataset.map(
                lambda x: {col_name: x[col_name]},
                remove_columns=[col for col in dataset.column_names if col != col_name],
            )
        else:
            col_name = "TextAsInput.MiT.LTR"
            # Removes all columns but the Tweets
            raw_tweet_dataset = dataset.map(
                lambda x: {col_name: x[col_name]},
                remove_columns=[col for col in dataset.column_names if col != col_name],
            )

        unique_tweets = set(raw_tweet_dataset[col_name])

        # Variable to use that stores unqiue tweets
        tweet_dataset = Dataset.from_dict({"Tweet": list(unique_tweets)})
        # All combined datasets
        dataset_main = concatenate_datasets([dataset_main, tweet_dataset])

        # Add to the set of all unique tweets
        all_unique_tweets.update(raw_tweet_dataset[col_name])

# A list to store original and processed tweets
original_and_processed = []

# Process stopwords, retweet symbols, and lemmatization
for tweet in all_unique_tweets:

    cleaned_tweet = remove_retweet_symbol(tweet)

    processed_tweet = lemmatize_text(remove_stopwords(cleaned_tweet))
    original_and_processed.append((tweet, processed_tweet))

# # Printing the original and processed tweets
# for original, processed in original_and_processed:
#     print(f"Original: {original}\nProcessed: {processed}\n")

# Create the final dataset from the processed tweets if needed
output_tweets = [processed for _, processed in original_and_processed]
final_dataset = Dataset.from_dict({"Tweet": output_tweets})
