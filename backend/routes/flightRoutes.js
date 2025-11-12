const express = require('express');
const router = express.Router();
const { getFlights, getTrends } = require('../controllers/flightController');

router.get('/', getFlights);
router.get('/trends', getTrends);

module.exports = router;
