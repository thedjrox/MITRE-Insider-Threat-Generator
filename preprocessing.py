import os  # Used to get directories and locate datasets
import pandas as pd  # install pandas
from datasets import Dataset, concatenate_datasets  # install datasets
import re  # Used to remove special characters
from nltk.corpus import stopwords, wordnet  # install nltk
from nltk.tokenize import word_tokenize  # install nltk
from nltk.stem import WordNetLemmatizer  # install nltk
import string  # Used to remove punctuation
import emoji  # Used to remove emojis
import torch
from transformers import MarianMTModel, MarianTokenizer
import langid  # Used for language detection

# Load the model and tokenizer for translation
model_name = "Helsinki-NLP/opus-mt-mul-en"  # Multi-language to English model
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

STOPWORDS = set(stopwords.words("english"))  # Set of stopwords
lemmatizer = WordNetLemmatizer()  # Lemmatizer object

#translates tweet of any language to English using MarianMTModel
def translator(tweet):
    inputs = tokenizer(tweet, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        translated = model.generate(**inputs)
    translated_texts = tokenizer.batch_decode(translated, skip_special_tokens=True)
    return translated_texts[0]

# Function to check if the tweet is in English using langid
def is_english(text):
    lang, confidence = langid.classify(text)
    return lang == 'en'

# Function to remove stopwords from a string
def remove_stopwords(text):
    return " ".join(word for word in text.split() if word.lower() not in STOPWORDS)

# Function to remove retweet symbols
def remove_retweet_symbol(text):
    return re.sub(r"^RT\s+", "", text)

# Function to lemmatize words in a string
def lemmatize_text(text):
    return " ".join(lemmatizer.lemmatize(word) for word in text.split())

# Function to lowercase the text
def to_lowercase(text):
    return text.lower()

# Function to remove punctuation
def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))

# Function to remove emojis
def remove_emojis(text):
    return emoji.replace_emoji(text, replace="")

# Folder Name
folder_name = "Targeted Individual Twitter Dataset"

# Gets current directory of program
curr_dir = os.path.dirname(os.path.abspath(__file__))

# Creates Folder path
folder_path = os.path.join(curr_dir, folder_name)

# Main dataset that will be worked with for training
dataset_main = Dataset.from_dict({"Tweet": []})

# Accumulate all unique tweets from all files
all_unique_tweets = set()

# Goes through each file in folder
print(f'Looking for files in folder: {folder_path}')
files = os.listdir(folder_path)

# Ensure there are files in the directory
if len(files) > 0:
    first_file = files[0]  # Get the first file
    print(f"First file found: {first_file}")
    file_path = os.path.join(folder_path, first_file)

    # Does action to each file
    if first_file.endswith(".csv"):
        df = pd.read_csv(f"{file_path}", encoding="utf-8")
        dataset = Dataset.from_pandas(df)
        col_name = ""
        if "Tweet" in dataset.column_names:
            col_name = "Tweet"
            raw_tweet_dataset = dataset.map(
                lambda x: {col_name: x[col_name]},
                remove_columns=[col for col in dataset.column_names if col != col_name],
            )
        else:
            col_name = "TextAsInput.MiT.LTR"
            raw_tweet_dataset = dataset.map(
                lambda x: {col_name: x[col_name]},
                remove_columns=[col for col in dataset.column_names if col != col_name],
            )

        unique_tweets = set(raw_tweet_dataset[col_name])
        # Add to the set of all unique tweets
        all_unique_tweets.update(unique_tweets)

# A list to store original, processed, and translated tweets
original_and_processed = []

# Process stopwords, retweet symbols, and lemmatization
for tweet in all_unique_tweets:
    cleaned_tweet = remove_retweet_symbol(tweet)  # Remove retweet symbols
    cleaned_tweet = to_lowercase(cleaned_tweet)  # Lowercase the text
    cleaned_tweet = remove_emojis(cleaned_tweet)  # Remove emojis
    cleaned_tweet = remove_punctuation(cleaned_tweet)  # Remove punctuation
    processed_tweet = lemmatize_text(remove_stopwords(cleaned_tweet))  # Remove stopwords and lemmatize

    # Check if the tweet is in English and translate if it's not
    if not is_english(processed_tweet):
        processed_tweet = translator(processed_tweet)  # Translate the non-English tweet
    

    original_and_processed.append((tweet, processed_tweet))

# Printing the original, processed, and translated tweets
for original, processed in original_and_processed:
    print(f"Original: {original}\nProcessed: {processed}\n")

# Create the final dataset from the processed tweets if needed
output_tweets = [processed for _, processed in original_and_processed]
final_dataset = Dataset.from_dict({"Tweet": output_tweets})


