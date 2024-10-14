import os #Used to get directories and locate datasets
import pandas as pd #install pandas
from datasets import Dataset, concatenate_datasets #install datasets
from transformers import MarianMTModel, MarianTokenizer

#translates tweets of all languages to English using MarianMTModel
def translate_batch(tweets):
    # Load the model and tokenizer
    model_name = "Helsinki-NLP/opus-mt-mul-en"  #Multi-language to English model
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)

    #Tokenize the tweets, converts list of tweets into token IDs
    inputs = tokenizer(tweets, return_tensors="pt", padding=True, truncation=True)

    #Execute the translation
    with torch.no_grad():
        translated = model.generate(**inputs)

    #Converts the token IDs back to human readable text
    translated_texts = tokenizer.batch_decode(translated, skip_special_tokens=True)

    return translated_texts


#Folder Name
folder_name = 'Targeted Individual Twitter Dataset'

#Gets current directory of program
curr_dir = os.path.dirname(os.path.abspath(__file__))

#Creates Folder path
folder_path = os.path.join(curr_dir, folder_name)

#Main dataset that we be worked with for training
dataset_main = Dataset.from_dict({"Tweet": []})

#Goes through each file in folder
for file in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file)
    #Does action to each file
    if file.endswith('.csv'):
        df = pd.read_csv(f'{file_path}', encoding='utf-8')
        dataset = Dataset.from_pandas(df)
        unique_tweets = []
        col_name = ""
        if 'Tweet' in dataset.column_names:
            col_name = "Tweet" 
            #Removes all columns but the Tweets
            raw_tweet_dataset = dataset.map(lambda x: {col_name: x[col_name]}, remove_columns=[col for col in dataset.column_names if col != col_name])
        else:
            col_name = "TextAsInput.MiT.LTR"
            #Removes all columns but the Tweets
            raw_tweet_dataset = dataset.map(lambda x: {col_name: x[col_name]}, remove_columns=[col for col in dataset.column_names if col != col_name])
             
        unique_tweets = set(raw_tweet_dataset[col_name])
        
        #Variable to use that stores unqiue tweets
        #tweet_dataset = Dataset.from_dict({"Tweet": list(unique_tweets)})

        #Translate unique tweets to English in batches of 16 (adjust the size if needed)
        batch_size = 16
        translated_tweets = []
        #iterate through the tweets through increments of batch_size, (ex. 0, 16, 32, ...)
        for i in range(0, len(unique_tweets), batch_size):
            #slices unique_tweets into a batch of 16 every iteration and saves it into a list called batch
            batch = list(unique_tweets)[i:i + batch_size]
            #translates the batch and appends it to translated_tweets list
            translated_tweets.extend(translate_batch(batch))

        # Create a dataset for the translated tweets
        translated_tweet_dataset = Dataset.from_dict({"Translated & Unique_Tweet": translated_tweets})

        #All combined datasets
        dataset_main = concatenate_datasets([dataset_main, translated_tweet_dataset])
