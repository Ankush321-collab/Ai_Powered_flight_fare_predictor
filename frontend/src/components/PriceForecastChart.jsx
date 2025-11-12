import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine } from 'recharts';
import mlService from '../api/mlService';

const PriceForecastChart = () => {
  const [formData, setFormData] = useState({
    airline: 'IndiGo',
    origin: 'Delhi',
    destination: 'Mumbai',
    days_ahead: 30
  });

  const [forecastData, setForecastData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const airlines = ['IndiGo', 'SpiceJet', 'Air India', 'Akasa Air', 'Air India Express'];
  const cities = ['Delhi', 'Mumbai', 'Bengaluru', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad', 'Jaipur', 'Goa'];

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'days_ahead' ? parseInt(value) : value
    }));
  };

  const handleGetForecast = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const result = await mlService.getPriceForecast(formData);
      setForecastData(result.data);
    } catch (err) {
      setError('Failed to get forecast. Please ensure backend services are running.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Format chart data
  const chartData = forecastData?.predictions?.map(pred => ({
    day: `Day ${pred.days_ahead}`,
    price: Math.round(pred.predicted_price),
    days_ahead: pred.days_ahead
  })) || [];

  const cheapest = forecastData?.cheapest;
  const avgPrice = chartData.length > 0 
    ? Math.round(chartData.reduce((sum, item) => sum + item.price, 0) / chartData.length)
    : 0;

  // Custom tooltip
  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      const isCheapest = data.days_ahead === cheapest?.days_ahead;
      
      return (
        <div className="bg-white p-3 rounded-lg shadow-lg border border-gray-200">
          <p className="font-semibold text-gray-800">{data.day}</p>
          <p className="text-lg font-bold text-blue-600">₹{data.price.toLocaleString('en-IN')}</p>
          {isCheapest && (
            <p className="text-xs text-green-600 font-semibold mt-1">✨ Cheapest Day!</p>
          )}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="flex items-center mb-6">
        <span className="text-3xl mr-3">📊</span>
        <h2 className="text-2xl font-bold text-gray-800">30-Day Price Forecast</h2>
      </div>

      {/* Form */}
      <form onSubmit={handleGetForecast} className="space-y-4 mb-6">
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

        <div className="bg-gradient-to-r from-teal-50 to-cyan-50 p-5 rounded-xl border-2 border-teal-200">
          <div className="flex items-center justify-between mb-3">
            <label className="text-lg font-semibold text-gray-800 flex items-center">
              📅 Forecast Period
            </label>
            <div className="bg-teal-600 text-white px-4 py-2 rounded-lg font-bold text-lg">
              {formData.days_ahead} days
            </div>
          </div>
          <div className="relative pt-2 pb-1">
            <input
              type="range"
              name="days_ahead"
              min="7"
              max="30"
              value={formData.days_ahead}
              onChange={handleInputChange}
              className="w-full h-3 bg-gradient-to-r from-green-200 via-teal-200 to-cyan-300 rounded-full appearance-none cursor-pointer slider-thumb"
            />
            {/* Visual markers */}
            <div className="flex justify-between mt-3 px-1">
              <div className="text-center">
                <div className="w-2 h-2 bg-green-500 rounded-full mx-auto mb-1"></div>
                <span className="text-xs font-medium text-gray-700">1 Week</span>
                <div className="text-[10px] text-gray-500">7 days</div>
              </div>
              <div className="text-center">
                <div className="w-2 h-2 bg-teal-500 rounded-full mx-auto mb-1"></div>
                <span className="text-xs font-medium text-gray-700">2 Weeks</span>
                <div className="text-[10px] text-gray-500">14 days</div>
              </div>
              <div className="text-center">
                <div className="w-2 h-2 bg-cyan-500 rounded-full mx-auto mb-1"></div>
                <span className="text-xs font-medium text-gray-700">3 Weeks</span>
                <div className="text-[10px] text-gray-500">21 days</div>
              </div>
              <div className="text-center">
                <div className="w-2 h-2 bg-blue-600 rounded-full mx-auto mb-1"></div>
                <span className="text-xs font-medium text-gray-700">1 Month</span>
                <div className="text-[10px] text-gray-500">30 days</div>
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
              : 'bg-gradient-to-r from-green-500 to-teal-600 hover:from-green-600 hover:to-teal-700 shadow-lg'
          }`}
        >
          {loading ? 'Loading...' : '📈 Get Forecast'}
        </button>
      </form>

      {/* Error Message */}
      {error && (
        <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-600 text-sm">{error}</p>
        </div>
      )}

      {/* Chart */}
      {forecastData && chartData.length > 0 && (
        <div className="space-y-4">
          {/* Stats Cards */}
          <div className="grid grid-cols-3 gap-4">
            <div className="bg-gradient-to-br from-green-50 to-green-100 p-4 rounded-lg border border-green-200">
              <p className="text-xs text-green-700 font-medium mb-1">Cheapest Day</p>
              <p className="text-2xl font-bold text-green-600">
                Day {cheapest?.days_ahead}
              </p>
              <p className="text-lg font-semibold text-green-700">
                ₹{cheapest?.predicted_price?.toLocaleString('en-IN')}
              </p>
            </div>

            <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-4 rounded-lg border border-blue-200">
              <p className="text-xs text-blue-700 font-medium mb-1">Average Price</p>
              <p className="text-2xl font-bold text-blue-600">₹{avgPrice.toLocaleString('en-IN')}</p>
            </div>

            <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-4 rounded-lg border border-purple-200">
              <p className="text-xs text-purple-700 font-medium mb-1">Price Range</p>
              <p className="text-sm font-semibold text-purple-700">
                ₹{Math.min(...chartData.map(d => d.price)).toLocaleString('en-IN')} - 
                ₹{Math.max(...chartData.map(d => d.price)).toLocaleString('en-IN')}
              </p>
            </div>
          </div>

          {/* Chart */}
          <div className="bg-gray-50 p-4 rounded-lg">
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={chartData} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis 
                  dataKey="day" 
                  tick={{ fontSize: 12 }}
                  interval={Math.floor(chartData.length / 6)}
                />
                <YAxis 
                  tick={{ fontSize: 12 }}
                  tickFormatter={(value) => `₹${(value / 1000).toFixed(0)}k`}
                />
                <Tooltip content={<CustomTooltip />} />
                <Legend />
                
                {/* Average price line */}
                <ReferenceLine 
                  y={avgPrice} 
                  stroke="#9ca3af" 
                  strokeDasharray="5 5"
                  label={{ value: 'Avg', position: 'right', fontSize: 12 }}
                />
                
                {/* Price line */}
                <Line 
                  type="monotone" 
                  dataKey="price" 
                  stroke="#3b82f6" 
                  strokeWidth={3}
                  dot={(props) => {
                    const { cx, cy, payload } = props;
                    const isCheapest = payload.days_ahead === cheapest?.days_ahead;
                    return (
                      <circle
                        cx={cx}
                        cy={cy}
                        r={isCheapest ? 8 : 4}
                        fill={isCheapest ? '#10b981' : '#3b82f6'}
                        stroke={isCheapest ? '#065f46' : '#1e40af'}
                        strokeWidth={2}
                      />
                    );
                  }}
                  activeDot={{ r: 6 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Recommendation */}
          <div className="bg-gradient-to-r from-green-50 to-teal-50 p-4 rounded-lg border-2 border-green-200">
            <div className="flex items-center">
              <span className="text-2xl mr-3">💡</span>
              <div>
                <p className="font-semibold text-green-800">Best Time to Fly</p>
                <p className="text-sm text-green-700">
                  Day {cheapest?.days_ahead} has the lowest predicted price at ₹{cheapest?.predicted_price?.toLocaleString('en-IN')}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* No data message */}
      {!forecastData && !loading && !error && (
        <div className="text-center py-12 text-gray-400">
          <p className="text-lg">Select route and click "Get Forecast" to see price predictions</p>
        </div>
      )}
    </div>
  );
};

export default PriceForecastChart;
