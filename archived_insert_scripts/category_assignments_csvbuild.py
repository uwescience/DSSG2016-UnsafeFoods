# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 15:00:15 2016

@author: kirenverma
"""

import os

wd = os.getcwd()
data_dir = os.path.join(wd,"..","data")
github_data_dir= os.path.join(wd,"..","github_data")

import json
import pandas as pd
import gzip

def parse(path):
  g = gzip.open(path, 'rb')
  for l in g:
    yield eval(l)

def getDF(path):
  i = 0
  df = {}
  for d in parse(path):
    df[i] = d
    i += 1
  return pd.DataFrame.from_dict(df, orient='index')


df_meta = getDF(os.path.join(data_dir, "meta_Grocery_and_Gourmet_Food.json.gz"))
df_meta.drop(["imUrl", "related"],1)

uptree = pd.DataFrame.from_csv(os.path.join(github_data_dir, "categories_pkeys.csv"))

pid = pd.DataFrame.from_csv(os.path.join(github_data_dir, "products_pkeys.csv"), index_col = False)
pid = pid.drop(["brand_id", "upc", "product_description", "product_name"],1)

pc_join = pd.merge(pid, df_meta, how = "left", on = ["asin"])



prod_series = []
cat_series = []
weird = []
for row in range(pc_join.shape[0]):
    for cat_list in pc_join.categories[row]:
        last_product = cat_list[-1].replace(",","").replace("'","")
        pkey = uptree[uptree.category_name == last_product].index.tolist()[0]
        while pkey == pkey:
            prod_series.append(pc_join.product_id[row])
            cat_series.append(pkey)
            print(pkey)
            pkey = uptree["parent_id"].ix[pkey]
prod_cat = pd.DataFrame({"category_key": cat_series, "product_key" : prod_series})

prod_cat.to_csv(os.path.join(github_data_dir, "cat_assign.csv"))



