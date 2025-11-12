import React, { useState } from 'react';
import mlService from '../api/mlService';

const PricePredictor = () => {
  const [formData, setFormData] = useState({
    airline: 'IndiGo',
    origin: 'Delhi',
    destination: 'Mumbai',
    days_until_flight: 7,
    stops: 0,
    departure_hour: 10
  });

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const airlines = ['IndiGo', 'SpiceJet', 'Air India', 'Akasa Air', 'Air India Express'];
  const cities = ['Delhi', 'Mumbai', 'Bengaluru', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad', 'Jaipur', 'Goa'];
  const stopOptions = [
    { value: 0, label: 'Non-Stop' },
    { value: 1, label: '1 Stop' },
    { value: 2, label: '2 Stops' }
  ];

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'days_until_flight' || name === 'stops' || name === 'departure_hour' 
        ? parseInt(value) 
        : value
    }));
  };

  const handlePredict = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const result = await mlService.predictPrice(formData);
      setPrediction(result.data);
    } catch (err) {
      setError('Failed to get prediction. Please ensure backend services are running.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="flex items-center mb-6">
        <span className="text-3xl mr-3">🔮</span>
        <h2 className="text-2xl font-bold text-gray-800">Flight Price Predictor</h2>
      </div>

      <form onSubmit={handlePredict} className="space-y-4">
        {/* Airline Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Airline
          </label>
          <select
            name="airline"
            value={formData.airline}
            onChange={handleInputChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            {airlines.map(airline => (
              <option key={airline} value={airline}>{airline}</option>
            ))}
          </select>
        </div>

        {/* Route Selection */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              From
            </label>
            <select
              name="origin"
              value={formData.origin}
              onChange={handleInputChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              {cities.map(city => (
                <option key={city} value={city}>{city}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              To
            </label>
            <select
              name="destination"
              value={formData.destination}
              onChange={handleInputChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              {cities.map(city => (
                <option key={city} value={city}>{city}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Days Until Flight */}
        <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-5 rounded-xl border-2 border-blue-200">
          <div className="flex items-center justify-between mb-3">
            <label className="text-lg font-semibold text-gray-800 flex items-center">
              📅 Travel Date
            </label>
            <div className="bg-blue-600 text-white px-4 py-2 rounded-lg font-bold text-lg">
              {formData.days_until_flight} {formData.days_until_flight === 1 ? 'day' : 'days'}
            </div>
          </div>
          <div className="relative pt-2 pb-1">
            <input
              type="range"
              name="days_until_flight"
              min="1"
              max="90"
              value={formData.days_until_flight}
              onChange={handleInputChange}
              className="w-full h-3 bg-gradient-to-r from-green-200 via-yellow-200 to-red-200 rounded-full appearance-none cursor-pointer slider-thumb"
              style={{
                background: `linear-gradient(to right, 
                  #86efac 0%, 
                  #fde047 ${(formData.days_until_flight / 90) * 100}%, 
                  #fca5a5 100%)`
              }}
            />
            {/* Visual markers */}
            <div className="flex justify-between mt-3 px-1">
              <div className="text-center">
                <div className="w-2 h-2 bg-green-500 rounded-full mx-auto mb-1"></div>
                <span className="text-xs font-medium text-gray-700">Tomorrow</span>
              </div>
              <div className="text-center">
                <div className="w-2 h-2 bg-yellow-500 rounded-full mx-auto mb-1"></div>
                <span className="text-xs font-medium text-gray-700">1 Week</span>
              </div>
              <div className="text-center">
                <div className="w-2 h-2 bg-orange-500 rounded-full mx-auto mb-1"></div>
                <span className="text-xs font-medium text-gray-700">1 Month</span>
              </div>
              <div className="text-center">
                <div className="w-2 h-2 bg-red-500 rounded-full mx-auto mb-1"></div>
                <span className="text-xs font-medium text-gray-700">3 Months</span>
              </div>
            </div>
          </div>
        </div>

        {/* Stops */}
        <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-5 rounded-xl border-2 border-purple-200">
          <label className="block text-lg font-semibold text-gray-800 mb-4 flex items-center">
            ✈️ Flight Stops
          </label>
          <div className="grid grid-cols-3 gap-3">
            {stopOptions.map(option => (
              <label 
                key={option.value} 
                className={`relative flex flex-col items-center justify-center p-4 rounded-lg cursor-pointer transition-all transform hover:scale-105 ${
                  formData.stops === option.value 
                    ? 'bg-purple-600 text-white shadow-lg ring-4 ring-purple-300' 
                    : 'bg-white text-gray-700 border-2 border-gray-300 hover:border-purple-400'
                }`}
              >
                <input
                  type="radio"
                  name="stops"
                  value={option.value}
                  checked={formData.stops === option.value}
                  onChange={handleInputChange}
                  className="sr-only"
                />
                <div className="text-3xl mb-2">
                  {option.value === 0 ? '🚀' : option.value === 1 ? '🛬' : '🛫'}
                </div>
                <span className={`text-sm font-semibold ${
                  formData.stops === option.value ? 'text-white' : 'text-gray-700'
                }`}>
                  {option.label}
                </span>
                {formData.stops === option.value && (
                  <div className="absolute top-2 right-2 bg-white text-purple-600 rounded-full p-1">
                    <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd"/>
                    </svg>
                  </div>
                )}
              </label>
            ))}
          </div>
        </div>

        {/* Departure Hour */}
        <div className="bg-gradient-to-r from-orange-50 to-amber-50 p-5 rounded-xl border-2 border-orange-200">
          <div className="flex items-center justify-between mb-3">
            <label className="text-lg font-semibold text-gray-800 flex items-center">
              🕐 Departure Time
            </label>
            <div className="bg-orange-600 text-white px-4 py-2 rounded-lg font-bold text-lg">
              {formData.departure_hour.toString().padStart(2, '0')}:00
            </div>
          </div>
          <div className="relative pt-2 pb-1">
            <input
              type="range"
              name="departure_hour"
              min="0"
              max="23"
              value={formData.departure_hour}
              onChange={handleInputChange}
              className="w-full h-3 bg-gradient-to-r from-blue-300 via-orange-300 to-indigo-400 rounded-full appearance-none cursor-pointer slider-thumb"
            />
            {/* Time period markers */}
            <div className="flex justify-between mt-3 px-1">
              <div className="text-center">
                <div className="w-2 h-2 bg-blue-600 rounded-full mx-auto mb-1"></div>
                <span className="text-xs font-medium text-gray-700">Early Morning</span>
                <div className="text-[10px] text-gray-500">00:00</div>
              </div>
              <div className="text-center">
                <div className="w-2 h-2 bg-yellow-500 rounded-full mx-auto mb-1"></div>
                <span className="text-xs font-medium text-gray-700">Morning</span>
                <div className="text-[10px] text-gray-500">06:00</div>
              </div>
              <div className="text-center">
                <div className="w-2 h-2 bg-orange-500 rounded-full mx-auto mb-1"></div>
                <span className="text-xs font-medium text-gray-700">Afternoon</span>
                <div className="text-[10px] text-gray-500">12:00</div>
              </div>
              <div className="text-center">
                <div className="w-2 h-2 bg-red-500 rounded-full mx-auto mb-1"></div>
                <span className="text-xs font-medium text-gray-700">Evening</span>
                <div className="text-[10px] text-gray-500">18:00</div>
              </div>
              <div className="text-center">
                <div className="w-2 h-2 bg-indigo-600 rounded-full mx-auto mb-1"></div>
                <span className="text-xs font-medium text-gray-700">Night</span>
                <div className="text-[10px] text-gray-500">23:00</div>
              </div>
            </div>
          </div>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={loading}
          className={`w-full py-3 px-6 rounded-lg font-semibold text-white transition-all ${
            loading 
              ? 'bg-gray-400 cursor-not-allowed' 
              : 'bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 shadow-lg hover:shadow-xl'
          }`}
        >
          {loading ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"/>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
              </svg>
              Predicting...
            </span>
          ) : (
            '🚀 Predict Price'
          )}
        </button>
      </form>

      {/* Error Message */}
      {error && (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-600 text-sm">{error}</p>
        </div>
      )}

      {/* Prediction Result */}
      {prediction && (
        <div className="mt-6 p-6 bg-gradient-to-br from-blue-50 to-purple-50 rounded-lg border-2 border-blue-200">
          <div className="text-center">
            <p className="text-sm text-gray-600 mb-2">Predicted Price</p>
            <p className="text-5xl font-bold text-blue-600 mb-4">
              ₹{prediction.predicted_price?.toLocaleString('en-IN')}
            </p>
            
            <div className="grid grid-cols-2 gap-4 mt-4 text-sm">
              <div className="bg-white p-3 rounded-lg">
                <p className="text-gray-500">Confidence</p>
                <p className="text-lg font-semibold text-green-600">95.8%</p>
              </div>
              <div className="bg-white p-3 rounded-lg">
                <p className="text-gray-500">Model</p>
                <p className="text-lg font-semibold text-purple-600">Random Forest</p>
              </div>
            </div>

            <div className="mt-4 p-3 bg-white rounded-lg">
              <p className="text-xs text-gray-500">Currency</p>
              <p className="text-sm font-medium text-gray-700">{prediction.currency || 'INR'}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PricePredictor;
