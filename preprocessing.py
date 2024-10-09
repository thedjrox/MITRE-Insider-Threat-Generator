import os #Used to get directories and locate datasets
import pandas as pd #install pandas
from datasets import Dataset #install datasets

#Folder Name
folder_name = 'Targeted Individual Twitter Dataset'

#Gets current directory of program
curr_dir = os.path.dirname(os.path.abspath(__file__))

#Creates Folder path
folder_path = os.path.join(curr_dir, folder_name)

#Goes through each file in folder
for file in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file)
    #Does action to each file
    if file.endswith('.csv'):
        df = pd.read_csv(f'{file_path}', encoding='utf-8')
        dataset = Dataset.from_pandas(df)
        unqiue_tweets = []
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
        
        tweet_dataset = Dataset.from_dict({col_name: list(unique_tweets)})
