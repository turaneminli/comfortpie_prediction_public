# Comfort Pie - IoT Temperature Prediction Service

The repository contains a Flask-based IoT application for Comfort Pie project that predicts future temperatures based on historical data collected from IoT devices. The application utilizes the ARIMA time series model from the `statsmodels` library and the `pycaret` library for streamlined machine learning.

## Features

- **Temperature Prediction:** Utilizes ARIMA time series model to predict temperatures.
- **Data Collection:** Gathers real-time temperature data from IoT devices connected to a MongoDB database.
- **Data Preprocessing:** Fills missing values and resamples data for accurate predictions.
- **API Endpoint:** Provides a Flask API endpoint `/next_hour_data` to retrieve temperature predictions for the next hour.

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/turaneminli/comfortpie_prediction_public.git
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   You can also do it in the virtual environment, which is recommended.

3. Set up MongoDB:

   - Configure MongoDB connection in `app.py` with your MongoDB credentials. Furthermore, if you would like to check, jupyter notebook you should change the MongoDB connection as well.

4. Run the Flask app:

   ```bash
   python app.py
   ```

5. Access temperature predictions:
   - Open [http://localhost:5000/next_hour_data](http://localhost:5000/next_hour_data) to get predictions for the next hour.

## Configuration

- Adjust MongoDB credentials and IoT device settings (if you have) in `app.py`.

## Dependencies

- Flask
- statsmodels
- pandas
- pymongo
- pycaret
- flask_cors
