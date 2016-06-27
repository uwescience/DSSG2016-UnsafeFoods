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
