import numpy as np
import pickle
import joblib
import matplotlib
import matplotlib.pyplot as plt
import time
import pandas
import os
from flask import Flask, request, jsonify, render_template
import json

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "9417L-N8ej71KwqkN_GQdwUO5hFeBAOJO0FasObjrJ_t"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
#payload_scoring = {"input_data": [{"fields": [array_of_input_fields], "values": [array_of_values_to_be_scored, another_array_of_values_to_be_scored]}]}

#response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/8e16b491-9bb5-40c2-9ded-a3094b4de776/predictions?version=2021-11-10', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
#print("Scoring response")
#print(response_scoring.json())


app = Flask(__name__)


@app.route('/')# route to display the home page
def home():
    return render_template('index.html') #rendering the home page

@app.route('/predict',methods=["POST","GET"])# route to show the predictions in a web UI
def predict():
    #  reading the inputs given by the user
    Location = request.form["Location"]
    MinTemp = request.form["MinTemp"]
    MaxTemp = request.form["MaxTemp"]
    Rainfall = request.form["Rainfall"]
    WindGustSpeed = request.form["WindGustSpeed"]
    WindSpeed9am = request.form["WindSpeed9am"]
    WindSpeed3pm = request.form["WindSpeed3pm"]
    Humidity9am = request.form["Humidity9am"]
    Humidity3pm = request.form["Humidity3pm"]
    Pressure9am = request.form["Pressure9am"]
    Pressure3pm = request.form["Pressure3pm"]
    Temp9am = request.form["Temp9am"]
    Temp3pm = request.form["Temp3pm"]
    RainToday = request.form["RainToday"]
    WindGustDir = request.form["WindGustDir"]
    WindDir9am = request.form["WindDir9am"]
    WindDir3pm = request.form["WindDir3pm"]
    t = [[int(Location),int(MinTemp),int(MaxTemp),int(Rainfall),
          int(WindGustSpeed),int(WindSpeed9am),int(WindSpeed3pm),int(Humidity9am),int(Humidity3pm),
          int(Pressure9am),int(Pressure3pm),int(Temp9am),int(Temp3pm),int(RainToday),
          int(WindGustDir),int(WindDir9am),int(WindDir3pm)]]
    payload_scoring = {"input_data": [{"field": [['Location', 'MinTemp', 'MaxTemp', 'Rainfall', 'WindGustSpeed',
       'WindSpeed9am', 'WindSpeed3pm', 'Humidity9am', 'Humidity3pm',
       'Pressure9am', 'Pressure3pm', 'Temp9am', 'Temp3pm', 'RainToday',
       'WindGustDir', 'WindDir9am', 'WindDir3pm']], "values": t}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/31b8a4af-295b-4f63-8af1-935bf55cd75b/predictions?version=2022-03-05', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions = response_scoring.json()
    pred = predictions['predictions'][0]['values'][0][0]
    if(pred=="Yes"):
        
        return render_template('chance.html')
    else:
     # predictions using the loaded model file
        return render_template('nochance.html')
     # showing the prediction results in a UI
if __name__=="__main__":
    
    # app.run(host='0.0.0.0', port=8000,debug=True)    # running the app
    port=int(os.environ.get('PORT',5000))
    app.run(port=port,debug=True,use_reloader=False)