# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 18:15:02 2016

@author: cvint

This script adds only the asins and generates their product ids for the reviews recall
database product table. We must go back in and populate the other fields separately.
"""

import psycopg2
import pandas

#Connect to database
conn = psycopg2.connect(database="RecallsReviews", user="unsafefoods", password="Password1", host="unsafefoods.csya4zsfb6y4.us-east-1.rds.amazonaws.com", port="5432")

print("Opened database successfully")

#upload review csv file
review_data = pandas.read_csv("C://Users/cvint/Desktop/DSSG Unsafe Foods/github-unsafe-foods/DSSG2016-UnsafeFoods/review_data.csv")

#create a cursor to execute SQL
cur = conn.cursor()

#This was used during the debugging and initial writing of the script.
#cur.execute("DELETE FROM Product;")

#track asins already added
already_added = []

for row in range(review_data.shape[0]):
    asin = review_data.asin[row].strip()
    if asin not in already_added:
        already_added.append(asin)
        cur.execute('INSERT INTO Product (product_id, asin)\
            VALUES (nextval(\'product_serial\'), \'%s\')' % asin)

#commit and close
conn.commit()
print("Records created successfully");
conn.close()
