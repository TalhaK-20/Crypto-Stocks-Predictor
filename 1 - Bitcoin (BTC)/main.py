import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib


# ------------------------ Reading Data ------------------------

data = pd.read_excel('data/Bitcoin.xlsx')
print(data.head())

data['Days'] = np.arange(len(data))
X = data[['Days']]
#  These are dependent factors
y_open = data['open']
y_high = data['high']
y_low = data['low']
y_close = data['close']


# ------------------------ Train & Test ------------------------

X_train, X_test, y_open_train, y_open_test = train_test_split(X, y_open, test_size=0.2, random_state=0)
_, _, y_high_train, y_high_test = train_test_split(X, y_high, test_size=0.2, random_state=0)
_, _, y_low_train, y_low_test = train_test_split(X, y_low, test_size=0.2, random_state=0)
_, _, y_close_train, y_close_test = train_test_split(X, y_close, test_size=0.2, random_state=0)


# ------------------------ Transferring Functionalities ------------------------

open_price_column = LinearRegression()
high = LinearRegression()
low = LinearRegression()
close = LinearRegression()


# ------------------------ Accuracy Portion ------------------------

open_price_column.fit(X_train, y_open_train)
high.fit(X_train, y_high_train)
low.fit(X_train, y_low_train)
close.fit(X_train, y_close_train)

accuracy_open = open_price_column.score(X_test, y_open_test)
accuracy_high = high.score(X_test, y_high_test)
accuracy_low = low.score(X_test, y_low_test)
accuracy_close = close.score(X_test, y_close_test)

print("\n")
print(f'Open Model Accuracy: {accuracy_open * 100:.2f}%')
print(f'High Model Accuracy: {accuracy_high * 100:.2f}%')
print(f'Low Model Accuracy: {accuracy_low * 100:.2f}%')
print(f'Close Model Accuracy: {accuracy_close * 100:.2f}%')


# ------------------------ Predictions Portion ------------------------

next_day = np.array([[data['Days'].max() + 1]])

pred_open = open_price_column.predict(next_day)
pred_high = high.predict(next_day)
pred_low = low.predict(next_day)
pred_close = close.predict(next_day)

print("\n")
print(f'Predicted Open Price for Next Day: {pred_open[0]}')
print(f'Predicted High Price for Next Day: {pred_high[0]}')
print(f'Predicted Low Price for Next Day: {pred_low[0]}')
print(f'Predicted Close Price for Next Day: {pred_close[0]}')


# ------------------------ Create Models Folder ------------------------

if not os.path.exists('models'):
    os.makedirs('models')


# ------------------------ Saving Models to Files ------------------------

joblib.dump(open_price_column, 'models/btc_price_open_model.pkl')
joblib.dump(high, 'models/btc_price_high_model.pkl')
joblib.dump(low, 'models/btc_price_low_model.pkl')
joblib.dump(close, 'models/btc_price_close_model.pkl')


# ------------------------ Loading Models from Files ------------------------

loaded_model_open = joblib.load('models/btc_price_open_model.pkl')
loaded_model_high = joblib.load('models/btc_price_high_model.pkl')
loaded_model_low = joblib.load('models/btc_price_low_model.pkl')
loaded_model_close = joblib.load('models/btc_price_close_model.pkl')


# ------------------------ New Predictions from Loaded Files ------------------------

new_open_prediction = loaded_model_open.predict(next_day)
new_high_prediction = loaded_model_high.predict(next_day)
new_low_prediction = loaded_model_low.predict(next_day)
new_close_prediction = loaded_model_close.predict(next_day)

print("\n")
print(f'Predicted Open Price for Next Day (Loaded Model): {new_open_prediction[0]}')
print(f'Predicted High Price for Next Day (Loaded Model): {new_high_prediction[0]}')
print(f'Predicted Low Price for Next Day (Loaded Model): {new_low_prediction[0]}')
print(f'Predicted Close Price for Next Day (Loaded Model): {new_close_prediction[0]}')
