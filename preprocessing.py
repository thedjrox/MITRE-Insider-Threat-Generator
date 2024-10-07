import os #Used to get directories and locate datasets
import pandas as pd #install pandas and openpyxl / Lets us not have to convert .xlsx to .csv
from datasets import Dataset #install datasets

#Folder Name
folder_name = 'Targeted_Individual_Twitter_Dataset'

#Gets current directory of program
curr_dir = os.path.dirname(os.path.abspath(__file__))

#Creates Folder path
folder_path = os.path.join(curr_dir, folder_name)

#Goes through each file in folder
for file in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file)
    #Does action to each file
    if os.path.isfile(file_path):
        df = pd.read_excel(f'{file_path}', engine='openpyxl')
        print(f'{file}')

        for col in df.select_dtypes(include=['datetime']):
            df[col] = df[col].astype(str)
        dataset = Dataset.from_pandas(df)

        

