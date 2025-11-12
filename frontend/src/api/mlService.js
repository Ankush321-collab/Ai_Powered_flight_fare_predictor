import axios from 'axios';

const ML_API = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:4000/api/ml'
});

// ML Service for flight price predictions
const mlService = {
  // Check ML service health
  checkHealth: async () => {
    try {
      const response = await ML_API.get('/health');
      return response.data;
    } catch (error) {
      console.error('ML Health check failed:', error);
      throw error;
    }
  },

  // Predict single flight price
  predictPrice: async (flightData) => {
    try {
      const response = await ML_API.post('/predict', {
        airline: flightData.airline,
        origin: flightData.origin,
        destination: flightData.destination,
        days_until_flight: flightData.days_until_flight || 7,
        stops: flightData.stops || 0,
        departure_hour: flightData.departure_hour || 10
      });
      return response.data;
    } catch (error) {
      console.error('Price prediction failed:', error);
      throw error;
    }
  },

  // Get 30-day price forecast
  getPriceForecast: async (routeData) => {
    try {
      const response = await ML_API.post('/predict/multiple', {
        airline: routeData.airline,
        origin: routeData.origin,
        destination: routeData.destination,
        days_ahead: routeData.days_ahead || 30
      });
      return response.data;
    } catch (error) {
      console.error('Price forecast failed:', error);
      throw error;
    }
  },

  // Get booking recommendation
  getBookingRecommendation: async (priceData) => {
    try {
      const response = await ML_API.post('/recommend', {
        current_price: priceData.current_price,
        airline: priceData.airline,
        origin: priceData.origin,
        destination: priceData.destination,
        days_until_flight: priceData.days_until_flight || 7
      });
      return response.data;
    } catch (error) {
      console.error('Booking recommendation failed:', error);
      throw error;
    }
  },

  // Search flights with ML predictions
  searchWithPredictions: async (searchData) => {
    try {
      const response = await ML_API.post('/search-with-predictions', {
        origin: searchData.origin,
        destination: searchData.destination,
        date: searchData.date
      });
      return response.data;
    } catch (error) {
      console.error('Search with predictions failed:', error);
      throw error;
    }
  }
};

export default mlService;
