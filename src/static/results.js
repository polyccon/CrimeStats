function drawPieChart(divid, data){
  var w = 400,
      h = 400,
      r = 200,

  color = d3.scale.category20c();
  data = data.sort(function (a, b) {
      return d3.ascending(a.value, b.value);
  })
  var vis = d3.select("#"+divid)
              .append("svg:svg")
              .data([data])
                .attr("width", w)
                .attr("height", h)
              .append("svg:g")
                .attr("transform", "translate(" + r + "," + r + ")")
  var arc = d3.svg.arc()
              .outerRadius(r);
  var pie = d3.layout.pie()
              .value(function(d) { return d.value; });
  var tip = d3.tip()
              .attr('class', 'd3-tip')
              .html(function(data) {
                 return "<strong class='text-font'>"+data.data.label+":</strong> <span class='text-font text-color'>"+ data.value + "</span>";
              })
  vis.call(tip);
  var arcs = vis.selectAll("g.slice")
               .data(pie)
               .enter()
               .append("svg:g")
                 .attr("class", "slice");
  arcs.append("svg:path")
          .attr("fill", function(d, i) { return color(i); } )
          .attr("d", arc)
          .on('mouseover', tip.show)
          .on('mouseout', tip.hide);
}
function drawBarChart(divid, data){
  color = d3.scale.category20c();
  data = data.sort(function (a, b) {
      return d3.ascending(a.value, b.value);
  })

  var margin = {
    top: 15,
    right: 70,
    bottom: 15,
    left: 200
  };

  var width = 960 - margin.left - margin.right,
      height = 500 - margin.top - margin.bottom;

  var svg = d3.select("#"+divid).append("svg")
                    .attr("width", width + margin.left + margin.right)
                    .attr("height", height + margin.top + margin.bottom)
               .append("g")
                    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  var x = d3.scale.linear()
            .range([0, width])
            .domain([0, d3.max(data, function (d) {
                return d.value;
            })]);

  var y = d3.scale.ordinal()
            .rangeRoundBands([height, 0], .1)
            .domain(data.map(function (d) {
                return d.label;
            }));

  var yAxis = d3.svg.axis()
            .scale(y)
            .tickSize(0)
            .orient("left");

  var gy = svg.append("g")
            .attr("class", "y axis")
            .call(yAxis)

  var bars = svg.selectAll(".bar")
            .data(data)
            .enter()
            .append("g")

  bars.append("rect")
      .attr("class", "bar")
      .attr("fill", function(d, i) { return color(i); } )
      .attr("y", function (d) {
          return y(d.label);
    })
      .attr("height", y.rangeBand())
      .attr("x", 0)
      .attr("width", function (d) {
          return x(d.value);
    });

  bars.append("text")
      .attr("class", "label")
      .attr("y", function (d) {
          return y(d.label) + y.rangeBand() / 2 + 4;
    })
      .attr("font-family", "sans-serif")
      .attr("font-size", "20px")
      .attr("fill", "red")
      .attr("x", function (d) {
          return x(d.value) + 3;
    })
    .text(function (d) {
        return d.value;
    });
}
