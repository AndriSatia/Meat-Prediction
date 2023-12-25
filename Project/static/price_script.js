var csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;

function predictPrice() {
  var tanggalPrediksi = $('#tanggal_prediksi').val();

  $.ajax({
    type: 'POST',
    url: '/predict_price/',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'X-CSRFToken': csrf_token,
    },
    data: { tanggal_prediksi: tanggalPrediksi },
    success: function (data) {
      $('#hasil_prediksi').html(data.hasil_prediksi);
    },
    error: function () {
      console.log('Error in prediction request.');
    },
  });
}
