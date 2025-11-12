import React, { useState } from 'react';
import mlService from '../api/mlService';

const BookingRecommendation = () => {
  const [formData, setFormData] = useState({
    current_price: 5500,
    airline: 'IndiGo',
    origin: 'Delhi',
    destination: 'Mumbai',
    days_until_flight: 7
  });

  const [recommendation, setRecommendation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const airlines = ['IndiGo', 'SpiceJet', 'Air India', 'Akasa Air', 'Air India Express'];
  const cities = ['Delhi', 'Mumbai', 'Bengaluru', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad', 'Jaipur', 'Goa'];

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'current_price' || name === 'days_until_flight' 
        ? parseInt(value) 
        : value
    }));
  };

  const handleGetRecommendation = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const result = await mlService.getBookingRecommendation(formData);
      setRecommendation(result.data);
    } catch (err) {
      setError('Failed to get recommendation. Please ensure backend services are running.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const isGoodDeal = recommendation?.action === 'book_now';
  const savingsPercentage = recommendation?.potential_savings && recommendation?.current_price
    ? Math.round((recommendation.potential_savings / recommendation.current_price) * 100)
    : 0;

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="flex items-center mb-6">
        <span className="text-3xl mr-3">🎯</span>
        <h2 className="text-2xl font-bold text-gray-800">Booking Recommendation</h2>
      </div>

      {/* Form */}
      <form onSubmit={handleGetRecommendation} className="space-y-4 mb-6">
        {/* Current Price */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Current Flight Price: ₹{formData.current_price.toLocaleString('en-IN')}
          </label>
          <input
            type="range"
            name="current_price"
            min="2000"
            max="20000"
            step="500"
            value={formData.current_price}
            onChange={handleInputChange}
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
          />
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>₹2,000</span>
            <span>₹20,000</span>
          </div>
        </div>

        {/* Airline */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Airline
          </label>
          <select
            name="airline"
            value={formData.airline}
            onChange={handleInputChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            {airlines.map(airline => (
              <option key={airline} value={airline}>{airline}</option>
            ))}
          </select>
        </div>

        {/* Route */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              From
            </label>
            <select
              name="origin"
              value={formData.origin}
              onChange={handleInputChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
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
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
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
              📅 Days Until Flight
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
              max="30"
              value={formData.days_until_flight}
              onChange={handleInputChange}
              className="w-full h-3 bg-gradient-to-r from-green-200 via-yellow-200 to-red-200 rounded-full appearance-none cursor-pointer slider-thumb"
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
                <span className="text-xs font-medium text-gray-700">2 Weeks</span>
              </div>
              <div className="text-center">
                <div className="w-2 h-2 bg-red-500 rounded-full mx-auto mb-1"></div>
                <span className="text-xs font-medium text-gray-700">1 Month</span>
              </div>
            </div>
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className={`w-full py-3 px-6 rounded-lg font-semibold text-white transition-all ${
            loading 
              ? 'bg-gray-400 cursor-not-allowed' 
              : 'bg-gradient-to-r from-purple-500 to-pink-600 hover:from-purple-600 hover:to-pink-700 shadow-lg'
          }`}
        >
          {loading ? 'Analyzing...' : '🔍 Get Recommendation'}
        </button>
      </form>

      {/* Error Message */}
      {error && (
        <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-600 text-sm">{error}</p>
        </div>
      )}

      {/* Recommendation Result */}
      {recommendation && (
        <div className={`p-6 rounded-lg border-2 ${
          isGoodDeal 
            ? 'bg-gradient-to-br from-green-50 to-emerald-50 border-green-300' 
            : 'bg-gradient-to-br from-yellow-50 to-orange-50 border-yellow-300'
        }`}>
          {/* Header */}
          <div className="flex items-center mb-4">
            <span className="text-4xl mr-3">
              {isGoodDeal ? '✅' : '⏳'}
            </span>
            <div>
              <h3 className={`text-2xl font-bold ${
                isGoodDeal ? 'text-green-700' : 'text-orange-700'
              }`}>
                {isGoodDeal ? 'BOOK NOW - Great Deal!' : 'WAIT - Better Prices Ahead'}
              </h3>
              <p className={`text-sm ${
                isGoodDeal ? 'text-green-600' : 'text-orange-600'
              }`}>
                {recommendation.recommendation}
              </p>
            </div>
          </div>

          {/* Price Comparison */}
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div className="bg-white p-4 rounded-lg shadow-sm">
              <p className="text-xs text-gray-500 mb-1">Current Price</p>
              <p className="text-2xl font-bold text-gray-800">
                ₹{recommendation.current_price?.toLocaleString('en-IN')}
              </p>
            </div>

            <div className="bg-white p-4 rounded-lg shadow-sm">
              <p className="text-xs text-gray-500 mb-1">Predicted Price</p>
              <p className="text-2xl font-bold text-blue-600">
                ₹{recommendation.predicted_price?.toLocaleString('en-IN')}
              </p>
            </div>
          </div>

          {/* Savings/Difference */}
          {recommendation.potential_savings && (
            <div className={`p-4 rounded-lg ${
              isGoodDeal ? 'bg-green-100' : 'bg-orange-100'
            }`}>
              <div className="flex items-center justify-between">
                <div>
                  <p className={`text-sm font-medium ${
                    isGoodDeal ? 'text-green-700' : 'text-orange-700'
                  }`}>
                    {isGoodDeal ? '💰 You Save' : '💡 Potential Savings'}
                  </p>
                  <p className={`text-3xl font-bold ${
                    isGoodDeal ? 'text-green-600' : 'text-orange-600'
                  }`}>
                    ₹{Math.abs(recommendation.potential_savings).toLocaleString('en-IN')}
                  </p>
                </div>
                <div className="text-right">
                  <div className={`text-4xl font-bold ${
                    isGoodDeal ? 'text-green-600' : 'text-orange-600'
                  }`}>
                    {Math.abs(savingsPercentage)}%
                  </div>
                  <p className="text-xs text-gray-600">
                    {isGoodDeal ? 'below predicted' : 'above predicted'}
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Confidence Badge */}
          <div className="mt-4 flex items-center justify-center">
            <div className="bg-white px-4 py-2 rounded-full shadow-sm border border-gray-200">
              <span className="text-xs text-gray-600">Confidence: </span>
              <span className="text-sm font-bold text-purple-600">
                {recommendation.confidence || 'High'} (95.8% Model Accuracy)
              </span>
            </div>
          </div>

          {/* Action Button */}
          <div className="mt-6">
            <button className={`w-full py-3 px-6 rounded-lg font-bold text-white shadow-lg transition-all ${
              isGoodDeal 
                ? 'bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700' 
                : 'bg-gradient-to-r from-orange-500 to-yellow-600 hover:from-orange-600 hover:to-yellow-700'
            }`}>
              {isGoodDeal ? '🎫 Book This Flight' : '🔔 Set Price Alert'}
            </button>
          </div>

          {/* Additional Info */}
          {!isGoodDeal && (
            <div className="mt-4 p-3 bg-white rounded-lg text-sm text-gray-600">
              <p className="flex items-center">
                <span className="mr-2">💡</span>
                <span>
                  Our model predicts prices will drop in the coming days. Consider waiting for a better deal.
                </span>
              </p>
            </div>
          )}
        </div>
      )}

      {/* No data message */}
      {!recommendation && !loading && !error && (
        <div className="text-center py-12 text-gray-400">
          <p className="text-lg">Enter flight details to get booking recommendation</p>
        </div>
      )}
    </div>
  );
};

export default BookingRecommendation;
