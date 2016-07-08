# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 18:32:15 2016

@author: cvint
"""

import psycopg2
import pandas
from datetime import datetime

#Connect to database
conn = psycopg2.connect(database="RecallsReviews", user="unsafefoods", password="Password1", host="unsafefoods.csya4zsfb6y4.us-east-1.rds.amazonaws.com", port="5432")

print("Opened database successfully")

#upload review csv file
review_data = pandas.read_csv("C://Users/cvint/Desktop/DSSG Unsafe Foods/github-unsafe-foods/DSSG2016-UnsafeFoods/review_data.csv")

#create a cursor to execute SQL
cur = conn.cursor()

#This was used during the debugging and initial writing of the script.
cur.execute("DELETE FROM Review;")

for row in range(review_data.shape[0]):
    review_date = review_data.reviewTime[row]
    review_text = review_data.reviewText[row]
    summary = review_data.summary[row]
    overall = int(review_data.overall[row])
    unix_review_time = int(review_data.unixReviewTime[row])
    amazon_reviewer_fk = review_data.reviewerID[row]
    review_asin = review_data.asin[row].strip()
    
    cur.execute('INSERT INTO Review (review_id, reviewer_id, product_id, review_text, \
        summary, overall, unix_review_time, review_time) VALUES (nextval(\'review_serial\'), \
        (SELECT reviewer_id from reviewer where amazon_reviewer_id = \'%s\'), \
        (SELECT product_id from product where asin = \'%s\'), \'%s\', \'%s\', \
        %d, %d, to_timestamp(\'%s\', \'dd mm yyyy\'));' % (amazon_reviewer_fk, \
        review_asin, review_text, summary, overall, unix_review_time, review_date))
    print(cur.statusmessage)

#commit and close
conn.commit()
print("Records created successfully");
conn.close()
