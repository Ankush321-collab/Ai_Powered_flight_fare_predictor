"""
Collect Real Flight Data for 30 Days - All Routes
==================================================
Scrapes REAL flight data from EasyMyTrip for 30 days across all major routes
and saves to MongoDB.

This will take approximately 6-8 hours to complete.
"""
import os
import sys
import time
import subprocess
from datetime import datetime, timedelta
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(env_path)

# Major Indian routes
ROUTES = [
    ('Delhi', 'Mumbai'),
    ('Delhi', 'Bengaluru'),
    ('Delhi', 'Kolkata'),
    ('Delhi', 'Chennai'),
    ('Delhi', 'Hyderabad'),
    ('Mumbai', 'Bengaluru'),
    ('Mumbai', 'Chennai'),
    ('Mumbai', 'Kolkata'),
    ('Mumbai', 'Hyderabad'),
    ('Bengaluru', 'Chennai'),
    ('Bengaluru', 'Kolkata'),
    ('Bengaluru', 'Hyderabad'),
    ('Delhi', 'Goa'),
    ('Mumbai', 'Goa'),
    ('Delhi', 'Jaipur'),
    ('Delhi', 'Ahmedabad'),
    ('Mumbai', 'Pune'),
    ('Bengaluru', 'Goa'),
]

def test_mongodb_connection():
    """Test MongoDB connection"""
    print("\n" + "="*80)
    print("Testing MongoDB Connection")
    print("="*80 + "\n")
    
    mongo_uri = os.getenv('MONGO_URI')
    if not mongo_uri:
        print("❌ MONGO_URI not found in .env file")
        return False
    
    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=10000)
        db = client['flightdb']
        
        # Test connection
        client.server_info()
        
        print(f"✅ MongoDB Connected Successfully!")
        print(f"📊 Database: {db.name}")
        print(f"📁 Collections: {db.list_collection_names()}")
        
        # Check current data
        flights_count = db.flights.count_documents({})
        print(f"📈 Current flights in DB: {flights_count}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ MongoDB Connection Failed: {e}")
        print("\n💡 Solutions:")
        print("1. Check if IP is whitelisted in MongoDB Atlas")
        print("2. Go to: https://cloud.mongodb.com")
        print("3. Network Access → Add IP Address → Allow from Anywhere (0.0.0.0/0)")
        print("4. Run: ipconfig /flushdns")
        return False

def scrape_route_for_date(origin, destination, date_str, delay=5):
    """Scrape one route for one date"""
    try:
        # Call save_to_mongo.py script
        cmd = [
            'python',
            'save_to_mongo.py',
            '--from', origin,
            '--to', destination,
            '--date', date_str,
            '--headless'
        ]
        
        result = subprocess.run(
            cmd,
            cwd=os.path.dirname(os.path.abspath(__file__)),
            capture_output=True,
            text=True,
            timeout=120  # 2 minutes timeout
        )
        
        # Check if successful
        if result.returncode == 0:
            # Count saved flights from output
            output = result.stdout
            if 'Saved' in output or 'saved' in output:
                return True
        
        return False
        
    except subprocess.TimeoutExpired:
        print(f"⏱️  Timeout scraping {origin}→{destination} on {date_str}")
        return False
    except Exception as e:
        print(f"❌ Error scraping {origin}→{destination}: {e}")
        return False
    finally:
        # Always add delay between requests
        time.sleep(delay)

def collect_real_data(days=30, start_date=None):
    """Collect real flight data for multiple days and routes"""
    print("\n" + "="*80)
    print("🚀 Starting Real Flight Data Collection")
    print("="*80 + "\n")
    
    # Use provided start date or today
    if start_date:
        base_date = datetime.strptime(start_date, '%d-%m-%Y')
    else:
        base_date = datetime.now()
    
    print(f"📅 Date Range: {base_date.strftime('%d/%m/%Y')} to {(base_date + timedelta(days=days-1)).strftime('%d/%m/%Y')}")
    print(f"🛫 Routes: {len(ROUTES)}")
    print(f"📊 Total Searches: {len(ROUTES) * days}")
    print(f"⏱️  Estimated Time: {(len(ROUTES) * days * 7) / 60:.1f} minutes\n")
    
    total_searches = len(ROUTES) * days
    successful = 0
    failed = 0
    
    start_time = time.time()
    
    for day_offset in range(days):
        current_date = base_date + timedelta(days=day_offset)
        date_str = current_date.strftime('%d/%m/%Y')
        
        print(f"\n{'='*80}")
        print(f"📅 Day {day_offset + 1}/{days}: {date_str}")
        print(f"{'='*80}\n")
        
        for idx, (origin, destination) in enumerate(ROUTES, 1):
            progress = (day_offset * len(ROUTES) + idx) / total_searches * 100
            
            print(f"[{progress:5.1f}%] {origin:15s} → {destination:15s} ... ", end='', flush=True)
            
            success = scrape_route_for_date(origin, destination, date_str, delay=5)
            
            if success:
                successful += 1
                print("✅ OK")
            else:
                failed += 1
                print("❌ FAILED")
        
        # Longer pause between days
        if day_offset < days - 1:
            print(f"\n⏸️  Pausing 10 seconds before next day...")
            time.sleep(10)
    
    elapsed_time = time.time() - start_time
    
    # Final summary
    print("\n" + "="*80)
    print("📊 Collection Complete!")
    print("="*80 + "\n")
    print(f"✅ Successful: {successful}/{total_searches}")
    print(f"❌ Failed: {failed}/{total_searches}")
    print(f"📈 Success Rate: {successful/total_searches*100:.1f}%")
    print(f"⏱️  Total Time: {elapsed_time/60:.1f} minutes")
    
    # Check MongoDB for final count
    try:
        client = MongoClient(os.getenv('MONGO_URI'), serverSelectionTimeoutMS=10000)
        db = client['flightdb']
        final_count = db.flights.count_documents({})
        print(f"💾 Total Flights in MongoDB: {final_count}")
        client.close()
    except:
        print("⚠️  Could not verify MongoDB count")
    
    return successful, failed

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Collect real flight data for 30 days')
    parser.add_argument('--days', type=int, default=30, help='Number of days to collect (default: 30)')
    parser.add_argument('--start-date', type=str, help='Start date in DD-MM-YYYY format (default: today)')
    parser.add_argument('--test-connection', action='store_true', help='Only test MongoDB connection')
    
    args = parser.parse_args()
    
    # Test MongoDB connection first
    if not test_mongodb_connection():
        print("\n❌ Please fix MongoDB connection before proceeding!")
        sys.exit(1)
    
    if args.test_connection:
        print("\n✅ Connection test successful! You can now collect data.")
        sys.exit(0)
    
    # Collect data
    print("\n⚠️  WARNING: This will make hundreds of web requests and take several hours!")
    print("Press Ctrl+C at any time to stop.\n")
    
    try:
        time.sleep(3)  # Give user time to read warning
        successful, failed = collect_real_data(days=args.days, start_date=args.start_date)
        
        print(f"\n✅ Data collection finished!")
        print(f"💡 Next step: python ../ml/train_improved_model.py")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user. Data collected so far is saved in MongoDB.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
