
from flask import request, Flask, render_template, jsonify
from flask_restful import Resource, Api
import csv, json, os, shutil, time, calendar
from datetime import datetime
from weather import Weather
weather = Weather()

myapp = Flask(__name__)
api = Api(myapp)

@myapp.route('/')
def main():
    return render_template('try2.html')

@myapp.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@myapp.route('/forecast/<date>', methods=['GET'])
def forecast(date):
    temp_date = date.replace("-","")
    fl = []
    with open('daily.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        count=0
        for row in reader:
            if(row['DATE']==temp_date or (count>0 and count<6)):
                fl.append({"DATE":row['DATE'], "TMAX":row['TMAX'], "TMIN":row['TMIN']})
                count = count+1
        
          


    if count<5:
        lookup = weather.lookup(560743)
        location = weather.lookup_by_location('cincinnati')
        forecasts = location.forecast()
        for forecast in forecasts:
            count=count+1
            if(count >5):
                break
            fl.append({"DATE":str(forecast.date()), "TMAX":float(forecast.high()), "TMIN":float(forecast.low())})
    

    return json.dumps(fl)
