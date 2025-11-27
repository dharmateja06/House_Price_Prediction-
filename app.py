from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO
import json
from bengaluru_model import train_bengaluru_model, predict_bengaluru_price

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
bengaluru_model, bengaluru_encoders, bengaluru_features, bengaluru_data = train_bengaluru_model()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/data')
def view_data():
    return render_template('data.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/bengaluru')
def bengaluru():
    return render_template('bengaluru.html')

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

@app.route('/predict_bengaluru', methods=['POST'])
def predict_bengaluru():
    try:
        form_data = request.form.to_dict()
        prediction = predict_bengaluru_price(bengaluru_model, bengaluru_encoders, bengaluru_features, form_data)
        
        return jsonify({
            'success': True,
            'prediction': round(prediction, 2),
            'message': f'Predicted Bengaluru house price: ₹{prediction:.2f} Lakhs'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Error in Bengaluru prediction. Please check your inputs.'
        })

@app.route('/api/data')
def get_data():
    """Get paginated data for table view"""
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 50))
    
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    # Get subset of data
    subset = data.iloc[start_idx:end_idx]
    
    return jsonify({
        'data': subset.to_dict('records'),
        'total': len(data),
        'page': page,
        'per_page': per_page,
        'total_pages': (len(data) + per_page - 1) // per_page
    })

@app.route('/api/analytics')
def get_analytics():
    """Generate analytics charts"""
    charts = {}
    
    # Price distribution
    plt.figure(figsize=(10, 6))
    plt.hist(data['Price_in_Lakhs'], bins=50, alpha=0.7, color='skyblue')
    plt.title('Price Distribution')
    plt.xlabel('Price (Lakhs)')
    plt.ylabel('Frequency')
    charts['price_dist'] = get_plot_url()
    
    # Price by State
    plt.figure(figsize=(12, 6))
    state_prices = data.groupby('State')['Price_in_Lakhs'].mean().sort_values(ascending=False).head(10)
    state_prices.plot(kind='bar', color='lightcoral')
    plt.title('Average Price by State (Top 10)')
    plt.xlabel('State')
    plt.ylabel('Average Price (Lakhs)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    charts['price_by_state'] = get_plot_url()
    
    # BHK vs Price
    plt.figure(figsize=(10, 6))
    bhk_prices = data.groupby('BHK')['Price_in_Lakhs'].mean()
    bhk_prices.plot(kind='bar', color='lightgreen')
    plt.title('Average Price by BHK')
    plt.xlabel('BHK')
    plt.ylabel('Average Price (Lakhs)')
    charts['bhk_vs_price'] = get_plot_url()
    
    # Property Type Distribution
    plt.figure(figsize=(8, 8))
    property_counts = data['Property_Type'].value_counts()
    plt.pie(property_counts.values, labels=property_counts.index, autopct='%1.1f%%')
    plt.title('Property Type Distribution')
    charts['property_type_dist'] = get_plot_url()
    
    return jsonify(charts)

@app.route('/api/bengaluru_localities')
def get_bengaluru_localities():
    """Get Bengaluru localities for dropdown"""
    localities = ['Koramangala', 'Indiranagar', 'Whitefield', 'Electronic City', 'HSR Layout', 
                 'Marathahalli', 'Sarjapur Road', 'Bannerghatta Road', 'Hebbal', 'Yeshwanthpur']
    return jsonify(localities)

def get_plot_url():
    """Convert matplotlib plot to base64 string"""
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return plot_url

if __name__ == '__main__':
    app.run(debug=True, port=5000)