# House Price Prediction - Simplified Version
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt

print("House Price Prediction Pipeline")
print("="*50)

# Load dataset
print("\n1. Loading Dataset...")
df = pd.read_csv("india_housing_prices.csv")
print(f"Dataset shape: {df.shape}")

# Data cleaning
print("\n2. Data Cleaning...")
df_clean = df.dropna(subset=['Price_in_Lakhs', 'Size_in_SqFt', 'BHK'])

# Feature selection
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

print(f"Features used: {len(feature_cols)}")
print(f"Samples: {len(X)}")

# Split data
print("\n3. Splitting Data...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Training: {len(X_train)}, Testing: {len(X_test)}")

# Train models
print("\n4. Training Models...")
models = {
    'Linear Regression': LinearRegression(),
    'Decision Tree': DecisionTreeRegressor(random_state=42),
    'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42)
}

results = {}
predictions = {}

for name, model in models.items():
    print(f"Training {name}...")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    results[name] = {'RMSE': rmse, 'MAE': mae, 'R2': r2}
    predictions[name] = y_pred

# Display results
print("\n5. Model Evaluation Results")
print("="*60)
for name, metrics in results.items():
    print(f"\n{name}:")
    print(f"  RMSE: {metrics['RMSE']:.4f}")
    print(f"  MAE:  {metrics['MAE']:.4f}")
    print(f"  R²:   {metrics['R2']:.4f}")

# Best model
best_model = min(results.keys(), key=lambda x: results[x]['RMSE'])
print(f"\nBest Model: {best_model}")

# Sample predictions
print(f"\n6. Sample Predictions ({best_model}):")
print("-" * 40)
sample_indices = np.random.choice(len(y_test), 10, replace=False)
for i in sample_indices:
    actual = y_test.iloc[i]
    predicted = predictions[best_model][i]
    print(f"Actual: {actual:8.2f} | Predicted: {predicted:8.2f}")

# Visualization
print("\n7. Creating Visualizations...")
plt.figure(figsize=(15, 5))

# Model comparison
plt.subplot(1, 3, 1)
models_list = list(results.keys())
rmse_values = [results[m]['RMSE'] for m in models_list]
plt.bar(models_list, rmse_values, color=['skyblue', 'lightgreen', 'lightcoral'])
plt.title('Model Comparison (RMSE)')
plt.ylabel('RMSE')
plt.xticks(rotation=45)

# Actual vs Predicted
plt.subplot(1, 3, 2)
best_pred = predictions[best_model]
plt.scatter(y_test, best_pred, alpha=0.6)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('Actual Price')
plt.ylabel('Predicted Price')
plt.title(f'Actual vs Predicted ({best_model})')

# R² comparison
plt.subplot(1, 3, 3)
r2_values = [results[m]['R2'] for m in models_list]
plt.bar(models_list, r2_values, color=['skyblue', 'lightgreen', 'lightcoral'])
plt.title('Model Comparison (R²)')
plt.ylabel('R² Score')
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig('model_performance.png', dpi=300, bbox_inches='tight')
plt.show()

print(f"\nPipeline completed successfully!")
print(f"Best model RMSE: {results[best_model]['RMSE']:.4f}")
print(f"Visualization saved: model_performance.png")