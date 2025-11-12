const express = require('express');
const router = express.Router();
const { generateInsight, getLatest } = require('../controllers/insightController');

router.post('/generate', generateInsight);
router.get('/latest', getLatest);

module.exports = router;
