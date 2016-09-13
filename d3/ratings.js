// Load ASINs and product titles into the select dropdown
d3.csv("https://raw.githubusercontent.com/uwescience/DSSG2016-UnsafeFoods/master/github_data/recalled_asins_with_product_titles.csv", function(error, data) {
    var select = d3.select("#dropdown")
            .attr("align", "center")
            .append("select")
            .attr("id", "opts")
            .attr("class", "js-example-basic-single")
            .style("width", "400px");

    // Start dropdown with ASIN "B001DGYKG0" selected
    select.selectAll("option")
        .data(data)
        .enter()
        .append("option")
        .attr("value", function (d) { return d.asin; })
        .text(function (d) { return d.title + " [ASIN: " + d.asin + "]"; })
        .property("selected", function(d){ return d.asin === "B001DGYKG0"; });

    // Initialize Select2
    $(document).ready(function() {
        $(".js-example-basic-single").select2();
    });

});

// Set width/height/margins for vis
var margin = {top: 100, right: 20, bottom: 50, left: 40};
var w = 600 - margin.left - margin.right;
var h = 400 - margin.top - margin.bottom;
var radius = 5;
var padding = 1;

// x and y scales
var x = d3.time.scale()
        .range([0, w]);

var y = d3.scale.linear()
        .range([h, 0]);

var xVar = "date",
    yVar = "rating";

// Load data
d3.csv("https://raw.githubusercontent.com/uwescience/DSSG2016-UnsafeFoods/master/github_data/recalled_amz_reviews.csv", function(error, data) {
    // Read in the data
    if (error) return console.warn(error);
    data.forEach(function(d) {
        d.date = new Date(d.unixReviewTime * 1000);
        d.rating = +d.overall;
        d.recalldate = new Date(d.initiation_date);
    });

    // Axis domains
    x.domain(d3.extent(data, function(d) { return d.date; }));
    y.domain(d3.extent(data, function(d) { return d.rating; })).nice();

    // Create x axis
    var xAxis = d3.svg.axis()
            .ticks(8)
            .scale(x);

    // Create y axis
    var yAxis = d3.svg.axis()
            .ticks(5)
            .scale(y)
            .orient("left");

    // Create SVG
    var svg = d3.select("#vis")
            .append("svg")
            .attr("width", w + margin.left + margin.right)
            .attr("height", h + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // Draw x axis and label
    svg.append("g")
        .classed("x axis", true)
        .attr("transform", "translate(0," + h + ")")
        .call(xAxis)
        .append("text")
        .classed("label", true)
        .attr("x", w)
        .attr("y", 40)
        .style("text-anchor", "end")
        .text("Date");

    // Draw y axis and label
    svg.append("g")
        .classed("y axis", true)
        .call(yAxis)
        .append("text")
        .classed("label", true)
        .attr("transform", "rotate(-90)")
        .attr("y", 3)
        .attr("dy", "-2.3em")
        .style("text-anchor", "end")
        .text("Rating");

    // Tooltips for points
    var tooltip = d3.select("body").append("div")
            .attr("class", "tooltip")
            .style("opacity", 0);

    var pointcolor = "teal";    // Color of points
    var in_dur = 50;            // Transition duration for bringing in tooltips
    var out_dur = 500;          // Duration for removing tooltips

    // Update plot when new ASIN is selected
    function updatePlot(newData) {

        // Subset data for selected ASIN
        var filteredData = data.filter(function(d) { return d.asin == newData; });

        // Create force directed layout
        var force = d3.layout.force()
                .nodes(filteredData)
                .size([w, h])
                .on("tick", tick)
                .charge(-1)
                .gravity(0)
                .chargeDistance(20);

        // Bind data to points
        var node = svg.selectAll(".dot")
                .data(filteredData);

        // Plot points
        node.enter().append("circle")
            .attr("class", "dot")
            .attr("r", radius)
            .attr("cx", function(d) { return x(d.date); })
            .attr("cy", function(d) { return y(d.rating); })
        // Show tooltips and change point color on mouseover
            .on("mouseover", function(d) {
                tooltip.transition()
                    .duration(in_dur)
                    .style("opacity", .9);
                tooltip.html("<b>" + d.summary + "</b><br>"
                             + "<i>" + d.date + "</i><br>"
                             + d.reviewText)
                    .style("left", (d3.event.pageX + 14)
                           + "px")
                    .style("top", (d3.event.pageY - 28)
                           + "px")
                    .style("font-size", "12px");

            })
            .on("mouseout", function(d) {
                tooltip.transition()
                    .duration(out_dur)
                    .style("opacity", 0);

            });

        // Remove old elements
        node.exit().remove();

        // Add line showing recall date

        // Use first row of filteredData to find the recall date -- this works
        // because we only have one recall (and hence one recall date) per
        // product, but if there were multiple it would have to be different
        var rowZero = filteredData[0];

        var recallLine = svg.selectAll(".line")
                .data([rowZero]); // Data needs to be an array!!

        recallLine.enter()
            .append("line")
            .attr("class", "line")
            .attr("y1", y(1))
            .attr("y2", y(5))
            .attr("stroke", "purple")
            .attr("stroke-linecap", "round")
            .attr("stroke-width", "5")
            .on("mouseover", function(d) {
                tooltip.transition()
                    .duration(in_dur)
                    .style("opacity", .9);
                tooltip.html("Recalled: " + d.recalldate)
                    .style("left", (d3.event.pageX + 14)
                           + "px")
                    .style("top", (d3.event.pageY - 28)
                           + "px");

            })
            .on("mouseout", function(d) {
                tooltip.transition()
                    .duration(out_dur)
                    .style("opacity", 0);
            });

        // Move vertical line to recall date
        recallLine.transition()
            .duration(400)
            .attr("x1", function(d) {
                console.dir(d);
                return x(new Date(d.recalldate));
            })
            .attr("x2", function(d) {
                return x(new Date(d.recalldate));
            });

        recallLine.exit().remove();

        var asin = svg.selectAll(".asinlabel")
                .data([rowZero]);

        asin.enter()
            .append("text")
            .attr("class", "asinlabel")
            .attr("x", 1)
            .attr("y", -50);

        asin.transition()
            .text(function(d) { return "Amazon ID: " + d.asin; });

        asin.exit().remove();

        // Begin arranging points
        force.start();

        // Function control final point location -- first tries to move points
        // to their x, y location, then detects collisions and adjusts
        // accordingly
        function tick(e) {
            node.each(moveTowardDataPosition(e.alpha))
                .each(collide(e.alpha));

            node.attr("cx", function(d) { return d.x; })
                .attr("cy", function(d) { return d.y; });
        }

        function moveTowardDataPosition(alpha) {
            return function(d) {
                d.x += (x(d[xVar]) - d.x) * 0.1 * alpha;
                d.y += (y(d[yVar]) - d.y) * 0.1 * alpha;
            };
        }

        function collide(alpha) {
            var quadtree = d3.geom.quadtree(filteredData);
            return function(d) {
                var r = (2 * radius) + padding,
                    nx1 = d.x - r,
                    nx2 = d.x + r,
                    ny1 = d.y - r,
                    ny2 = d.y + r;
                quadtree.visit(function(quad, x1, y1, x2, y2) {
                    if (quad.point && (quad.point !== d)) {
                        var x = d.x - quad.point.x,
                            y = d.y - quad.point.y,
                            l = Math.sqrt(x * x + y * y),
                            r = (2 * radius) + padding;
                        if (l < r) {
                            l = (l - r) / l * alpha;
                            d.x -= x *= l;
                            d.y -= y *= l;
                            quad.point.x += x;
                            quad.point.y += y;
                        }
                    }
                    return x1 > nx2 || x2 < nx1 || y1 > ny2 || y2 < ny1;
                });
            };
        }

    }

    // Initial plot to be shown when page is loaded. Finds the selected value of
    // the dropdown list and calls updatePlot() to generate the plot.
    var sel = document.getElementById("opts");
    var initial = sel.options[sel.selectedIndex].value;
    updatePlot(initial);

    // Update plot when new product is selected
    $("#opts").select2()
        .on("select2:select", function() {
            var newData = $("#opts").val();
            updatePlot(newData);
        });

});

// Products that might be good for demo:
// O.N.E. Coconut Water
// Newman's Own Con Queso Salsa
