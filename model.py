import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
import datetime
ticker = yf.Ticker('AAPL')
inf = ticker.info
df = pd.DataFrame().from_dict(inf, orient="index").T
ticker = yf.Ticker('AAPL')
inf = ticker.info

today = datetime.date.today()
sixty_days_prior = datetime.date.today() - datetime.timedelta(days=60)
df = ticker.history(start=sixty_days_prior, end=today, interval="1d")
df = df[["Close"]]
forecast_out = 1
#create another column (the target or dependent variable) shifted n units up
df['Prediction'] = df[["Close"]].shift(-forecast_out)
X = np.array(df.drop(["Prediction"], 1))
#remove the last n rows
X = X[:-forecast_out]
y = np.array(df["Prediction"])
#get all the y values except the last n rows
y = y[:-forecast_out]
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.1)
#svm_confidence = svr_rbf.score(x_test, y_test)
lr = LinearRegression()
#train the model
lr.fit(x_train, y_train)
x_forecast = np.array(df.drop(["Prediction"], 1))[-forecast_out:]
lr_prediction = lr.predict(x_forecast)