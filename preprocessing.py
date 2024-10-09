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
        print(f'{file}')
        dataset = Dataset.from_pandas(df)
        
        if 'Tweet' in dataset.column_names:
            #Removes all columns but the Tweets
            tweet_dataset = dataset.map(lambda x: {'Tweet': x['Tweet']}, remove_columns=[col for col in dataset.column_names if col != 'Tweet'])
            #Removes any duplicate Values in Dataset
            tweet_dataset = tweet_dataset.unique('Tweet')
        else:
            #Removes all columns but the Tweets
            tweet_dataset = dataset.map(lambda x: {'TextAsInput.MiT.LTR': x['TextAsInput.MiT.LTR']}, remove_columns=[col for col in dataset.column_names if col != 'TextAsInput.MiT.LTR'])
            #Removes any duplicate Values in Dataset
            tweet_dataset = tweet_dataset.unique('TextAsInput.MiT.LTR')       
        
        


