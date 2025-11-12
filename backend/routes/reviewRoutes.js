const express = require('express');
const router = express.Router();
const { getReviews, getSentimentStats } = require('../controllers/reviewController');

router.get('/', getReviews);
router.get('/sentiment/:airline', getSentimentStats);

module.exports = router;
