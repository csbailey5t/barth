var margin = {top: 20, right: 100, bottom: 300, left: 40},
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

var svg = d3.select("#main").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

d3.csv("mallet_results/barth_composition.txt", function(error, data) {

    var getFilename = function(d) { return d.file.split('/').pop(); };
    data.sort( function( a, b ){
      a = +getFilename(a).split('.').shift();
      b = +getFilename(b).split('.').shift();
      return d3.ascending( a, b );
    });

    color.domain(d3.keys(data[0]).filter(function(key) { return key.startsWith('topic-'); }));

    d3.select('#paragraph_select')
        .selectAll('option')
        .data(data)
        .enter()
        .append("option")
        .attr("value", function (d, i) { return i; })
        .text( function(d){ return getFilename(d); });

    d3.select('#paragraph_select')
        .on('change', function () {

            var parIndex = d3.event.target.selectedIndex;

            console.log(data[parIndex]);
        });



});
