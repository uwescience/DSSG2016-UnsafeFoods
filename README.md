# Mining Online Data for Early Identification of Unsafe Food Products

Materials for the
[Mining Online Data for Early Identification of Unsafe Food Products](http://escience.washington.edu/dssg/project-summaries-2016/)
project from the UW eScience Institute's
[Data Science for Social Good](http://escience.washington.edu/dssg/) program.

## Files

* `asins/` folder contains ASINs (Amazon Standard ID Numbers) corresponding to
  the UPCs in the `upcs/` folder and `asin_intersection.txt`
* `asins/asin-intersection.txt`: List of ASINs that appear in both FDA recall
   and amazon grocery and gourmet food review  datasets
* `asins/asin-intersection_health.txt`: List of ASINs that appear in both FDA recall
   and amazon health care review datasets
* `code/data-preprocessing.py`: Functions for data processing
* `code/amz-reviews-to-strict-json.py`: Code to convert the raw Amazon review
  file to strict JSON
* `code/amz-reviews-lda.R`: Code to conduct LDA topic modeling and create
  interactive visualizations in R
* `code/enforcement-data-merge.R`: Code to extract data on food products from
  the weekly FDA enforcement reports and generate one large CSV from the 200+
  weekly CSVs.
* `notebooks/Fetching ASINs (FINALLY).ipynb`: Code to gather all ASINs for a
  file of UPCs
* `notebooks/NLTK Workbook.ipynb`: Notebook to create a corpus from the Amazon
  review data
* `notebooks/NMF_exploration.ipynb`: iPython notebook that uses NMF to obtain
  topic results for subset of Amazon Review Data
* `notebooks/join_review-recall notebook.ipynb`: iPython notebook that constructs
  dataframe of amazon reviews, product metadata and recall status from 
  `reviews_Grocery_and_Gourmet_Food.json.jz`,`meta_Grocery_and_Gourmet_Food.json.gz'
   and `asin_intersection.txt`
* `upcs/` folder contains all of the UPCs from the FDA recalls, split into four
  files
* `github_data/` folder contains small data files to be stored on github 
  (rather than being in the ignored data folder)
* `github_data/amazon_product_categories.csv`: CSV file storing the amazon product
   category hierarchy. The first column contains each category name, and the second
   column contains the "parent" category". 
  
### Data

The contents of `data/` are ignored by git, but this is what it should contain:

* `data/raw/reviews_Grocery_and_Gourmet_Food.json.gz` is from
  http://jmcauley.ucsd.edu/data/amazon/links.html -- scroll down to
  "Per-category files" and select the Grocery and Gourmet Food reviews file.
  Note this is NOT the 5-core reviews file that appears under the "Files" header
  on the web page. This data file should have 1,297,156 reviews. This file is
  not strict JSON, but can be converted to strict JSON with
  `amz-reviews-to-strict-json.py`, which will output a file to the
  `data/processed/` folder.
* `data/raw/meta_Grocery_and_Gourmet_Food.json.gz' is is from
  http://jmcauley.ucsd.edu/data/amazon/links.html -- scroll down to
  "Per-category files" and select the Grocery and Gourmet Food metadata file.
  This data file should have 171,760 products.
* `data/raw/FDA_recalls.xml` -- this is the FDA recall data in XML form. In theory,
  this data should be available from data.gov at
  https://catalog.data.gov/dataset/all-fda-recalls-1ae7b, however the link on
  that page is broken. We used the Wayback machine to access a previous version
  of this data here:
  https://web.archive.org/web/20150504011324/http://www.fda.gov/DataSets/Recalls/RecallsDataSet.xml.
  In R, this can be converted to a CSV with the following code (assumes that the
  XML data is saved as a file called `FDA_recalls.xml`):
  
```R
## Install the XML package if it is not already installed
if(!"XML" %in% installed.packages()) {
  install.packages("XML")
}
## Load the XML package
library("XML")

## Parse XML
doc <- xmlTreeParse("FDA_recalls.xml", useInternalNodes = TRUE)

## Convert to data frame
dat <- xmlToDataFrame(doc)

## Write to CSV
write.csv(dat, "../processed/FDA_recalls.csv", row.names = FALSE)
```

* `data/raw/FDA-enforcement/` is a folder that contains weekly FDA enforcement
  reports downloaded manually from
  http://www.accessdata.fda.gov/scripts/ires/index.cfm. This data goes back to
  mid 2012.
* `data/processed/FDA_food_enforcements_2012-06_to_2016-07.csv` has data from
  the weekly enforcement reports for food products as one large file.
