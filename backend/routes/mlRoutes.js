const express = require('express');
const router = express.Router();
const mlController = require('../controllers/mlController');

// Health check
router.get('/health', mlController.healthCheck);

// Predict single price
router.post('/predict', mlController.predictPrice);

// Predict multiple dates
router.post('/predict/multiple', mlController.predictMultipleDates);

// Get booking recommendation
router.post('/recommend', mlController.getRecommendation);

// Search flights with ML predictions
router.post('/search-with-predictions', mlController.searchWithPredictions);

module.exports = router;
