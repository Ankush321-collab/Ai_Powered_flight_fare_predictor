const axios = require('axios');
const { spawn } = require('child_process');
const path = require('path');

const ML_SERVICE_URL = process.env.ML_SERVICE_URL || 'http://localhost:5001';

// Health check for ML service
exports.healthCheck = async (req, res) => {
  try {
    const response = await axios.get(`${ML_SERVICE_URL}/health`);
    res.json({
      status: 'success',
      ml_service: response.data
    });
  } catch (error) {
    res.status(500).json({
      status: 'error',
      message: 'ML service not available',
      error: error.message
    });
  }
};

// Predict single flight price
exports.predictPrice = async (req, res) => {
  try {
    const { airline, origin, destination, days_until_flight, stops, departure_hour } = req.body;
    
    // Validate input
    if (!airline || !origin || !destination || days_until_flight === undefined) {
      return res.status(400).json({
        status: 'error',
        message: 'Missing required fields: airline, origin, destination, days_until_flight'
      });
    }
    
    // Call ML service
    const response = await axios.post(`${ML_SERVICE_URL}/predict`, {
      airline,
      origin,
      destination,
      days_until_flight,
      stops: stops || 0,
      departure_hour: departure_hour || 12
    });
    
    res.json({
      status: 'success',
      data: response.data
    });
  } catch (error) {
    res.status(500).json({
      status: 'error',
      message: 'Price prediction failed',
      error: error.response?.data || error.message
    });
  }
};

// Predict prices for multiple dates
exports.predictMultipleDates = async (req, res) => {
  try {
    const { airline, origin, destination, days_ahead } = req.body;
    
    if (!airline || !origin || !destination) {
      return res.status(400).json({
        status: 'error',
        message: 'Missing required fields: airline, origin, destination'
      });
    }
    
    const response = await axios.post(`${ML_SERVICE_URL}/predict/multiple`, {
      airline,
      origin,
      destination,
      days_ahead: days_ahead || 30,
      stops: req.body.stops || 0,
      departure_hour: req.body.departure_hour || 12
    });
    
    res.json({
      status: 'success',
      data: response.data
    });
  } catch (error) {
    res.status(500).json({
      status: 'error',
      message: 'Multiple dates prediction failed',
      error: error.response?.data || error.message
    });
  }
};

// Get booking recommendation
exports.getRecommendation = async (req, res) => {
  try {
    const { current_price, airline, origin, destination } = req.body;
    
    if (!current_price || !airline || !origin || !destination) {
      return res.status(400).json({
        status: 'error',
        message: 'Missing required fields: current_price, airline, origin, destination'
      });
    }
    
    const response = await axios.post(`${ML_SERVICE_URL}/recommend`, {
      current_price,
      airline,
      origin,
      destination,
      stops: req.body.stops || 0,
      departure_hour: req.body.departure_hour || 12
    });
    
    res.json({
      status: 'success',
      data: response.data
    });
  } catch (error) {
    res.status(500).json({
      status: 'error',
      message: 'Recommendation failed',
      error: error.response?.data || error.message
    });
  }
};

// Search flights with ML predictions
exports.searchWithPredictions = async (req, res) => {
  try {
    const { origin, destination, date } = req.body;
    
    if (!origin || !destination || !date) {
      return res.status(400).json({
        status: 'error',
        message: 'Missing required fields: origin, destination, date'
      });
    }
    
    // Run Python scraper
    const pythonPath = 'python'; // or 'python3' or full path
    const scraperPath = path.join(__dirname, '../../scraper_nlp/save_to_mongo.py');
    
    const pythonProcess = spawn(pythonPath, [
      scraperPath,
      '--from', origin,
      '--to', destination,
      '--date', date,
      '--headless'
    ]);
    
    let scriptOutput = '';
    let scriptError = '';
    
    pythonProcess.stdout.on('data', (data) => {
      scriptOutput += data.toString();
      console.log(`Scraper output: ${data}`);
    });
    
    pythonProcess.stderr.on('data', (data) => {
      scriptError += data.toString();
      console.error(`Scraper error: ${data}`);
    });
    
    pythonProcess.on('close', async (code) => {
      if (code !== 0) {
        return res.status(500).json({
          status: 'error',
          message: 'Scraping failed',
          error: scriptError
        });
      }
      
      // After scraping, get flights from DB and add ML predictions
      try {
        const Flight = require('../models/Flight');
        const flights = await Flight.find({ origin, destination })
          .sort({ price: 1 })
          .limit(20);
        
        // Add ML predictions to each flight
        const flightsWithPredictions = await Promise.all(
          flights.map(async (flight) => {
            try {
              const predictionResponse = await axios.post(`${ML_SERVICE_URL}/predict`, {
                airline: flight.airline,
                origin: flight.origin,
                destination: flight.destination,
                days_until_flight: 7,
                stops: flight.stops || 0,
                departure_hour: parseInt(flight.departure_time?.split(':')[0]) || 12
              });
              
              return {
                ...flight.toObject(),
                ml_prediction: predictionResponse.data
              };
            } catch (mlError) {
              console.error('ML prediction failed for flight:', mlError.message);
              return flight.toObject();
            }
          })
        );
        
        // Get recommendation for cheapest flight
        const cheapest = flightsWithPredictions[0];
        let recommendation = null;
        
        if (cheapest) {
          try {
            const recResponse = await axios.post(`${ML_SERVICE_URL}/recommend`, {
              current_price: cheapest.price,
              airline: cheapest.airline,
              origin: cheapest.origin,
              destination: cheapest.destination,
              stops: cheapest.stops || 0,
              departure_hour: parseInt(cheapest.departure_time?.split(':')[0]) || 12
            });
            recommendation = recResponse.data;
          } catch (recError) {
            console.error('Recommendation failed:', recError.message);
          }
        }
        
        res.json({
          status: 'success',
          data: {
            flights: flightsWithPredictions,
            total: flightsWithPredictions.length,
            cheapest,
            recommendation
          }
        });
      } catch (dbError) {
        res.status(500).json({
          status: 'error',
          message: 'Database query failed',
          error: dbError.message
        });
      }
    });
    
  } catch (error) {
    res.status(500).json({
      status: 'error',
      message: 'Search failed',
      error: error.message
    });
  }
};
