---
layout: page
title:  Data processing
---

### Create Amazon Review/Recalled Product DataFrame

This section assumes that you have 2 datasets available on your local machine (please change the file paths accordingly):

1.  reviews_Grocery_and_Gourmet_Food.json.gz [http://jmcauley.ucsd.edu/data/amazon/](http://jmcauley.ucsd.edu/data/amazon/)


2.  asin_intersection_full.csv (available from our website)

The code below creates a dataframe that appends FDA recall variables to the Amazon review data.  These data are used for the preliminary classification models as well as topic modeling.


```python
##Amazon Review Data - code borrowed from http://jmcauley.ucsd.edu/data/amazon/
import pandas as pd
import gzip
import os
wd = os.getcwd()

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

food_review = getDF(os.path.join(wd,"..","..",\
                    "data/raw/reviews_Grocery_and_Gourmet_Food.json.gz"))
```


```python
##Recall Data includes ASIN ID and Recall Date
recall_data = pd.read_csv(os.path.join(wd,"..","..",
                        "data/processed/asin_intersection_full.csv"), encoding='ISO-8859-1')
full_df = pd.merge(food_review, recall_data, 
                   how = "left", on = ["asin"])
```


```python
##Match Formatting for Amazon Review Dates and Recall Date
full_df['unixReviewTime'] = \
    pd.to_datetime(full_df['unixReviewTime'], unit='s').dt.date
full_df['initiation_date'] = \
    pd.to_datetime(full_df['initiation_date'], unit='s').dt.date
```

Since it is unclear the best way to define the recall/review relationship (should a review be within 1 year of a recall in order to provide accurate information? 6 months?), we define four versions of the recall/review relationship:

1.  Review is within (+/-) 1 year of the recall date

2.  Review is within (+/-) 6 months of the recall date

3.  Review is at most 1 year before the recall date

4.  Review is at most 6 months before the recall date


```python
##Add Date bounderies
## +/- 1 year from recall date
full_df['initiation_date_plus1Y'] = \
    pd.to_datetime(full_df['initiation_date'] + pd.DateOffset(years=1)).dt.date
full_df['initiation_date_minus1Y'] = \
    pd.to_datetime(full_df['initiation_date'] - pd.DateOffset(years=1)).dt.date
    
## +/- 6 months from recall date
full_df['initiation_date_plus6M'] = \
    pd.to_datetime(full_df['initiation_date'] + pd.DateOffset(months=6)).dt.date
full_df['initiation_date_minus6M'] = \
    pd.to_datetime(full_df['initiation_date'] - pd.DateOffset(months=6)).dt.date
```


```python
##Define recall in 4 ways:
full_df['recalled_1y'] = (((full_df['unixReviewTime'] < \
                            full_df['initiation_date_plus1Y']) == True)\
                             & ((full_df['unixReviewTime'] > \
                            full_df['initiation_date_minus1Y']) == True)).astype('int')

full_df['recalled_6m'] = (((full_df['unixReviewTime'] < \
                            full_df['initiation_date_plus6M']) == True)\
                             & ((full_df['unixReviewTime'] > \
                            full_df['initiation_date_minus6M']) == True)).astype('int')

full_df['recalled_1yb4'] = (((full_df['unixReviewTime'] < \
                              full_df['initiation_date']) == True)\
                             & ((full_df['unixReviewTime'] > \
                            full_df['initiation_date_minus1Y']) == True)).astype('int')

full_df['recalled_6mb4'] = (((full_df['unixReviewTime'] < \
                              full_df['initiation_date']) == True)\
                             & ((full_df['unixReviewTime'] > \
                            full_df['initiation_date_minus6M']) == True)).astype('int')
```


```python
##Check number of recalled reviews for each definition of 'Recall'
print("Review +/- 1 Year from recall: %d" \
      % full_df['recalled_1y'].sum())
print("Review 1 year before recall: %d" \
      %full_df['recalled_1yb4'].sum())
print("Review +/- 6 Months from recall: %d" \
      %full_df['recalled_6m'].sum())
print("Review 6 months before recall: %d" \
      %full_df['recalled_6mb4'].sum())
```

    Review +/- 1 Year from recall: 1285
    Review 1 year before recall: 790
    Review +/- 6 Months from recall: 547
    Review 6 months before recall: 335


### Subset Data

Given that our text is very imbalanced (1.2 million non-recalled product reviews vs. a few thousand recalled reviews), the code below creates an artifically blanaced sample (0.5% random sample of the nonrecalled products and 100% recalled products)


```python
full_df_recalled = full_df[full_df.recalled_1y == 1]
full_df_nonrecalled = full_df[full_df.recalled_1y == 0]

from sklearn.cross_validation import train_test_split
X_testRecall, X_trainRecall, Y_testRecall, Y_trainRecall = \
                                            train_test_split(full_df_recalled['reviewText'], \
                                            full_df_recalled['recalled_1y'], \
                                            test_size=0.999, random_state=123)

X_testNoRecall, X_trainNoRecall, Y_testNoRecall, Y_trainNoRecall = \
                                            train_test_split(full_df_nonrecalled['reviewText'], \
                                            full_df_nonrecalled['recalled_1y'], \
                                            test_size=0.005, random_state=123)



##Combined to have subsets with 1/2 of the recall data each
Xtrain = pd.concat([X_trainRecall, X_trainNoRecall], axis=0)
Xtrain = pd.DataFrame(Xtrain, columns=['reviewText'], dtype=str)
Ytrain = pd.concat([Y_trainRecall, Y_trainNoRecall], axis=0)
```


```python
##Add all other "Recall" Definitions to the Ytrain dataset and create a final subset
Ytrain = pd.merge(pd.DataFrame(Ytrain), pd.DataFrame(full_df.recalled_1yb4), \
                  left_index=True, right_index=True)
Ytrain = pd.merge(Ytrain, pd.DataFrame(full_df.recalled_6m), \
                  left_index=True, right_index=True)
Ytrain = pd.merge(Ytrain, pd.DataFrame(full_df.recalled_6mb4), \
                  left_index=True, right_index=True)
Ytrain = pd.merge(Ytrain, pd.DataFrame(full_df.asin), \
                  left_index=True, right_index=True)
Subset = pd.merge(Xtrain, Ytrain, left_index=True, right_index=True)
```

### Clean Text Data

The code below cleans the text in the following way: removes special characters and english 'stopwords', accounts for missing returns, makes text lowercase, and stems words to their root. 


```python
##Tokenize review text for each review
import numpy as np
from nltk import word_tokenize
from nltk.stem.lancaster import LancasterStemmer
st = LancasterStemmer()

Subset['reviewText'] = Subset['reviewText'].str.replace("'", "")
Subset['reviewText'] = Subset['reviewText'].str.replace('[^a-zA-Z\s]',' ')
tokens_I = [word_tokenize(review) for review in Subset['reviewText']]
```


```python
##Separate strings with multiple uppercase characters (e.g., gCholesterol, VeronaStarbucks). This should take care of situations where the reviews included returns that were not treated as spaces in the raw text file
import re
def split_uppercase(tokens):
    tokens_II = np.empty((len(tokens),0)).tolist()
    for review in tokens:
        n = tokens.index(review)
        for word in review:
            split = re.sub(r'([A-Z][a-z])', r' \1', word)
            tokens_II[n].append(split)
    return tokens_II

tokens_II = split_uppercase(tokens_I)
```


```python
##Make all text lower case
def make_lowercase(tokens):
    tokens_final = np.empty((len(tokens),0)).tolist()
    for review in tokens:
        n = tokens.index(review)
        for word in review:
            lowercase_word = word.lower()
            tokens_final[n].append(lowercase_word)
    return tokens_final

tokens = make_lowercase(tokens_II)
```


```python
##Remove stopwords and stem
from nltk.corpus import stopwords
stopwords = stopwords.words('english')

def stem_tokens(tokens):
    stemmed_token = np.empty((len(tokens),0)).tolist()
    for review in tokens:
        n = tokens.index(review)
        for word in review:
            if word not in stopwords:
                stem = st.stem(word)
                stemmed_token[n].append(stem)
    return stemmed_token
        
stemmed = stem_tokens(tokens)
```


```python
##Manipulate stemmed text to be string instead of list (needed for count vectorizer)
def make_string(text):
    final_review_text = []
    for review in text:
        for word in review:
            n = review.index(word)
            if n == 0:
                string = review[n]
            else:
                string = string + " " + review[n]
        final_review_text.append(string)
    return final_review_text

final_text = make_string(stemmed)
```

### Create Document Term Matrix

We create a document term matrix that includes term frequencies.  TF-IDF weighting is not applied because all documents are relatively short and this would artificially inflate words that do not occur very often.


```python
##Count Vectorizer Matrix
from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer(binary=False, ngram_range=(1, 1))
text_matrix = vectorizer.fit_transform(final_text)
```
