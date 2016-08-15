# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 16:41:36 2016

@author: cvint
"""

import psycopg2

# coding: utf-8

# ## Import amazon review data

# In[1]:
import os
import numpy as np
# In[2]:

import json
import pandas as pd
import gzip

def parse(path):
  g = gzip.open(path, 'rb')
  for l in g:
    yield eval(l)

def getDF(path):
  i = 0
  df = {}
  for d in parse(path):
    df[i] = d
    i += 1
  return pd.DataFrame.from_dict(df, orient='index')


# In[5]:

df = getDF("C://Users/cvint/Desktop/DSSG Unsafe Foods/meta_Grocery_and_Gourmet_Food.json.gz")


#Connect to database
conn = psycopg2.connect(database="RecallsReviews", user="unsafefoods", password="Password1", host="unsafefoods.csya4zsfb6y4.us-east-1.rds.amazonaws.com", port="5432")

print("Opened database successfully")

#create a cursor to execute SQL
cur = conn.cursor()

#This was used during the debugging and initial writing of the script.
#cur.execute("DELETE FROM CategoryAssignment;")

for row in range(df.shape[row]):
    asin = df.asin[row]
    for cat_list_ind in range(len(df.categories[row])):
        for index in range(len(df.categories[row][cat_list_ind])):
            df.categories[row][cat_list_ind][index] = df.categories[row][cat_list_ind][index].replace('\'','')
            df.categories[row][cat_list_ind][index] = df.categories[row][cat_list_ind][index].replace(',','')
            category = df.categories[row][cat_list_ind][index]
            print(str(asin),category)
            
            cur.execute('INSERT INTO CategoryAssignment\
                (category_assn_id, product_id, category_id)\
                VALUES (nextval(\'cat_assn_serial\'), \
                (SELECT product_id FROM product where asin = \'%s\'),\
                (SELECT category_id FROM category where category_name = \'%s\'))'\
                % (asin, category))

conn.commit()
print("Records created successfully");
conn.close()
