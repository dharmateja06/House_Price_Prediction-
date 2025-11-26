from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import pickle
import os

app = Flask(__name__)

# Load and train model on startup
def load_model():
    df = pd.read_csv("india_housing_prices.csv")
    df_clean = df.dropna(subset=['Price_in_Lakhs', 'Size_in_SqFt', 'BHK'])
    
    numerical_features = ['BHK', 'Size_in_SqFt', 'Price_per_SqFt', 'Year_Built', 
                         'Floor_No', 'Total_Floors', 'Age_of_Property', 
                         'Nearby_Schools', 'Nearby_Hospitals']
    
    categorical_features = ['State', 'Property_Type', 'Furnished_Status', 
                           'Public_Transport_Accessibility', 'Parking_Space', 
                           'Security', 'Facing', 'Owner_Type', 'Availability_Status']
    
    # Encode categorical variables
    le_dict = {}
    for col in categorical_features:
        if col in df_clean.columns:
            le = LabelEncoder()
            df_clean[col + '_encoded'] = le.fit_transform(df_clean[col].astype(str))
            le_dict[col] = le
    
    # Prepare features
    feature_cols = [col for col in numerical_features if col in df_clean.columns]
    feature_cols += [col + '_encoded' for col in categorical_features if col in df_clean.columns]
    
    X = df_clean[feature_cols].fillna(0)
    y = df_clean['Price_in_Lakhs']
    
    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    return model, le_dict, feature_cols, df_clean

# Load model and encoders
model, encoders, feature_columns, data = load_model()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        form_data = request.form.to_dict()
        
        # Create feature vector
        features = {}
        
        # Numerical features
        features['BHK'] = float(form_data.get('bhk', 2))
        features['Size_in_SqFt'] = float(form_data.get('size', 1000))
        features['Year_Built'] = float(form_data.get('year_built', 2010))
        features['Floor_No'] = float(form_data.get('floor_no', 1))
        features['Total_Floors'] = float(form_data.get('total_floors', 5))
        features['Age_of_Property'] = 2024 - features['Year_Built']
        features['Nearby_Schools'] = float(form_data.get('nearby_schools', 5))
        features['Nearby_Hospitals'] = float(form_data.get('nearby_hospitals', 3))
        features['Price_per_SqFt'] = 0.1  # Default value
        
        # Categorical features
        categorical_inputs = {
            'State': form_data.get('state', 'Maharashtra'),
            'Property_Type': form_data.get('property_type', 'Apartment'),
            'Furnished_Status': form_data.get('furnished_status', 'Semi-furnished'),
            'Public_Transport_Accessibility': form_data.get('transport', 'Medium'),
            'Parking_Space': form_data.get('parking', 'Yes'),
            'Security': form_data.get('security', 'Yes'),
            'Facing': form_data.get('facing', 'North'),
            'Owner_Type': form_data.get('owner_type', 'Owner'),
            'Availability_Status': form_data.get('availability', 'Ready_to_Move')
        }
        
        # Encode categorical features
        for col, value in categorical_inputs.items():
            if col in encoders:
                try:
                    encoded_value = encoders[col].transform([value])[0]
                except:
                    encoded_value = 0  # Default for unknown categories
                features[col + '_encoded'] = encoded_value
        
        # Create feature array in correct order
        feature_array = []
        for col in feature_columns:
            feature_array.append(features.get(col, 0))
        
        # Make prediction
        prediction = model.predict([feature_array])[0]
        
        return jsonify({
            'success': True,
            'prediction': round(prediction, 2),
            'message': f'Predicted house price: ₹{prediction:.2f} Lakhs'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Error in prediction. Please check your inputs.'
        })

@app.route('/api/options')
def get_options():
    """Get unique values for dropdown options"""
    options = {}
    
    categorical_cols = ['State', 'Property_Type', 'Furnished_Status', 
                       'Public_Transport_Accessibility', 'Parking_Space', 
                       'Security', 'Facing', 'Owner_Type', 'Availability_Status']
    
    for col in categorical_cols:
        if col in data.columns:
            options[col] = sorted(data[col].unique().tolist())
    
    return jsonify(options)

if __name__ == '__main__':
    app.run(debug=True)