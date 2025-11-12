"""
Save Scraped Flight Data to MongoDB
====================================
Saves flight data from EasyMyTrip scraper to MongoDB.

Usage:
    python save_to_mongo.py --from "Delhi" --to "Mumbai" --date "15/11/2025"
"""
import os
import sys
import argparse
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

# Import scraper
from providers.easymytrip import search_flights

# Load environment from root directory
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(env_path)

def save_flights_to_mongodb(flights, origin, destination, search_date):
    """Save flight data to MongoDB"""
    mongo_uri = os.getenv('MONGO_URI')
    if not mongo_uri:
        print("❌ Error: MONGO_URI not found in .env file")
        return False
    
    try:
        # Connect to MongoDB
        client = MongoClient(mongo_uri)
        db = client['flightdb']
        collection = db['flights']
        
        print(f"\n✅ Connected to MongoDB")
        print(f"📊 Database: {db.name}")
        print(f"📁 Collection: {collection.name}")
        
        # Prepare documents
        documents = []
        for flight in flights:
            doc = {
                'origin': origin,
                'destination': destination,
                'search_date': search_date,
                'scraped_at': datetime.now(),
                'airline': flight['airline'],
                'flight_number': flight['flight_number'],
                'departure_time': flight['departure_time'],
                'arrival_time': flight['arrival_time'],
                'duration': flight['duration'],
                'stops': flight['stops'],
                'price': flight['price'],
                'currency': flight['currency']
            }
            documents.append(doc)
        
        # Insert into MongoDB
        if documents:
            result = collection.insert_many(documents)
            print(f"\n✅ Saved {len(result.inserted_ids)} flights to MongoDB")
            print(f"💰 Price range: ₹{min(f['price'] for f in flights):.0f} - ₹{max(f['price'] for f in flights):.0f}")
            return True
        else:
            print("⚠️  No flights to save")
            return False
            
    except Exception as e:
        print(f"❌ Error saving to MongoDB: {e}")
        return False
    finally:
        client.close()

def main():
    parser = argparse.ArgumentParser(description='Scrape flights and save to MongoDB')
    parser.add_argument('--from', dest='origin', required=True, help='Origin city (e.g., Delhi)')
    parser.add_argument('--to', dest='destination', required=True, help='Destination city (e.g., Mumbai)')
    parser.add_argument('--date', required=True, help='Travel date (DD/MM/YYYY)')
    parser.add_argument('--headless', action='store_true', help='Run browser in headless mode')
    parser.add_argument('--wait', type=int, default=20, help='Wait time in seconds (default: 20)')
    
    args = parser.parse_args()
    
    print("\n" + "="*80)
    print("Flight Scraper → MongoDB")
    print("="*80)
    print(f"\n🔍 Searching: {args.origin} → {args.destination}")
    print(f"📅 Date: {args.date}")
    print(f"⏳ Wait time: {args.wait} seconds")
    print(f"🖥️  Headless: {args.headless}")
    print("\nPlease wait while scraping...\n")
    
    # Scrape flights
    flights = search_flights(
        args.origin, 
        args.destination, 
        args.date,
        headless=args.headless,
        wait_sec=args.wait
    )
    
    if flights:
        print(f"\n✅ Found {len(flights)} flights")
        
        # Show cheapest
        cheapest = flights[0]
        print(f"\n💰 Cheapest: {cheapest['airline']} {cheapest['flight_number']} - ₹{cheapest['price']:.0f}")
        
        # Save to MongoDB
        success = save_flights_to_mongodb(flights, args.origin, args.destination, args.date)
        
        if success:
            print("\n✅ Done! Data saved to MongoDB")
        else:
            print("\n❌ Failed to save data")
    else:
        print("\n❌ No flights found")

if __name__ == '__main__':
    main()
