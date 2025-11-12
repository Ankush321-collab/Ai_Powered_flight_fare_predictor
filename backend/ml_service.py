"""
ML Prediction Service for Backend
==================================
Flask API that serves ML predictions to Node.js backend.

Run: python ml_service.py
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ml.predict_enhanced import EnhancedFarePrediction

app = Flask(__name__)
CORS(app)

# Load ML model once at startup
try:
    predictor = EnhancedFarePrediction()
    print("✅ ML Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading ML model: {e}")
    predictor = None

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': predictor is not None
    })

@app.route('/predict', methods=['POST'])
def predict_price():
    """
    Predict flight price.
    
    Request body:
    {
        "airline": "IndiGo",
        "origin": "Delhi",
        "destination": "Mumbai",
        "days_until_flight": 7,
        "stops": 0,
        "departure_hour": 10
    }
    """
    try:
        if predictor is None:
            return jsonify({'error': 'ML model not loaded'}), 500
        
        data = request.json
        
        # Validate required fields
        required = ['airline', 'origin', 'destination', 'days_until_flight']
        for field in required:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400
        
        # Get prediction
        predicted_price = predictor.predict(
            airline=data['airline'],
            origin=data['origin'],
            destination=data['destination'],
            days_until_flight=data['days_until_flight'],
            stops=data.get('stops', 0),
            departure_hour=data.get('departure_hour', 12)
        )
        
        return jsonify({
            'predicted_price': round(predicted_price, 2),
            'currency': 'INR',
            'model': 'enhanced_random_forest'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict/multiple', methods=['POST'])
def predict_multiple_dates():
    """
    Predict prices for multiple dates.
    
    Request body:
    {
        "airline": "IndiGo",
        "origin": "Delhi",
        "destination": "Mumbai",
        "days_ahead": 30
    }
    """
    try:
        if predictor is None:
            return jsonify({'error': 'ML model not loaded'}), 500
        
        data = request.json
        days_ahead = data.get('days_ahead', 30)
        
        predictions = []
        for days in range(1, days_ahead + 1):
            price = predictor.predict(
                airline=data['airline'],
                origin=data['origin'],
                destination=data['destination'],
                days_until_flight=days,
                stops=data.get('stops', 0),
                departure_hour=data.get('departure_hour', 12)
            )
            
            predictions.append({
                'days_ahead': days,
                'predicted_price': round(price, 2)
            })
        
        # Find cheapest
        cheapest = min(predictions, key=lambda x: x['predicted_price'])
        
        return jsonify({
            'predictions': predictions,
            'cheapest': cheapest,
            'currency': 'INR'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/recommend', methods=['POST'])
def get_recommendation():
    """
    Get booking recommendation based on current price vs predicted future prices.
    
    Request body:
    {
        "current_price": 5500,
        "airline": "IndiGo",
        "origin": "Delhi",
        "destination": "Mumbai"
    }
    """
    try:
        if predictor is None:
            return jsonify({'error': 'ML model not loaded'}), 500
        
        data = request.json
        current_price = data.get('current_price')
        
        if not current_price:
            return jsonify({'error': 'current_price required'}), 400
        
        # Predict prices for next 14 days
        predictions = []
        for days in range(1, 15):
            price = predictor.predict(
                airline=data['airline'],
                origin=data['origin'],
                destination=data['destination'],
                days_until_flight=days,
                stops=data.get('stops', 0),
                departure_hour=data.get('departure_hour', 12)
            )
            predictions.append({'days_ahead': days, 'price': price})
        
        # Find cheapest future prediction
        cheapest_future = min(predictions, key=lambda x: x['price'])
        
        # Generate recommendation
        savings = current_price - cheapest_future['price']
        
        if savings > 500:
            recommendation = f"Wait {cheapest_future['days_ahead']} days to save ₹{savings:.0f}"
            action = "wait"
        elif savings < -500:
            recommendation = f"Book now! Prices likely to increase by ₹{abs(savings):.0f}"
            action = "book_now"
        else:
            recommendation = "Book now or wait - prices are stable"
            action = "flexible"
        
        return jsonify({
            'current_price': current_price,
            'predicted_cheapest': round(cheapest_future['price'], 2),
            'days_to_wait': cheapest_future['days_ahead'],
            'potential_savings': round(savings, 2),
            'recommendation': recommendation,
            'action': action,
            'currency': 'INR'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 ML Prediction Service Starting...")
    print("="*60)
    print(f"Port: 5001")
    print(f"Endpoints:")
    print(f"  GET  /health           - Health check")
    print(f"  POST /predict          - Single price prediction")
    print(f"  POST /predict/multiple - Multiple dates prediction")
    print(f"  POST /recommend        - Booking recommendation")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5001, debug=True)
