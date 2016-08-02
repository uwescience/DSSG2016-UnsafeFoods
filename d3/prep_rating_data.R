
## Load required packages
library("jsonlite")
library("dplyr")

## Load Amazon review data
json_file <- "../data/raw/reviews_Grocery_and_Gourmet_Food.json"
amz <- stream_in(file(json_file))

## Load list of recalled products
recalled <- read.csv("../github_data/asin_intersection_full.csv",
                     stringsAsFactors = FALSE)

## Extract vector of ASINs of recalled products
recalled_asins <- unique(recalled$asin) %>%
  sapply(strsplit, ";") %>%
  unname() %>%
  unlist()

## Keep only recalled products
amz_recall <- filter(amz, asin %in% recalled_asins) %>%
  select(-reviewerID, -reviewerName, -helpful)

## TODO: merge with metadata to get product name

## Export CSV
write.csv(amz_recall, "recalled_amz.csv", row.names = FALSE)

## Export a single product for testing
amz_recall %>%
  filter(asin == "B000DZDJ0K") %>%
  write.csv("single_recalled_amz.csv", row.names = FALSE)
  
