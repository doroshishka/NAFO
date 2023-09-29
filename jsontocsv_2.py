import json
import csv
import re
#from modules import tools
#from modules import csv
import pandas as pd
import os

allfiles = []
regex = re.compile(r'user-(\d+)')
#regex = re.compile(r'\d{7,}')

def main():
    # giving directory name
    dirname = 'C:/Users/Larisa/OneDrive/Documents/Northeastern University/Ukraine/NAFO/ExtractUsers/outputs/outputs_2022.11.10_21.29.35,140149'
    ext = ('following')

    # Alternative Approach I used 
    # ext = ('.json')
    # if files.endswith(ext):

    df = pd.DataFrame()
    # iterating over all files
    for files in os.listdir(dirname):
        if ext in files:
            allfiles.append(os.path.join(dirname, files))
        else:
            continue

    edge_list(dir)

def edge_list(dir):

    df = pd.DataFrame()
    
    for dir in allfiles:
        f = regex.findall(dir)
        print(f)
        data = json.load(open(dir))
        if df.empty:
            df = pd.DataFrame(data["data"])
            df = pd.DataFrame().assign(edgelist=df['id'])
            filename= f[0]
            df['userid'] = filename
            df = df[['userid','edgelist']]
            
        else:
            df1 = pd.DataFrame(data["data"])
            df1 = pd.DataFrame().assign(edgelist=df1['id'])
            filename= f[0]
            df1['userid'] = filename
            df1 = df1[['userid','edgelist']]
            df = df.append(df1)
            
    
    print(df)
    
    df = "\t" + df
    df.to_csv('C:/Users/Larisa/OneDrive/Documents/Northeastern University/Ukraine/NAFO/Edge_list_November.csv')


if __name__ == "__main__":
    main()
