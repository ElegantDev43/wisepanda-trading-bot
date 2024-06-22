import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import tensorflow as tf
from keras.src.saving import load_model
from sklearn.preprocessing import MinMaxScaler
import plotly.graph_objects as go
from keras.src.saving import register_keras_serializable




import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


@register_keras_serializable()
def custom_mse(y_true, y_pred):
    return tf.reduce_mean(tf.square(y_pred - y_true))

async def predict_lstm(token):

    look_back = 1
    target = 'value'
    # Load the model
    model = load_model(f'src/engine/swing/model/LSTM_{token}.h5', custom_objects={'custom_mse': custom_mse})
    # fix random seed for reproducibility
    np.random.seed(170)
    # Load the CSV file
    raw_data = pd.read_csv(f"src/engine/swing/test_data/test_data_{token}.csv")
    data = pd.DataFrame(raw_data)
    data = data[target].values

    # Initialize the scaler and fit it on the initial look_back data
    scaler = MinMaxScaler(feature_range=(0, 1))

    predictions = []

#    data = data[:look_back]
    scaled_data = scaler.fit_transform(data.reshape(-1, 1))

    for i in range(0, 60, 1):
        # Extract the initial look_back data
        inputX = scaled_data[i:i+look_back].reshape(1, 1, look_back)
        print(inputX)
        # Make prediction
        prediction = model.predict(inputX)
        # Append prediction to the predictions list
        predictions.append(prediction[0][0])
        #scaled_data = np.append(scaled_data, prediction[0][0])

    predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1)).flatten()

    plt.figure(figsize=(10, 5))
    plt.plot(raw_data[target][:60], linewidth=1,color = 'red', label='Actual')
    plt.plot(predictions, linewidth=1, label='Prediction')
    plt.title('LSTM Neural Networks - XRP Model')
    plt.xlabel('Epochs numbers')
    plt.ylabel('MSE numbers')
    plt.legend()
    
    # Save the plot as a PNG file
    plt.savefig(f'src/engine/swing/data_png/prices_{token}_predict.png')
