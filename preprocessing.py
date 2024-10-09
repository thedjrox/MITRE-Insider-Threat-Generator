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
        df = pd.read_csv(f'{file_path}', engine='openpyxl')
        print(f'{file}')
        
#created a filtered dataframe and only the DocNumber and textasInput(tweets) columns
df_filtered = df[['DocNumber', 'TextAsInput.MiT.LTR']]

#save the filtered dataframe to a new file
filtered_file_path = os.path.join(folder_path, f'filtered_{file}')
#setting index to false gets rid of indexing each tweet, (ex. 0: tweet1, 1: tweet2,...)
df_filtered.to_csv(filtered_file_path, index=False)

