from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS, cross_origin
from flask import Blueprint
from flask_login import login_required, current_user

pred = Blueprint('pred', __name__)

import pickle
import pandas as pd
import numpy as np

model = pickle.load(open('car_pred/LinearModel.pkl', 'rb'))
car = pd.read_csv('car_pred/data/Cleaned_Car.csv')

@pred.route('/predict-price', methods=['GET', 'POST'])
@login_required
def index():
    companies = sorted(car['company'].unique())
    car_models = sorted(car['name'].unique())
    year = sorted(car['year'].unique(), reverse=True)
    fuel_type = car['fuel_type'].unique()

    companies.insert(0, 'Select Company')
    return render_template('index.html', companies=companies, car_models=car_models, years=year, fuel_types=fuel_type, user=current_user)

@pred.route('/predict', methods=['POST'])
@cross_origin()
def predict():
    company = request.form.get('company')
    car_model = request.form.get('car_models')
    year = request.form.get('year')
    fuel_type = request.form.get('fuel_type')
    driven = request.form.get('kilo_driven')

    prediction = model.predict(pd.DataFrame(columns=['name', 'company', 'year', 'kms_driven', 'fuel_type'],
                                            data=np.array([car_model, company, year, driven, fuel_type]).reshape(1, 5)))
    prediction = np.round(prediction[0], 2)

    return render_template('result.html', prediction=prediction, company=company, car_model=car_model, year=year, fuel_type=fuel_type, driven=driven, user=current_user)
