function renderBarChart(elementId, data, chartTitle) {
    const margin = { top: 20, right: 30, bottom: 40, left: 40 };
    const width = 600 - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;

    // Create SVG element
    const svg = d3.select(elementId)
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    // Set up the X and Y scales
    const x = d3.scaleBand()
        .domain(data.map(d => d.label))
        .range([0, width])
        .padding(0.1);

    const y = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.value)])
        .nice()
    svg.selectAll('.bar')
        .data(data)
        .enter()
        .append('rect')
        .attr('class', 'bar')
        .attr('x', d => x(d.label))
        .attr('y', d => y(d.value))
        .attr('width', x.bandwidth())
        .attr('height', d => height - y(d.value));

    // Add the X axis
    svg.append('g')
        .attr('class', 'x axis')
        .attr('transform', 'translate(0,' + height + ')')
        .call(d3.axisBottom(x).tickSize(0))
        .selectAll('.tick text')
        .style('text-anchor', 'middle');

    // Add the Y axis
    svg.append('g')
        .attr('class', 'y axis')
        .call(d3.axisLeft(y).ticks(5))
        .selectAll('.tick text')
        .attr('class', 'axis-label');

    // Add a title above the chart
    svg.append('text')
        .attr('x', width / 2)
        .attr('y', -10)
        .attr('class', 'chart-title')
        .style('text-anchor', 'middle')
        .text(chartTitle);
}

fetch(`/crime_data/${crimeLocation}`)
    .then(response => response.json())
    .then(data => {
        const categories = data.categories;  // Crime categories data
        const outcomes = data.outcomes;      // Crime outcomes data

        // Call the function to render the category chart
        renderBarChart('#category-bar-chart', categories, 'Crime Categories');

        // Call the function to render the outcome chart
        renderBarChart('#outcome-bar-chart', outcomes, 'Crime Outcomes');
    })
    .catch(error => console.error('Error fetching crime data:', error));