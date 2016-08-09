##########################
####  Supervised LDA  ####
##########################

## Packages
package_reqs <- c("jsonlite", "dplyr", "tm", "lda")

## Install any necessary packages
for (pkg in package_reqs) {
  if(!pkg %in% installed.packages()) {
    install.packages(pkg)
  }
}

## Load packages
sapply(package_reqs, library, character.only = TRUE)

## Source file that contains, among other things, a function to put documents
## into the format required by the lda package
source("lda-R-funs.R")

## Load Amazon review data
json_file <- "../data/raw/reviews_Grocery_and_Gourmet_Food.json"
amz <- stream_in(file(json_file))

## Load list of recalled products
recalled <- read.csv("../github_data/asin_intersection_full.csv",
                     stringsAsFactors = FALSE)

## Extract vector of ASINs of recalled products
recalled_asins <- unique(recalled$asin)

## Add recalled/not recalled column to Amazon reviews based on vector of ASINs
amz <- mutate(amz, recalled = ifelse(asin %in% recalled_asins, 1, 0))

## Extract vector of non-recalled ASINs
non_recalled_asins <- unique(amz[amz$recalled == 0, "asin"])

## Set seed for reproducibility
set.seed(123)

## Randomly samply 80% each of recalled and non-recalled asins for training set
training_asins <- c(sample(recalled_asins,
                           size = round(length(recalled_asins) * 0.8)),
                    sample(non_recalled_asins,
                           size = round(length(non_recalled_asins) * 0.8)))

## Use remaining asins for test set
testing_asins <- unique(amz$asin)[!unique(amz$asin) %in% training_asins]

## Subset data to create training set (and remove any empty reviews)
training <- filter(amz, asin %in% training_asins & reviewText != "") %>%
  sample_n(10000) %>%
  arrange(recalled)

## Vector of Amazon review text
training_reviews <- training$reviewText

## Vector of recalled/not-recalled column to be used as annotations for slda
## model
annotations <- as.integer(training$recalled)

## Process data and format as needed for the lda package
vec_to_lda_corpus <- function(vec) {

  vec <- tolower(vec)                   # force to lowercase
  vec <- gsub("'", "", vec)             # remove apostrophes
  vec <- gsub("[^a-zA-Z\\s]", " ", vec)  # remove non-letter characters

  ## tokenize on spaces (any number of spaces) and output as a list:
  doc.list <- strsplit(vec, "\\s+")

  ## stem words
  doc.list <- lapply(doc.list, stemDocument)

  ## compute the table of terms:
  term.table <- table(unlist(doc.list))
  term.table <- sort(term.table, decreasing = TRUE)
  
  ## stopwords:
  stop_words <- stopwords("SMART")

  ## remove terms that are stop words or empty strings:
  del <- names(term.table) %in% stop_words | names(term.table) == ""
  term.table <- term.table[!del]
  vocab <- names(term.table)

  ## Put documents into format required by lda package. get_terms function comes
  ## from lda-R-funs.R
  docs <- lapply(doc.list, get_terms, vocab = vocab)

  return(list(docs = docs, vocab = vocab))
}

documents <- vec_to_lda_corpus(training_reviews)

## Documents that are length zero need to get removed. These exist because of
## cases like having a review that contains only the word "A+" -- the + gets
## removed as a non-letter character, and the A gets removed as a stopword.
remove <- sapply(documents$docs, function(x) length(x) == 0)

docs_nonzero <- documents$docs[!remove]
annotations <- annotations[!remove]

## Fit slda:
## slda.em(documents, K, vocab, num.e.iterations, num.m.iterations, alpha,
## eta, annotations, params, variance, logistic = FALSE, lambda = 10,
## regularise = FALSE, method = "sLDA", trace = 0L, MaxNWts=3000)
ntopics <- 50                           # Number of topics to generate

fit <- slda.em(documents = docs_nonzero,
               K = ntopics,
               vocab = documents$vocab,
               num.e.iterations = 100,
               num.m.iterations = 100,
               alpha = 1.0,
               eta = 0.1,
               annotations = annotations,
               params = sample(c(-1, 1), ntopics, replace = TRUE),
               variance = 0.25,
               logistic = TRUE)


## Test set
testing <- filter(amz, asin %in% testing_asins & reviewText != "") %>%
  sample_n(2000) %>%
  arrange(recalled)
 
## Documents
test_docs <- vec_to_lda_corpus(testing$reviewText)

## Annotations (0 = not recalled, 1 = recalled)
test_annotations <- as.integer(testing$recalled)

## Remove any zero-length documents that might exist. Also remove their
## corresponding annotations
test_remove <- sapply(test_docs$docs, function(x) length(x) == 0)
test_docs_nonzero <- test_docs$docs[!test_remove]
test_annotations <- test_annotations[!test_remove]

## Test model
test_prediction <- slda.predict(documents = test_docs_nonzero,
                                topics = fit$topics,
                                model = fit$model,
                                alpha = 1.0,
                                eta = 0.1)

## View summary of predictions for non-recalled and recalled products
summary(test_prediction[which(test_annotations == 0)])
summary(test_prediction[which(test_annotations == 1)])
