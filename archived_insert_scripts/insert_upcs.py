# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 12:31:44 2016

@author: cvint
"""

import psycopg2
import pandas
import data_preprocessing as dp

#Connect to database
conn = psycopg2.connect(database="RecallsReviews", user="unsafefoods", password="Password1", host="unsafefoods.csya4zsfb6y4.us-east-1.rds.amazonaws.com", port="5432")

print("Opened database successfully")

#upload recalls csv file as provided by Miki Verma
recalls = pandas.read_csv("C://Users/cvint/Desktop/DSSG Unsafe Foods/github-unsafe-foods/DSSG2016-UnsafeFoods/github_data/recalls_upcs_asins_joined.csv",\
                            encoding='ISO-8859-1')

log = open('insert_upc_log__old_recalls.txt', 'w')

#create a cursor to execute SQL
cur = conn.cursor()

problem_rows = []

for row in range(3000,recalls.shape[0]):
    upcs = str(recalls.upcs[row]).split(';')
    asins = str(recalls.asins[row]).split(';')
    if len(asins) == len(upcs) and len(asins) > 0:   
        for i in range(len(asins)):
            if asins[i] not in ['','UPCNOTFOUND','nan'] and 'UPClength' not in asins[i]:
                cur.execute('UPDATE Product\
                        SET upc = \'%s\' where asin = \'%s\'' %(upcs[i], asins[i]))
                conn.commit()
                print('Attempted and Committed:' + str(asins))
    elif upcs is not None:
        asins = []
        for upc in upcs:
            asins.append(dp.UPCtoASIN(upc.strip()))
        for i in range(len(asins)):
            if asins[i] not in ['','UPCNOTFOUND'] and 'UPClength' not in asins[i]:
                cur.execute('UPDATE Product\
                        SET upc = \'%s\' where asin = \'%s\'' %(upcs[i], asins[i]))
                print('Attempted and Committed differing lengths:' + str(asins))
                conn.commit()
        log.write(str(asins)+'\n')
    else:
        print('empty row')

conn.commit()
print("Records created successfully");
conn.close()