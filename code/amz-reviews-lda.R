##########################################################
####  Visualizing topics in Amazon reviews using LDA  ####
##########################################################

## Load functions for doing LDA
source("lda-R-funs.R")

## Load Amazon review data
json_file <- "../data/processed/reviews_Grocery_and_Gourmet_Food_strict.json"
amz <- fromJSON(sprintf("[%s]", paste(readLines(json_file), collapse=",")))

## Load 5-core Amazon review data
json_5 <- "../data/raw/reviews_Grocery_and_Gourmet_Food_5.json"
amz5 <- fromJSON(sprintf("[%s]", paste(readLines(json_5), collapse=",")))

## Extract reviewText column from full review dataset
reviews <- amz$reviewText

## Random sample of 1000 reviews; 10 topics
topic_model_vis(reviews, obs_n = 1000, K = 10, dir = "../figs/n1000")

## View topics for one-star reviews
onestar <- amz[amz$overall == 1, "reviewText"]
topic_model_vis(onestar, obs_n = 2000, K = 7, dir = "../figs/n2000onestar")

## Replicate Mike's NMF approach using 5-core data with reviews of <5 stars
reviews5 <- amz5[amz5$overall < 5, "reviewText"]
topic_model_vis(reviews5, obs_n = length(reviews5), K = 15, G = 1000,
                dir = "../figs/5coreno5star")

## Serve the resulting file -- this should open a browser with an interactive
## visualization of the topics and frequent terms for each topic
httd(dir = "../figs/5coreno5star/")

###########################################################################
####  Compare reviews for recalled products and non-recalled products  ####
###########################################################################

## List of recalled products
recalled <- read.csv("../data/processed/recalls_upcs_asins_joined.csv",
                     stringsAsFactors = FALSE)

## Vector of ASINs from recalled products
recalled_asins <- unique(recalled$asins) %>%
  sapply(strsplit, ";") %>%
  unname() %>%
  unlist()

## Extract reviews matching these ASINs
amz_recalled <- amz %>%
  filter(asin %in% recalled_asins)

## Number of reviews of recalled products
n <- nrow(amz_recalled)

## Visualize topics for recalled products
topic_model_vis(amz_recalled$reviewText, obs_n = n, K = 20, G = 1000,
                dir = "../figs/recalled_products")

httd(dir = "../figs/recalled_products/")

## Create a visualization for non-recalled products with same parameters (number
## of reviews, number of clusters, sampling iterations, etc.)
nonrecalled <- filter(amz, !asin %in% recalled_asins)

topic_model_vis(nonrecalled$reviewText, obs_n = n, K = 20, G = 1000,
                dir = "../figs/non_recalled_products")

httd(dir = "../figs/non_recalled_products/")

## Export CSVs of topics to share with team
recalled_topic_table <- topic_table("../figs/recalled_products/lda.json")
write.csv(recalled_topic_table,
          "../figs/recalled_products/recalled_topic_table.csv",
          row.names = FALSE)

non_recalled_topic_table <- topic_table("../figs/non_recalled_products/lda.json")
write.csv(non_recalled_topic_table,
          "../figs/non_recalled_products/non_recalled_topic_table.csv",
          row.names = FALSE)

###############################################
####  Termite diagram of terms vs. topics  ####
###############################################

## Create static visualization inspired by:
## http://vis.stanford.edu/papers/termite

## TODO: Filter data by top terms overall, not top terms within topics. The way
## the data gets subset now, it discards information about prevalence of terms
## in other topics.

termite_table <- function(json_file, nwords = 15) {

  ## json_file: location (as a string) of the JSON file created by
  ## topic_model_vis

  ## nwords: number of words to show for each topic

  json_data <- fromJSON("../figs/recalled_products/lda.json") %>% 
    .$token.table %>%         
    as.data.frame()

  ## Terms with highest frequency 
  json_data %>%
    arrange(desc(Freq)) %>%
    top_n(60)

  ntopics <- length(unique(json_data$Topic)) # Number of topics

  output_table <- json_data %>%
    mutate(Topic = paste("Topic",
                         sprintf("%02d", Topic),
                         " ")) %>%      # Add "Topic" to topic number
    group_by(Topic) %>%
    arrange(desc(Freq)) %>%           # Arrange rows in descending Freq by topic
    top_n(nwords) %>%                 # Choose top n words per topic
    ungroup()

  return(output_table)
}

recalled_termite_table <- termite_table("../figs/recalled_products/lda.json",
                                        nwords = 5) %>%
  mutate(Term = as.character(Term))

termite_plot <- ggplot(recalled_termite_table, aes(x = Topic, y = Term, size = Freq)) +
  geom_point(alpha = 0.5) +
  scale_y_discrete(limits = recalled_termite_table$Term) +
  theme_gray() +
  theme(axis.text.y = element_text(size = 7),
        axis.text.x = element_text(size = 7, angle = 45, hjust = 1),
        legend.position = "none")

ggdraw(switch_axis_position(termite_plot, axis = 'x')) %>%
  ggsave("../figs/termite_plot.png", ., width = 8, height = 12)

