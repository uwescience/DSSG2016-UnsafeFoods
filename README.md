# Mining Online Data for Early Identification of Unsafe Food Products

Materials for the
[Mining Online Data for Early Identification of Unsafe Food Products](http://escience.washington.edu/dssg/project-summaries-2016/)
project from the UW eScience Institute's
[Data Science for Social Good](http://escience.washington.edu/dssg/) program.

## Files

* `data-preprocessing.py`: Functions for data processing

## Repository Structure

Raw data files should be placed in `data/raw/`. They won't be tracked by git
because the `.gitignore` contains `data/*`.

```
DSSG2016-UnsafeFoods/
├── .gitignore
├── README.md
├── code/
│   └── data-preprocessing.py
└── data/
    ├── processed/
    │   └── FDA_recalls.csv
    └── raw/
        ├── FDA_recalls.xml
        └── reviews_Grocery_and_Gourmet_Food.json.gz
```
