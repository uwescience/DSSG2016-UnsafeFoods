#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#
## Packages

package_reqs <- c("RPostgreSQL", "ggplot2", 
                  "wordcloud","tm",
                  "igraph", "GGally",
                  "networkD3","shiny", "SnowballC",
                  "dplyr","gridExtra")

## Install any necessary packages
for (pkg in package_reqs) {
  if(!pkg %in% installed.packages()) {
    install.packages(pkg)
  }
}


library(RPostgreSQL)
library(igraph)
library(networkD3)
library(ggplot2)
library(tm)
library(SnowballC)
library(wordcloud)
library(shiny)
library(dplyr)
library(grid)
library(gridExtra)

# create a connection
# save the password that we can "hide" it as best as we can by collapsing it
pw <- {
  "Password1"
}

# loads the PostgreSQL driver
drv <- dbDriver("PostgreSQL")

# creates a connection to the postgres database
# note that "con" will be used later in each connection to the database
con <- dbConnect(drv, dbname = "RecallsReviews2",
                 host = "unsafefoods2.csya4zsfb6y4.us-east-1.rds.amazonaws.com", port = 5432,
                 user = "unsafefoods2", password = pw)

rm(pw) # removes the password

#query product names for the time series option
product_names <- as.vector(dbGetQuery(con, "SELECT distinct product_name from product where 
                            product_id in (select product_id from recalledproduct);"))


# Define UI for application that draws a histogram
ui <- shinyUI(fluidPage(
   
   # Application title
   titlePanel("Amazon Reviews and FDA Recalls- Summary Statistics"),
   
   # Sidebar with a slider input for number of bins 
   sidebarLayout(
      sidebarPanel(
         selectInput("selectVis", "Select Visualization:",
                            c("Ratings Summary" = "rs",
                              "Timeline" = "tl",
                              "Word Cloud" = "wc",
                              "Category Summary"="cs",
                              "Recall Type Summary" = "rt")),
         conditionalPanel(
           condition = "input.selectVis == 'wc'",
           selectInput("wc_data", "Product Name",
                       product_names)
         )
      ),
      
      # Show a plot of the generated distribution
      mainPanel(
         plotOutput("selectedPlot")
      )#,
      
   )
))


# Define server logic required to draw a histogram
server <- shinyServer(function(input, output) {
   
   output$selectedPlot <- renderPlot({
     #ratings summary
     if (input$selectVis == "rs") {
       
       #get rating data from db
       ratings_data <- dbGetQuery(con, "SELECT overall, count(*) as num_reviews from review
                                  where product_id not in (select product_id from recalledproduct)
                                  group by overall;")
       
       #get proportion
       ratings_data$prop_reviews = sapply(ratings_data$num_reviews, function(i) {i/sum(ratings_data$num_reviews)*100})
       
       #get rating data from db
       ratings_data_recall <- dbGetQuery(con, "SELECT overall,count(*) as num_reviews from review
                                  where product_id in (select product_id from recalledproduct)
                                  group by overall;")
       
       #get proportion
       ratings_data_recall$prop_reviews = sapply(ratings_data_recall$num_reviews, function(i) {i/sum(ratings_data_recall$num_reviews)*100})
       
       #merge the recall and non recall data sets
       merged_data <- rbind(ratings_data,ratings_data_recall)
       merged_data$recalled <- c(rep("not recalled", 5),rep("recalled",5))
       
       #plot the data
       ggplot(merged_data, aes(x=overall,y=prop_reviews,fill=as.factor(recalled))) +
         geom_bar(stat="identity",position="dodge") +
         ggtitle("Reviews per Rating") +
         xlab("Rating") + ylab("Proportion of Reviews") +
         theme(plot.title=element_text(face="bold", size=18),
               axis.title=element_text(size=10)) +
         guides(fill=guide_legend(title="Recall Status")) +
         scale_fill_manual(values=c("#607D8B","#689F38"))
       
     }
     
     #timeline
     else if (input$selectVis == "tl") {
       
       review_time_data <- dbGetQuery(con, "SELECT rv.review_time,count(*)
                                        from review rv group by rv.review_time;")
       
       review_time_data_recall <- dbGetQuery(con, "SELECT rv.review_time,count(*)
                                        from review rv 
                                        where rv.product_id in (
                                        select product_id from recalledproduct)
                                            group by rv.review_time;")
       
       ggplot() + geom_line(data=review_time_data,aes(x=review_time,y=count),
                            colour="#BF360C",size=1) +
         geom_line(data=review_time_data_recall,aes(x=review_time,y=count),
                   colour="#1E88E5", size=1)+
         ggtitle("Reviews Timeline") +
         xlab("Date") + ylab("Reviews") +
         theme(plot.title=element_text(face="bold", size=18),
               axis.title=element_text(size=10))
     }
     
     #Word cloud output
     else if (input$selectVis == "wc") {
       
       review_text_data <- dbGetQuery(con, "SELECT rv.review_text,p.product_name
                                        from review rv join product p
                                        on rv.product_id = p.product_id
                                      where rv.product_id in
                                      (select product_id from recalledproduct);")
       
       #subset product-specific text
       review_subset <- subset(review_text_data,
                               review_text_data$product_name == input$wc_data)
       
       #get term frequencies
       review_corpus <- Corpus(VectorSource(review_subset$review_text))
       review_corpus <- tm_map(review_corpus, stemDocument, language="english")
       
       
       review.dtm <- DocumentTermMatrix(review_corpus,
                                        control = list(removePunctuation = TRUE,
                                                       stopwords = TRUE,
                                                       wordLengths=c(0,Inf)))
       frequencies <- colSums(as.matrix(review.dtm))
       terms <- colnames(review.dtm)
       wordcloud(terms,freq=frequencies, max.words=50,random.order = FALSE, colors = 
                            brewer.pal(5,"Dark2"))
       
       
     }
     
     #category summary selection
     else if (input$selectVis == "cs") {
       
       #fetch data from db
       category_data <- dbGetQuery(con, "select c.category_name,
                                   c2.category_name as parent_name from category c
                                   join category c2 on c.parent_id = c2.category_id;")
       
       category_graph <- graph_from_data_frame(category_data,directed=FALSE) 
       unique(category_data$category_name)
       
       #calculate shortest paths between the center and each top level category
       category_distances <- shortest_paths(category_graph,from="Grocery & Gourmet Food",to=V(category_graph))
       names(unlist(category_distances$vpath[1]))[]
       category_distances$path_length <- sapply(category_distances$vpath,function(x) {length(x)})
       category_distances$node <- sapply(category_distances$vpath, 
                                         function(x) {
         nodes <- names(unlist(x))
         nodes[length(nodes)]
       })
       
       #subset graph to only have categories within a distance of 3
       #from the grocery and gourmet foods node
       hclust_category <- cluster_fast_greedy(category_graph)
       igraph::plot_dendrogram(hclust_category)
           
     }
     
     else if (input$selectVis == "rt") {
       
       #fetch classification and review data
       class_data <- dbGetQuery(con, "select rv.review_text, rv.product_id, e.classification
                                from review rv join recalledproduct rp
                                on rv.product_id = rp.product_id
                                join recall rc on rc.recall_id = rp.recall_id
                                join event e on rc.event_id = e.event_id;")
       
       #get summary by product
       class_by_product <- class_data %>% group_by(product_id,classification) %>% summarize(n=n())
       
       #graph summary by product and by number of reviews
       p1 <- ggplot(class_data, aes(x = factor(1), fill = factor(classification))) +
         geom_bar(width = 1) + coord_polar(theta = "y") +
         guides(fill=guide_legend(title="Classification")) +
         scale_fill_manual(values=c("#607D8B","#FFB300","#4CAF50")) +
         ggtitle("Reviews per Classification Type") +
         xlab("") + ylab("") +
         theme(plot.title=element_text(face="bold", size=16),
               legend.title=element_text(size=10),
               panel.border = element_blank(),
               panel.grid=element_blank(),
               axis.ticks = element_blank())
         
         #by product
      p2 <- ggplot(class_by_product, aes(x = factor(1), fill = factor(classification))) +
         geom_bar(width = 1) + coord_polar(theta = "y") +
         guides(fill=guide_legend(title="Classification")) +
         scale_fill_manual(values=c("#607D8B","#FFB300","#4CAF50")) +
         ggtitle("Products per Classification Type") +
         xlab("") + ylab("") +
         theme(plot.title=element_text(face="bold", size=16),
               legend.title=element_text(size=10),
               panel.border = element_blank(),
               panel.grid=element_blank(),
               axis.ticks = element_blank())
       
       grid.arrange(p1, p2, ncol = 1, 
                    top = textGrob("Classification Summary", gp=gpar(fontsize=20,font=2)))
       
     }
     
   })
})

# Run the application 
shinyApp(ui = ui, server = server)

#dbDisconnect(con)

