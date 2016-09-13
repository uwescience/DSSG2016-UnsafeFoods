# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 12:57:20 2016

@author: cvint
"""

'''
This script is to insert recall data corresponding to inserted upc matches
'''

import psycopg2
import pandas

#Connect to database
conn = psycopg2.connect(database="RecallsReviews", user="unsafefoods", password="Password1", host="unsafefoods.csya4zsfb6y4.us-east-1.rds.amazonaws.com", port="5432")

print("Opened database successfully")

#upload recalls csv file as provided by Miki Verma
recalls = pandas.read_csv("C://Users/cvint/Desktop/DSSG Unsafe Foods/github-unsafe-foods/DSSG2016-UnsafeFoods/github_data/recalls_upcs_asins_joined.csv",\
                            encoding='ISO-8859-1')

#create a cursor to execute SQL
cur = conn.cursor()

#fetch upcs
cur.execute('SELECT DISTINCT upc from Product;')
upc_rows = cur.fetchall()
upcs = []
for row in upc_rows:
    upcs.append(row[0])
print(str(upcs))

for row in range(recalls.shape[0]):
    cur.execute('INSERT INTO Recall (recall_id) VALUES (nextval(\'recall_serial\'));')
    
    cur.execute('INSERT INTO Event (event_id, reason, initiation_date)\
                    VALUES (nextval(\'event_serial\'), \'%s\', to_date(\'%s\', \'Dy, DD Mon YYYY HH24:MI:SS\'));'\
                    % (recalls.REASON[row], recalls.DATE[row]))
        
    cur.execute('INSERT INTO Recall (recall_id, event_id, company_release_link, photos_link)\
                    VALUES (nextval(\'recall_serial\'), (SELECT event_id from EVENT WHERE reason = \'%s\'\
                    AND initiation_date = to_date(\'%s\', \'Dy, DD Mon YYYY HH24:MI:SS\') limit 1), \'%s\',\'%s\')'\
                    % (recalls.REASON[row], recalls.DATE[row], recalls.COMPANY_RELEASE_LINK[row],\
                    recalls.PHOTOS_LINK[row]))
    
    #get recall id for the recalledproduct inserts
    cur.execute('SELECT max(recall_id) from recall;')
    recall_id = cur.fetchall()[0][0]
    
    for upc in str(recalls.upcs[row]).split(';'):
        if upc not in upcs:
            cur.execute('INSERT INTO Product (product_id, upc, product_description\
                ) VALUES (nextval(\'product_serial\'),\'%s\',\'%s\'\
                )' % (str(upc).strip(),recalls.PRODUCT_DESCRIPTION[row]))
        
        cur.execute('INSERT INTO RecalledProduct (recalled_product_id, product_id, recall_id)\
                VALUES (nextval(\'recalled_product_serial\'),(\
                SELECT product_id from product where upc = \'%s\' limit 1), %d);'\
                % (str(upc).strip(), recall_id))
        
        print(str(upc) + ' was added')
        

conn.commit()
conn.close()
print('records committed')