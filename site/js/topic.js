var margin = {top: 20, right: 100, bottom: 30, left: 40},
    width = 960 - margin.left - margin.right,
    height = 600 - margin.top - margin.bottom;

var x = d3.scale.ordinal()
    .rangeRoundBands([0, width], 0.1);

var y = d3.scale.linear()
    .rangeRound([height, 0]);

var color = d3.scale.category20c();

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
    .ticks(10, "%");

var svg = d3.select("main").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

d3.csv("topic_data/topic0.csv", type, function(error, data) {
    if (error) throw error;

    var getFilename = function(d) { return d.file.split('/').pop(); };

    data.sort( function( a, b ){
      a = +getFilename(a).split('.').shift();
      b = +getFilename(b).split('.').shift();
      return d3.ascending( a, b );
    });

    // x.domain(data.map(getFilename));
    x.domain(data.map(function(d){return d.file;}))
    y.domain([0, .4]);

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis)
        .selectAll('text')
        .style('text-anchor', 'end')
        .attr('transform', 'rotate(-45)');

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
      .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Probability");

    svg.selectAll(".bar")
       .data(data)
       .enter().append("rect")
       .attr("class", "bar")
       .attr("x", function(d) {console.log(d.file);return d.file;})
       .attr("width", x.rangeBand())
       .attr("y", function(d){console.log(d.frequency);return y(d.frequency);})
       .attr("height", function(d){return height-y(d.frequency);});
});

function type(d) {
  d.frequency = +d.frequency;
  return d;
}
