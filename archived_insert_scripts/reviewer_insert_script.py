# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 17:09:14 2016

@author: cvint

This is the script used to add reviewers to the Reviewer table.

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
#cur.execute("DELETE FROM Reviewer;")

#track ids already added
already_added = []

for row in range(review_data.shape[0]):
    reviewer_id = review_data.reviewerID[row].strip()
    if reviewer_id not in already_added:
        already_added.append(reviewer_id)
        reviewer_name = review_data.reviewerName[row]
        cur.execute('INSERT INTO Reviewer (reviewer_id, amazon_reviewer_id, reviewer_name)\
            VALUES (nextval(\'reviewer_serial\'), \'%s\', \'%s\')' % (reviewer_id, reviewer_name))

#commit and close
conn.commit()
print("Records created successfully");
conn.close()