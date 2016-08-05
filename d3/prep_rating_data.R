## Load required packages
library("jsonlite")
library("dplyr")

## Load Amazon review data
json_file <- "../data/raw/reviews_Grocery_and_Gourmet_Food.json"
amz <- stream_in(file(json_file))

## Load list of recalled products
recalled <- read.csv("../github_data/asin_intersection_full.csv",
                     stringsAsFactors = FALSE)

## Keep only recalled products
amz_recall <- filter(amz, asin %in% recalled$asin) %>%
  select(-reviewerID, -reviewerName, -helpful) %>%
  ## Merge in initiation date
  merge(recalled[, c("asin", "initiation_date")], by = "asin")

## Export CSV
write.csv(amz_recall, "recalled_amz.csv", row.names = FALSE)

## Load metadata
metadata <- read.csv("../data/processed/meta_Grocery_and_Gourmet_Food.csv",
                     stringsAsFactors = FALSE)

asins_titles <- metadata %>%
  filter(asin %in% recalled$asin) %>%
  select(asin, title)

write.csv(asins_titles, "asins_titles.csv")
