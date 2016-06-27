# Mining Online Data for Early Identification of Unsafe Food Products

Materials for the
[Mining Online Data for Early Identification of Unsafe Food Products](http://escience.washington.edu/dssg/project-summaries-2016/)
project from the UW eScience Institute's
[Data Science for Social Good](http://escience.washington.edu/dssg/) program.

## Files

* `code/data-preprocessing.py`: Functions for data processing
* `notebooks/NLTK Workbook.ipynb`: Notebook to create a corpus from the Amazon
  review data
* `notebooks/Fetching ASINs (FINALLY).ipynb`: Code to gather all ASINs for a
  file of UPCs
* `upcs/` folder contains all of the UPCs from the FDA recalls, split into four
  files
* `data/reviews_Grocery_and_Gourmet_Food.json.gz` is from
  http://jmcauley.ucsd.edu/data/amazon/links.html -- scroll down to
  "Per-category files" and select the Grocery and Gourmet Food reviews file.
  Note this is NOT the 5-core reviews file that appears under the "Files" header
  on the web page. This data file should have 1,297,156 reviews.
* `data/FDA_recalls.xml` -- this is the FDA recall data in XML form. In theory,
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
write.csv(dat, "FDA_recalls.csv", row.names = FALSE)
```

## Repository Structure

Raw data files should be placed in `data/raw/`. They won't be tracked by git
because the `.gitignore` contains `data/*`.

```
DSSG2016-UnsafeFoods/
├── .gitignore
├── README.md
├── asins
│   └── asins-1.txt
├── code
│   ├── data-preprocessing.py
├── data
│   ├── processed
│   │   └── FDA_recalls.csv
│   └── raw
│       ├── FDA_recalls.xml
│       ├── reviews_Grocery_and_Gourmet_Food.json.gz
├── notebooks
│   ├── Fetching\ ASINs\ (FINALLY).ipynb
│   └── NLTK\ Workbook.ipynb
└── upcs
    ├── upcs-1.txt
    ├── upcs-2.txt
    ├── upcs-3.txt
    └── upcs-4.txt
```
