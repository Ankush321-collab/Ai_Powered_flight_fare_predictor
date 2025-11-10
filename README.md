# ✈️ AI-Powered Flight Fare Predictor# Flight Fare & Sentiment Analyzer



> Predicts flight prices with **95.8% accuracy** using Machine LearningProject scaffold for Flight Fare & Sentiment Analyzer (MERN + Python NLP + LLM)



## 🚀 How to Run This ProjectQuick start (local development):



### **Quick Start (3 Steps)**1) Backend

```

#### Step 1: Install Dependenciescd backend

```powershellnpm install

# Install Python packages (for ML & Scraper)npm run dev

pip install flask flask-cors scikit-learn pandas numpy joblib pymongo selenium beautifulsoup4```



# Install Node.js packages (for Backend)2) Scraper & NLP

cd backend```

npm installcd scraper_nlp

```python -m venv .venv

# On Windows PowerShell

#### Step 2: Start Backend Services.\.venv\Scripts\Activate.ps1; pip install -r requirements.txt

```powershellpython main.py

# Go to project root```

cd c:\Users\hp\Desktop\flight_fare_prediction

3) Frontend

# Run startup script (opens 2 windows)```

.\start-services.ps1cd frontend

```npm install

npm run dev

This starts:```

- **Flask ML Service** on port 5001 ✅

- **Node.js Backend** on port 4000 ✅See `backend/.env.example` and `scraper_nlp/requirements.txt` for environment variables and dependencies.



#### Step 3: Test It WorksDeployment guide is in `backend/DEPLOYMENT.md` and `frontend/DEPLOYMENT.md`.

```powershell
# Test health check
curl http://localhost:4000/api/ml/health

# Test price prediction
curl -X POST http://localhost:4000/api/ml/predict -H "Content-Type: application/json" -d '{\"airline\":\"IndiGo\",\"origin\":\"Delhi\",\"destination\":\"Mumbai\",\"days_until_flight\":7,\"stops\":0,\"departure_hour\":10}'
```

**Expected Response:**
```json
{
  "status":"success",
  "data":{
    "predicted_price":10568.9,
    "currency":"INR",
    "model":"enhanced_random_forest"
  }
}
```

---

## 📊 What's Inside

This project has **3 components**:

### 1. **Web Scraper** (Python)
Collects live flight data from EasyMyTrip
```powershell
cd scraper_nlp
python save_to_mongo.py
```
- Scrapes airline, price, timings
- Saves to MongoDB
- **Current data**: 945 flights, 12 routes

### 2. **ML Model** (Python - Flask API)
Predicts flight prices with 95.8% accuracy
```powershell
# Already running via start-services.ps1
# Manual start:
python backend\ml_service.py
```
- **Port**: 5001
- **Model**: Random Forest (27 features)
- **Accuracy**: 95.8% R² score, MAE ₹636

### 3. **Backend API** (Node.js)
REST API for frontend
```powershell
# Already running via start-services.ps1
# Manual start:
cd backend
npm start
```
- **Port**: 4000
- **Database**: MongoDB Atlas
- **Endpoints**: `/api/ml/*`, `/api/flights`, `/api/reviews`

---

## 🎯 API Endpoints You Can Use

### **Health Check**
```bash
GET http://localhost:4000/api/ml/health
```

### **Predict Single Price**
```bash
POST http://localhost:4000/api/ml/predict
Body: {
  "airline": "IndiGo",
  "origin": "Delhi",
  "destination": "Mumbai",
  "days_until_flight": 7,
  "stops": 0,
  "departure_hour": 10
}
```

### **Get 7-Day Forecast**
```bash
POST http://localhost:4000/api/ml/predict/multiple
Body: {
  "airline": "IndiGo",
  "origin": "Delhi",
  "destination": "Mumbai",
  "days_ahead": 7
}
```

### **Get Booking Recommendation**
```bash
POST http://localhost:4000/api/ml/recommend
Body: {
  "current_price": 5500,
  "airline": "IndiGo",
  "origin": "Delhi",
  "destination": "Mumbai",
  "days_until_flight": 7
}
```

---

## 📁 Project Structure

```
flight_fare_prediction/
│
├── scraper_nlp/              # Web Scraper
│   └── save_to_mongo.py      # Scrapes EasyMyTrip
│
├── ml/                       # Machine Learning
│   ├── train_improved_model.py   # Train model (95.8% accuracy)
│   ├── predict_enhanced.py       # Prediction logic
│   └── models/                   # Saved models (.pkl)
│
├── backend/                  # Backend Services
│   ├── ml_service.py         # Flask ML API (Port 5001)
│   ├── server.js             # Node.js API (Port 4000)
│   ├── routes/mlRoutes.js    # ML endpoints
│   └── controllers/mlController.js
│
├── frontend/                 # React Dashboard (Future)
│
├── .env                      # MongoDB connection
├── start-services.ps1        # 🚀 START HERE
└── test-ml-api.ps1          # Test all endpoints
```

---

## 🔧 Configuration

Your `.env` file should have:
```env
MONGO_URI=mongodb+srv://ankush:ankush%40123@cluster0.zvexyxw.mongodb.net/flightdb
PORT=4000
ML_SERVICE_URL=http://localhost:5001
```

---

## 🧪 Complete Testing

Run comprehensive tests:
```powershell
.\test-ml-api.ps1
```

This tests:
- ✅ Health check
- ✅ Single prediction
- ✅ 30-day forecast
- ✅ Booking recommendation

---

## 🛠️ Manual Start (Alternative)

If you don't want to use the script:

**Terminal 1 - Flask ML Service:**
```powershell
cd c:\Users\hp\Desktop\flight_fare_prediction
python backend\ml_service.py
```

**Terminal 2 - Node.js Backend:**
```powershell
cd c:\Users\hp\Desktop\flight_fare_prediction\backend
npm start
```

---

## 📊 ML Model Performance

- **Accuracy (R²)**: 95.8%
- **Mean Absolute Error**: ₹636
- **Training Data**: 945 flights across 12 routes
- **Features**: 27 engineered features
- **Algorithm**: Random Forest (200 trees)

**Routes Covered:**
- Delhi → Mumbai, Bengaluru
- Mumbai → Chennai, Bengaluru
- Goa → Bengaluru
- Kolkata → Delhi
- Pune → Delhi
- And more...

---

## 🐛 Troubleshooting

### Services Not Starting?
```powershell
# Kill processes on ports 4000 and 5001
Get-NetTCPConnection -LocalPort 4000 | ForEach-Object {
    Stop-Process -Id $_.OwningProcess -Force
}
Get-NetTCPConnection -LocalPort 5001 | ForEach-Object {
    Stop-Process -Id $_.OwningProcess -Force
}

# Restart services
.\start-services.ps1
```

### Module Not Found?
```powershell
# Python packages
pip install flask flask-cors scikit-learn pandas numpy joblib pymongo

# Node.js packages
cd backend
npm install
```

### MongoDB Connection Error?
- Check internet connection
- Verify `MONGO_URI` in `.env` file
- Ensure MongoDB Atlas IP whitelist includes your IP

---

## 📈 Next Steps

1. ✅ **Backend Integration** - COMPLETE
2. ⏳ **Frontend Integration** - Add predictions to React UI
3. ⏳ **Sentiment Analysis** - Analyze flight reviews
4. ⏳ **Real-time Tracking** - Monitor price changes
5. ⏳ **Email Alerts** - Notify on price drops

---

## 📚 Documentation

- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Complete setup guide
- **[backend/INTEGRATION_GUIDE.md](backend/INTEGRATION_GUIDE.md)** - Detailed API docs
- **[ml/README.md](ml/README.md)** - ML model details

---

## 💡 Example Usage

**Scenario**: Should I book a Delhi→Mumbai flight at ₹5,500?

**Request**:
```bash
curl -X POST http://localhost:4000/api/ml/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "current_price": 5500,
    "airline": "IndiGo",
    "origin": "Delhi",
    "destination": "Mumbai",
    "days_until_flight": 7
  }'
```

**Response**:
```json
{
  "recommendation": "Book now! This is ₹5,069 below predicted price",
  "action": "book_now",
  "predicted_price": 10569,
  "potential_savings": 5069
}
```

---

**Created by**: Ankush  
**Last Updated**: November 10, 2025  
**Status**: ✅ Production Ready  
**ML Accuracy**: 95.8%

---

⭐ **Quick Start Summary**:
1. `.\start-services.ps1` ← Start everything
2. `.\test-ml-api.ps1` ← Test it works
3. Visit `http://localhost:4000/api/ml/health` ← Confirm running
