"""
Feature Engineering for Flight Fare Prediction
==============================================
Prepares data for ML model training.
"""
import pandas as pd
import numpy as np
from datetime import datetime

def prepare_features(df):
    """
    Engineer features from raw flight data.
    
    Args:
        df: DataFrame with raw flight data from MongoDB
        
    Returns:
        DataFrame with ML-ready features
    """
    df = df.copy()
    
    # 1. Encode categorical variables
    df['airline_code'] = df['airline'].astype('category').cat.codes
    df['from_code'] = df['from'].astype('category').cat.codes
    df['to_code'] = df['to'].astype('category').cat.codes
    df['route_code'] = df['route'].astype('category').cat.codes
    
    # 2. Time-based features
    if 'departure_hour' not in df.columns:
        df['departure_hour'] = df['departure_time'].apply(extract_hour)
    
    # Time of day categories
    df['time_of_day'] = df['departure_hour'].apply(categorize_time_of_day)
    df['time_of_day_code'] = df['time_of_day'].astype('category').cat.codes
    
    # 3. Advanced booking features
    df['is_advance_booking'] = df['days_until_flight'] > 14
    df['is_last_minute'] = df['days_until_flight'] < 3
    
    # Booking window categories
    def booking_window(days):
        if days <= 3:
            return 'last_minute'
        elif days <= 7:
            return 'week_before'
        elif days <= 14:
            return 'two_weeks'
        elif days <= 30:
            return 'month_before'
        else:
            return 'advance'
    
    df['booking_window'] = df['days_until_flight'].apply(booking_window)
    df['booking_window_code'] = df['booking_window'].astype('category').cat.codes
    
    # 4. Flight characteristics
    df['is_direct'] = df['stops'] == 0
    df['has_stops'] = df['stops'] > 0
    
    # 5. Temporal features
    df['is_weekend'] = df['day_of_week_num'] >= 5
    df['is_monday'] = df['day_of_week_num'] == 0
    df['is_friday'] = df['day_of_week_num'] == 4
    
    # Season (assuming Northern Hemisphere)
    def get_season(month):
        if month in [12, 1, 2]:
            return 'winter'
        elif month in [3, 4, 5]:
            return 'spring'
        elif month in [6, 7, 8]:
            return 'summer'
        else:
            return 'fall'
    
    df['season'] = df['month'].apply(get_season)
    df['season_code'] = df['season'].astype('category').cat.codes
    
    # 6. Price statistics by route (for normalization)
    route_stats = df.groupby('route')['price'].agg(['mean', 'std', 'min', 'max']).reset_index()
    route_stats.columns = ['route', 'route_avg_price', 'route_std_price', 'route_min_price', 'route_max_price']
    df = df.merge(route_stats, on='route', how='left')
    
    # Price deviation from route average
    df['price_vs_avg'] = (df['price'] - df['route_avg_price']) / df['route_std_price'].replace(0, 1)
    
    return df

def extract_hour(time_str):
    """Extract hour from time string like '14:30' or 'N/A'"""
    if not isinstance(time_str, str) or time_str == 'N/A':
        return 12  # Default to noon
    try:
        return int(time_str.split(':')[0])
    except:
        return 12

def categorize_time_of_day(hour):
    """Categorize hour into time periods"""
    if 5 <= hour < 12:
        return 'morning'
    elif 12 <= hour < 17:
        return 'afternoon'
    elif 17 <= hour < 21:
        return 'evening'
    else:
        return 'night'

def get_feature_columns():
    """Return list of feature columns for model training"""
    return [
        'airline_code',
        'from_code',
        'to_code',
        'route_code',
        'days_until_flight',
        'stops',
        'departure_hour',
        'time_of_day_code',
        'day_of_week_num',
        'month',
        'is_weekend',
        'is_monday',
        'is_friday',
        'is_direct',
        'is_advance_booking',
        'is_last_minute',
        'booking_window_code',
        'season_code',
    ]

def get_mappings(df):
    """
    Extract category mappings for later prediction.
    
    Returns:
        dict: Mappings for categorical features
    """
    mappings = {
        'airline_map': dict(enumerate(df['airline'].astype('category').cat.categories)),
        'from_map': dict(enumerate(df['from'].astype('category').cat.categories)),
        'to_map': dict(enumerate(df['to'].astype('category').cat.categories)),
        'route_map': dict(enumerate(df['route'].astype('category').cat.categories)),
        'time_of_day_map': dict(enumerate(df['time_of_day'].astype('category').cat.categories)),
        'booking_window_map': dict(enumerate(df['booking_window'].astype('category').cat.categories)),
        'season_map': dict(enumerate(df['season'].astype('category').cat.categories)),
    }
    return mappings
