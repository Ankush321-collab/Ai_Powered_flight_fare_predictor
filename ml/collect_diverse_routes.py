"""
Comprehensive Multi-Route Data Collection
=========================================
Collects data for 20 diverse routes (10 domestic + 10 international)
for robust ML model training.

This will take ~2-3 hours to complete all routes.
You can run it in batches or let it run overnight.

Usage:
    python collect_diverse_routes.py
    python collect_diverse_routes.py --batch domestic  # Only domestic
    python collect_diverse_routes.py --batch international  # Only international
"""
import os
import sys
import argparse
from datetime import datetime, timedelta
from pymongo import MongoClient
from dotenv import load_dotenv
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from scraper_nlp.providers.easymytrip import search_flights

# Load environment
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(env_path)

# 🇮🇳 Top 10 Domestic Routes (India)
DOMESTIC_ROUTES = [
    ('Delhi', 'Mumbai'),           # DEL–BOM
    ('Bengaluru', 'Delhi'),        # BLR–DEL
    ('Mumbai', 'Chennai'),         # BOM–MAA
    ('Kolkata', 'Delhi'),          # CCU–DEL
    ('Hyderabad', 'Bengaluru'),    # HYD–BLR
    ('Pune', 'Delhi'),             # PNQ–DEL
    ('Ahmedabad', 'Mumbai'),       # AMD–BOM
    ('Jaipur', 'Delhi'),           # JAI–DEL
    ('Lucknow', 'Mumbai'),         # LKO–BOM
    ('Goa', 'Bengaluru'),          # GOI–BLR
]

# 🌍 Top 10 International Routes
INTERNATIONAL_ROUTES = [
    ('Delhi', 'Dubai'),            # DEL–DXB
    ('Mumbai', 'Singapore'),       # BOM–SIN
    ('Chennai', 'Kuala Lumpur'),   # MAA–KUL
    ('Delhi', 'London'),           # DEL–LHR
    ('Mumbai', 'New York'),        # BOM–JFK
    ('Hyderabad', 'Doha'),         # HYD–DOH
    ('Kolkata', 'Bangkok'),        # CCU–BKK
    ('Bengaluru', 'Frankfurt'),    # BLR–FRA
    ('Delhi', 'Toronto'),          # DEL–YYZ
    ('Mumbai', 'Muscat'),          # BOM–MCT
]

def collect_route_data(origin, destination, search_date, mongo_collection, route_type='domestic'):
    """Collect data for a single route"""
    print(f"\n{'='*80}")
    print(f"🔍 Route: {origin} → {destination} ({route_type.upper()})")
    print(f"📅 Date: {search_date}")
    print(f"{'='*80}")
    
    try:
        # Scrape flights (visible browser for reliability)
        print("⏳ Searching flights (please wait 30 seconds)...")
        flights = search_flights(
            origin,
            destination,
            search_date,
            headless=False,  # Visible browser (more reliable)
            wait_sec=30      # Longer wait for international routes
        )
        
        if not flights:
            print("❌ No flights found")
            return 0
        
        print(f"✅ Found {len(flights)} flights")
        
        # Add metadata
        for flight in flights:
            flight['origin'] = origin
            flight['destination'] = destination
            flight['search_date'] = search_date
            flight['scraped_at'] = datetime.now()
            flight['route'] = f"{origin}→{destination}"
            flight['route_type'] = route_type
        
        # Save to MongoDB
        result = mongo_collection.insert_many(flights)
        
        # Show price range
        prices = [f['price'] for f in flights]
        cheapest = min(flights, key=lambda x: x['price'])
        expensive = max(flights, key=lambda x: x['price'])
        
        print(f"\n💰 Price Analysis:")
        print(f"   Cheapest: {cheapest['airline']} {cheapest['flight_number']} - ₹{cheapest['price']:,.0f}")
        print(f"   Most Expensive: {expensive['airline']} - ₹{expensive['price']:,.0f}")
        print(f"   Average: ₹{sum(prices)/len(prices):,.0f}")
        print(f"   Range: ₹{min(prices):,.0f} - ₹{max(prices):,.0f}")
        print(f"\n✅ Saved {len(result.inserted_ids)} flights to MongoDB")
        
        return len(result.inserted_ids)
        
    except Exception as e:
        print(f"❌ Error: {str(e)[:100]}")
        import traceback
        traceback.print_exc()
        return 0

def main():
    parser = argparse.ArgumentParser(description='Collect diverse route data')
    parser.add_argument('--batch', choices=['domestic', 'international', 'all'],
                       default='all', help='Which routes to collect')
    parser.add_argument('--delay', type=int, default=60,
                       help='Delay between routes in seconds (default: 60)')
    
    args = parser.parse_args()
    
    # Connect to MongoDB
    mongo_uri = os.getenv('MONGO_URI')
    if not mongo_uri:
        print("❌ Error: MONGO_URI not found in .env")
        return
    
    client = MongoClient(mongo_uri)
    db = client['flightdb']
    collection = db['flights']
    
    # Determine which routes to collect
    if args.batch == 'domestic':
        routes = DOMESTIC_ROUTES
        route_type = 'domestic'
        print("\n🇮🇳 Collecting DOMESTIC routes only")
    elif args.batch == 'international':
        routes = INTERNATIONAL_ROUTES
        route_type = 'international'
        print("\n🌍 Collecting INTERNATIONAL routes only")
    else:
        routes = DOMESTIC_ROUTES + INTERNATIONAL_ROUTES
        route_type = 'mixed'
        print("\n🌏 Collecting ALL routes (domestic + international)")
    
    # Search 7 days ahead
    search_date = (datetime.now() + timedelta(days=7)).strftime('%d/%m/%Y')
    
    print("\n" + "="*80)
    print(f"📊 COMPREHENSIVE DATA COLLECTION")
    print("="*80)
    print(f"Total routes: {len(routes)}")
    print(f"Date: {search_date}")
    print(f"Delay between routes: {args.delay} seconds")
    print(f"Estimated time: {len(routes) * 2} - {len(routes) * 3} minutes")
    print("="*80)
    
    input("\n⏸️  Press ENTER to start collection (or Ctrl+C to cancel)...")
    
    # Collect data
    total_flights = 0
    successful_routes = 0
    failed_routes = []
    
    start_time = time.time()
    
    for i, (origin, dest) in enumerate(routes, 1):
        # Determine if this specific route is domestic or international
        if routes == DOMESTIC_ROUTES:
            current_type = 'domestic'
        elif routes == INTERNATIONAL_ROUTES:
            current_type = 'international'
        else:
            current_type = 'domestic' if (origin, dest) in DOMESTIC_ROUTES else 'international'
        
        print(f"\n\n{'#'*80}")
        print(f"Progress: [{i}/{len(routes)}] - {(i/len(routes)*100):.1f}% Complete")
        print(f"{'#'*80}")
        
        flights_saved = collect_route_data(origin, dest, search_date, collection, current_type)
        
        if flights_saved > 0:
            total_flights += flights_saved
            successful_routes += 1
        else:
            failed_routes.append(f"{origin}→{dest}")
        
        # Delay between routes (except for last one)
        if i < len(routes):
            print(f"\n⏳ Waiting {args.delay} seconds before next route...")
            time.sleep(args.delay)
    
    # Final summary
    elapsed_time = (time.time() - start_time) / 60
    
    print("\n\n" + "="*80)
    print("📊 COLLECTION COMPLETE!")
    print("="*80)
    print(f"✅ Successful routes: {successful_routes}/{len(routes)} ({successful_routes/len(routes)*100:.1f}%)")
    print(f"✈️  Total flights collected: {total_flights}")
    print(f"⏱️  Time taken: {elapsed_time:.1f} minutes")
    print(f"📁 Saved to: flightdb.flights")
    
    if failed_routes:
        print(f"\n❌ Failed routes ({len(failed_routes)}):")
        for route in failed_routes:
            print(f"   - {route}")
    
    # Check database stats
    total_in_db = collection.count_documents({})
    unique_routes = collection.distinct('route')
    
    print(f"\n📊 Database Statistics:")
    print(f"   Total flights in DB: {total_in_db}")
    print(f"   Unique routes: {len(unique_routes)}")
    print(f"   Routes: {', '.join(unique_routes[:10])}{'...' if len(unique_routes) > 10 else ''}")
    
    print(f"\n💡 Next Steps:")
    print(f"   1. Review collected data")
    print(f"   2. Train ML model: python train_model.py")
    print(f"   3. Test predictions: python test_predictions.py")
    print("="*80 + "\n")
    
    client.close()

if __name__ == '__main__':
    main()
