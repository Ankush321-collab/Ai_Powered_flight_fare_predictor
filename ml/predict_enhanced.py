"""
Enhanced Price Prediction Module
=================================
Works with the improved model that has 27 features.
"""
import os
import joblib
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(env_path)

# Route distances
ROUTE_DISTANCES = {
    'Delhi→Mumbai': 1400,
    'Delhi→Bengaluru': 2100,
    'Mumbai→Bengaluru': 980,
    'Mumbai→Chennai': 1340,
    'Kolkata→Delhi': 1470,
    'Pune→Delhi': 1450,
    'Ahmedabad→Mumbai': 530,
    'Jaipur→Delhi': 280,
    'Goa→Bengaluru': 560,
    'delhi→bengaluru': 2100,
}

class EnhancedFarePrediction:
    """Enhanced flight fare prediction with 27 features"""
    
    def __init__(self, model_dir=None):
        """Load trained model"""
        if model_dir is None:
            model_dir = os.path.join(os.path.dirname(__file__), 'models')
        
        model_path = os.path.join(model_dir, 'fare_prediction_model.pkl')
        metadata_path = os.path.join(model_dir, 'model_metadata.pkl')
        mappings_path = os.path.join(model_dir, 'feature_mappings.pkl')
        
        if not os.path.exists(model_path):
            raise FileNotFoundError("Model not found. Train with train_improved_model.py first")
        
        self.model = joblib.load(model_path)
        self.metadata = joblib.load(metadata_path)
        self.feature_columns = self.metadata['feature_columns']
        self.route_distances = self.metadata.get('route_distances', ROUTE_DISTANCES)
        
        # Load feature mappings (label encoders)
        if os.path.exists(mappings_path):
            self.feature_mappings = joblib.load(mappings_path)
        else:
            self.feature_mappings = {}
        
        # Load statistics from MongoDB
        self._load_statistics()
    
    def _load_statistics(self):
        """Load airline and route statistics from database"""
        try:
            mongo_uri = os.getenv('MONGO_URI')
            client = MongoClient(mongo_uri)
            db = client['flightdb']
            collection = db['flights']
            
            flights = list(collection.find({'price': {'$lt': 50000}}))
            df = pd.DataFrame(flights)
            
            if len(df) > 0:
                # Airline average prices
                self.airline_avg_price = df.groupby('airline')['price'].mean().to_dict()
                
                # Route competition
                self.route_competition = df.groupby('route')['airline'].nunique().to_dict()
                
                # Airline-route frequency
                self.airline_route_freq = df.groupby(['airline', 'route']).size().to_dict()
            else:
                self.airline_avg_price = {}
                self.route_competition = {}
                self.airline_route_freq = {}
            
            client.close()
        except:
            self.airline_avg_price = {'IndiGo': 6700, 'Air India': 11000, 'SpiceJet': 8300}
            self.route_competition = {}
            self.airline_route_freq = {}
    
    def predict(self, airline, origin, destination, days_until_flight,
                stops=0, departure_hour=12):
        """
        Predict flight fare with enhanced features.
        
        Args:
            airline: Airline name (e.g., 'IndiGo')
            origin: Origin city (e.g., 'Delhi')
            destination: Destination city (e.g., 'Mumbai')
            days_until_flight: Days until flight
            stops: Number of stops (default 0)
            departure_hour: Hour of departure 0-23 (default 12)
            
        Returns:
            Predicted price in INR
        """
        # Build feature vector
        flight_date = datetime.now() + timedelta(days=days_until_flight)
        route = f"{origin}→{destination}"
        
        # Use label encoders if available, otherwise use hash
        features = {}
        
        # Get encoded values from mappings
        airline_hash = hash(airline) % 1000
        origin_hash = hash(origin) % 1000
        dest_hash = hash(destination) % 1000
        route_hash = hash(route) % 1000
        
        # Try to use stored encodings
        airline_encoding = self.feature_mappings.get('airline_code', {})
        from_encoding = self.feature_mappings.get('from_code', {})
        to_encoding = self.feature_mappings.get('to_code', {})
        route_encoding = self.feature_mappings.get('route_code', {})
        
        # Map to encoded values (use hash if not found)
        features['airline_code'] = airline_encoding.get(airline_hash, airline_hash % 10)
        features['from_code'] = from_encoding.get(origin_hash, origin_hash % 10)
        features['to_code'] = to_encoding.get(dest_hash, dest_hash % 10)
        features['route_code'] = route_encoding.get(route_hash, route_hash % 10)
        
        features['days_until_flight'] = days_until_flight
        features['stops'] = stops
        features['departure_hour'] = departure_hour
        
        # Time features
        features['day_of_week_num'] = flight_date.weekday()
        features['month'] = flight_date.month
        features['is_weekend'] = 1 if flight_date.weekday() >= 5 else 0
        features['is_monday'] = 1 if flight_date.weekday() == 0 else 0
        features['is_friday'] = 1 if flight_date.weekday() == 4 else 0
        
        # Time of day
        if 5 <= departure_hour < 12:
            features['time_of_day_code'] = 0  # morning
        elif 12 <= departure_hour < 17:
            features['time_of_day_code'] = 1  # afternoon
        elif 17 <= departure_hour < 21:
            features['time_of_day_code'] = 2  # evening
        else:
            features['time_of_day_code'] = 3  # night
        
        # Flight characteristics
        features['is_direct'] = 1 if stops == 0 else 0
        features['is_advance_booking'] = 1 if days_until_flight > 14 else 0
        features['is_last_minute'] = 1 if days_until_flight < 3 else 0
        
        # Booking window
        if days_until_flight <= 3:
            features['booking_window_code'] = 0
        elif days_until_flight <= 7:
            features['booking_window_code'] = 1
        elif days_until_flight <= 14:
            features['booking_window_code'] = 2
        else:
            features['booking_window_code'] = 3
        
        # Season
        if flight_date.month in [12, 1, 2]:
            features['season_code'] = 0  # winter
        elif flight_date.month in [3, 4, 5]:
            features['season_code'] = 1  # spring
        elif flight_date.month in [6, 7, 8]:
            features['season_code'] = 2  # summer
        else:
            features['season_code'] = 3  # fall
        
        # ENHANCED FEATURES with realistic values
        # Route distance
        features['route_distance'] = self.route_distances.get(route, 1000)
        
        # Price per km - use realistic airline pricing
        base_price_per_km = {
            'IndiGo': 5.5,
            'SpiceJet': 5.2,
            'GoAir': 5.0,
            'Vistara': 7.5,
            'Air India': 8.0
        }.get(airline, 6.0)
        
        # Adjust price per km based on booking window
        if days_until_flight < 3:
            base_price_per_km *= 1.5  # Last minute surge
        elif days_until_flight > 30:
            base_price_per_km *= 0.85  # Early bird discount
            
        features['price_per_km'] = base_price_per_km
        
        # Route competition
        features['route_competition'] = self.route_competition.get(route, 5)
        
        # Airline-route frequency
        features['airline_route_frequency'] = self.airline_route_freq.get((airline, route), 10)
        
        # Peak hours
        features['is_peak_hour'] = 1 if 7 <= departure_hour <= 9 or 17 <= departure_hour <= 19 else 0
        features['is_red_eye'] = 1 if departure_hour >= 22 or departure_hour <= 4 else 0
        
        # Booking urgency
        if days_until_flight <= 2:
            features['booking_urgency'] = 3
        elif days_until_flight <= 7:
            features['booking_urgency'] = 2
        elif days_until_flight <= 14:
            features['booking_urgency'] = 1
        else:
            features['booking_urgency'] = 0
        
        # Route length category
        dist = features['route_distance']
        if dist < 500:
            features['route_length_category'] = 0
        elif dist < 1000:
            features['route_length_category'] = 1
        elif dist < 1500:
            features['route_length_category'] = 2
        else:
            features['route_length_category'] = 3
        
        # Airline price tier - realistic base prices
        airline_base_prices = {
            'IndiGo': 7200,
            'SpiceJet': 6800,
            'GoAir': 6500,
            'Vistara': 9500,
            'Air India': 10500
        }
        features['airline_price_tier'] = airline_base_prices.get(airline, 8000)
        
        # Create DataFrame with proper feature names to avoid sklearn warning
        X = pd.DataFrame([features], columns=self.feature_columns)
        
        # Predict
        predicted_price = self.model.predict(X)[0]
        
        return predicted_price

def test_enhanced_predictions():
    """Test the enhanced model"""
    print("\n" + "="*80)
    print("Testing Enhanced ML Model")
    print("="*80 + "\n")
    
    try:
        predictor = EnhancedFarePrediction()
        print("✅ Enhanced model loaded!\n")
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Test cases
    tests = [
        ('IndiGo', 'Delhi', 'Mumbai', 7, 0, 10, 'Delhi→Mumbai Morning'),
        ('IndiGo', 'Delhi', 'Mumbai', 7, 0, 20, 'Delhi→Mumbai Evening'),
        ('Air India', 'Delhi', 'Mumbai', 7, 0, 10, 'Air India (premium)'),
        ('IndiGo', 'Delhi', 'Mumbai', 3, 0, 10, 'Last minute'),
        ('IndiGo', 'Delhi', 'Mumbai', 21, 0, 10, 'Advance booking'),
        ('IndiGo', 'Delhi', 'Mumbai', 7, 1, 10, 'With 1 stop'),
        ('IndiGo', 'Delhi', 'Bengaluru', 7, 0, 10, 'Longer route'),
        ('IndiGo', 'Jaipur', 'Delhi', 7, 0, 10, 'Short route'),
        ('SpiceJet', 'Mumbai', 'Chennai', 7, 0, 10, 'Mumbai→Chennai'),
        ('IndiGo', 'Kolkata', 'Delhi', 7, 0, 18, 'Evening flight'),
    ]
    
    print(f"{'Route/Condition':<30} {'Predicted Price':<15}")
    print("-" * 50)
    
    for airline, origin, dest, days, stops, hour, label in tests:
        try:
            price = predictor.predict(airline, origin, dest, days, stops, hour)
            print(f"{label:<30} ₹{price:>12,.0f}")
        except Exception as e:
            print(f"{label:<30} Error: {e}")
    
    print("\n" + "="*80)
    print("✅ Testing Complete!")
    print("="*80 + "\n")

if __name__ == '__main__':
    test_enhanced_predictions()
