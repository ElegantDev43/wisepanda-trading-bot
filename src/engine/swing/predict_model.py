import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier,VotingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression ,LinearRegression,RidgeClassifier, Lasso
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB  # For Naive Bayes classifiers
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split,GridSearchCV,cross_val_score
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler,MinMaxScaler
from sklearn.feature_selection import SelectKBest, f_classif
from imblearn.over_sampling import SMOTE
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
#from xgboost import XGBClassifier

import pickle

from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder

async def prepare_model(token):
  # Define parameter grid
  param_grid = {
      'n_estimators': [50, 100, 200, 300],
      'learning_rate': [0.01, 0.1, 0.2, 0.4],
      'max_depth': [3, 4, 5, 6]
  }

  if os.path.exists(f'src/engine/swing/price_data/price_data_{token}.csv') != True:
    return

  dataFrame = pd.read_csv(f'src/engine/swing/price_data/price_data_{token}.csv', parse_dates=True, index_col= 3)
  dataFrame = dataFrame.iloc[::-1]

  if dataFrame.empty:
    return

  features = ['prev_value','prev_value_2',
            'sma_5','sma_10',
            'ema_5','ema_10',
            'tma','close',
            'swing', 'rsi','macd', 'signal',
            'bb_up','bb_low',
            'william','vol', 'onvolume','cmo','dpo','+di','-di','dx','adx','adxr',
            'lrs','mom','prc','sd','smi','tenkan_sen','kijun_sen','senkou_a','senkou_b','sar','cci','obv',
            'pvt','tsf'
            ]

  X = dataFrame[features]
  Y = dataFrame['Target_2']

#  scaler = MinMaxScaler(feature_range=(0,1))
  scaler = StandardScaler()
  X = scaler.fit_transform(X)
  # X_test_scaled = scaler.transform(X_test)

  X_train, X_test, y_train, y_test = train_test_split(X, Y,stratify=Y,test_size=0.2, random_state=42)

  # Feature scaling
  X_train_scaled = X_train
  X_test_scaled = X_test

#  smote = SMOTE(random_state=42)
#  X_train_scaled, y_train = smote.fit_resample(X_train_scaled, y_train)


  # Create an ensemble of models
  model = VotingClassifier(estimators=[
      ('rf', RandomForestClassifier(random_state=42)),
      #('xgb', XGBClassifier()),
      ('gb', GradientBoostingClassifier(random_state=42)),
  ], voting='soft')

  # Train the ensemble model
  model.fit(X_train_scaled, y_train)

  # model = RandomForestClassifier(n_estimators=300,max_depth=30, random_state=42)
  # model.fit(X_train_scaled, y_train)

  with open(f'src/engine/swing/model/model_{token}.pkl', 'wb') as f:
      pickle.dump(model, f)

  with open(f'src/engine/swing/model/model.pkl', 'wb') as f:
      pickle.dump(model, f)

  # Predict on test set
  y_pred = model.predict(X_test_scaled)

  print(y_pred)
  # Evaluate the model
  print("Accuracy:", accuracy_score(y_test, y_pred))
  print(classification_report(y_test, y_pred))


async def study_model(token):
    await prepare_model(token)