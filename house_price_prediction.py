# House Price Prediction using PySpark
# Complete pipeline for predicting house prices using regression models

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, isnan, count, mean, stddev
from pyspark.sql.types import DoubleType, IntegerType
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.regression import LinearRegression, DecisionTreeRegressor, RandomForestRegressor
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml import Pipeline
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Initialize Spark Session
print("Initializing Spark Session...")
spark = SparkSession.builder \
    .appName("HousePricePrediction") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
    .getOrCreate()

print(f"Spark Version: {spark.version}")

# Load the dataset
print("\n1. Loading Dataset...")
df = spark.read.csv("india_housing_prices.csv", header=True, inferSchema=True)

print(f"Dataset shape: {df.count()} rows, {len(df.columns)} columns")
print("\nDataset Schema:")
df.printSchema()

# Display first few rows
print("\nFirst 5 rows:")
df.show(5, truncate=False)

# Data Exploration and Cleaning
print("\n2. Data Exploration and Cleaning...")

# Check for null values
print("\nNull value counts:")
null_counts = df.select([count(when(col(c).isNull() | isnan(col(c)), c)).alias(c) for c in df.columns])
null_counts.show()

# Basic statistics for numerical columns
print("\nBasic Statistics:")
numerical_cols = ['BHK', 'Size_in_SqFt', 'Price_in_Lakhs', 'Price_per_SqFt', 'Year_Built', 
                  'Floor_No', 'Total_Floors', 'Age_of_Property', 'Nearby_Schools', 'Nearby_Hospitals']
df.select(numerical_cols).describe().show()

# Data Cleaning - Handle missing values and outliers
print("\n3. Data Preprocessing...")

# Remove rows with null values in critical columns
df_clean = df.filter(
    col("Price_in_Lakhs").isNotNull() & 
    col("Size_in_SqFt").isNotNull() & 
    col("BHK").isNotNull()
)

# Remove outliers using IQR method for price
price_stats = df_clean.select(
    mean("Price_in_Lakhs").alias("mean_price"),
    stddev("Price_in_Lakhs").alias("std_price")
).collect()[0]

# Keep prices within 3 standard deviations
price_threshold = price_stats["mean_price"] + 3 * price_stats["std_price"]
df_clean = df_clean.filter(col("Price_in_Lakhs") <= price_threshold)

# Convert categorical variables to numerical using StringIndexer
categorical_cols = ['State', 'City', 'Property_Type', 'Furnished_Status', 'Public_Transport_Accessibility', 
                   'Parking_Space', 'Security', 'Facing', 'Owner_Type', 'Availability_Status']

indexers = [StringIndexer(inputCol=col_name, outputCol=f"{col_name}_indexed", handleInvalid="keep") 
           for col_name in categorical_cols]

# Create pipeline for indexing
indexer_pipeline = Pipeline(stages=indexers)
df_indexed = indexer_pipeline.fit(df_clean).transform(df_clean)

print(f"Cleaned dataset shape: {df_indexed.count()} rows")

# Feature Selection and Engineering
print("\n4. Feature Selection and Engineering...")

# Select features for the model
feature_cols = [
    'BHK', 'Size_in_SqFt', 'Price_per_SqFt', 'Year_Built', 'Floor_No', 'Total_Floors', 
    'Age_of_Property', 'Nearby_Schools', 'Nearby_Hospitals',
    'State_indexed', 'City_indexed', 'Property_Type_indexed', 'Furnished_Status_indexed',
    'Public_Transport_Accessibility_indexed', 'Parking_Space_indexed', 'Security_indexed',
    'Facing_indexed', 'Owner_Type_indexed', 'Availability_Status_indexed'
]

# Create feature vector
assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
df_features = assembler.transform(df_indexed)

# Select final columns for modeling
final_df = df_features.select("features", col("Price_in_Lakhs").alias("label"))

print("Feature vector created successfully!")
print(f"Final dataset for modeling: {final_df.count()} rows")

# Split the dataset
print("\n5. Splitting Dataset...")
train_df, test_df = final_df.randomSplit([0.8, 0.2], seed=42)

print(f"Training set: {train_df.count()} rows")
print(f"Testing set: {test_df.count()} rows")

# Model Training and Evaluation
print("\n6. Training Regression Models...")

# Initialize models
lr = LinearRegression(featuresCol="features", labelCol="label")
dt = DecisionTreeRegressor(featuresCol="features", labelCol="label")
rf = RandomForestRegressor(featuresCol="features", labelCol="label", numTrees=100)

# Train models
print("\nTraining Linear Regression...")
lr_model = lr.fit(train_df)

print("Training Decision Tree Regression...")
dt_model = dt.fit(train_df)

print("Training Random Forest Regression...")
rf_model = rf.fit(train_df)

# Make predictions
print("\n7. Making Predictions...")
lr_predictions = lr_model.transform(test_df)
dt_predictions = dt_model.transform(test_df)
rf_predictions = rf_model.transform(test_df)

# Evaluate models
print("\n8. Model Evaluation...")

evaluator_rmse = RegressionEvaluator(labelCol="label", predictionCol="prediction", metricName="rmse")
evaluator_mae = RegressionEvaluator(labelCol="label", predictionCol="prediction", metricName="mae")
evaluator_r2 = RegressionEvaluator(labelCol="label", predictionCol="prediction", metricName="r2")

# Linear Regression Metrics
lr_rmse = evaluator_rmse.evaluate(lr_predictions)
lr_mae = evaluator_mae.evaluate(lr_predictions)
lr_r2 = evaluator_r2.evaluate(lr_predictions)

# Decision Tree Metrics
dt_rmse = evaluator_rmse.evaluate(dt_predictions)
dt_mae = evaluator_mae.evaluate(dt_predictions)
dt_r2 = evaluator_r2.evaluate(dt_predictions)

# Random Forest Metrics
rf_rmse = evaluator_rmse.evaluate(rf_predictions)
rf_mae = evaluator_mae.evaluate(rf_predictions)
rf_r2 = evaluator_r2.evaluate(rf_predictions)

# Display Results
print("\n" + "="*60)
print("MODEL EVALUATION RESULTS")
print("="*60)

print(f"\nLinear Regression:")
print(f"  RMSE: {lr_rmse:.4f}")
print(f"  MAE:  {lr_mae:.4f}")
print(f"  R²:   {lr_r2:.4f}")

print(f"\nDecision Tree Regression:")
print(f"  RMSE: {dt_rmse:.4f}")
print(f"  MAE:  {dt_mae:.4f}")
print(f"  R²:   {dt_r2:.4f}")

print(f"\nRandom Forest Regression:")
print(f"  RMSE: {rf_rmse:.4f}")
print(f"  MAE:  {rf_mae:.4f}")
print(f"  R²:   {rf_r2:.4f}")

# Determine best model
models_performance = {
    'Linear Regression': {'RMSE': lr_rmse, 'MAE': lr_mae, 'R2': lr_r2},
    'Decision Tree': {'RMSE': dt_rmse, 'MAE': dt_mae, 'R2': dt_r2},
    'Random Forest': {'RMSE': rf_rmse, 'MAE': rf_mae, 'R2': rf_r2}
}

best_model_name = min(models_performance.keys(), key=lambda x: models_performance[x]['RMSE'])
best_model = rf_model if best_model_name == 'Random Forest' else (dt_model if best_model_name == 'Decision Tree' else lr_model)

print(f"\n🏆 Best Model: {best_model_name}")
print(f"   Best RMSE: {models_performance[best_model_name]['RMSE']:.4f}")

# Display sample predictions
print("\n9. Sample Predictions vs Actual Values:")
print("="*60)

if best_model_name == 'Random Forest':
    sample_predictions = rf_predictions
elif best_model_name == 'Decision Tree':
    sample_predictions = dt_predictions
else:
    sample_predictions = lr_predictions

# Show 10 sample predictions
sample_results = sample_predictions.select("label", "prediction").limit(10)
sample_df = sample_results.toPandas()

print("Actual vs Predicted Prices (in Lakhs):")
print("-" * 40)
for i, row in sample_df.iterrows():
    actual = row['label']
    predicted = row['prediction']
    error = abs(actual - predicted)
    print(f"Actual: {actual:8.2f} | Predicted: {predicted:8.2f} | Error: {error:6.2f}")

# Feature Importance (for Random Forest)
if best_model_name == 'Random Forest':
    print(f"\n10. Feature Importance (Random Forest):")
    print("="*50)
    
    feature_importance = rf_model.featureImportances.toArray()
    feature_names = feature_cols
    
    # Create feature importance pairs and sort
    importance_pairs = list(zip(feature_names, feature_importance))
    importance_pairs.sort(key=lambda x: x[1], reverse=True)
    
    print("Top 10 Most Important Features:")
    print("-" * 40)
    for i, (feature, importance) in enumerate(importance_pairs[:10]):
        print(f"{i+1:2d}. {feature:25s}: {importance:.4f}")

# Save the best model
print(f"\n11. Saving the Best Model ({best_model_name})...")
model_path = "best_house_price_model"
best_model.write().overwrite().save(model_path)
print(f"Model saved to: {model_path}")

# Create visualization data
print("\n12. Creating Performance Visualization...")

# Convert sample predictions to pandas for plotting
viz_data = sample_predictions.select("label", "prediction").limit(100).toPandas()

# Create performance comparison chart
plt.figure(figsize=(15, 5))

# Subplot 1: Model Comparison
plt.subplot(1, 3, 1)
models = ['Linear Reg', 'Decision Tree', 'Random Forest']
rmse_values = [lr_rmse, dt_rmse, rf_rmse]
colors = ['skyblue', 'lightgreen', 'lightcoral']

bars = plt.bar(models, rmse_values, color=colors)
plt.title('Model Comparison (RMSE)', fontsize=12, fontweight='bold')
plt.ylabel('RMSE')
plt.xticks(rotation=45)

# Highlight best model
best_idx = rmse_values.index(min(rmse_values))
bars[best_idx].set_color('gold')
bars[best_idx].set_edgecolor('black')
bars[best_idx].set_linewidth(2)

# Add value labels on bars
for i, v in enumerate(rmse_values):
    plt.text(i, v + max(rmse_values)*0.01, f'{v:.2f}', ha='center', va='bottom', fontweight='bold')

# Subplot 2: Actual vs Predicted
plt.subplot(1, 3, 2)
plt.scatter(viz_data['label'], viz_data['prediction'], alpha=0.6, color='blue')
plt.plot([viz_data['label'].min(), viz_data['label'].max()], 
         [viz_data['label'].min(), viz_data['label'].max()], 'r--', lw=2)
plt.xlabel('Actual Price (Lakhs)')
plt.ylabel('Predicted Price (Lakhs)')
plt.title('Actual vs Predicted Prices', fontsize=12, fontweight='bold')

# Subplot 3: R² Comparison
plt.subplot(1, 3, 3)
r2_values = [lr_r2, dt_r2, rf_r2]
bars2 = plt.bar(models, r2_values, color=colors)
plt.title('Model Comparison (R²)', fontsize=12, fontweight='bold')
plt.ylabel('R² Score')
plt.xticks(rotation=45)

# Highlight best R² model
best_r2_idx = r2_values.index(max(r2_values))
bars2[best_r2_idx].set_color('gold')
bars2[best_r2_idx].set_edgecolor('black')
bars2[best_r2_idx].set_linewidth(2)

# Add value labels on bars
for i, v in enumerate(r2_values):
    plt.text(i, v + max(r2_values)*0.01, f'{v:.3f}', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('model_performance_comparison.png', dpi=300, bbox_inches='tight')
plt.show()

# Summary Report
print("\n" + "="*80)
print("HOUSE PRICE PREDICTION - FINAL SUMMARY REPORT")
print("="*80)

print(f"\n📊 Dataset Information:")
print(f"   • Total records processed: {df_indexed.count():,}")
print(f"   • Features used: {len(feature_cols)}")
print(f"   • Training samples: {train_df.count():,}")
print(f"   • Testing samples: {test_df.count():,}")

print(f"\n🏆 Best Performing Model: {best_model_name}")
print(f"   • RMSE: {models_performance[best_model_name]['RMSE']:.4f} Lakhs")
print(f"   • MAE:  {models_performance[best_model_name]['MAE']:.4f} Lakhs")
print(f"   • R²:   {models_performance[best_model_name]['R2']:.4f}")

print(f"\n💾 Model Artifacts:")
print(f"   • Best model saved to: {model_path}")
print(f"   • Performance chart saved: model_performance_comparison.png")

print(f"\n🎯 Model Interpretation:")
if models_performance[best_model_name]['R2'] > 0.8:
    print("   • Excellent model performance (R² > 0.8)")
elif models_performance[best_model_name]['R2'] > 0.6:
    print("   • Good model performance (R² > 0.6)")
elif models_performance[best_model_name]['R2'] > 0.4:
    print("   • Moderate model performance (R² > 0.4)")
else:
    print("   • Model needs improvement (R² < 0.4)")

print(f"\n✅ Pipeline completed successfully!")
print("="*80)

# Stop Spark Session
spark.stop()