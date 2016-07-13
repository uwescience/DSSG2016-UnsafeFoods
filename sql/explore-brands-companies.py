# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 14:40:55 2016

@author: cvint
"""


import psycopg2

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

df = getDF("C://Users/cvint/Desktop/DSSG Unsafe Foods/meta_Grocery_and_Gourmet_Food.json.gz")

print(df.columns)

#connect to db
conn = psycopg2.connect(database="RecallsReviews", user="unsafefoods", password="Password1", host="unsafefoods.csya4zsfb6y4.us-east-1.rds.amazonaws.com", port="5432")

print("Opened database successfully")

#create a cursor to execute SQL
cur = conn.cursor()

brands = list(set(df.brand))
used_brands = []
count = 0

for row in range(df.shape[0]):
    asin = df.asin[row]
    brand = df.brand[row]
    
    if brand not in used_brands:
        used_brands.append(brand)
        cur.execute('INSERT INTO Brand (brand_id, brand_name) \
                        VALUES (nextval(\'brand_serial\'), \'%s\')' % brand)
        cur.execute('UPDATE Product SET brand_id = (SELECT \
                        brand_id from Brand where brand_name = \'%s\') \
                        where asin = \'%s\'' %(brand, asin))
        print(count)
        count += 1
        
#commit and close
conn.commit()

print("Records created successfully");
conn.close()