# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 14:21:32 2016

@author: cvint
"""


import psycopg2
import pandas
from datetime import datetime
import dask.dataframe as dd
import numpy as np

#Connect to database
conn = psycopg2.connect(database="RecallsReviews", user="unsafefoods", password="Password1", host="unsafefoods.csya4zsfb6y4.us-east-1.rds.amazonaws.com", port="5432")

print("Opened database successfully")

#upload review csv file
review_data = pandas.read_csv("C://Users/cvint/all_reviews.csv")

print('read in data')

#create a cursor to execute SQL
cur = conn.cursor()

#find all products that don't already exist to add to product table

cur.execute('select distinct asin from product where asin is not null;')

asin_rows = cur.fetchall()
asins = [asin_row[0] for asin_row in asin_rows]
print(len(asins))
print(asins[:100])

review_asins = review_data.asin

asins_to_add = [asin for asin in review_asins if asin not in asins]
asins_to_add = list(set(asins_to_add))

for asin in asins_to_add:
    cur.execute('insert into product (product_id, asin) values (nextval(\'product_serial\'),\
        \'%s\')' % asin)
    conn.commit()
    print(asin)


#find all reviewers that don't already exist to add to reviewer table
cur.execute('select amazon_reviewer_id from reviewer;')
reviewers = cur.fetchall()
existing_reviewers = np.array(reviewers)
existing_reviewers = existing_reviewers[:][1]

all_reviewers = review_data.reviewerID

reviewers_to_add = [reviewer for reviewer in all_reviewers if reviewer not in existing_reviewers]

reviewers_to_add = list(set(reviewers_to_add))

for row in range(review_data.shape[0]):
    if review_data.reviewerID[row] in reviewers_to_add:
        reviewer_name = review_data.reviewerName[row]
        cur.execute('insert into reviewer (reviewer_id, amazon_reviewer_id, reviewer_name)\
                 VALUES (nextval(\'reviewer_serial\'), \'%s\', \'%s\')'\
                 % (review_data.reviewerID[row], reviewer_name))
        print(review_data.reviewerID[row])
        conn.commit()
                 
#drop everything in review table to repopulate from scratch
cur.execute('DELETE * FROM REVIEW')

for row in range(review_data.shape[0]):
    review_date = review_data.reviewTime[row]
    review_text = review_data.reviewText[row]
    summary = review_data.summary[row]
    overall = int(review_data.overall[row])
    unix_review_time = int(review_data.unixReviewTime[row])
    amazon_reviewer_fk = review_data.reviewerID[row]
    review_asin = review_data.asin[row].strip()
    
    review_text = str(review_text).replace('\'', '')
    summary = str(summary).replace('\'', '')
    
    cur.execute('INSERT INTO Review (review_id, reviewer_id, product_id, review_text, \
        summary, overall, unix_review_time, review_time) VALUES (nextval(\'review_serial\'), \
        (SELECT reviewer_id from reviewer where amazon_reviewer_id = \'%s\'), \
        (SELECT product_id from product where asin = \'%s\'), \'%s\', \'%s\', \
        %d, %d, to_timestamp(\'%s\', \'dd mm, yyyy\'));' % (amazon_reviewer_fk, \
        review_asin, review_text, summary, overall, unix_review_time, review_date))
    print(row)
    conn.commit()
    
#commit and close
conn.commit()
print("Records created successfully")
conn.close()