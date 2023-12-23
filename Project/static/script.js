$(document).ready(function () {
    // Use Ajax to get data from views.py
    $.ajax({
      url: "/graph/", // Use the correct URL for your Django view
      type: "GET",
      dataType: "json",
      success: function (result) {
        // Extract data for the chart
        var labels = result['tanggal'];
        var trueData = result['true_data'];
        var predictions = result['predictions'];
  
        // Create a line chart using Chart.js
        var ctx = document.getElementById('predictionChart').getContext('2d');
        var myChart = new Chart(ctx, {
          type: 'line',
          data: {
            labels: labels,
            datasets: [{
              label: 'True Data',
              data: trueData,
              borderColor: 'blue',
              backgroundColor: 'white',
              fill: false
            }, {
              label: 'Predictions',
              data: predictions,
              borderColor: 'red',
              backgroundColor: 'white',
              fill: false
            }]
          },
          options: {
            scales: {
              x: [{
                type: 'time',
                time: {
                  unit: 'day',
                  displayFormats: {
                    day: 'YYYY-MM-DD'
                  }
                }
              }],
              y: [{
                scaleLabel: {
                  display: true,
                  labelString: 'Value'
                }
              }]
            }
          }
        });
      },
      error: function (error) {
        console.error("Error fetching data:", error);
      }
    });
  });
  