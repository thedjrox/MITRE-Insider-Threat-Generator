import os #Used to get directories and locate datasets
import pandas as pd #install pandas
from datasets import Dataset #install datasets

#Folder Name
folder_name = 'Targeted Individual Twitter Dataset'

#Gets current directory of program
curr_dir = os.path.dirname(os.path.abspath(__file__))

#Creates Folder path
folder_path = os.path.join(curr_dir, folder_name)
column_names = ["__ProjectID", "CaseContact", "DocKDStatus", "DocAuthorID", "DocAuthorIDMicro", "DocName", "DocNumber", "DocTimestamp", "DocLanguageCode3", "DocLangDialect",	"DocScriptCode",	"DocDataType",	"DocDatatSize",	"DocDataFileType",	"DocGenreType",	"TextAsInput.MiT.LTR",	"TextAsInput.MiT.RTL",	"DocPermalink",	"TweetValue"]
columns_to_remove = [column_names[i] for i in range(len(column_names)) if i not in [6, 15]]
#Goes through each file in folder

for file in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file)
    #Does action to each file
    if file.endswith('.csv'):
        df = pd.read_csv(f'{file_path}', encoding='utf-8')
        print(f'{file}')
        print(df.info())
        dataset = Dataset.from_pandas(df)
        #dataset.remove_columns(columns_to_remove)
        #print(dataset.column_names);
        

        

