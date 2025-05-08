from flask import Flask, request, render_template
from sklearn.linear_model import LogisticRegression
import pickle
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prediction', methods=['POST'])
def prediction():
            vehicle_model = request.form['Vehicle_Model']
            if vehicle_model.lower() == 'bus':
                vehicle_model_val = '0'
            elif vehicle_model.lower() == 'car':
                vehicle_model_val = '1'
            elif vehicle_model.lower() == 'motorcycle':
                vehicle_model_val = '2'
            elif vehicle_model.lower() == 'suv':
                vehicle_model_val = '3'
            elif vehicle_model.lower() == 'truck':
                vehicle_model_val = '4'
            else:
                vehicle_model_val = '5'

            reported_issues = float(request.form['Reported_Issues'])
            vehicle_age = float(request.form['Vehicle_Age'])
            
            fuel_type = request.form['Fuel_Type']
            if fuel_type.lower() == 'electric':
                fuel_type_val = '1'
            elif fuel_type.lower() == 'petrol':
                fuel_type_val = '2'
            else:
                fuel_type_val = '3'
            
            transmission_type = request.form['Transmission_Type']
            if transmission_type.lower() == 'manual':
                transmission_type_val = '1'
            else:
                transmission_type_val = '0'
            
            fuel_efficiency = float(request.form.get('Fuel_Efficiency', 0))
            days_since_last_service = float(request.form.get('Days_Since_Last_Service', 0))

            maintenance_history = request.form['Maintenance_History']
            if maintenance_history.lower() == 'average':
                maintenance_history_good = '0'
                maintenance_history_average = '1'
                maintenance_history_poor = '0'
            elif maintenance_history.lower() == 'good':
                maintenance_history_good = '1'
                maintenance_history_average = '0'
                maintenance_history_poor = '0'
            elif maintenance_history.lower() == 'poor':
                maintenance_history_good = '0'
                maintenance_history_average = '0'
                maintenance_history_poor = '1'
            else:
                maintenance_history_good = '0'
                maintenance_history_average = '0'
                maintenance_history_poor = '0' 
            
            tire_condition = request.form['Tire_Condition']
            if tire_condition.lower() == 'good':
                tire_condition_good = '1'
                tire_condition_new = '0'
                tire_condition_worn_out = '0'
            elif tire_condition.lower() == 'new':
                tire_condition_good = '0'
                tire_condition_new = '1'
                tire_condition_worn_out = '0'
            elif tire_condition.lower() == 'worn out':
                tire_condition_good = '0'
                tire_condition_new = '0'
                tire_condition_worn_out = '1'
            else:
                tire_condition_good = '0'
                tire_condition_new = '0'
                tire_condition_worn_out = '0'
            
            brake_condition = request.form['Brake_Condition']
            if brake_condition.lower() == 'good':
                brake_condition_good = '1'
                brake_condition_new = '0'
                brake_condition_worn_out = '0'
            elif brake_condition.lower() == 'new':
                brake_condition_good = '0'
                brake_condition_new = '1'
                brake_condition_worn_out = '0'
            elif brake_condition.lower() == 'worn out':
                brake_condition_good = '0'
                brake_condition_new = '0'
                brake_condition_worn_out = '1'
            else:
                brake_condition_good = '0'
                brake_condition_new = '0'
                brake_condition_worn_out = '0'
            
            battery_status = request.form.get('Battery_Status')
            if battery_status.lower() == 'good':
                battery_status_good = '1'
                battery_status_new = '0'
                battery_status_weak = '0'
            elif battery_status.lower() == 'new':
                battery_status_good = '0'
                battery_status_new = '1'
                battery_status_weak = '0'
            elif battery_status.lower() == 'weak':
                battery_status_good = '0'
                battery_status_new = '0'
                battery_status_weak = '1'
            else:
                battery_status_good = '0'
                battery_status_new = '0'
                battery_status_weak = '0'
        

            # Create the input array
            input_data = np.array([
                vehicle_model_val, reported_issues, vehicle_age, fuel_type_val, transmission_type_val, 
                fuel_efficiency, days_since_last_service, maintenance_history_average, 
                maintenance_history_good, maintenance_history_poor, tire_condition_good, 
                tire_condition_new, tire_condition_worn_out, brake_condition_good, 
                brake_condition_new, brake_condition_worn_out, battery_status_good, 
                battery_status_new, battery_status_weak
            ])

            # Reshape the input data array to a 2D array with a single sample
            input_data = input_data.reshape(1, -1)
            
            # Load the logistic regression model
            loaded_model = pickle.load(open('logregmodel.pkl', 'rb'))
            # Predict using the loaded model
            prediction = loaded_model.predict(input_data)[0]

            if prediction == 1:
                result = "Yes, the vehicle needs maintenance"
            else:
                result = "No, the vehicle does not need maintenance"

            return render_template('index.html', prediction_text=result)

if __name__ == '__main__':
    app.run(debug=True)