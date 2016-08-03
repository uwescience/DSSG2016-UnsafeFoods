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
  select(-reviewerID, -reviewerName, -helpful)

## Export CSV
write.csv(amz_recall, "recalled_amz.csv", row.names = FALSE)

## Export a single product for testing
amz_recall %>%
  filter(asin == "B000DZDJ0K") %>%
  write.csv("single_recalled_amz.csv", row.names = FALSE)

amz_recall %>%
  filter(asin == "B001DGYKG0") %>%
  write.csv("single_recalled_amz_2.csv", row.names = FALSE)

## Load metadata
metadata <- read.csv("../data/processed/meta_Grocery_and_Gourmet_Food.csv",
                     stringsAsFactors = FALSE)

asins_titles <- metadata %>%
  filter(asin %in% recalled$asin) %>%
  select(asin, title)

write.csv(asins_titles, "asins_titles.csv")
