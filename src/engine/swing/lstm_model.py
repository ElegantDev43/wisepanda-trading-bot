import os
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import tensorflow as tf
from keras.src.models import Sequential
from keras.src.layers import LSTM, Dense, Activation, Dropout
from sklearn.preprocessing import MinMaxScaler
import plotly.graph_objects as go
from keras.src.saving import register_keras_serializable, load_model


from src.engine.swing.lstm_predict import predict_lstm

@register_keras_serializable()
def custom_mse(y_true, y_pred):
    return tf.reduce_mean(tf.square(y_pred - y_true))

target = 'value'
look_back = 1

# convert an array of values into a dataset matrix
def create_dataset(dataset, look_back=1):
	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), 0]
		dataX.append(a)
		dataY.append(dataset[i + look_back, 0])
	return np.array(dataX), np.array(dataY)


def build_lstm_model(input_data, output_size, neurons, activ_func='linear',
                     dropout=0.2, loss='mse', optimizer='adam'):
    model = Sequential()
    # model.add(LSTM(neurons * 2, return_sequences=True ,input_shape=(input_data.shape[1], input_data.shape[2])))
    model.add(LSTM(neurons, input_shape=(input_data.shape[1], input_data.shape[2])))
    model.add(Dropout(dropout))
    model.add(Dense(units=output_size))
    model.add(Activation(activ_func))

    model.compile(loss=loss, optimizer=optimizer)
    return model

async def study_lstm(token):
  
  if os.path.exists(f'src/engine/swing/price_data/price_data_{token}.csv') != True:
    return
  data = pd.read_csv(f"src/engine/swing/price_data/price_data_{token}.csv")

  # fix random seed for reproducibility
  np.random.seed(5)

  # Load the history and convert it for training
  data = pd.read_csv(f"src/engine/swing/price_data/price_data_{token}.csv")
  data = pd.DataFrame(data)
  data = data.set_index('date')
  data.index = pd.to_datetime(data.index, unit='ns')

  target = 'value'

  data = data[target]
  data = np.array(data)

  # normalize the dataset
  scaler = MinMaxScaler(feature_range=(0, 1))
  dataset = scaler.fit_transform(data.reshape(-1, 1))

  # split into train and test sets, 20% test data, 80% training data
  train_size = int(len(dataset) * 0.8)
  test_size = len(dataset) - train_size
  train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]

  # Splite train and test data as input and output data
  trainX, trainY = create_dataset(train, look_back)
  testX, testY = create_dataset(test, look_back)


  trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
  testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

  # Build the model and train
  model = build_lstm_model(
      trainX, output_size=1, neurons=16, dropout=0.24, loss=custom_mse, optimizer='adam')
  modelfit = model.fit(
      trainX, trainY, validation_data=(testX, testY), epochs=32, batch_size=32, verbose=1, shuffle=True)

  # Save the trained model
  model.save(f"LSTM_{token}.h5")
  
  await predict_lstm(token)