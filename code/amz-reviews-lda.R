##########################################################
####  Visualizing topics in Amazon reviews using LDA  ####
##########################################################

## LDA code based on: http://cpsievert.github.io/LDAvis/reviews/reviews.html

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

## Load 5-core Amazon review data
json_5 <- "../data/raw/reviews_Grocery_and_Gourmet_Food_5.json"
amz5 <- fromJSON(sprintf("[%s]", paste(readLines(json_5), collapse=",")))

## Function to put documents into the format required by the lda package:
get_terms <- function(x, vocab) {
  index <- match(x, vocab)
  index <- index[!is.na(index)]
  rbind(as.integer(index - 1), as.integer(rep(1, length(index))))
}

## Function to generate topic model and visualization
topic_model_vis <- function(data, obs_n = 1000, K = 10, seed = 30, dir) {

  ## Take a random sample of obs_n reviews
  set.seed(seed)
  reviews <- sample(data, size = obs_n)

  ## pre-processing:
  reviews <- tolower(reviews)                   # force to lowercase
  reviews <- gsub("'", "", reviews)             # remove apostrophes
  reviews <- gsub("[^a-zA-Z\\s]", " ", reviews)  # remove non-letter characters

  ## tokenize on spaces (any number of spaces) and output as a list:
  doc.list <- strsplit(reviews, "\\s+")

  ## stem words
  doc.list <- lapply(doc.list, stemDocument)

  ## compute the table of terms:
  term.table <- table(unlist(doc.list))
  term.table <- sort(term.table, decreasing = TRUE)

  ## stopwords:
  stop_words <- stopwords("SMART")

  ## remove terms that are stop words or occur fewer than 10 times or are empty
  ## strings:
  del <- names(term.table) %in% stop_words |
    term.table < 10 |
    names(term.table) == ""
  term.table <- term.table[!del]
  vocab <- names(term.table)

  ## Put documents into format required by LDA
  documents <- lapply(doc.list, get_terms, vocab = vocab)

  ## Compute some statistics related to the data set:
  D <- length(documents)                # number of documents
  W <- length(vocab)                    # number of terms in the vocab
  doc.length <- sapply(documents, function(x) sum(x[2, ]))  # number of tokens
                                        # per document
  N <- sum(doc.length)                     # total number of tokens in the data
  term.frequency <- as.integer(term.table) # frequencies of terms in the corpus

  ## MCMC and model tuning parameters:
  G <- 5000
  alpha <- 0.02
  eta <- 0.02

  ## Fit the model:
  set.seed(seed)
  fit <- lda.collapsed.gibbs.sampler(documents = documents, K = K, vocab = vocab, 
                                     num.iterations = G, alpha = alpha, 
                                     eta = eta, initial = NULL, burnin = 0,
                                     compute.log.likelihood = TRUE)
  
  ## Visualizing
  theta <- t(apply(fit$document_sums + alpha, 2, function(x) x/sum(x)))
  phi <- t(apply(t(fit$topics) + eta, 2, function(x) x/sum(x)))

  amz_reviews <- list(phi = phi,
                      theta = theta,
                      doc.length = doc.length,
                      vocab = vocab,
                      term.frequency = term.frequency)



  ## Create the JSON object to feed the visualization:
  json <- createJSON(phi = amz_reviews$phi, 
                     theta = amz_reviews$theta, 
                     doc.length = amz_reviews$doc.length, 
                     vocab = amz_reviews$vocab, 
                     term.frequency = amz_reviews$term.frequency)

  serVis(json, out.dir = dir, open.browser = FALSE)
  
}

## Extract reviewText column
reviews <- amz$reviewText

## Random sample of 1000 reviews; 10 topics
topic_model_vis(reviews, obs_n = 1000, K = 10, dir = "../figs/n1000")

## View topics for one-star reviews
onestar <- amz[amz$overall == 1, "reviewText"]
topic_model_vis(onestar, obs_n = 2000, K = 7, dir = "../figs/n2000onestar")

## Replicate Mike's NMF approach using 5-core data with reviews of <5 stars
reviews5 <- amz5[amz5$overall < 5, "reviewText"]
topic_model_vis(reviews5, obs_n = length(reviews5), K = 15,
                dir = "../figs/5coreno5star")

## Serve the resulting file -- this should open a browser with an interactive
## visualization of the topics and frequent terms for each topic
httd(dir = "../figs/5coreno5star/")
