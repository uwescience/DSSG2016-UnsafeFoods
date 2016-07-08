Exploration of Amazon Review Data
================
Kara Woo
July 8, 2016

Load packages and data
----------------------

First, load the required packages

``` r
library("jsonlite")
library("dplyr")
library("ggplot2")
library("scales")
library("lubridate")
library("viridis")
```

Then, load the Amazon review data and list of recalled UPCs/ASINs.

``` r
## Load Amazon review data
json_file <- "../data/processed/reviews_Grocery_and_Gourmet_Food_strict.json"
amz <- fromJSON(sprintf("[%s]", paste(readLines(json_file), collapse=",")))

## Load list of recalled UPCs/ASINs
recalled <- read.csv("../data/processed/recalls_upcs_asins_joined.csv",
                     stringsAsFactors = FALSE)

## Vector of ASINs from recalled products
recalled_asins <- unique(recalled$asins) %>%
  sapply(strsplit, ";") %>%
  unname() %>%
  unlist()

## Add column to indicate whether product was recalled. Also create a proper
## date column in YYYY-MM-DD, and a year column.
amz_clean <- amz %>%
  mutate(recall = ifelse(asin %in% recalled_asins, "Recalled",
                         "Not recalled"),
         date = as.Date(reviewTime, format = "%m %j, %Y"),
         year = year(date))
```

This is a custom ggplot2 theme for all of the plots:

``` r
mytheme <- theme_set(theme_minimal())
mytheme <- theme_update(
  strip.text = element_text(size = 12),
  axis.text = element_text(size = 12),
  axis.title = element_text(size = 14)
)
```

Review counts of recalled vs. non-recalled products
---------------------------------------------------

There are a total of 1638 reviews for recalled food products and 1295518 reviews for non-recalled food products.

``` r
ggplot(amz_clean, aes(x = recall, fill = recall)) +
  geom_bar() +
  scale_y_continuous(labels = comma) +
  scale_fill_viridis(discrete = TRUE, end = 0.7) +
  labs(y = "",
       x = "",
       title = "Number of Amazon product reviews") +
  theme(legend.position = "none")
```

![](../figs/total-review-n-1.png)

Reviews per year of recalled vs. non-recalled products
------------------------------------------------------

``` r
yearly_tally <- amz_clean %>%
  group_by(year, recall) %>%
  tally()

## Reviews over time for recalled and non-recalled food products
fullplot <- ggplot(yearly_tally, aes(x = year, y = n, color = recall)) +
  geom_line() +
  geom_point() +
  scale_color_viridis(discrete = TRUE, end = 0.7) +
  scale_y_continuous(labels = comma) +
  scale_x_continuous(limits = c(2000, 2015)) +
  labs(x = "Year",
       y = "",
       color = "",
       title = "Reviews per year")

## Recalled products only
recallplot <- ggplot(yearly_tally[yearly_tally$recall == "Recalled", ],
                     aes(x = year, y = n)) +
  geom_line(color = "#49be74") +
  geom_point(color = "#49be74") +
  scale_x_continuous(limits = c(2000, 2015)) +
  labs(x = "Year",
       y = "") +
  theme(axis.title.x = element_blank(),
        axis.text.x = element_text(size = 7, margin = margin(0, -10, 0, 0, "pt")),
        axis.text.y = element_text(size = 7, margin = margin(0, -10, 0, 0, "pt")),
        panel.grid = element_blank(),
        panel.border = element_rect(color = "black", fill = NA))

g = ggplotGrob(recallplot)
fullplot + annotation_custom(grob = g, xmin = 1999, xmax = 2009, ymin = 260000,
                             ymax = 460000)
```

![](../figs/yearly-counts-1.png)

Rating distribution for recalled and non-recalled products
----------------------------------------------------------

``` r
ggplot(amz_clean, aes(x = overall, fill = recall)) +
  geom_bar() +
  facet_grid(recall ~ ., scales = "free_y") +
  scale_fill_viridis(discrete = TRUE, end = 0.7) +
  labs(y = "Count",
       x = "Rating") +
  theme(legend.position = "none")
```

![](../figs/rating-distributions-1.png)
