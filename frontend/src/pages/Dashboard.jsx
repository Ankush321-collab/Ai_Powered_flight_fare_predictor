import React, { useEffect, useState } from 'react'
import AISummaryCard from '../components/AISummaryCard'
import FlightTrendsChart from '../components/FlightTrendsChart'
import SentimentChart from '../components/SentimentChart'
import PricePredictor from '../components/PricePredictor'
import PriceForecastChart from '../components/PriceForecastChart'
import BookingRecommendation from '../components/BookingRecommendation'
import FlightSearchML from '../components/FlightSearchML'
import Navbar from '../components/Navbar'

export default function Dashboard(){
  const [activeSection, setActiveSection] = useState('predictor');

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      {/* Navbar */}
      <Navbar activeSection={activeSection} onNavigate={setActiveSection} />

      {/* Content */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Price Predictor Section */}
        {activeSection === 'predictor' && (
          <div className="animate-fadeIn">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">� Flight Price Predictor</h2>
            <PricePredictor />
          </div>
        )}

        {/* 30-Day Forecast Section */}
        {activeSection === 'forecast' && (
          <div className="animate-fadeIn">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">📈 30-Day Price Forecast</h2>
            <PriceForecastChart />
          </div>
        )}

        {/* Booking Recommendation Section */}
        {activeSection === 'recommendation' && (
          <div className="animate-fadeIn">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">🎯 Booking Recommendation</h2>
            <BookingRecommendation />
          </div>
        )}

        {/* Flight Search Section */}
        {activeSection === 'search' && (
          <div className="animate-fadeIn">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">🔍 Flight Search with ML Predictions</h2>
            <FlightSearchML />
          </div>
        )}

        {/* Analytics Section */}
        {activeSection === 'analytics' && (
          <div className="space-y-6 animate-fadeIn">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">📊 Analytics & Trends</h2>
            
            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
              <div className="bg-gradient-to-br from-blue-500 to-blue-600 text-white p-6 rounded-lg shadow-lg">
                <p className="text-sm opacity-90">ML Model Accuracy</p>
                <p className="text-4xl font-bold mt-2">95.8%</p>
                <p className="text-xs mt-1 opacity-75">Random Forest</p>
              </div>

              <div className="bg-gradient-to-br from-green-500 to-green-600 text-white p-6 rounded-lg shadow-lg">
                <p className="text-sm opacity-90">Flights Analyzed</p>
                <p className="text-4xl font-bold mt-2">945</p>
                <p className="text-xs mt-1 opacity-75">12 Routes</p>
              </div>

              <div className="bg-gradient-to-br from-purple-500 to-purple-600 text-white p-6 rounded-lg shadow-lg">
                <p className="text-sm opacity-90">Avg. Error</p>
                <p className="text-4xl font-bold mt-2">₹636</p>
                <p className="text-xs mt-1 opacity-75">MAE Score</p>
              </div>

              <div className="bg-gradient-to-br from-orange-500 to-orange-600 text-white p-6 rounded-lg shadow-lg">
                <p className="text-sm opacity-90">Predictions Made</p>
                <p className="text-4xl font-bold mt-2">1.2K+</p>
                <p className="text-xs mt-1 opacity-75">Last 30 days</p>
              </div>
            </div>

            {/* Charts Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Flight Trends Chart */}
              <div className="lg:col-span-2 bg-white p-6 rounded-lg shadow-lg">
                <FlightTrendsChart />
              </div>

              {/* AI Summary & Sentiment */}
              <div className="space-y-6">
                <div className="bg-white p-6 rounded-lg shadow-lg">
                  <AISummaryCard />
                </div>
                <div className="bg-white p-6 rounded-lg shadow-lg">
                  <SentimentChart />
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="max-w-7xl mx-auto px-6 py-4 mt-12">
        <div className="bg-white rounded-lg shadow-sm p-4 text-center text-sm text-gray-600">
          <p>
            Powered by Enhanced Random Forest Model • 27 Features • Updated: {new Date().toLocaleDateString()}
          </p>
        </div>
      </div>
    </div>
  )
}
