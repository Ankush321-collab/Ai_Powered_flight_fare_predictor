"""Test the trained model with various scenarios"""
from predict_enhanced import EnhancedFarePrediction

print("\n" + "="*80)
print("🧪 Testing Newly Trained Model")
print("="*80 + "\n")

# Initialize predictor
predictor = EnhancedFarePrediction()

# Test scenarios
test_cases = [
    ("IndiGo", "Delhi", "Mumbai", 7, "Standard booking"),
    ("Air India", "Delhi", "Mumbai", 7, "Premium airline"),
    ("SpiceJet", "Delhi", "Bengaluru", 7, "Longer route"),
    ("Vistara", "Mumbai", "Chennai", 14, "Advance booking"),
    ("IndiGo", "Delhi", "Mumbai", 1, "Last minute"),
    ("IndiGo", "Delhi", "Mumbai", 30, "Early bird"),
    ("AirAsia India", "Delhi", "Goa", 7, "Budget airline"),
    ("Air India", "Delhi", "Hyderabad", 7, "Medium route"),
]

print(f"{'Airline':<15} {'Route':<20} {'Days':<6} {'Scenario':<20} {'Predicted Price':<15}")
print("-" * 80)

for airline, origin, dest, days, scenario in test_cases:
    try:
        price = predictor.predict(airline, origin, dest, days)
        print(f"{airline:<15} {origin}-{dest:<13} {days:<6} {scenario:<20} ₹{price:>10,.0f}")
    except Exception as e:
        print(f"{airline:<15} {origin}-{dest:<13} {days:<6} {scenario:<20} ERROR: {e}")

print("\n" + "="*80)
print("✅ Model Testing Complete!")
print("="*80 + "\n")
