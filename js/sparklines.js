var margin = {top: 20, right: 100, bottom: 30, left: 40},
    width = 225 - margin.left - margin.right,
    sparkHeight = 17,
    buffer = 2;

var sparkline = function(g, sparkHeight, width, row) {
    var x = d3.scale.ordinal().rangeRoundBands([0, width], 0.1),
        y = d3.scale.linear().rangeRound([sparkHeight - buffer, 0]);

    var topics = d3.entries(row).filter(function(a){
        return a.key.startsWith('topic-');
    });
    var bars = g.selectAll(".bar")
            .data(topics);


    x.domain(d3.keys(row).filter(
        function(key) { return key.startsWith('topic-'); }
    ));
    y.domain([0, d3.max(topics, function(topic) { return topic.value; })]);

    bars.enter().append("rect")
        .attr("class", "bar")
        .attr("x", function(d) { return x(d.key); })
        .attr("width", x.rangeBand());

    bars.transition()
        .attr("y", function(d) { return y(d.value); })
        .attr("height", function(d) {
            return sparkHeight - buffer - y(d.value);
        });

    bars.exit().remove();
};

var getFilename = function(d) {
    return d.file.split('/').pop();
};

d3.csv("barth.csv", function(error, data) {
    var height = (data.length * sparkHeight) + margin.top + margin.bottom;

    var color = d3.scale.category20c();

    var svg = d3.select("main").append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    data.sort( function( a, b ){
        a = getFilename(a);
        b = getFilename(b);
        return d3.ascending( a, b );
    });

    for (var i=0; i<data.length; i++) {
        svg.append('g')
            .attr('class', 'sparkline')
            .attr('transform', 'translate(0,' + (sparkHeight * i) + ')')
            .call(sparkline, sparkHeight, width, data[i]);
    }

});
