margin = top: 20, right: 20, bottom: 20, left: 40
width = 960 - margin.left - margin.right
height = 500 - margin.top - margin.bottom

x = d3.scale.linear()
  .range [0, width]

y = d3.scale.linear()
  .range [height, 0]

color = d3.scale.category10()

xAxis = d3.svg.axis()
  .scale x
  .orient "bottom"

yAxis = d3.svg.axis()
  .scale y
  .orient "left"

svg = d3.select "#main"
  .append "svg"
  .attr "width", width + margin.left + margin.right
  .attr "height", height + margin.top + margin.bottom
  .append "g"
  .attr "transform", "translate(" + margin.left + "," + margin.top + ")"

d3.json "clusters.json", (error, json) ->
  if error
    return console.warn error
  data = json

  d.posy = +d.xy[0] for d in data
  d.posx = +d.xy[1] for d in data
  #
  # data.forEach (d) ->
  #   d.posy = +d.xy[0]
  #   d.posx = +d.xy[1]

  x.domain d3.extent( data, (d) ->
    d.posx )
    .nice()
  y.domain d3.extent( data, (d) ->
    d.posy )
    .nice()

  svg.append "g"
    .attr "class", "x axis"
    .attr "transform", "translate(0," + height + ")"
    .call xAxis
    .append "text"
    .attr "class", "label"
    .attr "x", width
    .attr "y", -6
    .style "text-anchor", "end"
    .text "Width"

  svg.append "g"
    .attr "class", "y axis"
    .call yAxis
    .append "text"
    .attr "class", "label"
    .attr "transform", "rotate(-90)"
    .attr "y", 6
    .attr "dy", ".71em"
    .style "text-anchor", "end"
    .text "Length"

  svg.selectAll ".dot"
    .data data
    .enter()
    .append "circle"
    .attr "class", "dot"
    .attr "r", 3.5
    .attr "cx", (d) ->
      x d.posx
    .attr "cy", (d) ->
      y d.posy
    .style "fill", (d) ->
      color d.cluster

  legend = svg.selectAll ".legend"
    .data color.domain()
    .enter()
    .append "g"
    .attr "class", "legend"
    .attr "transform", (d, i) ->
      "translate(0," + i * 20 + ")"

  legend.append "rect"
    .attr "x", width - 18
    .attr "width", 18
    .attr "height", 18
    .style "fill", color

  legend.append "text"
    .attr "x", width - 24
    .attr "y", 9
    .attr "dy", ".35em"
    .style "text-anchor", "end"
    .text (d) ->
      d

# Need to get topics and display them...add in bunch of topics to json file itself, then reference those in the d3 file (this file)
