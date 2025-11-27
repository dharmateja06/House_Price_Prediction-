import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

def train_bengaluru_model():
    # Load main dataset and filter for Bengaluru
    df = pd.read_csv("india_housing_prices.csv")
    bengaluru_data = df[df['City'].str.contains('Bangalore', case=False, na=False)].copy()
    
    if len(bengaluru_data) == 0:
        # If no Bangalore data, create sample data
        bengaluru_data = df.sample(n=min(5000, len(df))).copy()
        bengaluru_data['City'] = 'Bangalore'
    
    # Clean data
    bengaluru_data = bengaluru_data.dropna(subset=['Price_in_Lakhs', 'Size_in_SqFt', 'BHK'])
    
    # Features for Bengaluru model
    numerical_features = ['BHK', 'Size_in_SqFt', 'Year_Built', 'Floor_No', 'Total_Floors', 
                         'Age_of_Property', 'Nearby_Schools', 'Nearby_Hospitals']
    
    categorical_features = ['Property_Type', 'Furnished_Status', 'Locality',
                           'Public_Transport_Accessibility', 'Parking_Space', 'Security']
    
    # Encode categorical variables
    le_dict = {}
    for col in categorical_features:
        if col in bengaluru_data.columns:
            le = LabelEncoder()
            bengaluru_data[col + '_encoded'] = le.fit_transform(bengaluru_data[col].astype(str))
            le_dict[col] = le
    
    # Prepare features
    feature_cols = [col for col in numerical_features if col in bengaluru_data.columns]
    feature_cols += [col + '_encoded' for col in categorical_features if col in bengaluru_data.columns]
    
    X = bengaluru_data[feature_cols].fillna(0)
    y = bengaluru_data['Price_in_Lakhs']
    
    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    return model, le_dict, feature_cols, bengaluru_data

def predict_bengaluru_price(model, encoders, feature_columns, input_data):
    features = {}
    
    # Numerical features
    features['BHK'] = float(input_data.get('bhk', 2))
    features['Size_in_SqFt'] = float(input_data.get('size', 1000))
    features['Year_Built'] = float(input_data.get('year_built', 2010))
    features['Floor_No'] = float(input_data.get('floor_no', 1))
    features['Total_Floors'] = float(input_data.get('total_floors', 5))
    features['Age_of_Property'] = 2024 - features['Year_Built']
    features['Nearby_Schools'] = float(input_data.get('nearby_schools', 5))
    features['Nearby_Hospitals'] = float(input_data.get('nearby_hospitals', 3))
    
    # Categorical features
    categorical_inputs = {
        'Property_Type': input_data.get('property_type', 'Apartment'),
        'Furnished_Status': input_data.get('furnished_status', 'Semi-furnished'),
        'Locality': input_data.get('locality', 'Koramangala'),
        'Public_Transport_Accessibility': input_data.get('transport', 'High'),
        'Parking_Space': input_data.get('parking', 'Yes'),
        'Security': input_data.get('security', 'Yes')
    }
    
    # Encode categorical features
    for col, value in categorical_inputs.items():
        if col in encoders:
            try:
                encoded_value = encoders[col].transform([value])[0]
            except:
                encoded_value = 0
            features[col + '_encoded'] = encoded_value
    
    # Create feature array
    feature_array = [features.get(col, 0) for col in feature_columns]
    
    # Make prediction
    prediction = model.predict([feature_array])[0]
    return prediction