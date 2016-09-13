# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 15:23:26 2016

@author: cvint
"""
import psycopg2
import pandas

#Connect to database
conn = psycopg2.connect(database="RecallsReviews", user="unsafefoods", password="Password1", host="unsafefoods.csya4zsfb6y4.us-east-1.rds.amazonaws.com", port="5432")

print("Opened database successfully")

#upload recalls csv file as provided by Miki Verma
recalls = pandas.read_csv("C://Users/cvint/Desktop/DSSG Unsafe Foods/github-unsafe-foods/DSSG2016-UnsafeFoods/github_data/enforce_upcs_2.csv",\
                            encoding='ISO-8859-1')

#create a cursor to execute SQL
cur = conn.cursor()

#track events already inserted
events_added = []

#fetch all upcs in product table
cur.execute('SELECT DISTINCT upc from product;')
upc_rows = cur.fetchall()
all_upcs = []
for upc_row in upc_rows:
    if upc_row[0]:
        all_upcs.append(upc_row[0])
print(str(all_upcs))

#iterate through the rows to insert enforcements
for row in range(recalls.shape[0]):
    
    event_id = recalls.event_id[row]
    
    #fetch company id to insert in table    
    company_name = recalls.recalling_firm[row]
    company_name = company_name.lower().replace('\'', '')
    company_name = company_name.lower().replace(',', '')
    cur.execute('SELECT company_id from company where company_name LIKE \'%s\'' %company_name)
    company_id = cur.fetchall()
    if company_id:
        company_id = company_id[0]
    
    else:
        cur.execute('INSERT INTO COMPANY (company_id, company_name) VALUES\
                        (nextval(\'company_serial\'), \'%s\')' %company_name)
        cur.execute('SELECT max(company_id) from company where company_name LIKE \'%s\'' %company_name)
        company_id = cur.fetchall()[0][0]
    
    #get classification
    classification = recalls.classification[row]
    classification_id = 0
    if 'III' in classification:
        classification_id = 3
    elif 'II' in classification:
        classification_id = 2
    else:
        classification_id = 1
    
    #clean up product description
    product_description = recalls.product_description[row]
    product_description = product_description.lower().replace('\'', '')
    product_description = product_description.lower().replace(',', '')
    
    #insert event if needed    
    if int(event_id) not in events_added:
        events_added.append(int(event_id))
        try:
            cur.execute('INSERT INTO EVENT (event_id,fda_event_id, reason, company_id,\
            voluntary_mandated, classification, \
            description) VALUES (nextval(\'event_serial\'),\
            %d, \'%s\', %d, (SELECT voluntary_mandated_id \
            from voluntarymandated where voluntary_mandated_name = \'%s\'), %d,\
            \'%s\')' % (int(event_id), recalls.reason_for_recall[row],\
            int(company_id), recalls.voluntary_mandated[row], classification_id,\
            product_description))
        except TypeError:
            print('company id not found')
    
    #insert recall based on fda recall id
    cur.execute('INSERT INTO recall (recall_id,event_id,fda_recall_id) \
                VALUES (nextval(\'recall_serial\'), (select event_id from \
                event where fda_event_id = %d), \'%s\')' % (int(event_id), recalls.recall_number[row]))
                
    #get all upcs for the row to insert recall assignments on upc
    if recalls.upcs[row] is not '':
        upcs = str(recalls.upcs[row]).split(';')
    
    
        #iterate thru upcs and add products and recalledprducts where necessary
        for upc in upcs:
            upc = upc.strip()
            contained = None
            for assigned_upc in all_upcs:
                if upc in assigned_upc or assigned_upc in upc:
                    contained = assigned_upc
                    break
            
            #insert product if it doesn't already exist
            if not contained:
                cur.execute('INSERT INTO PRODUCT (product_id, upc, product_description) \
                            VALUES (nextval(\'product_serial\'), \'%s\', \'%s\')' % (\
                            upc[:14], product_description))
                            
                            #insert product assignments
                cur.execute('INSERT INTO RecalledProduct (recalled_product_id, product_id,\
                            recall_id) VALUES (nextval(\'recalled_product_serial\'), \
                            (select product_id from product where upc = \'%s\' limit 1), \
                            (select recall_id from recall where fda_recall_id = \'%s\' limit 1))' %\
                            (upc[:14], recalls.recall_number[row]))
        
        
            #just insert product assignments if product already exists
            else:
                cur.execute('INSERT INTO RecalledProduct (recalled_product_id, product_id,\
                            recall_id) VALUES (nextval(\'recalled_product_serial\'), \
                            (select product_id from product where upc = \'%s\' limit 1), \
                            (select recall_id from recall where fda_recall_id = \'%s\' limit 1))' %\
                            (assigned_upc, recalls.recall_number[row]))
                            
    #insert dates
    #print(str(recalls.termination_date[row]))
    if str(recalls.recall_initiation_date[row]) is not 'nan':
        cur.execute('UPDATE Event set initiation_date = to_date(\'%s\', \'MM/DD/YYYY\')\
                    where fda_event_id = %d' % (recalls.recall_initiation_date[row], int(recalls.event_id[row])))
    
    if str(recalls.center_classification_date[row]) is not 'nan':
        cur.execute('UPDATE Event set classification_date = to_date(\'%s\', \'MM/DD/YYYY\')\
                    where fda_event_id = %d' % (recalls.center_classification_date[row], int(recalls.event_id[row])))
    
    #if str(recalls.termination_date[row]) is not None:
     #   cur.execute('UPDATE Event set termination_date = to_date(\'%s\', \'MM/DD/YYYY\')\
    #                where fda_event_id = %d' % (recalls.termination_date[row], int(recalls.event_id[row])))
    
    print(str(recalls.recall_number[row]))

#commit changes to db
conn.commit()

print('Recalls and events added :)')

#close db
conn.close()