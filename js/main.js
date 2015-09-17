var margin = {top: 20, right: 40, bottom: 20, left: 40},
    width = 1780 - margin.left - margin.right,
    height = 1200 - margin.top - margin.bottom;

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
    .tickFormat(d3.format(".0%"));

var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

d3.csv("barth.csv", function(error, data) {
  if (error) throw error;

  color.domain(d3.keys(data[0]).filter(function(key) { return key.startsWith('topic-'); }));

  data.forEach(function(d) {
    var y0 = 0;
    d.percentages = color.domain().map(function(name) { return {name: name, y0: y0, y1: y0 += +d[name]}; });
  });

  var getFilename = function(d) { return d.file.split('/').pop(); };
  data.sort( function( a, b ){
    a = +getFilename(a).split('.').shift();
    b = +getFilename(b).split('.').shift();
    return d3.ascending( a, b );
  });
  x.domain(data.map(getFilename));

  // svg.append("g")
  //       .attr("class", "x axis")
  //       .attr("transform", "translate(0," + height + ")")
  //       .call(xAxis)
  //       .selectAll('text')
  //       .style('text-anchor', 'end')
  //       .attr('transform', 'rotate(-45)');

    // svg.append("g")
    //     .attr("class", "y axis")
    //     .call(yAxis);

    var topic = svg.selectAll(".topic")
            .data(data)
          .enter().append("g")
            .attr("class", "topic")
            .attr("transform", function(d) {
                return "translate(" + x(getFilename(d)) + ",0)";
            });

    topic.selectAll("rect")
        .data(function(d) { return d.percentages; })
      .enter().append("rect")
        .attr("width", x.rangeBand())
        .attr("y", function(d) { return y(d.y1); })
        .attr("height", function(d) { return y(d.y0) - y(d.y1); })
        .style("fill", function(d) { return color(d.name); });

    // var legend = svg.select(".topic:last-child").selectAll(".legend")
    //      .data(function(d) { return d.percentages; })
    //    .enter().append("g")
    //      .attr("class", "legend")
    //      .attr("transform", function(d) { return "translate(" + x.rangeBand() / 2 + "," + y((d.y0 + d.y1) / 2) + ")"; });

    //  legend.append("line")
    //      .attr("x2", 10);


    //  legend.append("text")
    //      .attr("x", 13)
    //      .attr("dy", ".35em")
    //      .text(function(d) { return d.name; });

  });
