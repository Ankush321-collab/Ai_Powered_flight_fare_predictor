# Backend Integration Guide

## Architecture Overview

The Flight Fare Prediction system uses a **microservices architecture**:

```
┌─────────────────┐      HTTP       ┌──────────────────┐
│   Frontend      │ ←──────────────→ │  Node.js Backend │
│   (React)       │                  │  (Port 4000)     │
└─────────────────┘                  └──────────────────┘
                                             │
                                             │ HTTP (axios)
                                             ↓
                                     ┌──────────────────┐
                                     │ Flask ML Service │
                                     │  (Port 5001)     │
                                     └──────────────────┘
                                             │
                                             │ joblib
                                             ↓
                                     ┌──────────────────┐
                                     │  ML Model (.pkl) │
                                     │  R²=95.8%        │
                                     └──────────────────┘
```

## Services

### 1. Flask ML Service (Port 5001)
**File**: `backend/ml_service.py`

Python microservice that handles machine learning predictions.

**Endpoints**:
- `GET /health` - Health check
- `POST /predict` - Single price prediction
- `POST /predict/multiple` - 30-day forecast
- `POST /recommend` - Booking recommendation

**Features**:
- Uses Enhanced Random Forest model (95.8% R² accuracy)
- 27 engineered features
- Loads model once at startup for performance

### 2. Node.js Backend (Port 4000)
**File**: `backend/server.js`

Express.js API server that handles HTTP requests, routing, and database operations.

**ML Endpoints** (`/api/ml/*`):
- `GET /api/ml/health` - Check ML service status
- `POST /api/ml/predict` - Get price prediction
- `POST /api/ml/predict/multiple` - Get 30-day forecast
- `POST /api/ml/recommend` - Get booking recommendation
- `POST /api/ml/search-with-predictions` - Scrape flights + add ML predictions

**Other Endpoints**:
- `/api/flights` - Flight data operations
- `/api/reviews` - Review operations
- `/api/insights` - AI-generated insights

## Starting the Services

### Option 1: PowerShell Script (Recommended)
```powershell
.\start-services.ps1
```
This will:
1. Kill any existing processes on ports 4000 and 5001
2. Start Flask ML service in a new window
3. Start Node.js backend in a new window
4. Display service status

### Option 2: Manual Start

**Terminal 1 - ML Service**:
```powershell
cd c:\Users\hp\Desktop\flight_fare_prediction
python backend\ml_service.py
```

**Terminal 2 - Node.js Backend**:
```powershell
cd c:\Users\hp\Desktop\flight_fare_prediction\backend
npm start
```

## Testing the Integration

Run the test script:
```powershell
.\test-ml-api.ps1
```

Or manually test endpoints:

**Health Check**:
```powershell
curl http://localhost:4000/api/ml/health
```

**Price Prediction**:
```powershell
$body = @{
    airline = "IndiGo"
    origin = "Delhi"
    destination = "Mumbai"
    days_until_flight = 7
    stops = 0
    departure_hour = 10
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:4000/api/ml/predict" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

## API Request/Response Examples

### 1. Single Prediction

**Request**:
```json
POST /api/ml/predict
{
  "airline": "IndiGo",
  "origin": "Delhi",
  "destination": "Mumbai",
  "days_until_flight": 7,
  "stops": 0,
  "departure_hour": 10
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "predicted_price": 10569,
    "currency": "INR",
    "model": "enhanced_random_forest",
    "confidence": "95.8%"
  }
}
```

### 2. 30-Day Forecast

**Request**:
```json
POST /api/ml/predict/multiple
{
  "airline": "IndiGo",
  "origin": "Delhi",
  "destination": "Mumbai",
  "days_ahead": 30
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "predictions": [
      {"day": 1, "date": "2025-11-11", "price": 10569},
      {"day": 2, "date": "2025-11-12", "price": 10450},
      ...
    ],
    "cheapest_day": {
      "day": 15,
      "date": "2025-11-25",
      "price": 8750
    },
    "average_price": 10123,
    "price_range": {"min": 8750, "max": 12500}
  }
}
```

### 3. Booking Recommendation

**Request**:
```json
POST /api/ml/recommend
{
  "current_price": 5500,
  "airline": "IndiGo",
  "origin": "Delhi",
  "destination": "Mumbai",
  "days_until_flight": 7
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "recommendation": "Wait 5 days to save ₹1,200",
    "action": "wait",
    "current_price": 5500,
    "predicted_price": 4300,
    "potential_savings": 1200,
    "confidence": "High"
  }
}
```

### 4. Search with ML Predictions

**Request**:
```json
POST /api/ml/search-with-predictions
{
  "origin": "Delhi",
  "destination": "Mumbai",
  "date": "2025-11-15"
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "flights": [
      {
        "_id": "...",
        "airline": "IndiGo",
        "flight_number": "6E 2012",
        "origin": "Delhi",
        "destination": "Mumbai",
        "price": 5500,
        "departure_time": "06:00",
        "arrival_time": "08:15",
        "ml_prediction": {
          "predicted_price": 10569,
          "is_good_deal": true,
          "savings": 5069
        }
      },
      ...
    ],
    "cheapest": {
      "airline": "IndiGo",
      "price": 4897,
      "ml_prediction": 10123
    },
    "recommendation": {
      "action": "book_now",
      "message": "Great deal! Book now to save ₹5,226"
    }
  }
}
```

## Environment Variables

**backend/.env**:
```env
MONGO_URI=mongodb+srv://ankush:ankush%40123@cluster0.zvexyxw.mongodb.net/flightdb
PORT=4000
ML_SERVICE_URL=http://localhost:5001
```

## Troubleshooting

### ML Service Not Starting
- Check if Python is installed: `python --version`
- Verify Flask is installed: `pip list | Select-String flask`
- Check if port 5001 is already in use: `Get-NetTCPConnection -LocalPort 5001`

### Node.js Backend Not Starting
- Check if Node.js is installed: `node --version`
- Verify dependencies: `cd backend; npm install`
- Check MongoDB connection in `.env` file

### "ML service not available" Error
- Ensure Flask ML service is running on port 5001
- Check `ML_SERVICE_URL` in `.env` matches the Flask service URL
- Test Flask service directly: `curl http://localhost:5001/health`

### Port Already in Use
Kill existing process:
```powershell
# For port 4000
Get-NetTCPConnection -LocalPort 4000 | ForEach-Object {
    Stop-Process -Id $_.OwningProcess -Force
}

# For port 5001
Get-NetTCPConnection -LocalPort 5001 | ForEach-Object {
    Stop-Process -Id $_.OwningProcess -Force
}
```

## Next Steps

1. ✅ Backend integration complete
2. ⏳ Test all ML endpoints
3. ⏳ Integrate with frontend React components
4. ⏳ Add NLP sentiment analysis
5. ⏳ Deploy to production

## Performance Metrics

- **ML Model**: R²=95.8%, MAE=₹636, MAPE=6.8%
- **Training Data**: 945 flights across 12 routes
- **Prediction Time**: ~50ms per request
- **Model Size**: ~2MB (joblib compressed)
