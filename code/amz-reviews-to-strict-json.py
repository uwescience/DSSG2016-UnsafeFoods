# Convert downloaded Amazon review data to strict JSON
# Via Julian McAuley, http://jmcauley.ucsd.edu/data/amazon/links.html

import json
import gzip


def parse(path):
    g = gzip.open(path, 'r')
    for l in g:
        yield json.dumps(eval(l))

    
f = open("../data/processed/reviews_Grocery_and_Gourmet_Food_strict.json",
         'w')

for l in parse("../data/raw/reviews_Grocery_and_Gourmet_Food.json.gz"):
    f.write(l + '\n')
