import sklearn
# from sklearn.naive_bayes import GaussianNB
import pickle
import numpy as np
import pandas as pd
from flask_cors import CORS, cross_origin
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from crop_details import crop_details


from flask import Flask
from flask import render_template, abort, jsonify, request, redirect, json


# Open the file in binary mode
with open('crop_recommendation.pkl', 'rb') as file:
    # Call load method to deserialze
    model = pickle.load(file)

with open('fertilizer_Prediction-1.pkl', 'rb') as file:
    # Call load method to deserialze
    fertilizer_model_1 = pickle.load(file)

with open('fertilizer_Prediction-2.pkl', 'rb') as file:
    # Call load method to deserialze
    fertilizer_model_2 = pickle.load(file)

with open('fertilizer_Prediction-3.pkl', 'rb') as file:
    # Call load method to deserialze
    fertilizer_model_3 = pickle.load(file)

# encoding the label with the help of prebuilt model from pickle file "encoding_model.pkl"
with open('encoding_model.pkl', 'rb') as file:
    encoding_model = pickle.load(file)

with open('totalNutrients_model.pkl', 'rb') as file:
    totalNutrients_calculation_model = pickle.load(file)

app = Flask(__name__)
app.debug = True


@app.route('/')
@app.route('/Home.html')
def Home():
    return render_template('/Home.html')


@app.route('/crop-recommedation.html')
def crop_recommedation():
    return render_template('crop-recommedation.html')


@app.route('/crop-price.html')
def crop_price():
    return render_template('crop-price.html')


@app.route('/Fertilizer.html')
def Fertilizer():
    return render_template('Fertilizer.html')


@app.route('/Contact.html')
def Contact():
    return render_template('Contact.html')


@app.route('/predict', methods=['POST', 'get'])
@cross_origin()
def predict():
    try:
        # Get the data from the POST request
        # print("Ayuush")
        nitrogen = float(request.form.get('nitrogen'))
        print(nitrogen)
        phosphorous = float(request.form.get('phosphorous'))
        print(phosphorous)
        potassium = float(request.form.get('potassium'))
        print(potassium)
        temperature = float(request.form.get('temperature'))
        print(temperature)
        humidity = float(request.form.get('humidity'))
        print(humidity)
        pH = float(request.form.get('pH'))
        print(pH)
        rainfall = float(request.form.get('rainfall'))
        print(rainfall)

        data = np.array([nitrogen, phosphorous, potassium,
                        temperature, humidity, pH, rainfall]).reshape(1, 7)
        # Make prediction using the loaded model

        prediction = model.predict(data)
        prediction = prediction[0]

        return render_template("/prediction.html", prediction=prediction, suitable_time=crop_details[prediction]['suitable_time'], grow_techniques=crop_details[prediction]['grow_techniques'], fertilizer_details=crop_details[prediction]['fertilizer_details'], water_requirements=crop_details[prediction]['water_requirements'], yield_produce=crop_details[prediction]['yield_produce'])

    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/fertilizer_prediction', methods=['POST', 'get'])
@cross_origin()
def fertilizer_predict():
    try:
        # Get the data from the POST request
        # print("Ayuush")
        nitrogen = float(request.form.get('nitrogen'))
        print(nitrogen)
        phosphorous = float(request.form.get('phosphorous'))
        print(phosphorous)
        potassium = float(request.form.get('potassium'))
        print(potassium)
        temperature = float(request.form.get('temperature'))
        print(temperature)
        humidity = float(request.form.get('humidity'))
        print(humidity)
        pH = float(request.form.get('pH'))
        print(pH)
        rainfall = float(request.form.get('rainfall'))
        print(rainfall)
        crop = request.form.get('crop')
        print(crop)

        Encoded__crop_label = encoding_model.transform(
            pd.Series(crop).values.reshape(-1, 1))
        print(Encoded__crop_label)
        Required_NPK_array = totalNutrients_calculation_model.predict(
            Encoded__crop_label)
        Required_NPK_array = [
            np.round_(Required_NPK_array[:, :], decimals=0, out=None)]
        print(Required_NPK_array)

        total_N = Required_NPK_array[0][0][0]
        total_P = Required_NPK_array[0][0][1]
        total_K = Required_NPK_array[0][0][2]

        req_N = total_N - nitrogen
        req_P = total_P - phosphorous
        req_K = total_K - potassium

        final_input_array = [nitrogen, phosphorous, potassium, temperature,
                             humidity, pH, rainfall, total_N, total_P, total_K, req_N, req_P, req_K]
        final_input_array = np.array(final_input_array)

        # Make prediction using the loaded model
        fertilizer_1_prediction = fertilizer_model_1.predict(
            final_input_array.reshape(1, -1))[0]
        fertilizer_2_prediction = fertilizer_model_2.predict(
            final_input_array.reshape(1, -1))[0]
        fertilizer_3_prediction = fertilizer_model_3.predict(
            final_input_array.reshape(1, -1))[0]

        fertilizer_1_prediction = map(
            lambda n: "%.2f" % n, fertilizer_1_prediction)
        fertilizer_2_prediction = map(
            lambda n: "%.2f" % n, fertilizer_2_prediction)
        fertilizer_3_prediction = map(
            lambda n: "%.2f" % n, fertilizer_3_prediction)

        # Output_template
        columns1 = ['Urea-1', 'SSP-1', 'MOP-1',
                    'SOP-1', 'Potassium Nitrate-1', 'DAP-1']
        columns2 = ['Urea-2', 'SSP-2', 'MOP-2',
                    'SOP-2', 'Potassium Nitrate-2', 'DAP-2']
        columns3 = ['Urea-3', 'SSP-3', 'MOP-3',
                    'SOP-3', 'Potassium Nitrate-3', 'DAP-3']

        recommended_fertilizer_1 = dict(zip(columns1, fertilizer_1_prediction))
        recommended_fertilizer_2 = dict(zip(columns2, fertilizer_2_prediction))
        recommended_fertilizer_3 = dict(zip(columns3, fertilizer_3_prediction))

        print(recommended_fertilizer_1)
        print(recommended_fertilizer_2)
        print(recommended_fertilizer_3)

        final_recommendation = {
            "Fertilizer-Recommendtion-1": recommended_fertilizer_1,
            "Fertilizer-Recommendtion-2": recommended_fertilizer_2,
            "Fertilizer-Recommendtion-3": recommended_fertilizer_3
        }

        print(recommended_fertilizer_1['Urea-1'])

        return render_template("/know_your_fertilizer.html", urea_1=recommended_fertilizer_1['Urea-1'], ssp_1=recommended_fertilizer_1['SSP-1'], mop_1=recommended_fertilizer_1['MOP-1'], sop_1=recommended_fertilizer_1['SOP-1'], potassium_1=recommended_fertilizer_1['Potassium Nitrate-1'], dap_1=recommended_fertilizer_1['DAP-1'], urea_2=recommended_fertilizer_2['Urea-2'], ssp_2=recommended_fertilizer_2['SSP-2'], mop_2=recommended_fertilizer_2['MOP-2'], sop_2=recommended_fertilizer_2['SOP-2'], potassium_2=recommended_fertilizer_2['Potassium Nitrate-2'], dap_2=recommended_fertilizer_2['DAP-2'], urea_3=recommended_fertilizer_3['Urea-3'], ssp_3=recommended_fertilizer_3['SSP-3'], mop_3=recommended_fertilizer_3['MOP-3'], sop_3=recommended_fertilizer_3['SOP-3'], potassium_3=recommended_fertilizer_3['Potassium Nitrate-3'], dap_3=recommended_fertilizer_3['DAP-3'])

    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(port=8000, debug=True)
