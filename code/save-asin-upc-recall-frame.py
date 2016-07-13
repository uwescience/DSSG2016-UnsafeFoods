from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import pandas
recall_data = pandas.read_csv("recalls_upcs_asins_joined.csv",skip_blank_lines = True,encoding='ISO-8859-1')

run data-preprocessing.py

count = 0
print(count)
for row in range(recall_data.shape[0]):
    upcs = str(recall_data.upcs[row]).split(';')
    asins = []
    upcs = list(set(upcs))
    for upc in upcs:
        print(upc)
        upc = str(upc).strip()
        asins.append(UPCtoASIN(upc))
    recall_data.asins[row] = asins
    print(count)
    count+=1
	
recall_data.to_csv('recalls_upcs_asins_joined.csv')