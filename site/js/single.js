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

// d3.tsv("barth.keys", function(error, data){
//   // console.log(data[0].words);
//   var topics = ['topic-00', 'topic-01', 'topic-02', 'topic-03', 'topic-04', 'topic-05', 'topic-06', 'topic-07', 'topic-08', 'topic-09', 'topic-10', 'topic-11', 'topic-12', 'topic-13', 'topic-14', 'topic-15', 'topic-16', 'topic-17', 'topic-18', 'topic-19'];
//   for (var i = 0; i < data.length; i++) {
//     for (var j = 0; j < topics.length; j++){
//       var topic[j] = data[i]
//     }
//   }
//   console.log(topics);
// });

d3.csv("barth_composition_full.csv", function(error, data) {

    var getFilename = function(d) { return d.file.split('/').pop(); };
    data.sort( function( a, b ){
      a = +getFilename(a).split('.').shift();
      b = +getFilename(b).split('.').shift();
      return d3.ascending( a, b );
    });

    // var tooltip = d3.select("main")
    //   .append("div")
    //   .style("position", "absolute")
    //   .style("z-index", "10")
    //   .style("visibility", "hidden")
    //   .text("a simple tooltip");

    x.domain(d3.keys(data[0]).filter(function(key) { return key.startsWith('topic-'); }));
    y.domain([0, 1]);

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
      .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Probability");

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
            var paraData = data[parIndex];
            // console.log(paraData);

            var topics = d3.entries( paraData ).filter(function( a ){
                return a.key.startsWith('topic-');
            });

            // console.log(topics);
            var bars = svg.selectAll(".bar")
                  .data(topics);

            bars.enter().append("rect")
              .attr("class", "bar")
              .attr("x", function(d) { return x(d.key); })
              .attr("width", x.rangeBand());
              // .on("mouseover", function(){return tooltip.style("visibility", "visible");})
            	// .on("mousemove", function(){return tooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px");})
            	// .on("mouseout", function(){return tooltip.style("visibility", "hidden");});

            bars.transition()
                  .attr("y", function(d) { return y(d.value); })
                  .attr("height", function(d) { return height - y(d.value); });

            bars.exit().remove();

        });

        // Create tooltips with labels for each topic
        // Will need to pull in models/full/barth.keys to get data


});
