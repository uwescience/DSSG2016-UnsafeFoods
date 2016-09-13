# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 17:30:51 2016

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

df = getDF("C://Users/cvint/Desktop/DSSG Unsafe Foods/reviews_Grocery_and_Gourmet_Food.json.gz")


#connect to db
conn = psycopg2.connect(database="RecallsReviews", user="unsafefoods", password="Password1", host="unsafefoods.csya4zsfb6y4.us-east-1.rds.amazonaws.com", port="5432")

print("Opened database successfully")

#create a cursor to execute SQL
cur = conn.cursor()

#track asins already added
asins = []
cur.execute('SELECT distinct asin from Product;')
rows = cur.fetchall()
for row in rows:
    for asin in row:
        asins.append(asin)

for row in range(df.shape[0]):
    asin = df.asin[row].strip()
    if asin not in asins:
        asins.append(asin)
        cur.execute('INSERT INTO Product (product_id, asin)\
            VALUES (nextval(\'product_serial\'), \'%s\')' % asin)

#commit and close
conn.commit()

print("Records created successfully");
conn.close()
