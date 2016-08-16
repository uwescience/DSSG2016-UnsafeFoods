---
layout: page
title: Data organizing
---

# Our Approach

We decided to design and create a relational database to contain the joined FDA recall and Amazon review data. This way, researchers can continue to work on this topic, beginning with the analytical tasks, rather than spending so much time joining the data on unique identifiers and organizing it into a concise, easy-to-use format. 

Some visualizations based on summary statistics queried from the database can be found [here](https://escience.shinyapps.io/unsafefoods).


# Using the Unsafe Foods Database

## Understanding the Database

![alt text](https://github.com/cvint13/DSSG2016-UnsafeFoods/blob/gh-pages/assets/images/UnsafeFoodsDatabase.png "Unsafe Foods DB Schema")

The Unsafe Foods Database is a relational Postgres database that facilitates the querying and analysis of Amazon review data with respect to historical FDA recall data. We gathered the Amazon Review data from a [historical dataset](http://jmcauley.ucsd.edu/data/amazon/) that was published by Julian McAuley at UCSD. This data contains approximately 1.8 million individual reviews that include the reviewer ID, date and time of the review, the text, summary, rating, and product metadata.  

## Connecting to the Database in Python

In python, you need to download a module to connect with the PostGres database. My preferred module is psycopg2. In order to install this package successfully, you must install its dependencies first using the following commands in bash: 

```bash
sudo apt-get install gcc
sudo apt-get install python-setuptools
sudo easy_install psycopg2
```

After installing, you can invoke the module in your Python script and connect to the database using the following command and parameters:

```python
import psycopg2

#Connect to database
conn = psycopg2.connect(database = <Database-Name>, user = <your-user-name>, password = <your-password>, host = <your-host-name>, port = <your port number, usually 5432>)

print("Opened database successfully")
```

## Querying the Database

Using the above connection info, this section will connect to the database and execute some queries to illustrate the database's capabilities.


```python
import psycopg2

#We also want to import pandas and numpy to work with the data we have fetched
import pandas as pd
import numpy as np

#Connect to database; input depends on your settings
conn = psycopg2.connect(database=<db_name>, user=<user_name>, password=<password>, host=<host_name>, port=<port_name>)

print("Opened database successfully")
```

    Opened database successfully
    

First, let's go ahead and look at some of the metadata that we are working with. How many products are there per category?


```python
'''
You need to set up a cursor before you start executing queries.
One way to look at it is that your connection, 'conn', is your ticket to the database,
while your cursor, cur, will be your shopping cart.
'''
cur = conn.cursor()
```


```python
#execute SQL query
cur.execute('SELECT c.category_name, count(*) as NumProducts from\
                Category c Join CategoryAssignment ca on c.category_id = ca.category_id\
                JOIN Product p on ca.product_id = p.product_id\
                group by c.category_name order by NumProducts DESC;')

#fetch table from the cursor
category_breakdown = pd.DataFrame(cur.fetchall())
```


```python
category_breakdown
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Grocery &amp; Gourmet Food</td>
      <td>171760</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Beverages</td>
      <td>3925</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Cooking &amp; Baking</td>
      <td>2434</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Tea</td>
      <td>1791</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Chocolate</td>
      <td>1043</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Snack Foods</td>
      <td>983</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Coffee</td>
      <td>949</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Candy &amp; Chocolate</td>
      <td>927</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Tea Samplers</td>
      <td>763</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Herbal</td>
      <td>583</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Sugar</td>
      <td>489</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Single-Serve Cups</td>
      <td>464</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Baby Foods</td>
      <td>436</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Breakfast Foods</td>
      <td>418</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Cereal</td>
      <td>412</td>
    </tr>
    <tr>
      <th>15</th>
      <td>Nut</td>
      <td>411</td>
    </tr>
    <tr>
      <th>16</th>
      <td>Vinegars</td>
      <td>396</td>
    </tr>
    <tr>
      <th>17</th>
      <td>Oils</td>
      <td>396</td>
    </tr>
    <tr>
      <th>18</th>
      <td>Single Herbs &amp; Spices</td>
      <td>394</td>
    </tr>
    <tr>
      <th>19</th>
      <td>Fruit</td>
      <td>370</td>
    </tr>
    <tr>
      <th>20</th>
      <td>Bars</td>
      <td>343</td>
    </tr>
    <tr>
      <th>21</th>
      <td>Baby Formula</td>
      <td>324</td>
    </tr>
    <tr>
      <th>22</th>
      <td>Sauces</td>
      <td>298</td>
    </tr>
    <tr>
      <th>23</th>
      <td>Energy Drinks</td>
      <td>272</td>
    </tr>
    <tr>
      <th>24</th>
      <td>Sugar Substitutes</td>
      <td>254</td>
    </tr>
    <tr>
      <th>25</th>
      <td>Juices</td>
      <td>251</td>
    </tr>
    <tr>
      <th>26</th>
      <td>Cereals</td>
      <td>239</td>
    </tr>
    <tr>
      <th>27</th>
      <td>Sugars</td>
      <td>234</td>
    </tr>
    <tr>
      <th>28</th>
      <td>Chewing Gum</td>
      <td>229</td>
    </tr>
    <tr>
      <th>29</th>
      <td>Fruit Juice</td>
      <td>227</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
  </tbody>
</table>
<p>516 rows × 2 columns</p>
</div>



What about the number of reviews per category?


```python
#execute SQL query
cur.execute('SELECT c.category_name, count(*) as NumReviews from\
                Category c Join CategoryAssignment ca on c.category_id = ca.category_id\
                JOIN Review r on ca.product_id = r.product_id\
                group by c.category_name order by NumReviews DESC;')

#fetch table from the cursor
category_breakdown_reviews = pd.DataFrame(cur.fetchall())
```


```python
category_breakdown_reviews
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Grocery &amp; Gourmet Food</td>
      <td>1077410</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Beverages</td>
      <td>23570</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Cooking &amp; Baking</td>
      <td>20297</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Tea</td>
      <td>9737</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Sugar</td>
      <td>5793</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Vinegars</td>
      <td>4792</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Oils</td>
      <td>4792</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Chocolate</td>
      <td>4482</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Coffee</td>
      <td>4431</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Candy &amp; Chocolate</td>
      <td>3981</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Baby Foods</td>
      <td>3755</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Herbal</td>
      <td>3609</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Single Herbs &amp; Spices</td>
      <td>3582</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Baby Formula</td>
      <td>3553</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Nut</td>
      <td>3284</td>
    </tr>
    <tr>
      <th>15</th>
      <td>Coconut</td>
      <td>3276</td>
    </tr>
    <tr>
      <th>16</th>
      <td>Snack Foods</td>
      <td>3224</td>
    </tr>
    <tr>
      <th>17</th>
      <td>Sugars</td>
      <td>2943</td>
    </tr>
    <tr>
      <th>18</th>
      <td>Sugar Substitutes</td>
      <td>2848</td>
    </tr>
    <tr>
      <th>19</th>
      <td>Tea Samplers</td>
      <td>2303</td>
    </tr>
    <tr>
      <th>20</th>
      <td>Meal Replacement Drinks</td>
      <td>2244</td>
    </tr>
    <tr>
      <th>21</th>
      <td>Cereal</td>
      <td>2013</td>
    </tr>
    <tr>
      <th>22</th>
      <td>Breakfast Foods</td>
      <td>2009</td>
    </tr>
    <tr>
      <th>23</th>
      <td>Single-Serve Cups</td>
      <td>1854</td>
    </tr>
    <tr>
      <th>24</th>
      <td>Green</td>
      <td>1808</td>
    </tr>
    <tr>
      <th>25</th>
      <td>Chewing Gum</td>
      <td>1721</td>
    </tr>
    <tr>
      <th>26</th>
      <td>Fruit</td>
      <td>1650</td>
    </tr>
    <tr>
      <th>27</th>
      <td>Bars</td>
      <td>1630</td>
    </tr>
    <tr>
      <th>28</th>
      <td>Nuts</td>
      <td>1604</td>
    </tr>
    <tr>
      <th>29</th>
      <td>Nuts &amp; Seeds</td>
      <td>1555</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
  </tbody>
</table>
<p>475 rows × 2 columns</p>
</div>



How about we start looking at recalled products? Maybe a certain category gets a lot of recalls? 


```python
#execute SQL query
cur.execute('SELECT c.category_name, count(*) as NumRecalls from\
                Category c Join CategoryAssignment ca on c.category_id = ca.category_id\
                JOIN recalledproduct rp on ca.product_id = rp.product_id\
                where ca.product_id in (select product_id from recalledproduct)\
                group by c.category_name order by NumRecalls DESC;')

#fetch table from the cursor
category_breakdown_recalls = pd.DataFrame(cur.fetchall())
```


```python
category_breakdown_recalls
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Grocery &amp; Gourmet Food</td>
      <td>158</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Bars</td>
      <td>6</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Nut</td>
      <td>5</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Snack Foods</td>
      <td>4</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Single Herbs &amp; Spices</td>
      <td>3</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Butter</td>
      <td>3</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Energy &amp; Nutritional</td>
      <td>3</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Cereal</td>
      <td>3</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Candy &amp; Chocolate</td>
      <td>3</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Breakfast Foods</td>
      <td>3</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Breakfast &amp; Cereal Bars</td>
      <td>3</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Chocolate</td>
      <td>3</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Garlic</td>
      <td>2</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Peanut</td>
      <td>2</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Peanut Butter</td>
      <td>2</td>
    </tr>
    <tr>
      <th>15</th>
      <td>Cooking &amp; Baking</td>
      <td>2</td>
    </tr>
    <tr>
      <th>16</th>
      <td>Nut Butters</td>
      <td>2</td>
    </tr>
    <tr>
      <th>17</th>
      <td>Seasoned Coatings</td>
      <td>1</td>
    </tr>
    <tr>
      <th>18</th>
      <td>Cocoa</td>
      <td>1</td>
    </tr>
    <tr>
      <th>19</th>
      <td>Dips &amp; Spreads</td>
      <td>1</td>
    </tr>
    <tr>
      <th>20</th>
      <td>Crackers</td>
      <td>1</td>
    </tr>
    <tr>
      <th>21</th>
      <td>Beef</td>
      <td>1</td>
    </tr>
    <tr>
      <th>22</th>
      <td>Leaveners &amp; Yeasts</td>
      <td>1</td>
    </tr>
    <tr>
      <th>23</th>
      <td>Stews</td>
      <td>1</td>
    </tr>
    <tr>
      <th>24</th>
      <td>Cookies</td>
      <td>1</td>
    </tr>
    <tr>
      <th>25</th>
      <td>Chili</td>
      <td>1</td>
    </tr>
    <tr>
      <th>26</th>
      <td>Allspice</td>
      <td>1</td>
    </tr>
    <tr>
      <th>27</th>
      <td>Trail Mix</td>
      <td>1</td>
    </tr>
    <tr>
      <th>28</th>
      <td>Beverages</td>
      <td>1</td>
    </tr>
    <tr>
      <th>29</th>
      <td>Hot Cocoa</td>
      <td>1</td>
    </tr>
    <tr>
      <th>30</th>
      <td>Breadcrumbs &amp; Seasoned Coatings</td>
      <td>1</td>
    </tr>
    <tr>
      <th>31</th>
      <td>Beef Soups</td>
      <td>1</td>
    </tr>
    <tr>
      <th>32</th>
      <td>Canned &amp; Jarred Food</td>
      <td>1</td>
    </tr>
    <tr>
      <th>33</th>
      <td>Ranch</td>
      <td>1</td>
    </tr>
    <tr>
      <th>34</th>
      <td>Breadcrumbs</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



All of our products are in the Grocery and Gourmet Food category, but it looks like Canned Dry & Packaged Foods might be the biggest headache for Amazon.</br>
What about brands? What is the range of number of recalls that a single brand endured within the time frame of our recall data set?


```python
#execute SQL query
cur.execute('SELECT b.brand_id, count(*) as NumRecalls from\
                Brand b Join Product p on b.brand_id = p.brand_id\
                join recalledproduct rp on p.product_id = rp.product_id\
                group by b.brand_id order by NumRecalls DESC;')

#fetch table from the cursor
brand_breakdown = pd.DataFrame(cur.fetchall())
```


```python
brand_breakdown
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>5158</td>
      <td>13</td>
    </tr>
    <tr>
      <th>1</th>
      <td>7169</td>
      <td>8</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2650</td>
      <td>8</td>
    </tr>
    <tr>
      <th>3</th>
      <td>9864</td>
      <td>8</td>
    </tr>
    <tr>
      <th>4</th>
      <td>6327</td>
      <td>5</td>
    </tr>
    <tr>
      <th>5</th>
      <td>1154</td>
      <td>5</td>
    </tr>
    <tr>
      <th>6</th>
      <td>8812</td>
      <td>4</td>
    </tr>
    <tr>
      <th>7</th>
      <td>7259</td>
      <td>4</td>
    </tr>
    <tr>
      <th>8</th>
      <td>8705</td>
      <td>3</td>
    </tr>
    <tr>
      <th>9</th>
      <td>3321</td>
      <td>3</td>
    </tr>
    <tr>
      <th>10</th>
      <td>4942</td>
      <td>2</td>
    </tr>
    <tr>
      <th>11</th>
      <td>6382</td>
      <td>2</td>
    </tr>
    <tr>
      <th>12</th>
      <td>3802</td>
      <td>2</td>
    </tr>
    <tr>
      <th>13</th>
      <td>8864</td>
      <td>2</td>
    </tr>
    <tr>
      <th>14</th>
      <td>6689</td>
      <td>2</td>
    </tr>
    <tr>
      <th>15</th>
      <td>845</td>
      <td>2</td>
    </tr>
    <tr>
      <th>16</th>
      <td>7927</td>
      <td>2</td>
    </tr>
    <tr>
      <th>17</th>
      <td>7497</td>
      <td>2</td>
    </tr>
    <tr>
      <th>18</th>
      <td>8337</td>
      <td>2</td>
    </tr>
    <tr>
      <th>19</th>
      <td>3127</td>
      <td>2</td>
    </tr>
    <tr>
      <th>20</th>
      <td>985</td>
      <td>2</td>
    </tr>
    <tr>
      <th>21</th>
      <td>91</td>
      <td>1</td>
    </tr>
    <tr>
      <th>22</th>
      <td>8366</td>
      <td>1</td>
    </tr>
    <tr>
      <th>23</th>
      <td>8344</td>
      <td>1</td>
    </tr>
    <tr>
      <th>24</th>
      <td>2683</td>
      <td>1</td>
    </tr>
    <tr>
      <th>25</th>
      <td>2100</td>
      <td>1</td>
    </tr>
    <tr>
      <th>26</th>
      <td>7326</td>
      <td>1</td>
    </tr>
    <tr>
      <th>27</th>
      <td>6086</td>
      <td>1</td>
    </tr>
    <tr>
      <th>28</th>
      <td>230</td>
      <td>1</td>
    </tr>
    <tr>
      <th>29</th>
      <td>1410</td>
      <td>1</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
  </tbody>
</table>
<p>63 rows × 2 columns</p>
</div>



Don't forget to close your connection!


```python
conn.close()
```

This tutorial can be found in Jupyter Notebook form [here]({{site.url}}/notebooks/using-unsafefoods-db.ipynb).