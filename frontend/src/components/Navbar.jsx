import React, { useState } from 'react';

const Navbar = ({ activeSection, onNavigate }) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navItems = [
    { id: 'predictor', label: '🔮 Price Predictor', icon: '💰' },
    { id: 'forecast', label: '📈 30-Day Forecast', icon: '📊' },
    { id: 'recommendation', label: '🎯 Book or Wait', icon: '✅' },
    { id: 'search', label: '🔍 Flight Search', icon: '✈️' },
    { id: 'analytics', label: '📊 Analytics', icon: '📈' },
  ];

  return (
    <nav className="bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 shadow-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo/Brand */}
          <div className="flex items-center space-x-3">
            <div className="bg-white rounded-lg p-2 shadow-md">
              <span className="text-2xl">✈️</span>
            </div>
            <div className="hidden md:block">
              <h1 className="text-white font-bold text-xl">AI Flight Fare Predictor</h1>
              <p className="text-blue-100 text-xs">95.8% Accuracy • 945 Flights Analyzed</p>
            </div>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-1">
            {navItems.map((item) => (
              <button
                key={item.id}
                onClick={() => onNavigate(item.id)}
                className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
                  activeSection === item.id
                    ? 'bg-white text-purple-600 shadow-lg transform scale-105'
                    : 'text-white hover:bg-white/20 hover:shadow-md'
                }`}
              >
                <span className="mr-2">{item.icon}</span>
                <span className="hidden lg:inline">{item.label.split(' ').slice(1).join(' ')}</span>
              </button>
            ))}
          </div>

          {/* ML Status Indicator */}
          <div className="hidden md:flex items-center space-x-2 bg-white/10 px-3 py-1 rounded-full">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
            <span className="text-white text-sm font-medium">ML Active</span>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden text-white p-2 rounded-lg hover:bg-white/20"
          >
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              {mobileMenuOpen ? (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              ) : (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16M4 18h16"
                />
              )}
            </svg>
          </button>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden pb-4 space-y-2 animate-fadeIn">
            {navItems.map((item) => (
              <button
                key={item.id}
                onClick={() => {
                  onNavigate(item.id);
                  setMobileMenuOpen(false);
                }}
                className={`w-full text-left px-4 py-3 rounded-lg font-medium transition-all ${
                  activeSection === item.id
                    ? 'bg-white text-purple-600 shadow-md'
                    : 'text-white hover:bg-white/20'
                }`}
              >
                <span className="mr-2">{item.icon}</span>
                {item.label}
              </button>
            ))}
            <div className="flex items-center justify-center space-x-2 bg-white/10 px-3 py-2 rounded-lg mt-4">
              <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
              <span className="text-white text-sm font-medium">ML Service Active</span>
            </div>
          </div>
        )}
      </div>

      {/* Bottom border gradient */}
      <div className="h-1 bg-gradient-to-r from-pink-500 via-purple-500 to-indigo-500"></div>
    </nav>
  );
};

export default Navbar;
