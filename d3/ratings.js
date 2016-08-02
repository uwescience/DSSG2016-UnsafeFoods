
// Set width/height/margins
var margin = {top: 20, right: 190, bottom: 30, left: 50};
var w = 1000 - margin.left - margin.right;
var h = 480 - margin.top - margin.bottom;

// x and y scales 
var x = d3.time.scale()
        .range([0, w]);

var y = d3.scale.linear()
        .range([h, 0]);

var xVar = "date",
    yVar = "rating";

// Load data
d3.csv("single_recalled_amz.csv", function(error, data) {
    // Read in the data
    if (error) return console.warn(error);
    data.forEach(function(d) {
        d.date = new Date(d.unixReviewTime * 1000);
        d.rating = +d.overall;
    });

    console.log(data);
    
    // Calculate maxima and minima and use these to set x/y domain
    var xMax = d3.max(data, function(d) { return d[xVar]; }),
        xMin = d3.min(data, function(d) { return d[xVar]; }),
        yMax = d3.max(data, function(d) { return d[yVar]; }),
        yMin = d3.min(data, function(d) { return d[yVar]; });

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
        .attr("y", -6)
        .style("text-anchor", "end")
        .text("Date");

    // Add y axis label
    svg.append("g")
        .classed("y axis", true)
        .call(yAxis)
        .append("text")
        .classed("label", true)
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Rating");

    // Plot points
    svg.selectAll(".dot")
        .data(data)
        .enter().append("circle")
        .attr("class", "dot")
        .attr("r", 6)
        .attr("cx", function(d) { return x(d.date); })
        .attr("cy", function(d) { return y(d.rating); });

    
});
