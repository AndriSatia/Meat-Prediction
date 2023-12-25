from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
from django.views.decorators.csrf import csrf_exempt
from django.http import QueryDict

def data_model():
    model_filepath = 'Project/models/'
    model_filename = 'PrediksiDaging.h5'

    dataset_filepath = 'Project/datasets/'
    dataset_filename = 'Coba6.csv'

    model = load_model(model_filepath + model_filename)
    # Load dataset
    df = pd.read_csv(dataset_filepath + dataset_filename)
    df['Tanggal'] = pd.to_datetime(df['Tanggal'])
    df.sort_values('Tanggal', inplace=True)
    df = df.dropna(subset=['Harga'])
    data = df['Harga'].values.reshape(-1, 1)

    scaler = MinMaxScaler(feature_range=(0, 1))
    data_scaled = scaler.fit_transform(data)

    time_steps = 10
    X, y = create_dataset(data_scaled, time_steps)

    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    predictions = model.predict(X)

    predictions = scaler.inverse_transform(predictions)
    y = scaler.inverse_transform(y.reshape(1, -1)).flatten()

    return df, y, predictions, time_steps, model, scaler,

def create_dataset(dataset, time_steps=1):
    dataX, dataY = [], []
    for i in range(len(dataset)-time_steps):
        a = dataset[i:(i+time_steps), 0]
        dataX.append(a)
        dataY.append(dataset[i + time_steps, 0])
    return np.array(dataX), np.array(dataY)

import numpy as np

def plot_predictions(df, y_true, predictions, time_steps):
    tanggal_string = df['Tanggal'][time_steps:].dt.strftime('%Y-%m-%d').tolist()
    flatten_predictions = np.ndarray.flatten(predictions)

    result_data = {
        'tanggal': tanggal_string,
        'true_data': y_true.tolist(),
        'predictions': flatten_predictions.tolist()
    }
    return result_data


def index(request):
    return render(request, 'home.html')

def statistic(request):
    return render(request, 'statistic.html')

def about_us(request):
    return render(request, 'about_us.html')

def graph(request):
    df, y, predictions, time_steps, model, scaler = data_model()
    result = plot_predictions(df, y, predictions, time_steps)
    return JsonResponse(result)

@csrf_exempt
def predict_price(request):
    if request.method == 'POST':
        data = QueryDict(request.body)
        input_bulan_tahun = data.get('tanggal_prediksi')

        df, y, predictions, time_steps, model, scaler = data_model()

        tanggal_prediksi = pd.to_datetime(input_bulan_tahun, format='%d/%m/%Y')

        data_prediksi = df[df['Tanggal'] <= tanggal_prediksi]['Harga'].values.reshape(-1, 1)
        data_prediksi_scaled = scaler.transform(data_prediksi)

        X_prediksi, y_prediksi = create_dataset(data_prediksi_scaled, time_steps)
        X_prediksi = np.reshape(X_prediksi, (X_prediksi.shape[0], X_prediksi.shape[1], 1))

        prediksi = model.predict(X_prediksi)
        prediksi = scaler.inverse_transform(prediksi)

        hasil_prediksi = f'Prediksi harga pada tanggal {input_bulan_tahun}: Rp{prediksi[-1, 0]:.2f}'

        return JsonResponse({'hasil_prediksi': hasil_prediksi})

    return JsonResponse({})