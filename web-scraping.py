import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
import web-scraping-utils

PATH = 'enter your path here'

search_query = 'https://en.wikipedia.org/wiki/List_of_stolen_paintings'
page = requests.get(search_query)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find_all("table", class_="wikitable")

getTableContents(results)

df_table1 = pd.read_csv(FILE_PATH_FOLDER+'\df_table0.csv')
df_table2 = pd.read_csv(FILE_PATH_FOLDER+'\df_table1.csv')
df_table3 = pd.read_csv(FILE_PATH_FOLDER+'\df_table2.csv')
df_table4 = pd.read_csv(FILE_PATH_FOLDER+'\df_table3.csv')

# data clean up process

# renaming columns to allow for merging

df_table1.rename(columns={'Date stolen':'Date Stolen/Taken',
       'Location of theft':'Location'},inplace=True)
df_table2.rename(columns={'Date stolen':'Date Stolen/Taken',
       'Location of theft':'Location'},inplace=True)
df_table3.rename(columns={'Date taken':'Date Stolen/Taken'},inplace=True)
df_table4.rename(columns={'Date stolen':'Date Stolen/Taken',
       'Location of theft':'Location'},inplace=True)

# adding new columns
df_table1['Table'] = 'Unrecovered'
df_table1['Status'] = ''
df_table1['Date recovered']  = ''
df_table2['Table'] = 'Rumored to be destroyed or lost'
df_table2['Status'] = ''
df_table2['Date recovered']  = ''
df_table3['Table'] = 'Plundered by the Nazis'
df_table3['Reward'] = ''
df_table3['Date recovered']  = ''
df_table4['Table'] = 'Recovered'
df_table4['Reward'] = ''
df_table4['Status'] = ''

# dropping extra column

df_table1.drop(columns=['Painting'],inplace=True)
df_table2.drop(columns=['Painting'],inplace=True)
df_table3.drop(columns=['Painting'],inplace=True)
df_table4.drop(columns=['Painting'],inplace=True)

# creating new indices and arranging columns in order
df_table1_1 = df_table1.reindex(columns=(df_table1.columns.sort_values()))
df_table2_1 = df_table2.reindex(columns=(df_table2.columns.sort_values()))
df_table3_1 = df_table3.reindex(columns=(df_table3.columns.sort_values()))
df_table4_1 = df_table4.reindex(columns=(df_table4.columns.sort_values()))

# creating final dataset
art_crimes_df = df_table1_1.append(df_table2_1).append(df_table3_1).append(df_table4_1)

# storing file
art_crimes_df.to_csv(PATH+'\\art_crimes.csv',index=False)