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
review_data = pandas.read_csv("C://Users/cvint/all_reviews.csv")
print('read data')

#create a cursor to execute SQL
cur = conn.cursor()

#This was used during the debugging and initial writing of the script.
#cur.execute("DELETE FROM Review;")

#Track reviewers already added
cur.execute('SELECT amazon_reviewer_id from reviewer')
reviewer_ids = pandas.DataFrame(cur.fetchall())
reviewer_ids = list(reviewer_ids.iloc[:,0])
print(reviewer_ids[:10])

count = 0

for row in range(review_data.shape[0]):
    count += 1
    review_date = review_data.reviewTime[row]
    review_text = review_data.reviewText[row]
    summary = review_data.summary[row]
    overall = int(review_data.overall[row])
    unix_review_time = int(review_data.unixReviewTime[row])
    amazon_reviewer_fk = review_data.reviewerID[row]
    review_asin = review_data.asin[row].strip()
    
    review_text = str(review_text).replace('\'', '')
    summary = str(summary).replace('\'', '')
    reviewer_name = str(review_data.reviewerName[row]).replace('\'', '')
	#check to see if reviewer already exists
    if amazon_reviewer_fk not in reviewer_ids:
        cur.execute('INSERT INTO REVIEWER (reviewer_id, amazon_reviewer_id, reviewer_name)\
        VALUES (nextval(\'reviewer_serial\'),  \'%s\', \'%s\');' % (amazon_reviewer_fk, reviewer_name))
        reviewer_ids.append(amazon_reviewer_fk)
	
    #check if review already exists by checking unix review time and amazon reviewer id
    cur.execute('Select * from review where unix_review_time = %d and reviewer_id in (select reviewer_id from reviewer\
				where amazon_reviewer_id = \'%s\');' % (unix_review_time, amazon_reviewer_fk))
	
    result = pandas.DataFrame(cur.fetchall())
    print(result.shape)
	
    if result.shape[0] == 0:
        cur.execute('INSERT INTO Review (review_id, reviewer_id, product_id, review_text, \
        summary, overall, unix_review_time, review_time) VALUES (nextval(\'review_serial\'), \
        (SELECT reviewer_id from reviewer where amazon_reviewer_id = \'%s\' limit 1), \
        (SELECT product_id from product where asin = \'%s\' limit 1), \'%s\', \'%s\', \
        %d, %d, to_timestamp(\'%s\', \'dd mm yyyy\'));' % (amazon_reviewer_fk, \
        review_asin, review_text, summary, overall, unix_review_time, review_date))
        print(cur.statusmessage)
        if count % 50 == 0:
            conn.commit()
            print('committed')

#commit and close
conn.commit()
print("Records created successfully")
conn.close()
