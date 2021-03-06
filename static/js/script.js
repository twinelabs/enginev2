'use strict';

angular
  .module('dashApp', ['ui.grid'])
  .controller('dashCtrl', dashCtrl);

dashCtrl.$inject = [ '$scope', '$timeout' ];

function dashCtrl($scope, $timeout){
  var _ = this;

  // TABLES
  _.tables = [
    {
      id: 0,
      name: 'Demo',
      url: 'data/data.json',
      type: 'json',
      data: []
    },
    {
      id: 1,
      name: 'Demo2',
      url: 'data/demo_data.csv',
      type: 'csv',
      data: []
    }
  ];
  _.selectedTable = _.tables[0];

  // VIEWS
  _.views = [
    {
      id: 0,
      name: 'Summary'
    },
    {
      id: 1,
      name: 'Charts'
    },
    {
      id: 2,
      name: 'Statistics'
    }
  ];
  _.selectedView = _.views[1];

  // DATA
  _.data = [];
  _.dataFields = [];
  _.dataFieldsByType = {
    string: {
      fields: [],
      open: true,
      name: 'String Fields'
    },
    numeric: {
      fields: [],
      open: false,
      name: 'Numeric Fields'
    },
    date: {
      fields: [],
      open: false,
      name: 'Date Fields'
    }
  };
  _.selectedDataField;

  // CHARTS
  _.charts = {};
  _.chartData = null;

  // CHART CONTROLS
  _.chartControlSort = [
    {
      id: 0,
      name: 'desc'
    },
    {
      id: 1,
      name: 'asc'
    },
    {
      id: 2,
      name: 'abc'
    }
  ];
  _.selectedChartControlSort = _.chartControlSort[0];

  _.chartControlScale = [
    {
      id: 0,
      name: 'norm'
    },
    {
      id: 1,
      name: '100%'
    }
  ];
  _.selectedChartControlScale = _.chartControlScale[0];


  // TABLE
  _.gridOptions = {
    enableColumnMenus: false,
    columnDefs: [{ field: 'x', displayName: 'X' }, { field: 'y', displayName: 'Y' }],
  }
  _.showGrid = false;

  ////////////////////////////////////////////////////////////////////////////////////////

  // INIT LOAD FUUL FORMAT DATA
  d3.json('data/test_data_format.json', function(error, data){
    data.forEach(function(table){
      _.tables.push(table);
    });
  });


  ///////////////////////////////////////////////////////////////////////////////////////

  // UTILS
  _.loadData = loadData;

  _.click = click;

  _.getFieldTypes = getFieldTypes;

  // WATCH
  $scope.$watch('_.selectedTable', onSelectedTable);

  $scope.$watch('_.selectedView', onSelectedView);

  $scope.$watch('_.selectedDataField', onSelectedDataField);

  $scope.$watch('_.selectedChartControlSort', onSelectedChartControlSort);

  $scope.$watch('_.selectedChartControlScale', onSelectedChartControlScale);

  // WINDOW
  window.addEventListener('resize', function(e){
    for (var item in _.charts) if (_.charts[item]) _.charts[item].render();
  });

  // UTILS DEFINITION

  function click(type, $event){
    var node = $event.target.parentNode;
    node.style.display = 'none';
    $timeout(function(){
      node.style.display = null;
    }, 300);

    var ce, ct;

    if (_.charts.barChart && _.charts.barChart.export) {
      ct = _.charts.barChart.type;
      ce = _.charts.barChart.export;
    } else {
      return;
    }

    if (type == 'png') {
      ce.toPNG({}, function( data ) {
        ce.download( data, "image/png", "chart.png" );
      });
    }
    else if (type == 'pdf') {
      ce.toPDF({}, function( data ) {
        ce.download( data, "application/pdf", "chart.pdf" );
      });
    }
    else if (type == 'csv') {
      ce.toCSV({ updateData: updateData(ct) }, function( data ) {
        ce.download( data, "text/plain", "chart.csv" );
      });
    }
    else if (type == 'json') {
      ce.toJSON({ updateData: updateData(ct) }, function( data ) {
        ce.download( data, "text/plain", "chart.json" );
      });
    }

  }

  function updateData(type){
    return function(_data){
      var data = [];
      _data.forEach(function(d){
        var item = {};

        if (type == 'bar') {
          item[_.selectedDataField] = d.x;
          item['Count, %'] = d.y;
          item['count'] = d.count;
        }
        else if (type == 'horizontalBar') {
          item[_.selectedDataField] = d.y;
          item['Count, %'] = d.x;
          item['count'] = d.count;
        }

        data.push(item);
      });

      return data;
    }
  }

  function getFieldTypes(){
    return Object.keys(_.dataFieldsByType);
  }

  function loadData(cb){

    // Check if table has already data, or load data from somewhere
    if (!_.selectedTable.url) {

      _.data = _.selectedTable.data;

      if (_.data.length) {
        _.dataFieldsByType.string.fields = [];
        _.dataFieldsByType.numeric.fields = [];
        _.dataFieldsByType.date.fields = [];
        _.dataFields = [];

        _.dataFields = _.selectedTable.columns.map(function(c){ return c.name; });

        _.selectedTable.columns.forEach(function(c){
          _.dataFields.push(c.name);

          if (c.type === 'string') {
            _.dataFieldsByType.string.fields.push(c.name);
          }
          if (c.type === 'number') {
            _.dataFieldsByType.numeric.fields.push(c.name);
          }
          if (c.type === 'date') {
            _.dataFieldsByType.date.fields.push(c.name);
          }
        })
      }

      _.selectedDataField = null;

    } else {

      d3[_.selectedTable.type](_.selectedTable.url, function(error, data){
        if (error) throw error;

        _.data = data;

        if (data.length) {
          _.dataFieldsByType.string.fields = [];
          _.dataFieldsByType.numeric.fields = [];
          _.dataFieldsByType.date.fields = [];

          _.dataFields = Object.keys(data[0]);
          _.dataFields.shift();

          _.dataFields.forEach(function(f){
            if (!isNaN(+data[0][f]))
              _.dataFieldsByType.numeric.fields.push(f);
            else
              _.dataFieldsByType.string.fields.push(f);
          })
        }

        _.selectedDataField = null;

        if (typeof cb === 'function') cb();
      });

    }
  }


  // WATCHERS

  function onSelectedTable(){
    _.loadData(function(){
      onSelectedView(_.selectedView);
      $scope.$digest();
    });
  }

  function onSelectedView(v){
    // hide grid
    _.showGrid = false;

    // clear chart
    if (_.charts.barChart && _.charts.barChart.clear) {
      _.charts.barChart.clear();
      _.charts.barChart = null;
    }

    if (v.id == 1 && _.selectedDataField) {
      $timeout(function(){
        onSelectedDataField(_.selectedDataField);
      }, 20);
    }
  }

  function onSelectedDataField(f){
    if (!f) return;

    var chartOptions = {
      order: _.selectedChartControlSort.id,
      scale: _.selectedChartControlScale.id
    };

    // try to find type from data or calculate automatically
    if (_.selectedTable.columns) {

      var col = _.selectedTable.columns.filter(function(d){ return d.name === f })[0];

      if (col.type === 'number') {
        _.chartData = getHistogram(f, 8);
        _.charts.barChart = barChart(_.chartData, '#chart', chartOptions).fadeRender();
        _.gridOptions.data = _.chartData;
        _.gridOptions.columnDefs = [
          { field: 'x', displayName: f },
          { field: 'y', displayName: 'Count, %' },
          { field: 'count', displayName: 'Count' }
        ];
      }
      else if (col.type === 'string') {
        _.chartData = getFrequency(f);
        _.charts.barChart = horizontalBarChart(_.chartData, '#chart', chartOptions).fadeRender();
        _.gridOptions.data = _.chartData;
        _.gridOptions.columnDefs = [
          { field: 'y', displayName: f },
          { field: 'x', displayName: 'Count, %' },
          { field: 'count', displayName: 'Count' }
        ]
      }
      else if (col.type === 'date') {
        _.chartData = getDateHistogram(f, col.date_format, 8);
        _.charts.barChart = barChart(_.chartData, '#chart', chartOptions).fadeRender();
        _.gridOptions.data = _.chartData;
        _.gridOptions.columnDefs = [
          { field: 'x', displayName: f },
          { field: 'y', displayName: 'Count, %' },
          { field: 'count', displayName: 'Count' }
        ];
      }

    } else {

      var value = _.data[0][f];

      if (!isNaN(value)) {
        _.chartData = getHistogram(f, 8);
        _.charts.barChart = barChart(_.chartData, '#chart', chartOptions).fadeRender();
        _.gridOptions.data = _.chartData;
        _.gridOptions.columnDefs = [
          { field: 'x', displayName: f },
          { field: 'y', displayName: 'Count, %' },
          { field: 'count', displayName: 'Count' }
        ];
      } else {
        _.chartData = getFrequency(f);
        _.charts.barChart = horizontalBarChart(_.chartData, '#chart', chartOptions).fadeRender();
        _.gridOptions.data = _.chartData;
        _.gridOptions.columnDefs = [
          { field: 'y', displayName: f },
          { field: 'x', displayName: 'Count, %' },
          { field: 'count', displayName: 'Count' }
        ]
      }

    }

    // ADD EXPORT FOR CHART
    if (ChartExport) _.charts.barChart.export = new ChartExport.export(_.charts.barChart, {});

    // show grid
    _.showGrid = true;
  }

  function onSelectedChartControlSort(s){
    if (!s) return;

    if (_.charts.barChart) {
      _.charts.barChart.order(s.id).redraw();
    }
  }

  function onSelectedChartControlScale(s){
    if (!s) return;

    if (_.charts.barChart) {
      _.charts.barChart.scale(s.id).redraw();
    }
  }

  // CALCULATE DATA
  function getHistogram(f, N){
    var res;
    var L = _.data.length;
    var range = d3.extent(_.data, function(d){ return +d[f]; });

    N = calculateN(f, N, range, function(d){ return +d; });

    var data = [];
    for (var i = 0; i < N; i++) data.push([]);

    if (range[0] == range[1]) {

      _.data.forEach(function(d){
        data[0].push(+d[f]);
      });

      res = [{
        x: prettyNum(range[0]) + ' to ' + prettyNum(range[0]),
        y: 100,
        count: data[0].length
      }];

    } else {

      var step = (range[1] - range[0])/N;
      _.data.forEach(function(d){
        var v = +d[f];
        var idx = Math.trunc((v - range[0]) / step);
        if (idx == N) idx = N - 1;
        data[idx].push(v);
      });

      res = data.map(function(d, i){
        return {
          x: prettyNum(range[0] + i * step) + ' to ' + prettyNum(range[0] + (i + 1) * step),
          y: 100 * d.length / L,
          count: d.length
        };
      });

    }

    return res;
  }

  function getFrequency(f){
    var data = {};

    _.data.forEach(function(d){
      var v = d[f];
      if (!data[v]) data[v] = 0;
      data[v]++;
    });

    var L = _.data.length;

    return Object.keys(data).map(function(v){
      return {
        x: 100 * data[v] / L,
        y: v,
        count: data[v]
      }
    });
  }

  function getDateHistogram(f, format, N){
    var res;
    var fmt = d3.time.format(format);

    var L = _.data.length;
    var range = d3.extent(_.data, function(d){ return fmt.parse(d[f]); });

    N = calculateN(f, N, range, fmt.parse);

    var data = [];
    for (var i = 0; i < N; i++) data.push([]);

    if (range[0] == range[1]) {

      _.data.forEach(function(d){
        data[0].push(fmt.parse(d[f]));
      });

      res = [{
        x: fmt(range[0]) + ' to ' + fmt(range[0]),
        y: 100,
        count: data[0].length
      }];

    } else {

      var step = (range[1] - range[0])/N;

      _.data.forEach(function(d){
        var v = fmt.parse(d[f]);
        var idx = Math.trunc((v - range[0]) / step);
        if (idx == N) idx = N - 1;
        data[idx].push(v);
      });

      res = data.map(function(d, i){
        return {
          x: fmt(new Date(Math.round(+range[0] + i * step))) + ' to ' + fmt(new Date(Math.round(+range[0] + (i + 1) * step))),
          y: 100 * d.length / L,
          count: d.length
        };
      });

    }

    return res;
  }

  function calculateN(f, N, range, format){
    if (N == 1) return N;

    var L = _.data.length;
    var bulkCounts = 0;
    var data = {};

    var step = (range[1] - range[0])/N;
    var i = 0;
    while (i < L && bulkCounts < N) {
      var d = _.data[i];
      var v = format(d[f]);
      var idx = Math.trunc((v - range[0]) / step);
      if (idx == N) idx = N - 1;
      if (!data[idx]){
        data[idx] = true;
        bulkCounts++;
      };
      i++;
    }

    return bulkCounts == N ? N : calculateN(f, N - 1, range, format);
  }

  function prettyNum(n){
    return parseFloat(n.toFixed(2));
  }
}/**
 * Bar Chart Definition
 */
;function barChart(_data, selector, options){
  options = options || {};
  var data = _data.slice();

  var chart
    , fullWidth
    , fullHeight
    , margin
    , width
    , height
    , x
    , y
    , xAccessor = options.xAccessor || function(d) { return d.x }
    , yAccessor = options.yAccessor || function(d) { return d.y }
    , xAxis
    , yAxis
    , svg
    , bars
    , barLabels
    , xAxisG
    , yAxisG
    , tooltip
    , duration = 500
    , order = options.order || 0
    , scale = options.scale || 0
    ;

  // render the chart completely
  function render(){

    // clear
    clear();

    // set width
    fullWidth = options.fullWidth || $(selector).width() || 300;
    fullHeight = options.fullHeight || $(selector).height() - 30 || 300;

    margin = {top: 20, right: 10, bottom: 30, left: 30};
    width = fullWidth - margin.left - margin.right;
    height = fullHeight - margin.top - margin.bottom;

    x = d3.scale.ordinal()
      .rangeRoundBands([0, width], 0.1);

    y = d3.scale.linear()
      .range([height, 0])
      .nice();

    xAxis = d3.svg.axis()
      .scale(x)
      .orient('bottom')
      .tickSize(4)

    yAxis = d3.svg.axis()
      .scale(y)
      .orient('left')
      .tickSize(4);

    // Create svg
    svg = d3.select(selector).append('svg')
      .attr('width', fullWidth)
      .attr('height', fullHeight)
      .style({
        'position': 'relative'
      })
      .append('g')
      .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    if (!data || !data.length) {
      svg.append('text')
        .attr('transform', 'translate(' + width/2 + ',' + height/2 + ')')
        .style({
          'text-anchor': 'middle'
        })
        .html('No Data');

      return chart;
    }

    // sort data
    data.sort(ordering(order));

    x.domain(data.map(function(d, i) { return xAccessor(d, i); }));
    y.domain([0, scale ? 100 : 1.1 * d3.max(data, function(d, i) { return yAccessor(d, i); })]);

    // Draw the y Grid lines
    svg.append('g')
      .attr('class', 'grid')
      .style({
        'stroke': 'lightgrey',
        'stroke-opacity': 0.7,
        'shape-rendering': 'crispEdges'
      })
      .call(d3.svg.axis()
        .scale(y)
        .orient('left')
        .tickSize(-width, 0, 0)
        .tickFormat('')
      );

    // Draw stacked bars
    bars = svg.selectAll('.bar')
      .data(data);

    bars.enter().append('rect')
      .attr('class', 'bar')
      .attr('x', function(d, i) { return x(xAccessor(d, i)); })
      .attr('width', x.rangeBand())
      .attr('y', function(d, i) { return y(yAccessor(d, i)); })
      .attr('height', function(d, i) { return height - y(yAccessor(d, i)); })
      .style({
        'fill': 'steelblue',
        'shape-rendering': 'crispEdges'
      })
      .on('mouseover', mouseover)
      .on('mouseout', mouseout)
      .on('mousemove', mousemove);

    bars.exit().remove();

    // bar labels
    barLabels = svg.selectAll('.bar-label')
      .data(data);

    barLabels.enter().append('text')
      .attr('class', 'bar-label')
      .attr("text-anchor", "middle")
      .style("fill", function(d, i){ return height - y(yAccessor(d, i)) < 18 ? '#000' : "#fff"; })
      .style({
        'font': '13px sans-serif'
      })
      .attr("x", function(d, i) { return x(xAccessor(d, i)) + x.rangeBand() / 2; })
      .attr("y", function(d, i) { return y(yAccessor(d, i)) + (height - y(yAccessor(d, i)) < 18 ? -2 : 13); })
      .text(function(d){ return d.y + '%'; });

    barLabels.exit().remove();

    // X Axis
    xAxisG = svg.append('g')
      .attr('class', 'x axis')
      .attr('transform', 'translate(0,' + height + ')')
      .style({
        'font': '12px sans-serif'
      })
      .call(xAxis)

    xAxisG.selectAll('path')
      .style({
        'display': 'none'
      });

    xAxisG.selectAll('line')
      .style({
        'fill': 'none',
        'stroke': '#000',
        'shape-rendering': 'crispEdges'
      });

    // Y Axis
    yAxisG = svg.append('g')
      .attr('class', 'y axis')
      .attr('transform', 'translate(' + 0 + ',0)')
      .style({
        'font': '12px sans-serif'
      })
      .call(yAxis);

    yAxisG.selectAll('path')
      .style({
        'fill': 'none',
        'stroke': '#000',
        'shape-rendering': 'crispEdges'
      });

    yAxisG.selectAll('line')
      .style({
        'fill': 'none',
        'stroke': '#000',
        'shape-rendering': 'crispEdges'
      });

    // Tooltip
    tooltip = d3.select(selector).append('div')
      .attr('class', 'tip')
      .style('display', 'none');

    // export module
    chart.divRealWidth = fullWidth;
    chart.divRealHeight = fullHeight;
    chart.div = d3.select(selector).node();
    chart.svg = svg;

    return chart;
  }

  // redraw the chart with new data
  function redraw(){
    if (!data || !data.length || !svg.selectAll('.bar')[0].length) return render();

    // sort data
    data.sort(ordering(order));

    x.domain(data.map(function(d, i) { return xAccessor(d, i); }));
    y.domain([0, scale ? 100 : 1.1 * d3.max(data, function(d, i) { return yAccessor(d, i); })]);

    // Draw the y Grid lines
    svg.selectAll('.grid')
      .transition()
      .duration(duration)
      .call(d3.svg.axis()
        .scale(y)
        .orient('left')
        .tickSize(-width, 0, 0)
        .tickFormat('')
      );

    // bars
    bars = svg.selectAll('.bar')
      .data(data);

    bars
      .transition()
      .duration(duration)
      .attr('x', function(d, i) { return x(xAccessor(d, i)); })
      .attr('width', x.rangeBand())
      .attr('y', function(d, i) { return y(Math.max(0, yAccessor(d, i))); })
      .attr('height', function(d, i) { return Math.abs(y(yAccessor(d, i)) - y(0)); })

    bars.style({
        'fill': 'steelblue'
      })
      .on('mouseover', mouseover)
      .on('mouseout', mouseout)
      .on('mousemove', mousemove);

    bars.exit()
      .transition()
      .duration(duration)
      .attr('height', 0)
      .attr('y', y(0))
      .remove();

    // bar labels
    barLabels = svg.selectAll('.bar-label')
      .data(data);

    barLabels
      .transition()
      .duration(duration)
      .style("fill", function(d, i){ return height - y(yAccessor(d, i)) < 18 ? '#000' : "#fff"; })
      .attr("x", function(d, i) { return x(xAccessor(d, i)) + x.rangeBand() / 2; })
      .attr("y", function(d, i) { return y(yAccessor(d, i)) + (height - y(yAccessor(d, i)) < 18 ? -2 : 13); })
      .text(function(d){ return d.y + '%'; });

    barLabels.exit()
      .transition()
      .duration(duration)
      .attr('y', y(0))
      .remove();

    xAxisG.transition().duration(duration).call(xAxis);
    yAxisG.transition().duration(duration).call(yAxis);

    return chart;
  }

  // update with new data
  function updateData(_data){
    data = _data.slice();
  }

  // fade render
  function fadeRender(){
    var duration = 200;

    d3.select(selector)
      .style('opacity', 1)
      .transition()
      .duration(duration)
      .style('opacity', 0)
      .each('end', function(){
        render();

        d3.select(selector)
          .style('opacity', 0)
          .transition()
          .duration(duration)
          .style('opacity', 1);
      });

    return chart;
  }

  // clearing
  function clear(){
    //clear element
    d3.select(selector).html('');

    // remove tooltip
    d3.select(selector).selectAll('.tip').remove();
  }

  // ordering
  function ordering(order){
    switch (order) {
      // desc
      case 0: return function(a, b){ return yAccessor(b) - yAccessor(a); };

      // asc
      case 1: return function(a, b){ return yAccessor(a) - yAccessor(b); };

      // abc
      case 2: return function(a, b){ return yAccessor(b) - yAccessor(a); };
    }
  }

  // Utils
  function mouseover(d, i){
    d3.select(this)
      .style({
        'fill': 'brown'
      });

    tooltip.style('display', null);
  }

  function mouseout(d, i){
    d3.select(this)
      .style({
        'fill': 'steelblue'
      });

    tooltip.style('display', 'none');
  }

  function mousemove(d, i){
    var tpl =
      '<ul>' +
      '<li><b>' + xAccessor(d, i) + '</b></li>' +
      '<li>Count: ' + d.count +'</li>' +
      '<li>' + yAccessor(d, i) +'%</li>' +
      '</ul>';

    tooltip.html(tpl);

    var xPosition = d3.event.layerX - 40;
    var yPosition = d3.event.layerY - 30;

    tooltip.style('top', yPosition + 'px');
    tooltip.style('left', xPosition + 'px');
  }

  // main object
  chart = {
    selector: selector,
    type: 'bar',
    data: data,
    classNamePrefix: 'chart-export',
    x: function(){ return x; },
    y: function(){ return y; },
    render: render,
    redraw: redraw,
    updateData: updateData,
    fadeRender: fadeRender,
    clear: clear
  };

  chart.order = function(_){
    if (!arguments.length) return order;
    order = _;
    return chart;
  }

  chart.scale = function(_){
    if (!arguments.length) return scale;
    scale = _;
    return chart;
  }

  return chart;
}/**
 * Horizontal Bar Chart Definition
 */
;function horizontalBarChart(_data, selector, options){
  options = options || {};
  var data = _data.slice();

  var chart
    , fullWidth
    , fullHeight
    , margin
    , width
    , height
    , x
    , y
    , xAccessor = options.xAccessor || function(d) { return d.x }
    , yAccessor = options.yAccessor || function(d) { return d.y }
    , xAxis
    , yAxis
    , svg
    , bars
    , barLabels
    , xAxisG
    , yAxisG
    , tooltip
    , duration = 500
    , order = options.order || 0
    , scale = options.scale || 0
  ;

  // render the chart completely
  function render(){

    // clear
    clear();

    // set width
    fullWidth = options.fullWidth || $(selector).width() || 300;
    fullHeight = options.fullHeight || $(selector).height() - 30 || 300;

    margin = {top: 20, right: 10, bottom: 30, left: 80};
    if (data && data.length) {
      margin.left = d3.max(data.map(function(d, i){ return yAccessor(d, i).length * 6 + 15; }));
    }

    width = fullWidth - margin.left - margin.right;
    height = fullHeight - margin.top - margin.bottom;

    y = d3.scale.ordinal()
      .rangeRoundBands([height, 0], 0.1);

    x = d3.scale.linear()
      .range([0, width])
      .nice();

    xAxis = d3.svg.axis()
      .scale(x)
      .orient('bottom')
      .tickSize(4)

    yAxis = d3.svg.axis()
      .scale(y)
      .orient('left')
      .tickSize(4);


    // Create svg
    svg = d3.select(selector).append('svg')
      .attr('width', fullWidth)
      .attr('height', fullHeight)
      .style({
        'position': 'relative'
      })
      .append('g')
      .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    if (!data || !data.length) {
      svg
        .attr('transform', 'translate(0,0)')
        .append('text')
        .attr('transform', 'translate(' + fullWidth/2 + ',' + fullHeight/2 + ')')
        .style({
          'text-anchor': 'middle'
        })
        .html('No Data');

      return chart;
    }

    if (data.length > 10) {
      svg
        .attr('transform', 'translate(0,0)')
        .append('text')
        .attr('transform', 'translate(' + fullWidth/2 + ',' + fullHeight/2 + ')')
        .style({
          'text-anchor': 'middle'
        })
        .html('Too Many Values');

      return chart;
    }

    // sort data
    data.sort(ordering(order));

    x.domain([0, scale ? 100 : 1.1 * d3.max(data, function(d, i) { return xAccessor(d, i); })]);
    y.domain(data.map(function(d, i) { return yAccessor(d, i); }));

    // Draw the y Grid lines
    svg.append('g')
      .attr('class', 'grid')
      .style({
        'stroke': 'lightgrey',
        'stroke-opacity': 0.7,
        'shape-rendering': 'crispEdges'
      })
      .call(d3.svg.axis()
        .scale(x)
        .orient('bottom')
        .tickSize(height, 0, 0)
        .tickFormat('')
      );

    // Draw stacked bars
    bars = svg.selectAll('.bar')
      .data(data);

    bars.enter().append('rect')
      .attr('class', 'bar')
      .attr('width', function(d, i) { return x(xAccessor(d, i)); })
      .attr('y', function(d, i) { return y(yAccessor(d, i)); })
      .attr('height', y.rangeBand())
      .style({
        'fill': 'steelblue',
        'shape-rendering': 'crispEdges'
      })
      .on('mouseover', mouseover)
      .on('mouseout', mouseout)
      .on('mousemove', mousemove);

    bars.exit().remove();

    // bar labels
    barLabels = svg.selectAll('.bar-label')
      .data(data);

    barLabels.enter().append('text')
      .attr('class', 'bar-label')
      .attr("text-anchor", "end")
      .style("fill", function(d, i){ return x(xAccessor(d, i)) < 30 ? '#000' : "#fff"; })
      .style({
        'font': '13px sans-serif'
      })
      .attr("x", function(d, i) { return x(xAccessor(d, i)) + (x(xAccessor(d, i)) < 30 ? 32 : -4); })
      .attr("y", function(d, i) { return y(yAccessor(d, i)) + y.rangeBand() / 2 + 4; })
      .text(function(d){ return d.x + '%'; });

    barLabels.exit().remove();


    // X Axis
    xAxisG = svg.append('g')
      .attr('class', 'x axis')
      .attr('transform', 'translate(0,' + height + ')')
      .style({
        'font': '12px sans-serif'
      })
      .call(xAxis)

    xAxisG.selectAll('path')
      .style({
        'fill': 'none',
        'stroke': '#000',
        'shape-rendering': 'crispEdges'
      });

    xAxisG.selectAll('line')
      .style({
        'fill': 'none',
        'stroke': '#000',
        'shape-rendering': 'crispEdges'
      });

    // Y Axis
    yAxisG = svg.append('g')
      .attr('class', 'y axis')
      .attr('transform', 'translate(' + 0 + ',0)')
      .style({
        'font': '12px sans-serif'
      })
      .call(yAxis);

    yAxisG.selectAll('path')
      .style({
        'fill': 'none',
        'stroke': '#000',
        'shape-rendering': 'crispEdges'
      });

    yAxisG.selectAll('line')
      .style({
        'fill': 'none',
        'stroke': '#000',
        'shape-rendering': 'crispEdges'
      });

    // Tooltip
    tooltip = d3.select(selector).append('div')
      .attr('class', 'tip')
      .style('display', 'none');

    // export module
    chart.divRealWidth = fullWidth;
    chart.divRealHeight = fullHeight;
    chart.div = d3.select(selector).node();
    chart.svg = svg;

    return chart;
  }

  // redraw the chart with new data
  function redraw(){
    if (!data || !data.length || !svg.selectAll('.bar')[0].length) return render();

    // sort data
    data.sort(ordering(order));

    x.domain([0, scale ? 100 : 1.1 * d3.max(data, function(d, i) { return xAccessor(d, i); })]);
    y.domain(data.map(function(d, i) { return yAccessor(d, i); }));

    // Draw the y Grid lines
    svg.selectAll('.grid')
      .transition()
      .duration(duration)
      .call(d3.svg.axis()
        .scale(x)
        .orient('bottom')
        .tickSize(height, 0, 0)
        .tickFormat('')
      );

    bars = svg.selectAll('.bar')
      .data(data)

    bars
      .transition()
      .duration(duration)
      .attr('width', function(d, i) { return x(xAccessor(d, i)); })
      .attr('y', function(d, i) { return y(yAccessor(d, i)); })
      .attr('height', y.rangeBand())

    bars.style({
        'fill': 'steelblue'
      })
      .on('mouseover', mouseover)
      .on('mouseout', mouseout)
      .on('mousemove', mousemove);

    bars.exit()
      .transition()
      .duration(duration)
      .attr('width', 0)
      .remove();

    // bar labels
    barLabels = svg.selectAll('.bar-label')
      .data(data)

    barLabels.transition()
      .duration(duration)
      .attr("x", function(d, i) { return x(xAccessor(d, i)) + (x(xAccessor(d, i)) < 30 ? 32 : -4); })
      .attr("y", function(d, i) { return y(yAccessor(d, i)) + y.rangeBand() / 2 + 4; })
      .style("fill", function(d, i){ return x(xAccessor(d, i)) < 30 ? '#000' : "#fff"; })
      .text(function(d){ return d.x + '%'; });

    barLabels.exit()
      .transition()
      .duration(duration)
      .attr('x', 0)
      .remove();

    xAxisG.transition().duration(duration).call(xAxis);
    yAxisG.transition().duration(duration).call(yAxis);

    return chart;
  }

  // update with new data
  function updateData(_data){
    data = _data.slice();
  }

  // fade render
  function fadeRender(){
    var duration = 200;

    d3.select(selector)
      .style('opacity', 1)
      .transition()
      .duration(duration)
      .style('opacity', 0)
      .each('end', function(){
        render();

        d3.select(selector)
          .style('opacity', 0)
          .transition()
          .duration(duration)
          .style('opacity', 1);
      });

    return chart;
  }

  // clearing
  function clear(){
    //clear element
    d3.select(selector).html('');

    // remove tooltip
    d3.select(selector).selectAll('.tip').remove();
  }

  // ordering
  function ordering(order){
    switch (order) {
      // desc
      case 0: return function(a, b){ return xAccessor(a) - xAccessor(b); };

      // asc
      case 1: return function(a, b){ return xAccessor(b) - xAccessor(a); };

      // abc
      case 2: return function(a, b){ return yAccessor(b) > yAccessor(a); };
    }
  }

  // Utils
  function mouseover(d, i){
    d3.select(this)
      .style({
        'fill': 'brown'
      });

    tooltip.style('display', null);
  }

  function mouseout(d, i){
    d3.select(this)
      .style({
        'fill': 'steelblue'
      });

    tooltip.style('display', 'none');
  }

  function mousemove(d, i){
    var tpl =
      '<ul>' +
      '<li><b>' + yAccessor(d, i) + '</b></li>' +
      '<li>Count: ' + d.count +'</li>' +
      '<li>' + xAccessor(d, i) +'%</li>' +
      '</ul>';

    tooltip.html(tpl);

    var xPosition = d3.event.layerX - 35;
    var yPosition = d3.event.layerY - 30;

    tooltip.style('top', yPosition + 'px');
    tooltip.style('left', xPosition + 'px');
  }

  // main object
  chart = {
    selector: selector,
    type: 'horizontalBar',
    data: data,
    classNamePrefix: 'chart-export',
    x: function(){ return x; },
    y: function(){ return y; },
    render: render,
    redraw: redraw,
    updateData: updateData,
    fadeRender: fadeRender,
    clear: clear
  };

  chart.order = function(_){
    if (!arguments.length) return order;
    order = _;
    return chart;
  }

  chart.scale = function(_){
    if (!arguments.length) return scale;
    scale = _;
    return chart;
  }

  return chart;
}