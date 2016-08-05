##################################################
####  Discriminant NMF on Amazon review data  ####
##################################################

## Load required packages
library("jsonlite")
library("DNMF")
library("tm")
library("dplyr")

## Load Amazon review data
json_file <- "../data/raw/reviews_Grocery_and_Gourmet_Food.json"
amz <- stream_in(file(json_file))

## Load list of recalled products
recalled <- read.csv("../data/processed/recalls_upcs_asins_joined.csv",
                     stringsAsFactors = FALSE)

## Extract vector of ASINs of recalled products
recalled_asins <- unique(recalled$asins) %>%
  sapply(strsplit, ";") %>%
  unname() %>%
  unlist()

## Add recalled/not recalled column to Amazon reviews based on vector of ASINs
amz <- mutate(amz, recalled = ifelse(asin %in% recalled_asins, 1, 2))

## Set seed for reproducibility
set.seed(123)

## Subset data -- 1000 rows each for recalled and non-recalled reviews
amz_sub <- amz %>%
  group_by(recalled) %>%
  sample_n(1000)
  
## Vector of Amazon review text
reviews <- amz_sub$reviewText

## Create corpus
corp <- Corpus(VectorSource(reviews))

## Clean up data
corp <- tm_map(corp, removePunctuation)   
corp <- tm_map(corp, removeNumbers)
corp <- tm_map(corp, tolower)
corp <- tm_map(corp, removeWords, stopwords("english"))
corp <- tm_map(corp, stemDocument)
corp <- tm_map(corp, stripWhitespace)  
corp <- tm_map(corp, PlainTextDocument)   

## Create term document matrix
tdm <- TermDocumentMatrix(corp)

## Vector of 1 and 2 indicating recalled and not recalled
trainlabel <- amz_sub$recalled

## Run DNMF
dnmf_output <- DNMF(tdm, trainlabel)
