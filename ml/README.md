# ML Module - Enhanced Flight Fare Prediction

Enhanced machine learning module for predicting flight prices using Random Forest with **27 advanced features**.

## 📊 Model Performance

- **R² Score**: **95.8%** (explains 95.8% of price variation)
- **MAE**: **₹636** (average prediction error - only 6.8%!)
- **RMSE**: ₹1,502
- **MAPE**: 6.8% (mean absolute percentage error)

**Improvement over basic model:**
- 69% reduction in error (from ₹2,062 to ₹636)
- 21% increase in R² (from 74.5% to 95.8%)

## 📁 File Structure

```
ml/
├── train_improved_model.py      # Enhanced model training (27 features)
├── predict_enhanced.py           # Price prediction with enhanced features
├── feature_engineering.py        # Feature preparation and engineering
├── collect_diverse_routes.py     # Data collection for 20 routes
├── README.md                     # This file
├── __init__.py                   # Python package marker
├── models/                       # Trained model artifacts
│   ├── fare_prediction_model.pkl
│   ├── feature_mappings.pkl
│   └── model_metadata.pkl
└── data/                         # Optional CSV exports
```

## 🚀 Quick Start

### 1️⃣ Collect Training Data

```bash
cd ml
python collect_diverse_routes.py
```

### 2️⃣ Train Enhanced Model

```bash
python train_improved_model.py
```

### 3️⃣ Make Predictions

```python
from ml.predict_enhanced import EnhancedFarePrediction

predictor = EnhancedFarePrediction()
price = predictor.predict('IndiGo', 'Delhi', 'Mumbai', 7, 0, 10)
print(f"Predicted: ₹{price:,.0f}")
```

## 🔧 Enhanced Features (27 Total)

### Standard (18): airline, route, timing, booking window, season
### Advanced (9): distance, price/km, competition, peak hours, urgency

## 📈 Model Details

- **Algorithm**: Random Forest (200 trees, depth=20)
- **Training Split**: 80% train, 20% test
- **Performance**: 95.8% R² / ₹636 MAE

---

**Model Version**: 2.0 | **Accuracy**: 95.8% R² / ₹636 MAE
