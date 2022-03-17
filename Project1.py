#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 14:36:35 2022

@author: helenamaylindsay
"""

"""
Data
https://www.kaggle.com/prasertk/netflix-daily-top-10-in-us
"""
#import requests
#import pandas as pd
import csv
import json
import mysql.connector as msql
from mysql.connector import Error
#import sys
#import numpy as np
import pandas as pd

 
"""
1. Learn how to run multiple sys.argv (python3 Project1.py [input]) so that user can input the file conversion argument
2. Modify the number of columns from the source to the destination, reducing or adding columns. 
3. Connect to SQL 
4. Generate a brief summary of the data file ingestion including: 
     Number of records 
     Number of columns 
6. The processor should produce informative errors should it be unable to complete an operation. 
    (Try / Catch with error messages)
"""

""" 
Get input from user todetermine what file type to convert to?
"""

def conversion():
    filetype = input("What file type would you like to convert to? Choose json or sql: ")
    filetype = filetype.upper()
    return filetype
    print(filetype)
filetype = conversion()


file = pd.read_csv('/Users/helenamaylindsay/Desktop/DS3002/netflix daily top 10.csv')
file = file.rename({'Last Week Rank': 'Last_Week_Rank', 'Netflix Exclusive': 'Netflix_Exclusive', 'Netflix Release Date': 'Netflix_Release_Date', 'Days In Top 10': 'Days_In_Top_10', 'Viewership Score': 'Viewership_Score'}, axis=1)
file = file.to_csv('/Users/helenamaylindsay/Desktop/DS3002/netflix daily top 10.csv', index=False)


if "JSON" in filetype:
    
# Function to convert a CSV to JSON
# Takes the file paths as arguments
    def make_json(csvFilePath, jsonFilePath):
        
        
        jsonArray = []
        
        with open(csvFilePath, encoding='utf-8') as csvf: 
            
            #load csv file data using csv library's dictionary reader
            csvReader = csv.DictReader(csvf)
            #convert each csv row into python dict
            for row in csvReader: 
                #add this python dict to json array
                jsonArray.append(row)
              
        #convert python jsonArray to JSON String and write to file        
        with open(jsonFilePath, 'w', encoding='utf-8') as jsonf: 
            jsonString = json.dumps(jsonArray, indent=4)
            jsonString.split()
            jsonf.write(jsonString)
                
# Driver Code
    csvFilePath = r'/Users/helenamaylindsay/Desktop/DS3002/netflix daily top 10.csv'
    jsonFilePath = r'/Users/helenamaylindsay/Desktop/DS3002/netflix daily top 10.json'
    make_json(csvFilePath, jsonFilePath)
# Summary 
    file = pd.read_json('/Users/helenamaylindsay/Desktop/DS3002/netflix daily top 10.json')
    print(file.info())
    



if "SQL" in filetype:
        
    try:
        conn = msql.connect(host='localhost', user='root',  
                        password='Cabin128')#give ur username, password
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("DROP DATABASE Netflix")
            cursor.execute("CREATE DATABASE Netflix")
            print("Database is created")
            cursor.execute("USE Netflix")
            cursor.execute("""
		CREATE TABLE Netflix_Daily_Top10 (
			As_of varchar(50) primary key,
			Rank int NOT NULL,
            Last_Week_Rank varchar(50),
            Title varchar(50),
            Type_of_Film varchar(50),
            Netflix_Exclusive varchar(50),
            Netflix_Release_Date varchar(50),
            Days_In_Top_10 int NOT NULL,
            Viewership_Score int NOT NULL
			)
               """)
            print("Table is created")
            cursor.execute("ALTER TABLE Netflix.Netflix_Daily_Top10 DROP COLUMN As_of")
            #cursor.execute("ALTER TABLE Netflix.Netflix_Daily_Top10 RENAME COLUMN Type TO Type_of_Film")
    
    
    except Error as e:
        print("Error while connecting to MySQL", e)
    
    
    csv_data = pd.read_csv('/Users/helenamaylindsay/Desktop/DS3002/netflix daily top 10.csv') #, na_values= "NaN")
    csv_data.drop("As of", inplace=True, axis=1)
    csv_data.fillna("NO", inplace=True)
    

    df = pd.DataFrame(csv_data, columns= ['Rank','Last_Week_Rank','Title','Type_of_Film','Netflix_Exclusive','Netflix_Release_Date','Days_In_Top_10','Viewership_Score'])
    records = df.values.tolist()
    
    sql = "INSERT INTO Netflix_Daily_Top10 (Rank,Last_Week_Rank,Title,Type_of_Film,Netflix_Exclusive,Netflix_Release_Date,Days_In_Top_10,Viewership_Score) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

    # See which show/movie has the highest viewership score
    try:
        cursor.executemany(sql,records)
        cursor.execute("SELECT MAX(Viewership_Score), Title FROM Netflix.Netflix_Daily_Top10 GROUP BY Title ORDER BY MAX(Viewership_Score) DESC LIMIT 10;")
        
        #cursor.execute("SELECT count(Netflix.Netflix_Daily_Top10.columns) AS number_of_columns FROM Netflix.Netflix_Daily_Top10.columns")
        result = cursor.fetchall()
        print(result)
        
        cursor2 = conn.cursor()
        cursor2.execute("SELECT count(*) FROM Netflix.Netflix_Daily_Top10")
        result2 = cursor2.fetchall()
        print("Total Records =", result2)
        conn.commit()
        
        cursor3 = conn.cursor()
        cursor3.execute("SELECT count(*) as No_of_Column FROM information_schema.columns WHERE table_name ='Netflix_Daily_Top10';")
        result3 = cursor3.fetchall()
        print("Number of Columns =", result3)
        conn.commit()
    except Error as e:
        print("Error while uploading to MySQL", e)

    finally:
        print('DONE')

        cursor.close()
        conn.close()

    


     
    




