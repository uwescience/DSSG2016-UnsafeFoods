
// Set width/height/margins
var margin = {top: 50, right: 190, bottom: 50, left: 50};
var w = 1000 - margin.left - margin.right;
var h = 480 - margin.top - margin.bottom;
var radius = 6;
var padding = 1;

// x and y scales 
var x = d3.time.scale()
        .range([0, w]);

var y = d3.scale.linear()
        .range([h, 0]);

var xVar = "date",
    yVar = "rating";

// Load data
d3.csv("recalled_amz.csv", function(error, data) {
    // Read in the data
    if (error) return console.warn(error);
    data.forEach(function(d) {
        d.date = new Date(d.unixReviewTime * 1000);
        d.rating = +d.overall;
    });

    // Axis domains
    x.domain(d3.extent(data, function(d) { return d.date; }));
    y.domain(d3.extent(data, function(d) { return d.rating; })).nice();

    // Draw x axis
    var xAxis = d3.svg.axis()
            .ticks(8)
            .scale(x);

    // Draw y axis
    var yAxis = d3.svg.axis()
            .ticks(5)
            .scale(y)
            .orient("left");
    
    // Create SVG
    var svg = d3.select("#scatter")
            .append("svg")
            .attr("width", w + margin.left + margin.right)
            .attr("height", h + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    
    // Add x axis label
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

    // Add y axis label
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

    var pointcolor = "teal";
    var in_dur = 50;            // Transition duration for bringing in tooltips
    var out_dur = 500;          // Duration for removing tooltips

    // Update plot when new ASIN is selected
    function updatePlot(newData) {

        // Subset data for selected ASIN
        var filteredData = data.filter(function(d) { return d.asin == newData; });

        // Force directed layout
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
        
        node.enter().append("circle")
            .attr("class", "dot")
            .attr("r", radius)
            .style("fill", pointcolor)
            .attr("cx", function(d) { return x(d.date); })
            .attr("cy", function(d) { return y(d.rating); })
            .on("mouseover", function(d) { tooltip.transition()
                                           .duration(in_dur)
                                           .style("opacity", .9);
                                           tooltip.html("<b>" + d.summary + "</b><br>"
                                                        + "<i>" + d.date + "</i><br>"
                                                        + d.reviewText)
                                           .style("left", (d3.event.pageX + 14)
                                                  + "px")
                                           .style("top", (d3.event.pageY - 28)
                                                  + "px");
                                           
                                           d3.select(this)
                                           .style("fill", "goldenrod");
                                         })
            .on("mouseout", function(d) { tooltip.transition()
                                          .duration(out_dur)
                                          .style("opacity", 0);
                                          
                                          d3.select(this)
                                          .transition()
                                          .duration(out_dur)
                                          .style("fill", pointcolor);

                                        });

        // Remove old elements
        node.exit().remove();

        // Begin arranging points
        force.start();

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

    // Starting plot
    var sel = document.getElementById("opts");
    var initial = sel.options[sel.selectedIndex].value; // Find selected value
    updatePlot(initial);

    // Change plot when a different opt is selected
    d3.select('#opts')
        .on('change', function() {
            var newData = d3.select(this).property("value");
            updatePlot(newData);
        });    
    
});
