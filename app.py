from flask import Flask, jsonify
from statsmodels.tsa.arima.model import ARIMA
import pandas as pd
from datetime import datetime, timedelta
from pymongo import MongoClient
from pycaret.time_series import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Assume 'collection' is your MongoDB collection object
client = MongoClient(
    "<mongo_db_credentials>")
db = client['test']
collection = db['sensordatas']


def fetch_data_from_mongodb(room_number='Room108'):
    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    start_date = today - pd.DateOffset(hours=160)
    cursor = collection.find(
        {'temperature': {'$exists': True, '$ne': None},
         'roomNumber': room_number, 'createdAt': {'$gte': start_date}},
        {'createdAt': 1, 'temperature': 1, '_id': 0}
    )
    data = list(cursor)
    df = pd.DataFrame(data)
    print((df))
    return df


def fill_missing_values(df):
    df = df.drop_duplicates(
        subset=['createdAt'], keep='last').reset_index(drop=True)
    df['createdAt'] = pd.to_datetime(df['createdAt'])
    df.set_index('createdAt', inplace=True)
    df_resampled = df.resample('5T').mean()
    df_filled = df_resampled.interpolate(method='linear')

    return df_filled


def predict_temperature_pycaret(df_filled, steps=31):
    arima_model = ARIMA(df_filled, order=([1, 15, 18], 0, 3))
    arima_model_fit = arima_model.fit()
    preds = arima_model_fit.forecast(steps=steps)

    return preds


@app.route('/next_hour_data', methods=['GET'])
def get_next_hour_data():
    df = fetch_data_from_mongodb(room_number='Room108')
    df_filled = fill_missing_values(df)
    preds = predict_temperature_pycaret(df_filled, steps=32)

    # Generate timestamps for the next hour with 10-minute frequency
    start_time = df_filled.index[-1] + timedelta(minutes=5)
    timestamps = [start_time + timedelta(minutes=5*i)
                  for i in range(len(preds))]

    # Create a list of dictionaries with timestamps and predicted values
    data_list = [{'timestamp': timestamp.strftime(
        '%Y-%m-%d %H:%M:%S'), 'data': pred} for timestamp, pred in zip(timestamps, preds)]

    return jsonify(data_list)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
