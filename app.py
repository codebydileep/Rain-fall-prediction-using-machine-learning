
from flask import Flask,render_template,url_for,request,jsonify
from flask_cors import cross_origin
import pandas as pd
import numpy as np
import datetime
import pickle
from xgboost import XGBClassifier


app = Flask(__name__, template_folder="template")
model = pickle.load(open("xg_random.pkl", "rb"))
print("Model Loaded")

@app.route("/")
@cross_origin()
def home():
	return render_template("home.html")

@app.route("/predict", methods=['GET', 'POST'])
@cross_origin()
def predict():
    if request.method == "POST":
        # DATE
        date = request.form['date']
        day = float(pd.to_datetime(date, format="%Y-%m-%d").day)
        month = float(pd.to_datetime(date, format="%Y-%m-%d").month)
        # MinTemp
        minTemp = float(request.form['mintemp'])
        # MaxTemp
        maxTemp = float(request.form['maxtemp'])
        # Rainfall
        rainfall = float(request.form['rainfall'])
        # Evaporation
        evaporation = float(request.form['evaporation'])
        # Sunshine
        sunshine = float(request.form['sunshine'])
        # Wind Gust Speed
        windGustSpeed = float(request.form['windgustspeed'])
        # Wind Speed 9am
        windSpeed9am = float(request.form['windspeed9am'])
        # Wind Speed 3pm
        windSpeed3pm = float(request.form['windspeed3pm'])
        # Humidity 9am
        humidity9am = float(request.form['humidity9am'])
        # Humidity 3pm
        humidity3pm = float(request.form['humidity3pm'])
        # Pressure 9am
        pressure9am = float(request.form['pressure9am'])
        # Pressure 3pm
        pressure3pm = float(request.form['pressure3pm'])
        # Temperature 9am
        temp9am = float(request.form['temp9am'])
        # Temperature 3pm
        temp3pm = float(request.form['temp3pm'])
        # Cloud 9am
        cloud9am = float(request.form['cloud9am'])
        # Cloud 3pm
        cloud3pm = float(request.form['cloud3pm'])
        # Location
        location = float(request.form['location'])
        # Wind Dir 9am
        winddDir9am = float(request.form['winddir9am'])
        # Wind Dir 3pm
        winddDir3pm = float(request.form['winddir3pm'])
        # Wind Gust Dir
        windGustDir = float(request.form['windgustdir'])
        # Rain Today
        rainToday = float(request.form['raintoday'])

        input_lst = [location, minTemp, maxTemp, rainfall, evaporation, sunshine,
                     windGustDir, windGustSpeed, winddDir9am, winddDir3pm, windSpeed9am, windSpeed3pm,
                     humidity9am, humidity3pm, pressure9am, pressure3pm, cloud9am, cloud3pm, temp9am, temp3pm,
                     rainToday, month, day]

        # Convert the list to a 2D array with shape (1, 23)
        input_array = np.array(input_lst).reshape(1, -1)

        # Make the prediction
        pred = model.predict(input_array)
        output = pred[0]  # Get the first (and only) prediction result

        if output == 0:
            return render_template("sunny.html")
        else:
            return render_template("rainy.html")
    return render_template("home.html")

if __name__=='__main__':
	app.run(debug=True)