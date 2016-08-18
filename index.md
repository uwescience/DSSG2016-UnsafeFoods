---
layout: default
---

<a href="http://escience.washington.edu/dssg/">
<img src="{{ site.url }}{{ site.baseurl }}/assets/images/dssg.png">
</a>

# Mining Online Data for Early Identification of Unsafe Food Products

The goal of this project is to use product reviews from Amazon.com to identify
potentially unsafe food products. Foods that are mislabeled, contaminated, or
spoiled get recalled through a time-consuming process that can leave consumers
at risk of allergic reactions, injury, and illness for months. Our goal is to
use reviews that consumers post online to predict whether a product will be
recalled. Specifically, we:

1. Mine and integrate a large corpus of data posted online to understand trends
   and features in unsafe food product reports
   
2. Develop a preliminary classification model for early identification of unsafe
   foods
   
This is one of
[four projects](http://escience.washington.edu/dssg/project-summaries-2016/)
from the 2016 Data Science for Social Good summer fellowship at the University
of Washington [eScience Institute](http://escience.washington.edu/).

## Explore the Reviews

We created an exploratory tool for viewing reviews of recalled products. The
plot below shows reviews and ratings for a recalled product over time, as well
as the date the product was recalled (if no date appears, the recall happened
outside the date range of our Amazon review data). Hover over the points to view
the text of the review. In this case, a reviewer noted a labeling issue in 2011,
long before the product was recalled for mislabeling. The reviews in this tool
provide some support for the idea that product reviews can be a fruitful data
source for identifying unsafe foods.


<!-- Load D3 -->
<script src="https://d3js.org/d3.v3.min.js"></script>
<script src="https://d3js.org/d3-time.v1.min.js"></script>
<script src="https://d3js.org/d3-time-format.v2.min.js"></script>

<!-- Load JQuery -->
<script
src="https://code.jquery.com/jquery-3.1.0.min.js"
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

