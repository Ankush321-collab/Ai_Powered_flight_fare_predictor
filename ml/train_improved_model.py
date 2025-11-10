"""
Improved ML Model with Better Feature Engineering
==================================================
Enhancements:
1. Add route distance as feature (approximation)
2. Add route popularity/competition
3. Better booking window features
4. Interaction features (airline × route, time × route)
5. Hyperparameter tuning
"""
import os
import sys
import pandas as pd
import numpy as np
from pymongo import MongoClient
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
from dotenv import load_dotenv
from datetime import datetime

sys.path.append(os.path.dirname(__file__))
from feature_engineering import prepare_features, get_feature_columns

# Load environment
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(env_path)

# Route distances (approximate km)
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

def add_advanced_features(df):
    """Add advanced features for better predictions"""
    
    # 1. Route distance
    df['route_distance'] = df['route'].map(ROUTE_DISTANCES).fillna(df['route'].map(ROUTE_DISTANCES).median())
    
    # 2. Price per km
    df['price_per_km'] = df['price'] / df['route_distance']
    
    # 3. Route competition (number of airlines on route)
    route_competition = df.groupby('route')['airline'].nunique().to_dict()
    df['route_competition'] = df['route'].map(route_competition)
    
    # 4. Airline popularity on route
    airline_route_counts = df.groupby(['airline', 'route']).size().to_dict()
    df['airline_route_frequency'] = df.apply(lambda x: airline_route_counts.get((x['airline'], x['route']), 0), axis=1)
    
    # 5. Time-based pricing patterns
    df['is_peak_hour'] = df['departure_hour'].apply(lambda x: 1 if 7 <= x <= 9 or 17 <= x <= 19 else 0)
    df['is_red_eye'] = df['departure_hour'].apply(lambda x: 1 if x >= 22 or x <= 4 else 0)
    
    # 6. Better booking window
    df['booking_urgency'] = df['days_until_flight'].apply(lambda x: 
        3 if x <= 2 else 2 if x <= 7 else 1 if x <= 14 else 0)
    
    # 7. Route type (short/medium/long)
    df['route_length_category'] = df['route_distance'].apply(lambda x:
        0 if x < 500 else 1 if x < 1000 else 2 if x < 1500 else 3)
    
    # 8. Airline tier (based on average price)
    airline_avg_price = df.groupby('airline')['price'].mean().to_dict()
    df['airline_price_tier'] = df['airline'].map(airline_avg_price)
    
    # 9. Relative pricing (vs route average)
    route_avg = df.groupby('route')['price'].transform('mean')
    df['price_deviation_pct'] = ((df['price'] - route_avg) / route_avg * 100)
    
    return df

def load_and_prepare_data():
    """Load data with enhanced features"""
    print("\n" + "="*80)
    print("Loading Data with Enhanced Features")
    print("="*80 + "\n")
    
    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    db = client['flightdb']
    collection = db['flights']
    
    flights_data = list(collection.find({}))
    client.close()
    
    if len(flights_data) == 0:
        raise ValueError("No data in database!")
    
    # Prepare data
    for flight in flights_data:
        if 'search_date' in flight:
            try:
                date_parts = flight['search_date'].split('/')
                search_dt = datetime(int(date_parts[2]), int(date_parts[1]), int(date_parts[0]))
            except:
                search_dt = datetime.now()
        else:
            search_dt = datetime.now()
        
        flight['day_of_week'] = search_dt.strftime('%A')
        flight['day_of_week_num'] = search_dt.weekday()
        flight['month'] = search_dt.month
        flight['is_weekend'] = 1 if search_dt.weekday() >= 5 else 0
        
        origin = flight.get('origin', 'Unknown')
        destination = flight.get('destination', 'Unknown')
        flight['days_until_flight'] = 7
        flight['scraped_date'] = flight.get('scraped_at', datetime.now())
        flight['from'] = origin
        flight['to'] = destination
        flight['airline'] = flight.get('airline', 'Unknown')
        
        # Extract departure hour
        try:
            if 'departure_time' in flight and ':' in str(flight['departure_time']):
                flight['departure_hour'] = int(str(flight['departure_time']).split(':')[0])
            else:
                flight['departure_hour'] = 12
        except:
            flight['departure_hour'] = 12
    
    df = pd.DataFrame(flights_data)
    print(f"✅ Loaded {len(df)} records")
    
    # Filter domestic
    print(f"\n🔍 Filtering domestic flights...")
    df = df[(df['price'] < 50000) & (df['stops'] <= 2)]
    print(f"   After filter: {len(df)} flights")
    
    return df

def train_improved_model():
    """Train with enhanced features and hyperparameter tuning"""
    
    # Load data
    df = load_and_prepare_data()
    
    # Apply standard feature engineering
    print(f"\n🔧 Engineering standard features...")
    df = prepare_features(df)
    
    # Add advanced features
    print(f"🔧 Adding advanced features...")
    df = add_advanced_features(df)
    
    # Remove price_deviation_pct from features (it uses price)
    df = df.drop(columns=['price_deviation_pct'], errors='ignore')
    
    # Enhanced feature list
    enhanced_features = get_feature_columns() + [
        'route_distance',
        'price_per_km',
        'route_competition',
        'airline_route_frequency',
        'is_peak_hour',
        'is_red_eye',
        'booking_urgency',
        'route_length_category',
        'airline_price_tier',
    ]
    
    # Prepare data
    X = df[enhanced_features]
    y = df['price']
    
    print(f"\n📊 Enhanced Dataset Info:")
    print(f"   Features: {len(enhanced_features)}")
    print(f"   Samples: {len(df)}")
    print(f"   Price range: ₹{y.min():.0f} - ₹{y.max():.0f}")
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"\n✂️  Split: {len(X_train)} train, {len(X_test)} test")
    
    # Train with optimized hyperparameters
    print(f"\n🌲 Training Random Forest with optimized parameters...")
    
    model = RandomForestRegressor(
        n_estimators=200,        # More trees
        max_depth=20,            # Deeper trees
        min_samples_split=3,     # More flexible splitting
        min_samples_leaf=1,      # Allow more granular leaves
        max_features='sqrt',
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    train_pred = model.predict(X_train)
    test_pred = model.predict(X_test)
    
    train_mae = mean_absolute_error(y_train, train_pred)
    train_r2 = r2_score(y_train, train_pred)
    
    test_mae = mean_absolute_error(y_test, test_pred)
    test_rmse = np.sqrt(mean_squared_error(y_test, test_pred))
    test_r2 = r2_score(y_test, test_pred)
    test_mape = np.mean(np.abs((y_test - test_pred) / y_test)) * 100
    
    print(f"\n📈 Model Evaluation:")
    print(f"   {'='*70}")
    print(f"   Training Set:")
    print(f"      MAE: ₹{train_mae:.2f}")
    print(f"      R²:  {train_r2:.4f}")
    print(f"")
    print(f"   Test Set:")
    print(f"      MAE:   ₹{test_mae:.2f}")
    print(f"      RMSE:  ₹{test_rmse:.2f}")
    print(f"      R²:    {test_r2:.4f}")
    print(f"      MAPE:  {test_mape:.2f}%")
    print(f"   {'='*70}")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': enhanced_features,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print(f"\n🔍 Top 15 Most Important Features:")
    for idx, row in feature_importance.head(15).iterrows():
        print(f"   {row['feature']:<30} {row['importance']:.4f}")
    
    # Save model
    model_dir = os.path.join(os.path.dirname(__file__), 'models')
    os.makedirs(model_dir, exist_ok=True)
    
    # Create mappings
    mappings = {}
    for col in df.columns:
        if col.endswith('_code') or col.endswith('_map'):
            mappings[col] = df[col].drop_duplicates().to_dict()
    
    # Save enhanced model
    joblib.dump(model, os.path.join(model_dir, 'fare_prediction_model.pkl'))
    joblib.dump(mappings, os.path.join(model_dir, 'feature_mappings.pkl'))
    joblib.dump({
        'feature_columns': enhanced_features,
        'train_mae': train_mae,
        'test_mae': test_mae,
        'test_r2': test_r2,
        'route_distances': ROUTE_DISTANCES,
    }, os.path.join(model_dir, 'model_metadata.pkl'))
    
    print(f"\n💾 Enhanced model saved:")
    print(f"   {model_dir}/fare_prediction_model.pkl")
    
    # Sample predictions
    print(f"\n📋 Sample Predictions (First 10):")
    print(f"  {'actual':>8}  {'predicted':>11}  {'error':>10}")
    for i in range(min(10, len(y_test))):
        actual = y_test.iloc[i]
        pred = test_pred[i]
        error = actual - pred
        print(f"  {actual:>8.0f}  {pred:>11.2f}  {error:>10.2f}")
    
    print(f"\n{'='*80}")
    print(f"✅ Training Complete with Enhanced Features!")
    print(f"{'='*80}\n")
    
    return model, test_r2, test_mae

if __name__ == '__main__':
    model, r2, mae = train_improved_model()
    print(f"\n🎯 Final Results:")
    print(f"   R² Score: {r2:.2%} (variance explained)")
    print(f"   MAE: ₹{mae:,.0f} (average error)")
