$(document).ready(function () {
    $.ajax({
      url: "/graph/", 
      type: "GET",
      dataType: "json",
      success: function (result) {
        var labels = result['tanggal'];
        var trueData = result['true_data'];
        var predictions = result['predictions'];
  
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
  