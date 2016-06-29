##########################################################
####  Visualizing topics in Amazon reviews using LDA  ####
##########################################################

## LDA code from: http://cpsievert.github.io/LDAvis/reviews/reviews.html

## Install any necessary packages
for (pkg in c("jsonlite", "lda", "tm", "LDAvis", "servr")) {
  if(!pkg %in% installed.packages()) {
    install.packages(pkg)
  }
}

## Load packages
library("jsonlite")
library("lda")
library("tm")
library("LDAvis")
library("servr")

## Load Amazon review data
json_file <- "../data/processed/reviews_Grocery_and_Gourmet_Food_strict.json"
amz <- fromJSON(sprintf("[%s]", paste(readLines(json_file), collapse=",")))

## Take a random sample of 4000 reviews (so the code doesn't take forever)
set.seed(20)
reviews <- sample(amz$reviewText, 4000)

## read in some stopwords:
stop_words <- stopwords("SMART")

## pre-processing:
reviews <- gsub("'", "", reviews)  # remove apostrophes
reviews <- gsub("[[:punct:]]", " ", reviews)  # replace punctuation with space
reviews <- gsub("[[:cntrl:]]", " ", reviews)  # replace control characters with space
reviews <- gsub("^[[:space:]]+", "", reviews) # remove whitespace at beginning
                                              # of documents
reviews <- gsub("[[:space:]]+$", "", reviews) # remove whitespace at end of documents
reviews <- tolower(reviews)  # force to lowercase

## tokenize on space and output as a list:
doc.list <- strsplit(reviews, "[[:space:]]+")

## compute the table of terms:
term.table <- table(unlist(doc.list))
term.table <- sort(term.table, decreasing = TRUE)

## remove terms that are stop words or occur fewer than 5 times:
del <- names(term.table) %in% stop_words | term.table < 5
term.table <- term.table[!del]
vocab <- names(term.table)

## now put the documents into the format required by the lda package:
get.terms <- function(x) {
  index <- match(x, vocab)
  index <- index[!is.na(index)]
  rbind(as.integer(index - 1), as.integer(rep(1, length(index))))
}
documents <- lapply(doc.list, get.terms)

## Compute some statistics related to the data set:
D <- length(documents)  # number of documents
W <- length(vocab)  # number of terms in the vocab
doc.length <- sapply(documents, function(x) sum(x[2, ]))  # number of tokens per
                                                          # document
N <- sum(doc.length)  # total number of tokens in the data
term.frequency <- as.integer(term.table)  # frequencies of terms in the corpus

# MCMC and model tuning parameters:
K <- 15                                 # 15 topics
G <- 5000
alpha <- 0.02
eta <- 0.02

# Fit the model:

set.seed(357)
t1 <- Sys.time()
fit <- lda.collapsed.gibbs.sampler(documents = documents, K = K, vocab = vocab, 
                                   num.iterations = G, alpha = alpha, 
                                   eta = eta, initial = NULL, burnin = 0,
                                   compute.log.likelihood = TRUE)
t2 <- Sys.time()
t2 - t1                                 # Takes 3.7 minutes on Kara's machine


## Visualizing
theta <- t(apply(fit$document_sums + alpha, 2, function(x) x/sum(x)))
phi <- t(apply(t(fit$topics) + eta, 2, function(x) x/sum(x)))

amz_reviews <- list(phi = phi,
                     theta = theta,
                     doc.length = doc.length,
                     vocab = vocab,
                     term.frequency = term.frequency)



# create the JSON object to feed the visualization:
json <- createJSON(phi = amz_reviews$phi, 
                   theta = amz_reviews$theta, 
                   doc.length = amz_reviews$doc.length, 
                   vocab = amz_reviews$vocab, 
                   term.frequency = amz_reviews$term.frequency)

serVis(json, out.dir = "../figs", open.browser = FALSE)

## Serve the resulting file -- this should open a browser with an interactive
## visualizaiton of the topics and frequent terms for each topic
httd(dir = "../figs")
