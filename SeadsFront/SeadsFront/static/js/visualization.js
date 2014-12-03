var data1 = {{data|safe}};
  console.log(data1);
  google.load("visualization", "1", {packages:["corechart"]});
  google.setOnLoadCallback(drawChart);
  function drawChart() {
    var data = google.visualization.arrayToDataTable(data1);
    var options = {
      title: 'API_CALL: {{api_call}}',
      curveType: 'function',
      legend: { position: 'bottom' }
    };
    var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
    {% if data != -1 %}
    chart.draw(data, options);
    {% endif %}
  }

  $(function () {
    $('#datetimepicker2').datetimepicker({
      pick12HourFormat: true,
      defaultDate: "11/1/2014",
      language: 'en'
    }); 
  });

  $(function () {
    $('#datetimepicker1').datetimepicker({
      pick12HourFormat: true,
      defaultDate: "11/1/2014",
      language: 'en'
    });
  });

  $(function () {
    $("#datetimepicker1").on("dp.hide", function (e) {display_new_range()})
  });

  $(function () {
    $("#datetimepicker2").on("dp.hide", function (e) {display_new_range()})
  });
  
  function display_new_range() {
    var start_time = $("#datetimepicker1").data('DateTimePicker').date.unix();
    var end_time = $("#datetimepicker2").data('DateTimePicker').date.unix();
    $.get("", {start_time : start_time,  end_time : end_time}, function(data){
      console.log(data);
      data1 = data;
      drawChart();
    });
  };   