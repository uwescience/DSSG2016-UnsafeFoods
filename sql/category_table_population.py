# -*- coding: utf-8 -*-
"""
This is the script that was used to populate the Categories Table. 
Because of the crossover in parent and category ids in this hierarchical structure,
I iterated through the list of tuples twice, adding the category ids and 
parent ids separately.
"""

import psycopg2
import pandas

#Connect to database
conn = psycopg2.connect(database="RecallsReviews", user="unsafefoods", password="Password1", host="unsafefoods.csya4zsfb6y4.us-east-1.rds.amazonaws.com", port="5432")

print("Opened database successfully")

#upload category csv file as provided by Miki Verma
categories = pandas.read_csv("C://Users/cvint/Desktop/DSSG Unsafe Foods/github-unsafe-foods/DSSG2016-UnsafeFoods/github_data/amazon_product_categories.csv")

#Add an empty pandas column
categories['category_id'] = ''

#create a cursor to execute SQL
cur = conn.cursor()

#This was used during the debugging and initial writing of the script.
#cur.execute("DELETE FROM Category;")

#Iterate through categories, adding name and category id
for row in range(categories.shape[0]):
    name = categories.ProductCategory[row].strip()
    cur.execute("INSERT INTO Category (category_id,category_name) \
      VALUES (nextval(\'cat_serial\'),\'%s\');" % name)
    print(cur.statusmessage)
    cur.execute('SELECT category_id from category where category_name = \'%s\'' % name)
    categories.category_id[row] = cur.fetchone()[0]

print("Added categories step 1")
 
#reiterate through categories and updating parent id     
for row in range(categories.shape[0]):
    parent = categories.ParentCategory[row]
    if parent:
        cur.execute('SELECT category_id from category where category_name = \'%s\'' % parent)
        parent_id = cur.fetchone()
        if parent_id:
            parent_id = parent_id[0]
            cur.execute('UPDATE category set parent_id = %d where category_id = %d' \
                % (parent_id, categories.category_id[row]))
            print(cur.statusmessage)
    

print("added category parents")

#commit and close
conn.commit()
print("Records created successfully");
conn.close()