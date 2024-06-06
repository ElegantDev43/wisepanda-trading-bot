import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.preprocessing import StandardScaler

import pickle

from sklearn.metrics import accuracy_score, classification_report

async def study_model(token):
  # Define parameter grid
  param_grid = {
      'n_estimators': [50, 100, 200, 300],
      'learning_rate': [0.01, 0.1, 0.2, 0.4],
      'max_depth': [3, 4, 5, 6]
  }

  dataFrame = pd.read_csv(f'src/engine/swing/price_data/price_data_{token}.csv', parse_dates=True, index_col= 2)
  dataFrame = dataFrame.iloc[::-1]

  features = [
            'swing', 'rsi', 'sma_5','sma_10','sma_20','sma_40',
            'ema_5','ema_10','ema_20','ema_40','tma', 'macd', 'signal','bb_up','bb_low',
            'william','vol', 'onvolume','cmo','dpo','+di','-di','dx','adx','adxr',
            'lri','lrs','mp','mom','prc','sd','smi','ws'
            ]

  X = dataFrame[features]
  Y = dataFrame['Target']
  print(X)

  # Split data into training and test sets
  X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

  # Feature scaling
  scaler = StandardScaler()
  X_train_scaled = scaler.fit_transform(X_train)
  X_test_scaled = scaler.transform(X_test)

  # Train the model
  model = GradientBoostingClassifier(n_estimators=100, random_state=42)
  model.fit(X_train_scaled, y_train)

  with open(f'src/engine/swing/model/model_{token}.pkl', 'wb') as f:
      pickle.dump(model, f)

  # Predict on test set
  y_pred = model.predict(X_test_scaled)

  print(y_pred)
  # Evaluate the model
  print("Accuracy:", accuracy_score(y_test, y_pred))
  print(classification_report(y_test, y_pred))
