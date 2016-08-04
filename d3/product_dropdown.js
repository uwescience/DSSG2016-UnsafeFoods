// Load ASINs and product titles into the select dropdown
d3.csv("asins_titles.csv", function(error, data) {
    var select = d3.select("body")
            .append("div")
            .append("select")
            .attr("id", "opts")
            .attr("class", "js-example-basic-single");
    
    select.selectAll("option")
        .data(data)
        .enter()
        .append("option")
        .attr("value", function (d) { return d.asin; })
        .text(function (d) { return d.title; })
        .property("selected", function(d){ return d.asin === "B001DGYKG0"; });

});
