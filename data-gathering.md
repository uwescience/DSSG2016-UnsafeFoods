---
layout: page
title: Data gathering
---

For this project, we used
[Amazon reviews](http://jmcauley.ucsd.edu/data/amazon/links.html) of Grocery and
Gourmet Food products and
[enforcement reports](http://www.fda.gov/Safety/Recalls/EnforcementReports/default.htm)
from the Food and Drug Administration. These enforcement reports are made
available as weekly CSV files going back to 2012. It is possible to search the
FDA's website for all data on food products, but unfortunately the download is
limited to 1,000 rows at a time. We also attempted to access the data in a
public S3 bucket, but found a large portion of the data was missing, so we
ultimately chose to manually download the weekly CSV files and combine them
ourselves.

As our goal was to predict food recalls based on product reviews, our next step
after acquiring the data was to unite these two datasets.

The most reliable way to match recalled products with Amazon reviews was by
using the item's Universal Product Code (UPC), which is the number that appears
on a barcode and uniquely identifies that particular product. The FDA
enforcement reports often (but not always) contained the UPC or UPCs of the
product(s) being recalled within a larger text field. We used regular
expressions to extract these codes and, in some cases where partial UPCs were
provided, generated lists of the possible complete UPCs from the partial codes.

Amazon uses its own identifier, the Amazon Standard Identification Number
(ASIN), to identify products. Fortunately, conversion tools such as
[UPCtoASIN.com](http://upctoasin.com) exist to convert UPCs to ASINs. Once we
matched the UPCs of recalled products with their corresponding ASINs, we were
able to start exploring the differences in reviews for recalled and non-recalled
products.

[![Number of reviews for recalled vs. non-recalled products](https://github.com/uwescience/DSSG2016-UnsafeFoods/raw/master/figs/total-review-n-1.png)](https://github.com/uwescience/DSSG2016-UnsafeFoods/blob/master/notebooks/review_summary_vis.md#review-counts-of-recalled-vs-non-recalled-products)

Not surprisingly, there are vastly more reviews for products that have not been
recalled than there are for products that have been recalled, since most food
products never get recalled. Over 1,000,000 reviews were for non-recalled
products, and just over 5,000 were for recalled products. Reviews for recalled
products made up less than one half of one percent of the total dataset.

The number of reviews for both recalled and non-recalled products has increased
over time, likely tracking Amazon's popularity as a website and/or the number of
food products they carry.

[![Number of reviews over time](https://github.com/uwescience/DSSG2016-UnsafeFoods/raw/master/figs/monthly-counts-1.png)](https://github.com/uwescience/DSSG2016-UnsafeFoods/blob/master/notebooks/review_summary_vis.md#reviews-per-month-of-recalled-vs-non-recalled-products)

The Amazon review data also includes the rating (1-5 stars) that the reviewer
gave the product. For both recalled and non-recalled products, five-star reviews
are by far the most common.

[![Rating distribution for recalled and non-recalled products](https://github.com/uwescience/DSSG2016-UnsafeFoods/raw/master/figs/rating-distributions-1.png)](https://github.com/uwescience/DSSG2016-UnsafeFoods/blob/master/notebooks/review_summary_vis.md#rating-distribution-for-recalled-and-non-recalled-products)

## Explore the Reviews

We created an exploratory tool for viewing reviews of recalled products. The
plot below shows reviews and ratings for a recalled product over time, as well
as the date the product was recalled. Hover over the points to view the text of
the review. You can view different products using the dropdown menu below the
plot.

<!-- Load D3 -->
<script src="http://d3js.org/d3.v3.min.js"></script>
<script src="https://d3js.org/d3-time.v1.min.js"></script>
<script src="https://d3js.org/d3-time-format.v2.min.js"></script>

<!-- Load JQuery -->
<script
src="http://code.jquery.com/jquery-3.1.0.min.js"
integrity="sha256-cCueBR6CsyA4/9szpPfrX3s49M9vUU5BgtiJj06wt/s="
crossorigin="anonymous">
</script>

<!-- Use Select2 for dropdown menu -->
<link
href="https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.3/css/select2.min.css"
rel="stylesheet" />
<script
src="https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.3/js/select2.min.js">
</script>

<!-- CSS for plot -->
<link href="https://rawgit.com/uwescience/DSSG2016-UnsafeFoods/master/d3/style.css" type="text/css" rel="stylesheet" />

<div id="vis"></div>

<!-- Dropdown -->
<p class="dropdown-label">Select product:</p>
<div id="dropdown"></div>

<!-- Visualization code -->
<script src="https://rawgit.com/uwescience/DSSG2016-UnsafeFoods/master/d3/ratings.js"></script>

<div id="review-vis"></div>
