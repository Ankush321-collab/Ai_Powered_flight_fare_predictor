# Flight Fare Prediction - AI Powered# ✈️ AI-Powered Flight Fare Predictor# Flight Fare & Sentiment Analyzer



ML-powered flight price prediction and booking recommendation system.



## Quick Start> Predicts flight prices with **95.8% accuracy** using Machine LearningProject scaffold for Flight Fare & Sentiment Analyzer (MERN + Python NLP + LLM)



### Method 1: Auto Start (Easiest)

```powershell

python start_all.py## 🚀 How to Run This ProjectQuick start (local development):

```

This will open 3 terminal windows automatically.



### Method 2: Manual Start### **Quick Start (3 Steps)**1) Backend



**Terminal 1 - ML Service:**```

```powershell

python backend\ml_service.py#### Step 1: Install Dependenciescd backend

```

```powershellnpm install

**Terminal 2 - Backend:**

```powershell# Install Python packages (for ML & Scraper)npm run dev

cd backend

npm startpip install flask flask-cors scikit-learn pandas numpy joblib pymongo selenium beautifulsoup4```

```



**Terminal 3 - Frontend:**

```powershell# Install Node.js packages (for Backend)2) Scraper & NLP

cd frontend

npm run devcd backend```

```

npm installcd scraper_nlp

### Open App

Navigate to: **http://localhost:5173**```python -m venv .venv



---# On Windows PowerShell



## Features#### Step 2: Start Backend Services.\.venv\Scripts\Activate.ps1; pip install -r requirements.txt



✅ **Price Predictor** - Predict single flight prices  ```powershellpython main.py

✅ **30-Day Forecast** - View price trends for next 30 days  

✅ **Book or Wait** - Get AI recommendations  # Go to project root```

✅ **Flight Search** - Search with ML predictions  

✅ **Analytics** - View model performancecd c:\Users\hp\Desktop\flight_fare_prediction



---3) Frontend



## Model Info# Run startup script (opens 2 windows)```



- **Algorithm**: Random Forest Regressor.\start-services.ps1cd frontend

- **Training Data**: 50,220 flights (18 routes, 900 days)

- **Accuracy**: 92.45% R² Score```npm install

- **Average Error**: ₹707

- **Features**: 27 engineered featuresnpm run dev



---This starts:```



## Ports- **Flask ML Service** on port 5001 ✅



- ML Service (Flask): `5001`- **Node.js Backend** on port 4000 ✅See `backend/.env.example` and `scraper_nlp/requirements.txt` for environment variables and dependencies.

- Backend API (Node.js): `4000`

- Frontend (Vite): `5173`



---#### Step 3: Test It WorksDeployment guide is in `backend/DEPLOYMENT.md` and `frontend/DEPLOYMENT.md`.



## Project Structure```powershell

# Test health check

```curl http://localhost:4000/api/ml/health

├── backend/           # Node.js + Express API

│   ├── ml_service.py  # Flask ML service# Test price prediction

│   ├── server.js      # Express servercurl -X POST http://localhost:4000/api/ml/predict -H "Content-Type: application/json" -d '{\"airline\":\"IndiGo\",\"origin\":\"Delhi\",\"destination\":\"Mumbai\",\"days_until_flight\":7,\"stops\":0,\"departure_hour\":10}'

│   └── controllers/   # API controllers```

├── frontend/          # React + Vite

│   └── src/**Expected Response:**

│       ├── components/  # ML components```json

│       └── pages/       # Dashboard{

├── ml/                # ML models  "status":"success",

│   ├── train_improved_model.py  "data":{

│   ├── predict_enhanced.py    "predicted_price":10568.9,

│   └── models/        # Saved models    "currency":"INR",

└── scraper_nlp/       # Web scraping    "model":"enhanced_random_forest"

```  }

}

---```



## Tech Stack---



**Backend:**## 📊 What's Inside

- Node.js + Express

- Flask (ML service)This project has **3 components**:

- MongoDB Atlas

### 1. **Web Scraper** (Python)

**Frontend:**Collects live flight data from EasyMyTrip

- React 18```powershell

- Vitecd scraper_nlp

- Tailwind CSSpython save_to_mongo.py

- Recharts```

- Scrapes airline, price, timings

**ML:**- Saves to MongoDB

- scikit-learn- **Current data**: 945 flights, 12 routes

- Random Forest

- 27 engineered features### 2. **ML Model** (Python - Flask API)

Predicts flight prices with 95.8% accuracy

---```powershell

# Already running via start-services.ps1

## Troubleshooting# Manual start:

python backend\ml_service.py

**MongoDB connection fails:**```

```powershell- **Port**: 5001

ipconfig /flushdns- **Model**: Random Forest (27 features)

```- **Accuracy**: 95.8% R² score, MAE ₹636

Then restart backend.

### 3. **Backend API** (Node.js)

**ML Service not responding:**REST API for frontend

Check if port 5001 is free:```powershell

```powershell# Already running via start-services.ps1

netstat -ano | findstr :5001# Manual start:

```cd backend

npm start

**Frontend errors:**```

```powershell- **Port**: 4000

cd frontend- **Database**: MongoDB Atlas

npm install- **Endpoints**: `/api/ml/*`, `/api/flights`, `/api/reviews`

```

---

---

## 🎯 API Endpoints You Can Use

## Data

### **Health Check**

**Training Data:**```bash

- `ml/data/generated_flights_30days.csv` (1,620 flights)GET http://localhost:4000/api/ml/health

- `ml/data/generated_flights_900days.csv` (48,600 flights)```



**Retrain Model:**### **Predict Single Price**

```powershell```bash

cd mlPOST http://localhost:4000/api/ml/predict

python train_improved_model.pyBody: {

```  "airline": "IndiGo",

  "origin": "Delhi",

---  "destination": "Mumbai",

  "days_until_flight": 7,

## Environment Variables  "stops": 0,

  "departure_hour": 10

**Backend (.env):**}

``````

MONGO_URI=mongodb+srv://...

PORT=4000### **Get 7-Day Forecast**

``````bash

POST http://localhost:4000/api/ml/predict/multiple

**Frontend (.env):**Body: {

```  "airline": "IndiGo",

VITE_API_URL=http://localhost:4000/api/ml  "origin": "Delhi",

VITE_BACKEND_URL=http://localhost:4000/api  "destination": "Mumbai",

```  "days_ahead": 7

}

---```



Built with ❤️ using AI and Machine Learning### **Get Booking Recommendation**

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
