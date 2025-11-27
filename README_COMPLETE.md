# 🏠 House Price Prediction Dashboard

A comprehensive web application for predicting house prices in India (Pan-India and Bengaluru-specific) with interactive analytics and data exploration features.

## ✨ Features

### 🎯 Prediction
- **Pan-India Predictor** - Get price estimates for properties across India
- **Bengaluru Specific** - Dedicated model trained on Bengaluru housing data
- **Real-time Predictions** - Instant price estimates based on property features

### 📊 Analytics Dashboard
- **State-wise Analysis** - Average prices and trends by Indian states
- **Price Distribution** - Histogram of property prices across bins
- **Location Insights** - Top Bengaluru locations with listing counts
- **Price vs. Area Correlation** - Scatter plot analysis (Bengaluru)

### 📋 Data Browser
- **Paginated Tables** - Browse raw data with 25/50/100 rows per page
- **Interactive Charts** - Visualize data distributions and trends
- **Dataset Toggle** - Switch between Pan-India and Bengaluru datasets
- **Export-Ready Format** - Table view ready for analysis

### 🧭 Navigation
- **Global Navbar** - Consistent navigation across all pages
- **Mobile Responsive** - Works on desktop, tablet, and mobile devices
- **Dark-Themed UI** - Professional purple/blue gradient design

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements_web.txt
```

### 2. Start the Flask App
```bash
python app.py
```

The app will start at: **http://127.0.0.1:5000/**

### 3. Access the Interface
Open your browser and navigate to the link above. You'll see:
- Home page with quick-link navigation buttons
- Navbar at the top for accessing all sections

---

## 📍 Application Pages

### 🏠 **Home** (`/`)
Entry point with quick-link buttons to:
- Price Estimator (Pan-India & Bengaluru)
- Bengaluru Dedicated Page
- Links to Analytics and Data Browser (via navbar)

### 💰 **Estimator** (`/estimate`)
Combined prediction interface with region selector:
- **Pan-India Mode**: Predict prices across Indian states
  - Inputs: BHK, Total Sqft, Bathrooms, Property Type, State
  - Model: RandomForest trained on 20K samples
  
- **Bengaluru Mode**: Bengaluru-specific predictions
  - Inputs: BHK, Total Sqft, Bathrooms, Balcony, Location, Area Type
  - Special features: Location encoding, area type classification

### 📊 **Analytics** (`/analytics`)
Four interactive Chart.js visualizations:
1. **Average Price by State** - Bar chart with top states
2. **Price Distribution** - Pie chart of price bands (5L, 10L, 15L, etc.)
3. **Bengaluru Locations** - Top 10 locations by listings
4. **Price vs. Area** - Scatter plot correlation (Bengaluru)

### 📋 **Data Browser** (`/data`)
Explore housing datasets with dual views:
- **Table View**: Paginated data with sortable columns
- **Chart View**: Visual analysis of price distributions
- **Controls**:
  - Dataset selector (Pan-India / Bengaluru)
  - Rows per page (25 / 50 / 100)
  - Previous/Next pagination

### 🏘️ **Bengaluru** (`/karnataka/bengaluru`)
Direct Bengaluru predictor without region selection:
- Streamlined form for Bengaluru-specific properties
- Pre-populated with Bengaluru options
- Quick prediction interface

---

## 🔌 API Endpoints

### Page Routes
```
GET  /                  Home page
GET  /estimate          Combined estimator
GET  /analytics         Analytics dashboard
GET  /data              Data browser
GET  /karnataka/bengaluru    Bengaluru predictor
```

### Prediction APIs
```
POST /predict                       Pan-India prediction
POST /predict/bengaluru             Bengaluru prediction
```

### Data APIs
```
GET  /api/data/pan-india?page=1&per_page=50          Paginated pan-india data
GET  /api/data/bengaluru?page=1&per_page=50          Paginated bengaluru data
```

### Options APIs (for dropdowns)
```
GET  /api/all/options              All dropdown options (pan + bengaluru)
GET  /api/bengaluru/options        Bengaluru-specific options
```

### Analytics APIs (for chart data)
```
GET  /api/analytics/pan/state_summary               Average price by state
GET  /api/analytics/pan/price_bins                  Price distribution
GET  /api/analytics/bengaluru/location_summary      Top Bengaluru locations
GET  /api/analytics/bengaluru/price_vs_sqft         Price vs. area correlation
```

### Example API Calls
```bash
# Get Pan-India data
curl "http://127.0.0.1:5000/api/data/pan-india?page=1&per_page=50"

# Get Bengaluru data with 25 rows
curl "http://127.0.0.1:5000/api/data/bengaluru?page=1&per_page=25"

# Make a prediction
curl -X POST "http://127.0.0.1:5000/predict/bengaluru" \
  -d "bhk=2&total_sqft=1200&bath=2&balcony=1&area_type=Residential&location=Whitefield"
```

---

## 📊 Data Sources

### Pan-India Dataset (`india_housing_prices.csv`)
- **Columns**: State, Price_in_Lakhs, BHK, Size_in_SqFt, Property_Type, Furnished_Status, City
- **Rows**: ~4,340 properties
- **Model**: RandomForest (50 estimators) trained on 20K sampled rows
- **Purpose**: General price prediction across India

### Bengaluru Dataset (`Bengaluru_House_Data.csv`)
- **Columns**: location, area_type, price, size, total_sqft, bath, balcony, availability
- **Rows**: ~1,354 properties in Bengaluru
- **Model**: RandomForest trained on top 50 locations
- **Purpose**: Precise Bengaluru predictions with location insights

---

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask (Python)
- **ML**: scikit-learn (RandomForest models)
- **Data**: Pandas (2.3.3)
- **Encoding**: LabelEncoder for categorical features

### Frontend
- **CSS Framework**: Bootstrap 5.3.0
- **Charts**: Chart.js 4.3.0
- **Templating**: Jinja2

### Architecture
- **Models**: Trained at app startup (cached in memory)
- **Sampling**: Max 20K rows for training (speed optimization)
- **Encoding**: Separate LabelEncoder per dataset
- **Pagination**: Database-style slicing for large tables

---

## 📁 Project Structure

```
House_price_prediction/
├── app.py                                    Main Flask application
├── requirements_web.txt                      Web dependencies
├── india_housing_prices.csv                  Pan-India dataset
├── Bengaluru_House_Data.csv                  Bengaluru dataset
├── NAVBAR_AND_DATA_BROWSER_UPDATE.md         Update documentation
├── test_data_browser.py                      API test script
├── templates/
│   ├── index.html                            Home page
│   ├── estimate.html                         Combined estimator
│   ├── analytics.html                        Analytics dashboard
│   ├── bengaluru.html                        Bengaluru predictor
│   └── data.html                             Data browser (NEW)
├── static/
│   └── css/
│       ├── estimate.css                      Estimator styles
│       ├── bengaluru.css                     Bengaluru page styles
│       └── analytics.css                     Analytics styles
└── README.md                                 This file
```

---

## 🎨 UI/UX Design

### Color Scheme
- **Primary Gradient**: Linear gradient from #667eea (purple) to #764ba2 (darker purple)
- **Text**: White on gradient, dark gray on light backgrounds
- **Accent**: Green for success/estimates, red for errors

### Navigation
- **Sticky Navbar**: Always visible during scrolling
- **Mobile Toggle**: Hamburger menu on small screens
- **Active State**: Current page highlighted in navbar
- **Links**: Home, Estimate, Analytics, Data Browser

### Responsive Design
- **Desktop**: Full 2-column layouts, side-by-side charts
- **Tablet**: Stacked layouts, optimized spacing
- **Mobile**: Single column, touch-friendly buttons

---

## 📈 Model Details

### Pan-India Model
```python
RandomForestRegressor(
    n_estimators=50,      # Reduced for speed
    random_state=42,
    n_jobs=-1             # Use all CPU cores
)

Training Data:
  - Sampled: max 20,000 rows
  - Features: State, BHK, Size_in_SqFt, Property_Type, Furnished_Status
  - Encoding: LabelEncoder for categorical features
  - Target: Price_in_Lakhs
```

### Bengaluru Model
```python
RandomForestRegressor(
    n_estimators=50,
    random_state=42,
    n_jobs=-1
)

Training Data:
  - Rows: All Bengaluru data (1,354 rows)
  - Features: location, area_type, BHK, total_sqft, bath, balcony
  - Special Processing:
    * BHK extracted from "size" column (e.g., "2 BHK" → 2)
    * total_sqft parsed from ranges (e.g., "1000-1200" → 1100)
    * Top 50 locations encoded, others mapped to "Other"
  - Target: price (in Lakhs)
```

---

## 🧪 Testing

### Run API Tests
```bash
# Terminal 1: Start Flask app
python app.py

# Terminal 2: Run tests
python test_data_browser.py
```

Expected output:
```
✅ Testing: Pan-India data (page 1, 10 rows)
   Status: 200
   ✅ PASS
   ...

📊 TEST SUMMARY
✅ Passed: 12/12
❌ Failed: 0/12

🎉 ALL TESTS PASSED!
```

---

## 🚨 Troubleshooting

### Issue: "Connection refused" or port 5000 already in use
**Solution:**
```bash
# On Windows PowerShell
Get-Process | Where-Object {$_.Port -eq 5000}
Stop-Process -Name "python" -Force

# Then restart: python app.py
```

### Issue: Models loading slowly
**Solution:** This is normal on first run. Models are cached in memory after startup.

### Issue: "No Bengaluru data" error
**Solution:** Ensure `Bengaluru_House_Data.csv` is in the same directory as `app.py`

### Issue: Pandas or sklearn not found
**Solution:**
```bash
pip install -r requirements_web.txt
```

---

## 📝 Performance Notes

- **Startup Time**: ~5-10 seconds (first run, model training)
- **Prediction Time**: <100ms per request
- **Data Loading**: <50ms for paginated queries
- **Chart Rendering**: <500ms on client-side

---

## 🔮 Future Enhancements

1. **Advanced Filters** - Search/filter data browser by price, location, etc.
2. **Export Features** - Download data as CSV/Excel
3. **More Visualizations** - Heatmaps, box plots, time series
4. **User Authentication** - Save favorite predictions
5. **API Rate Limiting** - Prevent abuse
6. **Database Caching** - For faster pagination on large datasets
7. **Dark Mode** - Toggle theme preference
8. **Mobile App** - Native iOS/Android versions

---

## 📄 License

This project is provided as-is for educational and demonstration purposes.

---

## 👨‍💻 Development

### Adding New Features
1. Update `app.py` with new routes/endpoints
2. Create corresponding template in `templates/`
3. Add any new CSS to `static/css/`
4. Test with `test_data_browser.py`

### Modifying Models
Edit the `load_model()` and `load_bengaluru_model()` functions in `app.py` to:
- Change model parameters (n_estimators, max_depth, etc.)
- Add new features
- Change feature engineering logic

---

## ✅ Verification Checklist

- [x] Flask app runs without errors
- [x] All pages load correctly
- [x] Predictions work (both Pan-India and Bengaluru)
- [x] Analytics charts render correctly
- [x] Data browser pagination works
- [x] Navbar visible on all pages
- [x] Mobile responsive design
- [x] API endpoints respond with correct JSON
- [x] No console errors in browser DevTools

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the test output from `test_data_browser.py`
3. Check browser console (F12) for JavaScript errors
4. Ensure all CSV files are present and readable

---

**Happy Predicting! 🎉**

Start at: `http://127.0.0.1:5000/`
