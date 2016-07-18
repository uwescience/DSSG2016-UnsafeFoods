###################################################
####  Join FDA weekly enforcement report data  ####
###################################################

library("dplyr")

## List of filenames
files <- paste0("../data/raw/FDA-enforcement/",
                list.files("../data/raw/FDA-enforcement/", pattern = "*.csv"))

## List of datasets
datalist <- lapply(files, read.csv, stringsAsFactors = FALSE)

## Do the datasets all have the same number of headers? The exact same headers
## in the same order?
lapply(datalist, function(x) length(colnames(x)))

## They don't all have the same number of headers. It looks like these are the
## core headers, and then there can be any number of columns like
## "More.Code.Info", "More.Code.Info.1", etc.
common_names <- c("Product.Type", "Event.ID", "Status", "Recalling.Firm",
                  "Address1", "Address2", "City", "State.Province",
                  "Postal.Code", "Country", "Voluntary.Mandated",
                  "Initial.Firm.Notification.of.Consignee.or.Public",
                  "Distribution.Pattern", "Recall.Number", "Classification",
                  "Product.Description", "Product.Quantity",
                  "Reason.for.Recall", "Recall.Initiation.Date",
                  "Center.Classification.Date", "Termination.Date",
                  "Report.Date", "Code.Info")

## Do all datasets have at least the common_names headers?
lapply(datalist, function(x) all(common_names %in% colnames(x))) %>%
  unlist() %>%
  all()                                 # Yes

## Are the first 23 columns always in the same order?
lapply(datalist, function(x) colnames(x)[1:23] == common_names) %>%
  unlist() %>%
  all()                                 # Yes

## What are the headers that are not in the common_names?
lapply(datalist, function(x) colnames(x)[!colnames(x) %in% common_names]) %>%
  unlist() %>%
  unique()                              # They're all "More.Code.Info" cols

## Do all the datasets have >0 rows?
lapply(datalist, function(x) nrow(x) > 0) %>%
  unlist() %>%
  all()                                 # Yes

## Subset to only the data for food products
data_food <- lapply(datalist, function(x) filter(x, Product.Type == "Food"))

## Combine into one data frame
data_df <- bind_rows(data_food)

## Some (all?) of the More.Code.Info columns are empty. Look for the columns
## that only contain NAs or empty strings:
cols <- lapply(data_df, function(x) all(is.na(x) | x == ""))
keep <- names(cols[cols == FALSE]) # Non-empty columns

## Keep only the non-empty columns
data_df_keep <- data_df[keep]

## Export keeper columns to CSV
write.csv(data_df_keep,
          "../data/processed/FDA_food_enforcements_2012-06_to_2016-07.csv",
          row.names = FALSE)
