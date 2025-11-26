# House Price Prediction using PySpark

A comprehensive machine learning pipeline built with PySpark for predicting house prices using the Indian housing dataset.

## 🎯 Project Overview

This project implements a complete end-to-end machine learning pipeline using PySpark to predict house prices based on various property attributes. The pipeline includes data cleaning, feature engineering, model training, evaluation, and comparison of multiple regression algorithms.

## 📊 Dataset

The project uses the `india_housing_prices.csv` dataset containing the following features:

### Key Features:
- **Property Details**: BHK, Size_in_SqFt, Property_Type, Year_Built, Age_of_Property
- **Location**: State, City, Locality
- **Amenities**: Furnished_Status, Parking_Space, Security, Amenities
- **Infrastructure**: Nearby_Schools, Nearby_Hospitals, Public_Transport_Accessibility
- **Building Info**: Floor_No, Total_Floors, Facing
- **Market Info**: Owner_Type, Availability_Status
- **Target**: Price_in_Lakhs (house price)

## 🚀 Features

### Data Processing:
- ✅ Comprehensive data cleaning and preprocessing
- ✅ Null value handling and outlier removal
- ✅ Categorical variable encoding using StringIndexer
- ✅ Feature vector assembly using VectorAssembler

### Machine Learning Models:
- ✅ Linear Regression
- ✅ Decision Tree Regression  
- ✅ Random Forest Regression

### Evaluation Metrics:
- ✅ Root Mean Square Error (RMSE)
- ✅ Mean Absolute Error (MAE)
- ✅ R² Score (Coefficient of Determination)

### Visualization & Analysis:
- ✅ Model performance comparison charts
- ✅ Actual vs Predicted price scatter plots
- ✅ Feature importance analysis (Random Forest)
- ✅ Comprehensive summary report

## 🛠️ Installation

### Prerequisites:
- Python 3.8+
- Java 8 or 11 (required for PySpark)

### Setup:
1. Clone or download the project files
2. Install required dependencies:
```bash
pip install -r requirements.txt
```

### Alternative Installation:
```bash
pip install pyspark matplotlib seaborn pandas numpy
```

## 📁 Project Structure

```
House_price_prediction/
│
├── house_price_prediction.py    # Main PySpark pipeline
├── india_housing_prices.csv     # Dataset
├── requirements.txt             # Dependencies
├── README.md                   # Project documentation
│
└── Generated Files:
    ├── best_house_price_model/     # Saved best model
    └── model_performance_comparison.png  # Performance charts
```

## 🏃‍♂️ How to Run

1. **Ensure Java is installed** (required for PySpark):
   ```bash
   java -version
   ```

2. **Run the main pipeline**:
   ```bash
   python house_price_prediction.py
   ```

3. **Expected Output**:
   - Data loading and exploration statistics
   - Data cleaning and preprocessing steps
   - Model training progress for all three algorithms
   - Comprehensive evaluation metrics
   - Best model selection and saving
   - Performance visualization charts
   - Final summary report

## 📈 Pipeline Workflow

### 1. Data Loading & Exploration
- Load CSV dataset using PySpark
- Display schema and basic statistics
- Analyze data distribution and null values

### 2. Data Cleaning & Preprocessing
- Remove null values in critical columns
- Handle outliers using statistical methods
- Convert categorical variables to numerical indices

### 3. Feature Engineering
- Select relevant features for modeling
- Create feature vectors using VectorAssembler
- Split data into training (80%) and testing (20%) sets

### 4. Model Training
- Train three regression models in parallel
- Linear Regression for baseline performance
- Decision Tree for non-linear relationships
- Random Forest for ensemble learning

### 5. Model Evaluation
- Calculate RMSE, MAE, and R² for each model
- Compare model performances
- Select best performing model based on RMSE

### 6. Results & Visualization
- Generate performance comparison charts
- Display sample predictions vs actual values
- Show feature importance (for Random Forest)
- Save best model for future use

## 📊 Expected Results

The pipeline typically achieves:
- **Random Forest**: Best overall performance with lowest RMSE
- **Decision Tree**: Good performance with interpretability
- **Linear Regression**: Baseline performance for comparison

### Sample Output:
```
MODEL EVALUATION RESULTS
========================================
Linear Regression:
  RMSE: 85.2341
  MAE:  62.1847
  R²:   0.7234

Decision Tree Regression:
  RMSE: 78.9123
  MAE:  58.3421
  R²:   0.7689

Random Forest Regression:
  RMSE: 72.4567
  MAE:  54.2198
  R²:   0.8012

🏆 Best Model: Random Forest
```

## 🔧 Customization Options

### Model Parameters:
- Modify Random Forest `numTrees` parameter
- Adjust train/test split ratio
- Change outlier removal thresholds

### Feature Selection:
- Add/remove features in `feature_cols` list
- Implement additional feature engineering
- Apply different scaling techniques

### Evaluation:
- Add cross-validation
- Include additional metrics
- Implement model ensemble techniques

## 📋 Requirements

### System Requirements:
- **Memory**: Minimum 4GB RAM (8GB+ recommended)
- **Storage**: 500MB free space
- **OS**: Windows, macOS, or Linux

### Software Dependencies:
- **PySpark 3.5.0**: Distributed computing framework
- **Matplotlib 3.7.2**: Plotting and visualization
- **Seaborn 0.12.2**: Statistical data visualization
- **Pandas 2.0.3**: Data manipulation and analysis
- **NumPy 1.24.3**: Numerical computing

## 🎯 Use Cases

This pipeline can be adapted for:
- **Real Estate Valuation**: Property price estimation
- **Investment Analysis**: ROI calculations for properties
- **Market Research**: Housing market trend analysis
- **Insurance**: Property value assessment
- **Banking**: Loan amount determination

## 🔍 Troubleshooting

### Common Issues:

1. **Java Not Found Error**:
   - Install Java 8 or 11
   - Set JAVA_HOME environment variable

2. **Memory Issues**:
   - Reduce dataset size for testing
   - Increase Spark memory configuration

3. **Import Errors**:
   - Ensure all dependencies are installed
   - Check Python version compatibility

### Performance Tips:
- Use SSD storage for better I/O performance
- Increase available RAM for larger datasets
- Consider using Spark cluster for very large datasets

## 📝 License

This project is for educational and research purposes. Feel free to modify and adapt for your specific use cases.

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional regression algorithms
- Advanced feature engineering techniques
- Hyperparameter tuning implementation
- Cross-validation and model selection
- Real-time prediction API

---

**Happy Predicting! 🏠💰**