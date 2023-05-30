from selenium import webdriver
import time
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
import shutil

PATH = 'enter your path here'

def getHeadings(body):
    header = body[0]
    headings = []
    # loop through all th elements
    for item in header.find_all("th"): 
        # convert the th elements to text and strip "\n"
        item = (item.text).rstrip("\n")
        # append the clean column name to headings
        headings.append(item)
    return headings


def getRows(body):
    all_rows = []
    img_rows = []
    for row_num in range(len(body)): # A row at a time
        row = [] # this will hold entries for one row
        head_row = []
        for row_item in body[row_num].find_all("td"): 
            if(row_item.find("img")):
                if(len(row_item.find("img")['src'])==0):
                    head_row.append('no image')
                else:
                    head_row.append(row_item.find("img")['src']) #.split('160px-')[1]
            aa = re.sub("(\xa0)|(\n)|,","",row_item.text)
            #append aa to row - note one row entry is being appended
            row.append(aa)
        # append one row to all_rows
        all_rows.append(row)
        img_rows.append(head_row)
    return all_rows, img_rows


def buildFile(rows,t,headings):
    #saving dataset
    table_name = df_table = "df_table"+str(t)
    df_table = pd.DataFrame(data=rows,columns=headings)
    df_table.head()
    df_table = df_table.drop(index=0)
    df_table.fillna(value='N/A',inplace=True)
    df_table.to_csv(PATH+'\\'+table_name+'.csv',index=False)
    return table_name

def buildImg(img,df_table):
    #downloading images and saving image url for future use
    df_image = pd.DataFrame(data=img,columns=['Image'])
    df_image.dropna(inplace=True)
    url_base = '''https:'''
    url = []
    for img in df_image['Image']:
        if((len(img)==0)):
            continue
        else:
            full_url = url_base + img
            url.append(full_url)
            #print(url)
            img_name = img.split('px-')[1]
            r = requests.get(full_url, stream=True) #Get request on full_url
            if r.status_code == 200: 
                with open(PATH+'\\images\\'+img_name, 'wb') as f: 
                    r.raw.decode_content = True
                    #shutil.copyfileobj(r.raw, f)
    df_image['URL'] = url
    df_image.to_csv(PATH+df_table+'.csv',index=False)

def getTableContents(results):
    for t in range(len(results)):
        print("Looping over Table:",t)
        table = results[t]
        body = table.find_all("tr")
        headings = getHeadings(body)
        rows, img = getRows(body)
        df_table = buildFile(rows,t,headings)
        buildImg(img,df_table)
        print('Export Successful for Table',t)