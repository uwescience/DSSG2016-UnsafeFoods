import psycopg2

try:
    conn = psycopg2.connect("dbname='UnsafeFoods' user='postgres' host='108.179.150.158' password='Password1'")
except:
    print("I am unable to connect to the database")