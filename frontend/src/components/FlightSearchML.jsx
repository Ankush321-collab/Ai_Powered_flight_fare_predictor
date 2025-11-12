import React, { useState } from 'react';
import mlService from '../api/mlService';

const FlightSearchML = () => {
  const [searchData, setSearchData] = useState({
    origin: 'Delhi',
    destination: 'Mumbai',
    date: new Date().toISOString().split('T')[0]
  });

  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const cities = ['Delhi', 'Mumbai', 'Bengaluru', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad', 'Jaipur', 'Goa'];

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setSearchData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const result = await mlService.searchWithPredictions(searchData);
      setResults(result.data);
    } catch (err) {
      setError('Failed to search flights. This feature requires the scraper to run.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="flex items-center mb-6">
        <span className="text-3xl mr-3">🔍</span>
        <h2 className="text-2xl font-bold text-gray-800">Flight Search with ML Predictions</h2>
      </div>

      {/* Search Form */}
      <form onSubmit={handleSearch} className="space-y-4 mb-6">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              From
            </label>
            <select
              name="origin"
              value={searchData.origin}
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
              value={searchData.destination}
              onChange={handleInputChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              {cities.map(city => (
                <option key={city} value={city}>{city}</option>
              ))}
            </select>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Travel Date
          </label>
          <input
            type="date"
            name="date"
            value={searchData.date}
            onChange={handleInputChange}
            min={new Date().toISOString().split('T')[0]}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className={`w-full py-3 px-6 rounded-lg font-semibold text-white transition-all ${
            loading 
              ? 'bg-gray-400 cursor-not-allowed' 
              : 'bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 shadow-lg'
          }`}
        >
          {loading ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"/>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
              </svg>
              Searching & Predicting...
            </span>
          ) : (
            '🚀 Search Flights'
          )}
        </button>
      </form>

      {/* Error Message */}
      {error && (
        <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-600 text-sm">{error}</p>
          <p className="text-xs text-red-500 mt-1">
            Note: This feature runs the web scraper to fetch live flights. Ensure scraper dependencies are installed.
          </p>
        </div>
      )}

      {/* Loading State */}
      {loading && (
        <div className="text-center py-12">
          <div className="animate-pulse space-y-4">
            <div className="h-24 bg-gray-200 rounded-lg"></div>
            <div className="h-24 bg-gray-200 rounded-lg"></div>
            <div className="h-24 bg-gray-200 rounded-lg"></div>
          </div>
          <p className="mt-4 text-gray-500">Scraping flights and generating predictions...</p>
        </div>
      )}

      {/* Search Results */}
      {results && results.flights && results.flights.length > 0 && (
        <div className="space-y-4">
          {/* Summary Cards */}
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-4 rounded-lg border border-blue-200">
              <p className="text-xs text-blue-700 font-medium mb-1">Flights Found</p>
              <p className="text-3xl font-bold text-blue-600">{results.flights.length}</p>
            </div>

            {results.cheapest && (
              <div className="bg-gradient-to-br from-green-50 to-green-100 p-4 rounded-lg border border-green-200">
                <p className="text-xs text-green-700 font-medium mb-1">Cheapest Flight</p>
                <p className="text-2xl font-bold text-green-600">
                  ₹{results.cheapest.price?.toLocaleString('en-IN')}
                </p>
                <p className="text-xs text-green-600">{results.cheapest.airline}</p>
              </div>
            )}
          </div>

          {/* Overall Recommendation */}
          {results.recommendation && (
            <div className={`p-4 rounded-lg border-2 ${
              results.recommendation.action === 'book_now'
                ? 'bg-green-50 border-green-300'
                : 'bg-yellow-50 border-yellow-300'
            }`}>
              <div className="flex items-center">
                <span className="text-2xl mr-3">
                  {results.recommendation.action === 'book_now' ? '✅' : '⏳'}
                </span>
                <div>
                  <p className={`font-semibold ${
                    results.recommendation.action === 'book_now' 
                      ? 'text-green-700' 
                      : 'text-yellow-700'
                  }`}>
                    {results.recommendation.message}
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Flight Cards */}
          <div className="space-y-3">
            {results.flights.slice(0, 10).map((flight, index) => {
              const mlPred = flight.ml_prediction;
              const isGoodDeal = mlPred?.is_good_deal;
              const savings = mlPred?.savings || 0;

              return (
                <div
                  key={index}
                  className={`p-5 rounded-lg border-2 transition-all hover:shadow-lg ${
                    isGoodDeal 
                      ? 'bg-green-50 border-green-300' 
                      : 'bg-white border-gray-200'
                  }`}
                >
                  {/* Flight Header */}
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center space-x-3">
                      <div className="bg-blue-100 p-2 rounded-lg">
                        <span className="text-xl">✈️</span>
                      </div>
                      <div>
                        <p className="font-bold text-gray-800 text-lg">
                          {flight.airline || 'Unknown Airline'}
                        </p>
                        <p className="text-sm text-gray-500">
                          {flight.flight_number || 'N/A'}
                        </p>
                      </div>
                    </div>

                    {/* Good Deal Badge */}
                    {isGoodDeal && (
                      <div className="bg-green-500 text-white px-3 py-1 rounded-full text-xs font-bold">
                        ✨ GREAT DEAL!
                      </div>
                    )}
                  </div>

                  {/* Flight Details */}
                  <div className="grid grid-cols-3 gap-4 mb-3">
                    <div>
                      <p className="text-xs text-gray-500">Departure</p>
                      <p className="text-lg font-semibold text-gray-800">
                        {flight.departure_time || 'N/A'}
                      </p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-500">Arrival</p>
                      <p className="text-lg font-semibold text-gray-800">
                        {flight.arrival_time || 'N/A'}
                      </p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-500">Duration</p>
                      <p className="text-lg font-semibold text-gray-800">
                        {flight.duration || 'N/A'}
                      </p>
                    </div>
                  </div>

                  {/* Price & ML Prediction */}
                  <div className="flex items-center justify-between pt-3 border-t border-gray-200">
                    <div>
                      <p className="text-xs text-gray-500 mb-1">Current Price</p>
                      <p className="text-3xl font-bold text-blue-600">
                        ₹{flight.price?.toLocaleString('en-IN') || 'N/A'}
                      </p>
                    </div>

                    {mlPred && (
                      <div className="text-right">
                        <p className="text-xs text-gray-500 mb-1">ML Predicted</p>
                        <p className="text-lg font-semibold text-purple-600">
                          ₹{mlPred.predicted_price?.toLocaleString('en-IN')}
                        </p>
                        {savings > 0 && (
                          <p className="text-xs text-green-600 font-semibold mt-1">
                            💰 Save ₹{savings.toLocaleString('en-IN')}
                          </p>
                        )}
                        {savings < 0 && (
                          <p className="text-xs text-orange-600 font-semibold mt-1">
                            ⚠️ ₹{Math.abs(savings).toLocaleString('en-IN')} above predicted
                          </p>
                        )}
                      </div>
                    )}
                  </div>

                  {/* Action Button */}
                  <button className={`w-full mt-4 py-2 px-4 rounded-lg font-semibold transition-all ${
                    isGoodDeal
                      ? 'bg-green-500 text-white hover:bg-green-600'
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}>
                    {isGoodDeal ? '🎫 Book Now' : '📋 View Details'}
                  </button>
                </div>
              );
            })}
          </div>

          {/* Show More */}
          {results.flights.length > 10 && (
            <div className="text-center">
              <p className="text-gray-500 text-sm">
                Showing 10 of {results.flights.length} flights
              </p>
            </div>
          )}
        </div>
      )}

      {/* No Results */}
      {results && results.flights && results.flights.length === 0 && (
        <div className="text-center py-12 text-gray-400">
          <p className="text-lg">No flights found for this route</p>
          <p className="text-sm mt-2">Try a different route or date</p>
        </div>
      )}

      {/* Initial State */}
      {!results && !loading && !error && (
        <div className="text-center py-12 text-gray-400">
          <span className="text-6xl mb-4 block">🛫</span>
          <p className="text-lg">Search for flights to see ML-powered price predictions</p>
          <p className="text-sm mt-2">We'll scrape live data and predict best deals</p>
        </div>
      )}
    </div>
  );
};

export default FlightSearchML;
